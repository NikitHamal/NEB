"""
DeepAI chat views for the Arena chat system — supports file uploads.

These endpoints use the DeepAI (deepai.org) proxy which provides
access to multiple AI models including Standard, Genius, Super Genius,
and third-party models (GPT-4.1, Gemini, Claude, etc.).

DeepAI supports file attachments (images and documents) via its upload endpoint.
Free-tier models: standard, deepseek-v3.2, gemma-4, gpt-4.1-nano, etc.
Pro-only models: genius, supergenius, gpt-4o-mini, o3, claude-4.7-opus, etc.

Mounted under /api/neby-arena/ alongside the Qwen, eGov, and community views.
"""
import base64
import logging
import os
import secrets

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .arena_common import (
    Turn, require_provider_session, require_user, sse_error, sse_response,
    sse_text_delta, validated_content,
)
from .authentication import AuthTokenAuthentication
from .models import ArenaChatSession, ArenaChatAttachment
from .throttles import ArenaChatRateThrottle, ArenaListRateThrottle
from .utils import now_ms, uuid_str
from . import deepai_proxy

logger = logging.getLogger(__name__)


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
    user, err = require_user(request)
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
        arena_session_id=f'deepai:{secrets.token_hex(16)}',
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


# ========================= Send message (DeepAI) =========================

MAX_CONTENT_CHARS = 32000
MAX_FILES_PER_MESSAGE = 10
ALLOWED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif',
    '.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.csv',
    '.md', '.json',
}


def _upload_attachment(name, file_bytes):
    file_obj = deepai_proxy.upload_file_from_bytes(name, file_bytes)
    if not (file_obj and file_obj.get('download_url')):
        return None
    return {
        'type': 'attachment',
        'url': file_obj.get('download_url', ''),
        'original_filename': file_obj.get('original_filename', name),
        'mime_type': file_obj.get('content_type', ''),
        'uuid': file_obj.get('uuid', ''),
    }


def _multipart_attachments(request):
    uploaded = []
    for f in request.FILES.getlist('files')[:MAX_FILES_PER_MESSAGE]:
        if os.path.splitext(f.name)[1].lower() not in ALLOWED_EXTENSIONS:
            continue
        att = _upload_attachment(f.name, f.read())
        if att:
            uploaded.append(att)
    return uploaded


def _json_attachments(request):
    uploaded = []
    for fdata in (request.data.get('files') or [])[:MAX_FILES_PER_MESSAGE]:
        name = fdata.get('name', 'upload')
        data_b64 = fdata.get('data', '')
        if not data_b64:
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning("deepai: unsupported file type in SSE upload: %s", ext)
            continue
        try:
            file_bytes = base64.b64decode(data_b64)
        except Exception as e:
            logger.warning("deepai: failed to decode base64 file: %s", e)
            continue
        att = _upload_attachment(name, file_bytes)
        if att:
            uploaded.append(att)
    return uploaded


def _persist_attachments(user_msg, attachments):
    for att in attachments:
        mime = att.get('mime_type', '')
        ArenaChatAttachment.objects.create(
            id=uuid_str(),
            message=user_msg,
            file_type=att.get('type', 'attachment'),
            file_name=att.get('original_filename', ''),
            file_size=0,
            mime_type=mime,
            qwen_file_id=att.get('uuid', ''),
            qwen_file_url=att.get('url', ''),
            show_type='image' if 'image' in mime else 'document',
            file_class='deepai',
            created_at=now_ms(),
        )


def _stream_deepai_turn(turn, content, history, attachments):
    yield from turn.open()

    collected_text = ''
    finish_reason = 'stop'
    error_text = ''
    stream_kwargs = {}
    attachment_uuids = [att['uuid'] for att in attachments if att.get('uuid')]
    if attachment_uuids:
        stream_kwargs['attachment_uuids'] = attachment_uuids

    try:
        for chunk in deepai_proxy.stream_chat(
            user_message=content,
            model=turn.sess.model_id,
            history=history,
            **stream_kwargs,
        ):
            t = chunk.get('type')
            if t == 'content':
                text = chunk.get('text', '')
                collected_text += text
                yield sse_text_delta(text)
            elif t == 'done':
                finish_reason = chunk.get('finishReason', 'stop')
            elif t == 'error':
                error_text = chunk.get('message', 'upstream error')
                logger.warning("deepai stream: upstream error: %s", error_text)
                yield sse_error(error_text)
                break
    except Exception as e:
        logger.exception("deepai stream: unexpected error: %s", e)
        yield sse_error('Internal streaming error', 'server')
        error_text = str(e)

    yield from turn.close(collected_text, finish_reason, error_text)


def _send_deepai_message(request, session_id, collect_attachments):
    user, err = require_user(request)
    if err:
        return err
    sess, err = require_provider_session(user, session_id, 'deepai', 'DeepAI')
    if err:
        return err
    content, err = validated_content(request, MAX_CONTENT_CHARS)
    if err:
        return err

    attachments = collect_attachments(request)
    history = [
        {'role': m.role, 'content': m.content}
        for m in sess.messages.order_by('created_at')
        if m.role in ('user', 'assistant')
    ]
    turn = Turn.begin(sess, content)
    if attachments:
        _persist_attachments(turn.user_message(), attachments)
    return sse_response(_stream_deepai_turn(turn, content, history, attachments))


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_deepai(request, session_id):
    """multipart/form-data: content (required), files (up to 10). Streams SSE."""
    return _send_deepai_message(request, session_id, _multipart_attachments)


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def arena_send_message_deepai_sse(request, session_id):
    """JSON body: content (required), files as [{name, data(base64)}]. Streams SSE."""
    return _send_deepai_message(request, session_id, _json_attachments)
