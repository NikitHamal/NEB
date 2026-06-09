"""
Document parsing service — parse-once architecture.

On upload, a StudyDocument is created with parse_status='pending'.
This module runs the parsing pipeline in a background daemon thread:

  1. Upload file to Qwen OSS
  2. Trigger Qwen's file parsing (OCR for PDFs/images)
  3. Send an "extract raw text" prompt to Qwen with the parsed file
  4. Store the extracted text in StudyDocument.parsed_text

Once parsed, all generation views (summary, mindmap, quiz, flashcards)
use the stored parsed_text directly — no re-uploading or re-parsing.

The parsed text and Qwen file_id are cached for up to 1 hour (Qwen's
session limit). Within that window, the same file can be reused across
multiple generation calls without re-uploading.
"""
import logging
import threading
import time
from typing import Optional

from django.db import transaction

from api.models import StudyDocument
from api.utils import now_ms

logger = logging.getLogger(__name__)

PARSE_STATUS_PENDING = 'pending'
PARSE_STATUS_UPLOADING = 'uploading'
PARSE_STATUS_PARSING = 'parsing'
PARSE_STATUS_EXTRACTING = 'extracting'
PARSE_STATUS_READY = 'ready'
PARSE_STATUS_FAILED = 'failed'

EXTRACT_RAW_TEXT_PROMPT = (
    "Output the raw parsed text of the attached file exactly as it is stored "
    "in your context, without any summarization, formatting, or modification. "
    "Preserve the original structure, headings, paragraphs, and all content verbatim. "
    "Do not add any commentary, introduction, or explanation — just the raw text."
)

MAX_PARSED_TEXT_CHARS = 80000


def start_parse(doc_id: str) -> bool:
    """Kick off background parsing for a StudyDocument.

    Sets parse_status to 'uploading' and starts a daemon thread.
    Returns True if the thread was started, False if parsing is already
    in progress or the doc doesn't exist.
    """
    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        logger.warning('start_parse: StudyDocument %s not found', doc_id)
        return False

    if doc.parse_status in (PARSE_STATUS_UPLOADING, PARSE_STATUS_PARSING, PARSE_STATUS_EXTRACTING):
        logger.info('start_parse: doc %s already parsing (status=%s)', doc_id, doc.parse_status)
        return False

    if not doc.file_url:
        logger.warning('start_parse: doc %s has no file_url', doc_id)
        doc.parse_status = PARSE_STATUS_FAILED
        doc.parse_error = 'No file attached'
        doc.save(update_fields=['parse_status', 'parse_error'])
        return False

    doc.parse_status = PARSE_STATUS_UPLOADING
    doc.parse_error = ''
    doc.updated_at = now_ms()
    doc.save(update_fields=['parse_status', 'parse_error', 'updated_at'])

    t = threading.Thread(target=_parse_worker, args=(doc_id,), daemon=True, name=f'parse-doc-{doc_id}')
    t.start()
    logger.info('start_parse: started background parsing for doc %s', doc_id)
    return True


def reparse(doc_id: str) -> bool:
    """Force re-parse a document (e.g. after failure). Resets status and starts parsing."""
    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return False

    doc.parse_status = PARSE_STATUS_PENDING
    doc.parse_error = ''
    doc.updated_at = now_ms()
    doc.save(update_fields=['parse_status', 'parse_error', 'updated_at'])
    return start_parse(doc_id)


STUCK_TIMEOUT_MS = 10 * 60 * 1000  # 10 minutes


def get_parse_status(doc_id: str) -> dict:
    """Return the current parse status of a document.

    If a doc has been in an intermediate state (uploading/parsing/extracting)
    for longer than STUCK_TIMEOUT_MS, auto-mark it as failed so it can be re-parsed.
    """
    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return {'status': 'not_found', 'error': 'Document not found'}

    if doc.parse_status in (PARSE_STATUS_UPLOADING, PARSE_STATUS_PARSING, PARSE_STATUS_EXTRACTING):
        updated_at = doc.updated_at or 0
        now = now_ms()
        if updated_at and (now - updated_at) > STUCK_TIMEOUT_MS:
            StudyDocument.objects.filter(pk=doc_id).update(
                parse_status=PARSE_STATUS_FAILED,
                parse_error='Parsing timed out — please try again',
            )
            doc.refresh_from_db()

    return {
        'id': doc_id,
        'status': doc.parse_status,
        'parsedTextLength': len(doc.parsed_text) if doc.parsed_text else 0,
        'error': doc.parse_error,
        'parsedAt': doc.parsed_at,
    }


def _parse_worker(doc_id: str):
    """Background thread: upload → parse → extract raw text → store."""
    from api.qwen_utils.client import QwenClient
    from api.qwen_utils.text_extraction import extract_text_from_file, read_file_bytes

    client = QwenClient()

    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        logger.error('_parse_worker: doc %s disappeared', doc_id)
        return

    now = now_ms()

    # Step 1: Read file bytes
    try:
        file_data = read_file_bytes(doc.file_url)
    except Exception as e:
        logger.error('_parse_worker: failed to read file for doc %s: %s', doc_id, e)
        _mark_failed(doc_id, f'Failed to read file: {e}')
        return

    if file_data is None:
        _mark_failed(doc_id, 'File not found or empty')
        return

    # Step 2: Upload to Qwen OSS
    try:
        doc = _refresh_doc(doc_id)
        doc.parse_status = PARSE_STATUS_UPLOADING
        doc.updated_at = now
        doc.save(update_fields=['parse_status', 'updated_at'])

        file_obj = client.upload_file_from_bytes(doc.file_name or 'document.pdf', file_data)
        if not file_obj:
            _mark_failed(doc_id, 'Failed to upload file to AI service')
            return

        qwen_file_id = file_obj.get('id', '')
        doc = _refresh_doc(doc_id)
        doc.qwen_file_id = qwen_file_id
        doc.save(update_fields=['qwen_file_id'])

    except Exception as e:
        logger.error('_parse_worker: upload failed for doc %s: %s', doc_id, e)
        _mark_failed(doc_id, f'Upload failed: {e}')
        return

    # Step 3: Trigger Qwen file parsing (OCR for PDFs)
    import os
    ext = os.path.splitext(doc.file_name or '')[1].lower()
    is_image = ext in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
    is_document = ext in {'.pdf', '.doc', '.docx'} and not is_image

    if is_document and qwen_file_id:
        try:
            doc = _refresh_doc(doc_id)
            doc.parse_status = PARSE_STATUS_PARSING
            doc.updated_at = now_ms()
            doc.save(update_fields=['parse_status', 'updated_at'])

            success = client.parse_uploaded_file(qwen_file_id, poll=True, poll_interval=2, max_wait=120)
            if not success:
                logger.warning('_parse_worker: Qwen parse did not complete for doc %s, proceeding with local extraction', doc_id)
        except Exception as e:
            logger.warning('_parse_worker: Qwen parse error for doc %s: %s, proceeding with local extraction', doc_id, e)

    # Step 4: Extract raw text via Qwen prompt
    # For images and parsed documents, use Qwen's understanding of the file.
    # For TXT files, use local extraction.
    extracted_text = None

    if ext == '.txt':
        try:
            extracted_text = file_data.decode('utf-8')
        except UnicodeDecodeError:
            extracted_text = file_data.decode('utf-8', errors='replace')
    elif is_image or (is_document and qwen_file_id):
        # Use Qwen's file understanding with the extract-raw-text prompt
        try:
            doc = _refresh_doc(doc_id)
            doc.parse_status = PARSE_STATUS_EXTRACTING
            doc.updated_at = now_ms()
            doc.save(update_fields=['parse_status', 'updated_at'])

            chat_id = client.create_chat()
            if chat_id:
                file_obj_with_meta = dict(file_obj)
                if is_document:
                    file_obj_with_meta.setdefault('file', {}).setdefault('meta', {})['parse_meta'] = {'parse_status': 'success'}

                result = client.send_message(
                    chat_id,
                    EXTRACT_RAW_TEXT_PROMPT,
                    system_prompt='You are a document text extractor. Output the exact raw text content of the provided file without any modification, commentary, or formatting changes.',
                    uploaded_files=[file_obj_with_meta],
                )
                if result:
                    extracted_text = result
        except Exception as e:
            logger.error('_parse_worker: Qwen text extraction failed for doc %s: %s', doc_id, e)

    # Fallback: try local extraction if Qwen didn't produce text
    if not extracted_text or not extracted_text.strip():
        if is_document:
            logger.info('_parse_worker: falling back to local extraction for doc %s', doc_id)
            extracted_text = extract_text_from_file(doc.file_url, doc.file_name or '') or ''

    if not extracted_text or not extracted_text.strip():
        _mark_failed(doc_id, 'Could not extract any text from this document')
        return

    # Step 5: Store parsed text
    extracted_text = extracted_text[:MAX_PARSED_TEXT_CHARS]
    StudyDocument.objects.filter(pk=doc_id).update(
        parse_status=PARSE_STATUS_READY,
        parsed_text=extracted_text,
        parsed_at=now_ms(),
        parse_error='',
    )
    logger.info('_parse_worker: successfully parsed doc %s (%d chars)', doc_id, len(extracted_text))


def _mark_failed(doc_id: str, error: str):
    """Mark a document as failed."""
    StudyDocument.objects.filter(pk=doc_id).update(
        parse_status=PARSE_STATUS_FAILED,
        parse_error=error,
    )


def _refresh_doc(doc_id: str) -> StudyDocument:
    """Re-fetch the document from DB to get fresh state."""
    return StudyDocument.objects.get(pk=doc_id)