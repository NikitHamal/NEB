"""
Admin views for Background Coding Agent.
Provides admin-only web interface at /admin/backgroundagent/
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from api.models_bg_agent import (
    GitHubConnection,
    CodebaseProject,
    CodingSession,
    SessionMessage,
    FileChange,
    CommandExecution,
    AgentTask,
)
from api.utils import now_ms


@staff_member_required
def admin_background_agent(request):
    """
    Main admin dashboard for Background Coding Agent.
    Accessible only to staff/admin users at /admin/background-agent/
    """
    # Get overview stats
    total_connections = GitHubConnection.objects.count()
    total_projects = CodebaseProject.objects.count()
    total_sessions = CodingSession.objects.count()
    
    active_sessions = CodingSession.objects.filter(status='running').count()
    completed_sessions = CodingSession.objects.filter(status='completed').count()
    failed_sessions = CodingSession.objects.filter(status='failed').count()
    queued_sessions = CodingSession.objects.filter(status='queued').count()
    
    # Recent sessions with user info
    recent_sessions = CodingSession.objects.select_related(
        'user', 'project'
    ).order_by('-created_at')[:20]
    
    # Recent activity
    recent_messages = SessionMessage.objects.select_related(
        'session__user'
    ).order_by('-created_at')[:10]
    
    context = {
        'is_admin': True,
        'active_page': 'background_agent',
        'stats': {
            'total_connections': total_connections,
            'total_projects': total_projects,
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'completed_sessions': completed_sessions,
            'failed_sessions': failed_sessions,
            'queued_sessions': queued_sessions,
        },
        'recent_sessions': recent_sessions,
        'recent_messages': recent_messages,
    }
    
    return render(request, 'admin_panel/background_agent.html', context)


@staff_member_required
def admin_session_detail(request, session_id):
    """
    Detailed view of a specific coding session.
    Shows all messages, file changes, commands, and tasks.
    """
    session = get_object_or_404(
        CodingSession.objects.select_related('user', 'project'),
        id=session_id
    )
    
    # Get all related data
    messages = SessionMessage.objects.filter(session=session).order_by('created_at')
    file_changes = FileChange.objects.filter(session=session).order_by('file_path')
    commands = CommandExecution.objects.filter(session=session).order_by('-created_at')
    tasks = AgentTask.objects.filter(session=session).order_by('order')
    
    # Calculate stats
    total_lines_added = sum(fc.line_added for fc in file_changes)
    total_lines_removed = sum(fc.line_removed for fc in file_changes)
    
    context = {
        'is_admin': True,
        'active_page': 'background_agent',
        'session': session,
        'messages': messages,
        'file_changes': file_changes,
        'commands': commands,
        'tasks': tasks,
        'stats': {
            'total_messages': messages.count(),
            'total_file_changes': file_changes.count(),
            'total_commands': commands.count(),
            'total_tasks': tasks.count(),
            'lines_added': total_lines_added,
            'lines_removed': total_lines_removed,
        },
    }
    
    return render(request, 'admin_panel/session_detail.html', context)


@staff_member_required
def admin_api_session_control(request, session_id):
    """
    API endpoint for admins to control sessions.
    """
    from api.bg_agent_executors import pause_session, resume_session, cancel_session
    
    session = get_object_or_404(CodingSession, id=session_id)
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        if action == 'pause' and session.status == 'running':
            pause_session(session_id)
            return JsonResponse({'status': 'success', 'new_status': 'paused'})
        
        elif action == 'resume' and session.status == 'paused':
            resume_session(session_id)
            return JsonResponse({'status': 'success', 'new_status': 'running'})
        
        elif action == 'cancel' and session.status in ['queued', 'running', 'paused']:
            cancel_session(session_id)
            return JsonResponse({'status': 'success', 'new_status': 'cancelled'})
        
        return JsonResponse({'error': 'Invalid action or session state'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
