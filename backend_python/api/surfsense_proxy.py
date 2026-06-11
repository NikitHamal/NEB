"""
SurfSense anon-chat proxy for the NEBians app ("Neby AI" tab).

Reverse-engineered from https://www.surfsense.com/free/gpt-5.4-mini-no-login

The site is a Next.js app using a REST API at https://api.surfsense.com/api/v1/public/anon-chat/

API Details:
  - Models: GET /models
  - Model info: GET /models/{slug}
  - Chat stream: POST /stream (SSE)
  - Quota: GET /quota
  - Upload: POST /upload (FormData)
  - Document: GET /document

Auth: No login required. Session cookies via credentials: "include".
  Turnstile captcha may be required after quota exhaustion.

Chat stream request body:
  {
    "model_slug": "gpt-5.4-mini-no-login",
    "messages": [{"role": "user", "content": "..."}],
    "disabled_tools": ["web_search"],  // optional
    "turnstile_token": "..."           // optional
  }

SSE event types:
  start, start-step, text-start, text-delta, text-end,
  data-thinking-step, data-anon-quota, data-token-usage,
  tool-input-start, tool-input-delta, tool-input-available,
  tool-output-available, finish-step, finish, error

Models (free, no login):
  gpt-5.4-mini-no-login  (GPT 5.4 Mini, Azure OpenAI)
  gpt-o4-mini-no-login    (GPT O4 Mini, Azure OpenAI, reasoning)
"""

import json
import logging
from typing import Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

API_BASE = "https://api.surfsense.com/api/v1/public/anon-chat"
REQUEST_TIMEOUT = 180

MODELS = [
    {"id": "gpt-5.4-mini-no-login", "name": "GPT 5.4 Mini", "vision": False, "reasoning": False, "web_search": True},
    {"id": "gpt-o4-mini-no-login", "name": "GPT O4 Mini", "vision": False, "reasoning": True, "web_search": True},
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
                "thinking": m.get("reasoning", False),
                "tools": m.get("web_search", False),
            },
        }
        for m in MODELS
    ]


def _parse_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    result = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            content = "\n".join(text_parts)
        if role == "system":
            role = "user"
        if content:
            result.append({"role": role, "content": content})
    return result


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "gpt-5.4-mini-no-login",
    web_search: bool = True,
) -> Generator[Dict, None, None]:
    """Stream chat completion from surfsense.com anon-chat API.

    Yields dicts with keys:
      - {"type": "text", "content": "..."} for normal content
      - {"type": "thinking", "content": "..."} for reasoning content
      - {"type": "tool_call", "id": "...", "name": "...", "arguments": {...}}
      - {"type": "tool_result", "id": "...", "output": {...}}
      - {"type": "done", "finish_reason": "stop"} on completion
      - {"type": "error", "error": "..."} on error
    """
    parsed_messages = _parse_messages(messages)
    if not parsed_messages:
        yield {"type": "error", "error": "No messages to send"}
        return

    payload = {
        "model_slug": model,
        "messages": parsed_messages,
    }
    if not web_search:
        payload["disabled_tools"] = ["web_search"]

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "User-Agent": USER_AGENT,
        "Origin": "https://www.surfsense.com",
        "Referer": "https://www.surfsense.com/",
    }

    try:
        resp = requests.post(
            f"{API_BASE}/stream",
            json=payload,
            headers=headers,
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        logger.error("surfsense: request failed: %s", exc)
        yield {"type": "error", "error": str(exc)}
        return

    if resp.status_code == 404:
        body = resp.text[:500]
        yield {"type": "error", "error": f"Model not found (404): {body}"}
        return

    if resp.status_code == 403:
        body = resp.text[:500]
        try:
            err_data = json.loads(body)
            code = err_data.get("detail", {}).get("code") or err_data.get("error", {}).get("code", "")
            if code in ("CAPTCHA_REQUIRED", "CAPTCHA_INVALID"):
                yield {"type": "error", "error": f"captcha_required ({code})"}
                return
        except (json.JSONDecodeError, ValueError):
            pass
        yield {"type": "error", "error": f"Forbidden (403): {body}"}
        return

    if resp.status_code == 429:
        body = resp.text[:500]
        yield {"type": "error", "error": f"Rate limited (429): {body}"}
        return

    if resp.status_code != 200:
        body = resp.text[:500]
        logger.error("surfsense: HTTP %s: %s", resp.status_code, body)
        yield {"type": "error", "error": f"HTTP {resp.status_code}: {body}"}
        return

    current_tool_call_id = None
    current_tool_name = None

    for raw_line in resp.iter_lines(decode_unicode=True):
        if raw_line is None:
            continue
        line = raw_line.strip()
        if not line:
            continue

        if not line.startswith("data:"):
            continue

        data_str = line[5:].strip()
        if data_str == "[DONE]":
            break

        try:
            event = json.loads(data_str)
        except (json.JSONDecodeError, ValueError):
            continue

        event_type = event.get("type", "")

        if event_type == "text-delta":
            delta = event.get("delta", "")
            if delta:
                yield {"type": "text", "content": delta}

        elif event_type == "reasoning-delta":
            delta = event.get("delta", "")
            if delta:
                yield {"type": "thinking", "content": delta}

        elif event_type == "tool-input-start":
            current_tool_call_id = event.get("toolCallId")
            current_tool_name = event.get("toolName", "")

        elif event_type == "tool-input-available":
            tool_input = event.get("input", {})
            if isinstance(tool_input, str):
                try:
                    tool_input = json.loads(tool_input)
                except (json.JSONDecodeError, ValueError):
                    tool_input = {}
            if current_tool_call_id and current_tool_name:
                yield {
                    "type": "tool_call",
                    "id": current_tool_call_id,
                    "name": current_tool_name,
                    "arguments": tool_input if isinstance(tool_input, dict) else {},
                }

        elif event_type == "tool-output-available":
            output = event.get("output", {})
            if current_tool_call_id:
                yield {
                    "type": "tool_result",
                    "id": current_tool_call_id,
                    "output": output,
                }
            current_tool_call_id = None
            current_tool_name = None

        elif event_type == "data-token-usage":
            pass

        elif event_type == "data-anon-quota":
            pass

        elif event_type == "error":
            yield {"type": "error", "error": event.get("errorText", "unknown error")}
            return

        elif event_type == "finish":
            break

    yield {"type": "done", "finish_reason": "stop"}


def simple_chat(
    user_message: str,
    model: str = "gpt-5.4-mini-no-login",
    system_prompt: str = "",
    web_search: bool = True,
) -> Optional[str]:
    """Non-streaming convenience wrapper: send one message, return full text."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    collected = []
    for chunk in stream_chat(messages=messages, model=model, web_search=web_search):
        t = chunk.get("type")
        if t == "text":
            collected.append(chunk.get("content", ""))
        elif t == "error":
            return None
    return "".join(collected)