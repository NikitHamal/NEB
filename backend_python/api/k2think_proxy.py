"""Proxy for chat.ifm.ai/guest (MBZUAI K2 Horizon 375B reasoning model).

Guest mode needs no login, no cookies and no anti-bot tokens: a plain OpenAI-
style POST to ``/api/guest/chat/completions`` returns an SSE stream. The
reasoning model emits cumulative content events wrapped in
``<details type="reasoning">`` tags (reasoning lines are ``> ``-quoted);
the final answer follows the closing tag. The backend ends the stream cleanly
with a ``{"done": true}`` event (plus an OpenAI-style ``finish_reason: stop``
chunk); a ragged teardown after content is still treated as a normal end.

The old www.k2think.ai endpoint now returns HTTP 400, and its model id
``MBZUAI-IFM/K2-Think-v2`` is kept only as a deprecated alias that maps to
the Horizon model so stored sessions keep working.

Multi-turn history is repaired automatically: the backend rejects assistant
messages without a thinking field (``think``/``reasoning``/``reasoning_content``/
``think_fast``/``think_faster``), so an empty ``reasoning`` key is injected
into stored assistant turns that lack one.
"""
import json
import logging
import re
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

K2THINK_URL = "https://chat.ifm.ai"
CHAT_ENDPOINT = f"{K2THINK_URL}/api/guest/chat/completions"
REQUEST_TIMEOUT = 300

DEFAULT_MODEL = "IFM/K2-Horizon-375B-A23B"
DEPRECATED_MODEL = "MBZUAI-IFM/K2-Think-v2"

MODELS = [
    {"id": DEFAULT_MODEL, "name": "K2 Horizon 375B", "reasoning": True, "vision": False, "web_search": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}
MODEL_MAP[DEPRECATED_MODEL] = MODEL_MAP[DEFAULT_MODEL]


def _resolve_model(model: str) -> str:
    if model == DEPRECATED_MODEL:
        logger.warning("K2Think: deprecated model id %r mapped to %r", model, DEFAULT_MODEL)
        return DEFAULT_MODEL
    return model

_BROWSER_HEADERS = {
    "accept": "text/event-stream, application/json",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": K2THINK_URL,
    "referer": f"{K2THINK_URL}/guest",
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


def _strip_markup(delta: str) -> str:
    delta = re.sub(r"<details\b[^>]*>", "", delta)
    delta = re.sub(r"<summary\b[^>]*>.*?</summary>", "", delta, flags=re.DOTALL)
    delta = delta.replace("</details>", "")
    lines = [(ln[2:] if ln.startswith("> ") else ln) for ln in delta.split("\n")]
    return "\n".join(lines).strip()


def _parse_content(content: str):
    idx = content.rfind("</details>")
    if idx == -1:
        return _strip_markup(content), ""
    reasoning = _strip_markup(content[:idx])
    return reasoning, content[idx + len("</details>"):].lstrip("\n")


EFFORT_LEVELS = ("low", "medium", "high")

THINKING_KEYS = ("think", "reasoning", "reasoning_content", "think_fast", "think_faster")


def _repair_history(messages: List[Dict]) -> List[Dict]:
    repaired = []
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        if (m.get("role") == "assistant"
                and not any(k in m for k in THINKING_KEYS)):
            m = dict(m)
            m["reasoning"] = ""
        repaired.append(m)
    return repaired


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = DEFAULT_MODEL,
    reasoning_effort: str = "medium",
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return
    model = _resolve_model(model)
    if reasoning_effort not in EFFORT_LEVELS:
        reasoning_effort = "medium"

    payload = {
        "stream": True,
        "model": model,
        "messages": _repair_history(messages),
        "params": {},
        "features": {"web_search": False},
        "extra_body": {"chat_template_kwargs": {"reasoning_effort": reasoning_effort}},
    }

    session = CurlSession(headers=_BROWSER_HEADERS, impersonate="chrome")
    try:
        resp = session.post(CHAT_ENDPOINT, json=payload, stream=True, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            body = resp.text[:300]
            yield {"type": "error", "error": f"K2Think HTTP {resp.status_code}: {body}"}
            return

        prev_reasoning = ""
        prev_answer = ""
        saw_any = False
        stream_done = False
        buffer = ""
        try:
            for chunk_bytes in resp.iter_content():
                if stream_done:
                    break
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
                    if "task_id" in ev:
                        continue
                    if isinstance(ev.get("detail"), str) and "content" not in ev:
                        yield {"type": "error", "error": f"K2Think: {ev['detail'][:300]}"}
                        return
                    if ev.get("done") is True:
                        if "content" in ev:
                            reasoning, answer = _parse_content(ev.get("content") or "")
                            if answer.startswith(prev_answer):
                                a_delta = answer[len(prev_answer):]
                            else:
                                a_delta = answer
                            if a_delta.strip():
                                yield {"type": "text", "content": a_delta}
                                saw_any = True
                        stream_done = True
                        break
                    if "choices" in ev:
                        continue
                    if "content" in ev:
                        saw_any = True
                        reasoning, answer = _parse_content(ev.get("content") or "")
                        if reasoning.startswith(prev_reasoning):
                            r_delta = reasoning[len(prev_reasoning):]
                        else:
                            r_delta = ""
                        prev_reasoning = reasoning
                        if r_delta.strip():
                            yield {"type": "thought", "content": r_delta}
                        if answer.startswith(prev_answer):
                            a_delta = answer[len(prev_answer):]
                        else:
                            a_delta = answer
                        prev_answer = answer
                        if a_delta.strip():
                            yield {"type": "text", "content": a_delta}
        except Exception as exc:
            # The upstream closes the stream uncleanly after the final event.
            if saw_any:
                logger.warning("K2Think stream ended after content: %s", exc)
                yield {"type": "done", "finish_reason": "stop"}
                return
            yield {"type": "error", "error": f"stream failed: {exc}"}
            return

        if not saw_any:
            yield {"type": "error", "error": "stream ended without content"}
            return
        yield {"type": "done", "finish_reason": "stop"}
    finally:
        try:
            session.close()
        except Exception:
            pass


def simple_chat(
    user_message: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
    max_tokens: int = 500,
    reasoning_effort: str = "medium",
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
            logger.error("K2Think simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None
