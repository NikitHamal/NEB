"""Arena chat for the guest-site providers (K2 Horizon, Poolside, Inception).

They share one flow: a session row per chat, history replayed on each message,
the reply streamed back as OpenAI-style SSE. A provider is an entry in
SIMPLE_PROVIDERS; its model list and default model come from its proxy module.
"""
import logging
import secrets
from dataclasses import dataclass
from types import ModuleType
from typing import Callable

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from . import inception_proxy, k2think_proxy, poolside_proxy
from .arena_common import (
    Turn, require_provider_session, require_user, sse_error, sse_response,
    sse_text_delta, validated_content,
)
from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str

logger = logging.getLogger(__name__)

MAX_CONTENT_CHARS = 32000


@dataclass(frozen=True)
class SimpleProvider:
    key: str
    proxy: ModuleType
    label: str
    session_label: str
    stream_options: Callable = lambda request: {}

    @property
    def default_model(self):
        return self.proxy.MODELS[0]


def _inception_options(request):
    return {'reasoning_effort': request.data.get('reasoningEffort', 'high')}


SIMPLE_PROVIDERS = (
    SimpleProvider('k2think', k2think_proxy, 'K2 Horizon', 'K2 Horizon'),
    SimpleProvider('poolside', poolside_proxy, 'Poolside', 'Laguna'),
    SimpleProvider(
        'inception', inception_proxy, 'Inception', 'Inception',
        stream_options=_inception_options,
    ),
)


def _models_view(spec):
    @api_view(['GET'])
    @authentication_classes([AuthTokenAuthentication])
    @throttle_classes([ArenaListRateThrottle])
    def view(request):
        return Response({'models': spec.proxy.get_models(), 'provider': spec.key})
    return view


def _create_session_view(spec):
    @api_view(['POST'])
    @authentication_classes([AuthTokenAuthentication])
    @throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
    def view(request):
        user, err = require_user(request)
        if err:
            return err

        default = spec.default_model
        model_id = (request.data.get('modelId') or default['id']).strip()
        model_info = spec.proxy.MODEL_MAP.get(model_id)
        display_name = (model_info or {}).get('name', f'{spec.session_label} {model_id}')

        now = now_ms()
        sess = ArenaChatSession.objects.create(
            id=uuid_str(),
            user=user,
            provider=spec.key,
            arena_session_id=f'{spec.key}:{secrets.token_hex(16)}',
            arena_token_id='',
            qwen_chat_id='',
            model_id=model_id,
            model_code=model_id,
            model_display_name=display_name,
            title=display_name,
            is_active=True,
            message_count=0,
            last_message_at=0,
            created_at=now,
            updated_at=now,
        )

        return Response({
            'session': {
                'id': sess.id,
                'title': sess.title,
                'modelId': sess.model_id,
                'modelCode': sess.model_code,
                'modelName': sess.model_display_name,
                'provider': spec.key,
                'vision': False,
                'thinking': bool((model_info or default).get('reasoning')),
                'tools': False,
                'messageCount': 0,
                'createdAt': sess.created_at,
                'updatedAt': sess.updated_at,
            },
        }, status=status.HTTP_201_CREATED)
    return view


def _send_message_view(spec):
    @api_view(['POST'])
    @authentication_classes([AuthTokenAuthentication])
    @throttle_classes([ArenaChatRateThrottle])
    def view(request, session_id):
        user, err = require_user(request)
        if err:
            return err
        sess, err = require_provider_session(user, session_id, spec.key, spec.label)
        if err:
            return err
        content, err = validated_content(request, MAX_CONTENT_CHARS)
        if err:
            return err

        history = [
            {'role': m.role, 'content': m.content}
            for m in sess.messages.order_by('created_at')
            if m.role in ('user', 'assistant')
        ]
        stream_options = spec.stream_options(request)
        turn = Turn.begin(sess, content)

        def stream():
            yield from turn.open()

            collected_text = ''
            finish_reason = 'stop'
            error_text = ''

            try:
                for chunk in spec.proxy.stream_chat(
                    messages=history + [{'role': 'user', 'content': content}],
                    model=sess.model_id,
                    **stream_options,
                ):
                    t = chunk.get('type')
                    if t == 'text':
                        text = chunk.get('content', '')
                        collected_text += text
                        yield sse_text_delta(text)
                    elif t == 'done':
                        finish_reason = chunk.get('finish_reason', 'stop')
                    elif t == 'error':
                        error_text = chunk.get('error', 'upstream error')
                        logger.warning("%s stream: %s", spec.key, error_text)
                        yield sse_error(error_text)
                        break
            except Exception as e:
                logger.exception("%s stream: %s", spec.key, e)
                yield sse_error('Internal streaming error', 'server')
                error_text = str(e)

            yield from turn.close(collected_text, finish_reason, error_text)

        return sse_response(stream())
    return view


def simple_provider_urlpatterns():
    from django.urls import path

    patterns = []
    for spec in SIMPLE_PROVIDERS:
        patterns += [
            path(f'{spec.key}/models/', _models_view(spec), name=f'arena-{spec.key}-models'),
            path(f'{spec.key}/sessions/', _create_session_view(spec), name=f'arena-{spec.key}-create-session'),
            path(
                f'{spec.key}/sessions/<str:session_id>/messages/',
                _send_message_view(spec),
                name=f'arena-{spec.key}-send-message',
            ),
        ]
    return patterns
