from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_document, name='analyze_document'),
    path('analyze/streaming/', views.analyze_document_streaming, name='analyze_document_streaming'),
    path('analyze-clause/', views.analyze_single_clause, name='analyze_single_clause'),
] 