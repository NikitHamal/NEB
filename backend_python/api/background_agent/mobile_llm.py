"""Zeus-facing endpoints for user-switchable LLM providers (BYOK).

  GET    llm/catalog/              → every provider the picker can show
  GET    llm/providers/            → the user's saved rows (masked keys)
  POST   llm/providers/            → save a new custom provider or preset key
  PATCH  llm/providers/<id>/       → update a row
  DELETE llm/providers/<id>/       → remove a row
  POST   llm/test/                 → validate credentials with one tiny call

All behavior lives in ``api.llm.provider_store`` so the website settings UI
shares the exact same logic. API keys are write-only over the wire: stored
AES-GCM encrypted and only ever returned masked.
"""
from __future__ import annotations

import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from api.background_agent.mobile_auth import json_body, require_device, optional_device
from api.llm import provider_store
from api.llm.credentials import catalog_for_user

logger = logging.getLogger(__name__)


def _json(payload, status=200):
    response = JsonResponse(payload, status=status)
    response['Cache-Control'] = 'no-store, private'
    return response


def _error(message, status=400, code='request_failed'):
    return _json({'ok': False, 'error': str(message), 'code': code}, status=status)


def _admin(request):
    return request.background_agent_admin


def _payload(request):
    try:
        return json_body(request)
    except Exception:
        return None


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
        return _json({'ok': True, 'providers': provider_store.list_providers(admin)})

    payload = _payload(request)
    if payload is None:
        return _error('Invalid JSON body')
    data, status = provider_store.create_provider(admin, payload)
    return _json(data, status=status)


@csrf_exempt
@require_http_methods(['PATCH', 'DELETE'])
@require_device
def llm_provider_detail(request, provider_id):
    admin = _admin(request)
    row = provider_store.get_row(admin, provider_id)
    if row is None:
        return _error('Provider not found', 404, 'not_found')

    if request.method == 'DELETE':
        row.delete()
        return _json({'ok': True})

    payload = _payload(request)
    if payload is None:
        return _error('Invalid JSON body')
    data, status = provider_store.update_provider(row, payload)
    return _json(data, status=status)


@csrf_exempt
@require_POST
@require_device
def llm_test(request):
    """Run one tiny completion against (a) a saved row, or (b) transient
    credentials supplied in the body before saving them."""
    payload = _payload(request)
    if payload is None:
        return _error('Invalid JSON body')
    data, status = provider_store.run_test(_admin(request), payload)
    return _json(data, status=status)


@csrf_exempt
@require_POST
@optional_device
def llm_chat(request):
    """Unified chat endpoint for mobile agents (WebAgent & PhoneController)
    supporting all official providers (BYOK), custom endpoints, and community proxies (Motif, Qwen, K2Think, Poolside)."""
    admin = _admin(request)
    payload = _payload(request)
    if payload is None:
        return _error('Invalid JSON body')

    from api.llm.credentials import resolve
    slug = (payload.get('provider') or '').strip().lower()
    model = (payload.get('model') or '').strip()
    provider_id = (payload.get('providerId') or '').strip()
    messages = payload.get('messages') or []
    prompt = (payload.get('prompt') or '').strip()

    if not messages and prompt:
        system_prompt = (payload.get('system') or '').strip()
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

    if not messages:
        return _error('messages or prompt is required')

    resolved = resolve(admin, slug, model=model, user_provider_id=provider_id)
    if resolved is None:
        return _error(f'Provider "{slug}" cannot be resolved. Please verify credentials/model in Settings.', 400)

    # Community scrapers / proxies (simple_chat returns Optional[str], not a dict)
    if not resolved.official:
        user_msg = messages[-1].get('content', '') if messages else ''
        if not isinstance(user_msg, str):
            user_msg = ''
        sys_msg = next((m['content'] for m in messages if m.get('role') == 'system'), '')
        if not isinstance(sys_msg, str):
            sys_msg = ''
        if resolved.slug == 'motiftech':
            from api import motiftech_proxy
            reply = motiftech_proxy.simple_chat(
                user_message=user_msg,
                model=resolved.model or 'motif-102b',
                system_prompt=sys_msg,
            )
            if not reply:
                return _json({'ok': False, 'error': 'Motif request failed. Please retry.'})
            return _json({'ok': True, 'reply': reply, 'model': resolved.model})
        elif resolved.slug == 'k2think':
            from api import k2think_proxy
            reply = k2think_proxy.simple_chat(
                user_message=user_msg,
                model=resolved.model or 'IFM/K2-Horizon-375B-A23B',
                system_prompt=sys_msg,
            )
            if not reply:
                return _json({'ok': False, 'error': 'K2Think request failed. Please retry.'})
            return _json({'ok': True, 'reply': reply, 'model': resolved.model})
        elif resolved.slug == 'poolside':
            from api import poolside_proxy
            reply = poolside_proxy.simple_chat(
                user_message=user_msg,
                model=resolved.model or 'laguna-s-2.1',
                system_prompt=sys_msg,
            )
            if not reply:
                return _json({'ok': False, 'error': 'Poolside request failed. Please retry.'})
            return _json({'ok': True, 'reply': reply, 'model': resolved.model})
        else:
            from api import qwen_proxy
            reply = qwen_proxy.call_qwen(
                system_prompt=sys_msg,
                user_message=user_msg,
                model=resolved.model or 'qwen3.8-max',
                max_tokens=int(payload.get('max_tokens', 4096))
            )
            if not reply:
                return _json({'ok': False, 'error': 'Qwen returned an empty response. Please retry.'})
            return _json({'ok': True, 'reply': reply, 'model': resolved.model})

    # Official BYOK / Custom
    from api.llm.client import chat as _client_chat, LLMError
    try:
        res = _client_chat(
            format=resolved.format,
            base_url=resolved.base_url,
            api_key=resolved.api_key,
            model=resolved.model,
            messages=messages,
            max_tokens=int(payload.get('max_tokens', 4096)),
            temperature=float(payload.get('temperature', 0.2)),
            timeout=int(payload.get('timeout', 120)),
            provider=resolved.slug
        )
        return _json({
            'ok': True,
            'reply': res.text,
            'model': res.model,
            'usage': {
                'input_tokens': getattr(res, 'input_tokens', 0) or 0,
                'output_tokens': getattr(res, 'output_tokens', 0) or 0,
            },
        })
    except LLMError as e:
        return _json({'ok': False, 'error': str(e), 'status': e.status})

