"""
ASGI middleware for WebSocket connections.

JWTAuthMiddleware:    authenticates the user via the Django session cookie
                      (same mechanism as the rest of the site) or an
                      Authorization: Bearer <auth_token> header (used by
                      the Android app and curl-based clients). Sets
                      scope['user'] to the resolved User, or AnonymousUser.

OriginValidatorMiddleware: rejects WebSocket upgrade requests whose Origin
                      does not match ALLOWED_HOSTS / CORS_ALLOWED_ORIGINS.
                      Prevents cross-site WebSocket hijacking (CSWSH).
"""
import logging
from urllib.parse import urlparse

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from api.authentication import get_user_by_auth_token

logger = logging.getLogger(__name__)


def _origin_allowed(origin):
    """Check if a WebSocket Origin header is allowed."""
    if not origin:
        # Same-origin requests don't send Origin. Allow.
        return True
    try:
        parsed = urlparse(origin)
    except ValueError:
        return False
    host = (parsed.netloc or '').lower()
    if not host:
        return False
    # Match against ALLOWED_HOSTS (any allowed host is ok as origin host)
    allowed_hosts = {h.lower() for h in settings.ALLOWED_HOSTS}
    if host in allowed_hosts:
        return True
    # Match against CORS_ALLOWED_ORIGINS
    for allowed in settings.CORS_ALLOWED_ORIGINS:
        if allowed.lower().endswith(host) or host == allowed.lower().replace('https://', '').replace('http://', ''):
            return True
    return False


class OriginValidatorMiddleware:
    """Reject WS upgrade requests from disallowed origins."""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope.get('type') != 'websocket':
            return await self.inner(scope, receive, send)
        origin = None
        for name, value in scope.get('headers', []):
            if name == b'origin':
                origin = value.decode('latin-1', errors='replace')
                break
        if not _origin_allowed(origin):
            logger.warning('WS origin rejected: %r (path=%s)', origin, scope.get('path'))
            await send({'type': 'websocket.close', 'code': 1008})
            return
        return await self.inner(scope, receive, send)


class JWTAuthMiddleware(BaseMiddleware):
    """
    Resolves scope['user'] for WebSocket scopes.

    Order of precedence:
      1. session.user (set by CookieMiddleware + SessionMiddleware) — used by
         the web frontend, which already has a Django session cookie.
      2. Authorization: Bearer <auth_token> — used by mobile clients and
         for testing. Validated against User.auth_token.
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        if scope.get('type') != 'websocket':
            return await super().__call__(scope, receive, send)

        # AuthMiddlewareStack has already set scope['user'] from the
        # session cookie (if present). We override with the bearer token
        # if Authorization: Bearer <token> is provided. This is the
        # primary auth path for the Android app.
        existing = scope.get('user')
        bearer_user = None
        for name, value in scope.get('headers', []):
            if name == b'authorization':
                auth = value.decode('latin-1', errors='replace')
                if auth.lower().startswith('bearer '):
                    token = auth[7:].strip()
                    bearer_user = await database_sync_to_async(self._resolve_bearer)(token)
                break

        if bearer_user is not None:
            scope['user'] = bearer_user
        elif existing is not None and not getattr(existing, 'is_anonymous', True):
            # Session auth worked. Make sure the user is not locked.
            if getattr(existing, 'is_locked', False):
                scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

    @staticmethod
    def _resolve_bearer(token):
        try:
            u = get_user_by_auth_token(token)
            if u.is_locked:
                return None
            return u
        except Exception:  # noqa: BLE001
            return None
