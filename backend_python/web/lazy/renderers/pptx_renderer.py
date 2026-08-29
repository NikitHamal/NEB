"""Themed PPTX deck renderer.

Builds 16:9 presentations with a title slide, section dividers, bullet slides,
two-column comparisons, tables, quotes and a closing slide — each carrying real
speaker notes so the deck is presentable, not a set of stubs.
"""

import io
import re

try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.util import Emu, Inches, Pt
    HAS_PPTX = True
except ImportError:
    Presentation = None
    RGBColor = None
    PP_ALIGN = MSO_ANCHOR = None
    Emu = Inches = Pt = None
    HAS_PPTX = False

THEMES = {
    'neb': {'bg': 'FFFFFF', 'accent': '1F4E5F', 'text': '1A1A1A', 'muted': '5A6470', 'soft': 'EAF1F4', 'title_bg': '1F4E5F'},
    'modern': {'bg': 'FFFFFF', 'accent': '2563EB', 'text': '111827', 'muted': '6B7280', 'soft': 'EFF6FF', 'title_bg': '2563EB'},
    'dark': {'bg': '111827', 'accent': '38BDF8', 'text': 'F9FAFB', 'muted': '9CA3AF', 'soft': '1F2937', 'title_bg': '030712'},
    'minimal': {'bg': 'FFFFFF', 'accent': '111111', 'text': '222222', 'muted': '777777', 'soft': 'F5F5F5', 'title_bg': '111111'},
}

SLIDE_W = Inches(13.333) if Inches else 0
SLIDE_H = Inches(7.5) if Inches else 0


def _rgb(hex_color):
    if not RGBColor:
        return None
    return RGBColor.from_string(str(hex_color).lstrip('#').upper())


def _clean(value, limit=None):
    text = re.sub(r'\s+', ' ', str(value or '')).strip()
    return text[:limit] if limit else text


def _as_list(value, limit=12):
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r'\n+', value)
        items = [re.sub(r'^\s*(?:[-*•]|\d+[.)])\s*', '', p).strip() for p in parts]
    elif isinstance(value, (list, tuple)):
        items = []
        for entry in value:
            if isinstance(entry, dict):
                items.append(_clean(entry.get('text') or entry.get('item') or entry.get('title') or entry.get('value') or ''))
            else:
                items.append(_clean(entry))
    else:
        items = [_clean(value)]
    return [i for i in items if i][:limit]


def normalize_deck(raw, default_title='Presentation'):
    raw = raw if isinstance(raw, dict) else {}
    theme = str(raw.get('theme') or 'neb').strip().lower()
    if theme not in THEMES:
        theme = 'neb'

    slides = []
    for entry in (raw.get('slides') or [])[:80]:
        if isinstance(entry, str):
            slides.append({'layout': 'bullets', 'title': _clean(entry, 120), 'bullets': []})
            continue
        if not isinstance(entry, dict):
            continue
        layout = str(entry.get('layout') or entry.get('type') or '').strip().lower()
        if layout not in ('title', 'section', 'bullets', 'two_column', 'table', 'quote', 'closing', 'callout'):
            layout = 'bullets'
        slide = {
            'layout': layout,
            'title': _clean(entry.get('title') or entry.get('heading') or '', 140),
            'subtitle': _clean(entry.get('subtitle') or '', 220),
            'bullets': _as_list(entry.get('bullets') or entry.get('points') or entry.get('items')),
            'notes': _clean(entry.get('notes') or entry.get('speaker_notes') or '', 1200),
            'quote': _clean(entry.get('quote') or '', 400),
            'cite': _clean(entry.get('cite') or entry.get('source') or '', 160),
            'callout': _clean(entry.get('callout') or entry.get('note') or '', 300),
        }
        left = entry.get('left') if isinstance(entry.get('left'), dict) else {}
        right = entry.get('right') if isinstance(entry.get('right'), dict) else {}
        slide['left'] = {'title': _clean(left.get('title') or left.get('heading') or '', 120), 'bullets': _as_list(left.get('bullets') or left.get('points'), 8)}
        slide['right'] = {'title': _clean(right.get('title') or right.get('heading') or '', 120), 'bullets': _as_list(right.get('bullets') or right.get('points'), 8)}

        table = entry.get('table') if isinstance(entry.get('table'), dict) else None
        if table:
            header = _as_list(table.get('header') or table.get('columns'), 8)
            rows = []
            for row in (table.get('rows') or [])[:14]:
                rows.append(_as_list(row, 8) if isinstance(row, (list, tuple)) else [_clean(row)])
            slide['table'] = {'header': header, 'rows': [r for r in rows if r], 'caption': _clean(table.get('caption') or '', 160)}
        else:
            slide['table'] = None

        if not slide['title'] and not slide['bullets'] and not slide['quote']:
            continue
        slides.append(slide)

    if not slides:
        slides = [{'layout': 'title', 'title': _clean(raw.get('title') or default_title, 140), 'subtitle': _clean(raw.get('subtitle') or '', 220), 'notes': '', 'bullets': []}]

    return {
        'title': _clean(raw.get('title') or default_title, 140),
        'subtitle': _clean(raw.get('subtitle') or '', 220),
        'author': _clean(raw.get('author') or raw.get('presenter') or '', 120),
        'date': _clean(raw.get('date') or '', 60),
        'theme': theme,
        'slides': slides,
    }


def render(spec, safe_name='presentation'):
    deck = normalize_deck(spec)
    theme = THEMES[deck['theme']]

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    for index, slide in enumerate(deck['slides']):
        if index == 0 and slide.get('layout') != 'title':
            _title_slide(prs, blank, deck, theme)
        layout = slide.get('layout')
        if layout == 'title':
            _title_slide(prs, blank, deck, theme, slide)
        elif layout == 'section':
            _section_slide(prs, blank, slide, theme)
        elif layout == 'two_column':
            _two_column_slide(prs, blank, slide, theme)
        elif layout == 'table':
            _table_slide(prs, blank, slide, theme)
        elif layout == 'quote':
            _quote_slide(prs, blank, slide, theme)
        elif layout == 'closing':
            _closing_slide(prs, blank, slide, theme)
        else:
            _bullet_slide(prs, blank, slide, theme)

        if slide.get('notes'):
            prs.slides[-1].notes_slide.notes_text_frame.text = slide['notes']

    buffer = io.BytesIO()
    prs.save(buffer)
    return buffer.getvalue()


# --------------------------------------------------------------------------
# Slide builders
# --------------------------------------------------------------------------

def _blank_slide(prs, blank, theme, fill=None):
    slide = prs.slides.add_slide(blank)
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = _rgb(fill or theme['bg'])
    return slide


def _textbox(slide, left, top, width, height, text, size=20, bold=False, color=None,
             align=None, italic=False, font='Calibri', anchor=None):
    if align is None and PP_ALIGN:
        align = PP_ALIGN.LEFT
    if anchor is None and MSO_ANCHOR:
        anchor = MSO_ANCHOR.TOP
    box = slide.shapes.add_textbox(left, top, width, height)
    frame = box.text_frame
    frame.word_wrap = True
    if anchor:
        frame.vertical_anchor = anchor
    lines = str(text or '').split('\n')
    for idx, line in enumerate(lines):
        para = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        para.text = line
        if align:
            para.alignment = align
        if Pt:
            para.space_after = Pt(6)
        for run in para.runs:
            if Pt:
                run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.name = font
            if color or not color:
                rgb_val = _rgb(color or '1A1A1A')
                if rgb_val:
                    run.font.color.rgb = rgb_val
    return box


def _accent_bar(slide, theme, left=None, top=None, width=None, height=None):
    from pptx.enum.shapes import MSO_SHAPE
    left = left if left is not None else Inches(0.9)
    top = top if top is not None else Inches(0.62)
    width = width if width is not None else Inches(1.5)
    height = height if height is not None else Inches(0.07)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = _rgb(theme['accent'])
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def _title_slide(prs, blank, deck, theme, slide=None):
    slide_spec = slide or {}
    s = _blank_slide(prs, blank, theme, fill=theme['title_bg'])
    title_text = slide_spec.get('title') or deck['title']
    subtitle_text = slide_spec.get('subtitle') or deck.get('subtitle') or ''

    _textbox(s, Inches(1.0), Inches(2.3), Inches(11.3), Inches(2.0), title_text,
             size=44, bold=True, color='FFFFFF')
    if subtitle_text:
        _textbox(s, Inches(1.0), Inches(4.0), Inches(11.3), Inches(1.0), subtitle_text,
                 size=20, color='D6E2E7')

    meta = '  |  '.join([x for x in [deck.get('author'), deck.get('date')] if x])
    if meta:
        _textbox(s, Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.6), meta,
                 size=14, color='B9CBD3')


def _section_slide(prs, blank, slide, theme):
    s = _blank_slide(prs, blank, theme, fill=theme['soft'])
    _accent_bar(s, theme, top=Inches(3.0), width=Inches(2.2))
    _textbox(s, Inches(1.0), Inches(3.3), Inches(11.3), Inches(1.4), slide.get('title') or '',
             size=34, bold=True, color=theme['accent'])
    if slide.get('subtitle'):
        _textbox(s, Inches(1.0), Inches(4.7), Inches(11.3), Inches(0.8), slide['subtitle'],
                 size=16, color=theme['muted'])


def _bullet_slide(prs, blank, slide, theme):
    s = _blank_slide(prs, blank, theme)
    _textbox(s, Inches(0.9), Inches(0.55), Inches(11.5), Inches(0.9), slide.get('title') or '',
             size=30, bold=True, color=theme['accent'])
    _accent_bar(s, theme, top=Inches(1.45))

    bullets = slide.get('bullets') or []
    if bullets:
        box = s.shapes.add_textbox(Inches(0.95), Inches(1.85), Inches(11.4), Inches(4.6))
        frame = box.text_frame
        frame.word_wrap = True
        size = 20 if len(bullets) <= 6 else (17 if len(bullets) <= 9 else 15)
        for idx, item in enumerate(bullets):
            para = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
            para.text = f'•  {item}'
            para.space_after = Pt(12)
            para.level = 0
            for run in para.runs:
                run.font.size = Pt(size)
                run.font.name = 'Calibri'
                run.font.color.rgb = _rgb(theme['text'])

    if slide.get('callout'):
        _callout(s, theme, slide['callout'])


def _two_column_slide(prs, blank, slide, theme):
    s = _blank_slide(prs, blank, theme)
    _textbox(s, Inches(0.9), Inches(0.55), Inches(11.5), Inches(0.9), slide.get('title') or '',
             size=30, bold=True, color=theme['accent'])
    _accent_bar(s, theme, top=Inches(1.45))

    for column, left in (('left', Inches(0.95)), ('right', Inches(6.95))):
        data = slide.get(column) or {}
        _textbox(s, left, Inches(1.85), Inches(5.4), Inches(0.6), data.get('title') or '',
                 size=18, bold=True, color=theme['accent'])
        items = data.get('bullets') or []
        if items:
            box = s.shapes.add_textbox(left, Inches(2.5), Inches(5.4), Inches(4.0))
            frame = box.text_frame
            frame.word_wrap = True
            for idx, item in enumerate(items):
                para = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
                para.text = f'•  {item}'
                para.space_after = Pt(10)
                for run in para.runs:
                    run.font.size = Pt(15)
                    run.font.name = 'Calibri'
                    run.font.color.rgb = _rgb(theme['text'])


def _table_slide(prs, blank, slide, theme):
    s = _blank_slide(prs, blank, theme)
    _textbox(s, Inches(0.9), Inches(0.55), Inches(11.5), Inches(0.9), slide.get('title') or '',
             size=28, bold=True, color=theme['accent'])
    _accent_bar(s, theme, top=Inches(1.45))

    table_spec = slide.get('table') or {}
    header = table_spec.get('header') or []
    rows = table_spec.get('rows') or []
    cols = max([len(header)] + [len(r) for r in rows]) if (header or rows) else 0
    if not cols:
        _bullet_slide(prs, blank, slide, theme)
        return

    row_count = len(rows) + (1 if header else 0)
    shape = s.shapes.add_table(row_count, cols, Inches(0.95), Inches(1.9), Inches(11.4), Inches(0.5 * row_count))
    table = shape.table

    def fill_cell(cell, text, bold=False, bg=None, fg=None):
        cell.text = ''
        para = cell.text_frame.paragraphs[0]
        para.text = str(text or '')
        para.alignment = PP_ALIGN.LEFT
        for run in para.runs:
            run.font.size = Pt(13)
            run.font.bold = bold
            run.font.name = 'Calibri'
            run.font.color.rgb = _rgb(fg or theme['text'])
        if bg:
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb(bg)
        else:
            cell.fill.background()

    start = 0
    if header:
        for idx in range(cols):
            fill_cell(table.cell(0, idx), header[idx] if idx < len(header) else '', bold=True, bg=theme['accent'], fg='FFFFFF')
        start = 1
    for r_idx, row in enumerate(rows):
        for c_idx in range(cols):
            bg = theme['soft'] if r_idx % 2 == 0 else None
            fill_cell(table.cell(start + r_idx, c_idx), row[c_idx] if c_idx < len(row) else '', bg=bg)

    if table_spec.get('caption'):
        _textbox(s, Inches(0.95), Inches(1.9 + 0.5 * row_count + 0.15), Inches(11.4), Inches(0.5),
                 table_spec['caption'], size=12, italic=True, color=theme['muted'])


def _quote_slide(prs, blank, slide, theme):
    s = _blank_slide(prs, blank, theme, fill=theme['soft'])
    _textbox(s, Inches(1.6), Inches(2.2), Inches(10.1), Inches(2.6),
             f"\u201C{slide.get('quote') or slide.get('title') or ''}\u201D",
             size=28, italic=True, color=theme['accent'], align=PP_ALIGN.CENTER if PP_ALIGN else None)
    if slide.get('cite'):
        _textbox(s, Inches(1.6), Inches(5.0), Inches(10.1), Inches(0.6),
                 f"— {slide['cite']}", size=15, color=theme['muted'], align=PP_ALIGN.CENTER if PP_ALIGN else None)


def _closing_slide(prs, blank, slide, theme):
    s = _blank_slide(prs, blank, theme, fill=theme['title_bg'])
    _textbox(s, Inches(1.0), Inches(2.8), Inches(11.3), Inches(1.6),
             slide.get('title') or 'Thank You', size=40, bold=True, color='FFFFFF', align=PP_ALIGN.CENTER if PP_ALIGN else None)
    if slide.get('subtitle'):
        _textbox(s, Inches(1.0), Inches(4.4), Inches(11.3), Inches(0.8),
                 slide['subtitle'], size=18, color='D6E2E7', align=PP_ALIGN.CENTER if PP_ALIGN else None)


def _callout(slide, theme, text):
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(5.75), Inches(11.4), Inches(0.95))
    shape.fill.solid()
    shape.fill.fore_color.rgb = _rgb(theme['soft'])
    shape.line.color.rgb = _rgb(theme['accent'])
    shape.shadow.inherit = False
    frame = shape.text_frame
    frame.word_wrap = True
    para = frame.paragraphs[0]
    para.text = text
    for run in para.runs:
        run.font.size = Pt(14)
        run.font.name = 'Calibri'
        run.font.color.rgb = _rgb(theme['text'])
