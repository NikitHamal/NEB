"""Web views for the Background Coding Agent admin pages.

Accessible only for admin (staff) users. Provides:
- /backgroundagent/ — dashboard listing projects and tasks
- /backgroundagent/github-connect/ — GitHub OAuth with repo scope
- /backgroundagent/github/callback/ — OAuth callback storing the token
- /backgroundagent/project/new/ — create a new project (connect a repo)
- /backgroundagent/project/<id>/ — project detail with tasks
- /backgroundagent/task/<id>/ — task session detail with chat/logs/diff
- AJAX endpoints for task CRUD, chat, download zip, push to GitHub, create PR
"""
import json
import os
import tempfile

from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .view_helpers import (
    _is_staff_admin, _require_staff_admin, _https_redirect_uri,
    redirect as django_redirect, cache, now_ms, User, Resource, Post,
)

from api.models import CodingProject, CodingTask, CodingTaskMessage, CodingActionLog
from api.coding_agent.queue import (
    enqueue_task, serialize_task, serialize_message, serialize_action_log,
    mark_running, mark_paused, mark_completed, mark_failed, mark_stopped,
    update_iteration, log_action, get_pending_tasks,
)
from api.coding_agent.engine import add_user_message, _encrypt_token, _decrypt_token
from api.coding_agent.git_manager import (
    generate_branch_name, get_full_diff, get_diff_summary, create_zip_archive,
    commit_all, push_branch, create_pull_request, get_changed_files,
)
from api.utils import now_ms as _now_ms


def ba_dashboard(request):
    """Background agent dashboard — list all projects and recent tasks."""
    r = _require_staff_admin(request)
    if r:
        return r

    projects = CodingProject.objects.all().order_by('-updated_at')[:20]
    tasks = CodingTask.objects.all().order_by('-updated_at')[:30]

    stats = {
        'total_projects': CodingProject.objects.count(),
        'active_tasks': CodingTask.objects.filter(status__in=['queued', 'running', 'paused']).count(),
        'completed_tasks': CodingTask.objects.filter(status='completed').count(),
        'failed_tasks': CodingTask.objects.filter(status='failed').count(),
    }

    github_connected = bool(getattr(settings, 'GITHUB_CLIENT_ID', ''))
    admin_token = _get_admin_github_token(request)

    return render(request, 'admin_panel/background_agent.html', {
        'is_admin': True,
        'active_page': 'background_agent',
        'projects': [_serialize_project(p) for p in projects],
        'tasks': [serialize_task(t) for t in tasks],
        'stats': stats,
        'github_connected': github_connected,
        'github_authorized': bool(admin_token),
        'providers': _get_providers(),
    })


def ba_github_connect(request):
    """Redirect to GitHub OAuth with repo scope for the coding agent."""
    r = _require_staff_admin(request)
    if r:
        return r

    client_id = getattr(settings, 'GITHUB_CLIENT_ID', '')
    if not client_id:
        return HttpResponse('GitHub OAuth is not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in the environment.', status=501)

    redirect_uri = _https_redirect_uri(request, '/auth/github/callback/')
    state = 'ba_connect'
    authorize_url = (
        f'https://github.com/login/oauth/authorize'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&scope=repo,read:user,user:email'
        f'&state={state}'
    )
    return redirect(authorize_url)


def ba_github_callback(request):
    """Handle GitHub OAuth callback — store the token in the admin session."""
    r = _require_staff_admin(request)
    if r:
        return r

    code = request.GET.get('code')
    state = request.GET.get('state', '')
    if not code:
        return redirect('web:ba_dashboard')

    if state != 'ba_connect':
        return HttpResponse('Invalid state parameter.', status=400)

    import requests as _req
    token_url = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': _https_redirect_uri(request, '/auth/github/callback/'),
    }
    try:
        resp = _req.post(token_url, json=data, headers={'Accept': 'application/json'}, timeout=10)
        token_data = resp.json()
    except Exception as e:
        return HttpResponse(f'Failed to exchange GitHub code: {e}', status=502)

    access_token = token_data.get('access_token')
    if not access_token:
        return HttpResponse('Failed to get GitHub access token.', status=502)

    try:
        user_resp = _req.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
            timeout=10,
        )
        github_user = user_resp.json()
    except Exception:
        github_user = {}

    request.session['ba_github_token'] = _encrypt_token(access_token)
    request.session['ba_github_user'] = {
        'login': github_user.get('login', ''),
        'name': github_user.get('name', ''),
        'avatar_url': github_user.get('avatar_url', ''),
    }

    return redirect('web:ba_dashboard')


def ba_project_create(request):
    """Create a new coding project (connect a GitHub repo)."""
    r = _require_staff_admin(request)
    if r:
        return r

    if request.method == 'POST':
        # Load body from JSON if application/json, otherwise fall back to POST dict
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except Exception:
                data = {}
        else:
            data = request.POST

        repo_url = data.get('repo_url', '').strip()
        repo_full_name = data.get('repo_full_name', '').strip()
        default_branch = data.get('default_branch', 'main').strip() or 'main'

        if not repo_url:
            return JsonResponse({'error': 'Repository URL is required'}, status=400)

        if not repo_full_name:
            parts = repo_url.rstrip('/').split('/')
            if len(parts) >= 2:
                repo_full_name = f'{parts[-2]}/{parts[-1]}'
            else:
                repo_full_name = repo_url

        if repo_full_name.endswith('.git'):
            repo_full_name = repo_full_name[:-4]
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]

        token = _get_admin_github_token(request)
        encrypted_token = _encrypt_token(token) if token else ''

        try:
            admin_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            from api.utils import now_ms as _now_ms
            admin_user = User.objects.create(
                id=f"admin_{request.user.username}",
                username=request.user.username,
                email=getattr(request.user, 'email', '') or f"{request.user.username}@nebians.com",
                display_name=f"Admin {request.user.username.capitalize()}",
                role='student',
                created_at=_now_ms(),
                is_locked=True,
            )

        project = CodingProject.objects.create(
            repo_full_name=repo_full_name,
            repo_url=repo_url,
            default_branch=default_branch,
            github_token=encrypted_token,
            clone_status='pending',
            status=CodingProject.STATUS_ACTIVE,
            owner_id=admin_user.id if admin_user else None,
            created_at=_now_ms(),
            updated_at=_now_ms(),
        )

        return JsonResponse({
            'id': project.id,
            'repoFullName': project.repo_full_name,
            'status': 'created',
        })

    return render(request, 'admin_panel/background_agent_project_new.html', {
        'is_admin': True,
        'active_page': 'background_agent',
        'github_authorized': bool(_get_admin_github_token(request)),
        'providers': _get_providers(),
    })


def ba_project_detail(request, project_id):
    """Project detail page — shows project info and its tasks."""
    r = _require_staff_admin(request)
    if r:
        return r

    project = get_object_or_404(CodingProject, pk=project_id)
    tasks = CodingTask.objects.filter(project=project).order_by('-updated_at')

    return render(request, 'admin_panel/background_agent_project.html', {
        'is_admin': True,
        'active_page': 'background_agent',
        'project': _serialize_project(project),
        'tasks': [serialize_task(t) for t in tasks],
        'providers': _get_providers(),
    })


def ba_task_detail(request, task_id):
    """Task session detail — chat, action logs, diff, controls."""
    r = _require_staff_admin(request)
    if r:
        return r

    task = get_object_or_404(CodingTask, pk=task_id)
    project = task.project
    messages = CodingTaskMessage.objects.filter(task=task).order_by('created_at')
    action_logs = CodingActionLog.objects.filter(task=task).order_by('created_at')[:200]

    workspace = project.workspace_dir if project.workspace_dir else ''
    diff = ''
    changed_files = []
    if workspace and os.path.exists(workspace):
        try:
            diff = get_full_diff(workspace, max_chars=10000)
            changed_files = get_changed_files(workspace)
        except Exception:
            pass

    return render(request, 'admin_panel/background_agent_task.html', {
        'is_admin': True,
        'active_page': 'background_agent',
        'task': serialize_task(task),
        'project': _serialize_project(project),
        'messages': [serialize_message(m) for m in messages],
        'action_logs': [serialize_action_log(log) for log in action_logs],
        'diff': diff,
        'changed_files': changed_files,
        'ws_url': _get_ws_url(request),
    })


@require_POST
def ba_ajax_create_task(request, project_id):
    """AJAX: Create a new coding task within a project."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    project = get_object_or_404(CodingProject, pk=project_id)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST

    title = (data.get('title') or '').strip()
    goal = (data.get('goal') or '').strip()
    provider = (data.get('provider') or 'ai4bharat').strip()
    model_id = (data.get('model_id') or '').strip()

    if not title or not goal:
        return JsonResponse({'error': 'Title and goal are required'}, status=400)

    branch_name = generate_branch_name(title, _uuid())

    try:
        admin_user = User.objects.get(username=request.user.username)
        created_by_id = admin_user.id
    except User.DoesNotExist:
        created_by_id = None

    task = enqueue_task(
        project_id=project.id,
        title=title,
        goal=goal,
        branch_name=branch_name,
        created_by_id=created_by_id,
        provider=provider,
        model_id=model_id,
    )

    return JsonResponse(serialize_task(task))


@require_POST
def ba_ajax_task_action(request, task_id):
    """AJAX: Control a task — pause, resume, stop."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    task = get_object_or_404(CodingTask, pk=task_id)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST

    action = (data.get('action') or '').strip()

    if action == 'pause':
        mark_paused(task, 'Paused by admin')
        return JsonResponse({'status': 'paused'})
    elif action == 'resume':
        if task.status in ('paused', 'stopped'):
            CodingTask.objects.filter(pk=task.id).update(
                status=CodingTask.STATUS_QUEUED,
                updated_at=_now_ms(),
            )
            from api.coding_agent.queue import _notify_worker
            _notify_worker()
            return JsonResponse({'status': 'queued'})
        return JsonResponse({'error': 'Task is not paused'}, status=400)
    elif action == 'stop':
        mark_stopped(task)
        return JsonResponse({'status': 'stopped'})
    else:
        return JsonResponse({'error': 'Unknown action'}, status=400)


@require_POST
def ba_ajax_send_message(request, task_id):
    """AJAX: Send a user message to a task (interrupt/follow-up)."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    task = get_object_or_404(CodingTask, pk=task_id)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST

    message = (data.get('message') or '').strip()
    if not message:
        return JsonResponse({'error': 'Message is required'}, status=400)

    msg = add_user_message(task.id, message)

    return JsonResponse(serialize_message(msg))


@require_GET
def ba_ajax_task_status(request, task_id):
    """AJAX: Get the current status of a task (for polling)."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    task = get_object_or_404(CodingTask, pk=task_id)
    messages = CodingTaskMessage.objects.filter(task=task).order_by('-created_at')[:10]
    action_logs = CodingActionLog.objects.filter(task=task).order_by('-created_at')[:20]

    return JsonResponse({
        'task': serialize_task(task),
        'recentMessages': [serialize_message(m) for m in reversed(list(messages))],
        'recentActions': [serialize_action_log(log) for log in reversed(list(action_logs))],
    })


@require_GET
def ba_ajax_task_diff(request, task_id):
    """AJAX: Get the current diff for a task."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    task = get_object_or_404(CodingTask, pk=task_id)
    project = task.project
    workspace = project.workspace_dir if project.workspace_dir else ''

    diff = ''
    changed_files = []
    if workspace and os.path.exists(workspace):
        try:
            diff = get_full_diff(workspace, max_chars=20000)
            changed_files = get_changed_files(workspace)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({
        'diff': diff,
        'changedFiles': changed_files,
    })


@require_GET
def ba_ajax_download_zip(request, task_id):
    """Download the workspace changes as a zip file."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    task = get_object_or_404(CodingTask, pk=task_id)
    project = task.project
    workspace = project.workspace_dir if project.workspace_dir else ''

    if not workspace or not os.path.exists(workspace):
        return HttpResponse('Workspace not found', status=404)

    tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    tmp.close()
    try:
        create_zip_archive(workspace, tmp.name)
        with open(tmp.name, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{task.branch_name.replace("/", "-")}.zip"'
            return response
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


@require_POST
def ba_ajax_push_github(request, task_id):
    """AJAX: Manually push changes to GitHub and optionally create a PR."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    task = get_object_or_404(CodingTask, pk=task_id)
    project = task.project
    workspace = project.workspace_dir if project.workspace_dir else ''

    if not workspace or not os.path.exists(workspace):
        return JsonResponse({'error': 'Workspace not found'}, status=404)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST

    create_pr = data.get('create_pr', True)

    changed = get_changed_files(workspace)
    if not changed:
        return JsonResponse({'error': 'No changes to push'}, status=400)

    commit_msg = f'[coding-agent] {task.title}\n\nManual push by admin.'
    success, commit_result = commit_all(workspace, commit_msg)
    if not success:
        return JsonResponse({'error': commit_result}, status=500)

    token = _decrypt_token(project.github_token)
    if not token:
        return JsonResponse({'error': 'No GitHub token configured for this project'}, status=400)

    success, push_result = push_branch(workspace, task.branch_name, token, project.repo_url)
    if not success:
        return JsonResponse({'error': push_result}, status=500)

    result = {'pushed': True, 'commitResult': commit_result, 'pushResult': push_result}

    if create_pr:
        pr_body = f"""\
## Coding Agent Task

{task.goal[:500]}

---
*This PR was created by the NEBians Background Coding Agent.*
*Task: {task.title}*
*Provider: {task.provider}*
*Iterations: {task.iteration}*
"""
        pr_url, pr_number, pr_error = create_pull_request(
            token,
            project.repo_full_name,
            task.branch_name,
            project.default_branch,
            task.title,
            pr_body,
        )
        if pr_error:
            result['prError'] = pr_error
        else:
            result['prUrl'] = pr_url
            result['prNumber'] = pr_number
            if task.status != CodingTask.STATUS_COMPLETED:
                mark_completed(task, pr_url=pr_url, pr_number=pr_number)

    return JsonResponse(result)


@require_GET
def ba_ajax_list_models(request):
    """AJAX: List available AI models for a given provider."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    provider_id = request.GET.get('provider', 'ai4bharat').strip()
    models = []

    try:
        if provider_id == 'ai4bharat':
            from api.ai4bharat_proxy import acquire_token, fetch_models_for_client
            entry = acquire_token(require_low_budget=False)
            raw = fetch_models_for_client(entry['token'])
            for m in raw:
                if m.get('active') and not m.get('random_only'):
                    models.append({'id': m['id'], 'name': m['name']})

        elif provider_id == 'qwen':
            from api.qwen_utils.models import fetch_models
            raw = fetch_models()
            for m in raw:
                models.append({'id': m.get('id', ''), 'name': m.get('name', m.get('id', ''))})

        elif provider_id == 'egov':
            from api.egov_proxy import get_models
            for m in get_models():
                models.append({'id': m['id'], 'name': m['name']})

        elif provider_id == 'deepai':
            from api.deepai_proxy import get_models
            for m in get_models():
                if not m.get('locked'):
                    models.append({'id': m['id'], 'name': m['name']})

        elif provider_id == 'inception':
            from api.inception_proxy import get_models
            for m in get_models():
                models.append({'id': m['id'], 'name': m['name']})

    except Exception as e:
        return JsonResponse({'models': [], 'error': str(e)[:100]})

    return JsonResponse({'models': models})


@require_GET
def ba_ajax_github_repos(request):
    """AJAX: List current user's GitHub repositories."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    token = _get_admin_github_token(request)
    if not token:
        return JsonResponse({'error': 'GitHub not authorized'}, status=401)

    import requests as _req
    repos = []
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
        }
        url = 'https://api.github.com/user/repos?per_page=100&sort=updated'
        resp = _req.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            for repo in resp.json():
                repos.append({
                    'name': repo.get('name'),
                    'full_name': repo.get('full_name'),
                    'html_url': repo.get('html_url'),
                    'default_branch': repo.get('default_branch', 'main'),
                    'private': repo.get('private', False),
                })
        else:
            return JsonResponse({'error': f'GitHub API error: {resp.status_code}'}, status=502)
    except Exception as e:
        return JsonResponse({'error': f'Failed to fetch repositories: {e}'}, status=502)

    return JsonResponse({'repositories': repos})


@require_GET
def ba_ajax_github_repo_branches(request):
    """AJAX: List branches for a specific repository."""
    r = _require_staff_admin(request)
    if r:
        return JsonResponse({'error': 'Admin access required'}, status=403)

    token = _get_admin_github_token(request)
    if not token:
        return JsonResponse({'error': 'GitHub not authorized'}, status=401)

    repo_full_name = request.GET.get('repo_full_name', '').strip()
    if not repo_full_name:
        return JsonResponse({'error': 'Repository full name is required'}, status=400)

    import requests as _req
    branches = []
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
        }
        url = f'https://api.github.com/repos/{repo_full_name}/branches?per_page=100'
        resp = _req.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            for branch in resp.json():
                branches.append(branch.get('name'))
        else:
            return JsonResponse({'error': f'GitHub API error: {resp.status_code}'}, status=502)
    except Exception as e:
        return JsonResponse({'error': f'Failed to fetch branches: {e}'}, status=502)

    return JsonResponse({'branches': branches})


def _serialize_project(project):
    """Serialize a CodingProject for templates/API."""
    return {
        'id': project.id,
        'repoFullName': project.repo_full_name,
        'repoUrl': project.repo_url,
        'defaultBranch': project.default_branch,
        'cloneStatus': project.clone_status,
        'cloneError': project.clone_error,
        'status': project.status,
        'workspaceDir': project.workspace_dir,
        'createdAt': project.created_at,
        'updatedAt': project.updated_at,
        'ownerId': project.owner_id or '',
        'hasToken': bool(project.github_token),
        'taskCount': project.tasks.count(),
    }


def _get_admin_github_token(request):
    """Get the admin's GitHub token from the session."""
    encrypted = request.session.get('ba_github_token', '')
    if not encrypted:
        return ''
    return _decrypt_token(encrypted)


def _get_providers():
    """Get list of available AI providers."""
    return [
        {'id': 'ai4bharat', 'name': 'AI4Bharat Arena', 'description': 'Indic LLM Arena — token-pooled, free'},
        {'id': 'qwen', 'name': 'Qwen', 'description': 'Alibaba Qwen — vision & document capable'},
        {'id': 'egov', 'name': 'eGov AI', 'description': 'Philippine Government AI — vision & PDF'},
        {'id': 'deepai', 'name': 'DeepAI', 'description': 'DeepAI — multi-model, image capable'},
        {'id': 'inception', 'name': 'Inception', 'description': 'Inception AI — reasoning & web search'},
    ]


def _get_ws_url(request):
    """Get WebSocket URL for real-time updates."""
    try:
        from .view_helpers import _get_ws_public_url
        return _get_ws_public_url()
    except Exception:
        return ''


def _uuid():
    from api.utils import uuid_str
    return uuid_str()
