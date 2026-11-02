"""Consent page for the desktop browser hand-off (see api/desktop_auth.py)."""
from urllib.parse import quote

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from api import desktop_auth
from api.security import get_user_by_auth_token
from . import api_client as api


def _signed_in_user(request):
    token = api.get_session_token(request)
    if not token:
        return None
    try:
        user = get_user_by_auth_token(token)
    except Exception:
        return None
    return None if getattr(user, 'is_banned', False) else user


def _page(request, status, **ctx):
    resp = render(request, 'web/desktop_auth.html', dict(ctx), status=status)
    resp['Referrer-Policy'] = 'no-referrer'
    resp['X-Frame-Options'] = 'DENY'          # a consent page must never be framed (clickjacking)
    return resp


@never_cache
@require_http_methods(['GET', 'POST'])
def desktop_auth_page(request):
    state = request.GET.get('state') or request.POST.get('state') or ''
    rec = desktop_auth.peek(state)
    if not rec or rec.get('status') != 'pending':
        return _page(request, 410, mode='expired')

    user = _signed_in_user(request)
    if user is None:
        # Reuse the normal web login (Google / GitHub / email) and come straight back here.
        back = f"{reverse('web:desktop_auth')}?state={quote(state)}"
        return redirect(f"{reverse('web:login')}?next={quote(back)}")

    if request.method == 'POST':
        if request.POST.get('decision') == 'allow' and desktop_auth.approve(state, user.pk):
            return _page(request, 200, mode='done', username=user.username)
        desktop_auth.deny(state)
        return _page(request, 200, mode='denied')

    return _page(request, 200, mode='confirm', state=state, device=rec.get('device'),
                 username=user.username, display_name=getattr(user, 'display_name', '') or user.username,
                 photo_url=getattr(user, 'photo_url', '') or '')
