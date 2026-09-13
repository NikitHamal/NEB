"""Proxy for getunikey.ai anonymous chat (free trial, no login, no key).

``GET /api/anonymous/chat/status`` (header ``X-Anonymous-Fingerprint``)
reports the trial quota; ``POST /api/anonymous/chat/completions`` takes an
OpenAI-style ``{model, messages}`` body with ``stream:true`` and returns
OpenAI-style SSE deltas.

The trial quota (3 messages) is keyed on the self-reported FingerprintJS
visitor id (+ IP), so every call mints a fresh random fingerprint and gets
a full quota. History is replayed from the caller (stateless).
"""
import json
import logging
import uuid
from typing import Dict, Generator, List

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

STATUS_URL = "https://www.getunikey.ai/api/anonymous/chat/status"
CHAT_URL = "https://www.getunikey.ai/api/anonymous/chat/completions"
REQUEST_TIMEOUT = 180

DEFAULT_MODEL = "gpt-5.5"

MODELS = [
    {"id": "gpt-5.5", "name": "GPT 5.5 (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "google/gemini-3.5-flash", "name": "Gemini 3.5 Flash (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "google/gemini-3.1-pro-preview", "name": "Gemini 3.1 Pro Preview (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "x-ai/grok-4.3", "name": "Grok 4.3 (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "deepseek/deepseek-v4-pro", "name": "DeepSeek V4 Pro (Unikey trial)", "reasoning": True, "vision": False},
    {"id": "deepseek/deepseek-v4-flash", "name": "DeepSeek V4 Flash (Unikey trial)", "reasoning": True, "vision": False},
    {"id": "z-ai/glm-5.2", "name": "GLM 5.2 (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "minimax/minimax-m3", "name": "MiniMax M3 (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "moonshotai/kimi-k2.7-code", "name": "Kimi K2.7 Code (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "moonshotai/kimi-k3", "name": "Kimi K3 (Unikey trial)", "reasoning": False, "vision": False},
    {"id": "claude-opus-4-7", "name": "Claude Opus 4.7 (Unikey trial)", "reasoning": True, "vision": False},
    {"id": "claude-opus-4-8", "name": "Claude Opus 4.8 (Unikey trial)", "reasoning": True, "vision": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}


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
                "web_search": False,
            },
        }
        for m in MODELS
    ]


def _fresh_fingerprint() -> str:
    return "rnd" + uuid.uuid4().hex


def stream_chat(
    messages: List[Dict],
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return
    convo: List[Dict] = []
    if system_prompt:
        convo.append({"role": "system", "content": system_prompt})
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        role = (m.get("role") or "").lower()
        content = (m.get("content") or "").strip()
        if not content or role not in ("user", "assistant", "system"):
            continue
        convo.append({"role": role, "content": content})
    if not any(m["role"] == "user" for m in convo):
        yield {"type": "error", "error": "unikey: no user content to send"}
        return
    session = CurlSession(impersonate="chrome")
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Origin": "https://www.getunikey.ai",
        "Referer": "https://www.getunikey.ai/anonymous-chat",
        "X-Anonymous-Fingerprint": _fresh_fingerprint(),
    }
    try:
        resp = session.post(
            CHAT_URL,
            json={"model": model, "messages": convo, "stream": True},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
    except Exception as exc:
        yield {"type": "error", "error": f"unikey: cannot reach upstream ({exc})"}
        return
    if resp.status_code != 200:
        yield {"type": "error", "error": f"unikey HTTP {resp.status_code}: {resp.text[:200]}"}
        return
    texts: List[str] = []
    for line in resp.text.split("\n"):
        line = line.strip()
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        try:
            payload = json.loads(data)
        except ValueError:
            continue
        err = (payload.get("error") or {}).get("message") if isinstance(payload.get("error"), dict) else None
        if err:
            yield {"type": "error", "error": f"unikey: {err[:200]}"}
            return
        delta = ((payload.get("choices") or [{}])[0].get("delta") or {}).get("content", "")
        if not delta:
            delta = ((payload.get("choices") or [{}])[0].get("message") or {}).get("content", "")
        if delta:
            texts.append(delta)
    text = "".join(texts).strip()
    if not text:
        yield {"type": "error", "error": "unikey: stream ended without content"}
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
