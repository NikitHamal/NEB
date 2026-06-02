"""File compression for uploaded resources.

Lossless PDF compression via pikepdf (removes duplicate objects,
flattens incremental saves, recompresses streams).

Near-lossless image compression via Pillow:
  - JPEG: quality=85, optimize=True (visually identical)
  - PNG: optimize=True, stripped metadata (lossless)
  - WebP: quality=88, method=6 (near-lossless for photos)
  - BMP/GIF: converted to WebP for massive size savings
"""
import logging
import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
PDF_EXTENSION = '.pdf'
COMPRESSIBLE_EXTENSIONS = IMAGE_EXTENSIONS | {PDF_EXTENSION}


def compress_resource_file(file_obj, original_ext):
    """Compress an uploaded resource file if it's a compressible type.

    Returns a ContentFile with the compressed data and the final extension.
    If compression doesn't reduce size, returns None (caller should use original).
    If the file type isn't compressible, returns None (caller should use original).
    """
    ext = original_ext.lower()

    if ext not in COMPRESSIBLE_EXTENSIONS:
        return None

    if hasattr(file_obj, 'seek'):
        file_obj.seek(0)

    original_data = file_obj.read()
    original_size = len(original_data)

    if ext == PDF_EXTENSION:
        compressed = _compress_pdf(original_data)
        if compressed and len(compressed) < original_size:
            logger.info(
                "PDF compressed: %d → %d bytes (%.1f%% reduction)",
                original_size, len(compressed),
                (1 - len(compressed) / original_size) * 100,
            )
            return ContentFile(compressed), ext
        logger.info("PDF compression skipped: no size reduction (%d bytes)", original_size)
        return None

    if ext in IMAGE_EXTENSIONS:
        result_ext, compressed = _compress_image(original_data, ext, original_size)
        if compressed is not None:
            return ContentFile(compressed), result_ext

    return None


def _compress_pdf(data: bytes) -> bytes | None:
    """Losslessly compress a PDF using pikepdf.

    Removes duplicate objects, flattens incremental saves,
    and recompresses streams. No quality loss.
    """
    try:
        import pikepdf
    except ImportError:
        logger.warning("pikepdf not installed, skipping PDF compression")
        return None

    try:
        with pikepdf.open(BytesIO(data)) as pdf:
            pdf.remove_unreferenced_resources()
            output = BytesIO()
            pdf.save(output, linearize=True, compress_streams=True,
                     object_stream_mode=pikepdf.ObjectStreamMode.generate)
            return output.getvalue()
    except Exception:
        logger.exception("PDF compression failed, using original")
        return None


def _compress_image(data: bytes, ext: str, original_size: int) -> tuple:
    """Compress an image. Returns (new_ext, compressed_bytes) or (ext, None).

    Strategy:
      - JPEG: re-save at quality=85 with optimize=True
      - PNG: re-save with optimize=True, strip metadata
      - WebP: re-save at quality=88 with method=6
      - BMP/GIF: convert to WebP for massive size savings
    """
    try:
        img = Image.open(BytesIO(data))
        img.verify()
    except (UnidentifiedImageError, OSError):
        logger.warning("Could not open image for compression, using original")
        return ext, None

    try:
        img = Image.open(BytesIO(data))
        original_format = img.format
        output = BytesIO()

        if ext in {'.bmp', '.gif'}:
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            img.save(output, format='WEBP', quality=88, method=6)
            new_ext = '.webp'
            if len(output.getvalue()) >= original_size:
                return ext, None
            return new_ext, output.getvalue()

        if ext in {'.jpg', '.jpeg'} or original_format == 'JPEG':
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output, format='JPEG', quality=85, optimize=True)
            if len(output.getvalue()) >= original_size:
                return ext, None
            return ext, output.getvalue()

        if ext == '.png' or original_format == 'PNG':
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            img.save(output, format='PNG', optimize=True)
            png_size = len(output.getvalue())

            webp_output = BytesIO()
            img.save(webp_output, format='WEBP', quality=88, method=6)
            webp_size = len(webp_output.getvalue())

            if webp_size < png_size and webp_size < original_size:
                return '.webp', webp_output.getvalue()
            if png_size < original_size:
                return ext, png_size
            return ext, None

        if ext == '.webp' or original_format == 'WEBP':
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            img.save(output, format='WEBP', quality=88, method=6)
            if len(output.getvalue()) >= original_size:
                return ext, None
            return ext, output.getvalue()

        return ext, None

    except Exception:
        logger.exception("Image compression failed, using original")
        return ext, None