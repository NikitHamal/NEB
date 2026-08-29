import json
import re

from .lazy_io import strip_tags

LAZY_GENERATE_SYSTEM = """You are Lazy — an autonomous, professional document drafting engine for students, job applicants, and researchers.
You produce purely formal, print-ready documents (assignments, resumes, CVs, lab reports, research papers, essays).

STRICT DIRECTIVES:
- Return ONLY a single raw JSON object:
{
  "title": "Clear Document Title",
  "html": "<h1>...</h1>..."
}
- NEVER include conversational greetings, chit-chat, or pleasantries (e.g. NEVER output "Namaste sathi", "Hello", "Sure, here is...", "Excited for you...", "Hope this helps").
- NEVER include meta-commentary, introductory notes, or closing sign-offs in the HTML.
- The HTML content MUST be ONLY the pure professional document itself.

HTML Formatting Rules:
- Only standard semantic tags: <h1>, <h2>, <h3>, <h4>, <p>, <ul>, <ol>, <li>, <blockquote>, <strong>, <em>, <table>, <thead>, <tbody>, <tr>, <th>, <td>, <br>, <code>, <pre>.
- Structure with clear hierarchy: <h1> title at top, followed by well-structured <h2> sections and <h3> sub-sections.
- For Science & Math: Complete derivations, exact formulas, and step-by-step solved numerical problems.
- For Resumes & CVs: Clean contact header, executive summary, education, technical skills, projects, experience.
- Raw JSON only without markdown backticks."""


def clean_doc_html(html):
    """Sanitizes generated document HTML to strip any accidental conversational greetings or banter."""
    if not html:
        return ""
    cleaned = str(html).strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:html|json)?\s*\n?|```$", "", cleaned, flags=re.I).strip()

    # Strip any conversational opening paragraph such as "Namaste sathi! ...", "Hello! Here is...", "Sure, here's a..."
    patterns = [
        r"^(?:<p[^>]*>)?\s*(?:namaste(?:\s+sathi)?|hello|hi|hey|sure|excited\s+for\s+you|here\s+is\s+(?:a|the)?|here\'s\s+(?:a|the)?)[^\n<]{0,250}(?:</p>|\n+)",
        r"(?:<p[^>]*>)?\s*(?:hope\s+this\s+helps|let\s+me\s+know\s+if\s+you\s+need|feel\s+free\s+to\s+ask)[^\n<]{0,200}(?:</p>)?\s*$",
    ]
    for p in patterns:
        cleaned = re.sub(p, "", cleaned, flags=re.I | re.M).strip()
    return cleaned

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

LAZY_REPLY_SYSTEM = """You are Lazy, a focused, professional AI writing partner.
Reply directly, clearly, and concisely in markdown (short paragraphs, **bold** key terms, clean bullet lists). Max ~160 words unless in-depth analysis is requested.
NEVER start with greetings, pleasantries, or phrases like "Namaste!", "Hello!", or "Sure!".
You can reference the working document shown in context. Never invent that you edited it — state what you can do: draft, revise, extend, restructure, export."""

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


def _get_admin_bot_config(model_key="neby-pro"):
    """Fetch admin BotConfig for Neby Pro, Fast, or general bot."""
    from api.models import BotConfig
    names = []
    if model_key == "neby-pro":
        names = ["neby_pro", "neby-pro", "neby", "lazy_pro", "lazy"]
    elif model_key == "neby-fast":
        names = ["neby_fast", "neby-fast", "fast", "lazy_fast"]

    for name in names:
        cfg = BotConfig.objects.filter(bot_username__iexact=name, enabled=True).first()
        if cfg:
            return cfg

def get_lazy_prompts():
    """Retrieve custom admin-configured system prompts with fallback to defaults."""
    cfg = _get_admin_bot_config(model_key="neby-pro")
    prompts = {
        "generate": LAZY_GENERATE_SYSTEM,
        "edit": LAZY_EDIT_SYSTEM,
        "section": LAZY_SECTION_SYSTEM,
        "reply": LAZY_REPLY_SYSTEM,
        "planner": LAZY_PLANNER_SYSTEM,
    }
    if cfg and cfg.system_prompt:
        try:
            custom = json.loads(cfg.system_prompt)
            if isinstance(custom, dict):
                for k, v in custom.items():
                    if k in prompts and isinstance(v, str) and v.strip():
                        prompts[k] = v.strip()
        except Exception:
            if cfg.system_prompt.strip() and not cfg.system_prompt.strip().startswith("{"):
                prompts["generate"] = cfg.system_prompt.strip()
    return prompts


def llm_chat(user, system, prompt, max_tokens=1600, temperature=0.45, timeout=75, model_key="neby-pro"):
    from api.neby import call_ai_api
    from api.models import BotConfig

    # 1. Check if an Admin has configured a specific BotConfig for this mode (e.g. via /admin/bots/)
    bot_cfg = _get_admin_bot_config(model_key=model_key)
    if bot_cfg:
        try:
            res = call_ai_api(system, prompt, config=bot_cfg)
            if res and res.strip():
                return res.strip()
        except Exception:
            pass

    # 2. Check if user has personal BYOK credentials configured
    r = _resolve_provider(user)
    if r:
        try:
            from api.llm.client import chat
            result = chat(
                format=r.format, base_url=r.base_url, api_key=r.api_key, model=r.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=r.slug,
            )
            text = (result.text or "").strip()
            if text:
                return text
        except Exception:
            pass

    # 3. Dynamic default routing based on mode if no explicit bot config was found or succeeded
    if model_key == "neby-pro" or not model_key:
        pro_cfg = BotConfig(
            provider="qwen", model="qwen3.8-max",
            fallback_chain='[{"provider": "inception", "model": "mercury-2"}, {"provider": "k2think", "model": "MBZUAI-IFM/K2-Think-v2"}, {"provider": "geminiweb", "model": "geminiweb/gemini-flash-lite"}, {"provider": "longcat", "model": "longcat/LongCat-2.0"}, {"provider": "egov", "model": "AI1"}]'
        )
        try:
            res = call_ai_api(system, prompt, config=pro_cfg)
            if res and res.strip():
                return res.strip()
        except Exception:
            pass
    elif model_key == "neby-fast":
        fast_cfg = BotConfig(
            provider="geminiweb", model="geminiweb/gemini-flash-lite",
            fallback_chain='[{"provider": "longcat", "model": "longcat/LongCat-2.0"}, {"provider": "egov", "model": "AI1"}, {"provider": "deepai", "model": "standard"}]'
        )
        try:
            res = call_ai_api(system, prompt, config=fast_cfg)
            if res and res.strip():
                return res.strip()
        except Exception:
            pass

    # 4. Universal safety fallback via call_ai_api
    try:
        res = call_ai_api(system, prompt)
        if res and res.strip():
            return res.strip()
    except Exception:
        pass

    return None


def stream_proxy_chat(system, prompt, model_key="neby-pro"):
    """Directly streams thoughts and delta tokens from community proxies without blocking."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    PROVIDERS_WITH_INTERNAL_SEARCH = {"geminiweb", "longcat", "inception", "poolside", "qwen", "gmi"}

    if model_key == "neby-fast":
        proxies_to_try = [
            ("qwenfast", "qwen3.8-27b", {}),
            ("geminiweb", "geminiweb/gemini-flash-lite", {}),
            ("longcat", "longcat/LongCat-2.0", {}),
            ("tryingopen", "qwen/qwen3.8-27b", {"effort": "quick"}),
            ("egov", "AI1", {}),
            ("deepai", "standard", {}),
        ]
    else:  # neby-pro
        proxies_to_try = [
            ("geminiweb", "geminiweb/gemini-flash-lite", {}),
            ("qwenfast", "qwen3.8-27b", {}),
            ("tryingopen", "qwen/qwen3.8-27b", {"effort": "deep"}),
            ("inception", "mercury-2", {"reasoning_effort": "high"}),
            ("k2think", "MBZUAI-IFM/K2-Think-v2", {}),
            ("longcat", "longcat/LongCat-2.0", {}),
            ("egov", "AI1", {}),
            ("deepai", "standard", {}),
        ]

    # Pre-compute external search augmentation for providers WITHOUT internal search
    external_search_ctx = ""
    external_search_results = []
    try:
        from api.web_search import web_search, format_search_context, needs_search
        import re as _re
        if needs_search(prompt):
            raw_q = (prompt or "").strip()
            q = _re.sub(r'(?i)\b(search the web|please search|web search|browse|look up|on the web|from the web)\b', '', raw_q)
            q = _re.sub(r'(?i)^(what is|what\'s|who is|when is|where is|how to|what are|who won|tell me|give me|show me)\s+', '', q)
            q = _re.sub(r'\s*\?\s*$', '', q)
            q = " ".join(q.split())
            if len(q.split()) > 8:
                stop = {"what","is","the","a","an","is","are","was","were","be","been","being","have","has","had","do","does","did","will","would","should","could","can","may","might","must","shall","to","of","and","or","but","if","then","else","when","where","why","how","for","in","on","at","with","about","latest","current","today","please"}
                toks = _re.findall(r'\w+', q)
                kept = []
                for t in toks:
                    low = t.lower()
                    if low in stop and not t.isdigit():
                        continue
                    if len(t) < 2 and not t.isdigit():
                        continue
                    kept.append(t)
                    if len(kept) >= 10:
                        break
                if kept:
                    q = " ".join(kept)
            q = q[:120].strip()
            if q:
                external_search_results = web_search(q, num=3)
                if external_search_results:
                    external_search_ctx = format_search_context(external_search_results)
    except Exception:
        external_search_ctx = ""
        external_search_results = []

    search_yielded = False
    for slug, model, extra in proxies_to_try:
        try:
            got_any = False
            # For providers WITHOUT internal web search, inject our free search (Exa→DDG→Bing) if needed.
            # Providers WITH internal search (geminiweb, longcat, inception, etc.) use their own — no prompt injection.
            use_messages = messages
            use_prompt = prompt
            use_system = system
            if external_search_ctx and slug not in PROVIDERS_WITH_INTERNAL_SEARCH:
                if not search_yielded:
                    yield {"type": "search", "content": external_search_ctx, "results": external_search_results}
                    search_yielded = True
                augmented = f"{prompt}\n\n{external_search_ctx}\n\nUse the search results above if relevant, cite sources as [1] [2]."
                use_messages = [{"role": "system", "content": system}, {"role": "user", "content": augmented}]
                use_prompt = augmented
            if slug == "qwenfast":
                from api import qwenfast_proxy
                for chunk in qwenfast_proxy.stream_chat(messages=use_messages, model=model):
                    t = chunk.get("type")
                    if t == "text":
                        c = chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                    elif t == "done":
                        break
                    elif t == "error":
                        break
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return
            elif slug == "geminiweb":
                from api import geminiweb_proxy
                for chunk in geminiweb_proxy.stream_chat(use_messages, model=model):
                    t = chunk.get("type")
                    if t == "thought":
                        c = chunk.get("text") or chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "think", "content": c}
                    elif t in ("text", "content"):
                        c = chunk.get("text") or chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                    elif t == "done":
                        break
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return

            elif slug == "tryingopen":
                from api import tryingopen_proxy
                for chunk in tryingopen_proxy.stream_chat(use_messages, model=model, effort=extra.get("effort", "deep"), system_prompt=use_system):
                    t = chunk.get("type")
                    if t == "reasoning":
                        c = chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "think", "content": c}
                    elif t == "text":
                        c = chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                    elif t == "done":
                        break
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return

            elif slug == "inception":
                from api import inception_proxy
                for chunk in inception_proxy.stream_chat(use_messages, model=model, reasoning_effort=extra.get("reasoning_effort", "high")):
                    t = chunk.get("type")
                    if t in ("thought", "reasoning"):
                        c = chunk.get("text") or chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "think", "content": c}
                    elif t == "text":
                        c = chunk.get("content") or chunk.get("text") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                    elif t == "done":
                        break
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return

            elif slug == "k2think":
                from api import k2think_proxy
                for chunk in k2think_proxy.stream_chat(use_messages, model=model):
                    t = chunk.get("type")
                    if t in ("thought", "reasoning"):
                        c = chunk.get("text") or chunk.get("content") or ""
                        if c:
                            got_any = True
                            yield {"type": "think", "content": c}
                    elif t == "text":
                        c = chunk.get("content") or chunk.get("text") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return

            elif slug == "longcat":
                from api import longcat_proxy
                for chunk in longcat_proxy.stream_chat(use_messages, model=model):
                    t = chunk.get("type")
                    if t == "text":
                        c = chunk.get("content") or chunk.get("text") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return

            elif slug == "egov":
                from api import egov_proxy
                for chunk in egov_proxy.stream_chat(user_message=use_prompt, model=model, history=[], system_prompt=use_system):
                    t = chunk.get("type")
                    if t == "content":
                        c = chunk.get("text") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return

            elif slug == "deepai":
                from api import deepai_proxy
                for chunk in deepai_proxy.stream_chat(user_message=use_prompt, model=model, history=[], system_prompt=use_system):
                    t = chunk.get("type")
                    if t == "content":
                        c = chunk.get("text") or ""
                        if c:
                            got_any = True
                            yield {"type": "delta", "content": c}
                if got_any:
                    yield {"type": "model", "model": f"{slug}/{model}"}
                    return
        except Exception:
            continue


def llm_chat_stream(user, system, prompt, max_tokens=1200, temperature=0.6, timeout=90, model_key="neby-pro"):
    return stream_proxy_chat(system, prompt, model_key=model_key)


def _accumulate_stream(system, prompt, model_key, yield_think=True, status_prefix=""):
    """Generator: yields {type:'think'}, {type:'delta'} live, and {type:'status'} periodically,
    then yields {type:'_done', 'text': full_accumulated_text, 'model': 'provider/model'} as final."""
    accumulated = []
    chars_yielded = 0
    used_model = ""
    for chunk in stream_proxy_chat(system, prompt, model_key=model_key):
        t = chunk.get("type")
        content = chunk.get("content") or ""
        if t == "model":
            used_model = content or chunk.get("model") or ""
            yield {"type": "model", "model": used_model}
        elif t == "think" and content and yield_think:
            yield {"type": "think", "content": content}
        elif t == "search" and content:
            yield {"type": "search", "content": content, "results": chunk.get("results") or []}
            yield {"type": "think", "content": content[:200]}
        elif t == "delta" and content:
            accumulated.append(content)
            yield {"type": "delta", "content": content}
            total = sum(len(c) for c in accumulated)
            if total - chars_yielded > 120:
                chars_yielded = total
                yield {"type": "status", "tool": "generating", "label": f"{status_prefix}Writing... ({total} chars)"}
        elif t == "status" and content:
            yield chunk
    yield {"type": "_done", "text": "".join(accumulated), "model": used_model}


def stream_generate_doc(user, topic, pages=1, doc_type="assignment", instructions="", model_key="neby-pro"):
    """Streaming version of generate_doc. Yields live think/status frames, then a final
    {type:'doc_ready', ...} frame. Caller should yield each frame to the SSE stream."""
    pages = max(1, min(4, int(pages or 1)))
    doc_type = (doc_type or "assignment").lower()
    if doc_type not in ("assignment", "report", "resume", "essay"):
        doc_type = "assignment"
    prompt = f"Topic: {topic}\nType: {doc_type}\nPages: {pages}\n"
    if instructions:
        prompt += f"Extra instructions: {instructions[:600]}\n"
    prompt += "Generate now."

    system = get_lazy_prompts()["generate"]
    raw = None
    used_model = ""
    for frame in _accumulate_stream(system, prompt, model_key, yield_think=True, status_prefix="Drafting — "):
        if frame.get("type") == "_done":
            raw = frame["text"]
            used_model = frame.get("model") or used_model
        elif frame.get("type") == "model":
            used_model = frame.get("model") or ""
            yield frame
        else:
            yield frame

    data = parse_llm_json(raw) if raw else None
    html = ""
    title = topic
    if data and data.get("html"):
        html = str(data["html"])[:80000]
        title = str(data.get("title") or topic)[:120]
    elif raw:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-z]*\n?|```$", "", cleaned, flags=re.I).strip()
        if "<h" in cleaned or "<p" in cleaned:
            html = cleaned[:80000]
        else:
            lines = cleaned.split("\n")
            html_parts = []
            for line in lines:
                l = line.strip()
                if not l:
                    continue
                if l.startswith("# "):
                    title = l[2:].strip()
                    html_parts.append(f"<h1>{title}</h1>")
                elif l.startswith("## "):
                    html_parts.append(f"<h2>{l[3:].strip()}</h2>")
                elif l.startswith("### "):
                    html_parts.append(f"<h3>{l[4:].strip()}</h3>")
                elif l.startswith(("- ", "* ")):
                    html_parts.append(f"<li>{l[2:].strip()}</li>")
                else:
                    html_parts.append(f"<p>{l}</p>")
            html = "\n".join(html_parts)

    if not html:
        fb = fallback_doc(topic, pages, doc_type)
        yield {"type": "doc_ready", "title": fb["title"], "html": fb["html"], "provider": "fallback", "model": used_model or "fallback"}
        return

    html = clean_doc_html(html)
    if not re.search(r"<h1", html, re.I):
        html = f"<h1>{title}</h1>\n" + html
    yield {"type": "doc_ready", "title": title, "html": html, "provider": "llm", "model": used_model or "qwenfast/qwen3.8-27b"}


def stream_edit_doc(user, doc_html, instruction, model_key="neby-pro"):
    """Streaming version of edit_doc. Yields live frames then {type:'edit_ready', ...}."""
    plain = strip_tags(doc_html)[:9000]
    prompt = f"Instruction: {instruction[:600]}\n\nCurrent document:\n{doc_html[:40000]}\n\nPlain-text digest:\n{plain}"

    system = get_lazy_prompts()["edit"]
    raw = None
    used_model = ""
    for frame in _accumulate_stream(system, prompt, model_key, yield_think=True, status_prefix="Revising — "):
        if frame.get("type") == "_done":
            raw = frame["text"]
            used_model = frame.get("model") or used_model
        elif frame.get("type") == "model":
            used_model = frame.get("model") or ""
            yield frame
        else:
            yield frame

    data = parse_llm_json(raw) if raw else None
    if not data or not data.get("html"):
        yield {"type": "edit_ready", "html": None, "model": used_model}
        return
    html = str(data["html"])[:80000]
    title = str(data.get("title") or "")[:120]
    summary = str(data.get("summary") or instruction)[:200]
    yield {"type": "edit_ready", "html": html, "title": title, "summary": summary, "model": used_model or "qwenfast/qwen3.8-27b"}


def fallback_doc(topic, pages=1, doc_type="assignment"):
    topic = (topic or "Untitled").strip()[:80]
    title = topic.title() if len(topic.split()) <= 6 else topic.capitalize()
    paras = max(3, min(6, int(pages or 1) + 2))
    html = f"<h1>{title}</h1>"
    for i in range(paras):
        html += f"<h2>Section {i + 1}</h2><p><strong>{topic}</strong> — comprehensive study material covering core principles, mathematical derivations, formula summaries, and solved examples.</p>"
        if i == 0:
            html += "<blockquote>Essential concept summary and fundamental laws.</blockquote>"
    outline = [{"heading": f"Section {i + 1}", "bullets": []} for i in range(paras)]
    return {"title": title, "html": html, "outline": outline}


def generate_doc(user, topic, pages=1, doc_type="assignment", instructions="", model_key="neby-pro"):
    pages = max(1, min(4, int(pages or 1)))
    doc_type = (doc_type or "assignment").lower()
    if doc_type not in ("assignment", "report", "resume", "essay"):
        doc_type = "assignment"
    prompt = f"Topic: {topic}\nType: {doc_type}\nPages: {pages}\n"
    if instructions:
        prompt += f"Extra instructions: {instructions[:600]}\n"
    prompt += "Generate now."
    system = get_lazy_prompts()["generate"]
    raw = llm_chat(user, system, prompt, max_tokens=4000, model_key=model_key)
    data = parse_llm_json(raw) if raw else None

    html = ""
    title = topic
    if data and data.get("html"):
        html = str(data["html"])[:80000]
        title = str(data.get("title") or topic)[:120]
    elif raw:
        cleaned = raw.strip()
        if cleaned.startswith("```html"):
            cleaned = re.sub(r"^```(?:html)?|```$", "", cleaned, flags=re.I).strip()
        elif cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-z]*|```$", "", cleaned, flags=re.I).strip()

        if "<h" in cleaned or "<p" in cleaned:
            html = cleaned[:80000]
        else:
            lines = cleaned.split("\n")
            html_parts = []
            for line in lines:
                l = line.strip()
                if not l:
                    continue
                if l.startswith("# "):
                    title = l[2:].strip()
                    html_parts.append(f"<h1>{title}</h1>")
                elif l.startswith("## "):
                    html_parts.append(f"<h2>{l[3:].strip()}</h2>")
                elif l.startswith("### "):
                    html_parts.append(f"<h3>{l[4:].strip()}</h3>")
                elif l.startswith("- ") or l.startswith("* "):
                    html_parts.append(f"<li>{l[2:].strip()}</li>")
                else:
                    html_parts.append(f"<p>{l}</p>")
            html = "\n".join(html_parts)

    if not html:
        fb = fallback_doc(topic, pages, doc_type)
        fb["provider"] = "fallback"
        return fb

    html = clean_doc_html(html)
    if not re.search(r"<h1", html, re.I):
        html = f"<h1>{title}</h1>\n" + html
    return {"title": title, "html": html, "provider": "llm"}


def edit_doc(user, doc_html, instruction, model_key="neby-pro"):
    plain = strip_tags(doc_html)[:9000]
    prompt = f"Instruction: {instruction[:600]}\n\nCurrent document:\n{doc_html[:40000]}\n\nPlain-text digest:\n{plain}"
    system = get_lazy_prompts()["edit"]
    raw = llm_chat(user, system, prompt, max_tokens=3400, model_key=model_key)
    data = parse_llm_json(raw) if raw else None
    if not data or not data.get("html"):
        return None
    html = clean_doc_html(str(data["html"])[:80000])
    title = str(data.get("title") or "")[:120]
    summary = str(data.get("summary") or instruction)[:200]
    return {"html": html, "title": title, "summary": summary}


def append_section(user, doc_html, brief, model_key="neby-pro"):
    prompt = f"New section brief: {brief[:500]}\n\nExisting document (for style continuity):\n{doc_html[:30000]}"
    system = get_lazy_prompts()["section"]
    raw = llm_chat(user, system, prompt, max_tokens=900, model_key=model_key)
    data = parse_llm_json(raw) if raw else None
    if not data or not data.get("html"):
        return None
    heading = str(data.get("heading") or brief)[:100]
    body = str(data["html"])[:12000]
    return {"heading": heading, "body": body}


def breakdown_doc(user, doc_html, model_key="neby-pro"):
    plain = strip_tags(doc_html)[:8000]
    prompt = (
        "Turn this document into a concise actionable checklist the student can follow.\n"
        "Markdown only: a bold intro line, then '- [ ] task' items grouped under '### ' headings (3-5 groups, 3-5 tasks each).\n\n"
        f"Document:\n{plain}"
    )
    raw = llm_chat(user, "You compress documents into actionable study checklists. Output markdown only.", prompt, max_tokens=1100, temperature=0.35, model_key=model_key)
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


def stream_reply(user, prompt, max_tokens=1000, model_key="neby-pro"):
    system = get_lazy_prompts()["reply"]
    gen = llm_chat_stream(user, system, prompt, max_tokens=max_tokens, model_key=model_key)

    def wrapped():
        if gen is None:
            pieces = ["I'm running in offline mode right now — I can still sketch outlines and checklists locally. Try again shortly for full drafting."]
            for piece in pieces:
                yield {"type": "delta", "content": piece}
            yield {"type": "done", "model": "offline"}
            return
        got_any = False
        try:
            for chunk in gen:
                if chunk.get("type") in ("delta", "text"):
                    got_any = True
                elif chunk.get("type") == "done":
                    continue
                yield chunk
            if not got_any:
                yield {"type": "delta", "content": "I'm ready to help — tell me what document or topic you'd like to work on."}
                yield {"type": "done", "model": "empty"}
        except Exception as exc:
            yield {"type": "delta", "content": f"\n\n_(stream interrupted: {str(exc)[:80]})_"}
            yield {"type": "done", "model": "error"}

    return wrapped()
