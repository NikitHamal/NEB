"""
FreeGPT chat views for the Arena chat system.

These endpoints use the FreeGPT (standalone.freegpt.win:3001) proxy which provides
access to 400+ AI models including GPT-5, Claude, Gemini, DeepSeek, Grok, and more.

The site uses OneAPI backend with WASM PoW anti-bot and optional access code auth.
Models endpoint works without auth; chat endpoint requires an access code.

Mounted under /api/neby-arena/ alongside the other arena views.
"""
import json
import logging

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession, ArenaChatMessage, User
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str
from . import freegpt_proxy

logger = logging.getLogger(__name__)


def _require_user(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User):
        return None, Response(
            {'error': 'Unauthorized — please sign in'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return user, None


def _get_owned_session(user, session_id):
    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return None, Response(
            {'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND,
        )
    if sess.user_id != user.id:
        return None, Response(
            {'error': 'Forbidden — not your session'},
            status=status.HTTP_403_FORBIDDEN,
        )
    return sess, None


def _sse_format(obj):
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def _sse_done_marker():
    return "data: [DONE]\n\n"


# ========================= Model list =========================

@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle])
def arena_freegpt_models(request):
    models = freegpt_proxy.get_models()
    return Response({'models': models, 'provider': 'freegpt'})


# ========================= Create freegpt session =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_create_freegpt_session(request):
    user, err = _require_user(request)
    if err:
        return err

    model = request.data.get('model', 'gpt-5-nano')
    access_code = request.data.get('access_code', '')
    base_url = request.data.get('base_url', freegpt_proxy.DEFAULT_BASE)

    sess = ArenaChatSession.objects.create(
        user_id=user.id,
        provider='freegpt',
        model=model,
        metadata={
            'access_code': access_code,
            'base_url': base_url,
        },
    )
    return Response({
        'session_id': sess.id,
        'model': model,
        'provider': 'freegpt',
    }, status=status.HTTP_201_CREATED)


# ========================= Send message (SSE streaming) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_freegpt(request, session_id):
    user, err = _require_user(request)
    if err:
        return err

    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    content = request.data.get('content', '').strip()
    if not content:
        return Response(
            {'error': 'content is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    role = request.data.get('role', 'user')

    ArenaChatMessage.objects.create(
        session_id=sess.id,
        role=role,
        content=content,
    )

    access_code = (sess.metadata or {}).get('access_code', '')
    base_url = (sess.metadata or {}).get('base_url', freegpt_proxy.DEFAULT_BASE)

    history_msgs = list(
        ArenaChatMessage.objects
        .filter(session_id=sess.id)
        .order_by('ts')
        .values('role', 'content')
    )
    messages = [{"role": m["role"], "content": m["content"]} for m in history_msgs]

    def event_stream():
        for chunk in freegpt_proxy.stream_chat(
            messages=messages,
            model=sess.model,
            access_code=access_code,
            base_url=base_url,
        ):
            if "error" in chunk:
                yield _sse_format({"error": chunk["error"]})
                yield _sse_done_marker()
                return
            if "text" in chunk:
                yield _sse_format({"choices": [{"delta": {"content": chunk["text"]}}]})
            if "thinking" in chunk:
                yield _sse_format({"choices": [{"delta": {"reasoning_content": chunk["thinking"]}}]})
        yield _sse_done_marker()

    return StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        },
    )