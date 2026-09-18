import hmac
import os
import io
import zipfile
import json
import time
import uuid
import shutil
from django.conf import settings
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def _expected_secret():
    expected = (getattr(settings, 'AGENT_DROP_SECRET', '') or '').strip()
    if not expected:
        return ''
    if expected == 'dev-agent-drop-secret-change-me' and not settings.DEBUG:
        return ''
    return expected


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
    expected = _expected_secret()
    if expected and token and hmac.compare_digest(token.strip(), expected):
        return True
    try:
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated and (user.is_staff or user.is_superuser):
            return True
    except Exception:
        pass
    return False


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

        return JsonResponse({
            'status': 'ok',
            'batch_id': batch_id,
            'file_count': len(saved_files),
            'files': saved_files[:50],
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

        return JsonResponse({
            'status': 'ok',
            'batch_id': batch_id,
            'file_count': len(saved_files),
            'files': saved_files[:50],
        })

    return JsonResponse({'error': 'No file or JSON payload received'}, status=400)


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
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
@require_http_methods(["GET", "HEAD"])
def agent_drop_list(request):
    if not _is_authorized(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    sync_root = os.path.join(settings.MEDIA_ROOT, 'agent_sync')
    if not os.path.exists(sync_root):
        return JsonResponse({'batches': []})

    batches = []
    for name in sorted(os.listdir(sync_root), reverse=True):
        bpath = os.path.join(sync_root, name)
        if os.path.isdir(bpath):
            file_count = sum(len(files) for _, _, files in os.walk(bpath))
            total_size = sum(os.path.getsize(os.path.join(root, f)) for root, _, files in os.walk(bpath) for f in files)
            mtime = os.path.getmtime(bpath)
            batches.append({
                'batch_id': name,
                'file_count': file_count,
                'total_size_bytes': total_size,
                'created_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime)),
            })

    return JsonResponse({'batches': batches[:50]})


@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def agent_drop_delete(request, batch_id):
    if not _is_authorized(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    clean_batch_id = ''.join(c for c in batch_id if c.isalnum() or c in ('-', '_'))
    base_dir = os.path.join(settings.MEDIA_ROOT, 'agent_sync', clean_batch_id)

    if not os.path.exists(base_dir):
        return JsonResponse({'error': 'Batch not found'}, status=404)

    try:
        shutil.rmtree(base_dir)
        return JsonResponse({'status': 'deleted', 'batch_id': clean_batch_id})
    except Exception as e:
        return JsonResponse({'error': f'Failed to delete batch: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def agent_drop_apply(request, batch_id):
    """Applies / merges the dropped batch into the live codebase root."""
    if not _is_authorized(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    clean_batch_id = ''.join(c for c in batch_id if c.isalnum() or c in ('-', '_'))
    batch_dir = os.path.join(settings.MEDIA_ROOT, 'agent_sync', clean_batch_id)

    if not os.path.exists(batch_dir):
        return JsonResponse({'error': 'Batch not found'}, status=404)

    base_dir = settings.BASE_DIR
    applied_files = []

    try:
        for root, _, files in os.walk(batch_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, batch_dir)
                dst_path = _sanitize_path(base_dir, rel_path)
                if not dst_path:
                    continue
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
                applied_files.append(rel_path)

        return JsonResponse({
            'status': 'ok',
            'batch_id': clean_batch_id,
            'applied_count': len(applied_files),
            'files': applied_files[:100]
        })
    except Exception as e:
        return JsonResponse({'error': f'Failed to apply batch: {str(e)}'}, status=500)


# ── Bidirectional: Outgoing Codebase to Agent ───────────────────────────────

IGNORE_DIRS = {
    '.git', '.github', '.idea', '.vscode', '__pycache__', 'staticfiles',
    'media', 'virtualenv', 'node_modules', 'scratch', '.venv', 'env', 'logs', 'tmp'
}

IGNORE_EXTENSIONS = {'.pyc', '.pyo', '.pyd', '.DS_Store', '.sqlite3', '.keystore', '.jks', '.key', '.pem'}

SENSITIVE_BASENAMES = {
    '.env', '.env.example', '.ssh_deploy_info.json',
    'nebians-release.keystore', 'id_rsa', 'id_ed25519',
}


def _is_sensitive_path(rel_path):
    name = rel_path.replace('\\', '/').split('/')[-1].lower()
    if name in SENSITIVE_BASENAMES:
        return True
    if name.endswith(('.pem', '.key')):
        return True
    return False


def _should_include_file(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for p in parts:
        if p in IGNORE_DIRS:
            return False
    if _is_sensitive_path(rel_path):
        return False
    _, ext = os.path.splitext(rel_path)
    if ext in IGNORE_EXTENSIONS:
        return False
    return True


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def agent_drop_codebase_download(request):
    """Exports a clean zip of the latest live codebase so the agent can fetch updates."""
    if not _is_authorized(request):
        return HttpResponse('Unauthorized', status=401)

    base_dir = settings.BASE_DIR
    mem_zip = io.BytesIO()

    with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, base_dir).replace('\\', '/')
                if _should_include_file(rel_path):
                    zf.write(abs_path, rel_path)

    mem_zip.seek(0)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(mem_zip.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="nebians_codebase_{stamp}.zip"'
    return response


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def agent_drop_codebase_manifest(request):
    """Returns a JSON manifest of all codebase files with mtime & size."""
    if not _is_authorized(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    base_dir = settings.BASE_DIR
    manifest = []

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, base_dir).replace('\\', '/')
            if _should_include_file(rel_path):
                manifest.append({
                    'path': rel_path,
                    'size': os.path.getsize(abs_path),
                    'mtime': int(os.path.getmtime(abs_path)),
                })

    return JsonResponse({'files': manifest, 'total_files': len(manifest)})


@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def agent_drop_fetch_file(request):
    """Fetches the live content of a specific file."""
    if not _is_authorized(request):
        return HttpResponse('Unauthorized', status=401)

    rel_path = request.GET.get('path', '').strip()
    if not rel_path:
        return HttpResponse('Missing path parameter', status=400)

    if not _should_include_file(rel_path.replace('\\', '/').lstrip('/')):
        raise Http404('File not found')

    target = _sanitize_path(settings.BASE_DIR, rel_path)
    if not target or not os.path.isfile(target):
        raise Http404('File not found')

    with open(target, 'rb') as f:
        content = f.read()

    return HttpResponse(content, content_type='text/plain; charset=utf-8')
