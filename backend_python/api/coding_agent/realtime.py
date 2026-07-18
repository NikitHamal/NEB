"""Realtime broadcast helpers specific to the coding agent.

We push status / tool / log updates into two channels:
  · `agent.<session_id>` — every participant connected to the session detail
    page (admin users only for now) gets tool events, status flips, message
    additions.
  · `agent.user.<owner_user_id>` — admin inbox / overview pages get
    status:created / status:finished / status:pr_opened to keep the
    project list in sync.

We piggyback on the same ChannelLayer + Redis as the rest of the site
(see api.realtime and api.consumers_ws).
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

try:
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
except ImportError:
    def async_to_sync(fn, *args, **kwargs):  # type: ignore
        return None
    def get_channel_layer():
        return None

from api.utils import now_ms

logger = logging.getLogger(__name__)

GRP_SESSION_FMT = 'agent.{session_id}'
GRP_USER_FMT = 'agent.user.{user_id}'


def _send(group: str, event: str, data: Dict[str, Any]):
    layer = get_channel_layer()
    if layer is None:
        return
    try:
        async_to_sync(layer.group_send)(
            group,
            {
                'type': 'realtime.event',
                'channel': group,
                'event': event,
                'data': {**data, 'ts': now_ms()},
            },
        )
    except Exception as e:  # noqa: BLE001
        logger.debug('coding agent realtime send failed (group=%s event=%s): %s', group, event, e)


def session_group(session_id: str) -> str:
    return GRP_SESSION_FMT.format(session_id=session_id)


def user_group(user_id: str) -> str:
    return GRP_USER_FMT.format(user_id=user_id)


def announce_message(session_id: str, message: Dict[str, Any]) -> None:
    _send(session_group(session_id), 'agent.message_added', message)


def announce_tool_call(session_id: str, call: Dict[str, Any]) -> None:
    _send(session_group(session_id), 'agent.tool_call', call)


def announce_event(session_id: str, event: Dict[str, Any]) -> None:
    _send(session_group(session_id), 'agent.event', event)


def announce_status(session_id: str, status: str, **extras: Any) -> None:
    _send(session_group(session_id), 'agent.status', {'status': status, **extras})
    owner = extras.get('owner_user_id')
    if owner:
        _send(user_group(owner), 'agent.session_status', {'session_id': session_id, 'status': status, **extras})


def announce_file_change(session_id: str, change: Dict[str, Any]) -> None:
    _send(session_group(session_id), 'agent.file_change', change)


def broadcast_session_created(owner_user_id: str, payload: Dict[str, Any]) -> None:
    _send(user_group(owner_user_id), 'agent.session_created', payload)


def broadcast_pr_opened(owner_user_id: str, payload: Dict[str, Any]) -> None:
    _send(user_group(owner_user_id), 'agent.pr_opened', payload)
