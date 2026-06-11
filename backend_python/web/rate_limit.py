"""Lightweight cache-backed rate limiting for plain Django (non-DRF) web views.

DRF throttles only apply to /api/ endpoints. The web AJAX endpoints under
web/urls.py previously had no rate limiting at all, which left expensive
operations (AI generation, uploads, reports, searches) open to abuse.

Usage:
    from web.rate_limit import web_rate_limit

    @require_POST
    @web_rate_limit('ai-generate', limit=8, window=600)
    def ajax_space_generate_summary(request, space_id):
        ...

The decorator identifies the caller by authenticated user id when available
(via web.view_helpers._get_user_id), falling back to the client IP address.
It uses an atomic cache incr() when the backend supports it (Redis does),
falling back to a read-modify-write for LocMemCache in local dev.

On limit breach it returns HTTP 429 with a JSON body:
    {"success": false, "error": "Too many requests. Please try again shortly."}
"""
from __future__ import annotations

import functools
import time

from django.core.cache import cache
from django.http import JsonResponse


def _client_ip(request) -> str:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def _rate_key(scope: str, request) -> str:
    # Imported lazily to avoid a circular import (view_helpers imports models).
    from web.view_helpers import _get_user_id

    user_id = None
    try:
        user_id = _get_user_id(request)
    except Exception:  # noqa: BLE001 - never let identity lookup break limiting
        user_id = None
    ident = f'u:{user_id}' if user_id else f'ip:{_client_ip(request)}'
    # Bucket by window start so keys expire naturally.
    return f'wrl:{scope}:{ident}'


def _hit(key: str, window: int) -> int:
    """Increment and return the current request count for this key/window."""
    try:
        added = cache.add(key, 1, timeout=window)
        if added:
            return 1
        return cache.incr(key)
    except ValueError:
        # Key expired between add() and incr(); start a fresh window.
        cache.set(key, 1, timeout=window)
        return 1
    except Exception:  # noqa: BLE001 - cache backend hiccup: fail open
        return 1


def web_rate_limit(scope: str, limit: int, window: int = 60, method: str | None = 'POST'):
    """Rate-limit a Django view.

    Args:
        scope: short identifier shared by views that should count together.
        limit: max number of requests allowed per window.
        window: window size in seconds.
        method: only count requests of this HTTP method (None = all methods).
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if method is None or request.method == method:
                key = _rate_key(scope, request)
                count = _hit(key, window)
                if count > limit:
                    retry_after = max(1, window // 4)
                    resp = JsonResponse(
                        {'success': False,
                         'error': 'Too many requests. Please try again shortly.'},
                        status=429,
                    )
                    resp['Retry-After'] = str(retry_after)
                    return resp
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


__all__ = ['web_rate_limit']
