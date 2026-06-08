"""
Real-time broadcast helpers.

The single entry point for pushing events from Django code to all connected
WebSocket clients. All call sites should use these helpers so event names
and channel conventions stay consistent.

Channels layer is configured in settings.py with a Redis backend so
broadcasts fan out across all daphne / Passenger worker processes.
"""
import logging
from typing import Any, Dict, Optional

try:
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
except ImportError:
    def async_to_sync(fn, *args, **kwargs):  # type: ignore
        return None
    def get_channel_layer():
        return None

from django.core.cache import cache

from .consumers_ws import (
    GRP_FORUM_PUBLIC,
    GRP_POST_FMT,
    GRP_RESOURCE_FMT,
    GRP_RESOURCE_REQUEST_FMT,
    GRP_USER_FMT,
)
from .utils import now_ms

logger = logging.getLogger(__name__)


def _send(group: str, event: str, data: Dict[str, Any]):
    """Push an event to a single group. No-op if the channel layer is missing."""
    layer = get_channel_layer()
    if layer is None:
        return
    try:
        async_to_sync(layer.group_send)(
            group,
            {
                'type': 'realtime.event',
                'channel': group,
                'event': event,
                'data': {**data, 'ts': now_ms()},
            },
        )
    except Exception as e:  # noqa: BLE001
        # Don't let WS failures cascade into HTTP 500s.
        logger.warning('realtime send failed (group=%s event=%s): %s', group, event, e)


# ----------------------------------------------------------------------- forums

def broadcast_post_created(post_data: Dict[str, Any]):
    """A new post landed. Show it on /forum and home carousels."""
    _send(GRP_FORUM_PUBLIC, 'post.created', post_data)


def broadcast_post_updated(post_id: str, changes: Dict[str, Any]):
    _send(GRP_FORUM_PUBLIC, 'post.updated', {'post_id': post_id, 'changes': changes})
    _send(GRP_POST_FMT.format(post_id=post_id), 'post.updated', {'post_id': post_id, 'changes': changes})


def broadcast_post_deleted(post_id: str):
    _send(GRP_FORUM_PUBLIC, 'post.deleted', {'post_id': post_id})
    _send(GRP_POST_FMT.format(post_id=post_id), 'post.deleted', {'post_id': post_id})


def broadcast_post_like_changed(post_id: str, thumbs_up_count: int, is_thumbed_up_by_viewer_hint: Optional[bool] = None):
    _send(GRP_FORUM_PUBLIC, 'post.like_changed', {'post_id': post_id, 'thumbs_up_count': thumbs_up_count})
    _send(GRP_POST_FMT.format(post_id=post_id), 'post.like_changed', {'post_id': post_id, 'thumbs_up_count': thumbs_up_count})


def broadcast_reply_created(post_id: str, reply_data: Dict[str, Any]):
    _send(GRP_POST_FMT.format(post_id=post_id), 'reply.created', reply_data)
    _send(GRP_FORUM_PUBLIC, 'reply.created', {'post_id': post_id, 'reply': reply_data})


def broadcast_reply_updated(post_id: str, reply_id: str, changes: Dict[str, Any]):
    _send(GRP_POST_FMT.format(post_id=post_id), 'reply.updated', {'post_id': post_id, 'reply_id': reply_id, 'changes': changes})


def broadcast_reply_deleted(post_id: str, reply_id: str, deleted_by: str = 'self'):
    _send(GRP_POST_FMT.format(post_id=post_id), 'reply.deleted', {'post_id': post_id, 'reply_id': reply_id, 'deleted_by': deleted_by})


def broadcast_reply_like_changed(post_id: str, reply_id: str, thumbs_up_count: int):
    _send(GRP_POST_FMT.format(post_id=post_id), 'reply.like_changed', {
        'post_id': post_id, 'reply_id': reply_id, 'thumbs_up_count': thumbs_up_count,
    })


# ----------------------------------------------------------------------- resources

def broadcast_resource_like_changed(resource_id: str, like_count: int):
    _send(GRP_RESOURCE_FMT.format(resource_id=resource_id), 'resource.like_changed', {
        'resource_id': resource_id, 'like_count': like_count,
    })


def broadcast_resource_comment_created(resource_id: str, comment_data: Dict[str, Any]):
    _send(GRP_RESOURCE_FMT.format(resource_id=resource_id), 'resource.comment_created', comment_data)


def broadcast_resource_comment_deleted(resource_id: str, comment_id: str):
    _send(GRP_RESOURCE_FMT.format(resource_id=resource_id), 'resource.comment_deleted', {
        'resource_id': resource_id, 'comment_id': comment_id,
    })


def broadcast_resource_request_created(request_data: Dict[str, Any]):
    _send(GRP_FORUM_PUBLIC, 'resource_request.created', request_data)


# ----------------------------------------------------------------------- profile / social

def broadcast_follow_changed(target_user_id: str, follower_count: int, is_following_by_actor_id: Optional[str] = None):
    # Notify the target user
    _send(GRP_USER_FMT.format(user_id=target_user_id), 'follow.changed', {
        'target_user_id': target_user_id, 'follower_count': follower_count,
    })


def broadcast_user_stats_changed(user_id: str, stats: Dict[str, Any]):
    _send(GRP_USER_FMT.format(user_id=user_id), 'user.stats_changed', {'user_id': user_id, 'stats': stats})


# ----------------------------------------------------------------------- notifications

def broadcast_notification(user_id: str, payload: Dict[str, Any]):
    """Push a new notification to a single user.

    The payload is what the JS client will use to render the toast/badge
    update. Keep it small: id, verb, actor summary, target reference.
    """
    _send(GRP_USER_FMT.format(user_id=user_id), 'notification.new', payload)


def broadcast_unread_count(user_id: str, count: int):
    _send(GRP_USER_FMT.format(user_id=user_id), 'notification.unread_count', {'count': count})


# ----------------------------------------------------------------------- system

def broadcast_system(message: str, level: str = 'info'):
    """Site-wide announcement. Goes to all connected clients."""
    _send(GRP_FORUM_PUBLIC, 'system.message', {'message': message, 'level': level})


# ----------------------------------------------------------------------- health

def get_health_snapshot() -> Dict[str, Any]:
    """Return a small dict with current WS health stats. For the health endpoint."""
    # Best-effort: the channel layer doesn't expose group size, so we count
    # the in-process connections via cache keys set by the consumer.
    total_conns = cache.get('ws:health:total_conns') or 0
    return {
        'channel_layer': bool(get_channel_layer()),
        'cached_conns': total_conns,
        'now_ms': now_ms(),
    }
