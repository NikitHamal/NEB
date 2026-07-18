from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import string
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse

from api.models import BackgroundAgentDevicePairing, BackgroundAgentDeviceToken
from api.utils import now_ms, uuid_str

PAIR_TTL_MS = 10 * 60 * 1000
TOKEN_PREFIX = 'nba_'
USER_CODE_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def token_hash(value: str) -> str:
    return hmac.new(
        str(settings.SECRET_KEY).encode('utf-8'),
        value.encode('utf-8'),
        hashlib.sha256,
    ).hexdigest()


def create_pairing(device_name: str) -> tuple[BackgroundAgentDevicePairing, str]:
    now = now_ms()
    raw_device_code = secrets.token_urlsafe(48)
    pairing = BackgroundAgentDevicePairing.objects.create(
        id=uuid_str(),
        device_code_hash=token_hash(raw_device_code),
        user_code=_new_user_code(),
        device_name=_clean_device_name(device_name),
        status='pending',
        created_at=now,
        expires_at=now + PAIR_TTL_MS,
    )
    return pairing, raw_device_code


def approve_pairing(pairing: BackgroundAgentDevicePairing, admin_user) -> BackgroundAgentDevicePairing:
    now = now_ms()
    if pairing.expires_at <= now:
        pairing.status = 'expired'
        pairing.save(update_fields=['status'])
        raise ValueError('This authorization request has expired')
    if pairing.status not in {'pending', 'approved'}:
        raise ValueError('This authorization request is no longer available')
    pairing.admin_user = admin_user
    pairing.status = 'approved'
    pairing.approved_at = now
    pairing.save(update_fields=['admin_user', 'status', 'approved_at'])
    return pairing


def exchange_pairing(device_code: str) -> tuple[str, BackgroundAgentDeviceToken] | None:
    hashed = token_hash(device_code)
    now = now_ms()
    with transaction.atomic():
        pairing = BackgroundAgentDevicePairing.objects.select_for_update().filter(device_code_hash=hashed).first()
        if not pairing:
            raise ValueError('Invalid device code')
        pairing.poll_count += 1
        pairing.last_polled_at = now
        if pairing.expires_at <= now:
            pairing.status = 'expired'
            pairing.save(update_fields=['poll_count', 'last_polled_at', 'status'])
            raise ValueError('Authorization request expired')
        if pairing.status == 'pending':
            pairing.save(update_fields=['poll_count', 'last_polled_at'])
            return None
        if pairing.status == 'denied':
            pairing.save(update_fields=['poll_count', 'last_polled_at'])
            raise PermissionError('Authorization request denied')
        if pairing.status != 'approved' or not pairing.admin_user_id:
            raise ValueError('Authorization request already consumed')
        raw_token = TOKEN_PREFIX + secrets.token_urlsafe(48)
        device = BackgroundAgentDeviceToken.objects.create(
            id=uuid_str(),
            admin_user=pairing.admin_user,
            token_hash=token_hash(raw_token),
            device_name=pairing.device_name,
            created_at=now,
            last_used_at=now,
        )
        pairing.status = 'consumed'
        pairing.consumed_at = now
        pairing.save(update_fields=['status', 'consumed_at', 'poll_count', 'last_polled_at'])
        return raw_token, device


def authenticate_device(request):
    header = request.headers.get('Authorization', '')
    if not header.lower().startswith('bearer '):
        return None
    raw = header.split(' ', 1)[1].strip()
    if not raw.startswith(TOKEN_PREFIX) or len(raw) < 32:
        return None
    now = now_ms()
    device = BackgroundAgentDeviceToken.objects.select_related('admin_user').filter(token_hash=token_hash(raw)).first()
    if not device or device.revoked_at or (device.expires_at and device.expires_at <= now):
        return None
    admin = device.admin_user
    if not admin.is_admin or admin.is_locked or admin.is_bot:
        return None
    if now - device.last_used_at >= 60_000:
        BackgroundAgentDeviceToken.objects.filter(pk=device.pk).update(last_used_at=now)
        device.last_used_at = now
    return device


def require_device(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        device = authenticate_device(request)
        if not device:
            response = JsonResponse({'ok': False, 'error': 'Device authorization required', 'code': 'unauthorized'}, status=401)
            response['Cache-Control'] = 'no-store, private'
            response['Pragma'] = 'no-cache'
            return response
        request.background_agent_device = device
        request.background_agent_admin = device.admin_user
        return view(request, *args, **kwargs)
    return wrapped


def json_body(request) -> dict:
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError('Invalid JSON request body') from exc


def pairing_rate_allowed(request) -> bool:
    forwarded = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    address = forwarded or request.META.get('REMOTE_ADDR', 'unknown')
    key = 'bg-mobile-pair:' + hashlib.sha256(address.encode('utf-8')).hexdigest()
    try:
        return cache.add(key, '1', timeout=8)
    except Exception:
        return True


def _new_user_code() -> str:
    for _ in range(20):
        value = ''.join(secrets.choice(USER_CODE_ALPHABET) for _ in range(8))
        code = f'{value[:4]}-{value[4:]}'
        if not BackgroundAgentDevicePairing.objects.filter(user_code=code).exists():
            return code
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))


def _clean_device_name(value: str) -> str:
    cleaned = ' '.join((value or 'Zeus').strip().split())
    return cleaned[:120] or 'Zeus'
