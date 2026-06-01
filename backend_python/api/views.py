"""
All API views for NEBians.
Endpoints:
  POST   /api/auth/google
  GET    /api/users/check-username?username=
  POST   /api/users/profile
  GET    /api/users/profile/<username>
  GET    /api/users/profile/<username>/stats
  POST   /api/users/<userId>/follow           (toggle follow/unfollow)
  GET    /api/users/<userId>/followers
  GET    /api/users/<userId>/following
  GET    /api/users/me/photos
  POST   /api/users/me/photos
  POST   /api/users/me/photos/<photoId>/activate
  GET    /api/resources
  GET    /api/posts          (via posts_endpoint dispatcher)
  POST   /api/posts          (via posts_endpoint dispatcher)
  DELETE /api/posts/<postId>
  POST   /api/posts/<postId>/like
  GET    /api/posts/<postId>/replies   (via replies_endpoint dispatcher)
  POST   /api/posts/<postId>/replies   (via replies_endpoint dispatcher)
  POST   /api/replies/<replyId>/like
  POST   /api/fcm/register
"""
import logging
import time
import uuid

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.db.models import Q, F
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .authentication import verify_google_token
from .security import (
    hash_password, verify_password, hash_verification_code, verify_verification_code,
    validate_profile_photo_url, save_profile_image_upload,
    validate_external_https_url,
)
from .email_utils import send_verification_email
from .throttles import AuthRateThrottle, VerificationRateThrottle
from .models import User, Resource, Post, PostLike, Reply, ReplyLike, FCMToken, Follow, UserPhoto, EditHistory, Report, Bookmark, Notification
from .serializers import (
    UserSerializer, UserPublicSerializer,
    ResourceSerializer, PostSerializer, ReplySerializer,
    UserPhotoSerializer, UserStatsSerializer, FollowSerializer,
    EditHistorySerializer, ReportSerializer, BookmarkSerializer,
    NotificationSerializer,
)
from . import counters as _counters
from . import notifications as _notif

logger = logging.getLogger(__name__)


def _now_ms():
    """Current time as Unix milliseconds."""
    return int(time.time() * 1000)


def _profile_incomplete(user):
    """Check if user profile is missing mandatory fields."""
    return not user.display_name or not user.gender or not user.class_level


def _get_user_from_request(request):
    """
    Returns the authenticated User object if the request is authenticated,
    otherwise None. Does NOT raise.
    """
    user = getattr(request, 'user', None)
    if isinstance(user, User):
        return user
    return None


def _require_user(request):
    """
    Returns (user, error_response) tuple. If user is authenticated, returns
    (user, None). Otherwise returns (None, Response with 401).
    """
    user = _get_user_from_request(request)
    if user is None:
        return None, Response({'error': 'Unauthorized — please sign in again'}, status=401)
    return user, None


CODE_TTL_MS = 10 * 60 * 1000
CODE_RESEND_COOLDOWN_MS = 60 * 1000
MAX_CODE_ATTEMPTS = 5


def _validate_password_strength(password):
    try:
        validate_password(password)
    except ValidationError as exc:
        return Response({'error': ' '.join(exc.messages)}, status=400)
    return None


def _issue_verification_code(user, purpose):
    code = User.generate_verification_code()
    now = _now_ms()
    user.verification_code = hash_verification_code(code)
    user.verification_code_expires = now + CODE_TTL_MS
    user.verification_code_purpose = purpose
    user.verification_code_attempts = 0
    user.verification_code_last_sent_at = now
    user.save(update_fields=[
        'verification_code', 'verification_code_expires', 'verification_code_purpose',
        'verification_code_attempts', 'verification_code_last_sent_at'
    ])
    return code


def _verification_resend_blocked(user):
    last_sent = user.verification_code_last_sent_at or 0
    if not last_sent:
        # Legacy rows only had an expiry. Do not infer last-send time from expiry.
        return False
    return (_now_ms() - last_sent) < CODE_RESEND_COOLDOWN_MS


def _verify_user_code(user, code, purpose):
    now = _now_ms()
    if user.verification_code_expires < now:
        return False, Response({'error': 'Invalid or expired verification code'}, status=400)
    if purpose is not None and user.verification_code_purpose and user.verification_code_purpose != purpose:
        if purpose == 'password_reset' and user.verification_code_purpose == 'set_password':
            pass
        elif purpose == 'set_password' and user.verification_code_purpose == 'password_reset':
            pass
        else:
            return False, Response({'error': 'Invalid or expired verification code'}, status=400)
    if user.verification_code_attempts >= MAX_CODE_ATTEMPTS:
        return False, Response({'error': 'Too many invalid attempts. Please request a new code.'}, status=429)
    if not verify_verification_code(code, user.verification_code or ''):
        User.objects.filter(pk=user.pk).update(verification_code_attempts=F('verification_code_attempts') + 1)
        return False, Response({'error': 'Invalid or expired verification code'}, status=400)
    return True, None


def _clear_verification_code(user):
    user.verification_code = None
    user.verification_code_expires = 0
    user.verification_code_purpose = ''
    user.verification_code_attempts = 0
    user.verification_code_last_sent_at = 0


def _paginated_response(request, queryset, serializer_class, *, context=None, default_page_size=50, max_page_size=100):
    paginator = PageNumberPagination()
    try:
        page_size = int(request.query_params.get('page_size', default_page_size))
    except (TypeError, ValueError):
        page_size = default_page_size
    paginator.page_size = max(1, min(page_size, max_page_size))
    page = paginator.paginate_queryset(queryset, request)

    ctx = context or {}
    user = _get_user_from_request(request)
    if user and page:
        if serializer_class == PostSerializer:
            ctx['liked_post_ids'] = set(PostLike.objects.filter(
                user=user, post_id__in=[p.id for p in page]
            ).values_list('post_id', flat=True))
        elif serializer_class == ReplySerializer:
            ctx['liked_reply_ids'] = set(ReplyLike.objects.filter(
                user=user, reply_id__in=[r.id for r in page]
            ).values_list('reply_id', flat=True))

    serializer = serializer_class(page, many=True, context=ctx)
    return paginator.get_paginated_response(serializer.data)


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

@api_view(['POST'])
def auth_google(request):
    """
    Sign-in or Register via Google ID Token.
    Body: { "idToken": "<google_id_token>" }
    Returns: { "status": "success", "isNewUser": bool, "authToken": "...", "user": {...} }
    """
    id_token = request.data.get('idToken')
    if not id_token:
        logger.warning("auth_google: missing idToken")
        return Response({'error': 'idToken is required'}, status=400)

    google_info = verify_google_token(id_token)
    if not google_info:
        logger.warning("auth_google: Google token verification failed")
        return Response({'error': 'Invalid Google ID Token'}, status=401)

    user_id = google_info['userId']
    email = google_info.get('email') or ''
    display_name = google_info.get('displayName') or ''
    photo_url = google_info.get('photoUrl') or ''

    try:
        user = User.objects.get(pk=user_id)
        if not user.auth_token:
            user.auth_token = User.generate_token()
            user.save(update_fields=['auth_token'])
        logger.info("auth_google: existing user signed in: %s", user.username or user.id)
        return Response({
            'status': 'success',
            'isNewUser': False,
            'authToken': user.auth_token,
            'user': UserSerializer(user).data
        })
    except User.DoesNotExist:
        # New user — create with auth token, temporary username placeholder
        auth_token = User.generate_token()
        temp_username = f"user_{user_id[:8]}"
        user = User(
            pk=user_id,
            auth_token=auth_token,
            username=temp_username,
            email=email,
            display_name=display_name,
            photo_url=photo_url,
            created_at=_now_ms()
        )
        user.save()
        logger.info("auth_google: new user created: %s (temp_username=%s)", user_id, temp_username)
        return Response({
            'status': 'success',
            'isNewUser': True,
            'authToken': auth_token,
            'user': UserSerializer(user).data
        })


# ---------------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------------

@api_view(['GET'])
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
    user, err = _require_user(request)
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
    display_name = data.get('displayName', '') or user.display_name or ''
    gender = data.get('gender', '')
    class_level = data.get('classLevel', '')
    subjects = data.get('subjects', '')
    pradesh = data.get('pradesh', '')
    district = data.get('district', '')
    school = data.get('school', '')
    bio = data.get('bio', '')
    is_locked = bool(data.get('isLocked', False))

    user.username = username
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
    user.bio = bio
    user.is_locked = is_locked
    user.save()

    logger.info("user_profile: profile saved for user %s (username=%s)", user.id, user.username)
    return Response({'status': 'success', 'user': UserSerializer(user).data})


@api_view(['GET'])
def user_profile_get(request, username):
    """GET /api/users/profile/<username>"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    requesting_user = _get_user_from_request(request)
    is_owner = requesting_user and requesting_user.pk == user.pk

    if user.is_locked and not is_owner:
        return Response(UserPublicSerializer(user).data)

    return Response(UserSerializer(user).data)


# ---------------------------------------------------------------------------
# RESOURCES
# ---------------------------------------------------------------------------

@api_view(['GET'])
def resources_list(request):
    """GET /api/resources — public endpoint with enforced pagination."""
    resources = Resource.objects.all()

    subject = request.query_params.get('subject')
    grade = request.query_params.get('grade')
    rtype = request.query_params.get('type')
    search = request.query_params.get('search')

    if subject:
        resources = resources.filter(subject__iexact=subject)
    if grade:
        resources = resources.filter(grade_level__iexact=grade)
    if rtype:
        resources = resources.filter(type__iexact=rtype)
    if search:
        resources = resources.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    return _paginated_response(request, resources, ResourceSerializer)


@api_view(['GET'])
def resource_detail(request, resource_id):
    """GET /api/resources/<resourceId> — get a single resource."""
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    return Response(ResourceSerializer(resource).data)


@api_view(['POST'])
def resource_view(request, resource_id):
    """POST /api/resources/<resourceId>/view — increment view_count."""
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    Resource.objects.filter(pk=resource_id).update(view_count=F('view_count') + 1)
    return Response({'view_count': resource.view_count + 1})


# ---------------------------------------------------------------------------
# FORUM — POSTS
# ---------------------------------------------------------------------------

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
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
    return Response(PostSerializer(post, context={'request': request}).data, status=201)


@api_view(['GET', 'DELETE', 'PATCH'])
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
        user_id = post.user_id
        post.delete()
        _counters.decrement_user_post_count(user_id)
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

    return Response({'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up})


# ---------------------------------------------------------------------------
# FORUM — REPLIES
# ---------------------------------------------------------------------------

@api_view(['POST'])
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
        with transaction.atomic():
            post_id = reply.post_id
            parent_id = reply.parent_reply_id
            reply_user_id = reply.user_id
            reply.delete()
            Post.objects.filter(pk=post_id, reply_count__gt=0).update(reply_count=F('reply_count') - 1)
            if parent_id:
                Reply.objects.filter(pk=parent_id, reply_count__gt=0).update(reply_count=F('reply_count') - 1)
        _counters.decrement_user_reply_count(reply_user_id)
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

    return Response({'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up})


@api_view(['GET'])
def edit_history(request, target_type, target_id):
    """GET /api/edit-history/<target_type>/<target_id>/ — edit history for a post or reply."""
    if target_type not in ('post', 'reply'):
        return Response({'error': 'Invalid target_type'}, status=400)
    entries = EditHistory.objects.filter(target_type=target_type, target_id=target_id).select_related('edited_by')
    return Response(EditHistorySerializer(entries, many=True).data)


# ---------------------------------------------------------------------------
# AUTH — EMAIL SIGNUP / LOGIN / VERIFICATION
# ---------------------------------------------------------------------------

@api_view(['POST'])
@authentication_classes([])
@throttle_classes([AuthRateThrottle])
def auth_email_signup(request):
    """
    POST /api/auth/email/signup
    Body: { "email": "...", "password": "...", "username": "..." }
    Creates user with email, sends 6-digit verification code.
    """
    email = request.data.get('email', '').strip().lower()
    password = request.data.get('password', '')
    username = request.data.get('username', '').strip()

    if not email or not password or not username:
        return Response({'error': 'Email, password, and username are required'}, status=400)

    password_error = _validate_password_strength(password)
    if password_error:
        return password_error

    if len(username) < 3:
        return Response({'error': 'Username must be at least 3 characters'}, status=400)

    if not username.replace('_', '').isalnum():
        return Response({'error': 'Username can only contain letters, numbers, and underscores'}, status=400)

    if User.objects.filter(email__iexact=email).exists():
        return Response({'error': 'An account with this email already exists'}, status=409)

    if User.objects.filter(username__iexact=username).exists():
        return Response({'error': 'This username is already taken'}, status=409)

    user = User(
        pk=str(uuid.uuid4()),
        auth_token=User.generate_token(),
        username=username,
        email=email,
        password_hash=hash_password(password),
        email_verified=False,
        created_at=_now_ms()
    )
    user.save()
    code = _issue_verification_code(user, 'signup')

    send_verification_email(email, code, username)

    logger.info("auth_email_signup: new user %s (email=%s), verification code sent", username, email)
    return Response({
        'status': 'success',
        'message': 'Verification code sent to your email',
        'userId': user.id,
        'email': email,
    })


@api_view(['POST'])
@authentication_classes([])
@throttle_classes([VerificationRateThrottle])
def auth_email_verify(request):
    """
    POST /api/auth/email/verify
    Body: { "email": "...", "code": "123456" }
    Verifies the 6-digit code. On success, returns auth token + user.
    """
    email = request.data.get('email', '').strip().lower()
    code = request.data.get('code', '').strip()

    if not email or not code:
        return Response({'error': 'Email and verification code are required'}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'error': 'No account found with this email'}, status=404)

    if user.email_verified:
        return Response({'error': 'Email is already verified. Please log in.'}, status=400)

    ok, error_response = _verify_user_code(user, code, 'signup')
    if not ok:
        return error_response

    user.email_verified = True
    _clear_verification_code(user)
    user.auth_token = User.generate_token()
    user.save()

    logger.info("auth_email_verify: email verified for user %s", user.username)
    return Response({
        'status': 'success',
        'isNewUser': True,
        'profileIncomplete': _profile_incomplete(user),
        'authToken': user.auth_token,
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@authentication_classes([])
@throttle_classes([VerificationRateThrottle])
def auth_email_resend(request):
    """
    POST /api/auth/email/resend
    Body: { "email": "..." }
    Resends verification code. Rate-limited to prevent abuse.
    """
    email = request.data.get('email', '').strip().lower()

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'error': 'No account found with this email'}, status=404)

    if user.email_verified:
        return Response({'error': 'Email is already verified. Please log in.'}, status=400)

    if _verification_resend_blocked(user):
        return Response({'error': 'Please wait 60 seconds before requesting a new code'}, status=429)

    code = _issue_verification_code(user, 'signup')

    send_verification_email(email, code, user.username)

    logger.info("auth_email_resend: new code sent to %s", email)
    return Response({'status': 'success', 'message': 'New verification code sent'})


@api_view(['POST'])
@authentication_classes([])
@throttle_classes([AuthRateThrottle])
def auth_email_login(request):
    """
    POST /api/auth/email/login
    Body: { "email": "...", "password": "..." }
    The email field accepts either an email or a username.
    Logs in with email/username + password. Requires email_verified=True.
    """
    login_id = request.data.get('email', '').strip()
    password = request.data.get('password', '')

    if not login_id or not password:
        return Response({'error': 'Email/username and password are required'}, status=400)

    # Look up by email or username
    try:
        if '@' in login_id:
            user = User.objects.get(email__iexact=login_id)
        else:
            user = User.objects.get(username__iexact=login_id)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email/username or password'}, status=401)
    except User.MultipleObjectsReturned:
        return Response({'error': 'Multiple accounts found. Please use your email address.'}, status=400)

    if not user.email_verified:
        if not _verification_resend_blocked(user):
            code = _issue_verification_code(user, 'signup')
            send_verification_email(user.email, code, user.username)
        return Response({'error': 'Please verify your email first', 'needsVerification': True, 'email': user.email}, status=403)

    if not user.password_hash:
        return Response({'error': 'This account uses Google sign-in. Use "Forgot password?" to set a password for email login.', 'needsSetPassword': True, 'email': user.email}, status=400)

    password_ok, needs_rehash = verify_password(password, user.password_hash)
    if not password_ok:
        return Response({'error': 'Invalid email/username or password'}, status=401)

    user.auth_token = User.generate_token()
    update_fields = ['auth_token']
    if needs_rehash:
        user.password_hash = hash_password(password)
        update_fields.append('password_hash')
    user.save(update_fields=update_fields)

    logger.info("auth_email_login: user %s logged in", user.username)
    return Response({
        'status': 'success',
        'isNewUser': False,
        'profileIncomplete': _profile_incomplete(user),
        'authToken': user.auth_token,
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@authentication_classes([])
@throttle_classes([VerificationRateThrottle])
def auth_email_forgot(request):
    """
    POST /api/auth/email/forgot
    Body: { "email": "..." }
    Sends a verification code to reset or set a password.
    For Google-only accounts (no password), returns needsSetPassword: true
    so the frontend can show an appropriate UI.
    """
    email = request.data.get('email', '').strip().lower()

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'status': 'success', 'message': 'If an account exists with this email, a verification code has been sent'})

    needs_set_password = not bool(user.password_hash)
    purpose = 'set_password' if needs_set_password else 'password_reset'

    if _verification_resend_blocked(user):
        return Response({
            'status': 'success',
            'message': 'If an account exists with this email, a verification code has been sent',
            'needsSetPassword': needs_set_password,
        })

    code = _issue_verification_code(user, purpose)
    send_verification_email(email, code, user.username)

    logger.info("auth_email_forgot: %s code sent to %s", purpose, email)
    return Response({
        'status': 'success',
        'message': 'If an account exists with this email, a verification code has been sent',
        'needsSetPassword': needs_set_password,
    })


@api_view(['POST'])
@authentication_classes([])
@throttle_classes([VerificationRateThrottle])
def auth_email_reset_password(request):
    """
    POST /api/auth/email/reset-password
    Body: { "email": "...", "code": "123456", "newPassword": "...", "confirmPassword": "..." }
    Resets or sets a password using verification code.
    Works for both password_reset and set_password purposes.
    """
    email = request.data.get('email', '').strip().lower()
    code = request.data.get('code', '').strip()
    new_password = request.data.get('newPassword', '')
    confirm_password = request.data.get('confirmPassword', '')

    if not email or not code or not new_password:
        return Response({'error': 'Email, code, and new password are required'}, status=400)

    if confirm_password and new_password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=400)

    password_error = _validate_password_strength(new_password)
    if password_error:
        return password_error

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid or expired verification code'}, status=400)

    ok, error_response = _verify_user_code(user, code, None)
    if not ok:
        return error_response

    user.password_hash = hash_password(new_password)
    user.email_verified = True
    _clear_verification_code(user)
    user.auth_token = User.generate_token()
    user.save()

    logger.info("auth_email_reset_password: password set/reset for %s", user.username)
    return Response({
        'status': 'success',
        'profileIncomplete': _profile_incomplete(user),
        'authToken': user.auth_token,
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def auth_set_password(request):
    """
    POST /api/auth/set-password
    Body: { "password": "..." }
    Sets a password for a Google-only account so they can also log in with email/username.
    Requires authentication. Also sets email_verified=True since Google already verified it.
    """
    user, err = _require_user(request)
    if err:
        return err

    password = request.data.get('password', '')
    if not password:
        return Response({'error': 'Password is required'}, status=400)

    password_error = _validate_password_strength(password)
    if password_error:
        return password_error

    if user.password_hash:
        return Response({'error': 'Password already set. Use change-password instead.'}, status=400)

    user.password_hash = hash_password(password)
    user.email_verified = True
    user.save(update_fields=['password_hash', 'email_verified'])

    logger.info("auth_set_password: password set for user %s", user.username)
    return Response({
        'status': 'success',
        'message': 'Password set successfully',
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def auth_change_password(request):
    """
    POST /api/auth/change-password
    Body: { "currentPassword": "...", "newPassword": "..." }
    Changes password for an account that already has one.
    Requires authentication.
    """
    user, err = _require_user(request)
    if err:
        return err

    current_password = request.data.get('currentPassword', '')
    new_password = request.data.get('newPassword', '')

    if not current_password or not new_password:
        return Response({'error': 'Current password and new password are required'}, status=400)

    password_error = _validate_password_strength(new_password)
    if password_error:
        return password_error

    if not user.password_hash:
        return Response({'error': 'No password set. Use set-password instead.'}, status=400)

    password_ok, _needs_rehash = verify_password(current_password, user.password_hash)
    if not password_ok:
        return Response({'error': 'Current password is incorrect'}, status=401)

    user.password_hash = hash_password(new_password)
    user.auth_token = User.generate_token()
    user.save(update_fields=['password_hash', 'auth_token'])

    logger.info("auth_change_password: password changed for user %s", user.username)
    return Response({
        'status': 'success',
        'message': 'Password changed successfully',
        'authToken': user.auth_token,
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
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


@api_view(['GET'])
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


# ---------------------------------------------------------------------------
# FCM TOKENS
# ---------------------------------------------------------------------------

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def fcm_register(request):
    """POST /api/fcm/register"""
    token = request.data.get('token', '').strip()
    if not token:
        return Response({'error': 'FCM token is required'}, status=400)
    if len(token) < 10 or len(token) > 512:
        return Response({'error': 'Invalid FCM token format'}, status=400)

    user = _get_user_from_request(request)
    now = _now_ms()

    FCMToken.objects.update_or_create(
        token=token,
        defaults={'user': user, 'created_at': now}
    )

    return Response({'success': True})


# ---------------------------------------------------------------------------
# SEARCH
# ---------------------------------------------------------------------------

@api_view(['GET'])
def search_all(request):
    """GET /api/search?q=query — unified search across resources and posts."""
    query = request.query_params.get('q', '').strip()
    if not query:
        return Response({'resources': [], 'posts': []})

    resources = Resource.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__icontains=query)
    )
    posts = Post.objects.select_related('user').filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        is_archived=False,
    )

    resource_page = _paginated_response(request, resources, ResourceSerializer, default_page_size=25, max_page_size=50)
    post_page = _paginated_response(request, posts, PostSerializer, context={'request': request}, default_page_size=25, max_page_size=50)

    return Response({
        'resources': resource_page.data.get('results', []),
        'posts': post_page.data.get('results', []),
    })


# ---------------------------------------------------------------------------
# DISPATCHERS — combine GET+POST on the same URL into one Django view
# ---------------------------------------------------------------------------

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
    logger.info("posts_endpoint: created post %s by user %s", post.id, user.username)
    return Response(PostSerializer(post, context={'request': request}).data, status=201)


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
    _notif.notify_new_reply(user.id, post_id, reply.id)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id)
    return Response(ReplySerializer(reply, context={'request': request}).data, status=201)


# ---------------------------------------------------------------------------
# COMMUNITY — USER STATS
# ---------------------------------------------------------------------------

def _build_stats(user):
    """
    Build the stats dict for a given User instance.
    Uses denormalized counters on the User model when available,
    falls back to aggregate queries for legacy rows.
    """
    post_count = user.post_count if hasattr(user, 'post_count') and user.post_count > 0 else Post.objects.filter(user=user).count()
    reply_count = user.reply_count if hasattr(user, 'reply_count') and user.reply_count > 0 else Reply.objects.filter(user=user).count()
    follower_count = user.follower_count if hasattr(user, 'follower_count') and user.follower_count > 0 else Follow.objects.filter(following=user).count()
    following_count = user.following_count if hasattr(user, 'following_count') and user.following_count > 0 else Follow.objects.filter(follower=user).count()
    likes_given = user.likes_given_count if hasattr(user, 'likes_given_count') and user.likes_given_count > 0 else (
        PostLike.objects.filter(user=user).count() + ReplyLike.objects.filter(user=user).count()
    )
    likes_received = user.likes_received_count if hasattr(user, 'likes_received_count') and user.likes_received_count > 0 else (
        PostLike.objects.filter(post__user=user).count() + ReplyLike.objects.filter(reply__user=user).count()
    )

    contribution_score = user.contribution_score if hasattr(user, 'contribution_score') and user.contribution_score > 0 else (
        (post_count * 3) + (reply_count * 2) + likes_given + (likes_received * 2)
    )

    return {
        'username': user.username,
        'post_count': post_count,
        'reply_count': reply_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'likes_received': likes_received,
        'likes_given': likes_given,
        'contribution_score': contribution_score,
    }


def _build_stats_batch(user_qs):
    """
    Build stats for a queryset of users in a single aggregation pass.
    Returns a dict mapping user_id -> stats dict.
    """
    from django.db.models import Count, Q, Sum, Case, When, IntegerField

    user_ids = list(user_qs.values_list('id', flat=True))

    post_counts = dict(Post.objects.filter(user_id__in=user_ids).values('user_id').annotate(c=Count('id')).values_list('user_id', 'c'))
    reply_counts = dict(Reply.objects.filter(user_id__in=user_ids).values('user_id').annotate(c=Count('id')).values_list('user_id', 'c'))
    follower_counts = dict(Follow.objects.filter(following_id__in=user_ids).values('following_id').annotate(c=Count('id')).values_list('following_id', 'c'))
    following_counts = dict(Follow.objects.filter(follower_id__in=user_ids).values('follower_id').annotate(c=Count('id')).values_list('follower_id', 'c'))

    likes_given = {}
    for model, like_field in [(PostLike, 'user_id'), (ReplyLike, 'user_id')]:
        for uid, cnt in model.objects.filter(user_id__in=user_ids).values('user_id').annotate(c=Count('id')).values_list('user_id', 'c'):
            likes_given[uid] = likes_given.get(uid, 0) + cnt

    likes_received = {}
    for model, owner_field in [(PostLike, 'post__user_id'), (ReplyLike, 'reply__user_id')]:
        for uid, cnt in model.objects.filter(**{owner_field + '__in': user_ids}).values(owner_field).annotate(c=Count('id')).values_list(owner_field, 'c'):
            likes_received[uid] = likes_received.get(uid, 0) + cnt

    users_map = {u.id: u for u in user_qs if hasattr(u, 'id')}
    result = {}
    for uid in user_ids:
        u = users_map.get(uid)
        pc = post_counts.get(uid, 0)
        rc = reply_counts.get(uid, 0)
        fc = follower_counts.get(uid, 0)
        fwc = following_counts.get(uid, 0)
        lg = likes_given.get(uid, 0)
        lr = likes_received.get(uid, 0)
        score = (pc * 3) + (rc * 2) + lg + (lr * 2)
        result[uid] = {
            'username': u.username if u else '',
            'display_name': (u.display_name or u.username) if u else '',
            'photo_url': u.photo_url if u else '',
            'post_count': pc,
            'reply_count': rc,
            'follower_count': fc,
            'following_count': fwc,
            'likes_given': lg,
            'likes_received': lr,
            'contribution_score': score,
        }
    return result


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
    if user.is_locked and not is_owner:
        return Response({'error': 'This profile is private'}, status=403)

    stats = _build_stats(user)
    is_following = False
    if requesting_user and requesting_user.pk != user.pk:
        is_following = Follow.objects.filter(follower=requesting_user, following=user).exists()

    stats['is_following'] = is_following
    stats['is_self'] = is_owner
    return Response(stats)


# ---------------------------------------------------------------------------
# COMMUNITY — FOLLOW / UNFOLLOW
# ---------------------------------------------------------------------------

@api_view(['POST'])
@throttle_classes([AuthRateThrottle])
def user_follow_toggle(request, user_id):
    """
    POST /api/users/<userId>/follow
    Instagram-style toggle: follow if not following, unfollow if already following.
    Returns: { is_following: bool, follower_count: int }
    Android app: call after Follow/Unfollow button tap and update UI from response.
    """
    current_user, err = _require_user(request)
    if err:
        return err

    if current_user.id == user_id:
        return Response({'error': 'You cannot follow yourself'}, status=400)

    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    with transaction.atomic():
        existing = Follow.objects.filter(follower=current_user, following=target_user).first()
        if existing:
            existing.delete()
            is_following = False
            _counters.decrement_user_follower_count(target_user.id)
            _counters.decrement_user_following_count(current_user.id)
            _notif.notify_unfollow(current_user.id, target_user.id)
        else:
            Follow.objects.create(
                follower=current_user,
                following=target_user,
                created_at=_now_ms()
            )
            is_following = True
            _counters.increment_user_follower_count(target_user.id)
            _counters.increment_user_following_count(current_user.id)
            _notif.notify_new_follow(current_user.id, target_user.id)

    follower_count = target_user.follower_count if hasattr(target_user, 'follower_count') else Follow.objects.filter(following=target_user).count()
    return Response({'is_following': is_following, 'follower_count': follower_count})


@api_view(['GET'])
def user_followers_list(request, user_id):
    """
    GET /api/users/<userId>/followers
    Lists all Follow records where following=user_id (i.e. users who follow this user).
    """
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if target_user.is_locked and not (_get_user_from_request(request) and _get_user_from_request(request).pk == target_user.pk):
        return Response({'error': 'This profile is private'}, status=403)
    follows = Follow.objects.filter(following=target_user).select_related('follower')
    return _paginated_response(request, follows, FollowSerializer, default_page_size=50)


@api_view(['GET'])
def user_following_list(request, user_id):
    """
    GET /api/users/<userId>/following
    Lists all Follow records where follower=user_id (i.e. users this person follows).
    """
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if target_user.is_locked and not (_get_user_from_request(request) and _get_user_from_request(request).pk == target_user.pk):
        return Response({'error': 'This profile is private'}, status=403)
    follows = Follow.objects.filter(follower=target_user).select_related('following')
    return _paginated_response(request, follows, FollowSerializer, default_page_size=50)


# ---------------------------------------------------------------------------
# COMMUNITY — PROFILE PHOTO HISTORY
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# REPORTS
# ---------------------------------------------------------------------------

@api_view(['POST'])
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


# ---------------------------------------------------------------------------
# NOTIFICATIONS
# ---------------------------------------------------------------------------

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