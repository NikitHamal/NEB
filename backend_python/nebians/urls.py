"""
URL configuration for NEBians backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin-django/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('web.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
