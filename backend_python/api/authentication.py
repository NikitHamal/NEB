"""
Google Identity Services authentication for NEBians.

Uses the official Google OAuth 2.0 flow:
1. Frontend uses google.accounts.oauth2.initTokenClient (GIS) to get an ID token
2. Backend verifies the ID token using google-auth library (verify_oauth2_token)
3. A server-issued auth_token is returned for subsequent API calls

This replaces the old tokeninfo endpoint approach with proper cryptographic
verification using Google's public keys.
"""
import logging
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

logger = logging.getLogger(__name__)


def verify_google_token(id_token: str):
    """
    Verifies a Google ID Token using the official google-auth library.
    Uses Google's public keys (JWKS) for cryptographic verification —
    no network call to tokeninfo endpoint needed.

    Returns a dict with {userId, email, displayName, photoUrl} or None.
    """
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        client_id = settings.GOOGLE_CLIENT_ID

        idinfo = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            client_id,
        )

        if idinfo.get('iss') not in ('accounts.google.com', 'https://accounts.google.com'):
            logger.warning("Google token issuer mismatch: %s", idinfo.get('iss'))
            return None

        return {
            'userId': idinfo.get('sub'),
            'email': idinfo.get('email'),
            'displayName': idinfo.get('name'),
            'photoUrl': idinfo.get('picture'),
        }
    except ValueError as e:
        logger.warning("Google token verification failed (ValueError): %s", e)
        return None
    except Exception as e:
        logger.error("Google token verification error: %s", e)
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


GoogleTokenAuthentication = AuthTokenAuthentication