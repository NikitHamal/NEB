"""Authentication for the Background Agent.

Admins use the same validated platform-account session as the custom admin
panel.
"""
from __future__ import annotations

from django.urls import reverse
from django.shortcuts import redirect

from api.models import User
from api.security import get_user_by_auth_token
from . import api_client

SESSION_KEY = 'bg_agent_admin_id'
_REQUEST_ATTR = '_bg_admin'
_UNSET = object()


def _is_admin(user) -> bool:
    return bool(
        user
        and getattr(user, 'is_admin', False)
        and not getattr(user, 'is_banned', False)
        and not getattr(user, 'is_bot', False)
    )


def get_bg_admin(request):
    """Return the authenticated platform admin (api.User) or None.

    Cached on the request object for the duration of the request.
    """
    cached = getattr(request, _REQUEST_ATTR, _UNSET)
    if cached is not _UNSET:
        return cached
    if hasattr(request, 'session') and SESSION_KEY in request.session:
        request.session.pop(SESSION_KEY, None)
        request.session.modified = True
    user = None
    if hasattr(request, 'session'):
        token = request.session.get('auth_token')
        if token:
            try:
                user = get_user_by_auth_token(token)
            except (User.DoesNotExist, ValueError):
                api_client.clear_session_auth(request)
    if not _is_admin(user):
        user = None
    setattr(request, _REQUEST_ATTR, user)
    return user


def require_bg_admin(request):
    """Return None if an admin is signed in, else a redirect to the agent login.

    The login view bounces back to ?next= so deep links / API calls survive.
    """
    if get_bg_admin(request):
        return None
    login_url = reverse('web:background_agent_login')
    # Preserve the requested path so AJAX/HTML flows return after sign-in.
    full_path = request.get_full_path()
    return redirect(f'{login_url}?next={full_path}')


def require_bg_admin_json(request):
    """Same as require_bg_admin but returns a JsonResponse-ready flag.

    Returns None when authorized, else ``(False, error_response)``. JSON
    endpoints can't use a 302 redirect cleanly, so they should respond with a
    401 and let the frontend send the user to the login page.
    """
    from django.http import JsonResponse
    if get_bg_admin(request):
        return None
    resp = JsonResponse({'ok': False, 'error': 'Sign in to continue.', 'authRequired': True}, status=401)
    return (False, resp)


def logout_bg_admin(request) -> None:
    request.session.pop(SESSION_KEY, None)
    request.session.modified = True
    setattr(request, _REQUEST_ATTR, None)
