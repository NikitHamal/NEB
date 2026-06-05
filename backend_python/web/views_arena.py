"""Views Arena extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403

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
            
        now = int(time.time() * 1000)
        sess = ArenaChatSession.objects.create(
            id=str(uuid.uuid4()),
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
        msgs = list(sess.messages.order_by('created_at'))
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
            },
            'messages': [
                {
                    'id': m.id,
                    'role': m.role,
                    'content': m.content,
                    'parentId': m.parent_id,
                    'arenaMessageId': m.arena_message_id,
                    'finishReason': m.finish_reason,
                    'error': m.error,
                    'durationMs': m.duration_ms,
                    'createdAt': m.created_at,
                }
                for m in msgs
            ]
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
        sess.updated_at = int(time.time() * 1000)
        sess.save(update_fields=['title', 'is_active', 'updated_at'])
        return JsonResponse({'ok': True, 'title': sess.title, 'isActive': sess.is_active})
        
    elif request.method == 'DELETE':
        sess.delete()
        return JsonResponse({'ok': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

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
