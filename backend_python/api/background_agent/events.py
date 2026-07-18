"""Database-backed event stream helpers."""
from __future__ import annotations

import json

from api.models import BackgroundAgentEvent, BackgroundAgentMessage
from api.utils import now_ms, uuid_str


def _bounded_json(value, max_chars=60000):
    encoded = json.dumps(value or {}, ensure_ascii=False)
    if len(encoded) <= max_chars:
        return encoded
    return json.dumps({
        'truncated': True,
        'preview': encoded[:max_chars],
        'originalCharacters': len(encoded),
    }, ensure_ascii=False)


def emit(session, event_type: str, message: str = '', payload: dict | None = None):
    event = BackgroundAgentEvent.objects.create(
        session=session,
        event_type=event_type[:64],
        message=message,
        payload=_bounded_json(payload),
        created_at=now_ms(),
    )
    return event


def add_message(session, role: str, content: str, metadata: dict | None = None):
    latest = session.messages.order_by('-created_at').values_list('created_at', flat=True).first() or 0
    created_at = max(now_ms(), latest + 1)
    row = BackgroundAgentMessage.objects.create(
        id=uuid_str(),
        session=session,
        role=role,
        content=content,
        metadata=json.dumps(metadata or {}, ensure_ascii=False),
        created_at=created_at,
    )
    emit(session, 'message.created', payload={'messageId': row.id, 'role': role})
    return row
