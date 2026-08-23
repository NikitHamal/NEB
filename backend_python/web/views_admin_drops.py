"""Internal Admin View for managing Agent Drop batches."""
import os
import shutil
import time
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404

from .view_helpers import _require_staff_admin


def _format_size(num_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def admin_agent_drops(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        # Check if authorized via agent token in query string
        token = request.GET.get('token', '').strip()
        expected = getattr(settings, 'AGENT_DROP_SECRET', None) or os.environ.get('AGENT_DROP_SECRET') or '***REMOVED***'
        if not token or token != expected:
            return redirect_response

    sync_root = os.path.join(settings.MEDIA_ROOT, 'agent_sync')
    os.makedirs(sync_root, exist_ok=True)

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        batch_id = request.POST.get('batch_id', '').strip()
        
        if action == 'delete' and batch_id:
            clean_id = ''.join(c for c in batch_id if c.isalnum() or c in ('-', '_'))
            target = os.path.join(sync_root, clean_id)
            if os.path.exists(target):
                shutil.rmtree(target)
            return redirect('web:admin_agent_drops')

        if action == 'delete_all':
            for item in os.listdir(sync_root):
                target = os.path.join(sync_root, item)
                if os.path.isdir(target):
                    shutil.rmtree(target)
            return redirect('web:admin_agent_drops')

    token_param = getattr(settings, 'AGENT_DROP_SECRET', None) or os.environ.get('AGENT_DROP_SECRET') or '***REMOVED***'

    batches = []
    total_files_all = 0
    total_size_all = 0

    for name in sorted(os.listdir(sync_root), reverse=True):
        bpath = os.path.join(sync_root, name)
        if os.path.isdir(bpath):
            file_list = []
            batch_bytes = 0
            for root, _, files in os.walk(bpath):
                for f in files:
                    abs_f = os.path.join(root, f)
                    rel_f = os.path.relpath(abs_f, bpath).replace('\\', '/')
                    f_size = os.path.getsize(abs_f)
                    batch_bytes += f_size
                    file_list.append({
                        'path': rel_f,
                        'size': _format_size(f_size),
                    })

            mtime = os.path.getmtime(bpath)
            total_files_all += len(file_list)
            total_size_all += batch_bytes

            batches.append({
                'batch_id': name,
                'file_count': len(file_list),
                'files': file_list,
                'size_formatted': _format_size(batch_bytes),
                'created_at': time.strftime("%b %d, %Y • %I:%M %p", time.localtime(mtime)),
                'download_url': f'/api/agent-drop/{name}/download/?token={token_param}',
            })

    return render(request, 'admin_panel/agent_drops.html', {
        'is_admin': True,
        'active_page': 'agent_drops',
        'batches': batches,
        'total_batches': len(batches),
        'total_files': total_files_all,
        'total_size': _format_size(total_size_all),
        'agent_token': token_param,
    })
