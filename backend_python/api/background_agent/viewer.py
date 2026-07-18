"""Safe workspace and attachment previews for the background-agent UI."""
from __future__ import annotations

import mimetypes
from pathlib import Path

from django.conf import settings

from api.background_agent.attachments import safe_attachment_path
from api.background_agent.workspace import GitWorkspace
from api.models import BackgroundAgentAttachment, BackgroundAgentSession

TEXT_EXTENSIONS = {
    '.txt', '.md', '.markdown', '.rst', '.csv', '.tsv', '.json', '.jsonl', '.yaml', '.yml',
    '.toml', '.ini', '.cfg', '.conf', '.xml', '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.vue', '.svelte', '.py', '.pyi', '.rb', '.php',
    '.java', '.kt', '.kts', '.swift', '.go', '.rs', '.c', '.h', '.cc', '.cpp', '.hpp', '.cs', '.sh',
    '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd', '.sql', '.graphql', '.gql', '.gradle',
    '.properties', '.dockerfile', '.gitignore', '.editorconfig', '.lock', '.tex', '.log',
}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
SKIP_DIRS = {'.git', 'node_modules', '.gradle', '.idea', '.venv', 'venv', '__pycache__', 'dist', 'build', 'target'}


def preview_mode(name: str, content_type: str = '') -> str:
    ext = Path(name).suffix.lower()
    mime = (content_type or mimetypes.guess_type(name)[0] or '').lower()
    if ext in {'.md', '.markdown'}:
        return 'markdown'
    if ext in IMAGE_EXTENSIONS or mime.startswith('image/'):
        return 'image'
    if ext == '.pdf' or mime == 'application/pdf':
        return 'pdf'
    if mime.startswith('audio/'):
        return 'audio'
    if mime.startswith('video/'):
        return 'video'
    if ext in TEXT_EXTENSIONS or mime.startswith('text/') or mime in {'application/json', 'application/xml'}:
        return 'text'
    return 'binary'


def workspace_file(session: BackgroundAgentSession, relative: str) -> Path | None:
    if not session.workspace_path:
        return None
    workspace = GitWorkspace(session.project, session)
    return workspace.safe_path(relative, must_exist=True)


def list_workspace_files(session: BackgroundAgentSession) -> list[dict]:
    root = Path(session.workspace_path).resolve() if session.workspace_path else None
    if not root or not root.is_dir():
        return []
    workspace = GitWorkspace(session.project, session)
    changed = set(workspace.changed_files())
    limit = max(100, min(int(getattr(settings, 'BACKGROUND_AGENT_VIEWER_FILE_LIMIT', 2500)), 10000))
    rows: list[dict] = []
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith('.') for part in relative_path.parts[:-1]):
            continue
        relative = relative_path.as_posix()
        if not workspace.safe_path(relative, must_exist=True):
            continue
        content_type = mimetypes.guess_type(relative)[0] or 'application/octet-stream'
        rows.append({
            'path': relative,
            'name': path.name,
            'sizeBytes': path.stat().st_size,
            'contentType': content_type,
            'mode': preview_mode(relative, content_type),
            'changed': relative in changed,
        })
        if len(rows) >= limit:
            break
    rows.sort(key=lambda item: (not item['changed'], item['path'].lower()))
    return rows


def read_workspace_text(session: BackgroundAgentSession, relative: str) -> dict:
    path = workspace_file(session, relative)
    if not path or not path.is_file():
        raise FileNotFoundError('File not found')
    content_type = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    mode = preview_mode(path.name, content_type)
    max_bytes = max(65536, min(int(getattr(settings, 'BACKGROUND_AGENT_VIEWER_TEXT_BYTES', 2 * 1024 * 1024)), 8 * 1024 * 1024))
    data = path.read_bytes()
    truncated = len(data) > max_bytes
    data = data[:max_bytes]
    content = ''
    if mode in {'text', 'markdown'} and b'\x00' not in data:
        content = data.decode('utf-8', errors='replace')
    return {
        'path': relative,
        'name': path.name,
        'sizeBytes': path.stat().st_size,
        'contentType': content_type,
        'mode': mode,
        'content': content,
        'truncated': truncated,
    }


def attachment_payload(attachment: BackgroundAgentAttachment) -> dict:
    path = safe_attachment_path(attachment)
    if not path:
        raise FileNotFoundError('Attachment file is missing')
    mode = preview_mode(attachment.file_name, attachment.content_type)
    max_bytes = max(65536, min(int(getattr(settings, 'BACKGROUND_AGENT_VIEWER_TEXT_BYTES', 2 * 1024 * 1024)), 8 * 1024 * 1024))
    content = ''
    truncated = False
    if mode in {'text', 'markdown'}:
        data = path.read_bytes()
        truncated = len(data) > max_bytes
        content = data[:max_bytes].decode('utf-8', errors='replace')
    return {
        'id': attachment.id,
        'name': attachment.file_name,
        'sizeBytes': attachment.size_bytes,
        'contentType': attachment.content_type,
        'mode': mode,
        'content': content,
        'truncated': truncated,
    }
