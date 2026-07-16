"""Admin-only web/API surface for the durable background coding agent."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from api.background_agent.crypto import decrypt_secret, encrypt_secret
from api.background_agent.events import add_message, emit
from api.background_agent.github import GitHubClient, GitHubError
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
from .view_helpers import _require_staff_admin

logger = logging.getLogger(__name__)
_STATE_SALT = 'background-agent-github-oauth'


def _json_body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError('Invalid JSON request body')


def _json_error(message, status=400):
    return JsonResponse({'ok': False, 'error': str(message)}, status=status)


def _credential(request, required=False):
    credential = BackgroundAgentCredential.objects.filter(admin_user=request.user, revoked_at=0).first()
    if required and (not credential or not credential.is_connected):
        raise GitHubError('Connect a GitHub account first')
    return credential


def _github_client(request):
    credential = _credential(request, required=True)
    return GitHubClient(decrypt_secret(credential.encrypted_access_token)), credential


def _project_for_user(request, project_id):
    try:
        return BackgroundAgentProject.objects.select_related('credential').get(pk=project_id, admin_user=request.user)
    except BackgroundAgentProject.DoesNotExist:
        raise Http404('Project not found')


def _session_for_user(request, session_id):
    try:
        return BackgroundAgentSession.objects.select_related(
            'project', 'project__credential', 'bot_config'
        ).get(pk=session_id, admin_user=request.user)
    except BackgroundAgentSession.DoesNotExist:
        raise Http404('Session not found')


def _absolute_https_uri(request, route_name):
    uri = request.build_absolute_uri(reverse(route_name))
    if request.headers.get('X-Forwarded-Proto') == 'https' and uri.startswith('http://'):
        uri = 'https://' + uri[len('http://'):]
    return uri


@require_GET
def background_agent_page(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    credential = _credential(request)
    providers = BotConfig.objects.filter(enabled=True).order_by('name', 'id')
    return render(request, 'admin_panel/background_agent.html', {
        'active_page': 'background_agent',
        'is_admin': True,
        'github_connected': bool(credential and credential.is_connected),
        'github_login': credential.github_login if credential else '',
        'providers': providers,
    })


@require_GET
def background_agent_github_connect(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    client_id = getattr(settings, 'BACKGROUND_AGENT_GITHUB_CLIENT_ID', '')
    if not client_id:
        messages.error(request, 'Background-agent GitHub OAuth is not configured.')
        return redirect('web:background_agent')
    state = TimestampSigner(salt=_STATE_SALT).sign(str(request.user.pk))
    redirect_uri = _absolute_https_uri(request, 'web:background_agent_github_callback')
    return redirect(GitHubClient.authorize_url(state=state, redirect_uri=redirect_uri))


@require_GET
def background_agent_github_callback(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    state = request.GET.get('state', '')
    code = request.GET.get('code', '')
    if not state or not code:
        messages.error(request, 'GitHub authorization was cancelled or incomplete.')
        return redirect('web:background_agent')
    try:
        owner_id = TimestampSigner(salt=_STATE_SALT).unsign(state, max_age=600)
        if str(owner_id) != str(request.user.pk):
            raise BadSignature('OAuth user mismatch')
        redirect_uri = _absolute_https_uri(request, 'web:background_agent_github_callback')
        token, scopes = GitHubClient.exchange_code(code=code, redirect_uri=redirect_uri)
        github_user = GitHubClient(token).current_user()
        now = now_ms()
        credential, _ = BackgroundAgentCredential.objects.get_or_create(
            admin_user=request.user,
            defaults={'created_at': now},
        )
        credential.github_user_id = github_user.get('id') or 0
        credential.github_login = github_user.get('login') or ''
        credential.github_avatar_url = github_user.get('avatar_url') or ''
        credential.encrypted_access_token = encrypt_secret(token)
        credential.token_scopes = scopes
        credential.updated_at = now
        credential.last_validated_at = now
        credential.revoked_at = 0
        credential.save(update_fields=[
            'github_user_id', 'github_login', 'github_avatar_url',
            'encrypted_access_token', 'token_scopes', 'updated_at',
            'last_validated_at', 'revoked_at',
        ])
        messages.success(request, f"GitHub connected as {github_user.get('login') or 'account'}.")
    except (BadSignature, SignatureExpired, GitHubError, ValueError) as exc:
        logger.warning('Background agent GitHub connection failed: %s', exc)
        messages.error(request, str(exc))
    return redirect('web:background_agent')


@require_POST
def background_agent_github_disconnect(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    credential = _credential(request)
    if credential:
        credential.encrypted_access_token = ''
        credential.revoked_at = now_ms()
        credential.updated_at = now_ms()
        credential.save(update_fields=['encrypted_access_token', 'revoked_at', 'updated_at'])
    return JsonResponse({'ok': True})


@require_GET
def background_agent_state(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    credential = _credential(request)
    projects = BackgroundAgentProject.objects.filter(admin_user=request.user).order_by('-updated_at')[:100]
    sessions = BackgroundAgentSession.objects.filter(admin_user=request.user).select_related('project', 'bot_config').order_by('-created_at')[:100]
    providers = BotConfig.objects.filter(enabled=True).order_by('name', 'id')
    worker_cutoff = now_ms() - 30000
    workers = list(BackgroundAgentWorker.objects.filter(
        last_heartbeat_at__gte=worker_cutoff,
        status__in=('starting', 'idle', 'busy'),
    ).order_by('worker_id')[:50])
    return JsonResponse({
        'ok': True,
        'github': {
            'connected': bool(credential and credential.is_connected),
            'login': credential.github_login if credential else '',
            'avatarUrl': credential.github_avatar_url if credential else '',
            'scopes': (credential.token_scopes.split(',') if credential and credential.token_scopes else []),
        },
        'projects': [_serialize_project(p) for p in projects],
        'sessions': [_serialize_session_summary(s) for s in sessions],
        'providers': [{
            'id': p.id,
            'name': p.name,
            'provider': p.provider,
            'model': p.model,
            'label': f'{p.name} · {p.provider}/{p.model}',
        } for p in providers],
        'worker': {
            'online': len(workers),
            'healthy': bool(workers),
            'instances': [{
                'id': worker.worker_id,
                'status': worker.status,
                'currentKind': worker.current_kind,
                'currentId': worker.current_id,
                'lastHeartbeatAt': worker.last_heartbeat_at,
            } for worker in workers],
        },
    })


@require_GET
def background_agent_repositories(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    try:
        client, _ = _github_client(request)
        repos = client.list_repositories(
            page=int(request.GET.get('page', '1') or 1),
            per_page=int(request.GET.get('per_page', '50') or 50),
            query=request.GET.get('q', ''),
        )
        return JsonResponse({'ok': True, 'repositories': [_serialize_repo(r) for r in repos]})
    except (GitHubError, ValueError) as exc:
        return _json_error(exc, 502)


@require_GET
def background_agent_branches(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    full_name = request.GET.get('repo', '')
    try:
        client, _ = _github_client(request)
        repo = client.get_repository(full_name)
        branches = client.list_branches(full_name)
        return JsonResponse({
            'ok': True,
            'defaultBranch': repo.get('default_branch') or 'main',
            'branches': [{'name': b.get('name'), 'sha': (b.get('commit') or {}).get('sha', '')} for b in branches],
        })
    except GitHubError as exc:
        return _json_error(exc, 502)


@require_POST
def background_agent_create_project(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    try:
        payload = _json_body(request)
        full_name = (payload.get('repoFullName') or '').strip()
        preferred_branch = (payload.get('baseBranch') or '').strip()
        client, credential = _github_client(request)
        repo = client.get_repository(full_name)
        permissions = repo.get('permissions') or {}
        can_read = permissions.get('pull') is not False
        if not can_read:
            return _json_error('The connected GitHub account cannot read this repository', 403)
        now = now_ms()
        canonical_name = repo.get('full_name') or full_name
        project, created = BackgroundAgentProject.objects.get_or_create(
            admin_user=request.user,
            repo_full_name=canonical_name,
            defaults={
                'id': uuid_str(),
                'credential': credential,
                'created_at': now,
                'updated_at': now,
            },
        )
        project.credential = credential
        project.github_repo_id = repo.get('id') or 0
        project.repo_html_url = repo.get('html_url') or ''
        project.clone_url = repo.get('clone_url') or f'https://github.com/{canonical_name}.git'
        project.default_branch = repo.get('default_branch') or 'main'
        project.preferred_base_branch = preferred_branch or project.default_branch
        project.is_private = bool(repo.get('private'))
        project.status = 'new' if created else project.status
        project.last_error = ''
        project.updated_at = now
        project.save(update_fields=[
            'credential', 'github_repo_id', 'repo_html_url', 'clone_url',
            'default_branch', 'preferred_base_branch', 'is_private', 'status',
            'last_error', 'updated_at',
        ])
        return JsonResponse({'ok': True, 'project': _serialize_project(project)})
    except (ValueError, GitHubError) as exc:
        return _json_error(exc, 400 if isinstance(exc, ValueError) else 502)


@require_POST
def background_agent_create_session(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    try:
        payload = _json_body(request)
        project = _project_for_user(request, payload.get('projectId'))
        goal = (payload.get('goal') or '').strip()
        if len(goal) < 10:
            return _json_error('Describe the coding task in at least 10 characters')
        source_branch = (payload.get('sourceBranch') or project.preferred_base_branch or project.default_branch).strip()
        provider_id = payload.get('providerId')
        provider = BotConfig.objects.filter(pk=provider_id, enabled=True).first() if provider_id else BotConfig.objects.filter(enabled=True).first()
        if not provider:
            return _json_error('No enabled AI provider is configured', 409)
        max_iterations = max(5, min(int(payload.get('maxIterations') or 30), 100))
        title = (payload.get('title') or goal.splitlines()[0])[:255]
        now = now_ms()
        session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=request.user,
            bot_config=provider,
            title=title,
            goal=goal,
            source_branch=source_branch,
            status='queued',
            progress=0,
            progress_label='Queued for worker',
            max_iterations=max_iterations,
            created_at=now,
            updated_at=now,
        )
        add_message(session, 'user', goal, {'kind': 'initial_goal'})
        emit(session, 'session.queued', 'Task queued for the background worker', {
            'repository': project.repo_full_name,
            'sourceBranch': source_branch,
            'provider': f'{provider.provider}/{provider.model}',
        })
        return JsonResponse({'ok': True, 'session': _serialize_session_detail(session)}, status=201)
    except (ValueError, Http404) as exc:
        return _json_error(exc, 400)


@require_GET
def background_agent_session_detail(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    session = _session_for_user(request, session_id)
    return JsonResponse({'ok': True, 'session': _serialize_session_detail(session)})


@require_GET
def background_agent_session_events(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    session = _session_for_user(request, session_id)
    try:
        after = max(0, int(request.GET.get('after', '0') or 0))
    except ValueError:
        after = 0
    events = list(BackgroundAgentEvent.objects.filter(session=session, id__gt=after).order_by('id')[:500])
    serialized_events = [_serialize_event(e) for e in events]
    message_ids = [
        item['payload'].get('messageId')
        for item in serialized_events
        if item['type'] == 'message.created' and item['payload'].get('messageId')
    ]
    messages_by_id = {
        str(message.id): _serialize_message(message)
        for message in session.messages.filter(id__in=message_ids)
    }
    for item in serialized_events:
        message_id = item['payload'].get('messageId')
        if message_id and str(message_id) in messages_by_id:
            item['payload']['message'] = messages_by_id[str(message_id)]
    return JsonResponse({
        'ok': True,
        'session': _serialize_session_summary(session),
        'events': serialized_events,
        'actions': [_serialize_action(a) for a in session.actions.order_by('-created_at')[:50]],
        'artifacts': _serialize_artifacts(session),
    })


@require_POST
def background_agent_session_message(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    session = _session_for_user(request, session_id)
    try:
        payload = _json_body(request)
        content = (payload.get('content') or '').strip()
        if not content:
            return _json_error('Message cannot be empty')
        if len(content) > 50000:
            return _json_error('Message is too long')
        message = add_message(session, 'user', content, {'kind': 'followup'})
        if session.status in ('paused', 'waiting', 'failed', 'completed') and payload.get('resume', True):
            session.status = 'queued'
            session.control_state = ''
            session.completed_at = 0
            session.last_error = ''
            session.progress_label = 'Queued with new guidance'
            session.max_iterations = max(session.max_iterations + 15, session.iteration + 15)
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'control_state', 'completed_at', 'last_error', 'progress_label', 'max_iterations', 'updated_at'])
            emit(session, 'session.resumed', 'Session resumed with new guidance')
        return JsonResponse({'ok': True, 'message': _serialize_message(message), 'status': session.status})
    except ValueError as exc:
        return _json_error(exc)


@require_POST
def background_agent_session_control(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    session = _session_for_user(request, session_id)
    try:
        command = (_json_body(request).get('command') or '').strip().lower()
    except ValueError as exc:
        return _json_error(exc)
    if command == 'pause':
        if session.status in ('queued', 'preparing', 'running'):
            session.control_state = 'pause'
            session.progress_label = 'Pause requested'
            session.updated_at = now_ms()
            session.save(update_fields=['control_state', 'progress_label', 'updated_at'])
            emit(session, 'control.pause_requested', 'Pause requested')
    elif command == 'stop':
        if session.status in ('queued', 'paused', 'waiting'):
            session.status = 'cancelled'
            session.control_state = ''
            session.progress_label = 'Stopped'
            session.completed_at = now_ms()
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'control_state', 'progress_label', 'completed_at', 'updated_at'])
        else:
            session.control_state = 'stop'
            session.progress_label = 'Stop requested'
            session.updated_at = now_ms()
            session.save(update_fields=['control_state', 'progress_label', 'updated_at'])
        emit(session, 'control.stop_requested', 'Stop requested')
    elif command == 'resume':
        if session.status in ('paused', 'waiting', 'failed', 'completed'):
            session.status = 'queued'
            session.control_state = ''
            session.completed_at = 0
            session.last_error = ''
            session.progress_label = 'Queued to resume'
            session.max_iterations = max(session.max_iterations + 15, session.iteration + 15)
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'control_state', 'completed_at', 'last_error', 'progress_label', 'max_iterations', 'updated_at'])
            emit(session, 'session.resumed', 'Resume requested')
        elif session.status in ('queued', 'preparing', 'running'):
            return _json_error('The session is already active', 409)
        else:
            return _json_error('A cancelled session cannot be resumed', 409)
    else:
        return _json_error('Unknown control command')
    session.refresh_from_db()
    return JsonResponse({'ok': True, 'session': _serialize_session_summary(session)})


@require_POST
def background_agent_session_action(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return _json_error('Admin authentication required', 403)
    session = _session_for_user(request, session_id)
    try:
        payload = _json_body(request)
    except ValueError as exc:
        return _json_error(exc)
    action_name = (payload.get('action') or '').strip()
    if action_name not in {'push', 'open_pr', 'refresh', 'artifacts'}:
        return _json_error('Unknown action')
    if action_name in {'push', 'open_pr', 'artifacts'} and session.status in {'queued', 'preparing', 'running'}:
        return _json_error('Pause the session or wait for it to finish before delivering changes', 409)
    if action_name in {'push', 'open_pr', 'artifacts'} and not session.workspace_path:
        return _json_error('The session workspace is not ready yet', 409)
    action = BackgroundAgentAction.objects.create(
        id=uuid_str(),
        session=session,
        requested_by=request.user,
        action=action_name,
        status='queued',
        payload=json.dumps(payload.get('payload') or {}, ensure_ascii=False),
        created_at=now_ms(),
    )
    emit(session, 'action.queued', f'{action_name} queued', {'actionId': action.id, 'action': action_name})
    return JsonResponse({'ok': True, 'action': _serialize_action(action)}, status=202)


@require_GET
def background_agent_download_artifact(request, session_id, kind):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        raise Http404
    session = _session_for_user(request, session_id)
    try:
        artifact = BackgroundAgentArtifact.objects.get(session=session, kind=kind)
    except BackgroundAgentArtifact.DoesNotExist:
        raise Http404('Artifact is not available')
    path = Path(artifact.file_path).resolve()
    root = Path(getattr(settings, 'BACKGROUND_AGENT_ROOT', settings.BASE_DIR / 'background_agent_data')).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        raise Http404('Invalid artifact path')
    if not path.is_file():
        raise Http404('Artifact file is missing')
    content_type = 'application/zip' if kind == 'changes_zip' else 'text/x-diff'
    return FileResponse(path.open('rb'), as_attachment=True, filename=artifact.file_name, content_type=content_type)


def _serialize_repo(repo):
    permissions = repo.get('permissions') or {}
    owner = repo.get('owner') or {}
    return {
        'id': repo.get('id'),
        'fullName': repo.get('full_name') or '',
        'name': repo.get('name') or '',
        'owner': owner.get('login') or '',
        'private': bool(repo.get('private')),
        'archived': bool(repo.get('archived')),
        'defaultBranch': repo.get('default_branch') or 'main',
        'description': repo.get('description') or '',
        'htmlUrl': repo.get('html_url') or '',
        'updatedAt': repo.get('updated_at') or '',
        'canPush': bool(permissions.get('push') or permissions.get('maintain') or permissions.get('admin')),
    }


def _serialize_project(project):
    return {
        'id': str(project.id),
        'repoFullName': project.repo_full_name,
        'repoHtmlUrl': project.repo_html_url,
        'defaultBranch': project.default_branch,
        'preferredBaseBranch': project.preferred_base_branch or project.default_branch,
        'private': project.is_private,
        'status': project.status,
        'lastSyncedAt': project.last_synced_at,
        'lastError': project.last_error,
        'createdAt': project.created_at,
        'updatedAt': project.updated_at,
    }


def _serialize_session_summary(session):
    return {
        'id': str(session.id),
        'projectId': str(session.project_id),
        'repoFullName': session.project.repo_full_name,
        'title': session.title,
        'goal': session.goal[:2000],
        'sourceBranch': session.source_branch,
        'workBranch': session.work_branch,
        'status': session.status,
        'progress': session.progress,
        'progressLabel': session.progress_label,
        'iteration': session.iteration,
        'maxIterations': session.max_iterations,
        'provider': ({
            'id': session.bot_config_id,
            'name': session.bot_config.name,
            'provider': session.bot_config.provider,
            'model': session.bot_config.model,
        } if session.bot_config else None),
        'summary': session.summary,
        'lastError': session.last_error,
        'createdAt': session.created_at,
        'startedAt': session.started_at,
        'updatedAt': session.updated_at,
        'completedAt': session.completed_at,
    }


def _serialize_session_detail(session):
    data = _serialize_session_summary(session)
    try:
        changed_files = json.loads(session.changed_files or '[]')
    except (TypeError, json.JSONDecodeError):
        changed_files = []
    message_count = session.messages.count()
    messages_qs = list(session.messages.order_by('-created_at')[:250])
    messages_qs.reverse()
    events_qs = session.events.order_by('-id')[:200]
    actions_qs = session.actions.order_by('-created_at')[:50]
    artifacts = _serialize_artifacts(session)
    data.update({
        'baseSha': session.base_sha,
        'goal': session.goal,
        'headSha': session.head_sha,
        'changedFiles': changed_files,
        'diff': session.final_diff,
        'testSummary': session.test_summary,
        'messages': [_serialize_message(m) for m in messages_qs],
        'messageCount': message_count,
        'messagesTruncated': message_count > len(messages_qs),
        'events': [_serialize_event(e) for e in reversed(list(events_qs))],
        'actions': [_serialize_action(a) for a in actions_qs],
        'artifacts': artifacts,
    })
    return data


def _serialize_artifacts(session):
    return {a.kind: {
        'kind': a.kind,
        'fileName': a.file_name,
        'sizeBytes': a.size_bytes,
        'sha256': a.sha256,
        'downloadUrl': reverse('web:background_agent_download_artifact', args=[session.id, a.kind]),
    } for a in session.artifacts.all()}


def _serialize_message(message):
    try:
        metadata = json.loads(message.metadata or '{}')
    except (TypeError, json.JSONDecodeError):
        metadata = {}
    return {
        'id': str(message.id),
        'role': message.role,
        'content': message.content,
        'metadata': metadata,
        'createdAt': message.created_at,
    }


def _serialize_event(event):
    try:
        payload = json.loads(event.payload or '{}')
    except (TypeError, json.JSONDecodeError):
        payload = {}
    return {
        'id': event.id,
        'type': event.event_type,
        'message': event.message,
        'payload': payload,
        'createdAt': event.created_at,
    }


def _serialize_action(action):
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
