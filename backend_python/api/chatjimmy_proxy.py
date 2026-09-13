"""Proxy for chatjimmy.ai backend (free Llama chat, no login, no key).

Anonymous JSON POST to ``/api/chat`` with
``{messages:[{role,content}...], chatOptions:{selectedModel, topK}}``.
The response is plain text (optionally followed by ``<|stats|>`` /
``<|think|>`` blocks, which are stripped). History is passed through as
the messages array.
"""
import json
import logging
import random
import re
from typing import Dict, Generator, List

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

CHAT_URL = "https://chatjimmy.ai/api/chat"
REQUEST_TIMEOUT = 180

DEFAULT_MODEL = "llama3.1-8B"

MODELS = [
    {"id": DEFAULT_MODEL, "name": "Llama 3.1 8B (ChatJimmy)", "reasoning": False, "vision": False, "web_search": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_STATS_RE = re.compile(r"<\|stats\|>[\s\S]*?<\|\/stats\|>", re.IGNORECASE)
_THINK_RE = re.compile(r"<\|think\|>[\s\S]*?<\|\/think\|>", re.IGNORECASE)


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
                "web_search": m.get("web_search", False),
            },
        }
        for m in MODELS
    ]


def _clean(text: str) -> str:
    text = _STATS_RE.sub("", text)
    text = _THINK_RE.sub("", text)
    return text.strip()


def _fake_ip() -> str:
    return f"24.{random.randint(0, 9)}.{random.randint(0, 254)}.{random.randint(1, 254)}"


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
        yield {"type": "error", "error": "chatjimmy: no user content to send"}
        return
    session = CurlSession(impersonate="chrome")
    try:
        resp = session.post(
            CHAT_URL,
            json={"messages": convo,
                  "chatOptions": {"selectedModel": model, "topK": 8}},
            headers={"Content-Type": "application/json", "Accept": "*/*",
                     "Origin": "https://chatjimmy.ai",
                     "Referer": "https://chatjimmy.ai/",
                     "X-Real-IP": _fake_ip()},
            timeout=REQUEST_TIMEOUT,
        )
    except Exception as exc:
        yield {"type": "error", "error": f"chatjimmy: cannot reach upstream ({exc})"}
        return
    if resp.status_code != 200:
        yield {"type": "error", "error": f"chatjimmy HTTP {resp.status_code}: {resp.text[:200]}"}
        return
    text = _clean(resp.text)
    if not text:
        yield {"type": "error", "error": "chatjimmy: stream ended without content"}
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
