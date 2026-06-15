import secrets
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import DisallowedHost
from django.http import HttpResponseNotFound
from django.http.request import validate_host


def _resolve_ws_public_url():
    """Resolve the public WebSocket URL (uncached).

    Duplicated from web.view_helpers (small wrapper) to avoid a circular
    import between project middleware and the web app's view helpers.
    """
    ws_url = getattr(settings, 'WS_PUBLIC_URL', '') or ''
    if ws_url:
        return ws_url
    import glob as _glob, re as _re
    log_paths = sorted(_glob.glob('/tmp/cf_quick*.log'), reverse=True) + [
        '/home/consicac/nebians_api/logs/cloudflared.log',
    ]
    for path in log_paths:
        try:
            with open(path) as f:
                content = f.read()
            m = _re.search(r'https://([a-z0-9-]+\.trycloudflare\.com)', content)
            if m:
                return 'wss://' + m.group(1) + '/ws/'
        except OSError:
            continue
    return ''


def _get_ws_public_url_cached():
    """Cached (60s) resolution of the public WS URL — avoids per-request file I/O."""
    return cache.get_or_set('ws_public_url_resolved', _resolve_ws_public_url, 60)

SENSITIVE_PATHS_404 = (
    '/.git/',
    '/.env',
    '/.env.local',
    '/.env.production',
    '/.env.development',
    '/.DS_Store',
    '/wp-admin',
    '/wp-login',
    '/phpmyadmin',
    '/xmlrpc.php',
    '/web.config',
    '/.htaccess',
    '/.htpasswd',
    '/config.py',
    '/settings.py',
    '/database.yml',
    '/db.sqlite3',
    '/debug/',
    '/server-status',
    '/server-info',
)


def csp_nonce_context(request):
    return {'csp_nonce': getattr(request, 'csp_nonce', '')}


class BearerCsrfExemptMiddleware:
    """Skip CSRF enforcement for Bearer-token API clients (mobile apps).

    CSRF protects cookie/session-authenticated requests. Requests that carry an
    `Authorization: Bearer <token>` header are not cookie-authenticated from a
    browser context (browsers cannot attach custom Authorization headers
    cross-site without a CORS preflight), so CSRF does not apply to them.

    This lets the Android app call the `/ajax/` endpoints (which return the
    exact web JSON shapes) using its auth token.

    Place BEFORE CsrfViewMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if auth.startswith('Bearer ') and not request.COOKIES.get('sessionid'):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)


class AllowedHostMiddleware:
    """Extends Django's ALLOWED_HOSTS check with suffix wildcards.

    Suffix entries in settings.ALLOWED_HOSTS_GLOB (e.g. '.trycloudflare.com')
    match any subdomain. We rewrite the Host header to the canonical domain
    before CommonMiddleware's host validation runs, so Django-generated
    absolute URLs and CSRF checks use the production host.

    Place BEFORE CommonMiddleware.
    """

    CANONICAL_HOST = 'nebians.consica.com.np'

    def __init__(self, get_response):
        self.get_response = get_response
        self.suffixes = list(getattr(settings, 'ALLOWED_HOST_SUFFIXES', []))

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        matched_suffix = False
        original_host = None
        for suffix in self.suffixes:
            if host.endswith('.' + suffix) or host == suffix:
                matched_suffix = True
                original_host = request.META.get('HTTP_HOST')
                request.META['HTTP_HOST'] = self.CANONICAL_HOST
                request._mirrored_host = host
                break
        
        response = self.get_response(request)
        
        if matched_suffix and response.has_header('Location') and original_host:
            location = response['Location']
            canonical_prefix = f'https://{self.CANONICAL_HOST}'
            if location.startswith(canonical_prefix):
                response['Location'] = location.replace(canonical_prefix, f'https://{original_host}', 1)
            else:
                canonical_prefix_http = f'http://{self.CANONICAL_HOST}'
                if location.startswith(canonical_prefix_http):
                    response['Location'] = location.replace(canonical_prefix_http, f'http://{original_host}', 1)
                    
        return response


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lower().rstrip('/')
        for sensitive in SENSITIVE_PATHS_404:
            if path == sensitive.lower().rstrip('/') or path.startswith(sensitive.lower()):
                return HttpResponseNotFound('<h1>Not Found</h1>', content_type='text/html', status=404)

        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        response.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()')
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin-allow-popups')
        response.setdefault('X-Permitted-Cross-Domain-Policies', 'none')
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')

        if 'Server' in response:
            del response['Server']

        nonce = getattr(request, 'csp_nonce', '')
        img_sources = "img-src 'self' data: https:;"
        connect_sources = ["'self'", "https://accounts.google.com"]

        ws_url = _get_ws_public_url_cached()

        if ws_url:
            import re as _re2
            m = _re2.match(r'(wss?|https?)://([a-z0-9.-]+)', ws_url)
            if m:
                host = m.group(2)
                connect_sources.append('wss://' + host)
                connect_sources.append('https://' + host)

        connect_src_str = "connect-src " + " ".join(connect_sources) + ";"

        if settings.DEBUG:
            img_sources = "img-src 'self' data: http: https:;"
            connect_src_str = "connect-src 'self' http: https: wss:;"

        img_sources_blob = img_sources.replace("img-src ", "img-src blob: ")
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' 'unsafe-eval' https://accounts.google.com https://www.gstatic.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            f"{img_sources_blob} "
            "frame-src 'self' https:; "
            f"{connect_src_str} "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        response.setdefault('Content-Security-Policy', csp)
        return response