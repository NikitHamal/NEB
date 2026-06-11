"""Views Misc extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def bookmark_toggle(request):
    """POST /api/bookmarks/toggle — toggle bookmark on a post, reply, or resource."""
    user, err = _require_user(request)
    if err:
        return err
    target_type = request.data.get('target_type', '').strip()
    target_id = request.data.get('target_id', '').strip()
    if target_type not in ('post', 'reply', 'resource'):
        return Response({'error': 'target_type must be post, reply, or resource'}, status=400)
    if not target_id:
        return Response({'error': 'target_id is required'}, status=400)
    if target_type == 'post':
        if not Post.objects.filter(pk=target_id).exists():
            return Response({'error': 'Post not found'}, status=404)
    elif target_type == 'reply':
        if not Reply.objects.filter(pk=target_id).exists():
            return Response({'error': 'Reply not found'}, status=404)
    elif target_type == 'resource':
        if not Resource.objects.filter(pk=target_id).exists():
            return Response({'error': 'Resource not found'}, status=404)
    try:
        with transaction.atomic():
            existing = Bookmark.objects.select_for_update().filter(user=user, target_type=target_type, target_id=target_id).first()
            if existing:
                existing.delete()
                return Response({'isBookmarked': False})
            Bookmark.objects.create(
                id=str(uuid.uuid4()),
                user=user,
                target_type=target_type,
                target_id=target_id,
                created_at=_now_ms(),
            )
            return Response({'isBookmarked': True})
    except IntegrityError:
        return Response({'isBookmarked': True})

@api_view(['GET'])
@throttle_classes([SearchRateThrottle])
def bookmark_list(request):
    """GET /api/bookmarks?target_type=post — list user's bookmarks, optionally filtered by type."""
    user, err = _require_user(request)
    if err:
        return err
    target_type = request.query_params.get('target_type', '').strip()
    qs = Bookmark.objects.filter(user=user).select_related('user')
    if target_type:
        qs = qs.filter(target_type=target_type)
    return _paginated_response(request, qs, BookmarkSerializer, default_page_size=50)

@api_view(['GET'])
@throttle_classes([SearchRateThrottle])
def bookmark_check(request):
    """GET /api/bookmarks/check?target_type=post&target_id=xxx — check if bookmarked."""
    user, err = _require_user(request)
    if err:
        return err
    target_type = request.query_params.get('target_type', '').strip()
    target_id = request.query_params.get('target_id', '').strip()
    is_bookmarked = Bookmark.objects.filter(
        user=user, target_type=target_type, target_id=target_id
    ).exists()
    return Response({'isBookmarked': is_bookmarked})

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def fcm_register(request):
    """POST /api/fcm/register — register an FCM push token for the authenticated user."""
    user, err = _require_user(request)
    if err:
        return err
    token = request.data.get('token', '').strip()
    if not token:
        return Response({'error': 'FCM token is required'}, status=400)
    if len(token) < 10 or len(token) > 512:
        return Response({'error': 'Invalid FCM token format'}, status=400)

    now = _now_ms()
    with transaction.atomic():
        existing = FCMToken.objects.select_for_update().filter(token=token).first()
        if existing:
            if existing.user_id != user.id:
                existing.user = user
                existing.created_at = now
                existing.save(update_fields=['user', 'created_at'])
        else:
            FCMToken.objects.create(token=token, user=user, created_at=now)

    return Response({'success': True})

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def search_all(request):
    """GET /api/search?q=query — unified search across resources and posts."""
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({'resources': [], 'posts': []})

    import re
    import operator
    from functools import reduce
    from django.db.models import Value, BooleanField, Case, When

    terms = [t for t in re.sub(r'[^\w\s]', ' ', query).split() if t]
    if terms:
        res_q_list = []
        for term in terms:
            res_q_list.append(
                Q(title__icontains=term) | Q(description__icontains=term) | Q(subject__icontains=term)
            )
        resources = Resource.objects.filter(
            reduce(operator.and_, res_q_list),
            approval_status='approved',
            is_lead=True
        )
        exact_res_expr = Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__icontains=query)
        resources = resources.annotate(
            is_exact=Case(
                When(exact_res_expr, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('-is_exact', '-added_at')

        post_q_list = []
        for term in terms:
            post_q_list.append(
                Q(title__icontains=term) | Q(content__icontains=term)
            )
        posts = Post.objects.select_related('user').filter(
            reduce(operator.and_, post_q_list),
            is_archived=False,
        )
        exact_post_expr = Q(title__icontains=query) | Q(content__icontains=query)
        posts = posts.annotate(
            is_exact=Case(
                When(exact_post_expr, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('-is_exact', '-created_at')
    else:
        resources = Resource.objects.none()
        posts = Post.objects.none()

    resource_page = _paginated_response(request, resources, ResourceSerializer, default_page_size=25, max_page_size=50)
    post_page = _paginated_response(request, posts, PostSerializer, context={'request': request}, default_page_size=25, max_page_size=50)

    return Response({
        'resources': resource_page.data.get('results', []),
        'posts': post_page.data.get('results', []),
    })

@api_view(['POST'])
@throttle_classes([ReportRateThrottle])
def report_create(request):
    """POST /api/reports — submit a content/user report."""
    user, err = _require_user(request)
    if err:
        return err

    target_type = request.data.get('target_type', '').strip()
    target_id = request.data.get('target_id', '').strip()
    reason = request.data.get('reason', 'other').strip()
    description = request.data.get('description', '').strip()

    valid_types = {'post', 'reply', 'user', 'resource'}
    if target_type not in valid_types:
        return Response({'error': f'target_type must be one of: {", ".join(sorted(valid_types))}'}, status=400)
    if not target_id:
        return Response({'error': 'target_id is required'}, status=400)
    if reason not in dict(Report.REASON_CHOICES):
        return Response({'error': 'Invalid reason'}, status=400)

    err = _validate_text_length(description, MAX_REPORT_DESCRIPTION_LENGTH, 'Description')
    if err:
        return err

    report = Report.objects.create(
        id=str(uuid.uuid4()),
        reporter=user,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        description=description,
        status='open',
        created_at=_now_ms(),
    )
    logger.info("report_create: user %s reported %s/%s (reason=%s)", user.username, target_type, target_id, reason)
    return Response(ReportSerializer(report).data, status=201)

@api_view(['GET'])
def notifications_list(request):
    """
    GET /api/notifications — list current user's notifications.
    Query params: page, page_size, unread_only (bool)
    Returns: { "notifications": [...], "has_more": bool }
    """
    user, err = _require_user(request)
    if err:
        return err

    qs = Notification.objects.filter(recipient=user).select_related('actor')

    unread_only = request.query_params.get('unread_only', '').lower() in ('1', 'true', 'yes')
    if unread_only:
        qs = qs.filter(is_read=False)

    paginator = PageNumberPagination()
    try:
        page_size = int(request.query_params.get('page_size', 30))
    except (TypeError, ValueError):
        page_size = 30
    paginator.page_size = max(1, min(page_size, 100))
    page = paginator.paginate_queryset(qs, request)
    serializer = NotificationSerializer(page, many=True)
    return Response({
        'notifications': serializer.data,
        'has_more': page.has_next() if hasattr(page, 'has_next') else False
    })

@api_view(['POST'])
def notifications_mark_read(request):
    """
    POST /api/notifications/mark-read
    Body: { "notification_ids": ["id1", "id2", ...] }  OR  { "mark_all": true }
    Marks specific or all notifications as read.
    """
    user, err = _require_user(request)
    if err:
        return err

    mark_all = request.data.get('mark_all', False)
    notification_ids = request.data.get('notification_ids', [])

    if mark_all:
        count = Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
        _counters.reset_user_unread_notification_count(user.id)
        logger.info("notifications_mark_read: user %s marked all %d notifications as read", user.username, count)
        return Response({'status': 'ok', 'message': f'{count} notification(s) marked as read'})

    if not notification_ids:
        return Response({'status': 'error', 'message': 'Provide notification_ids or mark_all=true'}, status=400)

    notifs = Notification.objects.filter(recipient=user, pk__in=notification_ids, is_read=False)
    count = notifs.update(is_read=True)
    # Recalculate unread count from DB
    unread = Notification.objects.filter(recipient=user, is_read=False).count()
    User.objects.filter(pk=user.id).update(unread_notification_count=unread)
    logger.info("notifications_mark_read: user %s marked %d notifications as read", user.username, count)
    return Response({'status': 'ok', 'message': f'{count} notification(s) marked as read'})

@api_view(['GET'])
def notifications_unread_count(request):
    """
    GET /api/notifications/unread-count — returns { "count": N }
    Uses the denormalized counter for speed.
    """
    user, err = _require_user(request)
    if err:
        return err
    count = getattr(user, 'unread_notification_count', 0) or 0
    return Response({'count': count})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def realtime_config(request):
    """
    GET /api/realtime/config — public discovery endpoint for mobile clients.

    Returns the public WebSocket URL so native apps (Android) can connect to
    the realtime layer without scraping HTML pages.
    """
    import os as _os
    ws_url = _os.environ.get('WS_PUBLIC_URL', '').strip()
    if not ws_url:
        try:
            import glob as _glob
            import re as _re
            for path in sorted(_glob.glob('/tmp/cf_quick*.log'), reverse=True):
                try:
                    with open(path, 'r', errors='ignore') as fh:
                        matches = _re.findall(r'https://[a-z0-9-]+\.trycloudflare\.com', fh.read())
                    if matches:
                        ws_url = matches[-1].replace('https://', 'wss://') + '/ws/'
                        break
                except OSError:
                    continue
        except Exception:
            ws_url = ''
    return Response({'ws_url': ws_url, 'heartbeat_interval': 25})
