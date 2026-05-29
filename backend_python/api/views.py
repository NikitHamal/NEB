"""
All API views for NEBians.
Endpoints:
  POST   /api/auth/google
  GET    /api/users/check-username?username=
  POST   /api/users/profile
  GET    /api/users/profile/<username>
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

from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from .authentication import verify_google_token
from .models import User, Resource, Post, PostLike, Reply, ReplyLike, FCMToken
from .serializers import (
    UserSerializer, UserPublicSerializer,
    ResourceSerializer, PostSerializer, ReplySerializer
)

logger = logging.getLogger(__name__)


def _now_ms():
    """Current time as Unix milliseconds."""
    return int(time.time() * 1000)


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
        # Generate a new auth token on each sign-in for security
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
@authentication_classes([])
def user_profile_create_or_update(request):
    """POST /api/users/profile — create or update the authenticated user's profile."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        logger.warning("user_profile: missing Bearer header")
        return Response({'error': 'Unauthorized — please sign in again'}, status=401)

    token = auth_header[7:].strip()
    if not token:
        logger.warning("user_profile: empty Bearer token")
        return Response({'error': 'Unauthorized — please sign in again'}, status=401)

    # Look up user by auth_token
    try:
        user = User.objects.get(auth_token=token)
    except User.DoesNotExist:
        logger.warning("user_profile: no user found for auth token %s...", token[:8])
        return Response({'error': 'Unauthorized — please sign in again'}, status=401)

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
    display_name = data.get('displayName', '') or user.display_name or ''
    gender = data.get('gender', '')
    class_level = data.get('classLevel', '')
    subjects = data.get('subjects', '')
    pradesh = data.get('pradesh', '')
    district = data.get('district', '')
    school = data.get('school', '')
    is_locked = bool(data.get('isLocked', False))

    user.username = username
    user.email = email
    user.photo_url = photo_url
    user.display_name = display_name
    user.dob = dob
    user.gender = gender
    user.class_level = class_level
    user.subjects = subjects
    user.pradesh = pradesh
    user.district = district
    user.school = school
    user.is_locked = is_locked
    user.save()

    logger.info("user_profile: profile saved for user %s (username=%s)", user.id, user.username)
    return Response({'status': 'success', 'user': UserSerializer(user).data})


@api_view(['GET'])
@authentication_classes([])
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
    """GET /api/resources — public endpoint, no auth needed."""
    resources = Resource.objects.all()
    return Response(ResourceSerializer(resources, many=True).data)


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
    resource.view_count += 1
    resource.save(update_fields=['view_count'])
    return Response({'view_count': resource.view_count})


# ---------------------------------------------------------------------------
# FORUM — POSTS
# ---------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([])
def posts_list(request):
    """GET /api/posts"""
    posts = Post.objects.select_related('user').all()
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
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
    return Response(PostSerializer(post, context={'request': request}).data, status=201)


@api_view(['GET', 'DELETE'])
def post_detail(request, post_id):
    """GET /api/posts/<postId> — get a single post. DELETE /api/posts/<postId> — delete a post."""
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
        post.delete()
        logger.info("post_detail DELETE: deleted post %s by user %s", post_id, user.username)
        return Response({'success': True})

    return Response(PostSerializer(post, context={'request': request}).data)


@api_view(['POST'])
def post_like(request, post_id):
    """POST /api/posts/<postId>/like — toggle thumbs up."""
    user, err = _require_user(request)
    if err:
        return err

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    with transaction.atomic():
        existing = PostLike.objects.filter(post=post, user=user).first()
        if existing:
            existing.delete()
            post.thumbs_up_count = max(0, post.thumbs_up_count - 1)
            is_thumbed_up = False
        else:
            PostLike.objects.create(post=post, user=user)
            post.thumbs_up_count += 1
            is_thumbed_up = True
        post.save(update_fields=['thumbs_up_count'])

    return Response({'thumbsUpCount': post.thumbs_up_count, 'isThumbedUp': is_thumbed_up})


# ---------------------------------------------------------------------------
# FORUM — REPLIES
# ---------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([])
def replies_list(request, post_id):
    """GET /api/posts/<postId>/replies"""
    replies = Reply.objects.filter(post_id=post_id).select_related('user')
    serializer = ReplySerializer(replies, many=True, context={'request': request})
    return Response(serializer.data)


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
        post.reply_count += 1
        post.save(update_fields=['reply_count'])

    logger.info("replies_create: created reply on post %s by user %s", post_id, user.username)
    return Response(ReplySerializer(reply, context={'request': request}).data, status=201)


@api_view(['POST'])
def reply_like(request, reply_id):
    """POST /api/replies/<replyId>/like — toggle thumbs up."""
    user, err = _require_user(request)
    if err:
        return err

    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return Response({'error': 'Reply not found'}, status=404)

    with transaction.atomic():
        existing = ReplyLike.objects.filter(reply=reply, user=user).first()
        if existing:
            existing.delete()
            reply.thumbs_up_count = max(0, reply.thumbs_up_count - 1)
            is_thumbed_up = False
        else:
            ReplyLike.objects.create(reply=reply, user=user)
            reply.thumbs_up_count += 1
            is_thumbed_up = True
        reply.save(update_fields=['thumbs_up_count'])

    return Response({'thumbsUpCount': reply.thumbs_up_count, 'isThumbedUp': is_thumbed_up})


# ---------------------------------------------------------------------------
# FCM TOKENS
# ---------------------------------------------------------------------------

@api_view(['POST'])
def fcm_register(request):
    """POST /api/fcm/register"""
    token = request.data.get('token', '').strip()
    if not token:
        return Response({'error': 'FCM token is required'}, status=400)

    user = _get_user_from_request(request)
    now = _now_ms()

    FCMToken.objects.update_or_create(
        token=token,
        defaults={'user': user, 'created_at': now}
    )

    return Response({'success': True})


# ---------------------------------------------------------------------------
# DISPATCHERS — combine GET+POST on the same URL into one Django view
# ---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def posts_endpoint(request):
    """
    GET  /api/posts  → list posts
    POST /api/posts  → create post
    """
    if request.method == 'GET':
        posts = Post.objects.select_related('user').all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

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
        serializer = ReplySerializer(replies, many=True, context={'request': request})
        return Response(serializer.data)

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
        post.reply_count += 1
        post.save(update_fields=['reply_count'])

    logger.info("replies_endpoint: created reply on post %s by user %s", post_id, user.username)
    return Response(ReplySerializer(reply, context={'request': request}).data, status=201)