"""Views Users extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from collections import Counter
from django.db.models import Count, Q, Sum
from .services import record_username_change
from .models import Bookmark, Notification, NEPAL_DISTRICTS, ResourceComment, StudyDocument, StudyQuiz, StudyQuizAttempt, StudyFlashcard, StudyFlashcardReview

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def check_username(request):
    """GET /api/users/check-username?username=<name>"""
    username = request.query_params.get('username', '').strip()
    if not username:
        return Response({'error': 'username query parameter is required'}, status=400)

    exists = User.objects.filter(username__iexact=username).exists()
    return Response({'available': not exists})

@api_view(['POST'])
def user_profile_create_or_update(request):
    """POST /api/users/profile — create or update the authenticated user's profile."""
    user, err = _require_verified_user(request)
    if err:
        return err

    data = request.data
    logger.info("user_profile: updating profile for user %s, data keys: %s", user.id, list(data.keys()))

    username = data.get('username', '').strip()
    dob = data.get('dob', '').strip()
    if not username or not dob:
        logger.warning("user_profile: missing username or dob (username=%s, dob=%s)", repr(username), repr(dob))
        return Response({'error': 'Username and Date of Birth are required'}, status=400)

    # Check username conflict with another user
    conflict = User.objects.filter(username__iexact=username).exclude(pk=user.id).exists()
    if conflict:
        logger.warning("user_profile: username conflict for '%s'", username)
        return Response({'error': 'Username already taken'}, status=409)

    if username != user.username:
        _v_err, _v_code = services.validate_username_change(user, username)
        if _v_err:
            return Response(_v_err, status=_v_code)
        user.username = username
        record_username_change(user)
    else:
        user.username = username

    email = data.get('email', '') or user.email or ''
    photo_url = data.get('photoUrl', '') or user.photo_url or ''
    if photo_url and not str(photo_url).startswith(request.build_absolute_uri('/media/')):
        try:
            photo_url = validate_profile_photo_url(photo_url)
        except ValidationError as exc:
            return Response({'error': ' '.join(exc.messages)}, status=400)
    banner_url = data.get('bannerUrl', '') or user.banner_url or ''
    if banner_url and not str(banner_url).startswith(request.build_absolute_uri('/media/')):
        try:
            banner_url = validate_external_https_url(banner_url)
        except ValidationError as exc:
            return Response({'error': ' '.join(exc.messages)}, status=400)
    display_name = data.get('displayName', '') or data.get('display_name', '') or user.display_name or ''
    gender = data.get('gender', '')
    class_level = data.get('classLevel', '') or data.get('class_level', '')
    subjects = data.get('subjects', '')
    pradesh = data.get('pradesh', '')
    district = data.get('district', '')
    if district and district not in NEPAL_DISTRICTS:
        district = ''
    school = data.get('school', '')
    school_username = data.get('schoolUsername', data.get('school_username', ''))
    bio = data.get('bio', '')
    is_locked = bool(data.get('isLocked', data.get('is_locked', False)))
    role = data.get('role', '').strip().lower() or user.role
    teaching_subjects = data.get('teachingSubjects', '') or data.get('teaching_subjects', '')
    institution_type = data.get('institutionType', '') or data.get('institution_type', '')

    user.username = username
    if email and email.lower() != (user.email or '').lower():
        user.email_verified = False
    user.email = email
    user.photo_url = photo_url
    user.banner_url = banner_url
    user.display_name = display_name
    user.dob = dob
    user.gender = gender
    user.class_level = class_level
    user.subjects = subjects
    user.pradesh = pradesh
    user.district = district
    user.school = school
    user.school_username = school_username
    user.bio = bio
    user.is_locked = is_locked
    if role in ('student', 'teacher', 'institution', 'explorer'):
        user.role = role
    user.teaching_subjects = teaching_subjects
    user.institution_type = institution_type
    user.save()

    logger.info("user_profile: profile saved for user %s (username=%s)", user.id, user.username)
    return Response({'status': 'success', 'user': UserSerializer(user).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile_get(request, username):
    """GET /api/users/profile/<username>"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    requesting_user = _get_user_from_request(request)
    if not _can_view_locked_profile(requesting_user, user):
        return Response(UserPublicSerializer(user).data)

    return Response(UserSerializer(user).data)

@api_view(['GET'])
def user_profile_stats(request, username):
    """
    GET /api/users/profile/<username>/stats
    Returns aggregated community stats. Public endpoint.
    Android app: call this alongside user_profile_get to populate the profile screen.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    requesting_user = _get_user_from_request(request)
    is_owner = bool(requesting_user and requesting_user.pk == user.pk)
    is_following = False
    is_requested = False
    if requesting_user and requesting_user.pk != user.pk:
        is_following = Follow.objects.filter(follower=requesting_user, following=user).exists()
        from .models import FollowRequest
        is_requested = FollowRequest.objects.filter(sender=requesting_user, receiver=user).exists()

    if not _can_view_locked_profile(requesting_user, user):
        return Response({
            'post_count': 0,
            'reply_count': 0,
            'likes_given': 0,
            'likes_received': 0,
            'contribution_score': 0,
            'follower_count': 0,
            'following_count': 0,
            'uploaded_resources_count': 0,
            'is_following': is_following,
            'is_requested': is_requested,
            'is_self': is_owner,
            'is_private': True,
        })

    stats = _build_stats(user)
    public_resource_filter = {} if is_owner else {'approval_status': 'approved'}
    stats['post_count'] = Post.objects.filter(user=user, is_archived=False, is_anonymous=False).count()
    stats['reply_count'] = Reply.objects.filter(user=user, is_archived=False, is_anonymous=False).count()
    stats['uploaded_resources_count'] = Resource.objects.filter(
        uploaded_by=user,
        is_lead=True,
        **public_resource_filter
    ).count()
    stats['is_following'] = is_following
    stats['is_requested'] = is_requested
    stats['is_self'] = is_owner
    stats['is_private'] = False
    if is_owner and user.is_locked:
        from .models import FollowRequest
        stats['follow_requests_count'] = FollowRequest.objects.filter(receiver=user).count()
    return Response(stats)



def _analytics_counter_rows(counter, limit=5):
    if not counter:
        return []
    rows = counter.most_common(limit)
    max_count = max([count for _, count in rows] or [1])
    return [
        {'label': label or 'General', 'count': count, 'width': max(8, round((count / max_count) * 100))}
        for label, count in rows
    ]


def _analytics_short_post(post):
    return {
        'id': post.id,
        'title': post.title,
        'category': post.category,
        'view_count': post.view_count,
        'like_count': post.thumbs_up_count,
        'reply_count': post.reply_count,
        'created_at': post.created_at,
    }


def _analytics_short_resource(resource):
    return {
        'id': resource.id,
        'title': resource.title,
        'subject': resource.subject,
        'type': resource.type,
        'view_count': resource.view_count,
        'like_count': resource.like_count,
        'comment_count': resource.comment_count,
        'added_at': resource.added_at,
    }


def _day_counts(field, days):
    """Count(...) aggregates, one per [start, end) window, keyed d0..dN."""
    return {f'd{i}': Count('pk', filter=Q(**{f'{field}__gte': start, f'{field}__lt': end}))
            for i, (start, end) in enumerate(days)}


@api_view(['GET'])
def user_private_analytics(request):
    user, err = _require_user(request)
    if err:
        return err

    now = now_ms()
    day_ms = 86400000
    cutoff_30 = now - 30 * day_ms
    today_start = now - (now % day_ms)
    # Oldest first: index 0 is 13 days ago, the last one is today.
    days = [(today_start - i * day_ms, today_start - i * day_ms + day_ms) for i in range(13, -1, -1)]

    posts = Post.objects.filter(user=user, is_archived=False)
    replies = Reply.objects.filter(user=user, is_archived=False)
    resources = Resource.objects.filter(uploaded_by=user, is_lead=True)
    resource_comments = ResourceComment.objects.filter(user=user)
    study_docs = StudyDocument.objects.filter(user=user)
    quizzes = StudyQuiz.objects.filter(user=user)
    quiz_attempts = StudyQuizAttempt.objects.filter(user=user)
    flashcards = StudyFlashcard.objects.filter(user=user)
    flash_reviews = StudyFlashcardReview.objects.filter(user=user)

    # One conditional aggregate per table instead of a COUNT/SUM per number (this view
    # used to run ~110 queries, 70 of them for the 14-day activity chart).
    post_agg = posts.aggregate(total=Count('pk'), views=Sum('view_count'), likes=Sum('thumbs_up_count'),
                        replies=Sum('reply_count'), recent=Count('pk', filter=Q(created_at__gte=cutoff_30)),
                        **_day_counts('created_at', days))
    reply_agg = replies.aggregate(total=Count('pk'), recent=Count('pk', filter=Q(created_at__gte=cutoff_30)),
                          **_day_counts('created_at', days))
    res_agg = resources.aggregate(total=Count('pk'), views=Sum('view_count'), likes=Sum('like_count'),
                              comments=Sum('comment_count'), **_day_counts('added_at', days))
    quiz_agg = quiz_attempts.aggregate(total=Count('pk'), xp=Sum('xp_earned'), questions=Sum('total_questions'),
                                 score=Sum('score'), recent=Count('pk', filter=Q(completed_at__gte=cutoff_30)),
                                 **_day_counts('completed_at', days))
    review_agg = flash_reviews.aggregate(easy=Count('pk', filter=Q(confidence='easy')),
                                 medium=Count('pk', filter=Q(confidence='medium')),
                                 hard=Count('pk', filter=Q(confidence='hard')),
                                 recent=Count('pk', filter=Q(last_reviewed_at__gte=cutoff_30)),
                                 **_day_counts('last_reviewed_at', days))
    doc_agg = study_docs.aggregate(total=Count('pk'),
                              summaries=Count('pk', filter=Q(summary_compact__gt='') | Q(summary_detailed__gt='')),
                              mindmaps=Count('pk', filter=~Q(mindmap_json='')))

    post_views = post_agg['views'] or 0
    post_likes_received = post_agg['likes'] or 0
    post_replies_received = post_agg['replies'] or 0
    resource_views = res_agg['views'] or 0
    resource_likes_received = res_agg['likes'] or 0
    resource_comments_received = res_agg['comments'] or 0
    total_attempt_questions = quiz_agg['questions'] or 0
    total_attempt_score = quiz_agg['score'] or 0
    quiz_accuracy = round((total_attempt_score / total_attempt_questions) * 100) if total_attempt_questions else 0
    has_attempts = quiz_agg['total'] > 0

    easy_reviews = review_agg['easy']
    medium_reviews = review_agg['medium']
    hard_reviews = review_agg['hard']
    reviewed_total = easy_reviews + medium_reviews + hard_reviews

    activity_days = []
    max_activity = 1
    for n, i in enumerate(range(13, -1, -1)):
        key = f'd{n}'
        counts = {
            'posts': post_agg[key],
            'replies': reply_agg[key],
            'resources': res_agg[key],
            'study': quiz_agg[key] + review_agg[key],
        }
        total = sum(counts.values())
        max_activity = max(max_activity, total)
        activity_days.append({
            'label': 'Today' if i == 0 else f'{i}d',
            'total': total,
            'posts': counts['posts'],
            'replies': counts['replies'],
            'resources': counts['resources'],
            'study': counts['study'],
            'height': 0,
        })
    for day in activity_days:
        day['height'] = max(8, round((day['total'] / max_activity) * 100)) if day['total'] else 8

    category_counter = Counter(posts.values_list('category', flat=True))
    subject_counter = Counter()
    for subject in resources.values_list('subject', flat=True):
        for part in (subject or '').split(','):
            cleaned = part.strip()
            if cleaned:
                subject_counter[cleaned] += 1

    summaries_count = doc_agg['summaries']
    mindmaps_count = doc_agg['mindmaps']
    quizzes_count = quizzes.count()

    suggestions = []
    docs_count = doc_agg['total']
    if docs_count and summaries_count < docs_count:
        suggestions.append('Generate compact summaries for documents that still have no summary.')
    if docs_count and mindmaps_count < docs_count:
        suggestions.append('Create mindmaps for your main notes to see topic relationships faster.')
    if quizzes_count and not has_attempts:
        suggestions.append('Take at least one generated quiz to start tracking exam readiness.')
    if has_attempts and quiz_accuracy < 70:
        suggestions.append('Review hard flashcards, then generate a fresh quiz from the same document.')
    if hard_reviews:
        suggestions.append(f'Revisit {hard_reviews} hard flashcard review{"" if hard_reviews == 1 else "s"} today.')
    if not res_agg['total']:
        suggestions.append('Upload one useful resource to build your contribution footprint.')
    if not suggestions:
        suggestions.append('Keep using Study Lab regularly; your recent learning loop looks healthy.')

    return Response({
        'username': user.username,
        'stats': {
            'posts': post_agg['total'],
            'replies': reply_agg['total'],
            'postViews': post_views,
            'postLikesReceived': post_likes_received,
            'postRepliesReceived': post_replies_received,
            'resources': res_agg['total'],
            'resourceViews': resource_views,
            'resourceLikesReceived': resource_likes_received,
            'resourceCommentsReceived': resource_comments_received,
            'resourceCommentsMade': resource_comments.count(),
            'followers': Follow.objects.filter(following=user).count(),
            'following': Follow.objects.filter(follower=user).count(),
            'bookmarks': Bookmark.objects.filter(user=user).count(),
            'notificationsUnread': Notification.objects.filter(recipient=user, is_read=False).count(),
            'studyDocs': docs_count,
            'summaries': summaries_count,
            'mindmaps': mindmaps_count,
            'quizzes': quizzes_count,
            'quizAttempts': quiz_agg['total'],
            'quizAccuracy': quiz_accuracy,
            'quizXp': quiz_agg['xp'] or 0,
            'flashcards': flashcards.count(),
            'flashReviews': reviewed_total,
            'easyReviews': easy_reviews,
            'mediumReviews': medium_reviews,
            'hardReviews': hard_reviews,
            'recentPosts': post_agg['recent'],
            'recentReplies': reply_agg['recent'],
            'recentStudyActions': quiz_agg['recent'] + review_agg['recent'],
            'contributionScore': user.contribution_score,
            'likesGiven': user.likes_given_count,
        },
        'activityDays': activity_days,
        'topCategories': _analytics_counter_rows(category_counter),
        'topSubjects': _analytics_counter_rows(subject_counter),
        'topPosts': [_analytics_short_post(p) for p in posts.order_by('-view_count', '-thumbs_up_count')[:5]],
        'topResources': [_analytics_short_resource(r) for r in resources.order_by('-view_count', '-like_count')[:5]],
        'suggestions': suggestions[:5],
    })

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def user_search(request):
    """GET /api/users/search/?q= -- people for the app's @mention picker.

    The same people the web's ajax/user-search/ finds (username contains the term, account
    verified and not locked, eight at most), in the shape the app reads, with those whose
    username starts with the term first."""
    from django.db.models import Case, IntegerField, Value, When
    from .badges import user_badge_info
    from .models import Follow, User
    from .services import avatar_or_photo_url
    q = (request.query_params.get('q') or '').strip().lstrip('@')
    if len(q) < 2:
        return Response([])
    viewer = _get_user_from_request(request)
    users = list(
        User.objects.filter(username__icontains=q, is_locked=False, email_verified=True)
        .annotate(
            starts=Case(When(username__istartswith=q, then=Value(0)), default=Value(1), output_field=IntegerField()),
            n_followers=Count('followers_set', distinct=True),
        )
        .order_by('starts', 'username')[:8]
    )
    following = set()
    if viewer is not None and users:
        following = set(Follow.objects.filter(follower=viewer, following_id__in=[u.id for u in users])
                        .values_list('following_id', flat=True))
    return Response([{
        'id': u.id,
        'username': u.username,
        'display_name': u.display_name or u.username,
        'photo_url': avatar_or_photo_url(u),
        'bio': u.bio or None,
        'school': u.school or None,
        'class_level': u.class_level or None,
        'follower_count': u.n_followers,
        'is_following': u.id in following,
        'is_self': viewer is not None and u.id == viewer.id,
        'badge_info': user_badge_info(u),
    } for u in users])


@api_view(['GET'])
@permission_classes([AllowAny])
def user_suggestions(request):
    """GET /api/users/suggestions/?limit=12 -- people to follow, scored server-side.

    Replaces the ~43 requests the app's PeopleSuggestionRepository made; see
    api.people_suggestions for the signals, exclusions and scoring. Signed out: no results.
    """
    from .people_suggestions import parse_limit, suggest_people
    user = _get_user_from_request(request)
    if user is None or getattr(user, 'is_banned', False):
        return Response({'results': []})
    return Response({'results': suggest_people(user, parse_limit(request.query_params.get('limit')))})


@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def user_follow_toggle(request, user_id):
    """
    POST /api/users/<userId>/follow
    Supports either legacy toggle behavior or an idempotent action payload:
    {"action": "follow"} / {"action": "unfollow"}.
    """
    current_user, err = _require_user(request)
    if err:
        return err
    desired = None
    try:
        desired = (request.data.get('action') or request.data.get('intent') or '').strip().lower() or None
    except Exception:
        desired = None
    data, status_code = services.toggle_follow(current_user, user_id, desired=desired)
    return Response(data, status=status_code)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_followers_list(request, user_id):
    """
    GET /api/users/<userId>/followers
    Lists all Follow records where following=user_id (i.e. users who follow this user).
    """
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    requesting_user = _get_user_from_request(request)
    if not _can_view_locked_profile(requesting_user, target_user):
        return Response({'error': 'This profile is private'}, status=403)
    # FollowSerializer renders both ends of every row; joining only one of them cost a
    # query per row for the other.
    follows = Follow.objects.filter(following=target_user).select_related('follower', 'following')
    return _paginated_response(request, follows, FollowSerializer, default_page_size=50)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_following_list(request, user_id):
    """
    GET /api/users/<userId>/following
    Lists all Follow records where follower=user_id (i.e. users this person follows).
    """
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    requesting_user = _get_user_from_request(request)
    if not _can_view_locked_profile(requesting_user, target_user):
        return Response({'error': 'This profile is private'}, status=403)
    follows = Follow.objects.filter(follower=target_user).select_related('follower', 'following')
    return _paginated_response(request, follows, FollowSerializer, default_page_size=50)

@api_view(['GET', 'POST'])
def user_photos(request):
    """
    GET  /api/users/me/photos — list current user's saved photo URLs (newest first)
    POST /api/users/me/photos — save a new photo URL or upload an image file, and set active
                                Body: { "url": "https://..." } OR multipart file "file"
    """
    current_user, err = _require_user(request)
    if err:
        return err

    if request.method == 'GET':
        photos = UserPhoto.objects.filter(user=current_user)
        return Response(UserPhotoSerializer(photos, many=True).data)

    # POST — add new photo URL or upload file
    url = request.data.get('url', '').strip()
    file_obj = request.FILES.get('file')

    if not url and not file_obj:
        return Response({'error': 'Either an uploaded image file or web URL is required'}, status=400)

    if file_obj:
        try:
            url = save_profile_image_upload(request, current_user, file_obj)
        except ValidationError as exc:
            return Response({'error': ' '.join(exc.messages)}, status=400)
    else:
        try:
            url = validate_profile_photo_url(url)
        except ValidationError as exc:
            return Response({'error': ' '.join(exc.messages)}, status=400)

    with transaction.atomic():
        # Mark all existing photos as not current
        UserPhoto.objects.filter(user=current_user).update(is_current=False)
        # Save new photo
        photo = UserPhoto.objects.create(
            user=current_user,
            url=url,
            uploaded_at=_now_ms(),
            is_current=True,
        )
        # Update the user's main photo_url
        current_user.photo_url = url
        current_user.save(update_fields=['photo_url'])

    logger.info("user_photos: user %s set new photo %s", current_user.username, url)
    return Response(UserPhotoSerializer(photo).data, status=201)

@api_view(['POST'])
def user_photo_activate(request, photo_id):
    """
    POST /api/users/me/photos/<photoId>/activate
    Switch to a previously saved photo from history.
    Android app: call when user taps a photo in the history grid.
    """
    current_user, err = _require_user(request)
    if err:
        return err

    try:
        photo = UserPhoto.objects.get(pk=photo_id, user=current_user)
    except UserPhoto.DoesNotExist:
        return Response({'error': 'Photo not found'}, status=404)

    with transaction.atomic():
        UserPhoto.objects.filter(user=current_user).update(is_current=False)
        photo.is_current = True
        photo.save(update_fields=['is_current'])
        current_user.photo_url = photo.url
        current_user.save(update_fields=['photo_url'])

    logger.info("user_photo_activate: user %s switched to photo %s", current_user.username, photo_id)
    return Response({'success': True, 'photo_url': photo.url, 'photo': UserPhotoSerializer(photo).data})


@api_view(['GET', 'POST', 'DELETE'])
def user_delete_account_request(request):
    """
    GET /api/users/me/delete-account/ - Get status of deletion request
    POST /api/users/me/delete-account/ - Create deletion request
    DELETE /api/users/me/delete-account/ - Cancel/delete pending deletion request
    """
    user, err = _require_user(request)
    if err:
        return err

    from .models import AccountDeletionRequest
    from .utils import now_ms, uuid_str

    if request.method == 'GET':
        req = AccountDeletionRequest.objects.filter(user=user, status=AccountDeletionRequest.STATUS_PENDING).first()
        if req:
            return Response({
                'hasPending': True,
                'request': {
                    'id': req.id,
                    'status': req.status,
                    'reason': req.reason,
                    'createdAt': req.created_at,
                    'scheduledDeleteAt': req.scheduled_delete_at
                }
            })
        return Response({'hasPending': False, 'request': None})

    elif request.method == 'POST':
        reason = request.data.get('reason', '').strip()
        # Check if already has a pending request
        req = AccountDeletionRequest.objects.filter(user=user, status=AccountDeletionRequest.STATUS_PENDING).first()
        if not req:
            created_at = now_ms()
            scheduled_delete_at = created_at + 30 * 24 * 60 * 60 * 1000  # 30 days in ms
            req = AccountDeletionRequest.objects.create(
                id=uuid_str(),
                user=user,
                reason=reason,
                status=AccountDeletionRequest.STATUS_PENDING,
                created_at=created_at,
                scheduled_delete_at=scheduled_delete_at
            )
            logger.info("user_delete_account_request: user %s requested deletion", user.username)
        return Response({
            'success': True,
            'request': {
                'id': req.id,
                'status': req.status,
                'reason': req.reason,
                'createdAt': req.created_at,
                'scheduledDeleteAt': req.scheduled_delete_at
            }
        }, status=201)

    elif request.method == 'DELETE':
        deleted_count, _ = AccountDeletionRequest.objects.filter(user=user, status=AccountDeletionRequest.STATUS_PENDING).delete()
        if deleted_count > 0:
            logger.info("user_delete_account_request: user %s cancelled deletion request", user.username)
            return Response({'success': True, 'message': 'Account deletion request cancelled successfully'})
        return Response({'error': 'No pending deletion request found'}, status=404)


@api_view(['GET'])
def user_follow_requests_list(request):
    current_user, err = _require_user(request)
    if err:
        return err
    
    from .models import FollowRequest
    from .services import avatar_or_photo_url
    reqs = FollowRequest.objects.filter(receiver=current_user).select_related('sender')
    data = []
    for r in reqs:
        data.append({
            'id': r.id,
            'sender': {
                'id': r.sender.id,
                'username': r.sender.username,
                'display_name': r.sender.display_name or r.sender.username,
                'photo_url': avatar_or_photo_url(r.sender) or '',
            },
            'created_at': r.created_at
        })
    return Response(data)


@api_view(['POST'])
def user_follow_request_accept(request, request_id):
    current_user, err = _require_user(request)
    if err:
        return err
    
    from .models import FollowRequest, Follow
    from .utils import now_ms
    try:
        req = FollowRequest.objects.get(pk=request_id, receiver=current_user)
    except FollowRequest.DoesNotExist:
        return Response({'error': 'Follow request not found.'}, status=404)
        
    sender = req.sender
    receiver = req.receiver
    
    with transaction.atomic():
        req.delete()
        Follow.objects.get_or_create(
            follower=sender,
            following=receiver,
            defaults={'created_at': now_ms()}
        )
        follower_count = Follow.objects.filter(following=receiver).count()
        following_count = Follow.objects.filter(follower=sender).count()
        User.objects.filter(pk=receiver.id).update(follower_count=follower_count)
        User.objects.filter(pk=sender.id).update(following_count=following_count)
        
    from api import notifications as _notif
    from api import realtime as _rt
    _notif.notify_cancel_follow_request(sender.id, receiver.id)
    _notif.notify_new_follow(sender.id, receiver.id)
    _rt.broadcast_follow_changed(receiver.id, follower_count)
    
    return Response({'status': 'success'})


@api_view(['POST'])
def user_follow_request_reject(request, request_id):
    current_user, err = _require_user(request)
    if err:
        return err
    
    from .models import FollowRequest
    try:
        req = FollowRequest.objects.get(pk=request_id, receiver=current_user)
    except FollowRequest.DoesNotExist:
        return Response({'error': 'Follow request not found.'}, status=404)
        
    sender_id = req.sender_id
    req.delete()
    
    from api import notifications as _notif
    _notif.notify_cancel_follow_request(sender_id, current_user.id)
    
    return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([AllowAny])
def institutions_list(request):
    """GET /api/users/institutions/"""
    from .services import avatar_or_photo_url
    insts = User.objects.filter(role='institution')
    data = []
    for inst in insts:
        data.append({
            'id': inst.id,
            'username': inst.username,
            'displayName': inst.display_name or inst.username,
            'photoUrl': avatar_or_photo_url(inst) or ''
        })
    return Response({'institutions': data})

