import json, uuid
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .view_helpers import _require_admin

def _sse(obj):
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"

def _sse_done():
    return "data: [DONE]\n\n"

def _uuid():
    return str(uuid.uuid4())

PROVIDERS = [
    {'id': 'qwen',       'label': 'Qwen (chat.qwen.ai)',                           'stream': True,  'thinking': True,  'web_search': True,  'files': True},
    {'id': 'ai4bharat',  'label': 'AI4Bharat Arena (Indic LLM Arena)',             'stream': False, 'thinking': False, 'web_search': False, 'files': False},
    {'id': 'egov',       'label': 'eGov Chat AI (Philippines)',                    'stream': True,  'thinking': False, 'web_search': False, 'files': True},
    {'id': 'deepai',     'label': 'DeepAI (deepai.org)',                           'stream': True,  'thinking': True,  'web_search': False, 'files': True},
    {'id': 'inception',  'label': 'Inception Labs (Mercury 2)',                    'stream': True,  'thinking': True,  'web_search': True,  'files': False},
    {'id': 'custom',     'label': 'Custom OpenAI-compatible endpoint',             'stream': False, 'thinking': False, 'web_search': False, 'files': False},
]

MODEL_OPTIONS = {
    'qwen':      [{'id': 'qwen3.7-plus', 'label': 'Qwen 3.7 Plus'}, {'id': 'qwen3.7-max', 'label': 'Qwen 3.7 Max'}, {'id': 'qwen3.6-plus', 'label': 'Qwen 3.6 Plus'}],
    'ai4bharat': [],
    'egov':      [{'id': 'AI1', 'label': 'eGov AI1 (Global)'}, {'id': 'AI1-ph', 'label': 'eGov AI1 (Philippines)'}, {'id': 'AI2', 'label': 'eGov AI2 (Global)'}, {'id': 'AI2-ph', 'label': 'eGov AI2 (Philippines)'}],
    'deepai':    [{'id': 'standard', 'label': 'DeepAI Standard'}, {'id': 'deepseek-v3.2', 'label': 'DeepSeek V3.2'}, {'id': 'gemma-4', 'label': 'Gemma 4'}, {'id': 'gpt-4.1-nano', 'label': 'GPT-4.1 Nano'}, {'id': 'gpt-5-nano', 'label': 'GPT-5 Nano'}, {'id': 'gemini-2.5-flash-lite', 'label': 'Gemini 2.5 Flash Lite'}, {'id': 'llama-3.3-70b-instruct', 'label': 'Llama 3.3 70B'}, {'id': 'o4-mini', 'label': 'o4 Mini'}, {'id': 'gpt-4o-mini', 'label': 'GPT-4o Mini'}, {'id': 'gpt-oss-120b', 'label': 'GPT OSS 120B (Reasoning)'}],
    'inception': [{'id': 'mercury-2', 'label': 'Mercury 2 (default)'}, {'id': 'mercury-2-mini', 'label': 'Mercury 2 Mini'}],
    'custom':    [],
}

def admin_chat(request):
    admin = _require_admin(request)
    if isinstance(admin, JsonResponse):
        return admin
    ctx = {'active_page': 'chat', 'providers': PROVIDERS, 'model_options': json.dumps(MODEL_OPTIONS)}
    return render(request, 'admin_panel/chat.html', ctx)

def _stream_from_provider(provider, model, message, history, reasoning, web_search, files):
    """Normalize provider streaming to a common SSE format."""
    if provider == 'qwen':
        from api import qwen_proxy
        try:
            file_paths = [f.name for f in files] if files else None
            result = qwen_proxy.call_qwen(
                system_prompt='You are a helpful assistant.',
                user_message=message,
                model=model or 'qwen3.7-plus',
                max_tokens=2000,
                file_paths=file_paths,
            )
            if result:
                yield _sse({'type': 'text', 'content': result})
            else:
                yield _sse({'type': 'error', 'message': 'Empty response from Qwen'})
        except Exception as e:
            yield _sse({'type': 'error', 'message': str(e)})

    elif provider == 'ai4bharat':
        from api import ai4bharat_proxy
        try:
            result = ai4bharat_proxy.simple_chat(
                user_message=message,
                model_id=model or None,
                system_prompt='You are a helpful assistant.',
                max_tokens=2000,
            )
            if result:
                yield _sse({'type': 'text', 'content': result})
            else:
                yield _sse({'type': 'error', 'message': 'Empty response from AI4Bharat'})
        except Exception as e:
            yield _sse({'type': 'error', 'message': str(e)})

    elif provider == 'egov':
        from api import egov_proxy
        try:
            for chunk in egov_proxy.stream_chat(
                user_message=message,
                model=model or 'AI1',
                history=history or [],
                system_prompt='You are a helpful assistant.',
            ):
                t = chunk.get('type')
                if t == 'content':
                    yield _sse({'type': 'text', 'content': chunk.get('text', '')})
                elif t == 'done':
                    break
                elif t == 'error':
                    yield _sse({'type': 'error', 'message': chunk.get('message', 'upstream error')})
                    break
        except Exception as e:
            yield _sse({'type': 'error', 'message': str(e)})

    elif provider == 'deepai':
        from api import deepai_proxy
        try:
            for chunk in deepai_proxy.stream_chat(
                user_message=message,
                model=model or 'standard',
                history=history or [],
                system_prompt='You are a helpful assistant.',
            ):
                t = chunk.get('type')
                if t == 'content':
                    yield _sse({'type': 'text', 'content': chunk.get('text', '')})
                elif t == 'done':
                    break
                elif t == 'error':
                    yield _sse({'type': 'error', 'message': chunk.get('message', 'upstream error')})
                    break
        except Exception as e:
            yield _sse({'type': 'error', 'message': str(e)})

    elif provider == 'inception':
        from api import inception_proxy
        try:
            msgs = (history or []) + [{'role': 'user', 'content': message}]
            for chunk in inception_proxy.stream_chat(
                messages=msgs,
                model=model or 'mercury-2',
                reasoning_effort='high' if reasoning else 'low',
                web_search=web_search,
            ):
                t = chunk.get('type')
                if t == 'text':
                    yield _sse({'type': 'text', 'content': chunk.get('content', '')})
                elif t == 'done':
                    break
                elif t == 'error':
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
                yield _sse({'type': 'error', 'message': 'Empty response from custom endpoint'})
        except Exception as e:
            yield _sse({'type': 'error', 'message': str(e)})

@require_POST
def ajax_admin_chat_send(request):
    admin = _require_admin(request)
    if isinstance(admin, JsonResponse):
        return admin

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
                    model=model or 'qwen3.7-plus',
                    max_tokens=2000,
                    file_paths=file_paths,
                )
                if result:
                    yield _sse({'type': 'text', 'content': result})
                else:
                    yield _sse({'type': 'error', 'message': 'Empty response'})
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        elif provider == 'ai4bharat':
            from api import ai4bharat_proxy
            try:
                result = ai4bharat_proxy.simple_chat(
                    user_message=message,
                    model_id=model or None,
                    system_prompt='You are a helpful assistant.',
                    max_tokens=2000,
                )
                if result:
                    yield _sse({'type': 'text', 'content': result})
                else:
                    yield _sse({'type': 'error', 'message': 'Empty response'})
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        elif provider == 'egov':
            from api import egov_proxy
            try:
                for chunk in egov_proxy.stream_chat(
                    user_message=message,
                    model=model or 'AI1',
                    history=history,
                    system_prompt='You are a helpful assistant.',
                ):
                    t = chunk.get('type')
                    if t == 'content':
                        yield _sse({'type': 'text', 'content': chunk.get('text', '')})
                    elif t == 'done':
                        break
                    elif t == 'error':
                        yield _sse({'type': 'error', 'message': chunk.get('message', 'upstream error')})
                        break
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        elif provider == 'deepai':
            from api import deepai_proxy
            try:
                for chunk in deepai_proxy.stream_chat(
                    user_message=message,
                    model=model or 'standard',
                    history=history,
                    system_prompt='You are a helpful assistant.',
                ):
                    t = chunk.get('type')
                    if t == 'content':
                        yield _sse({'type': 'text', 'content': chunk.get('text', '')})
                    elif t == 'done':
                        break
                    elif t == 'error':
                        yield _sse({'type': 'error', 'message': chunk.get('message', 'upstream error')})
                        break
            except Exception as e:
                yield _sse({'type': 'error', 'message': str(e)})

        elif provider == 'inception':
            from api import inception_proxy
            try:
                msgs = history + [{'role': 'user', 'content': message}]
                for chunk in inception_proxy.stream_chat(
                    messages=msgs,
                    model=model or 'mercury-2',
                    reasoning_effort='high' if reasoning else 'low',
                    web_search=web_search,
                ):
                    t = chunk.get('type')
                    if t == 'text':
                        yield _sse({'type': 'text', 'content': chunk.get('content', '')})
                    elif t == 'done':
                        break
                    elif t == 'error':
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
            yield _sse({'type': 'error', 'message': f'Unknown provider: {provider}'})

        yield _sse({'type': 'done', 'finishReason': 'stop'})
        yield _sse_done()

    response = StreamingHttpResponse(generate(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response
