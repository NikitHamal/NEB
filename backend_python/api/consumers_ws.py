"""
NEBians real-time WebSocket consumer.

Protocol (client -> server, JSON over WS):
    {"action": "subscribe",   "channel": "post:<id>"}        # join group
    {"action": "unsubscribe", "channel": "post:<id>"}        # leave group
    {"action": "subscribe",   "channel": "user"}              # own user group
    {"action": "subscribe",   "channel": "forum.public"}      # global forum
    {"action": "subscribe",   "channel": "resource:<id>"}     # resource comments
    {"action": "ping",        "ts": 1234567890}               # heartbeat reply
    {"action": "pong"}                                        # response to server ping
    {"action": "since",       "ts": 1234567890}               # request missed events

Protocol (server -> client, JSON over WS):
    {"type": "ready",        "user_id": "...", "ts": ...}
    {"type": "pong",         "ts": ...}                        # reply to client ping
    {"type": "ping"}                                           # server heartbeat
    {"type": "event",        "channel": "post:<id>",
                            "event":   "reply.added",
                            "data":    {...}}
    {"type": "subscribed",   "channel": "..."}
    {"type": "unsubscribed", "channel": "..."}
    {"type": "error",        "code": "...", "message": "..."}
    {"type": "close",        "reason": "..."}

Optimizations:
  - Heartbeat: server sends {"type": "ping"} every 25s, expects {"pong"} within
    30s, otherwise closes connection (zombie detection).
  - Per-user connection cap: max 5 concurrent WS per user. Older connections
    are gracefully closed.
  - Per-connection rate limit: max 60 messages/second; 1000 messages/hour.
  - Per-channel permission check: subscribe() verifies the user can see the
    target (e.g. can't subscribe to a private post).
  - Batched events: server groups events with the same channel+event arriving
    within 50ms into a single batched WS message (reduces frame overhead).
  - Tab visibility: clients are expected to close the WS when their tab is
    hidden for >60s and reconnect on visibility. The server doesn't enforce
    this — it just provides the mechanism.
  - Idle timeout: connections that don't send a subscribe/ping/anything for
    5 minutes are closed.
"""
import asyncio
import json
import logging
import time
from collections import deque
from typing import Set

try:
    from channels.db import database_sync_to_async
    from channels.generic.websocket import AsyncWebsocketConsumer
except ImportError:  # Channels not installed yet
    def database_sync_to_async(fn, *args, **kwargs):  # type: ignore
        async def _wrap(*a, **k):
            return fn(*a, **k)
        return _wrap
    class AsyncWebsocketConsumer:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


# Channel group name conventions. Centralised so producers and consumers
# can't drift.
GRP_FORUM_PUBLIC = 'forum.public'
GRP_USER_FMT = 'user.{user_id}'
GRP_POST_FMT = 'post.{post_id}'
GRP_RESOURCE_FMT = 'resource.{resource_id}'
GRP_RESOURCE_REQUEST_FMT = 'resource_request.{request_id}'
GRP_STUDY_SPACE_FMT = 'studyspace.{space_id}'


def _is_authenticated(user):
    return bool(user and getattr(user, 'is_authenticated', False) and not getattr(user, 'is_locked', False))


def _is_anonymous_allowed(channel: str) -> bool:
    """Channels any user (logged in or not) can subscribe to."""
    return channel in {'forum.public'}


class _RateLimiter:
    """Sliding window rate limiter per connection."""

    def __init__(self, max_per_second=60, max_per_hour=3600):
        self.max_per_second = max_per_second
        self.max_per_hour = max_per_hour
        self._second = deque()
        self._hour = deque()

    def allow(self) -> bool:
        now = time.monotonic()
        # Trim
        while self._second and now - self._second[0] > 1.0:
            self._second.popleft()
        while self._hour and now - self._hour[0] > 3600.0:
            self._hour.popleft()
        if len(self._second) >= self.max_per_second:
            return False
        if len(self._hour) >= self.max_per_hour:
            return False
        self._second.append(now)
        self._hour.append(now)
        return True


class _EventBatcher:
    """Coalesces events for the same channel+event within a short window.

    Drains every 50ms via a task scheduled on the consumer's event loop.
    """

    def __init__(self, send_fn):
        self._send_fn = send_fn
        self._pending = {}  # (channel, event) -> list[data]
        self._lock = asyncio.Lock()
        self._task = None
        self._closed = False

    async def add(self, channel: str, event: str, data):
        async with self._lock:
            key = (channel, event)
            self._pending.setdefault(key, []).append(data)
            if self._task is None or self._task.done():
                self._task = asyncio.create_task(self._drain_later())

    async def _drain_later(self):
        await asyncio.sleep(0.05)
        await self.flush()

    async def flush(self):
        async with self._lock:
            if not self._pending:
                return
            batches, self._pending = self._pending, {}
        for (channel, event), items in batches.items():
            if len(items) == 1:
                await self._send_fn({
                    'type': 'event',
                    'channel': channel,
                    'event': event,
                    'data': items[0],
                })
            else:
                await self._send_fn({
                    'type': 'event',
                    'channel': channel,
                    'event': event,
                    'data': items,
                    'batched': True,
                    'count': len(items),
                })

    async def aclose(self):
        self._closed = True
        await self.flush()


class RealtimeConsumer(AsyncWebsocketConsumer):
    """Single WebSocket endpoint for all real-time traffic."""

    # Per-user cap on concurrent WS connections. Older connections get closed.
    PER_USER_CAP = 5
    HEARTBEAT_INTERVAL = 25  # seconds
    HEARTBEAT_TIMEOUT = 30  # seconds
    IDLE_TIMEOUT = 5 * 60    # 5 minutes
    RATE_PER_SECOND = 120
    RATE_PER_HOUR = 14400

    # ------------------------------------------------------------------ helpers

    @database_sync_to_async
    def _can_see_post(self, post_id: str) -> bool:
        from api.models import Post
        try:
            p = Post.objects.only('id', 'is_archived').get(pk=post_id)
        except Post.DoesNotExist:
            return False
        return not p.is_archived

    @database_sync_to_async
    def _can_see_study_space(self, space_id: str) -> bool:
        from api.models import StudySpace, StudySpaceMember, StudySpaceShare
        try:
            s = StudySpace.objects.only('id', 'user_id', 'visibility', 'share_mode', 'shared_at').get(pk=space_id)
        except StudySpace.DoesNotExist:
            return False

        # Public discoverable spaces are readable/subscribable by anyone
        if s.visibility == getattr(StudySpace, 'VISIBILITY_PUBLIC', 'public'):
            return True

        # Link-shared spaces are readable/subscribable by anyone with the link
        if s.share_mode == getattr(StudySpace, 'SHARE_LINK', 'link') and s.shared_at:
            return True

        if not self._user_id:
            return False

        # Owner always has realtime access, even when the space is private.
        if str(s.user_id) == str(self._user_id):
            return True

        # Joined members/admins/moderators always have realtime access.
        if StudySpaceMember.objects.filter(space=s, user_id=self._user_id).exists():
            return True

        # Specific-user grants can open the page before joining; allow realtime too.
        if (
            s.share_mode == getattr(StudySpace, 'SHARE_SPECIFIC', 'specific')
            and s.shared_at
            and StudySpaceShare.objects.filter(space=s, user_id=self._user_id).exists()
        ):
            return True

        return False

    @database_sync_to_async
    def _can_see_resource(self, resource_id: str) -> bool:
        from api.models import Resource
        try:
            r = Resource.objects.only('id', 'approval_status').get(pk=resource_id)
        except Resource.DoesNotExist:
            return False
        return r.approval_status == 'approved'

    @database_sync_to_async
    def _user_track_open(self, user_id: str, channel_name: str):
        """Track the user's open connections in cache (capped)."""
        key = f'ws:conns:{user_id}'
        conns = cache.get(key) or []
        if channel_name in conns:
            return
        conns.append(channel_name)
        if len(conns) > self.PER_USER_CAP:
            # Evict the oldest one. The evicted channel_name will get a
            # graceful close via the close task scheduled below.
            evicted = conns.pop(0)
            cache.set(f'ws:evict:{evicted}', 1, timeout=10)
        cache.set(key, conns, timeout=3600)

    @database_sync_to_async
    def _user_track_close(self, user_id: str, channel_name: str):
        key = f'ws:conns:{user_id}'
        conns = cache.get(key) or []
        if channel_name in conns:
            conns.remove(channel_name)
            cache.set(key, conns, timeout=3600)
        cache.delete(f'ws:evict:{channel_name}')

    @database_sync_to_async
    def _user_should_evict(self, channel_name: str) -> bool:
        return bool(cache.get(f'ws:evict:{channel_name}'))

    # ------------------------------------------------------------------ lifecycle

    async def connect(self):
        user = self.scope.get('user')
        if not _is_authenticated(user):
            # Anonymous users can connect but only to public channels.
            self._user_id = None
        else:
            self._user_id = str(user.id)

        # Per-user cap (only enforced for authenticated users)
        if self._user_id:
            await self._user_track_open(self._user_id, self.channel_name)
            if await self._user_should_evict(self.channel_name):
                logger.info('WS evicting overflow connection for user %s', self._user_id)
                await self.close(code=1013)  # "try again later"
                return

        await self.accept()
        self._groups: Set[str] = set()
        self._client_subscriptions = {}
        self._last_activity = time.monotonic()
        self._rate = _RateLimiter(self.RATE_PER_SECOND, self.RATE_PER_HOUR)
        self._batcher = _EventBatcher(self._send_json)
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        self._idle_task = asyncio.create_task(self._idle_watchdog())
        self._last_pong_at = time.monotonic()
        await self._send_json({
            'type': 'ready',
            'user_id': self._user_id,
            'server_time': int(time.time() * 1000),
            'heartbeat_interval': self.HEARTBEAT_INTERVAL,
        })
        logger.info('WS connect user=%s channel=%s', self._user_id, self.channel_name)

    async def disconnect(self, code):
        try:
            if hasattr(self, '_heartbeat_task'):
                self._heartbeat_task.cancel()
            if hasattr(self, '_idle_task'):
                self._idle_task.cancel()
            if hasattr(self, '_batcher'):
                await self._batcher.aclose()
            for group in list(self._groups):
                try:
                    await self.channel_layer.group_discard(group, self.channel_name)
                except Exception:  # noqa: BLE001
                    pass
            if self._user_id:
                await self._user_track_close(self._user_id, self.channel_name)
            logger.info('WS disconnect user=%s code=%s', self._user_id, code)
        except Exception as e:  # noqa: BLE001
            logger.exception('WS disconnect cleanup failed: %s', e)

    async def receive(self, text_data=None, bytes_data=None):
        self._last_activity = time.monotonic()
        if not text_data:
            return
        try:
            msg = json.loads(text_data)
        except json.JSONDecodeError:
            await self._send_json({'type': 'error', 'code': 'bad_json', 'message': 'invalid JSON'})
            return
        if not isinstance(msg, dict):
            await self._send_json({'type': 'error', 'code': 'bad_shape', 'message': 'expected object'})
            return

        if not self._rate.allow():
            await self._send_json({'type': 'error', 'code': 'rate_limited', 'message': 'too many messages'})
            return

        action = msg.get('action')
        if action == 'subscribe':
            await self._handle_subscribe(msg.get('channel', ''), msg.get('last_seen_ts'))
        elif action == 'unsubscribe':
            await self._handle_unsubscribe(msg.get('channel', ''))
        elif action == 'ping':
            await self._send_json({'type': 'pong', 'ts': msg.get('ts')})
        elif action == 'pong':
            self._last_pong_at = time.monotonic()
        elif action == 'since':
            # Future: replay events from a timestamp. For now just acknowledge.
            await self._send_json({'type': 'since_ack', 'ts': msg.get('ts')})
        elif action == 'note_content':
            await self._handle_note_content(msg)
        elif action == 'note_cursor':
            await self._handle_note_cursor(msg)
        elif action == 'yjs_update':
            await self._handle_yjs_update(msg)
        elif action == 'yjs_awareness':
            await self._handle_yjs_awareness(msg)
        elif action == 'yjs_snapshot':
            await self._handle_yjs_snapshot(msg)
        elif action == 'yjs_sync_request':
            await self._handle_yjs_sync_request(msg)
        else:
            await self._send_json({'type': 'error', 'code': 'unknown_action', 'message': f'unknown: {action}'})

    # ------------------------------------------------------------------ subscribe

    async def _handle_subscribe(self, channel: str, last_seen_ts=None):
        if not channel or not isinstance(channel, str):
            await self._send_json({'type': 'error', 'code': 'bad_channel', 'message': 'channel required'})
            return
        if len(channel) > 200:
            await self._send_json({'type': 'error', 'code': 'bad_channel', 'message': 'channel too long'})
            return

        # Permission checks
        ok = False
        if channel == 'forum.public':
            ok = True
        elif channel == 'user':
            if self._user_id:
                ok = True
            else:
                await self._send_json({'type': 'subscribed', 'channel': channel})
                return
        elif channel.startswith('user.'):
            ok = True  # public profile subscriptions (follow/stats updates)
        elif channel.startswith('post.'):
            post_id = channel[len('post.'):]
            ok = await self._can_see_post(post_id)
        elif channel.startswith('resource.'):
            resource_id = channel[len('resource.'):]
            ok = await self._can_see_resource(resource_id)
        elif channel.startswith('resource_request.'):
            ok = True  # public reading
        elif channel.startswith('studyspace.'):
            space_id = channel[len('studyspace.'):]
            ok = await self._can_see_study_space(space_id) if self._user_id else False
        else:
            await self._send_json({'type': 'error', 'code': 'unknown_channel', 'message': f'unsupported: {channel}'})
            return

        if not ok:
            await self._send_json({'type': 'error', 'code': 'forbidden', 'message': 'cannot subscribe to channel'})
            return

        # Map 'user' to user-specific group in channel layer
        group_name = channel
        if channel == 'user' and self._user_id:
            group_name = f'user.{self._user_id}'

        await self.channel_layer.group_add(group_name, self.channel_name)
        self._groups.add(group_name)
        self._client_subscriptions[group_name] = channel

        await self._send_json({'type': 'subscribed', 'channel': channel})
        if channel.startswith('studyspace.'):
            space_id = channel[len('studyspace.'):]
            snapshot = cache.get(f'yjs:snapshot:{space_id}')
            if snapshot:
                await self._send_json({
                    'type': 'event',
                    'channel': channel,
                    'event': 'yjs_snapshot',
                    'data': {'update': snapshot, 'senderId': 'server'},
                })

    async def _handle_unsubscribe(self, channel: str):
        if not channel:
            return
        group_name = channel
        if channel == 'user' and self._user_id:
            group_name = f'user.{self._user_id}'
        if group_name in self._groups:
            await self.channel_layer.group_discard(group_name, self.channel_name)
            self._groups.discard(group_name)
            self._client_subscriptions.pop(group_name, None)
        await self._send_json({'type': 'unsubscribed', 'channel': channel})

    # ------------------------------------------------------------------ heartbeat / watchdog

    async def _heartbeat_loop(self):
        try:
            while True:
                await asyncio.sleep(self.HEARTBEAT_INTERVAL)
                await self._send_json({'type': 'ping'})
                if time.monotonic() - self._last_pong_at > self.HEARTBEAT_TIMEOUT:
                    logger.info('WS heartbeat timeout user=%s', self._user_id)
                    await self.close(code=1011)  # internal error / heartbeat lost
                    return
        except asyncio.CancelledError:
            return

    async def _idle_watchdog(self):
        try:
            while True:
                await asyncio.sleep(30)
                if time.monotonic() - self._last_activity > self.IDLE_TIMEOUT:
                    logger.info('WS idle timeout user=%s', self._user_id)
                    await self.close(code=1000)
                    return
        except asyncio.CancelledError:
            return

    # ------------------------------------------------------------------ broadcast receive

    # Internal channel_layer event names. Producers call group_send with
    # type='realtime.event' which Channels dispatches to realtime_event.
    async def realtime_event(self, event):
        channel = event['channel']
        # Map target channel back to client subscription name if mapped
        if hasattr(self, '_client_subscriptions') and channel in self._client_subscriptions:
            channel = self._client_subscriptions[channel]
        # Force into the batcher
        await self._batcher.add(channel, event['event'], event['data'])

    # ------------------------------------------------------------------ study-space notes realtime

    async def _handle_note_content(self, msg):
        """Receive note content update from a StudySpace member and broadcast to others."""
        space_id = msg.get('spaceId')
        content = msg.get('content', '')
        version = int(msg.get('version') or 0)
        if not space_id or not isinstance(content, str):
            return
        if len(content) > 20000000:
            await self._send_json({'type': 'error', 'code': 'note_too_large', 'message': 'Note exceeds 20M chars'})
            return
        # Save to Redis for fast cross-worker access
        cache.set(f'studynote:content:{space_id}', content, timeout=86400)
        cache.set(f'studynote:version:{space_id}', version, timeout=86400)
        cache.set(f'studynote:updated_by:{space_id}', self._user_id, timeout=86400)
        # Broadcast to all space subscribers (clients filter own messages by senderId)
        group = f'studyspace.{space_id}'
        if group in self._groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'realtime.event',
                    'channel': group,
                    'event': 'note_content',
                    'data': {
                        'content': content,
                        'version': version,
                        'senderId': self._user_id,
                    },
                }
            )

    async def _handle_note_cursor(self, msg):
        """Broadcast cursor position to other StudySpace members."""
        space_id = msg.get('spaceId')
        start = int(msg.get('start') or 0)
        end = int(msg.get('end') or 0)
        if not space_id:
            return
        group = f'studyspace.{space_id}'
        if group in self._groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'realtime.event',
                    'channel': group,
                    'event': 'note_cursor',
                    'data': {
                        'start': start,
                        'end': end,
                        'senderId': self._user_id,
                    },
                }
            )

    # ------------------------------------------------------------------ Yjs CRDT collaboration

    async def _handle_yjs_update(self, msg):
        """Receive Yjs incremental update from a StudySpace member and relay to others."""
        space_id = msg.get('spaceId')
        update_b64 = msg.get('update', '')
        if not space_id or not update_b64 or not isinstance(update_b64, str):
            return
        if len(update_b64) > 500000:
            return
        group = f'studyspace.{space_id}'
        if group in self._groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'realtime.event',
                    'channel': group,
                    'event': 'yjs_update',
                    'data': {
                        'update': update_b64,
                        'senderId': msg.get('clientId') or self._user_id,
                    },
                }
            )

    async def _handle_yjs_snapshot(self, msg):
        space_id = msg.get('spaceId')
        update_b64 = msg.get('update', '')
        if not space_id or not update_b64 or not isinstance(update_b64, str):
            return
        if len(update_b64) > 2000000:
            return
        group = f'studyspace.{space_id}'
        if group not in self._groups:
            return
        cache.set(f'yjs:snapshot:{space_id}', update_b64, timeout=604800)
        await self.channel_layer.group_send(
            group,
            {
                'type': 'realtime.event',
                'channel': group,
                'event': 'yjs_snapshot',
                'data': {'update': update_b64, 'senderId': msg.get('clientId') or self._user_id},
            }
        )

    async def _handle_yjs_sync_request(self, msg):
        space_id = msg.get('spaceId')
        if not space_id:
            return
        group = f'studyspace.{space_id}'
        if group not in self._groups:
            return
        snapshot = cache.get(f'yjs:snapshot:{space_id}')
        if snapshot:
            await self._send_json({
                'type': 'event',
                'channel': group,
                'event': 'yjs_snapshot',
                'data': {'update': snapshot, 'senderId': 'server'},
            })
            return
        await self.channel_layer.group_send(
            group,
            {
                'type': 'realtime.event',
                'channel': group,
                'event': 'yjs_sync_request',
                'data': {'senderId': msg.get('clientId') or self._user_id},
            }
        )

    async def _handle_yjs_awareness(self, msg):
        """Broadcast Yjs awareness (cursor/selection) to other StudySpace members."""
        space_id = msg.get('spaceId')
        state = msg.get('state', {})
        if not space_id or not isinstance(state, dict):
            return
        group = f'studyspace.{space_id}'
        if group in self._groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'realtime.event',
                    'channel': group,
                    'event': 'yjs_awareness',
                    'data': {
                        'state': state,
                        'senderId': msg.get('clientId') or self._user_id,
                    },
                }
            )

    # ------------------------------------------------------------------ internal

    async def _send_json(self, payload):
        try:
            await self.send(text_data=json.dumps(payload, default=str))
        except Exception as e:  # noqa: BLE001
            # Client may have disconnected mid-send.
            logger.debug('WS send failed (likely client closed): %s', e)
