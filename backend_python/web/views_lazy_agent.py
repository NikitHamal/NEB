"""HTTP and SSE views for the autonomous Lazy agent.

These views create runs, stream their live event stream to the browser as
server-sent events, serve workspace artifacts, and expose thread history so a
reload reconstructs the full conversation.

The live event path is deliberately one-way: the agent worker thread publishes
into `lazy.broker`, and each SSE request subscribes to that run's channel. This
keeps the worker decoupled from HTTP — a disconnected browser never blocks or
crashes a run, and a reconnecting browser is replayed from the backlog.
"""

import json
import os
import time

from django.http import FileResponse, HttpResponseForbidden, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from api.models import LazyAgentRun, LazyAgentStep, LazyArtifact, LazyDocMessage, LazyDocSession
from api.utils import now_ms, uuid_str

from .lazy import broker, sandbox
from .lazy import DEFAULT_REGISTRY
from .lazy import events as lazy_events
from .lazy.loop import run as run_agent

# A stream that hears nothing for this long checks the database before assuming
# the worker is still thinking. Protects against a worker thread that died
# without publishing a terminal frame.
_SILENCE_TIMEOUT = 90.0


# --------------------------------------------------------------------------
# Auth helpers
# --------------------------------------------------------------------------

def _get_user(request):
    """Return the authenticated user or None.

    Accepts: session user_id, Authorization: Bearer <token>, ?token=...
    """
    from .views_lazy import _get_user_or_none
    user = _get_user_or_none(request)
    if user is not None:
        return user

    token = request.headers.get('Authorization', '').replace('Bearer ', '').strip() or request.GET.get('token', '').strip()
    if token:
        from api.models import User
        try:
            return User.objects.filter(auth_token=token).first()
        except Exception:
            return None
    return None


def _rate_limit(request, scope, limit, window=60):
    """Return a 429 response when the caller is over limit, else None.

    `view_helpers._rate_limit` answers a boolean, so the response is built here
    to keep every call site from having to remember that.
    """
    from .view_helpers import _rate_limit as over_limit
    try:
        if over_limit(request, scope, limit, window):
            return JsonResponse(
                {'ok': False, 'error': 'Too many requests — give Lazy a moment.'}, status=429,
            )
    except Exception:
        return None
    return None


# --------------------------------------------------------------------------
# Workspace UI
# --------------------------------------------------------------------------

@require_GET
def lazy_agent_page(request):
    """The Lazy agent workspace. Served at both /lazy/ and /lazy/agent/."""
    user = _get_user(request)
    if user is None:
        from django.shortcuts import redirect
        return redirect(f"{reverse('web:login')}?next=/lazy/")

    sessions = [
        {
            'id': s.id, 'title': s.title or 'New chat',
            'docTitle': s.doc_title or '', 'messageCount': s.message_count or 0,
            'updatedAt': int(s.updated_at or 0),
        }
        for s in LazyDocSession.objects.filter(user=user).order_by('-updated_at')[:60]
    ]
    credits = _credits_state(user)
    return render(request, 'web/lazy_agent.html', {
        'is_authenticated': True,
        'username': getattr(user, 'username', ''),
        'sessions_json': json.dumps(sessions, ensure_ascii=False),
        'credits_json': json.dumps(credits, ensure_ascii=False),
    })


def _credits_state(user):
    try:
        from .views_canvas import _canvas_credit_state
        unlimited, remaining, allowance = _canvas_credit_state(user)
        return {
            'remaining': max(0, int(remaining or 0)),
            'allowance': int(allowance or 0),
            'unlimited': bool(unlimited),
        }
    except Exception:
        return {'remaining': 0, 'allowance': 0, 'unlimited': False}


# --------------------------------------------------------------------------
# Run lifecycle
# --------------------------------------------------------------------------

@csrf_exempt
@require_POST
def agent_run_create(request):
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)

    rl = _rate_limit(request, 'lazy_agent_create', 30, 60)
    if rl is not None:
        return rl

    try:
        body = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        body = {}
    goal = (body.get('goal') or '').strip()
    if not goal:
        return JsonResponse({'ok': False, 'error': 'goal is required'}, status=400)
    title = (body.get('title') or goal[:80]).strip()[:200]
    session_id = (body.get('sessionId') or '').strip() or None
    model_key = (body.get('modelKey') or 'neby-pro').strip() or 'neby-pro'
    raw_sources = body.get('sources') or []
    if not isinstance(raw_sources, list):
        raw_sources = []

    session = None
    if session_id:
        session = LazyDocSession.objects.filter(id=session_id, user=user).first()
    if session is None:
        session = LazyDocSession.objects.create(
            id=uuid_str(), user=user, title=title, created_at=now_ms(), updated_at=now_ms(),
        )
    else:
        if not (session.title or '').strip() or session.title == 'New chat':
            session.title = title[:200]

    run = LazyAgentRun.objects.create(
        id=uuid_str(),
        user=user, session=session, goal=goal, title=title,
        status=LazyAgentRun.STATUS_QUEUED,
        model_key=model_key, max_iterations=18,
        plan_json=json.dumps({'summary': '', 'items': []}, ensure_ascii=False),
        transcript_json='[]',
        created_at=now_ms(), updated_at=now_ms(),
    )

    LazyDocMessage.objects.create(
        id=uuid_str(), session=session, role='user', content=goal[:40000],
        meta=json.dumps({
            'attachments': [{'name': s.get('name')} for s in raw_sources if isinstance(s, dict)][:8],
        }, ensure_ascii=False),
        created_at=now_ms(),
    )

    # Attachments are copied into the run workspace so tools operate on real
    # files on disk rather than in-memory blobs.
    sources = _materialize_sources(user, run.id, raw_sources)

    broker.open_run(run.id)
    broker.publish(run.id, lazy_events.run_start(run.id, goal, title))

    import threading
    threading.Thread(
        target=_worker, args=(run.id, sources), name=f'lazy-agent-{run.id[:8]}', daemon=True,
    ).start()

    return JsonResponse({
        'ok': True,
        'runId': run.id, 'sessionId': session.id,
        'streamUrl': reverse('web:ajax_lazy_agent_stream', args=[run.id]),
    })


def _materialize_sources(user, run_id, raw):
    """Resolve attached source references and drop them in `inputs/` on disk."""
    from .toolstore import get_source
    out = []
    for entry in raw or []:
        if not isinstance(entry, dict):
            continue
        token = entry.get('srcId') or entry.get('src_id') or entry.get('token')
        if not token:
            continue
        rec = get_source(token, user.id)
        if not rec:
            continue
        name = rec.get('name') or 'file'
        ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
        kind = rec.get('kind') or ext or 'file'
        safe_name = _safe_filename(name)
        rel = None
        data = rec.get('data') or b''
        if data:
            try:
                written = sandbox.write_file(run_id, f'inputs/{safe_name}', data)
                rel = written['path']
            except Exception:
                rel = None
        out.append({
            'name': name, 'kind': kind, 'mime': rec.get('mime') or '',
            'srcId': token, 'path': rel,
            'size': len(data) if data else 0,
        })
    return out


def _safe_filename(name):
    base = os.path.basename(str(name or 'file'))
    cleaned = ''.join(ch if (ch.isalnum() or ch in '._- ') else '_' for ch in base).strip()
    return (cleaned or 'file')[:120]


def _worker(run_id, sources):
    """Agent thread entry point. Never raises; always closes the broker channel."""
    try:
        run = LazyAgentRun.objects.get(id=run_id)
    except LazyAgentRun.DoesNotExist:
        broker.close_run(run_id)
        return

    run.status = LazyAgentRun.STATUS_RUNNING
    run.updated_at = now_ms()
    try:
        run.save(update_fields=['status', 'updated_at'])
    except Exception:
        pass

    def publish(frame):
        broker.publish(run_id, frame)

    ctx = {
        'user': run.user, 'run_id': run_id, 'run_obj': run,
        'session': run.session, 'sources': sources,
        'persist': True, 'emit': publish,
        'memory_mb': 512,
        'on_step': None,
    }

    ok = False
    message = ''
    try:
        run_agent(run_obj=run, registry=DEFAULT_REGISTRY, ctx=ctx, on_event=publish)
        run.refresh_from_db(fields=['status', 'meta', 'error'])
        ok = run.status == LazyAgentRun.STATUS_DONE
        try:
            message = (json.loads(run.meta or '{}') or {}).get('summary') or ''
        except Exception:
            message = ''
    except Exception as exc:
        message = f'Agent crashed: {exc}'
        publish(lazy_events.error(message, recoverable=False))
        try:
            run.status = LazyAgentRun.STATUS_FAILED
            run.error = f'{type(exc).__name__}: {exc}'[:400]
            run.finished_at = now_ms()
            run.save(update_fields=['status', 'error', 'finished_at'])
        except Exception:
            pass
    finally:
        _persist_assistant_message(run, ok, message)
        broker.finish(run_id, lazy_events.done(
            ok=ok,
            summary=message or ('Done.' if ok else 'Run failed.'),
            artifacts=[
                {'id': a.get('id'), 'kind': a.get('kind'), 'name': a.get('name'),
                 'url': a.get('url'), 'size': a.get('size'), 'mime': a.get('mime')}
                for a in (ctx.get('artifacts') or [])
            ],
            error_text='' if ok else (message or 'Run failed'),
        ))


def _persist_assistant_message(run, ok, summary):
    """Write the closing assistant turn so thread history replays identically."""
    session = run.session
    if session is None:
        return
    try:
        artifacts = [
            {'name': a.name, 'kind': a.kind, 'size': a.size, 'mime': a.mime,
             'url': f"/ajax/lazy/agent-artifact/{run.id}/{a.path}" if a.path else ''}
            for a in run.artifacts.all().order_by('created_at')[:40]
        ]
        LazyDocMessage.objects.create(
            id=uuid_str(), session=session, role='assistant',
            content=(summary or ('Done.' if ok else 'Run failed.'))[:40000],
            meta=json.dumps({
                'runId': run.id, 'ok': ok, 'files': artifacts,
                'docTitle': run.title or '', 'status': run.status,
            }, ensure_ascii=False),
            created_at=now_ms(),
        )
        session.message_count = LazyDocMessage.objects.filter(session=session).count()
        session.updated_at = now_ms()
        session.save(update_fields=['message_count', 'updated_at'])
    except Exception:
        pass


# --------------------------------------------------------------------------
# Live stream
# --------------------------------------------------------------------------

@require_GET
def agent_run_stream(request, run_id):
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    run = get_object_or_404(LazyAgentRun, id=run_id, user=user)

    # If the worker's channel is gone (process restart, or the run finished long
    # ago) rebuild it from the database so the client still gets everything.
    _ensure_channel(run)

    response = StreamingHttpResponse(
        _stream_generator(run_id), content_type='text/event-stream; charset=utf-8',
    )
    response['Cache-Control'] = 'no-cache, no-transform'
    response['X-Accel-Buffering'] = 'no'
    # Keeps intermediate proxies from closing an idle stream.
    response['Connection'] = 'keep-alive'
    return response


def _ensure_channel(run):
    """Rehydrate a broker channel from persisted steps when it is missing."""
    if broker.has_channel(run.id):
        return
    if run.status not in (
        LazyAgentRun.STATUS_DONE, LazyAgentRun.STATUS_FAILED, LazyAgentRun.STATUS_CANCELLED,
    ):
        # Run is queued/running but the worker thread is gone (server restarted).
        broker.open_run(run.id)
        broker.publish(run.id, lazy_events.error(
            'This run was interrupted by a server restart. Send a new message to continue.',
            recoverable=False,
        ))
        broker.finish(run.id, lazy_events.done(
            ok=False, summary='', error_text='Run interrupted by a server restart',
        ))
        try:
            run.status = LazyAgentRun.STATUS_FAILED
            run.error = 'interrupted by restart'
            run.finished_at = now_ms()
            run.save(update_fields=['status', 'error', 'finished_at'])
        except Exception:
            pass
        return

    broker.open_run(run.id)
    for frame in _initial_events(run):
        broker.publish(run.id, frame)
    try:
        summary = (json.loads(run.meta or '{}') or {}).get('summary') or ''
    except Exception:
        summary = ''
    broker.finish(run.id, lazy_events.done(
        ok=run.status == LazyAgentRun.STATUS_DONE,
        summary=summary or ('Done' if run.status == LazyAgentRun.STATUS_DONE else 'Run ended'),
        artifacts=_artifact_frames(run),
        error_text=run.error or '',
    ))


def _stream_generator(run_id):
    q = broker.subscribe(run_id)
    last_event = time.time()
    last_beat = time.time()
    try:
        while True:
            try:
                frame = q.get(timeout=0.8)
            except Exception:
                now = time.time()
                if now - last_beat > 12:
                    yield ': heartbeat\n\n'
                    last_beat = now
                # Nothing heard for a long time: confirm the run still exists
                # and is not terminal before waiting any longer.
                if now - last_event > _SILENCE_TIMEOUT and _run_is_terminal(run_id):
                    yield _sse_frame(lazy_events.done(ok=False, summary='', error_text='Run stopped responding'))
                    yield 'event: end\ndata: {}\n\n'
                    return
                continue

            last_event = time.time()
            if frame.get('type') == '_end':
                yield 'event: end\ndata: {}\n\n'
                return
            yield _sse_frame(frame)
            if frame.get('type') == 'done':
                yield 'event: end\ndata: {}\n\n'
                return
    finally:
        broker.unsubscribe(run_id, q)


def _run_is_terminal(run_id):
    try:
        status = LazyAgentRun.objects.filter(id=run_id).values_list('status', flat=True).first()
    except Exception:
        return True
    if status is None:
        return True
    return status in (
        LazyAgentRun.STATUS_DONE, LazyAgentRun.STATUS_FAILED, LazyAgentRun.STATUS_CANCELLED,
    )


def _sse_frame(payload):
    return f'data: {json.dumps(payload, ensure_ascii=False)}\n\n'


def _artifact_frames(run):
    out = []
    try:
        rows = list(run.artifacts.all().order_by('created_at')[:40])
    except Exception:
        rows = []
    for art in rows:
        out.append({
            'id': art.id, 'kind': art.kind, 'name': art.name, 'size': int(art.size or 0),
            'mime': art.mime or '',
            'url': f"/ajax/lazy/agent-artifact/{run.id}/{art.path}" if art.path else '',
        })
    return out


def _initial_events(run):
    """Rebuild the visible history of a finished run from persisted steps."""
    out = [lazy_events.run_start(run.id, run.goal or '', run.title or '')]
    try:
        plan = json.loads(run.plan_json or '{}')
    except Exception:
        plan = {}
    if plan and (plan.get('summary') or plan.get('items')):
        out.append(lazy_events.plan(plan.get('summary', ''), plan.get('items', [])))
    try:
        steps = list(run.steps.all().order_by('index')[:300])
    except Exception:
        steps = []
    for step in steps:
        try:
            detail = json.loads(step.detail or '{}')
        except Exception:
            detail = {}
        if not isinstance(detail, dict):
            detail = {}
        if step.kind == 'think':
            out.append(lazy_events.think(detail.get('detail') or step.title))
        elif step.kind == 'plan':
            out.append(lazy_events.plan(step.title, (detail.get('plan') or {}).get('items', [])))
        elif step.kind == 'tool':
            if detail.get('phase') == 'start':
                out.append(lazy_events.tool_start(step.title, detail.get('args') or {}, label=''))
            else:
                out.append(lazy_events.tool_end(
                    step.title, bool(detail.get('ok')), detail.get('summary') or '',
                    detail.get('durationMs') or 0,
                ))
        elif step.kind == 'artifact':
            out.append(lazy_events.artifact(
                detail.get('id', ''), detail.get('kind', ''), step.title,
                f"/ajax/lazy/agent-artifact/{run.id}/{detail.get('path', '')}",
                detail.get('size', 0), detail.get('mime', ''),
            ))
    return out


# --------------------------------------------------------------------------
# Control and inspection
# --------------------------------------------------------------------------

@csrf_exempt
@require_POST
def agent_run_cancel(request, run_id):
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    run = get_object_or_404(LazyAgentRun, id=run_id, user=user)
    if run.status in (LazyAgentRun.STATUS_DONE, LazyAgentRun.STATUS_FAILED, LazyAgentRun.STATUS_CANCELLED):
        return JsonResponse({'ok': True, 'alreadyFinished': True})

    # The loop polls this between iterations, so work actually stops rather than
    # the UI merely pretending it did.
    broker.request_cancel(run.id)
    run.status = LazyAgentRun.STATUS_CANCELLED
    run.finished_at = now_ms()
    run.save(update_fields=['status', 'finished_at'])
    broker.publish(run.id, lazy_events.status('Cancelling…'))
    return JsonResponse({'ok': True})


@require_GET
def agent_run_detail(request, run_id):
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    run = get_object_or_404(LazyAgentRun, id=run_id, user=user)
    steps = list(run.steps.all().order_by('index')[:300])
    return JsonResponse({
        'ok': True,
        'run': _serialize_run(run),
        'steps': [_serialize_step(s) for s in steps],
        'artifacts': _artifact_frames(run),
    })


@require_GET
def agent_runs_list(request):
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    try:
        limit = max(1, min(50, int(request.GET.get('limit') or 30)))
    except Exception:
        limit = 30
    runs = list(LazyAgentRun.objects.filter(user=user).order_by('-created_at')[:limit])
    return JsonResponse({'ok': True, 'runs': [_serialize_run(r) for r in runs]})


@require_GET
def agent_session_history(request, session_id):
    """Full replay of one thread: messages plus every artifact it produced."""
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    session = get_object_or_404(LazyDocSession, id=session_id, user=user)

    messages = []
    for m in session.messages.all().order_by('created_at', 'id')[:400]:
        try:
            meta = json.loads(m.meta or '{}')
            if not isinstance(meta, dict):
                meta = {}
        except Exception:
            meta = {}
        messages.append({
            'id': m.id, 'role': m.role, 'content': m.content or '',
            'meta': meta, 'createdAt': int(m.created_at or 0),
        })

    runs = [
        _serialize_run(r)
        for r in session.agent_runs.all().order_by('created_at')[:50]
    ]
    artifacts = []
    for art in LazyArtifact.objects.filter(session=session).order_by('created_at')[:60]:
        artifacts.append({
            'id': art.id, 'kind': art.kind, 'name': art.name, 'size': int(art.size or 0),
            'mime': art.mime or '',
            'url': f"/ajax/lazy/agent-artifact/{art.run_id}/{art.path}" if (art.path and art.run_id) else '',
        })

    return JsonResponse({
        'ok': True,
        'session': {
            'id': session.id, 'title': session.title or 'New chat',
            'docTitle': session.doc_title or '', 'docHtml': session.doc_html or '',
            'updatedAt': int(session.updated_at or 0),
        },
        'messages': messages,
        'runs': runs,
        'artifacts': artifacts,
    })


@require_GET
def agent_workspace_files(request, run_id):
    """Live listing of everything the agent has written into its workspace."""
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    run = get_object_or_404(LazyAgentRun, id=run_id, user=user)
    try:
        listing = sandbox.list_files(run.id, limit=250)
    except Exception:
        listing = {'files': []}
    files = []
    for entry in listing.get('files') or []:
        rel = entry.get('path') or ''
        files.append({
            'path': rel,
            'name': rel.rsplit('/', 1)[-1],
            'size': int(entry.get('size') or 0),
            'url': f"/ajax/lazy/agent-artifact/{run.id}/{rel}",
        })
    return JsonResponse({'ok': True, 'files': files})


def _serialize_run(run):
    try:
        plan = json.loads(run.plan_json or '{}')
    except Exception:
        plan = {}
    try:
        summary = (json.loads(run.meta or '{}') or {}).get('summary') or ''
    except Exception:
        summary = ''
    return {
        'id': run.id, 'title': run.title or '', 'goal': run.goal or '',
        'status': run.status, 'summary': summary,
        'createdAt': int(run.created_at or 0),
        'updatedAt': int(run.updated_at or 0), 'finishedAt': int(run.finished_at or 0),
        'iterations': int(run.iteration or 0), 'toolCalls': int(run.tool_calls or 0),
        'plan': plan, 'error': run.error or '',
        'sessionId': run.session_id or '',
    }


def _serialize_step(step):
    try:
        detail = json.loads(step.detail or '{}')
    except Exception:
        detail = {}
    return {
        'id': step.id, 'kind': step.kind, 'title': step.title,
        'iteration': int(step.iteration or 0), 'detail': detail, 'status': step.status,
        'createdAt': int(step.created_at or 0),
    }


# --------------------------------------------------------------------------
# Artifact serving
# --------------------------------------------------------------------------

_INLINE_TYPES = {'.html', '.txt', '.md', '.py', '.js', '.json', '.csv', '.svg', '.xml', '.css'}

_MIME = {
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.pdf': 'application/pdf',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.html': 'text/html; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    '.md': 'text/markdown; charset=utf-8',
    '.csv': 'text/csv; charset=utf-8',
    '.py': 'text/x-python; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.json': 'application/json; charset=utf-8',
    '.zip': 'application/zip',
    '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.webp': 'image/webp',
}


@require_GET
def agent_artifact(request, run_id, path):
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    run = get_object_or_404(LazyAgentRun, id=run_id, user=user)

    try:
        base = sandbox.workspace_path(run_id, create=False)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'workspace unavailable'}, status=404)
    full = os.path.abspath(os.path.join(base, str(path or '').replace('\\', '/')))
    if not full.startswith(os.path.abspath(base) + os.sep):
        return HttpResponseForbidden('path escapes workspace')
    if not os.path.isfile(full):
        return JsonResponse({'ok': False, 'error': 'not found'}, status=404)

    ext = os.path.splitext(full)[1].lower()
    mime = _MIME.get(ext, 'application/octet-stream')
    name = os.path.basename(full)

    # `download=1` forces a save dialog; everything else prefers inline preview
    # for types a browser can render, which is what the artifact cards use.
    wants_download = request.GET.get('download') in ('1', 'true', 'yes')
    disposition = 'attachment' if wants_download else ('inline' if ext in _INLINE_TYPES or ext in ('.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp') else 'attachment')

    response = FileResponse(open(full, 'rb'), content_type=mime, as_attachment=(disposition == 'attachment'))
    response['Content-Disposition'] = f'{disposition}; filename="{name}"'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_GET
def agent_artifact_raw(request, artifact_id):
    """Serve an artifact by its LazyArtifact id (works even if the run is old)."""
    user = _get_user(request)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'unauthenticated'}, status=401)
    art = get_object_or_404(LazyArtifact, id=artifact_id, user=user)
    if not art.path or not art.run_id:
        return JsonResponse({'ok': False, 'error': 'artifact has no stored file'}, status=404)
    return agent_artifact(request, art.run_id, art.path)
