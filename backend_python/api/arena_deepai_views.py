"""
DeepAI chat views for the Arena chat system — supports file uploads.

These endpoints use the DeepAI (deepai.org) proxy which provides
access to multiple AI models including Standard, Genius, Super Genius,
and third-party models (GPT-4.1, Gemini, Claude, etc.).

DeepAI supports file attachments (images and documents) via its upload endpoint.
Free-tier models: standard, deepseek-v3.2, gemma-4, gpt-4.1-nano, etc.
Pro-only models: genius, supergenius, gpt-4o-mini, o3, claude-4.7-opus, etc.

Mounted under /api/neby-arena/ alongside the AI4Bharat, Qwen, and eGov views.
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
from . import deepai_proxy

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
def arena_deepai_models(request):
    """Return the list of available DeepAI models."""
    models = deepai_proxy.get_models()
    return Response({'models': models, 'provider': 'deepai'})


# ========================= Create DeepAI session =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_create_deepai_session(request):
    """Create a new DeepAI-backed chat session."""
    user, err = _require_user(request)
    if err:
        return err

    model_id = (request.data.get('modelId') or 'standard').strip()
    title = (request.data.get('title') or '').strip()[:200]

    try:
        resolved_model, info = deepai_proxy.resolve_model(model_id)
    except deepai_proxy.DeepAIError as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    display_name = info.get('name', f'DeepAI {resolved_model}')

    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider='deepai',
        arena_session_id=f'deepai:{_secrets_token_hex(16)}',
        arena_token_id='',
        qwen_chat_id='',
        model_id=model_id,
        model_code=resolved_model,
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
            'provider': 'deepai',
            'vision': info.get('vision', False),
            'thinking': info.get('thinking', False),
            'locked': info.get('locked', False),
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=status.HTTP_201_CREATED)


def _secrets_token_hex(n=16):
    import secrets as _secrets
    return _secrets.token_hex(n)


# ========================= Send message (multipart with files) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_deepai(request, session_id):
    """Send a message to a DeepAI session, optionally with file attachments.

    Accepts multipart/form-data with:
      - content: text message (required)
      - files: up to 10 file attachments (optional, images and documents)

    Returns SSE stream with OpenAI-style deltas.
    """
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if sess.provider != 'deepai':
        return Response(
            {'error': 'This endpoint only works with DeepAI sessions.'},
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

    # Handle file uploads
    uploaded_attachments = []
    files = request.FILES.getlist('files')
    if files:
        for f in files[:10]:
            ext = os.path.splitext(f.name)[1].lower()
            allowed_exts = {
                '.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif',
                '.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.csv',
                '.md', '.json',
            }
            if ext not in allowed_exts:
                continue

            file_data = f.read()
            file_obj = deepai_proxy.upload_file_from_bytes(f.name, file_data)
            if file_obj and file_obj.get('download_url'):
                uploaded_attachments.append({
                    'type': 'attachment',
                    'url': file_obj.get('download_url', ''),
                    'original_filename': file_obj.get('original_filename', f.name),
                    'mime_type': file_obj.get('content_type', ''),
                    'uuid': file_obj.get('uuid', ''),
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

    # Persist attachment records
    if uploaded_attachments:
        user_msg = ArenaChatMessage.objects.get(pk=user_msg_id)
        for att in uploaded_attachments:
            ArenaChatAttachment.objects.create(
                id=uuid_str(),
                message=user_msg,
                file_type=att.get('type', 'attachment'),
                file_name=att.get('original_filename', ''),
                file_size=0,
                mime_type=att.get('mime_type', ''),
                qwen_file_id=att.get('uuid', ''),
                qwen_file_url=att.get('url', ''),
                show_type='image' if 'image' in att.get('mime_type', '') else 'document',
                file_class='deepai',
                created_at=now,
            )

    def _stream_deepai():
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

        # Build attachment UUIDs list for DeepAI
        attachment_uuids = [att['uuid'] for att in uploaded_attachments if att.get('uuid')]

        stream_kwargs = {}
        if attachment_uuids:
            stream_kwargs['attachment_uuids'] = attachment_uuids

        try:
            for chunk in deepai_proxy.stream_chat(
                user_message=content,
                model=sess.model_id,
                history=history,
                **stream_kwargs,
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
                    logger.warning("deepai stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("deepai stream: unexpected error: %s", e)
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
            logger.exception("deepai: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("deepai: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_deepai(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= SSE variant (JSON body with base64 files) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_deepai_sse(request, session_id):
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

    if sess.provider != 'deepai':
        return Response(
            {'error': 'This endpoint only works with DeepAI sessions.'},
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

    # Handle base64-encoded files from JSON body
    files_data = request.data.get('files', [])
    uploaded_attachments = []
    if files_data:
        import base64
        for fdata in files_data[:10]:
            name = fdata.get('name', 'upload')
            data_b64 = fdata.get('data', '')
            if not data_b64:
                continue

            ext = os.path.splitext(name)[1].lower()
            allowed_exts = {
                '.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif',
                '.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.csv',
                '.md', '.json',
            }
            if ext not in allowed_exts:
                logger.warning("deepai: unsupported file type in SSE upload: %s", ext)
                continue

            try:
                file_bytes = base64.b64decode(data_b64)
            except Exception as e:
                logger.warning("deepai: failed to decode base64 file: %s", e)
                continue

            file_obj = deepai_proxy.upload_file_from_bytes(name, file_bytes)
            if file_obj and file_obj.get('download_url'):
                uploaded_attachments.append({
                    'type': 'attachment',
                    'url': file_obj.get('download_url', ''),
                    'original_filename': file_obj.get('original_filename', name),
                    'mime_type': file_obj.get('content_type', ''),
                    'uuid': file_obj.get('uuid', ''),
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

    # Persist attachment records
    if uploaded_attachments:
        user_msg = ArenaChatMessage.objects.get(pk=user_msg_id)
        for att in uploaded_attachments:
            ArenaChatAttachment.objects.create(
                id=uuid_str(),
                message=user_msg,
                file_type=att.get('type', 'attachment'),
                file_name=att.get('original_filename', ''),
                file_size=0,
                mime_type=att.get('mime_type', ''),
                qwen_file_id=att.get('uuid', ''),
                qwen_file_url=att.get('url', ''),
                show_type='image' if 'image' in att.get('mime_type', '') else 'document',
                file_class='deepai',
                created_at=now,
            )

    def _stream_deepai():
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

        attachment_uuids = [att['uuid'] for att in uploaded_attachments if att.get('uuid')]

        stream_kwargs = {}
        if attachment_uuids:
            stream_kwargs['attachment_uuids'] = attachment_uuids

        try:
            for chunk in deepai_proxy.stream_chat(
                user_message=content,
                model=sess.model_id,
                history=history,
                **stream_kwargs,
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
                    logger.warning("deepai stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("deepai stream: unexpected error: %s", e)
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
            logger.exception("deepai: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("deepai: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_deepai(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response