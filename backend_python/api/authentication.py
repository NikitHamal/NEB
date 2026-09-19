"""
Google Identity Services authentication for NEBians.

Uses GIS on the frontend (One Tap / popup) to get a credential (JWT),
then verifies it on the backend using the google-auth library.

GIS credential tokens have:
- Issuer: accounts.google.com / https://accounts.google.com
- Audience: the OAuth 2.0 web client ID

Only tokens with a provider-asserted verified email are accepted.
The legacy Firebase ID-token audience was removed (Sep 2026): no client
uses Firebase Auth (Android uses FCM for push only), and accepting it let
anyone mint a valid token for an arbitrary email via our Firebase project.
"""
import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .security import get_user_by_auth_token, hash_auth_token

logger = logging.getLogger(__name__)

_AUTH_TOKEN_CACHE_SECONDS = 300


def verify_google_token(id_token: str):
    """
    Verifies a Google GIS ID Token.

    Returns a dict with {userId, email, email_verified, displayName,
    photoUrl} or None. Tokens without a verified email are rejected.
    """
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        google_client_id = settings.GOOGLE_CLIENT_ID
        if not google_client_id:
            logger.error("verify_google_token: GOOGLE_CLIENT_ID is not configured")
            return None

        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token,
                google_requests.Request(),
                google_client_id,
            )
        except ValueError as e:
            logger.warning("Google token verification failed: %s", e)
            return None

        issuer = idinfo.get('iss', '')
        if issuer not in ('accounts.google.com', 'https://accounts.google.com'):
            logger.warning("Google token rejected: invalid issuer %s", issuer)
            return None

        if not idinfo.get('email_verified', False):
            logger.warning("Google token rejected: email %s is not verified by the provider",
                           idinfo.get('email'))
            return None

        logger.info("Google token verified (email=%s)", idinfo.get('email'))
        return {
            'userId': idinfo.get('sub'),
            'email': idinfo.get('email'),
            'email_verified': True,
            'displayName': idinfo.get('name'),
            'photoUrl': idinfo.get('picture'),
        }
    except Exception as e:
        logger.error("Token verification error: %s", e)
        return None


class AuthTokenAuthentication(BaseAuthentication):
    """
    DRF authentication backend.
    Reads Authorization: Bearer <auth_token> header and resolves it
    to a User via the server-issued auth_token stored in the User model.
    Results are cached for 5 minutes to avoid per-request DB lookups.
    Expired, revoked, bot, and banned tokens are all rejected.
    Does NOT raise an error for missing/invalid tokens — views handle that.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header[7:].strip()
        if not token:
            return None

        try:
            # Always resolve through the central helper so expiry, bot, and
            # ban checks apply. The helper result is cached briefly; the
            # cached user row is re-validated below so a ban/lock takes
            # effect even within the cache window.
            user = get_user_by_auth_token(token)
            if getattr(user, 'is_bot', False) or getattr(user, 'is_banned', False):
                return None
            cache.set(f'auth_user:{hash_auth_token(token)}', user.id, _AUTH_TOKEN_CACHE_SECONDS)
            return (user, token)
        except User.DoesNotExist:
            logger.warning("Auth token not found, expired, revoked, or account barred")
            return None
        except ValueError:
            return None

    def authenticate_header(self, request):
        return 'Bearer'
