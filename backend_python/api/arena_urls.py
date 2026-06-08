"""URL patterns for the AI4Bharat Arena chat proxy and Qwen file-upload chat.

Mounted under /api/neby-arena/ by api/urls.py.
"""
from django.urls import path
from . import arena_views
from . import arena_qwen_views

urlpatterns = [
    # AI4Bharat Arena (text-only, anonymous token pool)
    path('models/', arena_views.arena_models, name='arena-models'),
    path('pool-stats/', arena_views.arena_pool_stats, name='arena-pool-stats'),
    path('sessions/', arena_views.arena_sessions, name='arena-sessions'),
    path('sessions/<str:session_id>/', arena_views.arena_session_detail, name='arena-session-detail'),
    path('sessions/<str:session_id>/messages/', arena_views.arena_send_message, name='arena-send-message'),
    path('messages/<str:message_id>/regenerate/', arena_views.arena_regenerate, name='arena-regenerate'),

    # Qwen provider (file upload support — images, PDFs, audio, video)
    path('qwen/models/', arena_qwen_views.arena_qwen_models, name='arena-qwen-models'),
    path('qwen/sessions/', arena_qwen_views.arena_create_qwen_session, name='arena-qwen-create-session'),
    path('qwen/sessions/<str:session_id>/messages/', arena_qwen_views.arena_send_message_qwen, name='arena-qwen-send-message'),
    path('qwen/sessions/<str:session_id>/messages/sse/', arena_qwen_views.arena_send_message_qwen_sse, name='arena-qwen-send-message-sse'),
]
