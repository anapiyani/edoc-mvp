import secrets

from django.db import models


def generate_document_token():
    return secrets.token_urlsafe(32)


class BitrixDocument(models.Model):
    """Имитация Bitrix: загруженный документ."""

    STATUS_AWAITING = 'awaiting_decision'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_AWAITING, 'awaiting_decision'),
        (STATUS_ACCEPTED, 'accepted'),
        (STATUS_REJECTED, 'rejected'),
    ]

    deal_id = models.CharField(max_length=255, db_index=True)
    doc_id = models.CharField(max_length=255, db_index=True)
    full_name = models.CharField(max_length=255, blank=True)
    iin = models.CharField(max_length=20, blank=True)
    file = models.FileField(upload_to='bitrix_documents/%Y/%m/', max_length=500)
    token = models.CharField(max_length=64, unique=True, default=generate_document_token, editable=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_AWAITING, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bitrix document'
        verbose_name_plural = 'Bitrix documents'

    def __str__(self):
        return f"{self.deal_id}/{self.doc_id} ({self.token[:8]}…)"
