import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from api.models import CanvasBoard, CanvasNebyRun, CanvasNode, CanvasSnapshot
from api.utils import now_ms, uuid_str
from .canvas_agent import create_plan_nodes, generate_plan, suggest_questions
from .canvas_history import board_payload, markdown_export, replace_board_from_payload, restore_snapshot, snapshot_board, snapshot_summary
from .canvas_templates import apply_template, template_catalog
from .view_helpers import _rate_limit
from .views_canvas import _call_llm_for_canvas, _canvas_credit_state, _require_user, _serialize_board, _serialize_node, _spend_canvas_credit


MAX_BOARD_NODES = 240
ALLOWED_KINDS = {'ai', 'note', 'question', 'source', 'comparison', 'practice', 'summary', 'task', 'decision', 'warning'}
ALLOWED_COLORS = {'default', 'blue', 'green', 'amber', 'rose', 'purple', 'slate'}


def _payload(request):
    try:
        data = json.loads(request.body or '{}')
        return data if isinstance(data, dict) else {}
    except (TypeError, ValueError):
        return {}


def _owned_board(user, board_id):
    return get_object_or_404(CanvasBoard, id=board_id, user=user)


@require_GET
def ajax_canvas_templates(request):
    user, err = _require_user(request)
    if err:
        return err
    return JsonResponse({'templates': template_catalog()})


@require_POST
def ajax_canvas_create_from_template(request):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_template_create', 12, 60):
        return JsonResponse({'error': 'Too many canvases created. Try again shortly.'}, status=429)
    data = _payload(request)
    key = str(data.get('template') or 'blank').strip().lower()
    catalog = {item['key']: item for item in template_catalog()}
    if key not in catalog:
        return JsonResponse({'error': 'Unknown canvas template'}, status=400)
    title = str(data.get('title') or catalog[key]['name']).strip()[:200] or catalog[key]['name']
    now = now_ms()
    board = CanvasBoard.objects.create(id=uuid_str(), user=user, title=title, created_at=now, updated_at=now)
    nodes = apply_template(board, user, key)
    board._node_count = len(nodes)
    return JsonResponse({'board': _serialize_board(board), 'nodes': [_serialize_node(node) for node in nodes]}, status=201)


@require_POST
def ajax_canvas_create_note(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_note_create', 40, 60):
        return JsonResponse({'error': 'Too many cards created. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    if CanvasNode.objects.filter(board=board).count() >= MAX_BOARD_NODES:
        return JsonResponse({'error': f'A canvas is limited to {MAX_BOARD_NODES} cards'}, status=400)
    data = _payload(request)
    title = str(data.get('title') or 'Note').strip()[:300] or 'Note'
    body = str(data.get('body') or '').strip()[:12000]
    kind = str(data.get('kind') or 'note').strip().lower()
    if kind not in ALLOWED_KINDS:
        kind = 'note'
    try:
        x = max(-100000.0, min(100000.0, float(data.get('x', 220))))
        y = max(-100000.0, min(100000.0, float(data.get('y', 160))))
    except (TypeError, ValueError):
        x, y = 220.0, 160.0
    parent_id = str(data.get('parentId') or '')
    parent = CanvasNode.objects.filter(id=parent_id, board=board).first() if parent_id else None
    meta = data.get('meta') if isinstance(data.get('meta'), dict) else {}
    color = str(meta.get('color') or 'default').lower()
    if color not in ALLOWED_COLORS:
        color = 'default'
    tags = meta.get('tags') if isinstance(meta.get('tags'), list) else []
    meta = {'color': color, 'tags': [str(tag).strip()[:32] for tag in tags[:8] if str(tag).strip()], 'pinned': bool(meta.get('pinned'))}
    content = {'title': title, 'summary': body[:500], 'sections': [{'type': 'text', 'content': body}] if body else []}
    now = now_ms()
    node = CanvasNode.objects.create(
        id=uuid_str(), board=board, parent=parent, user=user, prompt='', title=title,
        content=json.dumps(content, ensure_ascii=False), status='done', x=x, y=y,
        kind=kind, metadata=json.dumps(meta, ensure_ascii=False), created_at=now, updated_at=now,
    )
    board.updated_at = now
    board.save(update_fields=['updated_at'])
    return JsonResponse({'node': _serialize_node(node)}, status=201)


@require_POST
def ajax_canvas_node_update(request, node_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_node_update', 120, 60):
        return JsonResponse({'error': 'Too many card edits. Try again shortly.'}, status=429)
    node = CanvasNode.objects.select_related('board').filter(id=node_id, board__user=user).first()
    if not node:
        return JsonResponse({'error': 'Card not found'}, status=404)
    data = _payload(request)
    fields = []
    if 'title' in data:
        node.title = str(data.get('title') or 'Card').strip()[:300] or 'Card'
        fields.append('title')
    if 'body' in data:
        body = str(data.get('body') or '').strip()[:12000]
        try:
            content = json.loads(node.content or '{}')
            if not isinstance(content, dict):
                content = {}
        except (TypeError, ValueError):
            content = {}
        content['title'] = node.title or content.get('title') or 'Card'
        content['summary'] = body[:500]
        content['sections'] = [{'type': 'text', 'content': body}] if body else []
        node.content = json.dumps(content, ensure_ascii=False)
        fields.append('content')
    if 'kind' in data:
        kind = str(data.get('kind') or 'note').strip().lower()
        if kind in ALLOWED_KINDS:
            node.kind = kind
            fields.append('kind')
    if 'meta' in data and isinstance(data.get('meta'), dict):
        meta = data['meta']
        color = str(meta.get('color') or 'default').lower()
        if color not in ALLOWED_COLORS:
            color = 'default'
        tags = meta.get('tags') if isinstance(meta.get('tags'), list) else []
        clean_meta = {
            'color': color,
            'tags': [str(tag).strip()[:32] for tag in tags[:8] if str(tag).strip()],
            'pinned': bool(meta.get('pinned')),
        }
        node.metadata = json.dumps(clean_meta, ensure_ascii=False)
        fields.append('metadata')
    if not fields:
        return JsonResponse({'node': _serialize_node(node)})
    node.updated_at = now_ms()
    fields.append('updated_at')
    node.save(update_fields=list(dict.fromkeys(fields)))
    node.board.updated_at = node.updated_at
    node.board.save(update_fields=['updated_at'])
    return JsonResponse({'node': _serialize_node(node)})


@require_POST
def ajax_canvas_batch_move(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_batch_move', 60, 60):
        return JsonResponse({'error': 'Too many layout updates. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    data = _payload(request)
    items = data.get('nodes') if isinstance(data.get('nodes'), list) else []
    if len(items) > MAX_BOARD_NODES:
        return JsonResponse({'error': 'Too many positions'}, status=400)
    by_id = {str(item.get('id')): item for item in items if isinstance(item, dict) and item.get('id')}
    nodes = list(CanvasNode.objects.filter(board=board, id__in=list(by_id.keys())))
    now = now_ms()
    for node in nodes:
        item = by_id.get(str(node.id), {})
        try:
            node.x = max(-100000.0, min(100000.0, float(item.get('x', node.x))))
            node.y = max(-100000.0, min(100000.0, float(item.get('y', node.y))))
        except (TypeError, ValueError):
            continue
        node.updated_at = now
    if nodes:
        CanvasNode.objects.bulk_update(nodes, ['x', 'y', 'updated_at'])
        board.updated_at = now
        settings = {}
        try:
            settings = json.loads(board.settings or '{}')
            if not isinstance(settings, dict):
                settings = {}
        except (TypeError, ValueError):
            settings = {}
        if data.get('layout'):
            settings['layout'] = str(data.get('layout'))[:24]
            board.settings = json.dumps(settings, ensure_ascii=False)
            board.save(update_fields=['updated_at', 'settings'])
        else:
            board.save(update_fields=['updated_at'])
    return JsonResponse({'ok': True, 'updated': len(nodes)})


@require_GET
def ajax_canvas_snapshots(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    board = _owned_board(user, board_id)
    items = [snapshot_summary(snap) for snap in CanvasSnapshot.objects.filter(board=board).order_by('-created_at')[:24]]
    return JsonResponse({'snapshots': items})


@require_POST
def ajax_canvas_snapshot_create(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_snapshot_create', 24, 60):
        return JsonResponse({'error': 'Too many checkpoints. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    label = str(_payload(request).get('label') or 'Manual checkpoint').strip()[:120]
    snap = snapshot_board(board, user, label)
    return JsonResponse({'snapshot': snapshot_summary(snap)}, status=201)


@require_POST
def ajax_canvas_snapshot_restore(request, board_id, snapshot_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_snapshot_restore', 12, 60):
        return JsonResponse({'error': 'Too many restores. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    snap = CanvasSnapshot.objects.filter(id=snapshot_id, board=board, user=user).first()
    if not snap:
        return JsonResponse({'error': 'Checkpoint not found'}, status=404)
    try:
        payload = restore_snapshot(snap, user)
    except (TypeError, ValueError) as exc:
        return JsonResponse({'error': str(exc) or 'Could not restore checkpoint'}, status=400)
    return JsonResponse({'ok': True, 'board': payload['board'], 'nodes': payload['nodes']})


@require_GET
def ajax_canvas_export(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    board = _owned_board(user, board_id)
    fmt = str(request.GET.get('format') or 'json').lower()
    safe_name = ''.join(ch if ch.isalnum() or ch in '-_' else '-' for ch in board.title)[:64].strip('-') or 'canvas'
    if fmt == 'md':
        response = HttpResponse(markdown_export(board), content_type='text/markdown; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}.md"'
        return response
    response = HttpResponse(json.dumps(board_payload(board), ensure_ascii=False, indent=2), content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{safe_name}.canvas.json"'
    return response


@require_POST
def ajax_canvas_import(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_import', 6, 60):
        return JsonResponse({'error': 'Too many imports. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    if len(request.body or b'') > 4 * 1024 * 1024:
        return JsonResponse({'error': 'Canvas files are limited to 4 MB'}, status=413)
    data = _payload(request)
    source = data.get('canvas') if isinstance(data.get('canvas'), dict) else data
    try:
        payload = replace_board_from_payload(board, user, source)
    except (TypeError, ValueError) as exc:
        return JsonResponse({'error': str(exc) or 'Invalid canvas file'}, status=400)
    return JsonResponse({'ok': True, 'board': payload['board'], 'nodes': payload['nodes']})


@require_POST
def ajax_canvas_clone_shared(request, token):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_clone_shared', 8, 60):
        return JsonResponse({'error': 'Too many canvas copies. Try again shortly.'}, status=429)
    source = CanvasBoard.objects.filter(share_token=token).first()
    if not source:
        return JsonResponse({'error': 'Shared canvas not found'}, status=404)
    now = now_ms()
    board = CanvasBoard.objects.create(id=uuid_str(), user=user, title=f'{source.title} — copy'[:200], settings=source.settings, created_at=now, updated_at=now)
    payload = board_payload(source)
    payload['board']['title'] = board.title
    payload['board']['settings'] = payload['board'].get('settings', {})
    try:
        replace_board_from_payload(board, user, payload, snapshot_label='Imported shared canvas')
    except (TypeError, ValueError) as exc:
        board.delete()
        return JsonResponse({'error': str(exc) or 'Could not copy canvas'}, status=400)
    board._node_count = CanvasNode.objects.filter(board=board).count()
    return JsonResponse({'board': _serialize_board(board), 'url': f'/canvas/?board={board.id}'}, status=201)


@require_POST
def ajax_canvas_neby_explore(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_neby_explore', 8, 60):
        return JsonResponse({'error': 'Neby Explore is cooling down. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    count = CanvasNode.objects.filter(board=board).count()
    if count >= MAX_BOARD_NODES - 5:
        return JsonResponse({'error': f'A canvas is limited to {MAX_BOARD_NODES} cards'}, status=400)
    data = _payload(request)
    goal = str(data.get('goal') or 'Find the most useful next branches and deepen this canvas.').strip()[:1200]
    anchor_id = str(data.get('anchorId') or '')
    anchor = CanvasNode.objects.filter(id=anchor_id, board=board).first() if anchor_id else None
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': 'You are out of Neby credits.', 'need_credits': True}, status=402)
    snapshot_board(board, user, 'Before Neby Explore')
    plan, provider = generate_plan(board, goal, anchor=anchor)
    nodes = create_plan_nodes(board, user, plan, anchor=anchor)
    next_questions = [str(q)[:500] for q in (plan.get('nextQuestions') or [])[:6]]
    try:
        CanvasNebyRun.objects.create(
            board=board, user=user, kind='explore', goal=goal[:1200],
            summary=str(plan.get('summary') or '')[:500],
            questions=next_questions, provider=str(provider or '')[:60],
            created_at=now_ms(),
        )
    except Exception:
        pass
    unlimited2, remaining2, allowance = _canvas_credit_state(user)
    return JsonResponse({
        'summary': str(plan.get('summary') or '')[:500],
        'nodes': [_serialize_node(node) for node in nodes],
        'nextQuestions': next_questions,
        'provider': provider,
        'credits': {'unlimited': unlimited2, 'remaining': remaining2, 'allowance': allowance},
    })


@require_POST
def ajax_canvas_suggestions(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_suggestions', 12, 60):
        return JsonResponse({'error': 'Too many suggestion requests. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    goal = str(_payload(request).get('goal') or '').strip()[:700]
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': 'You are out of Neby credits.', 'need_credits': True}, status=402)
    suggestions, provider = suggest_questions(board, goal)
    try:
        CanvasNebyRun.objects.create(
            board=board, user=user, kind='suggest', goal=goal[:1200],
            summary='', questions=[str(q)[:500] for q in (suggestions or [])[:6]],
            provider=str(provider or '')[:60], created_at=now_ms(),
        )
    except Exception:
        pass
    unlimited2, remaining2, allowance = _canvas_credit_state(user)
    return JsonResponse({
        'suggestions': suggestions,
        'provider': provider,
        'credits': {'unlimited': unlimited2, 'remaining': remaining2, 'allowance': allowance},
    })


@require_GET
def ajax_canvas_neby_history(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    board = _owned_board(user, board_id)
    if request.method == 'DELETE' or request.GET.get('action') == 'clear':
        CanvasNebyRun.objects.filter(board=board).delete()
        return JsonResponse({'ok': True, 'runs': []})
    runs = CanvasNebyRun.objects.filter(board=board)[:30]
    return JsonResponse({'runs': [{
        'id': r.id,
        'kind': r.kind,
        'goal': r.goal,
        'summary': r.summary,
        'questions': r.questions or [],
        'provider': r.provider,
        'created_at': r.created_at,
    } for r in runs]})


WIDGET_SYSTEM = """You generate study-widget content for a learning canvas. Return ONLY compact JSON — no markdown fences.
Schemas by kind:
quiz: {"q": "...", "options": ["...","...","...","..."], "answer": 0}
flash: {"cards": [{"q": "...", "a": "..."}, ...] }  (3-5 cards)
timeline: {"events": [{"t": "label", "d": "one-line detail"}, ...]}  (3-5, chronological)
flow: {"start": {"label": "...", "desc": "..."}, "steps": [{"label": "...", "desc": "..."}, ...], "decision": {"cond": "...", "yes": "...", "no": "..."}}  (study process or reasoning flow)
Keep every string under 90 characters. Content must be factually accurate and study-appropriate for the topic."""


@require_POST
def ajax_canvas_widget_content(request):
    """Generate study content for a canvas widget (quiz/flash/timeline/flow) from a topic."""
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_widget_content', 20, 60):
        return JsonResponse({'error': 'Rate limited'}, status=429)
    data = _payload(request)
    kind = str(data.get('kind') or '').strip().lower()
    topic = str(data.get('topic') or '').strip()[:300]
    if kind not in ('quiz', 'flash', 'timeline', 'flow'):
        return JsonResponse({'error': 'Invalid widget kind'}, status=400)
    if not topic:
        return JsonResponse({'error': 'Topic required'}, status=400)
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': 'You are out of Neby credits.', 'need_credits': True}, status=402)

    from api.llm.credentials import resolve
    from api.llm.client import chat as llm_chat
    resolved = resolve(user, 'tryingopen') or resolve(user, 'geminiweb')
    if not resolved:
        return JsonResponse({'error': 'No AI provider available'}, status=503)
    prompt = f"Create {kind} widget content about: {topic}"
    try:
        result = llm_chat(
            format='openai', base_url=resolved.base_url, api_key=resolved.api_key,
            model=resolved.model,
            messages=[{'role': 'system', 'content': WIDGET_SYSTEM}, {'role': 'user', 'content': prompt}],
            max_tokens=900, timeout=60, provider='widget-content',
        )
        raw = (result.text or '').strip()
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]
        content = json.loads(raw.strip())
    except Exception as exc:
        return JsonResponse({'error': f'Generation failed: {exc}'}, status=502)

    # Sanitize per kind
    if kind == 'quiz':
        opts = [str(o)[:120] for o in (content.get('options') or [])[:4]]
        if not content.get('q') or len(opts) < 2:
            return JsonResponse({'error': 'Model returned incomplete quiz'}, status=502)
        while len(opts) < 4:
            opts.append('None of the above')
        content = {'q': str(content['q'])[:200], 'options': opts, 'answer': max(0, min(3, int(content.get('answer') or 0)))}
    elif kind == 'flash':
        cards = [{'q': str(c.get('q'))[:160], 'a': str(c.get('a'))[:240]} for c in (content.get('cards') or [])[:5] if c.get('q') and c.get('a')]
        if not cards:
            return JsonResponse({'error': 'Model returned incomplete flashcards'}, status=502)
        content = {'cards': cards}
    elif kind == 'timeline':
        events = [{'t': str(e.get('t'))[:80], 'd': str(e.get('d'))[:140]} for e in (content.get('events') or [])[:5] if e.get('t')]
        if not events:
            return JsonResponse({'error': 'Model returned incomplete timeline'}, status=502)
        content = {'events': events}
    else:
        st = content.get('start') or {}
        dec = content.get('decision') or {}
        steps = [{'label': str(s.get('label'))[:80], 'desc': str(s.get('desc'))[:140]} for s in (content.get('steps') or [])[:3] if s.get('label')]
        if not st.get('label') or not dec.get('cond'):
            return JsonResponse({'error': 'Model returned incomplete flow'}, status=502)
        content = {
            'start': {'label': str(st['label'])[:80], 'desc': str(st.get('desc') or '')[:140]},
            'steps': steps,
            'decision': {'cond': str(dec['cond'])[:120], 'yes': str(dec.get('yes') or 'Yes')[:80], 'no': str(dec.get('no') or 'No')[:80]},
        }
    unlimited2, remaining2, allowance = _canvas_credit_state(user)
    return JsonResponse({'content': content, 'provider': resolved.model, 'credits': {'unlimited': unlimited2, 'remaining': remaining2, 'allowance': allowance}})


@require_POST
def ajax_canvas_agent_prompt(request, board_id):
    """Agentic multi-step canvas prompt: plans, then executes tools
    (add_card / update_card / add_widget / connect / finish) over several turns."""
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_agent_prompt', 6, 60):
        return JsonResponse({'error': 'Agent cooling down. Try again shortly.'}, status=429)
    board = _owned_board(user, board_id)
    data = _payload(request)
    prompt = str(data.get('prompt') or '').strip()[:2000]
    if not prompt:
        return JsonResponse({'error': 'Prompt required'}, status=400)
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': 'You are out of Neby credits.', 'need_credits': True}, status=402)

    from api.llm.credentials import resolve
    from api.llm.client import chat as llm_chat

    def _nodes_ctx():
        nodes = CanvasNode.objects.filter(board=board).order_by('created_at')[:40]
        return [{'id': n.id, 'title': n.title[:80], 'parent': n.parent_id or ''} for n in nodes]

    TOOLS_DESC = """You are Neby, an agentic study-canvas builder. Respond ONLY with JSON:
{"think": "one line", "tool": "...", "args": {...}}
Tools:
- add_card: {"prompt": "...", "parent_id": "<existing id or empty>"} — creates one knowledge card (AI-generated content)
- add_widget: {"kind": "quiz|flash|timeline|flow", "topic": "..."} — creates an interactive study widget
- connect: {"parent_id": "...", "child_id": "..."} — link two existing cards
- finish: {"summary": "..."} — call when the user's request is fully handled
Rules: 1 tool per response. Use add_card for explanatory content, add_widget for practice/interactive content. Prefer 2-4 total steps. Always end with finish."""

    steps = []
    created_nodes = []
    history_msgs = [{'role': 'system', 'content': TOOLS_DESC},
                    {'role': 'user', 'content': f"Canvas request: {prompt}\nExisting cards: {json.dumps(_nodes_ctx())}"}]
    resolved = resolve(user, 'tryingopen') or resolve(user, 'geminiweb')
    if not resolved:
        return JsonResponse({'error': 'No AI provider available'}, status=503)

    summary = ''
    for step_i in range(5):
        try:
            result = llm_chat(
                format='openai', base_url=resolved.base_url, api_key=resolved.api_key,
                model=resolved.model, messages=history_msgs,
                max_tokens=400, timeout=60, provider='canvas-agent',
            )
            raw = (result.text or '').strip()
            if raw.startswith('```'):
                raw = raw.split('```')[1]
                if raw.startswith('json'):
                    raw = raw[4:]
            action = json.loads(raw.strip())
        except Exception as exc:
            steps.append({'tool': 'error', 'detail': str(exc)[:160]})
            break
        tool = str(action.get('tool') or '').strip()
        args = action.get('args') or {}
        steps.append({'tool': tool, 'think': str(action.get('think') or '')[:160]})
        if tool == 'finish':
            summary = str(args.get('summary') or '')[:500]
            break
        if tool == 'add_card':
            nprompt = str(args.get('prompt') or '').strip()[:500]
            if not nprompt:
                steps[-1]['error'] = 'empty prompt'
                continue
            parent_id = str(args.get('parent_id') or '').strip() or None
            parent = CanvasNode.objects.filter(id=parent_id, board=board).first() if parent_id else None
            existing = CanvasNode.objects.filter(board=board).count()
            if parent:
                siblings = CanvasNode.objects.filter(board=board, parent=parent).count()
                nx, ny = parent.x + siblings * 32, parent.y + 460
            else:
                nx, ny = 420 + existing * 80, 120 + (existing % 3) * 24
            now = now_ms()
            node = CanvasNode.objects.create(
                id=uuid_str(), board=board, parent=parent, user=user, prompt=nprompt,
                title=nprompt[:60], content='', status='generating', x=nx, y=ny,
                created_at=now, updated_at=now,
            )
            created_nodes.append(node.id)
            try:
                r2, content_data, _slug = _call_llm_for_canvas(user, nprompt, '', False, 'fast')
                node.title = (content_data.get('title') or nprompt[:50])[:300]
                node.content = json.dumps(content_data, ensure_ascii=False)
                node.status = 'done'
                node.updated_at = now_ms()
                node.save(update_fields=['title', 'content', 'status', 'updated_at'])
            except Exception:
                node.status = 'failed'
                node.save(update_fields=['status'])
            history_msgs.append({'role': 'assistant', 'content': json.dumps({'tool': 'add_card', 'id': node.id})})
        elif tool == 'add_widget':
            wkind = str(args.get('kind') or 'quiz')
            wtopic = str(args.get('topic') or prompt)[:200]
            steps[-1]['topic'] = wtopic
            steps[-1]['kind'] = wkind
            history_msgs.append({'role': 'assistant', 'content': json.dumps({'tool': 'add_widget', 'kind': wkind, 'topic': wtopic})})
        elif tool == 'connect':
            pid, cid = str(args.get('parent_id') or ''), str(args.get('child_id') or '')
            child = CanvasNode.objects.filter(id=cid, board=board).first()
            if child and CanvasNode.objects.filter(id=pid, board=board).exists():
                child.parent_id = pid
                child.save(update_fields=['parent'])
                history_msgs.append({'role': 'assistant', 'content': json.dumps({'tool': 'connect', 'ok': True})})
            else:
                history_msgs.append({'role': 'assistant', 'content': json.dumps({'tool': 'connect', 'ok': False})})
        else:
            history_msgs.append({'role': 'assistant', 'content': json.dumps({'tool': 'unknown'})})

    board.updated_at = now_ms()
    board.save(update_fields=['updated_at'])
    unlimited2, remaining2, allowance = _canvas_credit_state(user)
    nodes_out = [json.loads(n.content) if n.content else {} for n in []]
    out_nodes = []
    for nid in created_nodes:
        n = CanvasNode.objects.filter(id=nid).first()
        if n:
            out_nodes.append(_serialize_node(n))
    return JsonResponse({
        'steps': steps, 'summary': summary, 'nodes': out_nodes,
        'credits': {'unlimited': unlimited2, 'remaining': remaining2, 'allowance': allowance},
    })
