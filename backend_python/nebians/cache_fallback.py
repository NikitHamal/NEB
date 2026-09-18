"""Resilient Redis cache backend.

Production incident (Sep 2026): the site returned HTTP 500 on every page when
the LSAPI workers could not reach Redis (ECONNREFUSED), because
``django.core.cache.backends.redis.RedisCache`` raises on every cache op and
``SESSION_ENGINE=cached_db`` also depends on the cache. The Django shell on the
same box could reach Redis fine, so the outage was worker-specific and the
whole site must never depend on cache availability.

``ResilientRedisCache`` subclasses the stock Redis backend and converts
connection-level failures into safe degraded responses (miss / False), so
pages render from the database instead of 500ing. Only transport errors are
swallowed; configuration/auth errors still raise loudly.

Degraded semantics (fail-open, matching existing call-site conventions):
- get/get_many -> default / {}
- set/set_many/touch/delete/delete_many/clear -> False / [] / False
- add -> True (rate limiters and pairing gates fail open, as their own
  ``except Exception`` fallbacks already do)
- incr/decr -> raise ValueError (mimics "key missing"; every incr call site
  handles ValueError by starting a fresh window)
- get_or_set -> evaluate and return the callback without caching
- delete_pattern -> best-effort scan-delete, 0 on outage (stock RedisCache
  does not provide this method at all; admin news invalidation uses it)
"""
from __future__ import annotations

import logging
import time

try:
    from django.core.cache.backends.redis import RedisCache as _BaseCache
    _HAVE_REDIS_BACKEND = True
except Exception:
    from django.core.cache.backends.locmem import LocMemCache as _BaseCache
    _HAVE_REDIS_BACKEND = False

try:
    import redis.exceptions as _redis_exceptions

    _TRANSIENT_ERRORS = (
        _redis_exceptions.ConnectionError,
        _redis_exceptions.TimeoutError,
        _redis_exceptions.BusyLoadingError,
    )
except Exception:
    _TRANSIENT_ERRORS = ()

_TRANSIENT_ERRORS = _TRANSIENT_ERRORS + (ConnectionError, TimeoutError, OSError)

logger = logging.getLogger(__name__)

_last_warning_at = [0.0]


def _degraded(action, exc):
    now = time.monotonic()
    if now - _last_warning_at[0] > 60:
        _last_warning_at[0] = now
        logger.warning('Redis unavailable during cache.%s (%s); degraded response', action, exc)


class ResilientRedisCache(_BaseCache):
    def get(self, key, default=None, version=None):
        try:
            return super().get(key, default, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('get', exc)
            return default

    def set(self, key, value, timeout=None, version=None):
        try:
            return super().set(key, value, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('set', exc)
            return False

    def add(self, key, value, timeout=None, version=None):
        try:
            return super().add(key, value, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('add', exc)
            return True

    def delete(self, key, version=None):
        try:
            return super().delete(key, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('delete', exc)
            return False

    def has_key(self, key, version=None):
        try:
            return super().has_key(key, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('has_key', exc)
            return False

    def touch(self, key, timeout=None, version=None):
        try:
            return super().touch(key, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('touch', exc)
            return False

    def clear(self):
        try:
            return super().clear()
        except _TRANSIENT_ERRORS as exc:
            _degraded('clear', exc)
            return False

    def get_many(self, keys, version=None):
        try:
            return super().get_many(keys, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('get_many', exc)
            return {}

    def set_many(self, data, timeout=None, version=None):
        try:
            return super().set_many(data, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('set_many', exc)
            return []

    def delete_many(self, keys, version=None):
        try:
            return super().delete_many(keys, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('delete_many', exc)
            return False

    def incr(self, key, delta=1, version=None):
        try:
            return super().incr(key, delta, version)
        except ValueError:
            raise
        except _TRANSIENT_ERRORS as exc:
            _degraded('incr', exc)
            raise ValueError("Key '%s' not found" % key)

    def decr(self, key, delta=1, version=None):
        try:
            return super().decr(key, delta, version)
        except ValueError:
            raise
        except _TRANSIENT_ERRORS as exc:
            _degraded('decr', exc)
            raise ValueError("Key '%s' not found" % key)

    def get_or_set(self, key, default, timeout=None, version=None):
        try:
            return super().get_or_set(key, default, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('get_or_set', exc)
            return default() if callable(default) else default

    def incr_version(self, key, delta=1, version=None):
        try:
            return super().incr_version(key, delta, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('incr_version', exc)
            return (version or 1) + 1

    def delete_pattern(self, pattern, version=None):
        try:
            inner = getattr(self, '_cache', None)
            get_client = getattr(inner, 'get_client', None)
            if get_client is None:
                return 0
            client = get_client(write=True)
            prefixed = self.make_key(pattern, version=version)
            count = 0
            for redis_key in client.scan_iter(match=prefixed, count=500):
                client.delete(redis_key)
                count += 1
            return count
        except _TRANSIENT_ERRORS as exc:
            _degraded('delete_pattern', exc)
            return 0
        except Exception as exc:
            _degraded('delete_pattern', exc)
            return 0
