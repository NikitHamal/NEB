"""Zeus-facing endpoints for user-switchable LLM providers (BYOK).

  GET    llm/catalog/              → every provider the picker can show
  GET    llm/providers/            → the user's saved rows (masked keys)
  POST   llm/providers/            → save a new custom provider or preset key
  PATCH  llm/providers/<id>/       → update a row
  DELETE llm/providers/<id>/       → remove a row
  POST   llm/test/                 → validate credentials with one tiny call

API keys are write-only over the wire: stored AES-GCM encrypted and only ever
returned masked.
"""
from __future__ import annotations

import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from api.background_agent.mobile_auth import json_body, require_device
from api.llm.client import LLMError, quick_test
from api.llm.credentials import catalog_for_user, resolve
from api.llm.crypto import encrypt_key, mask_key, decrypt_key
from api.llm.registry import preset
from api.models import UserLLMProvider
from api.utils import now_ms, uuid_str

logger = logging.getLogger(__name__)

_VALID_FORMATS = ('openai', 'anthropic', 'gemini')


def _json(payload, status=200):
    response = JsonResponse(payload, status=status)
    response['Cache-Control'] = 'no-store, private'
    return response


def _error(message, status=400, code='request_failed'):
    return _json({'ok': False, 'error': str(message), 'code': code}, status=status)


def _admin(request):
    return request.background_agent_admin


def _row_payload(row) -> dict:
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


@csrf_exempt
@require_GET
@require_device
def llm_catalog(request):
    return _json({'ok': True, 'llm': catalog_for_user(_admin(request))})


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@require_device
def llm_providers(request):
    admin = _admin(request)
    if request.method == 'GET':
        rows = UserLLMProvider.objects.filter(user=admin).order_by('-updated_at')
        return _json({'ok': True, 'providers': [_row_payload(r) for r in rows]})

    try:
        payload = json_body(request)
    except Exception:
        return _error('Invalid JSON body')
    provider = (payload.get('provider') or '').strip().lower()

    if provider == 'custom':
        name = (payload.get('name') or '').strip()[:100] or 'Custom provider'
        api_format = (payload.get('apiFormat') or 'openai').strip().lower()
        if api_format not in _VALID_FORMATS:
            return _error('apiFormat must be openai, anthropic or gemini')
        base_url = (payload.get('baseUrl') or '').strip()
        if not base_url.startswith(('http://', 'https://')):
            return _error('Base URL must start with http:// or https://')
        models = [str(m).strip() for m in (payload.get('models') or []) if str(m).strip()][:40]
        default_model = (payload.get('defaultModel') or (models[0] if models else '')).strip()[:200]
        if not default_model:
            return _error('Add at least one model id for this provider')
        key_plain = (payload.get('apiKey') or '').strip()
        try:
            context_window = max(1024, min(int(payload.get('contextWindow') or 131072), 2_000_000))
            max_output = max(256, min(int(payload.get('maxOutputTokens') or 4096), 128000))
        except (TypeError, ValueError):
            return _error('contextWindow / maxOutputTokens must be numbers')
        row = UserLLMProvider.objects.create(
            id=uuid_str(), user=admin, name=name, provider='custom',
            api_format=api_format, base_url=base_url,
            api_key=encrypt_key(key_plain) if key_plain else '',
            models_json=json.dumps(models), default_model=default_model,
            context_window=context_window, max_output_tokens=max_output,
            enabled=True, created_at=now_ms(), updated_at=now_ms(),
        )
        return _json({'ok': True, 'provider': _row_payload(row)}, status=201)

    # Preset BYOK: store/replace the user's own key for a known provider.
    p = preset(provider)
    if not p or not p.official:
        return _error('Unknown provider. Use agnes, openai, anthropic, gemini, deepseek — or custom.')
    key_plain = (payload.get('apiKey') or '').strip()
    if not key_plain:
        return _error(f'An API key is required for {p.label}')
    default_model = (payload.get('defaultModel') or '').strip()[:200]
    base_url = (payload.get('baseUrl') or '').strip()
    if base_url and not base_url.startswith(('http://', 'https://')):
        return _error('Base URL must start with http:// or https://')
    row = UserLLMProvider.objects.filter(user=admin, provider=p.slug).first()
    now = now_ms()
    if row is None:
        row = UserLLMProvider(
            id=uuid_str(), user=admin, provider=p.slug, name=p.label,
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
    return _json({'ok': True, 'provider': _row_payload(row)}, status=201)


@csrf_exempt
@require_http_methods(['PATCH', 'DELETE'])
@require_device
def llm_provider_detail(request, provider_id):
    admin = _admin(request)
    row = UserLLMProvider.objects.filter(pk=provider_id, user=admin).first()
    if row is None:
        return _error('Provider not found', 404, 'not_found')

    if request.method == 'DELETE':
        row.delete()
        return _json({'ok': True})

    try:
        payload = json_body(request)
    except Exception:
        return _error('Invalid JSON body')

    changed = []
    if 'name' in payload and row.provider == 'custom':
        row.name = (payload.get('name') or '').strip()[:100] or row.name
        changed.append('name')
    if 'apiFormat' in payload and row.provider == 'custom':
        fmt = (payload.get('apiFormat') or '').strip().lower()
        if fmt in _VALID_FORMATS:
            row.api_format = fmt
            changed.append('api_format')
    if 'baseUrl' in payload and row.provider == 'custom':
        url = (payload.get('baseUrl') or '').strip()
        if url and not url.startswith(('http://', 'https://')):
            return _error('Base URL must start with http:// or https://')
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
    return _json({'ok': True, 'provider': _row_payload(row)})


@csrf_exempt
@require_POST
@require_device
def llm_test(request):
    """Run one tiny completion against (a) a saved row, or (b) transient
    credentials supplied in the body before saving them."""
    admin = _admin(request)
    try:
        payload = json_body(request)
    except Exception:
        return _error('Invalid JSON body')

    provider_id = (payload.get('providerId') or '').strip()
    if provider_id:
        row = UserLLMProvider.objects.filter(pk=provider_id, user=admin).first()
        if row is None:
            return _error('Provider not found', 404, 'not_found')
        resolved = resolve(admin, row.provider, user_provider_id=str(row.id)) \
            if row.provider == 'custom' else resolve(admin, row.provider)
        if resolved is None:
            return _error('This provider cannot be used yet (disabled or missing key)')
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
        if fmt not in _VALID_FORMATS:
            return _error('apiFormat must be openai, anthropic or gemini')
        if not base_url.startswith(('http://', 'https://')):
            return _error('Base URL must start with http:// or https://')
        if not model:
            return _error('A model id is required for the test')

    try:
        result = quick_test(format=fmt, base_url=base_url, api_key=api_key, model=model, provider=label)
        return _json({
            'ok': True,
            'latencyMs': result.duration_ms,
            'model': result.model,
            'reply': result.text[:120],
        })
    except LLMError as e:
        return _json({'ok': False, 'error': str(e)[:500], 'status': e.status})
