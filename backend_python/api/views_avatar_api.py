"""Mobile API for avatar customization — GET current style, POST update.

Mounted at /api/users/me/avatar/ and /api/users/me/avatar/customize/.
Uses the same _require_user helper as the rest of the users module so both
Bearer-token (Android) and session-cookie (web) clients work.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import avatar_options_for, avatar_url_for, save_avatar_customization
from .view_helpers import _require_user


@api_view(['GET'])
def avatar_style_get(request):
    user, err = _require_user(request)
    if err:
        return err
    opts = avatar_options_for(user)
    return Response({
        'avatar_url': avatar_url_for(user),
        'avatarUrl': avatar_url_for(user),
        'avatar_use_pp': bool(getattr(user, 'avatar_use_pp', False)),
        'style': opts,
        'raw': {
            'hue': getattr(user, 'avatar_hue', -1),
            'tone': getattr(user, 'avatar_tone', -1.0),
            'bg': getattr(user, 'avatar_bg', '') or '',
            'anim': getattr(user, 'avatar_anim', '') or '',
            'shape': getattr(user, 'avatar_shape', '') or '',
            'expression': getattr(user, 'avatar_expression', '') or '',
            'color': getattr(user, 'avatar_color', '') or '',
            'bgcolor': getattr(user, 'avatar_bg_color', '') or '',
            'eyecolor': getattr(user, 'avatar_eye_color', '') or '',
            'use_pp': bool(getattr(user, 'avatar_use_pp', False)),
        }
    })


@api_view(['POST'])
def avatar_style_update(request):
    user, err = _require_user(request)
    if err:
        return err
    payload = request.data if isinstance(request.data, dict) else {}
    norm = {}
    for k in ('background', 'bg', 'anim', 'shape', 'expression', 'color',
              'bgcolor', 'eyecolor', 'eyeColor', 'use_pp', 'hue', 'tone'):
        if k in payload:
            norm[k] = payload[k]
    if 'bg' in norm and 'background' not in norm:
        norm['background'] = norm.pop('bg')
    if 'eyeColor' in norm and 'eyecolor' not in norm:
        norm['eyecolor'] = norm.pop('eyeColor')
    result, code = save_avatar_customization(user, norm)
    if code != 200:
        return Response(result, status=code)
    url = avatar_url_for(user)
    return Response({
        'status': 'success',
        'avatar_url': url,
        'avatarUrl': url,
        'style': result,
        'avatar_use_pp': bool(getattr(user, 'avatar_use_pp', False)),
    })
