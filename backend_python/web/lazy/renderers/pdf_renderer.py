"""PDF renderer built from the document spec (not from scraped HTML).

Uses ReportLab platypus so tables, headings, code blocks and page furniture are
laid out properly rather than flattened into a text flow.
"""

import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, ListFlowable, ListItem,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

from . import images
from .. import docspec

ACCENT = colors.HexColor('#1F4E5F')
ACCENT_SOFT = colors.HexColor('#EAF1F4')
MUTED = colors.HexColor('#5A6470')
CODE_BG = colors.HexColor('#F4F5F7')
GRID = colors.HexColor('#C9D2D8')


USABLE_WIDTH_MM = 160.0
# A4 minus the 22 mm top and bottom margins.
USABLE_HEIGHT_MM = 253.0
# A figure is scaled to fit the text column by width, but a tall diagram scaled
# that way can end up taller than the frame itself. ReportLab refuses to place
# such a flowable and raises LayoutError, which used to abort the entire PDF
# render — so the agent saw no PDF at all and rebuilt the whole document.
# Capping height here and shrinking width to match keeps the aspect ratio and
# keeps the page layoutable.
MAX_FIGURE_HEIGHT_MM = 115.0


def render(spec, safe_name='document', base_path=None):
    spec = docspec.normalize_spec(spec)
    images.resolve(spec, base_path)
    options = spec.get('options') or {}
    font = options.get('font') or 'Times New Roman'
    size = int(options.get('font_size') or 12)

    buffer = io.BytesIO()
    doc = BaseDocTemplate(
        buffer, pagesize=A4,
        leftMargin=25 * mm, rightMargin=25 * mm,
        topMargin=22 * mm, bottomMargin=22 * mm,
        title=spec.get('title') or 'Document',
        author=spec.get('author') or '',
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='body')
    show_numbers = bool(options.get('page_numbers', True))
    doc.addPageTemplates([
        PageTemplate(id='main', frames=[frame], onPage=_make_decorator(show_numbers))
    ])

    styles = _styles(font, size, options)
    story = []

    if options.get('title_page'):
        story.extend(_front_matter(spec, styles))
        if spec.get('acknowledgement'):
            story.extend(_block_title('Acknowledgement', styles))
            story.extend(_paragraphs(spec['acknowledgement'], styles))
            story.append(PageBreak())
        if spec.get('abstract'):
            story.extend(_block_title('Abstract', styles))
            story.extend(_paragraphs(spec['abstract'], styles))
        if options.get('toc'):
            story.extend(_toc(spec, styles))
        story.append(PageBreak())

    for section in spec.get('sections') or []:
        story.extend(_render_section(section, styles))

    if spec.get('references'):
        story.append(PageBreak())
        story.extend(_block_title('References', styles))
        for idx, ref in enumerate(spec['references'], start=1):
            text = ref.get('text') or ''
            if ref.get('url'):
                text += f"  <font color='#5A6470'>{ref['url']}</font>"
            story.append(Paragraph(f'[{idx}] {_esc(text)}', styles['ref']))
            story.append(Spacer(1, 4))

    doc.build(story)
    return buffer.getvalue()


def _make_decorator(show_numbers):
    def decorate(canvas, doc):
        canvas.saveState()
        if show_numbers:
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(MUTED)
            canvas.drawCentredString(A4[0] / 2.0, 12 * mm, str(canvas.getPageNumber()))
        canvas.restoreState()
    return decorate


def _styles(font, size, options):
    base = getSampleStyleSheet()
    spacing = float(options.get('line_spacing') or 1.15)
    return {
        'title': ParagraphStyle('lzTitle', parent=base['Title'], fontName='Helvetica-Bold',
                                fontSize=size + 10, leading=size + 14, textColor=ACCENT, spaceAfter=8),
        'subtitle': ParagraphStyle('lzSub', parent=base['Normal'], fontName='Helvetica-Oblique',
                                   fontSize=size + 1, leading=size + 5, textColor=MUTED, alignment=TA_CENTER),
        'inst': ParagraphStyle('lzInst', parent=base['Normal'], fontName='Helvetica-Bold',
                               fontSize=size + 3, leading=size + 7, textColor=ACCENT, alignment=TA_CENTER),
        'kind': ParagraphStyle('lzKind', parent=base['Normal'], fontName='Helvetica',
                               fontSize=size, leading=size + 4, textColor=MUTED, alignment=TA_CENTER, spaceAfter=10),
        'h1': ParagraphStyle('lzH1', parent=base['Heading1'], fontName='Helvetica-Bold',
                             fontSize=size + 5, leading=size + 9, textColor=ACCENT,
                             spaceBefore=14, spaceAfter=6),
        'h2': ParagraphStyle('lzH2', parent=base['Heading2'], fontName='Helvetica-Bold',
                             fontSize=size + 3, leading=size + 7, textColor=ACCENT,
                             spaceBefore=12, spaceAfter=5),
        'h3': ParagraphStyle('lzH3', parent=base['Heading3'], fontName='Helvetica-Bold',
                             fontSize=size + 1, leading=size + 5, textColor=colors.HexColor('#2E3740'),
                             spaceBefore=10, spaceAfter=4),
        'h4': ParagraphStyle('lzH4', parent=base['Heading4'], fontName='Helvetica-Bold',
                             fontSize=size, leading=size + 4, textColor=colors.HexColor('#2E3740'),
                             spaceBefore=8, spaceAfter=3),
        'body': ParagraphStyle('lzBody', parent=base['Normal'], fontName='Helvetica',
                               fontSize=size, leading=size * spacing + 2,
                               alignment=TA_JUSTIFY, spaceAfter=6),
        'bullet': ParagraphStyle('lzBullet', parent=base['Normal'], fontName='Helvetica',
                                 fontSize=size, leading=size * spacing + 2, spaceAfter=2),
        'code': ParagraphStyle('lzCode', parent=base['Normal'], fontName='Courier',
                               fontSize=size - 2, leading=size, backColor=CODE_BG,
                               borderPadding=5, spaceBefore=4, spaceAfter=8),
        'quote': ParagraphStyle('lzQuote', parent=base['Normal'], fontName='Helvetica-Oblique',
                                fontSize=size, leading=size * spacing + 2, textColor=MUTED,
                                leftIndent=12 * mm, rightIndent=8 * mm, spaceBefore=4, spaceAfter=6),
        'formula': ParagraphStyle('lzFormula', parent=base['Normal'], fontName='Courier-Bold',
                                  fontSize=size, leading=size + 6, alignment=TA_CENTER,
                                  spaceBefore=6, spaceAfter=6),
        'caption': ParagraphStyle('lzCap', parent=base['Normal'], fontName='Helvetica-Bold',
                                  fontSize=9, leading=12, textColor=MUTED, spaceAfter=3),
        'cell': ParagraphStyle('lzCell', parent=base['Normal'], fontName='Helvetica',
                               fontSize=9, leading=12),
        'cellHead': ParagraphStyle('lzCellHead', parent=base['Normal'], fontName='Helvetica-Bold',
                                   fontSize=9, leading=12, textColor=colors.white),
        'ref': ParagraphStyle('lzRef', parent=base['Normal'], fontName='Helvetica',
                              fontSize=size - 1, leading=size + 2, leftIndent=10,
                              firstLineIndent=-10, spaceAfter=4),
        'note': ParagraphStyle('lzNote', parent=base['Normal'], fontName='Helvetica',
                               fontSize=size, leading=size * spacing + 2, spaceAfter=6),
    }


def _esc(text):
    return (str(text or '')
            .replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def _front_matter(spec, styles):
    out = []
    if spec.get('institution'):
        out.append(Paragraph(_esc(str(spec['institution']).upper()), styles['inst']))
        out.append(Spacer(1, 4))
    if spec.get('subject'):
        out.append(Paragraph(_esc(spec['subject']), styles['subtitle']))
        out.append(Spacer(1, 14))
    out.append(Paragraph(_esc(spec.get('title') or 'Untitled'), styles['title']))
    if spec.get('subtitle'):
        out.append(Paragraph(_esc(spec['subtitle']), styles['subtitle']))
    out.append(Spacer(1, 18))

    rows = []
    if spec.get('author'):
        rows.append(('Submitted by', spec['author'] + (f" (Roll No: {spec['roll_no']})" if spec.get('roll_no') else '')))
    if spec.get('grade'):
        rows.append(('Class / Grade', spec['grade']))
    if spec.get('teacher'):
        rows.append(('Submitted to', spec['teacher']))
    if spec.get('institution'):
        rows.append(('Institution', spec['institution']))
    if spec.get('date'):
        rows.append(('Date', spec['date']))

    if rows:
        data = [[Paragraph(f'<b>{_esc(k)}</b>', styles['cell']), Paragraph(_esc(v), styles['cell'])] for k, v in rows]
        table = Table(data, colWidths=[45 * mm, 90 * mm])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, GRID),
            ('BACKGROUND', (0, 0), (0, -1), ACCENT_SOFT),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        out.append(table)
    return out


def _toc(spec, styles):
    out = [Paragraph('Table of Contents', styles['h1'])]
    for idx, section in enumerate(spec.get('sections') or [], start=1):
        out.append(Paragraph(f'{idx}. {_esc(section.get("heading") or "")}', styles['note']))
    return out


def _block_title(text, styles):
    return [Paragraph(_esc(text), styles['h1'])]


def _paragraphs(text, styles):
    return [Paragraph(_esc(line.strip()), styles['body'])
            for line in str(text or '').split('\n') if line.strip()]


def _render_section(section, styles):
    out = []
    heading = section.get('heading')
    if heading:
        level = max(1, min(4, int(section.get('level') or 1)))
        out.append(Paragraph(_esc(heading), styles[f'h{level}']))
    for block in section.get('blocks') or []:
        out.extend(_render_block(block, styles))
    return out


def _render_block(block, styles):
    btype = block.get('type')

    if btype == 'paragraph':
        return _paragraphs(block.get('text') or '', styles)

    if btype in ('bullets', 'numbered'):
        items = block.get('items') or []
        if not items:
            return []
        flowables = [Paragraph(_esc(i), styles['bullet']) for i in items]
        return [ListFlowable(
            [ListItem(f, leftIndent=12) for f in flowables],
            bulletType='bullet' if btype == 'bullets' else '1',
            start='•' if btype == 'bullets' else '1',
        ), Spacer(1, 6)]

    if btype == 'table':
        return _render_table(block, styles)

    if btype == 'code':
        lines = str(block.get('text') or '').split('\n')
        body = '<br/>'.join(_esc(l).replace(' ', '&nbsp;') or '&nbsp;' for l in lines)
        return [Paragraph(body, styles['code'])]

    if btype == 'quote':
        text = f"\u201C{_esc(block.get('text') or '')}\u201D"
        if block.get('cite'):
            text += f"<br/><font size=9>— {_esc(block['cite'])}</font>"
        return [Paragraph(text, styles['quote'])]

    if btype == 'formula':
        return [Paragraph(_esc(block.get('latex') or ''), styles['formula'])]

    if btype == 'steps':
        items = block.get('items') or []
        if not items:
            return []
        out = []
        for item in items:
            text = ''
            if item.get('title'):
                text += f"<b>{_esc(item['title'])}</b>"
            if item.get('detail'):
                text += (' — ' if text else '') + _esc(item['detail'])
            out.append(Paragraph(text, styles['bullet']))
        return [ListFlowable([ListItem(f, leftIndent=12) for f in out], bulletType='1', start='1'), Spacer(1, 6)]

    if btype == 'callout':
        label = block.get('label') or 'Note'
        data = [[Paragraph(f'<b>{_esc(label)}:</b> {_esc(block.get("text") or "")}', styles['note'])]]
        table = Table(data, colWidths=[160 * mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), ACCENT_SOFT),
            ('BOX', (0, 0), (-1, -1), 0.5, ACCENT),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        return [table, Spacer(1, 8)]

    if btype == 'definition':
        text = f"<b>{_esc(block.get('term') or '')}</b> — {_esc(block.get('text') or '')}"
        return [Paragraph(text, styles['body'])]

    if btype == 'image_caption':
        return [Paragraph(_esc(block.get('text') or ''), styles['caption'])]

    if btype == 'image':
        return _render_image(block, styles)

    if btype == 'divider':
        return [Spacer(1, 6), Paragraph('—' * 40, styles['caption'])]

    return _paragraphs(block.get('text') or '', styles)


def _render_image(block, styles):
    if not images.rasterize(block):
        text = block.get('caption') or f"[Figure unavailable: {block.get('path') or 'image'}]"
        return [Paragraph(_esc(text), styles['caption']), Spacer(1, 8)]

    raw = block.get('_bytes')
    if not raw:
        return []

    width_px, height_px = images.block_dimensions(block)
    ratio = (float(height_px) / float(width_px)) if width_px else 0.66
    target = max(30.0, min(USABLE_WIDTH_MM, USABLE_WIDTH_MM * float(block.get('width') or 80) / 100.0))

    height = target * ratio
    if height > MAX_FIGURE_HEIGHT_MM:
        height = MAX_FIGURE_HEIGHT_MM
        target = (height / ratio) if ratio else target
    if height > USABLE_HEIGHT_MM:
        height = USABLE_HEIGHT_MM
        target = (height / ratio) if ratio else target

    try:
        flowable = Image(io.BytesIO(raw), width=target * mm, height=height * mm)
    except Exception:
        text = block.get('caption') or f"[Figure unavailable: {block.get('path') or 'image'}]"
        return [Paragraph(_esc(text), styles['caption']), Spacer(1, 8)]

    flowable.hAlign = str(block.get('align') or 'CENTER').upper()
    out = [Spacer(1, 6), flowable]
    if block.get('caption'):
        out.append(Spacer(1, 3))
        out.append(Paragraph(_esc(block['caption']), styles['caption']))
    out.append(Spacer(1, 8))
    return out


def _render_table(block, styles):
    header = block.get('header') or []
    rows = block.get('rows') or []
    cols = max([len(header)] + [len(r) for r in rows]) if (header or rows) else 0
    if not cols:
        return []

    out = []
    if block.get('caption'):
        out.append(Paragraph(_esc(block['caption']), styles['caption']))

    available = 160 * mm
    col_width = available / cols
    data = []
    if header:
        data.append([Paragraph(_esc(header[i] if i < len(header) else ''), styles['cellHead']) for i in range(cols)])
    for row in rows:
        data.append([Paragraph(_esc(row[i] if i < len(row) else ''), styles['cell']) for i in range(cols)])

    table = Table(data, colWidths=[col_width] * cols, repeatRows=1 if header else 0)
    style = [
        ('GRID', (0, 0), (-1, -1), 0.4, GRID),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    if header:
        style.append(('BACKGROUND', (0, 0), (-1, 0), ACCENT))
    table.setStyle(TableStyle(style))
    out.append(table)
    out.append(Spacer(1, 10))
    return out
