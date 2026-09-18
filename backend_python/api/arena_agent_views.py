"""Stateless single-shot chat for LLM clients (PixelForge agent and friends).

Unlike the session-based arena endpoints in arena_views.py, this view keeps no
rows: POST /api/neby-arena/agent/ {model, messages} streams the upstream answer
straight back as OpenAI-style SSE. Same Bearer auth and arena throttles apply.
"""
import json
import logging

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .arena_views import (
    _COMMUNITY_SLUGS,
    _community_model_meta,
    _community_proxy,
    _sse_done_marker,
    _sse_format,
)
from .authentication import AuthTokenAuthentication
from .throttles import ArenaChatRateThrottle

logger = logging.getLogger(__name__)

MAX_INPUT_CHARS = 32000


def _coerce_messages(raw):
    out = []
    total = 0
    for m in raw or []:
        if not isinstance(m, dict):
            continue
        role = str(m.get('role') or '').lower()
        content = str(m.get('content') or '')
        if role == 'system' and content.strip():
            content = '[System instructions]\n' + content.strip()
            role = 'user'
        if role not in ('user', 'assistant') or not content.strip():
            continue
        total += len(content)
        if total > MAX_INPUT_CHARS:
            break
        out.append({'role': role, 'content': content})
    return out


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_agent_chat(request):
    user = getattr(request, 'user', None)
    from .models import User as UserModel
    if not isinstance(user, UserModel):
        return Response({'error': 'Unauthorized — please sign in'}, status=status.HTTP_401_UNAUTHORIZED)

    model_id = str(request.data.get('model') or '').strip()
    meta = _community_model_meta(model_id)
    if not meta:
        return Response(
            {'error': f'Unknown model: {model_id}. Use GET /api/neby-arena/models/ for the catalog.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    messages = _coerce_messages(request.data.get('messages'))
    if not any(m['role'] == 'user' for m in messages):
        return Response({'error': 'messages must include at least one user message'}, status=status.HTTP_400_BAD_REQUEST)

    proxy = _community_proxy(meta['provider'])
    if proxy is None:
        return Response({'error': 'Unknown provider'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def gen():
        try:
            for chunk in proxy.stream_chat(messages, model=model_id):
                t = (chunk or {}).get('type')
                if t == 'text':
                    yield _sse_format({'choices': [{'index': 0, 'delta': {'content': chunk.get('content', '')}}]})
                elif t == 'thought':
                    yield _sse_format({'choices': [{'index': 0, 'delta': {'reasoning_content': chunk.get('content', '')}}]})
                elif t == 'error':
                    yield _sse_format({'error': {'message': str(chunk.get('error', 'upstream error'))[:500], 'code': 'upstream'}})
                    break
                elif t == 'done':
                    break
        except Exception as e:
            logger.exception('arena_agent_chat: streaming failed')
            yield _sse_format({'error': {'message': 'Internal streaming error', 'code': 'server'}})
        yield _sse_format({'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})
        yield _sse_done_marker()

    response = StreamingHttpResponse(gen(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
