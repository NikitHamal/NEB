import os
import io
import zipfile
import json
import time
import uuid
from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def _is_authorized(request):
    token = (
        request.headers.get('X-Agent-Token') or
        request.META.get('HTTP_X_AGENT_TOKEN') or
        request.GET.get('token') or
        request.POST.get('token')
    )
    if not token:
        auth_hdr = request.headers.get('Authorization', '') or request.META.get('HTTP_AUTHORIZATION', '')
        if auth_hdr.startswith('Bearer '):
            token = auth_hdr[7:].strip()
    expected = getattr(settings, 'AGENT_DROP_SECRET', None) or os.environ.get('AGENT_DROP_SECRET') or '***REMOVED***'
    if not expected or not token:
        return False
    return token.strip() == expected.strip()


def _sanitize_path(base_dir, user_path):
    clean = os.path.normpath(user_path.replace('\\', '/')).lstrip('/')
    target = os.path.abspath(os.path.join(base_dir, clean))
    if not target.startswith(os.path.abspath(base_dir)):
        return None
    return target


@csrf_exempt
@require_http_methods(["POST"])
def agent_drop_upload(request):
    if not _is_authorized(request):
        return JsonResponse({'error': 'Unauthorized: invalid or missing X-Agent-Token'}, status=401)

    batch_name = request.POST.get('batch_id') or request.GET.get('batch_id')
    if batch_name:
        batch_id = ''.join(c for c in batch_name if c.isalnum() or c in ('-', '_'))[:40]
    else:
        batch_id = time.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]

    base_dir = os.path.join(settings.MEDIA_ROOT, 'agent_sync', batch_id)
    os.makedirs(base_dir, exist_ok=True)

    saved_files = []

    # 1. Multi-part File / Zip upload
    if request.FILES:
        for key in request.FILES:
            uploaded = request.FILES[key]
            is_zip = (
                uploaded.name.lower().endswith('.zip') or
                uploaded.content_type in ('application/zip', 'application/x-zip-compressed')
            )
            if is_zip:
                try:
                    with zipfile.ZipFile(uploaded, 'r') as zf:
                        for member in zf.namelist():
                            if member.startswith('/') or '..' in member:
                                continue
                            target = _sanitize_path(base_dir, member)
                            if not target:
                                continue
                            if member.endswith('/'):
                                os.makedirs(target, exist_ok=True)
                            else:
                                os.makedirs(os.path.dirname(target), exist_ok=True)
                                with open(target, 'wb') as f:
                                    f.write(zf.read(member))
                                saved_files.append(member)
                except Exception as e:
                    return JsonResponse({'error': f'Invalid zip archive: {str(e)}'}, status=400)
            else:
                rel_path = request.POST.get('path') or uploaded.name
                target = _sanitize_path(base_dir, rel_path)
                if not target:
                    return JsonResponse({'error': 'Invalid file path'}, status=400)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, 'wb') as f:
                    for chunk in uploaded.chunks():
                        f.write(chunk)
                saved_files.append(rel_path)

        token_param = request.GET.get('token') or request.headers.get('X-Agent-Token', '')
        return JsonResponse({
            'status': 'ok',
            'batch_id': batch_id,
            'file_count': len(saved_files),
            'files': saved_files[:50],
            'download_url': f'/api/agent-drop/{batch_id}/download/?token={token_param}'
        })

    # 2. Raw JSON batch upload: { "files": { "path/to/file.py": "content..." } }
    if request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse({'error': 'Malformed JSON payload'}, status=400)

        files_map = data.get('files', {})
        if not isinstance(files_map, dict):
            return JsonResponse({'error': '"files" field must be a dictionary of {path: content}'}, status=400)

        for rel_path, content in files_map.items():
            target = _sanitize_path(base_dir, rel_path)
            if not target:
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content if isinstance(content, str) else str(content))
            saved_files.append(rel_path)

        token_param = request.GET.get('token') or request.headers.get('X-Agent-Token', '')
        return JsonResponse({
            'status': 'ok',
            'batch_id': batch_id,
            'file_count': len(saved_files),
            'files': saved_files[:50],
            'download_url': f'/api/agent-drop/{batch_id}/download/?token={token_param}'
        })

    return JsonResponse({'error': 'No file or JSON payload received'}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def agent_drop_download(request, batch_id):
    if not _is_authorized(request):
        return HttpResponse('Unauthorized', status=401)

    clean_batch_id = ''.join(c for c in batch_id if c.isalnum() or c in ('-', '_'))
    base_dir = os.path.join(settings.MEDIA_ROOT, 'agent_sync', clean_batch_id)

    if not os.path.exists(base_dir):
        raise Http404('Batch not found')

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(base_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, base_dir)
                zf.write(abs_path, rel_path)

    mem_zip.seek(0)
    response = HttpResponse(mem_zip.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="agent_drop_{clean_batch_id}.zip"'
    return response


@csrf_exempt
@require_http_methods(["GET"])
def agent_drop_list(request):
    if not _is_authorized(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    sync_root = os.path.join(settings.MEDIA_ROOT, 'agent_sync')
    if not os.path.exists(sync_root):
        return JsonResponse({'batches': []})

    token_param = request.GET.get('token') or request.headers.get('X-Agent-Token', '')
    batches = []
    for name in sorted(os.listdir(sync_root), reverse=True):
        bpath = os.path.join(sync_root, name)
        if os.path.isdir(bpath):
            file_count = sum(len(files) for _, _, files in os.walk(bpath))
            mtime = os.path.getmtime(bpath)
            batches.append({
                'batch_id': name,
                'file_count': file_count,
                'created_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)),
                'download_url': f'/api/agent-drop/{name}/download/?token={token_param}'
            })

    return JsonResponse({'batches': batches[:30]})
