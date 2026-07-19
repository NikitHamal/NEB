"""At-rest encryption for user-supplied LLM API keys.

Same AES-GCM pattern as `api.background_agent.crypto`, with its own
associated-data domain so LLM keys can never be swapped with GitHub tokens.
"""
from __future__ import annotations

import base64
import hashlib

from Crypto.Cipher import AES
from django.conf import settings

_VERSION = 'v1'
_ASSOCIATED_DATA = b'nebians-llm-provider-key'


def _key() -> bytes:
    material = f"{settings.SECRET_KEY}|llm-provider-key-v1".encode('utf-8')
    return hashlib.sha256(material).digest()


def encrypt_key(value: str) -> str:
    if not value:
        return ''
    cipher = AES.new(_key(), AES.MODE_GCM)
    cipher.update(_ASSOCIATED_DATA)
    ciphertext, tag = cipher.encrypt_and_digest(value.encode('utf-8'))
    payload = cipher.nonce + tag + ciphertext
    return f"{_VERSION}:{base64.urlsafe_b64encode(payload).decode('ascii')}"


def decrypt_key(value: str) -> str:
    if not value:
        return ''
    try:
        version, encoded = value.split(':', 1)
        if version != _VERSION:
            raise ValueError('Unsupported encrypted LLM key version')
        payload = base64.urlsafe_b64decode(encoded.encode('ascii'))
        nonce, tag, ciphertext = payload[:16], payload[16:32], payload[32:]
        cipher = AES.new(_key(), AES.MODE_GCM, nonce=nonce)
        cipher.update(_ASSOCIATED_DATA)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception as exc:
        raise ValueError('Unable to decrypt stored LLM API key') from exc


def mask_key(plain: str) -> str:
    """Display-safe representation, e.g. 'sk-…wxyz'."""
    plain = (plain or '').strip()
    if not plain:
        return ''
    if len(plain) <= 7:
        return '•' * len(plain)
    return f"{plain[:3]}…{plain[-4:]}"
