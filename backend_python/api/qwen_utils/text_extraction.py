"""
Text extraction — standalone functions to extract plain text from files.

Uses pypdf for PDFs and UTF-8 decode for TXT files. Images and other
binary formats return None (they should go through Qwen file upload instead).

This module has no Django dependencies beyond django.core.files.storage,
making it reusable from any context (views, management commands, etc.).
"""
import io
import logging
import os

logger = logging.getLogger(__name__)

MAX_TEXT_CHARS = 50000


def extract_text_from_file(file_url: str, file_name: str) -> str | None:
    """Extract text from a Django-stored file.

    Handles path resolution (/media/ prefix, leading slash).
    Returns extracted text (up to MAX_TEXT_CHARS) or None on failure.
    """
    if not file_url:
        return None

    file_path = _resolve_storage_path(file_url)
    if file_path is None:
        return None

    ext = os.path.splitext(file_name or '')[1].lower()

    try:
        from django.core.files.storage import default_storage

        if ext == '.txt':
            with default_storage.open(file_path, 'r') as f:
                text = f.read()
            if isinstance(text, bytes):
                text = text.decode('utf-8', errors='replace')
            return text.strip()[:MAX_TEXT_CHARS] if text and text.strip() else None

        if ext == '.pdf':
            with default_storage.open(file_path, 'rb') as f:
                file_data = f.read()
            return extract_text_from_pdf_bytes(file_data)

    except Exception as e:
        logger.warning('Failed to extract text from %s: %s', file_name, e)

    return None


def extract_text_from_pdf_bytes(data: bytes) -> str | None:
    """Extract text from raw PDF bytes using pypdf. Returns up to MAX_TEXT_CHARS."""
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(data))
        pages = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)
        combined = '\n\n'.join(pages)
        return combined.strip()[:MAX_TEXT_CHARS] if combined.strip() else None
    except Exception as e:
        logger.warning('Failed to extract PDF text: %s', e)
        return None


def extract_text_from_txt_bytes(data: bytes) -> str | None:
    """Decode raw TXT bytes as UTF-8. Returns up to MAX_TEXT_CHARS."""
    try:
        text = data.decode('utf-8')
        return text.strip()[:MAX_TEXT_CHARS] if text.strip() else None
    except UnicodeDecodeError:
        return None


def extract_text_from_bytes(file_name: str, data: bytes) -> str | None:
    """Extract text from raw bytes based on file extension.

    Does NOT need Django storage — works with in-memory bytes.
    """
    ext = os.path.splitext(file_name)[1].lower()

    if ext == '.txt':
        return extract_text_from_txt_bytes(data)

    if ext == '.pdf':
        return extract_text_from_pdf_bytes(data)

    return None


def read_file_bytes(file_url: str) -> bytes | None:
    """Read raw bytes from a Django-stored file.

    Handles path resolution (/media/ prefix, leading slash).
    Returns bytes or None on failure.
    """
    if not file_url:
        return None

    file_path = _resolve_storage_path(file_url)
    if file_path is None:
        return None

    try:
        from django.core.files.storage import default_storage
        if not default_storage.exists(file_path):
            return None
        with default_storage.open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        logger.warning('Failed to read file bytes from %s: %s', file_url, e)
        return None


def _resolve_storage_path(file_url: str) -> str | None:
    """Resolve a /media/ URL path to a Django storage path."""
    try:
        from django.core.files.storage import default_storage

        file_path = file_url
        if file_path.startswith('/media/'):
            file_path = file_path[len('/media/'):]
        elif file_path.startswith('/'):
            file_path = file_path.lstrip('/')

        if not default_storage.exists(file_path):
            return None
        return file_path
    except Exception:
        return None