"""Section drafting and targeted revision."""

import re

from . import llm


def _format_sources(sources):
    """Render research results as a citable block for a drafting prompt.

    Lives here rather than in engine.py because both modules need it and
    engine.py already imports from this one — importing the other way round
    would be a cycle.
    """
    if not sources:
        return ''
    out = ['AUTHORITATIVE SOURCES (cite when relevant):']
    for idx, src in enumerate(sources, start=1):
        out.append(f"[{idx}] {src.get('title') or src.get('url')}")
        if src.get('snippet'):
            out.append(f"    {src['snippet'][:240]}")
        if src.get('text'):
            out.append(f"    excerpt: {src['text'][:1400]}")
    return '\n'.join(out)


_SECTION_SYSTEM = """You are an expert writer producing ONE section of a larger document.

Return ONLY a JSON object of the form:
{
  "heading": "section title (echoed back)",
  "level": 1,
  "blocks": [
    {"type": "paragraph", "text": "..."},
    {"type": "bullets", "items": ["...", "..."]},
    {"type": "table", "caption": "...", "header": ["A", "B"], "rows": [["1","2"]]},
    {"type": "code", "language": "python", "text": "..."},
    {"type": "formula", "latex": "1/f = 1/v - 1/u"},
    {"type": "quote", "text": "...", "cite": "..."},
    {"type": "callout", "label": "Note", "text": "..."},
    {"type": "steps", "items": [{"title": "...", "detail": "..."}]}
  ]
}

Strict quality rules:
- Cover every "key_points" item declared in the outline; nothing dropped.
- No fluff ("It is important to note that", "In conclusion we can say"). Real content only.
- Tables: if "table" appears in BLOCK TYPES TO USE, a table block is REQUIRED — emit it.
  It is a serious defect to describe a table in prose ("the readings were recorded in a
  table with columns for...") instead of returning an actual table block. If the section
  is named for data (Observation Table, Result, Comparison, Specifications), return the
  data. Header row and at least 4 data rows required.
- Never fabricate measurements, statistics, survey results or quotes and present them as
  real. Where a document needs sample readings the student will replace, label them
  plainly: put "Sample reading — replace with your own" in the table caption.
- Code: include only for technical docs; use a realistic but minimal example.
- Formulas: LaTeX without $$ delimiters, centred.
- Cite sources using [n] notation where research was provided.
- Word count must be within ±20% of the target.
- Output ONLY the JSON.
"""


def _draft_section(user, outline, section, sources, total_sections, depth, directive=''):
    sources_text = _format_sources(sources)
    prompt_parts = [
        f'DOCUMENT TITLE: {outline.get("title")}',
        f'THIS SECTION: {section.get("heading")} (section {section.get("_idx", 0) + 1} of {total_sections})',
        f'SECTION PURPOSE: {section.get("purpose") or ""}',
        f'KEY POINTS TO COVER (do not miss any): {"; ".join(section.get("key_points") or []) or "(no key points given)"}',
        f'BLOCK TYPES TO USE: {", ".join(section.get("block_types") or ["paragraph"])}',
        f'TARGET WORDS: {section.get("target_words") or 300}',
        f'DOC TYPE: {outline.get("doc_type")}',
    ]
    if sources_text:
        prompt_parts.append(sources_text)
    if directive:
        prompt_parts.append(
            'REVISION DIRECTIVE — a senior editor rejected the previous draft. '
            f'You MUST satisfy all of the following:\n{directive}'
        )
    prompt_parts.append('Write this section now. Return the JSON only.')

    data, raw = llm.json_chat(
        user=user, system=_SECTION_SYSTEM,
        prompt='\n\n'.join(prompt_parts),
        max_tokens=2400, temperature=0.45, model_key='neby-pro',
        attempts=2,
    )
    if not data:
        return _fallback_section(section, raw)
    return data


def _fallback_section(section, raw):
    heading = section.get('heading') or 'Section'
    bullet_block = {
        'type': 'bullets',
        'items': section.get('key_points') or ['Topic to be expanded in the next pass.'],
    }
    return {
        'heading': heading,
        'level': int(section.get('level') or 1),
        'blocks': [bullet_block, {'type': 'paragraph', 'text': (raw or '').strip()[:1200]}],
    }


def _apply_global_fixes(sections, global_fixes):
    if not global_fixes:
        return sections
    fixes = ' '.join(str(g).lower() for g in global_fixes)
    for section in sections:
        if 'units' in fixes or 'si unit' in fixes:
            for block in section.get('blocks') or []:
                if block.get('type') == 'paragraph':
                    text = block.get('text') or ''
                    if re.search(r'\b\d+\s*cm\b(?!\))', text) and ' (cm)' not in text:
                        block['text'] = re.sub(r'\b(\d+)\s*cm\b(?!\))', r'\1 cm', text)
    return sections


def _revise_flagged(user, outline, sections, flagged, sources, critique=None, missing_tables=None):
    """Re-draft flagged sections, handing the writer the editor's exact complaint.

    Re-running the original prompt reproduces the original defect, so each
    section is re-drafted with its specific fixes and hard structural demands
    attached as a mandatory directive.
    """
    fixes_by_section = {}
    for issue in (critique or {}).get('issues') or []:
        if not isinstance(issue, dict):
            continue
        key = str(issue.get('section') or '').strip().lower()
        fix = str(issue.get('fix') or '').strip()
        if key and fix:
            fixes_by_section.setdefault(key, []).append(fix)

    missing = {str(h).strip().lower() for h in (missing_tables or [])}

    by_heading = {(s.get('heading') or '').strip().lower(): s for s in sections}
    revised = dict(by_heading)
    for entry in flagged:
        # The contract is a list of heading strings, but models routinely send
        # `[{"heading": "...", "directive": "..."}]` instead. One stray dict
        # used to raise AttributeError mid-pipeline and throw away a document
        # that had already been researched and drafted.
        heading = entry.get('heading') if isinstance(entry, dict) else entry
        key = str(heading or '').strip().lower()
        if key not in by_heading:
            continue
        section = by_heading[key]
        directive_parts = list(fixes_by_section.get(key) or [])
        if key in missing:
            directive_parts.append(
                'This section MUST contain a real "table" block with a header row and at '
                'least 4 data rows. Do NOT describe the table in prose — emit the data.'
            )
        new_data = _draft_section(
            user, outline, section, sources, len(sections), 'standard',
            directive=' '.join(directive_parts),
        )
        if new_data:
            # The re-draft comes back from the model with only heading/level/blocks;
            # the planner's metadata has to be carried across or later passes that
            # key off it (table checks, ordering) silently lose the section.
            for field in ('_idx', 'block_types', 'purpose', 'key_points', 'target_words'):
                new_data.setdefault(field, section.get(field))
            revised[key] = new_data
    return list(revised.values())
