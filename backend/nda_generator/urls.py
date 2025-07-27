from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_nda, name='generate_nda'),
    path('generate/streaming/', views.generate_nda_streaming_view, name='generate_nda_streaming'),
    path('export/', views.export_nda, name='export_nda'),
    path('download/<str:filename>/', views.download_nda, name='download_nda'),
] 