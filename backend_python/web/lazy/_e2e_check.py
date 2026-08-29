"""End-to-end smoke test for the Lazy agent runtime.

Stubs the model so the run costs nothing, then drives a real run through the
broker and asserts that a browser-style SSE subscriber sees the full life of
the run: start, plan, tool start/end, artifact, and a terminal done frame.

Run with:  .venv/Scripts/python.exe web/lazy/_e2e_check.py
"""

import os
import sys
import time

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402

from api.models import LazyAgentRun, LazyArtifact, User  # noqa: E402
from web.lazy import broker, llm  # noqa: E402

# The project enforces a strict host allowlist at the middleware layer; the test
# client presents "testserver", which would otherwise be rejected outright.
settings.ALLOWED_HOSTS = list(getattr(settings, 'ALLOWED_HOSTS', [])) + ['testserver', 'localhost']

FAILURES = []


def check(label, condition, detail=''):
    mark = 'PASS' if condition else 'FAIL'
    if not condition:
        FAILURES.append(label)
    print(f'  [{mark}] {label}' + (f' — {detail}' if detail else ''))


# --------------------------------------------------------------------------
# Stub model: turn 1 plans and writes a file, turn 2 verifies then finishes.
# --------------------------------------------------------------------------

STATE = {'turn': 0}


def fake_json_chat(user, system, prompt, max_tokens=2400, temperature=0.3,
                   timeout=90, model_key='neby-pro', attempts=2):
    STATE['turn'] += 1
    if STATE['turn'] == 1:
        return {
            'thought': 'The user wants a small project. I will write a script and verify it.',
            'plan': {
                'summary': 'Build and verify a small Python project',
                'items': [
                    {'id': 't1', 'text': 'Write the script', 'status': 'active'},
                    {'id': 't2', 'text': 'Run it to verify', 'status': 'pending'},
                ],
            },
            'calls': [{
                'name': 'write_file',
                'args': {
                    'path': 'src/main.py',
                    'content': 'values = [2, 4, 6]\nprint("sum:", sum(values))\n',
                },
            }],
            'done': False,
            'message': '',
        }, '{}'
    return {
        'thought': 'File written. Now execute it to prove it runs.',
        'plan': {
            'summary': 'Build and verify a small Python project',
            'items': [
                {'id': 't1', 'text': 'Write the script', 'status': 'done'},
                {'id': 't2', 'text': 'Run it to verify', 'status': 'active'},
            ],
        },
        'calls': [{'name': 'run_python', 'args': {'code': 'exec(open("src/main.py").read())'}}],
        'done': False,
        'message': '',
    }, '{}'


def fake_json_chat_finish(*args, **kwargs):
    return {
        'thought': 'The script ran and printed the expected sum.',
        'plan': {'summary': 'Build and verify a small Python project', 'items': [
            {'id': 't1', 'text': 'Write the script', 'status': 'done'},
            {'id': 't2', 'text': 'Run it to verify', 'status': 'done'},
        ]},
        'calls': [],
        'done': True,
        'message': 'Built and verified a small Python project — src/main.py prints the correct sum.',
    }, '{}'


def main():
    print('\nLazy agent — end-to-end runtime check\n')

    # The dev database carries throwaway rows with blank ids; pick a real one.
    user = User.objects.exclude(id='').filter(username='admin').first() or User.objects.exclude(id='').first()
    if user is None:
        print('  No usable users in the database; cannot run the check.')
        return 1
    print(f'  using {user.username} ({user.id})')

    llm.json_chat = fake_json_chat
    # Third turn onwards: finish.
    _orig = fake_json_chat

    def turn_switch(*a, **kw):
        if STATE['turn'] >= 2:
            return fake_json_chat_finish(*a, **kw)
        return _orig(*a, **kw)

    llm.json_chat = turn_switch

    client = Client()
    session = client.session
    session['user_id'] = str(user.id)
    session.save()

    print('1. Starting a run')
    resp = client.post(
        '/ajax/lazy/agent/run/',
        data='{"goal": "Build a tiny python project that sums a list and verify it runs"}',
        content_type='application/json',
    )
    check('run create returns 200', resp.status_code == 200, f'status={resp.status_code}')
    payload = resp.json()
    check('run create reports ok', payload.get('ok') is True, str(payload)[:160])
    run_id = payload.get('runId')
    check('run id present', bool(run_id), str(run_id))
    if not run_id:
        return 1

    print('\n2. Consuming the SSE stream as a browser would')
    stream = client.get(f'/ajax/lazy/agent/stream/{run_id}/')
    check('stream responds 200', stream.status_code == 200, f'status={stream.status_code}')
    check('stream is text/event-stream', 'text/event-stream' in stream['Content-Type'],
          stream['Content-Type'])

    types = []
    frames = []
    started = time.time()
    for raw in stream.streaming_content:
        line = raw.decode('utf-8').strip()
        if not line.startswith('data:'):
            continue
        body = line[5:].strip()
        if not body or body == '{}':
            continue
        import json
        try:
            frame = json.loads(body)
        except Exception:
            continue
        frames.append(frame)
        types.append(frame.get('type'))
        if frame.get('type') == 'done':
            break
        if time.time() - started > 60:
            break
    elapsed = time.time() - started

    check('stream completed without hanging', elapsed < 60, f'{elapsed:.1f}s')
    check('received run_start', 'run_start' in types)
    check('received think', 'think' in types)
    check('received plan', 'plan' in types)
    check('received tool_start', 'tool_start' in types)
    check('received tool_end', 'tool_end' in types)
    check('received done', 'done' in types, str(types))

    ok_frames = [f for f in frames if f.get('type') == 'tool_end']
    check('tool calls succeeded', all(f.get('ok') for f in ok_frames),
          str([(f.get('name'), f.get('ok')) for f in ok_frames]))

    run_py = [f for f in ok_frames if f.get('name') == 'run_python']
    check('sandbox executed python', bool(run_py) and run_py[0].get('ok'),
          (run_py[0].get('summary') if run_py else 'no run_python')[:120])

    # A blank observation makes the model believe the tool did nothing and redo
    # the work, so every successful call must come back with readable text.
    blank = [f.get('name') for f in ok_frames if not str(f.get('summary') or '').strip()]
    check('every tool reports a readable observation', not blank, str(blank))

    done_frame = next((f for f in frames if f.get('type') == 'done'), {})
    check('run finished ok', done_frame.get('ok') is True, str(done_frame)[:200])
    check('summary delivered', bool(done_frame.get('summary')), str(done_frame.get('summary'))[:120])

    print('\n3. Persisted state')
    run = LazyAgentRun.objects.get(id=run_id)
    check('run status is done', run.status == LazyAgentRun.STATUS_DONE, run.status)
    check('steps persisted', run.steps.count() >= 3, f'{run.steps.count()} steps')
    check('tool calls counted', run.tool_calls >= 2, str(run.tool_calls))
    check('plan persisted', bool(run.plan_json) and 'items' in run.plan_json)
    try:
        import json as _j
        meta = _j.loads(run.meta or '{}')
    except Exception:
        meta = {}
    check('summary saved to run meta', bool(meta.get('summary')), str(meta.get('summary'))[:80])

    from api.models import LazyDocMessage
    msgs = list(LazyDocMessage.objects.filter(session=run.session).order_by('created_at'))
    check('user message saved', any(m.role == 'user' for m in msgs), f'{len(msgs)} messages')
    check('assistant message saved', any(m.role == 'assistant' for m in msgs))

    print('\n4. Artifacts and workspace')
    listing = client.get(f'/ajax/lazy/agent/run/{run_id}/files/')
    check('workspace listing 200', listing.status_code == 200)
    files = listing.json().get('files') or []
    paths = [f['path'] for f in files]
    check('script written to workspace', 'src/main.py' in paths, str(paths)[:160])

    for f in files:
        dl = client.get(f['url'])
        check(f'download {f["path"]}', dl.status_code == 200, f'status={dl.status_code}')

    print('\n5. History replay after the run')
    hist = client.get(f'/ajax/lazy/agent/session/{run.session_id}/history/')
    check('history 200', hist.status_code == 200)
    hist_data = hist.json()
    check('history has messages', len(hist_data.get('messages') or []) >= 2,
          f'{len(hist_data.get("messages") or [])} messages')
    check('history has runs', len(hist_data.get('runs') or []) >= 1)

    print('\n6. Reconnect to a finished run (page reload)')
    broker.close_run(run_id)
    stream2 = client.get(f'/ajax/lazy/agent/stream/{run_id}/')
    types2 = []
    for raw in stream2.streaming_content:
        line = raw.decode('utf-8').strip()
        if not line.startswith('data:'):
            continue
        body = line[5:].strip()
        if not body or body == '{}':
            continue
        import json
        try:
            fr = json.loads(body)
        except Exception:
            continue
        types2.append(fr.get('type'))
        if fr.get('type') == 'done':
            break
    check('reload replays history', 'run_start' in types2 and 'done' in types2, str(types2))

    print('\n7. Cancellation stops real work')
    llm.json_chat = fake_json_chat  # never returns done
    r2 = client.post('/ajax/lazy/agent/run/', data='{"goal": "loop forever"}',
                     content_type='application/json').json()
    rid2 = r2.get('runId')
    time.sleep(1.2)
    cancelled = client.post(f'/ajax/lazy/agent/cancel/{rid2}/')
    check('cancel accepted', cancelled.status_code == 200 and cancelled.json().get('ok'))
    check('cancel flag set', broker.is_cancelled(rid2))
    deadline = time.time() + 20
    terminal = False
    while time.time() < deadline:
        st = LazyAgentRun.objects.filter(id=rid2).values_list('status', flat=True).first()
        if st in ('cancelled', 'done', 'failed'):
            terminal = True
            break
        time.sleep(0.3)
    final = LazyAgentRun.objects.filter(id=rid2).values_list('status', flat=True).first()
    check('run reaches cancelled', terminal and final == 'cancelled', str(final))

    # Handlers accumulate with `ctx.setdefault(key, []).append(...)`. Each call
    # receives a shallow copy of ctx, so those containers must be seeded in the
    # parent first — otherwise everything a handler records evaporates when the
    # call returns, silently disabling the artifact dedupe and the rebuild guard.
    print('\n8. Handler state survives the per-call ctx copy')
    from web.lazy import loop as _loop  # noqa: E402
    from web.lazy.registry import Param as _Param, ToolSpec as _ToolSpec  # noqa: E402

    parent = {'user': None, 'run_id': 'probe', 'persist': False}

    def _accumulating_handler(hctx, args):
        hctx.setdefault('artifacts', []).append({'name': args.get('k')})
        hctx.setdefault('_built_documents', []).append({'key': args.get('k')})
        hctx.setdefault('_registered_paths', set()).add(args.get('k'))
        return {'ok': True, 'summary': 'ok'}

    # The param must be declared or normalize_args drops it before the handler
    # ever sees it, and every probe call would look identical.
    _spec = _ToolSpec(name='probe', summary='', handler=_accumulating_handler,
                      params=[_Param('k', 'string')])

    class _Reg:
        def get(self, _name):
            return _spec

    for _k in ('one', 'two', 'three'):
        _loop._run_one_call(_Reg(), parent, None, 1, {'name': 'probe', 'args': {'k': _k}})

    check('artifacts accumulate across calls', len(parent.get('artifacts') or []) == 3,
          str(len(parent.get('artifacts') or [])))
    check('build history accumulates across calls',
          len(parent.get('_built_documents') or []) == 3,
          str(len(parent.get('_built_documents') or [])))
    check('registered paths accumulate across calls',
          len(parent.get('_registered_paths') or []) == 3,
          str(len(parent.get('_registered_paths') or [])))

    print('\n' + '=' * 60)
    if FAILURES:
        print(f'{len(FAILURES)} FAILED:')
        for f in FAILURES:
            print(f'  - {f}')
        return 1
    print('ALL CHECKS PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main())
