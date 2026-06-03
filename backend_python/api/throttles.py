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
    """Throttle for AI4Bharat Arena chat endpoints (per-user or per-IP).

    Generous limits — the upstream arena already enforces 20 msgs / token, and
    the pool spreads load across many tokens. We mainly want to prevent one
    user from monopolising the pool.
    """
    scope = 'arena_chat'


class ArenaListRateThrottle(_IdentityThrottle):
    """Cheaper to call (cached model list), but still rate-limited."""
    scope = 'arena_list'
