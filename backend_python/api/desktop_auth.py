"""Browser hand-off sign-in for the NEBians desktop app (PKCE-style).

Why this exists
---------------
A desktop binary cannot hold an OAuth client secret and cannot receive a
custom-scheme deep link reliably on every OS. The website, on the other hand,
already signs people in with Google, GitHub and email. So the desktop app asks
the *website* to vouch for the user:

    desktop                          backend                         browser
    -------                          -------                         -------
    verifier = random(32 bytes)
    challenge = b64url(sha256(verifier))
    POST /api/auth/desktop/start/ -> state, loginUrl
    open loginUrl  ----------------------------------------------->  /desktop-auth/?state=...
                                                                      (signs in with Google / GitHub / email
                                                                       using the normal web login, then taps
                                                                       "Allow")
                                     record[state] = approved(user)  <- POST /desktop-auth/
    POST /api/auth/desktop/poll/ {state, verifier}
       -> sha256(verifier) must match challenge, record is deleted (one use)
       -> a *fresh* bearer token is minted for the desktop session

Security properties
-------------------
* The bearer token never appears in a URL, a redirect, the browser, or the cache.
  Only the user id is parked in the cache, and only after an authenticated,
  CSRF-protected POST from the signed-in web session.
* Whoever opens the browser cannot collect the token: collecting it needs the
  `verifier`, which never leaves the desktop process (an observer of the login
  URL only ever sees `state`).
* `state` is 256 bits of entropy, valid for 10 minutes, consumed on first
  successful poll, and approval can only be performed once.
* Polling is throttled and verifier comparison is constant-time.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import re
import secrets
import time

from django.core.cache import cache

TTL_SECONDS = 600
POLL_INTERVAL_SECONDS = 2
_KEY = 'desktop_auth:v1:%s'
_STATE_RE = re.compile(r'^[A-Za-z0-9_-]{32,64}$')
_CHALLENGE_RE = re.compile(r'^[A-Za-z0-9_-]{43}$')          # b64url(sha256) has no padding
_VERIFIER_RE = re.compile(r'^[A-Za-z0-9_\-.~]{43,128}$')     # RFC 7636 charset/length
_DEVICE_RE = re.compile(r'[^\w .()\-]+')


def valid_state(state: str) -> bool:
    return bool(isinstance(state, str) and _STATE_RE.match(state))


def challenge_for(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')


def clean_device_name(raw) -> str:
    text = _DEVICE_RE.sub('', str(raw or ''))[:60].strip()
    return text or 'NEBians Desktop'


def create_request(challenge: str, device: str) -> str | None:
    """Park a pending request. Returns the state id or None for a malformed challenge."""
    if not isinstance(challenge, str) or not _CHALLENGE_RE.match(challenge):
        return None
    state = secrets.token_urlsafe(32)
    cache.set(_KEY % state, {
        'status': 'pending',
        'challenge': challenge,
        'device': clean_device_name(device),
        'created': int(time.time()),
    }, TTL_SECONDS)
    return state


def peek(state: str) -> dict | None:
    if not valid_state(state):
        return None
    rec = cache.get(_KEY % state)
    return rec if isinstance(rec, dict) else None


def approve(state: str, user_pk: str) -> bool:
    """Mark a pending request approved for `user_pk`. Idempotent-hostile: only pending -> approved."""
    rec = peek(state)
    if not rec or rec.get('status') != 'pending':
        return False
    remaining = max(30, TTL_SECONDS - (int(time.time()) - rec.get('created', 0)))
    rec = dict(rec, status='approved', user_pk=str(user_pk))
    cache.set(_KEY % state, rec, remaining)
    return True


def deny(state: str) -> None:
    if valid_state(state):
        cache.delete(_KEY % state)


def redeem(state: str, verifier: str):
    """Returns ('pending'|'invalid'|'ok', user_pk|None). Consumes an approved record."""
    if not valid_state(state) or not isinstance(verifier, str) or not _VERIFIER_RE.match(verifier):
        return 'invalid', None
    rec = peek(state)
    if not rec:
        return 'invalid', None
    if not hmac.compare_digest(challenge_for(verifier), rec.get('challenge', '')):
        return 'invalid', None
    if rec.get('status') != 'approved':
        return 'pending', None
    cache.delete(_KEY % state)
    return 'ok', rec.get('user_pk')
