"""Proxy for chat.inceptionlabs.ai (Inception Mercury 2 diffusion LLM)."""
import json
import logging
import threading
import time
import uuid
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

INCEPTION_URL = "https://chat.inceptionlabs.ai"
SESSION_URL = f"{INCEPTION_URL}/api/session"
CHAT_URL = f"{INCEPTION_URL}/api/chat"
VOICE_CONFIG_URL = f"{INCEPTION_URL}/api/voice/config"
STT_URL = f"{INCEPTION_URL}/api/stt"
TTS_URL = f"{INCEPTION_URL}/api/tts"
VOICE_TURN_URL = f"{INCEPTION_URL}/api/voice/turn"
VOICE_EXTRACT_URL = f"{INCEPTION_URL}/api/voice/extract"
REQUEST_TIMEOUT = 180

MODELS = [
    {"id": "mercury-2", "name": "Mercury 2", "reasoning": True, "reasoning_levels": ["low", "medium", "high"], "web_search": True},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_BROWSER_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": INCEPTION_URL,
    "referer": f"{INCEPTION_URL}/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

_SESSION_TOKEN: Optional[str] = None
_SESSION_EXPIRES: float = 0
_SESSION_LOCK = threading.Lock()


def _make_id() -> str:
    return uuid.uuid4().hex[:16]


def _ensure_session() -> str:
    global _SESSION_TOKEN, _SESSION_EXPIRES

    now = time.time()
    if _SESSION_TOKEN and _SESSION_EXPIRES > now + 60:
        return _SESSION_TOKEN

    with _SESSION_LOCK:
        now = time.time()
        if _SESSION_TOKEN and _SESSION_EXPIRES > now + 60:
            return _SESSION_TOKEN

        with CurlSession(headers=_BROWSER_HEADERS, impersonate="chrome") as session:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    resp = session.get(SESSION_URL, timeout=15)
                except Exception as exc:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise RuntimeError(f"Inception session failed: {exc}")

                if resp.status_code == 429 and attempt < max_retries - 1:
                    retry_after = int(resp.headers.get("retry-after", 2 ** attempt))
                    logger.warning("Inception rate-limited (429), retrying in %ds", retry_after)
                    time.sleep(retry_after)
                    continue

                if resp.status_code != 200:
                    raise RuntimeError(f"Inception session failed: HTTP {resp.status_code}")

                data = resp.json()
                token = data.get("token", "")
                if not token:
                    raise RuntimeError(f"Inception session returned no token: {data}")
                _SESSION_TOKEN = token
                _SESSION_EXPIRES = now + 3600
                logger.info("Inception: new session token obtained")
                return token

        raise RuntimeError("Inception session failed: exhausted retries")


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": False,
                "thinking": m.get("reasoning", False),
                "reasoning_levels": m.get("reasoning_levels", []),
                "tools": False,
                "web_search": m.get("web_search", False),
            },
        }
        for m in MODELS
    ]


def _messages_to_inception(messages: List[Dict[str, str]]) -> list:
    result = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, list):
            parts = [{"type": b.get("type", "text"), "text": b.get(b.get("type", "text"), b.get("text", ""))} for b in content]
        else:
            parts = [{"type": "text", "text": str(content)}]
        result.append({"parts": parts, "id": _make_id(), "role": role})
    return result


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "mercury-2",
    reasoning_effort: str = "high",
    web_search: bool = False,
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    try:
        token = _ensure_session()
    except RuntimeError as e:
        yield {"type": "error", "error": str(e)}
        return

    inception_msgs = _messages_to_inception(messages)

    payload = {
        "reasoningEffort": reasoning_effort,
        "webSearchEnabled": web_search,
        "voiceMode": False,
        "timezone": "UTC",
        "id": _make_id(),
        "messages": inception_msgs,
        "trigger": "submit-message",
    }

    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"

    try:
        session = CurlSession(headers=headers, impersonate="chrome")
        resp = session.post(
            CHAT_URL,
            json=payload,
            stream=True,
            timeout=REQUEST_TIMEOUT,
        )
    except Exception as exc:
        yield {"type": "error", "error": f"request failed: {exc}"}
        return

    if resp.status_code == 403:
        with _SESSION_LOCK:
            global _SESSION_TOKEN
            _SESSION_TOKEN = None
        yield {"type": "error", "error": "Session expired (403). Retrying will refresh."}
        return

    if resp.status_code != 200:
        body = resp.text[:300]
        yield {"type": "error", "error": f"Inception HTTP {resp.status_code}: {body}"}
        return

    buffer = ""
    for chunk_bytes in resp.iter_content():
        if chunk_bytes is None:
            continue
        buffer += chunk_bytes.decode("utf-8", errors="ignore")
        while "\n\n" in buffer:
            event_str, buffer = buffer.split("\n\n", 1)
            event_str = event_str.strip()
            if not event_str:
                continue
            if event_str == "data: [DONE]":
                yield {"type": "done", "finish_reason": "stop"}
                return
            if not event_str.startswith("data: "):
                continue
            try:
                data = json.loads(event_str[6:])
            except (json.JSONDecodeError, ValueError):
                continue
            etype = data.get("type", "")
            if etype == "text-delta":
                delta = data.get("delta", "")
                if delta:
                    yield {"type": "text", "content": delta}

    yield {"type": "done", "finish_reason": "stop"}


def simple_chat(
    user_message: str,
    model: str = "mercury-2",
    system_prompt: str = "",
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
            logger.error("Inception simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None


# ── Voice pipeline — separate STT / TTS for reuse in different products ──

def get_voice_config() -> Optional[Dict]:
    """GET /api/voice/config → {scenarios: [{id, name, extraction, ...}], ...}"""
    try:
        token = _ensure_session()
    except RuntimeError as e:
        logger.error("Voice config no session: %s", e)
        return None
    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"
    # GET needs no content-type json
    headers.pop("content-type", None)
    try:
        with CurlSession(headers=headers, impersonate="chrome") as s:
            r = s.get(VOICE_CONFIG_URL, timeout=15)
            if r.status_code != 200:
                logger.warning("Voice config HTTP %s: %s", r.status_code, r.text[:300])
                return None
            return r.json()
    except Exception as exc:
        logger.warning("Voice config failed: %s", exc)
        return None


def transcribe(audio_bytes: bytes, mime: str = "audio/webm", filename: str = "audio.webm") -> Optional[str]:
    """POST /api/stt — separate STT. Returns transcript text or None.

    Mirrors browser: FormData {file: Blob(audio/webm)} with sessionHeaders().
    Server ignores <1200 bytes (see 39dos: if(e.size<1200)return"").
    Uses CurlMime for curl_cffi (see examples/upload.py).
    """
    if not audio_bytes or len(audio_bytes) < 1200:
        logger.debug("STT: audio too small (%s bytes), skipping", len(audio_bytes) if audio_bytes else 0)
        return ""
    try:
        token = _ensure_session()
    except RuntimeError as e:
        logger.error("STT no session: %s", e)
        return None
    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"
    headers.pop("content-type", None)
    try:
        import curl_cffi
        mp = curl_cffi.CurlMime()
        mp.addpart(name="file", content_type=mime, filename=filename, data=audio_bytes)
        with CurlSession(headers=headers, impersonate="chrome") as s:
            r = s.post(STT_URL, multipart=mp, timeout=30)
        mp.close()
        if r.status_code != 200:
            logger.warning("STT HTTP %s: %s", r.status_code, r.text[:500])
            return None
        try:
            j = r.json()
        except Exception:
            return None
        text = j.get("text", "")
        if isinstance(text, str):
            return text.strip()
        return None
    except Exception as exc:
        logger.warning("STT failed: %s", exc)
        return None


def synthesize(text: str) -> Optional[bytes]:
    """POST /api/tts — separate TTS. Returns audio/mpeg bytes or None.

    Mirrors browser: fetch("/api/tts", {method:"POST", body: JSON.stringify({text: t.slice(0,5e3)})})
    Streams audio/mpeg; we buffer fully here. Use stream_synthesize for streaming.
    """
    if not text or not text.strip():
        return None
    text = text.strip()[:5000]
    try:
        token = _ensure_session()
    except RuntimeError as e:
        logger.error("TTS no session: %s", e)
        return None
    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"
    try:
        with CurlSession(headers=headers, impersonate="chrome") as s:
            r = s.post(TTS_URL, json={"text": text}, timeout=60)
            if r.status_code != 200:
                logger.warning("TTS HTTP %s: %s", r.status_code, r.text[:300])
                return None
            ctype = r.headers.get("content-type", "")
            if "audio" not in ctype and "octet" not in ctype:
                logger.debug("TTS non-audio ctype %s", ctype)
            return r.content
    except Exception as exc:
        logger.warning("TTS failed: %s", exc)
        return None


def stream_synthesize(text: str) -> Generator[bytes, None, None]:
    """Streaming TTS — yields audio chunks (mp3) as they arrive. For low-latency playback."""
    if not text or not text.strip():
        return
        yield  # make it a generator
    text = text.strip()[:5000]
    try:
        token = _ensure_session()
    except RuntimeError as e:
        logger.error("TTS stream no session: %s", e)
        return
    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"
    try:
        session = CurlSession(headers=headers, impersonate="chrome")
        resp = session.post(TTS_URL, json={"text": text}, stream=True, timeout=60)
        if resp.status_code != 200:
            logger.warning("TTS stream HTTP %s", resp.status_code)
            return
        for chunk in resp.iter_content(chunk_size=4096):
            if chunk:
                yield chunk
    except Exception as exc:
        logger.warning("TTS stream failed: %s", exc)
        return


def voice_extract(scenario_id: str, messages: List[Dict]) -> Optional[Dict]:
    """POST /api/voice/extract — scenario field extraction.

    Used by voice playground to extract structured fields (e.g. name, intent) from conversation.
    Body: {scenarioId, messages: [{role, content}]}
    Returns: {fields: {...}, ms: ...}
    """
    try:
        token = _ensure_session()
    except RuntimeError as e:
        logger.error("Voice extract no session: %s", e)
        return None
    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"
    try:
        with CurlSession(headers=headers, impersonate="chrome") as s:
            r = s.post(VOICE_EXTRACT_URL, json={"scenarioId": scenario_id, "messages": messages}, timeout=30)
            if r.status_code != 200:
                logger.debug("Voice extract HTTP %s: %s", r.status_code, r.text[:300])
                return None
            return r.json()
    except Exception as exc:
        logger.debug("Voice extract failed: %s", exc)
        return None


def voice_turn(
    messages: List[Dict[str, str]],
    scenario_id: Optional[str] = None,
    business_done: bool = False,
    timezone: str = "UTC",
) -> Generator[Dict, None, None]:
    """POST /api/voice/turn — full voice pipeline with tool streaming.

    Streams NDJSON: {t:"delta", d:"text"} | {t:"retract"} | {t:"tool_start", name, args, ms} | {t:"tool_end", ...}
    Note: voice/turn uses plain NDJSON (no `data: ` prefix), unlike chat which uses SSE.
    Audio is delivered via parallel TTS streaming (see synthesize). This generator yields text deltas and tool events.
    For audio, consume the text deltas and call stream_synthesize incrementally (mirrors browser's E player).
    """
    try:
        token = _ensure_session()
    except RuntimeError as e:
        yield {"type": "error", "error": str(e)}
        return
    # Resolve default scenario if not given
    if not scenario_id:
        cfg = get_voice_config()
        if cfg and cfg.get("scenarios"):
            scenario_id = cfg["scenarios"][0].get("id", "")
        if not scenario_id:
            yield {"type": "error", "error": "No scenario available"}
            return
    # Voice API expects messages as [{role, content}] with role "user"/"assistant"
    inception_msgs = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in messages]
    payload = {
        "scenarioId": scenario_id,
        "messages": inception_msgs,
        "businessDone": business_done,
        "timezone": timezone,
    }
    headers = dict(_BROWSER_HEADERS)
    headers["x-session-token"] = token
    headers["cookie"] = f"session={token}"
    try:
        session = CurlSession(headers=headers, impersonate="chrome")
        resp = session.post(VOICE_TURN_URL, json=payload, stream=True, timeout=REQUEST_TIMEOUT)
    except Exception as exc:
        yield {"type": "error", "error": f"voice turn request failed: {exc}"}
        return
    if resp.status_code != 200:
        try:
            body = resp.text[:500]
        except Exception:
            body = ""
        yield {"type": "error", "error": f"Voice turn HTTP {resp.status_code}: {body}"}
        return
    buf = ""
    for chunk_bytes in resp.iter_content():
        if chunk_bytes is None:
            continue
        try:
            buf += chunk_bytes.decode("utf-8", errors="ignore")
        except Exception:
            continue
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            line = line.strip()
            if not line:
                continue
            # Voice turn uses NDJSON without SSE prefix; but also handle SSE if present
            if line == "data: [DONE]" or line == "[DONE]":
                yield {"type": "done", "finish_reason": "stop"}
                return
            if line.startswith("data: "):
                line = line[6:].strip()
                if line == "[DONE]":
                    yield {"type": "done", "finish_reason": "stop"}
                    return
            try:
                data = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            t = data.get("t", "")
            if t == "delta" and isinstance(data.get("d"), str):
                yield {"type": "text", "content": data["d"]}
            elif t == "retract":
                yield {"type": "retract"}
            elif t == "tool_start":
                yield {"type": "tool_start", "name": data.get("name"), "args": data.get("args"), "ms": data.get("ms")}
            elif t == "tool_end":
                yield {"type": "tool_end", "name": data.get("name"), "args": data.get("args"), "result": data.get("result"), "ms": data.get("ms")}
            elif "error" in data:
                yield {"type": "error", "error": str(data["error"])}
    # Fallback if stream ended without DONE
    yield {"type": "done", "finish_reason": "stop"}
