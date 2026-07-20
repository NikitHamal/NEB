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

from api.background_agent.mobile_auth import json_body, require_device
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
