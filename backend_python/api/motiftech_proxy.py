"""Proxy for chat.motiftech.io guest chat (Motif 102B / Motif 12.7B).

Guest mode needs no login, no cookies and no API key: a plain JSON POST to
``/api/v1/enterprise/chat`` returns an SSE stream. The backend tracks
conversation context server-side via ``conversation_id`` (returned in the
``shared.data.conversation_id`` event), so for multi-turn arena chats we pass
the previously stored id and persist the new one on completion.

SSE events:
    shared.data.conversation_id -> {"conversation_id": "..."}
    chat.text                   -> answer text delta
    chat.step                   -> {"role": "answer"} marks the answer phase
    shared.data.message         -> server message id
    shared.sign                 -> "[[HUB_STOP_SIGN]]" marks end of stream
"""
import json
import logging
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

MOTIF_URL = "https://chat.motiftech.io"
CHAT_ENDPOINT = f"{MOTIF_URL}/api/v1/enterprise/chat"
REQUEST_TIMEOUT = 300

MODELS = [
    {"id": "motif-102b", "name": "Motif 3", "reasoning": False, "vision": False, "web_search": False},
    {"id": "motif-12-7b", "name": "Motif 12.7B", "reasoning": False, "vision": False, "web_search": False},
    {"id": "motif-12-7b-reasoning", "name": "Motif 12.7B Reasoning", "reasoning": True, "vision": False, "web_search": False},
    {"id": "motif-tiny", "name": "Motif Tiny", "reasoning": False, "vision": False, "web_search": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_BROWSER_HEADERS = {
    "accept": "text/event-stream, application/json",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": MOTIF_URL,
    "referer": f"{MOTIF_URL}/chat",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": m.get("vision", False),
                "thinking": m.get("reasoning", False),
                "tools": False,
                "web_search": m.get("web_search", False),
            },
        }
        for m in MODELS
    ]


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "motif-102b",
    conversation_id: Optional[str] = None,
    reasoning_effort: str = "small",
) -> Generator[Dict, None, None]:
    """Stream a chat turn. Yields dicts: text / done / error.

    ``messages`` replay the arena history; only the last user message is sent
    (the upstream tracks context via ``conversation_id``). The ``done`` chunk
    carries the new ``conversation_id`` for the caller to persist.
    """
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    last_user = next(
        (m.get('content', '') for m in reversed(messages) if m.get('role') == 'user'),
        '',
    )
    if not last_user:
        yield {"type": "error", "error": "no user message to send"}
        return

    payload = {
        "query": last_user,
        "conversation_id": conversation_id,
        "project_id": None,
        "template_id": None,
        "forced_skill_names": [],
        "disabled_skill_names": [],
        "language": "en",
        "timezone": "Asia/Katmandu",
        "mode": "chat",
        "reasoning_effort": reasoning_effort,
        "model": model,
    }

    session = CurlSession(headers=_BROWSER_HEADERS, impersonate="chrome")
    conv_id = conversation_id
    saw_text = False
    try:
        resp = session.post(CHAT_ENDPOINT, json=payload, stream=True, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            body = resp.text[:300]
            yield {"type": "error", "error": f"Motif HTTP {resp.status_code}: {body}"}
            return

        buffer = ""
        try:
            for chunk_bytes in resp.iter_content():
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
                    etype = ev.get("type") or ""
                    edata = ev.get("data")
                    if etype == "chat.text" and isinstance(edata, str) and edata:
                        saw_text = True
                        yield {"type": "text", "content": edata}
                    elif etype == "shared.data.conversation_id" and isinstance(edata, str) and edata:
                        conv_id = edata
                    elif etype == "shared.sign":
                        break
                    elif "error" in etype:
                        yield {"type": "error", "error": str(edata or ev)[:300]}
                        return
        except Exception as exc:
            if saw_text:
                logger.warning("Motif stream ended after content: %s", exc)
                yield {"type": "done", "finish_reason": "stop", "conversation_id": conv_id}
                return
            yield {"type": "error", "error": f"stream failed: {exc}"}
            return

        if not saw_text:
            yield {"type": "error", "error": "stream ended without content"}
            return
        yield {"type": "done", "finish_reason": "stop", "conversation_id": conv_id}
    finally:
        try:
            session.close()
        except Exception:
            pass


def simple_chat(
    user_message: str,
    model: str = "motif-102b",
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
            logger.error("Motif simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None
