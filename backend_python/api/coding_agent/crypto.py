"""At-rest encryption for retained GitHub OAuth tokens.

Same AES-GCM pattern as `api.background_agent.crypto`, with its own
associated-data domain so coding-agent tokens can never be swapped with
other credential types. Stored values look like ``v1:<base64>``; rows
written before encryption read back via the plaintext fallback in
``read_project_token`` until the data migration encrypts them.
"""
from __future__ import annotations

import base64
import hashlib

from Crypto.Cipher import AES
from django.conf import settings

_VERSION = 'v1'
_ASSOCIATED_DATA = b'nebians-coding-agent-github-token'


def _key() -> bytes:
    material = f"{settings.SECRET_KEY}|coding-agent-token-v1".encode('utf-8')
    return hashlib.sha256(material).digest()


def encrypt_token(value: str) -> str:
    if not value:
        return ''
    cipher = AES.new(_key(), AES.MODE_GCM)
    cipher.update(_ASSOCIATED_DATA)
    ciphertext, tag = cipher.encrypt_and_digest(value.encode('utf-8'))
    payload = cipher.nonce + tag + ciphertext
    return f"{_VERSION}:{base64.urlsafe_b64encode(payload).decode('ascii')}"


def _decrypt(value: str) -> str:
    version, encoded = value.split(':', 1)
    if version != _VERSION:
        raise ValueError('Unsupported encrypted token version')
    payload = base64.urlsafe_b64decode(encoded.encode('ascii'))
    nonce, tag, ciphertext = payload[:16], payload[16:32], payload[32:]
    cipher = AES.new(_key(), AES.MODE_GCM, nonce=nonce)
    cipher.update(_ASSOCIATED_DATA)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')


def read_project_token(project) -> str:
    """Return the raw GitHub token for a project row.

    Decrypts ``v1:`` ciphertext; falls back to plaintext for rows written
    before encryption (removed once the backfill migration has run
    everywhere — kept tolerant so a missed row fails safe, not loud).
    """
    raw = project.access_token or ''
    if not raw:
        return ''
    if raw.startswith(f'{_VERSION}:'):
        return _decrypt(raw)
    return raw


def store_project_token(project, raw_token: str) -> None:
    """Encrypt `raw_token` into `project.access_token` (in memory; caller saves)."""
    project.access_token = encrypt_token(raw_token or '')
