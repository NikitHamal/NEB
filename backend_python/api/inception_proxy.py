"""Proxy for chat.inceptionlabs.ai (Inception Mercury 2 diffusion LLM)."""
import json
import logging
import threading
import time
import uuid
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

INCEPTION_URL = "https://chat.inceptionlabs.ai"
SESSION_URL = f"{INCEPTION_URL}/api/session"
CHAT_URL = f"{INCEPTION_URL}/api/chat"
REQUEST_TIMEOUT = 180

MODELS = [
    {"id": "mercury-2", "name": "Mercury 2", "reasoning": True, "reasoning_levels": ["low", "medium", "high"], "web_search": True},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_BROWSER_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": INCEPTION_URL,
    "referer": f"{INCEPTION_URL}/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

_SESSION_TOKEN: Optional[str] = None
_SESSION_EXPIRES: float = 0
_SESSION_LOCK = threading.Lock()


def _make_id() -> str:
    return uuid.uuid4().hex[:16]


def _ensure_session() -> str:
    global _SESSION_TOKEN, _SESSION_EXPIRES

    now = time.time()
    if _SESSION_TOKEN and _SESSION_EXPIRES > now + 60:
        return _SESSION_TOKEN

    with _SESSION_LOCK:
        now = time.time()
        if _SESSION_TOKEN and _SESSION_EXPIRES > now + 60:
            return _SESSION_TOKEN

        with CurlSession(headers=_BROWSER_HEADERS, impersonate="chrome") as session:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    resp = session.get(SESSION_URL, timeout=15)
                except Exception as exc:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise RuntimeError(f"Inception session failed: {exc}")

                if resp.status_code == 429 and attempt < max_retries - 1:
                    retry_after = int(resp.headers.get("retry-after", 2 ** attempt))
                    logger.warning("Inception rate-limited (429), retrying in %ds", retry_after)
                    time.sleep(retry_after)
                    continue

                if resp.status_code != 200:
                    raise RuntimeError(f"Inception session failed: HTTP {resp.status_code}")

                data = resp.json()
                token = data.get("token", "")
                if not token:
                    raise RuntimeError(f"Inception session returned no token: {data}")
                _SESSION_TOKEN = token
                _SESSION_EXPIRES = now + 3600
                logger.info("Inception: new session token obtained")
                return token

        raise RuntimeError("Inception session failed: exhausted retries")


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": False,
                "thinking": m.get("reasoning", False),
                "reasoning_levels": m.get("reasoning_levels", []),
                "tools": False,
                "web_search": m.get("web_search", False),
            },
        }
        for m in MODELS
    ]


def _messages_to_inception(messages: List[Dict[str, str]]) -> list:
    result = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, list):
            parts = [{"type": b.get("type", "text"), "text": b.get(b.get("type", "text"), b.get("text", ""))} for b in content]
        else:
            parts = [{"type": "text", "text": str(content)}]
        result.append({"parts": parts, "id": _make_id(), "role": role})
    return result


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "mercury-2",
    reasoning_effort: str = "high",
    web_search: bool = False,
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    try:
        token = _ensure_session()
    except RuntimeError as e:
        yield {"type": "error", "error": str(e)}
        return

    inception_msgs = _messages_to_inception(messages)

    payload = {
        "reasoningEffort": reasoning_effort,
        "webSearchEnabled": web_search,
        "voiceMode": False,
        "timezone": "UTC",
        "id": _make_id(),
        "messages": inception_msgs,
        "trigger": "submit-message",
    }

    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"

    try:
        session = CurlSession(headers=headers, impersonate="chrome")
        resp = session.post(
            CHAT_URL,
            json=payload,
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
    except Exception as exc:
        yield {"type": "error", "error": f"request failed: {exc}"}
        return

    if resp.status_code == 403:
        with _SESSION_LOCK:
            global _SESSION_TOKEN
            _SESSION_TOKEN = None
        yield {"type": "error", "error": "Session expired (403). Retrying will refresh."}
        return

    if resp.status_code != 200:
        body = resp.text[:300]
        yield {"type": "error", "error": f"Inception HTTP {resp.status_code}: {body}"}
        return

    buffer = ""
    for chunk_bytes in resp.iter_content():
        if chunk_bytes is None:
            continue
        buffer += chunk_bytes.decode("utf-8", errors="ignore")
        while "\n\n" in buffer:
            event_str, buffer = buffer.split("\n\n", 1)
            event_str = event_str.strip()
            if not event_str:
                continue
            if event_str == "data: [DONE]":
                yield {"type": "done", "finish_reason": "stop"}
                return
            if not event_str.startswith("data: "):
                continue
            try:
                data = json.loads(event_str[6:])
            except (json.JSONDecodeError, ValueError):
                continue
            etype = data.get("type", "")
            if etype == "text-delta":
                delta = data.get("delta", "")
                if delta:
                    yield {"type": "text", "content": delta}

    yield {"type": "done", "finish_reason": "stop"}


def simple_chat(
    user_message: str,
    model: str = "mercury-2",
    system_prompt: str = "",
    reasoning_effort: str = "high",
    **kwargs,
) -> Optional[str]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    collected = []
    for chunk in stream_chat(messages=messages, model=model, reasoning_effort=reasoning_effort):
        t = chunk.get("type")
        if t == "text":
            collected.append(chunk.get("content", ""))
        elif t == "error":
            logger.error("Inception simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None
