import json
import uuid

from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from api.models import CanvasBoard, CanvasNode, User
from api.utils import now_ms, uuid_str
from .view_helpers import _ctx, _get_valid_token, _rate_limit, _blobatar_url_for
from api.security import get_user_by_auth_token

SYSTEM_PROMPT = """You are Wondering Canvas — a spatial research engine that turns any question into a rich, visual, node-based explanation.

You output ONLY a single JSON object (no markdown fences, no extra text) with this schema:
{
  "title": "Short crisp title derived from the prompt (3-6 words)",
  "summary": "One paragraph overview (40-60 words) with **bold** on key terms.",
  "sections": [
    {"type": "text", "content": "Markdown paragraph. Use **bold** for key terms. 40-70 words. No lists."},
    {
      "type": "flow",
      "title": "Pipeline / architecture title",
      "nodes": [{"label": "1-3 word stage", "tone": "blue|green|amber|rose|slate", "desc": "optional one-liner"}],
      "links": ["label on arrow into next node", "..."]  
    },
    {
      "type": "diagram",
      "title": "System map title",
      "nodes": [{"id": "slug", "label": "Short label", "desc": "One-line meaning"}],
      "edges": [{"from": "id", "to": "id"}],
      "note": "Optional caption"
    },
    {
      "type": "timeline",
      "title": "History / process title",
      "steps": [{"title": "Step or year", "sub": "one-line detail"}]
    },
    {
      "type": "stats",
      "items": [{"k": "Metric name", "v": "Value"}]
    },
    {
      "type": "comparison",
      "title": "Comparison title",
      "headers": ["Aspect", "Column A", "Column B"],
      "rows": [["Row label", "Col A value", "Col B value"]]
    },
    {"type": "quote", "text": "A crisp defining sentence.", "cite": "optional source"},
    {"type": "code", "lang": "python", "text": "short snippet when topic is programming"},
    {"type": "proscons", "title": "Trade-off title", "pros": ["..."], "cons": ["..."]},
    {
      "type": "cards",
      "title": "Visual reference title",
      "items": [{"title": "Name", "subtitle": "Who · year · tagline", "bullets": ["Attr: ..."], "desc": "One sentence."}]
    },
    {"type": "bullets", "title": "List title", "items": ["Point 1", "Point 2"]},
    {"type": "ask_user", "question": "What context do you mean?", "options": ["Option A", "Option B"], "placeholder": "Or type your context..."}
  ]
}

Rules:
- Always include at least 1 text section and be GENEROUS with visuals — pick 3-5 sections total.
- Use "flow" for any pipeline/architecture (3-6 nodes; tones cycle blue→green→amber→rose→slate; links array length = nodes-1, each a 1-2 word verb like "predicts", "encodes", "routes to").
- Use "diagram" when relationships branch or loop (interactive tap-to-explain).
- Use "timeline" for histories, lifecycles, multi-step processes (3-6 steps).
- Use "stats" for striking numbers/scales (2-4 items).
- Use "proscons" for trade-offs. Use "comparison" for head-to-head alternatives (3-5 rows).
- Sprinkle one "quote" (crisp definition) when natural. "code" ONLY for programming topics.
- "cards" only for objects/products/people. "bullets" sparingly.
- Use "ask_user" when the prompt is vague, ambiguous, or lacks context — do NOT hallucinate. Ask for clarification with 2-4 concise options. This is PREFERRED over guessing. Be truthful: if you don't know, say so and ask.
- Flow node labels are Title Case, 1-3 words. Timeline sub max 12 words.
- Web search is ALWAYS available to you. When any fact came from web results, add a top-level "references" array: "references": [{"title": "Page title", "url": "https://...", "source": "site name"}] — max 4, ONLY real URLs you actually saw. Never invent URLs; omit references if none were used.
- Be truthful, concise, educational. No repetition. No generic filler like "An overview of X broken into a visual structure". Raw JSON only.
"""


def _resolve_user(request):
    token = _get_valid_token(request)
    if token:
        try:
            return get_user_by_auth_token(token)
        except User.DoesNotExist:
            pass
    if hasattr(request, 'user') and request.user and request.user.is_authenticated:
        return request.user
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
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


CANVAS_MAX_NODES = 240

def _canvas_at_capacity(board, extra=1):
    return CanvasNode.objects.filter(board=board).count() + max(0, int(extra)) > CANVAS_MAX_NODES


def _serialize_board(board):
    try:
        settings = json.loads(getattr(board, 'settings', '') or '{}')
        if not isinstance(settings, dict):
            settings = {}
    except Exception:
        settings = {}
    return {
        'id': board.id,
        'title': board.title,
        'createdAt': board.created_at,
        'updatedAt': board.updated_at,
        'nodeCount': getattr(board, '_node_count', 0),
        'settings': settings,
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
    meta = {}
    try:
        if getattr(node, 'metadata', ''):
            meta = json.loads(node.metadata)
            if not isinstance(meta, dict):
                meta = {}
    except Exception:
        meta = {}
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
        'kind': getattr(node, 'kind', '') or 'ai',
        'meta': meta,
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

    vague = p.strip().lower()
    if vague in ["define environment", "what is environment", "environment", "explain environment", "define environment?", "what is an environment"] or (len(vague.split()) <= 3 and vague.startswith("define ") and "environment" in vague):
        return {
            "title": "Which environment?",
            "summary": "I'd like to be precise — **which environment** are you asking about?",
            "sections": [
                {"type": "ask_user", "question": "Which environment would you like to explore?", "options": ["Natural environment — ecosystems & conservation", "Programming / software environment", "World model / AI environment", "Learning / study environment"], "placeholder": "Or describe your context…"}
            ]
        }
    if len(p.strip().split()) <= 2 and not parent_context:
        clean = p.strip()
        if clean and len(clean) < 20:
            return {
                "title": "Could you clarify?",
                "summary": f"You asked **\"{prompt.strip()}\"** — could you share a bit more context so I can be precise?",
                "sections": [
                    {"type": "ask_user", "question": f"What would you like to know about \"{prompt.strip()}\" ?", "options": ["Give me a definition", "Show me an example", "Explain how it works", "Compare it to something else"], "placeholder": "Add more detail…"}
                ]
            }

    if "raw sensory" in p:
        return {
            "title": "Raw Sensory Data",
            "summary": "**Raw sensory data** is the unprocessed stream from the environment — pixels, audio waves, proprioceptive signals — before any abstraction.",
            "sections": [
                {"type": "flow", "title": "From photons to plans", "nodes": [
                    {"label": "Sensors", "tone": "slate"},
                    {"label": "Encoder", "tone": "blue", "desc": "CNN / ViT"},
                    {"label": "Latent State", "tone": "green"},
                    {"label": "World Model", "tone": "amber"},
                ], "links": ["captures", "compresses", "feeds"]},
                {"type": "stats", "items": [
                    {"k": "Raw video", "v": "~1 Gbps"},
                    {"k": "Latent state", "v": "~4 KB"},
                    {"k": "Compression", "v": "100000x"},
                ]},
                {"type": "comparison", "title": "Raw vs Latent", "headers": ["Aspect", "Raw", "Latent"], "rows": [
                    ["Size", "MB per frame", "Hundreds of floats"],
                    ["Noise", "High", "Filtered"],
                    ["Planning", "Too heavy", "Compact rollouts"],
                ]},
            ],
        }
    if "dynamics" in p and "predict" in p:
        return {
            "title": "Dynamics Predictor",
            "summary": "The **dynamics predictor** learns how latent state evolves under an action — the foresight engine of a world model.",
            "sections": [
                {"type": "text", "content": "Given current **latent state** and an **action**, it outputs the next-state distribution. Training minimizes prediction gap against real futures, forcing internalized **causality**."},
                {"type": "flow", "title": "One imagination step", "nodes": [
                    {"label": "State z(t)", "tone": "blue"},
                    {"label": "Action a(t)", "tone": "slate"},
                    {"label": "Next State", "tone": "green"},
                    {"label": "Reward r(t)", "tone": "amber"},
                ], "links": ["plus", "predicts", "scores"]},
                {"type": "proscons", "title": "Deterministic vs stochastic heads", "pros": ["Stable rollouts", "Cheap to sample"], "cons": ["Misses multimodality", "Blur on uncertainty"]},
            ],
        }
    if "world model" in p:
        return {
            "title": "World Models",
            "summary": "A **world model** is an internal, predictive simulation of the environment — an agent imagines futures, evaluates actions, and plans without touching reality.",
            "sections": [
                {"type": "quote", "text": "Instead of reacting purely on instinct, a world model can mentally 'play out' scenarios, anticipate consequences, and plan long-term."},
                {"type": "flow", "title": "Components of a World Model", "nodes": [
                    {"label": "Perception", "tone": "green", "desc": "encodes raw data"},
                    {"label": "Dynamics Predictor", "tone": "blue", "desc": "imagines next state"},
                    {"label": "Reward Estimator", "tone": "amber"},
                    {"label": "Action Policy", "tone": "rose", "desc": "picks best move"},
                ], "links": ["encodes", "predicts", "informs"]},
                {"type": "diagram", "title": "The learning loop", "nodes": [
                    {"id": "act", "label": "Act", "desc": "policy acts in world"},
                    {"id": "sense", "label": "Sense", "desc": "observe result"},
                    {"id": "train", "label": "Train", "desc": "update model"},
                    {"id": "imagine", "label": "Imagine", "desc": "dream rollouts"},
                    {"id": "plan", "label": "Plan", "desc": "pick better action"},
                ], "edges": [{"from": "act", "to": "sense"}, {"from": "sense", "to": "train"}, {"from": "train", "to": "imagine"}, {"from": "imagine", "to": "plan"}, {"from": "plan", "to": "act"}], "note": "Tap any stage to unpack it."},
                {"type": "timeline", "title": "Milestones", "steps": [
                    {"title": "1989", "sub": "Sutton's Dyna — learn, imagine, plan"},
                    {"title": "2018", "sub": "World Models paper dreams in VAE space"},
                    {"title": "2023", "sub": "DreamerV3 masters 150+ tasks"},
                    {"title": "2025", "sub": "Video world models scale to games"},
                ]},
                {"type": "comparison", "title": "World Models vs LLMs", "headers": ["Aspect", "World Models", "LLMs"], "rows": [
                    ["Objective", "Predict next state", "Predict next token"],
                    ["Grounding", "Physics of environment", "Human text"],
                    ["Planning", "Imagined rollouts", "Chain-of-thought"],
                ]},
                {"type": "stats", "items": [
                    {"k": "Rollout speed", "v": "1000x realtime"},
                    {"k": "Dreamer tasks", "v": "150+"},
                ]},
            ],
        }
    if "control theory" in p or ("control" in p and "loop" not in p):
        return {
            "title": "Control Theory",
            "summary": "**Control theory** is the mathematics of steering systems toward desired behavior by adjusting inputs based on measured feedback.",
            "sections": [
                {"type": "flow", "title": "Closed loop", "nodes": [
                    {"label": "Reference", "tone": "slate", "desc": "goal"},
                    {"label": "Controller", "tone": "blue", "desc": "computes input"},
                    {"label": "Plant", "tone": "green", "desc": "the system"},
                    {"label": "Sensor", "tone": "amber", "desc": "measures output"},
                ], "links": ["setpoint", "drives", "produces"]},
                {"type": "diagram", "title": "Feedback path", "nodes": [
                    {"id": "err", "label": "Error", "desc": "reference minus measured"},
                    {"id": "pid", "label": "PID", "desc": "P·I·D terms summed"},
                    {"id": "out", "label": "Output", "desc": "physical response"},
                    {"id": "fb", "label": "Feedback", "desc": "sensor closes loop"},
                ], "edges": [{"from": "err", "to": "pid"}, {"from": "pid", "to": "out"}, {"from": "out", "to": "fb"}, {"from": "fb", "to": "err"}]},
                {"type": "timeline", "title": "From governor to Mars", "steps": [
                    {"title": "1788", "sub": "Watt's centrifugal governor"},
                    {"title": "1942", "sub": "Ziegler-Nichols PID tuning rules"},
                    {"title": "1969", "sub": "Apollo lunar module guidance"},
                    {"title": "Now", "sub": "Every drone, rocket and thermostat"},
                ]},
                {"type": "proscons", "title": "Open vs closed loop", "pros": ["Rejects disturbances", "Self-correcting"], "cons": ["Sensor noise risk", "Can oscillate if mistuned"]},
            ],
        }
    if "chair" in p or "danish" in p:
        return {
            "title": "Iconic Danish Chairs",
            "summary": "Danish modern distilled function to its purest form — honest materials, human proportions, quiet craft that still feels contemporary.",
            "sections": [
                {"type": "quote", "text": "A chair should be beautiful from all sides and angles.", "cite": "Hans J. Wegner"},
                {"type": "cards", "title": "Four icons", "items": [
                    {"title": "CH07 Shell Chair", "subtitle": "Wegner · 1963", "bullets": ["Molded plywood + steel", "Floating lightness"], "desc": "Three curved shells give winged comfort."},
                    {"title": "Wishbone CH24", "subtitle": "Wegner · 1949", "bullets": ["Solid wood + paper cord", "100+ hand steps"], "desc": "Steamed Y-back, woven seat."},
                    {"title": "PK22", "subtitle": "Kjærholm · 1956", "bullets": ["Steel + wicker", "Industrial elegance"], "desc": "Thin frame, suspended comfort."},
                    {"title": "Sibast No 8", "subtitle": "Sibast · 1953", "bullets": ["Teak + leather", "Quiet luxury"], "desc": "Stitched back, soft curves."},
                ]},
                {"type": "timeline", "title": "Golden age", "steps": [
                    {"title": "1944", "sub": "China chair series begins"},
                    {"title": "1949", "sub": "Wishbone enters production"},
                    {"title": "1956", "sub": "PK22 wins Milan Triennale"},
                    {"title": "1963", "sub": "Shell chair debuts"},
                ]},
            ],
        }
    base_title = title_cap if title_cap else "Understanding"
    return {
        "title": base_title,
        "summary": f"**{prompt.strip()[:60]}** — here's a concise, structured view. If you share a bit more context, I can tailor the next card precisely.",
        "sections": [
            {"type": "text", "content": f"**{prompt.strip()[:60]}** can be viewed as a system of parts. The key is to separate *what's being described*, *how it behaves*, and *why it matters*. This structure lets you drill into any part via the thread or ask a follow-up below."},
            {"type": "flow", "title": "Core pipeline", "nodes": [
                {"label": "Input", "tone": "slate"},
                {"label": "Encode", "tone": "blue"},
                {"label": "Predict", "tone": "green"},
                {"label": "Decide", "tone": "amber"},
            ], "links": ["arrives as", "into state", "forward"]},
            {"type": "stats", "items": [
                {"k": "Core idea", "v": "Model → Imagine → Act"},
                {"k": "Key lever", "v": "Prediction quality"},
            ]},
            {"type": "proscons", "title": "Two lenses", "pros": ["Structure & foresight", "Data efficient"], "cons": ["Needs a good model", "Harder to debug"]},
        ],
    }


def _extract_json_str(s):
    """Return substring from first '{' to matching '}' accounting for strings."""
    start = s.find('{')
    if start == -1:
        return None
    depth = 0
    in_str = None
    esc = False
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == in_str:
                in_str = None
        else:
            if ch in ('"', "'"):
                in_str = ch
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return s[start:i+1]
    return None


def _try_lenient_loads(s):
    import re, ast
    try:
        return json.loads(s)
    except Exception:
        pass
    # trailing commas before } or ]
    try:
        fixed = re.sub(r',\s*([}\]])', r'\1', s)
        return json.loads(fixed)
    except Exception:
        pass
    # Python-literal fallback (single quotes, True/False/None)
    try:
        v = ast.literal_eval(s)
        if isinstance(v, dict):
            return v
    except Exception:
        pass
    # single-quote to double-quote heuristic (only if no double quotes inside)
    try:
        fixed = re.sub(r",\s*([}\]])", r"\1", s)
        # very naive: replace single quotes wrapping keys/values when safe
        # use ast again after normalising
        v = ast.literal_eval(fixed)
        if isinstance(v, dict):
            return v
    except Exception:
        pass
    return None


def _parse_canvas_json(prompt, raw):
    """Parse LLM output into canvas card content. Returns dict or None if unusable."""
    raw = (raw or "").strip()
    if not raw:
        return None
    # strip markdown fences
    if "```" in raw:
        import re
        m = re.search(r'```(?:json)?\s*([\s\S]*?)```', raw, re.I)
        if m:
            raw = m.group(1).strip()
        elif raw.strip().startswith("```"):
            raw = raw.strip().strip("`")
            if raw.lstrip().lower().startswith("json"):
                raw = raw.lstrip()[4:].strip()
    # extract the JSON object if there's surrounding text
    jstr = _extract_json_str(raw)
    candidate = jstr if jstr else raw
    data = _try_lenient_loads(candidate)
    if data is None and jstr and jstr != raw:
        data = _try_lenient_loads(raw)
    if not isinstance(data, dict) or "title" not in data:
        return None
    if not data.get("sections"):
        data["sections"] = [{"type": "text", "content": raw[:800]}]
    refs = data.get("references")
    if isinstance(refs, list) and refs and not any(s.get("type") == "references" for s in data.get("sections", [])):
        items = []
        for r in refs[:6]:
            if isinstance(r, str):
                items.append({"title": r[:120], "url": "", "source": ""})
            elif isinstance(r, dict) and (r.get("url") or r.get("title")):
                items.append({
                    "title": (r.get("title") or r.get("url") or "")[:140],
                    "url": (r.get("url") or "")[:500],
                    "source": (r.get("source") or "")[:80],
                })
        if items:
            data["sections"].append({"type": "references", "items": items})
    return data


def _wrap_raw_text(prompt, raw):
    raw = (raw or "").strip()
    return {
        "title": prompt.strip().split("?")[0][:40] or "Result",
        "summary": raw[:260] + ("…" if len(raw) > 260 else ""),
        "sections": [{"type": "text", "content": raw[:1800]}],
    }


# Fused primary: Gemini Web (primary) + Motif 3 High + Laguna S 2.1
# All three are free web proxies; their outputs are scored and fused.
_CANVAS_PRIMARY_MODEL = 'laguna-s-2.1'
_GEMINIWEB_MODEL = 'geminiweb/gemini-flash-lite'
_MOTIF_MODEL = 'motif-102b'
_FUSION_MODEL_LABEL = 'fusion:geminiweb+motif-high+laguna-s-2.1'


def _score_canvas_data(data):
    if not isinstance(data, dict):
        return -1
    sections = data.get('sections') or []
    if not isinstance(sections, list):
        return -1
    score = len(sections) * 10
    types = set()
    for s in sections:
        if isinstance(s, dict) and isinstance(s.get('type'), str):
            types.add(s['type'])
    for t in ('flow', 'diagram', 'timeline', 'stats', 'proscons', 'comparison', 'quote'):
        if t in types:
            score += 5
    # penalize vague ask_user when not needed — small penalty
    if types == {'ask_user'} or (len(types) == 1 and 'ask_user' in types):
        score -= 2
    summary = data.get('summary') or ''
    if isinstance(summary, str) and 20 < len(summary.split()) < 90:
        score += 4
    title = data.get('title') or ''
    if isinstance(title, str) and 2 <= len(title.split()) <= 8:
        score += 3
    refs = data.get('references')
    if isinstance(refs, list) and refs:
        score += 4
    # bonus for rich visual mix
    if len(types) >= 4:
        score += 4
    return score


def _merge_fusion_references(winner, candidates):
    """Merge unique references from all candidates into winner (in-place)."""
    try:
        seen = set()
        merged = []
        # collect existing
        for sec in winner.get('sections') or []:
            if isinstance(sec, dict) and sec.get('type') == 'references':
                for it in sec.get('items') or []:
                    u = (it.get('url') or '').strip().lower()
                    if u:
                        seen.add(u)
        # collect from candidates' raw references + sections
        for cand in candidates:
            if not isinstance(cand, dict):
                continue
            # top-level references array
            for r in (cand.get('references') or [])[:4]:
                if isinstance(r, dict):
                    u = (r.get('url') or '').strip()
                    key = (u or r.get('title') or '').strip().lower()
                    if key and key not in seen:
                        seen.add(key)
                        merged.append({
                            'title': (r.get('title') or r.get('url') or '')[:140],
                            'url': (r.get('url') or '')[:500],
                            'source': (r.get('source') or '')[:80],
                        })
            # references section items
            for sec in cand.get('sections') or []:
                if isinstance(sec, dict) and sec.get('type') == 'references':
                    for it in sec.get('items') or []:
                        u = (it.get('url') or '').strip().lower()
                        if u and u not in seen:
                            seen.add(u)
                            merged.append(it)
                        elif not u:
                            t = (it.get('title') or '').strip().lower()
                            if t and t not in seen:
                                seen.add(t)
                                merged.append(it)
        if merged:
            # cap at 4, prefer those with URLs
            merged = sorted(merged, key=lambda x: (0 if x.get('url') else 1))[:4]
            # append or create references section
            has_ref_sec = False
            for sec in winner.get('sections') or []:
                if isinstance(sec, dict) and sec.get('type') == 'references':
                    # merge into existing
                    existing_urls = set((it.get('url') or '').strip().lower() for it in sec.get('items') or [])
                    for it in merged:
                        if (it.get('url') or '').strip().lower() not in existing_urls:
                            sec.setdefault('items', []).append(it)
                    has_ref_sec = True
                    break
            if not has_ref_sec:
                winner.setdefault('sections', []).append({'type': 'references', 'items': merged})
    except Exception:
        pass


def _call_llm_for_canvas(user, prompt, parent_context, web_search_enabled, speed_mode):
    from api.llm.credentials import resolve
    from api.llm.client import chat, LLMError

    user_prompt = prompt.strip()
    if parent_context:
        user_prompt = f"Ancestor context (use to keep drill-downs consistent):\n{parent_context}\n\n---\n\nNew question to answer as a new child card: {prompt.strip()}"
    speed_note = "Fast" if (speed_mode or "fast").lower() == "fast" else "Deep"
    user_prompt = f"[{speed_note} mode — answer quickly but thoroughly]\n" + user_prompt

    # ── 1. Fused primary: Gemini Web + Motif 3 High + Laguna S 2.1 ──
    import logging as _logging
    _log = _logging.getLogger(__name__)

    def _call_gemini():
        try:
            from api.geminiweb_proxy import simple_chat as _g
            return _g(user_prompt, _GEMINIWEB_MODEL, SYSTEM_PROMPT, 3600)
        except Exception as e:
            _log.warning("Canvas geminiweb call failed: %s", e)
            return None

    def _call_motif():
        try:
            from api.motiftech_proxy import simple_chat as _m
            return _m(user_prompt, _MOTIF_MODEL, SYSTEM_PROMPT, 3600, reasoning_effort="high")
        except Exception as e:
            _log.warning("Canvas motif-high call failed: %s", e)
            return None

    def _call_laguna():
        try:
            from api.poolside_proxy import simple_chat as _p
            return _p(user_prompt, _CANVAS_PRIMARY_MODEL, SYSTEM_PROMPT, 3600)
        except Exception as e:
            _log.warning("Canvas laguna call failed: %s", e)
            return None

    raw_by = {}
    data_by = {}
    score_by = {}
    try:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        ex = ThreadPoolExecutor(max_workers=3)
        fut_map = {
            ex.submit(_call_gemini): 'geminiweb',
            ex.submit(_call_motif): 'motif',
            ex.submit(_call_laguna): 'poolside',
        }
        try:
            for fut in as_completed(fut_map, timeout=58):
                key = fut_map[fut]
                try:
                    raw = fut.result(timeout=1)
                except Exception as e:
                    _log.warning("Canvas %s future error: %s", key, e)
                    raw = None
                raw_by[key] = raw
                if raw:
                    d = _parse_canvas_json(prompt, raw)
                    if d:
                        data_by[key] = d
                        score_by[key] = _score_canvas_data(d)
                    else:
                        score_by[key] = -1
                else:
                    score_by[key] = -1
        except Exception as e:
            _log.warning("Canvas fusion as_completed timeout/error: %s", e)
        finally:
            try:
                ex.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                ex.shutdown(wait=False)

        # pick best valid candidate (geminiweb wins ties as primary)
        best_key = None
        best_score = -1
        priority = {'geminiweb': 3, 'motif': 2, 'poolside': 1}
        for k, sc in score_by.items():
            if k not in data_by:
                continue
            prio = priority.get(k, 0)
            # score + tiny tie-breaker
            adj = sc + prio * 0.1
            if adj > best_score:
                best_score = adj
                best_key = k
        if best_key and best_key in data_by:
            winner = data_by[best_key]
            # collect all valid candidates for reference merging
            all_valid = [data_by[k] for k in data_by]
            # also include raw-parsed fallback for raw that had references but not scored?
            _merge_fusion_references(winner, all_valid)
            return {'slug': 'fusion', 'model': _FUSION_MODEL_LABEL}, winner, 'fusion'

        # no valid JSON — fall back to best substantial raw (prefer geminiweb)
        for k in ('geminiweb', 'motif', 'poolside'):
            raw = raw_by.get(k)
            if raw and len(raw.strip()) > 200:
                _log.info("Canvas fusion no valid JSON, wrapping raw from %s", k)
                return {'slug': 'fusion', 'model': _FUSION_MODEL_LABEL}, _wrap_raw_text(prompt, raw), 'fusion'
        # else fall through to official providers
    except Exception as e:
        _log.warning("Canvas fusion block error: %s", e)
        pass

    # ── 2. Fallback: official key-backed providers in priority order ──
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

    if resolved:
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
            data = _parse_canvas_json(prompt, raw)
            if data:
                return resolved, data, resolved.slug
            if raw:
                return resolved, _wrap_raw_text(prompt, raw), resolved.slug
        except (LLMError, Exception):
            pass

    # ── 3. Last resort: offline mock so canvas still works ──
    return None, _mock_content(prompt, parent_context), "mock"


def _canvas_credit_state(user):
    """Returns (unlimited, remaining, monthly_allowance)."""
    if user is None:
        return True, 0, 0
    if getattr(user, 'is_admin', False) or getattr(user, 'is_staff', False):
        return True, 0, 0
    try:
        from api.marketplace import total_ai_credits, get_payment_config
        cfg = get_payment_config()
        allowance = ((cfg.free_credits_per_month if cfg else 10)) + (user.ai_credits or 0)
        return False, total_ai_credits(user, cfg), allowance
    except Exception:
        return False, 0, 10


def _spend_canvas_credit(user):
    """Deduct one Neby credit for a generation. Admins are unlimited.
    Returns (ok, unlimited, remaining)."""
    unlimited, remaining, _ = _canvas_credit_state(user)
    if unlimited or user is None:
        return True, True, remaining
    if remaining <= 0:
        return False, False, 0
    try:
        from api.marketplace import consume_ai_credit
        ok = consume_ai_credit(user)
        _, left, _ = _canvas_credit_state(user)
        return ok, False, left
    except Exception:
        return True, False, remaining


_CREDIT_ERROR = ("You're out of Neby credits — top up by converting NEBians points "
                 "on the Credits page, or wait for next month's free credits.")


@never_cache
def canvas_page(request):
    user = _get_user_or_none(request)
    if not user:
        from django.shortcuts import redirect
        from django.urls import reverse
        login_url = reverse('web:login')
        return redirect(f"{login_url}?next=/canvas/")
    boards = []
    current_board = None
    current_board_id = request.GET.get('board') or request.GET.get('b') or ''
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
    try:
        ctx['boards_json'] = json.dumps([_serialize_board(b) for b in boards])
    except Exception:
        ctx['boards_json'] = '[]'
    if user and not ctx.get('user'):
        # Bearer/API-style page load: session is empty, so populate footer user + auth flag
        ctx['is_authenticated'] = True
        photo = user.photo_url or ''
        try:
            avatar = _blobatar_url_for(user) if (getattr(user, 'avatar_use_pp', False) or not photo) else photo
        except Exception:
            avatar = photo
        ctx['user'] = {
            'id': str(user.id),
            'username': user.username,
            'display_name': getattr(user, 'display_name', '') or '',
            'photo_url': photo,
            'avatar_url': avatar,
        }
    unlimited, remaining, allowance = _canvas_credit_state(user)
    pct = 100 if unlimited else int(round((max(0, remaining) / max(1, allowance)) * 100))
    ctx['canvas_credits'] = {
        'unlimited': unlimited,
        'remaining': max(0, remaining),
        'allowance': max(1, allowance),
        'pct': max(0, min(100, pct)),
        'is_admin': bool(getattr(user, 'is_admin', False)),
        'low': (not unlimited) and remaining <= max(1, allowance) * 0.25,
    }
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
def ajax_canvas_board_share(request, board_id):
    board, user, err = _get_board_for_user(request, board_id)
    if err:
        return err
    try:
        payload = json.loads(request.body or '{}')
    except Exception:
        payload = {}
    if payload.get('revoke'):
        board.share_token = None
        board.shared_at = 0
        board.save(update_fields=['share_token', 'shared_at'])
        return JsonResponse({'enabled': False})
    if not board.share_token:
        board.share_token = (uuid.uuid4().hex + uuid.uuid4().hex)[:48]
        board.shared_at = now_ms()
        board.save(update_fields=['share_token', 'shared_at'])
    return JsonResponse({'enabled': True, 'url': f'/canvas/shared/{board.share_token}/'})


def canvas_shared(request, token):
    board = get_object_or_404(CanvasBoard, share_token=token)
    owner_name = ''
    try:
        owner_name = board.user.username or ''
    except Exception:
        pass
    ctx = _ctx(
        request,
        boards=[],
        current_board=None,
        current_board_id=board.id,
        shared=True,
        readonly=True,
        shared_token=token,
        shared_title=board.title,
        shared_owner=owner_name,
    )
    ctx['hide_footer_links'] = True
    return render(request, 'web/canvas.html', ctx)


@require_GET
def ajax_canvas_shared_detail(request, token):
    board = get_object_or_404(CanvasBoard, share_token=token)
    nodes = CanvasNode.objects.filter(board=board).order_by('created_at')
    owner_name = ''
    try:
        owner_name = board.user.username or ''
    except Exception:
        pass
    return JsonResponse({
        'board': {'id': board.id, 'title': board.title},
        'owner': owner_name,
        'readonly': True,
        'nodes': [_serialize_node(n) for n in nodes],
    })


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
    x = max(-100000, min(100000, x))
    y = max(-100000, min(100000, y))

    web_search_enabled = bool(payload.get('web_search_enabled') or payload.get('webSearchEnabled'))
    speed_mode = (payload.get('speed_mode') or payload.get('speedMode') or 'fast').strip().lower()
    if speed_mode not in ('fast', 'deep'):
        speed_mode = 'fast'

    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': _CREDIT_ERROR, 'need_credits': True}, status=402)

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
    node.x = max(-100000, min(100000, x))
    node.y = max(-100000, min(100000, y))
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
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        node.status = 'failed'
        node.error = _CREDIT_ERROR
        node.save(update_fields=['status', 'error'])
        return JsonResponse({'error': _CREDIT_ERROR, 'need_credits': True}, status=402)
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
    try:
        x = float(payload.get('x')) if payload.get('x') is not None else None
        y = float(payload.get('y')) if payload.get('y') is not None else None
    except Exception:
        x, y = None, None
    if x is not None:
        x = max(-100000, min(100000, x))
    if y is not None:
        y = max(-100000, min(100000, y))
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': _CREDIT_ERROR, 'need_credits': True}, status=402)
    node = _create_node_from_prompt(user, parent.board, prompt, parent, x, y, web_search_enabled, speed_mode)
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
    try:
        x = float(payload.get('x')) if payload.get('x') is not None else None
        y = float(payload.get('y')) if payload.get('y') is not None else None
    except Exception:
        x, y = None, None
    if x is None or y is None:
        x = parent.x + 580
        y = parent.y + 70
        try:
            siblings = CanvasNode.objects.filter(board=parent.board, parent=parent).count()
            y += siblings * 18
        except Exception:
            pass
    else:
        x = max(-100000, min(100000, x))
        y = max(-100000, min(100000, y))
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': _CREDIT_ERROR, 'need_credits': True}, status=402)
    node = _create_node_from_prompt(user, parent.board, prompt, parent, x, y, web_search_enabled, speed_mode)
    return JsonResponse({'node': _serialize_node(node)})
