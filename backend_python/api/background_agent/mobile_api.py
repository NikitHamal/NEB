from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.http import FileResponse, Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from api.background_agent.attachments import save_uploads
from api.background_agent.crypto import decrypt_secret
from api.background_agent.events import add_message, emit
from api.background_agent.github import GitHubClient, GitHubError
from api.background_agent.lifecycle import archive_session, delete_session, restore_session
from api.background_agent.mobile_auth import (
    create_pairing,
    exchange_pairing,
    json_body,
    pairing_rate_allowed,
    require_device,
)
from api.models import (
    BackgroundAgentAction,
    BackgroundAgentArtifact,
    BackgroundAgentCredential,
    BackgroundAgentEvent,
    BackgroundAgentProject,
    BackgroundAgentSession,
    BackgroundAgentWorker,
    BotConfig,
)
from api.utils import now_ms, uuid_str
from api.llm.credentials import catalog_for_user
from api.llm.runtime import selection_payload


def _json(payload, status=200):
    response = JsonResponse(payload, status=status)
    response['Cache-Control'] = 'no-store, private'
    response['Pragma'] = 'no-cache'
    response['X-Content-Type-Options'] = 'nosniff'
    return response


def _error(message, status=400, code='request_failed'):
    return _json({'ok': False, 'error': str(message), 'code': code}, status=status)


def _admin(request):
    return request.background_agent_admin


def _credential(admin, required=False):
    value = BackgroundAgentCredential.objects.filter(admin_user=admin).first()
    if required and (not value or not value.is_connected):
        raise GitHubError('Connect GitHub from the NEBians background-agent website first')
    return value


def _github(admin):
    credential = _credential(admin, required=True)
    return GitHubClient(decrypt_secret(credential.encrypted_access_token)), credential


def _project(admin, project_id):
    value = BackgroundAgentProject.objects.select_related('credential').filter(pk=project_id, admin_user=admin).first()
    if not value:
        raise Http404('Project not found')
    return value


def _session(admin, session_id):
    value = BackgroundAgentSession.objects.select_related('project', 'bot_config').filter(pk=session_id, admin_user=admin).first()
    if not value:
        raise Http404('Session not found')
    return value


def _provider():
    return BotConfig.objects.filter(enabled=True, provider='qwen').order_by('id').first()


def _payload(request):
    if 'application/json' in (request.content_type or '').lower():
        return json_body(request)
    return request.POST.dict()


def _repo_data(repo):
    owner = repo.get('owner') or {}
    permissions = repo.get('permissions') or {}
    return {
        'id': repo.get('id'),
        'name': repo.get('name') or '',
        'fullName': repo.get('full_name') or '',
        'owner': owner.get('login') or '',
        'description': repo.get('description') or '',
        'private': bool(repo.get('private')),
        'archived': bool(repo.get('archived')),
        'defaultBranch': repo.get('default_branch') or 'main',
        'htmlUrl': repo.get('html_url') or '',
        'cloneUrl': repo.get('clone_url') or '',
        'updatedAt': repo.get('updated_at') or '',
        'canPush': bool(permissions.get('push') or permissions.get('maintain') or permissions.get('admin')),
    }


def _project_data(project):
    return {
        'id': str(project.id),
        'repoFullName': project.repo_full_name,
        'repoHtmlUrl': project.repo_html_url,
        'cloneUrl': project.clone_url,
        'defaultBranch': project.default_branch,
        'preferredBaseBranch': project.preferred_base_branch or project.default_branch,
        'private': project.is_private,
        'status': project.status,
        'autofixEnabled': bool(getattr(project, 'autofix_enabled', True)),
        'lastSyncedAt': project.last_synced_at,
        'lastError': project.last_error,
        'createdAt': project.created_at,
        'updatedAt': project.updated_at,
    }


def _attachment_data(attachment):
    return {
        'id': str(attachment.id),
        'name': attachment.file_name,
        'kind': attachment.kind,
        'contentType': attachment.content_type,
        'sizeBytes': attachment.size_bytes,
        'extension': attachment.extension,
    }


def _message_data(message):
    try:
        metadata = json.loads(message.metadata or '{}')
    except (TypeError, json.JSONDecodeError):
        metadata = {}
    return {
        'id': str(message.id),
        'role': message.role,
        'content': message.content,
        'label': metadata.get('label') or '',
        'metadata': metadata,
        'attachments': [_attachment_data(item) for item in message.attachments.all().order_by('created_at')],
        'createdAt': message.created_at,
    }


def _event_data(event):
    try:
        payload = json.loads(event.payload or '{}')
    except (TypeError, json.JSONDecodeError):
        payload = {}
    return {'id': event.id, 'type': event.event_type, 'message': event.message, 'payload': payload, 'createdAt': event.created_at}


def _action_data(action):
    try:
        result = json.loads(action.result or '{}')
    except (TypeError, json.JSONDecodeError):
        result = {}
    return {
        'id': str(action.id),
        'action': action.action,
        'status': action.status,
        'result': result,
        'error': action.error,
        'createdAt': action.created_at,
        'startedAt': action.started_at,
        'completedAt': action.completed_at,
    }


def _artifact_data(session, request):
    values = {}
    for artifact in session.artifacts.all():
        values[artifact.kind] = {
            'kind': artifact.kind,
            'fileName': artifact.file_name,
            'sizeBytes': artifact.size_bytes,
            'sha256': artifact.sha256,
            'downloadUrl': reverse('bg_mobile_artifact', args=[session.id, artifact.kind]),
        }
    return values


def _todos_data(session):
    try:
        todos = json.loads(getattr(session, 'todos_json', '') or '[]')
    except (TypeError, json.JSONDecodeError):
        return []
    if not isinstance(todos, list):
        return []
    clean = []
    for item in todos[:24]:
        if isinstance(item, dict) and item.get('content'):
            clean.append({'content': str(item['content'])[:220], 'status': str(item.get('status') or 'pending')})
    return clean


def _branch_description(session):
    try:
        state = json.loads(session.agent_state or '{}')
        return str(state.get('branchDescription') or '').strip()
    except (TypeError, json.JSONDecodeError):
        return ''


def _request_compaction(session, source):
    """Handle the /compact command from Zeus: run the anchored compaction at the next iteration."""
    now = now_ms()
    session.compact_requested_at = now
    session.updated_at = now
    update = ['compact_requested_at', 'updated_at']
    queued = False
    if session.status in ('paused', 'waiting'):
        session.status = 'queued'
        session.control_state = ''
        session.progress_label = 'Queued for context compaction'
        update += ['status', 'control_state', 'progress_label']
        queued = True
    session.save(update_fields=update)
    message = add_message(session, 'user', '/compact', {'kind': 'command', 'command': 'compact', 'source': source})
    if queued:
        emit(session, 'session.resumed', 'Session queued for manual context compaction')
    active = session.status in ('queued', 'preparing', 'running')
    note = ('Older context will be summarized at the start of the next agent iteration.'
            if active else 'Compaction will run when the session next resumes.')
    emit(session, 'context.compact_requested', 'Manual context compaction requested', {
        'queued': queued, 'status': session.status, 'source': source,
    })
    return _json({
        'ok': True,
        'message': _message_data(message),
        'command': 'compact',
        'queued': queued,
        'note': note,
        'status': session.status,
    })


def _llm_data(session):
    """Lightweight LLM selection summary for session payloads (no DB hits)."""
    from api.llm.runtime import describe_session_llm
    return describe_session_llm(session)


def _session_data(session, request=None, detail=False):
    window = session.context_window_tokens or 131072
    data = {
        'id': str(session.id),
        'projectId': str(session.project_id),
        'repoFullName': session.project.repo_full_name,
        'todos': _todos_data(session),
        'repoHtmlUrl': session.project.repo_html_url,
        'cloneUrl': session.project.clone_url,
        'title': session.title,
        'goal': session.goal if detail else session.goal[:2000],
        'sourceBranch': session.source_branch,
        'workBranch': session.work_branch,
        'branchDescription': _branch_description(session),
        'baseSha': session.base_sha,
        'headSha': session.head_sha,
        'status': session.status,
        'progress': session.progress,
        'progressLabel': session.progress_label,
        'iteration': session.iteration,
        'maxIterations': session.max_iterations,
        'summary': session.summary,
        'testSummary': session.test_summary,
        'lastError': session.last_error,
        'archived': bool(session.archived_at),
        'archivedAt': session.archived_at,
        'createdAt': session.created_at,
        'startedAt': session.started_at,
        'updatedAt': session.updated_at,
        'completedAt': session.completed_at,
        'context': {
            'estimatedTokens': session.context_tokens_estimate,
            'windowTokens': window,
            'percent': min(100, round((session.context_tokens_estimate * 100) / max(1, window))),
            'compactions': session.context_compactions,
        },
        'llm': _llm_data(session),
    }
    if detail:
        try:
            data['changedFiles'] = json.loads(session.changed_files or '[]')
        except (TypeError, json.JSONDecodeError):
            data['changedFiles'] = []
        messages = list(session.messages.prefetch_related('attachments').order_by('-created_at')[:250])
        messages.reverse()
        data.update({
            'diff': session.final_diff,
            'messages': [_message_data(item) for item in messages],
            'events': [_event_data(item) for item in session.events.order_by('-id')[:200][::-1]],
            'actions': [_action_data(item) for item in session.actions.order_by('-created_at')[:50]],
            'artifacts': _artifact_data(session, request) if request else {},
        })
    return data


@csrf_exempt
@require_POST
def pair_start(request):
    if not pairing_rate_allowed(request):
        return _error('Please wait before starting another authorization request', 429, 'rate_limited')
    try:
        payload = json_body(request)
        pairing, device_code = create_pairing(payload.get('deviceName') or 'Zeus')
        verification_path = reverse('web:background_agent_mobile_authorize')
        public_base = str(getattr(settings, 'BACKGROUND_AGENT_PUBLIC_URL', '') or '').rstrip('/')
        if public_base:
            verification_url = public_base + verification_path
        else:
            host = request.get_host()
            scheme = request.scheme if host.startswith(('localhost', '127.0.0.1')) else 'https'
            verification_url = f'{scheme}://{host}{verification_path}'
        return _json({
            'ok': True,
            'deviceCode': device_code,
            'userCode': pairing.user_code,
            'verificationUrl': verification_url,
            'verificationUrlComplete': verification_url + '?code=' + pairing.user_code,
            'expiresIn': 600,
            'interval': 3,
        }, status=201)
    except ValueError as exc:
        return _error(exc)


@csrf_exempt
@require_POST
def pair_token(request):
    try:
        payload = json_body(request)
        result = exchange_pairing((payload.get('deviceCode') or '').strip())
        if result is None:
            return _error('Authorization pending', 428, 'authorization_pending')
        raw_token, device = result
        return _json({
            'ok': True,
            'accessToken': raw_token,
            'tokenType': 'Bearer',
            'device': {'id': device.id, 'name': device.device_name},
        })
    except PermissionError as exc:
        return _error(exc, 403, 'access_denied')
    except ValueError as exc:
        return _error(exc, 400, 'invalid_grant')


@csrf_exempt
@require_GET
@require_device
def me(request):
    device = request.background_agent_device
    admin = _admin(request)
    credential = _credential(admin)
    return _json({
        'ok': True,
        'device': {'id': device.id, 'name': device.device_name, 'scopes': device.scopes.split(','), 'lastUsedAt': device.last_used_at},
        'user': {'id': str(admin.id), 'username': admin.username, 'displayName': admin.display_name or admin.username, 'photoUrl': admin.photo_url or ''},
        'github': {'connected': bool(credential and credential.is_connected), 'login': credential.github_login if credential else '', 'avatarUrl': credential.github_avatar_url if credential else ''},
    })


@csrf_exempt
@require_POST
@require_device
def revoke(request):
    device = request.background_agent_device
    device.revoked_at = now_ms()
    device.save(update_fields=['revoked_at'])
    return _json({'ok': True})


@csrf_exempt
@require_GET
@require_device
def state(request):
    admin = _admin(request)
    include_archived = request.GET.get('archived') == '1'
    session_query = BackgroundAgentSession.objects.filter(admin_user=admin).select_related('project', 'bot_config')
    if include_archived:
        session_query = session_query.filter(archived_at__gt=0)
    else:
        session_query = session_query.filter(archived_at=0)
    sessions = session_query.order_by('-updated_at')[:100]
    projects = BackgroundAgentProject.objects.filter(admin_user=admin).order_by('-updated_at')[:100]
    cutoff = now_ms() - 30_000
    workers = BackgroundAgentWorker.objects.filter(last_heartbeat_at__gte=cutoff, status__in=('starting', 'idle', 'busy'))
    provider = _provider()
    try:
        from api.llm.runtime import default_model_state
        model_state = default_model_state(admin, provider)
    except Exception:
        from api.qwen_utils.models import get_default_model as _qwen_default
        qwen_model = _qwen_default() or 'qwen3.8-max'
        model_state = {'provider': 'qwen', 'model': qwen_model, 'label': f'Qwen ({qwen_model})', 'configured': bool(provider)}
    return _json({
        'ok': True,
        'projects': [_project_data(item) for item in projects],
        'sessions': [_session_data(item) for item in sessions],
        'worker': {'online': workers.count(), 'healthy': workers.exists()},
        'model': model_state,
        'llm': catalog_for_user(admin),
    })


@csrf_exempt
@require_GET
@require_device
def repositories(request):
    try:
        client, _ = _github(_admin(request))
        values = client.list_repositories(page=max(1, int(request.GET.get('page', 1))), per_page=min(100, max(1, int(request.GET.get('perPage', 100)))), query=request.GET.get('q', ''))
        return _json({'ok': True, 'repositories': [_repo_data(item) for item in values]})
    except (GitHubError, ValueError) as exc:
        return _error(exc, 502, 'github_error')


@csrf_exempt
@require_GET
@require_device
def branches(request):
    full_name = (request.GET.get('repo') or '').strip()
    try:
        client, _ = _github(_admin(request))
        repo = client.get_repository(full_name)
        values = client.list_branches(full_name)
        return _json({'ok': True, 'defaultBranch': repo.get('default_branch') or 'main', 'branches': [{'name': item.get('name'), 'sha': (item.get('commit') or {}).get('sha', '')} for item in values]})
    except GitHubError as exc:
        return _error(exc, 502, 'github_error')


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@require_device
def projects(request):
    admin = _admin(request)
    if request.method == 'GET':
        values = BackgroundAgentProject.objects.filter(admin_user=admin).order_by('-updated_at')[:100]
        return _json({'ok': True, 'projects': [_project_data(item) for item in values]})
    try:
        payload = json_body(request)
        full_name = (payload.get('repoFullName') or '').strip()
        client, credential = _github(admin)
        repo = client.get_repository(full_name)
        now = now_ms()
        canonical = repo.get('full_name') or full_name
        project, created = BackgroundAgentProject.objects.get_or_create(
            admin_user=admin,
            repo_full_name=canonical,
            defaults={'id': uuid_str(), 'credential': credential, 'created_at': now, 'updated_at': now},
        )
        project.credential = credential
        project.github_repo_id = repo.get('id') or 0
        project.repo_html_url = repo.get('html_url') or ''
        project.clone_url = repo.get('clone_url') or f'https://github.com/{canonical}.git'
        project.default_branch = repo.get('default_branch') or 'main'
        project.preferred_base_branch = (payload.get('baseBranch') or project.default_branch).strip()
        project.is_private = bool(repo.get('private'))
        project.status = 'new' if created else project.status
        project.last_error = ''
        project.updated_at = now
        project.save()
        return _json({'ok': True, 'project': _project_data(project)}, status=201 if created else 200)
    except (ValueError, GitHubError) as exc:
        return _error(exc, 502 if isinstance(exc, GitHubError) else 400)


@csrf_exempt
@require_POST
@require_device
def project_settings(request, project_id):
    """Per-project automation settings. Currently: the CI auto-fix toggle."""
    admin = _admin(request)
    project = BackgroundAgentProject.objects.filter(admin_user=admin, pk=project_id).first()
    if not project:
        return _error('Project not found', 404, 'not_found')
    try:
        payload = json_body(request)
        project.autofix_enabled = bool(payload.get('autofixEnabled', True))
        project.updated_at = now_ms()
        project.save(update_fields=['autofix_enabled', 'updated_at'])
        return _json({'ok': True, 'project': _project_data(project)})
    except ValueError as exc:
        return _error(exc, 400)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@require_device
def sessions(request):
    admin = _admin(request)
    if request.method == 'GET':
        query = BackgroundAgentSession.objects.filter(admin_user=admin).select_related('project', 'bot_config')
        if request.GET.get('archived') == '1':
            query = query.filter(archived_at__gt=0)
        else:
            query = query.filter(archived_at=0)
        return _json({'ok': True, 'sessions': [_session_data(item) for item in query.order_by('-updated_at')[:100]]})
    try:
        payload = _payload(request)
        project = _project(admin, payload.get('projectId'))
        goal = (payload.get('goal') or '').strip()
        if len(goal) < 10:
            return _error('Describe the coding task in at least 10 characters')
        provider = _provider()
        selection = selection_payload(
            payload.get('llmProvider') or '', payload.get('llmModel') or '',
            (payload.get('llmProviderId') or ''),
        )
        # A selection is only honored when it can actually be served right now
        # (key present); otherwise the session uses the shared default path.
        if selection['llm_provider']:
            from api.llm.credentials import resolve as _llm_resolve
            resolved = _llm_resolve(admin, selection['llm_provider'], model=selection['llm_model'],
                                    user_provider_id=selection['llm_provider_id'])
            if resolved is None:
                return _error('Selected provider is not available (missing API key?). Add a key in Providers first.', 409, 'llm_unavailable')
        elif not provider:
            return _error('No model is configured right now. Add a provider or ask the admin to share one.', 409, 'model_unavailable')
        source_branch = (payload.get('sourceBranch') or project.preferred_base_branch or project.default_branch).strip()
        now = now_ms()
        session = BackgroundAgentSession.objects.create(
            id=uuid_str(), project=project, admin_user=admin, bot_config=provider,
            title=(payload.get('title') or goal.splitlines()[0])[:255], goal=goal,
            source_branch=source_branch, status='paused',
            llm_provider=selection['llm_provider'], llm_model=selection['llm_model'],
            llm_provider_id=selection['llm_provider_id'],
            context_window_tokens=int(getattr(settings, 'BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS', 131072)),
            created_at=now, updated_at=now,
        )
        message = add_message(session, 'user', goal, {'kind': 'initial_goal', 'source': 'zeus'})
        attachments = save_uploads(session, message, request.FILES.getlist('files'))
        session.status = 'queued'
        session.progress_label = 'Queued for worker'
        session.updated_at = now
        session.save(update_fields=['status', 'progress_label', 'updated_at'])
        emit(session, 'session.queued', 'Task queued from Zeus', {'repository': project.repo_full_name, 'sourceBranch': source_branch, 'attachmentCount': len(attachments)})
        return _json({'ok': True, 'session': _session_data(session, request, detail=True)}, status=201)
    except (ValueError, Http404) as exc:
        return _error(exc, 400)


@csrf_exempt
@require_GET
@require_device
def session_detail(request, session_id):
    return _json({'ok': True, 'session': _session_data(_session(_admin(request), session_id), request, detail=True)})


@csrf_exempt
@require_GET
@require_device
def session_events(request, session_id):
    session = _session(_admin(request), session_id)
    try:
        after = max(0, int(request.GET.get('after', 0)))
    except ValueError:
        after = 0
    events = list(BackgroundAgentEvent.objects.filter(session=session, id__gt=after).order_by('id')[:500])
    return _json({'ok': True, 'session': _session_data(session), 'events': [_event_data(item) for item in events], 'actions': [_action_data(item) for item in session.actions.order_by('-created_at')[:50]], 'artifacts': _artifact_data(session, request)})


@csrf_exempt
@require_POST
@require_device
def session_message(request, session_id):
    session = _session(_admin(request), session_id)
    try:
        payload = _payload(request)
        content = (payload.get('content') or '').strip()
        uploads = request.FILES.getlist('files')
        if not content and not uploads:
            return _error('Add a message or attachment')
        if content.lower() == '/compact' or content.lower().startswith('/compact '):
            return _request_compaction(session, source='zeus')
        message = add_message(session, 'user', content or 'Review the attached files as additional task context.', {'kind': 'followup', 'source': 'zeus'})
        saved = save_uploads(session, message, uploads)
        if session.status in ('paused', 'waiting', 'failed', 'completed'):
            session.status = 'queued'
            session.control_state = ''
            session.completed_at = 0
            session.last_error = ''
            session.progress_label = 'Queued with new guidance'
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'control_state', 'completed_at', 'last_error', 'progress_label', 'updated_at'])
            emit(session, 'session.resumed', 'Session resumed from Zeus')
        return _json({'ok': True, 'message': _message_data(message), 'attachmentCount': len(saved), 'status': session.status})
    except ValueError as exc:
        return _error(exc)


@csrf_exempt
@require_POST
@require_device
def session_control(request, session_id):
    session = _session(_admin(request), session_id)
    try:
        command = (json_body(request).get('command') or '').strip().lower()
        now = now_ms()
        if command == 'pause' and session.status in ('queued', 'preparing', 'running'):
            session.control_state = 'pause'
            session.progress_label = 'Pause requested'
        elif command == 'stop':
            if session.status in ('queued', 'paused', 'waiting'):
                session.status = 'cancelled'
                session.control_state = ''
                session.progress_label = 'Stopped'
                session.completed_at = now
            else:
                session.control_state = 'stop'
                session.progress_label = 'Stop requested'
        elif command == 'resume' and session.status in ('paused', 'waiting', 'failed', 'completed'):
            session.status = 'queued'
            session.control_state = ''
            session.completed_at = 0
            session.last_error = ''
            session.progress_label = 'Queued to resume'
        else:
            return _error('Control command is not valid for the current state', 409, 'invalid_state')
        session.updated_at = now
        session.save()
        emit(session, f'control.{command}_requested', f'{command.title()} requested from Zeus')
        return _json({'ok': True, 'session': _session_data(session)})
    except ValueError as exc:
        return _error(exc)


@csrf_exempt
@require_POST
@require_device
def session_action(request, session_id):
    session = _session(_admin(request), session_id)
    try:
        payload = json_body(request)
        name = (payload.get('action') or '').strip()
        if name not in {'push', 'open_pr', 'refresh', 'artifacts'}:
            return _error('Unknown action')
        if name in {'push', 'open_pr', 'artifacts'} and session.status in {'queued', 'preparing', 'running'}:
            return _error('Pause the session or wait for it to finish', 409, 'invalid_state')
        action = BackgroundAgentAction.objects.create(
            id=uuid_str(), session=session, requested_by=_admin(request), action=name,
            status='queued', payload=json.dumps(payload.get('payload') or {}, ensure_ascii=False), created_at=now_ms(),
        )
        emit(session, 'action.queued', f'{name} queued from Zeus', {'actionId': action.id, 'action': name})
        return _json({'ok': True, 'action': _action_data(action)}, status=202)
    except ValueError as exc:
        return _error(exc)


@csrf_exempt
@require_http_methods(['POST', 'DELETE'])
@require_device
def session_lifecycle(request, session_id):
    session = _session(_admin(request), session_id)
    try:
        if request.method == 'DELETE':
            delete_session(session)
            return _json({'ok': True, 'deleted': True})
        action = (json_body(request).get('action') or '').strip().lower()
        if action == 'archive':
            archive_session(session)
        elif action == 'restore':
            restore_session(session)
        else:
            return _error('Unknown lifecycle action')
        return _json({'ok': True, 'session': _session_data(session)})
    except ValueError as exc:
        return _error(exc, 409, 'invalid_state')


@csrf_exempt
@require_GET
@require_device
def artifact(request, session_id, kind):
    session = _session(_admin(request), session_id)
    item = BackgroundAgentArtifact.objects.filter(session=session, kind=kind).first()
    if not item:
        raise Http404('Artifact is not available')
    path = Path(item.file_path).resolve()
    root = Path(getattr(settings, 'BACKGROUND_AGENT_ROOT', settings.BASE_DIR / 'background_agent_data')).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise Http404('Invalid artifact path') from exc
    if not path.is_file():
        raise Http404('Artifact file is missing')
    content_type = 'application/zip' if kind == 'changes_zip' else 'text/x-diff'
    response = FileResponse(path.open('rb'), as_attachment=True, filename=item.file_name, content_type=content_type)
    response['Cache-Control'] = 'no-store, private'
    response['X-Content-Type-Options'] = 'nosniff'
    return response
