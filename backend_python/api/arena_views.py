"""
DRF views for the AI4Bharat Arena chat proxy (Neby AI on Android).

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
    data: {"error":{"message":"...","code":"token_dead|upstream|server"}}\\n\\n
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
from . import ai4bharat_proxy as arena
from .llm import registry

logger = logging.getLogger(__name__)

# Community (scraper) providers surfaced in the generic /models/ list and
# routed here for session create + streaming. Their proxies are stateless:
# we replay the session history on every call.
_COMMUNITY_SLUGS = ('k2think', 'poolside')


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
                'thinking': preset.slug == 'k2think',
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
    """Return a lean list of LLM models with 5-min cache.

    Community providers (K2 Think, Poolside) are always included. AI4Bharat
    models are merged in best-effort — if the arena is unreachable the list
    still serves the community models instead of failing with 503.
    """
    from django.core.cache import cache

    cached = cache.get(_MODELS_CACHE_KEY)
    if cached:
        return Response({'models': cached, 'cached': True})

    community = _community_models()

    # Need a token to call the arena. Pull one from the pool.
    try:
        entry = arena.acquire_token(require_low_budget=False)
    except arena.ArenaError as e:
        logger.warning("arena_models: arena unavailable (%s) — serving community models only", e)
        cache.set(_MODELS_CACHE_KEY, community, _MODELS_CACHE_TTL)
        return Response({'models': community, 'cached': False})

    try:
        models = arena.fetch_models_for_client(entry['token'])
    except arena.ArenaAuthError:
        # token is bad — try once more with a fresh one
        try:
            fresh = arena._new_anonymous_token()
            models = arena.fetch_models_for_client(fresh['token'])
        except Exception as e:
            logger.warning("arena_models: fallback fetch failed (%s) — serving community models only", e)
            cache.set(_MODELS_CACHE_KEY, community, _MODELS_CACHE_TTL)
            return Response({'models': community, 'cached': False})
    except Exception as e:
        logger.warning("arena_models: fetch failed (%s) — serving community models only", e)
        cache.set(_MODELS_CACHE_KEY, community, _MODELS_CACHE_TTL)
        return Response({'models': community, 'cached': False})

    # Trim to chat-friendly fields
    public = [
        {
            'id': m['id'],
            'code': m['code'],
            'name': m['name'],
            'provider': m['provider'],
            'thinking': m['thinking'],
            'randomOnly': m['random_only'],
            'active': m['active'],
        }
        for m in models
        if m['active'] and not m['random_only']
    ]
    merged = community + public
    cache.set(_MODELS_CACHE_KEY, merged, _MODELS_CACHE_TTL)
    return Response({'models': merged, 'cached': False})


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

    # Community providers (K2 Think / Poolside) — stateless proxies, no arena token.
    community_meta = _community_model_meta(model_id)
    if community_meta:
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

    # Get a healthy token
    try:
        entry = arena.acquire_token(require_low_budget=True)
    except arena.ArenaRateLimit:
        return Response(
            {'error': 'AI pool is at capacity — try again shortly', 'code': 'pool_exhausted'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except arena.ArenaError as e:
        logger.error("arena_sessions create: token mint failed: %s", e)
        return Response(
            {'error': 'AI service temporarily unavailable'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Fetch the chosen model so we can cache its display name client-side
    model_meta = None
    try:
        all_models = arena.list_models(entry['token'])
        model_meta = next((m for m in all_models if m.get('id') == model_id), None)
    except Exception:
        pass

    # Create arena session with the bound token
    try:
        remote = arena.create_session(entry['token'], model_id)
    except arena.ArenaAuthError:
        # Token dead — try a fresh one once
        try:
            fresh = arena._new_anonymous_token()
            remote = arena.create_session(fresh['token'], model_id)
            entry = fresh
        except Exception as e:
            logger.error("arena_sessions create: fresh-token fallback failed: %s", e)
            return Response(
                {'error': 'AI service temporarily unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
    except arena.ArenaRateLimit as e:
        return Response(
            {'error': str(e), 'code': 'pool_exhausted'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except arena.ArenaError as e:
        logger.error("arena_sessions create: create_session failed: %s", e)
        return Response(
            {'error': 'Could not start AI session — try again'},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    # Record the bind
    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        arena_session_id=remote['id'],
        arena_token_id=entry['token'],
        model_id=model_id,
        model_code=(model_meta or {}).get('model_code', ''),
        model_display_name=(model_meta or {}).get('display_name', ''),
        title=title or 'New chat',
        is_active=True,
        message_count=0,
        last_message_at=0,
        created_at=now,
        updated_at=now,
    )
    arena.commit_token_use(entry['token'], message_used=False, session_opened=True)

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

    # Look up the last assistant message as the parent (for threading)
    last = (
        sess.messages.filter(role='assistant')
        .order_by('-created_at')
        .first()
    )
    parent_ids = [last.arena_message_id] if (last and last.arena_message_id) else []

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
        parent_ids=parent_ids,
        upstream_kwargs=dict(
            mode='send',
            token=sess.arena_token_id,
            session_id=sess.arena_session_id,
            user_content=user_content,
            model_id=sess.model_id,
            user_message_id=user_msg_id,
            assistant_message_id=asst_msg_id,
            parent_message_ids=parent_ids,
        ),
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

    # The arena uses the assistant message id (its own) for regenerate
    arena_msg_id = target.arena_message_id or target.id

    yield from _stream_assistant(
        sess=sess,
        user_msg_id=target.parent_id,
        asst_msg_id=target.id,  # reuse id so it overwrites in place
        asst_started_at=asst_started_at,
        parent_ids=[],
        upstream_kwargs=dict(
            mode='regenerate',
            token=sess.arena_token_id,
            assistant_message_id=arena_msg_id,
        ),
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
    """SSE streaming body for stateless community proxies (K2 Think / Poolside).

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
    # Upstreams occasionally cut the stream after reasoning without an answer —
    # retry once before reporting failure.
    attempts_left = 2
    while attempts_left > 0:
        attempts_left -= 1
        try:
            for chunk in proxy.stream_chat(messages=history, model=model):
                t = chunk.get('type')
                if t == 'text':
                    text = chunk.get('content', '')
                    if not text:
                        continue
                    collected_text += text
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'content': text}}],
                    })
                elif t == 'done':
                    finish_reason = chunk.get('finish_reason', 'stop')
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
                       parent_ids: list, upstream_kwargs: dict, bump_session_counter: bool,
                       preinsert_assistant: bool = True):
    """Shared SSE streaming body for both send and regenerate.

    Persists an assistant row (or reuses an existing id for regenerate), opens
    the upstream stream, translates a0:/ad: chunks to OpenAI-style SSE deltas,
    and finalises the row on completion.
    """
    # Community providers (K2 Think / Poolside) — stateless, replay history.
    if sess.provider in _COMMUNITY_SLUGS:
        yield from _stream_community(
            sess=sess,
            user_msg_id=user_msg_id,
            asst_msg_id=asst_msg_id,
            asst_started_at=asst_started_at,
            upstream_kwargs=upstream_kwargs,
            bump_session_counter=bump_session_counter,
            preinsert_assistant=preinsert_assistant,
        )
        return

    # Pre-insert assistant row in 'pending' state — skipped for regenerate
    # (the row already exists and we're overwriting its content).
    if preinsert_assistant:
        ArenaChatMessage.objects.create(
            id=asst_msg_id, session=sess, role='assistant',
            content='', parent_id=user_msg_id,
            arena_message_id='', finish_reason='', error='',
            duration_ms=0, created_at=asst_started_at,
        )

    # Validate / acquire token
    token = sess.arena_token_id
    if not token:
        try:
            entry = arena.acquire_token(require_low_budget=False)
            token = entry['token']
            sess.arena_token_id = token
            sess.save(update_fields=['arena_token_id'])
        except arena.ArenaError as e:
            logger.error("stream: token mint failed: %s", e)
            yield _sse_format({'error': {'message': 'AI service unavailable', 'code': 'upstream'}})
            yield _sse_done_marker()
            return

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
    mode = upstream_kwargs.pop('mode')

    try:
        if mode == 'send':
            gen = arena.stream_chat(**upstream_kwargs)
        else:
            gen = arena.regenerate(**upstream_kwargs)

        for chunk in gen:
            t = chunk.get('type')
            if t == 'content':
                text = chunk.get('text', '')
                collected_text += text
                yield _sse_format({
                    'choices': [{'index': 0, 'delta': {'content': text}}],
                })
            elif t == 'done':
                finish_reason = chunk.get('finishReason', 'stop')
            elif t == 'error':
                error_text = chunk.get('message', 'upstream error')
                logger.warning("stream: upstream error: %s", error_text)
                yield _sse_format({
                    'error': {'message': error_text, 'code': 'upstream'},
                })
                break
    except Exception as e:
        logger.exception("stream: unexpected error: %s", e)
        yield _sse_format({
            'error': {'message': 'Internal streaming error', 'code': 'server'},
        })
        error_text = str(e)

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
        logger.exception("stream: failed to finalize assistant row: %s", e)

    # Bump session counters + commit token usage on success
    if not error_text and bump_session_counter:
        try:
            ArenaChatSession.objects.filter(pk=sess.id).update(
                message_count=sess.message_count + 1,
                last_message_at=now_ms(),
                updated_at=now_ms(),
            )
            sess.message_count = sess.message_count + 1
            sess.last_message_at = now_ms()
            arena.commit_token_use(token, message_used=True, session_opened=False)
        except Exception as e:
            logger.warning("stream: counter commit failed: %s", e)

    # Final SSE event
    if not error_text:
        yield _sse_format({
            'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
        })
    yield _sse_done_marker()


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
    if sess.provider not in ('', 'ai4bharat') and sess.provider not in _COMMUNITY_SLUGS:
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
    if target.session.provider not in ('', 'ai4bharat') and target.session.provider not in _COMMUNITY_SLUGS:
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


# ========================= Diagnostic: pool stats (auth required) =========================

@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle])
def arena_pool_stats(request):
    user, err = _require_user(request)
    if err:
        return err
    # Only staff can see the pool snapshot
    if not getattr(user, 'is_staff', False):
        return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    return Response(arena.pool_stats())
