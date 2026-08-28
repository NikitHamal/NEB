import os
import time
import secrets
from urllib.parse import urlparse
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
    ws_url_txt = getattr(settings, 'WS_URL_TXT', '') or os.path.join(
        getattr(settings, 'BASE_DIR', ''), 'ws_url.txt')
    log_paths = [ws_url_txt] + [
        '/home/consicac/nebians_api/logs/cloudflared.log',
    ] + sorted(_glob.glob('/tmp/cf_quick*.log'), reverse=True)
    for path in log_paths:
        try:
            with open(path) as f:
                content = f.read()
            matches = _re.findall(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)', content)
            if matches:
                return 'wss://' + matches[-1].rstrip('/').rstrip('/ws').rstrip('/') + '/ws/'
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


_SKIP_PREFIXES = (
    '/static/', '/ajax/', '/api/',
    '/admin/',
    '/manifest.json', '/robots.txt', '/sitemap.xml',
    '/favicon.ico',
)

_APP_HEADERS = ('HTTP_X_APP_PLATFORM', 'HTTP_X_APP_VERSION')

_SEARCH_DOMAINS = ('google.', 'bing.', 'yahoo.', 'duckduckgo.', 'baidu.', 'yandex.', 'ask.', 'ecosia.', 'qwant.')
_SOCIAL_DOMAINS = ('facebook.', 'twitter.', 'x.com', 'instagram.', 'linkedin.', 'reddit.', 'tiktok.', 'pinterest.', 'youtube.', 'whatsapp.', 'telegram.', 'discord.', 'snapchat.')


def _classify_referrer(referrer_domain, own_domain):
    if not referrer_domain:
        return 'direct'
    if referrer_domain == own_domain or referrer_domain.endswith('.' + own_domain):
        return 'internal'
    rd = referrer_domain.lower()
    for sd in _SEARCH_DOMAINS:
        if sd in rd:
            return 'search'
    for sd in _SOCIAL_DOMAINS:
        if sd in rd:
            return 'social'
    return 'referral'


def _resolve_geo(ip_address):
    """Resolve country/city from IP using ip-api.com (free, no key needed).
    Results are cached in Redis for 30 days to avoid repeated API calls."""
    if not ip_address or ip_address in ('127.0.0.1', '::1', '0.0.0.0'):
        return '', ''
    cache_key = f'geo:{ip_address}'
    cached = cache.get(cache_key)
    if cached:
        parts = cached.split('|', 1)
        return parts[0] if parts else '', parts[1] if len(parts) > 1 else ''
    try:
        import urllib.request as _urlopen
        url = f'http://ip-api.com/json/{ip_address}?fields=country,city'
        req = _urlopen.Request(url, headers={'User-Agent': 'NEBians/1.0'})
        with _urlopen(req, timeout=3) as resp:
            data = __import__('json').loads(resp.read().decode())
            if data.get('status') == 'success':
                country = data.get('country', '') or ''
                city = data.get('city', '') or ''
                cache.set(cache_key, f'{country}|{city}', 2592000)  # 30 days
                return country, city
    except Exception:
        pass
    return '', ''


def _detect_platform(user_agent):
    if not user_agent:
        return ''
    ua = user_agent.lower()
    if 'android' in ua:
        return 'android'
    if 'iphone' in ua or 'ipad' in ua or 'ios' in ua:
        return 'ios'
    if 'windows' in ua:
        return 'windows'
    if 'macintosh' in ua or 'mac os x' in ua:
        return 'mac'
    if 'linux' in ua:
        return 'linux'
    if 'cros' in ua:
        return 'chromeos'
    return ''


class PageViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method != 'GET':
            return response
        if response.status_code != 200:
            return response

        path = request.path.lower()
        for prefix in _SKIP_PREFIXES:
            if path.startswith(prefix):
                return response

        now = int(time.time() * 1000)
        referrer = request.META.get('HTTP_REFERER', '') or ''
        own_domain = request.get_host().split(':')[0].lower()

        referrer_domain = ''
        if referrer:
            try:
                referrer_domain = urlparse(referrer).hostname or ''
            except Exception:
                referrer_domain = ''

        referrer_type = _classify_referrer(referrer_domain, own_domain)

        utm_source = request.GET.get('utm_source', '') or ''
        utm_medium = request.GET.get('utm_medium', '') or ''
        utm_campaign = request.GET.get('utm_campaign', '') or ''

        user_agent = request.META.get('HTTP_USER_AGENT', '') or ''

        is_app = False
        for header in _APP_HEADERS:
            if request.META.get(header, ''):
                is_app = True
                break
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if auth.startswith('Bearer ') and not request.COOKIES.get('sessionid'):
            is_app = True

        source = 'app' if is_app else 'web'
        platform = ''
        if is_app:
            platform = request.META.get('HTTP_X_APP_PLATFORM', '') or _detect_platform(user_agent)
        else:
            platform = _detect_platform(user_agent)

        ip_address = request.META.get('REMOTE_ADDR', None)
        session_key = request.session.session_key or ''
        user_id = None
        user_identifier = ''
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                user_id = int(request.user.id) if str(request.user.id).isdigit() else None
                if user_id is not None:
                    from api.models import User as UserModel
                    try:
                        uid_str = str(request.user.id)
                        user_identifier = uid_str[:255]
                        UserModel.objects.filter(pk=uid_str).update(last_active=now)
                        cache.sadd('presence:online', uid_str)
                        cache.expire('presence:online', 300)
                        cache.set(f'presence:user:{uid_str}', now, 300)
                    except Exception:
                        pass
            except (ValueError, TypeError):
                pass

        try:
            from api.models import PageView
            # Resolve geo-IP for web visitors
            geo_country, geo_city = '', ''
            if ip_address:
                try:
                    geo_country, geo_city = _resolve_geo(ip_address)
                except Exception:
                    pass
            PageView.objects.create(
                path=request.path,
                full_url=request.build_absolute_uri(),
                referrer=referrer[:2000],
                referrer_domain=referrer_domain[:255],
                referrer_type=referrer_type,
                utm_source=utm_source[:255],
                utm_medium=utm_medium[:255],
                utm_campaign=utm_campaign[:255],
                user_agent=user_agent[:2000],
                source=source,
                platform=platform,
                ip_address=ip_address,
                session_key=session_key[:40],
                user_id=user_id,
                user_identifier=user_identifier,
                country=geo_country,
                city=geo_city,
                created_at=now,
            )
        except Exception:
            pass

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
        connect_sources = ["'self'", "https://accounts.google.com", "https://cdn.jsdelivr.net", "https://huggingface.co", "https://*.huggingface.co", "https://github.com", "https://*.githubusercontent.com", "wss://*.trycloudflare.com", "https://*.trycloudflare.com"]

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
            f"script-src 'self' 'nonce-{nonce}' https://accounts.google.com https://www.gstatic.com https://cdn.jsdelivr.net; "
            "worker-src 'self' blob:; "
            "child-src 'self' blob:; "
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
    """Intercepts and records server errors, 429 rate limit lockouts, and unhandled exceptions
    on API endpoints into structured logs for the background agent to analyze and self-heal."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log critical API response failures (429 rate limits, 400 bad requests on uploads/auth, 500s)
        if request.path.startswith('/api/') and response.status_code in (400, 429, 500, 502, 503):
            try:
                log_dir = Path(getattr(settings, 'BASE_DIR', '.')) / 'logs'
                log_dir.mkdir(parents=True, exist_ok=True)
                err_file = log_dir / 'server_errors.log'
                client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
                with open(err_file, 'a', encoding='utf-8') as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] HTTP {response.status_code} | {request.method} {request.path} | IP: {client_ip}\n")
                    if response.status_code == 429:
                        f.write("Event: RATE_LIMIT_LOCKOUT (Too many requests)\n")
                    elif response.status_code >= 500:
                        f.write(f"Event: SERVER_ERROR_{response.status_code}\n")
                    f.write("---\n")
            except Exception:
                pass
                
        return response

    def process_exception(self, request, exception):
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
            return JsonResponse({
                'error': f'Server error: {exception.__class__.__name__}',
                'detail': str(exception) or 'An unexpected error occurred.',
                'path': request.path
            }, status=500)
        return None