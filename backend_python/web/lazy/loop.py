"""The agent loop: plan -> act -> observe, with persistence and live events.

The loop is deliberately a pure orchestrator. It builds context, calls the LLM,
dispatches tool calls against the registry, appends results to the transcript,
persists every step to the database, and emits SSE frames. All it needs is a
registry, a run context and a sink for events.
"""

import concurrent.futures
import json
import time

from api.utils import now_ms

from . import broker, context, events, llm, summarize
from .registry import missing_required, normalize_args, rejected_args

DEFAULT_MAX_ITERATIONS = 14


def run(run_obj, registry, ctx, on_event=None, on_step=None, max_iterations=None):
    """Execute one Lazy run end-to-end.

    The caller is expected to have already saved the run row in `running` status
    and created the workspace. This function drives the LLM loop, dispatches
    tool calls, persists every visible step, and emits live SSE frames.
    """
    max_iterations = max(1, min(40, int(max_iterations or run_obj.max_iterations or DEFAULT_MAX_ITERATIONS)))

    def emit(frame):
        if on_event:
            on_event(frame)
        if on_step:
            on_step(frame.get('type'), frame)

    emit(events.run_start(run_obj.id, run_obj.goal or '', run_obj.title or ''))

    transcript = _load_transcript(run_obj)
    plan = _load_plan(run_obj) or {'summary': '', 'items': []}

    workspace_note = _workspace_note(ctx)
    system_prompt = context.build_system_prompt(registry, workspace_note)

    sources = ctx.get('sources') or []
    if sources:
        names = ', '.join(str(s.get('name') or s.get('path') or s) for s in sources[:8])
        workspace_note = (workspace_note + f"\n\nATTACHED FILES (use these for the pdf_tool): {names}").strip()

    for iteration in range(1, max_iterations + 1):
        # A browser "Cancel" must stop burning model calls on the next boundary
        # rather than after the current step finishes.
        if broker.is_cancelled(run_obj.id):
            emit(events.status('Stopping — cancelled by you'))
            _finalize(run_obj, plan, transcript, ok=False, message='Cancelled by you.',
                      status=run_obj.STATUS_CANCELLED)
            return

        run_obj.iteration = iteration
        prompt = context.build_turn_prompt(
            goal=run_obj.goal or '',
            plan=plan,
            transcript=transcript,
            workspace_note=workspace_note,
            attachments=sources,
        )
        data, raw = llm.json_chat(
            user=ctx['user'], system=system_prompt, prompt=prompt,
            max_tokens=2400, temperature=0.4, model_key=run_obj.model_key or 'neby-pro',
        )
        if not data:
            # Losing the model on the last turn is an upstream hiccup, not a
            # failed job — if the run already produced files the user still has
            # their deliverable, so close it out cleanly instead of showing a
            # red failure next to a perfectly good document.
            produced = list(ctx.get('artifacts') or [])
            if produced and iteration > 1:
                emit(events.status('Model connection lost — wrapping up with what is already built'))
                _finalize(
                    run_obj, plan, transcript, ok=True, force_done=True,
                    message=f'Finished your deliverable ({len(produced)} file(s) above); '
                            'the model dropped out on the final check, so nothing was lost.',
                )
                return
            emit(events.error('The model could not be reached. Please retry.', recoverable=True))
            run_obj.status = run_obj.STATUS_FAILED
            run_obj.error = 'llm unavailable'
            run_obj.finished_at = now_ms()
            run_obj.save(update_fields=['status', 'iteration', 'error', 'finished_at', 'updated_at'])
            return

        turn_record = {'n': iteration, 'thought': data.get('thought') or ''}
        thought = (data.get('thought') or '').strip()
        if thought:
            emit(events.think(thought[:1200]))
            _persist_step(run_obj, iteration, 'think', thought[:300], {'detail': thought[:2000]})

        new_plan = data.get('plan')
        if isinstance(new_plan, dict) and (new_plan.get('items') or new_plan.get('summary')):
            plan = new_plan
            run_obj.plan_json = json.dumps(plan, ensure_ascii=False)
            _persist_step(run_obj, iteration, 'plan', plan.get('summary') or '', {'plan': plan})
            emit(events.plan(plan.get('summary') or '', plan.get('items') or []))

        calls = _coerce_calls(data.get('calls'))
        turn_record['calls'] = calls

        if data.get('done') and not calls:
            # Deliberately no terminal frame here: the caller publishes `done`
            # only once the run is fully persisted. Emitting it early would let
            # the browser close the stream and read a half-written run.
            _finalize(run_obj, plan, transcript, ok=True, message=data.get('message') or 'Done')
            return

        if not calls and not data.get('done'):
            emit(events.message(data.get('message') or 'I did not find anything to do.'))
            _finalize(run_obj, plan, transcript, ok=True, message=data.get('message') or '')
            return

        observations = _dispatch_calls(
            run_obj=run_obj, iteration=iteration, calls=calls,
            registry=registry, ctx=ctx, emit=emit,
        )
        turn_record['observations'] = observations
        transcript.append(turn_record)

        if len(transcript) > 8:
            transcript = _compact_transcript(transcript)

        run_obj.transcript_json = json.dumps(transcript, ensure_ascii=False)[:50000]
        run_obj.tool_calls = int(run_obj.tool_calls or 0) + len(calls)
        run_obj.updated_at = now_ms()
        run_obj.save(update_fields=['iteration', 'transcript_json', 'tool_calls', 'plan_json', 'updated_at'])

        if data.get('done'):
            _finalize(run_obj, plan, transcript, ok=True, message=data.get('message') or 'Done.')
            return

    emit(events.error(f'Reached the {max_iterations}-step limit without finishing. Reviewing what I have so far.', recoverable=True))
    _finalize(run_obj, plan, transcript, ok=True, message='Step limit reached; current outputs are available above.', force_done=True)


# --------------------------------------------------------------------------
# Internals
# --------------------------------------------------------------------------

def _coerce_calls(raw):
    out = []
    if not isinstance(raw, list):
        return out
    for entry in raw[:5]:
        if not isinstance(entry, dict):
            continue
        name = entry.get('name') or entry.get('tool') or entry.get('action')
        if not name:
            continue
        args = entry.get('args') if isinstance(entry.get('args'), dict) else entry
        out.append({'name': str(name), 'args': args if isinstance(args, dict) else {}})
    return out


def _load_transcript(run_obj):
    try:
        data = json.loads(run_obj.transcript_json or '[]')
    except Exception:
        data = []
    if not isinstance(data, list):
        data = []
    return data[-8:]


def _load_plan(run_obj):
    try:
        data = json.loads(run_obj.plan_json or '{}')
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault('summary', '')
    data.setdefault('items', [])
    return data


def _compact_transcript(transcript):
    """Keep recent turns verbatim; summarise older ones to bound the prompt."""
    if len(transcript) <= 6:
        return transcript
    head, tail = transcript[:-4], transcript[-4:]
    summary_turns = []
    for turn in head:
        calls = ', '.join(c.get('name') or '?' for c in turn.get('calls') or [])
        snippet = (turn.get('thought') or '')[:160]
        summary_turns.append({'n': turn.get('n'), 'thought': f'(summary) {snippet}', 'calls': turn.get('calls') or []})
    return summary_turns + tail


def _workspace_note(ctx):
    try:
        from . import sandbox
        listing = sandbox.list_files(ctx['run_id'], limit=120)
    except Exception as exc:
        return f'(workspace unavailable: {exc})'
    files = listing.get('files') or []
    if not files:
        return 'WORKSPACE: empty'
    lines = ['WORKSPACE FILES:']
    for entry in files[:60]:
        size_kb = max(1, int(entry.get('size', 0) or 0) // 1024)
        lines.append(f'  {entry["path"]} ({size_kb} KB)')
    if len(files) > 60:
        lines.append(f'  …and {len(files) - 60} more')
    return '\n'.join(lines)


def _dispatch_calls(run_obj, iteration, calls, registry, ctx, emit):
    read_only = [c for c in calls if registry.get(c['name']) and registry.get(c['name']).concurrent_safe]
    mutating = [c for c in calls if c not in read_only]

    observations = []
    if read_only:
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(read_only))) as pool:
            futures = {pool.submit(_run_one_call, registry, ctx, run_obj, iteration, call): call for call in read_only}
            for fut in concurrent.futures.as_completed(futures):
                observations.append(fut.result())

    for call in mutating:
        if broker.is_cancelled(run_obj.id):
            observations.append({'name': call.get('name') or '?', 'ok': False, 'error': 'cancelled', 'result': 'cancelled'})
            continue
        observations.append(_run_one_call(registry, ctx, run_obj, iteration, call))

    return observations


def _run_one_call(registry, ctx, run_obj, iteration, call):
    spec = registry.get(call.get('name'))
    if not spec:
        return {'name': call.get('name') or '?', 'ok': False, 'error': f'unknown tool {call.get("name")}'}

    args = normalize_args(spec, call.get('args') or {})
    missing = missing_required(spec, args)
    if missing:
        rejected = rejected_args(spec, call.get('args') or {})
        # "missing required args: spec" tells the model nothing when it did
        # send a spec — we just could not read it. It reads that as truncation
        # and re-sends the same broken payload. Name the rejection instead.
        detail = '; '.join(
            f'{rejected.get(name) or "not provided"}'
            for name in missing if rejected.get(name)
        )
        if detail:
            return {'name': spec.name, 'ok': False,
                    'error': f'{", ".join(missing)} was rejected: {detail}'}
        return {'name': spec.name, 'ok': False, 'error': f'missing required args: {", ".join(missing)}'}

    started = time.time()
    # Handlers accumulate state with `ctx.setdefault(key, []).append(...)`. The
    # copy below is shallow, so seeding these in the parent first makes the
    # handler share the very same container objects — otherwise every
    # accumulator is created inside the throwaway copy and silently lost when
    # the call returns.
    for _shared, _empty in (('artifacts', list), ('_built_documents', list),
                            ('_registered_paths', set)):
        if not isinstance(ctx.get(_shared), _empty):
            ctx[_shared] = _empty()
    handler_ctx = dict(ctx)
    handler_ctx['iteration'] = iteration
    handler_ctx.setdefault('run_obj', run_obj)

    if callable(getattr(ctx, 'emit', None)):
        ctx['emit'](events.tool_start(spec.name, args, label=spec.summary))
    else:
        _safe_emit(ctx, events.tool_start(spec.name, args, label=spec.summary))

    _persist_step(run_obj, iteration, 'tool', spec.name, {'args': _trim_args(args), 'phase': 'start'})

    try:
        result = spec.handler(handler_ctx, args)
    except Exception as exc:
        result = {'ok': False, 'error': f'{type(exc).__name__}: {exc}'[:240]}

    duration = int((time.time() - started) * 1000)
    if not isinstance(result, dict):
        result = {'ok': True, 'result': result}
    ok = bool(result.get('ok'))
    # Handlers return structured payloads and often omit prose. An unreadable
    # observation makes the model think the tool did nothing and repeat it, so
    # every result is rendered into a sentence here as a last resort.
    summary = str(result.get('summary') or result.get('text') or '')[:600]
    if not summary.strip():
        summary = summarize.describe(spec.name, result)

    _safe_emit(ctx, events.tool_end(spec.name, ok, summary, duration))
    _persist_step(run_obj, iteration, 'tool', spec.name, {'args': _trim_args(args), 'ok': ok, 'summary': summary, 'durationMs': duration, 'error': result.get('error') or ''})

    if result.get('html') and not ctx.get('doc_html'):
        ctx['doc_html'] = result['html']

    observation = {'name': spec.name, 'ok': ok, 'result': summary, 'error': result.get('error') or ''}
    if ctx.get('doc_html') and result.get('html'):
        observation['htmlPreview'] = True
    return observation


def _safe_emit(ctx, frame):
    cb = ctx.get('emit')
    if callable(cb):
        try:
            cb(frame)
        except Exception:
            pass


def _trim_args(args):
    out = {}
    for key, value in (args or {}).items():
        if isinstance(value, str) and len(value) > 240:
            out[key] = value[:240] + '…'
        elif isinstance(value, (dict, list)):
            try:
                out[key] = json.dumps(value, ensure_ascii=False)[:400]
            except Exception:
                out[key] = f'<{type(value).__name__}>'
        else:
            out[key] = value
    return out


def _persist_step(run_obj, iteration, kind, title, detail):
    try:
        from api.models import LazyAgentStep
        from api.utils import uuid_str
        step_index = LazyAgentStep.objects.filter(run=run_obj).count() + 1
        LazyAgentStep.objects.create(
            id=uuid_str(),
            run=run_obj,
            index=step_index,
            iteration=iteration,
            kind=kind,
            title=(title or '')[:300],
            detail=json.dumps(detail if isinstance(detail, dict) else {'value': str(detail)}, ensure_ascii=False)[:6000],
            status=str(detail.get('ok') if isinstance(detail, dict) and 'ok' in detail else 'ok'),
            created_at=now_ms(),
        )
    except Exception:
        pass


def _emit_final_artifacts(ctx, emit):
    for art in ctx.get('artifacts') or []:
        if not isinstance(art, dict):
            continue
        emit(events.artifact(
            art_id=art.get('id') or '',
            kind=art.get('kind') or 'other',
            name=art.get('name') or '',
            url=art.get('url') or '',
            size=art.get('size') or 0,
            mime=art.get('mime') or '',
        ))


def _finalize(run_obj, plan, transcript, ok=True, message='', force_done=False, status=None):
    if status is None:
        status = run_obj.STATUS_DONE if ok else run_obj.STATUS_FAILED
    run_obj.status = status
    run_obj.transcript_json = json.dumps(transcript or [], ensure_ascii=False)[:50000]
    run_obj.plan_json = json.dumps(plan or {}, ensure_ascii=False)
    run_obj.finished_at = now_ms()
    run_obj.updated_at = run_obj.finished_at
    if message:
        # The closing line the user reads in chat; kept on the run so a reload
        # can show the same summary the browser saw live.
        try:
            meta = json.loads(run_obj.meta or '{}')
            if not isinstance(meta, dict):
                meta = {}
        except Exception:
            meta = {}
        meta['summary'] = str(message)[:2000]
        run_obj.meta = json.dumps(meta, ensure_ascii=False)
    fields = ['status', 'transcript_json', 'plan_json', 'finished_at', 'updated_at']
    if message:
        fields.append('meta')
    run_obj.save(update_fields=fields)
