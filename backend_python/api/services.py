"""
Direct service functions for web views to call instead of HTTP API roundtrips.
These replicate the business logic from api/views.py but return Python dicts
instead of DRF Response objects, and accept User objects instead of DRF requests.
"""
import logging

from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User, Post, PostLike, PostImage, Poll, PollOption, PollVote, Reply, ReplyLike, Follow, UserPhoto, EditHistory
from .models import Resource, ResourceLike, ResourceComment, ResourceCommentLike
from .security import hash_password, issue_auth_token, verify_password, validate_profile_photo_url, validate_external_https_url
from .utils import now_ms, uuid_str
from . import counters as _counters
from . import notifications as _notif
from . import neby as _neby
from . import realtime as _rt

logger = logging.getLogger(__name__)


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
            _notif.notify_post_liked(user.id, post_id)
        else:
            like.delete()
            Post.objects.filter(pk=post_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(post.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.decrement_user_likes_received(post.user_id)
            _notif.notify_post_unliked(user.id, post_id)
    _rt.broadcast_post_like_changed(post_id, current_count)
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
            _notif.notify_reply_liked(user.id, reply_id)
        else:
            like.delete()
            Reply.objects.filter(pk=reply_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(reply.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.decrement_user_likes_received(reply.user_id)
            _notif.notify_reply_unliked(user.id, reply_id)
    _rt.broadcast_reply_like_changed(reply.post_id, reply_id, current_count)
    return {'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up}


def create_reply(user, post_id, content, parent_reply_id=None):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return None
    content = content.strip()
    if not content:
        return None
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
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id)
    _neby.enqueue_if_reply_mention(reply)
    from .serializers import ReplySerializer
    reply_data = ReplySerializer(reply).data
    _rt.broadcast_reply_created(post_id, reply_data)
    return reply_data


def create_post(user, title, content, category, image_urls=None, poll_data=None):
    title = title.strip()
    content = content.strip()
    category = category.strip()
    if not title or not content or not category:
        return None
    now = now_ms()
    post = Post.objects.create(
        id=uuid_str(),
        user=user,
        title=title,
        content=content,
        category=category,
        thumbs_up_count=0,
        reply_count=0,
        created_at=now,
    )
    if image_urls:
        for i, url in enumerate(image_urls[:3]):
            PostImage.objects.create(
                id=uuid_str(),
                post=post,
                image_url=url,
                order=i,
                created_at=now,
            )
    if poll_data:
        poll = Poll.objects.create(
            id=uuid_str(),
            post=post,
            question=poll_data.get('question', ''),
            poll_type=poll_data.get('poll_type', 'voting'),
            allow_multiple=poll_data.get('allow_multiple', False),
            explanation=poll_data.get('explanation', ''),
            duration_ms=poll_data.get('duration_ms', 0),
            total_votes=0,
            created_at=now,
        )
        for i, opt in enumerate(poll_data.get('options', [])):
            if isinstance(opt, dict):
                opt_text = opt.get('text', '').strip()
                is_correct = opt.get('is_correct', False)
            else:
                opt_text = opt.strip()
                is_correct = False
            if opt_text:
                PollOption.objects.create(
                    id=uuid_str(),
                    poll=poll,
                    text=opt_text,
                    is_correct=is_correct,
                    vote_count=0,
                    order=i,
                )
    _counters.increment_user_post_count(user.id)
    _neby.enqueue_if_post_mention(post)
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
    poll.refresh_from_db()
    options = list(PollOption.objects.filter(poll=poll).order_by('order'))
    return {
        'id': poll.id,
        'question': poll.question,
        'pollType': poll.poll_type,
        'allowMultiple': poll.allow_multiple,
        'explanation': poll.explanation,
        'total_votes': poll.total_votes,
        'isExpired': poll.is_expired,
        'options': [{'id': o.id, 'text': o.text, 'is_correct': o.is_correct, 'vote_count': o.vote_count, 'order': o.order} for o in options],
        'userVote': [str(o.id) for o in valid_options] if poll.allow_multiple else str(valid_options[0].id),
    }, 200


def toggle_follow(user, target_user_id, desired=None):
    """Follow/unfollow a user.

    desired may be "follow" or "unfollow" for idempotent UI calls. When omitted,
    the legacy toggle behavior is preserved. Counts are recalculated from the
    Follow table so stale denormalized counters cannot make profiles show 0.
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

    notify_follow = False
    notify_unfollow = False
    with transaction.atomic():
        existing = Follow.objects.select_for_update().filter(follower=user, following=target_user).first()
        if existing:
            if desired == 'follow':
                is_following = True
            else:
                existing.delete()
                is_following = False
                notify_unfollow = True
        else:
            if desired == 'unfollow':
                is_following = False
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
    _rt.broadcast_follow_changed(target_user.id, follower_count)
    return {
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_mutual': is_mutual,
    }, 200

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
    # Comment-level like broadcasts go to the resource channel because the
    # client renders comments inline under the resource view.
    _rt.broadcast_resource_like_changed(comment.resource_id, current_count)
    return {'likeCount': current_count, 'isLiked': is_liked}


def create_resource_comment(user, resource_id, content, parent_comment_id=None):
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return None
    content = content.strip()
    if not content:
        return None
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
            created_at=now,
        )
        Resource.objects.filter(pk=resource_id).update(comment_count=F('comment_count') + 1)
        if parent_comment_id:
            ResourceComment.objects.filter(pk=parent_comment_id).update(reply_count=F('reply_count') + 1)
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


def _serialize_resource_comment(comment):
    """Serialize a ResourceComment to a dict for JSON responses."""
    return {
        'id': comment.id,
        'resourceId': comment.resource_id,
        'authorId': comment.user_id,
        'authorName': comment.user.username if hasattr(comment, 'user') and comment.user else '',
        'authorPhoto': comment.user.photo_url if hasattr(comment, 'user') and comment.user else '',
        'parentCommentId': comment.parent_comment_id or '',
        'content': comment.content,
        'likeCount': comment.like_count,
        'replyCount': comment.reply_count,
        'isEdited': comment.is_edited,
        'createdAt': comment.created_at,
    }
