"""
EasyChat / eqing.tech chat proxy for the NEBians app ("Neby AI" tab).

Reverse-engineered from https://chat3.eqing.tech/ (EasyChat v2.10.11).

The site uses an OpenAI-compatible API with:
  - Chat endpoint: POST {apiHost}/v1/chat/completions  (SSE streaming)
  - Models endpoint: GET  {apiHost}/v1/models
  - Auth: guest ID header (x-guest-id) or Supabase Bearer token
  - Captcha: altcha proof-of-work (captchaToken in request body)
  - Anti-abuse: guest ID tracking, rate limiting (429)

Streaming format: OpenAI SSE (data: {"choices":[{"delta":{"content":"..."}}]})
  Plus custom events: [JSON], [ADD], [ORIGIN], [CALLBACK]
  [CALLBACK] CLEAR-CAPTCHA-TOKEN resets the captcha token

Altcha PoW captcha:
  1. Fetch challenge from {apiHost}/v1/altcha (GET)
  2. Challenge: {"algorithm":"SHA-256","challenge":"...","salt":"...","signature":"..."}
  3. Solve: find nonce N where SHA-256(salt + N) starts with challenge prefix
  4. Solution: base64(JSON({algorithm,challenge,salt,signature,nonce}))
  5. Send solution as captchaToken in chat request body
"""

import base64
import hashlib
import json
import logging
import secrets
import string
import time
from typing import Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

API_BASE = "https://easy-api-eo.llm99.com"
SITE_URL = "https://chat3.eqing.tech"
REQUEST_TIMEOUT = 120

FREE_MODELS = [
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "vision": False, "thinking": False},
    {"id": "gpt-4o-mini-image-free", "name": "GPT-4o Mini Vision", "vision": True, "thinking": False},
    {"id": "gpt-5-free", "name": "GPT-5 Free", "vision": False, "thinking": False},
    {"id": "grok-4.1-fast-free", "name": "Grok 4.1 Fast", "vision": False, "thinking": False},
    {"id": "openrouter-free", "name": "OpenRouter Free", "vision": False, "thinking": False},
    {"id": "gemini-3-flash", "name": "Gemini 3 Flash", "vision": False, "thinking": False},
    {"id": "code-claude-3.5-sonnet-free", "name": "Claude 3.5 Sonnet Free", "vision": True, "thinking": False},
    {"id": "code-claude-3-opus", "name": "Claude 3 Opus Free", "vision": True, "thinking": False},
]

VIP_MODELS = [
    {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "vision": False, "thinking": False},
    {"id": "claude-3.5-sonnet", "name": "Claude 3.5 Sonnet", "vision": True, "thinking": False},
    {"id": "gpt-4o-all", "name": "GPT-4o All", "vision": False, "thinking": False},
    {"id": "gpt-4-all", "name": "GPT-4 All", "vision": True, "thinking": False},
    {"id": "yi-lightning", "name": "Yi Lightning", "vision": False, "thinking": False},
    {"id": "o1-mini", "name": "o1 Mini", "vision": False, "thinking": True},
    {"id": "g-0S5FXLyFN", "name": "G Custom", "vision": True, "thinking": False},
]

SVIP_MODELS = [
    {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "vision": True, "thinking": False},
    {"id": "gpt-4o", "name": "GPT-4o", "vision": True, "thinking": False},
    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "vision": True, "thinking": False},
]

NEW_MODELS = [
    {"id": "gpt-5-3-all", "name": "GPT-5.3 All", "vision": False, "thinking": False},
    {"id": "gpt-5-2-all", "name": "GPT-5.2 All", "vision": False, "thinking": False},
    {"id": "gpt-5-3-image", "name": "GPT-5.3 Image", "vision": True, "thinking": False},
    {"id": "claude-sonnet-4-6-thinking", "name": "Claude Sonnet 4.6 Thinking", "vision": False, "thinking": True},
    {"id": "claude-opus-4-6-thinking", "name": "Claude Opus 4.6 Thinking", "vision": False, "thinking": True},
    {"id": "gemini-3.1-pro", "name": "Gemini 3.1 Pro", "vision": False, "thinking": False},
    {"id": "gpt-5-2-thinking", "name": "GPT-5.2 Thinking", "vision": False, "thinking": True},
    {"id": "gpt-5-2-thinking-extended", "name": "GPT-5.2 Thinking Ext", "vision": False, "thinking": True},
    {"id": "gpt-5-2-thinking-max", "name": "GPT-5.2 Thinking Max", "vision": False, "thinking": True},
    {"id": "gpt-5-4-thinking", "name": "GPT-5.4 Thinking", "vision": False, "thinking": True},
    {"id": "gpt-5-4-thinking-extended", "name": "GPT-5.4 Thinking Ext", "vision": False, "thinking": True},
    {"id": "gpt-5-4-thinking-max", "name": "GPT-5.4 Thinking Max", "vision": False, "thinking": True},
    {"id": "gpt-5-5-thinking", "name": "GPT-5.5 Thinking", "vision": False, "thinking": True},
    {"id": "gpt-5-5-thinking-extended", "name": "GPT-5.5 Thinking Ext", "vision": False, "thinking": True},
    {"id": "gpt-5-5-thinking-max", "name": "GPT-5.5 Thinking Max", "vision": False, "thinking": True},
    {"id": "gpt-5.5(xhigh)", "name": "GPT-5.5 xHigh", "vision": False, "thinking": False},
    {"id": "gpt-5.3-codex(xhigh)", "name": "GPT-5.3 Codex xHigh", "vision": False, "thinking": False},
    {"id": "gpt-5.2(high)", "name": "GPT-5.2 High", "vision": False, "thinking": False},
    {"id": "o3", "name": "o3", "vision": False, "thinking": True},
]

ALL_MODELS = FREE_MODELS + VIP_MODELS + SVIP_MODELS + NEW_MODELS
_THINKING_MODELS = set(m["id"] for m in ALL_MODELS if m.get("thinking"))

_guest_id = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(24))
_captcha_token = None
_captcha_token_time = 0.0
_CAPTCHA_TTL = 300.0


class EQingError(Exception):
    def __init__(self, message, status_code=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def _generate_guest_id():
    global _guest_id
    _guest_id = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(24))
    return _guest_id


def _is_thinking_model(model):
    return model in _THINKING_MODELS or "thinking" in model.lower() or "deepseek-r" in model.lower()


def _solve_altcha_challenge(challenge_data, max_iterations=1000000):
    algorithm = challenge_data.get("algorithm", "SHA-256")
    challenge = challenge_data.get("challenge", "")
    salt = challenge_data.get("salt", "")
    signature = challenge_data.get("signature", "")

    if not challenge or not salt:
        logger.warning("eqing: altcha challenge missing required fields")
        return None

    if algorithm != "SHA-256":
        logger.warning("eqing: unsupported altcha algorithm: %s", algorithm)
        return None

    for nonce in range(max_iterations):
        message = f"{salt}{nonce}"
        hash_result = hashlib.sha256(message.encode()).hexdigest()
        if hash_result.startswith(challenge):
            solution = {
                "algorithm": algorithm,
                "challenge": challenge,
                "salt": salt,
                "signature": signature,
                "nonce": nonce,
            }
            return base64.b64encode(json.dumps(solution).encode()).decode()

    logger.warning("eqing: altcha challenge not solved within %d iterations", max_iterations)
    return None


def _fetch_captcha_token():
    global _captcha_token, _captcha_token_time

    if _captcha_token and (time.time() - _captcha_token_time) < _CAPTCHA_TTL:
        return _captcha_token

    try:
        r = requests.get(
            f"{API_BASE}/v1/altcha",
            headers={
                "Accept": "application/json",
                "x-requested-with": "XMLHttpRequest",
                "x-guest-id": _guest_id,
            },
            timeout=15,
        )
        if r.status_code != 200:
            logger.warning("eqing: altcha challenge failed with status %d", r.status_code)
            return _captcha_token

        content_type = r.headers.get("content-type", "")
        if "json" not in content_type:
            logger.warning("eqing: altcha challenge returned non-JSON: %s", content_type)
            return _captcha_token

        challenge_data = r.json()
        token = _solve_altcha_challenge(challenge_data)
        if token:
            _captcha_token = token
            _captcha_token_time = time.time()
            return token

    except Exception as exc:
        logger.warning("eqing: altcha challenge error: %s", exc)

    return _captcha_token


def get_models():
    try:
        r = requests.get(
            f"{API_BASE}/v1/models",
            headers={
                "Content-Type": "application/json",
                "x-requested-with": "XMLHttpRequest",
                "x-guest-id": _generate_guest_id(),
            },
            timeout=15,
        )
        if r.status_code == 200:
            data = r.json()
            models = data.get("data", [])
            locked_ids = (
                set(m["id"] for m in VIP_MODELS)
                | set(m["id"] for m in SVIP_MODELS)
                | set(m["id"] for m in NEW_MODELS)
            )
            return [
                {
                    "id": m.get("id", ""),
                    "name": m.get("id", ""),
                    "provider": "eqing",
                    "vision": any(v in m.get("id", "").lower() for v in ["image", "vision", "4o", "gpt-5-3-image"]),
                    "thinking": _is_thinking_model(m.get("id", "")),
                    "locked": m.get("id", "") in locked_ids,
                }
                for m in models
            ]
    except Exception as exc:
        logger.warning("eqing: failed to fetch models: %s", exc)

    return [
        {
            "id": m["id"],
            "name": m["name"],
            "provider": "eqing",
            "vision": m.get("vision", False),
            "thinking": m.get("thinking", False),
            "locked": m in VIP_MODELS or m in SVIP_MODELS or m in NEW_MODELS,
        }
        for m in ALL_MODELS
    ]


def resolve_model(model_id):
    if not model_id:
        model_id = "gpt-4o-mini"
    return model_id


def _build_messages(user_message, history=None, system_prompt=""):
    if history is None:
        history = []

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            content = "\n".join(text_parts)
        if content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})
    return messages


def chat(user_message, model="gpt-4o-mini", history=None, system_prompt="", timeout=REQUEST_TIMEOUT):
    if history is None:
        history = []

    model_id = resolve_model(model)
    messages = _build_messages(user_message, history, system_prompt)

    body = {
        "model": model_id,
        "messages": messages,
        "stream": False,
    }

    if not _is_thinking_model(model_id):
        body["temperature"] = 0.5

    total_chars = sum(len(m.get("content", "")) for m in messages if isinstance(m.get("content"), str))
    body["chat_token"] = max(1, total_chars // 4)

    captcha_token = _fetch_captcha_token()
    if captcha_token:
        body["captchaToken"] = captcha_token

    headers = {
        "Content-Type": "application/json",
        "x-requested-with": "XMLHttpRequest",
        "x-guest-id": _guest_id,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Origin": SITE_URL,
        "Referer": f"{SITE_URL}/",
    }

    try:
        r = requests.post(
            f"{API_BASE}/v1/chat/completions",
            json=body,
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        logger.exception("eqing: chat request failed: %s", exc)
        raise EQingError(f"Request failed: {exc}") from exc

    if r.status_code == 403:
        global _captcha_token, _captcha_token_time
        _captcha_token = None
        _captcha_token_time = 0.0
        try:
            error_data = r.json()
            msg = error_data.get("message", "Forbidden")
        except (json.JSONDecodeError, ValueError):
            msg = r.text[:200]
        raise EQingError(f"403 Forbidden: {msg}", status_code=403, body=r.text[:500])

    if r.status_code == 429:
        raise EQingError("Rate limited (429)", status_code=429, body=r.text[:200])

    if r.status_code != 200:
        raise EQingError(f"HTTP {r.status_code}", status_code=r.status_code, body=r.text[:500])

    try:
        data = r.json()
        choices = data.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            return message.get("content", "")
    except (json.JSONDecodeError, ValueError):
        pass

    return r.text


def stream_chat(user_message, model="gpt-4o-mini", history=None, system_prompt="", timeout=REQUEST_TIMEOUT):
    if history is None:
        history = []

    model_id = resolve_model(model)
    messages = _build_messages(user_message, history, system_prompt)

    body = {
        "model": model_id,
        "messages": messages,
        "stream": True,
    }

    if not _is_thinking_model(model_id):
        body["temperature"] = 0.5
        body["presence_penalty"] = 0
        body["frequency_penalty"] = 0
        body["top_p"] = 1

    total_chars = sum(len(m.get("content", "")) for m in messages if isinstance(m.get("content"), str))
    body["chat_token"] = max(1, total_chars // 4)

    captcha_token = _fetch_captcha_token()
    if captcha_token:
        body["captchaToken"] = captcha_token

    headers = {
        "Content-Type": "application/json",
        "x-requested-with": "XMLHttpRequest",
        "x-guest-id": _guest_id,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Origin": SITE_URL,
        "Referer": f"{SITE_URL}/",
    }

    try:
        r = requests.post(
            f"{API_BASE}/v1/chat/completions",
            json=body,
            headers=headers,
            timeout=timeout,
            stream=True,
        )
    except requests.RequestException as exc:
        logger.exception("eqing: stream request failed: %s", exc)
        yield {"type": "error", "message": f"Request failed: {exc}"}
        return

    if r.status_code == 403:
        global _captcha_token, _captcha_token_time
        _captcha_token = None
        _captcha_token_time = 0.0
        try:
            error_data = r.json()
            msg = error_data.get("message", "Forbidden")
            callback = error_data.get("callback", "")
            if callback == "CLEAR-CAPTCHA-TOKEN":
                _captcha_token = None
                _captcha_token_time = 0.0
        except (json.JSONDecodeError, ValueError):
            msg = r.text[:200]
        yield {"type": "error", "message": f"403 Forbidden: {msg}"}
        return

    if r.status_code == 429:
        yield {"type": "error", "message": "Rate limited (429), please try again later"}
        return

    if r.status_code != 200:
        body_text = r.text[:500] if hasattr(r, "text") else ""
        yield {"type": "error", "message": f"HTTP {r.status_code}: {body_text}"}
        return

    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue

        line = line.strip()

        if line.startswith("event: "):
            event_type = line[7:].strip()
            if event_type == "[CALLBACK]":
                continue
            continue

        if line.startswith("data: "):
            data_str = line[6:]
            if data_str == "[DONE]":
                break

            try:
                data = json.loads(data_str)
            except (json.JSONDecodeError, ValueError):
                continue

            choices = data.get("choices", [])
            if not choices:
                callback = data.get("callback")
                if callback == "CLEAR-CAPTCHA-TOKEN":
                    _captcha_token = None
                    _captcha_token_time = 0.0
                continue

            delta = choices[0].get("delta", {})
            content = delta.get("content", "")
            reasoning = delta.get("reasoning_content", "")

            if reasoning:
                yield {"type": "content", "text": f"\n"}

            if content:
                yield {"type": "content", "text": content}

    yield {"type": "done", "finishReason": "stop"}


def simple_chat(user_message, model="gpt-4o-mini", system_prompt="", timeout=60):
    try:
        return chat(
            user_message=user_message,
            model=model,
            history=[],
            system_prompt=system_prompt,
            timeout=timeout,
        )
    except EQingError as exc:
        logger.warning("eqing: simple_chat error: %s", exc)
        return ""