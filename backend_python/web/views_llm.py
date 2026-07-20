"""NEBians website LLM provider settings (Background Agent session auth).

  GET    backgroundagent/api/llm/providers/           → catalog + saved rows
  POST   backgroundagent/api/llm/providers/           → save custom / preset key
  PATCH  backgroundagent/api/llm/providers/<id>/      → update a row
  DELETE backgroundagent/api/llm/providers/<id>/      → remove a row
  POST   backgroundagent/api/llm/test/                → one-call credential test

These mirror the Zeus mobile endpoints and delegate to
``api.llm.provider_store`` so both clients share identical behavior — and the
same ``UserLLMProvider`` rows that the background agent runner resolves.
"""
from __future__ import annotations

import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST

from api.llm import provider_store
from api.llm.credentials import catalog_for_user
from .background_agent_auth import get_bg_admin, require_bg_admin_json

logger = logging.getLogger(__name__)


def _json(payload, status=200):
    response = JsonResponse(payload, status=status)
    response['Cache-Control'] = 'no-store, private'
    return response


def _error(message, status=400, code='request_failed'):
    return _json({'ok': False, 'error': str(message), 'code': code}, status=status)


def _json_body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (ValueError, UnicodeDecodeError):
        return None


@require_http_methods(['GET', 'POST'])
def background_agent_llm_providers(request):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    admin = get_bg_admin(request)
    if request.method == 'GET':
        return _json({
            'ok': True,
            'catalog': catalog_for_user(admin),
            'providers': provider_store.list_providers(admin),
        })
    payload = _json_body(request)
    if payload is None:
        return _error('Invalid JSON body')
    data, status = provider_store.create_provider(admin, payload)
    return _json(data, status=status)


@require_http_methods(['PATCH', 'DELETE'])
def background_agent_llm_provider_detail(request, provider_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    admin = get_bg_admin(request)
    row = provider_store.get_row(admin, provider_id)
    if row is None:
        return _error('Provider not found', 404, 'not_found')

    if request.method == 'DELETE':
        row.delete()
        return _json({'ok': True})

    payload = _json_body(request)
    if payload is None:
        return _error('Invalid JSON body')
    data, status = provider_store.update_provider(row, payload)
    return _json(data, status=status)


@require_POST
def background_agent_llm_test(request):
    """Validate credentials with one tiny completion — saved row or the
    values the user is still typing into the settings dialog."""
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    payload = _json_body(request)
    if payload is None:
        return _error('Invalid JSON body')
    data, status = provider_store.run_test(get_bg_admin(request), payload)
    return _json(data, status=status)
