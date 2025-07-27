from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_document, name='analyze_document'),
    path('analyze-clause/', views.analyze_single_clause, name='analyze_single_clause'),
] 