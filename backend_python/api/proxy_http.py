"""Resilient HTTP sessions for keyless chat proxies.

Context (Oct 2026): on an overloaded shared box a worker process can be
unable to spawn new threads. curl_cffi resolves DNS on a helper thread, so
its requests then fail with errors like ``getaddrinfo() thread failed to
start`` while plain ``requests`` (blocking getaddrinfo in the calling
thread) still goes through.

``new_session()`` prefers curl_cffi Chrome impersonation (needed to pass
WAFs and bot checks) and ``resilient_request()`` re-issues the call once
through a plain ``requests`` session when the curl-backed call raises a
transport error. Both libraries expose ``.status_code`` / ``.text`` /
``.content`` / ``.json()`` / ``iter_content()`` on responses, so call sites
switch transparently. The retry fires only on exceptions, never on HTTP
error statuses, so behavior is unchanged when the box is healthy.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
)


def new_session(impersonate: str = "chrome", headers: Optional[Dict[str, str]] = None,
                force_requests: bool = False, **kw) -> Any:
    """Build a session, preferring curl_cffi impersonation.

    Falls back to plain requests when curl_cffi is missing OR its session
    cannot even be constructed (also a thread-starvation symptom).
    The returned session carries ``_neb_plain`` (True when requests-backed).
    Extra kwargs (e.g. ``timeout``) are passed to curl_cffi only; plain
    requests takes per-request timeouts instead.
    """
    if not force_requests:
        try:
            from curl_cffi.requests import Session as CurlSession  # type: ignore

            s = CurlSession(impersonate=impersonate, **kw)
            if headers:
                s.headers.update(headers)
            s._neb_plain = False  # type: ignore[attr-defined]
            return s
        except Exception as exc:
            logger.debug("proxy_http: curl session unavailable (%s); using requests", exc)
    import requests

    s = requests.Session()
    s.headers.update({"User-Agent": CHROME_UA})
    if headers:
        s.headers.update(headers)
    s._neb_plain = True  # type: ignore[attr-defined]
    return s


def _plain_copy(src):
    """Fresh requests session carrying the old session's headers + cookies."""
    import requests

    dst = requests.Session()
    try:
        dst.headers.update(dict(src.headers))
    except Exception:
        dst.headers.update({"User-Agent": CHROME_UA})
    try:
        dst.cookies.update(src.cookies)
    except Exception:
        pass
    try:
        proxies = getattr(src, "proxies", None)
        if proxies:
            dst.proxies.update(dict(proxies))
    except Exception:
        pass
    dst._neb_plain = True  # type: ignore[attr-defined]
    return dst


def is_plain(session) -> bool:
    return bool(getattr(session, "_neb_plain", False))


def resilient_request(session, method: str, url: str, **kwargs) -> Tuple[Any, Any]:
    """Issue one request, retrying once via plain requests on transport error.

    Returns ``(response, session_to_use)`` — callers must keep using the
    returned session, since the fallback swaps the underlying object.
    Raises the last exception when both attempts fail.

    A ``proxy=<url>`` kwarg (curl_cffi style) is translated to
    ``session.proxies`` for the plain-requests path.
    """
    method = method.lower()
    proxy = kwargs.pop("proxy", None)
    if proxy and is_plain(session):
        try:
            session.proxies.update({"http": proxy, "https": proxy})
        except Exception:
            pass
    try:
        if proxy and not is_plain(session):
            resp = getattr(session, method)(url, proxy=proxy, **kwargs)
        else:
            resp = getattr(session, method)(url, **kwargs)
        return resp, session
    except Exception as exc:
        if is_plain(session):
            raise
        logger.debug("proxy_http: curl %s %s failed (%s); retrying via requests",
                     method.upper(), url, exc)
        plain = _plain_copy(session)
        if proxy:
            try:
                plain.proxies.update({"http": proxy, "https": proxy})
            except Exception:
                pass
        resp = getattr(plain, method)(url, **kwargs)
        return resp, plain


def resilient_get(session, url: str, **kwargs) -> Tuple[Any, Any]:
    return resilient_request(session, "get", url, **kwargs)


def resilient_post(session, url: str, **kwargs) -> Tuple[Any, Any]:
    return resilient_request(session, "post", url, **kwargs)
