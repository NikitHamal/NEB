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
        existing = Bookmark.objects.filter(user=user, target_type=target_type, target_id=target_id).first()
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
    qs = Bookmark.objects.filter(user=user)
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

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def fcm_unregister(request):
    """POST /api/fcm/unregister — remove FCM token(s) from the current user on logout."""
    user, err = _require_user(request)
    if err:
        return err
    token = request.data.get('token', '').strip()
    if token:
        FCMToken.objects.filter(token=token, user=user).delete()
    else:
        FCMToken.objects.filter(user=user).delete()
    return Response({'success': True})

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def search_all(request):
    """GET /api/search?q=query — unified search across resources, posts and people."""
    query = request.query_params.get('q', '').strip()
    tab = (request.query_params.get('tab') or 'all').strip().lower()
    subject = (request.query_params.get('subject') or '').strip()
    grade = (request.query_params.get('grade') or '').strip()
    rtype = (request.query_params.get('type') or '').strip()
    requesting_user = _get_user_from_request(request)


    if not query:
        return Response({'resources': [], 'posts': [], 'users': []})

    import re
    import operator
    from functools import reduce
    from django.db.models import Value, BooleanField, Case, When
    from .badges import user_badge_info

    terms = [t for t in re.sub(r'[^\w\s]', ' ', query).split() if t]
    resources = Resource.objects.none()
    posts = Post.objects.none()
    users = User.objects.none()

    if terms:
        if tab in ('all', 'resources'):
            res_q_list = []
            for term in terms:
                res_q_list.append(
                    Q(title__icontains=term) | Q(description__icontains=term) | Q(subject__icontains=term) |
                    Q(grade_level__icontains=term) | Q(faculty__icontains=term) | Q(program__icontains=term) |
                    Q(school__icontains=term) | Q(tags__icontains=term)
                )
            resources = Resource.objects.filter(
                reduce(operator.and_, res_q_list),
                approval_status='approved',
                is_lead=True
            )
            if subject:
                resources = resources.filter(subject__iexact=subject)
            if grade:
                resources = resources.filter(grade_level__iexact=grade)
            if rtype:
                resources = resources.filter(type__iexact=rtype)
            exact_res_expr = (
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(subject__icontains=query) | Q(tags__icontains=query)
            )
            resources = resources.annotate(
                is_exact=Case(
                    When(exact_res_expr, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).order_by('-is_exact', '-added_at')

        if tab in ('all', 'posts'):
            post_q_list = []
            for term in terms:
                post_q_list.append(
                    Q(title__icontains=term) | Q(content__icontains=term) | Q(category__icontains=term) |
                    Q(user__username__icontains=term) | Q(user__display_name__icontains=term)
                )
            posts = Post.objects.select_related('user').filter(
                reduce(operator.and_, post_q_list),
                is_archived=False,
            )
            if subject:
                posts = posts.filter(category__iexact=subject)
            exact_post_expr = Q(title__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query)
            posts = posts.annotate(
                is_exact=Case(
                    When(exact_post_expr, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).order_by('-is_exact', '-created_at')

        if tab in ('all', 'people', 'users') and requesting_user and requesting_user.is_authenticated:
            user_q_list = []
            for term in terms:
                user_q_list.append(
                    Q(username__icontains=term) | Q(display_name__icontains=term) | Q(bio__icontains=term) |
                    Q(school__icontains=term) | Q(class_level__icontains=term) | Q(subjects__icontains=term)
                )
            users = User.objects.filter(reduce(operator.and_, user_q_list), is_locked=False, email_verified=True).order_by('-follower_count', 'username')[:30]

    resource_page = _paginated_response(
        request, resources, ResourceSerializer, context={'request': request}, default_page_size=25, max_page_size=50
    )
    post_page = _paginated_response(
        request, posts, PostSerializer, context={'request': request}, default_page_size=25, max_page_size=50
    )

    following_ids = set()
    user_list = list(users)
    if requesting_user and user_list:
        following_ids = set(Follow.objects.filter(
            follower=requesting_user, following_id__in=[u.id for u in user_list]
        ).values_list('following_id', flat=True))

    serialized_users = []
    for user in user_list:
        from .services import avatar_or_photo_url
        serialized_users.append({
            'id': str(user.id),
            'username': user.username,
            'display_name': user.display_name or '',
            'photo_url': avatar_or_photo_url(user) or '',
            'bio': user.bio or '',
            'school': user.school or '',
            'class_level': user.class_level or '',
            'follower_count': user.follower_count or 0,
            'is_following': bool(user.id in following_ids),
            'is_self': bool(requesting_user and requesting_user.id == user.id),
            'badge_info': user_badge_info(user),
        })

    return Response({
        'resources': resource_page.data.get('results', []),
        'posts': post_page.data.get('results', []),
        'users': serialized_users,
    })

@api_view(['POST'])
@throttle_classes([ReportRateThrottle])
def report_create(request):
    """POST /api/reports — submit a content/user report."""
    user, err = _require_user(request)
    if err:
        return err

    target_type = str(request.data.get('target_type', '') or '').strip()
    target_id = str(request.data.get('target_id', '') or '').strip()
    reason = str(request.data.get('reason', 'other') or 'other').strip()
    description = str(request.data.get('description', '') or '').strip()

    valid_types = {'post', 'reply', 'user', 'resource'}
    if target_type not in valid_types:
        return Response({'error': f'target_type must be one of: {", ".join(sorted(valid_types))}'}, status=400)
    if not target_id:
        return Response({'error': 'target_id is required'}, status=400)
    if reason not in dict(Report.REASON_CHOICES):
        return Response({'error': 'Invalid reason'}, status=400)

    target_exists = {
        'post': lambda pk: Post.objects.filter(pk=pk).exists(),
        'reply': lambda pk: Reply.objects.filter(pk=pk).exists(),
        'user': lambda pk: User.objects.filter(pk=pk).exists(),
        'resource': lambda pk: Resource.objects.filter(pk=pk).exists(),
    }[target_type](target_id)
    if not target_exists:
        return Response({'error': 'Reported target no longer exists'}, status=404)

    detail_lines = []
    if description:
        detail_lines.append(description)
    context_path = str(request.data.get('context_path', '') or request.data.get('screen', '') or '').strip()
    app_version = str(request.data.get('app_version', '') or '').strip()
    platform = str(request.data.get('platform', '') or 'android').strip()
    if context_path:
        detail_lines.append(f'Context: {context_path[:300]}')
    if platform:
        detail_lines.append(f'Platform: {platform[:80]}')
    if app_version:
        detail_lines.append(f'App version: {app_version[:80]}')
    description = '\n\n'.join(detail_lines)

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
    GET /api/realtime/config — public discovery endpoint for mobile and web clients.

    Returns the public WebSocket URL and, when the request is authenticated via
    session cookie, a short-lived signed ticket for cross-domain (trycloudflare)
    WebSocket auth. Web clients refetch this on every reconnect so a tunnel
    restart + ticket rotation is picked up without a page reload.
    """
    import os as _os
    from django.conf import settings as _settings
    from django.core.cache import cache as _cache
    from django.core.signing import TimestampSigner as _Signer
    # Resolve WS URL using the same newest-mtime logic as the page renderer
    ws_url = _os.environ.get('WS_PUBLIC_URL', '').strip()
    if not ws_url and hasattr(_settings, 'WS_PUBLIC_URL'):
        ws_url = (_settings.WS_PUBLIC_URL or '').strip()
    if not ws_url:
        try:
            import glob as _glob, re as _re
            candidates = []
            base_dir = _os.path.dirname(_os.path.dirname(__file__))
            paths = [
                '/home/consicac/nebians_api/logs/start_ws_tunnel.log',
                _os.path.join(base_dir, 'logs', 'cloudflared.log'),
                '/home/consicac/nebians_api/logs/cloudflared.log',
            ] + sorted(_glob.glob('/tmp/cf_quick*.log'), reverse=True)
            for path in paths:
                try:
                    with open(path, 'r', errors='ignore') as fh:
                        content = fh.read()
                    matches = _re.findall(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)', content)
                    if matches:
                        host = matches[-1].rstrip('/').rstrip('/ws').rstrip('/')
                        url = 'wss://' + host + '/ws/'
                        try:
                            mtime = _os.path.getmtime(path)
                        except OSError:
                            mtime = 0
                        candidates.append((mtime, url))
                except OSError:
                    continue
            if candidates:
                candidates.sort(key=lambda x: x[0], reverse=True)
                ws_url = candidates[0][1]
            else:
                # Fallback ws_url.txt cache
                try:
                    with open(_os.path.join(base_dir, 'ws_url.txt'), 'r', errors='ignore') as fh:
                        content = fh.read().strip()
                    if content:
                        m = _re.search(r'([a-z0-9-]+\.trycloudflare\.com)', content)
                        if m:
                            ws_url = 'wss://' + m.group(1) + '/ws/'
                        elif content.startswith('wss://'):
                            ws_url = content.strip()
                except OSError:
                    pass
        except Exception:
            ws_url = ''
    if ws_url:
        try:
            from nebians.tunnel_health import is_tunnel_healthy
            if not is_tunnel_healthy():
                ws_url = ''
        except Exception:
            pass
    # Generate a fresh ticket when the caller is authenticated and the tunnel is cross-domain.
    ticket = ''
    if ws_url and 'trycloudflare.com' in ws_url:
        user_id = None
        # 1) DRF's request.user if session auth succeeded (when authentication not empty)
        try:
            u = getattr(request, 'user', None)
            if u and getattr(u, 'is_authenticated', False) and not getattr(u, 'is_locked', False):
                user_id = str(u.pk if hasattr(u, 'pk') else u.id)
        except Exception:
            pass
        # 2) Fallback: resolve via session token (web cookies don't go through DRF auth here because we AllowAny)
        if not user_id:
            try:
                from web.view_helpers import _get_user_id as _resolve_uid
                uid = _resolve_uid(request)
                if uid:
                    user_id = str(uid)
            except Exception:
                pass
        if user_id:
            try:
                ticket = _Signer(salt='ws-ticket').sign(user_id)
            except Exception:
                ticket = ''
    return Response({'ws_url': ws_url, 'ticket': ticket, 'heartbeat_interval': 25})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def analytics_track(request):
    """
    POST /api/analytics/track/

    Mobile app analytics tracking endpoint. Called by the Android app
    when a user views a screen (since the middleware only captures web requests).
    Body: { path, referrer?, utm_source?, utm_medium?, utm_campaign?, platform? }
    """
    import time as _time
    try:
        path = request.data.get('path', '') or ''
        if not path or len(path) > 2000:
            return Response({'status': 'ignored'})
        referrer = request.data.get('referrer', '') or ''
        utm_source = request.data.get('utm_source', '') or ''
        utm_medium = request.data.get('utm_medium', '') or ''
        utm_campaign = request.data.get('utm_campaign', '') or ''
        app_platform = request.data.get('platform', '') or ''

        from nebians.middleware import _classify_referrer, _detect_platform
        from urllib.parse import urlparse

        own_domain = request.get_host().split(':')[0].lower()
        referrer_domain = ''
        if referrer:
            try:
                referrer_domain = urlparse(referrer).hostname or ''
            except Exception:
                pass
        referrer_type = _classify_referrer(referrer_domain, own_domain)
        platform = app_platform or _detect_platform(request.META.get('HTTP_USER_AGENT', ''))

        user_agent = request.META.get('HTTP_USER_AGENT', '') or ''

        user_id = None
        user, _ = _require_user(request)
        if user and not isinstance(user, Response):
            try:
                user_id = int(user.id) if str(user.id).isdigit() else None
                if user_id is not None:
                    try:
                        from api.models import User as UserModel
                        now_ms = int(_time.time() * 1000)
                        UserModel.objects.filter(pk=str(user_id)).update(last_active=now_ms)
                        from django.core.cache import cache
                        cache.sadd('presence:online', str(user_id))
                        cache.expire('presence:online', 300)
                        cache.set(f'presence:user:{str(user_id)}', now_ms, 300)
                    except Exception:
                        pass
            except (ValueError, TypeError):
                pass

        from api.models import PageView
        PageView.objects.create(
            path=path[:2000],
            full_url=request.build_absolute_uri(),
            referrer=referrer[:2000],
            referrer_domain=referrer_domain[:255],
            referrer_type=referrer_type,
            utm_source=utm_source[:255],
            utm_medium=utm_medium[:255],
            utm_campaign=utm_campaign[:255],
            user_agent=user_agent[:2000],
            source='app',
            platform=platform[:30],
            ip_address=request.META.get('REMOTE_ADDR'),
            session_key='',
            user_id=user_id,
            user_identifier=str(user_id) if user_id else '',
            created_at=int(_time.time() * 1000),
        )
        return Response({'status': 'ok'})
    except Exception:
        return Response({'status': 'error'}, status=500)
