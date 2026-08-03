"""
Qwen provider views for the Arena chat system — supports file uploads.

These endpoints use the Qwen (chat.qwen.ai) proxy which supports
images, PDFs, audio, and video via Alibaba Cloud OSS upload.

Mounted under /api/neby-arena/ alongside the AI4Bharat views.
"""
import json
import logging
import os
import tempfile
import uuid

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession, ArenaChatMessage, ArenaChatAttachment, User
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str
from . import qwen_proxy
from .qwen_utils.file_upload import (
    upload_file_from_bytes, classify_file, ALLOWED_EXTENSIONS, MAX_FILE_SIZE,
    MAX_FILES_PER_MESSAGE,
)

logger = logging.getLogger(__name__)


def _require_user(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User):
        return None, Response(
            {'error': 'Unauthorized — please sign in'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return user, None


# ========================= Qwen Model List =========================

@api_view(['GET'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle])
def arena_qwen_models(request):
    """Return the live Qwen model catalog from chat.qwen.ai.

    Cached for 5 minutes in Redis. Returns full capability metadata
    (vision, document, video, audio, thinking, search, context length, etc.)
    """
    from .qwen_utils.models import fetch_models

    models = fetch_models()
    return Response({'models': models, 'cached': True})


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


def _validate_file_upload(files):
    """Validate uploaded files. Returns (clean_files, error_response)."""
    if len(files) > MAX_FILES_PER_MESSAGE:
        return None, Response(
            {'error': f'Too many files (max {MAX_FILES_PER_MESSAGE})'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    clean = []
    for f in files:
        name = f.name
        ext = os.path.splitext(name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return None, Response(
                {'error': f'File type not supported: {ext}. Supported: {", ".join(sorted(ALLOWED_EXTENSIONS))}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if f.size > MAX_FILE_SIZE:
            return None, Response(
                {'error': f'File too large: {name} ({f.size} bytes, max {MAX_FILE_SIZE})'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        clean.append(f)
    return clean, None


def _upload_files_to_qwen(files, session, headers):
    """Upload Django UploadedFile objects to Qwen OSS. Returns list of file_obj dicts."""
    uploaded = []
    for f in files:
        file_data = f.read()
        file_obj = upload_file_from_bytes(f.name, file_data, session, headers)
        if file_obj:
            uploaded.append(file_obj)
        else:
            logger.warning("Failed to upload file to Qwen OSS: %s", f.name)
    return uploaded


def _persist_attachments(user_msg, uploaded_files):
    """Save ArenaChatAttachment rows for a user message."""
    for fobj in uploaded_files:
        ArenaChatAttachment.objects.create(
            id=uuid_str(),
            message=user_msg,
            file_type=fobj.get('type', ''),
            file_name=fobj.get('name', ''),
            file_size=fobj.get('size', 0),
            mime_type=fobj.get('file_type', ''),
            qwen_file_id=fobj.get('id', ''),
            qwen_file_url=fobj.get('url', ''),
            show_type=fobj.get('showType', ''),
            file_class=fobj.get('file_class', ''),
            created_at=now_ms(),
        )


# ========================= Create Qwen session =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_create_qwen_session(request):
    """Create a new Qwen-backed chat session (for file upload support)."""
    user, err = _require_user(request)
    if err:
        return err

    model_id = (request.data.get('modelId') or '').strip()
    title = (request.data.get('title') or '').strip()[:200]

    if not model_id:
        return Response(
            {'error': 'modelId is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    qwen_session, qwen_cookies = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.36'
    qwen_session.headers['x-request-id'] = str(uuid.uuid4())

    chat_id = qwen_proxy.create_chat(qwen_session, model=model_id, _pool_session=qwen_session)
    if not chat_id:
        return Response(
            {'error': 'Could not start Qwen session — try again'},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider='qwen',
        arena_session_id=f'qwen:{chat_id}',
        arena_token_id='',
        qwen_chat_id=chat_id,
        model_id=model_id,
        model_code=model_id,
        model_display_name=title or 'New chat',
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
            'provider': 'qwen',
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=status.HTTP_201_CREATED)


# ========================= Send message with files (Qwen) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_qwen(request, session_id):
    """Send a message to a Qwen session, optionally with file attachments.

    Accepts multipart/form-data with:
      - content: text message (required)
      - files: up to 5 file attachments (optional)

    Returns SSE stream with OpenAI-style deltas.
    """
    user, err = _require_user(request)
    if err:
        return err
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if sess.provider != 'qwen':
        return Response(
            {'error': 'This endpoint only works with Qwen sessions. Use /sessions/<id>/messages/ for AI4Bharat.'},
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
    files = request.FILES.getlist('files')
    uploaded_file_objs = []
    if files:
        clean_files, file_err = _validate_file_upload(files)
        if file_err:
            return file_err

        qwen_session, _ = qwen_proxy._get_session()
        midtoken = qwen_proxy.get_midtoken(qwen_session)
        if midtoken:
            qwen_session.headers['bx-umidtoken'] = midtoken
            qwen_session.headers['bx-v'] = '2.5.36'
        qwen_session.headers['x-request-id'] = str(uuid.uuid4())
        req_headers = dict(qwen_session.headers)

        uploaded_file_objs = _upload_files_to_qwen(clean_files, qwen_session, req_headers)
        if not uploaded_file_objs and files:
            logger.warning("All file uploads failed for session %s", session_id)

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
    if uploaded_file_objs:
        user_msg = ArenaChatMessage.objects.get(pk=user_msg_id)
        _persist_attachments(user_msg, uploaded_file_objs)

    # SSE header
    def _stream_qwen():
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

        # Get Qwen session
        qwen_session, _ = qwen_proxy._get_session()
        midtoken = qwen_proxy.get_midtoken(qwen_session)
        if midtoken:
            qwen_session.headers['bx-umidtoken'] = midtoken
            qwen_session.headers['bx-v'] = '2.5.36'
        qwen_session.headers['x-request-id'] = str(uuid.uuid4())

        chat_id = sess.qwen_chat_id
        model = sess.model_id or 'qwen3.8-max'

        # Look up parent_id from last assistant message for threading
        last_asst = (
            sess.messages.filter(role='assistant')
            .order_by('-created_at')
            .first()
        )
        parent_id = last_asst.arena_message_id if last_asst else None

        # Send message via Qwen proxy
        result = qwen_proxy.send_message(
            qwen_session, chat_id, content, model=model,
            parent_id=parent_id, uploaded_files=uploaded_file_objs or None,
            _pool_session=qwen_session,
        )

        collected_text = ''
        finish_reason = 'stop'
        error_text = ''

        if result:
            collected_text = result
        else:
            error_text = 'Qwen returned an empty response'
            finish_reason = 'error'
            yield _sse_format({
                'error': {'message': error_text, 'code': 'upstream'},
            })

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
            logger.exception("Failed to finalize assistant row: %s", e)

        # Bump session counters
        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("Counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_qwen(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= Qwen streaming (SSE) =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_qwen_sse(request, session_id):
    """SSE streaming variant of send_message_qwen.

    Accepts JSON body with:
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

    if sess.provider != 'qwen':
        return Response(
            {'error': 'This endpoint only works with Qwen sessions.'},
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
    uploaded_file_objs = []
    if files_data:
        if len(files_data) > MAX_FILES_PER_MESSAGE:
            return Response(
                {'error': f'Too many files (max {MAX_FILES_PER_MESSAGE})'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qwen_session, _ = qwen_proxy._get_session()
        midtoken = qwen_proxy.get_midtoken(qwen_session)
        if midtoken:
            qwen_session.headers['bx-umidtoken'] = midtoken
            qwen_session.headers['bx-v'] = '2.5.36'
        qwen_session.headers['x-request-id'] = str(uuid.uuid4())
        req_headers = dict(qwen_session.headers)

        import base64

        for fdata in files_data:
            name = fdata.get('name', 'upload')
            data_b64 = fdata.get('data', '')
            if not data_b64:
                continue

            ext = os.path.splitext(name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                logger.warning("Unsupported file type in SSE upload: %s", ext)
                continue

            try:
                file_bytes = base64.b64decode(data_b64)
            except Exception as e:
                logger.warning("Failed to decode base64 file: %s", e)
                continue

            if len(file_bytes) > MAX_FILE_SIZE:
                logger.warning("File too large in SSE upload: %s (%d bytes)", name, len(file_bytes))
                continue

            file_obj = upload_file_from_bytes(name, file_bytes, qwen_session, req_headers)
            if file_obj:
                uploaded_file_objs.append(file_obj)

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

    if uploaded_file_objs:
        user_msg = ArenaChatMessage.objects.get(pk=user_msg_id)
        _persist_attachments(user_msg, uploaded_file_objs)

    def _stream_qwen():
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

        qwen_session, _ = qwen_proxy._get_session()
        midtoken = qwen_proxy.get_midtoken(qwen_session)
        if midtoken:
            qwen_session.headers['bx-umidtoken'] = midtoken
            qwen_session.headers['bx-v'] = '2.5.36'
        qwen_session.headers['x-request-id'] = str(uuid.uuid4())

        chat_id = sess.qwen_chat_id
        model = sess.model_id or 'qwen3.8-max'

        last_asst = (
            sess.messages.filter(role='assistant')
            .order_by('-created_at')
            .first()
        )
        parent_id = last_asst.arena_message_id if last_asst else None

        result = qwen_proxy.send_message(
            qwen_session, chat_id, content, model=model,
            parent_id=parent_id, uploaded_files=uploaded_file_objs or None,
            _pool_session=qwen_session,
        )

        collected_text = ''
        finish_reason = 'stop'
        error_text = ''

        if result:
            collected_text = result
        else:
            error_text = 'Qwen returned an empty response'
            finish_reason = 'error'
            # Error event before [DONE]
            yield _sse_format({
                'error': {'message': error_text, 'code': 'upstream'},
            })

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
            logger.exception("Failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("Counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_qwen(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response