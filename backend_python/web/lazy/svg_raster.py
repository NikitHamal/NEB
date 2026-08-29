"""Dependency-free SVG -> PNG rasterizer.

The diagram engine emits a small, well-known SVG subset (rect/circle/ellipse/
line/polygon/path/text, plus arrow markers). Third-party rasterizers all lean
on a native cairo library that is not reliably present on Windows servers, so
we rasterize that subset ourselves with Pillow. Output is rendered at 2x and
down-sampled, which gives clean antialiased edges.

Anything outside the subset is ignored rather than fatal — a missing decorative
detail is better than a document with no figure at all.
"""

import math
import os
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

SVG_NS = 'http://www.w3.org/2000/svg'
XLINK_NS = 'http://www.w3.org/1999/xlink'

NAMED_COLORS = {
    'none': None, 'transparent': None,
    'white': '#ffffff', 'black': '#000000', 'red': '#ff0000',
    'green': '#008000', 'blue': '#0000ff', 'grey': '#808080',
    'gray': '#808080', 'silver': '#c0c0c0', 'orange': '#ffa500',
    'yellow': '#ffff00', 'purple': '#800080', 'teal': '#008080',
}

FONT_CANDIDATES = [
    ('C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/segoeuib.ttf'),
    ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
     '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
]

_font_cache = {}


def _localname(tag):
    if isinstance(tag, str) and tag.startswith('{'):
        return tag.split('}', 1)[1]
    return tag


def _num(value, default=0.0):
    if value is None:
        return default
    text = str(value).strip().replace('px', '')
    try:
        return float(text)
    except ValueError:
        match = re.search(r'-?\d+(?:\.\d+)?', text)
        return float(match.group()) if match else default


def _color(value, default='#000000'):
    if value is None:
        return default
    text = str(value).strip()
    if not text or text in ('none', 'transparent'):
        return None
    if text.startswith('#'):
        return text
    if text.startswith('rgb'):
        nums = re.findall(r'[\d.]+', text)
        if len(nums) >= 3:
            return '#%02x%02x%02x' % (int(float(nums[0])), int(float(nums[1])), int(float(nums[2])))
        return default
    return NAMED_COLORS.get(text.lower(), default)


def _rgba(value, alpha=255):
    hex_color = _color(value, '#000000')
    if not hex_color:
        return None
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        r = g = b = 0
    return (r, g, b, int(alpha))


def _load_font(bold, size):
    key = ('b' if bold else 'r', int(size))
    if key in _font_cache:
        return _font_cache[key]

    font = None
    for regular, bold_path in FONT_CANDIDATES:
        path = bold_path if bold else regular
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, int(size))
                break
            except OSError:
                continue

    if font is None:
        try:
            import matplotlib
            folder = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
            name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
            font = ImageFont.truetype(os.path.join(folder, name), int(size))
        except Exception:
            font = ImageFont.load_default()

    _font_cache[key] = font
    return font


class _Context:
    __slots__ = ('fill', 'stroke', 'stroke_width', 'opacity',
                 'font_size', 'font_family', 'font_weight', 'anchor')

    def __init__(self):
        self.fill = '#1e293b'
        self.stroke = None
        self.stroke_width = 1.0
        self.opacity = 1.0
        self.font_size = 14.0
        self.font_family = ''
        self.font_weight = '400'
        self.anchor = 'start'

    def inherit(self, element):
        child = _Context()
        for attr in self.__slots__:
            setattr(child, attr, getattr(self, attr))
        mapping = {
            'fill': ('fill', str),
            'stroke': ('stroke', str),
            'stroke-width': ('stroke_width', float),
            'opacity': ('opacity', float),
            'font-size': ('font_size', float),
            'font-family': ('font_family', str),
            'font-weight': ('font_weight', str),
            'text-anchor': ('anchor', str),
        }
        for key, (attr, cast) in mapping.items():
            raw = element.get(key)
            if raw is not None:
                try:
                    setattr(child, attr, cast(raw))
                except (TypeError, ValueError):
                    pass
        raw_opacity = element.get('fill-opacity')
        if raw_opacity is None and element.get('opacity') is None:
            child.opacity = self.opacity
        return child


def _points(value):
    nums = re.findall(r'-?\d+(?:\.\d+)?', str(value or ''))
    coords = [float(n) for n in nums]
    return [(coords[i], coords[i + 1]) for i in range(0, len(coords) - 1, 2)]


def _parse_path(d):
    """Flatten a path's `d` attribute into a list of polylines."""
    tokens = re.findall(r'[MmLlCcSsQqTtAaZz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?', str(d or ''))
    polylines, current = [], []
    index, start = 0, (0.0, 0.0)
    cursor = (0.0, 0.0)
    command = None

    def pop_numbers(count):
        nonlocal index
        values = []
        while len(values) < count and index < len(tokens):
            token = tokens[index]
            index += 1
            if re.match(r'^[MmLlCcSsQqTtAaZz]$', token):
                command_holder.append(token)
                break
            values.append(float(token))
        return values

    while index < len(tokens):
        token = tokens[index]
        index += 1
        if re.match(r'^[MmLlCcSsQqTtAaZz]$', token):
            command = token
            if token in ('Z', 'z') and current:
                current.append(current[0])
                polylines.append(current)
                current = []
                cursor = start
            continue
        index -= 1
        command_holder = []
        upper = (command or 'M').upper()

        if upper == 'M':
            vals = pop_numbers(2)
            if len(vals) == 2:
                cursor = (vals[0], vals[1]) if command == 'M' else (cursor[0] + vals[0], cursor[1] + vals[1])
                if current:
                    polylines.append(current)
                current = [cursor]
                start = cursor
        elif upper == 'L':
            vals = pop_numbers(2)
            if len(vals) == 2:
                cursor = (vals[0], vals[1]) if command == 'L' else (cursor[0] + vals[0], cursor[1] + vals[1])
                if not current:
                    current = [cursor]
                else:
                    current.append(cursor)
        elif upper in ('C', 'S', 'Q', 'T'):
            count = 6 if upper in ('C', 'S') else 4
            vals = pop_numbers(count)
            if len(vals) >= 2:
                end = (vals[-2], vals[-1])
                if command.islower():
                    end = (cursor[0] + vals[-2], cursor[1] + vals[-1])
                for step in range(1, 13):
                    t = step / 12.0
                    current.append((cursor[0] + (end[0] - cursor[0]) * t,
                                    cursor[1] + (end[1] - cursor[1]) * t))
                cursor = end
        elif upper == 'A':
            vals = pop_numbers(7)
            if len(vals) >= 2:
                if command.islower():
                    cursor = (cursor[0] + vals[-2], cursor[1] + vals[-1])
                else:
                    cursor = (vals[-2], vals[-1])
                current.append(cursor)
        if command_holder:
            command = command_holder[0]
            index -= 1

    if current:
        polylines.append(current)
    return polylines


def _draw_arrow(draw, start, end, size, color):
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length < 0.5:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base_x = end[0] - ux * size
    base_y = end[1] - uy * size
    half = size * 0.42
    draw.polygon(
        [(end[0], end[1]),
         (base_x + px * half, base_y + py * half),
         (base_x - px * half, base_y - py * half)],
        fill=color,
    )


class _Rasterizer:
    def __init__(self, width, height, scale):
        self.scale = scale
        self.width = max(1, int(round(width * scale)))
        self.height = max(1, int(round(height * scale)))
        self.image = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))
        self.markers = {}

    def sx(self, value):
        return float(value) * self.scale

    def collect_markers(self, root):
        for element in root.iter():
            if _localname(element.tag) == 'marker':
                marker_id = element.get('id')
                if not marker_id:
                    continue
                size = _num(element.get('markerWidth'), 7)
                color = None
                for child in element.iter():
                    if _localname(child.tag) in ('path', 'polygon'):
                        color = _color(child.get('fill'), '#1e293b')
                        break
                self.markers[marker_id] = (size, color or '#1e293b')

    def run(self, root, context):
        for element in root:
            self.draw(element, context)

    def draw(self, element, context):
        tag = _localname(element.tag)
        if not isinstance(tag, str):
            return
        if tag in ('defs', 'marker', 'title', 'desc', 'style'):
            return

        ctx = context.inherit(element)
        if tag == 'g':
            self.run(element, ctx)
            return

        opacity = max(0.0, min(1.0, ctx.opacity))
        if opacity < 0.999:
            scratch = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            surface, layer = scratch, True
        else:
            surface, layer = self.image, False

        try:
            self._shape(ImageDraw.Draw(surface), tag, element, ctx)
        except Exception:
            pass

        if layer:
            scratch.putalpha(scratch.getchannel('A').point(lambda v: int(v * opacity)))
            self.image = Image.alpha_composite(self.image, scratch)

    def _shape(self, draw, tag, element, ctx):
        scale = self.scale

        if tag == 'rect':
            x = self.sx(_num(element.get('x')))
            y = self.sx(_num(element.get('y')))
            w = self.sx(_num(element.get('width')))
            h = self.sx(_num(element.get('height')))
            rx = self.sx(_num(element.get('rx'))) or self.sx(_num(element.get('ry')))
            fill = _rgba(ctx.fill, 255)
            stroke = _rgba(ctx.stroke, 255)
            box = [x, y, x + w, y + h]
            if rx > 0.5:
                draw.rounded_rectangle(box, radius=rx, fill=fill,
                                       outline=stroke, width=int(ctx.stroke_width * scale) if stroke else 0)
            else:
                draw.rectangle(box, fill=fill,
                               outline=stroke, width=int(ctx.stroke_width * scale) if stroke else 0)

        elif tag in ('circle', 'ellipse'):
            cx = self.sx(_num(element.get('cx')))
            cy = self.sx(_num(element.get('cy')))
            if tag == 'circle':
                rx = ry = self.sx(_num(element.get('r')))
            else:
                rx = self.sx(_num(element.get('rx')))
                ry = self.sx(_num(element.get('ry')))
            fill = _rgba(ctx.fill, 255)
            stroke = _rgba(ctx.stroke, 255)
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill,
                         outline=stroke, width=int(ctx.stroke_width * scale) if stroke else 0)

        elif tag == 'line':
            start = (self.sx(_num(element.get('x1'))), self.sx(_num(element.get('y1'))))
            end = (self.sx(_num(element.get('x2'))), self.sx(_num(element.get('y2'))))
            stroke = _rgba(ctx.stroke or ctx.fill, 255)
            if stroke:
                draw.line([start, end], fill=stroke,
                          width=max(1, int(round(ctx.stroke_width * scale))))
            marker = element.get('marker-end') or ''
            match = re.search(r'url\(#([^)]+)\)', marker)
            if match and match.group(1) in self.markers:
                size, color = self.markers[match.group(1)]
                _draw_arrow(draw, start, end, size * scale * 0.9, _rgba(color, 255))

        elif tag in ('polyline', 'polygon'):
            pts = [(self.sx(x), self.sx(y)) for x, y in _points(element.get('points'))]
            if len(pts) < 2:
                return
            fill = _rgba(ctx.fill, 255) if tag == 'polygon' else None
            stroke = _rgba(ctx.stroke or ctx.fill, 255)
            if fill:
                draw.polygon(pts, fill=fill,
                             outline=stroke if stroke else None)
            elif stroke:
                draw.line(pts + [pts[0]] if tag == 'polygon' else pts,
                          fill=stroke, width=max(1, int(round(ctx.stroke_width * scale))))

        elif tag == 'path':
            fill = _rgba(ctx.fill, 255)
            stroke = _rgba(ctx.stroke, 255)
            for poly in _parse_path(element.get('d')):
                pts = [(self.sx(x), self.sx(y)) for x, y in poly]
                if len(pts) < 2:
                    continue
                if fill and len(pts) > 2:
                    draw.polygon(pts, fill=fill, outline=stroke if stroke else None)
                elif stroke:
                    draw.line(pts, fill=stroke,
                              width=max(1, int(round(ctx.stroke_width * scale))), joint='curve')

        elif tag == 'text':
            self._text(draw, element, ctx)

    def _text(self, draw, element, ctx):
        scale = self.scale
        size = max(6.0, _num(element.get('font-size'), ctx.font_size) * scale)
        weight = str(element.get('font-weight') or ctx.font_weight)
        bold = weight in ('600', '700', '800', '900', 'bold', 'bolder')
        font = _load_font(bold, size)
        fill = _rgba(element.get('fill') or ctx.fill, 255) or (30, 41, 59, 255)

        anchor = str(element.get('text-anchor') or ctx.anchor)
        code = {'middle': 'm', 'end': 'r'}.get(anchor, 'l') + 's'

        base_x = self.sx(_num(element.get('x')))
        base_y = self.sx(_num(element.get('y')))

        spans = [c for c in element if _localname(c.tag) == 'tspan']
        if spans:
            cursor_y = base_y
            for index, span in enumerate(spans):
                raw_dy = span.get('dy')
                if index == 0:
                    cursor_y = base_y + (self.sx(_num(raw_dy)) if raw_dy else 0)
                elif raw_dy:
                    cursor_y += self.sx(_num(raw_dy))
                else:
                    cursor_y += size * 1.2
                x = self.sx(_num(span.get('x'), base_x / scale)) if span.get('x') else base_x
                text = ''.join(span.itertext())
                if text.strip():
                    draw.text((x, cursor_y), text, font=font, fill=fill, anchor=code)
        else:
            text = ''.join(element.itertext())
            if text.strip():
                draw.text((base_x, base_y), text, font=font, fill=fill, anchor=code)

    def to_png(self):
        return self.image.convert('RGB')


def rasterize_svg(svg_text, scale=2.0, max_width=2400):
    """Render an SVG string to PNG bytes. Returns None if it cannot be parsed."""
    if not svg_text:
        return None
    if isinstance(svg_text, bytes):
        svg_text = svg_text.decode('utf-8', errors='replace')
    svg_text = svg_text.strip()
    if not svg_text.startswith('<'):
        return None

    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError:
        return None

    width = _num(root.get('width'), 0)
    height = _num(root.get('height'), 0)
    view = root.get('viewBox')
    if (not width or not height) and view:
        parts = [float(p) for p in re.findall(r'-?\d+(?:\.\d+)?', view)]
        if len(parts) >= 4:
            width, height = parts[2], parts[3]
    if not width or not height:
        width, height = 900.0, 600.0
    if width <= 0 or height <= 0:
        return None

    if width * scale > max_width:
        scale = max_width / width

    try:
        raster = _Rasterizer(width, height, scale)
        raster.collect_markers(root)
        context = _Context()
        context.font_size = _num(root.get('font-size'), 14)
        context.font_family = str(root.get('font-family') or '')
        context.fill = str(root.get('fill') or '#1e293b')
        raster.run(root, context)

        import io
        buffer = io.BytesIO()
        raster.to_png().save(buffer, format='PNG', optimize=True)
        return buffer.getvalue()
    except Exception:
        return None
