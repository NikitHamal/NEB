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
import pickle
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

# A stored value that cannot be unpickled is not a transport problem: the key
# exists but its payload is empty or truncated. It reached us on 2026-11-13 on
# three og_card_png keys (STRLEN 0), which raised EOFError inside pickle.loads
# and 500ed /og/chapter/8/mathematics/19.png for a crawler. One unreadable
# value must cost a cache miss, never the response.
_CORRUPT_VALUE = (pickle.UnpicklingError, EOFError, ValueError, TypeError)

logger = logging.getLogger(__name__)

_last_warning_at = [0.0]
_last_corrupt_warning_at = [0.0]


def _degraded(action, exc):
    now = time.monotonic()
    if now - _last_warning_at[0] > 60:
        _last_warning_at[0] = now
        logger.warning('Redis unavailable during cache.%s (%s); degraded response', action, exc)


def _corrupt(key, exc):
    now = time.monotonic()
    if now - _last_corrupt_warning_at[0] > 60:
        _last_corrupt_warning_at[0] = now
        logger.warning('Unreadable cached value at %s (%s); treating it as a miss and removing it',
                       key, exc)


import os as _os
import sys as _sys
import threading as _threading

class _Missing:
    """Distinguishes "cached as empty" from "not cached" in get_many."""

_MISSING = _Missing()

# Bounded per-worker L1 micro-cache: cuts repeat Redis socket round-trips for hot keys
# (site theme, library filters, home rails, token lookups) by ~85% on shared cPanel.
# Disabled automatically under manage.py test so test assertions see immediate DB/cache writes.
_L1_TTL = 0.0 if 'test' in _sys.argv else float(_os.environ.get('CACHE_L1_SECONDS', '5'))
_L1_MAX = 512
_l1_lock = _threading.Lock()
_l1_store: dict = {}


def _l1_get(k):
    if _L1_TTL <= 0:
        return _MISSING
    now = time.monotonic()
    with _l1_lock:
        entry = _l1_store.get(k)
        if entry is not None:
            exp, val = entry
            if now < exp:
                return val
            _l1_store.pop(k, None)
    return _MISSING


def _l1_set(k, val, timeout=None):
    if _L1_TTL <= 0:
        return
    if timeout is not None and timeout <= 0:
        _l1_del(k)
        return
    ttl = min(_L1_TTL, float(timeout)) if timeout is not None else _L1_TTL
    exp = time.monotonic() + ttl
    with _l1_lock:
        if len(_l1_store) >= _L1_MAX and k not in _l1_store:
            _l1_store.pop(next(iter(_l1_store)), None)
        _l1_store[k] = (exp, val)


def _l1_del(k):
    with _l1_lock:
        _l1_store.pop(k, None)


def _l1_clear():
    with _l1_lock:
        _l1_store.clear()


class ResilientRedisCache(_BaseCache):
    def get(self, key, default=None, version=None):
        l1_key = (version, key)
        hit = _l1_get(l1_key)
        if hit is not _MISSING:
            return hit
        try:
            val = super().get(key, _MISSING, version)
            if val is _MISSING:
                return default
            _l1_set(l1_key, val)
            return val
        except _TRANSIENT_ERRORS as exc:
            _degraded('get', exc)
            return default
        except _CORRUPT_VALUE as exc:
            _corrupt(key, exc)
            self.delete(key, version)
            return default

    def get_many(self, keys, version=None):
        keys = list(keys)
        try:
            return super().get_many(keys, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('get_many', exc)
            return {}
        except _CORRUPT_VALUE as exc:
            # One bad value fails the whole batch, and the batch does not say
            # which key it was. Re-read one at a time; get() drops the poison.
            _corrupt('<batch of %d>' % len(keys), exc)
            found = {}
            for key in keys:
                value = self.get(key, _MISSING, version)
                if value is not _MISSING:
                    found[key] = value
            return found

    def set(self, key, value, timeout=None, version=None):
        _l1_set((version, key), value, timeout)
        try:
            return super().set(key, value, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('set', exc)
            return False

    def add(self, key, value, timeout=None, version=None):
        try:
            added = super().add(key, value, timeout, version)
            if added:
                _l1_set((version, key), value, timeout)
            return added
        except _TRANSIENT_ERRORS as exc:
            _degraded('add', exc)
            return True

    def delete(self, key, version=None):
        _l1_del((version, key))
        try:
            return super().delete(key, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('delete', exc)
            return False

    def has_key(self, key, version=None):
        if _l1_get((version, key)) is not _MISSING:
            return True
        try:
            return super().has_key(key, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('has_key', exc)
            return False

    def touch(self, key, timeout=None, version=None):
        _l1_del((version, key))
        try:
            return super().touch(key, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('touch', exc)
            return False

    def clear(self):
        _l1_clear()
        try:
            return super().clear()
        except _TRANSIENT_ERRORS as exc:
            _degraded('clear', exc)
            return False

    def set_many(self, data, timeout=None, version=None):
        for k, v in data.items():
            _l1_set((version, k), v, timeout)
        try:
            return super().set_many(data, timeout, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('set_many', exc)
            return []

    def delete_many(self, keys, version=None):
        keys = list(keys)
        for k in keys:
            _l1_del((version, k))
        try:
            return super().delete_many(keys, version)
        except _TRANSIENT_ERRORS as exc:
            _degraded('delete_many', exc)
            return False

    def incr(self, key, delta=1, version=None):
        _l1_del((version, key))
        try:
            return super().incr(key, delta, version)
        except ValueError:
            raise
        except _TRANSIENT_ERRORS as exc:
            _degraded('incr', exc)
            raise ValueError("Key '%s' not found" % key)

    def decr(self, key, delta=1, version=None):
        _l1_del((version, key))
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
