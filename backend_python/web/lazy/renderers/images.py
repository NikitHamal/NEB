"""Shared image plumbing for every renderer.

Diagrams and charts land in the run workspace as SVG or PNG. Each renderer
needs the same three things: a safe path inside the workspace, the raw bytes,
and a raster format its engine can actually consume. This module is that
single source of truth so DOCX, PDF, PPTX and the HTML preview all agree on
what an `image` block means.

SVG is the awkward one: python-docx and ReportLab cannot ingest it directly,
so we rasterize once through svglib -> renderPM and cache the PNG back into
the block.
"""

import base64
import io
import os

MIME_BY_EXT = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.webp': 'image/webp',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.svg': 'image/svg+xml',
}

SVG_MIME = 'image/svg+xml'
RASTER_EXTS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff', '.webp'}


def safe_abspath(base_path, path):
    """Join `path` under `base_path`, refusing anything that escapes it."""
    if not path or not base_path:
        return None
    base_abs = os.path.abspath(base_path)
    full = os.path.abspath(os.path.join(base_abs, str(path)))
    if not (full == base_abs or full.startswith(base_abs + os.sep)):
        return None
    return full


def mime_for(path, default='image/png'):
    ext = os.path.splitext(str(path or ''))[1].lower()
    return MIME_BY_EXT.get(ext, default)


def _decode_data(value):
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    if isinstance(value, str) and value.strip():
        payload = value.split(',', 1)[1] if value.startswith('data:') else value
        try:
            return base64.b64decode(payload, validate=False)
        except Exception:
            return None
    return None


def block_bytes(block, base_path=None):
    """Return the raw bytes for an image block, or None.

    Checks inline `data` first, then reads `path` from the workspace. A
    successful read is memoised on the block so repeated renderer passes do
    not hit the disk again.
    """
    if not isinstance(block, dict):
        return None
    if block.get('_bytes') is not None:
        return block['_bytes']

    raw = None
    if block.get('data') is not None:
        raw = _decode_data(block['data'])
    elif block.get('path'):
        full = safe_abspath(base_path, block['path'])
        if full:
            try:
                with open(full, 'rb') as handle:
                    raw = handle.read()
            except OSError:
                raw = None

    if raw is None:
        return None
    block['_bytes'] = raw
    if not block.get('mime'):
        block['mime'] = mime_for(block.get('path') or '')
    return raw


def block_dimensions(block, default=(1200, 800)):
    """Natural pixel size of the image, falling back to a sensible default."""
    raw = block.get('_bytes')
    if not raw:
        return default
    try:
        from PIL import Image
        with Image.open(io.BytesIO(raw)) as img:
            return img.size
    except Exception:
        return default


def is_svg(block):
    raw = block.get('_bytes') or b''
    if str(block.get('mime') or '') == SVG_MIME:
        return True
    if str(block.get('path') or '').lower().endswith('.svg'):
        return True
    head = raw[:512].lstrip()
    return head.startswith(b'<svg') or (head.startswith(b'<?xml') and b'<svg' in head)


def rasterize(block):
    """Convert an SVG block to PNG bytes in place. Returns True on success."""
    if not is_svg(block):
        return True
    if block.get('_png'):
        block['_bytes'] = block['_png']
        block['mime'] = 'image/png'
        return True

    raw = block.get('_bytes')
    if not raw:
        return False

    png = _rasterize_svg_bytes(raw)
    if not png:
        return False

    block['_svg'] = raw
    block['_png'] = png
    block['_bytes'] = png
    block['mime'] = 'image/png'
    return True


def _rasterize_svg_bytes(raw):
    """Try the shipped pure-Pillow rasterizer, then any native backend."""
    from .. import svg_raster

    png = svg_raster.rasterize_svg(raw.decode('utf-8', errors='replace')
                                   if isinstance(raw, (bytes, bytearray)) else raw)
    if png:
        return png

    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM

        drawing = svg2rlg(io.BytesIO(raw))
        if drawing is None:
            return None
        drawing.scale(2.0, 2.0)
        buffer = io.BytesIO()
        renderPM.drawToFile(drawing, buffer, fmt='PNG', dpi=144)
        return buffer.getvalue() or None
    except Exception:
        return None


def resolve(spec, base_path=None):
    """Pre-load every image block in a spec so renderers can assume bytes."""
    count = 0
    for section in spec.get('sections') or []:
        for block in section.get('blocks') or []:
            if not isinstance(block, dict) or block.get('type') != 'image':
                continue
            if block_bytes(block, base_path):
                count += 1
    return count


def b64(block):
    """Base64 payload for the HTML preview, or an empty string."""
    raw = block.get('_bytes')
    if not raw:
        return ''
    return base64.b64encode(raw).decode('ascii')
