"""Human-readable labels for background-agent tool calls.

Used by the runner to emit a single clean event/message per tool call
(e.g. "Read src/app.py") and mirrored by the frontend so a tool call always
renders as one tidy line instead of a start/result/completed triple.
"""
from __future__ import annotations

from typing import Any


def _short(text: Any, limit: int = 72) -> str:
    value = str(text or '').replace('\n', ' ').strip()
    return value if len(value) <= limit else value[:limit - 1] + '…'


def _join_paths(paths: Any) -> str:
    if not paths:
        return 'all'
    if isinstance(paths, (list, tuple)):
        items = [str(p) for p in paths if p]
        return _short(', '.join(items)) if items else 'all'
    return _short(paths)


def tool_label(tool: str, arguments: dict | None = None, *, ok: bool = True) -> str:
    """Return a concise, human-friendly label for a single tool call."""
    a = arguments or {}
    name = (tool or '').strip()
    arrow = ' → '

    mapping = {
        'read_file': lambda: f'Read {_short(a.get("path"))}',
        'write_file': lambda: f'Write {_short(a.get("path"))}',
        'edit_file': lambda: f'Edit {_short(a.get("path"))}',
        'multi_edit': lambda: f'Edit {_short(a.get("path"))} · {len(a.get("edits") or [])} changes',
        'delete_file': lambda: f'Delete {_short(a.get("path"))}',
        'copy_file': lambda: f'Copy {_short(a.get("source"))}{arrow}{_short(a.get("destination"))}',
        'move_file': lambda: f'Move {_short(a.get("source"))}{arrow}{_short(a.get("destination"))}',
        'create_directory': lambda: f'Create dir {_short(a.get("path"))}',
        'list_files': lambda: f'List {_short(a.get("path") or ".")}',
        'glob_files': lambda: f'Glob {_short(a.get("pattern") or "*")}',
        'search_text': lambda: f'Search "{_short(a.get("query"), 48)}"',
        'done': lambda: f'Done · {_short(a.get("summary"), 56)}',
        'ask_user': lambda: f'Ask · {_short(a.get("question"), 56)}',
        'apply_patch': lambda: 'Apply patch',
        'run_command': lambda: f'Run {_short(" ".join(a.get("argv") or []))}',
        'git_status': lambda: 'Git status',
        'git_diff': lambda: 'Git diff',
        'git_log': lambda: 'Git log',
        'git_stage': lambda: f'Stage {_join_paths(a.get("paths"))}',
        'git_commit': lambda: f'Commit · {_short(a.get("message"), 56)}',
        'git_push': lambda: f'Push {_short(a.get("branch") or "HEAD")}',
        'update_plan': lambda: f'Plan · {len(a.get("todos") or [])} steps',
        'git_pull': lambda: 'Pull',
        'git_restore': lambda: f'Restore {_join_paths(a.get("paths"))}',
    }
    builder = mapping.get(name)
    if builder:
        try:
            return builder()
        except Exception:
            pass
    return name.replace('_', ' ').title() or 'Tool'


# Frontend mirror — keep in sync with background-agent-session.js TOOL_LABELS.
TOOL_VERBS = {
    'read_file': 'Read',
    'write_file': 'Write',
    'edit_file': 'Edit',
    'multi_edit': 'Edit',
    'delete_file': 'Delete',
    'copy_file': 'Copy',
    'move_file': 'Move',
    'create_directory': 'Create dir',
    'list_files': 'List',
    'glob_files': 'Glob',
    'search_text': 'Search',
    'done': 'Done',
    'ask_user': 'Ask',
    'apply_patch': 'Apply patch',
    'run_command': 'Run',
    'git_status': 'Git status',
    'git_diff': 'Git diff',
    'git_log': 'Git log',
    'git_stage': 'Stage',
    'git_commit': 'Commit',
    'git_push': 'Push',
    'git_pull': 'Pull',
    'git_restore': 'Restore',
    'update_plan': 'Plan',
}
