"""Live probe of every keyless chat provider, native path only.

    cd backend_python && python api/probe_keyless_chat.py [slug[:model] ...]

Each provider is called through its own proxy with a one-line identity
question. Prints ok/FAIL, latency, the model the upstream says it is, and the
first words of the reply. Nothing is written anywhere. Use it before adding a
model id to `api/llm/registry.py`: an id that is not in the upstream list or
does not answer here must not be shipped.
"""
import importlib
import os
import sys
import time
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

def _load_env():
    path = os.path.join(os.path.dirname(HERE), '.env')
    if not os.path.exists(path):
        return
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY='probe',
        CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
        INSTALLED_APPS=[],
    )
    django.setup()

# The native path only: a provider that needs another provider's help is not
# working. Neutralise the substitution mesh if this checkout still has it.
try:
    import api.keyless_fallback as _kf
    _kf.stream_keyless_fallback = lambda *a, **k: iter(())
    _kf.simple_keyless_fallback = lambda *a, **k: ''
except ImportError:
    pass

PROMPT = 'Reply with one short sentence: which model are you and who made you?'

# slug -> proxy module, default model
TARGETS = {
    'deepai': ('deepai_proxy', 'standard'),
    'qwencloud': ('qwencloud_proxy', None),
    'inception': ('inception_proxy', None),
    'k2think': ('k2think_proxy', None),
    'poolside': ('poolside_proxy', None),
    'motiftech': ('motiftech_proxy', None),
    'tryingopen': ('tryingopen_proxy', None),
    'longcat': ('longcat_proxy', None),
    'geminiweb': ('geminiweb_proxy', None),
    'yqcloud': ('yqcloud_proxy', None),
    'chatjimmy': ('chatjimmy_proxy', None),
    'unikey': ('unikey_proxy', None),
    'ptero': ('ptero_proxy', None),
    'metaai': ('metaai_proxy', None),
}


OPENAI_STYLE = ('llm7', 'kilo', 'zen')


def _openai_style(slug, model):
    import requests
    from api.llm.registry import preset
    p = preset(slug)
    model = model or p.default_model
    t0 = time.time()
    try:
        r = requests.post(
            p.base_url.rstrip('/') + '/chat/completions',
            headers={'Authorization': f'Bearer {p.default_key or "anonymous"}', 'User-Agent': 'Mozilla/5.0'},
            json={'model': model, 'messages': [{'role': 'user', 'content': PROMPT}], 'max_tokens': 120},
            timeout=60,
        )
        data = r.json()
        text = (data.get('choices') or [{}])[0].get('message', {}).get('content') or ''
        return slug, model, bool(text.strip()), time.time() - t0, text or f'HTTP {r.status_code} {str(data)[:120]}'
    except Exception as exc:  # noqa: BLE001
        return slug, model, False, time.time() - t0, f'{type(exc).__name__}: {exc}'


def _qwen(slug, model):
    from api.qwen_proxy import call_qwen
    model = model or 'qwen3.8-max'
    t0 = time.time()
    out = call_qwen('', PROMPT, model=model, max_tokens=200)
    return slug, model, bool(out), time.time() - t0, out or ''


def audit_openai_style():
    """Registry ids that the upstream /models list does not contain."""
    import requests
    from api.llm.registry import preset
    for slug in OPENAI_STYLE:
        p = preset(slug)
        try:
            r = requests.get(p.base_url.rstrip('/') + '/models', headers={'Authorization': f'Bearer {p.default_key or "x"}'}, timeout=30)
            live = {m['id'] for m in r.json()['data']}
        except Exception as exc:  # noqa: BLE001
            print(f'audit {slug}: models list failed: {exc}')
            continue
        gone = [m.id for m in p.models if m.id not in live]
        print(f'audit {slug}: {len(p.models)} listed, not in upstream: {gone or "none"}')


def _run(slug, model):
    if slug in OPENAI_STYLE:
        return _openai_style(slug, model)
    if slug == 'qwen':
        return _qwen(slug, model)
    mod = importlib.import_module(f'api.{TARGETS[slug][0]}')
    kw = {'model': model} if model else {}
    t0 = time.time()
    try:
        out = mod.simple_chat(user_message=PROMPT, **kw)
    except Exception as exc:  # noqa: BLE001
        return slug, model, False, time.time() - t0, f'{type(exc).__name__}: {exc}'
    text = (out or '').strip()
    bad = (not text) or text.startswith('[Error]')
    return slug, model, not bad, time.time() - t0, text


def main(argv):
    if argv:
        jobs = []
        for a in argv:
            slug, _, model = a.partition(':')
            jobs.append((slug, model or None))
    else:
        audit_openai_style()
        jobs = [(s, TARGETS[s][1]) for s in TARGETS] + [('qwen', None)] + [(s, None) for s in OPENAI_STYLE]
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(_run, s, m) for s, m in jobs]
        for f in cf.as_completed(futs):
            slug, model, ok, dt, text = f.result()
            print(f"{'ok  ' if ok else 'FAIL'} {slug:11s} {str(model or 'default'):34s} {dt:5.1f}s  {text[:160]!r}")


if __name__ == '__main__':
    main(sys.argv[1:])
