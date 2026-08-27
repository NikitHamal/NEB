import json
import re

from api.models import LazyDocMessage
from api.utils import now_ms, uuid_str
from . import toolstore as tstore
from . import study_tools
from .study_tools import ToolError
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

CONV_RE = re.compile(r"(convert|export|save|transform|turn|change)[^.?!]{0,40}\b(word|docx)\b|\bpdf\b[^.?!]{0,20}\b(to|into|as)\b[^.?!]{0,10}\b(word|docx)\b", re.I)
MERGE_RE = re.compile(r"\b(merge|combine|join|stitch)\b", re.I)
SPLIT_RE = re.compile(r"\b(split|chop)\b[^.?!]{0,30}\b(pages?|parts?|halves?)\b", re.I)
EXTRACT_PAGES_RE = re.compile(r"\b(extract|pull|take out)\b[^.?!]{0,30}\bpages?\b", re.I)
ROTATE_RE = re.compile(r"\brotate\b", re.I)
COMPRESS_RE = re.compile(r"\b(compress|shrink|reduce\s+(the\s+)?size)\b", re.I)
INFO_RE = re.compile(r"how many pages|page count|\bpdf info\b", re.I)
EXTRACT_IMG_RE = re.compile(r"\b(extract|pull out|get)\b[^.?!]{0,25}\b(images?|photos?|pictures?|diagrams?)\b", re.I)
IMG2PDF_RE = re.compile(r"\bimages?\b[^.?!]{0,30}\bpdf\b|\b(jpgs?|jpegs?|pngs?)\b[^.?!]{0,30}\bpdf\b", re.I)
WCOUNT_RE = re.compile(r"@word\s*count\b|word\s*count\s*:|how many words", re.I)


def _extract_pages_param(low):
    m = re.search(r"(\d+)\s*(?:-|–|to)\s*(\d+)", low)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    singles = [s for s in re.findall(r"\b(\d{1,4})\b", low)]
    if len(singles) >= 2 and (re.search(r"\band\b", low) or "," in low):
        return ",".join(singles[:6])
    if singles:
        return singles[0]
    return ""


def _quick_intent(text, kinds):
    low = (text or "")
    has_pdf = "pdf" in kinds
    has_img = any(k in ("png", "jpg", "jpeg") for k in kinds)
    r = CONV_RE.search(low)
    if r and has_pdf:
        return ("pdf_to_docx", {})
    r = MERGE_RE.search(low)
    if r and has_pdf:
        return ("pdf_merge", {})
    r = EXTRACT_PAGES_RE.search(low)
    if r and has_pdf:
        return ("pdf_extract_pages", {"pages": _extract_pages_param(low)})
    r = SPLIT_RE.search(low)
    if r and has_pdf:
        m = re.search(r"every\s+(\d{1,3})", low)
        params = {"ranges": "" if m else _extract_pages_param(low), "every": m.group(1) if m else ""}
        return ("pdf_split", params)
    r = ROTATE_RE.search(low)
    if r and has_pdf:
        ang = re.findall(r"(90|180|270)", low)
        page_spec = ""
        if re.search(r"\d+\s*-\s*\d+", low) or re.search(r"\bpages?\b", low):
            page_spec = _extract_pages_param(low)
        return ("pdf_rotate", {"angle": ang[0] if ang else "90", "pages": page_spec})
    r = COMPRESS_RE.search(low)
    if r and has_pdf:
        return ("pdf_compress", {})
    r = EXTRACT_IMG_RE.search(low)
    if r and has_pdf:
        return ("pdf_extract_images", {})
    r = IMG2PDF_RE.search(low)
    if r and has_img:
        return ("images_to_pdf", {"page": "a4" if re.search(r"\ba4\b", low, re.I) else "auto"})
    r = INFO_RE.search(low)
    if r and has_pdf:
        return ("pdf_info", {})
    r = WCOUNT_RE.search(low)
    if r and kinds:
        return ("word_count", {})
    return None
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
    if tool not in ("reply", "generate_doc", "edit_doc", "append_section", "breakdown", "run_tool"):
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


def _materialize_sources(refs, user_id):
    out = []
    for ref in refs:
        rec = tstore.get_source(ref.get("srcId"), user_id)
        if rec:
            out.append({"name": rec["name"], "kind": rec["kind"], "data": rec["data"], "srcId": ref.get("srcId")})
    return out


def _run_tool_turn(user, session, tool_id, params, sources, tools, say):
    try:
        result = study_tools.run_tool(tool_id, sources, params)
    except ToolError as exc:
        msg = str(exc)
        tools.append({"name": tool_id or "tool", "summary": f"Blocked: {msg[:70]}"})
        for piece in chunk_text(msg):
            yield {"type": "delta", "content": piece}
            say(piece)
        return
    except Exception:
        msg = "That file operation didn't complete cleanly — please retry with a smaller or simpler file."
        tools.append({"name": tool_id or "tool", "summary": "Failed"})
        for piece in chunk_text(msg):
            yield {"type": "delta", "content": piece}
            say(piece)
        return
    collected = []
    for art in result.get("artifacts") or []:
        token = tstore.put_artifact(user.id, art["name"], art.get("mime", ""), art.get("bytes", b""))
        frame = {
            "type": "file",
            "name": art["name"],
            "url": f"/ajax/lazy/file/{token}/",
            "size": len(art.get("bytes", b"")),
        }
        collected.append(frame)
        yield frame
    summary = result.get("text") or result.get("summary") or ""
    for piece in chunk_text(summary or "Done."):
        yield {"type": "delta", "content": piece}
        say(piece)
    tools.append({"name": tool_id, "summary": summary[:90]})
def stream_turn(session, user, user_text, sink, sources=None):
    """Generator: yields SSE-ready dict frames; on completion sets sink['turn']."""
    tools = []
    reply = []

    def say(text):
        reply.append(text)
        return {"type": "delta", "content": text}

    srcs = list(sources or [])
    kinds = sorted({s.get("kind", "") for s in srcs})
    collected_files = []

    quick = _quick_intent(user_text, kinds)
    if quick is not None:
        tool_id, params = quick
        yield {"type": "status", "tool": tool_id, "label": f"Running {tool_id.replace('_', ' ')}…"}
        materialized = _materialize_sources(srcs, user.id)
        for frame in _run_tool_turn(user, session, tool_id, params, materialized, tools, say):
            if frame.get("type") == "file":
                collected_files.append(frame)
            yield frame
        sink["turn"] = {
            "tools": tools,
            "reply": "".join(reply).strip() or "(no output)",
            "doc_updated": False,
            "files": collected_files,
        }
        return

    decision = plan(user, session, user_text)
    yield {"type": "think", "content": decision["think"]}
    tool = decision["tool"]
    args = decision.get("args") or {}

    if tool == "run_tool":
        tid = str(args.get("id") or args.get("tool") or "").strip().lower()
        params = args.get("params") if isinstance(args.get("params"), dict) else {}
        label = (tid.replace("_", " ") or "tool").title()
        yield {"type": "status", "tool": tid or "tools", "label": f"Running {label}…"}
        materialized = _materialize_sources(srcs, user.id)
        for frame in _run_tool_turn(user, session, tid, params, materialized, tools, say):
            if frame.get("type") == "file":
                collected_files.append(frame)
            yield frame
        sink["turn"] = {
            "tools": tools,
            "reply": "".join(reply).strip() or "(no output)",
            "doc_updated": False,
            "files": collected_files,
        }
        return
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
        "files": collected_files,
    }


def persist_turn(session, turn_result):
    now = now_ms()
    assistant = LazyDocMessage.objects.create(
        id=uuid_str(), session=session, role="assistant",
        content=turn_result["reply"][:40000],
        meta=json.dumps({
            "tools": turn_result["tools"],
            "docUpdated": turn_result["doc_updated"],
            "files": turn_result.get("files") or [],
        }, ensure_ascii=False),
        created_at=now,
    )
    session.message_count = LazyDocMessage.objects.filter(session=session).count()
    session.updated_at = now
    session.save(update_fields=["doc_html", "doc_title", "message_count", "updated_at"])
    return assistant