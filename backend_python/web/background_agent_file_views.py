from __future__ import annotations

import mimetypes
from pathlib import Path
from urllib.parse import quote, urlencode

from django.http import FileResponse, Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from api.background_agent.attachments import safe_attachment_path
from api.background_agent.viewer import (
    attachment_payload,
    list_workspace_files,
    preview_mode,
    read_workspace_text,
    workspace_file,
)
from api.models import BackgroundAgentAttachment, BackgroundAgentSession
from .background_agent_auth import get_bg_admin, require_bg_admin, require_bg_admin_json


def _session_for_admin(request, session_id):
    try:
        return BackgroundAgentSession.objects.select_related('project', 'project__credential').get(
            pk=session_id,
            admin_user=get_bg_admin(request),
        )
    except BackgroundAgentSession.DoesNotExist:
        raise Http404('Session not found')


def _json_error(message, status=400):
    return JsonResponse({'ok': False, 'error': str(message)}, status=status)


@require_GET
def background_agent_session_files(request, session_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
    return JsonResponse({'ok': True, 'files': list_workspace_files(session)})


@require_GET
def background_agent_session_file(request, session_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
    attachment_id = (request.GET.get('attachment') or '').strip()
    try:
        if attachment_id:
            attachment = BackgroundAgentAttachment.objects.get(pk=attachment_id, session=session)
            payload = attachment_payload(attachment)
            query = {'attachment': attachment.id}
        else:
            relative = (request.GET.get('path') or '').strip()
            if not relative:
                return _json_error('path is required')
            payload = read_workspace_text(session, relative)
            query = {'path': relative}
        payload['previewUrl'] = reverse(
            'web:background_agent_session_preview', args=[session.id],
        ) + '?' + urlencode(query)
        return JsonResponse({'ok': True, 'file': payload})
    except (BackgroundAgentAttachment.DoesNotExist, FileNotFoundError):
        return _json_error('File not found', 404)


@require_GET
def background_agent_session_preview(request, session_id):
    if require_bg_admin(request):
        raise Http404
    session = _session_for_admin(request, session_id)
    attachment_id = (request.GET.get('attachment') or '').strip()
    if attachment_id:
        try:
            attachment = BackgroundAgentAttachment.objects.get(pk=attachment_id, session=session)
        except BackgroundAgentAttachment.DoesNotExist:
            raise Http404('Attachment not found')
        path = safe_attachment_path(attachment)
        content_type = attachment.content_type or 'application/octet-stream'
        filename = attachment.file_name
    else:
        relative = (request.GET.get('path') or '').strip()
        path = workspace_file(session, relative)
        content_type = ''
        filename = Path(relative).name
    if not path or not path.is_file():
        raise Http404('File not found')
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    mode = preview_mode(filename, content_type)
    if mode in {'text', 'markdown'}:
        content_type = 'text/plain; charset=utf-8'
    elif mode == 'binary':
        content_type = 'application/octet-stream'
    response = FileResponse(path.open('rb'), content_type=content_type)
    response['Content-Disposition'] = "inline; filename*=UTF-8''" + quote(filename)
    response['Content-Security-Policy'] = "sandbox; default-src 'none'; img-src 'self' data:; media-src 'self'; style-src 'unsafe-inline'"
    response['Cross-Origin-Resource-Policy'] = 'same-origin'
    response['X-Content-Type-Options'] = 'nosniff'
    return response
