from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_nda, name='generate_nda'),
    path('export/', views.export_nda, name='export_nda'),
] 