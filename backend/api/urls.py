from django.urls import path

from . import views
from .bitrix_views import bitrix_document_upload

urlpatterns = [
    path('health/', views.health),
    path('bitrix/documents/', bitrix_document_upload),
]
