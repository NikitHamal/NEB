"""Turn a Django request into a page-view event, or decide it is not one.

Used by the tracking middleware (web pages) and by `/api/analytics/track/`
(screens inside the mobile app) so both write identical, comparable rows.
"""
from __future__ import annotations

import time

from django.conf import settings

from . import rules

# Not pages: assets, API, fragments, link-preview art, the admin console.
SKIP_PREFIXES = (
    '/static/', '/media/', '/ajax/', '/api/', '/admin/', '/og/', '/.well-known/',
    '/manifest.json', '/robots.txt', '/sitemap', '/favicon.ico', '/sw.js', '/health',
)

_APP_HEADERS = ('HTTP_X_APP_PLATFORM', 'HTTP_X_APP_VERSION')
_PREFETCH_HEADERS = ('HTTP_SEC_PURPOSE', 'HTTP_PURPOSE', 'HTTP_X_PURPOSE', 'HTTP_X_MOZ')


def own_hosts(request) -> set[str]:
    hosts = {request.get_host().split(':')[0].lower()}
    for h in getattr(settings, 'ALLOWED_HOSTS', []) or []:
        h = (h or '').lstrip('.').lower()
        if h and '*' not in h and h not in ('localhost', '127.0.0.1', '[::1]'):
            hosts.add(h)
    for h in getattr(settings, 'ANALYTICS_OWN_HOSTS', []) or []:
        hosts.add(h.lower())
    return hosts


def client_ip(request) -> str:
    meta = request.META
    return (
        meta.get('HTTP_CF_CONNECTING_IP')
        or (meta.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip())
        or meta.get('REMOTE_ADDR', '')
        or ''
    )


def _geo_from_headers(meta) -> tuple[str, str]:
    code = (
        meta.get('HTTP_CF_IPCOUNTRY')
        or meta.get('HTTP_CLOUDFRONT_VIEWER_COUNTRY')
        or meta.get('HTTP_X_COUNTRY_CODE')
        or meta.get('HTTP_X_VERCEL_IP_COUNTRY')
        or ''
    )
    city = meta.get('HTTP_CF_IPCITY') or meta.get('HTTP_X_VERCEL_IP_CITY') or ''
    return rules.country_from_code(code), city[:100]


def _resolve_user(request):
    """The signed-in api.User, if any.

    The site signs people in by putting an auth token in the session, not via
    django.contrib.auth, so `request.user` is always anonymous. (The previous
    tracker trusted request.user, which is why it never recorded a single
    member.) Views usually resolved the user already; that result is reused.
    """
    cached = getattr(request, '_nebians_platform_user', None)
    if cached is not None:
        return cached
    try:
        from web.view_helpers import _get_platform_user

        return _get_platform_user(request)
    except Exception:
        return None


def is_trackable_request(request, response) -> bool:
    """The middleware's gate: a successful, full-page HTML GET by a human."""
    if request.method != 'GET' or response.status_code != 200:
        return False
    path = request.path.lower()
    if path.startswith(SKIP_PREFIXES):
        return False
    if not (response.get('Content-Type', '') or '').lower().startswith('text/html'):
        return False
    meta = request.META
    # HTMX fragments are parts of a page, not page views (boosted navigation is).
    if meta.get('HTTP_HX_REQUEST') and not meta.get('HTTP_HX_BOOSTED'):
        return False
    for h in _PREFETCH_HEADERS:
        if 'prefetch' in (meta.get(h, '') or '').lower():
            return False
    return True


def event_from_request(request, *, path: str | None = None, referrer: str | None = None,
                       utm: dict | None = None, force_app: bool = False,
                       app_platform: str = '', user=None) -> dict | None:
    """Build the event dict for `writer.submit`, or None to drop the hit.

    None means: a bot, or the site's own staff browsing their own site.
    """
    meta = request.META
    ua = meta.get('HTTP_USER_AGENT', '') or ''

    is_app = force_app or any(meta.get(h) for h in _APP_HEADERS)
    if not is_app and (meta.get('HTTP_AUTHORIZATION', '') or '').startswith('Bearer ') \
            and not request.COOKIES.get('sessionid'):
        is_app = True
    if rules.is_bot(ua, is_app=is_app):
        return None

    if user is None:
        user = _resolve_user(request)
    uid = ''
    if user is not None:
        uid = str(getattr(user, 'id', '') or '')
        if uid and getattr(settings, 'ANALYTICS_EXCLUDE_STAFF', True) and getattr(user, 'is_admin', False):
            return None

    now = int(time.time() * 1000)
    secret = settings.SECRET_KEY
    ip = client_ip(request)
    if uid:
        visitor = rules.user_visitor_id(secret, uid)
    else:
        local_day = time.strftime('%Y-%m-%d', time.localtime(now / 1000))
        visitor = rules.anon_visitor_id(secret, local_day, ip, ua)

    utm = utm if utm is not None else {k: request.GET.get(f'utm_{k}', '') or '' for k in ('source', 'medium', 'campaign')}
    ref_url = referrer if referrer is not None else (meta.get('HTTP_REFERER', '') or '')
    ref = rules.classify_referrer(ref_url, own_hosts(request), utm.get('source', ''), utm.get('medium', ''))

    page_path = path if path is not None else request.path
    page = rules.classify_page(page_path)

    platform = app_platform or (meta.get('HTTP_X_APP_PLATFORM', '') if is_app else '') \
        or rules.detect_platform(ua)
    country, city = _geo_from_headers(meta)

    return {
        'path': page_path[:2000],
        'page_key': page.key[:200],
        'referrer': rules.referrer_label(ref_url),
        'referrer_domain': ref.host[:255],
        'referrer_type': ref.channel,
        'referrer_name': ref.name[:80],
        'utm_source': (utm.get('source', '') or '')[:255],
        'utm_medium': (utm.get('medium', '') or '')[:255],
        'utm_campaign': (utm.get('campaign', '') or '')[:255],
        'source': 'app' if is_app else 'web',
        'platform': (platform or '')[:30],
        'device_class': rules.device_class(ua) if not is_app or ua else 'mobile',
        'browser': rules.browser_name(ua)[:30],
        'visitor_id': visitor,
        'user_identifier': uid[:255],
        'country': country,
        'city': city,
        'created_at': now,
        '_touch_user': uid,
        '_ip': ip,
    }
