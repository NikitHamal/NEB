import json
import logging
import time
from typing import Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

API_BASE = "https://g4f.space/v1"
REQUEST_TIMEOUT = 180
RATE_LIMIT_SLEEP = 61
DEFAULT_MODEL = "openai"

MODELS = [
    {"id": "openai", "name": "GPT-5.4 Nano (Fast)", "server": "mkoloq41e34074b6133e"},
    {"id": "openai-fast", "name": "GPT Fast", "server": "mkoloq41e34074b6133e"},
    {"id": "deepseek", "name": "DeepSeek", "server": "mkoloq41e34074b6133e"},
    {"id": "gpt-5.4", "name": "GPT-5.4", "server": "mkoloq41e34074b6133e"},
    {"id": "gpt-5.4-nano", "name": "GPT-5.4 Nano", "server": "mkoloq41e34074b6133e"},
    {"id": "gpt-5.4-reasoning", "name": "GPT-5.4 Reasoning", "server": "mkoloq41e34074b6133e"},
    {"id": "gpt-5.2", "name": "GPT-5.2", "server": "mkoloq41e34074b6133e"},
    {"id": "gpt-5.5", "name": "GPT-5.5", "server": "mkoloq41e34074b6133e"},
    {"id": "grok", "name": "Grok", "server": "mkoloq41e34074b6133e"},
    {"id": "grok-4", "name": "Grok 4", "server": "mkoloq41e34074b6133e"},
    {"id": "grok-4-fast", "name": "Grok 4 Fast", "server": "mkoloq41e34074b6133e"},
    {"id": "claude", "name": "Claude", "server": "mkoloq41e34074b6133e"},
    {"id": "kimi", "name": "Kimi", "server": "mkoloq41e34074b6133e"},
    {"id": "mistral", "name": "Mistral", "server": "mkoloq41e34074b6133e"},
    {"id": "qwen3-coder", "name": "Qwen 3 Coder", "server": "mkoloq41e34074b6133e"},
    {"id": "perplexity-fast", "name": "Perplexity Fast", "server": "mkoloq41e34074b6133e"},
    {"id": "perplexity-reasoning", "name": "Perplexity Reasoning", "server": "mkoloq41e34074b6133e"},
    {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash", "server": "mkol5tgcd33cc358ddbc"},
    {"id": "gemini-3.1-flash-lite", "name": "Gemini 3.1 Flash Lite", "server": "mkol5tgcd33cc358ddbc"},
    {"id": "gemini-3.5-flash", "name": "Gemini 3.5 Flash", "server": "mkol5tgcd33cc358ddbc"},
    {"id": "deepseek-v4-flash", "name": "DeepSeek V4 Flash", "server": "mpsmwmt5fa6174293958"},
    {"id": "deepseek-v4-flash-thinking", "name": "DeepSeek V4 Flash Thinking", "server": "mpsmwmt5fa6174293958"},
    {"id": "grok-4.3", "name": "Grok 4.3", "server": "mpsmwmt5fa6174293958"},
    {"id": "glm-5.1", "name": "GLM 5.1", "server": "mpsmwmt5fa6174293958"},
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "server": "mp3lmkuad07322459f47"},
    {"id": "gpt-oss-120b", "name": "GPT OSS 120B", "server": "mlj8gd8y789d112ec50d"},
    {"id": "gemini-3-flash", "name": "Gemini 3 Flash", "server": "mlv668eaa6d92f50ff10"},
    {"id": "gemma4:31b", "name": "Gemma 4 31B", "server": "mnkjel2208cf770e5009"},
    {"id": "gpt-oss:20b", "name": "GPT OSS 20B", "server": "mnkjel2208cf770e5009"},
    {"id": "nemotron-3-super", "name": "Nemotron 3 Super", "server": "mnkjel2208cf770e5009"},
    {"id": "deepseek-r1:14b", "name": "DeepSeek R1 14B", "server": "mq7ktfibad45c29f3839"},
    {"id": "kimi-k2.6", "name": "Kimi K2.6", "server": "mp5miql908c8738d71be"},
    {"id": "gpt-5.5", "name": "GPT 5.5 (B)", "server": "mp5miql908c8738d71be"},
    {"id": "deepseek-pro", "name": "DeepSeek Pro", "server": "mp5miql908c8738d71be"},
    {"id": "gemini-3.1-pro-preview", "name": "Gemini 3.1 Pro Preview", "server": "mp77ka5la97d6825b53b"},
    {"id": "qwen3.7-max", "name": "Qwen 3.7 Max", "server": "mpq6idkk49907f3c4a5b"},
    {"id": "deepseek-v4-pro", "name": "DeepSeek V4 Pro (D)", "server": "mqcs3lw9218274130973"},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_ROTATION_ORDER = [
    "openai", "deepseek", "gpt-5.4-nano", "grok", "claude", "kimi",
    "mistral", "gemini-2.5-flash", "deepseek-v4-flash", "glm-5.1",
    "qwen3-coder", "perplexity-fast", "gpt-5.4-reasoning",
    "grok-4.3", "gemini-3.5-flash", "gpt-4o-mini", "gpt-oss-120b",
    "kimi-k2.6", "gemma4:31b", "nemotron-3-super",
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": False,
                "thinking": "reason" in m["id"] or "think" in m["id"],
                "tools": False,
            },
        }
        for m in MODELS
    ]


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = DEFAULT_MODEL,
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    requested_server = MODEL_MAP[model].get("server", "")
    rotation = [model]
    for m in _ROTATION_ORDER:
        if m == model:
            continue
        ms = MODEL_MAP.get(m, {}).get("server", "")
        if ms != requested_server:
            rotation.append(m)
    for m in _ROTATION_ORDER:
        if m not in rotation:
            rotation.append(m)

    last_error = None

    for attempt_idx, model_id in enumerate(rotation):
        if attempt_idx > 0:
            logger.info("g4f proxy: rotating to '%s' (attempt %d)", model_id, attempt_idx + 1)
            if last_error and "rate" in last_error.lower():
                import time as _time
                _time.sleep(RATE_LIMIT_SLEEP)

        payload = {
            "model": model_id,
            "messages": [
                {"role": msg.get("role", "user"), "content": msg.get("content", "")}
                for msg in messages
            ],
            "stream": True,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "User-Agent": USER_AGENT,
        }

        try:
            resp = requests.post(
                f"{API_BASE}/chat/completions",
                json=payload,
                headers=headers,
                stream=True,
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as exc:
            last_error = f"request failed: {exc}"
            logger.warning("g4f proxy: %s on '%s'", exc, model_id)
            continue

        if resp.status_code == 429:
            last_error = f"rate limited (429) on '{model_id}'"
            logger.warning("g4f proxy: %s", last_error)
            continue

        if resp.status_code != 200:
            body = resp.text[:300]
            last_error = f"HTTP {resp.status_code}: {body}"
            logger.warning("g4f proxy: %s", last_error)
            continue

        content_type = resp.headers.get("content-type", "")

        if "text/event-stream" in content_type:
            for raw_line in resp.iter_lines(decode_unicode=True):
                if raw_line is None:
                    continue
                line = raw_line.strip()
                if not line:
                    continue
                if line == "data: [DONE]":
                    break
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                try:
                    event = json.loads(data_str)
                except (json.JSONDecodeError, ValueError):
                    continue

                choices = event.get("choices", [])
                if not choices:
                    continue
                delta = choices[0].get("delta", {})
                finish_reason = choices[0].get("finish_reason")

                text = delta.get("content", "")
                if text:
                    yield {"type": "text", "content": text}

                reasoning = delta.get("reasoning", "") or delta.get("reasoning_content", "")
                if reasoning:
                    yield {"type": "thinking", "content": reasoning}

                if finish_reason:
                    yield {"type": "done", "finish_reason": finish_reason}
                    return

            yield {"type": "done", "finish_reason": "stop"}
            return
        else:
            try:
                data = resp.json()
            except (json.JSONDecodeError, ValueError):
                last_error = f"non-json response from '{model_id}'"
                continue

            choices = data.get("choices", [])
            if choices:
                msg = choices[0].get("message", {})
                text = msg.get("content", "")
                reasoning = msg.get("reasoning", "") or msg.get("reasoning_content", "")
                if text:
                    yield {"type": "text", "content": text}
                if reasoning:
                    yield {"type": "thinking", "content": reasoning}
                yield {"type": "done", "finish_reason": choices[0].get("finish_reason", "stop")}
                return
            else:
                last_error = "unexpected response format"
                continue

    yield {"type": "error", "error": f"All models exhausted: {last_error}"}


def simple_chat(
    user_message: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
) -> Optional[str]:
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
