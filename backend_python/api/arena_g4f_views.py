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
from . import g4f_proxy

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


@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle])
def arena_g4f_models(request):
    models = g4f_proxy.get_models()
    return Response({'models': models, 'provider': 'g4f'})


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_create_g4f_session(request):
    user, err = _require_user(request)
    if err:
        return err

    model_id = (request.data.get('modelId') or 'openai').strip()
    title = (request.data.get('title') or '').strip()[:200]

    model_info = None
    for m in g4f_proxy.MODELS:
        if m['id'] == model_id:
            model_info = m
            break

    display_name = (model_info or {}).get('name', f'G4F {model_id}')

    now = now_ms()
    import secrets as _secrets
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider='g4f',
        arena_session_id=f'g4f:{_secrets.token_hex(16)}',
        arena_token_id='',
        qwen_chat_id='',
        model_id=model_id,
        model_code=model_id,
        model_display_name=title or display_name,
        title=title or display_name,
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
            'provider': 'g4f',
            'vision': (model_info or {}).get('vision', False),
            'thinking': (model_info or {}).get('reasoning', False),
            'tools': False,
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_g4f(request, session_id):
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if sess.provider != 'g4f':
        return Response(
            {'error': 'This endpoint only works with G4F sessions.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    content = (request.data.get('content') or '').strip()
    if not content:
        return Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(content) > 32000:
        return Response(
            {'error': 'Message too long (max 32000 chars)'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({'role': m.role, 'content': m.content})

    now = now_ms()
    user_msg_id = uuid_str()
    asst_msg_id = uuid_str()
    asst_started_at = now_ms()

    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    def _stream_g4f():
        yield _sse_format({
            'choices': [{
                'index': 0,
                'delta': {'role': 'assistant', 'messageId': asst_msg_id, 'userMessageId': user_msg_id},
            }],
        })

        ArenaChatMessage.objects.create(
            id=asst_msg_id, session=sess, role='assistant',
            content='', parent_id=user_msg_id,
            arena_message_id='', finish_reason='', error='',
            duration_ms=0, created_at=asst_started_at,
        )

        collected_text = ''
        collected_thinking = ''
        finish_reason = 'stop'
        error_text = ''

        try:
            for chunk in g4f_proxy.stream_chat(
                messages=history + [{'role': 'user', 'content': content}],
                model=sess.model_id,
            ):
                t = chunk.get('type')
                if t == 'text':
                    text = chunk.get('content', '')
                    collected_text += text
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'content': text}}],
                    })
                elif t == 'thinking':
                    thinking = chunk.get('content', '')
                    collected_thinking += thinking
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'reasoning_content': thinking}}],
                    })
                elif t == 'done':
                    finish_reason = chunk.get('finish_reason', 'stop')
                elif t == 'error':
                    error_text = chunk.get('error', 'upstream error')
                    logger.warning("g4f stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("g4f stream: unexpected error: %s", e)
            yield _sse_format({
                'error': {'message': 'Internal streaming error', 'code': 'server'},
            })
            error_text = str(e)

        duration_ms = max(0, now_ms() - asst_started_at)
        try:
            ArenaChatMessage.objects.filter(pk=asst_msg_id).update(
                content=collected_text,
                finish_reason=finish_reason,
                error=error_text[:200],
                duration_ms=duration_ms,
                arena_message_id=asst_msg_id,
            )
        except Exception as e:
            logger.exception("g4f: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("g4f: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_g4f(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response
