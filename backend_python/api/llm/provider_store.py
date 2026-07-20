"""Shared storage + validation logic for user LLM providers (BYOK + custom).

Both the Zeus mobile API (device-token auth) and the NEBians website settings
UI (session auth) delegate here so create/update/delete/test behavior stays
identical across clients. API keys are AES-GCM encrypted at rest and only
ever returned masked — never round-tripped.
"""
from __future__ import annotations

import json
import logging

from api.llm.client import LLMError, quick_test
from api.llm.credentials import resolve
from api.llm.crypto import encrypt_key, mask_key, decrypt_key
from api.llm.registry import preset
from api.models import UserLLMProvider
from api.utils import now_ms, uuid_str

logger = logging.getLogger(__name__)

VALID_FORMATS = ('openai', 'anthropic', 'gemini')


def err(message, code='request_failed'):
    return {'ok': False, 'error': str(message), 'code': code}


def row_payload(row) -> dict:
    """Public shape of a saved provider row (key masked only)."""
    try:
        models = json.loads(row.models_json or '[]')
    except (ValueError, TypeError):
        models = []
    masked = ''
    if row.api_key:
        try:
            masked = mask_key(decrypt_key(row.api_key))
        except Exception:
            masked = 'set'
    return {
        'id': str(row.id),
        'name': row.name or '',
        'provider': row.provider,
        'apiFormat': row.api_format,
        'baseUrl': row.base_url,
        'keyMasked': masked,
        'keySet': bool(row.api_key),
        'models': [str(m) for m in models if str(m).strip()],
        'defaultModel': row.default_model,
        'contextWindow': row.context_window,
        'maxOutputTokens': row.max_output_tokens,
        'enabled': row.enabled,
        'updatedAt': row.updated_at,
    }


def list_providers(user) -> list:
    rows = UserLLMProvider.objects.filter(user=user).order_by('-updated_at')
    return [row_payload(r) for r in rows]


def get_row(user, provider_id):
    return UserLLMProvider.objects.filter(pk=provider_id, user=user).first()


def create_provider(user, payload: dict):
    """Create a custom provider or upsert a preset BYOK key.

    Returns ``(data, http_status)`` — data is the public JSON dict.
    """
    provider = (payload.get('provider') or '').strip().lower()

    if provider == 'custom':
        name = (payload.get('name') or '').strip()[:100] or 'Custom provider'
        api_format = (payload.get('apiFormat') or 'openai').strip().lower()
        if api_format not in VALID_FORMATS:
            return err('apiFormat must be openai, anthropic or gemini'), 400
        base_url = (payload.get('baseUrl') or '').strip()
        if not base_url.startswith(('http://', 'https://')):
            return err('Base URL must start with http:// or https://'), 400
        models = [str(m).strip() for m in (payload.get('models') or []) if str(m).strip()][:40]
        default_model = (payload.get('defaultModel') or (models[0] if models else '')).strip()[:200]
        if not default_model:
            return err('Add at least one model id for this provider'), 400
        key_plain = (payload.get('apiKey') or '').strip()
        try:
            context_window = max(1024, min(int(payload.get('contextWindow') or 131072), 2_000_000))
            max_output = max(256, min(int(payload.get('maxOutputTokens') or 4096), 128000))
        except (TypeError, ValueError):
            return err('contextWindow / maxOutputTokens must be numbers'), 400
        row = UserLLMProvider.objects.create(
            id=uuid_str(), user=user, name=name, provider='custom',
            api_format=api_format, base_url=base_url,
            api_key=encrypt_key(key_plain) if key_plain else '',
            models_json=json.dumps(models), default_model=default_model,
            context_window=context_window, max_output_tokens=max_output,
            enabled=True, created_at=now_ms(), updated_at=now_ms(),
        )
        return {'ok': True, 'provider': row_payload(row)}, 201

    # Preset BYOK: store/replace the user's own key for a known provider.
    p = preset(provider)
    if not p or not p.official:
        return err('Unknown provider. Use agnes, openai, anthropic, gemini, deepseek — or custom.'), 400
    key_plain = (payload.get('apiKey') or '').strip()
    if not key_plain:
        return err(f'An API key is required for {p.label}'), 400
    default_model = (payload.get('defaultModel') or '').strip()[:200]
    base_url = (payload.get('baseUrl') or '').strip()
    if base_url and not base_url.startswith(('http://', 'https://')):
        return err('Base URL must start with http:// or https://'), 400
    row = UserLLMProvider.objects.filter(user=user, provider=p.slug).first()
    now = now_ms()
    if row is None:
        row = UserLLMProvider(
            id=uuid_str(), user=user, provider=p.slug, name=p.label,
            api_format=p.format, created_at=now,
        )
    row.api_key = encrypt_key(key_plain)
    if default_model:
        row.default_model = default_model
    elif not row.default_model:
        row.default_model = p.default_model
    if base_url:
        row.base_url = base_url
    row.context_window = p.context_window
    row.max_output_tokens = p.max_output_tokens
    row.enabled = True
    row.updated_at = now
    row.save()
    return {'ok': True, 'provider': row_payload(row)}, 201


def update_provider(row, payload: dict):
    """Patch a saved row. Key fields only ever change when new values arrive.
    Returns ``(data, http_status)``."""
    changed = []
    if 'name' in payload and row.provider == 'custom':
        row.name = (payload.get('name') or '').strip()[:100] or row.name
        changed.append('name')
    if 'apiFormat' in payload and row.provider == 'custom':
        fmt = (payload.get('apiFormat') or '').strip().lower()
        if fmt in VALID_FORMATS:
            row.api_format = fmt
            changed.append('api_format')
    if 'baseUrl' in payload:
        url = (payload.get('baseUrl') or '').strip()
        if url and not url.startswith(('http://', 'https://')):
            return err('Base URL must start with http:// or https://'), 400
        # Allowed on preset rows too, so proxies/gateways can override a
        # preset's default endpoint without re-entering the key.
        row.base_url = url
        changed.append('base_url')
    if 'apiKey' in payload:
        key_plain = (payload.get('apiKey') or '').strip()
        row.api_key = encrypt_key(key_plain) if key_plain else ''
        changed.append('api_key')
    if 'models' in payload and row.provider == 'custom':
        models = [str(m).strip() for m in (payload.get('models') or []) if str(m).strip()][:40]
        row.models_json = json.dumps(models)
        changed.append('models_json')
    if 'defaultModel' in payload:
        row.default_model = (payload.get('defaultModel') or '').strip()[:200]
        changed.append('default_model')
    if 'enabled' in payload:
        row.enabled = bool(payload.get('enabled'))
        changed.append('enabled')
    if changed:
        row.updated_at = now_ms()
        row.save(update_fields=changed + ['updated_at'])
    return {'ok': True, 'provider': row_payload(row)}, 200


def run_test(user, payload: dict):
    """Run one tiny completion against (a) a saved row, or (b) transient
    credentials supplied in the body before saving them.
    Returns ``(data, http_status)`` — failures are HTTP 200 with ok=False so
    clients can show the provider's own error message verbatim."""
    provider_id = (payload.get('providerId') or '').strip()
    if provider_id:
        row = get_row(user, provider_id)
        if row is None:
            return err('Provider not found', 'not_found'), 404
        resolved = resolve(user, row.provider, user_provider_id=str(row.id)) \
            if row.provider == 'custom' else resolve(user, row.provider)
        if resolved is None:
            return err('This provider cannot be used yet (disabled or missing key)'), 400
        fmt, base_url, api_key, model = resolved.format, resolved.base_url, resolved.api_key, resolved.model
        label = resolved.label
    else:
        fmt = (payload.get('apiFormat') or 'openai').strip().lower()
        base_url = (payload.get('baseUrl') or '').strip()
        api_key = (payload.get('apiKey') or '').strip()
        model = (payload.get('model') or '').strip()
        slug = (payload.get('provider') or '').strip().lower()
        p = preset(slug)
        if p and p.official:
            fmt = p.format
            base_url = base_url or p.base_url
            model = model or p.default_model
        label = p.label if p else 'Custom provider'
        if fmt not in VALID_FORMATS:
            return err('apiFormat must be openai, anthropic or gemini'), 400
        if not base_url.startswith(('http://', 'https://')):
            return err('Base URL must start with http:// or https://'), 400
        if not model:
            return err('A model id is required for the test'), 400

    try:
        # 30s cap on the wire — the UI mirrors this with a ~45s abort guard,
        # so a slow provider can never strand the "Test connection" button.
        result = quick_test(format=fmt, base_url=base_url, api_key=api_key, model=model, provider=label, timeout=30)
        return {
            'ok': True,
            'latencyMs': result.duration_ms,
            'model': result.model,
            'reply': result.text[:120],
        }, 200
    except LLMError as e:
        return {'ok': False, 'error': str(e)[:500], 'status': e.status}, 200
