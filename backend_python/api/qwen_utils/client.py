"""
QwenClient — standalone, reusable client for Qwen AI interactions.

Wraps session management, file upload, file parsing, chat creation,
and message sending into a single class that can be used from any
Django view, management command, or future service.

Usage:
    client = QwenClient()
    chat_id = client.create_chat()
    result = client.send_message(chat_id, "Hello", system_prompt="...")
    file_obj = client.upload_file_from_bytes("doc.pdf", data)
    parsed = client.prepare_file_for_qwen("doc.pdf", data)
"""
import logging
import os
from typing import Dict, List, Optional, Tuple

from api import qwen_proxy
from api.qwen_utils.file_upload import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
    classify_file,
    parse_file,
    upload_file,
    upload_file_from_bytes,
    wait_for_parse,
)
from api.qwen_utils.models import get_default_model

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}


class QwenClient:
    """Reusable Qwen AI client. Handles session lifecycle, file upload,
    file parsing, chat creation, and message sending."""

    def __init__(self, model: Optional[str] = None):
        self._model = model
        self._session = None
        self._headers = None
        self._pool_session = None  # tracked for use/fail accounting

    def _ensure_session(self) -> Tuple[object, Dict]:
        """Lazily create and return a Qwen session + headers dict."""
        if self._session is None:
            self._session, _ = qwen_proxy._get_session()
            self._pool_session = self._session
            midtoken = qwen_proxy.get_midtoken(self._session)
            if midtoken:
                self._session.headers['bx-umidtoken'] = midtoken
                self._session.headers['bx-v'] = '2.5.31'
            self._headers = dict(self._session.headers)
        return self._session, self._headers

    @property
    def session(self):
        s, _ = self._ensure_session()
        return s

    @property
    def headers(self):
        _, h = self._ensure_session()
        return h

    def reset_session(self):
        """Force a fresh session on next operation."""
        if self._session:
            qwen_proxy._mark_failed(self._session)
        self._session = None
        self._headers = None
        self._pool_session = None

    def get_model(self) -> str:
        """Return the default Qwen model ID."""
        if self._model:
            return self._model
        return get_default_model()

    def create_chat(self, model: Optional[str] = None) -> Optional[str]:
        """Create a new Qwen chat session. Returns the chat_id or None."""
        model_id = model or self.get_model()
        return qwen_proxy.create_chat(self.session, model=model_id, _pool_session=self._pool_session)

    def send_message(
        self,
        chat_id: str,
        message: str,
        model: Optional[str] = None,
        parent_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        uploaded_files: Optional[List[dict]] = None,
    ) -> Optional[str]:
        """Send a message in a Qwen chat. Returns the response text or None."""
        model_id = model or self.get_model()
        return qwen_proxy.send_message(
            self.session,
            chat_id,
            message,
            model=model_id,
            parent_id=parent_id,
            system_prompt=system_prompt,
            uploaded_files=uploaded_files or [],
            _pool_session=self._pool_session,
        )

    def upload_file_from_bytes(self, filename: str, data: bytes) -> Optional[dict]:
        """Upload file bytes to Qwen OSS. Returns the file_obj dict or None."""
        session, headers = self._ensure_session()
        return upload_file_from_bytes(filename, data, session, headers)

    def upload_file(self, filepath: str) -> Optional[dict]:
        """Upload a local file to Qwen OSS. Returns the file_obj dict or None."""
        session, headers = self._ensure_session()
        return upload_file(filepath, session, headers)

    def parse_uploaded_file(self, file_id: str, poll: bool = True, poll_interval: float = 2, max_wait: float = 120) -> bool:
        """Trigger Qwen's file parsing (OCR for PDFs, etc.).

        If poll=True, waits until parsing completes or times out.
        Returns True if parsing succeeded.
        """
        session, headers = self._ensure_session()
        if not parse_file(file_id, session, headers):
            return False
        if poll:
            return wait_for_parse(file_id, session, headers, interval=poll_interval, max_wait=max_wait)
        return True

    def prepare_file_for_qwen(self, filename: str, data: bytes) -> Optional[Dict]:
        """Upload a file and prepare it for Qwen chat inclusion.

        For images: uploads to OSS, returns file_obj with is_image=True.
        For documents (PDF, DOC, DOCX): uploads to OSS, triggers parse,
            waits for completion, adds parse_meta, returns file_obj.
        For TXT: decodes locally, returns text_content.
        For other types: attempts upload, returns file_obj or None.

        Returns a dict with keys:
            - is_image (bool)
            - has_file (bool)
            - uploaded_files (list[dict] or None)
            - text_content (str or None)
        """
        ext = os.path.splitext(filename)[1].lower()

        if ext == '.txt':
            try:
                text = data.decode('utf-8')
                if text.strip():
                    return {
                        'is_image': False,
                        'has_file': False,
                        'uploaded_files': None,
                        'text_content': text,
                    }
            except UnicodeDecodeError:
                pass
            return None

        if ext not in ALLOWED_EXTENSIONS:
            return None

        file_obj = self.upload_file_from_bytes(filename, data)
        if not file_obj:
            return None

        is_image = ext in IMAGE_EXTENSIONS
        is_document = ext in DOCUMENT_EXTENSIONS and not is_image

        if is_document:
            file_id = file_obj.get('id', '')
            if file_id:
                self.parse_uploaded_file(file_id, poll=True)
                file_obj.setdefault('file', {}).setdefault('meta', {})['parse_meta'] = {'parse_status': 'success'}

        return {
            'is_image': is_image,
            'has_file': True,
            'uploaded_files': [file_obj],
            'text_content': None,
        }

    def send_doc_task(
        self,
        prepared: Dict,
        file_prompt: str,
        text_prompt: str,
        system_prompt: str,
        model: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Run a Qwen task against either uploaded file(s) or extracted text.

        Returns (result_text, error_message). On success, error is None.
        On failure, result is None and error is a human-readable string.
        """
        chat_id = self.create_chat(model=model)
        if not chat_id:
            return None, 'Could not start AI session — try again'

        if prepared.get('has_file') or prepared.get('is_image'):
            result = self.send_message(
                chat_id,
                file_prompt,
                model=model,
                parent_id=None,
                system_prompt=system_prompt,
                uploaded_files=prepared.get('uploaded_files') or [],
            )
        else:
            full_text = text_prompt + "\n\n--- DOCUMENT CONTENT ---\n" + (prepared.get('text_content') or '') + "\n--- END ---"
            result = self.send_message(
                chat_id,
                full_text,
                model=model,
                parent_id=None,
                system_prompt=system_prompt,
            )

        if not result:
            return None, 'AI returned an empty response'
        return result, None

    def two_turn_generation(
        self,
        outline_prompt: str,
        full_prompt: str,
        combined_text: str,
        system_prompt: str,
        model: Optional[str] = None,
        exclusion_text: str = '',
    ) -> Tuple[Optional[str], Optional[str]]:
        """Run a 2-turn Qwen generation: outline first, then expand.

        Returns (final_result, error_message).
        """
        chat_id = self.create_chat(model=model)
        if not chat_id:
            return None, 'Could not start AI session — try again'

        text_with_docs = outline_prompt + "\n\n--- DOCUMENTS ---\n" + combined_text + "\n--- END ---"
        outline_result = self.send_message(
            chat_id, text_with_docs,
            model=model, parent_id=None,
            system_prompt=system_prompt,
        )
        if not outline_result:
            return None, 'AI returned an empty response'

        expanded = full_prompt + "\n\n--- OUTLINE ---\n" + outline_result + "\n--- END ---\n\n--- DOCUMENTS ---\n" + combined_text + "\n--- END ---"
        if exclusion_text:
            expanded += "\n\n" + exclusion_text

        result = self.send_message(
            chat_id, expanded,
            model=model, parent_id=None,
            system_prompt=system_prompt,
        )
        if not result:
            return None, 'AI returned an empty response'

        return result, None

    def simple_chat(
        self,
        message: str,
        system_prompt: str = '',
        model: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Send a single message to a fresh Qwen chat. Returns (result, error)."""
        chat_id = self.create_chat(model=model)
        if not chat_id:
            return None, 'Could not start AI session — try again'
        result = self.send_message(
            chat_id, message,
            model=model, parent_id=None,
            system_prompt=system_prompt or None,
        )
        if not result:
            return None, 'AI returned an empty response'
        return result, None