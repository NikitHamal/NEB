"""Deterministic SVG diagram builder.

Documents and decks look dramatically better with a real figure, and students
routinely lose marks on hand-drawn ones. This module turns a small declarative
spec into clean, printable vector art with no third-party dependencies, so it
works on any host.

Every builder returns a standalone SVG string sized in points, ready to be saved
as an artifact or embedded in an HTML preview.
"""

import math
import re

from xml.sax.saxutils import escape as _xml_escape

# Palettes are deliberately print-safe: they survive a black-and-white printer
# because each step also differs in shape or position, not only in colour.
PALETTES = {
    'classic': ['#2563eb', '#0ea5e9', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6', '#10b981', '#64748b'],
    'warm': ['#dc2626', '#ea580c', '#d97706', '#ca8a04', '#65a30d', '#16a34a', '#0d9488', '#0891b2'],
    'cool': ['#1e40af', '#3b82f6', '#0ea5e9', '#06b6d4', '#0d9488', '#059669', '#4f46e5', '#7c3aed'],
    'mono': ['#1f2937', '#374151', '#4b5563', '#6b7280', '#9ca3af', '#d1d5db', '#111827', '#374151'],
}

# Single quotes inside the family list: the attribute itself is double-quoted,
# so nested double quotes would produce malformed XML.
FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
_CHAR_W = 0.56  # average glyph width as a fraction of font size


def _esc(text):
    return _xml_escape(str(text if text is not None else ''))


def _palette(name):
    return PALETTES.get(str(name or 'classic').lower(), PALETTES['classic'])


def _wrap(text, size, max_chars):
    """Greedy word wrap that also breaks over-long single words."""
    words = str(text or '').split()
    lines, current = [], ''
    for word in words:
        candidate = f'{current} {word}'.strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        while len(word) > max_chars:
            lines.append(word[:max_chars - 1] + '-')
            word = word[max_chars - 1:]
        current = word
    if current:
        lines.append(current)
    return lines or ['']


def _svg_open(width, height, title=''):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}" role="img" '
        f'aria-label="{_esc(title)}">'
        f'<title>{_esc(title)}</title>'
    )


def _text_block(x, y, lines, size, fill, anchor='middle', weight='500', line_height=None):
    """Render wrapped lines as <tspan> rows inside a single <text> element."""
    if not lines:
        return ''
    gap = line_height or int(size * 1.35)
    spans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else gap
        spans.append(f'<tspan x="{x:.1f}" dy="{dy}">{_esc(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{"".join(spans)}</text>'
    )


def _arrow_marker(color, marker_id):
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>'
    )


# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------

def _flow(spec, palette):
    """Vertical (or horizontal) box-and-arrow flow."""
    nodes = spec.get('nodes') or []
    if not nodes:
        return None
    horizontal = str(spec.get('direction', 'vertical')).lower().startswith('h')

    box_w, box_h = (170, 74) if horizontal else (260, 78)
    gap = 56
    pad_x, pad_y, top = 40, 34, 74

    if horizontal:
        width = pad_x * 2 + len(nodes) * box_w + (len(nodes) - 1) * gap
        height = top + box_h + pad_y
    else:
        width = pad_x * 2 + box_w
        height = top + len(nodes) * box_h + (len(nodes) - 1) * gap + pad_y

    parts = [_svg_open(width, height, spec.get('title') or 'Process flow')]
    parts.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')
    title = spec.get('title')
    if title:
        parts.append(_text_block(width / 2, 40, _wrap(title, 20, 60), 20, '#0f172a', weight='700'))
    parts.append(_arrow_marker('#94a3b8', 'arrow'))

    positions = []
    for index, node in enumerate(nodes):
        if horizontal:
            x = pad_x + index * (box_w + gap)
            y = top
        else:
            x = (width - box_w) / 2
            y = top + index * (box_h + gap)
        positions.append((x, y, box_w, box_h))

        color = palette[index % len(palette)]
        label = node.get('label') or node.get('text') or f'Step {index + 1}'
        sub = node.get('sub') or node.get('detail') or ''
        radius = 12
        parts.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="{radius}" '
            f'fill="{color}" opacity="0.10"/>'
        )
        parts.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="{radius}" '
            f'fill="none" stroke="{color}" stroke-width="2"/>'
        )
        label_lines = _wrap(label, 14, int(box_w / (14 * _CHAR_W)) - 2)
        sub_lines = _wrap(sub, 11, int(box_w / (11 * _CHAR_W)) - 2) if sub else []
        total = len(label_lines) * 19 + (len(sub_lines) * 15 if sub_lines else 0)
        cursor = y + box_h / 2 - total / 2 + 14
        parts.append(_text_block(x + box_w / 2, cursor, label_lines, 14, '#0f172a', weight='600'))
        if sub_lines:
            parts.append(_text_block(
                x + box_w / 2, cursor + len(label_lines) * 19 + 4, sub_lines, 11, '#475569', weight='400',
            ))

    for index in range(len(positions) - 1):
        x1, y1, w1, h1 = positions[index]
        x2, y2, w2, h2 = positions[index + 1]
        if horizontal:
            sx, sy, ex, ey = x1 + w1, y1 + h1 / 2, x2 - 3, y2 + h2 / 2
        else:
            sx, sy, ex, ey = x1 + w1 / 2, y1 + h1, x2 + w2 / 2, y2 - 3
        parts.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>'
        )
    parts.append('</svg>')
    return ''.join(parts)


def _cycle(spec, palette):
    """Circular process — good for cycles, feedback loops, life cycles."""
    nodes = spec.get('nodes') or []
    if len(nodes) < 2:
        return None
    count = len(nodes)
    radius = max(150, 62 * count)
    cx = cy = radius + 130
    size = 2 * (radius + 130)
    node_r = max(46, min(74, int(2 * math.pi * radius / (count * 2.9))))

    parts = [_svg_open(size, size, spec.get('title') or 'Cycle')]
    parts.append(f'<rect width="{size}" height="{size}" fill="#ffffff"/>')
    title = spec.get('title')
    if title:
        parts.append(_text_block(size / 2, 44, _wrap(title, 20, 56), 20, '#0f172a', weight='700'))
    parts.append(_arrow_marker('#94a3b8', 'arrow'))

    points = []
    for index in range(count):
        angle = -math.pi / 2 + (2 * math.pi * index / count)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))

    for index, (px, py) in enumerate(points):
        nxt = points[(index + 1) % count]
        dx, dy = nxt[0] - px, nxt[1] - py
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist
        sx, sy = px + ux * node_r, py + uy * node_r
        ex, ey = nxt[0] - ux * (node_r + 6), nxt[1] - uy * (node_r + 6)
        parts.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>'
        )

    for index, (px, py) in enumerate(points):
        color = palette[index % len(palette)]
        node = nodes[index] or {}
        label = node.get('label') or node.get('text') or f'Step {index + 1}'
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{node_r}" fill="{color}" opacity="0.12"/>')
        parts.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{node_r}" fill="none" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        lines = _wrap(label, 12, max(8, int(node_r / (12 * _CHAR_W))))
        start_y = py - (len(lines) - 1) * 8
        parts.append(_text_block(px, start_y + 4, lines, 12, '#0f172a', weight='600'))
    parts.append('</svg>')
    return ''.join(parts)


def _mindmap(spec, palette):
    """Central topic with radial branches and optional sub-leaves."""
    center = spec.get('center') or spec.get('title') or 'Topic'
    branches = spec.get('branches') or spec.get('nodes') or []
    if not branches:
        return None

    width, height = 900, 620
    cx, cy = width / 2, height / 2
    parts = [_svg_open(width, height, center)]
    parts.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')

    ellipse_w, ellipse_h = 208, 74
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{ellipse_w / 2}" ry="{ellipse_h / 2}" fill="#1e293b"/>')
    lines = _wrap(center, 16, 22)
    parts.append(_text_block(cx, cy - (len(lines) - 1) * 10 + 5, lines, 16, '#ffffff', weight='700'))

    count = len(branches)
    for index, branch in enumerate(branches):
        angle = -math.pi / 2 + (2 * math.pi * index / count)
        spread = min(210, 120 + 16 * count)
        bx = cx + spread * math.cos(angle)
        by = cy + spread * math.sin(angle) * 0.78
        color = palette[index % len(palette)]

        parts.append(
            f'<path d="M {cx + (ellipse_w / 2) * math.cos(angle):.1f} '
            f'{cy + (ellipse_h / 2) * math.sin(angle):.1f} Q {(cx + bx) / 2:.1f} '
            f'{(cy + by) / 2:.1f} {bx:.1f} {by:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="2.5" opacity="0.85"/>'
        )

        label = branch.get('label') or branch.get('text') or f'Branch {index + 1}'
        label_lines = _wrap(label, 12, 20)
        box_w = min(210, max(96, 12 * _CHAR_W * max(len(l) for l in label_lines) + 26))
        box_h = 22 + len(label_lines) * 16
        parts.append(
            f'<rect x="{bx - box_w / 2:.1f}" y="{by - box_h / 2:.1f}" width="{box_w:.1f}" '
            f'height="{box_h:.1f}" rx="10" fill="{color}" opacity="0.12"/>'
        )
        parts.append(
            f'<rect x="{bx - box_w / 2:.1f}" y="{by - box_h / 2:.1f}" width="{box_w:.1f}" '
            f'height="{box_h:.1f}" rx="10" fill="none" stroke="{color}" stroke-width="2"/>'
        )
        parts.append(_text_block(bx, by - (len(label_lines) - 1) * 8 + 4, label_lines, 12, '#0f172a', weight='600'))

        leaves = branch.get('children') or branch.get('items') or []
        for leaf_index, leaf in enumerate(leaves[:3]):
            text = leaf.get('text') if isinstance(leaf, dict) else leaf
            lx = bx + (78 if math.cos(angle) >= 0 else -78)
            ly = by + (leaf_index - (len(leaves[:3]) - 1) / 2) * 26
            parts.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3.5" fill="{color}"/>')
            parts.append(_text_block(
                lx + (8 if math.cos(angle) >= 0 else -8), ly + 4,
                _wrap(text, 11, 16), 11, '#475569', weight='400',
                anchor='start' if math.cos(angle) >= 0 else 'end',
            ))
    parts.append('</svg>')
    return ''.join(parts)


def _timeline(spec, palette):
    """Horizontal timeline with alternating entries above and below the axis."""
    events = spec.get('events') or spec.get('nodes') or []
    if not events:
        return None
    count = len(events)
    width = max(860, 150 * count)
    height = 420
    axis_y = height / 2 + 10
    pad = 70
    step = (width - 2 * pad) / max(1, count - 1) if count > 1 else 0

    parts = [_svg_open(width, height, spec.get('title') or 'Timeline')]
    parts.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')
    title = spec.get('title')
    if title:
        parts.append(_text_block(width / 2, 42, _wrap(title, 20, 70), 20, '#0f172a', weight='700'))
    parts.append(
        f'<line x1="{pad}" y1="{axis_y}" x2="{width - pad}" y2="{axis_y}" '
        f'stroke="#cbd5e1" stroke-width="3"/>'
    )

    for index, event in enumerate(events):
        x = pad + step * index
        color = palette[index % len(palette)]
        above = index % 2 == 0
        parts.append(f'<circle cx="{x:.1f}" cy="{axis_y}" r="9" fill="{color}"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{axis_y}" r="4" fill="#ffffff"/>')

        label = event.get('label') or event.get('title') or event.get('text') or ''
        date = event.get('date') or event.get('time') or ''
        detail = event.get('detail') or event.get('sub') or ''

        leader = 46 if above else 46
        ly = axis_y - leader if above else axis_y + leader
        parts.append(
            f'<line x1="{x:.1f}" y1="{axis_y}" x2="{x:.1f}" y2="{ly:.1f}" '
            f'stroke="{color}" stroke-width="1.5" opacity="0.5"/>'
        )

        block = ([str(date)] if date else []) + _wrap(label, 13, 18)
        text_y = ly - (14 if above else -4)
        parts.append(_text_block(x, text_y, block, 13, '#0f172a', weight='600'))
        if detail:
            detail_y = text_y + (len(block) * 17 if above else len(block) * 17)
            parts.append(_text_block(x, detail_y if above else detail_y + 14, _wrap(detail, 11, 22), 11, '#64748b', weight='400'))
    parts.append('</svg>')
    return ''.join(parts)


def _compare(spec, palette):
    """Two (or three) column comparison with a shared heading row."""
    columns = spec.get('columns') or []
    if len(columns) < 2:
        return None
    columns = columns[:3]
    rows = max(len((c.get('items') or [])) for c in columns)
    col_w, row_h, head_h = 250, 46, 62
    width = 60 + col_w * len(columns)
    height = 96 + head_h + rows * row_h

    parts = [_svg_open(width, height, spec.get('title') or 'Comparison')]
    parts.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')
    title = spec.get('title')
    if title:
        parts.append(_text_block(width / 2, 42, _wrap(title, 20, 60), 20, '#0f172a', weight='700'))

    for index, column in enumerate(columns):
        color = palette[index % len(palette)]
        x = 30 + index * col_w
        parts.append(
            f'<rect x="{x}" y="76" width="{col_w - 8}" height="{head_h}" rx="10" fill="{color}"/>'
        )
        heading = column.get('title') or column.get('label') or f'Option {index + 1}'
        parts.append(_text_block(
            x + (col_w - 8) / 2, 76 + head_h / 2 + 5, _wrap(heading, 15, 22), 15, '#ffffff', weight='700',
        ))
        items = column.get('items') or []
        for row_index in range(rows):
            y = 76 + head_h + row_index * row_h
            if row_index % 2 == 0:
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{col_w - 8}" height="{row_h}" '
                    f'fill="#f1f5f9" opacity="0.7"/>'
                )
            text = items[row_index] if row_index < len(items) else ''
            if isinstance(text, dict):
                text = text.get('text') or text.get('label') or ''
            parts.append(_text_block(
                x + 14, y + row_h / 2 + 4, _wrap(text, 12, 30), 12, '#334155',
                weight='400', anchor='start',
            ))
    parts.append('</svg>')
    return ''.join(parts)


def _hierarchy(spec, palette):
    """Top-down tree. Each node may carry `children`."""
    root = spec.get('root') or {'label': spec.get('title') or 'Root', 'children': spec.get('nodes') or []}
    levels = []

    def walk(node, depth):
        if depth > 4:
            return
        while len(levels) <= depth:
            levels.append([])
        levels[depth].append(node)
        for child in (node.get('children') or [])[:4]:
            if isinstance(child, dict):
                walk(child, depth + 1)
            else:
                walk({'label': child}, depth + 1)

    walk(root, 0)
    widest = max(len(level) for level in levels)
    node_w, node_h, gap_y = 176, 58, 92
    width = max(760, widest * (node_w + 26) + 60)
    height = 90 + len(levels) * (node_h + gap_y)

    parts = [_svg_open(width, height, str(root.get('label') or 'Hierarchy'))]
    parts.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')

    positions = []
    for depth, level in enumerate(levels):
        count = len(level)
        step = width / (count + 1)
        row = []
        for index, node in enumerate(level):
            row.append((step * (index + 1), 90 + depth * (node_h + gap_y)))
        positions.append(row)

    for depth, row in enumerate(positions):
        for index, (x, y) in enumerate(row):
            node = levels[depth][index]
            color = palette[depth % len(palette)]
            label = node.get('label') or node.get('text') or f'Node {index + 1}'
            if depth > 0:
                parents = positions[depth - 1]
                # Connect to the nearest parent horizontally — keeps edges short.
                parent = min(parents, key=lambda p: abs(p[0] - x))
                parts.append(
                    f'<path d="M {parent[0]:.1f} {parent[1] + node_h:.1f} '
                    f'C {parent[0]:.1f} {parent[1] + node_h + 30:.1f} {x:.1f} {y - 30:.1f} '
                    f'{x:.1f} {y:.1f}" fill="none" stroke="#cbd5e1" stroke-width="2"/>'
                )
            parts.append(
                f'<rect x="{x - node_w / 2:.1f}" y="{y:.1f}" width="{node_w}" height="{node_h}" '
                f'rx="10" fill="{color}" opacity="0.12"/>'
            )
            parts.append(
                f'<rect x="{x - node_w / 2:.1f}" y="{y:.1f}" width="{node_w}" height="{node_h}" '
                f'rx="10" fill="none" stroke="{color}" stroke-width="2"/>'
            )
            lines = _wrap(label, 12, int(node_w / (12 * _CHAR_W)) - 2)
            parts.append(_text_block(x, y + node_h / 2 - (len(lines) - 1) * 8 + 4, lines, 12, '#0f172a', weight='600'))
    parts.append('</svg>')
    return ''.join(parts)


def _pyramid(spec, palette):
    """Layered triangle — trophic levels, Maslow, data hierarchies."""
    levels = spec.get('levels') or spec.get('nodes') or []
    if not levels:
        return None
    width, top_w, height = 720, 150, 460
    bottom_w = 620
    step = (height - 90) / len(levels)
    apex_y, base_y = 80, height - 40

    parts = [_svg_open(width, height, spec.get('title') or 'Pyramid')]
    parts.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')
    title = spec.get('title')
    if title:
        parts.append(_text_block(width / 2, 40, _wrap(title, 20, 60), 20, '#0f172a', weight='700'))

    for index, level in enumerate(levels):
        y1 = apex_y + step * index
        y2 = apex_y + step * (index + 1)
        t = index / len(levels)
        t2 = (index + 1) / len(levels)
        half1 = top_w / 2 + (bottom_w - top_w) / 2 * t
        half2 = top_w / 2 + (bottom_w - top_w) / 2 * t2
        cx = width / 2
        color = palette[index % len(palette)]
        parts.append(
            f'<polygon points="{cx - half1:.1f},{y1:.1f} {cx + half1:.1f},{y1:.1f} '
            f'{cx + half2:.1f},{y2:.1f} {cx - half2:.1f},{y2:.1f}" fill="{color}" opacity="0.82"/>'
        )
        label = level.get('label') if isinstance(level, dict) else level
        parts.append(_text_block(
            cx, (y1 + y2) / 2 + 5, _wrap(label, 13, 40), 13, '#ffffff', weight='600',
        ))
    parts.append('</svg>')
    return ''.join(parts)


BUILDERS = {
    'flow': _flow,
    'flowchart': _flow,
    'process': _flow,
    'steps': _flow,
    'cycle': _cycle,
    'loop': _cycle,
    'mindmap': _mindmap,
    'concept': _mindmap,
    'timeline': _timeline,
    'compare': _compare,
    'comparison': _compare,
    'table': _compare,
    'hierarchy': _hierarchy,
    'tree': _hierarchy,
    'pyramid': _pyramid,
}

KINDS = sorted(set(BUILDERS))


def build_diagram(spec):
    """Render a diagram spec to an SVG string, or None when it cannot be drawn."""
    if not isinstance(spec, dict):
        return None
    kind = str(spec.get('kind') or spec.get('type') or '').strip().lower()
    builder = BUILDERS.get(kind)
    if builder is None:
        # Infer from the shape of the payload when the model omits `kind`.
        if spec.get('branches') or (spec.get('nodes') and spec.get('center')):
            builder = _mindmap
        elif spec.get('events'):
            builder = _timeline
        elif spec.get('columns'):
            builder = _compare
        elif spec.get('levels'):
            builder = _pyramid
        elif spec.get('root'):
            builder = _hierarchy
        else:
            builder = _flow
    try:
        svg = builder(spec, _palette(spec.get('palette')))
    except Exception:
        return None
    return svg


def is_svg(text):
    return bool(text) and '<svg' in str(text)[:400]


def sanitize_svg(text):
    """Strip script-bearing markup from model-supplied SVG before we serve it."""
    if not text:
        return ''
    cleaned = re.sub(r'<\s*(script|foreignObject)\b.*?<\s*/\s*\1\s*>', '', str(text), flags=re.S | re.I)
    cleaned = re.sub(r'\son\w+\s*=\s*"[^"]*"', '', cleaned, flags=re.I)
    cleaned = re.sub(r'\son\w+\s*=\s*\'[^\']*\'', '', cleaned, flags=re.I)
    cleaned = re.sub(r'javascript:', '', cleaned, flags=re.I)
    return cleaned
