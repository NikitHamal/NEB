"""URL patterns for the AI4Bharat Arena chat proxy, Qwen file-upload chat, eGov Chat AI, DeepAI, EQing, FreeGPT, DeepSeek AI, and SurfSense.

Mounted under /api/neby-arena/ by api/urls.py.
"""
from django.urls import path
from . import arena_views
from . import arena_qwen_views
from . import arena_egov_views
from . import arena_deepai_views
from . import arena_inception_views

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

    # eGov Chat AI (Philippine government AI, file upload support — images, PDFs)
    path('egov/models/', arena_egov_views.arena_egov_models, name='arena-egov-models'),
    path('egov/sessions/', arena_egov_views.arena_create_egov_session, name='arena-egov-create-session'),
    path('egov/sessions/<str:session_id>/messages/', arena_egov_views.arena_send_message_egov, name='arena-egov-send-message'),
    path('egov/sessions/<str:session_id>/messages/sse/', arena_egov_views.arena_send_message_egov_sse, name='arena-egov-send-message-sse'),

    # DeepAI (multi-model chat, file upload support — images, documents)
    path('deepai/models/', arena_deepai_views.arena_deepai_models, name='arena-deepai-models'),
    path('deepai/sessions/', arena_deepai_views.arena_create_deepai_session, name='arena-deepai-create-session'),
    path('deepai/sessions/<str:session_id>/messages/', arena_deepai_views.arena_send_message_deepai, name='arena-deepai-send-message'),
    path('deepai/sessions/<str:session_id>/messages/sse/', arena_deepai_views.arena_send_message_deepai_sse, name='arena-deepai-send-message-sse'),

    # Inception Labs (Mercury 2 diffusion LLM — no API key required)
    path('inception/models/', arena_inception_views.arena_inception_models, name='arena-inception-models'),
    path('inception/sessions/', arena_inception_views.arena_create_inception_session, name='arena-inception-create-session'),
    path('inception/sessions/<str:session_id>/messages/', arena_inception_views.arena_send_message_inception, name='arena-inception-send-message'),
]
