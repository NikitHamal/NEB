"""Views Arena extracted from views.py."""
import json
import os

from django.http import StreamingHttpResponse, JsonResponse

from .view_helpers import *  # noqa: F401,F403
from web.rate_limit import web_rate_limit


def _sse_format(obj):
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def _sse_done_marker():
    return "data: [DONE]\n\n"

def ajax_arena_sessions(request):
    """Session-based AJAX wrapper for listing or creating AI4Bharat Arena sessions."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    from api import ai4bharat_proxy as arena
    from api.models import ArenaChatSession

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
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        model_id = (data.get('modelId') or '').strip()
        title = (data.get('title') or '').strip()[:200]
        if not model_id:
            return JsonResponse({'error': 'modelId is required'}, status=400)
            
        try:
            entry = arena.acquire_token(require_low_budget=True)
        except arena.ArenaRateLimit:
            return JsonResponse({'error': 'AI pool capacity reached', 'code': 'pool_exhausted'}, status=503)
        except arena.ArenaError as e:
            logger.error("ajax_arena_sessions create: token mint failed: %s", e)
            return JsonResponse({'error': 'AI service temporarily unavailable'}, status=503)
            
        model_meta = None
        try:
            all_models = arena.list_models(entry['token'])
            model_meta = next((m for m in all_models if m.get('id') == model_id), None)
        except Exception:
            pass
            
        try:
            remote = arena.create_session(entry['token'], model_id)
        except arena.ArenaAuthError:
            try:
                fresh = arena._new_anonymous_token()
                remote = arena.create_session(fresh['token'], model_id)
                entry = fresh
            except Exception as e:
                logger.error("ajax_arena_sessions create fallback failed: %s", e)
                return JsonResponse({'error': 'AI service temporarily unavailable'}, status=503)
        except arena.ArenaRateLimit as e:
            return JsonResponse({'error': str(e), 'code': 'pool_exhausted'}, status=503)
        except arena.ArenaError as e:
            logger.error("ajax_arena_sessions create failed: %s", e)
            return JsonResponse({'error': 'Could not start AI session — try again'}, status=502)
            
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
            }
        }, status=201)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def ajax_arena_session_detail(request, session_id):
    """Session-based AJAX wrapper for getting, updating or deleting a chat session."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    from api.models import ArenaChatSession

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
        
    from api.models import ArenaChatSession

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
        
    from api.arena_views import _stream_send
    
    gen = _stream_send(sess, content)
    response = StreamingHttpResponse(gen, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response

@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_regenerate(request, message_id):
    """Session-based AJAX wrapper for regenerating the last assistant response."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    from api.models import ArenaChatMessage

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
        
    from api.arena_views import _stream_regenerate
    
    gen = _stream_regenerate(target.session, target.id)
    response = StreamingHttpResponse(gen, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= Qwen file-upload AJAX views =========================

def ajax_arena_create_qwen_session(request):
    """Session-based AJAX wrapper for creating a Qwen chat session (with file upload support)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from api import qwen_proxy

    model_id = (data.get('modelId') or '').strip()
    title = (data.get('title') or '').strip()[:200]
    if not model_id:
        from api.qwen_utils.models import get_default_model
        model_id = get_default_model()

    qwen_session, qwen_cookies = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.31'

    chat_id = qwen_proxy.create_chat(qwen_session, model=model_id, _pool_session=qwen_session)
    if not chat_id:
        return JsonResponse({'error': 'Could not start Qwen session — try again'}, status=502)

    from api.models import ArenaChatSession

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
            'provider': 'qwen',
        }
    }, status=201)


@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_send_message_qwen(request, session_id):
    """Session-based AJAX wrapper for sending a Qwen message with optional file attachments.

    Accepts multipart/form-data:
      - content: text message (required)
      - files: uploaded files (optional, max 5)
    """
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    from api.models import ArenaChatSession

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

    if sess.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if sess.provider != 'qwen':
        return JsonResponse({'error': 'This endpoint only works with Qwen sessions.'}, status=400)

    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > 8000:
        return JsonResponse({'error': 'Message too long (max 8000 chars)'}, status=400)

    from api.qwen_utils.file_upload import (
        upload_file_from_bytes, classify_file, ALLOWED_EXTENSIONS, MAX_FILE_SIZE,
        MAX_FILES_PER_MESSAGE,
    )
    from api.models import ArenaChatMessage, ArenaChatAttachment
    from api import qwen_proxy

    # Handle file uploads
    files = request.FILES.getlist('files')
    uploaded_file_objs = []
    if files:
        if len(files) > MAX_FILES_PER_MESSAGE:
            return JsonResponse({'error': f'Too many files (max {MAX_FILES_PER_MESSAGE})'}, status=400)

        arena_qwen_session, _ = qwen_proxy._get_session()
        midtoken = qwen_proxy.get_midtoken(arena_qwen_session)
        if midtoken:
            arena_qwen_session.headers['bx-umidtoken'] = midtoken
            arena_qwen_session.headers['bx-v'] = '2.5.31'
        req_headers = dict(arena_qwen_session.headers)

        for f in files:
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue
            if f.size > MAX_FILE_SIZE:
                continue

            file_data = f.read()
            file_obj = upload_file_from_bytes(f.name, file_data, arena_qwen_session, req_headers)
            if file_obj:
                uploaded_file_objs.append(file_obj)

    # Pre-insert user message
    now = now_ms()
    user_msg_id = uuid_str()
    asst_msg_id = uuid_str()
    asst_started_at = now

    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    # Persist attachments
    if uploaded_file_objs:
        user_msg = ArenaChatMessage.objects.get(pk=user_msg_id)
        for fobj in uploaded_file_objs:
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
                created_at=now,
            )

    # SSE streaming response
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
            qwen_session.headers['bx-v'] = '2.5.31'

        chat_id = sess.qwen_chat_id
        model = sess.model_id or 'qwen3.7-plus'

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