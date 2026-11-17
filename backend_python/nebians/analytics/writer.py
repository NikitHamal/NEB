"""Off-request-path writer for page views.

The request thread does one non-blocking thing, `submit()`, and returns. A
single daemon worker per process drains a bounded queue, assigns the visit to a
session and writes the row. Analytics is best-effort by definition: the queue
drops on overflow, so a stalled database costs page views, never latency or
memory.

Sessions
--------
A session is a run of hits from one visitor with no gap longer than 30 minutes.
The "current session" lives in the shared cache (Redis in production) under the
visitor id. A cache miss starts a new session and marks that row `is_entry`, so
sessions, landing pages and acquisition sources are all just `is_entry=True`
rows. If the cache is unavailable the session id degrades to a deterministic
30-minute bucket instead of exploding into one session per hit.

Geography
---------
Country comes from edge headers (see events.py). Looking an IP up on a third
party sends every visitor's address to that third party, so the remote lookup
below is OFF unless `ANALYTICS_GEO_REMOTE=1`.
"""
from __future__ import annotations

import hashlib
import logging
import os
import queue
import secrets
import sys
import threading
import time

from django.conf import settings
from django.core.cache import cache
from django.db import connections

from .rules import SESSION_GAP_MS

logger = logging.getLogger(__name__)

_IN_TESTS = 'test' in sys.argv
_FORCE_SUBMIT_IN_TESTS = False
_MAX_PENDING = 512
_queue: "queue.Queue[dict]" = queue.Queue(maxsize=_MAX_PENDING)
_worker: threading.Thread | None = None
_worker_lock = threading.Lock()
# Fork safety. LiteSpeed's LSAPI (and gunicorn --preload, uWSGI) fork request
# processes from a parent that may already have called submit(). A forked child
# inherits the Thread *object* (is_alive() can still say True) but not the OS
# thread, and the inherited queue's lock may be held by a thread that no longer
# exists. So remember which pid built the worker and rebuild everything when the
# pid changes.
_owner_pid = os.getpid()

# ip-api.com free tier answers 45/minute per calling IP and bans for an hour
# after that. Stay under it on purpose.
_GEO_BUDGET_PER_MIN = 40
_geo_window_start = 0.0
_geo_window_count = 0


def assign_session(visitor_id: str, now_ms: int) -> tuple[str, bool]:
    """Return (session_id, is_entry) for a hit by `visitor_id` at `now_ms`."""
    key = f'an:sess:{visitor_id}'
    try:
        cur = cache.get(key)
        if cur:
            sid, _, last = cur.partition('|')
            if sid and last.isdigit() and 0 <= now_ms - int(last) <= SESSION_GAP_MS:
                cache.set(key, f'{sid}|{now_ms}', SESSION_GAP_MS // 1000 + 60)
                return sid, False
        sid = secrets.token_hex(8)
        cache.set(key, f'{sid}|{now_ms}', SESSION_GAP_MS // 1000 + 60)
        return sid, True
    except Exception:
        bucket = now_ms // SESSION_GAP_MS
        sid = hashlib.sha256(f'{visitor_id}|{bucket}'.encode()).hexdigest()[:16]
        return sid, False


def _geo_budget_available() -> bool:
    global _geo_window_start, _geo_window_count
    now = time.time()
    if now - _geo_window_start >= 60:
        _geo_window_start = now
        _geo_window_count = 0
    if _geo_window_count >= _GEO_BUDGET_PER_MIN:
        return False
    _geo_window_count += 1
    return True


def _geo_remote(ip: str) -> tuple[str, str]:
    """Opt-in: country/city from ip-api.com. Misses are cached too."""
    if not ip or ip in ('127.0.0.1', '::1', '0.0.0.0'):
        return '', ''
    cached = cache.get(f'geo:{ip}')
    if cached:
        country, _, city = cached.partition('|')
        return country, city
    if not _geo_budget_available():
        return '', ''
    country, city = '', ''
    try:
        import json
        import urllib.request

        req = urllib.request.Request(
            f'http://ip-api.com/json/{ip}?fields=status,country,city',
            headers={'User-Agent': 'NEBians/1.0'},
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
        if data.get('status') == 'success':
            country = data.get('country') or ''
            city = data.get('city') or ''
    except Exception:
        pass
    try:
        cache.set(f'geo:{ip}', f'{country}|{city}', 2592000 if country else 21600)
    except Exception:
        pass
    return country, city


def _should_touch_user(uid: str) -> bool:
    if _IN_TESTS:
        return True
    key = f'an:touch:{uid}'
    try:
        if cache.get(key):
            return False
        cache.set(key, 1, 60)
    except Exception:
        pass
    return True


def _write(item: dict) -> None:
    from django.db import close_old_connections

    from api.models import PageView, User as UserModel

    close_old_connections()
    try:
        touch = item.pop('_touch_user', '')
        ip = item.pop('_ip', '')
        if touch and _should_touch_user(touch):
            try:
                UserModel.objects.filter(pk=touch).update(last_active=item['created_at'])
            except Exception:
                pass
        if not item.get('country') and ip and getattr(settings, 'ANALYTICS_GEO_REMOTE', False):
            item['country'], item['city'] = _geo_remote(ip)
        item['session_id'], item['is_entry'] = assign_session(item['visitor_id'], item['created_at'])
        PageView.objects.create(**item)
    finally:
        close_old_connections()


def _run(q: "queue.Queue[dict]") -> None:
    while True:
        item = q.get()
        try:
            _write(item)
        except Exception:
            logger.debug('page view write failed', exc_info=True)
        finally:
            q.task_done()
            if q.empty() and not _IN_TESTS:
                try:
                    connections.close_all()
                except Exception:
                    pass


def _ensure_worker() -> None:
    global _worker, _queue, _worker_lock, _owner_pid
    pid = os.getpid()
    if pid != _owner_pid:
        # We are a forked child: nothing inherited from the parent works here.
        _worker_lock = threading.Lock()
        _queue = queue.Queue(maxsize=_MAX_PENDING)
        _worker = None
        _owner_pid = pid
    if _worker is not None and _worker.is_alive():
        return
    with _worker_lock:
        if _worker is not None and _worker.is_alive():
            return
        # The thread targets the queue it was created for, so a rebuilt queue
        # can never be drained by a stale worker.
        _worker = threading.Thread(
            target=_run, args=(_queue,), name='nebians-pageviews', daemon=True,
        )
        _worker.start()


def submit(item: dict) -> None:
    """Hand a row to the worker. Never blocks, never raises."""
    if _IN_TESTS and not _FORCE_SUBMIT_IN_TESTS:
        return
    try:
        _ensure_worker()
        _queue.put_nowait(item)
    except queue.Full:
        logger.debug('page view queue full; dropping')
    except Exception:
        logger.debug('page view submit failed', exc_info=True)
