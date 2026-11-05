"""Session-authenticated AJAX endpoints for the Neby Arena chat.

The chat turn itself lives in api/arena_*; these views only identify the
signed-in web user and hand over to it.
"""
import json

from django.http import JsonResponse

from api import deepai_proxy
from api.arena_common import sse_response
from api.arena_views import _stream_regenerate, _stream_send
from api.arena_deepai_views import (
    MAX_CONTENT_CHARS as DEEPAI_MAX_CONTENT_CHARS, MAX_FILES_PER_MESSAGE as DEEPAI_MAX_FILES,
    create_deepai_chat_session, deepai_session_payload, deepai_turn_response,
    upload_attachments,
)
from api.arena_qwen_views import (
    MAX_CONTENT_CHARS as QWEN_MAX_CONTENT_CHARS, create_qwen_chat_session,
    qwen_session_payload, qwen_turn_response, upload_named_files,
)
from api.models import ArenaChatMessage, ArenaChatSession, User
from api.utils import now_ms, uuid_str
from api.qwen_utils.file_upload import MAX_FILES_PER_MESSAGE as QWEN_MAX_FILES
from web.rate_limit import web_rate_limit
from .view_helpers import _get_user_id

def ajax_arena_sessions(request):
    """Session-based AJAX wrapper for listing or creating chat sessions."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        sessions = ArenaChatSession.objects.filter(user=user, is_active=True).order_by('-updated_at')[:100]
        return JsonResponse({
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
                for s in sessions
            ]
        })

    elif request.method == 'POST':
        from api.arena_views import _community_model_meta
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        model_id = (data.get('modelId') or '').strip()
        title = (data.get('title') or '').strip()[:200]
        if not model_id:
            return JsonResponse({'error': 'modelId is required'}, status=400)

        community_meta = _community_model_meta(model_id)
        if not community_meta:
            return JsonResponse({'error': f'Unknown model: {model_id}'}, status=400)

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

        return JsonResponse({
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
            }
        }, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def ajax_arena_session_detail(request, session_id):
    """Session-based AJAX wrapper for getting, updating or deleting a chat session."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

    if sess.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if request.method == 'GET':
        msgs = list(sess.messages.order_by('created_at').prefetch_related('attachments'))
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
        return JsonResponse({
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

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        new_title = data.get('title')
        if new_title is not None:
            sess.title = str(new_title).strip()[:200]
        if 'isActive' in data:
            sess.is_active = bool(data.get('isActive'))
        sess.updated_at = now_ms()
        sess.save(update_fields=['title', 'is_active', 'updated_at'])
        return JsonResponse({'ok': True, 'title': sess.title, 'isActive': sess.is_active})

    elif request.method == 'DELETE':
        sess.delete()
        return JsonResponse({'ok': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_send_message(request, session_id):
    """Session-based AJAX wrapper for sending a message and streaming the SSE response."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

    if sess.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    content = (data.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > 8000:
        return JsonResponse({'error': 'Message too long (max 8000 chars)'}, status=400)

    return sse_response(_stream_send(sess, content))

@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_regenerate(request, message_id):
    """Session-based AJAX wrapper for regenerating the last assistant response."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        target = ArenaChatMessage.objects.select_related('session').get(pk=message_id)
    except ArenaChatMessage.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

    if target.session.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if target.role != 'assistant':
        return JsonResponse({'error': 'Only assistant messages can be regenerated'}, status=400)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    return sse_response(_stream_regenerate(target.session, target.id))


# ========================= Qwen file-upload AJAX views =========================

def _json_body(request):
    try:
        return json.loads(request.body), None
    except ValueError:
        return None, JsonResponse({'error': 'Invalid JSON'}, status=400)


def _session_user(request):
    """The signed-in User for a POST, or (None, error response)."""
    user_id = _get_user_id(request)
    if not user_id:
        return None, JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None, JsonResponse({'error': 'User not found'}, status=404)
    if request.method != 'POST':
        return None, JsonResponse({'error': 'Method not allowed'}, status=405)
    return user, None


def _posted_message(request, session_id, provider, label, max_chars):
    """Owned session plus the posted text of a send request, or an error response."""
    user_id = _get_user_id(request)
    if not user_id:
        return None, None, JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return None, None, JsonResponse({'error': 'Session not found'}, status=404)
    if sess.user_id != user_id:
        return None, None, JsonResponse({'error': 'Forbidden'}, status=403)
    if request.method != 'POST':
        return None, None, JsonResponse({'error': 'Method not allowed'}, status=405)
    if sess.provider != provider:
        return None, None, JsonResponse(
            {'error': f'This endpoint only works with {label} sessions.'}, status=400,
        )
    content = (request.POST.get('content') or '').strip()
    if not content:
        return None, None, JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > max_chars:
        return None, None, JsonResponse(
            {'error': f'Message too long (max {max_chars} chars)'}, status=400,
        )
    return sess, content, None


def ajax_arena_create_qwen_session(request):
    user, err = _session_user(request)
    if err:
        return err
    data, err = _json_body(request)
    if err:
        return err

    model_id = (data.get('modelId') or '').strip()
    title = (data.get('title') or '').strip()[:200]
    if not model_id:
        from api.qwen_utils.models import get_default_model
        model_id = get_default_model()

    sess = create_qwen_chat_session(user, model_id, title)
    if not sess:
        return JsonResponse({'error': 'Could not start Qwen session — try again'}, status=502)
    return JsonResponse({'session': qwen_session_payload(sess)}, status=201)


@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_send_message_qwen(request, session_id):
    """Multipart body: content plus up to five files."""
    sess, content, err = _posted_message(request, session_id, 'qwen', 'Qwen', QWEN_MAX_CONTENT_CHARS)
    if err:
        return err
    files = request.FILES.getlist('files')
    if len(files) > QWEN_MAX_FILES:
        return JsonResponse({'error': f'Too many files (max {QWEN_MAX_FILES})'}, status=400)
    uploaded = upload_named_files((f.name, f.read()) for f in files) if files else []
    return qwen_turn_response(sess, content, uploaded)


# ========================= DeepAI Chat AI AJAX views =========================

def ajax_arena_deepai_models(request):
    return JsonResponse({'models': deepai_proxy.get_models(), 'provider': 'deepai'})


def ajax_arena_create_deepai_session(request):
    user, err = _session_user(request)
    if err:
        return err
    data, err = _json_body(request)
    if err:
        return err

    model_id = (data.get('modelId') or 'standard').strip()
    title = (data.get('title') or '').strip()[:200]
    try:
        sess, info = create_deepai_chat_session(user, model_id, title)
    except deepai_proxy.DeepAIError as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    return JsonResponse({'session': deepai_session_payload(sess, info)}, status=201)


@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_send_message_deepai(request, session_id):
    """Multipart body: content plus up to ten image or document files."""
    sess, content, err = _posted_message(
        request, session_id, 'deepai', 'DeepAI', DEEPAI_MAX_CONTENT_CHARS,
    )
    if err:
        return err
    files = request.FILES.getlist('files')[:DEEPAI_MAX_FILES]
    return deepai_turn_response(sess, content, upload_attachments((f.name, f.read()) for f in files))
