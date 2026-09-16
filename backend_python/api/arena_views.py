"""
DRF views for community chat proxies (Neby AI on Android).

Endpoints (mounted under /api/neby-arena/):
    GET    /models/                         List LLM models (cached)
    GET    /sessions/                       List user's chat sessions
    POST   /sessions/                       Create a new chat session
    GET    /sessions/<id>/                  Get session + full message history
    PATCH  /sessions/<id>/                  Update title / is_active
    DELETE /sessions/<id>/                  Soft-delete (set is_active=False) and purge
    POST   /sessions/<id>/messages/         Send a user message, stream SSE response
    POST   /messages/<id>/regenerate/       Regenerate the last assistant message

SSE wire format (OpenAI-style):
    data: {"choices":[{"index":0,"delta":{"role":"assistant"}}]}\\n\\n
    data: {"choices":[{"index":0,"delta":{"content":"chunk"}}]}\\n\\n
    ...
    data: {"choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}\\n\\n
    data: [DONE]\\n\\n

On error:
    data: {"error":{"message":"...","code":"upstream|server"}}\\n\\n
    data: [DONE]\\n\\n
"""
import json
import logging

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession, ArenaChatMessage, ArenaChatAttachment, User
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str
from .llm import registry

logger = logging.getLogger(__name__)

# Community (scraper) providers surfaced in the generic /models/ list and
# routed here for session create + streaming. Their proxies are stateless:
# we replay the session history on every call.
_COMMUNITY_SLUGS = ('k2think', 'poolside', 'motiftech', 'qwencloud', 'yqcloud', 'chatjimmy', 'unikey', 'ptero')


def _community_models():
    """Static model catalog for community providers, shaped like arena models."""
    out = []
    for preset in registry.SCRAPER_PRESETS:
        if preset.slug not in _COMMUNITY_SLUGS:
            continue
        for spec in preset.models:
            out.append({
                'id': spec.id,
                'code': spec.id,
                'name': spec.label,
                'provider': preset.slug,
                'thinking': preset.slug in ('k2think', 'qwencloud', 'motiftech', 'unikey'),
                'randomOnly': False,
                'active': True,
            })
    return out


def _community_model_meta(model_id):
    return next((m for m in _community_models() if m['id'] == model_id), None)


def _community_proxy(provider):
    if provider == 'k2think':
        from . import k2think_proxy
        return k2think_proxy
    if provider == 'poolside':
        from . import poolside_proxy
        return poolside_proxy
    if provider == 'motiftech':
        from . import motiftech_proxy
        return motiftech_proxy
    if provider == 'qwencloud':
        from . import qwencloud_proxy
        return qwencloud_proxy
    if provider == 'yqcloud':
        from . import yqcloud_proxy
        return yqcloud_proxy
    if provider == 'chatjimmy':
        from . import chatjimmy_proxy
        return chatjimmy_proxy
    if provider == 'unikey':
        from . import unikey_proxy
        return unikey_proxy
    if provider == 'ptero':
        from . import ptero_proxy
        return ptero_proxy
    return None


# ========================= Helpers =========================

def _require_user(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User):
        return None, Response(
            {'error': 'Unauthorized — please sign in'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return user, None


def _get_owned_session(user, session_id: str):
    """Return (session, error_response). 404 if not found, 403 if not owner."""
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


# ========================= Model list =========================

_MODELS_CACHE_KEY = 'arena:models:list'
_MODELS_CACHE_TTL = 60 * 5  # 5 minutes


@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle])
def arena_models(request):
    """Return the community model catalog with 5-min cache."""
    from django.core.cache import cache

    cached = cache.get(_MODELS_CACHE_KEY)
    if cached:
        return Response({'models': cached, 'cached': True})

    community = _community_models()
    cache.set(_MODELS_CACHE_KEY, community, _MODELS_CACHE_TTL)
    return Response({'models': community, 'cached': False})


# ========================= Session list / create =========================

@api_view(['GET', 'POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_sessions(request):
    """List or create chat sessions for the current user."""
    user, err = _require_user(request)
    if err:
        return err

    if request.method == 'GET':
        items = list(
            ArenaChatSession.objects
            .filter(user=user, is_active=True)
            .order_by('-updated_at')[:200]
        )
        return Response({
            'sessions': [
                {
                    'id': s.id,
                    'title': s.title,
                    'modelId': s.model_id,
                    'modelCode': s.model_code,
                    'modelName': s.model_display_name,
                    'messageCount': s.message_count,
                    'createdAt': s.created_at,
                    'updatedAt': s.updated_at,
                    'lastMessageAt': s.last_message_at,
                    'provider': s.provider,
                }
                for s in items
            ],
        })

    # POST: create
    model_id = (request.data.get('modelId') or '').strip()
    title = (request.data.get('title') or '').strip()[:200]
    if not model_id:
        return Response(
            {'error': 'modelId is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Community providers (K2 Horizon / Poolside) — stateless proxies, no token.
    community_meta = _community_model_meta(model_id)
    if not community_meta:
        return Response(
            {'error': f'Unknown model: {model_id}'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider=community_meta['provider'],
        arena_session_id=model_id,
        arena_token_id='',
        model_id=model_id,
        model_code=model_id,
        model_display_name=community_meta['name'],
        title=title or 'New chat',
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
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
            'provider': sess.provider,
        },
    }, status=status.HTTP_201_CREATED)


# ========================= Session detail / patch / delete =========================

@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_session_detail(request, session_id: str):
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if request.method == 'GET':
        msgs = list(sess.messages.order_by('created_at'))
        msg_data = []
        for m in msgs:
            atts = list(m.attachments.all())
            msg_data.append({
                'id': m.id,
                'role': m.role,
                'content': m.content,
                'parentId': m.parent_id,
                'arenaMessageId': m.arena_message_id,
                'finishReason': m.finish_reason,
                'error': m.error,
                'durationMs': m.duration_ms,
                'createdAt': m.created_at,
                'attachments': [
                    {
                        'id': a.id,
                        'fileType': a.file_type,
                        'fileName': a.file_name,
                        'fileSize': a.file_size,
                        'mimeType': a.mime_type,
                        'showType': a.show_type,
                        'fileClass': a.file_class,
                    }
                    for a in atts
                ] if atts else [],
            })
        return Response({
            'session': {
                'id': sess.id,
                'title': sess.title,
                'modelId': sess.model_id,
                'modelCode': sess.model_code,
                'modelName': sess.model_display_name,
                'messageCount': sess.message_count,
                'createdAt': sess.created_at,
                'updatedAt': sess.updated_at,
                'lastMessageAt': sess.last_message_at,
                'isActive': sess.is_active,
                'provider': sess.provider,
            },
            'messages': msg_data,
        })

    if request.method == 'PATCH':
        new_title = request.data.get('title')
        if new_title is not None:
            sess.title = str(new_title).strip()[:200]
        if 'isActive' in request.data:
            sess.is_active = bool(request.data.get('isActive'))
        sess.updated_at = now_ms()
        sess.save(update_fields=['title', 'is_active', 'updated_at'])
        return Response({'ok': True, 'title': sess.title, 'isActive': sess.is_active})

    # DELETE: hard delete (cascade to messages via FK)
    sess.delete()
    return Response({'ok': True})


# ========================= Send message (streaming) =========================

def _sse_format(obj) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def _sse_done_marker() -> str:
    return "data: [DONE]\n\n"


def _stream_send(sess, user_content: str):
    """Generator: handle a normal send — persist user msg, stream assistant, persist it."""
    now = now_ms()
    user_msg_id = uuid_str()
    asst_msg_id = uuid_str()
    asst_started_at = now_ms()

    # Pre-insert user message
    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=user_content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    yield from _stream_assistant(
        sess=sess,
        user_msg_id=user_msg_id,
        asst_msg_id=asst_msg_id,
        asst_started_at=asst_started_at,
        upstream_kwargs=dict(mode='send'),
        bump_session_counter=True,
    )


def _stream_regenerate(sess, target_msg_id: str):
    """Generator: handle a regenerate — stream assistant, replace target msg in place."""
    asst_started_at = now_ms()
    target = sess.messages.filter(pk=target_msg_id).first()
    if not target:
        yield _sse_format({'error': {'message': 'Target message not found', 'code': 'not_found'}})
        yield _sse_done_marker()
        return

    yield from _stream_assistant(
        sess=sess,
        user_msg_id=target.parent_id,
        asst_msg_id=target.id,  # reuse id so it overwrites in place
        asst_started_at=asst_started_at,
        upstream_kwargs=dict(mode='regenerate', assistant_message_id=target.id),
        bump_session_counter=False,  # don't double-count a regenerate
        preinsert_assistant=False,   # row already exists, just overwrite content
    )


def _build_history(sess, stop_at_msg_id=None):
    """Replay session rows as an OpenAI-style message list for stateless proxies.

    Skips empty placeholder assistant rows. Stops at (and excludes) a message id
    — used for regenerate to cut off the answer being replaced.
    """
    msgs = sess.messages.order_by('created_at')
    out = []
    for m in msgs:
        if stop_at_msg_id is not None and m.pk == stop_at_msg_id:
            break
        if m.role == 'user' and m.content:
            out.append({'role': 'user', 'content': m.content})
        elif m.role == 'assistant' and m.content:
            out.append({'role': 'assistant', 'content': m.content})
    return out


def _stream_community(sess, user_msg_id: str, asst_msg_id: str, asst_started_at: int,
                      upstream_kwargs: dict, bump_session_counter: bool,
                      preinsert_assistant: bool = True):
    """SSE streaming body for stateless community proxies (K2 Horizon / Poolside).

    History is replayed from the session rows, so send and regenerate both work
    without upstream session state. Reasoning (thought) chunks are dropped.
    """
    proxy = _community_proxy(sess.provider)
    if proxy is None:
        yield _sse_format({'error': {'message': 'Unknown provider', 'code': 'server'}})
        yield _sse_done_marker()
        return

    if preinsert_assistant:
        ArenaChatMessage.objects.create(
            id=asst_msg_id, session=sess, role='assistant',
            content='', parent_id=user_msg_id,
            arena_message_id='', finish_reason='', error='',
            duration_ms=0, created_at=asst_started_at,
        )

    mode = upstream_kwargs.get('mode')
    if mode == 'regenerate':
        target_id = upstream_kwargs.get('assistant_message_id') or asst_msg_id
        history = _build_history(sess, stop_at_msg_id=target_id)
    else:
        history = _build_history(sess)

    preset = registry.preset(sess.provider)
    model = sess.model_id or (preset.default_model if preset else '')

    # Open header — announce assistant role + ids
    yield _sse_format({
        'choices': [{
            'index': 0,
            'delta': {'role': 'assistant', 'messageId': asst_msg_id, 'userMessageId': user_msg_id},
        }],
    })

    collected_text = ''
    finish_reason = 'stop'
    error_text = ''
    # Motif tracks context server-side via conversation_id — we keep it in
    # arena_token_id (unused for community sessions) and persist the fresh one.
    # QwenCloud likewise keeps server-side tab history; arena_token_id stores
    # "session_id|tab_code" for it.
    conv_id = sess.arena_token_id or None
    # Upstreams occasionally cut the stream after reasoning without an answer —
    # retry once before reporting failure.
    attempts_left = 2
    while attempts_left > 0:
        attempts_left -= 1
        try:
            kwargs = {}
            if sess.provider == 'motiftech':
                kwargs['conversation_id'] = conv_id
            elif sess.provider == 'qwencloud' and conv_id and '|' in conv_id:
                sid, _, tab = conv_id.partition('|')
                if sid and tab:
                    kwargs['session_id'] = sid
                    kwargs['tab_code'] = tab
            for chunk in proxy.stream_chat(messages=history, model=model, **kwargs):
                t = chunk.get('type')
                if t == 'text':
                    text = chunk.get('content', '')
                    if not text:
                        continue
                    collected_text += text
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'content': text}}],
                    })
                elif t == 'session':
                    sid, tab = chunk.get('session_id') or '', chunk.get('tab_code') or ''
                    if sid and tab and f'{sid}|{tab}' != (conv_id or ''):
                        conv_id = f'{sid}|{tab}'
                        try:
                            ArenaChatSession.objects.filter(pk=sess.id).update(arena_token_id=conv_id)
                        except Exception as e:
                            logger.warning("stream[%s]: session persist failed: %s", sess.provider, e)
                elif t == 'done':
                    finish_reason = chunk.get('finish_reason', 'stop')
                    new_conv = chunk.get('conversation_id')
                    if new_conv and new_conv != conv_id:
                        conv_id = new_conv
                        try:
                            ArenaChatSession.objects.filter(pk=sess.id).update(arena_token_id=new_conv)
                        except Exception as e:
                            logger.warning("stream[%s]: conversation_id persist failed: %s", sess.provider, e)
                elif t == 'error':
                    error_text = chunk.get('error') or chunk.get('message') or 'upstream error'
                    logger.warning("stream[%s]: upstream error: %s", sess.provider, error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("stream[%s]: unexpected error: %s", sess.provider, e)
            yield _sse_format({
                'error': {'message': 'Internal streaming error', 'code': 'server'},
            })
            error_text = str(e)
        if collected_text or error_text:
            break

    # Upstream may cut the stream after reasoning without an answer — surface
    # that instead of silently persisting an empty reply.
    if not error_text and not collected_text:
        error_text = f'{sess.provider} returned no answer — try again'
        yield _sse_format({
            'error': {'message': error_text, 'code': 'upstream'},
        })

    # Finalise the assistant row
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
        logger.exception("stream[%s]: failed to finalize assistant row: %s", sess.provider, e)

    # Bump session counters on success (no arena token to commit)
    if not error_text and bump_session_counter:
        try:
            ArenaChatSession.objects.filter(pk=sess.id).update(
                message_count=sess.message_count + 1,
                last_message_at=now_ms(),
                updated_at=now_ms(),
            )
            sess.message_count = sess.message_count + 1
            sess.last_message_at = now_ms()
        except Exception as e:
            logger.warning("stream[%s]: counter commit failed: %s", sess.provider, e)

    # Final SSE event
    if not error_text:
        yield _sse_format({
            'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
        })
    yield _sse_done_marker()


def _stream_assistant(sess, user_msg_id: str, asst_msg_id: str, asst_started_at: int,
                       upstream_kwargs: dict, bump_session_counter: bool,
                       preinsert_assistant: bool = True):
    """Shared SSE streaming body for both send and regenerate.

    Community providers (K2 Horizon / Poolside / Motiftech) are stateless —
    history is replayed from the session rows, so send and regenerate both
    work without upstream session state.
    """
    yield from _stream_community(
        sess=sess,
        user_msg_id=user_msg_id,
        asst_msg_id=asst_msg_id,
        asst_started_at=asst_started_at,
        upstream_kwargs=upstream_kwargs,
        bump_session_counter=bump_session_counter,
        preinsert_assistant=preinsert_assistant,
    )


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message(request, session_id: str):
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    content = (request.data.get('content') or '').strip()
    if not content:
        return Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(content) > 8000:
        return Response(
            {'error': 'Message too long (max 8000 chars)'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if sess.provider not in _COMMUNITY_SLUGS:
        return Response(
            {'error': f'This session uses the {sess.provider} provider — use its dedicated endpoint.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    gen = _stream_send(sess, content)
    response = StreamingHttpResponse(gen, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= Regenerate =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_regenerate(request, message_id: str):
    user, err = _require_user(request)
    if err:
        return err

    try:
        target = ArenaChatMessage.objects.select_related('session').get(pk=message_id)
    except ArenaChatMessage.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
    if target.session.user_id != user.id:
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    if target.role != 'assistant':
        return Response(
            {'error': 'Only assistant messages can be regenerated'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if target.session.provider not in _COMMUNITY_SLUGS:
        return Response(
            {'error': f'This session uses the {target.session.provider} provider — use its dedicated endpoint.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    gen = _stream_regenerate(target.session, target.id)
    response = StreamingHttpResponse(gen, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response
