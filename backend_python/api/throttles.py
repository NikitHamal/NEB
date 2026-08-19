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


class WriteActionRateThrottle(_IdentityThrottle):
    scope = 'write_action'


class ReportRateThrottle(_IdentityThrottle):
    scope = 'report'


class SearchRateThrottle(_IdentityThrottle):
    scope = 'search'


class UploadRateThrottle(_IdentityThrottle):
    scope = 'upload'


class ViewIncrementRateThrottle(_IdentityThrottle):
    scope = 'view_increment'


class ArenaChatRateThrottle(_IdentityThrottle):
    """Throttle for community chat endpoints (per-user or per-IP).

    Generous limits — we mainly want to prevent one user from monopolising
    the shared upstream proxies.
    """
    scope = 'arena_chat'


class ArenaListRateThrottle(_IdentityThrottle):
    """Cheaper to call (cached model list), but still rate-limited."""
    scope = 'arena_list'


class SignupRateThrottle(_IdentityThrottle):
    scope = 'signup'
