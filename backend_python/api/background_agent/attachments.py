"""Attachment storage and prompt integration for background-agent sessions."""
from __future__ import annotations

import hashlib
import mimetypes
import re
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from api.models import BackgroundAgentAttachment, BackgroundAgentMessage, BackgroundAgentSession
from api.utils import now_ms, uuid_str

TEXT_EXTENSIONS = {
    '.txt', '.md', '.markdown', '.rst', '.csv', '.tsv', '.json', '.jsonl', '.yaml', '.yml',
    '.toml', '.ini', '.cfg', '.conf', '.xml', '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.vue', '.svelte', '.py', '.pyi', '.rb', '.php',
    '.java', '.kt', '.kts', '.swift', '.go', '.rs', '.c', '.h', '.cc', '.cpp', '.hpp', '.cs', '.sh',
    '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd', '.sql', '.graphql', '.gql', '.gradle', '.properties',
    '.dockerfile', '.gitignore', '.editorconfig', '.env.example', '.lock', '.tex', '.log',
}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
QWEN_FILE_EXTENSIONS = IMAGE_EXTENSIONS | {
    '.pdf', '.txt', '.doc', '.docx', '.mp4', '.avi', '.mov', '.m4v', '.mkv', '.webm',
    '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a',
}
BLOCKED_EXTENSIONS = {
    '.exe', '.dll', '.so', '.dylib', '.com', '.scr', '.msi', '.apk', '.ipa', '.deb', '.rpm',
    '.dmg', '.iso', '.img', '.bin', '.class', '.jar', '.war', '.pyc', '.pyo',
}


def upload_limits() -> tuple[int, int]:
    max_files = max(1, min(int(getattr(settings, 'BACKGROUND_AGENT_MAX_ATTACHMENTS', 5)), 10))
    max_bytes = max(1024, min(int(getattr(settings, 'BACKGROUND_AGENT_MAX_ATTACHMENT_BYTES', 20 * 1024 * 1024)), 50 * 1024 * 1024))
    return max_files, max_bytes


def _safe_filename(name: str) -> str:
    clean = Path(name or 'attachment').name
    clean = re.sub(r'[^A-Za-z0-9._()\- ]+', '_', clean).strip(' .')
    return clean[:180] or 'attachment'


def _root_for_session(session: BackgroundAgentSession) -> Path:
    root = Path(getattr(settings, 'BACKGROUND_AGENT_ROOT', settings.BASE_DIR / 'background_agent_data')).resolve()
    target = (root / 'sessions' / str(session.id) / 'uploads').resolve()
    target.relative_to(root)
    target.mkdir(parents=True, exist_ok=True)
    return target


def attachment_kind(filename: str, content_type: str = '') -> str:
    ext = Path(filename).suffix.lower()
    mime = (content_type or '').lower()
    if ext in IMAGE_EXTENSIONS or mime.startswith('image/'):
        return 'image'
    if ext in TEXT_EXTENSIONS or mime.startswith('text/') or mime in {'application/json', 'application/xml'}:
        return 'text'
    if ext == '.pdf' or mime == 'application/pdf':
        return 'pdf'
    if mime.startswith('audio/'):
        return 'audio'
    if mime.startswith('video/'):
        return 'video'
    return 'document'


def save_uploads(
    session: BackgroundAgentSession,
    message: BackgroundAgentMessage,
    uploads: list[UploadedFile],
) -> list[BackgroundAgentAttachment]:
    max_files, max_bytes = upload_limits()
    if len(uploads) > max_files:
        raise ValueError(f'Attach up to {max_files} files per message')
    validated = []
    for upload in uploads:
        filename = _safe_filename(upload.name)
        ext = Path(filename).suffix.lower()
        if ext in BLOCKED_EXTENSIONS:
            raise ValueError(f'{filename} is not an allowed attachment type')
        if upload.size > max_bytes:
            raise ValueError(f'{filename} exceeds the {max_bytes // (1024 * 1024)} MB attachment limit')
        validated.append((upload, filename, ext))
    root = _root_for_session(session)
    rows: list[BackgroundAgentAttachment] = []
    for upload, filename, ext in validated:
        digest = hashlib.sha256()
        stored_name = f'{uuid_str()}-{filename}'
        path = (root / stored_name).resolve()
        path.relative_to(root)
        with path.open('wb') as destination:
            for chunk in upload.chunks():
                digest.update(chunk)
                destination.write(chunk)
        content_type = (getattr(upload, 'content_type', '') or mimetypes.guess_type(filename)[0] or 'application/octet-stream')[:160]
        row = BackgroundAgentAttachment.objects.create(
            id=uuid_str(),
            session=session,
            message=message,
            file_name=filename,
            stored_name=stored_name,
            file_path=str(path),
            content_type=content_type,
            extension=ext[:24],
            kind=attachment_kind(filename, content_type),
            size_bytes=path.stat().st_size,
            sha256=digest.hexdigest(),
            created_at=now_ms(),
        )
        rows.append(row)
    return rows


def safe_attachment_path(attachment: BackgroundAgentAttachment) -> Path | None:
    root = Path(getattr(settings, 'BACKGROUND_AGENT_ROOT', settings.BASE_DIR / 'background_agent_data')).resolve()
    path = Path(attachment.file_path).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path if path.is_file() else None


def read_text_preview(attachment: BackgroundAgentAttachment, max_chars: int | None = None) -> str:
    if attachment.kind != 'text':
        return ''
    path = safe_attachment_path(attachment)
    if not path:
        return ''
    limit = max_chars or int(getattr(settings, 'BACKGROUND_AGENT_ATTACHMENT_TEXT_CHARS', 24000))
    data = path.read_bytes()[: max(limit * 4, 65536)]
    if b'\x00' in data:
        return ''
    text = data.decode('utf-8', errors='replace')
    if len(text) > limit:
        text = text[:limit] + '\n[attachment excerpt truncated]'
    return text


def prompt_attachment_block(message: BackgroundAgentMessage) -> str:
    rows = list(message.attachments.order_by('created_at'))
    if not rows:
        return ''
    parts = ['ATTACHMENTS:']
    for attachment in rows:
        parts.append(
            f'- {attachment.file_name} ({attachment.kind}, {attachment.size_bytes} bytes, sha256 {attachment.sha256[:12]})'
        )
        excerpt = read_text_preview(attachment)
        if excerpt:
            parts.append(f'```{attachment.extension.lstrip(".") or "text"}\n{excerpt}\n```')
    return '\n'.join(parts)


def qwen_files_for_iteration(session: BackgroundAgentSession) -> tuple[list[str], list[BackgroundAgentAttachment]]:
    max_files, _ = upload_limits()
    candidates = list(session.attachments.filter(
        extension__in=QWEN_FILE_EXTENSIONS,
    ).order_by('-created_at')[:max_files])
    candidates.reverse()
    paths: list[str] = []
    selected: list[BackgroundAgentAttachment] = []
    for attachment in candidates:
        if attachment.extension not in QWEN_FILE_EXTENSIONS:
            continue
        path = safe_attachment_path(attachment)
        if path:
            paths.append(str(path))
            selected.append(attachment)
    return paths, selected


def mark_qwen_files_sent(attachments: list[BackgroundAgentAttachment], iteration: int) -> None:
    if not attachments:
        return
    BackgroundAgentAttachment.objects.filter(pk__in=[row.pk for row in attachments]).update(sent_iteration=iteration)
