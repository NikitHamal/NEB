import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from api.models import BackgroundAgentSession, BackgroundAgentMessage, User
from api.utils import uuid_str, now_ms
from .view_helpers import _require_staff_admin

def admin_backgroundagent_list(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response: return redirect_response
    sessions = BackgroundAgentSession.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/backgroundagent/dashboard.html', {
        'sessions': sessions,
        'active_page': 'backgroundagent'
    })

def admin_backgroundagent_new(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response: return redirect_response

    if request.method == 'POST':
        repo_url = request.POST.get('repo_url', '').strip()
        goal = request.POST.get('goal', '').strip()
        if not repo_url or not goal:
            return HttpResponse("Repo URL and Goal are required", status=400)

        session_id = uuid_str()
        branch_name = f"backgroundagent-{session_id[:8]}"

        user = User.objects.get(username=request.user.username)

        session = BackgroundAgentSession.objects.create(
            id=session_id,
            user=user,
            repo_url=repo_url,
            branch_name=branch_name,
            goal=goal,
            status='running',
            created_at=now_ms(),
            updated_at=now_ms()
        )

        BackgroundAgentMessage.objects.create(
            id=uuid_str(),
            session=session,
            role='user',
            content=goal,
            created_at=now_ms()
        )

        return redirect('web:admin_backgroundagent_detail', session_id=session.id)

    return render(request, 'admin_panel/backgroundagent/new.html', {
        'active_page': 'backgroundagent'
    })

def admin_backgroundagent_detail(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response: return redirect_response

    session = get_object_or_404(BackgroundAgentSession, id=session_id)
    messages = session.messages.all().order_by('created_at')

    return render(request, 'admin_panel/backgroundagent/session_detail.html', {
        'session': session,
        'messages': messages,
        'active_page': 'backgroundagent'
    })


def admin_backgroundagent_action(request, session_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response: return redirect_response

    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    session = get_object_or_404(BackgroundAgentSession, id=session_id)
    action = request.POST.get('action')

    if action == 'pause':
        if session.status == 'running':
            session.status = 'paused'
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'updated_at'])
    elif action == 'resume':
        if session.status == 'paused' or session.status == 'stopped':
            session.status = 'running'
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'updated_at'])
    elif action == 'stop':
        if session.status in ['running', 'paused']:
            session.status = 'stopped'
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'updated_at'])
    elif action == 'chat':
        message = request.POST.get('message', '').strip()
        if message:
            BackgroundAgentMessage.objects.create(
                id=uuid_str(),
                session=session,
                role='user',
                content=message,
                created_at=now_ms()
            )
            session.status = 'running' # Resume automatically if user talks
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'updated_at'])
    elif action == 'download_diff':
        import os
        from django.http import FileResponse
        repo_dir = f"/tmp/nebians_agent_{session.id}"
        diff_path = f"/tmp/nebians_agent_{session.id}_diff.patch"

        if os.path.exists(repo_dir):
            os.system(f"cd {repo_dir} && git diff main > {diff_path}")
            if os.path.exists(diff_path):
                return FileResponse(open(diff_path, 'rb'), as_attachment=True, filename=f"{session.id}_changes.patch")
        return HttpResponse("Diff not found or repo not cloned yet.", status=404)

    elif action == 'push_pr':
        # Handled in the worker, but we just trigger the status update
        session.status = 'pushing'
        session.updated_at = now_ms()
        session.save(update_fields=['status', 'updated_at'])

    return redirect('web:admin_backgroundagent_detail', session_id=session.id)
