"""
Публичные эндпоинты по токену документа: инфо, файл, решение.
"""
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import BitrixDocument


def get_document_by_token(token):
    """Возвращает документ по токену или None."""
    if not token:
        return None
    try:
        return BitrixDocument.objects.get(token=token)
    except BitrixDocument.DoesNotExist:
        return None


@extend_schema(
    summary='Информация о документе по токену',
    description='Для страницы sign/{token}. При невалидном токене — 404.',
    responses={
        200: {
            'description': 'Document info',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'deal_id': {'type': 'string'},
                            'doc_id': {'type': 'string'},
                            'sign_url': {'type': 'string', 'format': 'uri'},
                            'status': {'type': 'string', 'enum': ['awaiting_decision', 'accepted', 'rejected']},
                            'full_name': {'type': 'string', 'nullable': True},
                            'iin': {'type': 'string', 'nullable': True},
                        },
                    },
                },
            },
        },
        404: {'description': 'Invalid token'},
    },
)
@api_view(['GET'])
def document_by_token(request, token):
    """GET /api/public/documents/<token>/ — инфо о документе."""
    doc = get_document_by_token(token)
    if doc is None:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    sign_url = f"{settings.FRONTEND_URL}/sign/{doc.token}"
    return Response({
        'deal_id': doc.deal_id,
        'doc_id': doc.doc_id,
        'sign_url': sign_url,
        'status': doc.status,
        'full_name': doc.full_name or None,
        'iin': doc.iin or None,
    })


@extend_schema(
    summary='Скачать PDF по токену',
    description='Возвращает PDF-файл. При невалидном токене — 404.',
    responses={
        200: {'content': {'application/pdf': {'schema': {'type': 'string', 'format': 'binary'}}}},
        404: {'description': 'Invalid token'},
    },
)
@api_view(['GET'])
def document_file(request, token):
    """GET /api/public/documents/<token>/file/ — отдать PDF."""
    doc = get_document_by_token(token)
    if doc is None or not doc.file:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        with doc.file.open('rb') as fh:
            content = fh.read()
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="document.pdf"'
        response['X-Frame-Options'] = 'SAMEORIGIN'  # allow embedding in iframe on same origin
        return response
    except Exception:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary='Отправить решение по документу',
    description='decision: "accepted" | "rejected". Если документ уже обработан — 409 Conflict.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {'decision': {'type': 'string', 'enum': ['accepted', 'rejected']}},
            'required': ['decision'],
        },
    },
    responses={
        200: {
            'description': 'Decision saved',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {'status': {'type': 'string', 'enum': ['accepted', 'rejected']}},
                    },
                },
            },
        },
        404: {'description': 'Invalid token'},
        409: {'description': 'Document already processed'},
    },
)
@api_view(['POST'])
def document_decision(request, token):
    """POST /api/public/documents/<token>/decision/ — принять/отклонить."""
    doc = get_document_by_token(token)
    if doc is None:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    if doc.status != BitrixDocument.STATUS_AWAITING:
        return Response(
            {'error': 'Document already processed', 'status': doc.status},
            status=status.HTTP_409_CONFLICT,
        )

    decision = (request.data.get('decision') or '').strip().lower()
    if decision not in ('accepted', 'rejected'):
        return Response(
            {'error': 'decision must be "accepted" or "rejected"'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    doc.status = BitrixDocument.STATUS_ACCEPTED if decision == 'accepted' else BitrixDocument.STATUS_REJECTED
    doc.save(update_fields=['status'])

    return Response({'status': doc.status}, status=status.HTTP_200_OK)
