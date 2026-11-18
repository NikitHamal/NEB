"""Proxy for ptero.pro free chat (WordPress REST, guest token + WP nonce, no login).

``GET https://ptero.pro/`` warms the session cookie jar and extracts the active
``X-WP-Nonce`` token; ``POST /wp-json/mlp/v1/chat`` takes ``{message, model,
history, lang, mode}`` with a self-minted ``X-MLP-Guest-Token`` header and
returns ``{reply, model_used, ...}``.
"""
import json
import logging
import re
import threading
import time
import uuid
from typing import Dict, Generator, List, Optional, Tuple

from .proxy_http import new_session, resilient_get, resilient_post

logger = logging.getLogger(__name__)

SITE_URL = "https://ptero.pro/"
CHAT_URL = "https://ptero.pro/wp-json/mlp/v1/chat"
STATUS_URL = "https://ptero.pro/wp-json/mlp/v1/status"
REQUEST_TIMEOUT = 180

DEFAULT_MODEL = "deepseek-v4-flash:runware"

MODELS = [
    {"id": "deepseek-v4-flash:runware", "name": "DeepSeek V4 Flash (Ptero, free)", "reasoning": False, "vision": True},
    {"id": "minimax-m3.1-flash:runware", "name": "MiniMax M3.1 Flash (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "qwen3.7-flash:minirouter", "name": "Qwen 3.7 Flash (Ptero, free)", "reasoning": False, "vision": True},
    {"id": "glm-5.3-flash", "name": "GLM 5.3 Flash (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "kimi-k3:apinex", "name": "Kimi K3 (Ptero, free)", "reasoning": False, "vision": False},
]

LEGACY_MODELS = {
    "mercury-2.5:free": "deepseek-v4-flash:runware",
    "mercury-2:free": "deepseek-v4-flash:runware",
    "qwen3.7-flash:free": "qwen3.7-flash:minirouter",
    "qwen3.6-35b-a3b:free": "qwen3.7-flash:minirouter",
    "qwen2.5-1.5b:local": "qwen3.7-flash:minirouter",
    "deepseek-v4.1-flash:free": "deepseek-v4-flash:runware",
    "deepseek-v4-flash-0731:free": "deepseek-v4-flash:runware",
    "gpt-oss-20b:free": "deepseek-v4-flash:runware",
    "gpt-5-nano:free": "minimax-m3.1-flash:runware",
    "agnes-2.5-flash:free": "glm-5.3-flash",
    "nemotron-3.5-lightning:free": "glm-5.3-flash",
    "nova-micro:free": "minimax-m3.1-flash:runware",
}

MODEL_MAP = {m["id"]: m for m in MODELS}
_NONCE_LOCK = threading.Lock()
_CACHED_NONCE: str = ""
_CACHED_AT: float = 0.0


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": False,
                "vision": m.get("vision", False),
                "thinking": m.get("reasoning", False),
                "tools": False,
                "web_search": False,
            },
        }
        for m in MODELS
    ]


def _fresh_guest_token() -> str:
    return uuid.uuid4().hex


def _warm_nonce(session, force: bool = False) -> Tuple[str, object]:
    global _CACHED_NONCE, _CACHED_AT
    now = time.time()
    if not force and _CACHED_NONCE and (now - _CACHED_AT) < 600:
        return _CACHED_NONCE, session
    with _NONCE_LOCK:
        if not force and _CACHED_NONCE and (time.time() - _CACHED_AT) < 600:
            return _CACHED_NONCE, session
        resp, session = resilient_get(session, SITE_URL, timeout=20)
        html = resp.text or ""
        m = re.search(r'var\s+nonce\s*=\s*["\']([a-f0-9]{10})["\']|data-referral-nonce=["\']([a-f0-9]{10})["\']', html, re.I)
        nonce = (m.group(1) or m.group(2)) if m else ""
        if nonce:
            _CACHED_NONCE = nonce
            _CACHED_AT = time.time()
        return nonce, session


def _split_history(messages: List[Dict], system_prompt: str = ""):
    systems: List[str] = []
    if system_prompt and system_prompt.strip():
        systems.append(system_prompt.strip())
    turns: List[Dict] = []
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        role = (m.get("role") or "").lower()
        content = (m.get("content") or "").strip()
        if not content:
            continue
        if role == "system":
            systems.append(content)
        elif role in ("user", "assistant"):
            turns.append({"role": role, "content": content})
    if not turns or turns[-1]["role"] != "user":
        return None, None, "ptero: no user content to send"
    message = turns[-1]["content"]
    if systems:
        message = "[System instructions: " + "\n".join(systems) + "]\n\n" + message
    history = [{"role": t["role"], "text": t["content"], "attachments": []} for t in turns[:-1]]
    return history, message, ""


def _post(history: List[Dict], message: str, model: str):
    session = new_session(impersonate="chrome")
    last_status = 0
    last_body = ""
    mode = "quick" if len(message) <= 24 else "full"
    for attempt in range(2):
        try:
            nonce, session = _warm_nonce(session, force=(attempt > 0))
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Origin": "https://ptero.pro",
                "Referer": "https://ptero.pro/",
                "X-MLP-Guest-Token": _fresh_guest_token(),
                "X-MLP-Guest-Username": "nebian",
            }
            if nonce:
                headers["X-WP-Nonce"] = nonce
            resp, session = resilient_post(
                session,
                CHAT_URL,
                json={
                    "message": message,
                    "model": model,
                    "history": history,
                    "attachments": [],
                    "lang": "en",
                    "mode": mode,
                },
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
        except Exception as exc:
            return None, 0, f"ptero: cannot reach upstream ({exc})"
        last_status = resp.status_code
        last_body = resp.text or ""
        if resp.status_code in (403, 429):
            continue
        if resp.status_code != 200:
            return None, resp.status_code, f"ptero HTTP {resp.status_code}: {last_body[:200]}"
        try:
            return json.loads(last_body), 200, ""
        except ValueError:
            return None, 200, "ptero: invalid JSON response"
    return None, last_status, f"ptero HTTP {last_status or 429}: rate limited, retry later"


def stream_chat(
    messages: List[Dict],
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
) -> Generator[Dict, None, None]:
    resolved_model = LEGACY_MODELS.get(model, model or DEFAULT_MODEL)
    if resolved_model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return
    history, message, err = _split_history(messages, system_prompt)
    if err:
        yield {"type": "error", "error": err}
        return
    data, _, err = _post(history, message, resolved_model)
    if not err and data:
        text = (data.get("reply") or "").strip()
        if text:
            yield {"type": "text", "content": text}
            yield {"type": "done", "finish_reason": "stop"}
            return
        detail = ""
        if isinstance(data.get("error"), dict):
            detail = str(data["error"].get("message") or "")[:200]
        elif data.get("code"):
            detail = str(data.get("message") or data.get("code"))[:200]
        err = f"ptero: empty reply{(' — ' + detail) if detail else ''}"

    yield {"type": "error", "error": err or "ptero: empty reply"}


def simple_chat(
    user_message: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
    max_tokens: int = 0,
    **_: object,
) -> str:
    texts: List[str] = []
    for chunk in stream_chat(
        [{"role": "user", "content": user_message}], model=model, system_prompt=system_prompt
    ):
        if chunk.get("type") == "text":
            texts.append(chunk.get("content", ""))
        elif chunk.get("type") == "error":
            return f"[Error] {chunk.get('error', 'unknown error')}"
    return "".join(texts)
