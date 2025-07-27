from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload/', views.upload_document, name='upload_document'),
    path('api/documents/', views.get_documents, name='get_documents'),
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/chat/streaming/', views.chat_message_streaming, name='chat_message_streaming'),
    path('api/chat/<int:document_id>/', views.get_chat_history, name='get_chat_history'),
] 