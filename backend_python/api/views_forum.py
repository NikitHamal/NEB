"""Views Forum extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from .models import PostImage, Poll, PollOption, PollVote
from .security import save_post_image_upload, POST_IMAGE_MAX_COUNT
from . import services

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def posts_create(request):
    """POST /api/posts"""
    user, err = _require_user(request)
    if err:
        return err

    title = request.data.get('title', '').strip()
    content = request.data.get('content', '').strip()
    category = request.data.get('category', '').strip()
    if not title or not content or not category:
        return Response({'error': 'Missing fields'}, status=400)

    err = _validate_text_length(title, MAX_POST_TITLE_LENGTH, 'Title')
    if err:
        return err
    err = _validate_text_length(content, MAX_POST_CONTENT_LENGTH, 'Content')
    if err:
        return err

    now = _now_ms()
    post = Post.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        title=title,
        content=content,
        category=category,
        thumbs_up_count=0,
        reply_count=0,
        created_at=now,
    )

    logger.info("posts_create: created post %s by user %s", post.id, user.username)
    _counters.increment_user_post_count(user.id)
    _rt.broadcast_post_created(PostSerializer(post, context={'request': request}).data)
    return Response(PostSerializer(post, context={'request': request}).data, status=201)

@api_view(['GET', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
def post_detail(request, post_id):
    """GET/PATCH/DELETE /api/posts/<postId>"""
    try:
        post = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    if request.method == 'DELETE':
        user, err = _require_user(request)
        if err:
            return err
        if post.user_id != user.id:
            return Response({'error': 'Forbidden'}, status=403)
        try:
            _cleanup.delete_post_with_cleanup(post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
        _rt.broadcast_post_deleted(post_id)
        logger.info("post_detail DELETE: deleted post %s by user %s", post_id, user.username)
        return Response({'success': True})

    if request.method == 'PATCH':
        user, err = _require_user(request)
        if err:
            return err
        if post.user_id != user.id:
            return Response({'error': 'Forbidden'}, status=403)
        data = request.data
        now = _now_ms()
        if 'title' in data:
            EditHistory.objects.create(
                id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                field='title', old_value=post.title, new_value=data['title'].strip(),
                edited_by=user, edited_at=now
            )
            post.title = data['title'].strip()
        if 'content' in data:
            EditHistory.objects.create(
                id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                field='content', old_value=post.content, new_value=data['content'].strip(),
                edited_by=user, edited_at=now
            )
            post.content = data['content'].strip()
        if 'category' in data:
            EditHistory.objects.create(
                id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                field='category', old_value=post.category, new_value=data['category'].strip(),
                edited_by=user, edited_at=now
            )
            post.category = data['category'].strip()
        post.is_edited = True
        post.edited_at = now
        post.save()
        return Response(PostSerializer(post, context={'request': request}).data)

    return Response(PostSerializer(post, context={'request': request}).data)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ViewIncrementRateThrottle])
def post_view(request, post_id):
    """POST /api/posts/<postId>/view — increment view_count."""
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    Post.objects.filter(pk=post_id).update(view_count=F('view_count') + 1)
    return Response({'view_count': post.view_count + 1})

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def post_like(request, post_id):
    """POST /api/posts/<postId>/like — toggle thumbs up."""
    user, err = _require_user(request)
    if err:
        return err

    with transaction.atomic():
        try:
            post = Post.objects.select_for_update().get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if created:
            Post.objects.filter(pk=post.pk).update(thumbs_up_count=F('thumbs_up_count') + 1)
            is_thumbed_up = True
            current_count = post.thumbs_up_count + 1
            _counters.increment_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.increment_user_likes_received(post.user_id)
            _notif.notify_post_liked(user.id, post_id)
        else:
            like.delete()
            Post.objects.filter(pk=post.pk, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(post.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.decrement_user_likes_received(post.user_id)
            _notif.notify_post_unliked(user.id, post_id)

    _rt.broadcast_post_like_changed(post_id, current_count)
    return Response({'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up})

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def replies_create(request, post_id):
    """POST /api/posts/<postId>/replies"""
    user, err = _require_user(request)
    if err:
        return err

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    content = request.data.get('content', '').strip()
    parent_reply_id = request.data.get('parentReplyId', None)
    if not content:
        return Response({'error': 'Content is required'}, status=400)

    err = _validate_text_length(content, MAX_REPLY_CONTENT_LENGTH, 'Content')
    if err:
        return err

    now = _now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=str(uuid.uuid4()),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)

    logger.info("replies_create: created reply on post %s by user %s", post_id, user.username)
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id)
    _rt.broadcast_reply_created(post_id, ReplySerializer(reply, context={'request': request}).data)
    return Response(ReplySerializer(reply, context={'request': request}).data, status=201)

@api_view(['DELETE', 'PATCH'])
def reply_detail(request, reply_id):
    """DELETE /api/replies/<replyId> — delete a reply. PATCH /api/replies/<replyId> — edit a reply."""
    user, err = _require_user(request)
    if err:
        return err
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return Response({'error': 'Reply not found'}, status=404)

    if reply.user_id != user.id:
        return Response({'error': 'Forbidden'}, status=403)

    if request.method == 'DELETE':
        try:
            _cleanup.delete_reply_with_cleanup(reply.id)
        except Reply.DoesNotExist:
            return Response({'error': 'Reply not found'}, status=404)
        _rt.broadcast_reply_deleted(reply.post_id, reply.id, deleted_by=str(user.id))
        return Response({'success': True})

    content = request.data.get('content', '').strip()
    if content:
        now = _now_ms()
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='reply', target_id=reply.id,
            field='content', old_value=reply.content, new_value=content,
            edited_by=user, edited_at=now
        )
        reply.content = content
        reply.is_edited = True
        reply.edited_at = now
        reply.save()
    return Response(ReplySerializer(reply, context={'request': request}).data)

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def reply_like(request, reply_id):
    """POST /api/replies/<replyId>/like — toggle thumbs up."""
    user, err = _require_user(request)
    if err:
        return err

    with transaction.atomic():
        try:
            reply = Reply.objects.select_for_update().get(pk=reply_id)
        except Reply.DoesNotExist:
            return Response({'error': 'Reply not found'}, status=404)
        like, created = ReplyLike.objects.get_or_create(reply=reply, user=user)
        if created:
            Reply.objects.filter(pk=reply.pk).update(thumbs_up_count=F('thumbs_up_count') + 1)
            is_thumbed_up = True
            current_count = reply.thumbs_up_count + 1
            _counters.increment_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.increment_user_likes_received(reply.user_id)
            _notif.notify_reply_liked(user.id, reply_id)
        else:
            like.delete()
            Reply.objects.filter(pk=reply.pk, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(reply.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.decrement_user_likes_received(reply.user_id)
            _notif.notify_reply_unliked(user.id, reply_id)

    _rt.broadcast_reply_like_changed(reply.post_id, reply_id, current_count)
    return Response({'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up})

@api_view(['GET'])
@permission_classes([AllowAny])
def edit_history(request, target_type, target_id):
    """GET /api/edit-history/<target_type>/<target_id>/ — edit history for a post or reply."""
    if target_type not in ('post', 'reply'):
        return Response({'error': 'Invalid target_type'}, status=400)
    entries = EditHistory.objects.filter(target_type=target_type, target_id=target_id).select_related('edited_by')
    return Response(EditHistorySerializer(entries, many=True).data)

@api_view(['GET', 'POST'])
def posts_endpoint(request):
    """
    GET  /api/posts  → list posts (with optional filtering/pagination)
    POST /api/posts  → create post

    GET query params:
      username — filter by author username (case-insensitive)
      category — filter by category (case-insensitive)
      search   — search in title + content (case-insensitive)
      page     — page number for pagination (endpoint is always paginated)
    """
    if request.method == 'GET':
        posts = Post.objects.select_related('user').filter(is_archived=False)

        username = request.query_params.get('username')
        category = request.query_params.get('category')
        search = request.query_params.get('search')

        if username:
            posts = posts.filter(user__username__iexact=username)
        if category:
            posts = posts.filter(category__iexact=category)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        return _paginated_response(request, posts, PostSerializer, context={'request': request})

    # POST — create
    user, err = _require_user(request)
    if err:
        return err

    title = request.data.get('title', '').strip()
    content = request.data.get('content', '').strip()
    category = request.data.get('category', '').strip()
    if not title or not content or not category:
        return Response({'error': 'Missing fields'}, status=400)

    err = _validate_text_length(title, MAX_POST_TITLE_LENGTH, 'Title')
    if err:
        return err
    err = _validate_text_length(content, MAX_POST_CONTENT_LENGTH, 'Content')
    if err:
        return err

    image_urls = request.data.get('image_urls', [])
    if image_urls and len(image_urls) > POST_IMAGE_MAX_COUNT:
        return Response({'error': f'Maximum {POST_IMAGE_MAX_COUNT} images per post'}, status=400)

    poll_data = None
    poll_raw = request.data.get('poll')
    if poll_raw:
        options = poll_raw.get('options', [])
        if len(options) < 2:
            return Response({'error': 'Poll must have at least 2 options'}, status=400)
        if len(options) > 6:
            return Response({'error': 'Poll can have at most 6 options'}, status=400)
        for opt in options:
            if not opt.strip():
                return Response({'error': 'Poll options cannot be empty'}, status=400)
        poll_data = {
            'question': poll_raw.get('question', ''),
            'duration_ms': int(poll_raw.get('duration_ms', 0) or 0),
            'options': [opt.strip() for opt in options],
        }

    result = services.create_post(user, title, content, category, image_urls=image_urls, poll_data=poll_data)
    if result:
        logger.info("posts_endpoint: created post %s by user %s", result['id'], user.username)
        return Response(result, status=201)
    return Response({'error': 'Failed to create post'}, status=400)

@api_view(['GET', 'POST'])
def replies_endpoint(request, post_id):
    """
    GET  /api/posts/<postId>/replies  → list replies
    POST /api/posts/<postId>/replies  → create reply
    """
    if request.method == 'GET':
        replies = Reply.objects.filter(post_id=post_id).select_related('user')
        return _paginated_response(request, replies, ReplySerializer, context={'request': request})

    # POST — create reply
    user, err = _require_user(request)
    if err:
        return err

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    content = request.data.get('content', '').strip()
    parent_reply_id = request.data.get('parentReplyId', None)
    if not content:
        return Response({'error': 'Content is required'}, status=400)

    err = _validate_text_length(content, MAX_REPLY_CONTENT_LENGTH, 'Content')
    if err:
        return err

    now = _now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=str(uuid.uuid4()),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)

    logger.info("replies_endpoint: created reply on post %s by user %s", post_id, user.username)
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id)
    try:
        from .neby import enqueue_if_reply_mention
        enqueue_if_reply_mention(reply)
    except Exception:
        pass
    _rt.broadcast_reply_created(post_id, ReplySerializer(reply, context={'request': request}).data)
    return Response(ReplySerializer(reply, context={'request': request}).data, status=201)


@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def post_images(request, post_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    if post.user_id != user.id:
        return Response({'error': 'Forbidden'}, status=403)
    existing_count = PostImage.objects.filter(post=post).count()
    files = request.data.getlist('images') if hasattr(request.data, 'getlist') else []
    if not files:
        return Response({'error': 'No images provided'}, status=400)
    if existing_count + len(files) > POST_IMAGE_MAX_COUNT:
        return Response({'error': 'Maximum 3 images per post'}, status=400)
    now = _now_ms()
    uploaded = []
    for i, f in enumerate(files):
        try:
            url = save_post_image_upload(request, user, f, order=existing_count + i)
            img = PostImage.objects.create(
                id=str(uuid.uuid4()),
                post=post,
                image_url=url,
                order=existing_count + i,
                created_at=now,
            )
            uploaded.append({'id': img.id, 'imageUrl': img.image_url, 'order': img.order})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    return Response({'images': uploaded}, status=201)


@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def poll_vote(request, poll_id):
    user, err = _require_user(request)
    if err:
        return err
    option_id = request.data.get('option_id', '').strip()
    if not option_id:
        return Response({'error': 'option_id is required'}, status=400)
    result, status_code = services.vote_poll(user, poll_id, option_id)
    if 'error' in result:
        return Response(result, status=status_code)
    return Response(result)
