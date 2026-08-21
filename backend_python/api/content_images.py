"""Inline content images — Meta-style image chips embedded inside text.

Content is stored as plain text with tokens of the form ``[[img:ID]]`` where
ID is the numeric pk of a :class:`api.models.ContentImage` row.  Media URLs
are fully deterministic from the id (``/media/content_images/<id>.webp``),
so neither the server nor any client needs a lookup to render a chip.
"""
import hashlib
import io
import os
import re
import time

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

TOKEN_RE = re.compile(r'\[\[img:(\d{1,10})\]\]')
MAX_IMAGES_PER_CONTENT = 8
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_DIMENSION = 2048
THUMB_DIMENSION = 240
ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP', 'GIF', 'BMP', 'MPO'}

MEDIA_DIR = 'content_images'


def image_url(image_id):
    return f'{settings.MEDIA_URL}{MEDIA_DIR}/{int(image_id)}.webp'


def thumb_url(image_id):
    return f'{settings.MEDIA_URL}{MEDIA_DIR}/{int(image_id)}t.webp'


def extract_image_ids(text):
    """Ordered unique image ids referenced by a piece of content."""
    seen = set()
    ids = []
    for m in TOKEN_RE.finditer(str(text or '')):
        iid = int(m.group(1))
        if iid not in seen:
            seen.add(iid)
            ids.append(iid)
    return ids


def plain_text(text, placeholder='[image]'):
    """Replace tokens with a plain-text placeholder (for excerpts/quotes)."""
    return TOKEN_RE.sub(placeholder, str(text or ''))


def strip_tokens(text):
    """Remove tokens entirely (meta descriptions, search snippets)."""
    return TOKEN_RE.sub('', str(text or ''))


def clean_content(text, max_images=MAX_IMAGES_PER_CONTENT):
    """Keep only tokens whose image rows exist; cap the number of images.

    Unknown ids are dropped silently so stale or forged tokens can never
    reach the render pipeline.
    """
    text = str(text or '')
    ids = extract_image_ids(text)
    if not ids:
        return TOKEN_RE.sub('', text)
    from .models import ContentImage
    valid = set(
        ContentImage.objects.filter(pk__in=ids[:max_images + 50])
        .values_list('id', flat=True)
    )
    kept = 0

    def _repl(m):
        nonlocal kept
        iid = int(m.group(1))
        if iid in valid and kept < max_images:
            kept += 1
            return m.group(0)
        return ''

    return TOKEN_RE.sub(_repl, text)


def mark_used(ids):
    """Flag images referenced by saved content so cleanup never deletes them."""
    ids = [i for i in ids if i]
    if ids:
        from .models import ContentImage
        ContentImage.objects.filter(pk__in=ids).update(used=True)


_SENTINEL_RE = re.compile(r'ZQXIMG(\d{1,10})ZQXEND')


def _chip_html(image_id):
    iid = int(image_id)
    full = image_url(iid)
    thumb = thumb_url(iid)
    return (
        f'<span class="neb-chip" data-neb-img="{iid}" data-neb-full="{full}" '
        f'role="button" tabindex="0" aria-label="Attached image">'
        f'<img src="{thumb}" alt="Image" loading="lazy" decoding="async"></span>'
    )


def tokenize_for_markdown(text):
    """Swap tokens for markdown-safe sentinels before markdown rendering."""
    return TOKEN_RE.sub(lambda m: f'ZQXIMG{m.group(1)}ZQXEND', str(text or ''))


def detokenize_html(html):
    """Swap sentinels back out for chip markup after markdown rendering."""
    if not html:
        return html
    return _SENTINEL_RE.sub(lambda m: _chip_html(m.group(1)), html)


def _has_alpha(image):
    return (
        image.mode in ('RGBA', 'LA')
        or (image.mode == 'P' and 'transparency' in image.info)
    )


def save_content_image(file_obj):
    """Validate, normalise and store an uploaded inline image.

    Returns the new (or deduplicated) ContentImage row.
    Raises ValidationError on bad input.
    """
    from django.core.exceptions import ValidationError
    from .models import ContentImage

    if file_obj is None:
        raise ValidationError('No image provided.')
    size = getattr(file_obj, 'size', 0) or 0
    if size > MAX_UPLOAD_BYTES:
        raise ValidationError('Image is too large. Maximum size is 10 MB.')
    data = file_obj.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValidationError('Image is too large. Maximum size is 10 MB.')

    sha = hashlib.sha256(data).hexdigest()
    existing = ContentImage.objects.filter(sha256=sha).first()
    if existing:
        return existing

    try:
        image = Image.open(io.BytesIO(data))
        image.verify()
        image = Image.open(io.BytesIO(data))
    except Exception:
        raise ValidationError('Only JPG, PNG, WEBP, or GIF images are allowed.')
    image_format = (image.format or '').upper()
    if image_format not in ALLOWED_FORMATS:
        raise ValidationError('Only JPG, PNG, WEBP, or GIF images are allowed.')

    animated = image_format == 'GIF' and getattr(image, 'is_animated', False)
    width, height = image.width, image.height

    if animated:
        full_bytes, full_ext = data, '.gif'
    else:
        image = ImageOps.exif_transpose(image)
        keep_alpha = _has_alpha(image)
        if not keep_alpha and image.mode != 'RGB':
            image = image.convert('RGB')
        elif keep_alpha and image.mode != 'RGBA':
            image = image.convert('RGBA')
        if image.width > MAX_DIMENSION or image.height > MAX_DIMENSION:
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)
            width, height = image.width, image.height
        buf = io.BytesIO()
        image.save(buf, format='WEBP', quality=85, method=5)
        full_bytes, full_ext = buf.getvalue(), '.webp'

    try:
        image.seek(0)
        thumb = image.convert('RGBA')
    except Exception:
        thumb = Image.new('RGBA', (8, 8))
    thumb.thumbnail((THUMB_DIMENSION, THUMB_DIMENSION), Image.LANCZOS)
    tbuf = io.BytesIO()
    thumb.save(tbuf, format='WEBP', quality=80, method=5)

    row = ContentImage.objects.create(
        width=width,
        height=height,
        size=len(data),
        sha256=sha,
        is_animated=animated,
        used=False,
        created_at=int(time.time() * 1000),
    )
    full_name = default_storage.save(
        os.path.join(MEDIA_DIR, f'{row.id}{full_ext}'), ContentFile(full_bytes)
    )
    thumb_name = default_storage.save(
        os.path.join(MEDIA_DIR, f'{row.id}t.webp'), ContentFile(tbuf.getvalue())
    )
    row.file.name = full_name
    row.thumb.name = thumb_name
    row.save(update_fields=['file', 'thumb'])
    return row


def delete_files(row):
    for f in (row.file, row.thumb):
        if f:
            try:
                default_storage.delete(f.name)
            except Exception:
                pass
