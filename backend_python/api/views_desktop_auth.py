"""API half of the desktop browser hand-off. See api/desktop_auth.py for the protocol."""
from django.conf import settings

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .security import issue_auth_token
from .serializers import UserSerializer
from .throttles import AuthRateThrottle
from .view_helpers import logger
from . import desktop_auth


def _site_origin(request) -> str:
    configured = (getattr(settings, 'SITE_URL', '') or getattr(settings, 'PUBLIC_SITE_URL', '') or '').rstrip('/')
    if configured.startswith('http'):
        return configured
    return request.build_absolute_uri('/').rstrip('/')


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def desktop_auth_start(request):
    """Body: { "challenge": "<b64url sha256 of the verifier>", "device": "Windows 11 · NEBians 0.2" }
    Returns: { state, loginUrl, expiresIn, interval }"""
    state = desktop_auth.create_request(request.data.get('challenge'), request.data.get('device'))
    if not state:
        return Response({'error': 'A valid PKCE challenge is required.'}, status=400)
    return Response({
        'state': state,
        'loginUrl': f"{_site_origin(request)}/desktop-auth/?state={state}",
        'expiresIn': desktop_auth.TTL_SECONDS,
        'interval': desktop_auth.POLL_INTERVAL_SECONDS,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def desktop_auth_poll(request):
    """Body: { "state": "...", "verifier": "..." }
    202 {status:'pending'} while waiting; 200 {status:'success', authToken, isNewUser, user} once;
    410 when the request expired / was denied / was already redeemed; 400 for malformed input."""
    state = request.data.get('state')
    verifier = request.data.get('verifier')
    if not desktop_auth.valid_state(state) or not isinstance(verifier, str):
        return Response({'error': 'state and verifier are required.'}, status=400)

    outcome, user_pk = desktop_auth.redeem(state, verifier)
    if outcome == 'pending':
        return Response({'status': 'pending'}, status=202)
    if outcome != 'ok':
        return Response({'status': 'expired', 'error': 'This sign-in request expired or was cancelled.'}, status=410)

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return Response({'status': 'expired', 'error': 'This account no longer exists.'}, status=410)
    if getattr(user, 'is_banned', False):
        return Response({'error': 'This account has been banned'}, status=403)

    auth_token = issue_auth_token(user)
    username = user.username or ''
    is_new = username.startswith(('user_', 'github_')) and not getattr(user, 'bio', '')
    logger.info('desktop_auth: session issued for %s', user.username or user.id)
    return Response({
        'status': 'success',
        'isNewUser': bool(is_new),
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    })
