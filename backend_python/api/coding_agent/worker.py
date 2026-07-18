"""Worker logic — runs one session at a time, advancing the runtime."""
from __future__ import annotations

import logging
import time
from typing import Optional

from .models import CodingAgentSession
from .realtime import announce_status
from .runtime import AgentRuntime

logger = logging.getLogger(__name__)


def advance_session(session_id: str, max_steps: int = 1) -> CodingAgentSession:
    session = CodingAgentSession.objects.select_related('project').get(pk=session_id)

    def _broadcast(label: str, status_value: str, **extra):
        try:
            owner_user_id = session.project.owner_user_id
            announce_status(session.id, status_value, event=label, owner_user_id=owner_user_id, **extra)
        except Exception:  # noqa: BLE001
            logger.exception('broadcast failed')

    runtime = AgentRuntime(
        session=session,
        on_event=lambda ev: _broadcast(ev.event_type, session.status, summary=ev.summary[:240]),
    )
    if session.status == CodingAgentSession.STATUS_QUEUED:
        runtime.bootstrap()
        _broadcast('agent.bootstrap', CodingAgentSession.STATUS_RUNNING)

    for step_n in range(max_steps):
        session.refresh_from_db()
        if session.status not in {CodingAgentSession.STATUS_RUNNING, CodingAgentSession.STATUS_SETUP}:
            return session
        try:
            result = runtime.step()
        except Exception as e:  # noqa: BLE001
            logger.exception('runtime.step failed: %s', e)
            session.error_message = ('Internal runtime error: ' + str(e))[:4000]
            session.status = CodingAgentSession.STATUS_AWAITING_INPUT
            session.save(update_fields=['error_message', 'status', 'updated_at'])
            _broadcast('agent.runtime_error', session.status, summary=str(e)[:240])
            return session
        if result.finished or session.is_terminal() or session.status != CodingAgentSession.STATUS_RUNNING:
            _broadcast('agent.status', session.status)
            return session
    return session


def advance_queued_sessions(max_sessions: int = 1, max_steps_per_session: int = 4) -> int:
    """Find queued and stalled-running sessions and advance them.

    A 'stalled-running' session is a session still in STATUS_RUNNING but whose
    last_activity_at is older than STALL_AGE_MS — picked up by the worker in
    case the previous run was killed mid-step.
    """
    STALL_AGE_MS = 90_000
    cutoff = int(time.time() * 1000) - STALL_AGE_MS
    qs = CodingAgentSession.objects.filter(
        status__in=[CodingAgentSession.STATUS_QUEUED, CodingAgentSession.STATUS_SETUP]
    ) | CodingAgentSession.objects.filter(
        status=CodingAgentSession.STATUS_RUNNING,
        last_activity_at__lt=cutoff,
    )
    sessions = list(qs.order_by('priority', 'created_at')[:max_sessions])
    n = 0
    for session in sessions:
        try:
            advance_session(session.id, max_steps=max_steps_per_session)
            n += 1
        except Exception as e:  # noqa: BLE001
            logger.exception('worker advance failed for %s: %s', session.id, e)
    return n
