from __future__ import annotations

import json
import logging
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from api.background_agent.attachments import save_uploads
from api.background_agent.crypto import decrypt_secret
from api.background_agent.events import add_message, emit
from api.background_agent.github import GitHubClient, GitHubError
from api.background_agent.oauth import SESSION_STATE_KEY, build_authorize_url, make_state
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
from .background_agent_file_views import (
    background_agent_session_file,
    background_agent_session_files,
    background_agent_session_preview,
)
from .background_agent_serializers import (
    serialize_action as _serialize_action,
    serialize_artifacts as _serialize_artifacts,
    serialize_event as _serialize_event,
    serialize_message as _serialize_message,
    serialize_project as _serialize_project,
    serialize_repo as _serialize_repo,
    serialize_session_detail as _serialize_session_detail,
    serialize_session_summary as _serialize_session_summary,
)
from .background_agent_auth import (
    authenticate_bg_admin,
    get_bg_admin,
    login_bg_admin,
    logout_bg_admin,
    require_bg_admin,
    require_bg_admin_json,
)

logger = logging.getLogger(__name__)


def _json_body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError('Invalid JSON request body')


def _json_error(message, status=400):
    return JsonResponse({'ok': False, 'error': str(message)}, status=status)


def _request_payload(request):
    content_type = (request.content_type or '').lower()
    if 'application/json' in content_type:
        return _json_body(request)
    return request.POST.dict()


def _qwen_provider():
    return BotConfig.objects.filter(
        enabled=True, provider='qwen', model__iexact='qwen3.7-plus',
    ).first()


def _admin(request):
    """The signed-in platform admin (api.User). Caller has already authorized."""
    return get_bg_admin(request)


def _credential(request, required=False):
    admin = _admin(request)
    credential = BackgroundAgentCredential.objects.filter(admin_user=admin).first()
    if required and (not credential or not credential.is_connected):
        raise GitHubError('Connect a GitHub account first')
    return credential


def _github_client(request):
    credential = _credential(request, required=True)
    return GitHubClient(decrypt_secret(credential.encrypted_access_token)), credential


def _project_for_admin(request, project_id):
    admin = _admin(request)
    try:
        return BackgroundAgentProject.objects.select_related('credential').get(pk=project_id, admin_user=admin)
    except BackgroundAgentProject.DoesNotExist:
        raise Http404('Project not found')


def _session_for_admin(request, session_id):
    admin = _admin(request)
    try:
        return BackgroundAgentSession.objects.select_related(
            'project', 'project__credential', 'bot_config'
        ).get(pk=session_id, admin_user=admin)
    except BackgroundAgentSession.DoesNotExist:
        raise Http404('Session not found')


def _absolute_https_uri(request, route_name, args=None):
    uri = request.build_absolute_uri(reverse(route_name, args=args))
    if request.headers.get('X-Forwarded-Proto') == 'https' and uri.startswith('http://'):
        uri = 'https://' + uri[len('http://'):]
    return uri


def _base_context(request, **extra):
    admin = get_bg_admin(request)
    ctx = {
        'csp_nonce': getattr(request, 'csp_nonce', ''),
        'bg_admin': {
            'username': admin.username,
            'display_name': admin.display_name or admin.username,
            'photo_url': admin.photo_url or '',
        } if admin else None,
    }
    ctx.update(extra)
    return ctx



def background_agent_login(request):
    """Standalone sign-in: username OR email + password, platform admins only."""
    admin = get_bg_admin(request)
    if admin:
        return redirect(request.GET.get('next') or 'web:background_agent')
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next') or reverse('web:background_agent')
        # Only allow same-origin relative redirects.
        if not (str(next_url).startswith('/') and not str(next_url).startswith('//')):
            next_url = reverse('web:background_agent')
        user, error = authenticate_bg_admin(identifier, password)
        if user:
            login_bg_admin(request, user)
            return redirect(next_url)
        return render(request, 'background_agent/login.html', {
            'csp_nonce': getattr(request, 'csp_nonce', ''),
            'error': error or 'Sign in failed.',
            'next': next_url,
        })
    return render(request, 'background_agent/login.html', {
        'csp_nonce': getattr(request, 'csp_nonce', ''),
        'next': request.GET.get('next', ''),
    })


def background_agent_logout(request):
    logout_bg_admin(request)
    return redirect('web:background_agent_login')



@never_cache
@require_GET
def background_agent_page(request):
    redirect_response = require_bg_admin(request)
    if redirect_response:
        return redirect_response
    credential = _credential(request)
    return render(request, 'background_agent/dashboard.html', _base_context(request,
        github_connected=bool(credential and credential.is_connected),
        github_login=credential.github_login if credential else '',
    ))


@never_cache
@require_GET
def background_agent_session_page(request, session_id):
    """Dedicated, full-screen session view (separate from the dashboard)."""
    redirect_response = require_bg_admin(request)
    if redirect_response:
        return redirect_response
    session = _session_for_admin(request, session_id)
    credential = _credential(request)
    return render(request, 'background_agent/session.html', _base_context(request,
        session_id=str(session.id),
        session_title=session.title or (session.goal[:80] + '…' if len(session.goal) > 80 else session.goal),
        github_connected=bool(credential and credential.is_connected),
    ))



@require_GET
def background_agent_github_connect(request):
    redirect_response = require_bg_admin(request)
    if redirect_response:
        return redirect_response
    if not (getattr(settings, 'BACKGROUND_AGENT_GITHUB_CLIENT_ID', '') or getattr(settings, 'GITHUB_CLIENT_ID', '')):
        messages.error(request, 'GitHub OAuth is not configured.')
        return redirect('web:background_agent')
    admin = _admin(request)
    state = make_state(admin.id)
    request.session[SESSION_STATE_KEY] = state
    request.session.modified = True
    # Reuse the main app's registered callback URL — single redirect URI.
    redirect_uri = _absolute_https_uri(request, 'web:github_callback')
    return redirect(build_authorize_url(state=state, redirect_uri=redirect_uri))


@require_POST
def background_agent_github_disconnect(request):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    credential = _credential(request)
    if credential:
        credential.encrypted_access_token = ''
        credential.revoked_at = now_ms()
        credential.updated_at = now_ms()
        credential.save(update_fields=['encrypted_access_token', 'revoked_at', 'updated_at'])
    return JsonResponse({'ok': True})



@never_cache
@require_GET
def background_agent_state(request):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    admin = _admin(request)
    credential = _credential(request)
    projects = BackgroundAgentProject.objects.filter(admin_user=admin).order_by('-updated_at')[:100]
    sessions = BackgroundAgentSession.objects.filter(admin_user=admin).select_related('project', 'bot_config').order_by('-created_at')[:100]
    provider = _qwen_provider()
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
        'model': {
            'provider': 'qwen',
            'model': 'qwen3.7-plus',
            'label': 'Qwen 3.7 Plus',
            'configured': bool(provider),
        },
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
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
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
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
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
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
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
            admin_user=_admin(request),
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
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    try:
        payload = _request_payload(request)
        project = _project_for_admin(request, payload.get('projectId'))
        goal = (payload.get('goal') or '').strip()
        if len(goal) < 10:
            return _json_error('Describe the coding task in at least 10 characters')
        source_branch = (payload.get('sourceBranch') or project.preferred_base_branch or project.default_branch).strip()
        provider = _qwen_provider()
        if not provider:
            return _json_error('Enable a Qwen provider configuration before starting a task', 409)
        title = (payload.get('title') or goal.splitlines()[0])[:255]
        now = now_ms()
        session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=_admin(request),
            bot_config=provider,
            title=title,
            goal=goal,
            source_branch=source_branch,
            status='queued',
            progress=0,
            progress_label='Queued for worker',
            max_iterations=0,
            context_window_tokens=int(getattr(settings, 'BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS', 131072)),
            created_at=now,
            updated_at=now,
        )
        message = add_message(session, 'user', goal, {'kind': 'initial_goal'})
        attachments = save_uploads(session, message, request.FILES.getlist('files'))
        emit(session, 'session.queued', 'Task queued for the background worker', {
            'repository': project.repo_full_name,
            'sourceBranch': source_branch,
            'provider': 'qwen/qwen3.7-plus',
            'attachmentCount': len(attachments),
        })
        return JsonResponse({'ok': True, 'session': _serialize_session_detail(session)}, status=201)
    except (ValueError, Http404) as exc:
        return _json_error(exc, 400)


@require_GET
def background_agent_session_detail(request, session_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
    return JsonResponse({'ok': True, 'session': _serialize_session_detail(session)})


@require_GET
def background_agent_session_events(request, session_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
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
        for message in session.messages.filter(id__in=message_ids).prefetch_related('attachments')
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
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
    try:
        payload = _request_payload(request)
        content = (payload.get('content') or '').strip()
        uploads = request.FILES.getlist('files')
        if not content and not uploads:
            return _json_error('Add a message or attachment')
        if len(content) > 50000:
            return _json_error('Message is too long')
        message_content = content or 'Review the attached files as additional task context.'
        message = add_message(session, 'user', message_content, {'kind': 'followup'})
        attachments = save_uploads(session, message, uploads)
        if session.status in ('paused', 'waiting', 'failed', 'completed') and str(payload.get('resume', 'true')).lower() != 'false':
            session.status = 'queued'
            session.control_state = ''
            session.completed_at = 0
            session.last_error = ''
            session.progress_label = 'Queued with new guidance'
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'control_state', 'completed_at', 'last_error', 'progress_label', 'updated_at'])
            emit(session, 'session.resumed', 'Session resumed with new guidance')
        return JsonResponse({
            'ok': True,
            'message': _serialize_message(message),
            'attachmentCount': len(attachments),
            'status': session.status,
        })
    except ValueError as exc:
        return _json_error(exc)


@require_POST
def background_agent_session_control(request, session_id):
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
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
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'control_state', 'completed_at', 'last_error', 'progress_label', 'updated_at'])
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
    guard = require_bg_admin_json(request)
    if guard:
        return guard[1]
    session = _session_for_admin(request, session_id)
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
        requested_by=_admin(request),
        action=action_name,
        status='queued',
        payload=json.dumps(payload.get('payload') or {}, ensure_ascii=False),
        created_at=now_ms(),
    )
    emit(session, 'action.queued', f'{action_name} queued', {'actionId': action.id, 'action': action_name})
    return JsonResponse({'ok': True, 'action': _serialize_action(action)}, status=202)


@require_GET
def background_agent_download_artifact(request, session_id, kind):
    redirect_response = require_bg_admin(request)
    if redirect_response:
        raise Http404
    session = _session_for_admin(request, session_id)
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


