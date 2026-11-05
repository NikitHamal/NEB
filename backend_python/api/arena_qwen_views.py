"""
Qwen provider views for the Arena chat system — supports file uploads.

These endpoints use the Qwen (chat.qwen.ai) proxy which supports
images, PDFs, audio, and video via Alibaba Cloud OSS upload.

Mounted under /api/neby-arena/ alongside the community views.
"""
import base64
import logging
import os
import uuid

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .arena_common import (
    Turn, require_provider_session, require_user, sse_error, sse_response,
    validated_content,
)
from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession, ArenaChatAttachment
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str
from . import qwen_proxy
from .qwen_utils.file_upload import (
    upload_file_from_bytes, ALLOWED_EXTENSIONS, MAX_FILE_SIZE,
    MAX_FILES_PER_MESSAGE,
)

logger = logging.getLogger(__name__)

MAX_CONTENT_CHARS = 8000


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


def _fresh_qwen_session():
    qwen_session, _ = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.36'
    qwen_session.headers['x-request-id'] = str(uuid.uuid4())
    return qwen_session


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


def create_qwen_chat_session(user, model_id, title):
    """A session row backed by a fresh chat.qwen.ai chat, or None when upstream refuses."""
    qwen_session = _fresh_qwen_session()
    chat_id = qwen_proxy.create_chat(qwen_session, model=model_id, _pool_session=qwen_session)
    if not chat_id:
        return None
    now = now_ms()
    return ArenaChatSession.objects.create(
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


def qwen_session_payload(sess):
    return {
        'id': sess.id,
        'title': sess.title,
        'modelId': sess.model_id,
        'modelCode': sess.model_code,
        'modelName': sess.model_display_name,
        'provider': 'qwen',
        'messageCount': 0,
        'createdAt': sess.created_at,
        'updatedAt': sess.updated_at,
    }


# ========================= Create Qwen session =========================

@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaListRateThrottle, ArenaChatRateThrottle])
def arena_create_qwen_session(request):
    """Create a new Qwen-backed chat session (for file upload support)."""
    user, err = require_user(request)
    if err:
        return err

    model_id = (request.data.get('modelId') or '').strip()
    title = (request.data.get('title') or '').strip()[:200]

    if not model_id:
        return Response(
            {'error': 'modelId is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    sess = create_qwen_chat_session(user, model_id, title)
    if not sess:
        return Response(
            {'error': 'Could not start Qwen session — try again'},
            status=status.HTTP_502_BAD_GATEWAY,
        )
    return Response({'session': qwen_session_payload(sess)}, status=status.HTTP_201_CREATED)


# ========================= Send message (Qwen) =========================

def upload_named_files(named_files):
    """Upload (name, bytes) pairs to Qwen, skipping unsupported or oversized ones."""
    qwen_session = _fresh_qwen_session()
    req_headers = dict(qwen_session.headers)
    uploaded = []
    for name, file_bytes in named_files:
        ext = os.path.splitext(name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning("Unsupported file type in upload: %s", ext)
            continue
        if len(file_bytes) > MAX_FILE_SIZE:
            logger.warning("File too large in upload: %s (%d bytes)", name, len(file_bytes))
            continue
        file_obj = upload_file_from_bytes(name, file_bytes, qwen_session, req_headers)
        if file_obj:
            uploaded.append(file_obj)
    return uploaded


def _decode_json_files(files_data):
    named = []
    for fdata in files_data:
        data_b64 = fdata.get('data', '')
        if not data_b64:
            continue
        try:
            named.append((fdata.get('name', 'upload'), base64.b64decode(data_b64)))
        except Exception as e:
            logger.warning("Failed to decode base64 file: %s", e)
    return named


def _multipart_files(request, session_id):
    """Uploaded files for the multipart endpoint -> (file objs, error response)."""
    files = request.FILES.getlist('files')
    if not files:
        return [], None
    clean_files, file_err = _validate_file_upload(files)
    if file_err:
        return None, file_err
    qwen_session = _fresh_qwen_session()
    uploaded = _upload_files_to_qwen(clean_files, qwen_session, dict(qwen_session.headers))
    if not uploaded:
        logger.warning("All file uploads failed for session %s", session_id)
    return uploaded, None


def _json_files(request):
    """Base64 files for the JSON endpoint -> (file objs, error response)."""
    files_data = request.data.get('files', [])
    if not files_data:
        return [], None
    if len(files_data) > MAX_FILES_PER_MESSAGE:
        return None, Response(
            {'error': f'Too many files (max {MAX_FILES_PER_MESSAGE})'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return upload_named_files(_decode_json_files(files_data)), None


def _stream_qwen_turn(turn, content, uploaded_file_objs):
    yield from turn.open()
    sess = turn.sess

    qwen_session = _fresh_qwen_session()
    model = sess.model_id or 'qwen3.8-max'
    last_asst = (
        sess.messages.filter(role='assistant')
        .order_by('-created_at')
        .first()
    )
    parent_id = last_asst.arena_message_id if last_asst else None

    result = qwen_proxy.send_message(
        qwen_session, sess.qwen_chat_id, content, model=model,
        parent_id=parent_id, uploaded_files=uploaded_file_objs or None,
        _pool_session=qwen_session,
    )

    error_text = '' if result else 'Qwen returned an empty response'
    if error_text:
        yield sse_error(error_text)
    yield from turn.close(result or '', 'error' if error_text else 'stop', error_text)


def qwen_turn_response(sess, content, uploaded_file_objs):
    turn = Turn.begin(sess, content)
    if uploaded_file_objs:
        _persist_attachments(turn.user_message(), uploaded_file_objs)
    return sse_response(_stream_qwen_turn(turn, content, uploaded_file_objs))


def _send_qwen_message(request, session_id, collect_files):
    user, err = require_user(request)
    if err:
        return err
    sess, err = require_provider_session(user, session_id, 'qwen', 'Qwen')
    if err:
        return err
    content, err = validated_content(request, MAX_CONTENT_CHARS)
    if err:
        return err
    uploaded_file_objs, err = collect_files()
    if err:
        return err

    return qwen_turn_response(sess, content, uploaded_file_objs)


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_qwen(request, session_id):
    """multipart/form-data: content (required), files (up to 5). Streams SSE."""
    return _send_qwen_message(request, session_id, lambda: _multipart_files(request, session_id))


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_qwen_sse(request, session_id):
    """JSON body: content (required), files as [{name, data(base64)}]. Streams SSE."""
    return _send_qwen_message(request, session_id, lambda: _json_files(request))
