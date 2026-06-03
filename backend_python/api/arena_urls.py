"""URL patterns for the AI4Bharat Arena chat proxy.

Mounted under /api/neby-arena/ by api/urls.py.
"""
from django.urls import path
from . import arena_views

urlpatterns = [
    path('models/', arena_views.arena_models, name='arena-models'),
    path('pool-stats/', arena_views.arena_pool_stats, name='arena-pool-stats'),
    path('sessions/', arena_views.arena_sessions, name='arena-sessions'),
    path('sessions/<str:session_id>/', arena_views.arena_session_detail, name='arena-session-detail'),
    path('sessions/<str:session_id>/messages/', arena_views.arena_send_message, name='arena-send-message'),
    path('messages/<str:message_id>/regenerate/', arena_views.arena_regenerate, name='arena-regenerate'),
]
