from django.conf import settings

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=()')
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin-allow-popups')
        response.setdefault('X-Permitted-Cross-Domain-Policies', 'none')
        
        img_sources = "img-src 'self' data: https:;"
        connect_sources = "connect-src 'self' https://accounts.google.com;"
        
        if settings.DEBUG:
            img_sources = "img-src 'self' data: http: https:;"
            connect_sources = "connect-src 'self' http: https:;"
            
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://accounts.google.com https://www.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            f"{img_sources} "
            "frame-src 'self' https:; "
            f"{connect_sources} "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        )
        response.setdefault('Content-Security-Policy', csp)
        return response
