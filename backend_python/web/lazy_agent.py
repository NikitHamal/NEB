import json
import re

from api.models import LazyDocMessage
from api.utils import now_ms, uuid_str
from .lazy_io import strip_tags
from .lazy_service import (
    LAZY_PLANNER_SYSTEM, append_section, breakdown_doc, edit_doc,
    generate_doc, llm_chat, parse_llm_json, stream_reply,
)

MAX_CONTEXT_MESSAGES = 10
DOC_SNIPPET = 1400


def _meta(raw):
    try:
        v = json.loads(raw or "{}")
        return v if isinstance(v, dict) else {}
    except Exception:
        return {}


def build_context(session):
    msgs = list(LazyDocMessage.objects.filter(session=session).order_by("-created_at", "-id")[:MAX_CONTEXT_MESSAGES])
    msgs.reverse()
    lines = []
    for m in msgs:
        content = (m.content or "").strip()[:700]
        att = _meta(m.meta).get("attachmentText")
        if m.role == "user" and att:
            content += "\n[attached file excerpt]: " + str(att)[:3000]
        lines.append(f"{m.role}: {content}")
    doc_digest = strip_tags(session.doc_html)[:DOC_SNIPPET]
    if session.doc_html:
        doc_state = f"WORKING DOCUMENT: \"{session.doc_title or session.title}\" ({len(session.doc_html)} chars HTML)."
        if doc_digest:
            doc_state += f"\nDigest: {doc_digest}"
    else:
        doc_state = "WORKING DOCUMENT: none yet."
    return "\n".join(lines), doc_state


WRITE_RE = re.compile(r"\b(write|draft|generate|create|make|compose|prepare|essay|assignment|report|resume|cv|letter|summary)\b", re.I)
EDIT_RE = re.compile(r"\b(improve|fix|shorten|expand|reword|formal|restructure|proofread|polish|rewrite|tone)\b", re.I)
ADD_RE = re.compile(r"\b(add|append|another)\b.*\bsection\b|\bsection (about|on|for)\b", re.I)
PLAN_RE = re.compile(r"checklist|breakdown|to-?do|\bplan\b|\bsteps\b", re.I)


def plan(user, session, user_text):
    history, doc_state = build_context(session)
    prompt = (
        f"{doc_state}\n\nRECENT CONVERSATION:\n{history or '(empty)'}\n\n"
        f"NEW USER MESSAGE:\n{user_text[:1500]}\n\nPick exactly one tool. JSON only."
    )
    raw = llm_chat(user, LAZY_PLANNER_SYSTEM, prompt, max_tokens=320, temperature=0.2, timeout=45)
    data = parse_llm_json(raw) if raw else None
    low = user_text.lower()
    has_doc = bool(session.doc_html)
    if not data or not data.get("tool"):
        if WRITE_RE.search(low) and not PLAN_RE.search(low):
            tool, args = "generate_doc", {"topic": user_text[:200], "type": "assignment", "pages": 2}
        elif has_doc and EDIT_RE.search(low):
            tool, args = "edit_doc", {"instruction": user_text[:400]}
        elif has_doc and ADD_RE.search(low):
            tool, args = "append_section", {"brief": user_text[:300]}
        elif has_doc and PLAN_RE.search(low):
            tool, args = "breakdown", {}
        else:
            tool, args = "reply", {"text": ""}
        return {"think": "heuristic fallback", "tool": tool, "args": args}
    think = str(data.get("think") or "")[:280]
    tool = str(data.get("tool") or "reply").strip().lower()[:24]
    if tool not in ("reply", "generate_doc", "edit_doc", "append_section", "breakdown"):
        tool = "reply"
    args = data.get("args") if isinstance(data.get("args"), dict) else {}
    return {"think": think, "tool": tool, "args": args}


def chunk_text(text, size=90):
    out = []
    i = 0
    text = text or ""
    while i < len(text) and len(out) < 400:
        piece = text[i:i + size]
        nl = piece.rfind("\n")
        if nl > 30:
            piece = piece[:nl + 1]
        out.append(piece)
        i += len(piece)
    return out


def stream_turn(session, user, user_text, sink):
    """Generator: yields SSE-ready dict frames; on completion sets sink['turn']."""
    tools = []
    reply = []

    def say(text):
        reply.append(text)
        return {"type": "delta", "content": text}

    decision = plan(user, session, user_text)
    yield {"type": "think", "content": decision["think"]}
    tool = decision["tool"]
    args = decision.get("args") or {}

    if tool == "generate_doc":
        topic = str(args.get("topic") or user_text)[:300]
        pages = args.get("pages") or 2
        try:
            pages = max(1, min(4, int(pages)))
        except Exception:
            pages = 2
        doc_type = str(args.get("type") or "assignment")[:20]
        yield {"type": "status", "tool": "generate_doc", "label": f"Drafting {doc_type} — {topic[:60]}"}
        result = generate_doc(user, topic, pages=pages, doc_type=doc_type)
        session.doc_html = result["html"]
        session.doc_title = result["title"]
        tools.append({"name": "generate_doc", "summary": f"Drafted \u201c{result['title'][:60]}\u201d ({pages}p)"})
        yield {"type": "doc", "title": result["title"], "html": result["html"]}
        yield say(f"Drafted **{result['title']}** — it's open in the document panel. Tell me what to change.")

    elif tool == "edit_doc":
        instruction = str(args.get("instruction") or user_text)[:600]
        if not session.doc_html:
            yield {"type": "status", "tool": "generate_doc", "label": "Nothing to edit yet — drafting instead"}
            result = generate_doc(user, user_text[:200], pages=2)
            session.doc_html = result["html"]
            session.doc_title = result["title"]
            tools.append({"name": "generate_doc", "summary": f"No draft existed — created \u201c{result['title'][:60]}\u201d"})
            yield {"type": "doc", "title": result["title"], "html": result["html"]}
            yield say(f"There was nothing to edit yet, so I drafted **{result['title']}** instead.")
        else:
            yield {"type": "status", "tool": "edit_doc", "label": f"Revising — {instruction[:60]}"}
            result = edit_doc(user, session.doc_html, instruction)
            if result:
                session.doc_html = result["html"]
                if result.get("title"):
                    session.doc_title = result["title"]
                tools.append({"name": "edit_doc", "summary": result.get("summary") or instruction[:80]})
                yield {"type": "doc", "title": session.doc_title, "html": session.doc_html}
                yield say(result.get("summary") or "Document revised.")
            else:
                tools.append({"name": "edit_doc", "summary": "Revision failed — previous version kept"})
                yield say("I couldn't apply that revision cleanly, so your previous version is untouched. Try a narrower instruction.")

    elif tool == "append_section":
        brief = str(args.get("brief") or user_text)[:400]
        if not session.doc_html:
            yield {"type": "status", "tool": "generate_doc", "label": "No document yet — drafting first"}
            result = generate_doc(user, brief[:200], pages=2)
            session.doc_html = result["html"]
            session.doc_title = result["title"]
            tools.append({"name": "generate_doc", "summary": f"Created base document \u201c{result['title'][:50]}\u201d"})
            yield {"type": "doc", "title": result["title"], "html": result["html"]}
            yield say(f"No document existed, so I drafted **{result['title']}** first.")
        else:
            yield {"type": "status", "tool": "append_section", "label": f"Writing section — {brief[:60]}"}
            result = append_section(user, session.doc_html, brief)
            if result:
                block = f"<h2>{result['heading']}</h2>" + result["body"]
                session.doc_html += block
                tools.append({"name": "append_section", "summary": f"Added section \u201c{result['heading'][:60]}\u201d"})
                yield {"type": "doc", "title": session.doc_title, "html": session.doc_html}
                yield say(f"Added **{result['heading']}** to the end of the document.")
            else:
                tools.append({"name": "append_section", "summary": "Section generation failed"})
                yield say("The new section didn't come through — try again with a slightly different brief.")

    elif tool == "breakdown":
        yield {"type": "status", "tool": "breakdown", "label": "Building checklist from the document"}
        if session.doc_html:
            md = breakdown_doc(user, session.doc_html)
            tools.append({"name": "breakdown", "summary": "Generated task checklist"})
            for piece in chunk_text(md):
                yield say(piece)
        else:
            yield say("There's no document to break down yet — ask me to draft one first.")

    else:
        history, doc_state = build_context(session)
        prompt = f"{doc_state}\n\nCONVERSATION:\n{history}\n\nReply to: {user_text[:1200]}"
        got_any = False
        for chunk in stream_reply(user, prompt):
            ctype = chunk.get("type")
            if ctype == "text":
                content = chunk.get("content") or ""
                if content:
                    got_any = True
                    reply.append(content)
                    yield {"type": "delta", "content": content}
            elif ctype == "done":
                break
        if not got_any:
            yield say("Here's where we stand — tell me what to draft or revise next.")

    sink["turn"] = {
        "tools": tools,
        "reply": "".join(reply).strip() or "(no output)",
        "doc_updated": bool(session.doc_html and any(t["name"] in ("generate_doc", "edit_doc", "append_section") for t in tools)),
    }


def persist_turn(session, turn_result):
    now = now_ms()
    assistant = LazyDocMessage.objects.create(
        id=uuid_str(), session=session, role="assistant",
        content=turn_result["reply"][:40000],
        meta=json.dumps({"tools": turn_result["tools"], "docUpdated": turn_result["doc_updated"]}, ensure_ascii=False),
        created_at=now,
    )
    session.message_count = LazyDocMessage.objects.filter(session=session).count()
    session.updated_at = now
    session.save(update_fields=["doc_html", "doc_title", "message_count", "updated_at"])
    return assistant
