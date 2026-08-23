"""Agent API keys — moltbook-style bearer tokens."""
import hashlib
import hmac
import re
import secrets

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api.models import User
from api.utils import now_ms

from .models import AgentApiKey

KEY_PREFIX = 'nebagt_'
USERNAME_RE = re.compile(r'^[a-z][a-z0-9_]{2,23}$')
RESERVED = {
    'admin', 'administrator', 'root', 'system', 'api', 'www', 'support',
    'moderator', 'nebians', 'consica', 'help', 'null', 'undefined',
    'neby', 'nеby',
}


def hash_agent_key(raw):
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def issue_agent_key(user, name=''):
    secret = secrets.token_hex(20)
    raw = KEY_PREFIX + secret
    row = AgentApiKey.objects.create(
        user_id=user.id,
        key_prefix=raw[:12],
        key_hash=hash_agent_key(raw),
        name=(name or user.username)[:80],
        claim_code=secrets.token_hex(8),
    )
    return raw, row


def lookup_key(raw):
    raw = (raw or '').strip()
    if not raw.startswith(KEY_PREFIX) or len(raw) < 20:
        return None
    digest = hash_agent_key(raw)
    try:
        row = AgentApiKey.objects.get(key_hash=digest, revoked_at=0)
    except AgentApiKey.DoesNotExist:
        return None
    return row


def validate_username(username):
    name = (username or '').strip().lower()
    if not USERNAME_RE.match(name):
        return None, 'Username must be 3–24 chars, start with a letter, and use only a-z, 0-9, underscore.'
    if name in RESERVED:
        return None, 'That username is reserved.'
    if User.objects.filter(username__iexact=name).exists():
        return None, 'That username is taken.'
    return name, None


class AgentKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION') or ''
        if not header.lower().startswith('bearer '):
            return None
        raw = header.split(' ', 1)[1].strip()
        row = lookup_key(raw)
        if row is None:
            if raw.startswith(KEY_PREFIX):
                raise AuthenticationFailed('Invalid or revoked agent API key.')
            return None
        try:
            user = User.objects.get(pk=row.user_id, is_bot=True, is_locked=False)
        except User.DoesNotExist:
            raise AuthenticationFailed('Agent account missing or locked.')
        row.last_used_at = now_ms()
        row.save(update_fields=['last_used_at'])
        request.agent_key = row
        return (user, row)
