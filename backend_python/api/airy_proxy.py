"""
Airy TTS Proxy — https://airy.so (Out of Set Inc.)

Zero-auth, verified 2026-09-18:
  GET  https://api.airy.so/v1/studio/voices          -> 104 unlocked voices (en + ko)
  POST https://api.airy.so/v1/studio/speech          -> raw audio stream
       headers: Content-Type: application/json
                X-Studio-Anonymous-Id: <uuid4>      (REQUIRED — 403 without)
                X-Studio-Activity-Source: generate
       body:   {"model":"airy-tts-v1","input":<text>,"voice":<voice_id>,
                "language":"en|ko","style":"normal|bright|calm|whisper",
                "response_format":"mp3|opus|pcm|wav","speed":0.5..2.0}
       200 headers: x-audio-sample-rate, x-audio-channels,
                    x-audio-sample-format (s16le), x-audio-duration-sec

Hard limits: 640 characters per request, 12 requests/minute per IP.
Long text is therefore split at sentence boundaries and synthesised in
batches. response_format=mp3 returns bare MPEG frame streams (no ID3 tag),
so the batches concatenate byte-for-byte into one playable file.
"""
from __future__ import annotations

import base64
import logging
import re
import threading
import time
import uuid
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE = "https://api.airy.so"
SPEECH_URL = f"{BASE}/v1/studio/speech"
VOICES_URL = f"{BASE}/v1/studio/voices"

MODEL = "airy-tts-v1"
CHAR_LIMIT = 640
CHUNK_TARGET = 638
MAX_CHUNKS = 8
RATE_PER_MIN = 12
MIN_INTERVAL = 60.0 / RATE_PER_MIN + 0.2

STYLES = ("normal", "bright", "calm", "whisper")
LANGS = ("en", "ko")
DEFAULT_VOICE = "a597bb7a98fc9ec1"
# Sentence boundaries pack imperfectly, so the advertised text ceiling sits
# below MAX_CHUNKS * CHUNK_TARGET; anything that still overruns reports it.
MAX_TEXT = 4800

_last_call = 0.0
_pace_lock = threading.Lock()
_voice_cache: List[Dict] = []
_voice_cache_at = 0.0
VOICE_TTL = 6 * 3600

_LATIN_END = ".!?…"
_CJK_END = "。！？"
_CLOSERS = "\"'”’)]）】»"
_WS = re.compile(r"\s+")


def _sentence_ends_here(text: str, i: int) -> Optional[int]:
    """Return the index to resume from if text[i] terminates a sentence."""
    ch = text[i]
    j = i + 1
    while j < len(text) and text[j] in _CLOSERS:
        j += 1
    if ch in _CJK_END:
        return j
    if j >= len(text) or text[j].isspace():
        return j
    return None


def _split_sentences(text: str) -> List[str]:
    text = _WS.sub(" ", text).strip()
    out: List[str] = []
    start = 0
    i = 0
    n = len(text)
    while i < n:
        if text[i] in _LATIN_END or text[i] in _CJK_END:
            resume = _sentence_ends_here(text, i)
            if resume is not None:
                sentence = text[start:resume].strip()
                if sentence:
                    out.append(sentence)
                start = resume
                i = resume
                continue
        i += 1
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return out


def _session():
    try:
        from curl_cffi import requests as creq  # type: ignore

        return creq.Session(impersonate="chrome"), True
    except Exception:
        import requests as req  # type: ignore

        s = req.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"})
        return s, False


def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "X-Studio-Anonymous-Id": str(uuid.uuid4()),
        "X-Studio-Activity-Source": "generate",
        "Referer": "https://airy.so/",
        "Origin": "https://airy.so",
    }


def _pace() -> None:
    """Space outbound calls so a batch stays inside Airy's 12 req/min/IP cap."""
    global _last_call
    with _pace_lock:
        wait = MIN_INTERVAL - (time.time() - _last_call)
        _last_call = time.time() + max(wait, 0.0)
    if wait > 0:
        time.sleep(wait)


def split_chunks(text: str, limit: int = CHUNK_TARGET) -> List[str]:
    """Pack sentences into <=limit chunks, hard-splitting anything oversized."""
    chunks: List[str] = []
    current = ""
    for sentence in _split_sentences(text):
        while len(sentence) > limit:
            head, sentence = _cut(sentence, limit)
            chunks.append(head)
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip()
        if current and len(candidate) > limit:
            chunks.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def _cut(sentence: str, limit: int) -> tuple:
    space = sentence.rfind(" ", 0, limit + 1)
    cut = space if space > limit // 2 else limit
    return sentence[:cut].strip(), sentence[cut:].strip()


def get_voices(refresh: bool = False) -> List[Dict]:
    global _voice_cache, _voice_cache_at
    now = time.time()
    if not refresh and _voice_cache and now - _voice_cache_at < VOICE_TTL:
        return _voice_cache
    sess, _ = _session()
    try:
        r = sess.get(VOICES_URL, headers={"X-Studio-Anonymous-Id": str(uuid.uuid4())}, timeout=(10, 25))
        if r.status_code != 200:
            logger.warning("airy voices %s: %s", r.status_code, r.text[:200])
            return _voice_cache or []
        data = r.json()
    except Exception:
        logger.exception("airy voices fetch failed")
        return _voice_cache or []
    finally:
        try:
            sess.close()
        except Exception:
            pass
    voices = []
    for v in data.get("voices") or []:
        vid = (v.get("id") or "").strip()
        if not vid:
            continue
        previews = v.get("audio_url") or {}
        voices.append({
            "id": vid,
            "name": (v.get("display_name") or vid).strip(),
            "gender": (v.get("gender") or "neutral").strip(),
            "langs": v.get("langs") or ["en"],
            "preview_en": previews.get("en") or "",
            "preview_ko": previews.get("ko") or "",
        })
    if voices:
        _voice_cache = voices
        _voice_cache_at = now
    return voices


def resolve_voice(voice: Optional[str]) -> str:
    wanted = (voice or "").strip()
    if not wanted:
        return DEFAULT_VOICE
    if re.fullmatch(r"[0-9a-f]{8,16}", wanted):
        return wanted
    lowered = wanted.lower()
    for v in get_voices():
        if v["name"].lower() == lowered or v["id"].lower() == lowered:
            return v["id"]
    for v in get_voices():
        if lowered in v["name"].lower():
            return v["id"]
    return DEFAULT_VOICE


def _voice_name(voice_id: str) -> str:
    for v in get_voices():
        if v["id"] == voice_id:
            return v["name"]
    return voice_id


def _request_chunk(sess, text: str, voice_id: str, style: str, speed: float, language: str) -> tuple:
    payload = {
        "model": MODEL,
        "input": text,
        "voice": voice_id,
        "language": language,
        "style": style,
        "response_format": "mp3",
        "speed": speed,
    }
    r = sess.post(SPEECH_URL, json=payload, headers=_headers(), timeout=(15, 120))
    if r.status_code != 200:
        detail = r.text[:300]
        try:
            detail = (r.json().get("error") or {}).get("message") or detail
        except Exception:
            pass
        return None, f"Airy {r.status_code}: {detail}", 0.0
    audio = r.content
    if len(audio) < 512:
        return None, "Airy returned an empty audio stream", 0.0
    try:
        duration = float(r.headers.get("x-audio-duration-sec") or 0)
    except (TypeError, ValueError):
        duration = 0.0
    return audio, None, duration


def synthesize_chunks(text: str, voice_id: str, style: str, speed: float, language: str,
                      on_progress=None) -> Dict:
    chunks = split_chunks(text)
    if not chunks:
        return {"status": "error", "error": "text required"}
    if len(chunks) > MAX_CHUNKS:
        return {"status": "error", "error": f"text too long for Airy — {len(chunks)} batches needed, max {MAX_CHUNKS} (~{MAX_TEXT} chars)"}

    sess, _ = _session()
    pieces: List[bytes] = []
    seconds = 0.0
    try:
        for index, chunk in enumerate(chunks):
            if index:
                _pace()
            audio, error, duration = _request_chunk(sess, chunk, voice_id, style, speed, language)
            if error:
                return {"status": "error", "error": error, "raw": f"batch {index + 1}/{len(chunks)}"}
            pieces.append(audio)
            seconds += duration
            if on_progress:
                try:
                    on_progress(index + 1, len(chunks))
                except Exception:
                    pass
    except Exception as exc:
        logger.exception("airy synthesize failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass

    audio = b"".join(pieces)
    return {"status": "success", "audio": audio, "batches": len(chunks), "duration": round(seconds, 2)}


def generate_tts(text: str, voice: Optional[str] = None, style: str = "normal",
                 speed=1.0, language: str = "en") -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = _WS.sub(" ", text.replace("\r", "\n")).strip()[:MAX_TEXT + 1]
    if len(text) > MAX_TEXT:
        return {"status": "error", "error": f"text too long for Airy (max ~{MAX_TEXT} chars)"}

    voice_id = resolve_voice(voice)
    style = (style or "normal").strip().lower()
    if style not in STYLES:
        style = "normal"
    language = (language or "en").strip().lower()
    language = language[:2] if language[:2] in LANGS else "en"
    try:
        sp = float(speed)
    except (TypeError, ValueError):
        sp = 1.0
    sp = max(0.5, min(2.0, sp))

    result = synthesize_chunks(text, voice_id, style, sp, language)
    if result.get("status") != "success":
        return result

    audio = result["audio"]
    return {
        "status": "success",
        "provider": "airy",
        "service": "Airy Studio",
        "voice": _voice_name(voice_id),
        "voiceId": voice_id,
        "style": style,
        "language": language,
        "speed": sp,
        "batches": result["batches"],
        "durationSec": result["duration"],
        "audioUrl": "",
        "dataUrl": f"data:audio/mpeg;base64,{base64.b64encode(audio).decode('ascii')}",
        "bytes": len(audio),
        "contentType": "audio/mpeg",
        "text": text,
    }


def get_models() -> List[Dict]:
    return [
        {
            "id": "airy/airy-tts-v1",
            "name": "Airy TTS v1",
            "maker": "Out of Set",
            "params": "studio",
            "context": f"{CHAR_LIMIT} chars/call",
            "blurb": f"104 voices · en+ko · {CHAR_LIMIT} chars per batch, auto-chunked",
            "goodAt": "Natural speech",
            "capabilities": {"tts": True},
        }
    ]


def probe() -> Dict:
    r = generate_tts("Hello from Airy text to speech.")
    return {"ok": r.get("status") == "success", "result": {k: v for k, v in r.items() if k != "dataUrl"}}
