import secrets
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import HttpResponseNotFound
from django.http.request import validate_host

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

        ws_url = getattr(settings, 'WS_PUBLIC_URL', '') or ''
        if not ws_url:
            try:
                import glob as _glob
                import re as _re
                for path in sorted(_glob.glob('/tmp/cf_quick*.log'), reverse=True):
                    try:
                        with open(path) as f:
                            content = f.read()
                        m = _re.search(r'https://([a-z0-9-]+\.trycloudflare\.com)', content)
                        if m:
                            ws_url = 'wss://' + m.group(1) + '/ws/'
                            break
                    except OSError:
                        continue
            except Exception:
                pass

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