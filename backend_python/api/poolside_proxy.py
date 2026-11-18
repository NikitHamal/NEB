"""Proxy for chat.poolside.ai/guest (Poolside Laguna S 2.1 / XS 2.1).

Guest chat needs no login, no cookies and no anti-bot tokens. The flow is:

1. POST /api/chats -> creates a chat, returns its id
2. POST /api/chat   -> submits a message, returns 202 + generationId/streamUrl
3. GET  /api/chat/{id}/stream?generationId=... -> typed SSE stream whose
   text-delta events carry the answer.

The chat history lives server-side (keyed by chatId + baseMessageId), so a
stateless request must flatten the full message history into one user message
to preserve context across turns.
"""
import json
import logging
import uuid
from typing import Dict, Generator, List, Optional

from .proxy_http import new_session, resilient_get, resilient_post
from .model_catalog import model_catalog

logger = logging.getLogger(__name__)

BASE_URL = "https://chat.poolside.ai"
CHATS_ENDPOINT = f"{BASE_URL}/api/chats"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat"
REQUEST_TIMEOUT = 300

MODELS = [
    {"id": "laguna-s-2.1", "name": "Laguna S 2.1", "reasoning": False, "vision": False, "web_search": True},
    {"id": "laguna-xs-2.1", "name": "Laguna XS 2.1", "reasoning": False, "vision": False, "web_search": True},
]


def get_models() -> List[Dict]:
    return model_catalog(MODELS)


MODEL_MAP = {m["id"]: m for m in MODELS}

_BROWSER_HEADERS = {
    "accept": "application/json, text/event-stream",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": BASE_URL,
    "referer": f"{BASE_URL}/guest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


def _flatten_history(messages: List[Dict[str, str]]) -> str:
    parts = []
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content")
        if isinstance(content, list):
            content = "\n".join(
                str(item.get("text", "")) for item in content
                if isinstance(item, dict) and item.get("type") == "text"
            )
        if not content:
            continue
        parts.append(f"{role}: {content}")
    return "\n\n".join(parts)


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "laguna-s-2.1",
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    upstream_model = f"poolside/{model}"
    session = new_session(impersonate="chrome", headers=_BROWSER_HEADERS)
    saw_any = False
    finish_reason = "stop"
    err_msg = ""
    try:
        try:
            resp, session = resilient_post(session, CHATS_ENDPOINT, json={
                "title": "neby",
                "model": upstream_model,
                "inferenceMode": "platform",
                "incognito": False,
            }, timeout=30)
            if resp.status_code != 200:
                err_msg = f"Poolside create-chat HTTP {resp.status_code}: {resp.text[:300]}"
            else:
                chat_id = resp.json().get("id")
                if not chat_id:
                    err_msg = f"Poolside create-chat missing id: {resp.text[:300]}"
                else:
                    message_id = str(uuid.uuid4())
                    generation_id = str(uuid.uuid4())
                    payload = {
                        "chatId": chat_id,
                        "model": upstream_model,
                        "inferenceMode": "platform",
                        "options": {"webSearch": True, "slack": False, "slackWrite": False, "thinking": True},
                        "id": chat_id,
                        "trigger": "submit-message",
                        "messageId": message_id,
                        "baseMessageId": None,
                        "message": {
                            "messageId": message_id,
                            "parts": [{"type": "text", "text": _flatten_history(messages)}],
                            "id": message_id,
                            "role": "user",
                        },
                        "generationId": generation_id,
                    }
                    resp, session = resilient_post(
                        session,
                        CHAT_ENDPOINT,
                        json=payload,
                        headers={"x-poolside-stream-protocol": "resumable-v1"},
                        timeout=60,
                    )
                    if resp.status_code != 202:
                        err_msg = f"Poolside send HTTP {resp.status_code}: {resp.text[:300]}"
                    else:
                        stream_url = (resp.json() or {}).get("streamUrl") or ""
                        if not stream_url:
                            err_msg = "Poolside send missing streamUrl"
                        else:
                            stream_resp, session = resilient_get(
                                session,
                                f"{BASE_URL}{stream_url}",
                                headers={"Accept": "text/event-stream"},
                                stream=True,
                                timeout=REQUEST_TIMEOUT,
                            )
                            if stream_resp.status_code != 200:
                                err_msg = f"Poolside stream HTTP {stream_resp.status_code}"
                            else:
                                buffer = ""
                                for chunk_bytes in stream_resp.iter_content():
                                    if chunk_bytes is None:
                                        continue
                                    buffer += chunk_bytes.decode("utf-8", errors="replace")
                                    while "\n" in buffer:
                                        line, buffer = buffer.split("\n", 1)
                                        line = line.strip("\r")
                                        if not line.startswith("data:"):
                                            continue
                                        raw = line[5:].strip()
                                        if not raw:
                                            continue
                                        try:
                                            ev = json.loads(raw)
                                        except (json.JSONDecodeError, ValueError):
                                            continue
                                        ev_type = ev.get("type")
                                        if ev_type == "text-delta":
                                            delta = ev.get("delta")
                                            if delta:
                                                saw_any = True
                                                yield {"type": "text", "content": delta}
                                        elif ev_type == "finish":
                                            finish_reason = ev.get("finishReason") or "stop"
                                        elif ev_type == "error":
                                            err_msg = ev.get("errorText") or ev.get("error") or "Poolside upstream error"
                                            break
        except Exception as exc:
            if saw_any:
                logger.warning("Poolside stream ended after content: %s", exc)
                yield {"type": "done", "finish_reason": finish_reason}
                return
            err_msg = f"stream failed: {exc}"

        if saw_any:
            yield {"type": "done", "finish_reason": finish_reason}
            return

        yield {"type": "error", "error": err_msg or "stream ended without content"}
    finally:
        try:
            session.close()
        except Exception:
            pass


def simple_chat(
    user_message: str,
    model: str = "laguna-s-2.1",
    system_prompt: str = "",
    max_tokens: int = 500,
    **kwargs,
) -> Optional[str]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    collected = []
    for chunk in stream_chat(messages=messages, model=model):
        t = chunk.get("type")
        if t == "text":
            collected.append(chunk.get("content", ""))
        elif t == "error":
            logger.error("Poolside simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None
