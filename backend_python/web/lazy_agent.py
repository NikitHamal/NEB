import concurrent.futures
import json
import re

from api.models import LazyDocMessage
from api.utils import now_ms, uuid_str
from . import toolstore as tstore
from . import study_tools
from .study_tools import ToolError
from .lazy_io import strip_tags
from .lazy_service import (
    LAZY_GENERATE_SYSTEM, LAZY_PLANNER_SYSTEM, append_section, breakdown_doc, edit_doc,
    generate_doc, llm_chat, parse_llm_json, stream_generate_doc, stream_edit_doc, stream_reply,
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
    r = INFO_RE.search(low)
    if r and has_pdf:
        return ("pdf_info", {})
    r = EXTRACT_IMG_RE.search(low)
    if r and has_pdf:
        return ("pdf_extract_images", {})
    r = IMG2PDF_RE.search(low)
    if r and has_img:
        return ("images_to_pdf", {})
    r = WCOUNT_RE.search(low)
    if r and kinds:
        return ("word_count", {})
    return None


def plan(user, session, user_text, model_key="neby-pro"):
    history, doc_state = build_context(session)
    prompt = (
        f"{doc_state}\n\nRECENT CONVERSATION:\n{history or '(empty)'}\n\n"
        f"NEW USER MESSAGE:\n{user_text[:1500]}\n\nPick exactly one tool. JSON only."
    )
    from .lazy_service import get_lazy_prompts
    planner_system = get_lazy_prompts()["planner"]
    raw = None
    try:
        from api import geminiweb_proxy
        res, err = geminiweb_proxy.simple_chat(prompt, system_prompt=planner_system, model="geminiweb/gemini-flash-lite", max_tokens=320)
        if res and res.strip():
            raw = res.strip()
    except Exception:
        pass

    if not raw:
        raw = llm_chat(user, planner_system, prompt, max_tokens=320, temperature=0.2, timeout=10, model_key=model_key)

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
    if tool not in ("reply", "generate_doc", "edit_doc", "append_section", "breakdown", "run_tool", "ask_clarification", "parallel_subagents"):
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


def build_dynamic_clarification(user_text):
    low = user_text.lower()
    questions = []

    if any(k in low for k in ("physics", "chemistry", "math", "numerical", "problem", "calculate", "formula", "induction", "optics", "mechanics")):
        questions.append({
            "q": "What balance of theory and numericals do you want?",
            "type": "radio",
            "options": [
                "Theory + 5 Standard Numericals (NEB Exam format)",
                "Complete Chapter Coverage (Derivations + 10 Numericals)",
                "Formula Sheet & Quick Practice (3 Numericals)"
            ]
        })
        questions.append({
            "q": "Include step-by-step numerical solutions?",
            "type": "radio",
            "options": [
                "Full step-by-step solutions with SI units",
                "Questions with final numerical answer keys only",
                "Practice sheet (questions only)"
            ]
        })
    elif any(k in low for k in ("lab", "experiment", "practical", "report")):
        questions.append({
            "q": "What report format do you need?",
            "type": "radio",
            "options": [
                "Full Formal Report (Objective, Apparatus, Theory, Observations, Conclusion)",
                "Standard 2-Page Lab Record Sheet",
                "Short Summary & Viva Guide"
            ]
        })
        questions.append({
            "q": "Include sample observation table with readings?",
            "type": "radio",
            "options": [
                "Yes, realistic sample readings & calculation table",
                "Blank observation table with column headers",
                "Procedure and theoretical formulas only"
            ]
        })
    elif any(k in low for k in ("essay", "article", "speech", "opinion")):
        questions.append({
            "q": "What length and structure do you prefer?",
            "type": "radio",
            "options": [
                "Academic Essay (approx. 500-700 words, formal)",
                "Extended Analysis (approx. 1000 words with counterarguments)",
                "Concise Opinion Piece (approx. 350 words)"
            ]
        })
    elif any(k in low for k in ("resume", "cv", "bio")):
        questions.append({
            "q": "Which layout fits your profile best?",
            "type": "radio",
            "options": [
                "Student / Fresh Graduate Entry-Level Resume",
                "Academic & Scholarship CV",
                "Technical & Skills-Focused Resume"
            ]
        })
    else:
        questions.append({
            "q": "What depth should this document have?",
            "type": "radio",
            "options": [
                "Standard 2-Page Assignment (Core concepts & examples)",
                "Comprehensive Multi-Section In-Depth Document",
                "Concise 1-Page Summary Sheet"
            ]
        })
        questions.append({
            "q": "Target academic curriculum standard?",
            "type": "radio",
            "options": [
                "Grade 11/12 NEB Curriculum Standard",
                "College / Bachelor Level Submission",
                "General Academic Revision"
            ]
        })
    return questions


def _run_subagent_task(user, task_name, task_goal, topic_context, model_key="neby-pro"):
    sub_system = (
        "You are an expert subagent assistant specialized in deep curriculum research, mathematical problem solving, "
        "and section drafting for NEB students. Provide a crisp, high-scoring, rigorous output."
    )
    prompt = f"TASK: {task_name}\nGOAL: {task_goal}\n\nTOPIC CONTEXT:\n{topic_context[:1600]}\n\nExecute the subtask thoroughly now:"
    output = llm_chat(user, sub_system, prompt, max_tokens=1500, temperature=0.3, model_key=model_key)
    return {
        "name": task_name,
        "goal": task_goal,
        "result": output or "(Completed)"
    }


def stream_turn(session, user, user_text, sink, sources=None, model_key="neby-pro"):
    """Generator: yields SSE-ready dict frames; on completion sets sink['turn']."""
    tools = []
    reply = []
    used_model = ""

    def say(text):
        reply.append(text)
        return {"type": "delta", "content": text}

    srcs = list(sources or [])
    kinds = sorted({s.get("kind", "") for s in srcs})
    collected_files = []
    steps = []

    quick = _quick_intent(user_text, kinds)
    if quick is not None:
        tool_id, params = quick
        lbl = f"Running {tool_id.replace('_', ' ')}…"
        steps.append({"text": lbl, "done": True})
        yield {"type": "status", "tool": tool_id, "label": lbl}
        materialized = _materialize_sources(srcs, user.id)
        for frame in _run_tool_turn(user, session, tool_id, params, materialized, tools, say):
            if frame.get("type") == "file":
                collected_files.append(frame)
            yield frame
        sink["turn"] = {
            "think": None,
            "steps": steps,
            "tools": tools,
            "reply": "".join(reply).strip() or "(no output)",
            "doc_updated": False,
            "files": collected_files,
            "model": used_model or f"tool/{tool_id}",
        }
        return

    yield {"type": "status", "tool": "planning", "label": "Planning..."}
    decision = plan(user, session, user_text, model_key=model_key)
    if decision.get("think"):
        steps.append({"text": decision["think"], "done": True})
        yield {"type": "think", "content": decision["think"]}
    tool = decision["tool"]
    args = decision.get("args") or {}

    if tool == "run_tool":
        tid = str(args.get("id") or args.get("tool") or "").strip().lower()
        params = args.get("params") if isinstance(args.get("params"), dict) else {}
        label = (tid.replace("_", " ") or "tool").title()
        lbl = f"Running {label}…"
        steps.append({"text": lbl, "done": True})
        yield {"type": "status", "tool": tid or "tools", "label": lbl}
        materialized = _materialize_sources(srcs, user.id)
        for frame in _run_tool_turn(user, session, tid, params, materialized, tools, say):
            if frame.get("type") == "file":
                collected_files.append(frame)
            yield frame

    elif tool == "ask_clarification":
        clarification_title = args.get("title") or "Before I draft the document, confirm a few details:"
        questions = args.get("questions") or build_dynamic_clarification(user_text)
        tools.append({"name": "ask_clarification", "summary": f"Clarified {len(questions)} structural details"})
        yield say("Before I draft the assignment, confirm a few details.")
        yield {
            "type": "approval",
            "title": clarification_title,
            "questions": questions,
            "originalPrompt": user_text
        }

    elif tool == "parallel_subagents" or (tool == "generate_doc" and ("subagent" in user_text.lower() or "parallel" in user_text.lower() or "comprehensive" in user_text.lower())):
        tasks = args.get("tasks") if isinstance(args.get("tasks"), list) and args.get("tasks") else [
            {"name": "Theory & Derivations", "goal": "Analyze and outline fundamental concepts, laws, and step-by-step derivations"},
            {"name": "Numerical Problems & Models", "goal": "Formulate 5 rigorous numerical problems with SI units, given values, and full solutions"},
            {"name": "Exam Tips & Viva Checkpoints", "goal": "Highlight common misconceptions, high-scoring points, and board exam notes"}
        ]

        lbl = f"Spawning {len(tasks)} parallel subagents…"
        steps.append({"text": lbl, "done": False})
        yield {"type": "status", "tool": "parallel_subagents", "label": lbl}

        sub_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(tasks))) as executor:
            future_to_task = {
                executor.submit(_run_subagent_task, user, t.get("name", "Subtask"), t.get("goal", ""), user_text, model_key): t
                for t in tasks
            }
            for future in concurrent.futures.as_completed(future_to_task):
                t_spec = future_to_task[future]
                try:
                    res = future.result()
                    sub_results.append(res)
                    t_name = res["name"]
                    t_lbl = f"Subagent completed: {t_name}"
                    steps.append({"text": t_lbl, "done": True})
                    yield {"type": "status", "tool": "subagent", "label": t_lbl}
                    tools.append({"name": t_name, "action": f"Subagent: {t_name}", "arg": t_spec.get("goal") or "Executed", "summary": f"Completed ({len(res['result'].split())} words)"})
                except Exception:
                    sub_results.append({"name": t_spec.get("name", "Subtask"), "result": ""})

        synthesis_prompt = (
            f"Synthesize the findings of {len(sub_results)} parallel research subagents into a unified, print-ready document HTML.\n"
            f"TOPIC: {user_text}\n\nSUBAGENT FINDINGS:\n" +
            "\n\n".join([f"### {r['name']}\n{r['result']}" for r in sub_results])
        )
        raw_doc = llm_chat(user, LAZY_GENERATE_SYSTEM, synthesis_prompt, max_tokens=3500, model_key=model_key)
        data = parse_llm_json(raw_doc) if raw_doc else None
        if data and data.get("html"):
            session.doc_html = str(data["html"])[:80000]
            session.doc_title = str(data.get("title") or user_text[:60])
            tools.append({"name": "synthesis", "action": "Synthesize document", "arg": session.doc_title, "summary": f"Unified master document: {session.doc_title}"})
            yield {"type": "doc", "title": session.doc_title, "html": session.doc_html}
            yield say(f"Drafted **{session.doc_title}** using {len(tasks)} parallel subagents. The complete document is ready in the preview panel.")
        else:
            result = generate_doc(user, user_text, pages=2, model_key=model_key)
            session.doc_html = result["html"]
            session.doc_title = result["title"]
            yield {"type": "doc", "title": result["title"], "html": result["html"]}
            yield say(f"Drafted **{result['title']}** with parallel subagent synthesis.")

    elif tool == "generate_doc":
        topic = str(args.get("topic") or user_text)[:300]
        pages = args.get("pages") or 2
        try:
            pages = max(1, min(4, int(pages)))
        except Exception:
            pages = 2
        doc_type = str(args.get("type") or "assignment")[:20]
        lbl = f"Drafting {doc_type} — {topic[:60]}"
        steps.append({"text": lbl, "done": True})
        yield {"type": "status", "tool": "generate_doc", "label": lbl}
        doc_result = None
        for frame in stream_generate_doc(user, topic, pages=pages, doc_type=doc_type, model_key=model_key):
            if frame.get("type") == "doc_ready":
                doc_result = frame
                if frame.get("model"):
                    used_model = frame.get("model") or used_model
            elif frame.get("type") == "model":
                used_model = frame.get("model") or used_model
                yield frame
            else:
                yield frame
        if doc_result:
            session.doc_html = doc_result["html"]
            session.doc_title = doc_result["title"]
            tools.append({"name": "generate_doc", "summary": f"Drafted '{doc_result['title'][:60]}' ({pages}p)"})
            yield {"type": "doc", "title": doc_result["title"], "html": doc_result["html"]}
            text_out = f"Drafted **{doc_result['title']}** — it's open in the document panel. Tell me what to change."
            for piece in chunk_text(text_out, size=20):
                yield say(piece)
        else:
            yield say("Generation failed — please try again.")

    elif tool == "edit_doc":
        instruction = str(args.get("instruction") or user_text)[:600]
        if not session.doc_html:
            lbl = "Nothing to edit yet — drafting instead"
            steps.append({"text": lbl, "done": True})
            yield {"type": "status", "tool": "generate_doc", "label": lbl}
            doc_result = None
            for frame in stream_generate_doc(user, user_text[:200], pages=2, model_key=model_key):
                if frame.get("type") == "doc_ready":
                    doc_result = frame
                else:
                    yield frame
            if doc_result:
                session.doc_html = doc_result["html"]
                session.doc_title = doc_result["title"]
                tools.append({"name": "generate_doc", "summary": f"No draft existed — created '{doc_result['title'][:60]}'"})
                yield {"type": "doc", "title": doc_result["title"], "html": doc_result["html"]}
                text_out = f"There was nothing to edit yet, so I drafted **{doc_result['title']}** instead."
                for piece in chunk_text(text_out, size=20):
                    yield say(piece)
        else:
            lbl = f"Revising — {instruction[:60]}"
            steps.append({"text": lbl, "done": True})
            yield {"type": "status", "tool": "edit_doc", "label": lbl}
            edit_result = None
            for frame in stream_edit_doc(user, session.doc_html, instruction, model_key=model_key):
                if frame.get("type") == "edit_ready":
                    edit_result = frame
                    if frame.get("model"):
                        used_model = frame.get("model") or used_model
                elif frame.get("type") == "model":
                    used_model = frame.get("model") or used_model
                    yield frame
                else:
                    yield frame
            if edit_result and edit_result.get("html"):
                session.doc_html = edit_result["html"]
                if edit_result.get("title"):
                    session.doc_title = edit_result["title"]
                tools.append({"name": "edit_doc", "summary": edit_result.get("summary") or instruction[:80]})
                yield {"type": "doc", "title": session.doc_title, "html": session.doc_html}
                text_out = edit_result.get("summary") or "Document revised."
                for piece in chunk_text(text_out, size=20):
                    yield say(piece)
            else:
                tools.append({"name": "edit_doc", "summary": "Revision failed — previous version kept"})
                text_out = "I couldn't apply that revision cleanly, so your previous version is untouched. Try a narrower instruction."
                for piece in chunk_text(text_out, size=20):
                    yield say(piece)

    elif tool == "append_section":
        brief = str(args.get("brief") or user_text)[:400]
        if not session.doc_html:
            lbl = "No document yet — drafting first"
            steps.append({"text": lbl, "done": True})
            yield {"type": "status", "tool": "generate_doc", "label": lbl}
            result = generate_doc(user, brief[:200], pages=2, model_key=model_key)
            session.doc_html = result["html"]
            session.doc_title = result["title"]
            tools.append({"name": "generate_doc", "summary": f"Created base document '{result['title'][:50]}'"})
            yield {"type": "doc", "title": result["title"], "html": result["html"]}
            yield say(f"No document existed, so I drafted **{result['title']}** first.")
        else:
            lbl = f"Writing section — {brief[:60]}"
            steps.append({"text": lbl, "done": True})
            yield {"type": "status", "tool": "append_section", "label": lbl}
            result = append_section(user, session.doc_html, brief, model_key=model_key)
            if result:
                block = f"<h2>{result['heading']}</h2>" + result["body"]
                session.doc_html += block
                tools.append({"name": "append_section", "summary": f"Added section '{result['heading'][:60]}'"})
                yield {"type": "doc", "title": session.doc_title, "html": session.doc_html}
                yield say(f"Added **{result['heading']}** to the end of the document.")
            else:
                tools.append({"name": "append_section", "summary": "Section generation failed"})
                yield say("The new section didn't come through — try again with a slightly different brief.")

    elif tool == "breakdown":
        lbl = "Building checklist from the document"
        steps.append({"text": lbl, "done": True})
        yield {"type": "status", "tool": "breakdown", "label": lbl}
        if session.doc_html:
            md = breakdown_doc(user, session.doc_html, model_key=model_key)
            tools.append({"name": "breakdown", "summary": "Generated task checklist"})
            for piece in chunk_text(md):
                yield say(piece)
        else:
            yield say("There's no document to break down yet — ask me to draft one first.")

    else:
        history, doc_state = build_context(session)
        prompt = f"{doc_state}\n\nCONVERSATION:\n{history}\n\nReply to: {user_text[:1200]}"
        got_any = False
        for chunk in stream_reply(user, prompt, model_key=model_key):
            ctype = chunk.get("type")
            content = chunk.get("content") or ""
            if ctype == "think" and content:
                if not decision.get("think"):
                    decision["think"] = content
                else:
                    decision["think"] += content
                yield {"type": "think", "content": content}
            elif ctype == "model":
                used_model = chunk.get("model") or chunk.get("content") or used_model
                yield chunk
            elif (ctype in ("delta", "text")) and content:
                got_any = True
                reply.append(content)
                yield {"type": "delta", "content": content}
            elif ctype == "done":
                if chunk.get("model"):
                    used_model = chunk.get("model") or used_model
                break
        if not got_any:
            yield say("Here's where we stand — tell me what to draft or revise next.")

    sink["turn"] = {
        "think": decision.get("think"),
        "steps": steps,
        "tools": tools,
        "reply": "".join(reply).strip() or "(no output)",
        "doc_updated": bool(session.doc_html and any(t["name"] in ("generate_doc", "edit_doc", "append_section") for t in tools)),
        "files": collected_files,
        "model": used_model or "qwencloud/qwen3.8-max",
    }


def persist_turn(session, turn_result):
    now = now_ms()
    assistant = LazyDocMessage.objects.create(
        id=uuid_str(), session=session, role="assistant",
        content=turn_result["reply"][:40000],
        meta=json.dumps({
            "think": turn_result.get("think"),
            "steps": turn_result.get("steps") or [],
            "tools": turn_result["tools"],
            "docUpdated": turn_result["doc_updated"],
            "docTitle": session.doc_title or "",
            "files": turn_result.get("files") or [],
            "model": turn_result.get("model") or "",
        }, ensure_ascii=False),
        created_at=now,
    )
    session.message_count = LazyDocMessage.objects.filter(session=session).count()
    session.updated_at = now
    session.save(update_fields=["doc_html", "doc_title", "message_count", "updated_at"])
    return assistant