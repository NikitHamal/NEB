"""
eGov Chat AI views for the Arena chat system — supports file uploads.

These endpoints use the eGov (egov-chat-ai.e.gov.ph) proxy which provides
free AI chat with Philippine and global knowledge scopes, plus file uploads
(images and PDFs).

Mounted under /api/neby-arena/ alongside the Qwen and community views.
"""
import json
import logging
import os

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession, ArenaChatMessage, ArenaChatAttachment, User
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str
from . import egov_proxy

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
def arena_egov_models(request):
    """Return the list of available eGov models."""
    models = egov_proxy.get_models()
    return Response({'models': models, 'provider': 'egov'})


# ========================= Create eGov session =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_create_egov_session(request):
    """Create a new eGov-backed chat session."""
    user, err = _require_user(request)
    if err:
        return err

    model_id = (request.data.get('modelId') or 'AI1').strip()
    title = (request.data.get('title') or '').strip()[:200]

    # Resolve scope/model
    scope, resolved_model = egov_proxy.resolve_scope_and_model(model_id)

    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider='egov',
        arena_session_id=f'egov:{secrets_token_hex(16)}',
        arena_token_id='',
        qwen_chat_id='',
        model_id=model_id,
        model_code=resolved_model,
        model_display_name=title or f'eGov {resolved_model}',
        title=title or f'eGov {resolved_model}',
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
            'provider': 'egov',
            'scope': scope,
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=status.HTTP_201_CREATED)


def secrets_token_hex(n=16):
    import secrets as _secrets
    return _secrets.token_hex(n)


# ========================= Send message (streaming) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_egov(request, session_id):
    """Send a message to an eGov session, optionally with file attachments.

    Accepts multipart/form-data with:
      - content: text message (required)
      - files: up to 5 file attachments (optional, images and PDFs)

    Returns SSE stream with OpenAI-style deltas.
    """
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if sess.provider != 'egov':
        return Response(
            {'error': 'This endpoint only works with eGov sessions.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    content = (request.data.get('content') or '').strip()
    if not content:
        return Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(content) > 8000:
        return Response(
            {'error': 'Message too long (max 8000 chars)'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Handle file uploads
    uploaded_cdn_urls = []
    files = request.FILES.getlist('files')
    if files:
        for f in files[:5]:  # max 5 files
            ext = os.path.splitext(f.name)[1].lower()
            # Validate file type based on model
            scope, resolved_model = egov_proxy.resolve_scope_and_model(sess.model_id)
            if resolved_model == 'AI2':
                allowed_exts = {'.jpg', '.jpeg', '.png', '.gif'}
            else:
                allowed_exts = {'.jpg', '.jpeg', '.png', '.heif', '.pdf'}

            if ext not in allowed_exts:
                continue

            import base64
            file_data = f.read()
            file_obj = egov_proxy.upload_file_from_bytes(f.name, file_data, model=resolved_model)
            if file_obj and file_obj.get('cdnUrl'):
                uploaded_cdn_urls.append({
                    'type': 'image',
                    'image': file_obj['cdnUrl'],
                    'original_filename': file_obj.get('original_filename', f.name),
                    'mime_type': file_obj.get('mime_type', ''),
                })

    # Build history from previous messages in this session
    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({
                'role': m.role,
                'content': m.content,
            })

    # Pre-insert user message
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

    scope, resolved_model = egov_proxy.resolve_scope_and_model(sess.model_id)

    def _stream_egov():
        yield _sse_format({
            'choices': [{
                'index': 0,
                'delta': {'role': 'assistant', 'messageId': asst_msg_id, 'userMessageId': user_msg_id},
            }],
        })

        # Pre-insert assistant row
        ArenaChatMessage.objects.create(
            id=asst_msg_id, session=sess, role='assistant',
            content='', parent_id=user_msg_id,
            arena_message_id='', finish_reason='', error='',
            duration_ms=0, created_at=asst_started_at,
        )

        # Build content parts for eGov
        content_parts = []
        for att in uploaded_cdn_urls:
            content_parts.append({'type': att['type'], 'image': att['image']})
        content_parts.append({'type': 'text', 'text': content})

        collected_text = ''
        finish_reason = 'stop'
        error_text = ''

        try:
            for chunk in egov_proxy.stream_chat(
                user_message=content,
                model=sess.model_id,
                history=history,
            ):
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
                    logger.warning("egov stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("egov stream: unexpected error: %s", e)
            yield _sse_format({
                'error': {'message': 'Internal streaming error', 'code': 'server'},
            })
            error_text = str(e)

        # Finalize assistant row
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
            logger.exception("egov: failed to finalize assistant row: %s", e)

        # Bump session counters
        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("egov: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_egov(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= SSE variant (JSON body with base64 files) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_egov_sse(request, session_id):
    """SSE streaming variant — accepts JSON body with optional base64 files.

    Body:
      - content: text message (required)
      - files: array of {name, data} base64-encoded files (optional)

    Returns SSE stream with OpenAI-style deltas.
    """
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if sess.provider != 'egov':
        return Response(
            {'error': 'This endpoint only works with eGov sessions.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    content = (request.data.get('content') or '').strip()
    if not content:
        return Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(content) > 8000:
        return Response(
            {'error': 'Message too long (max 8000 chars)'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Handle base64-encoded files from JSON body
    files_data = request.data.get('files', [])
    uploaded_cdn_urls = []
    if files_data:
        import base64
        scope, resolved_model = egov_proxy.resolve_scope_and_model(sess.model_id)
        if resolved_model == 'AI2':
            allowed_exts = {'.jpg', '.jpeg', '.png', '.gif'}
        else:
            allowed_exts = {'.jpg', '.jpeg', '.png', '.heif', '.pdf'}

        for fdata in files_data[:5]:
            name = fdata.get('name', 'upload')
            data_b64 = fdata.get('data', '')
            if not data_b64:
                continue

            ext = os.path.splitext(name)[1].lower()
            if ext not in allowed_exts:
                logger.warning("egov: unsupported file type in SSE upload: %s", ext)
                continue

            try:
                file_bytes = base64.b64decode(data_b64)
            except Exception as e:
                logger.warning("egov: failed to decode base64 file: %s", e)
                continue

            file_obj = egov_proxy.upload_file_from_bytes(name, file_bytes, model=resolved_model)
            if file_obj and file_obj.get('cdnUrl'):
                uploaded_cdn_urls.append({
                    'type': 'image',
                    'image': file_obj['cdnUrl'],
                    'original_filename': file_obj.get('original_filename', name),
                    'mime_type': file_obj.get('mime_type', ''),
                })

    # Build history from previous messages
    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({
                'role': m.role,
                'content': m.content,
            })

    # Pre-insert user message
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

    # Persist attachments on the user message
    if uploaded_cdn_urls:
        user_msg = ArenaChatMessage.objects.get(pk=user_msg_id)
        for att in uploaded_cdn_urls:
            ArenaChatAttachment.objects.create(
                id=uuid_str(),
                message=user_msg,
                file_type=att.get('type', 'image'),
                file_name=att.get('original_filename', ''),
                file_size=0,
                mime_type=att.get('mime_type', ''),
                qwen_file_id='',
                qwen_file_url=att.get('image', ''),
                show_type='image' if 'image' in att.get('mime_type', '') else 'document',
                file_class='egov',
                created_at=now,
            )

    scope, resolved_model = egov_proxy.resolve_scope_and_model(sess.model_id)

    def _stream_egov():
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
        finish_reason = 'stop'
        error_text = ''

        try:
            for chunk in egov_proxy.stream_chat(
                user_message=content,
                model=sess.model_id,
                history=history,
            ):
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
                    logger.warning("egov stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("egov stream: unexpected error: %s", e)
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
            logger.exception("egov: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("egov: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_egov(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response