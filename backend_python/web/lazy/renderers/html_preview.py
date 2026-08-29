"""HTML preview renderer for the in-app document panel.

Renders a document spec to semantic HTML so the workspace can show a faithful
preview of exactly what the exported .docx / .pdf will contain. Uses `lzdoc-*`
classes so styling lives in CSS rather than inline attributes.
"""

from html import escape

from . import images
from .. import docspec

DOC_TYPE_LABELS = {
    'assignment': 'Assignment',
    'lab_report': 'Lab Report',
    'research_paper': 'Research Paper',
    'essay': 'Essay',
    'report': 'Report',
    'project_report': 'Project Report',
    'cv': 'Curriculum Vitae',
    'resume': 'Resume',
    'letter': 'Letter',
    'notes': 'Notes',
    'thesis': 'Thesis',
    'business_report': 'Business Report',
    'case_study': 'Case Study',
    'article': 'Article',
    'speech': 'Speech',
    'generic': 'Document',
}


def render(spec, default_title='Untitled Document', base_path=None):
    spec = docspec.normalize_spec(spec, default_title)
    images.resolve(spec, base_path)
    parts = ['<div class="lzdoc">']

    options = spec.get('options') or {}
    if options.get('title_page'):
        parts.append(_front_matter(spec))

    parts.append('<div class="lzdoc-body">')
    for section in spec.get('sections') or []:
        parts.append(_render_section(section))
    parts.append('</div>')

    if spec.get('references'):
        parts.append(_render_references(spec))

    parts.append('</div>')
    return '\n'.join(p for p in parts if p)


def _front_matter(spec):
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

    html = ['<header class="lzdoc-front">']
    if spec.get('institution'):
        html.append(f'<div class="lzdoc-inst">{escape(spec["institution"])}</div>')
    if spec.get('subject'):
        html.append(f'<div class="lzdoc-subject">{escape(spec["subject"])}</div>')

    label = DOC_TYPE_LABELS.get(spec.get('doc_type'), 'Document')
    html.append(f'<div class="lzdoc-kind">{escape(label)}</div>')
    html.append(f'<h1 class="lzdoc-title">{escape(spec["title"])}</h1>')
    if spec.get('subtitle'):
        html.append(f'<p class="lzdoc-subtitle">{escape(spec["subtitle"])}</p>')

    if rows:
        html.append('<table class="lzdoc-meta"><tbody>')
        for label_text, value in rows:
            html.append(
                f'<tr><th>{escape(label_text)}</th><td>{escape(value)}</td></tr>'
            )
        html.append('</tbody></table>')

    if spec.get('acknowledgement'):
        html.append('<section class="lzdoc-ack"><h2>Acknowledgement</h2>')
        html.append(_paragraphs(spec['acknowledgement']))
        html.append('</section>')

    if spec.get('abstract'):
        html.append('<section class="lzdoc-abstract"><h2>Abstract</h2>')
        html.append(_paragraphs(spec['abstract']))
        html.append('</section>')

    html.append('</header>')
    return '\n'.join(html)


def _paragraphs(text):
    return '\n'.join(
        f'<p>{escape(line.strip())}</p>'
        for line in str(text or '').split('\n') if line.strip()
    )


def _render_section(section):
    out = []
    heading = section.get('heading')
    if heading:
        level = max(1, min(4, int(section.get('level') or 1)))
        out.append(f'<h{level}>{escape(heading)}</h{level}>')
    for block in section.get('blocks') or []:
        out.append(_render_block(block))
    return '\n'.join(out)


def _render_block(block):
    btype = block.get('type')

    if btype == 'paragraph':
        return _paragraphs(block.get('text') or '')

    if btype == 'bullets':
        items = ''.join(f'<li>{escape(i)}</li>' for i in block.get('items') or [])
        return f'<ul>{items}</ul>' if items else ''

    if btype == 'numbered':
        items = ''.join(f'<li>{escape(i)}</li>' for i in block.get('items') or [])
        return f'<ol>{items}</ol>' if items else ''

    if btype == 'table':
        return _render_table(block)

    if btype == 'code':
        text = escape(block.get('text') or '')
        lang = escape(block.get('language') or '')
        return f'<pre class="lzdoc-code" data-lang="{lang}"><code>{text}</code></pre>'

    if btype == 'quote':
        cite = block.get('cite')
        cite_html = f'<cite>— {escape(cite)}</cite>' if cite else ''
        return f'<blockquote>{escape(block.get("text") or "")}{cite_html}</blockquote>'

    if btype == 'formula':
        return f'<div class="lzdoc-formula">{escape(block.get("latex") or "")}</div>'

    if btype == 'steps':
        items = []
        for item in block.get('items') or []:
            title = escape(item.get('title') or '')
            detail = escape(item.get('detail') or '')
            inner = f'<strong>{title}</strong>' if title else ''
            if title and detail:
                inner += ' — '
            inner += detail
            items.append(f'<li>{inner}</li>')
        return f'<ol class="lzdoc-steps">{"".join(items)}</ol>' if items else ''

    if btype == 'callout':
        label = escape(block.get('label') or 'Note')
        return f'<aside class="lzdoc-callout"><strong>{label}:</strong> {escape(block.get("text") or "")}</aside>'

    if btype == 'definition':
        term = escape(block.get('term') or '')
        return f'<p class="lzdoc-def"><strong>{term}</strong> — {escape(block.get("text") or "")}</p>'

    if btype == 'image_caption':
        return f'<figcaption>{escape(block.get("text") or "")}</figcaption>'

    if btype == 'image':
        data = images.b64(block)
        src = ''
        if data:
            mime = str(block.get('mime') or 'image/png')
            src = f'data:{mime};base64,{data}'
        elif block.get('path'):
            # A `rel:` marker means the file lives in the run workspace and the
            # agent frontend rewrites it to a real artifact URL.
            src = f'rel:{block["path"]}'
        if not src:
            return ''
        width = max(15.0, min(100.0, float(block.get('width') or 80)))
        align = str(block.get('align') or 'center')
        caption = block.get('caption') or ''
        style = f'width:{width:.0f}%;max-width:100%;height:auto;display:block;margin:0 auto;'
        figure = (
            f'<figure class="lzdoc-figure" style="text-align:{align};">'
            f'<img src="{escape(src)}" alt="{escape(block.get("alt") or caption or "Figure")}" '
            f'data-lazy-img="1" style="{style}"/>'
        )
        if caption:
            figure += f'<figcaption>{escape(caption)}</figcaption>'
        figure += '</figure>'
        return figure

    if btype == 'divider':
        return '<hr />'

    return _paragraphs(block.get('text') or '')


def _render_table(block):
    header = block.get('header') or []
    rows = block.get('rows') or []
    cols = max([len(header)] + [len(r) for r in rows]) if (header or rows) else 0
    if not cols:
        return ''

    out = []
    if block.get('caption'):
        out.append(f'<div class="lzdoc-tablecap">{escape(block["caption"])}</div>')
    out.append('<table><thead><tr>')
    for idx in range(cols):
        out.append(f'<th>{escape(header[idx] if idx < len(header) else "")}</th>')
    out.append('</tr></thead><tbody>')
    for row in rows:
        out.append('<tr>')
        for idx in range(cols):
            out.append(f'<td>{escape(row[idx] if idx < len(row) else "")}</td>')
        out.append('</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)


def _render_references(spec):
    out = ['<section class="lzdoc-refs"><h2>References</h2><ol>']
    for ref in spec.get('references') or []:
        url = ref.get('url')
        text = escape(ref.get('text') or '')
        if url:
            text += f' <a href="{escape(url)}" target="_blank" rel="noopener">{escape(url)}</a>'
        out.append(f'<li>{text}</li>')
    out.append('</ol></section>')
    return '\n'.join(out)
