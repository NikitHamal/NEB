"""Engine behind the admin chat test: catalog, live model lists, one streaming
turn per provider, and the cooldown retry. Native path only: a provider that
cannot answer reports its own error, nothing is rerouted to another provider.
"""
import importlib
import re
import time

from django.core.cache import cache

from api.llm.registry import admin_catalog

_CAPS = {
    'qwen': (True, True, True, False), 'deepai': (True, True, False, True),
    'inception': (True, True, True, False), 'k2think': (True, True, False, False),
    'poolside': (True, False, True, False), 'motiftech': (True, True, False, False),
    'metaai': (True, True, False, False), 'longcat': (True, True, True, False),
    'geminiweb': (True, False, True, False), 'yqcloud': (True, False, True, False),
    'chatjimmy': (False, False, False, False), 'unikey': (True, True, False, False),
    'ptero': (False, False, False, False),
}
_DISPATCH = {  # slug -> (kind, module)   legacy = deepai style, messages = the rest
    'deepai': ('legacy', 'deepai_proxy'), 'inception': ('messages', 'inception_proxy'),
    'k2think': ('messages', 'k2think_proxy'), 'poolside': ('messages', 'poolside_proxy'),
    'motiftech': ('messages', 'motiftech_proxy'), 'metaai': ('messages', 'metaai_proxy'),
    'longcat': ('messages', 'longcat_proxy'), 'geminiweb': ('messages', 'geminiweb_proxy'),
    'yqcloud': ('messages', 'yqcloud_proxy'), 'chatjimmy': ('messages', 'chatjimmy_proxy'),
    'unikey': ('messages', 'unikey_proxy'), 'ptero': ('messages', 'ptero_proxy'),
}
_TRANSIENT = re.compile(r'429|rate.?limit|too many|cooldown|cool.?down|busy|overload|try again|retry|temporar|'
                        r'502|503|504|timed? ?out|failed to respond|empty', re.I)
RETRY_ATTEMPTS = 3


def build_lists():
    cat = admin_catalog()
    official = {e['slug'] for e in cat['official']}
    providers, models = [], {}
    for e in cat['scrapers'] + cat['official']:
        slug = e['slug']
        if slug not in official and slug != 'qwen' and slug not in _DISPATCH:
            continue  # TTS and other non-chat presets
        s, t, w, f = _CAPS.get(slug, (True, False, False, False))
        providers.append({'id': slug, 'label': e['label'], 'stream': s, 'thinking': t, 'web_search': w,
                          'files': f, 'keyless': not e['key_required'], 'official': slug in official})
        models[slug] = e['models']
    providers.append({'id': 'custom', 'label': 'Custom endpoint', 'stream': False, 'thinking': False,
                      'web_search': False, 'files': False, 'keyless': False, 'official': False})
    models['custom'] = []
    return providers, models


def _openai_live(slug):
    import requests
    from api.llm.registry import preset
    p = preset(slug)
    r = requests.get(p.base_url.rstrip('/') + '/models', timeout=20,
                     headers={'Authorization': f'Bearer {p.default_key or "x"}', **(p.extra_headers or {})})
    ids = [m['id'] for m in r.json()['data']]
    if slug == 'kilo':   # anonymous callers only reach the free tier
        ids = [i for i in ids if i == 'kilo-auto/free' or i.endswith(':free')]
    elif slug == 'zen':
        ids = [i for i in ids if i.endswith('-free') or i == 'big-pickle']
    elif slug == 'llm7':  # the anonymous aliases; the named models need a key
        ids = [i for i in ids if i in ('default', 'fast')] or ['default', 'fast']
    return [{'id': i, 'label': i} for i in ids]


def _ptero_state():
    st = cache.get('adminchat:ptero')
    if st is None:
        try:
            import requests
            st = requests.get('https://ptero.pro/wp-json/mlp/v1/status', timeout=8,
                              headers={'User-Agent': 'Mozilla/5.0'}).json()
        except Exception:
            st = {}
        cache.set('adminchat:ptero', st, 15)
    return st


def model_list(slug, registry_models):
    """Live list where the upstream publishes one, flagged with live availability."""
    key = f'adminchat:models:{slug}'
    out = cache.get(key)
    if out is None:
        out = None
        try:
            if slug == 'qwen':
                from api.qwen_utils.models import fetch_models
                out = [{'id': m['id'], 'label': m['name'] or m['id']} for m in fetch_models(True) if m.get('is_active')]
            elif slug in ('kilo', 'zen', 'llm7'):
                out = _openai_live(slug)
        except Exception:
            out = None
        out = out or [dict(m) for m in registry_models]
        cache.set(key, out, 600)
    out = [dict(m) for m in out]
    if slug == 'ptero':
        st = _ptero_state()
        down = set(st.get('disabled_models') or [])
        cool = set(st.get('cooldown_models') or [])
        for m in out:
            m['state'] = 'disabled' if m['id'] in down else 'cooldown' if m['id'] in cool else 'ready'
    return out


def _chunks(slug, model, message, history, reasoning, web_search):
    kind, mod_name = _DISPATCH[slug]
    mod = importlib.import_module(f'api.{mod_name}')
    if kind == 'legacy':
        for c in mod.stream_chat(user_message=message, model=model, history=history,
                                 system_prompt='You are a helpful assistant.'):
            t = c.get('type')
            if t == 'content':
                yield {'type': 'text', 'content': c.get('text', '')}
            elif t == 'error':
                yield {'type': 'error', 'message': c.get('message', 'upstream error')}
                return
        return
    kw = {'messages': history + [{'role': 'user', 'content': message}], 'model': model}
    if slug == 'inception':
        kw.update(reasoning_effort='high' if reasoning else 'low', web_search=web_search)
    elif slug == 'k2think':
        kw['reasoning_effort'] = 'high' if reasoning else 'low'
    elif slug == 'motiftech':
        kw['reasoning_effort'] = 'high' if reasoning else 'small'
    elif slug == 'geminiweb':
        kw['enable_search'] = web_search
    elif slug == 'longcat':
        kw.update(reasoning=reasoning, web_search=web_search)
    for c in mod.stream_chat(**kw):
        t = c.get('type')
        if t == 'text' and c.get('content'):
            yield {'type': 'text', 'content': c['content']}
        elif t in ('thought', 'thinking', 'reasoning'):
            yield {'type': 'thought', 'content': c.get('content') or c.get('thought') or c.get('thinking') or ''}
        elif t == 'search':
            yield {'type': 'search', 'content': c.get('text') or c.get('content') or '', 'results': c.get('results') or []}
        elif t == 'error':
            yield {'type': 'error', 'message': c.get('error') or 'upstream error'}
            return


def _official(slug, model, message, history, api_key):
    from api.llm import client
    from api.llm.registry import preset
    from api.astroweb_bridge_views import _official_api_key
    p = preset(slug)
    key = api_key or _official_api_key(slug) or p.default_key
    if not key and p.key_required:
        yield {'type': 'error', 'message': f'{p.label}: no API key configured'}
        return
    try:
        for c in client.chat_stream(format=p.format, base_url=p.base_url, api_key=key, model=model,
                                    messages=history + [{'role': 'user', 'content': message}],
                                    provider=slug, max_tokens=2000):
            t = c.get('type')
            if t == 'text' and c.get('content'):
                yield {'type': 'text', 'content': c['content']}
            elif t in ('reasoning', 'thought', 'thinking'):
                yield {'type': 'thought', 'content': c.get('content', '')}
    except Exception as exc:  # LLMError and transport errors alike
        yield {'type': 'error', 'message': str(exc)}


def _qwen(model, message, history, reasoning, web_search):
    from api import qwen_app
    yield from qwen_app.stream_chat(history + [{'role': 'user', 'content': message}], model, reasoning, web_search)


def _attempt(slug, model, message, history, reasoning, web_search, api_key, api_url):
    if slug == 'qwen':
        return _qwen(model, message, history, reasoning, web_search)
    if slug == 'custom':
        from api.custom_provider import call_custom
        text = call_custom(api_url=api_url, api_key=api_key, model=model, user_message=message,
                           system_prompt='You are a helpful assistant.', max_tokens=2000)
        return iter([{'type': 'text', 'content': text} if text else {'type': 'error', 'message': 'Empty response'}])
    if slug in _DISPATCH:
        if slug == 'ptero':
            st = _ptero_state()
            if model in (st.get('disabled_models') or []) or model in (st.get('cooldown_models') or []):
                return iter([{'type': 'error', 'message': f'ptero reports {model} is cooling down. Pick another model.'}])
        return _chunks(slug, model, message, history, reasoning, web_search)
    return _official(slug, model, message, history, api_key)


def run_turn(slug, model, message, history, reasoning=False, web_search=False, api_key='', api_url=''):
    """Yield events. A transient failure before any text is retried with a short wait."""
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        saw_text, err = False, ''
        try:
            for ev in _attempt(slug, model, message, history, reasoning, web_search, api_key, api_url):
                if ev['type'] == 'error':
                    err = ev['message']
                    break
                saw_text = saw_text or ev['type'] == 'text'
                yield ev
        except Exception as exc:
            err = str(exc)
        if saw_text or not err:
            return
        if attempt < RETRY_ATTEMPTS and _TRANSIENT.search(err) and 'cooling down' not in err:
            m = re.search(r'(?:retry[^0-9]{0,20}|after )(\d+(?:\.\d+)?)\s*s', err, re.I)
            wait = min(float(m.group(1)) + 0.2, 2.5) if m else 0.6 * attempt
            yield {'type': 'retry', 'attempt': attempt + 1, 'wait': round(wait, 1), 'reason': err[:140]}
            time.sleep(wait)
            continue
        yield {'type': 'error', 'message': err or 'No answer'}
        return
    yield {'type': 'error', 'message': 'No answer'}
