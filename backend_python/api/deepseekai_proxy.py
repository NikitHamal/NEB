"""
Deep-Seek AI chat proxy for the NEBians app ("Neby AI" tab).

Reverse-engineered from https://deep-seek.ai/chat (Laravel + OpenRouter proxy).

The site is a Laravel app that proxies requests to OpenRouter:
  - Chat endpoint: POST https://deep-seek.ai/api/chat
  - Auth: CSRF token from <meta name="csrf-token"> + session cookies (XSRF-TOKEN, deepseek_session)
  - Body: JSON {"model": "<model_id>", "messages": [{"role": "...", "content": "..."}]}
  - Response: SSE stream (OpenAI-compatible format)
  - Rate limit: HTTP 429 with {"error": {"limit_exhausted": true, "limit_type": "default"}}
  - Reasoning models: return "reasoning" and "reasoning_details" fields in delta

Models:
  - deepseek/deepseek-v4-flash (DeepSeek-V4 Flash)
  - deepseek/deepseek-r1 (DeepSeek-R1, reasoning)
  - deepseek/deepseek-v3.2 (DeepSeek-V3.2)

Flow:
  1. GET https://deep-seek.ai/chat to obtain CSRF token + session cookies
  2. POST /api/chat with CSRF token header + cookies + JSON body
  3. Parse SSE stream, yield OpenAI-compatible deltas

This module provides a synchronous Python client suitable for Django views.
"""

import json
import logging
import re
from typing import Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

SITE_URL = "https://deep-seek.ai"
CHAT_URL = f"{SITE_URL}/api/chat"
PAGE_URL = f"{SITE_URL}/chat"
REQUEST_TIMEOUT = 180

MODELS = [
    {"id": "deepseek/deepseek-v4-flash", "name": "DeepSeek-V4 Flash", "vision": False, "thinking": False},
    {"id": "deepseek/deepseek-r1", "name": "DeepSeek-R1", "vision": False, "thinking": True},
    {"id": "deepseek/deepseek-v3.2", "name": "DeepSeek-V3.2", "vision": False, "thinking": False},
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": m.get("vision", False),
                "thinking": m.get("thinking", False),
            },
        }
        for m in MODELS
    ]


def _get_session() -> Dict[str, str]:
    """Fetch the chat page to obtain CSRF token and session cookies."""
    resp = requests.get(
        PAGE_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    resp.encoding = "utf-8"
    html = resp.text
    csrf_match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', html)
    csrf = csrf_match.group(1) if csrf_match else ""

    cookies = {}
    for name, value in resp.cookies.items():
        cookies[name] = value

    return {"csrf": csrf, "cookies": cookies}


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "deepseek/deepseek-v4-flash",
) -> Generator[Dict, None, None]:
    """Stream chat completion from deep-seek.ai.

    Yields dicts with keys:
      - {"type": "text", "content": "..."} for normal content
      - {"type": "thinking", "content": "..."} for reasoning content
      - {"type": "done", "finish_reason": "stop"} on completion
      - {"type": "error", "error": "..."} on error
    """
    session = _get_session()
    csrf = session["csrf"]
    cookies = session["cookies"]

    # deep-seek.ai Laravel/OpenRouter proxy rejects role='system' and redirects to aichat.org.
    # We combine any 'system' prompt into the first 'user' message.
    formatted_messages = []
    system_content = ""
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            if system_content:
                system_content += "\n" + content
            else:
                system_content = content
        else:
            formatted_messages.append({"role": role, "content": content})

    if system_content:
        user_msg_idx = -1
        for idx, m in enumerate(formatted_messages):
            if m["role"] == "user":
                user_msg_idx = idx
                break
        if user_msg_idx != -1:
            formatted_messages[user_msg_idx]["content"] = f"[System Instructions]\n{system_content}\n\n{formatted_messages[user_msg_idx]['content']}"
        else:
            formatted_messages.insert(0, {"role": "user", "content": system_content})

    payload = {
        "model": model,
        "messages": formatted_messages,
    }

    headers = {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": csrf,
        "Accept": "text/event-stream",
        "User-Agent": USER_AGENT,
        "Referer": f"{SITE_URL}/chat",
        "Origin": SITE_URL,
    }

    try:
        resp = requests.post(
            CHAT_URL,
            json=payload,
            headers=headers,
            cookies=cookies,
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        logger.error("deepseekai: request failed: %s", exc)
        yield {"type": "error", "error": str(exc)}
        return

    resp.encoding = "utf-8"

    if resp.status_code == 429:
        try:
            err = resp.json()
            err_data = err.get("error", {})
            yield {
                "type": "error",
                "error": err_data.get("error", "daily limit reached"),
                "limit_exhausted": err_data.get("limit_exhausted", True),
            }
        except Exception:
            yield {"type": "error", "error": "rate_limited", "limit_exhausted": True}
        return

    if resp.status_code != 200:
        body = resp.text[:500]
        logger.error("deepseekai: HTTP %s: %s", resp.status_code, body)
        yield {"type": "error", "error": f"HTTP {resp.status_code}: {body}"}
        return

    current_event = ""
    for raw_line in resp.iter_lines(decode_unicode=True):
        if raw_line is None:
            continue
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("event:"):
            current_event = line[6:].strip()
            continue

        if line.startswith(":"):
            continue

        if line.startswith("data:"):
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                return

            if current_event == "error":
                try:
                    err = json.loads(data_str)
                    err_data = err.get("error", {})
                    yield {
                        "type": "error",
                        "error": err_data.get("error", "Unknown error"),
                        "limit_exhausted": err_data.get("limit_exhausted", False),
                        "limit_type": err_data.get("limit_type", "default"),
                    }
                except json.JSONDecodeError:
                    pass
                current_event = ""
                continue

            try:
                chunk = json.loads(data_str)
                choices = chunk.get("choices", [])
                if not choices:
                    continue

                delta = choices[0].get("delta", {})
                content = delta.get("content", "")
                reasoning = delta.get("reasoning", "")
                finish_reason = choices[0].get("finish_reason")

                if content:
                    yield {"type": "text", "content": content}

                if reasoning:
                    yield {"type": "thinking", "content": reasoning}

                if finish_reason == "stop":
                    yield {"type": "done", "finish_reason": "stop"}

            except json.JSONDecodeError:
                continue


def simple_chat(
    user_message: str,
    model: str = "deepseek/deepseek-v4-flash",
    system_prompt: str = "",
) -> Optional[str]:
    """Non-streaming convenience wrapper: send one message, return full text."""
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
            return None
    return "".join(collected)