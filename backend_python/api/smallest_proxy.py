"""
Smallest AI TTS proxy — https://smallest.ai (Lightning v3.1 / v3.1 Pro)

Verified live 2026-11-08:
  GET  https://api.smallest.ai/waves/v1/lightning-v3.1/get_voices       234 voices, NO auth
  GET  https://api.smallest.ai/waves/v1/lightning-v3.1-pro/get_voices   269 voices, NO auth
  POST https://api.smallest.ai/waves/v1/tts                             audio, API key required

The two voice catalogues are public, so the picker fills with no key at all;
only synthesis needs SMALLEST_API_KEY in the server .env (free key from
https://app.smallest.ai), the same pattern as Fish Audio's FISH_API_KEY.

Request body: {"text","voice_id","model":"lightning_v3.1|lightning_v3.1_pro",
               "sample_rate":24000,"speed":1.0,"language":"en",
               "output_format":"mp3"}
Response: raw audio bytes (PCM, MP3, WAV, ulaw, alaw), mono.

Server-side limits that shape this module:
  * 250 characters max per request (~140 is the documented optimum), so text
    is packed at sentence ends and synthesised in batches.
  * The two pools have DIFFERENT voice catalogues, and a Pro voice id sent to
    the standard pool (or the reverse) can produce wrong audio, so every
    request carries the pool's model field and resolves voices in its own
    catalogue.
  * Lightning v3.1 is retired 2026-11-30 and the Pro preview checkpoint
    (lightning_v3.1_pro_10_26) is promoted 2026-11-28, so Pro is the default.

Nepali (ne) has no trained voice on either pool; `hi` (Indian accent plus
Hindi code-switching) is the closest match and `en` is the safe default.
"""
from __future__ import annotations

import base64
import logging
import os
import re
import threading
import time
from typing import Dict, List, Optional
from .proxy_http import new_session

logger = logging.getLogger(__name__)

BASE = "https://api.smallest.ai"
TTS_URL = f"{BASE}/waves/v1/tts"
API_KEY_ENV = "SMALLEST_API_KEY"

CHUNK_LIMIT = 240          # docs cap a request at 250 chars
MAX_CHUNKS = 12
MAX_TEXT = 2400            # sentence packing is imperfect, so this sits below MAX_CHUNKS * CHUNK_LIMIT
MIN_INTERVAL = 0.4         # seconds between batches; the Standard plan allows 10 concurrent

SAMPLE_RATES = (8000, 16000, 24000, 44100)
DEFAULT_SAMPLE_RATE = 24000
LANG_CODES = (
    "en", "hi", "ta", "es", "kn", "mr", "te", "or", "pa", "ml", "gu", "bn",
    "fr", "de", "it", "nl", "sv", "pt", "pl", "ru", "auto",
)
DEFAULT_LANGUAGE = "en"
LANG_NAMES = {
    "english": "en", "hindi": "hi", "tamil": "ta", "spanish": "es",
    "kannada": "kn", "marathi": "mr", "telugu": "te", "odia": "or",
    "punjabi": "pa", "malayalam": "ml", "gujarati": "gu", "bengali": "bn",
    "french": "fr", "german": "de", "italian": "it", "dutch": "nl",
    "swedish": "sv", "portuguese": "pt", "polish": "pl", "russian": "ru",
}

_PRO_VOICES_URL = f"{BASE}/waves/v1/lightning-v3.1-pro/get_voices"

# Pool table: our model id -> upstream model field + public catalogue URL.
POOLS: Dict[str, Dict] = {
    "smallest/lightning-v3.1-pro": {
        "model": "lightning_v3.1_pro",
        "label": "Lightning v3.1 Pro",
        "voices_url": _PRO_VOICES_URL,
        "default_voice": "kelsey",
        "note": "269 voices · 31 languages · premium pool, needs SMALLEST_API_KEY",
    },
    "smallest/lightning-v3.1-pro-10-26": {
        "model": "lightning_v3.1_pro_10_26",
        "label": "Lightning v3.1 Pro (Oct 26 preview)",
        "voices_url": _PRO_VOICES_URL,
        "default_voice": "kelsey",
        "note": "newest checkpoint · en/es/hi only · preview ID retires 2026-12-28",
    },
    "smallest/lightning-v3.1": {
        "model": "lightning_v3.1",
        "label": "Lightning v3.1",
        "voices_url": f"{BASE}/waves/v1/lightning-v3.1/get_voices",
        "default_voice": "magnus",
        "note": "234 voices · 20 languages · retires 2026-11-30, use Pro instead",
    },
}
DEFAULT_POOL = "smallest/lightning-v3.1-pro"

_last_call = 0.0
_pace_lock = threading.Lock()
_voice_caches: Dict[str, List[Dict]] = {}
_voice_cache_at: Dict[str, float] = {}
VOICE_TTL = 6 * 3600

_LATIN_END = ".!?"
_CJK_END = "。！？"
_CLOSERS = "\"'”’)]）】»"
_WS = re.compile(r"\s+")
_MPEG_SYNC = re.compile(rb"\xff[\xe0-\xff]")


def api_key() -> str:
    return (os.environ.get(API_KEY_ENV) or "").strip()


def resolve_pool(model: Optional[str]) -> str:
    wanted = (model or "").strip().lower()
    if wanted in POOLS:
        return wanted
    if wanted.startswith("smallest"):
        if "10-26" in wanted or "10_26" in wanted:
            return "smallest/lightning-v3.1-pro-10-26"
        if "pro" in wanted:
            return "smallest/lightning-v3.1-pro"
        if "v3.1" in wanted:
            return "smallest/lightning-v3.1"
    return DEFAULT_POOL


def _sentence_ends_here(text: str, i: int) -> Optional[int]:
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


def _cut(sentence: str, limit: int) -> tuple:
    space = sentence.rfind(" ", 0, limit + 1)
    cut = space if space > limit // 2 else limit
    return sentence[:cut].strip(), sentence[cut:].strip()


def split_chunks(text: str, limit: int = CHUNK_LIMIT) -> List[str]:
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


def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "audio/mpeg, audio/wav, application/json",
        "Authorization": f"Bearer {api_key()}",
        "Referer": "https://smallest.ai/",
        "Origin": "https://smallest.ai",
    }


def _pace() -> None:
    global _last_call
    with _pace_lock:
        wait = MIN_INTERVAL - (time.time() - _last_call)
        _last_call = time.time() + max(wait, 0.0)
    if wait > 0:
        time.sleep(wait)


def get_voices(pool: Optional[str] = None, refresh: bool = False) -> List[Dict]:
    """Voice catalogue for one pool (public endpoint, no API key needed)."""
    pool = resolve_pool(pool)
    now = time.time()
    cached = _voice_caches.get(pool) or []
    if not refresh and cached and now - _voice_cache_at.get(pool, 0.0) < VOICE_TTL:
        return cached
    sess = new_session()
    try:
        r = sess.get(POOLS[pool]["voices_url"], timeout=(10, 25))
        if r.status_code != 200:
            logger.warning("smallest voices %s: %s", r.status_code, r.text[:200])
            return cached
        data = r.json()
    except Exception:
        logger.exception("smallest voices fetch failed")
        return cached
    finally:
        try:
            sess.close()
        except Exception:
            pass

    voices: List[Dict] = []
    for v in data.get("voices") or []:
        vid = (v.get("voiceId") or "").strip()
        if not vid:
            continue
        tags = v.get("tags") or {}
        langs = [LANG_NAMES.get(str(x).strip().lower(), str(x).strip().lower())
                 for x in (tags.get("language") or [])]
        voices.append({
            "id": vid,
            "name": (v.get("displayName") or vid).strip(),
            "gender": (tags.get("gender") or "neutral").strip(),
            "accent": (tags.get("accent") or "").strip(),
            "age": (tags.get("age") or "").strip(),
            "langs": langs,
            "usecases": tags.get("usecases") or [],
            "recommended": tags.get("recommendedLanguages") or [],
        })
    if voices:
        _voice_caches[pool] = voices
        _voice_cache_at[pool] = now
    return voices


def resolve_voice(voice: Optional[str], pool: Optional[str] = None) -> str:
    pool = resolve_pool(pool)
    wanted = (voice or "").strip()
    if not wanted:
        return POOLS[pool]["default_voice"]
    lowered = wanted.lower()
    for v in get_voices(pool):
        if v["id"].lower() == lowered:
            return v["id"]
    for v in get_voices(pool):
        if v["name"].lower() == lowered:
            return v["id"]
    for v in get_voices(pool):
        if lowered in v["name"].lower():
            return v["id"]
    return POOLS[pool]["default_voice"]


def _voice_name(voice_id: str, pool: str) -> str:
    for v in get_voices(pool):
        if v["id"] == voice_id:
            return v["name"]
    return voice_id


def _strip_container(data: bytes) -> bytes:
    """Drop a leading ID3v2 tag and any bytes before the first MPEG frame.

    Smallest returns a self-contained MP3 per request; when batches are
    stitched, only the first chunk may keep its tag.
    """
    if data[:3] == b"ID3":
        size = ((data[6] & 0x7f) << 21) | ((data[7] & 0x7f) << 14) | \
               ((data[8] & 0x7f) << 7) | (data[9] & 0x7f)
        data = data[10 + size:] if len(data) > 10 + size else b""
    match = _MPEG_SYNC.search(data)
    if match:
        data = data[match.start():]
    return data


def _error_detail(r) -> str:
    try:
        body = r.json()
        if isinstance(body, dict):
            errors = body.get("errors") or body.get("error") or body.get("message")
            if isinstance(errors, list):
                return "; ".join(str(e) for e in errors)[:300]
            if errors:
                return str(errors)[:300]
    except Exception:
        pass
    return (r.text or "")[:300]


def _request_chunk(sess, text: str, voice_id: str, pool: str, speed: float,
                   language: str, sample_rate: int) -> tuple:
    payload = {
        "text": text,
        "voice_id": voice_id,
        "model": POOLS[pool]["model"],
        "language": language,
        "speed": speed,
        "sample_rate": sample_rate,
        "output_format": "mp3",
    }
    r = sess.post(TTS_URL, json=payload, headers=_headers(), timeout=(15, 120))
    if r.status_code != 200:
        detail = _error_detail(r)
        if r.status_code in (401, 403) and not api_key():
            detail = f"{API_KEY_ENV} is not set in the server .env"
        return None, f"Smallest AI {r.status_code}: {detail}", 0.0
    audio = _strip_container(r.content)
    if len(audio) < 512:
        return None, "Smallest AI returned an empty audio stream", 0.0
    return audio, None, 0.0


def synthesize_chunks(text: str, voice_id: str, pool: str, speed: float, language: str,
                      sample_rate: int, on_progress=None) -> Dict:
    chunks = split_chunks(text)
    if not chunks:
        return {"status": "error", "error": "text required"}
    if len(chunks) > MAX_CHUNKS:
        return {"status": "error",
                "error": f"text too long for Smallest AI — {len(chunks)} batches needed, "
                         f"max {MAX_CHUNKS} (~{MAX_TEXT} chars)"}
    if not api_key():
        return {"status": "error",
                "error": f"Smallest AI needs {API_KEY_ENV} in the server .env "
                         f"(free key from app.smallest.ai)"}

    sess = new_session()
    pieces: List[bytes] = []
    try:
        for index, chunk in enumerate(chunks):
            if index:
                _pace()
            audio, error, _ = _request_chunk(sess, chunk, voice_id, pool, speed, language, sample_rate)
            if error:
                return {"status": "error", "error": error, "raw": f"batch {index + 1}/{len(chunks)}"}
            pieces.append(audio)
            if on_progress:
                try:
                    on_progress(index + 1, len(chunks))
                except Exception:
                    pass
    except Exception as exc:
        logger.exception("smallest synthesize failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass

    audio = b"".join(pieces)
    return {"status": "success", "audio": audio, "batches": len(chunks)}


def generate_tts(text: str, voice: Optional[str] = None, model: Optional[str] = None,
                 speed=1.0, language: Optional[str] = None,
                 sample_rate=DEFAULT_SAMPLE_RATE, on_progress=None) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = _WS.sub(" ", text.replace("\r", "\n")).strip()[:MAX_TEXT + 1]
    if len(text) > MAX_TEXT:
        return {"status": "error", "error": f"text too long for Smallest AI (max ~{MAX_TEXT} chars)"}

    pool = resolve_pool(model)
    voice_id = resolve_voice(voice, pool)
    try:
        sp = float(speed)
    except (TypeError, ValueError):
        sp = 1.0
    sp = max(0.5, min(2.0, sp))
    lang = (language or "").strip().lower()
    lang = lang if lang in LANG_CODES else DEFAULT_LANGUAGE
    try:
        rate = int(sample_rate)
    except (TypeError, ValueError):
        rate = DEFAULT_SAMPLE_RATE
    rate = rate if rate in SAMPLE_RATES else DEFAULT_SAMPLE_RATE

    result = synthesize_chunks(text, voice_id, pool, sp, lang, rate, on_progress)
    if result.get("status") != "success":
        return result

    audio = result["audio"]
    return {
        "status": "success",
        "provider": "smallest",
        "service": f"Smallest AI {POOLS[pool]['label']}",
        "voice": _voice_name(voice_id, pool),
        "voiceId": voice_id,
        "model": pool,
        "language": lang,
        "speed": sp,
        "sampleRate": rate,
        "batches": result["batches"],
        "durationSec": 0,
        "audioUrl": "",
        "dataUrl": f"data:audio/mpeg;base64,{base64.b64encode(audio).decode('ascii')}",
        "bytes": len(audio),
        "contentType": "audio/mpeg",
        "text": text,
    }


def get_models() -> List[Dict]:
    out: List[Dict] = []
    for pool_id, pool in POOLS.items():
        out.append({
            "id": pool_id,
            "name": pool["label"],
            "maker": "Smallest AI",
            "params": "lightning",
            "context": f"{CHUNK_LIMIT} chars/call",
            "blurb": pool["note"],
            "goodAt": "Natural multilingual speech",
            "capabilities": {"tts": True, "requires_key": True},
        })
    return out


def probe() -> Dict:
    r = generate_tts("Hello from Smallest AI text to speech.")
    return {"ok": r.get("status") == "success", "result": {k: v for k, v in r.items() if k != "dataUrl"}}
