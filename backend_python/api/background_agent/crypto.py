"""Small authenticated-encryption helper for retained OAuth credentials."""
from __future__ import annotations

import base64
import hashlib

from Crypto.Cipher import AES
from django.conf import settings

_VERSION = 'v1'
_ASSOCIATED_DATA = b'nebians-background-agent-github-token'


def _key() -> bytes:
    material = f"{settings.SECRET_KEY}|background-agent-token-v1".encode('utf-8')
    return hashlib.sha256(material).digest()


def encrypt_secret(value: str) -> str:
    if not value:
        return ''
    cipher = AES.new(_key(), AES.MODE_GCM)
    cipher.update(_ASSOCIATED_DATA)
    ciphertext, tag = cipher.encrypt_and_digest(value.encode('utf-8'))
    payload = cipher.nonce + tag + ciphertext
    return f"{_VERSION}:{base64.urlsafe_b64encode(payload).decode('ascii')}"


def decrypt_secret(value: str) -> str:
    if not value:
        return ''
    try:
        version, encoded = value.split(':', 1)
        if version != _VERSION:
            raise ValueError('Unsupported encrypted secret version')
        payload = base64.urlsafe_b64decode(encoded.encode('ascii'))
        nonce, tag, ciphertext = payload[:16], payload[16:32], payload[32:]
        cipher = AES.new(_key(), AES.MODE_GCM, nonce=nonce)
        cipher.update(_ASSOCIATED_DATA)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception as exc:
        raise ValueError('Unable to decrypt stored GitHub credential') from exc
