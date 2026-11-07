"""Views Misc extracted from views.py."""
import uuid
from django.db import IntegrityError, transaction
from django.db.models import Q
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import counters as _counters
from .models import Bookmark, FCMToken, Follow, Notification, Post, Reply, Report, Resource, User
from .serializers import (
    BookmarkSerializer,
    NotificationSerializer,
    PostSerializer,
    ReportSerializer,
    ResourceSerializer,
)
from .throttles import (
    AuthRateThrottle,
    ReportRateThrottle,
    SearchRateThrottle,
    WriteActionRateThrottle,
)
from .view_helpers import (
    MAX_REPORT_DESCRIPTION_LENGTH,
    _get_user_from_request,
    _now_ms,
    _page_results,
    _page_rows,
    _paginated_response,
    _require_user,
    _validate_text_length,
    logger,
)

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
    if not FCMToken.objects.filter(token=token).update(user=user, created_at=now):
        try:
            with transaction.atomic():
                FCMToken.objects.create(token=token, user=user, created_at=now)
        except IntegrityError:
            FCMToken.objects.filter(token=token).update(user=user, created_at=now)

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

    # Only the rows go back to the client, so neither list pays for a COUNT(*) of every
    # match (a second full LIKE scan of resources and of posts).
    resource_results = _page_results(
        request, resources, ResourceSerializer, context={'request': request}, default_page_size=25, max_page_size=50
    )
    post_results = _page_results(
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
        'resources': resource_results,
        'posts': post_results,
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

    try:
        page_size = int(request.query_params.get('page_size', 30))
    except (TypeError, ValueError):
        page_size = 30
    # No total is returned, so no COUNT(*) either; same pages, same 404 past the end. One
    # row past the page says whether there is another (the app stops paging on has_more).
    page, has_more = _page_rows(request, qs, max(1, min(page_size, 100)), peek=True)
    serializer = NotificationSerializer(page, many=True)
    return Response({
        'notifications': serializer.data,
        'has_more': has_more,
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

    from . import push_engine
    if mark_all:
        push_engine.mark_all_opened_for_user(user.id, 'inbox')
        count = Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
        _counters.reset_user_unread_notification_count(user.id)
        logger.info("notifications_mark_read: user %s marked all %d notifications as read", user.username, count)
        return Response({'status': 'ok', 'message': f'{count} notification(s) marked as read'})

    if not notification_ids:
        return Response({'status': 'error', 'message': 'Provide notification_ids or mark_all=true'}, status=400)

    notifs = Notification.objects.filter(recipient=user, pk__in=notification_ids, is_read=False)
    push_engine.mark_opened(list(notifs.exclude(campaign_id='').values_list('id', flat=True)), 'inbox')
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
@throttle_classes([])
def realtime_config(request):
    """GET /api/realtime/config/ -- how this client opens its realtime stream.

    Hosted transport (Ably, see api/realtime_ably.py): returns a self-signed,
    subscribe-only token plus the SSE endpoint; the browser or app connects to
    Ably directly and this server holds no socket. Pure HMAC, no database, no
    network call, so it is cheap enough to be hit on every page.

    `ws_url` stays in the payload (empty unless WS_PUBLIC_URL is set) for older
    clients that still speak the self-hosted WebSocket.
    """
    import os as _os
    from django.conf import settings as _settings
    from . import realtime_ably

    ws_url = _os.environ.get('WS_PUBLIC_URL', '').strip()
    if not ws_url and hasattr(_settings, 'WS_PUBLIC_URL'):
        ws_url = (_settings.WS_PUBLIC_URL or '').strip()

    user_id = None
    try:
        u = getattr(request, 'user', None)
        if u and getattr(u, 'is_authenticated', False) and not getattr(u, 'is_locked', False):
            user_id = str(u.pk if hasattr(u, 'pk') else u.id)
    except Exception:
        user_id = None
    if not user_id:
        try:  # the app sends `Authorization: Bearer <token>`
            if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer '):
                bearer_user, bearer_err = _require_user(request)
                if not bearer_err and bearer_user is not None:
                    user_id = str(bearer_user.pk)
        except Exception:
            user_id = None
    if not user_id:
        try:
            from web.view_helpers import _get_user_id as _resolve_uid
            uid = _resolve_uid(request)
            if uid:
                user_id = str(uid)
        except Exception:
            user_id = None

    payload = {'ws_url': ws_url, 'ticket': '', 'heartbeat_interval': 25}
    try:
        shard = int(request.GET.get('shard', ''))
    except (TypeError, ValueError):
        shard = None
    hint = '%s|%s' % (
        (request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR') or '').split(',')[0].strip(),
        request.META.get('HTTP_USER_AGENT', '')[:80],
    )
    hosted = realtime_ably.client_config(user_id, shard=shard, hint=hint)
    if hosted:
        payload.update(hosted)
    else:
        payload['transport'] = 'ws' if ws_url else 'none'
    response = Response(payload)
    response['Cache-Control'] = 'private, no-store'
    return response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def analytics_track(request):
    """
    POST /api/analytics/track/

    Screen views from the mobile app (the middleware only sees web pages).
    Body: { path, referrer?, utm_source?, utm_medium?, utm_campaign?, platform? }

    Goes through the same pipeline as web hits (bot filter, hashed visitor,
    sessions, queued write), so app and web rows are directly comparable.
    """
    from nebians import analytics

    path = request.data.get('path', '') or ''
    if not isinstance(path, str) or not path.startswith('/') or len(path) > 2000 \
            or path.lower().startswith(analytics.events.SKIP_PREFIXES):
        return Response({'status': 'ignored'})
    user, _ = _require_user(request)
    if isinstance(user, Response):
        user = None
    event = analytics.event_from_request(
        request,
        path=path.split('?', 1)[0],
        referrer=str(request.data.get('referrer', '') or ''),
        utm={k: str(request.data.get(f'utm_{k}', '') or '') for k in ('source', 'medium', 'campaign')},
        force_app=True,
        app_platform=str(request.data.get('platform', '') or '')[:30],
        user=user,
    )
    if event:
        analytics.submit(event)
    return Response({'status': 'ok'})
