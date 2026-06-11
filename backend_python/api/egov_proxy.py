"""
eGov Chat AI proxy for the NEBians app ("Neby AI" tab).

Reverse-engineered from https://egov-chat-ai.e.gov.ph/ (Philippine government AI chat).
The site is a Next.js App Router app using React Server Actions:

  Chat action (hash: e9cdae80f2464df764330696f476c324ccbfd7cb):
    POST /chat?model=<model>&scope=<scope>
    Headers: Next-Action, Content-Type: text/plain;charset=UTF-8
    Body: JSON array [scope, model, sessionId, userMessage, conversationHistory]

  Upload action (hash: 75c980102f4a31e2fc1369cda63e30e9f538a02c):
    POST /chat?model=<model>&scope=<scope>
    Headers: Next-Action, Content-Type: multipart/form-data
    Body: FormData with fields: 0=["$K1"], 1_files=<file>, 1_model=<model>
    Returns: file_data object {filename, original_filename, mime_type, cdnUrl}

  Streaming format: RSC (React Server Components) NDJSON-like stream
    Lines: <id>:{"curr":"<text>","next":"$@<nextId>"}
    Final line: <id>:{}

  Models:
    AI1 - accepts jpeg/jpg/png/heif/pdf (scope: ph = "Juan" Philippine AI, global = Google model)
    AI2 - accepts jpeg/jpg/png/gif (different model, limited responses via API)

  Scopes: "ph" (Philippines-specific), "global" (general knowledge)

This module provides a synchronous Python client suitable for Django views.
"""

import json
import logging
import os
import secrets
import mimetypes
import uuid

import requests

logger = logging.getLogger(__name__)

# ========================= Configuration =========================

EGOV_BASE_URL = "https://egov-chat-ai.e.gov.ph"
CHAT_ACTION_HASH = "e9cdae80f2464df764330696f476c324ccbfd7cb"
UPLOAD_ACTION_HASH = "75c980102f4a31e2fc1369cda63e30e9f538a02c"
REQUEST_TIMEOUT = 120
UPLOAD_TIMEOUT = 60
CDN_BASE = "https://storage.googleapis.com/egovai-bucket/"

# Accepted file types per model
UPLOAD_ACCEPT_TYPES_AI1 = {"image/jpeg", "image/jpg", "image/png", "image/heif", "application/pdf"}
UPLOAD_ACCEPT_TYPES_AI2 = {"image/jpeg", "image/jpg", "image/png", "image/gif"}

# ========================= Errors =========================

class EGovError(Exception):
    """Generic eGov API failure (non-2xx or unexpected payload)."""
    def __init__(self, message, status_code=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


# ========================= Model resolution =========================

def resolve_scope_and_model(model: str):
    """
    Resolve model string to (scope, model_id).

    Models:
      - "AI1" or "AI1-global" -> ("global", "AI1")
      - "AI1-ph" -> ("ph", "AI1")
      - "AI2" or "AI2-global" -> ("global", "AI2")
      - "AI2-ph" -> ("ph", "AI2")
      - Default -> ("global", "AI1")
    """
    model_lower = (model or "").lower().strip()

    if model_lower.endswith("-ph"):
        scope = "ph"
        model_id = model_lower[:-3].upper()
        if model_id not in ("AI1", "AI2"):
            model_id = "AI1"
        return scope, model_id

    if model_lower.endswith("-global"):
        model_id = model_lower[:-7].upper()
        if model_id not in ("AI1", "AI2"):
            model_id = "AI1"
        return "global", model_id

    if model_lower in ("ai1", "ai2"):
        return "global", model_lower.upper()

    return "global", "AI1"


# ========================= RSC Stream Parser =========================

def parse_rsc_stream(text: str) -> str:
    """
    Parse React Server Components streaming format and extract accumulated text.

    The stream consists of lines in the format:
        <id>:<json>
    Where JSON objects have "curr" (current text chunk) and "next" (reference to next chunk).
    """
    chunks = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        colon_idx = line.find(":")
        if colon_idx < 0:
            continue
        payload = line[colon_idx + 1:]
        if not payload or payload.startswith('"$'):
            continue
        try:
            data = json.loads(payload)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(data, dict) and "curr" in data:
            line_id = line[:colon_idx]
            chunks[line_id] = data.get("curr", "")

    ordered_ids = sorted(chunks.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))
    return "".join(chunks[cid] for cid in ordered_ids)


# ========================= Chat API =========================

def chat(
    user_message: str,
    model: str = "AI1",
    scope: str = None,
    history: list = None,
    system_prompt: str = "",
    timeout: int = REQUEST_TIMEOUT,
) -> str:
    """
    Send a chat message to eGov AI and return the full response text.

    Args:
        user_message: The user's message text.
        model: Model identifier (AI1, AI1-ph, AI2, AI2-ph, etc.).
        scope: Override scope ("ph" or "global"). If None, resolved from model.
        history: List of previous messages as dicts with "role" and "content" keys.
                 Each content can be a string or list of content parts.
        system_prompt: Optional system prompt prepended to the user message.
        timeout: Request timeout in seconds.

    Returns:
        The full response text, or empty string on failure.
    """
    if history is None:
        history = []

    resolved_scope, model_id = resolve_scope_and_model(model)
    if scope:
        resolved_scope = scope
    session_id = secrets.token_hex(16)

    # Build content parts
    content_parts = []

    # Process history into eGov format
    conversation_history = []
    user_text = ""

    for i, msg in enumerate(history):
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif item.get("type") == "image_url":
                        url = item.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        if url:
                            content_parts.append({"type": "image", "image": url})
            content = "\n".join(text_parts)

        if not content:
            continue

        if role == "system":
            system_prompt = (system_prompt + "\n" + content).strip()
        elif role == "assistant":
            conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": content}],
            })
        else:
            if i == len(history) - 1:
                user_text = content
            else:
                conversation_history.append({
                    "role": "user",
                    "content": [{"type": "text", "text": content}],
                })

    # Build current user message
    if user_message:
        user_text = user_message

    if user_text:
        content_parts.append({"type": "text", "text": user_text})

    if not content_parts:
        logger.warning("egov: no content to send")
        return ""

    # Prepend system prompt
    if system_prompt.strip():
        for i, part in enumerate(content_parts):
            if part.get("type") == "text":
                content_parts[i] = {
                    "type": "text",
                    "text": f"[System Instructions]\n{system_prompt.strip()}\n\n{part['text']}",
                }
                break
        else:
            content_parts.insert(0, {"type": "text", "text": f"[System Instructions]\n{system_prompt.strip()}"})

    user_msg = {"role": "user", "content": content_parts}

    # Build request body
    body = json.dumps([resolved_scope, model_id, session_id, user_msg, conversation_history])

    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Next-Action": CHAT_ACTION_HASH,
        "Accept": "text/x-component",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Origin": EGOV_BASE_URL,
        "Referer": f"{EGOV_BASE_URL}/chat?model={model_id}&scope={resolved_scope}",
    }

    try:
        resp = requests.post(
            f"{EGOV_BASE_URL}/chat?model={model_id}&scope={resolved_scope}",
            data=body.encode("utf-8"),
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as e:
        logger.error("egov: chat transport error: %s", e)
        return ""

    resp.encoding = "utf-8"

    if resp.status_code != 200:
        logger.error("egov: chat HTTP %d: %s", resp.status_code, resp.text[:300])
        return ""

    text = parse_rsc_stream(resp.text)
    if not text.strip():
        logger.warning("egov: empty response from model %s scope %s", model_id, resolved_scope)
    return text


# ========================= Streaming Chat =========================

def stream_chat(
    user_message: str,
    model: str = "AI1",
    scope: str = None,
    history: list = None,
    system_prompt: str = "",
    timeout: int = REQUEST_TIMEOUT,
):
    """
    Send a chat message and yield SSE-style chunks.

    Each yielded item is one of:
        {'type': 'content', 'text': '...'}      — a token of assistant text
        {'type': 'done',   'finishReason': 'stop'}
        {'type': 'error',  'message': '...', 'status': int}
    """
    if history is None:
        history = []

    resolved_scope, model_id = resolve_scope_and_model(model)
    if scope:
        resolved_scope = scope
    session_id = secrets.token_hex(16)

    # Build content parts (same logic as chat())
    content_parts = []
    conversation_history = []
    user_text = ""

    for i, msg in enumerate(history):
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif item.get("type") == "image_url":
                        url = item.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        if url:
                            content_parts.append({"type": "image", "image": url})
            content = "\n".join(text_parts)

        if not content:
            continue

        if role == "system":
            system_prompt = (system_prompt + "\n" + content).strip()
        elif role == "assistant":
            conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": content}],
            })
        else:
            if i == len(history) - 1:
                user_text = content
            else:
                conversation_history.append({
                    "role": "user",
                    "content": [{"type": "text", "text": content}],
                })

    if user_message:
        user_text = user_message
    if user_text:
        content_parts.append({"type": "text", "text": user_text})

    if not content_parts:
        yield {"type": "error", "message": "No content to send", "status": 400}
        return

    if system_prompt.strip():
        for i, part in enumerate(content_parts):
            if part.get("type") == "text":
                content_parts[i] = {
                    "type": "text",
                    "text": f"[System Instructions]\n{system_prompt.strip()}\n\n{part['text']}",
                }
                break
        else:
            content_parts.insert(0, {"type": "text", "text": f"[System Instructions]\n{system_prompt.strip()}"})

    user_msg = {"role": "user", "content": content_parts}
    body = json.dumps([resolved_scope, model_id, session_id, user_msg, conversation_history])

    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Next-Action": CHAT_ACTION_HASH,
        "Accept": "text/x-component",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Origin": EGOV_BASE_URL,
        "Referer": f"{EGOV_BASE_URL}/chat?model={model_id}&scope={resolved_scope}",
    }

    try:
        resp = requests.post(
            f"{EGOV_BASE_URL}/chat?model={model_id}&scope={resolved_scope}",
            data=body.encode("utf-8"),
            headers=headers,
            stream=True,
            timeout=timeout,
        )
    except requests.RequestException as e:
        yield {"type": "error", "message": f"Transport error: {e}", "status": 0}
        return

    resp.encoding = "utf-8"

    if resp.status_code != 200:
        body_text = ""
        try:
            body_text = resp.text[:500]
        except Exception:
            pass
        yield {
            "type": "error",
            "message": f"HTTP {resp.status_code}: {body_text}",
            "status": resp.status_code,
        }
        return

    # Parse RSC stream in real-time
    accumulated = ""
    try:
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line:
                continue

            colon_idx = line.find(":")
            if colon_idx < 0:
                continue

            payload = line[colon_idx + 1:]
            if not payload or payload.startswith('"$'):
                continue

            try:
                data = json.loads(payload)
            except (json.JSONDecodeError, ValueError):
                continue

            if not isinstance(data, dict):
                continue

            if "curr" in data:
                curr_text = data.get("curr", "")
                if curr_text:
                    new_text = accumulated + curr_text
                    delta = new_text[len(accumulated):]
                    accumulated = new_text
                    if delta:
                        yield {"type": "content", "text": delta}

    except Exception as e:
        logger.exception("egov: stream error: %s", e)
        yield {"type": "error", "message": f"Stream error: {e}", "status": 0}
        return
    finally:
        try:
            resp.close()
        except Exception:
            pass

    yield {"type": "done", "finishReason": "stop"}


# ========================= File Upload =========================

def upload_file(file_path: str, model: str = "AI1", timeout: int = UPLOAD_TIMEOUT):
    """
    Upload a file to eGov's GCS bucket via the Next.js server action.

    Returns file_data dict with: filename, original_filename, mime_type, cdnUrl
    or None on failure.
    """
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_data = f.read()

    boundary = secrets.token_hex(16)

    body = b""
    body += f"------{boundary}\r\nContent-Disposition: form-data; name=\"0\"\r\n\r\n[\"$K1\"]\r\n".encode()
    body += f"------{boundary}\r\nContent-Disposition: form-data; name=\"1_files\"; filename=\"{filename}\"\r\nContent-Type: {mime_type}\r\n\r\n".encode()
    body += file_data
    body += f"\r\n------{boundary}\r\nContent-Disposition: form-data; name=\"1_model\"\r\n\r\n{model}\r\n".encode()
    body += f"------{boundary}--\r\n".encode()

    headers = {
        "Next-Action": UPLOAD_ACTION_HASH,
        "Accept": "text/x-component",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Origin": EGOV_BASE_URL,
        "Referer": f"{EGOV_BASE_URL}/chat?model={model}&scope=global",
        "Content-Type": f"multipart/form-data; boundary=----{boundary}",
    }

    try:
        resp = requests.post(
            f"{EGOV_BASE_URL}/chat?model={model}&scope=global",
            data=body,
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as e:
        logger.error("egov: upload transport error: %s", e)
        return None

    resp.encoding = "utf-8"

    if resp.status_code != 200:
        logger.warning("egov: upload failed with status %d: %s", resp.status_code, resp.text[:500])
        return None

    # Parse RSC response for file data
    for line in resp.text.split("\n"):
        line = line.strip()
        if not line:
            continue
        colon_idx = line.find(":")
        if colon_idx < 0:
            continue
        payload = line[colon_idx + 1:]
        if not payload:
            continue
        try:
            data = json.loads(payload)
            if isinstance(data, dict) and "file_data" in data:
                return data["file_data"]
            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    if isinstance(item, dict) and "file_data" in item:
                        return item["file_data"]
        except (json.JSONDecodeError, ValueError):
            continue

    logger.warning("egov: upload returned 200 but no file_data in response: %s", resp.text[:500])
    return None


def upload_file_from_bytes(filename: str, file_data: bytes, model: str = "AI1", timeout: int = UPLOAD_TIMEOUT):
    """
    Upload file bytes to eGov's GCS bucket. Returns file_data dict or None.
    """
    mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    boundary = secrets.token_hex(16)

    body = b""
    body += f"------{boundary}\r\nContent-Disposition: form-data; name=\"0\"\r\n\r\n[\"$K1\"]\r\n".encode()
    body += f"------{boundary}\r\nContent-Disposition: form-data; name=\"1_files\"; filename=\"{filename}\"\r\nContent-Type: {mime_type}\r\n\r\n".encode()
    body += file_data
    body += f"\r\n------{boundary}\r\nContent-Disposition: form-data; name=\"1_model\"\r\n\r\n{model}\r\n".encode()
    body += f"------{boundary}--\r\n".encode()

    headers = {
        "Next-Action": UPLOAD_ACTION_HASH,
        "Accept": "text/x-component",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Origin": EGOV_BASE_URL,
        "Referer": f"{EGOV_BASE_URL}/chat?model={model}&scope=global",
        "Content-Type": f"multipart/form-data; boundary=----{boundary}",
    }

    try:
        resp = requests.post(
            f"{EGOV_BASE_URL}/chat?model={model}&scope=global",
            data=body,
            headers=headers,
            timeout=timeout,
        )
    except requests.RequestException as e:
        logger.error("egov: upload transport error: %s", e)
        return None

    resp.encoding = "utf-8"

    if resp.status_code != 200:
        logger.warning("egov: upload failed with status %d: %s", resp.status_code, resp.text[:500])
        return None

    for line in resp.text.split("\n"):
        line = line.strip()
        if not line:
            continue
        colon_idx = line.find(":")
        if colon_idx < 0:
            continue
        payload = line[colon_idx + 1:]
        if not payload:
            continue
        try:
            data = json.loads(payload)
            if isinstance(data, dict) and "file_data" in data:
                return data["file_data"]
            if isinstance(data, list) and len(data) > 0:
                for item in data:
                    if isinstance(item, dict) and "file_data" in item:
                        return item["file_data"]
        except (json.JSONDecodeError, ValueError):
            continue

    logger.warning("egov: upload returned 200 but no file_data in response: %s", resp.text[:500])
    return None


# ========================= Model list =========================

def get_models():
    """Return the list of available eGov models."""
    return [
        {"id": "AI1", "name": "eGov AI1 (Global)", "scope": "global",
         "capabilities": {"vision": True, "pdf": True, "reasoning": False}},
        {"id": "AI1-ph", "name": "eGov AI1 (Philippines/Juan)", "scope": "ph",
         "capabilities": {"vision": True, "pdf": True, "reasoning": False}},
        {"id": "AI2", "name": "eGov AI2 (Global)", "scope": "global",
         "capabilities": {"vision": True, "pdf": False, "reasoning": False}},
        {"id": "AI2-ph", "name": "eGov AI2 (Philippines)", "scope": "ph",
         "capabilities": {"vision": True, "pdf": False, "reasoning": False}},
    ]


# ========================= Simple one-shot chat (for the bot) =========================

def simple_chat(user_message: str, model: str = "AI1", system_prompt: str = "",
                max_tokens: int = 500, timeout: int = 60):
    """Convenience wrapper for the Neby bot — send one message, return full text (or None)."""
    result = chat(
        user_message=user_message,
        model=model,
        system_prompt=system_prompt,
        timeout=timeout,
    )
    if not result:
        return None
    out = result.strip()[:max_tokens * 4]
    logger.info("egov.simple_chat: model=%s reply_chars=%d", model, len(out))
    return out or None


# ========================= Self-test =========================

if __name__ == '__main__':
    import sys
    print("== eGov proxy self-test ==")
    for m in get_models():
        print(f"  {m['id']}: {m['name']} (scope={m['scope']})")
    print()
    print("Testing AI1 (global)...")
    result = chat("What is 2+2? Answer briefly.", model="AI1")
    print(f"  Response: {result[:200]}")
    print()
    print("Testing AI1-ph (Philippines)...")
    result = chat("What is the capital of the Philippines?", model="AI1-ph")
    print(f"  Response: {result[:200]}")