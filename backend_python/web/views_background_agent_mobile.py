from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.http import require_http_methods

from api.background_agent.mobile_auth import approve_pairing
from api.models import BackgroundAgentDevicePairing
from api.utils import now_ms
from web.background_agent_auth import get_bg_admin, require_bg_admin


@require_http_methods(['GET', 'POST'])
def background_agent_mobile_authorize(request):
    redirect_response = require_bg_admin(request)
    if redirect_response:
        next_url = reverse('web:background_agent_mobile_authorize')
        code = (request.GET.get('code') or request.POST.get('code') or '').strip()
        if code:
            next_url += '?code=' + code
        return redirect(reverse('web:background_agent_login') + '?' + urlencode({'next': next_url}))
    code = (request.GET.get('code') or request.POST.get('code') or '').strip().upper()
    pairing = BackgroundAgentDevicePairing.objects.filter(user_code=code).first() if code else None
    approved = False
    error = ''
    if request.method == 'POST':
        if not pairing:
            error = 'That authorization code is not valid.'
        else:
            try:
                approve_pairing(pairing, get_bg_admin(request))
                approved = True
                messages.success(request, 'Zeus is authorized. Return to the app to continue.')
            except ValueError as exc:
                error = str(exc)
    elif pairing and pairing.expires_at <= now_ms():
        error = 'This authorization request has expired.'
    return render(request, 'background_agent/mobile_authorize.html', {
        'csp_nonce': getattr(request, 'csp_nonce', ''),
        'bg_admin': get_bg_admin(request),
        'code': code,
        'pairing': pairing,
        'approved': approved,
        'error': error,
    })
