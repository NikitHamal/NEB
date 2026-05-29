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

from django.db import transaction
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from .authentication import verify_google_token
from .models import User, Resource, Post, PostLike, Reply, ReplyLike, FCMToken, Follow, UserPhoto
from .serializers import (
    UserSerializer, UserPublicSerializer,
    ResourceSerializer, PostSerializer, ReplySerializer,
    UserPhotoSerializer, UserStatsSerializer, FollowSerializer,
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
    """GET /api/resources — public endpoint, no auth needed.

    Query params:
      subject — filter by subject (case-insensitive)
      grade   — filter by grade_level (case-insensitive)
      type    — filter by type (case-insensitive)
      search  — search in title + description (case-insensitive)
      page    — page number for pagination (optional; if absent, returns all)
    """
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

    page_param = request.query_params.get('page')
    if page_param is not None:
        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(resources, request)
        serializer = ResourceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
        post.delete()
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
            post.title = data['title'].strip()
        if 'content' in data:
            post.content = data['content'].strip()
        if 'category' in data:
            post.category = data['category'].strip()
        post.save()
        return Response(PostSerializer(post, context={'request': request}).data)

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
            post = reply.post
            reply.delete()
            post.reply_count = max(0, post.reply_count - 1)
            post.save(update_fields=['reply_count'])
        return Response({'success': True})

    content = request.data.get('content', '').strip()
    if content:
        reply.content = content
        reply.save()
    return Response(ReplySerializer(reply, context={'request': request}).data)


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
        Q(title__icontains=query) | Q(content__icontains=query)
    )

    return Response({
        'resources': ResourceSerializer(resources, many=True).data,
        'posts': PostSerializer(posts, many=True, context={'request': request}).data,
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
      category — filter by category (case-insensitive)
      search   — search in title + content (case-insensitive)
      page     — page number for pagination (optional; if absent, returns all)
    """
    if request.method == 'GET':
        posts = Post.objects.select_related('user').all()

        category = request.query_params.get('category')
        search = request.query_params.get('search')

        if category:
            posts = posts.filter(category__iexact=category)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        page_param = request.query_params.get('page')
        if page_param is not None:
            paginator = PageNumberPagination()
            paginator.page_size = 50
            page = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

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


# ---------------------------------------------------------------------------
# COMMUNITY — USER STATS
# ---------------------------------------------------------------------------

def _build_stats(user):
    """
    Build the stats dict for a given User instance.
    contribution_score: posts*3 + replies*2 + likes_given*1
    Designed to be extended (resources submitted, etc.) in future.
    """
    from django.db.models import Sum
    post_count = Post.objects.filter(user=user).count()
    reply_count = Reply.objects.filter(user=user).count()
    follower_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    post_likes = Post.objects.filter(user=user).aggregate(t=Sum('thumbs_up_count'))['t'] or 0
    reply_likes = Reply.objects.filter(user=user).aggregate(t=Sum('thumbs_up_count'))['t'] or 0
    likes_received = post_likes + reply_likes

    likes_given = (PostLike.objects.filter(user=user).count() +
                   ReplyLike.objects.filter(user=user).count())

    contribution_score = (post_count * 3) + (reply_count * 2) + likes_given

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


@api_view(['GET'])
@authentication_classes([])
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

    stats = _build_stats(user)
    requesting_user = _get_user_from_request(request)
    is_following = False
    if requesting_user and requesting_user.pk != user.pk:
        is_following = Follow.objects.filter(follower=requesting_user, following=user).exists()

    stats['is_following'] = is_following
    stats['is_self'] = bool(requesting_user and requesting_user.pk == user.pk)
    return Response(stats)


# ---------------------------------------------------------------------------
# COMMUNITY — FOLLOW / UNFOLLOW
# ---------------------------------------------------------------------------

@api_view(['POST'])
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
        else:
            Follow.objects.create(
                follower=current_user,
                following=target_user,
                created_at=_now_ms()
            )
            is_following = True

    follower_count = Follow.objects.filter(following=target_user).count()
    return Response({'is_following': is_following, 'follower_count': follower_count})


@api_view(['GET'])
@authentication_classes([])
def user_followers_list(request, user_id):
    """
    GET /api/users/<userId>/followers
    Lists all Follow records where following=user_id (i.e. users who follow this user).
    """
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    follows = Follow.objects.filter(following=target_user).select_related('follower')
    return Response(FollowSerializer(follows, many=True).data)


@api_view(['GET'])
@authentication_classes([])
def user_following_list(request, user_id):
    """
    GET /api/users/<userId>/following
    Lists all Follow records where follower=user_id (i.e. users this person follows).
    """
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    follows = Follow.objects.filter(follower=target_user).select_related('following')
    return Response(FollowSerializer(follows, many=True).data)


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
        import os
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return Response({'error': 'Invalid image format. Only JPG, PNG, GIF, and WEBP are allowed.'}, status=400)
            
        filename = f"{current_user.id}_{_now_ms()}{ext}"
        path = default_storage.save(os.path.join('profile_photos', filename), ContentFile(file_obj.read()))
        url = request.build_absolute_uri(settings.MEDIA_URL + path)

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