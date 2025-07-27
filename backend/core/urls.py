from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/documents/', include('documents.urls')),
    path('api/nda/', include('nda_generator.urls')),
    path('api/redlining/', include('redlining.urls')),
    path('api/ai/status/', views.ai_status, name='ai_status'),
    path('api/ai/switch/', views.switch_ai_provider, name='switch_ai_provider'),
    path('api/ai/test/', views.test_ai_connection, name='test_ai_connection'),
    path('api/jurisdictions/', views.jurisdictions, name='jurisdictions'),
    path('api/jurisdictions/<str:jurisdiction_name>/', views.jurisdiction_details, name='jurisdiction_details'),
    path('', include('documents.urls')),  # Main app handles frontend
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 