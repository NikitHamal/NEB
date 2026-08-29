"""High-fidelity DOCX renderer.

Produces submission-ready Word documents: A4 page setup, a real title page for
formal types, styled heading hierarchy, bordered tables with shaded headers,
monospaced code blocks, centred formulas, an optional auto-updating table of
contents, running headers and PAGE-numbered footers.

This is deliberately not a text dump — the output is meant to be handed in as-is.
"""

import io

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

from . import images
from .. import docspec

ACCENT = '1F4E5F'
ACCENT_SOFT = 'EAF1F4'
CODE_BG = 'F4F5F7'
QUOTE_BAR = 'B0B7BE'
MUTED = '5A6470'

MONO_FONT = 'Consolas'


USABLE_WIDTH_MM = 160.0


def render(spec, safe_name='document', base_path=None):
    """Render a normalized document spec to .docx bytes."""
    spec = docspec.normalize_spec(spec)
    images.resolve(spec, base_path)
    doc = Document()
    options = spec.get('options') or {}
    font_name = options.get('font') or 'Times New Roman'
    font_size = int(options.get('font_size') or 12)

    _setup_page(doc, options)
    _setup_styles(doc, font_name, font_size, options)
    _add_footer(doc, options)
    if options.get('header'):
        _add_header(doc, options['header'])

    if options.get('title_page'):
        _add_title_page(doc, spec, font_name)
        if options.get('toc'):
            _add_toc(doc, font_name)
        if spec.get('acknowledgement'):
            _add_acknowledgement(doc, spec, font_name)
        if spec.get('abstract'):
            _add_abstract(doc, spec, font_name)
        _start_body(doc, options)
    elif options.get('toc'):
        _add_toc(doc, font_name)

    _render_sections(doc, spec, font_name)
    if spec.get('references'):
        _render_references(doc, spec, font_name)

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


# --------------------------------------------------------------------------
# Page + style setup
# --------------------------------------------------------------------------

def _setup_page(doc, options):
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.left_margin = Mm(25)
    section.right_margin = Mm(25)
    section.top_margin = Mm(22)
    section.bottom_margin = Mm(22)
    section.header_distance = Mm(12)
    section.footer_distance = Mm(12)


def _setup_styles(doc, font_name, font_size, options):
    normal = doc.styles['Normal']
    normal.font.name = font_name
    normal.font.size = Pt(font_size)
    normal.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(attr), font_name)
    normal.paragraph_format.line_spacing = float(options.get('line_spacing') or 1.15)
    normal.paragraph_format.space_after = Pt(6)

    sizes = {1: font_size + 6, 2: font_size + 4, 3: font_size + 2, 4: font_size + 1}
    for level, size in sizes.items():
        try:
            style = doc.styles[f'Heading {level}']
        except KeyError:
            continue
        style.font.name = font_name
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(ACCENT if level <= 2 else '2E3740')
        style.paragraph_format.space_before = Pt(14 if level <= 2 else 10)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.keep_with_next = True
        srp = style.element.get_or_add_rPr()
        sfonts = srp.find(qn('w:rFonts'))
        if sfonts is None:
            sfonts = OxmlElement('w:rFonts')
            srp.append(sfonts)
        for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            sfonts.set(qn(attr), font_name)


def _add_footer(doc, options):
    if not options.get('page_numbers', True):
        return
    for section in doc.sections:
        paragraph = section.footer.paragraphs[0] if section.footer.paragraphs else section.footer.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run()
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(MUTED)
        _field(paragraph, 'PAGE')


def _add_header(doc, text):
    for section in doc.sections:
        paragraph = section.header.paragraphs[0] if section.header.paragraphs else section.header.add_paragraph()
        paragraph.text = ''
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(text)
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor.from_string(MUTED)
        run.italic = True


def _field(paragraph, instruction):
    """Insert a Word field (PAGE / TOC) that Word refreshes on open."""
    run = paragraph.add_run()
    begin = OxmlElement('w:fldChar')
    begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = instruction
    end = OxmlElement('w:fldChar')
    end.set(qn('w:fldCharType'), 'end')
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)
    return run


def _add_toc(doc, font_name):
    heading = doc.add_paragraph('Table of Contents', style='Heading 1')
    heading.paragraph_format.space_after = Pt(10)

    paragraph = doc.add_paragraph()
    run = paragraph.add_run()
    begin = OxmlElement('w:fldChar')
    begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = r'TOC \o "1-3" \h \z \u'
    separate = OxmlElement('w:fldChar')
    separate.set(qn('w:fldCharType'), 'separate')
    placeholder = OxmlElement('w:t')
    placeholder.text = 'Right-click and choose "Update Field" to build the table of contents.'
    end = OxmlElement('w:fldChar')
    end.set(qn('w:fldCharType'), 'end')
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(separate)
    run._r.append(placeholder)
    run._r.append(end)
    doc.add_page_break()


# --------------------------------------------------------------------------
# Front matter
# --------------------------------------------------------------------------

def _add_title_page(doc, spec, font_name):
    institution = spec.get('institution') or ''
    if institution:
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(institution.upper())
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor.from_string(ACCENT)
        para.paragraph_format.space_after = Pt(4)

    subject = spec.get('subject') or ''
    if subject:
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(subject)
        run.italic = True
        run.font.size = Pt(12)
        para.paragraph_format.space_after = Pt(18)

    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(spec.get('title') or 'Untitled')
    run.bold = True
    run.font.size = Pt(22)
    run.font.color.rgb = RGBColor.from_string(ACCENT)
    para.paragraph_format.space_before = Pt(10)
    para.paragraph_format.space_after = Pt(6)

    if spec.get('subtitle'):
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(spec['subtitle'])
        run.font.size = Pt(13)
        run.italic = True
        run.font.color.rgb = RGBColor.from_string(MUTED)
        para.paragraph_format.space_after = Pt(28)

    rows = []
    if spec.get('author'):
        rows.append(('Submitted by', spec['author'] + (f"  (Roll No: {spec['roll_no']})" if spec.get('roll_no') else '')))
    if spec.get('grade'):
        rows.append(('Class / Grade', spec['grade']))
    if spec.get('teacher'):
        label = 'Submitted to' if spec.get('doc_type') in ('assignment', 'lab_report', 'project_report') else 'Supervisor'
        rows.append((label, spec['teacher']))
    if spec.get('institution'):
        rows.append(('Institution', spec['institution']))
    if spec.get('date'):
        rows.append(('Date', spec['date']))

    if rows:
        table = doc.add_table(rows=len(rows), cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = 'Table Grid'
        for idx, (label, value) in enumerate(rows):
            label_cell, value_cell = table.rows[idx].cells
            label_cell.text = ''
            run = label_cell.paragraphs[0].add_run(label)
            run.bold = True
            run.font.size = Pt(11)
            value_cell.text = ''
            run = value_cell.paragraphs[0].add_run(value)
            run.font.size = Pt(11)
            _shade(label_cell, ACCENT_SOFT)
            label_cell.width = Mm(45)
            value_cell.width = Mm(85)
        doc.add_paragraph()
    doc.add_page_break()


def _add_acknowledgement(doc, spec, font_name):
    doc.add_paragraph('Acknowledgement', style='Heading 1')
    for line in [l for l in str(spec['acknowledgement']).split('\n') if l.strip()]:
        doc.add_paragraph(line.strip())
    doc.add_page_break()


def _add_abstract(doc, spec, font_name):
    doc.add_paragraph('Abstract', style='Heading 1')
    for line in [l for l in str(spec['abstract']).split('\n') if l.strip()]:
        para = doc.add_paragraph(line.strip())
        para.paragraph_format.left_indent = Mm(10)
        para.paragraph_format.right_indent = Mm(10)


def _start_body(doc, options):
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.left_margin = Mm(25)
    section.right_margin = Mm(25)
    section.top_margin = Mm(22)
    section.bottom_margin = Mm(22)
    _add_footer(doc, options)
    if options.get('header'):
        _add_header(doc, options['header'])


# --------------------------------------------------------------------------
# Body
# --------------------------------------------------------------------------

def _render_sections(doc, spec, font_name):
    first = True
    for section in spec.get('sections') or []:
        heading = section.get('heading')
        if heading:
            level = max(1, min(4, int(section.get('level') or 1)))
            if level == 1 and not first:
                doc.add_page_break()
            doc.add_heading(heading, level=level)
        first = False
        for block in section.get('blocks') or []:
            _render_block(doc, block)


def _render_block(doc, block):
    btype = block.get('type')

    if btype == 'paragraph':
        doc.add_paragraph(block.get('text') or '')

    elif btype == 'bullets':
        for item in block.get('items') or []:
            para = doc.add_paragraph(item, style='List Bullet')
            para.paragraph_format.space_after = Pt(3)

    elif btype == 'numbered':
        for item in block.get('items') or []:
            para = doc.add_paragraph(item, style='List Number')
            para.paragraph_format.space_after = Pt(3)

    elif btype == 'table':
        _render_table(doc, block)

    elif btype == 'code':
        _render_code(doc, block)

    elif btype == 'quote':
        para = doc.add_paragraph()
        para.paragraph_format.left_indent = Mm(12)
        para.paragraph_format.right_indent = Mm(8)
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run(f"\u201C{block.get('text') or ''}\u201D")
        run.italic = True
        run.font.color.rgb = RGBColor.from_string(MUTED)
        _left_bar(para, QUOTE_BAR)
        if block.get('cite'):
            cite = doc.add_paragraph()
            cite.paragraph_format.left_indent = Mm(12)
            run = cite.add_run(f"— {block['cite']}")
            run.italic = True
            run.font.size = Pt(10)

    elif btype == 'formula':
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_before = Pt(8)
        para.paragraph_format.space_after = Pt(8)
        run = para.add_run(block.get('latex') or '')
        run.font.name = 'Cambria Math'
        run.italic = True
        run.font.size = Pt(12)

    elif btype == 'steps':
        for idx, item in enumerate(block.get('items') or [], start=1):
            para = doc.add_paragraph(style='List Number')
            run = para.add_run(item.get('title') or '')
            run.bold = True
            if item.get('title') and item.get('detail'):
                para.add_run(' — ')
            if item.get('detail'):
                para.add_run(item['detail'])

    elif btype == 'callout':
        _render_callout(doc, block)

    elif btype == 'definition':
        para = doc.add_paragraph()
        run = para.add_run(block.get('term') or '')
        run.bold = True
        if block.get('text'):
            para.add_run(f" — {block['text']}")

    elif btype == 'image_caption':
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(block.get('text') or '')
        run.italic = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor.from_string(MUTED)

    elif btype == 'image':
        _render_image(doc, block)

    elif btype == 'divider':
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.add_run('—' * 30)


def _render_image(doc, block):
    if not images.rasterize(block):
        _render_image_caption(doc, block, missing=True)
        return
    raw = block.get('_bytes')
    if not raw:
        return
    width_px, height_px = images.block_dimensions(block)
    ratio = (float(height_px) / float(width_px)) if width_px else 0.66
    target = max(30.0, min(USABLE_WIDTH_MM, USABLE_WIDTH_MM * float(block.get('width') or 80) / 100.0))

    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(8)
    para.paragraph_format.space_after = Pt(4)
    try:
        para.add_run().add_picture(io.BytesIO(raw), width=Mm(target), height=Mm(target * ratio))
    except Exception:
        _render_image_caption(doc, block, missing=True)
        return
    _render_image_caption(doc, block)


def _render_image_caption(doc, block, missing=False):
    text = block.get('caption') or ''
    if missing:
        text = text or f"[Figure could not be embedded: {block.get('path') or 'image'}]"
    if not text:
        return
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text)
    run.italic = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string(MUTED)
    para.paragraph_format.space_after = Pt(10)


def _render_table(doc, block):
    header = block.get('header') or []
    rows = block.get('rows') or []
    col_count = max([len(header)] + [len(r) for r in rows]) if (header or rows) else 0
    if not col_count:
        return

    if block.get('caption'):
        cap = doc.add_paragraph()
        run = cap.add_run(block['caption'])
        run.bold = True
        run.font.size = Pt(10)
        cap.paragraph_format.space_after = Pt(2)

    table = doc.add_table(rows=1, cols=col_count)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    if header:
        for idx in range(col_count):
            cell = table.rows[0].cells[idx]
            cell.text = ''
            run = cell.paragraphs[0].add_run(str(header[idx] if idx < len(header) else ''))
            run.bold = True
            run.font.size = Pt(10)
            _shade(cell, ACCENT_SOFT)
        offset = 1
    else:
        table.rows[0]._element.getparent().remove(table.rows[0]._element)
        offset = 0

    for row in rows:
        cells = table.add_row().cells
        for idx in range(col_count):
            cell = cells[idx]
            cell.text = ''
            run = cell.paragraphs[0].add_run(str(row[idx] if idx < len(row) else ''))
            run.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _render_code(doc, block):
    text = block.get('text') or ''
    if not text.strip():
        return
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    cell = table.rows[0].cells[0]
    cell.text = ''
    _shade(cell, CODE_BG)
    for idx, line in enumerate(text.split('\n')):
        para = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        para.paragraph_format.space_after = Pt(0)
        para.paragraph_format.line_spacing = 1.0
        run = para.add_run(line if line.strip() else ' ')
        run.font.name = MONO_FONT
        run.font.size = Pt(9)
        rpr = run._element.get_or_add_rPr()
        rfonts = rpr.find(qn('w:rFonts'))
        if rfonts is None:
            rfonts = OxmlElement('w:rFonts')
            rpr.append(rfonts)
        for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
            rfonts.set(qn(attr), MONO_FONT)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _render_callout(doc, block):
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    cell = table.rows[0].cells[0]
    cell.text = ''
    _shade(cell, ACCENT_SOFT)
    para = cell.paragraphs[0]
    label = block.get('label') or 'Note'
    run = para.add_run(f'{label}: ')
    run.bold = True
    run.font.color.rgb = RGBColor.from_string(ACCENT)
    para.add_run(block.get('text') or '')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _render_references(doc, spec, font_name):
    doc.add_page_break()
    doc.add_heading('References', level=1)
    for idx, ref in enumerate(spec.get('references') or [], start=1):
        para = doc.add_paragraph()
        para.paragraph_format.left_indent = Mm(10)
        para.paragraph_format.first_line_indent = Mm(-10)
        para.paragraph_format.space_after = Pt(4)
        run = para.add_run(f'[{idx}] ')
        run.bold = True
        para.add_run(ref.get('text') or '')
        if ref.get('url'):
            url_run = para.add_run(f" {ref['url']}")
            url_run.font.size = Pt(9)
            url_run.font.color.rgb = RGBColor.from_string(MUTED)


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------

def _shade(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)


def _left_bar(paragraph, hex_color):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '18')
    left.set(qn('w:space'), '8')
    left.set(qn('w:color'), hex_color)
    borders.append(left)
    p_pr.append(borders)
