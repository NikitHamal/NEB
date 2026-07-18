from __future__ import annotations

import json

from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods

from api.background_agent.lifecycle import archive_session, delete_session, restore_session
from api.models import BackgroundAgentSession
from web.background_agent_auth import get_bg_admin, require_bg_admin_json
from web.background_agent_serializers import serialize_session_summary


def _session(request, session_id):
    value = BackgroundAgentSession.objects.select_related('project', 'bot_config').filter(
        pk=session_id,
        admin_user=get_bg_admin(request),
    ).first()
    if not value:
        raise Http404('Session not found')
    return value


@require_http_methods(['POST', 'DELETE'])
def background_agent_session_lifecycle(request, session_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session(request, session_id)
    try:
        if request.method == 'DELETE':
            delete_session(session)
            return JsonResponse({'ok': True, 'deleted': True})
        payload = json.loads(request.body.decode('utf-8') or '{}')
        action = (payload.get('action') or '').strip().lower()
        if action == 'archive':
            archive_session(session)
        elif action == 'restore':
            restore_session(session)
        else:
            return JsonResponse({'ok': False, 'error': 'Unknown lifecycle action'}, status=400)
        return JsonResponse({'ok': True, 'session': serialize_session_summary(session)})
    except (ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=409)
