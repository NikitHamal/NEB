from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings
from django.db import transaction

from api.background_agent.events import emit
from api.models import BackgroundAgentSession
from api.utils import now_ms

ACTIVE_STATUSES = {'queued', 'preparing', 'running'}
TERMINAL_STATUSES = {'completed', 'failed', 'cancelled', 'paused', 'waiting'}


def archive_session(session: BackgroundAgentSession) -> BackgroundAgentSession:
    if session.status in ACTIVE_STATUSES:
        raise ValueError('Pause or stop the task before archiving it')
    if not session.archived_at:
        session.archived_at = now_ms()
        session.updated_at = session.archived_at
        session.save(update_fields=['archived_at', 'updated_at'])
        emit(session, 'session.archived', 'Session archived')
    return session


def restore_session(session: BackgroundAgentSession) -> BackgroundAgentSession:
    if session.archived_at:
        session.archived_at = 0
        session.updated_at = now_ms()
        session.save(update_fields=['archived_at', 'updated_at'])
        emit(session, 'session.restored', 'Session restored')
    return session


def delete_session(session: BackgroundAgentSession) -> None:
    if session.status in ACTIVE_STATUSES:
        raise ValueError('Stop the task before deleting it')
    paths = _session_paths(session)
    with transaction.atomic():
        session.delete()
    for path in paths:
        _remove_path(path)


def _session_paths(session: BackgroundAgentSession) -> list[Path]:
    roots = [_root_path()]
    values = [session.workspace_path]
    values.extend(session.artifacts.values_list('file_path', flat=True))
    values.extend(session.attachments.values_list('file_path', flat=True))
    output = []
    for value in values:
        if not value:
            continue
        path = Path(value).resolve()
        if any(_is_within(path, root) for root in roots):
            output.append(path)
    output.sort(key=lambda item: len(item.parts), reverse=True)
    return output


def _root_path() -> Path:
    return Path(getattr(settings, 'BACKGROUND_AGENT_ROOT', settings.BASE_DIR / 'background_agent_data')).resolve()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _remove_path(path: Path) -> None:
    try:
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            path.unlink(missing_ok=True)
    except OSError:
        pass
