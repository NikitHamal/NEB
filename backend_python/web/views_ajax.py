"""Views Ajax extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403

@require_POST
def ajax_like_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_post_like(user, post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    cache.delete_many(['home_posts', 'forum_all_posts'])
    return JsonResponse(result)

@require_POST
def ajax_like_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_reply_like(user, reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    return JsonResponse(result)

@require_POST
def ajax_create_reply(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentReplyId')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    if len(content) > 10000:
        return JsonResponse({'error': 'Content must be 10000 characters or fewer'}, status=400)
    result = services.create_reply(user, post_id, content, parent_id)
    if result:
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)

@require_POST
def ajax_like_resource(request, resource_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_resource_like(user, resource_id)
    except Resource.DoesNotExist:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    return JsonResponse(result)

@require_POST
def ajax_like_resource_comment(request, comment_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_resource_comment_like(user, comment_id)
    except ResourceComment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    return JsonResponse(result)

@require_POST
def ajax_resource_comment(request, resource_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentCommentId')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    result = services.create_resource_comment(user, resource_id, content, parent_id)
    if result:
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)

@require_POST
def ajax_delete_resource_comment(request, comment_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    is_admin = bool(user.is_admin)
    ok = services.delete_resource_comment(user, comment_id, is_admin=is_admin)
    if ok:
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Permission denied or comment not found'}, status=403)

@require_POST
def ajax_create_post(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    category = data.get('category', '').strip()
    image_urls = data.get('images', [])
    poll_data = data.get('poll')
    if len(title) > 200:
        return JsonResponse({'error': 'Title must be 200 characters or fewer'}, status=400)
    if len(content) > 20000:
        return JsonResponse({'error': 'Content must be 20000 characters or fewer'}, status=400)
    if image_urls and len(image_urls) > 3:
        return JsonResponse({'error': 'Maximum 3 images per post'}, status=400)
    if poll_data:
        options = poll_data.get('options', [])
        if len(options) < 2:
            return JsonResponse({'error': 'Poll must have at least 2 options'}, status=400)
        if len(options) > 6:
            return JsonResponse({'error': 'Poll can have at most 6 options'}, status=400)
        for opt in options:
            if not opt.strip():
                return JsonResponse({'error': 'Poll options cannot be empty'}, status=400)
            if len(opt.strip()) > 200:
                return JsonResponse({'error': 'Poll option must be 200 characters or fewer'}, status=400)
    result = services.create_post(user, title, content, category, image_urls=image_urls, poll_data=poll_data)
    if result:
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Missing fields'}, status=400)

@require_POST
def ajax_bookmark_toggle(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    target_type = data.get('target_type', '').strip()
    target_id = data.get('target_id', '').strip()
    if target_type not in ('post', 'reply', 'resource'):
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    if not target_id:
        return JsonResponse({'error': 'target_id required'}, status=400)
    if target_type == 'post':
        if not Post.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Post not found'}, status=404)
    elif target_type == 'reply':
        if not Reply.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Reply not found'}, status=404)
    elif target_type == 'resource':
        if not Resource.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Resource not found'}, status=404)
    existing = Bookmark.objects.filter(user=user, target_type=target_type, target_id=target_id).first()
    if existing:
        existing.delete()
        return JsonResponse({'isBookmarked': False})
    Bookmark.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        target_type=target_type,
        target_id=target_id,
        created_at=int(time.time() * 1000),
    )
    return JsonResponse({'isBookmarked': True})

@require_POST
def ajax_bookmark_check(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'isBookmarked': False})
    target_type = request.GET.get('target_type', '').strip()
    target_id = request.GET.get('target_id', '').strip()
    is_bookmarked = Bookmark.objects.filter(
        user_id=user_id, target_type=target_type, target_id=target_id
    ).exists()
    return JsonResponse({'isBookmarked': is_bookmarked})

@require_POST
def ajax_report(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    target_type = data.get('target_type', '').strip()
    target_id = data.get('target_id', '').strip()
    reason = data.get('reason', 'other').strip()
    description = data.get('description', '').strip()
    valid_types = {'post', 'reply', 'user', 'resource'}
    if target_type not in valid_types:
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    if not target_id:
        return JsonResponse({'error': 'target_id required'}, status=400)
    if reason not in dict(Report.REASON_CHOICES):
        return JsonResponse({'error': 'Invalid reason'}, status=400)
    if len(description) > 2000:
        return JsonResponse({'error': 'Description must be 2000 characters or fewer'}, status=400)
    report = Report.objects.create(
        id=str(uuid.uuid4()),
        reporter=user,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        description=description,
        status='open',
        created_at=int(time.time() * 1000),
    )
    logger.info("ajax_report: user %s reported %s/%s (reason=%s)", user.username, target_type, target_id, reason)
    return JsonResponse({'success': True, 'id': report.id})

@require_POST
def ajax_archive_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    reply.is_archived = not reply.is_archived
    reply.save(update_fields=['is_archived'])
    _clear_page_cache()
    _rt.broadcast_reply_deleted(reply.post_id, reply_id, deleted_by='archive')
    return JsonResponse({'success': True, 'isArchived': reply.is_archived})

@require_POST
def ajax_delete_post(request, post_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    try:
        _cleanup.delete_post_with_cleanup(post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    _clear_page_cache()
    _rt.broadcast_post_deleted(post_id)
    return JsonResponse({'success': True})

@require_POST
def ajax_edit_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    now = int(time.time() * 1000)
    if 'title' in data:
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='post', target_id=post.id,
            field='title', old_value=post.title, new_value=data['title'].strip(),
            edited_by_id=user_id, edited_at=now
        )
        post.title = data['title'].strip()
    if 'content' in data:
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='post', target_id=post.id,
            field='content', old_value=post.content, new_value=data['content'].strip(),
            edited_by_id=user_id, edited_at=now
        )
        post.content = data['content'].strip()
    if 'category' in data:
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='post', target_id=post.id,
            field='category', old_value=post.category, new_value=data['category'].strip(),
            edited_by_id=user_id, edited_at=now
        )
        post.category = data['category'].strip()
    post.is_edited = True
    post.edited_at = now
    post.save()
    _clear_page_cache()
    _rt.broadcast_post_updated(post.id, {
        'title': post.title, 'content': post.content, 'category': post.category,
        'is_edited': True, 'edited_at': now,
    })
    return JsonResponse(_serialize_post(post, user_id))

@require_POST
def ajax_archive_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    post.is_archived = not post.is_archived
    post.save(update_fields=['is_archived'])
    _clear_page_cache()
    _rt.broadcast_post_deleted(post_id)
    return JsonResponse({'success': True, 'isArchived': post.is_archived})

@require_POST
def ajax_edit_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    now = int(time.time() * 1000)
    EditHistory.objects.create(
        id=str(uuid.uuid4()), target_type='reply', target_id=reply.id,
        field='content', old_value=reply.content, new_value=content,
        edited_by_id=user_id, edited_at=now
    )
    reply.content = content
    reply.is_edited = True
    reply.edited_at = now
    reply.save()
    _clear_page_cache()
    _rt.broadcast_reply_updated(reply.post_id, reply.id, {
        'content': reply.content, 'is_edited': True, 'edited_at': now,
    })
    return JsonResponse(_serialize_reply(reply, user_id))

@require_POST
def ajax_delete_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    try:
        _cleanup.delete_reply_with_cleanup(reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    _clear_page_cache()
    _rt.broadcast_reply_deleted(reply.post_id, reply_id, deleted_by=str(user_id))
    return JsonResponse({'success': True})

def ajax_edit_history(request, target_type, target_id):
    if target_type not in ('post', 'reply'):
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    entries = EditHistory.objects.filter(target_type=target_type, target_id=target_id).select_related('edited_by')
    data = []
    for e in entries:
        data.append({
            'id': e.id, 'field': e.field, 'oldValue': e.old_value, 'newValue': e.new_value,
            'editedByUsername': e.edited_by.username, 'editedByPhotoUrl': e.edited_by.photo_url or '',
            'editedAt': e.edited_at,
        })
    return JsonResponse(data, safe=False)

def ajax_reply_thread(request, reply_id):
    user_id = _get_user_id(request)
    try:
        parent = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    parent_data = _serialize_reply(parent, user_id)
    parent_data['authorFollowed'] = False
    if user_id and parent.user_id != user_id:
        parent_data['authorFollowed'] = Follow.objects.filter(
            follower_id=user_id, following_id=parent.user_id
        ).exists()
    all_descendants = Reply.objects.select_related('user').filter(
        post_id=parent.post_id, parent_reply__isnull=False
    ).order_by('created_at')
    all_replies = _serialize_replies(all_descendants, user_id)
    id_to_reply = {r['id']: r for r in all_replies}
    children_map = {}
    for r in all_replies:
        pid = r['parentReplyId']
        children_map.setdefault(pid, []).append(r)
    def build_tree(parent_id):
        children = children_map.get(parent_id, [])
        for child in children:
            child['children'] = build_tree(child['id'])
        return children
    thread_replies = build_tree(reply_id)
    return JsonResponse({
        'parent': parent_data,
        'replies': thread_replies,
    }, safe=False)

def ajax_user_popup(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    is_private = bool(u.is_locked)
    data = {
        'id': u.id,
        'username': u.username,
        'displayName': u.display_name or u.username,
        'photoUrl': u.photo_url or '',
        'bio': '' if is_private else (u.bio or ''),
        'classLevel': '' if is_private else (u.class_level or ''),
        'isLocked': u.is_locked,
        'badgeInfo': _user_badge_info(u),
    }
    if not is_private:
        data['postCount'] = getattr(u, 'post_count', 0) or 0 or Post.objects.filter(user=u).count()
        data['replyCount'] = getattr(u, 'reply_count', 0) or 0 or Reply.objects.filter(user=u).count()
        data['followerCount'] = getattr(u, 'follower_count', 0) or 0 or Follow.objects.filter(following=u).count()
    else:
        data['postCount'] = 0
        data['replyCount'] = 0
        data['followerCount'] = 0
    user_id = _get_user_id(request)
    if user_id:
        data['isFollowing'] = Follow.objects.filter(follower_id=user_id, following_id=u.id).exists()
        data['isSelf'] = (user_id == u.id)
    else:
        data['isFollowing'] = False
        data['isSelf'] = False
    return JsonResponse(data)

def ajax_user_search(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse([], safe=False)
    users = User.objects.filter(
        username__icontains=q
    ).values('id', 'username', 'display_name', 'photo_url')[:8]
    results = []
    for u in users:
        results.append({
            'id': u['id'],
            'username': u['username'],
            'displayName': u['display_name'] or u['username'],
            'photoUrl': u['photo_url'] or '',
        })
    return JsonResponse(results, safe=False)

def ajax_check_username(request):
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'available': False})
    result = services.check_username_available(username)
    return JsonResponse(result)

@require_POST
def ajax_set_theme(request):
    try:
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        request.session['theme'] = 'dark' if theme == 'dark' else 'light'
    except (json.JSONDecodeError, KeyError):
        pass
    return JsonResponse({'status': 'ok'})

@require_POST
def ajax_follow_user(request, user_id):
    user_id_obj = _get_user_id(request)
    if not user_id_obj:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id_obj)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = services.toggle_follow(user, user_id)
    if isinstance(result, tuple):
        return JsonResponse(result[0], status=result[1])
    return JsonResponse(result)

def ajax_user_photos(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)

    from api.models import UserPhoto
    try:
        current_user = get_user_by_auth_token(token)
    except User.DoesNotExist:
        api.clear_session_auth(request)
        return JsonResponse({'error': 'Please log in again.'}, status=401)

    if request.method == 'GET':
        try:
            photos = UserPhoto.objects.filter(user=current_user)
            # Manual serialization to avoid DRF serializer context issues in vanilla Django views
            photos_data = []
            for photo in photos:
                photos_data.append({
                    'id': photo.id,
                    'url': photo.url,
                    'uploaded_at': photo.uploaded_at,
                    'is_current': photo.is_current,
                })
            return JsonResponse({'photos': photos_data})
        except Exception as e:
            logger.error("Failed to retrieve user photos: %s", e)
            return JsonResponse({'error': f"Failed to retrieve photos: {str(e)}"}, status=500)

    elif request.method == 'POST':
        from django.db import transaction

        file_obj = request.FILES.get('file')
        if file_obj:
            try:
                url = save_profile_image_upload(request, current_user, file_obj)
            except ValidationError as exc:
                return JsonResponse({'error': ' '.join(exc.messages)}, status=400)
        else:
            # Fallback to URL
            url = ''
            content_type = request.META.get('CONTENT_TYPE', '')
            if 'application/json' in content_type:
                try:
                    data = json.loads(request.body)
                    url = data.get('url', '').strip()
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON request'}, status=400)
            else:
                url = request.POST.get('url', '').strip()

            if not url:
                return JsonResponse({'error': 'Either URL or file is required'}, status=400)
            try:
                url = validate_profile_photo_url(url)
            except ValidationError as exc:
                return JsonResponse({'error': ' '.join(exc.messages)}, status=400)

        try:
            with transaction.atomic():
                UserPhoto.objects.filter(user=current_user).update(is_current=False)
                photo = UserPhoto.objects.create(
                    user=current_user,
                    url=url,
                    uploaded_at=int(time.time() * 1000),
                    is_current=True,
                )
                current_user.photo_url = url
                current_user.save(update_fields=['photo_url'])
        except Exception as e:
            logger.error("Failed to save user photo database record: %s", e)
            return JsonResponse({'error': f"Database error (run migrations on live server): {str(e)}"}, status=500)

        # Update user in session
        try:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = url
                user_data['photoUrl'] = url
                api.set_session_auth(request, token, user_data)
        except Exception as e:
            logger.error("Failed to update user session avatar: %s", e)

        return JsonResponse({
            'id': photo.id,
            'url': url,
            'uploaded_at': photo.uploaded_at,
            'is_current': True
        }, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@require_POST
def ajax_set_password(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    password = data.get('password', '')
    if not password or len(password) < 8:
        return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
    result, status_code = services.set_password(user, password)
    if result.get('status') == 'success':
        _clear_page_cache()
        user_data = _normalize_user_data(UserSerializer(user).data)
        user_data['hasPassword'] = True
        api.set_session_auth(request, api.get_session_token(request), user_data)
        return JsonResponse({'status': 'success', 'message': 'Password set successfully'})
    return JsonResponse({'error': result.get('error', 'Failed to set password')}, status=status_code or 400)

@require_POST
def ajax_change_password(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    current_password = data.get('currentPassword', '')
    new_password = data.get('newPassword', '')
    if not current_password or not new_password:
        return JsonResponse({'error': 'Current password and new password are required'}, status=400)
    result, status_code = services.change_password(user, current_password, new_password)
    if result.get('status') == 'success':
        _clear_page_cache()
        new_token = result.get('authToken') or api.get_session_token(request)
        user_data = _normalize_user_data(UserSerializer(user).data)
        api.set_session_auth(request, new_token, user_data)
        return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})
    return JsonResponse({'error': result.get('error', 'Failed to change password')}, status=status_code or 400)

@require_POST
def ajax_activate_photo(request, photo_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = services.activate_photo(user, photo_id)
    if result:
        new_url = result.get('photo_url') or result.get('url')
        if new_url:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = new_url
                user_data['photoUrl'] = new_url
                token = api.get_session_token(request)
                if token:
                    api.set_session_auth(request, token, user_data)
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_upload_post_image(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    file_obj = request.FILES.get('image')
    if not file_obj:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    from api.security import save_post_image_upload
    try:
        url = save_post_image_upload(request, user, file_obj)
    except DjangoValidationError as e:
        return JsonResponse({'error': str(e.message)}, status=400)
    return JsonResponse({'url': url})


@require_POST
def ajax_poll_vote(request, poll_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    option_id = data.get('option_id', '').strip()
    if not option_id:
        return JsonResponse({'error': 'Option ID is required'}, status=400)
    result, status_code = services.vote_poll(user, poll_id, option_id)
    if 'error' in result:
        return JsonResponse(result, status=status_code)
    return JsonResponse(result)
