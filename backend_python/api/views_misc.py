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
    qs = Bookmark.objects.filter(user=user).order_by('-created_at')
    if target_type:
        qs = qs.filter(target_type=target_type)

    paginator = PageNumberPagination()
    try:
        page_size = int(request.query_params.get('page_size', 50))
    except (TypeError, ValueError):
        page_size = 50
    paginator.page_size = max(1, min(page_size, 100))
    page = paginator.paginate_queryset(qs, request)

    # Batch-resolve target objects so the client can render rich cards without N+1 calls.
    resource_ids = [b.target_id for b in page if b.target_type == 'resource']
    post_ids = [b.target_id for b in page if b.target_type == 'post']
    resources = {r.id: r for r in Resource.objects.filter(pk__in=resource_ids)} if resource_ids else {}
    posts = {p.id: p for p in Post.objects.filter(pk__in=post_ids)} if post_ids else {}

    ctx = {'request': request}
    if post_ids:
        ctx['liked_post_ids'] = set(PostLike.objects.filter(
            user=user, post_id__in=post_ids
        ).values_list('post_id', flat=True))

    enriched = []
    for b in page:
        item = {
            'id': b.id,
            'target_type': b.target_type,
            'target_id': b.target_id,
            'created_at': b.created_at,
            'resource': None,
            'post': None,
        }
        if b.target_type == 'resource' and b.target_id in resources:
            item['resource'] = ResourceSerializer(resources[b.target_id]).data
        elif b.target_type == 'post' and b.target_id in posts:
            item['post'] = PostSerializer(posts[b.target_id], context=ctx).data
        enriched.append(item)

    return paginator.get_paginated_response(enriched)

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
    """
    user, err = _require_user(request)
    if err:
        return err

    qs = Notification.objects.filter(recipient=user).select_related('actor')

    unread_only = request.query_params.get('unread_only', '').lower() in ('1', 'true', 'yes')
    if unread_only:
        qs = qs.filter(is_read=False)

    return _paginated_response(request, qs, NotificationSerializer, default_page_size=30, max_page_size=100)

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
        return Response({'success': True, 'marked_count': count})

    if not notification_ids:
        return Response({'error': 'Provide notification_ids or mark_all=true'}, status=400)

    notifs = Notification.objects.filter(recipient=user, pk__in=notification_ids, is_read=False)
    count = notifs.update(is_read=True)
    # Recalculate unread count from DB
    unread = Notification.objects.filter(recipient=user, is_read=False).count()
    User.objects.filter(pk=user.id).update(unread_notification_count=unread)
    logger.info("notifications_mark_read: user %s marked %d notifications as read", user.username, count)
    return Response({'success': True, 'marked_count': count})

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
@throttle_classes([SearchRateThrottle])
def analytics_me(request):
    """
    GET /api/analytics/me — private learning analytics for the authenticated user.
    Mirrors the web `analytics()` dashboard (web/views_study_lab.py) as JSON.
    """
    from collections import Counter
    from django.db.models import Sum, Avg, Max
    from .models import (
        ResourceComment, StudyDocument, StudyQuiz, StudyQuizAttempt,
        StudyFlashcard, StudyFlashcardReview,
    )

    user, err = _require_user(request)
    if err:
        return err

    now = now_ms()
    day_ms = 86400000
    cutoff_30 = now - 30 * day_ms

    posts = Post.objects.filter(user=user, is_archived=False)
    replies = Reply.objects.filter(user=user, is_archived=False)
    resources = Resource.objects.filter(uploaded_by=user)
    resource_comments = ResourceComment.objects.filter(user=user)
    study_docs = StudyDocument.objects.filter(user=user)
    quizzes = StudyQuiz.objects.filter(user=user)
    quiz_attempts = StudyQuizAttempt.objects.filter(user=user)
    flashcards = StudyFlashcard.objects.filter(user=user)
    flash_reviews = StudyFlashcardReview.objects.filter(user=user)

    post_views = posts.aggregate(total=Sum('view_count')).get('total') or 0
    post_likes_received = posts.aggregate(total=Sum('thumbs_up_count')).get('total') or 0
    post_replies_received = posts.aggregate(total=Sum('reply_count')).get('total') or 0
    resource_views = resources.aggregate(total=Sum('view_count')).get('total') or 0
    resource_likes_received = resources.aggregate(total=Sum('like_count')).get('total') or 0
    resource_comments_received = resources.aggregate(total=Sum('comment_count')).get('total') or 0

    quiz_stats = quiz_attempts.aggregate(xp=Sum('xp_earned'))
    total_attempt_questions = quiz_attempts.aggregate(total=Sum('total_questions')).get('total') or 0
    total_attempt_score = quiz_attempts.aggregate(total=Sum('score')).get('total') or 0
    quiz_accuracy = round((total_attempt_score / total_attempt_questions) * 100) if total_attempt_questions else 0

    easy_reviews = flash_reviews.filter(confidence='easy').count()
    medium_reviews = flash_reviews.filter(confidence='medium').count()
    hard_reviews = flash_reviews.filter(confidence='hard').count()
    reviewed_total = easy_reviews + medium_reviews + hard_reviews

    today_start = now - (now % day_ms)
    activity_days = []
    max_activity = 1
    for i in range(13, -1, -1):
        start = today_start - i * day_ms
        end = start + day_ms
        counts = {
            'posts': posts.filter(created_at__gte=start, created_at__lt=end).count(),
            'replies': replies.filter(created_at__gte=start, created_at__lt=end).count(),
            'resources': resources.filter(added_at__gte=start, added_at__lt=end).count(),
            'study': quiz_attempts.filter(completed_at__gte=start, completed_at__lt=end).count()
                + flash_reviews.filter(last_reviewed_at__gte=start, last_reviewed_at__lt=end).count(),
        }
        total = sum(counts.values())
        max_activity = max(max_activity, total)
        activity_days.append({'label': 'Today' if i == 0 else f'{i}d', 'total': total, 'counts': counts, 'height': 8})
    for d in activity_days:
        d['height'] = max(8, round((d['total'] / max_activity) * 100)) if d['total'] else 8

    category_counter = Counter(posts.values_list('category', flat=True))
    subject_counter = Counter()
    for subject in resources.values_list('subject', flat=True):
        for part in (subject or '').split(','):
            part = part.strip()
            if part:
                subject_counter[part] += 1

    def _counter_rows(counter, limit=5):
        if not counter:
            return []
        max_count = max(counter.values()) or 1
        return [
            {'label': label, 'count': count, 'width': max(6, round((count / max_count) * 100))}
            for label, count in counter.most_common(limit)
        ]

    summaries_count = study_docs.filter(summary_compact__gt='').count() + study_docs.filter(summary_detailed__gt='').count()
    if not summaries_count:
        summaries_count = study_docs.exclude(summary='').count()
    mindmaps_count = study_docs.exclude(mindmap_json='').count()

    suggestions = []
    if study_docs.count() and summaries_count < study_docs.count():
        suggestions.append('Generate compact summaries for documents that still have no summary.')
    if study_docs.count() and mindmaps_count < study_docs.count():
        suggestions.append('Create mindmaps for your main notes to see topic relationships faster.')
    if quizzes.count() and not quiz_attempts.exists():
        suggestions.append('Take at least one generated quiz to start tracking exam readiness.')
    if quiz_attempts.exists() and quiz_accuracy < 70:
        suggestions.append('Review hard flashcards, then generate a fresh quiz from the same document.')
    if hard_reviews:
        suggestions.append(f"Revisit {hard_reviews} hard flashcard review{'' if hard_reviews == 1 else 's'} today.")
    if not resources.exists():
        suggestions.append('Upload one useful resource to build your contribution footprint.')
    if not suggestions:
        suggestions.append('Keep using Study Lab regularly; your recent learning loop looks healthy.')

    return Response({
        'stats': {
            'posts': posts.count(),
            'replies': replies.count(),
            'postViews': post_views,
            'postLikesReceived': post_likes_received,
            'postRepliesReceived': post_replies_received,
            'resources': resources.count(),
            'resourceViews': resource_views,
            'resourceLikesReceived': resource_likes_received,
            'resourceCommentsReceived': resource_comments_received,
            'resourceCommentsMade': resource_comments.count(),
            'followers': Follow.objects.filter(following=user).count(),
            'following': Follow.objects.filter(follower=user).count(),
            'bookmarks': Bookmark.objects.filter(user=user).count(),
            'studyDocs': study_docs.count(),
            'summaries': summaries_count,
            'mindmaps': mindmaps_count,
            'quizzes': quizzes.count(),
            'quizAttempts': quiz_attempts.count(),
            'quizAccuracy': quiz_accuracy,
            'quizXp': quiz_stats.get('xp') or 0,
            'flashcards': flashcards.count(),
            'flashReviews': reviewed_total,
            'easyReviews': easy_reviews,
            'mediumReviews': medium_reviews,
            'hardReviews': hard_reviews,
            'recentPosts': posts.filter(created_at__gte=cutoff_30).count(),
            'recentReplies': replies.filter(created_at__gte=cutoff_30).count(),
            'recentStudyActions': quiz_attempts.filter(completed_at__gte=cutoff_30).count()
                + flash_reviews.filter(last_reviewed_at__gte=cutoff_30).count(),
        },
        'activityDays': activity_days,
        'topCategories': _counter_rows(category_counter),
        'topSubjects': _counter_rows(subject_counter),
        'suggestions': suggestions[:5],
    })
