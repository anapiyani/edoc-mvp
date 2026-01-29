from django.contrib import admin
from .models import BitrixDocument


@admin.register(BitrixDocument)
class BitrixDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'deal_id', 'doc_id', 'status', 'token', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('deal_id', 'doc_id', 'token', 'full_name', 'iin')
    readonly_fields = ('token', 'created_at')
