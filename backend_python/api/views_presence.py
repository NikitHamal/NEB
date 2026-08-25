"""Views Presence — heartbeat and online user tracking."""
from django.core.cache import cache
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .view_helpers import _require_user
from .throttles import WriteActionRateThrottle

import os as _os, redis as _redis


def _get_presence_redis():
    """Return raw Redis client for presence set ops (sadd/smembers etc).

    Uses the same connection URL as the Django cache backend but opens a
    separate connection so we can call Redis set commands not exposed by
    Django's RedisCache wrapper.
    """
    loc = _os.environ.get('CACHE_LOCATION', '')
    if loc:
        return _redis.from_url(loc)
    return _redis.Redis(host='127.0.0.1', port=6379, db=0)


_REDIS = _get_presence_redis()


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([WriteActionRateThrottle])
def presence_heartbeat(request):
    """
    POST /api/presence/heartbeat/

    Mobile app presence heartbeat. Updates last_active and Redis presence.
    Body (optional): { "screen": "home" }
    """
    import time
    user, err = _require_user(request)
    if err:
        return err
    if hasattr(user, 'is_locked') and user.is_locked:
        return Response({'status': 'ignored'})

    try:
        now_ms = int(time.time() * 1000)
        uid = str(user.id)

        from api.models import User
        User.objects.filter(pk=uid).update(last_active=now_ms)

        try:
            _REDIS.sadd('presence:online', uid)
            _REDIS.expire('presence:online', 300)
        except Exception:
            pass

        try:
            cache.set(f'presence:user:{uid}', now_ms, 300)
            cache.set(f'presence:user:{uid}:screen', request.data.get('screen', ''), 300)
        except Exception:
            pass

        return Response({'status': 'ok', 'server_time': now_ms})
    except Exception:
        return Response({'status': 'error'}, status=500)


def get_online_users():
    """Return list of currently online user IDs and count."""
    try:
        members = list(_REDIS.smembers('presence:online') or [])
        now_ms = int(__import__('time').time() * 1000)
        active = []
        for uid in members:
            uid = uid.decode() if isinstance(uid, bytes) else uid
            ts = cache.get(f'presence:user:{uid}')
            if ts and (now_ms - ts) < 300000:
                screen = cache.get(f'presence:user:{uid}:screen', '') or ''
                active.append({'user_id': uid, 'screen': screen})
            else:
                _REDIS.srem('presence:online', uid)
        return active, len(active)
    except Exception:
        return [], 0
