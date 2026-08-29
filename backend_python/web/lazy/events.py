"""SSE frame builders shared by the agent loop and the streaming view.

Every frame is a plain dict so the view can `json.dumps` it straight onto the
wire. Keeping the vocabulary in one file means the JS harness and the Python
loop can never drift apart silently.
"""

RUN_START = 'run_start'
PLAN = 'plan'
THINK = 'think'
STATUS = 'status'
TOOL_START = 'tool_start'
TOOL_END = 'tool_end'
ARTIFACT = 'artifact'
DOC = 'doc'
DELTA = 'delta'
MESSAGE = 'message'
ERROR = 'error'
DONE = 'done'


def run_start(run_id, goal, title=''):
    return {'type': RUN_START, 'runId': run_id, 'goal': goal, 'title': title}


def plan(summary, items):
    return {'type': PLAN, 'summary': summary or '', 'items': items or []}


def think(content):
    return {'type': THINK, 'content': content or ''}


def status(label, tool=''):
    return {'type': STATUS, 'label': label or '', 'tool': tool or ''}


def tool_start(name, args, label=''):
    return {
        'type': TOOL_START,
        'name': name,
        'args': _safe_args(args),
        'label': label or _humanize(name),
    }


def tool_end(name, ok, summary='', duration_ms=0):
    return {
        'type': TOOL_END,
        'name': name,
        'ok': bool(ok),
        'summary': (summary or '')[:600],
        'durationMs': int(duration_ms or 0),
    }


def artifact(art_id, kind, name, url, size=0, mime='', extra=None):
    frame = {
        'type': ARTIFACT,
        'id': art_id,
        'kind': kind,
        'name': name,
        'url': url,
        'size': int(size or 0),
        'mime': mime or '',
    }
    if extra:
        frame.update(extra)
    return frame


def doc(title, html):
    return {'type': DOC, 'title': title or '', 'html': html or ''}


def delta(content):
    return {'type': DELTA, 'content': content or ''}


def message(content):
    return {'type': MESSAGE, 'content': content or ''}


def error(message_text, recoverable=True):
    return {'type': ERROR, 'message': message_text or '', 'recoverable': bool(recoverable)}


def done(ok=True, summary='', artifacts=None, error_text=''):
    return {
        'type': DONE,
        'ok': bool(ok),
        'summary': summary or '',
        'artifacts': artifacts or [],
        'error': error_text or '',
    }


def _humanize(name):
    return str(name or '').replace('_', ' ').replace('-', ' ').strip().title() or 'Working'


def _safe_args(args):
    """Trim argument previews so a 40k-character file body never hits the wire."""
    if not isinstance(args, dict):
        return {}
    out = {}
    for key, value in list(args.items())[:8]:
        if isinstance(value, (dict, list)):
            out[key] = f'<{type(value).__name__} {len(value)} items>'
        else:
            text = str(value)
            out[key] = text[:160] + ('…' if len(text) > 160 else '')
    return out
