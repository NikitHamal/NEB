"""File compression for uploaded resources.

PDF compression — tries in order:
  1. Ghostscript /ebook (150 DPI image resampling + font subsetting) — same
     engine as ilovepdf, typically 60-80% size reduction for scanned docs.
  2. pikepdf (stream recompression only) — fallback if gs not installed.
  3. pypdf (pure Python stream compression) — final fallback.

Lossless image compression via Pillow (for new uploads):
  - JPEG: skipped — JPEG cannot be losslessly re-compressed
  - PNG/BMP/GIF: converted to lossless WebP (zero quality loss, ~30-60% smaller)
  - WebP: re-saved with lossless=True (only if smaller)

Lossy image compression (for batch recompression of existing files):
  - JPEG: quality=85, optimize=True (visually identical, ~20-40% smaller)
  - PNG → WebP: quality=88, method=6 (near-lossless, major size savings)
  - BMP/GIF → WebP: quality=88, method=6
  - WebP: quality=88, method=6
"""
import logging
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
PDF_EXTENSION = '.pdf'
COMPRESSIBLE_EXTENSIONS = IMAGE_EXTENSIONS | {PDF_EXTENSION}


def compress_resource_file(file_obj, original_ext, lossless=True):
    """Compress an uploaded resource file if it's a compressible type.

    Args:
        file_obj: File-like object to compress.
        original_ext: Original file extension (e.g. '.pdf', '.png').
        lossless: If True (default), use only lossless compression so no
                  quality is sacrificed. If False, use aggressive lossy
                  compression (suitable for batch re-processing).

    Returns:
        (ContentFile, final_ext) tuple on success, or None if compression
        would not reduce file size or the type is not compressible.
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
        if lossless:
            result_ext, compressed = _compress_image_lossless(original_data, ext, original_size)
        else:
            result_ext, compressed = _compress_image_lossy(original_data, ext, original_size)

        if compressed is not None:
            logger.info(
                "Image compressed (%s): %d → %d bytes (%.1f%% reduction)",
                ext, original_size, len(compressed),
                (1 - len(compressed) / original_size) * 100,
            )
            return ContentFile(compressed), result_ext

    return None


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def _compress_pdf(data: bytes) -> bytes | None:
    """Compress a PDF. Tries Ghostscript → pikepdf → pypdf in order.

    Ghostscript /ebook: 150 DPI image resampling + font subsetting.
    Same approach as ilovepdf — typically 60-80% reduction on scanned docs.
    pikepdf and pypdf are fallbacks for environments without gs installed.
    """
    # 1. Ghostscript — highest quality, best compression
    try:
        import subprocess
        import tempfile

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as inp:
            inp.write(data)
            inp_path = inp.name

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as out:
            out_path = out.name

        try:
            result = subprocess.run(
                [
                    'gs', '-q',
                    '-sDEVICE=pdfwrite',
                    '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/ebook',
                    '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-dDetectDuplicateImages=true',
                    '-dCompressFonts=true',
                    '-r150',
                    f'-sOutputFile={out_path}',
                    inp_path,
                ],
                capture_output=True,
                timeout=120,
            )
            if result.returncode == 0:
                import os
                with open(out_path, 'rb') as f:
                    compressed = f.read()
                if len(compressed) < len(data):
                    logger.info(
                        "Ghostscript PDF compressed: %d → %d bytes (%.1f%% reduction)",
                        len(data), len(compressed),
                        (1 - len(compressed) / len(data)) * 100,
                    )
                    return compressed
                logger.info("Ghostscript produced no improvement, trying fallback")
        finally:
            import os
            try:
                os.unlink(inp_path)
            except OSError:
                pass
            try:
                os.unlink(out_path)
            except OSError:
                pass

    except FileNotFoundError:
        logger.debug("Ghostscript (gs) not found, falling back to pikepdf/pypdf")
    except Exception as e:
        logger.warning("Ghostscript compression failed: %s", str(e))

    # 2. pypdf — pure Python, no system library requirements
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(BytesIO(data))
        writer = PdfWriter()
        for page in reader.pages:
            try:
                page.compress_content_streams()  # Lossless deflate compression
            except Exception:
                pass
            writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        compressed = output.getvalue()
        if len(compressed) < len(data):
            logger.info(
                "pypdf PDF compressed: %d → %d bytes (%.1f%% reduction)",
                len(data), len(compressed),
                (1 - len(compressed) / len(data)) * 100,
            )
            return compressed
    except Exception as e:
        logger.warning("pypdf compression failed: %s", str(e))

    # 3. pikepdf — requires qpdf system library
    try:
        import pikepdf
        with pikepdf.open(BytesIO(data)) as pdf:
            pdf.remove_unreferenced_resources()
            output = BytesIO()
            pdf.save(output, linearize=True, compress_streams=True,
                     object_stream_mode=pikepdf.ObjectStreamMode.generate)
            compressed = output.getvalue()
            if len(compressed) < len(data):
                logger.info(
                    "pikepdf PDF compressed: %d → %d bytes (%.1f%% reduction)",
                    len(data), len(compressed),
                    (1 - len(compressed) / len(data)) * 100,
                )
                return compressed
    except Exception as e:
        logger.warning("pikepdf compression failed: %s", str(e))

    return None



# ---------------------------------------------------------------------------
# Images — lossless mode (new uploads)
# ---------------------------------------------------------------------------

def _compress_image_lossless(data: bytes, ext: str, original_size: int) -> tuple:
    """Losslessly compress an image. Returns (new_ext, bytes) or (ext, None).

    Strategy:
      - JPEG: skipped — cannot be losslessly re-compressed (returns None)
      - PNG/BMP/GIF: converted to lossless WebP (only if smaller)
      - WebP: re-saved with lossless=True (only if smaller)
    """
    if ext in {'.jpg', '.jpeg'}:
        # JPEG is inherently lossy; re-encoding always discards data.
        # Return None to preserve the original.
        return ext, None

    try:
        img = Image.open(BytesIO(data))
        img.verify()
    except (UnidentifiedImageError, OSError):
        logger.warning("Could not open image for lossless compression, using original")
        return ext, None

    try:
        img = Image.open(BytesIO(data))

        if ext in {'.png', '.bmp', '.gif'}:
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            webp_out = BytesIO()
            img.save(webp_out, format='WEBP', lossless=True, quality=100, method=6)
            webp_bytes = webp_out.getvalue()
            if len(webp_bytes) < original_size:
                return '.webp', webp_bytes
            return ext, None

        if ext == '.webp':
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            out = BytesIO()
            img.save(out, format='WEBP', lossless=True, quality=100, method=6)
            candidate = out.getvalue()
            if len(candidate) < original_size:
                return ext, candidate
            return ext, None

        return ext, None

    except Exception:
        logger.exception("Lossless image compression failed, using original")
        return ext, None


# ---------------------------------------------------------------------------
# Images — lossy mode (batch recompression of existing files)
# ---------------------------------------------------------------------------

def _compress_image_lossy(data: bytes, ext: str, original_size: int) -> tuple:
    """Lossily compress an image. Returns (new_ext, bytes) or (ext, None).

    Strategy:
      - JPEG: quality=85, optimize=True (visually identical)
      - PNG → WebP: quality=88, method=6 (significant savings)
      - BMP/GIF → WebP: quality=88, method=6
      - WebP: quality=88, method=6
    """
    try:
        img = Image.open(BytesIO(data))
        img.verify()
    except (UnidentifiedImageError, OSError):
        logger.warning("Could not open image for lossy compression, using original")
        return ext, None

    try:
        img = Image.open(BytesIO(data))

        if ext in {'.jpg', '.jpeg'}:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            out = BytesIO()
            img.save(out, format='JPEG', quality=85, optimize=True)
            candidate = out.getvalue()
            if len(candidate) < original_size:
                return ext, candidate
            return ext, None

        if ext in {'.png', '.bmp', '.gif'}:
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            webp_out = BytesIO()
            img.save(webp_out, format='WEBP', quality=88, method=6)
            webp_bytes = webp_out.getvalue()
            if len(webp_bytes) < original_size:
                return '.webp', webp_bytes
            return ext, None

        if ext == '.webp':
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            out = BytesIO()
            img.save(out, format='WEBP', quality=88, method=6)
            candidate = out.getvalue()
            if len(candidate) < original_size:
                return ext, candidate
            return ext, None

        return ext, None

    except Exception:
        logger.exception("Lossy image compression failed, using original")
        return ext, None