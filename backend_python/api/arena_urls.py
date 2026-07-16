"""URL patterns for the AI4Bharat Arena chat proxy, Qwen file-upload chat, eGov Chat AI, DeepAI, EQing, FreeGPT, DeepSeek AI, and SurfSense.

Mounted under /api/neby-arena/ by api/urls.py.
"""
from django.urls import path
from . import arena_views
from . import arena_qwen_views
from . import arena_egov_views
from . import arena_deepai_views
from . import arena_eqing_views
from . import arena_freegpt_views
from . import arena_deepseekai_views
from . import arena_surfsense_views
from . import arena_g4f_views
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

    # EQing / EasyChat (OpenAI-compatible API with altcha PoW captcha)
    path('eqing/models/', arena_eqing_views.arena_eqing_models, name='arena-eqing-models'),
    path('eqing/sessions/', arena_eqing_views.arena_create_eqing_session, name='arena-eqing-create-session'),
    path('eqing/sessions/<str:session_id>/messages/', arena_eqing_views.arena_send_message_eqing, name='arena-eqing-send-message'),

    # FreeGPT (OneAPI-backed, WASM PoW anti-bot, access code auth)
    path('freegpt/models/', arena_freegpt_views.arena_freegpt_models, name='arena-freegpt-models'),
    path('freegpt/sessions/', arena_freegpt_views.arena_create_freegpt_session, name='arena-freegpt-create-session'),
    path('freegpt/sessions/<str:session_id>/messages/', arena_freegpt_views.arena_send_message_freegpt, name='arena-freegpt-send-message'),

    # DeepSeek AI (deep-seek.ai, Laravel + OpenRouter proxy)
    path('deepseekai/models/', arena_deepseekai_views.arena_deepseekai_models, name='arena-deepseekai-models'),
    path('deepseekai/sessions/', arena_deepseekai_views.arena_create_deepseekai_session, name='arena-deepseekai-create-session'),
    path('deepseekai/sessions/<str:session_id>/messages/', arena_deepseekai_views.arena_send_message_deepseekai, name='arena-deepseekai-send-message'),

    # SurfSense (free GPT 5.4 Mini / O4 Mini, web search, Azure OpenAI)
    path('surfsense/models/', arena_surfsense_views.arena_surfsense_models, name='arena-surfsense-models'),
    path('surfsense/sessions/', arena_surfsense_views.arena_create_surfsense_session, name='arena-surfsense-create-session'),
    path('surfsense/sessions/<str:session_id>/messages/', arena_surfsense_views.arena_send_message_surfsense, name='arena-surfsense-send-message'),

    # G4F (g4f.space — 50+ models, auto-rotate on rate limits, OpenAI-compatible)
    path('g4f/models/', arena_g4f_views.arena_g4f_models, name='arena-g4f-models'),
    path('g4f/sessions/', arena_g4f_views.arena_create_g4f_session, name='arena-g4f-create-session'),
    path('g4f/sessions/<str:session_id>/messages/', arena_g4f_views.arena_send_message_g4f, name='arena-g4f-send-message'),

    # Inception Labs (Mercury 2 diffusion LLM — no API key required)
    path('inception/models/', arena_inception_views.arena_inception_models, name='arena-inception-models'),
    path('inception/sessions/', arena_inception_views.arena_create_inception_session, name='arena-inception-create-session'),
    path('inception/sessions/<str:session_id>/messages/', arena_inception_views.arena_send_message_inception, name='arena-inception-send-message'),
]
