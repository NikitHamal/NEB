import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from api.models import CanvasBoard, CanvasObject
from api.utils import now_ms, uuid_str
from .view_helpers import _rate_limit
from .views_canvas import _require_user, _serialize_node, _spend_canvas_credit, _canvas_credit_state
from .canvas_agent import _bot_config, _raw_json, board_context
from .canvas_agent_tools import AGENT_LOOP_SYSTEM, TOOL_SCHEMA, _parse_json, execute_tool, commit_created
from .canvas_history import snapshot_board

MAX_OBJECTS = 800
MAX_AGENT_TURNS = 6


def _owned_board(user, board_id):
    from django.shortcuts import get_object_or_404
    return get_object_or_404(CanvasBoard, id=board_id, user=user)


def _payload(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (TypeError, ValueError):
        return {}


def _serialize_object(obj):
    try:
        payload = json.loads(obj.payload or "{}")
        if not isinstance(payload, dict):
            payload = {}
    except (TypeError, ValueError):
        payload = {}
    payload.setdefault("id", obj.id)
    payload.setdefault("type", obj.obj_type)
    payload.setdefault("x", obj.x)
    payload.setdefault("y", obj.y)
    payload["z"] = obj.z
    return payload


@require_GET
def ajax_canvas_objects(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    board = _owned_board(user, board_id)
    rows = CanvasObject.objects.filter(board=board).order_by("z", "created_at")[:MAX_OBJECTS]
    return JsonResponse({"objects": [_serialize_object(o) for o in rows]})


@require_POST
def ajax_canvas_objects_save(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, "canvas_objects_save", 40, 60):
        return JsonResponse({"error": "Too many object saves"}, status=429)
    board = _owned_board(user, board_id)
    data = _payload(request)
    items = data.get("objects") if isinstance(data.get("objects"), list) else []
    items = items[:MAX_OBJECTS]
    now = now_ms()
    from django.db import transaction
    with transaction.atomic():
        CanvasObject.objects.filter(board=board).delete()
        bulk = []
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            oid = str(item.get("id") or uuid_str())[:36]
            otype = str(item.get("type") or "pen")[:24]
            bulk.append(CanvasObject(
                id=oid,
                board=board,
                user=user,
                obj_type=otype,
                payload=json.dumps(item, ensure_ascii=False)[:200000],
                x=float(item.get("x") or item.get("x1") or 0),
                y=float(item.get("y") or item.get("y1") or 0),
                z=i,
                created_at=now,
                updated_at=now,
            ))
        if bulk:
            CanvasObject.objects.bulk_create(bulk)
    board.updated_at = now
    board.save(update_fields=["updated_at"])
    return JsonResponse({"ok": True, "count": len(bulk)})


def _call_planner(board, goal, history, anchor=None):
    config = _bot_config(1800)
    if not config:
        return {
            "thought": "Working offline with a compact exploration plan.",
            "tool_calls": [
                {"name": "add_card", "args": {"title": "How it works", "prompt": f"How does {goal} work?", "kind": "ai", "summary": "Map the mechanism in clear steps."}},
                {"name": "add_card", "args": {"title": "Practice", "prompt": f"Retrieval questions for {goal}", "kind": "practice", "summary": "Turn the map into active recall."}},
                {"name": "finish", "args": {"summary": "Added a mechanism branch and a practice branch."}},
            ],
            "done": False,
        }, "fallback"
    from api.neby import call_ai_api
    hist = json.dumps(history[-4:], ensure_ascii=False)[:6000]
    prompt = (
        f"USER GOAL:\n{goal[:1200]}\n\nCANVAS:\n{board_context(board)}\n\n"
        f"TOOLS:\n{json.dumps(TOOL_SCHEMA, ensure_ascii=False)}\n\n"
        f"RECENT TURNS:\n{hist or '[]'}"
    )
    if anchor:
        prompt += f"\nANCHOR: {anchor.title or anchor.prompt[:120]} ({anchor.id})"
    data = _parse_json(call_ai_api(AGENT_LOOP_SYSTEM, prompt, config)) or _raw_json("")
    calls = data.get("tool_calls") if isinstance(data.get("tool_calls"), list) else []
    clean = []
    for item in calls[:3]:
        if isinstance(item, dict) and item.get("name"):
            clean.append({"name": str(item.get("name"))[:40], "args": item.get("args") if isinstance(item.get("args"), dict) else {}})
    if not clean:
        clean = [{"name": "finish", "args": {"summary": "Could not plan a useful next step."}}]
    return {
        "thought": str(data.get("thought") or "")[:280],
        "tool_calls": clean,
        "done": bool(data.get("done")),
    }, config.provider


@require_POST
def ajax_canvas_agent_run(request, board_id):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, "canvas_agent_run", 6, 60):
        return JsonResponse({"error": "Neby is cooling down. Try again shortly."}, status=429)
    board = _owned_board(user, board_id)
    data = _payload(request)
    goal = str(data.get("goal") or "Find the most useful next branches.").strip()[:1600]
    anchor_id = str(data.get("anchorId") or "")
    from api.models import CanvasNode
    anchor = CanvasNode.objects.filter(id=anchor_id, board=board).first() if anchor_id else None
    ok, unlimited, remaining = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({"error": "You are out of Neby credits.", "need_credits": True}, status=402)
    snapshot_board(board, user, "Before Neby agent")
    created = {"nodes": [], "objects": []}
    history = []
    summary = ""
    provider = "fallback"
    for _ in range(MAX_AGENT_TURNS):
        plan, provider = _call_planner(board, goal, history, anchor=anchor)
        results = []
        done = bool(plan.get("done"))
        for call in plan.get("tool_calls") or []:
            result = execute_tool(board, user, call.get("name"), call.get("args") or {}, created)
            results.append({"name": call.get("name"), "ok": bool(result.get("ok")), "result": result})
            if result.get("done"):
                done = True
                summary = result.get("summary") or summary
        history.append({
            "thought": plan.get("thought") or "",
            "tools": [{"name": c.get("name")} for c in (plan.get("tool_calls") or [])],
            "results": [{"name": r["name"], "ok": r["ok"]} for r in results],
        })
        if done:
            break
    nodes = commit_created(board, created)
    if not summary:
        summary = (history[-1].get("thought") if history else "") or "Exploration complete."
    unlimited2, remaining2, allowance = _canvas_credit_state(user)
    return JsonResponse({
        "summary": summary[:500],
        "trace": history,
        "nodes": [_serialize_node(n) for n in nodes],
        "objects": created.get("objects") or [],
        "provider": provider,
        "credits": {"unlimited": unlimited2, "remaining": remaining2, "allowance": allowance},
    })
