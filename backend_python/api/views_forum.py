"""Views Forum extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from .models import PostImage, PostMedia, Poll, PollOption, PollVote
from . import notifications as _notif
from .security import (
    save_post_image_upload, save_forum_media_upload, validate_forum_attachments,
    POST_IMAGE_MAX_COUNT,
)
from . import services


def _client_wants_anonymous(request) -> bool:
    """isAnonymous / is_anonymous from either JSON body or multipart form."""
    value = request.data.get('isAnonymous', request.data.get('is_anonymous', False))
    if isinstance(value, str):
        return value.strip().lower() in ('1', 'true', 'yes', 'on')
    return bool(value)


def _attach_forum_media(target, attachments, now):
    """persist validated attachment descriptors as PostMedia rows."""
    kind_attr = 'post' if isinstance(target, Post) else 'reply'
    for order, item in enumerate(attachments):
        PostMedia.objects.create(
            id=str(uuid.uuid4()),
            kind=item['kind'], url=item['url'], name=item['name'],
            mime_type=item['mime_type'], size_bytes=item['size_bytes'],
            order=order, created_at=now,
            **{kind_attr: target},
        )


def _parse_attachments_or_error(request):
    """Returns (attachments, error_response)."""
    try:
        return validate_forum_attachments(request.data.get('attachments')), None
    except ValidationError as exc:
        messages = exc.messages if hasattr(exc, 'messages') else [str(exc)]
        return None, Response({'error': messages[0] if messages else 'Invalid attachments'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([UploadRateThrottle])
def forum_media_upload(request):
    """POST /api/forum/uploads/ — one video/audio/file, returns the descriptor
    the client echoes back inside the post/reply `attachments` payload."""
    user, err = _require_verified_user(request)
    if err:
        return err
    file_obj = request.FILES.get('file')
    try:
        descriptor = save_forum_media_upload(request, file_obj)
    except ValidationError as exc:
        messages = exc.messages if hasattr(exc, 'messages') else [str(exc)]
        return Response({'error': messages[0] if messages else 'Invalid file'}, status=400)
    return Response({'ok': True, 'attachment': descriptor}, status=201)


@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def posts_create(request):
    """POST /api/posts"""
    user, err = _require_verified_user(request)
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

    attachments, error_response = _parse_attachments_or_error(request)
    if error_response:
        return error_response

    now = _now_ms()
    post = Post.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        title=title,
        content=content,
        category=category,
        thumbs_up_count=0,
        reply_count=0,
        is_anonymous=_client_wants_anonymous(request),
        created_at=now,
    )
    if attachments:
        _attach_forum_media(post, attachments, now)

    logger.info("posts_create: created post %s by user %s", post.id, user.username)
    _counters.increment_user_post_count(user.id)
    _notif.send_mention_all_if_eligible(user, f'{title} {content}', 'post', post.id)
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
        if 'title' in data:
            err = _validate_text_length(str(data['title']).strip(), MAX_POST_TITLE_LENGTH, 'Title')
            if err:
                return err
        if 'content' in data:
            err = _validate_text_length(str(data['content']).strip(), MAX_POST_CONTENT_LENGTH, 'Content')
            if err:
                return err
        image_urls = data.get('image_urls', data.get('images', None))
        cleaned_image_urls = None
        if image_urls is not None:
            if not isinstance(image_urls, list):
                return Response({'error': 'image_urls must be a list'}, status=400)
            cleaned_image_urls = []
            for raw_url in image_urls:
                url = str(raw_url or '').strip()
                if url:
                    cleaned_image_urls.append(url)
            if len(cleaned_image_urls) > POST_IMAGE_MAX_COUNT:
                return Response({'error': f'Maximum {POST_IMAGE_MAX_COUNT} images per post'}, status=400)
        now = _now_ms()
        if 'title' in data:
            title = str(data['title']).strip()
            EditHistory.objects.create(
                id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                field='title', old_value=post.title, new_value=title,
                edited_by=user, edited_at=now
            )
            post.title = title
        if 'content' in data:
            content = str(data['content']).strip()
            EditHistory.objects.create(
                id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                field='content', old_value=post.content, new_value=content,
                edited_by=user, edited_at=now
            )
            post.content = content
        if 'category' in data:
            category = str(data['category']).strip()
            EditHistory.objects.create(
                id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                field='category', old_value=post.category, new_value=category,
                edited_by=user, edited_at=now
            )
            post.category = category
        if cleaned_image_urls is not None:
            old_urls = list(PostImage.objects.filter(post=post).order_by('order', 'created_at').values_list('image_url', flat=True))
            if old_urls != cleaned_image_urls:
                EditHistory.objects.create(
                    id=str(uuid.uuid4()), target_type='post', target_id=post.id,
                    field='images', old_value='\n'.join(old_urls), new_value='\n'.join(cleaned_image_urls),
                    edited_by=user, edited_at=now
                )
                PostImage.objects.filter(post=post).delete()
                for order, url in enumerate(cleaned_image_urls):
                    PostImage.objects.create(
                        id=str(uuid.uuid4()), post=post, image_url=url, order=order, created_at=now
                    )
        if 'attachments' in data:
            cleaned_attachments, error_response = _parse_attachments_or_error(request)
            if error_response:
                return error_response
            PostMedia.objects.filter(post=post).delete()
            if cleaned_attachments:
                _attach_forum_media(post, cleaned_attachments, now)
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

    _rt.broadcast_post_like_changed(post_id, current_count, is_thumbed_up_by_viewer_hint=is_thumbed_up, user_id=str(user.id))
    return Response({'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up})

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def replies_create(request, post_id):
    """POST /api/posts/<postId>/replies"""
    user, err = _require_verified_user(request)
    if err:
        return err

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    content = request.data.get('content', '').strip()
    parent_reply_id = request.data.get('parentReplyId', None)

    err = _validate_text_length(content, MAX_REPLY_CONTENT_LENGTH, 'Content')
    if err:
        return err

    if parent_reply_id and not Reply.objects.filter(pk=parent_reply_id, post_id=post_id).exists():
        return Response({'error': 'Invalid parent reply'}, status=400)

    attachments, error_response = _parse_attachments_or_error(request)
    if error_response:
        return error_response
    # Voice notes / attachments can be the entire reply.
    if not content and not attachments:
        return Response({'error': 'Content is required'}, status=400)
    anonymous = _client_wants_anonymous(request)

    now = _now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=str(uuid.uuid4()),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            is_anonymous=anonymous,
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)
        if attachments:
            _attach_forum_media(reply, attachments, now)

    logger.info("replies_create: created reply on post %s by user %s", post_id, user.username)
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id, anonymous_actor=anonymous)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id, anonymous_actor=anonymous)
    _notif.send_mention_all_if_eligible(user, content, 'reply', reply.id)
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

    _rt.broadcast_reply_like_changed(reply.post_id, reply_id, current_count, is_thumbed_up_by_viewer_hint=is_thumbed_up, user_id=str(user.id))
    return Response({'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up})

@api_view(['GET'])
@permission_classes([AllowAny])
def edit_history(request, target_type, target_id):
    """GET /api/edit-history/<target_type>/<target_id>/ — edit history for a post or reply."""
    if target_type not in ('post', 'reply'):
        return Response({'error': 'Invalid target_type'}, status=400)
    entries = EditHistory.objects.filter(
        target_type=target_type, target_id=target_id
    ).select_related('edited_by').order_by('-edited_at')[:20]
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
        posts = Post.objects.select_related('user').filter(is_archived=False, user__email_verified=True)

        username = request.query_params.get('username')
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        sort = (request.query_params.get('sort') or 'new').strip().lower()
        if sort not in ('hot', 'new', 'top', 'discussed'):
            sort = 'new'

        if username:
            posts = posts.filter(user__username__iexact=username)
        if category:
            posts = posts.filter(category__iexact=category)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        if sort == 'top':
            posts = posts.order_by('-thumbs_up_count', '-created_at')
        elif sort == 'discussed':
            posts = posts.order_by('-reply_count', '-created_at')
        else:
            # 'new' and 'hot' both pre-sort by recency; 'hot' re-ranks the page below.
            posts = posts.order_by('-created_at')

        response = _paginated_response(request, posts, PostSerializer, context={'request': request})
        if sort == 'hot' and isinstance(response.data, dict):
            results = response.data.get('results')
            if isinstance(results, list):
                import math
                import time as _time
                now_ms_val = int(_time.time() * 1000)

                def _hot_score(p):
                    engagement = (p.get('thumbsUpCount', 0) * 3
                                  + p.get('replyCount', 0) * 2
                                  + min(p.get('viewCount', 0) or 0, 1000) * 0.1)
                    age_hours = max(0.0, (now_ms_val - (p.get('createdAt') or 0)) / 3600000.0)
                    if engagement <= 0:
                        return -age_hours / 168.0
                    return math.log2(max(engagement, 1)) - age_hours / 168.0

                response.data['results'] = sorted(results, key=_hot_score, reverse=True)
        return response

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

    attachments, error_response = _parse_attachments_or_error(request)
    if error_response:
        return error_response

    result = services.create_post(
        user, title, content, category,
        image_urls=image_urls, poll_data=poll_data,
        is_anonymous=_client_wants_anonymous(request), attachments=attachments,
    )
    if result:
        logger.info("posts_endpoint: created post %s by user %s", result['id'], user.username)
        post = Post.objects.select_related('user').get(pk=result['id'])
        return Response(PostSerializer(post, context={'request': request}).data, status=201)
    return Response({'error': 'Failed to create post'}, status=400)

@api_view(['GET', 'POST'])
def replies_endpoint(request, post_id):
    """
    GET  /api/posts/<postId>/replies  → list replies
    POST /api/posts/<postId>/replies  → create reply
    """
    if request.method == 'GET':
        replies = Reply.objects.filter(post_id=post_id, user__email_verified=True).select_related('user')
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

    err = _validate_text_length(content, MAX_REPLY_CONTENT_LENGTH, 'Content')
    if err:
        return err

    if parent_reply_id and not Reply.objects.filter(pk=parent_reply_id, post_id=post_id).exists():
        return Response({'error': 'Invalid parent reply'}, status=400)

    attachments, error_response = _parse_attachments_or_error(request)
    if error_response:
        return error_response
    # Voice notes / attachments can be the entire reply.
    if not content and not attachments:
        return Response({'error': 'Content is required'}, status=400)
    anonymous = _client_wants_anonymous(request)

    now = _now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=str(uuid.uuid4()),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            is_anonymous=anonymous,
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)
        if attachments:
            _attach_forum_media(reply, attachments, now)

    logger.info("replies_endpoint: created reply on post %s by user %s", post_id, user.username)
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id, anonymous_actor=anonymous)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id, anonymous_actor=anonymous)
    try:
        from .neby import enqueue_if_reply_mention
        enqueue_if_reply_mention(reply)
    except Exception:
        pass
    _notif.send_mention_all_if_eligible(user, content, 'reply', reply.id)
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
        return Response({'error': f'Maximum {POST_IMAGE_MAX_COUNT} images per post'}, status=400)
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