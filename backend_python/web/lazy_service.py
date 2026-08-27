import json
import re

from .lazy_io import strip_tags

LAZY_GENERATE_SYSTEM = """You are Lazy — a document engine inside an agentic chat for Nepali NEB students. Produce print-ready A4 document HTML.

Return ONLY a single JSON object (no markdown fences):
{
  "title": "Document title, 4-8 words",
  "html": "<h1>Title</h1><h2>Section</h2><p>...</p> ..."
}

HTML rules:
- Only these tags: <h1> <h2> <h3> <p> <ul> <ol> <li> <blockquote> <strong> <em> <br> <table> <thead> <tbody> <tr> <th> <td>.
- First element is the <h1> title, then 3-7 sections each opening with <h2>.
- 60-140 words per section; <strong> on key terms; one <blockquote> definition when natural.
- assignment: thesis → claims → evidence → counterpoint → conclusion (+ references placeholder).
- report: executive summary → method → findings → analysis → recommendations.
- resume: header → summary → experience → education → skills (compact).
- Length ∝ pages (1 page ≈ 450 words). Formal register, no filler. Raw JSON only."""

LAZY_EDIT_SYSTEM = """You are Lazy — you revise an existing document per an instruction.

Return ONLY JSON:
{ "title": "updated document title or empty to keep", "html": "<full revised document html>", "summary": "one line: what changed" }

Rules:
- Return the COMPLETE revised document (every section), same allowed tags as generation.
- Apply the instruction faithfully; preserve everything not affected; keep academic tone.
- Raw JSON only."""

LAZY_SECTION_SYSTEM = """You write ONE new section appended to an existing document.
Return ONLY JSON: { "heading": "Section heading", "html": "<p>...</p>" }
60-140 words, formal, same style as the surrounding document. Raw JSON only."""

LAZY_REPLY_SYSTEM = """You are Lazy, a warm, sharp writing assistant chatting with a Nepali student about the document you co-write.
Reply in tight markdown (short paragraphs, **bold** key terms, bullets when listing). Max ~180 words unless asked for depth.
You can reference the working document shown in context. Never invent that you edited it — say what you *can* do: draft, revise, extend, restructure, export."""

LAZY_PLANNER_SYSTEM = """You are the planner for Lazy, an agentic document chat. Pick exactly ONE next action.

Return ONLY compact JSON:
{"think": "one short line of reasoning", "tool": "...", "args": {...}}

Tools:
- reply            {"text": "what to tell the user"}          — pure conversation / questions / feedback with no document change
- generate_doc     {"topic": "...", "type": "assignment|report|resume|essay", "pages": 1-4}   — create or fully replace the working document
- edit_doc         {"instruction": "how to change it"}         — revise the existing document (tone, length, section fixes, restructuring)
- append_section   {"brief": "what this section covers"}       — add one new section at the end
- breakdown        {}                                          — turn the current document into a markdown task checklist in chat
- run_tool         {"id": "<tool id>", "params": {...}}        — operate on ATTACHED files with the tools listed below

Available tools for run_tool (id → params):
- pdf_to_docx {}          — convert an attached PDF into an editable Word (.docx), layout preserved
- pdf_merge {}            — merge all attached PDFs into one
- pdf_extract_pages {"pages": "2-5,8"}
- pdf_split {"every": 5}  or {"ranges": "1-10,11-20"}
- pdf_rotate {"angle": "90|180|270", "pages": "" for all}
- pdf_compress {}
- pdf_info {}
- pdf_extract_images {}
- images_to_pdf {"page": "auto|a4"}
- word_count {}           — words/chars/read-time of attached doc or pasted text

Decision rules:
- If the user asks to convert/merge/split/extract/rotate/compress attached files or asks about them → run_tool with the right id.
- If there is NO existing document and the user asks to write/draft/create anything → generate_doc.
- If a document EXISTS and the user asks to improve/shorten/expand/reword/restructure/fix → edit_doc.
- If they want more content added without touching the rest → append_section.
- If they ask for a plan/checklist/steps from the doc → breakdown.
- Greetings, meta questions, explanations, feedback loops → reply.
- args must be filled concretely from the conversation. Raw JSON only."""


def parse_llm_json(raw):
    raw = (raw or "").strip()
    if not raw:
        return None
    if "```" in raw:
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw, re.I)
        if m:
            raw = m.group(1).strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if 0 <= start < end:
        raw = raw[start:end + 1]
    try:
        return json.loads(raw)
    except Exception:
        return None


def _resolve_provider(user):
    from api.llm.credentials import resolve
    for slug in ("agnes", "openai", "gemini", "deepseek", "gmi", "empero"):
        try:
            r = resolve(user, slug)
            if r and r.api_key:
                return r
        except Exception:
            continue
    return None


def llm_chat(user, system, prompt, max_tokens=1600, temperature=0.45, timeout=75):
    r = _resolve_provider(user)
    if not r:
        return None
    try:
        from api.llm.client import chat
        result = chat(
            format=r.format, base_url=r.base_url, api_key=r.api_key, model=r.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=r.slug,
        )
        text = (result.text or "").strip()
        return text or None
    except Exception:
        return None


def llm_chat_stream(user, system, prompt, max_tokens=1200, temperature=0.6, timeout=90):
    r = _resolve_provider(user)
    if not r:
        return None

    def gen():
        from api.llm.client import chat_stream
        yield from chat_stream(
            format=r.format, base_url=r.base_url, api_key=r.api_key, model=r.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=r.slug,
        )
    return gen()


def fallback_doc(topic, pages=1, doc_type="assignment"):
    topic = (topic or "Untitled").strip()[:80]
    title = topic.title() if len(topic.split()) <= 6 else topic.capitalize()
    paras = max(3, min(6, int(pages or 1) + 2))
    html = f"<h1>{title}</h1>"
    for i in range(paras):
        html += f"<h2>Section {i + 1}</h2><p><strong>{topic}</strong> — offline draft placeholder for {doc_type}. A free model slot was unavailable, so this skeleton keeps you moving; ask again to regenerate with full content.</p>"
        if i == 0:
            html += "<blockquote>A crisp defining sentence for this topic.</blockquote>"
    outline = [{"heading": f"Section {i + 1}", "bullets": []} for i in range(paras)]
    return {"title": title, "html": html, "outline": outline}


def generate_doc(user, topic, pages=1, doc_type="assignment", instructions=""):
    pages = max(1, min(4, int(pages or 1)))
    doc_type = (doc_type or "assignment").lower()
    if doc_type not in ("assignment", "report", "resume", "essay"):
        doc_type = "assignment"
    prompt = f"Topic: {topic}\nType: {doc_type}\nPages: {pages}\n"
    if instructions:
        prompt += f"Extra instructions: {instructions[:600]}\n"
    prompt += "Generate now."
    raw = llm_chat(user, LAZY_GENERATE_SYSTEM, prompt, max_tokens=3400 if pages >= 3 else 2400)
    data = parse_llm_json(raw) if raw else None
    if not data or not data.get("html"):
        fb = fallback_doc(topic, pages, doc_type)
        fb["provider"] = "fallback"
        return fb
    html = str(data["html"])[:80000]
    title = str(data.get("title") or topic)[:120]
    if not re.search(r"<h1", html, re.I):
        html = f"<h1>{title}</h1>" + html
    return {"title": title, "html": html, "provider": "llm"}


def edit_doc(user, doc_html, instruction):
    plain = strip_tags(doc_html)[:9000]
    prompt = f"Instruction: {instruction[:600]}\n\nCurrent document:\n{doc_html[:40000]}\n\nPlain-text digest:\n{plain}"
    raw = llm_chat(user, LAZY_EDIT_SYSTEM, prompt, max_tokens=3400)
    data = parse_llm_json(raw) if raw else None
    if not data or not data.get("html"):
        return None
    html = str(data["html"])[:80000]
    title = str(data.get("title") or "")[:120]
    summary = str(data.get("summary") or instruction)[:200]
    return {"html": html, "title": title, "summary": summary}


def append_section(user, doc_html, brief):
    prompt = f"New section brief: {brief[:500]}\n\nExisting document (for style continuity):\n{doc_html[:30000]}"
    raw = llm_chat(user, LAZY_SECTION_SYSTEM, prompt, max_tokens=900)
    data = parse_llm_json(raw) if raw else None
    if not data or not data.get("html"):
        return None
    heading = str(data.get("heading") or brief)[:100]
    body = str(data["html"])[:12000]
    return {"heading": heading, "body": body}


def breakdown_doc(user, doc_html):
    plain = strip_tags(doc_html)[:8000]
    prompt = (
        "Turn this document into a concise actionable checklist the student can follow.\n"
        "Markdown only: a bold intro line, then '- [ ] task' items grouped under '### ' headings (3-5 groups, 3-5 tasks each).\n\n"
        f"Document:\n{plain}"
    )
    raw = llm_chat(user, "You compress documents into actionable study checklists. Output markdown only.", prompt, max_tokens=1100, temperature=0.35)
    if raw:
        cleaned = re.sub(r"^```(?:markdown)?|```$", "", raw.strip(), flags=re.I | re.M).strip()
        if cleaned:
            return cleaned[:8000]
    heads = re.findall(r"<h2[^>]*>(.*?)</h2>", doc_html or "", re.I)
    lines = ["**Checklist** (offline)", ""]
    for h in heads[:6]:
        h = strip_tags(h)[:70]
        lines.append(f"### {h}")
        lines.append("- [ ] Review this section")
        lines.append("- [ ] Add evidence/examples")
        lines.append("")
    return "\n".join(lines)


def stream_reply(user, prompt, max_tokens=1000):
    gen = llm_chat_stream(user, LAZY_REPLY_SYSTEM, prompt, max_tokens=max_tokens)

    def wrapped():
        if gen is None:
            pieces = ["I'm running in offline mode right now — I can still sketch outlines and checklists locally. Try again shortly for full drafting."]
            for piece in pieces:
                yield {"type": "text", "content": piece}
            yield {"type": "done", "model": "offline"}
            return
        got_any = False
        try:
            for chunk in gen:
                if chunk.get("type") == "text":
                    got_any = True
                elif chunk.get("type") == "done":
                    continue
                yield chunk
            if not got_any:
                yield {"type": "text", "content": "The model returned nothing — try rephrasing."}
                yield {"type": "done", "model": "empty"}
        except Exception as exc:
            yield {"type": "text", "content": f"\n\n_(stream interrupted: {str(exc)[:80]})_"}
            yield {"type": "done", "model": "error"}

    return wrapped()
