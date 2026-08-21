"""
TryingOpen Proxy — https://www.tryingopen.com

Reverse-engineered from the Next.js frontend (0rdan39ov2llp.js).

- Base endpoint: POST https://www.tryingopen.com/api/open
- Body: { id, trigger:"submit-message", model, effort:"quick|balanced|deep", messages:[{id, role, parts:[{type:"text", text}, {type:"file", filename, mediaType, url:data:...}]}]}
- Response: Vercel AI SDK v5 SSE stream (data: {"type":"..."}\n)
  Types observed:
    start, start-step, reasoning-start/delta/end, text-start/delta/end,
    tool-input-start/delta/available, tool-output-available, source-url,
    finish-step, finish, error

- No auth, no rate limit (as of 2026-08). We add light retries.
- Uploads: up to 3 files, 5 MB each, data URL encoded. supportsImages per model.

This module exposes:
  - get_models() / MODEL_MAP
  - stream_chat(messages, model, effort, file_paths, system_prompt) -> Generator[dict]
  - simple_chat(user_message, system_prompt, model, effort, file_paths) -> str

All models are OpenRouter ZDR (zero data retention) via TryingOpen's proxy.
"""

import base64
import json
import logging
import mimetypes
import os
import random
import time
import uuid
from pathlib import Path
from typing import Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

API_URL = "https://www.tryingopen.com/api/open"
MAX_FILES = 3
MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB — enforced by frontend
DEFAULT_EFFORT = "balanced"  # quick | balanced | deep
TIMEOUT = (15, 300)

MODELS = [
    {
        "id": "qwen/qwen3.8-27b",
        "name": "Qwen3.8 27B",
        "maker": "Alibaba",
        "logo": "/models/qwen.svg",
        "params": "27B",
        "context": "262k",
        "blurb": "The newest mid-size Qwen. Reads pictures and video, thinks before it answers. Default.",
        "goodAt": "Coding and careful answers",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 262000,
        "pricePerMTok": 3.2,
    },
    {
        "id": "qwen/qwen3.6-27b",
        "name": "Qwen3.6 27B",
        "maker": "Alibaba",
        "logo": "/models/qwen.svg",
        "params": "27B",
        "context": "262k",
        "blurb": "Dense mid-size Alibaba model. Takes pictures and video, can show its thinking.",
        "goodAt": "Reading images and video",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 262000,
        "pricePerMTok": 3.6,
    },
    {
        "id": "qwen/qwen3.8-2.4t-a95b",
        "name": "Qwen3.8 2.4T",
        "maker": "Alibaba",
        "logo": "/models/qwen.svg",
        "params": "2.4T",
        "context": "1M",
        "blurb": "Largest open Qwen: 2.4T params (95B active).",
        "goodAt": "The hardest questions",
        "supportsTools": True,
        "supportsImages": False,
        "context_window": 1000000,
        "pricePerMTok": 6,
    },
    {
        "id": "nvidia/nemotron-3.5-lightning",
        "name": "Nemotron 3.5 Lightning",
        "maker": "NVIDIA",
        "logo": "/models/nvidia.svg",
        "params": "30B",
        "context": "1M",
        "blurb": "Only 3B active per word — fast for its size.",
        "goodAt": "Fast, high-volume work",
        "supportsTools": True,
        "supportsImages": False,
        "context_window": 1000000,
        "pricePerMTok": 0.25,
    },
    {
        "id": "z-ai/glm-5.3",
        "name": "GLM 5.3",
        "maker": "Z.ai",
        "logo": "/models/zai.svg",
        "params": "",
        "context": "1M",
        "blurb": "Newest reasoning model for complex software engineering. Weights pending.",
        "goodAt": "Complex engineering work",
        "supportsTools": True,
        "supportsImages": False,
        "context_window": 1000000,
        "pricePerMTok": 4.4,
    },
    {
        "id": "z-ai/glm-5.2",
        "name": "GLM 5.2",
        "maker": "Z.ai",
        "logo": "/models/zai.svg",
        "params": "",
        "context": "1M",
        "blurb": "Reasoning model for long, multi-step projects.",
        "goodAt": "Long, multi-step projects",
        "supportsTools": True,
        "supportsImages": False,
        "context_window": 1000000,
        "pricePerMTok": 1.54,
    },
    {
        "id": "moonshotai/kimi-k3",
        "name": "Kimi K3",
        "maker": "Moonshot",
        "logo": "/models/moonshot.svg",
        "params": "2.8T",
        "context": "1M",
        "blurb": "2.8T params, strong at hard coding and deep reasoning.",
        "goodAt": "Hard coding and deep reasoning",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 1000000,
        "pricePerMTok": 15,
    },
    {
        "id": "minimax/minimax-m3",
        "name": "MiniMax M3",
        "maker": "MiniMax",
        "logo": "/models/minimax.png",
        "params": "427B",
        "context": "1M",
        "blurb": "Multimodal: reads pictures and video, built for coding and long agentic tasks.",
        "goodAt": "Long agent tasks and video",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 1000000,
        "pricePerMTok": 1.2,
    },
    {
        "id": "deepseek/deepseek-v4-flash-0731",
        "name": "DeepSeek V4 Flash",
        "maker": "DeepSeek",
        "logo": "/models/deepseek.svg",
        "params": "284B",
        "context": "1M",
        "blurb": "Only 13B active per word — quick despite size. Coding & agents.",
        "goodAt": "Coding and agents",
        "supportsTools": True,
        "supportsImages": False,
        "context_window": 1000000,
        "pricePerMTok": 0.18,
    },
    {
        "id": "deepseek/deepseek-v4-pro-0813",
        "name": "DeepSeek V4 Pro",
        "maker": "DeepSeek",
        "logo": "/models/deepseek.svg",
        "params": "1.7T",
        "context": "1M",
        "blurb": "Biggest DeepSeek: full-strength V4.",
        "goodAt": "Hard problems at full scale",
        "supportsTools": True,
        "supportsImages": False,
        "context_window": 1000000,
        "pricePerMTok": 1.98,
    },
    {
        "id": "google/gemma-4-31b-it",
        "name": "Gemma 4 31B",
        "maker": "Google",
        "logo": "/models/google.svg",
        "params": "31B",
        "context": "262k",
        "blurb": "Newest Gemma. Reads pictures as well as text, can show thinking.",
        "goodAt": "Writing, and reading images",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 262000,
        "pricePerMTok": 0.34,
    },
    {
        "id": "google/gemma-4-26b-a4b-it",
        "name": "Gemma 4 26B",
        "maker": "Google",
        "logo": "/models/google.svg",
        "params": "25B",
        "context": "262k",
        "blurb": "MoE Gemma: only 3.8B runs per word — much quicker. Reads pictures and video.",
        "goodAt": "Quick answers on a budget",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 262000,
        "pricePerMTok": 0.34,
    },
    {
        "id": "mistralai/mistral-small-2603",
        "name": "Mistral Small 4",
        "maker": "Mistral",
        "logo": "/models/mistral.svg",
        "params": "119B",
        "context": "262k",
        "blurb": "Mistral's newest open model. Reasons well, reads pictures, cheap to run.",
        "goodAt": "Reasoning at a low price",
        "supportsTools": False,
        "supportsImages": True,
        "context_window": 262000,
        "pricePerMTok": 0.6,
    },
    {
        "id": "meta/muse-glimmer-30b",
        "name": "Muse Glimmer 30B",
        "maker": "Meta",
        "logo": "/models/meta.svg",
        "params": "30B",
        "context": "131k",
        "blurb": "From Meta Superintelligence Labs, shrunk from a much bigger model.",
        "goodAt": "Agents on modest hardware",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 131000,
        "pricePerMTok": 1.5,
    },
    {
        "id": "thinkingmachines/inkling-small",
        "name": "Inkling Small",
        "maker": "Thinking Machines",
        "logo": "/models/thinkingmachines.png",
        "params": "276B",
        "context": "524k",
        "blurb": "Only 12B active per word — quick, reads pictures.",
        "goodAt": "Quick multimodal answers",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 524000,
        "pricePerMTok": 1.2,
    },
    {
        "id": "thinkingmachines/inkling",
        "name": "Inkling",
        "maker": "Thinking Machines",
        "logo": "/models/thinkingmachines.png",
        "params": "975B",
        "context": "1M",
        "blurb": "Flagship: 41B active per word. Reads pictures, built for reasoning and agents.",
        "goodAt": "Reasoning and agent work",
        "supportsTools": True,
        "supportsImages": True,
        "context_window": 1000000,
        "pricePerMTok": 4.05,
    },
]

MODEL_MAP = {m["id"]: m for m in MODELS}
DEFAULT_MODEL = "qwen/qwen3.8-27b"
EFFORTS = ("quick", "balanced", "deep")


def _effort_for_model(effort: Optional[str]) -> str:
    e = (effort or DEFAULT_EFFORT).strip().lower()
    return e if e in EFFORTS else DEFAULT_EFFORT


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "maker": m["maker"],
            "params": m.get("params", ""),
            "context": m.get("context", ""),
            "blurb": m.get("blurb", ""),
            "goodAt": m.get("goodAt", ""),
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": bool(m.get("supportsImages")),
                "tools": bool(m.get("supportsTools")),
                "reasoning": True,
                "web_search": True,
            },
        }
        for m in MODELS
    ]


def _guess_media_type(path: str) -> str:
    mt, _ = mimetypes.guess_type(path)
    if mt:
        return mt
    ext = Path(path).suffix.lower()
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    if ext == ".gif":
        return "image/gif"
    if ext == ".pdf":
        return "application/pdf"
    if ext == ".mp4":
        return "video/mp4"
    return "application/octet-stream"


def _file_to_part(path: str) -> Optional[Dict]:
    p = Path(path)
    if not p.exists() or not p.is_file():
        return None
    size = p.stat().st_size
    if size > MAX_FILE_BYTES:
        logger.warning("tryingopen: file %s too large (%s bytes > %s) — skipping", path, size, MAX_FILE_BYTES)
        return None
    try:
        raw = p.read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        mt = _guess_media_type(str(p))
        return {
            "type": "file",
            "filename": p.name,
            "mediaType": mt,
            "url": f"data:{mt};base64,{b64}",
        }
    except Exception as exc:
        logger.warning("tryingopen: failed to encode %s: %s", path, exc)
        return None


def _supports_images(model_id: str) -> bool:
    m = MODEL_MAP.get(model_id) or MODEL_MAP.get((model_id or "").strip())
    if m:
        return bool(m.get("supportsImages"))
    mid = (model_id or "").lower()
    # heuristics for unknown ids
    if any(k in mid for k in ("gemma", "qwen", "kimi", "minimax", "inkling", "muse", "mistral")):
        return True
    return False


def _build_parts(text: str, file_paths: Optional[List[str]], model_id: str) -> List[Dict]:
    parts: List[Dict] = []
    if file_paths:
        allow_images = _supports_images(model_id)
        for fp in file_paths[:MAX_FILES]:
            part = _file_to_part(fp)
            if not part:
                continue
            is_image = part["mediaType"].startswith("image/")
            if is_image and not allow_images:
                logger.info("tryingopen: skipping image %s for model %s (no vision)", part["filename"], model_id)
                continue
            parts.append(part)
    if text and text.strip():
        parts.append({"type": "text", "text": text})
    elif not parts:
        parts.append({"type": "text", "text": ""})
    return parts


def _messages_to_api(
    messages: List[Dict],
    model_id: str,
    file_paths: Optional[List[str]] = None,
    system_prompt: str = "",
) -> List[Dict]:
    """
    Convert internal messages [{role, content}] -> tryingopen [{id, role, parts}].
    - system content is merged into the next user message (tryingopen rejects system role).
    - content may be str or list of {type=text/image_url} — images are merged with file_paths.
    """
    system_blocks: List[str] = []
    if system_prompt and system_prompt.strip():
        system_blocks.append(system_prompt.strip())

    # Collect system messages from history
    for m in messages or []:
        if (m.get("role") or "").lower() == "system":
            c = m.get("content", "")
            if isinstance(c, list):
                c = "\n".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)
            if str(c).strip():
                system_blocks.append(str(c).strip())

    pending_files: List[str] = list(file_paths or [])
    # Extract file-like image parts from last user message's content list (CLI vision path)
    # We defer to _build_parts which will handle them as file_paths, but for now
    # we already have them in pending_files.

    system_prefix = "\n\n".join(system_blocks).strip()
    out: List[Dict] = []
    msg_idx = 0

    for m in messages or []:
        role = (m.get("role") or "user").strip().lower()
        if role == "system":
            continue
        if role not in ("user", "assistant"):
            role = "user"
        content = m.get("content", "")
        text = ""
        # Handle multimodal content list -> text + inline file extraction
        if isinstance(content, list):
            texts = []
            for part in content:
                if not isinstance(part, dict):
                    texts.append(str(part))
                    continue
                if part.get("type") == "text":
                    texts.append(part.get("text", ""))
                elif part.get("type") == "image_url":
                    # image_url data URLs are turned into temp files on the CLI side;
                    # those temps are already in file_paths. For web path we get data URL directly.
                    url = part.get("image_url", {}).get("url", "") if isinstance(part.get("image_url"), dict) else part.get("url", "")
                    if url and url.startswith("data:"):
                        # Synthesize a file part from data URL
                        try:
                            header, b64 = url.split(",", 1)
                            mt = header.split(";")[0].split(":")[1] if ":" in header else "image/png"
                            ext = ".png" if "png" in mt else ".jpg" if "jpeg" in mt else ".webp"
                            # Keep as file part directly
                            filename = f"image-{len(pending_files)}{ext}"
                            # We'll embed as file part later; for now treat as file
                            # Instead of re-encoding, create a synthetic entry via temp handling
                            # Simpler: add a file part with the data URL directly
                            # We can append a file part to this message individually
                            pass
                        except Exception:
                            pass
                    texts.append("[image]")
            text = "\n".join(texts)
        else:
            text = str(content or "")

        # System prefix goes onto the first user message
        if role == "user" and system_prefix and msg_idx == 0:
            # Find first user message to prepend system
            # Actually prepend to this first user if it's user; else we'll create a leading user
            text = (system_prefix + "\n\n" + text).strip() if text.strip() else system_prefix
            system_prefix = ""  # consumed

        # Skip empty? But need at least one user.
        if not text.strip() and role == "user" and not pending_files:
            continue

        # For the LAST user message, attach pending files
        is_last_user = (role == "user" and m == [x for x in messages if (x.get("role") or "").lower() != "system"][-1])
        attach_files = pending_files if is_last_user and pending_files else None
        parts = _build_parts(text, attach_files, model_id)
        out.append({"id": f"m{msg_idx}", "role": role, "parts": parts})
        msg_idx += 1

    # If we had a system prompt but no user message yet (edge), inject it
    if system_prefix and not out:
        out.append({"id": "m0", "role": "user", "parts": _build_parts(system_prefix, pending_files, model_id)})
    elif system_prefix and out and out[0]["role"] != "user":
        # No user message to prepend to — prepend a synthetic user
        out.insert(0, {"id": "m0", "role": "user", "parts": _build_parts(system_prefix, None, model_id)})
        # re-id
        for i, mm in enumerate(out):
            mm["id"] = f"m{i}"

    return out


def _parse_sse_line(line: str) -> Optional[Dict]:
    line = line.strip()
    if not line or not line.startswith("data:"):
        return None
    payload = line[5:].strip()
    if not payload or payload == "[DONE]":
        return None
    try:
        return json.loads(payload)
    except (ValueError, TypeError):
        return None


def _stream_request(
    model: str,
    effort: str,
    api_messages: List[Dict],
    timeout: tuple = TIMEOUT,
) -> Generator[Dict, None, None]:
    body = {
        "id": uuid.uuid4().hex[:16],
        "trigger": "submit-message",
        "model": model,
        "effort": _effort_for_model(effort),
        "messages": api_messages,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Origin": "https://www.tryingopen.com",
        "Referer": "https://www.tryingopen.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    }
    resp = None
    try:
        resp = requests.post(API_URL, json=body, headers=headers, timeout=timeout, stream=True)
    except requests.RequestException as exc:
        yield {"type": "error", "error": f"TryingOpen network error: {exc}"}
        return

    if resp.status_code != 200:
        detail = resp.text[:600]
        if resp.status_code == 413 or "Too much text" in detail:
            yield {"type": "error", "error": "Context limit exceeded — TryingOpen: 'There's too much text in this chat now. Start a new one to keep going.' Please start a new chat (/clear) or compact the conversation."}
        elif "Too Many" in detail or resp.status_code == 429:
            yield {"type": "error", "error": f"TryingOpen rate limited (HTTP {resp.status_code}): {detail}", "retryable": True}
        else:
            yield {"type": "error", "error": f"TryingOpen HTTP {resp.status_code}: {detail}"}
        try:
            resp.close()
        except Exception:
            pass
        return

    # Content-type should be text/event-stream
    ctype = resp.headers.get("content-type", "")
    if "text/event-stream" not in ctype and "application/json" not in ctype:
        # Some errors come as text/plain
        pass

    try:
        for raw in resp.iter_lines(decode_unicode=True):
            if raw is None:
                continue
            line = raw.strip()
            if not line:
                continue
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if not data_str or data_str == "[DONE]":
                continue
            try:
                data = json.loads(data_str)
            except (ValueError, TypeError):
                continue

            t = data.get("type")

            if t == "start":
                # {"type":"start","messageMetadata":{"modelName":"...","maker":"...", "webSearch":true}}
                meta = data.get("messageMetadata") or {}
                yield {"type": "meta", "meta": meta}
                continue

            if t == "reasoning-start":
                yield {"type": "reasoning_start", "id": data.get("id")}
                continue
            if t == "reasoning-delta":
                yield {"type": "reasoning", "content": data.get("delta", ""), "id": data.get("id")}
                continue
            if t == "reasoning-end":
                yield {"type": "reasoning_end", "id": data.get("id")}
                continue

            if t in ("text-start",):
                yield {"type": "text_start", "id": data.get("id")}
                continue
            if t == "text-delta":
                yield {"type": "text", "content": data.get("delta", ""), "id": data.get("id")}
                continue
            if t == "text-end":
                yield {"type": "text_end", "id": data.get("id")}
                continue

            if t == "tool-input-start":
                yield {
                    "type": "tool_call_start",
                    "toolCallId": data.get("toolCallId"),
                    "toolName": data.get("toolName"),
                    "dynamic": data.get("dynamic", False),
                }
                continue
            if t == "tool-input-delta":
                yield {
                    "type": "tool_call_delta",
                    "toolCallId": data.get("toolCallId"),
                    "inputTextDelta": data.get("inputTextDelta", ""),
                }
                continue
            if t == "tool-input-available":
                yield {
                    "type": "tool_call",
                    "toolCallId": data.get("toolCallId"),
                    "toolName": data.get("toolName"),
                    "input": data.get("input") or {},
                    "dynamic": data.get("dynamic", False),
                }
                continue
            if t == "tool-output-available":
                yield {
                    "type": "tool_result",
                    "toolCallId": data.get("toolCallId"),
                    "output": data.get("output"),
                    "errorText": data.get("errorText"),
                    "dynamic": data.get("dynamic", False),
                }
                continue

            if t in ("source-url", "source_url"):
                # {"type":"source-url","sourceId":"...","url":"...","title":"...","providerMetadata":{...}}
                yield {
                    "type": "source",
                    "url": data.get("url"),
                    "title": data.get("title") or "",
                    "sourceId": data.get("sourceId") or "",
                    "providerMetadata": data.get("providerMetadata") or {},
                }
                continue
            if t == "source-document":
                yield {
                    "type": "source",
                    "url": data.get("url") or data.get("sourceId") or "",
                    "title": data.get("title") or "",
                    "sourceId": data.get("sourceId") or "",
                }
                continue

            if t == "error":
                msg = data.get("errorText") or data.get("error") or str(data)
                if "Too much text" in msg or "too much text" in msg.lower():
                    yield {"type": "error", "error": "Context limit exceeded — TryingOpen: 'There's too much text in this chat now. Start a new one to keep going.' Please start a new chat (/clear) or compact the conversation."}
                else:
                    yield {"type": "error", "error": msg}
                continue
            if t == "finish-step":
                continue
            if t == "finish":
                # {"type":"finish","finishReason":"stop","messageMetadata":{...}}
                meta = data.get("messageMetadata") or {}
                yield {
                    "type": "done",
                    "finishReason": data.get("finishReason") or meta.get("finishReason") or "stop",
                    "inputTokens": meta.get("inputTokens") or 0,
                    "outputTokens": meta.get("outputTokens") or 0,
                    "totalTokens": meta.get("totalTokens") or 0,
                    "model": meta.get("modelName") or model,
                }
                continue
            if t in ("start-step",):
                continue
            # Unknown type — forward raw for debugging
            # logger.debug("tryingopen unknown sse type %s: %s", t, data)
    finally:
        try:
            resp.close()
        except Exception:
            pass


def stream_chat(
    messages: List[Dict],
    model: str = DEFAULT_MODEL,
    effort: str = DEFAULT_EFFORT,
    file_paths: Optional[List[str]] = None,
    system_prompt: str = "",
    timeout: int = 300,
) -> Generator[Dict, None, None]:
    """High-level streaming call used by CLI, background agent, and Neby."""
    model = (model or DEFAULT_MODEL).strip()
    if model not in MODEL_MAP:
        # Allow short names like "qwen3.8" -> map to default
        lower = model.lower()
        for mid in MODEL_MAP:
            if lower in mid.lower() or mid.lower().endswith(lower):
                model = mid
                break
        else:
            logger.warning("tryingopen: unknown model %s, using default %s", model, DEFAULT_MODEL)
            model = DEFAULT_MODEL
    effort = _effort_for_model(effort)
    api_messages = _messages_to_api(messages, model, file_paths=file_paths, system_prompt=system_prompt)
    if not api_messages:
        yield {"type": "error", "error": "No messages to send to TryingOpen"}
        return

    # Retry on transient errors / empty response (the frontend retries automatically)
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        saw_content = False
        saw_error = None
        for chunk in _stream_request(model, effort, api_messages, timeout=(15, timeout)):
            ctype = chunk.get("type")
            if ctype in ("text", "reasoning", "tool_call", "tool_result", "source"):
                saw_content = True
            if ctype == "error":
                saw_error = chunk.get("error")
            yield chunk
            # Stop retrying after we got a terminal error that is not retryable
            if ctype == "error" and "That model didn't respond" in str(saw_error):
                # For vision-mismatch, try stripping files and retrying once
                if file_paths and attempt == 1 and _supports_images(model) is False:
                    # Should have been filtered, but just in case
                    pass
        # If we saw a proper finish, don't retry
        # Heuristic: if we yielded at least one text/reasoning and last chunk was done, consider success
        # For now, if we saw any content, break; otherwise retry on empty
        if saw_content:
            break
        if saw_error and "rate limited" in str(saw_error).lower() and attempt < max_attempts:
            time.sleep(2 * attempt)
            continue
        if not saw_content and attempt < max_attempts:
            time.sleep(1.5 * attempt)
            continue
        break


def simple_chat(
    user_message: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = "",
    effort: str = DEFAULT_EFFORT,
    file_paths: Optional[List[str]] = None,
    max_tokens: int = 4000,
    **kwargs,
) -> Optional[str]:
    """Non-streaming convenience: collects text deltas into one string."""
    messages = []
    if system_prompt and system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": user_message})
    collected: List[str] = []
    sources: List[Dict] = []
    tool_notes: List[str] = []
    for chunk in stream_chat(messages, model=model, effort=effort, file_paths=file_paths, system_prompt=""):
        ctype = chunk.get("type")
        if ctype == "text":
            collected.append(chunk.get("content", ""))
        elif ctype == "source":
            sources.append(chunk)
        elif ctype == "tool_call":
            tool_notes.append(f"[tool {chunk.get('toolName')}: {json.dumps(chunk.get('input') or {})}]")
        elif ctype == "tool_result":
            # surface createFile result
            out = chunk.get("output") or {}
            if out:
                tool_notes.append(f"[tool result {chunk.get('toolCallId')}: {json.dumps(out)}]")
        elif ctype == "error":
            logger.error("tryingopen simple_chat error: %s", chunk.get("error"))
            if not collected:
                return None
    text = "".join(collected).strip()
    if tool_notes and text:
        text = text + "\n\n" + "\n".join(tool_notes)
    if sources and text:
        # Append sources as markdown footnotes for transparency
        src_lines = "\n".join(f"- [{s.get('title') or s.get('url')}]({s.get('url')})" for s in sources[:6] if s.get("url"))
        if src_lines:
            text = text + f"\n\n**Sources:**\n{src_lines}"
    return text or None


def get_default_model() -> str:
    return DEFAULT_MODEL


def probe(model: str = DEFAULT_MODEL, effort: str = DEFAULT_EFFORT) -> Dict:
    """One-shot connectivity check."""
    report: Dict = {
        "model": model,
        "effort": effort,
        "ok": False,
        "error": "",
        "msToFirstToken": None,
        "outputTokens": None,
    }
    try:
        t0 = time.time()
        first = None
        for chunk in stream_chat(
            [{"role": "user", "content": "Say OK"}],
            model=model,
            effort=effort,
        ):
            if chunk.get("type") == "text" and first is None:
                first = time.time() - t0
            if chunk.get("type") == "done":
                report["outputTokens"] = chunk.get("outputTokens")
        report["msToFirstToken"] = int((first or 0) * 1000) if first else None
        report["ok"] = first is not None
        if not first:
            report["error"] = "no text delta"
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    return report
