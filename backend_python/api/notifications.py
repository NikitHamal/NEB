"""
Notification service layer.
Handles creating, deleting, and managing notifications with proper
counter updates and deduplication.

Design principles:
- Never notify yourself (actor != recipient)
- Deduplicate: one notification per (recipient, actor, verb, target_type, target_id)
- Auto-delete on undo (unlike, unfollow) or content deletion
- Denormalized unread_notification_count on User model for fast badge queries
- System notifications have no actor (null)
"""
import logging

from django.core.cache import cache
from django.db import transaction
from django.db.models import F

from .models import Notification, User, Post, Reply, Resource, ResourceComment
from .utils import now_ms, uuid_str
from . import counters as _counters
from . import realtime as _rt

logger = logging.getLogger(__name__)


def _create_notification(*, recipient_id, actor_id, verb, target_type, target_id,
                         reference_type='', reference_id='', message=''):
    """
    Core notification creation. Handles deduplication and counter updates.
    Returns the created Notification, or None if skipped (self-notification, bot recipient, or duplicate).
    Note: bots are allowed to be actors (so bot replies can notify post authors),
    but bot accounts never receive notifications.
    """
    if str(recipient_id) == str(actor_id):
        return None
    try:
        recipient = User.objects.get(pk=recipient_id)
    except User.DoesNotExist:
        return None
    if recipient.is_bot:
        return None
    existing = Notification.objects.filter(
        recipient_id=recipient_id,
        actor_id=actor_id,
        verb=verb,
        target_type=target_type,
        target_id=target_id,
    ).first()
    if existing:
        return existing
    notification = Notification.objects.create(
        id=uuid_str(),
        recipient_id=recipient_id,
        actor_id=actor_id,
        verb=verb,
        target_type=target_type,
        target_id=target_id,
        reference_type=reference_type,
        reference_id=reference_id,
        message=message,
        is_read=False,
        created_at=now_ms(),
    )
    _counters.increment_user_unread_notification_count(recipient_id)
    _rt.broadcast_notification(recipient_id, {
        'id': notification.id,
        'verb': verb,
        'actor_id': actor_id,
        'target_type': target_type,
        'target_id': target_id,
        'reference_type': reference_type,
        'reference_id': reference_id,
        'message': message,
        'created_at': notification.created_at,
    })
    # Also push the new unread count so the badge updates without polling.
    try:
        user = recipient
        _rt.broadcast_unread_count(user.id, user.unread_notification_count)
    except Exception:  # noqa: BLE001
        pass
    return notification


def _delete_notification(*, recipient_id, actor_id, verb, target_type, target_id):
    """
    Delete a specific notification (e.g. when user unlikes something).
    Decrements the unread counter only if the notification was unread.
    """
    try:
        notif = Notification.objects.get(
            recipient_id=recipient_id,
            actor_id=actor_id,
            verb=verb,
            target_type=target_type,
            target_id=target_id,
        )
    except Notification.DoesNotExist:
        return
    was_unread = not notif.is_read
    notif.delete()
    if was_unread:
        _counters.decrement_user_unread_notification_count(recipient_id)


def notify_post_liked(actor_id, post_id):
    """Called when someone likes a post. Creates notification for post author."""
    try:
        post = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        return None
    return _create_notification(
        recipient_id=post.user_id,
        actor_id=actor_id,
        verb='like_post',
        target_type='post',
        target_id=post_id,
    )


def notify_post_unliked(actor_id, post_id):
    """Called when someone unlikes a post. Removes the notification."""
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return
    _delete_notification(
        recipient_id=post.user_id,
        actor_id=actor_id,
        verb='like_post',
        target_type='post',
        target_id=post_id,
    )


def notify_reply_liked(actor_id, reply_id):
    """Called when someone likes a reply. Creates notification for reply author."""
    try:
        reply = Reply.objects.select_related('user').get(pk=reply_id)
    except Reply.DoesNotExist:
        return None
    return _create_notification(
        recipient_id=reply.user_id,
        actor_id=actor_id,
        verb='like_reply',
        target_type='reply',
        target_id=reply_id,
    )


def notify_reply_unliked(actor_id, reply_id):
    """Called when someone unlikes a reply. Removes the notification."""
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return
    _delete_notification(
        recipient_id=reply.user_id,
        actor_id=actor_id,
        verb='like_reply',
        target_type='reply',
        target_id=reply_id,
    )


def notify_new_reply(actor_id, post_id, reply_id):
    """
    Called when someone replies to a post.
    Notifies the post author (verb='reply').
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return None
    return _create_notification(
        recipient_id=post.user_id,
        actor_id=actor_id,
        verb='reply',
        target_type='post',
        target_id=post_id,
        reference_type='reply',
        reference_id=reply_id,
    )


def notify_reply_to_reply(actor_id, parent_reply_id, post_id, reply_id):
    """
    Called when someone replies to a reply (nested reply).
    Notifies the parent reply author (verb='reply_reply').
    """
    try:
        parent_reply = Reply.objects.get(pk=parent_reply_id)
    except Reply.DoesNotExist:
        return None
    if str(parent_reply.user_id) == str(actor_id):
        return None
    return _create_notification(
        recipient_id=parent_reply.user_id,
        actor_id=actor_id,
        verb='reply_reply',
        target_type='reply',
        target_id=parent_reply_id,
        reference_type='post',
        reference_id=post_id,
    )


def notify_new_follow(actor_id, target_user_id):
    """Called when someone follows a user."""
    return _create_notification(
        recipient_id=target_user_id,
        actor_id=actor_id,
        verb='follow',
        target_type='user',
        target_id=target_user_id,
    )


def notify_unfollow(actor_id, target_user_id):
    """Called when someone unfollows a user. Removes the follow notification."""
    _delete_notification(
        recipient_id=target_user_id,
        actor_id=actor_id,
        verb='follow',
        target_type='user',
        target_id=target_user_id,
    )


def notify_system(recipient_id, message, target_type='system', target_id=''):
    """
    Create a system notification (no actor).
    target_id defaults to empty string for general announcements.
    """
    try:
        recipient = User.objects.get(pk=recipient_id)
    except User.DoesNotExist:
        return None
    if recipient.is_bot:
        return None
    notif = Notification.objects.create(
        id=uuid_str(),
        recipient_id=recipient_id,
        actor_id=None,
        verb='system',
        target_type=target_type,
        target_id=target_id,
        reference_type='',
        reference_id='',
        message=message,
        is_read=False,
        created_at=now_ms(),
    )
    _counters.increment_user_unread_notification_count(recipient_id)
    _rt.broadcast_notification(recipient_id, {
        'id': notif.id,
        'verb': 'system',
        'actor_id': None,
        'target_type': target_type,
        'target_id': target_id,
        'reference_type': '',
        'reference_id': '',
        'message': message,
        'created_at': notif.created_at,
    })
    return notif


def notify_system_broadcast(message, target_type='system', target_id=''):
    """Send a system notification to all users (skip bots)."""
    user_ids = list(User.objects.filter(is_bot=False).values_list('id', flat=True))
    now = now_ms()
    objs = []
    for uid in user_ids:
        objs.append(Notification(
            id=uuid_str(),
            recipient_id=uid,
            actor_id=None,
            verb='system',
            target_type=target_type,
            target_id=target_id,
            reference_type='',
            reference_id='',
            message=message,
            is_read=False,
            created_at=now,
        ))
    Notification.objects.bulk_create(objs)
    User.objects.filter(is_bot=False).update(unread_notification_count=F('unread_notification_count') + 1)
    cache.delete_many([f'unread_count:{uid}' for uid in user_ids])
    # Fan out to all connected users. Each user has their own `user.<id>`
    # group, so we walk them. Cheap because we only push the metadata; the
    # full notification row is fetched on demand by the client.
    for uid in user_ids:
        _rt.broadcast_notification(uid, {
            'verb': 'system',
            'actor_id': None,
            'target_type': target_type,
            'target_id': target_id,
            'message': message,
            'created_at': now,
        })
    _rt.broadcast_system(message)


def notify_resource_liked(actor_id, resource_id):
    """Called when someone likes a resource. Creates notification for resource uploader."""
    try:
        resource = Resource.objects.select_related('uploaded_by').get(pk=resource_id)
    except Resource.DoesNotExist:
        return None
    if not resource.uploaded_by_id:
        return None
    return _create_notification(
        recipient_id=resource.uploaded_by_id,
        actor_id=actor_id,
        verb='like_resource',
        target_type='resource',
        target_id=resource_id,
    )


def notify_resource_unliked(actor_id, resource_id):
    """Called when someone unlikes a resource. Removes the notification."""
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return
    if not resource.uploaded_by_id:
        return
    _delete_notification(
        recipient_id=resource.uploaded_by_id,
        actor_id=actor_id,
        verb='like_resource',
        target_type='resource',
        target_id=resource_id,
    )


def notify_resource_comment_liked(actor_id, comment_id):
    """Called when someone likes a resource comment. Creates notification for comment author."""
    try:
        comment = ResourceComment.objects.select_related('user').get(pk=comment_id)
    except ResourceComment.DoesNotExist:
        return None
    return _create_notification(
        recipient_id=comment.user_id,
        actor_id=actor_id,
        verb='like_resource_comment',
        target_type='resource_comment',
        target_id=comment_id,
        reference_type='resource',
        reference_id=comment.resource_id,
    )


def notify_resource_comment_unliked(actor_id, comment_id):
    """Called when someone unlikes a resource comment. Removes the notification."""
    try:
        comment = ResourceComment.objects.get(pk=comment_id)
    except ResourceComment.DoesNotExist:
        return
    _delete_notification(
        recipient_id=comment.user_id,
        actor_id=actor_id,
        verb='like_resource_comment',
        target_type='resource_comment',
        target_id=comment_id,
    )


def notify_resource_comment(actor_id, resource_id, comment_id):
    """Called when someone comments on a resource. Notifies the resource uploader."""
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return None
    if not resource.uploaded_by_id:
        return None
    return _create_notification(
        recipient_id=resource.uploaded_by_id,
        actor_id=actor_id,
        verb='resource_comment',
        target_type='resource',
        target_id=resource_id,
        reference_type='resource_comment',
        reference_id=comment_id,
    )


def notify_resource_comment_reply(actor_id, parent_comment_id, resource_id, comment_id):
    """Called when someone replies to a resource comment. Notifies the parent comment author."""
    try:
        parent_comment = ResourceComment.objects.get(pk=parent_comment_id)
    except ResourceComment.DoesNotExist:
        return None
    if str(parent_comment.user_id) == str(actor_id):
        return None
    return _create_notification(
        recipient_id=parent_comment.user_id,
        actor_id=actor_id,
        verb='resource_comment_reply',
        target_type='resource_comment',
        target_id=parent_comment_id,
        reference_type='resource',
        reference_id=resource_id,
    )


def notify_resource_approved(resource_id, uploader_id):
    """Called when a resource is approved. Notifies the uploader."""
    if not uploader_id:
        return None
    return notify_system(
        recipient_id=uploader_id,
        message='Your resource has been approved! It is now visible to everyone.',
        target_type='resource',
        target_id=resource_id,
    )


def notify_resource_rejected(resource_id, uploader_id, reason=''):
    """Called when a resource is rejected. Notifies the uploader with the reason."""
    if not uploader_id:
        return None
    msg = 'Your resource was not approved.'
    if reason:
        msg = f'Your resource was not approved. Reason: {reason}'
    return notify_system(
        recipient_id=uploader_id,
        message=msg,
        target_type='resource',
        target_id=resource_id,
    )


def delete_notifications_for_target(target_type, target_id):
    """
    Delete ALL notifications related to a target (e.g. when a post or reply is deleted).
    Properly decrements unread counters for affected recipients.
    """
    notifs = Notification.objects.filter(target_type=target_type, target_id=target_id)
    unread_recipient_ids = list(
        notifs.filter(is_read=False).values_list('recipient_id', flat=True).distinct()
    )
    notifs.delete()
    for rid in unread_recipient_ids:
        count = Notification.objects.filter(recipient_id=rid, is_read=False).count()
        User.objects.filter(pk=rid).update(unread_notification_count=count)
        cache.delete(f'unread_count:{rid}')


def delete_notifications_for_actor_and_target(actor_id, verb, target_type, target_id):
    """
    Delete notifications matching actor+verb+target, regardless of recipient.
    Used when content is deleted by the author.
    """
    notifs = Notification.objects.filter(
        actor_id=actor_id,
        verb=verb,
        target_type=target_type,
        target_id=target_id,
    )
    unread_recipient_ids = list(
        notifs.filter(is_read=False).values_list('recipient_id', flat=True).distinct()
    )
    notifs.delete()
    for rid in unread_recipient_ids:
        count = Notification.objects.filter(recipient_id=rid, is_read=False).count()
        User.objects.filter(pk=rid).update(unread_notification_count=count)
        cache.delete(f'unread_count:{rid}')