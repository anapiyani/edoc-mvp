"""
Имитация Bitrix: загрузка документа.
POST /api/bitrix/documents/ — multipart/form-data.
"""
from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import BitrixDocument

MAX_FILE_SIZE = 20 * 1024 * 1024 
PDF_MAGIC = b'%PDF'


def is_pdf_file(uploaded_file):
    """Проверка, что файл — PDF: content-type, расширение и сигнатура %PDF."""
    if uploaded_file.content_type and uploaded_file.content_type.lower() != 'application/pdf':
        return False
    name = (uploaded_file.name or '').lower()
    if not name.endswith('.pdf'):
        return False
    try:
        head = b''
        for chunk in uploaded_file.chunks():
            head += chunk
            if len(head) >= 5:
                break
        if not head.startswith(PDF_MAGIC):
            return False
        uploaded_file.seek(0) 
    except Exception:
        return False
    return True


@extend_schema(
    summary='Загрузка документа (имитация Bitrix)',
    description='Multipart: deal_id, doc_id (required), full_name, iin (optional), file (required, PDF, ≤ 20MB).',
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'deal_id': {'type': 'string', 'description': 'Required'},
                'doc_id': {'type': 'string', 'description': 'Required'},
                'full_name': {'type': 'string', 'description': 'Optional'},
                'iin': {'type': 'string', 'description': 'Optional'},
                'file': {'type': 'string', 'format': 'binary', 'description': 'Required, PDF, max 20MB'},
            },
            'required': ['deal_id', 'doc_id', 'file'],
        }
    },
    responses={
        201: {
            'description': 'Document created',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'deal_id': {'type': 'string'},
                            'doc_id': {'type': 'string'},
                            'sign_url': {'type': 'string', 'format': 'uri'},
                            'status': {'type': 'string', 'enum': ['awaiting_decision', 'accepted', 'rejected']},
                        },
                    },
                },
            },
        },
        400: {'description': 'Validation error'},
        409: {'description': 'Document with this deal_id and doc_id already exists'},
    },
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def bitrix_document_upload(request):
    """
    POST /api/bitrix/documents/
    Поля: deal_id (required), doc_id (required), full_name (optional), iin (optional), file (required, PDF, ≤ 20MB).
    """
    deal_id = (request.data.get('deal_id') or request.POST.get('deal_id') or '').strip()
    doc_id = (request.data.get('doc_id') or request.POST.get('doc_id') or '').strip()
    full_name = (request.data.get('full_name') or request.POST.get('full_name') or '').strip()
    iin = (request.data.get('iin') or request.POST.get('iin') or '').strip()
    uploaded_file = request.FILES.get('file') or request.data.get('file')

    errors = []
    if not deal_id:
        errors.append('deal_id is required.')
    if not doc_id:
        errors.append('doc_id is required.')
    if not uploaded_file:
        errors.append('file is required.')
    else:
        if uploaded_file.size > MAX_FILE_SIZE:
            errors.append('file must be at most 20 MB.')
        elif not is_pdf_file(uploaded_file):
            errors.append('file must be a valid PDF (content-type, .pdf extension, and %PDF signature).')

    if errors:
        return Response(
            {'error': ' '.join(errors)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if BitrixDocument.objects.filter(deal_id=deal_id, doc_id=doc_id).exists():
        return Response(
            {'error': 'A document with this deal_id and doc_id already exists.'},
            status=status.HTTP_409_CONFLICT,
        )

    try:
        doc = BitrixDocument(
            deal_id=deal_id,
            doc_id=doc_id,
            full_name=full_name or '',
            iin=iin or '',
            file=uploaded_file,
        )
        doc.save()
    except IntegrityError:
        return Response(
            {'error': 'A document with this deal_id and doc_id already exists.'},
            status=status.HTTP_409_CONFLICT,
        )
    except OSError as e:
        return Response(
            {'error': f'Failed to save file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        return Response(
            {'error': 'Failed to create document. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    sign_url = f"{settings.FRONTEND_URL}/sign/{doc.token}"

    return Response(
        {
            'deal_id': doc.deal_id,
            'doc_id': doc.doc_id,
            'sign_url': sign_url,
            'status': doc.status,
        },
        # Spec says 200; 201 is also reasonable, but keep it strict.
        status=status.HTTP_200_OK,
    )
