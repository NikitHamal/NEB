"""URL patterns for the community chat proxies, Qwen file-upload chat, DeepAI, EQing, FreeGPT, DeepSeek AI, and SurfSense.

Mounted under /api/neby-arena/ by api/urls.py.
"""
from django.urls import path
from . import arena_views
from . import arena_agent_views
from . import arena_qwen_views
from . import arena_deepai_views
from .arena_simple_providers import simple_provider_urlpatterns

urlpatterns = [
    # Community chat (K2 Horizon / Poolside / Motiftech — stateless proxies)
    path('models/', arena_views.arena_models, name='arena-models'),
    path('sessions/', arena_views.arena_sessions, name='arena-sessions'),
    path('sessions/<str:session_id>/', arena_views.arena_session_detail, name='arena-session-detail'),
    path('sessions/<str:session_id>/messages/', arena_views.arena_send_message, name='arena-send-message'),
    path('messages/<str:message_id>/regenerate/', arena_views.arena_regenerate, name='arena-regenerate'),

    # Stateless single-shot chat for LLM clients (no session rows kept)
    path('agent/', arena_agent_views.arena_agent_chat, name='arena-agent-chat'),

    # Qwen provider (file upload support — images, PDFs, audio, video)
    path('qwen/models/', arena_qwen_views.arena_qwen_models, name='arena-qwen-models'),
    path('qwen/sessions/', arena_qwen_views.arena_create_qwen_session, name='arena-qwen-create-session'),
    path('qwen/sessions/<str:session_id>/messages/', arena_qwen_views.arena_send_message_qwen, name='arena-qwen-send-message'),
    path('qwen/sessions/<str:session_id>/messages/sse/', arena_qwen_views.arena_send_message_qwen_sse, name='arena-qwen-send-message-sse'),

    # DeepAI (multi-model chat, file upload support — images, documents)
    path('deepai/models/', arena_deepai_views.arena_deepai_models, name='arena-deepai-models'),
    path('deepai/sessions/', arena_deepai_views.arena_create_deepai_session, name='arena-deepai-create-session'),
    path('deepai/sessions/<str:session_id>/messages/', arena_deepai_views.arena_send_message_deepai, name='arena-deepai-send-message'),
    path('deepai/sessions/<str:session_id>/messages/sse/', arena_deepai_views.arena_send_message_deepai_sse, name='arena-deepai-send-message-sse'),

    *simple_provider_urlpatterns(),
]
