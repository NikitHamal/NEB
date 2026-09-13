"""Proxy for chat9.yqcloud.top (Yqcloud free chat, api.binjie.fun backend).

Anonymous, no login, no key, no anti-bot tokens: a plain JSON POST to
``/api/generateStream`` with ``{prompt, userId, network, system,
withoutContext, stream}`` returns the answer as a raw text stream.
History is sent inside the prompt (flattened transcript); ``userId`` only
needs to be stable-looking (``#/chat/<ms>``).
"""
import json
import logging
import time
from typing import Dict, Generator, List

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://api.binjie.fun/api/generateStream"
PAGE_ORIGIN = "https://chat9.yqcloud.top"
REQUEST_TIMEOUT = 180

DEFAULT_MODEL = "yqcloud-default"

MODELS = [
    {"id": DEFAULT_MODEL, "name": "Yqcloud Chat", "reasoning": False, "vision": False, "web_search": True},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_BROWSER_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": PAGE_ORIGIN,
    "referer": f"{PAGE_ORIGIN}/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
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


def _flatten(messages: List[Dict]) -> str:
    lines = []
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        role = (m.get("role") or "").lower()
        content = (m.get("content") or "").strip()
        if not content or role not in ("user", "assistant"):
            continue
        lines.append(f"{'User' if role == 'user' else 'Assistant'}: {content}" if len(lines) else content)
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0]
    return "\n\n".join(lines)


def _extract_system(messages: List[Dict]) -> str:
    for m in messages or []:
        if isinstance(m, dict) and (m.get("role") or "").lower() == "system" and m.get("content"):
            return str(m["content"])
    return ""


def stream_chat(
    messages: List[Dict],
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return
    prompt = _flatten(messages)
    if not prompt.strip():
        yield {"type": "error", "error": "yqcloud: no user content to send"}
        return
    system_prompt = system_prompt or _extract_system(messages)
    body = {
        "prompt": prompt,
        "userId": f"#/chat/{int(time.time() * 1000)}",
        "network": True,
        "system": system_prompt or "",
        "withoutContext": False,
        "stream": True,
    }
    session = CurlSession(headers=_BROWSER_HEADERS, impersonate="chrome")
    try:
        resp = session.post(API_ENDPOINT, json=body, stream=True, timeout=REQUEST_TIMEOUT)
    except Exception as exc:
        yield {"type": "error", "error": f"yqcloud: cannot reach upstream ({exc})"}
        return
    if resp.status_code != 200:
        yield {"type": "error", "error": f"yqcloud HTTP {resp.status_code}: {resp.text[:200]}"}
        return
    saw_any = False
    try:
        for chunk in resp.iter_content():
            if chunk is None:
                continue
            text = chunk.decode("utf-8", errors="replace")
            if text:
                saw_any = True
                yield {"type": "text", "content": text}
    except Exception as exc:
        if saw_any:
            logger.warning("yqcloud stream ended after content: %s", exc)
        else:
            yield {"type": "error", "error": f"yqcloud stream failed: {exc}"}
            return
    if not saw_any:
        yield {"type": "error", "error": "yqcloud: stream ended without content"}
        return
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
