"""
Direct service functions for web views to call instead of HTTP API roundtrips.
These replicate the business logic from api/views.py but return Python dicts
instead of DRF Response objects, and accept User objects instead of DRF requests.
"""
import logging
import uuid
import time

from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User, Post, PostLike, Reply, ReplyLike, Follow, UserPhoto, EditHistory
from .security import hash_password, verify_password, validate_profile_photo_url, validate_external_https_url
from . import counters as _counters

logger = logging.getLogger(__name__)


def _now_ms():
    return int(time.time() * 1000)


def toggle_post_like(user, post_id):
    with transaction.atomic():
        try:
            post = Post.objects.select_for_update().get(pk=post_id)
        except Post.DoesNotExist:
            raise
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if created:
            Post.objects.filter(pk=post_id).update(thumbs_up_count=F('thumbs_up_count') + 1)
            is_thumbed_up = True
            current_count = post.thumbs_up_count + 1
            _counters.increment_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.increment_user_likes_received(post.user_id)
        else:
            like.delete()
            Post.objects.filter(pk=post_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(post.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.decrement_user_likes_received(post.user_id)
    return {'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up}


def toggle_reply_like(user, reply_id):
    with transaction.atomic():
        try:
            reply = Reply.objects.select_for_update().get(pk=reply_id)
        except Reply.DoesNotExist:
            raise
        like, created = ReplyLike.objects.get_or_create(reply=reply, user=user)
        if created:
            Reply.objects.filter(pk=reply_id).update(thumbs_up_count=F('thumbs_up_count') + 1)
            is_thumbed_up = True
            current_count = reply.thumbs_up_count + 1
            _counters.increment_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.increment_user_likes_received(reply.user_id)
        else:
            like.delete()
            Reply.objects.filter(pk=reply_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(reply.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.decrement_user_likes_received(reply.user_id)
    return {'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up}


def create_reply(user, post_id, content, parent_reply_id=None):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return None
    content = content.strip()
    if not content:
        return None
    now = _now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=str(uuid.uuid4()),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            reply_count=0,
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)
    _counters.increment_user_reply_count(user.id)
    from .serializers import ReplySerializer
    return ReplySerializer(reply).data


def create_post(user, title, content, category):
    title = title.strip()
    content = content.strip()
    category = category.strip()
    if not title or not content or not category:
        return None
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
    _counters.increment_user_post_count(user.id)
    from .serializers import PostSerializer
    return PostSerializer(post).data


def toggle_follow(user, target_user_id):
    if str(user.id) == str(target_user_id):
        return {'error': 'You cannot follow yourself'}, 400
    try:
        target_user = User.objects.get(pk=target_user_id)
    except User.DoesNotExist:
        return {'error': 'User not found'}, 404
    with transaction.atomic():
        existing = Follow.objects.filter(follower=user, following=target_user).first()
        if existing:
            existing.delete()
            is_following = False
            _counters.decrement_user_follower_count(target_user.id)
            _counters.decrement_user_following_count(user.id)
        else:
            Follow.objects.create(follower=user, following=target_user, created_at=_now_ms())
            is_following = True
            _counters.increment_user_follower_count(target_user.id)
            _counters.increment_user_following_count(user.id)
    follower_count = target_user.follower_count if hasattr(target_user, 'follower_count') and target_user.follower_count > 0 else Follow.objects.filter(following=target_user).count()
    return {'is_following': is_following, 'follower_count': follower_count}


def check_username_available(username):
    exists = User.objects.filter(username__iexact=username).exists()
    return {'available': not exists}


def set_password(user, password):
    from django.contrib.auth.password_validation import validate_password as django_validate_password
    try:
        django_validate_password(password)
    except DjangoValidationError as exc:
        return {'error': ' '.join(exc.messages)}, 400
    if user.password_hash:
        return {'error': 'Password already set. Use change-password instead.'}, 400
    user.password_hash = hash_password(password)
    user.email_verified = True
    user.save(update_fields=['password_hash', 'email_verified'])
    from .serializers import UserSerializer
    return {'status': 'success', 'message': 'Password set successfully', 'user': UserSerializer(user).data}


def change_password(user, current_password, new_password):
    from django.contrib.auth.password_validation import validate_password as django_validate_password
    if not current_password or not new_password:
        return {'error': 'Current password and new password are required'}, 400
    try:
        django_validate_password(new_password)
    except DjangoValidationError as exc:
        return {'error': ' '.join(exc.messages)}, 400
    if not user.password_hash:
        return {'error': 'No password set. Use set-password instead.'}, 400
    password_ok, needs_rehash = verify_password(current_password, user.password_hash)
    if not password_ok:
        return {'error': 'Current password is incorrect'}, 401
    user.password_hash = hash_password(new_password)
    user.auth_token = User.generate_token()
    user.save(update_fields=['password_hash', 'auth_token'])
    from .serializers import UserSerializer
    return {
        'status': 'success',
        'message': 'Password changed successfully',
        'authToken': user.auth_token,
        'user': UserSerializer(user).data,
    }


def activate_photo(user, photo_id):
    try:
        photo = UserPhoto.objects.get(pk=photo_id, user=user)
    except UserPhoto.DoesNotExist:
        return None
    UserPhoto.objects.filter(user=user).update(is_current=False)
    photo.is_current = True
    photo.save(update_fields=['is_current'])
    user.photo_url = photo.url
    user.save(update_fields=['photo_url'])
    return {'id': photo.id, 'url': photo.url, 'uploaded_at': photo.uploaded_at, 'is_current': True, 'success': True, 'photo_url': photo.url}