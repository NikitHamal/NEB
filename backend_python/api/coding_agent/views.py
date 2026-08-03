"""Admin views for the background coding agent.

Routes live under /admin/background-agent/. Only staff admins reach them.

Surface area:
  · Pages (rendered HTML):
      - project_list        /admin/background-agent/
      - project_new         /admin/background-agent/projects/new/
      - project_detail      /admin/background-agent/projects/<id>/
      - session_list        /admin/background-agent/sessions/
      - session_detail      /admin/background-agent/sessions/<id>/

  · AJAX endpoints (JSON, all require staff + log entry):
      - ajax_project_create     /admin/background-agent/ajax/projects/create/
      - ajax_project_delete     /admin/background-agent/ajax/projects/<id>/delete/
      - ajax_project_refresh    /admin/background-agent/ajax/projects/<id>/refresh/
      - ajax_session_create     /admin/background-agent/ajax/sessions/create/
      - ajax_session_message    /admin/background-agent/ajax/sessions/<id>/message/
      - ajax_session_control    /admin/background-agent/ajax/sessions/<id>/control/ (pause/resume/stop)
      - ajax_session_diff       /admin/background-agent/ajax/sessions/<id>/diff/
      - ajax_session_files      /admin/background-agent/ajax/sessions/<id>/files/
      - ajax_session_push       /admin/background-agent/ajax/sessions/<id>/push/
      - ajax_session_open_pr    /admin/background-agent/ajax/sessions/<id>/pr/
      - ajax_session_download   /admin/background-agent/ajax/sessions/<id>/download/  (zipped diff)
      - ajax_session_resume     /admin/background-agent/ajax/sessions/<id>/resume-text/ (when awaiting_input)
      - ajax_github_repos       /admin/background-agent/ajax/github/repos/  (repo picker)
"""
from __future__ import annotations

import io
import json
import logging
import zipfile
from pathlib import Path
from typing import Any, Dict, List

from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import get_valid_filename
from django.views.decorators.http import require_GET, require_POST

from api.models import User
from api.utils import now_ms, uuid_str

from .git_workspace import (
    fetch_default_branch,
    github_exchange_code,
    github_oauth_authorize,
    github_user,
    list_user_repos,
    open_pull_request,
    push_branch,
    search_repos,
    safe_branch_name,
)
from .models import (
    CodingAgentEvent,
    CodingAgentFileChange,
    CodingAgentMessage,
    CodingAgentProject,
    CodingAgentSession,
)
from .realtime import (
    announce_event,
    announce_message,
    announce_status,
)
from .runtime import derive_session_title
from .worker import advance_session

logger = logging.getLogger(__name__)


def _is_admin(request: HttpRequest) -> bool:
    u = getattr(request, 'user', None)
    if not (u and getattr(u, 'is_authenticated', False)):
        return False
    if getattr(u, 'is_staff', False):
        return True
    if getattr(u, 'is_admin', False):
        return True
    role = getattr(u, 'role', '')
    if isinstance(role, str) and role == 'admin':
        return True
    return False


def _api_user(request: HttpRequest) -> User:
    """Resolve the api.models.User row for the currently-authenticated user.

    NEBians uses two User tables:
      · `auth_user` (Django built-in) — what staff admins log in with via
        the `/admin/` panel.
      · `users` (`api.User`) — what the rest of the schema FKs into.

    For the coding agent we need an `api.User` row keyed by the staff admin's
    username (or `id`, if usernames collide). Created lazily on first access.
    """
    u = request.user
    if u is None or not getattr(u, 'is_authenticated', False):
        raise PermissionDenied('login required')
    username = getattr(u, 'username', None) or ''
    if username:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            pass
    uid = str(getattr(u, 'id', '') or '')
    if uid:
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
    user, _ = User.objects.get_or_create(
        id=uid or uuid_str(),
        defaults={'username': username or 'admin', 'role': 'admin'},
    )
    return user


def _resolve_owner_user(request: HttpRequest) -> User:
    """Backwards-compatible alias for `_api_user`."""
    return _api_user(request)


def _require_admin(request: HttpRequest) -> User:
    if not _is_admin(request):
        raise PermissionDenied('admin only')
    return _resolve_owner_user(request)


def _ctx(request: HttpRequest, **extra: Any) -> Dict[str, Any]:
    user = _require_admin(request)
    return {
        'request': request,
        'admin_user': user,
        'is_admin': True,
        'page_title': 'Background Coding Agent',
        **(extra or {}),
    }






@login_required
def project_list(request: HttpRequest) -> HttpResponse:
    _require_admin(request)
    projects = list(CodingAgentProject.objects.filter(owner_user=_api_user(request)).order_by('-updated_at'))
    sessions_recent = list(
        CodingAgentSession.objects.filter(project__owner_user=_api_user(request))
        .select_related('project')
        .order_by('-created_at')[:25]
    )
    return render(request, 'coding_agent/project_list.html', _ctx(
        request,
        projects=projects,
        sessions_recent=sessions_recent,
        active_tab='projects',
    ))


@login_required
def project_new(request: HttpRequest) -> HttpResponse:
    _require_admin(request)
    return render(request, 'coding_agent/project_new.html', _ctx(request, active_tab='projects'))


@login_required
def project_detail(request: HttpRequest, project_id: str) -> HttpResponse:
    _require_admin(request)
    project = CodingAgentProject.objects.filter(pk=project_id, owner_user=_api_user(request)).first()
    if not project:
        return redirect('coding_agent:project_list')
    sessions = list(CodingAgentProject.objects.get(pk=project_id).sessions.order_by('-created_at'))
    return render(request, 'coding_agent/project_detail.html', _ctx(
        request,
        project=project,
        sessions=sessions,
        active_tab='projects',
    ))


@login_required
def session_list(request: HttpRequest) -> HttpResponse:
    _require_admin(request)
    sessions = list(
        CodingAgentSession.objects.filter(project__owner_user=_api_user(request))
        .select_related('project')
        .order_by('-created_at')
    )
    return render(request, 'coding_agent/session_list.html', _ctx(request, sessions=sessions, active_tab='sessions'))


@login_required
def session_detail(request: HttpRequest, session_id: str) -> HttpResponse:
    _require_admin(request)
    session = CodingAgentSession.objects.select_related('project').filter(pk=session_id, project__owner_user=_api_user(request)).first()
    if not session:
        return redirect('coding_agent:session_list')
    messages = list(
        CodingAgentMessage.objects.filter(session=session).order_by('sequence', 'created_at')
    )
    events_recent = list(CodingAgentEvent.objects.filter(session=session).order_by('-created_at')[:60])
    events_recent.reverse()
    files_recent = list(CodingAgentFileChange.objects.filter(session=session).order_by('-created_at')[:60])
    files_recent.reverse()
    messages_initial = json.dumps([_serialize_message_in_view(m) for m in messages], ensure_ascii=False)
    files_initial = json.dumps([{
        'id': fc.id, 'path': fc.path, 'op': fc.op, 'additions': fc.additions,
        'deletions': fc.deletions, 'committed': fc.committed, 'commit_sha': fc.commit_sha,
    } for fc in files_recent], ensure_ascii=False)
    events_initial = json.dumps([{
        'event_type': ev.event_type, 'summary': ev.summary, 'detail': ev.detail,
        'created_at': ev.created_at,
    } for ev in events_recent], ensure_ascii=False)
    return render(request, 'coding_agent/session_detail.html', _ctx(
        request,
        session=session,
        messages=messages,
        events_recent=events_recent,
        files_recent=files_recent,
        messages_initial=messages_initial,
        files_initial=files_initial,
        events_initial=events_initial,
        active_tab='sessions',
    ))


@login_required
def agent_list(request: HttpRequest) -> HttpResponse:
    _require_admin(request)
    return render(request, 'coding_agent/agent_list.html', _ctx(request, active_tab='agents'))


def _serialize_message_in_view(m: CodingAgentMessage) -> Dict[str, Any]:
    attachments = []
    if getattr(m, 'attachments_json', None):
        try:
            attachments = json.loads(m.attachments_json)
        except Exception:
            pass
    return {
        'id': m.id,
        'role': m.role,
        'kind': m.kind,
        'content': m.content,
        'tool_name': m.tool_name,
        'tool_args': m.tool_args_json,
        'tool_result': m.tool_result_json,
        'tool_status': m.tool_status,
        'attachments': attachments,
        'iteration': m.iteration,
        'sequence': m.sequence,
        'created_at': m.created_at,
        'is_visible': m.is_visible,
    }




@login_required
@require_GET
def github_oauth_start(request: HttpRequest) -> HttpResponse:
    _require_admin(request)
    client_id = django_settings.GITHUB_CLIENT_ID
    if not client_id:
        return JsonResponse({'error': 'GitHub OAuth is not configured on the server.'}, status=501)
    redirect_uri = request.build_absolute_uri(reverse('coding_agent:github_oauth_callback'))
    state_obj = {'u': request.user.id, 't': now_ms(), 'n': uuid_str()}
    request.session['coding_agent_gh_state'] = state_obj
    state = state_obj['n']
    return redirect(github_oauth_authorize(client_id, redirect_uri, state, scope='repo read:user user:email'))


@login_required
@require_GET
def github_oauth_callback(request: HttpRequest) -> HttpResponse:
    _require_admin(request)
    expected = request.session.pop('coding_agent_gh_state', None)
    code = request.GET.get('code', '')
    state = request.GET.get('state', '')
    if not expected or state != expected.get('n'):
        return JsonResponse({'error': 'OAuth state mismatch.'}, status=400)
    if not code:
        return JsonResponse({'error': 'Missing OAuth code.'}, status=400)
    client_id = django_settings.GITHUB_CLIENT_ID
    client_secret = django_settings.GITHUB_CLIENT_SECRET
    redirect_uri = request.build_absolute_uri(reverse('coding_agent:github_oauth_callback'))
    try:
        token_data = github_exchange_code(client_id, client_secret, code, redirect_uri)
        access_token = token_data['access_token']
        scope = token_data.get('scope', 'repo')
        user_info = github_user(access_token)
    except Exception as e:
        logger.exception('GitHub OAuth callback failed: %s', e)
        return JsonResponse({'error': 'OAuth failed: ' + str(e)}, status=502)
    request.session['coding_agent_gh_access_token'] = access_token
    request.session['coding_agent_gh_scope'] = scope
    request.session['coding_agent_gh_login'] = user_info.get('login', '')
    return redirect(reverse('coding_agent:project_new') + '?gh=connected')




@login_required
@require_POST
def ajax_upload_attachment(request: HttpRequest) -> JsonResponse:
    _require_admin(request)
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    uploaded_file = request.FILES['file']
    filename = get_valid_filename(uploaded_file.name)
    file_id = uuid_str()[:8]
    ext = Path(filename).suffix.lower()
    save_filename = f"{file_id}_{filename}"
    
    upload_dir = Path(django_settings.MEDIA_ROOT) / 'coding_agent_uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)
    full_path = upload_dir / save_filename
    
    with open(full_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
            
    media_url = f"{django_settings.MEDIA_URL.rstrip('/')}/coding_agent_uploads/{save_filename}"
    is_image = ext in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp'}
    
    attachment_info = {
        'id': save_filename,
        'name': filename,
        'size': uploaded_file.size,
        'path': str(full_path),
        'url': media_url,
        'is_image': is_image,
        'ext': ext,
    }
    return JsonResponse({'ok': True, 'attachment': attachment_info})


@login_required
@require_GET
def ajax_session_workspace_files(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    if not session.workspace_path or not Path(session.workspace_path).exists():
        return JsonResponse({'files': [], 'error': 'workspace not initialized'})
        
    workspace = Path(session.workspace_path)
    file_list = []
    for p in workspace.rglob('*'):
        if p.is_file() and not any(part.startswith('.') for part in p.relative_to(workspace).parts):
            rel = str(p.relative_to(workspace))
            file_list.append({
                'path': rel,
                'size': p.stat().st_size,
                'is_md': rel.lower().endswith('.md'),
            })
    file_list.sort(key=lambda x: x['path'])
    return JsonResponse({'files': file_list[:500]})


@login_required
@require_GET
def ajax_session_file_content(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    rel_path = request.GET.get('path', '').strip()
    if not rel_path or not session.workspace_path:
        return JsonResponse({'error': 'path required'}, status=400)
        
    workspace = Path(session.workspace_path).resolve()
    target_path = (workspace / rel_path).resolve()
    
    if not str(target_path).startswith(str(workspace)) or not target_path.exists() or not target_path.is_file():
        return JsonResponse({'error': 'file not found or path escape'}, status=404)
        
    ext = target_path.suffix.lower()
    is_image = ext in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp'}
    
    if is_image:
        return JsonResponse({
            'path': rel_path,
            'is_image': True,
            'url': f"{django_settings.MEDIA_URL.rstrip('/')}/workspace/{session.id}/{rel_path}",
            'ext': ext,
        })
        
    try:
        content = target_path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return JsonResponse({'error': f'failed to read file: {e}'}, status=500)
        
    return JsonResponse({
        'path': rel_path,
        'is_image': False,
        'content': content,
        'ext': ext,
        'is_md': ext == '.md',
        'lines': len(content.splitlines()),
    })


@login_required
@require_GET
def ajax_session_logs(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
        
    events = list(CodingAgentEvent.objects.filter(session=session).order_by('created_at'))
    tool_calls = list(session.tool_calls.order_by('created_at'))
    
    logs = []
    for ev in events:
        logs.append({
            'timestamp': ev.created_at,
            'type': 'event',
            'category': ev.event_type,
            'text': f"[{ev.event_type.upper()}] {ev.summary}" + (f"\n{ev.detail}" if ev.detail else ""),
        })
    for tc in tool_calls:
        logs.append({
            'timestamp': tc.created_at,
            'type': 'tool',
            'category': tc.name,
            'text': f"$ tool execute: {tc.name} ({tc.status}, {tc.duration_ms}ms)\nArgs: {tc.args_json}\nOutput: {tc.result_text[:1000]}",
        })
        
    logs.sort(key=lambda x: x['timestamp'])
    return JsonResponse({'logs': logs, 'status': session.status, 'branch': session.branch})


@login_required
@require_GET
def ajax_github_repos(request: HttpRequest) -> JsonResponse:
    _require_admin(request)
    token = request.session.get('coding_agent_gh_access_token')
    query = request.GET.get('q', '').strip()
    if not token:
        return JsonResponse({'error': 'GitHub account not connected. Click "Connect GitHub" first.'}, status=400)
    try:
        if query:
            repos = search_repos(token, query)
        else:
            repos = list_user_repos(request.user, token, refresh=request.GET.get('refresh') == '1')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)
    return JsonResponse({'repos': repos})


@login_required
@require_POST
def ajax_project_create(request: HttpRequest) -> JsonResponse:
    admin = _require_admin(request)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    repo_full_name = (body.get('repo_full_name') or '').strip()
    if '/' not in repo_full_name:
        return JsonResponse({'error': 'repo_full_name required'}, status=400)
    owner_login, repo_name = repo_full_name.split('/', 1)
    access_token = request.session.pop('coding_agent_gh_access_token', '')
    scope = request.session.pop('coding_agent_gh_scope', 'repo')
    if not access_token:
        return JsonResponse({'error': 'GitHub account not connected.'}, status=400)
    project, created = CodingAgentProject.objects.get_or_create(
        owner_user=admin,
        repo_full_name=repo_full_name,
        defaults={
            'id': uuid_str(),
            'repo_owner': owner_login,
            'repo_name': repo_name,
            'access_token': access_token,
            'token_scope': scope,
            'github_user_login': request.session.pop('coding_agent_gh_login', '') or owner_login,
        },
    )
    if not created:
        project.access_token = access_token
        project.token_scope = scope
        project.repo_owner = owner_login
        project.repo_name = repo_name
        project.save()
    try:
        fetch_default_branch(project)
        ensure_clone(project)
    except Exception as e:
        return JsonResponse({'error': 'Repo fetch failed: ' + str(e)}, status=502)
    request.session.pop('coding_agent_gh_login', None)
    return JsonResponse({'ok': True, 'project_id': project.id, 'created': created})


@login_required
@require_POST
def ajax_project_refresh(request: HttpRequest, project_id: str) -> JsonResponse:
    admin = _require_admin(request)
    project = CodingAgentProject.objects.filter(pk=project_id, owner_user=admin).first()
    if not project:
        return JsonResponse({'error': 'project not found'}, status=404)
    try:
        ensure_clone(project, refresh=True)
        fetch_default_branch(project)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)
    return JsonResponse({'ok': True})


@login_required
@require_POST
def ajax_project_delete(request: HttpRequest, project_id: str) -> JsonResponse:
    admin = _require_admin(request)
    project = CodingAgentProject.objects.filter(pk=project_id, owner_user=admin).first()
    if not project:
        return JsonResponse({'error': 'project not found'}, status=404)
    project.is_archived = True
    project.save(update_fields=['is_archived', 'updated_at'])
    return JsonResponse({'ok': True})




@login_required
@require_POST
def ajax_session_create(request: HttpRequest) -> JsonResponse:
    admin = _require_admin(request)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    project_id = body.get('project_id')
    task = (body.get('task') or '').strip()
    title = (body.get('title') or '').strip()
    provider = (body.get('provider') or 'qwen').strip()
    model = (body.get('model') or 'qwen3.8-max').strip()
    attachments = body.get('attachments') or []
    attachments_json = json.dumps(attachments, ensure_ascii=False) if attachments else '[]'
    
    if not project_id or not task:
        return JsonResponse({'error': 'project_id and task are required'}, status=400)
    project = CodingAgentProject.objects.filter(pk=project_id, owner_user=admin).first()
    if not project:
        return JsonResponse({'error': 'project not found'}, status=404)
    session = CodingAgentSession.objects.create(
        id=uuid_str(),
        project=project,
        title=title or derive_session_title(task),
        task=task,
        status=CodingAgentSession.STATUS_QUEUED,
        provider=provider,
        model=model,
        assigned_to=admin,
        branch=safe_branch_name(title or task),
        created_at=now_ms(),
        updated_at=now_ms(),
        last_activity_at=now_ms(),
    )
    if attachments_json != '[]':
        user_msg = CodingAgentMessage.objects.filter(session=session, role=CodingAgentMessage.ROLE_USER).first()
        if user_msg:
            user_msg.attachments_json = attachments_json
            user_msg.save(update_fields=['attachments_json'])
            
    CodingAgentEvent.objects.create(
        id=uuid_str(),
        session=session,
        event_type=CodingAgentEvent.EVENT_STATUS,
        summary='Session queued',
        detail='Task received from admin UI.',
        created_at=now_ms(),
    )
    try:
        advance_session(session.id, max_steps=1)
    except Exception as e:
        logger.exception('Immediate drain failed: %s', e)
    return JsonResponse({'ok': True, 'session_id': session.id, 'branch': session.branch})


@login_required
@require_POST
def ajax_session_message(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    content = (body.get('content') or '').strip()
    attachments = body.get('attachments') or []
    attachments_json = json.dumps(attachments, ensure_ascii=False) if attachments else '[]'
    if not content and not attachments:
        return JsonResponse({'error': 'content or attachments required'}, status=400)
    last = CodingAgentMessage.objects.filter(session=session).order_by('-sequence').values_list('sequence', flat=True).first() or 0
    msg = CodingAgentMessage.objects.create(
        id=uuid_str(),
        session=session,
        role=CodingAgentMessage.ROLE_USER,
        kind=CodingAgentMessage.KIND_MESSAGE,
        content=content,
        attachments_json=attachments_json,
        iteration=session.iterations,
        sequence=int(last) + 1,
        created_at=now_ms(),
    )
    session.refresh_from_db()
    if session.status in {CodingAgentSession.STATUS_FINISHED, CodingAgentSession.STATUS_FAILED, CodingAgentSession.STATUS_STOPPED, CodingAgentSession.STATUS_PR_OPENED, CodingAgentSession.STATUS_AWAITING_INPUT}:
        session.status = CodingAgentSession.STATUS_RUNNING
        session.error_message = ''
        session.save(update_fields=['status', 'error_message', 'updated_at'])
    elif session.status == CodingAgentSession.STATUS_PAUSED:
        session.status = CodingAgentSession.STATUS_RUNNING
        session.paused_at = 0
        session.save(update_fields=['status', 'paused_at', 'updated_at'])
    announce_message(session.id, _serialize_message(msg))
    CodingAgentEvent.objects.create(
        id=uuid_str(),
        session=session,
        event_type=CodingAgentEvent.EVENT_INTERRUPT,
        summary='User follow-up',
        detail=content[:5000],
        created_at=now_ms(),
    )
    try:
        advance_session(session.id, max_steps=1)
    except Exception as e:
        logger.exception('immediate drain failed: %s', e)
    return JsonResponse({'ok': True, 'message_id': msg.id})


@login_required
@require_POST
def ajax_session_control(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    action = (body.get('action') or '').strip().lower()
    if action not in {'pause', 'resume', 'stop'}:
        return JsonResponse({'error': 'action must be pause/resume/stop'}, status=400)
    now = now_ms()
    if action == 'pause':
        if session.status in {CodingAgentSession.STATUS_RUNNING, CodingAgentSession.STATUS_SETUP}:
            session.status = CodingAgentSession.STATUS_PAUSED
            session.paused_at = now
            session.save(update_fields=['status', 'paused_at', 'updated_at'])
            CodingAgentEvent.objects.create(
                id=uuid_str(), session=session, event_type=CodingAgentEvent.EVENT_STATUS,
                summary='Paused', detail='Admin paused the session.', created_at=now,
            )
    elif action == 'resume':
        if session.status == CodingAgentSession.STATUS_PAUSED:
            session.status = CodingAgentSession.STATUS_RUNNING
            session.paused_at = 0
            session.save(update_fields=['status', 'paused_at', 'updated_at'])
            CodingAgentEvent.objects.create(
                id=uuid_str(), session=session, event_type=CodingAgentEvent.EVENT_STATUS,
                summary='Resumed', detail='Admin resumed the session.', created_at=now,
            )
            try:
                advance_session(session.id, max_steps=1)
            except Exception as e:
                logger.exception('resume drain: %s', e)
    elif action == 'stop':
        session.status = CodingAgentSession.STATUS_STOPPED
        session.stopped_at = now
        session.finished_at = now
        session.save(update_fields=['status', 'stopped_at', 'finished_at', 'updated_at'])
        CodingAgentEvent.objects.create(
            id=uuid_str(), session=session, event_type=CodingAgentEvent.EVENT_STATUS,
            summary='Stopped by admin', detail='User pressed Stop.', created_at=now,
        )
    announce_status(session.id, session.status, event=action)
    return JsonResponse({'ok': True, 'status': session.status})


@login_required
@require_POST
def ajax_session_resume(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    answer = (body.get('answer') or '').strip()
    if not answer:
        return JsonResponse({'error': 'answer required'}, status=400)
    last = CodingAgentMessage.objects.filter(session=session).order_by('-sequence').values_list('sequence', flat=True).first() or 0
    CodingAgentMessage.objects.create(
        id=uuid_str(),
        session=session,
        role=CodingAgentMessage.ROLE_USER,
        kind=CodingAgentMessage.KIND_MESSAGE,
        content=answer,
        iteration=session.iterations,
        sequence=int(last) + 1,
        created_at=now_ms(),
    )
    session.status = CodingAgentSession.STATUS_RUNNING
    session.error_message = ''
    session.save(update_fields=['status', 'error_message', 'updated_at'])
    CodingAgentEvent.objects.create(
        id=uuid_str(), session=session, event_type=CodingAgentEvent.EVENT_INTERRUPT,
        summary='User answered follow-up', detail=answer[:5000], created_at=now_ms(),
    )
    try:
        advance_session(session.id, max_steps=1)
    except Exception as e:
        logger.exception('resume drain: %s', e)
    return JsonResponse({'ok': True})




@login_required
@require_GET
def ajax_session_files(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    changes = list(CodingAgentFileChange.objects.filter(session=session).order_by('-created_at'))
    return JsonResponse({
        'changes': [{
            'id': c.id,
            'path': c.path,
            'op': c.op,
            'additions': c.additions,
            'deletions': c.deletions,
            'committed': c.committed,
            'commit_sha': c.commit_sha,
            'patch': c.patch,
            'created_at': c.created_at,
        } for c in changes],
        'branch': session.branch,
        'base_ref': session.base_ref,
        'has_workspace': bool(session.workspace_path),
    })


@login_required
@require_GET
def ajax_session_diff(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    if not session.workspace_path:
        return JsonResponse({'diff': '', 'error': 'no workspace yet'})
    import subprocess as _sp
    proc = _sp.run(
        ['git', '-C', session.workspace_path, 'diff', '--stat', '--patch', f'origin/{session.project.default_branch}...{session.branch}'],
        capture_output=True, text=True, timeout=30,
    )
    return JsonResponse({
        'diff': proc.stdout,
        'branch': session.branch,
        'base': session.project.default_branch,
        'error': proc.stderr if proc.returncode != 0 else '',
    })


def _build_zip(session: CodingAgentSession) -> Tuple[bytes, str]:
    import subprocess as _sp
    import io

    repo_path = session.workspace_path
    if not repo_path or not Path(repo_path).exists():
        raise RuntimeError('Workspace not present. The agent has not finished setup yet.')

    diff_proc = _sp.run(
        ['git', '-C', repo_path, 'diff', '--binary', f'origin/{session.project.default_branch}...{session.branch}'],
        capture_output=True, text=False, timeout=60,
    )
    files_proc = _sp.run(
        ['git', '-C', repo_path, 'diff', '--name-only', f'origin/{session.project.default_branch}...{session.branch}'],
        capture_output=True, text=True, timeout=30,
    )

    buf = io.BytesIO()
    safe_name = get_valid_filename(session.title or session.task[:30]) or 'session'
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.writestr('README.txt', 'Diff against %s for branch %s\nSession: %s\nRepo: %s\nAuthor: %s\n' % (
            session.project.default_branch, session.branch, session.id,
            session.project.repo_full_name, session.project.github_user_login or '',
        ))
        zf.writestr('session.json', json.dumps({
            'id': session.id,
            'title': session.title,
            'task': session.task,
            'branch': session.branch,
            'base_branch': session.project.default_branch,
            'base_ref': session.base_ref,
            'status': session.status,
            'summary': session.summary,
            'provider': session.provider,
            'model': session.model,
            'iterations': session.iterations,
            'created_at': session.created_at,
            'finished_at': session.finished_at,
        }, ensure_ascii=False, indent=2))
        zf.writestr('diff.patch', diff_proc.stdout)
        try:
            log_proc = _sp.run(
                ['git', '-C', repo_path, 'log', '--pretty=format:%h%x09%an%x09%ad%x09%s', f'origin/{session.project.default_branch}..{session.branch}'],
                capture_output=True, text=True, timeout=20,
            )
            zf.writestr('commits.log', log_proc.stdout)
        except Exception:
            pass
        for fname in [ln for ln in files_proc.stdout.splitlines() if ln]:
            full = Path(repo_path) / fname
            if not full.exists() or full.is_dir():
                continue
            try:
                zf.write(full, arcname='files/' + fname)
            except OSError:
                continue
    return buf.getvalue(), 'coding-agent-' + safe_name + '-' + session.id[:8] + '.zip'


@login_required
@require_GET
def ajax_session_download(request: HttpRequest, session_id: str) -> HttpResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    try:
        data, filename = _build_zip(session)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    resp = HttpResponse(data, content_type='application/zip')
    resp['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return resp


@login_required
@require_POST
def ajax_session_push(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    if not session.workspace_path:
        return JsonResponse({'error': 'session has no workspace'}, status=400)
    try:
        info = push_branch(session.project, session)
        session.push_state = 'pushed'
        session.save(update_fields=['push_state', 'updated_at'])
        CodingAgentEvent.objects.create(
            id=uuid_str(), session=session, event_type=CodingAgentEvent.EVENT_PUSH,
            summary='Branch pushed to origin/' + session.branch,
            detail=json.dumps(info, ensure_ascii=False)[:4000],
            created_at=now_ms(),
        )
    except Exception as e:
        session.push_state = 'push_failed'
        session.error_message = ('Push failed: ' + str(e))[:4000]
        session.save(update_fields=['push_state', 'error_message', 'updated_at'])
        return JsonResponse({'error': str(e)}, status=502)
    announce_event(session.id, {'type': 'push', 'branch': session.branch, 'remote_sha': info.get('remote_sha', '')})
    return JsonResponse({'ok': True, 'remote_sha': info.get('remote_sha', '')})


@login_required
@require_POST
def ajax_session_open_pr(request: HttpRequest, session_id: str) -> JsonResponse:
    admin = _require_admin(request)
    session = CodingAgentSession.objects.filter(pk=session_id, project__owner_user=admin).first()
    if not session:
        return JsonResponse({'error': 'session not found'}, status=404)
    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    title = (body.get('title') or session.title or session.task[:80]).strip()[:200]
    body_text = (body.get('body') or _default_pr_body(session)).strip()[:6000]
    if session.push_state != 'pushed':
        try:
            push_branch(session.project, session)
            session.push_state = 'pushed'
            session.save(update_fields=['push_state', 'updated_at'])
        except Exception as e:
            session.push_state = 'push_failed'
            session.error_message = ('Push failed: ' + str(e))[:4000]
            session.save(update_fields=['push_state', 'error_message', 'updated_at'])
            return JsonResponse({'error': 'Push failed: ' + str(e)}, status=502)
    try:
        info = open_pull_request(session.project, session, title=title, body=body_text)
        session.pr_url = info.get('url') or ''
        session.pr_number = int(info.get('number') or 0)
        session.status = CodingAgentSession.STATUS_PR_OPENED
        session.finished_at = now_ms()
        session.save(update_fields=['pr_url', 'pr_number', 'status', 'finished_at', 'updated_at'])
        CodingAgentEvent.objects.create(
            id=uuid_str(), session=session, event_type=CodingAgentEvent.EVENT_PR,
            summary='Pull request opened: #' + str(session.pr_number),
            detail=session.pr_url,
            payload_json=json.dumps(info, ensure_ascii=False)[:4000],
            created_at=now_ms(),
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)
    announce_event(session.id, {'type': 'pr', 'url': session.pr_url, 'number': session.pr_number})
    return JsonResponse({'ok': True, 'pr_url': session.pr_url, 'pr_number': session.pr_number})


def _default_pr_body(session: CodingAgentSession) -> str:
    changes = CodingAgentFileChange.objects.filter(session=session).order_by('created_at')
    body_parts = [
        '## Summary',
        '',
        session.summary or ('Automated change proposed by the NEBians Background Coding Agent.'),
        '',
        '## Task',
        '',
        session.task,
        '',
        '## Changes',
        '',
    ]
    for c in changes:
        body_parts.append('- `%s` (%s, +%d/-%d)' % (c.path, c.get_op_display(), c.additions, c.deletions))
    body_parts.extend([
        '',
        '## Stats',
        '- Model: ' + (session.model or '?') + ' via ' + (session.provider or '?'),
        '- Iterations: ' + str(session.iterations),
        '- Session ID: ' + session.id,
    ])
    return '\n'.join(body_parts)




def _serialize_message(m: CodingAgentMessage) -> Dict[str, Any]:
    attachments = []
    if getattr(m, 'attachments_json', None):
        try:
            attachments = json.loads(m.attachments_json)
        except Exception:
            pass
    return {
        'id': m.id,
        'role': m.role,
        'kind': m.kind,
        'content': m.content,
        'tool_name': m.tool_name,
        'tool_args': m.tool_args_json,
        'tool_result': m.tool_result_json,
        'tool_status': m.tool_status,
        'attachments': attachments,
        'iteration': m.iteration,
        'sequence': m.sequence,
        'created_at': m.created_at,
        'is_visible': m.is_visible,
    }
