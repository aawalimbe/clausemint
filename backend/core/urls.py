from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/documents/', include('documents.urls')),
    path('api/nda/', include('nda_generator.urls')),
    path('api/redlining/', include('redlining.urls')),
    path('', include('documents.urls')),  # Main app handles frontend
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 