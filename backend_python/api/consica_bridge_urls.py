"""URL patterns for the Consica AI Bridge.

Mounted under /api/consica-bridge/ by api/urls.py.
The path is intentionally non-obvious to reduce casual discovery.
"""
from django.urls import path
from . import consica_bridge_views

urlpatterns = [
    path('generate/', consica_bridge_views.consica_generate, name='consica-bridge-generate'),
]
