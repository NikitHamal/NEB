"""Document quality engine.

Turns a one-line brief into a submission-ready document. Pipeline:
research -> outline -> parallel section drafting -> assembly -> critique ->
targeted revision -> render. The agent loop invokes this through a single
tool call; callers see the result as one bundled deliverable.
"""

import concurrent.futures
import re

from . import docspec, llm, research, sandbox
from .engine_quality import _dedupe_tables, _missing_tables, _topic_overlap
from .engine_sections import (
    _SECTION_SYSTEM, _apply_global_fixes, _draft_section,
    _fallback_section, _format_sources, _revise_flagged,
)
from .engine_visuals import _inject_visuals
from .renderers import render_docx, render_html, render_pdf

DEFAULT_AUDIENCE = 'NEB Grade 11-12 student, Nepali academic context'
DEFAULT_TEMPLATE = 'neb_classic'
DOC_TYPE_KEYS = {
    'assignment', 'lab_report', 'research_paper', 'essay', 'report',
    'project_report', 'cv', 'resume', 'letter', 'notes', 'thesis',
    'business_report', 'case_study', 'article', 'speech',
}

DEPTH_WORDS = {
    'short': (450, 900),
    'standard': (1200, 2200),
    'comprehensive': (2500, 4500),
    'long': (4000, 7000),
}


def _workspace_path(ctx):
    """Workspace root for image resolution. Empty string when there is none."""
    try:
        run_id = (ctx or {}).get('run_id')
        if not run_id:
            return ''
        return sandbox.workspace_path(run_id, create=False)
    except Exception:
        return ''


def _front_matter_hint(brief, doc_type, audience):
    if not brief:
        return ''
    return f'BRIEF: {brief.strip()[:1200]}\nDOC TYPE: {doc_type}\nAUDIENCE: {audience}'


def _coerce_depth(value, default='standard'):
    key = str(value or default).strip().lower()
    return key if key in DEPTH_WORDS else default


def _resolve_doc_type(value, brief):
    text = (str(value or '') + ' ' + str(brief or '')).lower()
    for key in DOC_TYPE_KEYS:
        if re.search(r'\b' + re.escape(key.replace('_', ' ')) + r'\b', text):
            return key
    return 'assignment'


def _gather_research(brief, research_mode, audience):
    if not research_mode or not brief:
        return []
    queries = []
    base = re.sub(r'[^\w\s]', ' ', str(brief))
    tokens = [t for t in re.split(r'\s+', base) if len(t) > 3][:10]
    if tokens:
        queries.append(str(brief).strip())
    if len(tokens) > 4:
        queries.append(' '.join(tokens[:4]) + ' Nepal context')
    if 'assignment' in (brief or '').lower() or 'report' in (brief or '').lower():
        queries.append('NEB syllabus ' + ' '.join(tokens[:3]))
    if not queries:
        queries.append(str(brief).strip())

    pack = research.research_pack(queries[0], max_results=4, fetch_top=2, per_page_chars=4500)
    sources = list(pack.get('sources') or [])
    for extra in queries[1:2]:
        pack2 = research.research_pack(extra, max_results=3, fetch_top=1, per_page_chars=3500)
        sources.extend(pack2.get('sources') or [])
    seen, unique = set(), []
    for src in sources:
        if not src or not src.get('url') or src['url'] in seen:
            continue
        seen.add(src['url'])
        unique.append(src)
    return unique[:5]


_OUTLINE_SYSTEM = """You are the senior editor of a high-quality academic and professional
publishing house. You plan a document before anyone writes a word.

You must produce a JSON object with this exact shape:
{
  "title": "...",
  "subtitle": "...",
  "_title_locked": false,
  "doc_type": "...",
  "template": "neb_classic|modern|formal|minimal",
  "front": {
    "author": "...", "roll_no": "...", "grade": "...",
    "subject": "...", "institution": "...",
    "teacher": "...", "date": "..."
  },
  "abstract": "3-6 line executive summary, leave empty if not needed",
  "acknowledgement": "2-4 line acknowledgement, leave empty if not needed",
  "sections": [
    {"heading": "Section title", "level": 1,
     "purpose": "what this section accomplishes in one line",
     "key_points": ["point 1", "point 2", "point 3"],
     "block_types": ["paragraph", "bullets", "table", "formula", "code", "quote", "callout", "steps"],
     "target_words": 400
    }
  ],
  "references": ["source 1", "source 2"]
}

Rules:
- Sections must follow the natural academic progression for the document type.
  For lab reports: Objective, Theory, Apparatus, Procedure, Observation,
  Calculation, Result, Discussion, Conclusion, Precautions.
  For essays: Introduction, Body (2-4 named subsections), Conclusion.
  For assignments: Introduction, Main body, Discussion, Conclusion, References.
- 4-9 sections is right for a standard document; 7-12 for a comprehensive one.
- "key_points" must list concrete facts to include (formulas, definitions, observations)
  rather than vague hints like "discuss the topic".
- "block_types" pre-declares which block kinds the drafter should reach for.
  "table" is MANDATORY for any section whose purpose is to present readings,
  observations, readings-vs-values, comparisons, specifications or schedules
  (e.g. "Observation Table", "Result", "Comparison", "Bill of materials").
  If a section is named for data, it must be planned as data.
- Total target words across sections must match the requested depth.
- If a REQUIRED TITLE is given, "title" must be that exact string and every section must
  serve that exact subject. Web sources are background only; they never redefine the topic.
- Output ONLY the JSON. No prose, no markdown fences.
"""


def _plan_outline(user, brief, doc_type, audience, depth, sources, template, title=''):
    sources_text = _format_sources(sources)
    min_w, max_w = DEPTH_WORDS[depth]
    prompt_parts = [
        _front_matter_hint(brief, doc_type, audience),
        f'DEPTH: {depth} ({min_w}-{max_w} words total)',
        f'TEMPLATE: {template}',
    ]
    if title:
        prompt_parts.append(
            f'REQUIRED TITLE (use this as "title", verbatim): {title}\n'
            'The subject of the document is fixed by that title and by the BRIEF. '
            'Research sources may mention other experiments or topics — ignore them. '
            'Planning a document about a different topic is a critical failure.'
        )
    if sources_text:
        prompt_parts.append(sources_text)
    prompt_parts.append(
        'Produce the outline JSON for this document. Be specific and concrete.'
    )
    data, _ = llm.json_chat(
        user=user, system=_OUTLINE_SYSTEM,
        prompt='\n\n'.join(prompt_parts),
        max_tokens=2000, temperature=0.3, model_key='neby-pro',
    )
    if not data or not isinstance(data, dict):
        return _fallback_outline(brief, doc_type, template, depth)
    return data


def _fallback_outline(brief, doc_type, template, depth):
    scaffolds = {
        'lab_report': [
            'Objective', 'Theory', 'Apparatus Required',
            'Procedure', 'Observation', 'Calculation',
            'Result', 'Discussion', 'Conclusion', 'Precautions',
        ],
        'research_paper': [
            'Introduction', 'Literature Review', 'Methodology',
            'Findings', 'Discussion', 'Conclusion', 'Limitations',
        ],
        'essay': ['Introduction', 'Body', 'Counter-arguments', 'Conclusion'],
        'project_report': [
            'Introduction', 'Objectives', 'Methodology',
            'Implementation', 'Results', 'Conclusion', 'Future Scope',
        ],
        'cv': ['Header', 'Profile', 'Education', 'Skills', 'Projects', 'Experience'],
        'assignment': ['Introduction', 'Main Body', 'Discussion', 'Conclusion'],
    }
    sections = scaffolds.get(doc_type, scaffolds['assignment'])
    min_w, max_w = DEPTH_WORDS[depth]
    total = max(min_w, min(max_w, 1600))
    per_section = max(180, total // max(1, len(sections)))
    return {
        'title': (brief or 'Untitled Document')[:140],
        'doc_type': doc_type,
        'template': template,
        'sections': [
            {'heading': h, 'level': 1, 'purpose': '', 'key_points': [], 'block_types': ['paragraph', 'bullets'], 'target_words': per_section}
            for h in sections
        ],
        'references': [],
    }


_CRITIQUE_SYSTEM = """You are a senior editor reviewing a document for quality.

Read the document and return a JSON object:
{
  "score": 0-100,
  "issues": [{"section": "Section heading", "kind": "fact|completeness|structure|clarity|formula|citation", "fix": "concrete fix"}],
  "sections_to_revise": ["Section heading 1", "Section heading 2"],
  "global_fixes": ["Apply SI units everywhere", "Add a real citation in Theory"]
}

Be honest. Only flag things that would prevent the document from being submitted as-is.
If the document is already strong, return score 85+, empty arrays.

Check these structural faults specifically:
- A section that talks about a table, readings or results but shows none. Treat any
  "STRUCTURAL DEFECTS FOUND BY AUTOMATED CHECK" entry as a confirmed defect: score 60 or
  below, put the section in "sections_to_revise", and describe the fix as "add a table
  block with header and data rows".
- Measurements, statistics or survey results presented as real when the document could
  not have observed them. Flag as kind "fact".

Output ONLY the JSON.
"""


def _critique(user, outline, sections, sources, missing_tables=None):
    if not sections:
        return {'score': 0, 'issues': [], 'sections_to_revise': [], 'global_fixes': []}

    sections_text = []
    for sec in sections:
        blocks = sec.get('blocks') or []
        bits = [sec.get('heading') or '']
        for block in blocks[:8]:
            btype = block.get('type')
            if btype == 'paragraph':
                bits.append(block.get('text') or '')
            elif btype in ('bullets', 'numbered'):
                bits.extend(block.get('items') or [])
            elif btype == 'table':
                bits.append(f"Table: {block.get('caption') or ''}")
                bits.extend(block.get('header') or [])
            elif btype == 'formula':
                bits.append(block.get('latex') or '')
        sections_text.append('\n'.join(bits)[:3000])

    prompt = (
        f'TITLE: {outline.get("title")}\nDOC TYPE: {outline.get("doc_type")}\n\n'
        f'SECTIONS:\n\n' + '\n\n--- SECTION ---\n\n'.join(sections_text)
    )
    missing = missing_tables if missing_tables is not None else _missing_tables(outline, sections)
    if missing:
        prompt += (
            '\n\nSTRUCTURAL DEFECTS FOUND BY AUTOMATED CHECK:\n'
            + '\n'.join(f'- "{h}" has NO table block. The reader is told a table exists but '
                        f'no data is shown. This section must be revised to emit a real table.'
                        for h in missing)
        )

    if sources:
        prompt += '\n\nAvailable sources:\n' + _format_sources(sources)

    data, _ = llm.json_chat(
        user=user, system=_CRITIQUE_SYSTEM, prompt=prompt,
        max_tokens=1400, temperature=0.2, model_key='neby-pro', attempts=2,
    )
    if not data or not isinstance(data, dict):
        return {'score': 70, 'issues': [], 'sections_to_revise': [], 'global_fixes': []}
    return data


def build_document(user, ctx, title, brief, doc_type='', audience='',
                   depth='standard', template='', research_mode=True,
                   output_formats=None, emit=None, on_step=None,
                   visuals_enabled=True):
    """End-to-end pipeline. Returns a dict of artifacts."""
    output_formats = output_formats or ['docx', 'pdf', 'html']
    ctx = ctx or {}
    doc_type = _resolve_doc_type(doc_type, brief)
    template = (template or DEFAULT_TEMPLATE) if template in {'neb_classic', 'modern', 'formal', 'minimal', 'corporate'} else DEFAULT_TEMPLATE
    depth = _coerce_depth(depth)
    audience = audience or DEFAULT_AUDIENCE
    title = title or brief or 'Untitled Document'

    def step(label, detail=''):
        if on_step:
            on_step(label, detail)
        if emit:
            emit({'type': 'status', 'label': label, 'detail': detail})

    step('Classifying request and choosing template', f'{doc_type} · {template} · {depth}')

    sources = []
    if research_mode:
        step('Researching authoritative sources')
        sources = _gather_research(brief, True, audience)
        step(f'Research collected ({len(sources)} sources)')
    else:
        step('Skipping web research (disabled)')

    step('Planning the document outline')
    outline = _plan_outline(user, brief, doc_type, audience, depth, sources, template, title)
    # The planner reads research results before it writes the title, and a strong
    # off-topic source can pull the whole document somewhere else. The requested
    # title is the user's instruction, so it always wins.
    planned_title = str(outline.get('title') or '').strip()
    if title and planned_title and _topic_overlap(title, planned_title) < 0.2:
        step('Outline drifted off-topic; pinning it back', planned_title[:60])
        outline['title'] = title
    elif title:
        outline['title'] = title
    section_plans = outline.get('sections') or []
    step(f'Outline ready: {len(section_plans)} sections')

    sections = []
    if section_plans:
        step('Drafting sections in parallel', f'workers: {min(4, len(section_plans))}')
        indexed = [{**sp, '_idx': idx} for idx, sp in enumerate(section_plans)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(indexed))) as pool:
            futures = {pool.submit(_draft_section, user, outline, sp, sources, len(indexed), depth): sp for sp in indexed}
            for fut in concurrent.futures.as_completed(futures):
                spec = futures[fut]
                try:
                    sections.append(fut.result())
                except Exception:
                    sections.append(_fallback_section(spec, ''))
        sections.sort(key=lambda s: next(
            (idx for idx, sp in enumerate(indexed) if (sp.get('heading') or '') == (s.get('heading') or '')),
            999,
        ))

    step('Reviewing the draft')
    missing_tables = _missing_tables(outline, sections)
    if missing_tables:
        step(f'{len(missing_tables)} section(s) missing their data table')
    critique = _critique(user, outline, sections, sources, missing_tables)
    score = int(critique.get('score') or 0)
    flagged = list(critique.get('sections_to_revise') or [])
    # A section named for data must show data, even if the critic let it pass.
    for heading in missing_tables:
        if heading not in flagged:
            flagged.append(heading)
    step(f'Critique complete: {score}/100, {len(flagged)} sections to revise')

    if flagged:
        step('Revising flagged sections')
        sections = _revise_flagged(
            user, outline, sections, flagged, sources,
            critique=critique, missing_tables=missing_tables,
        )
        step('Revision applied')

    sections = _apply_global_fixes(sections, critique.get('global_fixes') or [])

    dropped = _dedupe_tables(sections)
    if dropped:
        step(f'Removed {dropped} duplicate table(s)')

    figures = []
    if visuals_enabled and sections:
        try:
            figures = _inject_visuals(
                user, ctx, outline, sections,
                _workspace_path(ctx), step,
            )
        except Exception as exc:
            step('Figures skipped', str(exc)[:100])
        if figures:
            step(f'{len(figures)} figures embedded')

    spec = {
        'title': (outline.get('title') or title).strip()[:300],
        'subtitle': (outline.get('subtitle') or '').strip()[:300],
        'doc_type': outline.get('doc_type') or doc_type,
        'template': outline.get('template') or template,
        'abstract': (outline.get('abstract') or '').strip(),
        'acknowledgement': (outline.get('acknowledgement') or '').strip(),
        'sections': sections,
        'references': [{'text': str(ref).strip(), 'url': ''} for ref in (outline.get('references') or []) if str(ref).strip()],
    }
    front = outline.get('front') if isinstance(outline.get('front'), dict) else {}
    spec.update({
        'author': str(front.get('author') or '').strip()[:160],
        'roll_no': str(front.get('roll_no') or '').strip()[:60],
        'grade': str(front.get('grade') or '').strip()[:60],
        'subject': str(front.get('subject') or '').strip()[:160],
        'institution': str(front.get('institution') or '').strip()[:200],
        'teacher': str(front.get('teacher') or '').strip()[:160],
        'date': str(front.get('date') or '').strip()[:60],
    })

    normalized = docspec.normalize_spec(spec, default_title=title)
    base_path = _workspace_path(ctx)

    artifacts = []
    safe_stub = re.sub(r'[^A-Za-z0-9_-]+', '_', normalized['title'])[:60] or 'document'

    render_errors = []
    for fmt in output_formats:
        try:
            if fmt == 'docx':
                bytes_data = render_docx(normalized, base_path=base_path)
                artifacts.append({'kind': 'doc', 'name': f'{safe_stub}.docx', 'mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'bytes': bytes_data})
            elif fmt == 'pdf':
                bytes_data = render_pdf(normalized, base_path=base_path)
                artifacts.append({'kind': 'pdf', 'name': f'{safe_stub}.pdf', 'mime': 'application/pdf', 'bytes': bytes_data})
            elif fmt == 'html':
                html = render_html(normalized, base_path=base_path)
                artifacts.append({'kind': 'doc', 'name': f'{safe_stub}.html', 'mime': 'text/html; charset=utf-8', 'bytes': html.encode('utf-8') if isinstance(html, str) else html})
            else:
                raise ValueError(f'unsupported format "{fmt}"')
        except Exception as exc:
            # A dropped format used to vanish without a trace, so the agent saw a
            # successful build that was missing the PDF it asked for and rebuilt
            # the whole document. Report it instead.
            reason = f'{type(exc).__name__}: {exc}'[:200]
            render_errors.append({'format': str(fmt), 'error': reason})
            step(f'Render {fmt} failed', reason[:120])

    return {
        'spec': normalized,
        'html': render_html(normalized, base_path=base_path),
        'artifacts': artifacts,
        'render_errors': render_errors,
        'figures': figures,
        'score': score,
        'issues': critique.get('issues') or [],
        'word_count': docspec.spec_word_count(normalized),
    }
