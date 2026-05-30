"""
Firebase Authentication for NEBians.

Uses Firebase Auth on the frontend (signInWithPopup) to get an ID token,
then verifies it on the backend using the google-auth library.

Firebase ID tokens have:
- Issuer: https://securetoken.google.com/<project_id>
- Audience: <project_id> (NOT the OAuth web client ID)

So we use verify_oauth2_token with the Firebase project ID as audience,
and accept the Firebase issuer in addition to the Google OAuth issuer.
"""
import logging
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

logger = logging.getLogger(__name__)

FIREBASE_ISSUER_PREFIX = 'https://securetoken.google.com/'

def verify_google_token(id_token: str):
    """
    Verifies a Firebase ID Token using the google-auth library.
    Accepts tokens from both Google OAuth and Firebase Auth flows.

    Returns a dict with {userId, email, displayName, photoUrl} or None.
    """
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        firebase_project_id = settings.FIREBASE_PROJECT_ID
        google_client_id = settings.GOOGLE_CLIENT_ID

        idinfo = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            firebase_project_id,
        )

        issuer = idinfo.get('iss', '')
        valid_issuers = (
            'accounts.google.com',
            'https://accounts.google.com',
            f'{FIREBASE_ISSUER_PREFIX}{firebase_project_id}',
        )
        if issuer not in valid_issuers:
            logger.warning("Token issuer mismatch: %s (expected one of: %s)", issuer, valid_issuers)
            return None

        return {
            'userId': idinfo.get('sub'),
            'email': idinfo.get('email'),
            'displayName': idinfo.get('name'),
            'photoUrl': idinfo.get('picture'),
        }
    except ValueError as e:
        logger.warning("Token verification failed (ValueError): %s", e)
        return None
    except Exception as e:
        logger.error("Token verification error: %s", e)
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