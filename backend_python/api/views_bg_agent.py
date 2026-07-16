"""
API Views for Background Coding Agent.
Handles GitHub OAuth connection, session management, and agent control.
"""
import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from api.models import User
from api.models_bg_agent import (
    GitHubConnection,
    CodebaseProject,
    CodingSession,
    SessionMessage,
    FileChange,
    CommandExecution,
    AgentTask,
    DownloadPackage,
)
from api.utils import now_ms, uuid_str
from api.bg_agent_executors import run_coding_session, pause_session, resume_session, cancel_session
from api.view_helpers import *  # noqa: F401,F403

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def github_connect(request):
    """
    Handle GitHub OAuth connection.
    GET: Get connection status
    POST: Save OAuth token after callback
    """
    user = User.objects.get(pk=request.user.id)
    
    if request.method == 'GET':
        connections = GitHubConnection.objects.filter(user=user)
        return Response({
            'connections': [{
                'id': c.id,
                'github_username': c.github_username,
                'installed': c.installed,
                'permissions': json.loads(c.permissions) if c.permissions else [],
                'created_at': c.created_at,
            } for c in connections]
        })
    
    elif request.method == 'POST':
        data = request.data
        access_token = data.get('access_token')
        github_user_id = data.get('github_user_id')
        github_username = data.get('github_username')
        
        if not all([access_token, github_user_id, github_username]):
            return Response({'error': 'Missing required fields'}, status=400)
        
        # Create or update connection
        connection, created = GitHubConnection.objects.update_or_create(
            user=user,
            github_user_id=github_user_id,
            defaults={
                'github_username': github_username,
                'access_token': access_token,
                'updated_at': now_ms(),
            }
        )
        
        return Response({
            'status': 'success',
            'connection': {
                'id': connection.id,
                'github_username': connection.github_username,
                'installed': connection.installed,
            },
            'created': created
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def github_install_app(request):
    """
    Guide user to install GitHub app with proper permissions.
    Returns installation URL.
    """
    client_id = getattr(settings, 'GITHUB_CLIENT_ID', '')
    if not client_id:
        return Response({'error': 'GitHub OAuth not configured'}, status=500)
    
    # Request scopes for repo access
    scopes = ['repo', 'workflow', 'write:packages', 'read:packages']
    
    install_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope={'+'.join(scopes)}"
    
    return Response({
        'install_url': install_url,
        'scopes': scopes
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def projects_list(request):
    """
    List or create codebase projects.
    """
    user = User.objects.get(pk=request.user.id)
    
    if request.method == 'GET':
        connection_id = request.query_params.get('connection_id')
        
        projects = CodebaseProject.objects.filter(github_connection__user=user)
        if connection_id:
            projects = projects.filter(github_connection_id=connection_id)
        
        return Response({
            'projects': [{
                'id': p.id,
                'repo_full_name': p.repo_full_name,
                'repo_owner': p.repo_owner,
                'repo_name': p.repo_name,
                'base_branch': p.base_branch,
                'last_synced_at': p.last_synced_at,
                'created_at': p.created_at,
                'session_count': p.sessions.count(),
            } for p in projects.order_by('-created_at')]
        })
    
    elif request.method == 'POST':
        data = request.data
        connection_id = data.get('connection_id')
        repo_owner = data.get('repo_owner')
        repo_name = data.get('repo_name')
        base_branch = data.get('base_branch', 'main')
        
        if not all([connection_id, repo_owner, repo_name]):
            return Response({'error': 'Missing required fields'}, status=400)
        
        try:
            connection = GitHubConnection.objects.get(id=connection_id, user=user)
        except GitHubConnection.DoesNotExist:
            return Response({'error': 'GitHub connection not found'}, status=404)
        
        clone_url = f"https://github.com/{repo_owner}/{repo_name}.git"
        repo_full_name = f"{repo_owner}/{repo_name}"
        
        # Check if project already exists
        existing = CodebaseProject.objects.filter(
            github_connection=connection,
            repo_full_name=repo_full_name
        ).first()
        
        if existing:
            return Response({
                'status': 'exists',
                'project': {
                    'id': existing.id,
                    'repo_full_name': existing.repo_full_name,
                }
            })
        
        # Create new project
        project = CodebaseProject.objects.create(
            github_connection=connection,
            repo_owner=repo_owner,
            repo_name=repo_name,
            repo_full_name=repo_full_name,
            clone_url=clone_url,
            base_branch=base_branch,
            created_at=now_ms(),
            updated_at=now_ms()
        )
        
        return Response({
            'status': 'created',
            'project': {
                'id': project.id,
                'repo_full_name': project.repo_full_name,
                'base_branch': project.base_branch,
            }
        }, status=201)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sessions_list(request, project_id=None):
    """
    List sessions for a project or create a new session.
    """
    user = User.objects.get(pk=request.user.id)
    
    if request.method == 'GET':
        sessions = CodingSession.objects.filter(user=user)
        
        if project_id:
            sessions = sessions.filter(project_id=project_id)
        
        status_filter = request.query_params.get('status')
        if status_filter:
            sessions = sessions.filter(status=status_filter)
        
        return Response({
            'sessions': [{
                'id': s.id,
                'project_id': s.project_id,
                'project_name': s.project.repo_full_name,
                'title': s.title,
                'description': s.description[:200],
                'status': s.status,
                'current_step': s.current_step,
                'progress_percent': s.progress_percent,
                'session_branch': s.session_branch,
                'pr_number': s.pr_number,
                'pr_url': s.pr_url,
                'provider': s.provider,
                'model_name': s.model_name,
                'started_at': s.started_at,
                'completed_at': s.completed_at,
                'created_at': s.created_at,
                'message_count': s.messages.count(),
                'file_changes_count': s.file_changes.count(),
            } for s in sessions.order_by('-created_at')]
        })
    
    elif request.method == 'POST':
        if not project_id:
            return Response({'error': 'project_id required'}, status=400)
        
        data = request.data
        title = data.get('title', 'Untitled Task')
        description = data.get('description', '')
        instructions = data.get('instructions', '')
        provider = data.get('provider', 'qwen')
        model_name = data.get('model_name', 'qwen-coder')
        model_params = data.get('model_params', {})
        
        if not description:
            return Response({'error': 'Task description is required'}, status=400)
        
        try:
            project = CodebaseProject.objects.get(id=project_id)
            # Verify user has access
            if project.github_connection.user != user:
                return Response({'error': 'Access denied'}, status=403)
        except CodebaseProject.DoesNotExist:
            return Response({'error': 'Project not found'}, status=404)
        
        # Generate unique branch name
        branch_name = f"nebians-agent/{uuid_str()[:8]}"
        
        # Create session
        session = CodingSession.objects.create(
            project=project,
            user=user,
            title=title,
            description=description,
            instructions=instructions,
            session_branch=branch_name,
            provider=provider,
            model_name=model_name,
            model_params=json.dumps(model_params),
            status='queued',
            created_at=now_ms(),
            updated_at=now_ms()
        )
        
        # Add initial user message
        SessionMessage.objects.create(
            session=session,
            role='user',
            content=f"Task: {title}\n\n{description}",
            created_at=now_ms()
        )
        
        # Trigger background execution
        # In production, this would be queued to Celery/RQ
        from django.core.management import call_command
        from threading import Thread
        
        def run_async():
            run_coding_session(session.id)
        
        thread = Thread(target=run_async, daemon=True)
        thread.start()
        
        return Response({
            'status': 'started',
            'session': {
                'id': session.id,
                'title': session.title,
                'status': session.status,
                'session_branch': session.session_branch,
                'created_at': session.created_at,
            }
        }, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def session_detail(request, session_id):
    """
    Get detailed information about a coding session.
    """
    user = User.objects.get(pk=request.user.id)
    
    try:
        session = CodingSession.objects.select_related('project').get(
            id=session_id,
            user=user
        )
    except CodingSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)
    
    # Get recent messages
    messages = SessionMessage.objects.filter(session=session).order_by('-created_at')[:50]
    
    # Get file changes
    file_changes = FileChange.objects.filter(session=session)
    
    # Get tasks
    tasks = AgentTask.objects.filter(session=session).order_by('order')
    
    # Get commands
    commands = CommandExecution.objects.filter(session=session).order_by('-created_at')[:20]
    
    return Response({
        'session': {
            'id': session.id,
            'project': {
                'id': session.project.id,
                'repo_full_name': session.project.repo_full_name,
                'base_branch': session.project.base_branch,
            },
            'title': session.title,
            'description': session.description,
            'instructions': session.instructions,
            'status': session.status,
            'current_step': session.current_step,
            'progress_percent': session.progress_percent,
            'session_branch': session.session_branch,
            'base_commit': session.base_commit,
            'pr_number': session.pr_number,
            'pr_url': session.pr_url,
            'diff_summary': session.diff_summary,
            'provider': session.provider,
            'model_name': session.model_name,
            'started_at': session.started_at,
            'paused_at': session.paused_at,
            'completed_at': session.completed_at,
            'created_at': session.created_at,
            'updated_at': session.updated_at,
        },
        'messages': [{
            'id': m.id,
            'role': m.role,
            'content': m.content,
            'action_type': m.action_type,
            'action_data': json.loads(m.action_data) if m.action_data else None,
            'attachments': json.loads(m.attachments) if m.attachments else None,
            'created_at': m.created_at,
        } for m in messages.reverse()],
        'file_changes': [{
            'id': fc.id,
            'file_path': fc.file_path,
            'change_type': fc.change_type,
            'line_added': fc.line_added,
            'line_removed': fc.line_removed,
            'created_at': fc.created_at,
        } for fc in file_changes],
        'tasks': [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'plan': t.plan,
            'result_summary': t.result_summary,
            'order': t.order,
            'created_at': t.created_at,
            'started_at': t.started_at,
            'completed_at': t.completed_at,
        } for t in tasks],
        'commands': [{
            'id': c.id,
            'command': c.command,
            'status': c.status,
            'exit_code': c.exit_code,
            'duration_ms': c.duration_ms,
            'created_at': c.created_at,
            'completed_at': c.completed_at,
        } for c in commands],
        'stats': {
            'total_messages': session.messages.count(),
            'total_file_changes': session.file_changes.count(),
            'total_tasks': session.tasks.count(),
            'total_commands': session.commands.count(),
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def session_message(request, session_id):
    """
    Send a message to the agent (interrupt, followup, give instructions).
    """
    user = User.objects.get(pk=request.user.id)
    
    try:
        session = CodingSession.objects.get(id=session_id, user=user)
    except CodingSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)
    
    if session.status not in ['running', 'paused', 'waiting_input']:
        return Response({'error': 'Cannot send message to session in current status'}, status=400)
    
    data = request.data
    content = data.get('content', '').strip()
    
    if not content:
        return Response({'error': 'Message content required'}, status=400)
    
    # Add user message
    message = SessionMessage.objects.create(
        session=session,
        role='user',
        content=content,
        created_at=now_ms()
    )
    
    # If session was waiting for input, resume it
    if session.status == 'waiting_input':
        session.status = 'running'
        session.save(update_fields=['status', 'updated_at'])
    
    return Response({
        'status': 'sent',
        'message': {
            'id': message.id,
            'role': message.role,
            'content': message.content,
            'created_at': message.created_at,
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def session_control(request, session_id):
    """
    Control session: pause, resume, cancel, restart.
    """
    user = User.objects.get(pk=request.user.id)
    
    try:
        session = CodingSession.objects.get(id=session_id, user=user)
    except CodingSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)
    
    data = request.data
    action = data.get('action', '').lower()
    
    if action == 'pause':
        if session.status != 'running':
            return Response({'error': 'Session is not running'}, status=400)
        pause_session(session_id)
        return Response({'status': 'paused'})
    
    elif action == 'resume':
        if session.status != 'paused':
            return Response({'error': 'Session is not paused'}, status=400)
        resume_session(session_id)
        return Response({'status': 'resumed'})
    
    elif action == 'cancel':
        if session.status not in ['queued', 'running', 'paused']:
            return Response({'error': 'Cannot cancel session in current status'}, status=400)
        cancel_session(session_id)
        return Response({'status': 'cancelled'})
    
    elif action == 'restart':
        if session.status not in ['failed', 'cancelled', 'completed']:
            return Response({'error': 'Can only restart failed/cancelled/completed sessions'}, status=400)
        # Create new session with same params
        session.status = 'queued'
        session.progress_percent = 0
        session.started_at = 0
        session.completed_at = 0
        session.save(update_fields=['status', 'progress_percent', 'started_at', 'completed_at', 'updated_at'])
        run_coding_session(session_id)
        return Response({'status': 'restarted'})
    
    else:
        return Response({'error': f'Unknown action: {action}'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_changes(request, session_id):
    """
    Download zip package of all changes.
    """
    user = User.objects.get(pk=request.user.id)
    
    try:
        session = CodingSession.objects.get(id=session_id, user=user)
    except CodingSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)
    
    # Find latest download package
    package = DownloadPackage.objects.filter(session=session).order_by('-created_at').first()
    
    if not package or not os.path.exists(package.file_path):
        # Create new package
        from api.bg_agent_executors import BackgroundCodingAgent
        agent = BackgroundCodingAgent(session)
        agent._create_download_package()
        package = DownloadPackage.objects.filter(session=session).order_by('-created_at').first()
    
    if not package:
        return Response({'error': 'No changes to download'}, status=404)
    
    # Increment download count
    package.download_count += 1
    package.save(update_fields=['download_count', 'updated_at'])
    
    # Serve file
    from django.http import FileResponse
    response = FileResponse(open(package.file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="nebians_changes_{session_id[:8]}.zip"'
    response['Content-Type'] = 'application/zip'
    
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def file_change_detail(request, session_id, change_id):
    """
    Get detailed diff for a specific file change.
    """
    user = User.objects.get(pk=request.user.id)
    
    try:
        change = FileChange.objects.get(
            id=change_id,
            session_id=session_id,
            session__user=user
        )
    except FileChange.DoesNotExist:
        return Response({'error': 'File change not found'}, status=404)
    
    return Response({
        'file_change': {
            'id': change.id,
            'file_path': change.file_path,
            'change_type': change.change_type,
            'old_content': change.old_content,
            'new_content': change.new_content,
            'diff_patch': change.diff_patch,
            'line_added': change.line_added,
            'line_removed': change.line_removed,
            'created_at': change.created_at,
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def push_to_github(request, session_id):
    """
    Manually push changes to GitHub (if PR wasn't auto-created).
    """
    user = User.objects.get(pk=request.user.id)
    
    try:
        session = CodingSession.objects.get(id=session_id, user=user)
    except CodingSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)
    
    if session.status != 'completed':
        return Response({'error': 'Session must be completed before pushing'}, status=400)
    
    # The changes should already be pushed during finalization
    # This endpoint can trigger PR creation if it failed earlier
    
    import requests
    
    connection = session.project.github_connection
    pr_title = f"[NEBians Agent] {session.title}"
    pr_body = session.diff_summary or f"Automated changes for: {session.description}"
    
    api_url = f"https://api.github.com/repos/{session.project.repo_full_name}/pulls"
    headers = {
        'Authorization': f'Bearer {connection.access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': pr_title,
        'body': pr_body,
        'head': session.session_branch,
        'base': session.project.base_branch
    }
    
    try:
        resp = requests.post(api_url, json=data, headers=headers, timeout=30)
        resp.raise_for_status()
        pr_data = resp.json()
        
        session.pr_number = pr_data.get('number')
        session.pr_url = pr_data.get('html_url', '')
        session.save(update_fields=['pr_number', 'pr_url', 'updated_at'])
        
        return Response({
            'status': 'success',
            'pr_number': session.pr_number,
            'pr_url': session.pr_url,
        })
    except Exception as e:
        logger.exception(f"Failed to create PR: {e}")
        return Response({'error': f'Failed to create PR: {str(e)}'}, status=500)


# Admin-only views for monitoring all sessions
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_sessions_dashboard(request):
    """
    Admin dashboard showing all coding sessions across all users.
    """
    # Get stats
    total_sessions = CodingSession.objects.count()
    active_sessions = CodingSession.objects.filter(status='running').count()
    completed_sessions = CodingSession.objects.filter(status='completed').count()
    failed_sessions = CodingSession.objects.filter(status='failed').count()
    
    # Recent sessions
    recent = CodingSession.objects.select_related('user', 'project').order_by('-created_at')[:50]
    
    return Response({
        'stats': {
            'total': total_sessions,
            'active': active_sessions,
            'completed': completed_sessions,
            'failed': failed_sessions,
        },
        'recent_sessions': [{
            'id': s.id,
            'user': {
                'username': s.user.username,
                'display_name': s.user.display_name,
            },
            'project': s.project.repo_full_name,
            'title': s.title,
            'status': s.status,
            'progress_percent': s.progress_percent,
            'created_at': s.created_at,
            'completed_at': s.completed_at,
        } for s in recent]
    })
