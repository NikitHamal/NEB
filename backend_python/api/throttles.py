"""Custom DRF throttles for authentication-sensitive endpoints."""
from rest_framework.throttling import SimpleRateThrottle


class _IdentityThrottle(SimpleRateThrottle):
    """Rate limit by authenticated user id when present, otherwise by IP."""
    scope = 'auth'

    def get_cache_key(self, request, view):
        user = getattr(request, 'user', None)
        if getattr(user, 'is_authenticated', False):
            ident = f'user:{user.pk}'
        else:
            ident = f'ip:{self.get_ident(request)}'
        return self.cache_format % {'scope': self.scope, 'ident': ident}


class AuthRateThrottle(_IdentityThrottle):
    scope = 'auth'


class VerificationRateThrottle(_IdentityThrottle):
    scope = 'verification'
