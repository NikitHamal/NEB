"""
Custom authentication: verifies server-issued auth tokens.
The client sends:  Authorization: Bearer <auth_token>

On /api/auth/google, the Google ID Token is verified once, and a
server-issued auth_token is returned. Subsequent authenticated
endpoints use this auth_token to identify the user — no repeated
Google verification needed.
"""
import logging
import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

logger = logging.getLogger(__name__)


def verify_google_token(id_token: str):
    """
    Validates a Google ID Token via Google's tokeninfo endpoint.
    Returns a dict with {userId, email, displayName, photoUrl} or None.
    """
    try:
        resp = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': id_token},
            timeout=10
        )
        if not resp.ok:
            logger.warning("Google tokeninfo returned %s: %s", resp.status_code, resp.text[:200])
            return None
        payload = resp.json()
        expected_aud = settings.GOOGLE_CLIENT_ID
        if payload.get('aud') != expected_aud:
            logger.warning("Google token aud mismatch: expected=%s got=%s", expected_aud, payload.get('aud'))
            return None
        return {
            'userId': payload.get('sub'),
            'email': payload.get('email'),
            'displayName': payload.get('name'),
            'photoUrl': payload.get('picture'),
        }
    except Exception as e:
        logger.error("Google token verification failed: %s", e)
        return None


class AuthTokenAuthentication(BaseAuthentication):
    """
    DRF authentication backend.
    Reads Authorization: Bearer <auth_token> header and resolves it
    to a User via the server-issued auth_token stored in the User model.
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
            user = User.objects.get(auth_token=token)
            return (user, token)
        except User.DoesNotExist:
            logger.warning("Auth token not found: %s...", token[:8])
            return None

    def authenticate_header(self, request):
        return 'Bearer'


# Legacy import alias — views that referenced GoogleTokenAuthentication
# will still work, but it now uses auth_token-based lookup.
GoogleTokenAuthentication = AuthTokenAuthentication
