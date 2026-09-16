"""Proxy for ptero.pro free chat (WordPress REST, guest token, no login, no key).

``POST /wp-json/mlp/v1/chat`` takes ``{message, model, history, lang,
mode}`` with a self-minted ``X-MLP-Guest-Token`` header and returns
``{reply, model_used, ...}``. Quota (30 req/min, 500k tokens/hr) is keyed
on the guest token, so every call mints a fresh random token and retries
once with a new identity on 429. History entries use ``{role, text}``.
"""
import json
import logging
import uuid
from typing import Dict, Generator, List

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

CHAT_URL = "https://ptero.pro/wp-json/mlp/v1/chat"
STATUS_URL = "https://ptero.pro/wp-json/mlp/v1/status"
REQUEST_TIMEOUT = 180

DEFAULT_MODEL = "mercury-2.5:free"

MODELS = [
    {"id": "mercury-2.5:free", "name": "Mercury 2.5 (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "qwen3.7-flash:free", "name": "Qwen 3.7 Flash (Ptero, free)", "reasoning": False, "vision": True},
    {"id": "deepseek-v4.1-flash:free", "name": "DeepSeek V4.1 Flash (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "deepseek-v4-flash-0731:free", "name": "DeepSeek V4 Flash (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "gpt-oss-20b:free", "name": "GPT-OSS 20B (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "gpt-5-nano:free", "name": "GPT-5 Nano (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "mercury-2:free", "name": "Mercury 2 (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "qwen3.6-35b-a3b:free", "name": "Qwen 3.6 35B (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "qwen2.5-1.5b:local", "name": "Qwen 2.5 1.5B (Ptero local, free)", "reasoning": False, "vision": False},
    {"id": "agnes-2.5-flash:free", "name": "Agnes 2.5 Flash (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "nemotron-3.5-lightning:free", "name": "Nemotron 3.5 Lightning (Ptero, free)", "reasoning": False, "vision": False},
    {"id": "nova-micro:free", "name": "Nova Micro (Ptero, free)", "reasoning": False, "vision": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}


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


def _split_history(messages: List[Dict], system_prompt: str = ""):
    """Split caller messages into ptero (history, message) payload parts."""
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
    session = CurlSession(impersonate="chrome")
    last_status = 0
    last_body = ""
    for _ in range(2):
        try:
            resp = session.post(
                CHAT_URL,
                json={
                    "message": message,
                    "model": model,
                    "history": history,
                    "attachments": [],
                    "lang": "en",
                    "mode": "full",
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Origin": "https://ptero.pro",
                    "Referer": "https://ptero.pro/",
                    "X-MLP-Guest-Token": _fresh_guest_token(),
                    "X-MLP-Guest-Username": "nebian",
                },
                timeout=REQUEST_TIMEOUT,
            )
        except Exception as exc:
            return None, 0, f"ptero: cannot reach upstream ({exc})"
        last_status = resp.status_code
        last_body = resp.text or ""
        if resp.status_code == 429:
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
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return
    history, message, err = _split_history(messages, system_prompt)
    if err:
        yield {"type": "error", "error": err}
        return
    data, _, err = _post(history, message, model)
    if err:
        yield {"type": "error", "error": err}
        return
    text = (data.get("reply") or "").strip()
    if not text:
        detail = ""
        if isinstance(data.get("error"), dict):
            detail = str(data["error"].get("message") or "")[:200]
        elif data.get("code"):
            detail = str(data.get("message") or data.get("code"))[:200]
        yield {"type": "error", "error": f"ptero: empty reply{(' — ' + detail) if detail else ''}"}
        return
    yield {"type": "text", "content": text}
    yield {"type": "done", "finish_reason": "stop"}


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
