"""
Direct service functions for web views to call instead of HTTP API roundtrips.
These replicate the business logic from api/views.py but return Python dicts
instead of DRF Response objects, and accept User objects instead of DRF requests.
"""
import logging
import re
from collections import Counter

from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User, Post, PostLike, PostImage, Poll, PollOption, PollVote, Reply, ReplyLike, Follow, UserPhoto, EditHistory, FollowRequest
from .models import Resource, ResourceLike, ResourceComment, ResourceCommentLike, Bookmark, Notification, FCMToken, ResourceRequest
from .models import BlogComment, BlogCommentLike, Announcement
from .security import hash_password, issue_auth_token, verify_password, POST_IMAGE_MAX_COUNT
from .utils import now_ms, uuid_str
from . import counters as _counters
from . import notifications as _notif
from . import neby as _neby
from . import realtime as _rt
from . import content_images as _cimg

logger = logging.getLogger(__name__)


def _prep_inline_images(content):
    """Sanitise [[img:ID]] tokens in user content and flag the referenced
    uploads as used. Returns (cleaned_content, referenced_ids)."""
    cleaned = _cimg.clean_content(content)
    ids = _cimg.extract_image_ids(cleaned)
    if ids:
        _cimg.mark_used(ids)
    return cleaned, ids


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
            transaction.on_commit(lambda: _counters.increment_user_likes_given(user.id))
            if post.user_id != user.id:
                transaction.on_commit(lambda: _counters.increment_user_likes_received(post.user_id))
            transaction.on_commit(lambda: _notif.notify_post_liked(user.id, post_id))
        else:
            like.delete()
            Post.objects.filter(pk=post_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(post.thumbs_up_count - 1, 0)
            transaction.on_commit(lambda: _counters.decrement_user_likes_given(user.id))
            if post.user_id != user.id:
                transaction.on_commit(lambda: _counters.decrement_user_likes_received(post.user_id))
            transaction.on_commit(lambda: _notif.notify_post_unliked(user.id, post_id))
    _rt.broadcast_post_like_changed(post_id, current_count, is_thumbed_up_by_viewer_hint=is_thumbed_up, user_id=str(user.id))
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
            transaction.on_commit(lambda: _counters.increment_user_likes_given(user.id))
            if reply.user_id != user.id:
                transaction.on_commit(lambda: _counters.increment_user_likes_received(reply.user_id))
            transaction.on_commit(lambda: _notif.notify_reply_liked(user.id, reply_id))
        else:
            like.delete()
            Reply.objects.filter(pk=reply_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(reply.thumbs_up_count - 1, 0)
            transaction.on_commit(lambda: _counters.decrement_user_likes_given(user.id))
            if reply.user_id != user.id:
                transaction.on_commit(lambda: _counters.decrement_user_likes_received(reply.user_id))
            transaction.on_commit(lambda: _notif.notify_reply_unliked(user.id, reply_id))
    _rt.broadcast_reply_like_changed(reply.post_id, reply_id, current_count, is_thumbed_up_by_viewer_hint=is_thumbed_up, user_id=str(user.id))
    return {'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up}


def create_reply(user, post_id, content, parent_reply_id=None, is_anonymous=False, attachments=None,
                 poll_data=None):
    if not getattr(user, 'email_verified', False):
        return None
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return None
    content = content.strip()
    if not content and not attachments and not poll_data:
        return None
    if parent_reply_id and not Reply.objects.filter(pk=parent_reply_id, post_id=post_id).exists():
        # Invalid parent reply (missing or belongs to another post)
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=uuid_str(),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            reply_count=0,
            is_anonymous=bool(is_anonymous),
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)
        if poll_data:
            from . import polls as _polls
            _polls.create_poll(poll_data, reply=reply, now=now)
        if attachments:
            from .models import PostMedia
            for order, item in enumerate(attachments):
                PostMedia.objects.create(
                    id=uuid_str(), reply=reply,
                    kind=item['kind'], url=item['url'], name=item['name'],
                    mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                    order=order, created_at=now,
                )
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id, anonymous_actor=is_anonymous)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id, anonymous_actor=is_anonymous)
    _neby.enqueue_if_reply_mention(reply)
    _notif.send_mention_all_if_eligible(user, content, 'reply', reply.id)
    from .serializers import ReplySerializer
    reply_data = ReplySerializer(reply).data
    _rt.broadcast_reply_created(post_id, reply_data)
    return reply_data


def create_post(user, title, content, category, image_urls=None, poll_data=None,
                is_anonymous=False, attachments=None, own_tag=False):
    if not getattr(user, 'email_verified', False):
        return None
    from .categories import normalize_category

    title = title.strip()
    content = content.strip()
    category = normalize_category(category, own_tag=own_tag)
    if not title or not content or not category:
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    post = Post.objects.create(
        id=uuid_str(),
        user=user,
        title=title,
        content=content,
        category=category,
        thumbs_up_count=0,
        reply_count=0,
        is_anonymous=bool(is_anonymous),
        created_at=now,
    )
    if image_urls:
        for i, url in enumerate(image_urls[:POST_IMAGE_MAX_COUNT]):
            PostImage.objects.create(
                id=uuid_str(),
                post=post,
                image_url=url,
                order=i,
                created_at=now,
            )
    if attachments:
        from .models import PostMedia
        for order, item in enumerate(attachments):
            PostMedia.objects.create(
                id=uuid_str(), post=post,
                kind=item['kind'], url=item['url'], name=item['name'],
                mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                order=order, created_at=now,
            )
    if poll_data:
        from . import polls as _polls
        _polls.create_poll(poll_data, post=post, now=now)
    _counters.increment_user_post_count(user.id)
    _neby.enqueue_if_post_mention(post)
    _notif.send_mention_all_if_eligible(user, f'{title} {content}', 'post', post.id)
    from .serializers import PostSerializer
    post_data = PostSerializer(post).data
    _rt.broadcast_post_created(post_data)
    return post_data


def vote_poll(user, poll_id, option_ids):
    """Vote on a poll. option_ids can be a single id or a list for multiple selection."""
    if isinstance(option_ids, str):
        option_ids = [option_ids]
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        return {'error': 'Poll not found'}, 404
    if poll.is_expired:
        return {'error': 'This poll has expired'}, 400
    valid_options = []
    for oid in option_ids:
        try:
            opt = PollOption.objects.get(pk=oid, poll=poll)
            valid_options.append(opt)
        except PollOption.DoesNotExist:
            return {'error': 'Invalid poll option'}, 400
    if not valid_options:
        return {'error': 'No options selected'}, 400
    if not poll.allow_multiple and len(valid_options) > 1:
        return {'error': 'This poll allows only one option'}, 400
    with transaction.atomic():
        if poll.allow_multiple:
            existing = PollVote.objects.filter(poll=poll, user=user, option__in=valid_options)
            if existing.exists():
                return {'error': 'You have already voted on one or more of these options'}, 400
            for opt in valid_options:
                PollVote.objects.create(
                    id=uuid_str(),
                    poll=poll,
                    option=opt,
                    user=user,
                    created_at=now_ms(),
                )
                PollOption.objects.filter(pk=opt.id).update(vote_count=F('vote_count') + 1)
            Poll.objects.filter(pk=poll_id).update(total_votes=F('total_votes') + len(valid_options))
        else:
            existing = PollVote.objects.filter(poll=poll, user=user).first()
            if existing:
                return {'error': 'You have already voted on this poll'}, 400
            opt = valid_options[0]
            PollVote.objects.create(
                id=uuid_str(),
                poll=poll,
                option=opt,
                user=user,
                created_at=now_ms(),
            )
            PollOption.objects.filter(pk=opt.id).update(vote_count=F('vote_count') + 1)
            Poll.objects.filter(pk=poll_id).update(total_votes=F('total_votes') + 1)
    from . import polls as _polls
    poll = Poll.objects.prefetch_related('options').get(pk=poll_id)
    payload = _polls.poll_dict(poll, user.id)
    payload['total_votes'] = poll.total_votes
    return payload, 200


def toggle_follow(user, target_user_id, desired=None):
    """Follow/unfollow a user or send/cancel follow request for private accounts.

    desired may be "follow" or "unfollow" for idempotent UI calls. When omitted,
    the toggle behavior is preserved.
    """
    desired = (desired or '').strip().lower() or None
    if desired not in (None, 'follow', 'unfollow'):
        desired = None
    if str(user.id) == str(target_user_id):
        return {'error': 'You cannot follow yourself'}, 400
    try:
        target_user = User.objects.get(pk=target_user_id)
    except User.DoesNotExist:
        return {'error': 'User not found'}, 404

    is_following = False
    requested = False
    notify_follow = False
    notify_unfollow = False
    notify_request = False
    notify_cancel_request = False
    
    with transaction.atomic():
        # Check if already following
        existing_follow = Follow.objects.select_for_update().filter(follower=user, following=target_user).first()
        
        # Check if there is a pending request
        existing_request = FollowRequest.objects.select_for_update().filter(sender=user, receiver=target_user).first()
        
        if target_user.is_locked:
            # For private profiles:
            if existing_follow:
                # If already following, we can unfollow
                if desired == 'follow':
                    is_following = True
                else:
                    existing_follow.delete()
                    is_following = False
                    notify_unfollow = True
            elif existing_request:
                # If there's a pending request, we can cancel it
                if desired == 'follow':
                    requested = True
                else:
                    existing_request.delete()
                    requested = False
                    notify_cancel_request = True
            else:
                # Neither exists
                if desired == 'unfollow':
                    pass
                else:
                    # Create a new follow request
                    FollowRequest.objects.create(
                        id=uuid_str(),
                        sender=user,
                        receiver=target_user,
                        created_at=now_ms()
                    )
                    requested = True
                    notify_request = True
        else:
            # For public profiles (standard logic):
            if existing_follow:
                if desired == 'follow':
                    is_following = True
                else:
                    existing_follow.delete()
                    is_following = False
                    notify_unfollow = True
            else:
                if desired == 'unfollow':
                    pass
                else:
                    Follow.objects.create(follower=user, following=target_user, created_at=now_ms())
                    is_following = True
                    notify_follow = True

        follower_count = Follow.objects.filter(following=target_user).count()
        following_count = Follow.objects.filter(follower=user).count()
        is_mutual = bool(is_following and Follow.objects.filter(follower=target_user, following=user).exists())
        User.objects.filter(pk=target_user.id).update(follower_count=follower_count)
        User.objects.filter(pk=user.id).update(following_count=following_count)

    if notify_follow:
        _notif.notify_new_follow(user.id, target_user.id)
    elif notify_unfollow:
        _notif.notify_unfollow(user.id, target_user.id)
    elif notify_request:
        _notif.notify_new_follow_request(user.id, target_user.id)
    elif notify_cancel_request:
        _notif.notify_cancel_follow_request(user.id, target_user.id)
        
    _rt.broadcast_follow_changed(target_user.id, follower_count)
    
    return {
        'is_following': is_following,
        'requested': requested,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_mutual': is_mutual,
    }, 200

def check_username_available(username):
    exists = User.objects.filter(username__iexact=username).exists()
    return {'available': not exists}


# Every field avatar_or_photo_url() reads. A queryset that renders avatars and uses
# .only() must include these, or each user costs one extra query per field.
AVATAR_FIELDS = ('username', 'photo_url')


def avatar_or_photo_url(user):
    """The uploaded profile photo, or '' when there is none.

    There are no generated avatars: every client draws the same neutral
    fallback (the initial on a flat tone) when this is empty. Old rows that
    stored a generated-avatar path as their photo count as "no photo"."""
    photo = (getattr(user, 'photo_url', None) or '').strip()
    from urllib.parse import urlparse
    if urlparse(photo).path.startswith('/avatar/'):
        return ''
    return photo


def get_user_anon_tag(user_or_id):
    """Deterministic anonymous handle derived from user ID (e.g. Anon#8f2c)."""
    if not user_or_id:
        return 'Anonymous Nebian'
    uid = getattr(user_or_id, 'id', user_or_id)
    if not uid:
        return 'Anonymous Nebian'
    import hashlib
    h = hashlib.sha256(str(uid).encode('utf-8')).hexdigest()[:4].lower()
    return f'Anon#{h}'


USERNAME_COOLDOWN_DAYS = [7, 15, 30, 60, 100]
DAY_MS = 24 * 60 * 60 * 1000


def username_change_status(user, now=None):
    from .utils import now_ms
    now = now or now_ms()
    count = user.username_change_count or 0
    last = user.username_changed_at or 0
    if count <= 0 or not last:
        return {
            'allowed': True,
            'change_count': count,
            'cooldown_days': 0,
            'days_left': 0,
            'next_change_at': 0,
            'schedule': list(USERNAME_COOLDOWN_DAYS),
        }
    cooldown_days = USERNAME_COOLDOWN_DAYS[min(count - 1, len(USERNAME_COOLDOWN_DAYS) - 1)]
    next_change_at = last + cooldown_days * DAY_MS
    days_left = max(0, (next_change_at - now) / DAY_MS)
    return {
        'allowed': now >= next_change_at,
        'change_count': count,
        'cooldown_days': cooldown_days,
        'days_left': days_left,
        'next_change_at': next_change_at,
        'schedule': list(USERNAME_COOLDOWN_DAYS),
    }


def record_username_change(user, now=None):
    from .utils import now_ms
    now = now or now_ms()
    user.username_changed_at = now
    user.username_change_count = (user.username_change_count or 0) + 1


def validate_username_change(user, new_username, now=None):
    if new_username == user.username:
        return {'error': 'New username is the same as the current one.'}, 400
    if not new_username or len(new_username) < 3 or len(new_username) > 50 or not new_username.replace('_', '').isalnum():
        return {'error': 'Username must be 3-50 characters and can only contain letters, numbers, and underscores.'}, 400
    status = username_change_status(user, now)
    if not status['allowed']:
        from datetime import datetime
        ready = datetime.fromtimestamp(status['next_change_at'] / 1000.0)
        return {
            'error': 'You changed your username recently. You can change it again on %s (in %d days).' % (
                ready.strftime('%B %d, %Y'), int(status['days_left']) + 1),
            'status': status,
        }, 429
    conflict = User.objects.filter(username__iexact=new_username).exclude(pk=user.id).exists()
    if conflict:
        return {'error': 'Username already taken.'}, 409
    return None, 200


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
    return {'status': 'success', 'message': 'Password set successfully', 'user': UserSerializer(user).data}, 200


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
    # Revoke every existing session BEFORE issuing the new token, so a
    # password change evicts attackers holding old bearer tokens.
    from .security import revoke_all_user_tokens
    revoke_all_user_tokens(user)
    user.password_hash = hash_password(new_password)
    auth_token = issue_auth_token(user, save=False)
    user.save(update_fields=['password_hash', 'auth_token'])
    from .serializers import UserSerializer
    return {
        'status': 'success',
        'message': 'Password changed successfully',
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    }, 200


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


def toggle_resource_like(user, resource_id):
    with transaction.atomic():
        try:
            resource = Resource.objects.select_for_update().get(pk=resource_id)
        except Resource.DoesNotExist:
            raise
        like, created = ResourceLike.objects.get_or_create(resource=resource, user=user)
        if created:
            Resource.objects.filter(pk=resource_id).update(like_count=F('like_count') + 1)
            is_liked = True
            current_count = resource.like_count + 1
            _counters.increment_user_likes_given(user.id)
            if resource.uploaded_by_id and str(resource.uploaded_by_id) != str(user.id):
                _counters.increment_user_likes_received(resource.uploaded_by_id)
        else:
            like.delete()
            Resource.objects.filter(pk=resource_id, like_count__gt=0).update(like_count=F('like_count') - 1)
            is_liked = False
            current_count = max(resource.like_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if resource.uploaded_by_id and str(resource.uploaded_by_id) != str(user.id):
                _counters.decrement_user_likes_received(resource.uploaded_by_id)
    if is_liked:
        _notif.notify_resource_liked(user.id, resource_id)
    else:
        _notif.notify_resource_unliked(user.id, resource_id)
    _rt.broadcast_resource_like_changed(resource_id, current_count)
    return {'likeCount': current_count, 'isLiked': is_liked}


def toggle_resource_comment_like(user, comment_id):
    with transaction.atomic():
        try:
            comment = ResourceComment.objects.select_for_update().get(pk=comment_id)
        except ResourceComment.DoesNotExist:
            raise
        like, created = ResourceCommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            ResourceComment.objects.filter(pk=comment_id).update(like_count=F('like_count') + 1)
            is_liked = True
            current_count = comment.like_count + 1
            _counters.increment_user_likes_given(user.id)
            if comment.user_id and str(comment.user_id) != str(user.id):
                _counters.increment_user_likes_received(comment.user_id)
        else:
            like.delete()
            ResourceComment.objects.filter(pk=comment_id, like_count__gt=0).update(like_count=F('like_count') - 1)
            is_liked = False
            current_count = max(comment.like_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if comment.user_id and str(comment.user_id) != str(user.id):
                _counters.decrement_user_likes_received(comment.user_id)
    if is_liked:
        _notif.notify_resource_comment_liked(user.id, comment_id)
    else:
        _notif.notify_resource_comment_unliked(user.id, comment_id)
    # Comment-level like events broadcast on their own comment-scoped event;
    # the resource-level like_changed keeps carrying only resource counts.
    _rt.broadcast_resource_comment_like_changed(
        comment.resource_id, comment_id, current_count,
        is_liked_by_viewer_hint=is_liked, user_id=str(user.id),
    )
    return {'likeCount': current_count, 'isLiked': is_liked}


def create_resource_comment(user, resource_id, content, parent_comment_id=None, attachments=None, is_anonymous=False):
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return None
    content = content.strip()
    if not content and not attachments:
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    with transaction.atomic():
        comment = ResourceComment.objects.create(
            id=uuid_str(),
            resource=resource,
            parent_comment_id=parent_comment_id,
            user=user,
            content=content,
            like_count=0,
            reply_count=0,
            is_anonymous=bool(is_anonymous),
            created_at=now,
        )
        Resource.objects.filter(pk=resource_id).update(comment_count=F('comment_count') + 1)
        if parent_comment_id:
            ResourceComment.objects.filter(pk=parent_comment_id).update(reply_count=F('reply_count') + 1)
        if attachments:
            from .models import ResourceCommentMedia
            for order, item in enumerate(attachments):
                ResourceCommentMedia.objects.create(
                    id=uuid_str(), comment=comment,
                    kind=item['kind'], url=item['url'], name=item['name'],
                    mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                    order=order, created_at=now,
                )
    if user:
        _counters.increment_user_reply_count(user.id)
        if parent_comment_id:
            _notif.notify_resource_comment_reply(user.id, parent_comment_id, resource_id, comment.id)
        else:
            _notif.notify_resource_comment(user.id, resource_id, comment.id)
    data = _serialize_resource_comment(comment)
    _rt.broadcast_resource_comment_created(resource_id, data)
    return data


def delete_resource_comment(user, comment_id, is_admin=False):
    try:
        comment = ResourceComment.objects.select_related('resource').get(pk=comment_id)
    except ResourceComment.DoesNotExist:
        return False
    if not is_admin and comment.user_id != user.id:
        return False
    resource_id = comment.resource_id
    parent_id = comment.parent_comment_id
    # Count this comment + all children for counter adjustment
    child_count = ResourceComment.objects.filter(parent_comment_id=comment_id).count()
    total_removed = 1 + child_count
    with transaction.atomic():
        # Delete children first (cascades anyway, but for counter accuracy)
        ResourceComment.objects.filter(parent_comment_id=comment_id).delete()
        comment.delete()
        Resource.objects.filter(pk=resource_id, comment_count__gt=0).update(
            comment_count=F('comment_count') - total_removed
        )
    if parent_id:
        ResourceComment.objects.filter(pk=parent_id, reply_count__gt=0).update(
            reply_count=F('reply_count') - 1
        )
    _counters.decrement_user_reply_count(user.id)
    _rt.broadcast_resource_comment_deleted(resource_id, comment_id)
    return True


def _serialize_media_payload(media_iterable):
    """PostMedia/ResourceCommentMedia rows → camelCase attachment dicts,
    same shape as PostMediaSerializer."""
    from .security import get_video_qualities, media_poster
    res = []
    for m in media_iterable:
        thumb = media_poster(m)
        quals = get_video_qualities(m.url) if getattr(m, 'kind', '') == 'video' else []
        res.append({
            'id': m.id,
            'kind': m.kind,
            'url': m.url,
            'thumbnailUrl': thumb,
            'thumbnail_url': thumb,
            'qualities': quals,
            'name': m.name,
            'mimeType': m.mime_type,
            'sizeBytes': m.size_bytes,
            'order': m.order,
            'createdAt': m.created_at,
        })
    return res


def _serialize_resource_comment(comment):
    """Serialize a ResourceComment to a dict for JSON responses."""
    media = comment.media.all() if hasattr(comment, 'media') else []
    user = getattr(comment, 'user', None)
    if user:
        author_photo = avatar_or_photo_url(user) or ''
    else:
        author_photo = ''
    return {
        'id': comment.id,
        'resourceId': comment.resource_id,
        'authorId': comment.user_id or '',
        'authorName': comment.user.username if hasattr(comment, 'user') and comment.user else 'Deleted user',
        'authorPhoto': author_photo,
        'parentCommentId': comment.parent_comment_id or '',
        'content': comment.content,
        'likeCount': comment.like_count,
        'replyCount': comment.reply_count,
        'isEdited': comment.is_edited,
        'createdAt': comment.created_at,
        'attachments': _serialize_media_payload(media),
    }


# ── Blog Comment Services ──

def toggle_blog_comment_like(user, comment_id):
    with transaction.atomic():
        try:
            comment = BlogComment.objects.select_for_update().get(pk=comment_id)
        except BlogComment.DoesNotExist:
            raise
        like, created = BlogCommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            BlogComment.objects.filter(pk=comment_id).update(like_count=F('like_count') + 1)
            is_liked = True
            current_count = comment.like_count + 1
        else:
            like.delete()
            BlogComment.objects.filter(pk=comment_id, like_count__gt=0).update(like_count=F('like_count') - 1)
            is_liked = False
            current_count = max(comment.like_count - 1, 0)
    return {'likeCount': current_count, 'isLiked': is_liked}

def create_blog_comment(user, slug, content, parent_comment_id=None, attachments=None, is_anonymous=False):
    try:
        announcement = Announcement.objects.get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        return None
    content = content.strip()
    if not content and not attachments:
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    with transaction.atomic():
        comment = BlogComment.objects.create(
            id=uuid_str(),
            announcement=announcement,
            parent_comment_id=parent_comment_id,
            author=user,
            text=content,
            like_count=0,
            reply_count=0,
            is_anonymous=bool(is_anonymous),
            created_at=now,
        )
        if parent_comment_id:
            BlogComment.objects.filter(pk=parent_comment_id).update(reply_count=F('reply_count') + 1)
        if attachments:
            from .models import BlogCommentMedia
            for order, item in enumerate(attachments):
                BlogCommentMedia.objects.create(
                    id=uuid_str(), comment=comment,
                    kind=item['kind'], url=item['url'], name=item['name'],
                    mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                    order=order, created_at=now,
                )
    return {'id': comment.id}

def delete_blog_comment(user, comment_id, is_admin=False):
    try:
        comment = BlogComment.objects.get(pk=comment_id)
    except BlogComment.DoesNotExist:
        return False
    if not is_admin and comment.author_id != str(user.id):
        return False
    parent_id = comment.parent_comment_id
    with transaction.atomic():
        BlogComment.objects.filter(parent_comment_id=comment_id).delete()
        comment.delete()
    if parent_id:
        BlogComment.objects.filter(pk=parent_id, reply_count__gt=0).update(
            reply_count=F('reply_count') - 1
        )
    return True


def delete_user_account(user_id, completed_by=None):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return False

    Resource.objects.filter(uploaded_by=user).update(
        uploaded_by=None,
        source_type='anonymous',
        author_name='Anonymous'
    )
    ResourceRequest.objects.filter(requested_by=user).update(
        requested_by=None,
        requester_name='Anonymous'
    )

    with transaction.atomic():
        post_likes = list(PostLike.objects.filter(user=user).values_list('post_id', 'post__user_id'))
        PostLike.objects.filter(user=user).delete()
        for post_id, n in Counter(pid for pid, _ in post_likes).items():
            Post.objects.filter(pk=post_id, thumbs_up_count__gte=n).update(
                thumbs_up_count=F('thumbs_up_count') - n
            )
        for uid, n in Counter(uid for _, uid in post_likes if uid and uid != user.id).items():
            User.objects.filter(pk=uid, likes_received_count__gte=n).update(
                likes_received_count=F('likes_received_count') - n
            )

        reply_likes = list(ReplyLike.objects.filter(user=user).values_list('reply_id', 'reply__user_id'))
        ReplyLike.objects.filter(user=user).delete()
        for reply_id, n in Counter(rid for rid, _ in reply_likes).items():
            Reply.objects.filter(pk=reply_id, thumbs_up_count__gte=n).update(
                thumbs_up_count=F('thumbs_up_count') - n
            )
        for uid, n in Counter(uid for _, uid in reply_likes if uid and uid != user.id).items():
            User.objects.filter(pk=uid, likes_received_count__gte=n).update(
                likes_received_count=F('likes_received_count') - n
            )

        liked_resources = Counter(
            ResourceLike.objects.filter(user=user).values_list('resource_id', flat=True)
        )
        ResourceLike.objects.filter(user=user).delete()
        for resource_id, n in liked_resources.items():
            Resource.objects.filter(pk=resource_id, like_count__gte=n).update(
                like_count=F('like_count') - n
            )

        liked_rcomments = Counter(
            ResourceCommentLike.objects.filter(user=user).values_list('comment_id', flat=True)
        )
        ResourceCommentLike.objects.filter(user=user).delete()
        for comment_id, n in liked_rcomments.items():
            ResourceComment.objects.filter(pk=comment_id, like_count__gte=n).update(
                like_count=F('like_count') - n
            )

        liked_bcomments = Counter(
            BlogCommentLike.objects.filter(user=user).values_list('comment_id', flat=True)
        )
        BlogCommentLike.objects.filter(user=user).delete()
        for comment_id, n in liked_bcomments.items():
            BlogComment.objects.filter(pk=comment_id, like_count__gte=n).update(
                like_count=F('like_count') - n
            )

        followed_ids = list(Follow.objects.filter(follower=user).values_list('following_id', flat=True))
        follower_ids = list(Follow.objects.filter(following=user).values_list('follower_id', flat=True))
        Follow.objects.filter(follower=user).delete()
        Follow.objects.filter(following=user).delete()
        for uid, n in Counter(followed_ids).items():
            if uid != user.id:
                User.objects.filter(pk=uid, follower_count__gte=n).update(
                    follower_count=F('follower_count') - n
                )
        for uid, n in Counter(follower_ids).items():
            if uid != user.id:
                User.objects.filter(pk=uid, following_count__gte=n).update(
                    following_count=F('following_count') - n
                )

        Bookmark.objects.filter(user=user).delete()
        EditHistory.objects.filter(edited_by=user).delete()
        UserPhoto.objects.filter(user=user).delete()
        FCMToken.objects.filter(user=user).delete()
        PollVote.objects.filter(user=user).delete()

        affected_recipients = set(
            Notification.objects.filter(recipient=user).values_list('recipient_id', flat=True)
        )
        affected_recipients.update(
            r for r in Notification.objects.filter(actor=user).values_list('recipient_id', flat=True) if r
        )
        Notification.objects.filter(recipient=user).delete()
        Notification.objects.filter(actor=user).delete()

        user.delete()

    _notif.batch_fix_unread_counts(affected_recipients)
    logger.info(
        "delete_user_account: deleted user %s (completed_by=%s)",
        user_id, getattr(completed_by, 'id', None),
    )
    return True