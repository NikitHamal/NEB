"""Standalone auth for the Background Agent.

The Background Agent lives outside the Django admin panel. Admins sign in with
their *platform* account (api.User) using a username or email plus a password.
Authentication is independent of:

  * Django's auth.User / the `/admin/` staff login (left untouched), and
  * the public site's bearer-token auth (auth_token).

A logged-in admin is kept in the session under SESSION_KEY and surfaced on the
request as ``request.bg_admin``. The GitHub OAuth credential is bound to this
same api.User account, so the same admin does not re-authorize when signing in
from another device.
"""
from __future__ import annotations

from django.urls import reverse
from django.shortcuts import redirect

from api.models import User
from api.security import verify_password

SESSION_KEY = 'bg_agent_admin_id'
_REQUEST_ATTR = '_bg_admin'
_UNSET = object()


def _is_admin(user) -> bool:
    return bool(user and getattr(user, 'is_admin', False) and not getattr(user, 'is_locked', False) and not getattr(user, 'is_bot', False))


def get_bg_admin(request):
    """Return the authenticated platform admin (api.User) or None.

    Cached on the request object for the duration of the request.
    """
    cached = getattr(request, _REQUEST_ATTR, _UNSET)
    if cached is not _UNSET:
        return cached
    user_id = request.session.get(SESSION_KEY) if hasattr(request, 'session') else None
    user = None
    if user_id:
        user = User.objects.filter(pk=user_id).first()
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


def login_bg_admin(request, user) -> None:
    request.session[SESSION_KEY] = str(user.id)
    request.session.modified = True
    setattr(request, _REQUEST_ATTR, user)


def logout_bg_admin(request) -> None:
    request.session.pop(SESSION_KEY, None)
    request.session.modified = True
    setattr(request, _REQUEST_ATTR, None)


def authenticate_bg_admin(identifier: str, password: str):
    """Authenticate by username OR email + password. Returns (user, error).

    Only active platform admins (is_admin, not locked, not a bot) may sign in.
    """
    identifier = (identifier or '').strip()
    if not identifier or not password:
        return None, 'Enter your username or email and password.'
    user = (
        User.objects.filter(username__iexact=identifier).first()
        or User.objects.filter(email__iexact=identifier).first()
    )
    if not user or not user.password_hash:
        # Identical message for unknown-user vs wrong-password to avoid leakage.
        return None, 'Invalid credentials.'
    ok, needs_rehash = verify_password(password, user.password_hash)
    if not ok:
        return None, 'Invalid credentials.'
    if getattr(user, 'is_banned', False):
        return None, 'This account has been banned.'
    if not _is_admin(user):
        return None, 'This account is not an administrator.'
    if needs_rehash:
        # Re-hash with the current default hasher without changing the password.
        try:
            from api.security import hash_password
            user.password_hash = hash_password(password)
            user.save(update_fields=['password_hash'])
        except Exception:
            pass
    return user, None
