import secrets

from django.core.cache import cache


CODE_TTL_SECONDS = 120
_PAYLOAD_PREFIX = 'mobile_oauth:payload:'
_CLAIM_PREFIX = 'mobile_oauth:claimed:'


def issue_mobile_oauth_code(auth_token, is_new_user, username, profile_complete=None):
    code = secrets.token_urlsafe(32)
    payload = {
        'authToken': auth_token,
        'isNewUser': bool(is_new_user),
        'username': username or '',
    }
    if profile_complete is not None:
        payload['profileComplete'] = bool(profile_complete)
    cache.set(f'{_PAYLOAD_PREFIX}{code}', payload, CODE_TTL_SECONDS)
    return code


def exchange_mobile_oauth_code(code):
    normalized = str(code or '').strip()
    if not normalized:
        return None
    if not cache.add(f'{_CLAIM_PREFIX}{normalized}', True, CODE_TTL_SECONDS):
        return None
    payload_key = f'{_PAYLOAD_PREFIX}{normalized}'
    payload = cache.get(payload_key)
    cache.delete(payload_key)
    return payload
