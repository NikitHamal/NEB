"""
Neby Code realtime bridge.

Sync helpers used by web views and the code agent worker to talk to the
user's locally running neby_code daemon through the Channels channel
layer (daphne relays to the daemon's WebSocket) and to receive results
through a Redis request/response mailbox.
"""
import json
import logging
import threading
import time
import uuid

from django.conf import settings

logger = logging.getLogger(__name__)

_LAYER = None
_LAYER_LOCK = threading.Lock()
_REDIS = None
_REDIS_LOCK = threading.Lock()

RESULT_TTL = 600


def _layer():
    from channels.layers import get_channel_layer
    return get_channel_layer()


def _redis():
    global _REDIS
    if _REDIS is None:
        with _REDIS_LOCK:
            if _REDIS is None:
                import os
                import redis as redis_lib
                url = (
                    getattr(settings, 'CACHE_LOCATION', '')
                    or getattr(settings, 'REDIS_URL', '')
                    or os.environ.get('CACHE_LOCATION', '')
                    or os.environ.get('REDIS_URL', '')
                    or ''
                ).strip()
                if url:
                    if not url.startswith(('redis://', 'rediss://', 'unix://')):
                        url = 'redis://' + url
                    _REDIS = redis_lib.Redis.from_url(url, socket_connect_timeout=3, socket_timeout=5)
                else:
                    _REDIS = redis_lib.Redis(
                        host='127.0.0.1', port=6379, db=0,
                        socket_connect_timeout=3, socket_timeout=5,
                    )
    return _REDIS


def daemon_group(user_id: str) -> str:
    return f'code.daemon.{user_id}'


def ui_group(session_id: str) -> str:
    return f'code.ui.{session_id}'


def dispatch_to_daemon(user_id: str, payload: dict, timeout: float = 6.0) -> bool:
    from asgiref.sync import async_to_sync
    try:
        payload = dict(payload or {})
        layer = _layer()
        if layer is None:
            logger.warning('code dispatch failed: no channel layer configured')
            return False
        async_to_sync(layer.group_send)(daemon_group(user_id), {
            'type': 'code.event',
            'payload': payload,
        })
        return True
    except Exception as e:  # noqa: BLE001
        logger.warning('code dispatch failed user=%s: %s', user_id, e)
        return False


def push_ui(session_id: str, event: str, data: dict):
    """Broadcast a frame to every browser subscribed to code.ui.<id>."""
    from asgiref.sync import async_to_sync
    try:
        async_to_sync(_layer().group_send)(ui_group(session_id), {
            'type': 'realtime.event',
            'channel': ui_group(session_id),
            'event': event,
            'data': data,
        })
    except Exception as e:  # noqa: BLE001
        logger.debug('code ui push failed session=%s: %s', session_id, e)


def call_daemon(user_id: str, action: str, args: dict = None,
                timeout: float = 12.0, session_id: str = '') -> dict:
    """Round-trip a single action to the daemon; returns the result dict.

    Result shape: {'ok': bool, 'data': ..., 'error': str}
    """
    call_id = uuid.uuid4().hex
    key = f'code:res:{call_id}'
    try:
        r = _redis()
        r.delete(key)
    except Exception as e:  # noqa: BLE001
        logger.warning('redis unavailable for call_daemon: %s', e)
        return {'ok': False, 'error': 'daemon_offline'}

    sent = dispatch_to_daemon(user_id, {
        'action': action,
        'call_id': call_id,
        'session_id': session_id,
        'args': args or {},
    }, timeout=timeout)
    if not sent:
        return {'ok': False, 'error': 'dispatch_failed'}
    deadline = time.monotonic() + timeout
    cancel_sent = False
    try:
        while time.monotonic() < deadline:
            item = r.blpop(key, timeout=min(1.0, max(0.1, deadline - time.monotonic())))
            if item:
                try:
                    return json.loads(item[1])
                except Exception:  # noqa: BLE001
                    break
            if action == 'term.run' and session_id and not cancel_sent:
                try:
                    from api.models import CodeSession
                    is_cancelled = bool(
                        CodeSession.objects.filter(pk=session_id, cancel_flag=True).values_list('cancel_flag', flat=True).first()
                    )
                except Exception:  # noqa: BLE001
                    is_cancelled = False
                if is_cancelled:
                    cancel_sent = True
                    dispatch_to_daemon(user_id, {
                        'action': 'term.cancel',
                        'call_id': uuid.uuid4().hex,
                        'session_id': session_id,
                        'args': {'call_id': call_id},
                    })
                    return {'ok': False, 'error': 'cancelled'}
    except Exception as e:  # noqa: BLE001
        logger.warning('redis blpop error: %s', e)
    return {'ok': False, 'error': 'daemon_timeout'}


def store_result(call_id: str, payload: dict):
    """Called by the WS consumer when the daemon answers a call."""
    try:
        _redis().lpush(f'code:res:{call_id}', json.dumps(payload, default=str))
        _redis().expire(f'code:res:{call_id}', RESULT_TTL)
    except Exception as e:  # noqa: BLE001
        logger.warning('code result store failed call=%s: %s', call_id, e)


def set_presence(user_id: str, info: dict):
    try:
        _redis().set(f'code:daemon:{user_id}', json.dumps(info, default=str), ex=75)
    except Exception:  # noqa: BLE001
        pass


def clear_presence(user_id: str, channel_name: str = ''):
    try:
        cur = get_presence(user_id)
        if cur and channel_name and cur.get('_ch') != channel_name:
            return
        _redis().delete(f'code:daemon:{user_id}')
    except Exception:  # noqa: BLE001
        pass


def get_presence(user_id: str):
    try:
        raw = _redis().get(f'code:daemon:{user_id}')
        return json.loads(raw) if raw else None
    except Exception:  # noqa: BLE001
        return None


def now_ms() -> int:
    return int(time.time() * 1000)
