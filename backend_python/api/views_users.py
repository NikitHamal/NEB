"""Views Users extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403

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
    if not _can_view_locked_profile(requesting_user, user):
        is_following = bool(requesting_user and Follow.objects.filter(follower=requesting_user, following=user).exists())
        return Response({
            'username': user.username,
            'post_count': 0,
            'reply_count': 0,
            'follower_count': 0,
            'following_count': 0,
            'likes_received': 0,
            'likes_given': 0,
            'contribution_score': 0,
            'is_following': is_following,
            'is_self': is_owner,
            'is_private': True,
        })

    stats = _build_stats(user)
    is_following = False
    if requesting_user and requesting_user.pk != user.pk:
        is_following = Follow.objects.filter(follower=requesting_user, following=user).exists()

    stats['is_following'] = is_following
    stats['is_self'] = is_owner
    return Response(stats)

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
    follows = Follow.objects.filter(following=target_user).select_related('follower')
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
    follows = Follow.objects.filter(follower=target_user).select_related('following')
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
