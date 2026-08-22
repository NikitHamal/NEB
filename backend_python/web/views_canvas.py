import json
import time
import uuid

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape

from api.models import CanvasBoard, CanvasNode, User
from api.utils import now_ms, uuid_str
from .view_helpers import _ctx, _get_valid_token, _get_user_id, _avatar_url, _user_badge_info, _rate_limit
from api.security import get_user_by_auth_token

SYSTEM_PROMPT = """You are Wondering Canvas — a spatial research engine that turns any question into a rich, visual, node-based explanation.

You output ONLY a single JSON object (no markdown fences, no extra text) with this schema:
{
  "title": "Short crisp title derived from the prompt (3-6 words)",
  "summary": "One paragraph overview (40-60 words) with **bold** on key terms.",
  "sections": [
    {"type": "text", "content": "Markdown paragraph. Use **bold** for key terms. 40-70 words. No lists."},
    {
      "type": "diagram",
      "title": "Diagram title (e.g., 'Core Architecture')",
      "nodes": [{"id": "slug", "label": "Short label", "desc": "One-line meaning"}],
      "edges": [{"from": "id", "to": "id"}],
      "note": "Optional small caption below diagram."
    },
    {
      "type": "comparison",
      "title": "Comparison title",
      "headers": ["Aspect", "Column A", "Column B"],
      "rows": [["Row label", "Col A value", "Col B value"]]
    },
    {
      "type": "cards",
      "title": "Visual reference title",
      "items": [
        {"title": "Item name", "subtitle": "Designer / year / tagline", "bullets": ["Material: ...", "Philosophy: ..."], "desc": "One sentence."}
      ]
    },
    {
      "type": "bullets",
      "title": "Optional bullet list title",
      "items": ["Point 1", "Point 2", "Point 3"]
    }
  ]
}

Rules:
- Always include at least 1 text section.
- Include a diagram when the topic has a system/process/architecture (use 3-5 nodes). Include comparison when topic has alternatives. Include cards/visual refs only when topic is about objects/products/people.
- Keep total sections 2-4.
- Diagram nodes: ids are lowercase slugs without spaces, labels 1-3 words, desc max 10 words.
- Edges must reference valid node ids.
- Comparison: 3-5 rows, headers length 3 (first is Aspect).
- Cards: 2-4 items if used.
- Write in clear, concise, educational English. No repetition.
- Do NOT wrap output in markdown. Output raw JSON only.
"""


def _resolve_user(request):
    token = _get_valid_token(request)
    if not token:
        return None
    try:
        return get_user_by_auth_token(token)
    except User.DoesNotExist:
        return None


def _get_user_or_none(request):
    user = _resolve_user(request)
    return user


def _require_user(request):
    user = _resolve_user(request)
    if not user:
        return None, JsonResponse({'error': 'Authentication required'}, status=401)
    if getattr(user, 'is_locked', False):
        return None, JsonResponse({'error': 'Account locked'}, status=403)
    return user, None


def _serialize_board(board):
    return {
        'id': board.id,
        'title': board.title,
        'createdAt': board.created_at,
        'updatedAt': board.updated_at,
        'nodeCount': getattr(board, '_node_count', 0),
    }


def _serialize_node(node):
    content = {}
    try:
        if node.content:
            content = json.loads(node.content)
            if not isinstance(content, dict):
                content = {}
    except Exception:
        content = {}
    return {
        'id': node.id,
        'boardId': node.board_id,
        'parentId': node.parent_id or '',
        'prompt': node.prompt,
        'title': node.title,
        'content': content,
        'status': node.status,
        'x': node.x,
        'y': node.y,
        'webSearchEnabled': node.web_search_enabled,
        'modelUsed': node.model_used,
        'error': node.error,
        'createdAt': node.created_at,
        'updatedAt': node.updated_at,
    }


def _parent_chain_context(board, parent_id, limit=3):
    if not parent_id:
        return ""
    chain = []
    current_id = parent_id
    seen = set()
    while current_id and len(chain) < limit and current_id not in seen:
        seen.add(current_id)
        try:
            n = CanvasNode.objects.get(id=current_id, board=board)
        except CanvasNode.DoesNotExist:
            break
        chain.append(n)
        current_id = n.parent_id
    chain.reverse()
    parts = []
    for n in chain:
        title = n.title or n.prompt[:60]
        summary = ""
        try:
            if n.content:
                c = json.loads(n.content)
                summary = c.get('summary', '') or c.get('title', '')
        except Exception:
            summary = ""
        parts.append(f"Parent: {title}\nPrompt: {n.prompt}\nSummary: {summary[:200]}")
    return "\n\n---\n\n".join(parts)


def _mock_content(prompt, parent_context=""):
    p = (prompt or "").lower()
    title = (prompt.strip().split("?")[0][:40].strip() or "Untitled")
    if len(title) > 38:
        title = title[:38].rsplit(" ", 1)[0] + "…"
    title_cap = title.title() if len(title.split()) <= 6 else title.capitalize()

    if "raw sensory" in p:
        return {
            "title": "Raw Sensory Data",
            "summary": "**Raw sensory data** is the unprocessed stream from the environment — pixels, audio waves, or proprioceptive signals before any abstraction.",
            "sections": [
                {"type": "text", "content": "Sensors deliver high-dimensional, noisy observations. **Perception** compresses this into a compact latent code that the **world model** can predict forward, filtering noise while preserving task-relevant structure."},
                {"type": "bullets", "title": "Why it matters", "items": ["Basis for every prediction the agent makes.", "Quality of encoding limits planning accuracy.", "Better compression → more imagined rollouts per second."]},
                {"type": "comparison", "title": "Raw vs Latent", "headers": ["Aspect", "Raw sensory", "Latent state"], "rows": [["Size", "Megabytes per second", "Hundreds of floats"], ["Noise", "High", "Filtered"], ["Use for planning", "No — too heavy", "Yes — compact rollouts"]]},
            ],
        }
    if "dynamics" in p and "predict" in p:
        return {
            "title": "Dynamics Predictor",
            "summary": "The **dynamics predictor** learns how the latent world state evolves when an action is taken — the core foresight module of a world model.",
            "sections": [
                {"type": "text", "content": "Given the current **latent state** and an **action**, the dynamics predictor outputs the next state distribution. Training minimizes the gap between predicted and actual future encodings, forcing the model to internalize physics and causality."},
                {"type": "diagram", "title": "Prediction step", "nodes": [{"id": "state", "label": "State", "desc": "Current latent state"}, {"id": "action", "label": "Action", "desc": "Agent's choice"}, {"id": "next", "label": "Next State", "desc": "Predicted future"}], "edges": [{"from": "state", "to": "next"}, {"from": "action", "to": "next"}]},
            ],
        }
    if "world model" in p:
        return {
            "title": "World Models",
            "summary": "A **world model** is an internal, predictive simulation of the environment that lets an agent imagine future states, evaluate actions, and plan without touching the real world.",
            "sections": [
                {"type": "text", "content": "World models compress **raw sensory data** into a compact latent state, then simulate how that state evolves. Unlike **LLMs** that predict the next token, world models predict the next *world state* and the **reward** that follows, enabling **model-based planning** and safer exploration."},
                {"type": "diagram", "title": "World Model Architecture", "nodes": [
                    {"id": "perception", "label": "Perception", "desc": "Encodes raw sensory data"},
                    {"id": "memory", "label": "Memory / State", "desc": "Latent world representation"},
                    {"id": "dynamics", "label": "Dynamics Predictor", "desc": "Predicts next state"},
                    {"id": "reward", "label": "Reward Estimator", "desc": "Predicts reward signal"},
                    {"id": "policy", "label": "Action Policy", "desc": "Chooses best action"},
                ], "edges": [
                    {"from": "perception", "to": "memory"},
                    {"from": "memory", "to": "dynamics"},
                    {"from": "dynamics", "to": "reward"},
                    {"from": "memory", "to": "policy"},
                    {"from": "reward", "to": "policy"},
                ], "note": "Tap any block to see what it does."},
                {"type": "comparison", "title": "World Models vs LLMs", "headers": ["Aspect", "World Models", "LLMs"], "rows": [
                    ["Core objective", "Predict future world states", "Predict next token"],
                    ["Representation", "Latent dynamics + reward", "Statistical language distribution"],
                    ["Planning", "Imagined rollouts, then act", "Generate text, no simulation"],
                    ["Data efficiency", "High (imagination)", "High but needs huge text"],
                ]},
            ],
        }
    if "control theory" in p or "control" in p:
        return {
            "title": "Control Theory",
            "summary": "**Control theory** is the mathematics of steering systems toward desired behavior by adjusting inputs based on feedback from the environment.",
            "sections": [
                {"type": "text", "content": "Every controlled system has a **plant** (what you steer), a **sensor** that measures output, and a **controller** that decides the next input. The controller closes the **feedback loop**, comparing the measured output to the **reference** and correcting the error over time."},
                {"type": "diagram", "title": "Feedback Loop", "nodes": [
                    {"id": "reference", "label": "Reference", "desc": "Desired value"},
                    {"id": "controller", "label": "Controller", "desc": "Computes correction"},
                    {"id": "plant", "label": "Plant", "desc": "System being controlled"},
                    {"id": "sensor", "label": "Sensor", "desc": "Measures output"},
                ], "edges": [
                    {"from": "reference", "to": "controller"},
                    {"from": "controller", "to": "plant"},
                    {"from": "plant", "to": "sensor"},
                    {"from": "sensor", "to": "controller"},
                ]},
                {"type": "comparison", "title": "Open vs Closed Loop", "headers": ["Aspect", "Open Loop", "Closed Loop"], "rows": [
                    ["Feedback", "None — fixed sequence", "Continuous measurement"],
                    ["Robustness", "Fragile to disturbances", "Corrects for noise"],
                    ["Example", "Toaster timer", "Thermostat"],
                ]},
            ],
        }
    if "chair" in p or "danish" in p or "design" in p:
        return {
            "title": "Iconic Danish Chairs",
            "summary": "Danish modern chairs distilled function to its purest form — honest materials, human proportions, and quiet craft that still feels contemporary today.",
            "sections": [
                {"type": "text", "content": "The golden age of **Danish design** (1940s-60s) prized **material honesty**, **ergonomic clarity**, and restrained joinery. Designers like **Hans Wegner** and **Arne Vodder** let wood, rattan, and leather speak without ornament, producing chairs that are light to the eye but deeply engineered."},
                {"type": "cards", "title": "Four icons", "items": [
                    {"title": "CH07 Shell Chair", "subtitle": "Hans Wegner · 1963", "bullets": ["Material: Molded plywood + steel", "Philosophy: Floating lightness"], "desc": "Three curved shell forms give winged comfort with minimal structure."},
                    {"title": "Wishbone Chair (CH24)", "subtitle": "Hans Wegner · 1949", "bullets": ["Material: Solid wood + paper cord", "Philosophy: Perfected craft"], "desc": "Steamed Y-back and woven seat; 100+ steps by hand."},
                    {"title": "PK22 Chair", "subtitle": "Poul Kjærholm · 1956", "bullets": ["Material: Steel + wicker/leather", "Philosophy: Industrial elegance"], "desc": "Thin steel frame contrasts soft, suspended seating."},
                    {"title": "Sibast No. 8", "subtitle": "Helge Sibast · 1953", "bullets": ["Material: Teak + leather", "Philosophy: Quiet luxury"], "desc": "Subtle curves and stitched back emphasize upholstery craft."},
                ]},
            ],
        }
    # Generic fallback
    base_title = title_cap if title_cap else "Understanding " + (prompt[:30] if prompt else "the topic")
    return {
        "title": base_title,
        "summary": f"An overview of **{prompt[:80]}** — key ideas broken down into a visual structure you can explore in parallel.",
        "sections": [
            {"type": "text", "content": f"**{prompt.strip()[:60]}** can be understood as a system of interacting parts. The core idea is to separate *what the system perceives*, *how it predicts change*, and *how it evaluates outcomes*. Each part is simple alone; together they enable coherent behaviour in complex environments."},
            {"type": "bullets", "title": "Key ideas", "items": [
                "Compress the world into a compact internal state.",
                "Model how actions change that state over time.",
                "Use the model to imagine futures before acting.",
            ]},
            {"type": "comparison", "title": "Two perspectives", "headers": ["Aspect", "Approach A", "Approach B"], "rows": [
                ["Focus", "Structure & simulation", "Data & pattern matching"],
                ["Strength", "Planning and foresight", "Breadth and fluency"],
                ["Trade-off", "Needs a good model", "Needs huge data"],
            ]},
        ],
    }


def _call_llm_for_canvas(user, prompt, parent_context, web_search_enabled, speed_mode):
    from api.llm.credentials import resolve
    from api.llm.client import chat, LLMError

    user_prompt = prompt.strip()
    if parent_context:
        user_prompt = f"Ancestor context (use to keep drill-downs consistent):\n{parent_context}\n\n---\n\nNew question to answer as a new child card: {prompt.strip()}"
        if selected_hint := parent_context[:120]:
            pass
    if web_search_enabled:
        user_prompt += "\n\n[Web search is enabled — cite what you can, but do not hallucinate URLs. Prefer concise, grounded explanations.]"
    speed_note = "Fast" if (speed_mode or "fast").lower() == "fast" else "Deep"
    user_prompt = f"[{speed_note} mode — answer quickly but thoroughly]\n" + user_prompt

    # Try official providers in priority order
    candidates = [
        ('agnes', ''),
        ('openai', ''),
        ('gemini', ''),
        ('deepseek', ''),
        ('anthropic', ''),
    ]
    resolved = None
    for slug, model in candidates:
        try:
            r = resolve(user, slug, model=model)
            if r and r.api_key:
                resolved = r
                break
        except Exception:
            continue
    if not resolved:
        # Try qwen bot presence (scraper fallback — but we want JSON, so use scraper via LLM client is not available)
        # Fall back to mock so canvas still works offline/demo.
        return None, _mock_content(prompt, parent_context), "mock"

    try:
        result = chat(
            format=resolved.format,
            base_url=resolved.base_url,
            api_key=resolved.api_key,
            model=resolved.model,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt},
            ],
            max_tokens=2600 if speed_note == "Fast" else 3600,
            timeout=45,
            temperature=0.45,
            provider=resolved.slug,
        )
        raw = (result.text or "").strip()
        # Strip fences if model adds them despite instructions
        if raw.startswith("```"):
            raw = raw.strip("`")
            # remove first line if it's json
            if raw.lstrip().lower().startswith("json"):
                raw = raw.lstrip()[4:].strip()
        try:
            data = json.loads(raw)
            if not isinstance(data, dict) or "title" not in data:
                raise ValueError("invalid shape")
            # Light validation
            if not data.get("sections"):
                data["sections"] = [{"type": "text", "content": raw[:800]}]
            return resolved, data, resolved.slug
        except Exception:
            # Fall back to wrapping raw as text section
            return resolved, {
                "title": prompt.strip().split("?")[0][:40] or "Result",
                "summary": raw[:260] + ("…" if len(raw) > 260 else ""),
                "sections": [{"type": "text", "content": raw[:1800]}],
            }, resolved.slug
    except LLMError as e:
        # On provider error, return mock so UI doesn't hang
        return None, _mock_content(prompt, parent_context), f"mock-fallback:{e}"
    except Exception as e:
        return None, _mock_content(prompt, parent_context), f"mock-error:{e}"


def canvas_page(request):
    boards = []
    current_board = None
    current_board_id = request.GET.get('board') or request.GET.get('b') or ''
    user = _get_user_or_none(request)
    if user:
        qs = CanvasBoard.objects.filter(user=user).order_by('-updated_at')
        boards = list(qs[:50])
        for b in boards:
            b._node_count = CanvasNode.objects.filter(board=b).count()
        if current_board_id:
            try:
                current_board = CanvasBoard.objects.get(id=current_board_id, user=user)
            except CanvasBoard.DoesNotExist:
                current_board = boards[0] if boards else None
        else:
            if boards:
                current_board = boards[0]

    ctx = _ctx(request, boards=boards, current_board=current_board, current_board_id=getattr(current_board, 'id', '') if current_board else '')
    ctx['hide_footer_links'] = True
    return render(request, 'web/canvas.html', ctx)


@require_GET
def ajax_canvas_boards(request):
    user, err = _require_user(request)
    if err:
        return err
    boards = CanvasBoard.objects.filter(user=user).order_by('-updated_at')
    data = []
    for b in boards:
        cnt = CanvasNode.objects.filter(board=b).count()
        b._node_count = cnt
        data.append(_serialize_board(b))
    return JsonResponse({'boards': data})


@require_POST
def ajax_canvas_create_board(request):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'canvas_create_board', 20, 60):
        return JsonResponse({'error': 'Rate limited. Slow down.'}, status=429)
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    title = (payload.get('title') or '').strip()[:200]
    if not title:
        title = 'Untitled canvas'
    now = now_ms()
    board = CanvasBoard.objects.create(
        id=uuid_str(),
        user=user,
        title=title,
        created_at=now,
        updated_at=now,
    )
    return JsonResponse({'board': _serialize_board(board)})


def _get_board_for_user(request, board_id):
    user, err = _require_user(request)
    if err:
        return None, None, err
    try:
        board = CanvasBoard.objects.get(id=board_id, user=user)
        return board, user, None
    except CanvasBoard.DoesNotExist:
        return None, None, JsonResponse({'error': 'Board not found'}, status=404)


@require_GET
def ajax_canvas_board_detail(request, board_id):
    board, user, err = _get_board_for_user(request, board_id)
    if err:
        return err
    nodes = CanvasNode.objects.filter(board=board).order_by('created_at')
    nodes_data = [_serialize_node(n) for n in nodes]
    return JsonResponse({'board': _serialize_board(board), 'nodes': nodes_data})


@require_POST
def ajax_canvas_board_update(request, board_id):
    board, user, err = _get_board_for_user(request, board_id)
    if err:
        return err
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    title = (payload.get('title') or '').strip()[:200]
    if not title:
        return JsonResponse({'error': 'Title required'}, status=400)
    board.title = title
    board.updated_at = now_ms()
    board.save(update_fields=['title', 'updated_at'])
    return JsonResponse({'board': _serialize_board(board)})


@require_POST
def ajax_canvas_board_delete(request, board_id):
    board, user, err = _get_board_for_user(request, board_id)
    if err:
        return err
    board.delete()
    return JsonResponse({'ok': True})


@require_POST
def ajax_canvas_create_node(request, board_id):
    board, user, err = _get_board_for_user(request, board_id)
    if err:
        return err
    if _rate_limit(request, 'canvas_create_node', 30, 60):
        return JsonResponse({'error': 'Rate limited'}, status=429)
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    prompt = (payload.get('prompt') or '').strip()
    if not prompt:
        return JsonResponse({'error': 'Prompt required'}, status=400)
    if len(prompt) > 2000:
        prompt = prompt[:2000]
    parent_id = (payload.get('parent_id') or payload.get('parentId') or '').strip() or None
    if parent_id:
        try:
            parent = CanvasNode.objects.get(id=parent_id, board=board)
        except CanvasNode.DoesNotExist:
            return JsonResponse({'error': 'Parent not found'}, status=404)
    else:
        parent = None

    try:
        x = float(payload.get('x', 0))
        y = float(payload.get('y', 0))
    except Exception:
        x, y = 0, 0
    # clamp canvas positions sanity
    x = max(-8000, min(8000, x))
    y = max(-8000, min(8000, y))

    web_search_enabled = bool(payload.get('web_search_enabled') or payload.get('webSearchEnabled'))
    speed_mode = (payload.get('speed_mode') or payload.get('speedMode') or 'fast').strip().lower()
    if speed_mode not in ('fast', 'deep'):
        speed_mode = 'fast'

    now = now_ms()
    # Default placement if not supplied: stagger
    if x == 0 and y == 0:
        existing = CanvasNode.objects.filter(board=board).count()
        if parent:
            # children below parent with slight offset per sibling count
            siblings = CanvasNode.objects.filter(board=board, parent=parent).count()
            x = parent.x + (siblings * 32)
            y = parent.y + 460
        else:
            # root nodes spread horizontally
            x = 420 + (existing * 80)
            y = 120 + (existing % 3) * 24

    node = CanvasNode.objects.create(
        id=uuid_str(),
        board=board,
        parent=parent,
        user=user,
        prompt=prompt,
        title=prompt[:60],
        content='',
        status='generating',
        x=x,
        y=y,
        web_search_enabled=web_search_enabled,
        model_used=speed_mode,
        created_at=now,
        updated_at=now,
    )
    board.updated_at = now
    board.save(update_fields=['updated_at'])

    # Generate content synchronously (fast path). If LLM is slow, client sees pulsing 'generating' for a few seconds.
    parent_ctx = _parent_chain_context(board, parent_id) if parent_id else ""
    resolved, content_data, model_slug = _call_llm_for_canvas(user, prompt, parent_ctx, web_search_enabled, speed_mode)

    # Ensure title extraction
    title = (content_data.get('title') or prompt.split('?')[0][:50] or prompt[:50]).strip()
    node.title = title[:300]
    node.content = json.dumps(content_data, ensure_ascii=False)
    node.status = 'done'
    node.model_used = model_slug[:100]
    node.updated_at = now_ms()
    node.save(update_fields=['title', 'content', 'status', 'model_used', 'updated_at'])

    return JsonResponse({'node': _serialize_node(node)})


@require_POST
def ajax_canvas_node_move(request, node_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        node = CanvasNode.objects.select_related('board').get(id=node_id, board__user=user)
    except CanvasNode.DoesNotExist:
        return JsonResponse({'error': 'Node not found'}, status=404)
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    try:
        x = float(payload.get('x', node.x))
        y = float(payload.get('y', node.y))
    except Exception:
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)
    node.x = max(-10000, min(10000, x))
    node.y = max(-10000, min(10000, y))
    node.updated_at = now_ms()
    node.save(update_fields=['x', 'y', 'updated_at'])
    node.board.updated_at = now_ms()
    node.board.save(update_fields=['updated_at'])
    return JsonResponse({'node': _serialize_node(node)})


@require_POST
def ajax_canvas_node_delete(request, node_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        node = CanvasNode.objects.select_related('board').get(id=node_id, board__user=user)
    except CanvasNode.DoesNotExist:
        return JsonResponse({'error': 'Node not found'}, status=404)
    # Delete node and orphan children (set parent to node's parent)
    children = CanvasNode.objects.filter(parent=node)
    for c in children:
        c.parent = node.parent
        c.save(update_fields=['parent'])
    node.delete()
    node.board.updated_at = now_ms()
    node.board.save(update_fields=['updated_at'])
    return JsonResponse({'ok': True})


@require_POST
def ajax_canvas_node_retry(request, node_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        node = CanvasNode.objects.select_related('board').get(id=node_id, board__user=user)
    except CanvasNode.DoesNotExist:
        return JsonResponse({'error': 'Node not found'}, status=404)
    node.status = 'generating'
    node.error = ''
    node.updated_at = now_ms()
    node.save(update_fields=['status', 'error', 'updated_at'])
    parent_ctx = _parent_chain_context(node.board, node.parent_id) if node.parent_id else ""
    resolved, content_data, model_slug = _call_llm_for_canvas(user, node.prompt, parent_ctx, node.web_search_enabled, node.model_used or 'fast')
    node.title = (content_data.get('title') or node.prompt[:50]).strip()[:300]
    node.content = json.dumps(content_data, ensure_ascii=False)
    node.status = 'done'
    node.model_used = model_slug[:100]
    node.updated_at = now_ms()
    node.save(update_fields=['title', 'content', 'status', 'model_used', 'updated_at'])
    return JsonResponse({'node': _serialize_node(node)})


def _create_node_from_prompt(user, board, prompt, parent, x, y, web_search_enabled, speed_mode):
    now = now_ms()
    if x is None or y is None:
        if parent:
            siblings = CanvasNode.objects.filter(board=board, parent=parent).count()
            x = parent.x + (siblings * 28)
            y = parent.y + 460
        else:
            existing = CanvasNode.objects.filter(board=board).count()
            x = 420 + (existing * 72)
            y = 120 + (existing % 3) * 20
    node = CanvasNode.objects.create(
        id=uuid_str(),
        board=board,
        parent=parent,
        user=user,
        prompt=prompt,
        title=prompt[:60],
        content='',
        status='generating',
        x=float(x),
        y=float(y),
        web_search_enabled=bool(web_search_enabled),
        model_used=(speed_mode or 'fast')[:100],
        created_at=now,
        updated_at=now,
    )
    board.updated_at = now
    board.save(update_fields=['updated_at'])
    parent_ctx = _parent_chain_context(board, parent.id if parent else None) if parent else ""
    resolved, content_data, model_slug = _call_llm_for_canvas(user, prompt, parent_ctx, bool(web_search_enabled), speed_mode or 'fast')
    title = (content_data.get('title') or prompt.split('?')[0][:50] or prompt[:50]).strip()
    node.title = title[:300]
    node.content = json.dumps(content_data, ensure_ascii=False)
    node.status = 'done'
    node.model_used = model_slug[:100]
    node.updated_at = now_ms()
    node.save(update_fields=['title', 'content', 'status', 'model_used', 'updated_at'])
    return node


@require_POST
def ajax_canvas_node_followup(request, node_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        parent = CanvasNode.objects.select_related('board').get(id=node_id, board__user=user)
    except CanvasNode.DoesNotExist:
        return JsonResponse({'error': 'Node not found'}, status=404)
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    prompt = (payload.get('prompt') or '').strip()
    if not prompt:
        return JsonResponse({'error': 'Prompt required'}, status=400)
    if len(prompt) > 2000:
        prompt = prompt[:2000]
    web_search_enabled = bool(payload.get('web_search_enabled') or payload.get('webSearchEnabled') or parent.web_search_enabled)
    speed_mode = (payload.get('speed_mode') or payload.get('speedMode') or 'fast').strip().lower()
    if speed_mode not in ('fast', 'deep'):
        speed_mode = 'fast'
    node = _create_node_from_prompt(user, parent.board, prompt, parent, None, None, web_search_enabled, speed_mode)
    return JsonResponse({'node': _serialize_node(node)})


@require_POST
def ajax_canvas_node_dig_deeper(request, node_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        parent = CanvasNode.objects.select_related('board').get(id=node_id, board__user=user)
    except CanvasNode.DoesNotExist:
        return JsonResponse({'error': 'Node not found'}, status=404)
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    selected = (payload.get('selected_text') or payload.get('selectedText') or '').strip()
    if not selected:
        return JsonResponse({'error': 'Selection required'}, status=400)
    if len(selected) > 500:
        selected = selected[:500]
    prompt = f"Explain '{selected}' in depth — definition, why it matters, a tiny example, and how it connects to '{parent.title or parent.prompt[:40]}'."
    custom_prompt = (payload.get('prompt') or '').strip()
    if custom_prompt:
        prompt = custom_prompt
    if len(prompt) > 2000:
        prompt = prompt[:2000]
    web_search_enabled = bool(payload.get('web_search_enabled') or payload.get('webSearchEnabled') or parent.web_search_enabled)
    speed_mode = (payload.get('speed_mode') or payload.get('speedMode') or 'fast').strip().lower()
    if speed_mode not in ('fast', 'deep'):
        speed_mode = 'fast'
    x = parent.x + 560
    y = parent.y + 70
    try:
        siblings = CanvasNode.objects.filter(board=parent.board, parent=parent).count()
        y += siblings * 18
    except Exception:
        pass
    node = _create_node_from_prompt(user, parent.board, prompt, parent, x, y, web_search_enabled, speed_mode)
    return JsonResponse({'node': _serialize_node(node)})
