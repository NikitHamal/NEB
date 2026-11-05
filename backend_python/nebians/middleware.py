import os
from pathlib import Path
import time
import secrets
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseNotFound
from whitenoise.middleware import WhiteNoiseMiddleware

from . import analytics


def _resolve_ws_public_url():
    """Resolve the public WebSocket URL (uncached).

    Duplicated from web.view_helpers (small wrapper) to avoid a circular
    import between project middleware and the web app's view helpers.
    Picks the NEWEST file by mtime that contains a trycloudflare host, so a
    fresh start_ws_tunnel.log wins over a stale ws_url.txt.
    """
    ws_url = (getattr(settings, 'WS_PUBLIC_URL', '') or '').strip()
    if not ws_url:
        ws_url = (os.environ.get('WS_PUBLIC_URL', '') or '').strip()
    if ws_url:
        return ws_url
    import glob as _glob, re as _re
    candidates = []
    log_paths = [
        '/home/consicac/nebians_api/logs/start_ws_tunnel.log',
        '/home/consicac/nebians_api/logs/cloudflared.log',
        os.path.join(getattr(settings, 'BASE_DIR', ''), 'logs', 'cloudflared.log'),
    ] + sorted(_glob.glob('/tmp/cf_quick*.log'), reverse=True)
    for path in log_paths:
        try:
            with open(path, 'rb') as f:
                f.seek(0, 2)
                f.seek(max(0, f.tell() - 65536))
                content = f.read().decode('utf-8', 'ignore')
            matches = _re.findall(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)', content)
            if matches:
                host = matches[-1].rstrip('/').rstrip('/ws').rstrip('/')
                url = 'wss://' + host + '/ws/'
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    mtime = 0
                candidates.append((mtime, url))
        except OSError:
            continue
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    # Fallback: ws_url.txt cache (not authoritative — logs win even if ws_url.txt newer)
    ws_url_txt = getattr(settings, 'WS_URL_TXT', '') or os.path.join(
        getattr(settings, 'BASE_DIR', ''), 'ws_url.txt')
    try:
        with open(ws_url_txt) as f:
            content = f.read().strip()
        if content:
            m = _re.search(r'([a-z0-9-]+\.trycloudflare\.com)', content)
            if m:
                return 'wss://' + m.group(1) + '/ws/'
            if content.startswith('wss://'):
                return content.strip()
    except OSError:
        pass
    return ''


def _get_ws_public_url_cached():
    """Cached (15s) resolution of the public WS URL — avoids per-request file I/O."""
    # Don't cache empty — next request should retry immediately to pick up a new tunnel.
    # A down tunnel resolves to '' so clients use polling instead of a dead host.
    url = cache.get('ws_public_url_resolved')
    if url is None:
        url = _resolve_ws_public_url()
        if url:
            cache.set('ws_public_url_resolved', url, 15)
    if url:
        try:
            from nebians.tunnel_health import is_tunnel_healthy
            if not is_tunnel_healthy():
                return ''
        except Exception:
            pass
    return url

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


class ResilientWhiteNoiseMiddleware(WhiteNoiseMiddleware):
    """WhiteNoise, but a file that vanished mid-deploy is a 404, not a 500.

    WhiteNoise indexes STATIC_ROOT once per process, at worker start.
    `collectstatic --clear` deletes and rewrites that tree while the LSAPI
    workers are still serving with the old index, so for those few seconds a
    request can name a compressed file that is momentarily gone. That is a
    transient miss, not a server error, and it must never mail the admins.
    """

    def __call__(self, request):
        if not request.path_info.startswith(self.static_prefix):
            return super().__call__(request)
        try:
            return super().__call__(request)
        except FileNotFoundError:
            return HttpResponseNotFound()


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
        if auth.startswith('Bearer '):
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
        # Use raw HTTP_HOST to avoid get_host() raising DisallowedHost before we
        # can rewrite the trycloudflare wildcard. ALLOWED_HOSTS now also contains
        # '.trycloudflare.com' so get_host() would pass, but raw header is safer
        # and avoids a validation round-trip.
        raw_host = request.META.get('HTTP_HOST', '') or request.META.get('SERVER_NAME', '')
        host = raw_host.split(':')[0].lower()
        # Refresh suffixes from settings each request so a .env change without
        # code deploy still takes effect (settings are reloaded per worker).
        suffixes = list(getattr(settings, 'ALLOWED_HOST_SUFFIXES', [])) or self.suffixes
        matched_suffix = False
        original_host = None
        for suffix in suffixes:
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


class PageViewTrackingMiddleware:
    """Record one anonymous page view per real, full-page HTML hit.

    All decisions (what counts, who is a bot, what a referrer means) live in
    nebians.analytics; this class only wires them to the request cycle.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Anonymous page-cache hits are page views like any other. They used to
        # be skipped (a DB write per hit), which hid most logged-out traffic on
        # the public pages. Recording is now a non-blocking queue put, so the
        # cache win is kept and the visit is still counted.
        try:
            if analytics.is_trackable_request(request, response):
                event = analytics.event_from_request(request)
                if event:
                    analytics.submit(event)
        except Exception:
            pass  # analytics must never break a page
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
        response.setdefault('Permissions-Policy', 'geolocation=(), microphone=(self), camera=(), payment=()')
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin-allow-popups')
        response.setdefault('X-Permitted-Cross-Domain-Policies', 'none')
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')

        if 'Server' in response:
            del response['Server']

        nonce = getattr(request, 'csp_nonce', '')
        img_sources = "img-src 'self' data: https:;"
        connect_sources = ["'self'", "data:", "blob:", "https://accounts.google.com", "https://cdn.jsdelivr.net", "https://esm.sh", "https://tessdata.projectnaptha.com", "https://huggingface.co", "https://*.huggingface.co", "https://github.com", "https://*.githubusercontent.com", "wss://*.trycloudflare.com", "https://*.trycloudflare.com"]

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
            connect_src_str = "connect-src 'self' data: blob: http: https: wss:;"

        img_sources_blob = img_sources.replace("img-src ", "img-src blob: ")
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' 'wasm-unsafe-eval' https://accounts.google.com https://www.gstatic.com https://cdn.jsdelivr.net https://esm.sh; "
            "worker-src 'self' blob: data: https://cdn.jsdelivr.net; "
            "child-src 'self' blob: data: https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
            f"{img_sources_blob} "
            "media-src 'self' https: blob: data:; "
            "frame-src 'self' https:; "
            f"{connect_src_str} "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        response.setdefault('Content-Security-Policy', csp)
        return response


class ApiUnhandledExceptionMiddleware:
    """Intercepts and records server errors (5xx) and unhandled exceptions
    on API endpoints into structured logs for the background agent to analyze and self-heal."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log only server errors (5xx) here. 4xx (including 429 throttles)
        # are normal client behavior — DRF already answers them as JSON
        # with Retry-After — and file-logging each one churns the disk on
        # an overloaded box with zero diagnostic value.
        if request.path.startswith('/api/') and response.status_code in (500, 502, 503):
            try:
                log_dir = Path(getattr(settings, 'BASE_DIR', '.')) / 'logs'
                log_dir.mkdir(parents=True, exist_ok=True)
                err_file = log_dir / 'server_errors.log'
                client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
                with open(err_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] HTTP {response.status_code} | {request.method} {request.path} | IP: {client_ip}\n")
                    f.write(f"Event: SERVER_ERROR_{response.status_code}\n")
                    f.write("---\n")
            except Exception:
                pass
                
        return response

    def process_exception(self, request, exception):
        from django.core.exceptions import PermissionDenied
        from django.http import Http404
        # Http404/403 are normal web traffic (mistyped URLs, bot probes, locked
        # profiles) — let Django's default handling render the error page. Logging
        # them here at ERROR would fire an admin email for every stray hit.
        if isinstance(exception, (Http404, PermissionDenied)):
            return None
        import logging
        import traceback
        from django.http import JsonResponse
        
        logger = logging.getLogger('django.request')
        logger.exception("Unhandled server exception at %s: %s", request.path, exception)
        try:
            log_dir = Path(getattr(settings, 'BASE_DIR', '.')) / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            err_file = log_dir / 'server_errors.log'
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
            with open(err_file, 'a', encoding='utf-8') as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] UNHANDLED EXCEPTION | {request.method} {request.path} | IP: {client_ip}\n")
                f.write(f"Error: {exception.__class__.__name__}: {str(exception)}\n")
                traceback.print_exc(file=f)
                f.write("---\n")
        except Exception:
            pass

        if request.path.startswith('/api/') or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            resp = JsonResponse({
                'error': f'Server error: {exception.__class__.__name__}',
                'detail': str(exception) or 'An unexpected error occurred.',
                'path': request.path
            }, status=500)
            resp['Cache-Control'] = 'no-store'
            return resp
        return None