import json, uuid
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .view_helpers import _require_staff_admin

from api.llm.registry import admin_catalog

def _sse(obj):
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"

def _sse_done():
    return "data: [DONE]\n\n"

def _uuid():
    return str(uuid.uuid4())

_CAPS = {
    'qwen':      {'stream': True,  'thinking': True,  'web_search': True,  'files': True},
    'qwenfast':  {'stream': True,  'thinking': False, 'web_search': False, 'files': False},
    'egov':      {'stream': True,  'thinking': False, 'web_search': False, 'files': True},
    'deepai':    {'stream': True,  'thinking': True,  'web_search': False, 'files': True},
    'inception': {'stream': True,  'thinking': True,  'web_search': True,  'files': False},
    'k2think':   {'stream': True,  'thinking': True,  'web_search': False, 'files': False},
    'poolside':  {'stream': True,  'thinking': False, 'web_search': True,  'files': False},
    'motiftech': {'stream': True,  'thinking': True,  'web_search': False, 'files': False},
    'metaai':    {'stream': True,  'thinking': True,  'web_search': False, 'files': False},
    'tryingopen': {'stream': True, 'thinking': True,  'web_search': False, 'files': False},
    'longcat':   {'stream': True,  'thinking': True,  'web_search': True,  'files': False},
    'geminiweb': {'stream': True,  'thinking': False, 'web_search': False, 'files': False},
    'empero':    {'stream': True,  'thinking': True,  'web_search': False, 'files': False},
}


def _build_provider_lists():
    catalog = admin_catalog()
    providers = []
    model_options = {}
    for entry in catalog['scrapers'] + catalog['official']:
        slug = entry['slug']
        caps = _CAPS.get(slug, {'stream': True, 'thinking': False, 'web_search': False, 'files': False})
        providers.append({'id': slug, 'label': entry['label'], **caps})
        model_options[slug] = [{'id': m['id'], 'label': m['label']} for m in entry['models']]
    providers.append({'id': 'custom', 'label': 'Custom OpenAI-compatible endpoint',
                      'stream': False, 'thinking': False, 'web_search': False, 'files': False})
    model_options['custom'] = []
    return providers, model_options


PROVIDERS, MODEL_OPTIONS = _build_provider_lists()

# Dispatch table for community proxies. Each entry:
#   kind='legacy'  -> stream_chat(user_message=, model=, history=, system_prompt=), chunks {type:'content', text}
#   kind='messages'-> stream_chat(messages=, model=...), chunks {type:'text'|'error', content/error}
_SCRAPER_DISPATCH = {
    'qwenfast':  ('messages', 'qwenfast_proxy'),
    'egov':      ('legacy', 'egov_proxy'),
    'deepai':    ('legacy', 'deepai_proxy'),
    'inception': ('messages', 'inception_proxy'),
    'k2think':   ('messages', 'k2think_proxy'),
    'poolside':  ('messages', 'poolside_proxy'),
    'motiftech': ('messages', 'motiftech_proxy'),
    'metaai':    ('messages', 'metaai_proxy'),
    'tryingopen': ('messages', 'tryingopen_proxy'),
    'longcat':   ('messages', 'longcat_proxy'),
    'geminiweb': ('messages', 'geminiweb_proxy'),
}

_INCEPTION_SLUGS = ('inception',)
_TRYINGOPEN_SLUGS = ('tryingopen',)


def _iter_scraper_chunks(slug, message, history, model, reasoning, web_search):
    kind, mod_name = _SCRAPER_DISPATCH[slug]
    import importlib
    mod = importlib.import_module(f'api.{mod_name}')
    if kind == 'legacy':
        for chunk in mod.stream_chat(
            user_message=message,
            model=model,
            history=history,
            system_prompt='You are a helpful assistant.',
        ):
            t = chunk.get('type')
            if t == 'content':
                yield {'type': 'text', 'content': chunk.get('text', '')}
            elif t == 'done':
                return
            elif t == 'error':
                yield {'type': 'error', 'error': chunk.get('message', 'upstream error')}
                return
        return
    msgs = history + [{'role': 'user', 'content': message}]
    kwargs = {'messages': msgs, 'model': model}
    if slug in _INCEPTION_SLUGS:
        kwargs['reasoning_effort'] = 'high' if reasoning else 'low'
        kwargs['web_search'] = web_search
    elif slug in _TRYINGOPEN_SLUGS:
        kwargs['effort'] = 'deep' if reasoning else 'quick'
    for chunk in mod.stream_chat(**kwargs):
        t = chunk.get('type')
        if t == 'text':
            yield {'type': 'text', 'content': chunk.get('content', '')}
        elif t == 'done':
            return
        elif t == 'error':
            yield {'type': 'error', 'error': chunk.get('error', 'upstream error')}
            return


def admin_chat(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    ctx = {'active_page': 'chat', 'providers': PROVIDERS, 'model_options': json.dumps(MODEL_OPTIONS)}
    return render(request, 'admin_panel/chat.html', ctx)

@require_POST
def ajax_admin_chat_send(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    provider = (request.POST.get('provider') or '').strip().lower()
    model = (request.POST.get('model') or '').strip()
    message = (request.POST.get('message') or '').strip()
    reasoning = request.POST.get('reasoning') == 'true'
    web_search = request.POST.get('web_search') == 'true'
    files = request.FILES.getlist('files') if provider in ('qwen', 'egov', 'deepai') else []

    if not message:
        return JsonResponse({'error': 'Message is required'}, status=400)

    try:
        history_raw = request.POST.get('history', '[]')
        history = json.loads(history_raw) if history_raw else []
    except (json.JSONDecodeError, TypeError):
        history = []

    msg_id = _uuid()

    def generate():
        yield _sse({'type': 'start', 'messageId': msg_id, 'thinking': reasoning, 'webSearch': web_search})

        if provider == 'qwen':
            from api import qwen_proxy
            try:
                file_paths = [f.name for f in files] if files else None
                result = qwen_proxy.call_qwen(
                    system_prompt='You are a helpful assistant.',
                    user_message=message,
                    model=model or 'qwen3.8-max',
                    max_tokens=2000,
                    file_paths=file_paths,
                )
                if result:
                    yield _sse({'type': 'text', 'content': result})
                else:
                    yield _sse({'type': 'error', 'message': 'Empty response'})
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        elif provider in _SCRAPER_DISPATCH:
            try:
                default_model = MODEL_OPTIONS.get(provider, [{}])[0].get('id', '')
                for chunk in _iter_scraper_chunks(
                    provider, message, history,
                    model or default_model, reasoning, web_search,
                ):
                    if chunk.get('type') == 'text':
                        yield _sse({'type': 'text', 'content': chunk.get('content', '')})
                    elif chunk.get('type') == 'error':
                        yield _sse({'type': 'error', 'message': chunk.get('error', 'upstream error')})
                        break
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        elif provider == 'custom':
            from api.custom_provider import call_custom
            api_url = request.POST.get('api_url', '')
            api_key = request.POST.get('api_key', '')
            if not api_url:
                yield _sse({'type': 'error', 'message': 'Custom provider requires an API URL'})
                yield _sse_done()
                return
            try:
                result = call_custom(
                    api_url=api_url,
                    api_key=api_key,
                    model=model or '',
                    system_prompt='You are a helpful assistant.',
                    user_message=message,
                    max_tokens=2000,
                )
                if result:
                    yield _sse({'type': 'text', 'content': result})
                else:
                    yield _sse({'type': 'error', 'message': 'Empty response'})
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        else:
            from api.llm.registry import is_official_slug, preset as _preset
            from api.llm import client as llm_client
            from api.astroweb_bridge_views import _official_api_key
            if is_official_slug(provider):
                p = _preset(provider)
                default_m = p.default_model if p else ''
                target_model = model or default_m
                msgs = history + [{'role': 'user', 'content': message}]
                try:
                    for chunk in llm_client.chat_stream(
                        format=p.format if p else 'openai',
                        base_url=p.base_url if p else '',
                        api_key=_official_api_key(provider) or (p.key_env if p else '') or 'free',
                        model=target_model,
                        messages=msgs,
                        provider=provider,
                        max_tokens=2000,
                    ):
                        if chunk.get('type') == 'text':
                            yield _sse({'type': 'text', 'content': chunk.get('content', '')})
                        elif chunk.get('type') == 'error':
                            yield _sse({'type': 'error', 'message': chunk.get('error', 'upstream error')})
                            break
                except Exception as e:
                    yield _sse({'type': 'error', 'message': str(e)})
            else:
                yield _sse({'type': 'error', 'message': f'Unknown provider: {provider}'})

        yield _sse({'type': 'done', 'finishReason': 'stop'})
        yield _sse_done()

    response = StreamingHttpResponse(generate(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response
