"""Proxy for chat.motiftech.io guest chat (Motif 102B / 12.7B / Tiny).

Guest mode needs no login, no cookies and no API key: a plain JSON POST to
``/api/v1/enterprise/chat`` returns an SSE stream. The backend tracks
conversation context server-side via ``conversation_id`` (returned in the
``shared.data.conversation_id`` event).
"""
import json
import logging
from typing import Dict, Generator, List, Optional

from .proxy_http import new_session, resilient_post
from .model_catalog import model_catalog

logger = logging.getLogger(__name__)

MOTIF_URL = "https://chat.motiftech.io"
CHAT_ENDPOINT = f"{MOTIF_URL}/api/v1/enterprise/chat"
REQUEST_TIMEOUT = 300

MODELS = [
    {"id": "motif-102b", "name": "Motif 3 (102B)", "reasoning": True, "vision": False, "web_search": False},
    {"id": "motif-12-7b-reasoning", "name": "Motif 12.7B Reasoning", "reasoning": True, "vision": False, "web_search": False},
    {"id": "motif-12-7b", "name": "Motif 12.7B", "reasoning": True, "vision": False, "web_search": False},
    {"id": "motif-tiny", "name": "Motif Tiny", "reasoning": False, "vision": False, "web_search": False},
]


def get_models() -> List[Dict]:
    return model_catalog(MODELS)


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

_EFFORT_MAP = {
    "low": "small",
    "small": "small",
    "medium": "medium",
    "high": "high",
}


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "motif-102b",
    conversation_id: Optional[str] = None,
    reasoning_effort: str = "high",
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    effort = _EFFORT_MAP.get((reasoning_effort or "high").lower(), "high")
    last_user = next(
        (m.get("content", "") for m in reversed(messages) if m.get("role") == "user"),
        "",
    )
    if not last_user:
        yield {"type": "error", "error": "no user message to send"}
        return
    if conversation_id is None:
        prior = [
            m for m in (messages or [])
            if isinstance(m, dict) and (m.get("content") or "").strip()
            and (m.get("role") or "").lower() in ("user", "assistant", "system")
        ]
        prior = prior[:-1] if prior and (prior[-1].get("role") or "").lower() == "user" else prior
        if prior:
            transcript = "\n\n".join(
                f"{m.get('role', 'user').capitalize()}: {m['content'].strip()}" for m in prior
            )
            last_user = f"Previous conversation:\n{transcript}\n\nCurrent message: {last_user}"

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
        "reasoning_effort": effort,
        "model": model,
    }

    session = new_session(impersonate="chrome", headers=_BROWSER_HEADERS)
    conv_id = conversation_id
    saw_text = False
    err_msg = ""
    try:
        try:
            resp, session = resilient_post(session, CHAT_ENDPOINT, json=payload, stream=True, timeout=REQUEST_TIMEOUT)
        except Exception as exc:
            resp = None
            err_msg = f"Motif request failed: {exc}"
        if resp is not None and resp.status_code != 200:
            err_msg = f"Motif HTTP {resp.status_code}: {resp.text[:300]}"
        elif resp is not None:
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
                            err_msg = str(edata or ev)[:300]
                            break
            except Exception as exc:
                if saw_text:
                    logger.warning("Motif stream ended after content: %s", exc)
                    yield {"type": "done", "finish_reason": "stop", "conversation_id": conv_id}
                    return
                err_msg = f"stream failed: {exc}"

        if saw_text:
            yield {"type": "done", "finish_reason": "stop", "conversation_id": conv_id}
            return

        from .keyless_fallback import stream_keyless_fallback
        fell_back = False
        for ch in stream_keyless_fallback("motiftech", model, messages, reasoning=(effort == "high")):
            fell_back = True
            yield ch
        if not fell_back:
            yield {"type": "error", "error": err_msg or "stream ended without content"}
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
            logger.error("Motif simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None
