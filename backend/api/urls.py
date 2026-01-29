from django.urls import path

from . import views
from .bitrix_views import bitrix_document_upload
from .public_views import document_by_token, document_file, document_decision

urlpatterns = [
    path('health/', views.health),
    path('bitrix/documents/', bitrix_document_upload),
    path('public/documents/<str:token>/', document_by_token),
    path('public/documents/<str:token>/file/', document_file),
    path('public/documents/<str:token>/decision/', document_decision),
]
