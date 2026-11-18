import base64
import concurrent.futures as cf
import json
import time
import uuid

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from . import admin_chat_engine as engine
from .view_helpers import _require_staff_admin

PROVIDERS, MODEL_OPTIONS = engine.build_lists()
_LABELS = {p['id']: p['label'] for p in PROVIDERS}


def _sse(obj):
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def admin_chat(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    return render(request, 'admin_panel/chat.html', {
        'active_page': 'chat', 'providers': PROVIDERS, 'providers_json': json.dumps(PROVIDERS),
        'model_options': json.dumps(MODEL_OPTIONS),
    })


def ajax_admin_chat_models(request, slug):
    if _require_staff_admin(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if slug not in MODEL_OPTIONS:
        return JsonResponse({'error': 'Unknown provider'}, status=404)
    return JsonResponse({'models': engine.model_list(slug, MODEL_OPTIONS[slug])})


def ajax_admin_chat_health(request):
    """One short native call per keyless provider, in parallel. Read-only."""
    if _require_staff_admin(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    slugs = [p['id'] for p in PROVIDERS if p['keyless'] and p['id'] != 'custom']
    ping = 'Reply with the single word OK.'

    def one(slug):
        t0, text, err = time.time(), '', ''
        model = (MODEL_OPTIONS.get(slug) or [{}])[0].get('id', '')
        for ev in engine.run_turn(slug, model, ping, []):
            if ev['type'] == 'text':
                text += ev['content']
            elif ev['type'] == 'error':
                err = ev['message']
        return {'id': slug, 'ok': bool(text.strip()), 'ms': int((time.time() - t0) * 1000),
                'error': '' if text.strip() else (err or 'no answer')[:200]}

    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(one, slugs))
    return JsonResponse({'results': results})


def _voice(message, history, scenario):
    from api.inception_proxy import get_voice_config, synthesize, voice_turn
    scenario = scenario or ((get_voice_config() or {}).get('scenarios') or [{}])[0].get('id') or 'open'
    spoken = []
    for ch in voice_turn(history + [{'role': 'user', 'content': message}], scenario_id=scenario):
        t = ch.get('type')
        if t == 'text':
            spoken.append(ch.get('content', ''))
            yield {'type': 'text', 'content': ch.get('content', '')}
        elif t in ('tool_start', 'tool_end'):
            yield {'type': 'thought', 'content': f"Tool {ch.get('name')} {'done' if t == 'tool_end' else (ch.get('args') or '')}"}
        elif t == 'error':
            yield {'type': 'error', 'message': ch.get('error') or 'voice error'}
            return
    full = ''.join(spoken).strip()
    if full:
        audio = synthesize(full[:5000])
        if audio:
            yield {'type': 'audio', 'dataUrl': 'data:audio/mpeg;base64,' + base64.b64encode(audio).decode(),
                   'bytes': len(audio), 'contentType': 'audio/mpeg'}


@require_POST
def ajax_admin_chat_send(request):
    if _require_staff_admin(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    post = request.POST
    provider = (post.get('provider') or '').strip().lower()
    message = (post.get('message') or '').strip()
    if not message:
        return JsonResponse({'error': 'Message is required'}, status=400)
    if provider not in MODEL_OPTIONS:
        return JsonResponse({'error': f'Unknown provider: {provider}'}, status=400)
    try:
        history = json.loads(post.get('history') or '[]')
    except (json.JSONDecodeError, TypeError):
        history = []
    # The model the user picked is the model that is called: no remapping.
    model = (post.get('model') or '').strip() or (MODEL_OPTIONS[provider] or [{}])[0].get('id', '')
    reasoning, web_search = post.get('reasoning') == 'true', post.get('web_search') == 'true'
    voice = provider == 'inception' and post.get('voice_mode') == 'true'

    def generate():
        t0, chars = time.time(), 0
        yield _sse({'type': 'start', 'messageId': str(uuid.uuid4()), 'provider': provider,
                    'providerLabel': _LABELS.get(provider, provider), 'model': model,
                    'thinking': reasoning, 'webSearch': web_search})
        events = (_voice(message, history, (post.get('voice_scenario') or '').strip() or None) if voice else
                  engine.run_turn(provider, model, message, history, reasoning, web_search,
                                  (post.get('api_key') or '').strip(), post.get('api_url', '')))
        try:
            for ev in events:
                chars += len(ev.get('content') or '') if ev['type'] == 'text' else 0
                yield _sse(ev)
        except Exception as exc:
            yield _sse({'type': 'error', 'message': str(exc)})
        yield _sse({'type': 'done', 'ms': int((time.time() - t0) * 1000), 'chars': chars, 'model': model})
        yield "data: [DONE]\n\n"

    response = StreamingHttpResponse(generate(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
