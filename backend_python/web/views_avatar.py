"""Blobatar avatar endpoint and the "My Avatar" username/avatar page."""
import json
import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from api.blobatar import blobatar as render_blobatar
from api.blobatar.expression import EXPRESSIONS
from api.models import User
from api.services import (
    avatar_options_for,
    record_username_change,
    save_avatar_customization,
    username_change_status,
    validate_username_change,
)

from .view_helpers import (
    _blobatar_url_for,
    _clear_page_cache,
    _ctx,
    _rate_limit,
    _get_user_id,
    api,
)

AVATAR_CACHE = "public, max-age=86400, stale-while-revalidate=2592000"
AVATAR_SECURITY = {
    "content-security-policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
    "x-content-type-options": "nosniff",
    "access-control-allow-origin": "*",
}
USAGE = (
    "blobatar avatar generator — v2.0.0 (10 shapes, 14 expressions)\n\n"
    "GET /avatar/<name>/?size=256&background=circle&hue=200&tone=0.6&anim=bob&title=hi\n"
    "  size|s       integer 8-1024 (square output)\n"
    "  background   square|circle|squircle (default: none)\n"
    "  hue          integer 0-360\n"
    "  tone         float 0-1\n"
    "  anim         bob|wave|spin|pulse (SMIL animation, works in <img>)\n"
    "  title        string (max 128 chars)\n"
    "  expression   idle|happy|sad|mad|surprised|wink|sleepy|smug|unsure|scared|love|shy|sick|thinking\n"
    "  shape        round|organic|boxy|capsule|nub|cloud|droplet|hexagon|sun|triangle\n"
    "  color        #rrggbb (head color override)\n"
    "  bgcolor      #rrggbb (background color override)\n"
    "  eyecolor     #rrggbb (eye color override)\n"
)

SHAPE_TRAITS = {
    'round': 0.11, 'organic': 0.35, 'boxy': 0.54, 'capsule': 0.65,
    'nub': 0.745, 'cloud': 0.825, 'droplet': 0.8875, 'hexagon': 0.9325,
    'sun': 0.965, 'triangle': 0.99,
}

_EXPRESSIONS = sorted(EXPRESSIONS.keys())

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
_HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')


def _base36(n):
    if n == 0:
        return "0"
    out = []
    while n:
        n, r = divmod(n, 36)
        out.append(_DIGITS[r])
    return ''.join(reversed(out))


def _etag(body):
    h = 0x811C9DC5
    for ch in body:
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return '"%s"' % _base36(h)


def _clamp(value, lo, hi):
    return max(lo, min(hi, value))


def _parse_options(params):
    opts = {}
    raw_size = params.get('size') or params.get('s')
    if raw_size is not None:
        try:
            opts['size'] = _clamp(int(raw_size), 8, 1024)
        except (TypeError, ValueError):
            raise ValueError('size must be an integer between 8 and 1024')
    bg = params.get('background')
    if bg is not None:
        if bg not in ('none', 'square', 'circle', 'squircle'):
            raise ValueError('background must be one of: none, square, circle, squircle')
        opts['background'] = False if bg == 'none' else bg
    anim = params.get('anim')
    if anim is not None:
        if anim not in ('bob', 'wave', 'spin', 'pulse'):
            raise ValueError('anim must be one of: bob, wave, spin, pulse')
        opts['anim'] = anim
    hue = params.get('hue')
    if hue is not None:
        try:
            opts['hue'] = _clamp(int(hue), 0, 360)
        except (TypeError, ValueError):
            raise ValueError('hue must be an integer between 0 and 360')
    tone = params.get('tone')
    if tone is not None:
        try:
            opts['tone'] = _clamp(float(tone), 0.0, 1.0)
        except (TypeError, ValueError):
            raise ValueError('tone must be a number between 0 and 1')
    title = params.get('title')
    if title is not None:
        opts['title'] = title[:128]
    expression = params.get('expression')
    if expression is not None:
        if expression not in _EXPRESSIONS:
            raise ValueError('expression must be one of: ' + ', '.join(_EXPRESSIONS))
        opts['expression'] = expression
    shape = params.get('shape')
    if shape is not None:
        if shape not in SHAPE_TRAITS:
            raise ValueError('shape must be one of: ' + ', '.join(sorted(SHAPE_TRAITS)))
        traits = opts.setdefault('traits', {})
        traits['shape'] = SHAPE_TRAITS[shape]
    for param, field in (('color', 'head'), ('bgcolor', 'bg'), ('eyecolor', 'eye')):
        value = params.get(param)
        if value is not None:
            if not _HEX_RE.match(value):
                raise ValueError('%s must be a hex color like #a1b2c3' % param)
            palette = opts.setdefault('palette', {})
            palette[field] = value.lower()
    return opts


@require_GET
def avatar_svg_index(request):
    return HttpResponse(USAGE, content_type='text/plain; charset=utf-8')


@require_GET
def avatar_svg(request, name):
    if not name or len(name) > 200:
        return HttpResponse('name too long (max 200 chars)', status=400,
                            content_type='text/plain; charset=utf-8')
    try:
        opts = _parse_options(request.GET)
    except ValueError as e:
        return HttpResponse(str(e), status=400, content_type='text/plain; charset=utf-8')
    body = render_blobatar(name, opts)
    headers = {
        'content-type': 'image/svg+xml; charset=utf-8',
        'cache-control': AVATAR_CACHE,
        'etag': _etag(body),
    }
    headers.update(AVATAR_SECURITY)
    if request.headers.get('if-none-match') == headers['etag']:
        return HttpResponse(status=304, headers=headers)
    return HttpResponse(body, headers=headers)


def _session_user_dict(db_user):
    return {
        'id': db_user.id,
        'username': db_user.username,
        'display_name': db_user.display_name or db_user.username,
        'role': db_user.role,
        'photo_url': db_user.photo_url or '',
        'email_verified': db_user.email_verified,
        'banner_url': db_user.banner_url or '',
        'is_admin': db_user.is_admin,
        'moderator_level': db_user.moderator_level,
        'verification_level': db_user.verification_level,
        'teacher_verified': db_user.teacher_verified,
        'institution_verified': db_user.institution_verified,
        'is_bot': db_user.is_bot,
        'avatar_bg': db_user.avatar_bg,
        'avatar_hue': db_user.avatar_hue,
        'avatar_tone': db_user.avatar_tone,
        'avatar_anim': db_user.avatar_anim,
        'avatar_shape': db_user.avatar_shape,
        'avatar_expression': db_user.avatar_expression,
        'avatar_color': db_user.avatar_color,
        'avatar_bg_color': db_user.avatar_bg_color,
        'avatar_eye_color': db_user.avatar_eye_color,
        'avatar_use_pp': db_user.avatar_use_pp,
    }


def my_avatar(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('%s?next=%s' % (reverse('web:login'), request.get_full_path()))
    session_user = api.get_session_user(request)
    if not session_user:
        return redirect('%s?next=%s' % (reverse('web:login'), request.get_full_path()))
    try:
        db_user = User.objects.get(pk=session_user.get('id'))
    except User.DoesNotExist:
        return redirect('%s?next=%s' % (reverse('web:login'), request.get_full_path()))
    if not getattr(db_user, 'email_verified', False):
        return redirect('%s?next=%s' % (reverse('web:login'), request.get_full_path()))
    status = username_change_status(db_user)
    prefs = avatar_options_for(db_user)
    return render(request, 'web/my_avatar.html', _ctx(request,
        avatar_status=status,
        avatar_status_json=json.dumps(status),
        avatar_main_url=_blobatar_url_for(db_user),
        avatar_prefs=prefs,
        avatar_prefs_json=json.dumps(prefs),
        avatar_raw=json.dumps({
            'bg': db_user.avatar_bg,
            'hue': db_user.avatar_hue,
            'tone': db_user.avatar_tone,
            'anim': db_user.avatar_anim,
            'shape': db_user.avatar_shape,
            'expression': db_user.avatar_expression,
            'color': db_user.avatar_color,
            'bgcolor': db_user.avatar_bg_color,
            'eyecolor': db_user.avatar_eye_color,
            'use_pp': db_user.avatar_use_pp,
        }),
        has_photo=bool(db_user.photo_url),
        avatar_use_pp=db_user.avatar_use_pp,
        has_avatar_changed=request.GET.get('changed') == '1',
    ))


@require_POST
def ajax_avatar_change_username(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'avatar_username', 10, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        db_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if not getattr(db_user, 'email_verified', False):
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        payload = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        payload = {}
    username = str(payload.get('username', '') or '').strip()
    err, code = validate_username_change(db_user, username)
    if err:
        return JsonResponse(err, status=code)
    db_user.username = username
    record_username_change(db_user)
    db_user.save()
    _clear_page_cache()
    token = api.get_session_token(request)
    user_data = dict(api.get_session_user(request) or {})
    user_data.update(_session_user_dict(db_user))
    api.set_session_auth(request, token, user_data)
    status = username_change_status(db_user)
    return JsonResponse({
        'status': 'success',
        'username': db_user.username,
        'avatarUrl': _blobatar_url_for(db_user),
        'changeCount': status['change_count'],
        'nextChangeAt': status['next_change_at'],
        'cooldownDays': status['cooldown_days'],
    })


@require_POST
def ajax_avatar_customize(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'avatar_customize', 20, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        db_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        payload = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        payload = {}
    result, code = save_avatar_customization(db_user, payload)
    if isinstance(result, dict) and 'error' in result:
        return JsonResponse(result, status=code)
    _clear_page_cache()
    token = api.get_session_token(request)
    user_data = dict(api.get_session_user(request) or {})
    user_data.update(_session_user_dict(db_user))
    api.set_session_auth(request, token, user_data)
    return JsonResponse({
        'status': 'success',
        'avatarUrl': _blobatar_url_for(db_user),
    })