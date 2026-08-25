"""
URL configuration for NEBians backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

handler404 = 'web.views.custom_404'
handler500 = 'web.views.custom_500'

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'web/img/favicon.ico', permanent=True)),
    path('admin-django/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('web.urls')),
    # Old coding agent app removed — replaced by web:background_agent* views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
