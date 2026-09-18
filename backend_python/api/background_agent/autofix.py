"""CI auto-fix watcher - REMOVED (Sep 2026 security audit).

The watcher embedded raw CI logs into the tool-calling agent's prompt with no
sanitization envelope (prompt-injection entry point) and autonomously queued
repair sessions. It has been permanently disabled: this module is kept only so
existing imports keep working. ``scan_failed_runs`` is a no-op returning 0.

The ``autofix_enabled`` / ``BackgroundAgentAutofixRun`` database columns are
intentionally left in place to avoid a destructive migration; they are no
longer read or written anywhere.
"""
from __future__ import annotations


def scan_failed_runs(max_sessions: int = 3) -> int:
    """Disabled stub - always queues nothing."""
    return 0
