"""
DeepAI chat proxy for the NEBians app ("Neby AI" tab).

Reverse-engineered from https://deepai.org/ (Deep AI, Inc.).

The site uses a custom chat API at https://api.deepai.org/ with:
  - Chat endpoint: POST /hacking_is_a_serious_crime
  - Auth: api-key header with client-generated "tryit" key (fingerprint-based)
  - Body: FormData with chatHistory, model, session_uuid, chat_style, etc.
  - Anti-abuse flag: hacker_is_stinky = "very_stinky"
  - Streaming: raw byte stream, text before \\x1c delimiter, JSON metadata after
  - Thinking models: return {"task_id": "..."}, poll /check_chat_task_status

Models (free tier):
  standard, deepseek-v3.2, gemma-4, gpt-4.1-nano, gpt-oss-120b,
  gpt-5-nano, llama-3.3-70b-instruct, llama-3.1-8b-instant,
  llama-4-scout, qwen3-30b-a3b, gemini-2.5-flash-lite

Models (Pro only):
  genius, supergenius, gpt-4o-mini, gpt-4.1, o4-mini, o3,
  gemini-3-pro-preview, claude-4.7-opus, grok-4.3, gpt-5.3-chat-latest,
  gpt-5.2, chatgpt-4o-latest

Upload endpoint: POST /chat_attachments/upload (FormData with file field)
  Returns: {success: true, attachment: {uuid, original_filename, content_type, download_url}}

This module provides a synchronous Python client suitable for Django views.
"""

import hashlib
import json
import logging
import math
import random
import time
import uuid

import requests

logger = logging.getLogger(__name__)

# ========================= Configuration =========================

DEEPAI_API_BASE = "https://api.deepai.org"
DEEPAI_SITE_URL = "https://deepai.org"
CHAT_ENDPOINT = "/hacking_is_a_serious_crime"
THINKING_STATUS_ENDPOINT = "/check_chat_task_status"
UPLOAD_ENDPOINT = "/chat_attachments/upload"
REQUEST_TIMEOUT = 180
UPLOAD_TIMEOUT = 120

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
_SALT = "hackers_become_a_little_stinkier_every_time_they_hack"

FREE_MODELS = [
    {"id": "standard", "name": "DeepAI Standard", "locked": False, "vision": False, "thinking": False},
    {"id": "deepseek-v3.2", "name": "DeepSeek V3.2", "locked": False, "vision": False, "thinking": False},
    {"id": "gemma-4", "name": "Gemma 4", "locked": False, "vision": True, "thinking": False},
    {"id": "gpt-4.1-nano", "name": "GPT-4.1 Nano", "locked": False, "vision": False, "thinking": False},
    {"id": "gpt-5-nano", "name": "GPT-5 Nano", "locked": False, "vision": True, "thinking": False},
    {"id": "gpt-oss-120b", "name": "GPT OSS 120B", "locked": False, "vision": False, "thinking": True},
    {"id": "gemini-2.5-flash-lite", "name": "Gemini 2.5 Flash Lite", "locked": False, "vision": True, "thinking": False},
    {"id": "llama-3.3-70b-instruct", "name": "Llama 3.3 70B", "locked": False, "vision": False, "thinking": False},
    {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B", "locked": False, "vision": False, "thinking": False},
    {"id": "llama-4-scout", "name": "Llama 4 Scout", "locked": False, "vision": True, "thinking": False},
    {"id": "qwen3-30b-a3b", "name": "Qwen3 30B", "locked": False, "vision": True, "thinking": True},
]

PRO_MODELS = [
    {"id": "genius", "name": "DeepAI Genius", "locked": True, "vision": False, "thinking": False},
    {"id": "supergenius", "name": "DeepAI Super Genius", "locked": True, "vision": False, "thinking": True},
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "locked": True, "vision": True, "thinking": False},
    {"id": "gpt-4.1", "name": "GPT-4.1", "locked": True, "vision": True, "thinking": False},
    {"id": "o4-mini", "name": "o4 Mini", "locked": True, "vision": False, "thinking": True},
    {"id": "o3", "name": "o3", "locked": True, "vision": False, "thinking": True},
    {"id": "gemini-3-pro-preview", "name": "Gemini 3.1 Pro", "locked": True, "vision": True, "thinking": True},
    {"id": "claude-4.7-opus", "name": "Claude Opus 4.7", "locked": True, "vision": True, "thinking": False},
    {"id": "grok-4.3", "name": "Grok 4.3", "locked": True, "vision": False, "thinking": True},
    {"id": "gpt-5.3-chat-latest", "name": "GPT-5.3 Chat", "locked": True, "vision": False, "thinking": False},
    {"id": "gpt-5.2", "name": "GPT-5.2", "locked": True, "vision": True, "thinking": False},
    {"id": "chatgpt-4o-latest", "name": "ChatGPT 4o Latest", "locked": True, "vision": True, "thinking": False},
]

ALL_MODELS = FREE_MODELS + PRO_MODELS


# ========================= Errors =========================

class DeepAIError(Exception):
    """Generic DeepAI API failure (non-2xx or unexpected payload)."""
    def __init__(self, message, status_code=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


# ========================= Helpers =========================

def _generate_tryit_key():
    """Generate an anonymous tryit API key mimicking the browser client."""
    random_num = str(math.floor(random.random() * 100000000000))

    def _h(s):
        return hashlib.sha256(s.encode()).hexdigest()[:64]

    inner = _h(USER_AGENT + _h(USER_AGENT + _h(USER_AGENT + random_num + _SALT)))
    return f"tryit-{random_num}-{inner}"


def _model_info(model):
    """Look up model metadata by ID."""
    for m in ALL_MODELS:
        if m["id"] == model:
            return m
    return None


def _is_thinking_model(model):
    info = _model_info(model)
    return info.get("thinking", False) if info else False


def _is_vision_model(model):
    info = _model_info(model)
    return info.get("vision", False) if info else False


def _build_chat_history(history):
    """Convert simple history list to DeepAI chatHistory format."""
    result = []
    for msg in history:
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


def get_models():
    """Return available DeepAI models as a list of dicts."""
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "provider": "deepai",
            "vision": m.get("vision", False),
            "thinking": m.get("thinking", False),
            "locked": m.get("locked", False),
        }
        for m in ALL_MODELS
    ]


def resolve_model(model_id):
    """
    Validate and resolve a model ID.
    Returns (model_id, model_info_dict) or raises DeepAIError.
    """
    if not model_id:
        model_id = "standard"
    info = _model_info(model_id)
    if info is None:
        raise DeepAIError(f"Unknown DeepAI model: {model_id}")
    return model_id, info


# ========================= Chat API =========================

def chat(
    user_message,
    model="standard",
    history=None,
    system_prompt="",
    timeout=REQUEST_TIMEOUT,
):
    """
    Send a chat message to DeepAI and return the full response text.

    Args:
        user_message: The user's message text.
        model: Model identifier (e.g. "standard", "deepseek-v3.2").
        history: List of previous messages as dicts with "role" and "content".
        system_prompt: Optional system prompt prepended to the user message.
        timeout: Request timeout in seconds.

    Returns:
        The full response text, or empty string on failure.
    """
    if history is None:
        history = []

    model_id, info = resolve_model(model)
    api_key = _generate_tryit_key()

    chat_history = _build_chat_history(history)
    if system_prompt and not any(m.get("role") == "user" and system_prompt in m.get("content", "") for m in chat_history):
        chat_history.insert(0, {"role": "user", "content": f"[System Instructions]\n{system_prompt}"})

    chat_history.append({"role": "user", "content": user_message})

    form_fields = {
        "chatHistory": json.dumps(chat_history),
        "model": model_id,
        "session_uuid": str(uuid.uuid4()),
        "chat_style": "chat",
        "sensitivity_request_id": str(uuid.uuid4()),
        "hacker_is_stinky": "very_stinky",
    }

    if _is_thinking_model(model_id):
        form_fields["thinking_support"] = "1"

    headers = {
        "api-key": api_key,
        "User-Agent": USER_AGENT,
        "Origin": DEEPAI_SITE_URL,
        "Referer": f"{DEEPAI_SITE_URL}/chat/",
    }

    try:
        r = requests.post(
            f"{DEEPAI_API_BASE}{CHAT_ENDPOINT}",
            data=form_fields,
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        logger.exception("deepai: chat request failed: %s", exc)
        raise DeepAIError(f"Request failed: {exc}") from exc

    if r.status_code == 401:
        raise DeepAIError("Unauthorized (401)", status_code=401, body=r.text)
    if r.status_code == 402:
        raise DeepAIError("Quota exceeded (402)", status_code=402, body=r.text)
    if r.status_code != 200:
        raise DeepAIError(f"HTTP {r.status_code}", status_code=r.status_code, body=r.text[:500])

    content_type = r.headers.get("content-type", "")

    if _is_thinking_model(model_id) and "application/json" in content_type:
        try:
            data = r.json()
        except (json.JSONDecodeError, ValueError):
            raise DeepAIError("Thinking model returned invalid JSON")

        task_id = data.get("task_id")
        if not task_id:
            raise DeepAIError("Thinking model returned no task_id")

        return _poll_thinking_task(task_id, api_key, timeout=timeout)

    text = r.text
    sep_idx = text.find("\x1c")
    if sep_idx != -1:
        text = text[:sep_idx]

    return text.strip()


def _poll_thinking_task(task_id, api_key, timeout=REQUEST_TIMEOUT):
    """Poll the thinking task status endpoint until result is available."""
    poll_url = f"{DEEPAI_API_BASE}{THINKING_STATUS_ENDPOINT}"
    headers = {"api-key": api_key, "User-Agent": USER_AGENT}
    max_attempts = timeout // 2

    for _ in range(max_attempts):
        try:
            r = requests.get(
                poll_url,
                params={"type": "thinking-task", "task_id": task_id},
                headers=headers,
                timeout=30,
            )
        except requests.RequestException:
            time.sleep(2)
            continue

        if r.status_code != 200:
            raise DeepAIError(f"Thinking poll HTTP {r.status_code}", status_code=r.status_code)

        try:
            data = r.json()
        except (json.JSONDecodeError, ValueError):
            time.sleep(2)
            continue

        status = data.get("status", "")

        if status in ("complete", "completed", "done"):
            return data.get("result", data.get("text", ""))

        if status in ("failed", "error"):
            raise DeepAIError(data.get("error", "thinking task failed"))

        time.sleep(2)

    raise DeepAIError("Thinking task timed out")


# ========================= Streaming Chat =========================

def stream_chat(
    user_message,
    model="standard",
    history=None,
    system_prompt="",
    timeout=REQUEST_TIMEOUT,
):
    """
    Stream chat from DeepAI, yielding dicts with type 'content', 'done', or 'error'.

    Yields:
        {"type": "content", "text": "..."} - incremental text chunk
        {"type": "done", "finishReason": "stop"} - stream complete
        {"type": "error", "message": "..."} - error occurred
    """
    if history is None:
        history = []

    model_id, info = resolve_model(model)
    api_key = _generate_tryit_key()

    chat_history = _build_chat_history(history)
    if system_prompt and not any(m.get("role") == "user" and system_prompt in m.get("content", "") for m in chat_history):
        chat_history.insert(0, {"role": "user", "content": f"[System Instructions]\n{system_prompt}"})

    chat_history.append({"role": "user", "content": user_message})

    form_fields = {
        "chatHistory": json.dumps(chat_history),
        "model": model_id,
        "session_uuid": str(uuid.uuid4()),
        "chat_style": "chat",
        "sensitivity_request_id": str(uuid.uuid4()),
        "hacker_is_stinky": "very_stinky",
    }

    if _is_thinking_model(model_id):
        form_fields["thinking_support"] = "1"

    headers = {
        "api-key": api_key,
        "User-Agent": USER_AGENT,
        "Origin": DEEPAI_SITE_URL,
        "Referer": f"{DEEPAI_SITE_URL}/chat/",
    }

    try:
        r = requests.post(
            f"{DEEPAI_API_BASE}{CHAT_ENDPOINT}",
            data=form_fields,
            headers=headers,
            timeout=timeout,
            stream=True,
        )
    except requests.RequestException as exc:
        logger.exception("deepai: stream request failed: %s", exc)
        yield {"type": "error", "message": f"Request failed: {exc}"}
        return

    if r.status_code == 401:
        yield {"type": "error", "message": "Unauthorized (401)"}
        return
    if r.status_code == 402:
        yield {"type": "error", "message": "Quota exceeded (402)"}
        return
    if r.status_code != 200:
        body = r.text[:500] if hasattr(r, 'text') else ''
        yield {"type": "error", "message": f"HTTP {r.status_code}: {body}"}
        return

    content_type = r.headers.get("content-type", "")

    if _is_thinking_model(model_id) and "application/json" in content_type:
        try:
            data = r.json()
        except (json.JSONDecodeError, ValueError):
            yield {"type": "error", "message": "Thinking model returned invalid JSON"}
            return

        task_id = data.get("task_id")
        if not task_id:
            yield {"type": "error", "message": "Thinking model returned no task_id"}
            return

        yield from _stream_thinking_task(task_id, api_key, timeout=timeout)
        return

    text_buffer = ""
    json_buffer = ""
    in_json_payload = False
    for chunk in r.iter_content(chunk_size=4096, decode_unicode=True):
        if not chunk:
            continue
        text_buffer += chunk

        while True:
            if in_json_payload:
                newline_idx = text_buffer.find("\n")
                if newline_idx == -1:
                    json_buffer += text_buffer
                    text_buffer = ""
                    break
                json_buffer += text_buffer[:newline_idx]
                text_buffer = text_buffer[newline_idx + 1:]
                in_json_payload = False
                if json_buffer.strip():
                    try:
                        payload = json.loads(json_buffer.strip())
                        if isinstance(payload, dict) and "function_call" in payload:
                            yield {"type": "tool_call", "data": payload["function_call"]}
                    except (json.JSONDecodeError, ValueError):
                        pass
                json_buffer = ""
                continue

            sep_idx = text_buffer.find("\x1c")
            if sep_idx != -1:
                text_part = text_buffer[:sep_idx]
                text_buffer = text_buffer[sep_idx + 1:]
                if text_part:
                    yield {"type": "content", "text": text_part}
                in_json_payload = True
                json_buffer = ""
                continue

            yield_len = max(0, len(text_buffer) - 256)
            if yield_len > 0:
                to_yield = text_buffer[:yield_len]
                text_buffer = text_buffer[yield_len:]
                yield {"type": "content", "text": to_yield}
            break

    if text_buffer:
        yield {"type": "content", "text": text_buffer}

    yield {"type": "done", "finishReason": "stop"}


def _stream_thinking_task(task_id, api_key, timeout=REQUEST_TIMEOUT):
    """Poll thinking task and yield result as a single content chunk."""
    poll_url = f"{DEEPAI_API_BASE}{THINKING_STATUS_ENDPOINT}"
    headers = {"api-key": api_key, "User-Agent": USER_AGENT}
    max_attempts = timeout // 2

    for _ in range(max_attempts):
        try:
            r = requests.get(
                poll_url,
                params={"type": "thinking-task", "task_id": task_id},
                headers=headers,
                timeout=30,
            )
        except requests.RequestException:
            time.sleep(2)
            continue

        if r.status_code != 200:
            yield {"type": "error", "message": f"Thinking poll HTTP {r.status_code}"}
            return

        try:
            data = r.json()
        except (json.JSONDecodeError, ValueError):
            time.sleep(2)
            continue

        status = data.get("status", "")

        if status in ("complete", "completed", "done"):
            result_text = data.get("result", data.get("text", ""))
            if result_text:
                yield {"type": "content", "text": result_text}
            yield {"type": "done", "finishReason": "stop"}
            return

        if status in ("failed", "error"):
            yield {"type": "error", "message": data.get("error", "thinking task failed")}
            return

        time.sleep(2)

    yield {"type": "error", "message": "Thinking task timed out"}


# ========================= File Upload =========================

def upload_file(file_path, model="standard", timeout=UPLOAD_TIMEOUT):
    """
    Upload a file to DeepAI as a chat attachment.

    Args:
        file_path: Path to the file to upload.
        model: Model identifier (for reference only).
        timeout: Upload timeout in seconds.

    Returns:
        Attachment dict with: uuid, original_filename, content_type, download_url
        or None on failure.
    """
    import os
    import mimetypes

    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    api_key = _generate_tryit_key()
    headers = {"api-key": api_key, "User-Agent": USER_AGENT, "Origin": DEEPAI_SITE_URL}

    try:
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, mime_type)}
            r = requests.post(
                f"{DEEPAI_API_BASE}{UPLOAD_ENDPOINT}",
                files=files,
                headers=headers,
                timeout=timeout,
            )
    except requests.RequestException as exc:
        logger.warning("deepai: upload request failed: %s", exc)
        return None

    if r.status_code != 200:
        logger.warning("deepai: upload failed with status %d: %s", r.status_code, r.text[:300])
        return None

    try:
        data = r.json()
    except (json.JSONDecodeError, ValueError):
        logger.warning("deepai: upload response not JSON: %s", r.text[:300])
        return None

    if data.get("success"):
        return data.get("attachment")

    logger.warning("deepai: upload response not success: %s", r.text[:300])
    return None


def upload_file_from_bytes(filename, file_data, content_type=None, model="standard", timeout=UPLOAD_TIMEOUT):
    """
    Upload file bytes to DeepAI as a chat attachment.

    Args:
        filename: Name of the file.
        file_data: Raw file bytes.
        content_type: MIME type (auto-detected if None).
        model: Model identifier (for reference only).
        timeout: Upload timeout in seconds.

    Returns:
        Attachment dict or None on failure.
    """
    import mimetypes

    if not content_type:
        ext = ""
        if "." in filename:
            ext = "." + filename.rsplit(".", 1)[1].lower()
        content_type = mimetypes.types_map.get(ext, "application/octet-stream")

    api_key = _generate_tryit_key()
    headers = {"api-key": api_key, "User-Agent": USER_AGENT, "Origin": DEEPAI_SITE_URL}

    try:
        files = {"file": (filename, file_data, content_type)}
        r = requests.post(
            f"{DEEPAI_API_BASE}{UPLOAD_ENDPOINT}",
            files=files,
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        logger.warning("deepai: upload request failed: %s", exc)
        return None

    if r.status_code != 200:
        logger.warning("deepai: upload failed with status %d: %s", r.status_code, r.text[:300])
        return None

    try:
        data = r.json()
    except (json.JSONDecodeError, ValueError):
        logger.warning("deepai: upload response not JSON: %s", r.text[:300])
        return None

    if data.get("success"):
        return data.get("attachment")

    logger.warning("deepai: upload response not success: %s", r.text[:300])
    return None


# ========================= Simple Chat (for Neby bot) =========================

def simple_chat(user_message, model="standard", system_prompt="", timeout=60):
    """
    Simple one-shot chat for the Neby bot. Returns just the response text string.

    Args:
        user_message: The user's message text.
        model: Model identifier.
        system_prompt: Optional system instructions.
        timeout: Request timeout in seconds.

    Returns:
        Response text string, or empty string on failure.
    """
    try:
        return chat(
            user_message=user_message,
            model=model,
            history=[],
            system_prompt=system_prompt,
            timeout=timeout,
        )
    except DeepAIError as exc:
        logger.warning("deepai: simple_chat error: %s", exc)
        return ""