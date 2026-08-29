"""The canonical document specification.

Every renderer (DOCX, PDF, HTML preview) consumes the same normalized spec, so
styling is decided once and output is consistent across formats. The agent emits
loose JSON; `normalize_spec` coerces, repairs and fills defaults so a sloppy
model response still produces a correctly structured, submission-ready document
instead of throwing.
"""

import re
import unicodedata

DOC_TYPES = {
    'assignment', 'lab_report', 'research_paper', 'essay', 'report',
    'project_report', 'cv', 'resume', 'letter', 'notes', 'thesis',
    'business_report', 'case_study', 'article', 'speech', 'generic',
}

TEMPLATES = {'neb_classic', 'modern', 'formal', 'minimal', 'corporate'}
BLOCK_TYPES = {
    'paragraph', 'bullets', 'numbered', 'table', 'code', 'quote',
    'formula', 'steps', 'callout', 'image_caption', 'divider', 'definition',
    'image', 'figure',
}

DEFAULT_TEMPLATE = 'neb_classic'
DEFAULT_DOC_TYPE = 'assignment'

_TEMPLATE_FONTS = {
    'neb_classic': ('Times New Roman', 12),
    'formal': ('Times New Roman', 12),
    'modern': ('Calibri', 11),
    'minimal': ('Calibri', 11),
    'corporate': ('Georgia', 11),
}


def _clean(value, limit=None):
    if value is None:
        return ''
    text = str(value)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    if limit:
        text = text[:limit]
    return text


def _as_list(value, item_limit=200):
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r'\n+', value)
        items = [re.sub(r'^\s*(?:[-*•]|\d+[.)])\s*', '', p).strip() for p in parts]
    elif isinstance(value, (list, tuple)):
        items = []
        for entry in value:
            if isinstance(entry, dict):
                items.append(_clean(entry.get('text') or entry.get('item') or entry.get('value') or entry.get('title') or ''))
            else:
                items.append(_clean(entry))
    else:
        items = [_clean(value)]
    return [i for i in items if i][:item_limit]


_CODE_FRAGMENT_RE = re.compile(r'[={\[\]()<>;]|^\s*(import|def |for |while |print\()')

_REFERENCE_HEADINGS = {
    'references', 'reference', 'bibliography', 'works cited', 'works-cited',
    'sources', 'reference list', 'citations',
}


def _is_reference_heading(heading):
    key = re.sub(r'[^a-z\s-]+', '', str(heading or '').strip().lower()).strip()
    key = re.sub(r'^\d+[.)]\s*', '', key)
    return key in _REFERENCE_HEADINGS


def _merge_reference_section(sections):
    """Drop a planned References section, harvesting any citations it holds.

    Returns `(sections, harvested_texts)`. Only a section that is *purely* a
    reference list is removed — if it also carries tables or figures it is a
    real discussion section that happens to be named References, so it stays.
    """
    harvested = []
    kept = []
    for section in sections or []:
        if not _is_reference_heading(section.get('heading')):
            kept.append(section)
            continue
        blocks = section.get('blocks') or []
        if any(str(b.get('type')) in ('table', 'image') for b in blocks):
            kept.append(section)
            continue
        for block in blocks:
            btype = str(block.get('type') or '')
            if btype in ('bullets', 'numbered', 'list'):
                harvested.extend(str(i).strip() for i in (block.get('items') or []))
            elif btype == 'steps':
                for item in (block.get('items') or []):
                    if not isinstance(item, dict):
                        harvested.append(str(item).strip())
                        continue
                    parts = [str(item.get('title') or '').strip(),
                             str(item.get('detail') or '').strip()]
                    harvested.append('. '.join(p for p in parts if p))
            elif btype in ('paragraph', 'quote'):
                harvested.append(str(block.get('text') or '').strip())
    return kept, [h for h in harvested if h]


def _is_degenerate_table(header, rows):
    """Reject table-shaped noise before it reaches a renderer.

    Models occasionally emit a stray code fragment or a single stray value as a
    one-cell "table". It renders as a lonely boxed cell in the middle of an
    otherwise clean document, which reads as a layout bug to the reader.
    """
    cells = [str(c).strip() for row in rows for c in row] + [str(h).strip() for h in header]
    filled = [c for c in cells if c]
    if not filled:
        return True
    if not rows:
        return True
    width = max([len(header)] + [len(r) for r in rows])
    if width < 2:
        return True
    # A one-row table whose cells look like a code statement, not data.
    if len(rows) == 1:
        return any(_CODE_FRAGMENT_RE.search(c) and len(c) > 25 for c in filled)
    return False


def _normalize_table(raw):
    if not isinstance(raw, dict):
        return None
    header = _as_list(raw.get('header') or raw.get('columns') or raw.get('head'))
    rows_raw = raw.get('rows') or raw.get('data') or raw.get('body') or []
    rows = []
    if isinstance(rows_raw, list):
        for row in rows_raw[:200]:
            if isinstance(row, dict):
                cells = [_clean(row.get(c, '')) for c in (header or sorted(row.keys()))]
            elif isinstance(row, (list, tuple)):
                cells = [_clean(c) for c in row]
            else:
                cells = [_clean(row)]
            rows.append([c[:600] for c in cells])
    if not header and not rows:
        return None
    if _is_degenerate_table(header, rows):
        return None
    if header and rows:
        width = len(header)
        rows = [(r + [''] * width)[:width] for r in rows]
    return {
        'type': 'table',
        'header': [h[:200] for h in header],
        'rows': rows,
        'caption': _clean(raw.get('caption') or raw.get('title') or ''),
        'align': raw.get('align') or '',
    }


def _normalize_block(raw):
    """Coerce one loosely-typed block into a canonical block dict (or None)."""
    if raw is None:
        return None
    if isinstance(raw, str):
        text = _clean(raw)
        if not text:
            return None
        return {'type': 'paragraph', 'text': text}

    if not isinstance(raw, dict):
        return None

    btype = str(raw.get('type') or raw.get('kind') or '').strip().lower()
    if btype in ('table', 'table_block'):
        table = _normalize_table(raw)
        return table

    if btype in ('bullets', 'bullet', 'ul', 'list', 'points'):
        items = _as_list(raw.get('items') or raw.get('points') or raw.get('list'))
        return {'type': 'bullets', 'items': items} if items else None

    if btype in ('numbered', 'ol', 'numbered_list', 'steps_list'):
        items = _as_list(raw.get('items') or raw.get('steps') or raw.get('list'))
        return {'type': 'numbered', 'items': items} if items else None

    if btype in ('code', 'pre', 'snippet', 'codeblock'):
        text = _clean(raw.get('text') or raw.get('code') or raw.get('content'))
        return {'type': 'code', 'text': text, 'language': _clean(raw.get('language') or raw.get('lang') or '')} if text else None

    if btype in ('quote', 'blockquote', 'citation'):
        text = _clean(raw.get('text') or raw.get('quote'))
        return {'type': 'quote', 'text': text, 'cite': _clean(raw.get('cite') or raw.get('source') or '')} if text else None

    if btype in ('formula', 'equation', 'math'):
        latex = _clean(raw.get('latex') or raw.get('formula') or raw.get('text') or raw.get('expr'))
        return {'type': 'formula', 'latex': latex} if latex else None

    if btype in ('steps', 'procedure', 'steps_block'):
        items = raw.get('items') or raw.get('steps') or []
        out = []
        if isinstance(items, list):
            for entry in items[:60]:
                if isinstance(entry, dict):
                    out.append({
                        'title': _clean(entry.get('title') or entry.get('name') or ''),
                        'detail': _clean(entry.get('detail') or entry.get('text') or ''),
                    })
                else:
                    out.append({'title': '', 'detail': _clean(entry)})
        return {'type': 'steps', 'items': [s for s in out if s['title'] or s['detail']]} if out else None

    if btype in ('callout', 'note', 'callout_block', 'info'):
        text = _clean(raw.get('text') or raw.get('note') or raw.get('body'))
        return {'type': 'callout', 'text': text, 'label': _clean(raw.get('label') or 'Note')} if text else None

    if btype in ('definition', 'def'):
        term = _clean(raw.get('term') or raw.get('name'))
        text = _clean(raw.get('text') or raw.get('definition') or raw.get('meaning'))
        return {'type': 'definition', 'term': term, 'text': text} if (term or text) else None

    if btype in ('divider', 'hr', 'separator'):
        return {'type': 'divider'}

    if btype in ('image_caption', 'caption', 'figure'):
        text = _clean(raw.get('text') or raw.get('caption'))
        return {'type': 'image_caption', 'text': text, 'label': _clean(raw.get('label') or 'Figure')} if text else None

    if btype in ('image', 'figure', 'img', 'chart'):
        # Image blocks need a `path` (workspace-relative) or `data` (raw bytes).
        path = _clean(raw.get('path') or raw.get('src') or raw.get('file'))
        data = raw.get('data') or raw.get('bytes')
        if not path and not data:
            return None
        try:
            width = float(raw.get('width') or raw.get('width_pct') or 80)
        except (TypeError, ValueError):
            width = 80.0
        width = max(15.0, min(100.0, width))
        return {
            'type': 'image',
            'path': path,
            'data': data,
            'alt': _clean(raw.get('alt') or raw.get('caption') or 'Figure'),
            'caption': _clean(raw.get('caption') or raw.get('title') or ''),
            'width': width,
            'align': _clean(raw.get('align') or 'center'),
        }

    # Unknown or missing type: fall back to whatever text is present.
    text = _clean(raw.get('text') or raw.get('content') or raw.get('body') or raw.get('value'))
    if text:
        return {'type': 'paragraph', 'text': text}
    return None


def _normalize_section(raw, index=0):
    if isinstance(raw, str):
        heading = _clean(raw, 300)
        return {'heading': heading, 'level': 1, 'blocks': []} if heading else None

    if not isinstance(raw, dict):
        return None

    heading = _clean(raw.get('heading') or raw.get('title') or raw.get('name') or '', 300)
    try:
        level = max(1, min(4, int(raw.get('level') or 1)))
    except Exception:
        level = 1

    blocks_raw = raw.get('blocks') or raw.get('content') or raw.get('body') or raw.get('items')
    blocks = []
    if isinstance(blocks_raw, list):
        for entry in blocks_raw[:120]:
            block = _normalize_block(entry)
            if block:
                blocks.append(block)
    elif isinstance(blocks_raw, str):
        block = _normalize_block(blocks_raw)
        if block:
            blocks.append(block)
    elif isinstance(blocks_raw, dict):
        block = _normalize_block(blocks_raw)
        if block:
            blocks.append(block)

    if not heading and not blocks:
        return None
    return {'heading': heading, 'level': level, 'blocks': blocks}


def normalize_spec(raw, default_title='Untitled Document'):
    """Turn any plausible agent output into a valid, renderable document spec."""
    raw = raw if isinstance(raw, dict) else {}

    doc_type = str(raw.get('doc_type') or raw.get('type') or '').strip().lower()
    doc_type = doc_type if doc_type in DOC_TYPES else DEFAULT_DOC_TYPE

    template = str(raw.get('template') or '').strip().lower()
    template = template if template in TEMPLATES else DEFAULT_TEMPLATE

    font, font_size = _TEMPLATE_FONTS.get(template, _TEMPLATE_FONTS[DEFAULT_TEMPLATE])
    options = raw.get('options') if isinstance(raw.get('options'), dict) else {}
    try:
        line_spacing = float(options.get('line_spacing') or 1.15)
        line_spacing = max(1.0, min(2.5, line_spacing))
    except Exception:
        line_spacing = 1.15

    sections = []
    sections_raw = raw.get('sections') or raw.get('body') or raw.get('chapters') or []
    if isinstance(sections_raw, dict):
        sections_raw = [sections_raw]
    if isinstance(sections_raw, list):
        for entry in sections_raw[:80]:
            section = _normalize_section(entry)
            if section:
                sections.append(section)

    references = []
    refs_raw = raw.get('references') or raw.get('bibliography') or []
    if isinstance(refs_raw, list):
        for entry in refs_raw[:100]:
            if isinstance(entry, dict):
                text = _clean(entry.get('text') or entry.get('citation') or entry.get('title') or '')
                references.append({'text': text, 'url': _clean(entry.get('url') or '', 500)})
            else:
                text = _clean(entry)
                if text:
                    references.append({'text': text, 'url': ''})
    references = [r for r in references if r['text']]

    # Every renderer emits its own References section from `spec['references']`,
    # and the planner is also told to include one in the outline. Left alone the
    # document grows a second "References" heading with an empty body under it.
    # Fold the planned section into the real reference list and drop the shell.
    sections, harvested = _merge_reference_section(sections)
    seen_refs = {r['text'].strip().lower() for r in references}
    for text in harvested:
        key = text.strip().lower()
        if key and key not in seen_refs:
            seen_refs.add(key)
            references.append({'text': text, 'url': ''})

    title = _clean(raw.get('title') or raw.get('doc_title') or '', 300) or default_title

    spec = {
        'title': title,
        'subtitle': _clean(raw.get('subtitle') or '', 300),
        'doc_type': doc_type,
        'template': template,
        'author': _clean(raw.get('author') or raw.get('student') or '', 160),
        'roll_no': _clean(raw.get('roll_no') or raw.get('roll') or '', 60),
        'grade': _clean(raw.get('grade') or raw.get('class') or '', 60),
        'subject': _clean(raw.get('subject') or '', 160),
        'institution': _clean(raw.get('institution') or raw.get('school') or raw.get('college') or '', 200),
        'teacher': _clean(raw.get('teacher') or raw.get('submitted_to') or raw.get('supervisor') or '', 160),
        'date': _clean(raw.get('date') or '', 60),
        'abstract': _clean(raw.get('abstract') or raw.get('summary') or '', 4000),
        'acknowledgement': _clean(raw.get('acknowledgement') or raw.get('acknowledgment') or '', 3000),
        'options': {
            'toc': bool(options.get('toc', len(sections) >= 4)),
            'page_numbers': bool(options.get('page_numbers', True)),
            'header': _clean(options.get('header') or '', 160),
            'title_page': bool(options.get('title_page', doc_type in (
                'assignment', 'lab_report', 'research_paper', 'project_report',
                'thesis', 'report', 'business_report', 'case_study',
            ))),
            'line_spacing': line_spacing,
            'font': _clean(options.get('font') or font, 60) or font,
            'font_size': font_size,
        },
        'sections': sections,
        'references': references,
    }
    return spec


def spec_word_count(spec):
    text = plain_text(spec)
    return len(re.findall(r"\b[\w'-]+\b", text))


def plain_text(spec):
    """Flatten a spec to plain text — used for word counts and LLM summaries."""
    parts = [
        spec.get('title') or '', spec.get('subtitle') or '',
        spec.get('abstract') or '', spec.get('acknowledgement') or '',
    ]
    for section in spec.get('sections') or []:
        if section.get('heading'):
            parts.append(section['heading'])
        for block in section.get('blocks') or []:
            btype = block.get('type')
            if btype == 'paragraph':
                parts.append(block.get('text') or '')
            elif btype in ('bullets', 'numbered'):
                parts.extend(block.get('items') or [])
            elif btype == 'table':
                parts.extend(block.get('header') or [])
                for row in block.get('rows') or []:
                    parts.extend(row)
                if block.get('caption'):
                    parts.append(block['caption'])
            elif btype in ('code', 'quote', 'formula', 'callout'):
                parts.append(block.get('text') or block.get('latex') or '')
            elif btype == 'steps':
                for item in block.get('items') or []:
                    parts.append(f"{item.get('title') or ''} {item.get('detail') or ''}")
            elif btype == 'definition':
                parts.append(f"{block.get('term') or ''} {block.get('text') or ''}")
            elif btype == 'image_caption':
                parts.append(block.get('text') or '')
    for ref in spec.get('references') or []:
        parts.append(ref.get('text') or '')
    return '\n'.join(p for p in parts if p)


def spec_outline(spec):
    """Compact outline used when feeding document state back to the model."""
    lines = [f"# {spec.get('title')}"]
    for section in spec.get('sections') or []:
        indent = '  ' * max(0, int(section.get('level') or 1) - 1)
        lines.append(f"{indent}- {section.get('heading') or '(untitled)'}")
    return '\n'.join(lines)
