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


# ========================= eGov Chat AI AJAX views =========================

def ajax_arena_egov_models(request):
    """Session-based AJAX wrapper for listing eGov models."""
    from api import egov_proxy
    models = egov_proxy.get_models()
    return JsonResponse({'models': models, 'provider': 'egov'})


def ajax_arena_create_egov_session(request):
    """Session-based AJAX wrapper for creating an eGov chat session."""
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

    from api import egov_proxy
    from api.models import ArenaChatSession

    model_id = (data.get('modelId') or 'AI1').strip()
    title = (data.get('title') or '').strip()[:200]

    scope, resolved_model = egov_proxy.resolve_scope_and_model(model_id)

    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider='egov',
        arena_session_id=f'egov:{_secrets_token_hex(16)}',
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
            'provider': 'egov',
            'scope': scope,
        },
    }, status=201)


def _secrets_token_hex(n=16):
    import secrets as _s
    return _s.token_hex(n)


@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_send_message_egov(request, session_id):
    """Session-based AJAX wrapper for sending an eGov message with optional file attachments.

    Accepts multipart/form-data:
      - content: text message (required)
      - files: up to 5 file attachments (optional, images and PDFs)
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

    if sess.provider != 'egov':
        return JsonResponse({'error': 'This endpoint only works with eGov sessions.'}, status=400)

    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > 8000:
        return JsonResponse({'error': 'Message too long (max 8000 chars)'}, status=400)

    from api import egov_proxy
    from api.models import ArenaChatMessage, ArenaChatAttachment

    # Handle file uploads
    uploaded_cdn_urls = []
    files = request.FILES.getlist('files')
    if files:
        scope, resolved_model = egov_proxy.resolve_scope_and_model(sess.model_id)
        for f in files[:5]:
            ext = os.path.splitext(f.name)[1].lower()
            if resolved_model == 'AI2':
                allowed_exts = {'.jpg', '.jpeg', '.png', '.gif'}
            else:
                allowed_exts = {'.jpg', '.jpeg', '.png', '.heif', '.pdf'}
            if ext not in allowed_exts:
                continue
            file_data = f.read()
            file_obj = egov_proxy.upload_file_from_bytes(f.name, file_data, model=resolved_model)
            if file_obj and file_obj.get('cdnUrl'):
                uploaded_cdn_urls.append({
                    'type': 'image',
                    'image': file_obj['cdnUrl'],
                    'original_filename': file_obj.get('original_filename', f.name),
                    'mime_type': file_obj.get('mime_type', ''),
                })

    # Build history from previous messages
    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({'role': m.role, 'content': m.content})

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


# ========================= DeepAI Chat AI AJAX views =========================

def ajax_arena_deepai_models(request):
    """Session-based AJAX wrapper for listing DeepAI models."""
    from api import deepai_proxy
    models = deepai_proxy.get_models()
    return JsonResponse({'models': models, 'provider': 'deepai'})


def ajax_arena_create_deepai_session(request):
    """Session-based AJAX wrapper for creating a DeepAI chat session."""
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

    from api import deepai_proxy
    from api.models import ArenaChatSession

    model_id = (data.get('modelId') or 'standard').strip()
    title = (data.get('title') or '').strip()[:200]

    try:
        resolved_model, info = deepai_proxy.resolve_model(model_id)
    except deepai_proxy.DeepAIError as exc:
        return JsonResponse({'error': str(exc)}, status=400)

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

    return JsonResponse({
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
    }, status=201)


@web_rate_limit('arena-send', limit=30, window=60)
def ajax_arena_send_message_deepai(request, session_id):
    """Session-based AJAX wrapper for sending a DeepAI message with optional file attachments.

    Accepts multipart/form-data:
      - content: text message (required)
      - files: up to 10 file attachments (optional, images and documents)
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

    if sess.provider != 'deepai':
        return JsonResponse({'error': 'This endpoint only works with DeepAI sessions.'}, status=400)

    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > 32000:
        return JsonResponse({'error': 'Message too long (max 32000 chars)'}, status=400)

    from api import deepai_proxy
    from api.models import ArenaChatMessage, ArenaChatAttachment

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
    asst_started_at = now

    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    # Persist attachments
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

    attachment_uuids = [att['uuid'] for att in uploaded_attachments if att.get('uuid')]

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


# ========================= EQing / EasyChat =========================

def ajax_arena_eqing_models(request):
    from api import eqing_proxy
    models = eqing_proxy.get_models()
    return JsonResponse({'models': models, 'provider': 'eqing'})


def ajax_arena_create_eqing_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    user = _require_web_user(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    model_id = (request.POST.get('modelId') or 'gpt-4o-mini').strip()
    title = (request.POST.get('title') or '').strip()[:200]

    resolved_model = eqing_proxy.resolve_model(model_id)

    model_info = None
    for m in eqing_proxy.ALL_MODELS:
        if m['id'] == resolved_model:
            model_info = m
            break

    display_name = (model_info or {}).get('name', f'EQing {resolved_model}')

    now = _now_ms()
    sess = ArenaChatSession.objects.create(
        id=_uuid_str(),
        user=user,
        provider='eqing',
        arena_session_id=f'eqing:{_secrets_token_hex(16)}',
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

    return JsonResponse({
        'session': {
            'id': sess.id,
            'title': sess.title,
            'modelId': sess.model_id,
            'modelCode': sess.model_code,
            'modelName': sess.model_display_name,
            'provider': 'eqing',
            'vision': (model_info or {}).get('vision', False),
            'thinking': (model_info or {}).get('thinking', False),
            'locked': (model_info or {}).get('locked', False),
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=201)


def ajax_arena_send_message_eqing(request, session_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    user = _require_web_user(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

    if sess.user_id != user.id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if sess.provider != 'eqing':
        return JsonResponse({'error': 'This endpoint only works with EQing sessions.'}, status=400)

    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)

    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({'role': m.role, 'content': m.content})

    now = _now_ms()
    user_msg_id = _uuid_str()
    asst_msg_id = _uuid_str()
    asst_started_at = _now_ms()

    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    def _stream_eqing():
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
            for chunk in eqing_proxy.stream_chat(
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
                    logger.warning("eqing stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("eqing stream: unexpected error: %s", e)
            yield _sse_format({
                'error': {'message': 'Internal streaming error', 'code': 'server'},
            })
            error_text = str(e)

        duration_ms = max(0, _now_ms() - asst_started_at)
        try:
            ArenaChatMessage.objects.filter(pk=asst_msg_id).update(
                content=collected_text,
                finish_reason=finish_reason,
                error=error_text[:200],
                duration_ms=duration_ms,
                arena_message_id=asst_msg_id,
            )
        except Exception as e:
            logger.exception("eqing: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=_now_ms(),
                    updated_at=_now_ms(),
                )
            except Exception as e:
                logger.warning("eqing: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_eqing(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= FreeGPT Arena Views =========================

def ajax_arena_freegpt_models(request):
    from api import freegpt_proxy
    models = freegpt_proxy.get_models()
    return JsonResponse({'models': models, 'provider': 'freegpt'})


def ajax_arena_create_freegpt_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    user = _require_web_user(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    model_id = (request.POST.get('modelId') or 'gpt-5-nano').strip()
    title = (request.POST.get('title') or '').strip()[:200]
    access_code = (request.POST.get('accessCode') or '').strip()

    display_name = f'FreeGPT {model_id}'

    now = _now_ms()
    sess = ArenaChatSession.objects.create(
        id=_uuid_str(),
        user=user,
        provider='freegpt',
        arena_session_id=f'freegpt:{_secrets_token_hex(16)}',
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

    return JsonResponse({
        'session': {
            'id': sess.id,
            'title': sess.title,
            'modelId': sess.model_id,
            'modelCode': sess.model_code,
            'modelName': sess.model_display_name,
            'provider': 'freegpt',
            'vision': any(v in model_id.lower() for v in ['vision', '-4o', '4.1', 'opus', 'sonnet']),
            'thinking': any(t in model_id.lower() for t in ['thinking', 'reasoner']),
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=201)


def ajax_arena_send_message_freegpt(request, session_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    user = _require_web_user(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

    if sess.user_id != user.id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if sess.provider != 'freegpt':
        return JsonResponse({'error': 'This endpoint only works with FreeGPT sessions.'}, status=400)

    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)

    access_code = (request.POST.get('accessCode') or '').strip()

    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({'role': m.role, 'content': m.content})

    from api import freegpt_proxy

    now = _now_ms()
    user_msg_id = _uuid_str()
    asst_msg_id = _uuid_str()
    asst_started_at = _now_ms()

    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    def _stream_freegpt():
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
            for chunk in freegpt_proxy.stream_chat(
                messages=history + [{'role': 'user', 'content': content}],
                model=sess.model_id,
                access_code=access_code,
            ):
                if 'error' in chunk:
                    error_text = chunk['error']
                    logger.warning("freegpt stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
                if 'text' in chunk:
                    text = chunk['text']
                    collected_text += text
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'content': text}}],
                    })
                if 'thinking' in chunk:
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'reasoning_content': chunk['thinking']}}],
                    })
        except Exception as e:
            logger.exception("freegpt stream: unexpected error: %s", e)
            yield _sse_format({
                'error': {'message': 'Internal streaming error', 'code': 'server'},
            })
            error_text = str(e)

        duration_ms = max(0, _now_ms() - asst_started_at)
        try:
            ArenaChatMessage.objects.filter(pk=asst_msg_id).update(
                content=collected_text,
                finish_reason=finish_reason,
                error=error_text[:200],
                duration_ms=duration_ms,
                arena_message_id=asst_msg_id,
            )
        except Exception as e:
            logger.exception("freegpt: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=_now_ms(),
                    updated_at=_now_ms(),
                )
            except Exception as e:
                logger.warning("freegpt: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_freegpt(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= DeepSeek AI (deep-seek.ai) =========================

def ajax_arena_deepseekai_models(request):
    from api import deepseekai_proxy
    models = deepseekai_proxy.get_models()
    return JsonResponse({'models': models, 'provider': 'deepseekai'})


def ajax_arena_create_deepseekai_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    user = _require_web_user(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    model_id = (request.POST.get('modelId') or 'deepseek/deepseek-v4-flash').strip()
    title = (request.POST.get('title') or '').strip()[:200]

    from api import deepseekai_proxy
    model_info = None
    for m in deepseekai_proxy.MODELS:
        if m['id'] == model_id:
            model_info = m
            break

    display_name = (model_info or {}).get('name', f'DeepSeek {model_id}')

    now = _now_ms()
    sess = ArenaChatSession.objects.create(
        id=_uuid_str(),
        user=user,
        provider='deepseekai',
        arena_session_id=f'deepseekai:{_secrets_token_hex(16)}',
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

    return JsonResponse({
        'session': {
            'id': sess.id,
            'title': sess.title,
            'modelId': sess.model_id,
            'modelCode': sess.model_code,
            'modelName': sess.model_display_name,
            'provider': 'deepseekai',
            'vision': (model_info or {}).get('vision', False),
            'thinking': (model_info or {}).get('thinking', False),
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=201)


def ajax_arena_send_message_deepseekai(request, session_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    user = _require_web_user(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

    if sess.user_id != user.id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if sess.provider != 'deepseekai':
        return JsonResponse({'error': 'This endpoint only works with DeepSeek AI sessions.'}, status=400)

    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)

    prev_messages = list(sess.messages.order_by('created_at'))
    history = []
    for m in prev_messages:
        if m.role in ('user', 'assistant'):
            history.append({'role': m.role, 'content': m.content})

    from api import deepseekai_proxy

    now = _now_ms()
    user_msg_id = _uuid_str()
    asst_msg_id = _uuid_str()
    asst_started_at = _now_ms()

    ArenaChatMessage.objects.create(
        id=user_msg_id, session=sess, role='user',
        content=content, parent_id='',
        arena_message_id='', finish_reason='', error='',
        duration_ms=0, created_at=now,
    )

    def _stream_deepseekai():
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
            for chunk in deepseekai_proxy.stream_chat(
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
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {'reasoning_content': chunk.get('content', '')}}],
                    })
                elif t == 'done':
                    finish_reason = chunk.get('finish_reason', 'stop')
                elif t == 'error':
                    error_text = chunk.get('error', 'upstream error')
                    logger.warning("deepseekai stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("deepseekai stream: unexpected error: %s", e)
            yield _sse_format({
                'error': {'message': 'Internal streaming error', 'code': 'server'},
            })
            error_text = str(e)

        duration_ms = max(0, _now_ms() - asst_started_at)
        try:
            ArenaChatMessage.objects.filter(pk=asst_msg_id).update(
                content=collected_text,
                finish_reason=finish_reason,
                error=error_text[:200],
                duration_ms=duration_ms,
                arena_message_id=asst_msg_id,
            )
        except Exception as e:
            logger.exception("deepseekai: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=_now_ms(),
                    updated_at=_now_ms(),
                )
            except Exception as e:
                logger.warning("deepseekai: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_deepseekai(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


# ========================= SurfSense (surfsense.com) =========================

def ajax_arena_surfsense_models(request):
    from api import surfsense_proxy
    models = surfsense_proxy.get_models()
    return JsonResponse({'models': models, 'provider': 'surfsense'})


def ajax_arena_create_surfsense_session(request):
    import json as _json
    user = _require_user(request)
    if isinstance(user, JsonResponse):
        return user

    body = {}
    try:
        body = _json.loads(request.body)
    except Exception:
        pass

    model_id = (body.get('modelId') or request.POST.get('modelId') or 'gpt-5.4-mini-no-login').strip()
    title = (body.get('title') or request.POST.get('title') or '').strip()[:200]

    from api import surfsense_proxy
    model_info = None
    for m in surfsense_proxy.MODELS:
        if m['id'] == model_id:
            model_info = m
            break

    display_name = (model_info or {}).get('name', f'SurfSense {model_id}')

    now = now_ms()
    sess = ArenaChatSession.objects.create(
        id=uuid_str(),
        user=user,
        provider='surfsense',
        arena_session_id=f'surfsense:{_secrets_token_hex(16)}',
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

    return JsonResponse({
        'session': {
            'id': sess.id,
            'title': sess.title,
            'modelId': sess.model_id,
            'modelCode': sess.model_code,
            'modelName': sess.model_display_name,
            'provider': 'surfsense',
            'vision': (model_info or {}).get('vision', False),
            'thinking': (model_info or {}).get('reasoning', False),
            'tools': (model_info or {}).get('web_search', True),
            'messageCount': 0,
            'createdAt': sess.created_at,
            'updatedAt': sess.updated_at,
        },
    }, status=201)


def ajax_arena_send_message_surfsense(request, session_id):
    user = _require_user(request)
    if isinstance(user, JsonResponse):
        return user
    sess, err = _get_owned_session(user, session_id)
    if err:
        return err

    if sess.provider != 'surfsense':
        return JsonResponse(
            {'error': 'This endpoint only works with SurfSense sessions.'},
            status=400,
        )

    body = {}
    try:
        body = json.loads(request.body)
    except Exception:
        pass

    content = (body.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > 32000:
        return JsonResponse({'error': 'Message too long (max 32000 chars)'}, status=400)

    web_search = body.get('webSearch', True)

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

    from api import surfsense_proxy

    def _stream_surfsense():
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
            for chunk in surfsense_proxy.stream_chat(
                messages=history + [{'role': 'user', 'content': content}],
                model=sess.model_id,
                web_search=web_search,
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
                elif t == 'tool_call':
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {
                            'tool_call': {
                                'id': chunk.get('id', ''),
                                'name': chunk.get('name', ''),
                                'arguments': chunk.get('arguments', {}),
                            }
                        }}],
                    })
                elif t == 'tool_result':
                    yield _sse_format({
                        'choices': [{'index': 0, 'delta': {
                            'tool_result': {
                                'id': chunk.get('id', ''),
                                'output': chunk.get('output', {}),
                            }
                        }}],
                    })
                elif t == 'done':
                    finish_reason = chunk.get('finish_reason', 'stop')
                elif t == 'error':
                    error_text = chunk.get('error', 'upstream error')
                    logger.warning("surfsense stream: upstream error: %s", error_text)
                    yield _sse_format({
                        'error': {'message': error_text, 'code': 'upstream'},
                    })
                    break
        except Exception as e:
            logger.exception("surfsense stream: unexpected error: %s", e)
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
            logger.exception("surfsense: failed to finalize assistant row: %s", e)

        if not error_text:
            try:
                ArenaChatSession.objects.filter(pk=sess.id).update(
                    message_count=sess.message_count + 1,
                    last_message_at=now_ms(),
                    updated_at=now_ms(),
                )
            except Exception as e:
                logger.warning("surfsense: counter commit failed: %s", e)

        if not error_text:
            yield _sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield _sse_done_marker()

    response = StreamingHttpResponse(_stream_surfsense(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response