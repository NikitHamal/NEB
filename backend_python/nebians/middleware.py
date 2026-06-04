import secrets
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http.request import validate_host


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
        for suffix in self.suffixes:
            if host.endswith('.' + suffix) or host == suffix:
                # Rewrite the HTTP_HOST header so Django uses the canonical
                # host in URL generation, CSRF checks, and the
                # Vary/Origin handling. The actual client connection is
                # still on the trycloudflare domain.
                request.META['HTTP_HOST'] = self.CANONICAL_HOST
                request._mirrored_host = host
                break
        return self.get_response(request)


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        response.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()')
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin-allow-popups')
        response.setdefault('X-Permitted-Cross-Domain-Policies', 'none')
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')

        nonce = getattr(request, 'csp_nonce', '')
        img_sources = "img-src 'self' data: https:;"
        connect_sources = "connect-src 'self' https://accounts.google.com;"

        if settings.DEBUG:
            img_sources = "img-src 'self' data: http: https:;"
            connect_sources = "connect-src 'self' http: https:;"

        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' 'unsafe-eval' https://accounts.google.com https://www.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            f"{img_sources} "
            "frame-src 'self' https:; "
            f"{connect_sources} "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        response.setdefault('Content-Security-Policy', csp)
        return response