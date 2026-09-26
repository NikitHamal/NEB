"""Page-view analytics, moved off the request path.

Every GET used to end with a synchronous `PageView.objects.create()` and, on a
cold IP, a blocking `urlopen` to ip-api.com with a three second timeout. Both
sat between the view returning and the browser getting its first byte, so the
page was as slow as whichever of the two was having a worse day.

ip-api.com's free tier allows 45 lookups a minute per calling IP and then
answers 429 for the rest of the hour. The old code only cached a *successful*
lookup, so once the site crossed that rate every subsequent visitor paid the
round trip again and got nothing for it -- a slowdown that gets worse exactly
as traffic gets better, which is what it looked like from the outside.

So: the request thread does one non-blocking thing, `submit()`, and returns. A
single daemon worker per process drains the queue, resolves geo (caching
failures too, so a throttled upstream is asked once per window rather than once
per visitor) and writes the row.

Analytics is best-effort by definition. The queue is bounded and drops on
overflow: a stalled database costs page views, never latency or memory.
"""
from __future__ import annotations

import logging
import queue
import threading
import time

from django.core.cache import cache

logger = logging.getLogger(__name__)

# One HTTP round trip and one INSERT per item; a few hundred is minutes of
# burst traffic at any volume this site sees, and bounded memory if the
# database goes away.
_MAX_PENDING = 512

_queue: "queue.Queue[dict]" = queue.Queue(maxsize=_MAX_PENDING)
_worker: threading.Thread | None = None
_worker_lock = threading.Lock()

# ip-api.com answers 45/minute per calling IP. Stay under it on purpose: a 429
# would otherwise get us banned for the hour and take every lookup with it.
_GEO_BUDGET_PER_MIN = 40
_geo_window_start = 0.0
_geo_window_count = 0


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


def geo_cached(ip_address: str):
    """Whatever we already know about this IP, without touching the network."""
    if not ip_address or ip_address in ('127.0.0.1', '::1', '0.0.0.0'):
        return '', ''
    cached = cache.get(f'geo:{ip_address}')
    if not cached:
        return None
    country, _, city = cached.partition('|')
    return country, city


def _geo_resolve(ip_address: str):
    """Look the IP up for real. Only ever called on the worker thread."""
    known = geo_cached(ip_address)
    if known is not None:
        return known
    if not _geo_budget_available():
        return '', ''
    country, city = '', ''
    try:
        import json
        import urllib.request

        req = urllib.request.Request(
            f'http://ip-api.com/json/{ip_address}?fields=country,city',
            headers={'User-Agent': 'NEBians/1.0'},
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
        if data.get('status') == 'success':
            country = data.get('country') or ''
            city = data.get('city') or ''
    except Exception:
        pass
    # Cache the miss as well, and for long enough to matter. An IP that the
    # upstream cannot or will not resolve must not be retried per page view.
    ttl = 2592000 if country or city else 21600
    try:
        cache.set(f'geo:{ip_address}', f'{country}|{city}', ttl)
    except Exception:
        pass
    return country, city


def _write(item: dict) -> None:
    from django.db import close_old_connections

    from api.models import PageView, User as UserModel

    close_old_connections()
    try:
        uid = item.pop('_touch_user', '')
        if uid:
            try:
                UserModel.objects.filter(pk=uid).update(last_active=item['created_at'])
            except Exception:
                pass
        ip = item.get('ip_address')
        if ip:
            item['country'], item['city'] = _geo_resolve(ip)
        PageView.objects.create(**item)
    finally:
        close_old_connections()


def _run() -> None:
    while True:
        item = _queue.get()
        try:
            _write(item)
        except Exception:
            logger.debug('page view write failed', exc_info=True)
        finally:
            _queue.task_done()


def _ensure_worker() -> None:
    global _worker
    if _worker is not None and _worker.is_alive():
        return
    with _worker_lock:
        if _worker is not None and _worker.is_alive():
            return
        _worker = threading.Thread(
            target=_run, name='nebians-pageviews', daemon=True
        )
        _worker.start()


def submit(item: dict) -> None:
    """Hand a row to the worker. Never blocks, never raises."""
    try:
        _ensure_worker()
        _queue.put_nowait(item)
    except queue.Full:
        logger.debug('page view queue full; dropping')
    except Exception:
        logger.debug('page view submit failed', exc_info=True)
