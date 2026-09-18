"""
Google Identity Services authentication for NEBians.

Uses GIS on the frontend (One Tap / popup) to get a credential (JWT),
then verifies it on the backend using the google-auth library.

GIS credential tokens have:
- Issuer: accounts.google.com / https://accounts.google.com
- Audience: the OAuth 2.0 web client ID

We also accept Firebase ID tokens (issuer: securetoken.google.com/<project>)
for backward compatibility.
"""
import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .security import get_user_by_auth_token, hash_auth_token

logger = logging.getLogger(__name__)

FIREBASE_ISSUER_PREFIX = 'https://securetoken.google.com/'

_AUTH_TOKEN_CACHE_SECONDS = 300


def verify_google_token(id_token: str):
    """
    Verifies a Google ID Token from GIS or Firebase Auth.

    Returns a dict with {userId, email, displayName, photoUrl} or None.
    """
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        firebase_project_id = settings.FIREBASE_PROJECT_ID
        google_client_id = settings.GOOGLE_CLIENT_ID

        audiences = [google_client_id, firebase_project_id]

        last_error = None
        for audience in audiences:
            try:
                idinfo = google_id_token.verify_oauth2_token(
                    id_token,
                    google_requests.Request(),
                    audience,
                )

                issuer = idinfo.get('iss', '')
                valid_issuers = (
                    'accounts.google.com',
                    'https://accounts.google.com',
                    f'{FIREBASE_ISSUER_PREFIX}{firebase_project_id}',
                )
                if issuer not in valid_issuers:
                    last_error = f"Invalid issuer: {issuer}"
                    continue

                logger.info("Google token verified (audience=%s, issuer=%s, email=%s)",
                            audience, issuer, idinfo.get('email'))
                return {
                    'userId': idinfo.get('sub'),
                    'email': idinfo.get('email'),
                    'email_verified': bool(idinfo.get('email_verified', False)),
                    'displayName': idinfo.get('name'),
                    'photoUrl': idinfo.get('picture'),
                }
            except ValueError as e:
                last_error = str(e)
                logger.debug("Token verification failed for audience %s: %s", audience, e)
                continue

        logger.warning("Token verification failed for all audiences: %s", last_error)
        return None
    except Exception as e:
        logger.error("Token verification error: %s", e)
        return None


class AuthTokenAuthentication(BaseAuthentication):
    """
    DRF authentication backend.
    Reads Authorization: Bearer <auth_token> header and resolves it
    to a User via the server-issued auth_token stored in the User model.
    Results are cached for 5 minutes to avoid per-request DB lookups.
    Does NOT raise an error for missing/invalid tokens — views handle that.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header[7:].strip()
        if not token:
            return None

        cache_key = f'auth_user:{hash_auth_token(token)}'
        user_id = cache.get(cache_key)
        if user_id is not None:
            try:
                return (User.objects.get(pk=user_id), token)
            except User.DoesNotExist:
                cache.delete(cache_key)

        try:
            user = get_user_by_auth_token(token)
            cache.set(cache_key, user.id, _AUTH_TOKEN_CACHE_SECONDS)
            return (user, token)
        except User.DoesNotExist:
            logger.warning("Auth token not found")
            return None

    def authenticate_header(self, request):
        return 'Bearer'
