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
import uuid
import time

from django.db import transaction
from django.db.models import F

from .models import Notification, User, Post, Reply
from . import counters as _counters

logger = logging.getLogger(__name__)


def _now_ms():
    return int(time.time() * 1000)


def _create_notification(*, recipient_id, actor_id, verb, target_type, target_id,
                         reference_type='', reference_id='', message=''):
    """
    Core notification creation. Handles deduplication and counter updates.
    Returns the created Notification, or None if skipped (self-notification or duplicate).
    """
    if str(recipient_id) == str(actor_id):
        return None
    try:
        recipient = User.objects.get(pk=recipient_id)
    except User.DoesNotExist:
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
        id=str(uuid.uuid4()),
        recipient_id=recipient_id,
        actor_id=actor_id,
        verb=verb,
        target_type=target_type,
        target_id=target_id,
        reference_type=reference_type,
        reference_id=reference_id,
        message=message,
        is_read=False,
        created_at=_now_ms(),
    )
    _counters.increment_user_unread_notification_count(recipient_id)
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
    notif = Notification.objects.create(
        id=str(uuid.uuid4()),
        recipient_id=recipient_id,
        actor_id=None,
        verb='system',
        target_type=target_type,
        target_id=target_id,
        reference_type='',
        reference_id='',
        message=message,
        is_read=False,
        created_at=_now_ms(),
    )
    _counters.increment_user_unread_notification_count(recipient_id)
    return notif


def notify_system_broadcast(message, target_type='system', target_id=''):
    """Send a system notification to all users."""
    user_ids = list(User.objects.values_list('id', flat=True))
    now = _now_ms()
    objs = []
    for uid in user_ids:
        objs.append(Notification(
            id=str(uuid.uuid4()),
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
    User.objects.all().update(unread_notification_count=F('unread_notification_count') + 1)


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