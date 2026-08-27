import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from . import study_tools, toolstore
from .study_tools import ToolError
from .view_helpers import _ctx, _rate_limit
from .views_canvas import _require_user

MAX_TOOL_UPLOAD = 8 * 1024 * 1024
_EXT_TO_KIND = {
    '.pdf': 'pdf', '.docx': 'docx', '.txt': 'txt',
    '.png': 'png', '.jpg': 'jpg', '.jpeg': 'jpeg',
    '.gif': 'gif', '.webp': 'webp',
}


@require_GET
def doc_tools_page(request):
    ctx = _ctx(request)
    ctx['registry_json'] = json.dumps(study_tools.REGISTRY, ensure_ascii=False)
    return render(request, 'web/doc_tools.html', ctx)


def _tool_defs():
    return {t['id']: t for t in study_tools.REGISTRY}


@require_POST
def ajax_tools_run(request):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'tools_run', 12, 120):
        return JsonResponse({'error': 'Tools are cooling down — try again shortly.'}, status=429)
    tool_id = (request.POST.get('tool') or '').strip().lower()
    defs = _tool_defs()
    meta = defs.get(tool_id)
    if meta is None:
        return JsonResponse({'error': 'Unknown tool.'}, status=400)
    try:
        params = json.loads(request.POST.get('params') or '{}')
    except Exception:
        params = {}
    if not isinstance(params, dict):
        params = {}
    kinds = meta.get('inputs', {}).get('kinds', [])
    min_files = meta.get('inputs', {}).get('min', 0)
    f_obj = request.FILES.getlist('files') or []
    if len(f_obj) > (meta.get('inputs', {}).get('max') or 12):
        return JsonResponse({'error': 'Too many files.'}, status=400)
    if len(f_obj) < min_files:
        return JsonResponse({'error': f'This tool needs at least {min_files} file(s).'}, status=400)
    sources = []
    for f in f_obj:
        if getattr(f, 'size', 0) > MAX_TOOL_UPLOAD:
            return JsonResponse({'error': f'{getattr(f, "name", "file")} exceeds 8 MB.'}, status=413)
        name = (getattr(f, 'name', '') or '')
        ext = os.path.splitext(name)[1].lower()
        kind = _EXT_TO_KIND.get(ext)
        if kind not in kinds:
            return JsonResponse({'error': f'{name} is not a valid input for this tool.'}, status=400)
        data = f.read(MAX_TOOL_UPLOAD + 1)
        if len(data) > MAX_TOOL_UPLOAD:
            return JsonResponse({'error': f'{name} exceeds 8MB'}, status=413)
        sources.append({'name': name, 'kind': kind, 'data': data})
    try:
        result = study_tools.run_tool(tool_id, sources, params)
    except ToolError as exc:
        return JsonResponse({'ok': False, 'error': str(exc)})
    except Exception:
        return JsonResponse({'ok': False, 'error': "That file operation didn't complete cleanly — try a smaller or simpler file."})
    files = []
    for art in result.get('artifacts') or []:
        token = toolstore.put_artifact(user.id, art['name'], art.get('mime', ''), art.get('bytes', b''))
        files.append({
            'name': art['name'],
            'mime': art.get('mime', ''),
            'size': len(art.get('bytes', b'')),
            'url': f"/ajax/lazy/file/{token}/",
        })
    return JsonResponse({'ok': True, 'text': result.get('text') or 'Done.', 'files': files})