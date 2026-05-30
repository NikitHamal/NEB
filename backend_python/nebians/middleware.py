"""Small security-header middleware without adding another dependency."""

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()')
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin-allow-popups')
        response.setdefault('X-Permitted-Cross-Domain-Policies', 'none')
        response.setdefault(
            'Content-Security-Policy',
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://accounts.google.com https://www.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "frame-src 'self' https:; "
            "connect-src 'self' https://accounts.google.com; "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        return response
