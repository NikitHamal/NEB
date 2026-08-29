"""Helpers shared by every Lazy tool module.

Kept separate so the per-domain modules can import them without importing
each other, which would create a cycle through `tools.build_registry`.
"""

import json
import os

from . import sandbox


def _safe(fn, *args, **kwargs):
    try:
        out = fn(*args, **kwargs)
        if isinstance(out, dict):
            out.setdefault('ok', True)
        return out if isinstance(out, dict) else {'ok': True, 'result': out}
    except sandbox.SandboxError as exc:
        return {'ok': False, 'error': f'sandbox: {exc}'}
    except Exception as exc:
        return {'ok': False, 'error': f'{type(exc).__name__}: {exc}'[:240]}


def _register_artifact(ctx, rel_path, kind='other', mime='', name=''):
    """Record an artifact in the run's in-memory registry and as a LazyArtifact row.

    ``rel_path`` is the workspace-relative path of the produced file. The actual
    filesystem path is resolved inside this function, so callers don't need to
    know where the workspace lives.
    """
    rel = (rel_path or '').replace('\\', '/') if isinstance(rel_path, str) else ''
    if not rel:
        return {'id': '', 'path': '', 'kind': kind, 'name': name}
    if not name:
        name = rel.rsplit('/', 1)[-1]

    # Tools like run_python re-scan the workspace on every call. Without this
    # guard the same file would be announced and stored once per invocation.
    already = ctx.setdefault('_registered_paths', set())
    if rel in already:
        existing = next(
            (a for a in ctx.get('artifacts', []) if a.get('path') == rel), None,
        )
        if existing:
            return existing
    already.add(rel)

    base = sandbox.workspace_path(ctx['run_id'], create=False)
    full = os.path.join(base, rel)
    try:
        size = os.path.getsize(full) if os.path.isfile(full) else 0
    except Exception:
        size = 0
    url = f"/ajax/lazy/agent-artifact/{ctx['run_id']}/{rel}"
    art_id = ''
    if ctx.get('persist'):
        try:
            from api.models import LazyAgentStep, LazyArtifact
            from api.utils import now_ms, uuid_str
            art = LazyArtifact.objects.create(
                id=uuid_str(),
                user=ctx['user'],
                run=ctx.get('run_obj'),
                session=ctx.get('session'),
                kind=kind,
                name=name,
                mime=mime or '',
                size=size,
                storage='workspace',
                path=rel,
                meta=json.dumps({'run_id': ctx.get('run_id')}, ensure_ascii=False),
                created_at=now_ms(),
            )
            art_id = art.id
            LazyAgentStep.objects.create(
                id=uuid_str(),
                run=ctx['run_obj'],
                index=int(ctx.get('step_index', 0)) + 1,
                iteration=int(ctx.get('iteration', 0)),
                kind='artifact',
                title=name,
                detail=json.dumps({'id': art_id, 'kind': kind, 'size': size, 'path': rel, 'mime': mime}, ensure_ascii=False),
                status='ok',
                created_at=now_ms(),
            )
        except Exception:
            art_id = ''
    record = {
        'id': art_id,
        'kind': kind,
        'name': name,
        'mime': mime,
        'size': size,
        'path': rel,
        'url': url,
    }
    ctx.setdefault('artifacts', []).append(record)

    # Announce it the moment it exists rather than waiting for the run to end,
    # so the browser shows download links while the agent is still working.
    emit = ctx.get('emit')
    if callable(emit):
        try:
            emit(dict(record, type='artifact'))
        except Exception:
            pass

    return dict(record)


def _save_artifact_bytes(ctx, name, mime, kind, data):
    full = sandbox.write_file(ctx['run_id'], f'outputs/{name}', data)
    art = _register_artifact(ctx, full['path'], kind=kind, mime=mime, name=name)
    return {'ok': True, 'artifact': art, 'path': full['path'], 'size': full['size']}
