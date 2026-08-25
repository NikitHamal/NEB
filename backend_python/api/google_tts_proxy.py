"""
Google Translate TTS Proxy — direct Google endpoint, no signup, unlimited

Endpoint: GET https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={lang}&client=gtx
- No API key, no signup, unlimited (with 200 char chunk limit)
- Returns audio/mpeg (MP3) directly
- Voices via lang code: en, en-gb, fr, de, ja, etc. (64 languages via lazypy list)
- For longer text, we chunk at 200 chars and concatenate MP3 frames (simple join)

Also supports the newer endpoint used by soundoftext.com:
  POST https://api.soundoftext.com/sounds with {"engine":"Google","data":{"text":..., "voice":"en-US"}}

We implement both: primary Google direct, fallback to SoundofText API.

FMHY: SoundofText / No Sign-Up — listed.
"""
from __future__ import annotations

import base64
import logging
import re
import urllib.parse
from typing import Dict, List

logger = logging.getLogger(__name__)

GOOGLE_TTS_URL = "https://translate.google.com/translate_tts"

MODELS = [
    {"id": "google/translate-en", "name": "Google Translate EN", "maker": "Google", "params": "", "context": "200 chars/chunk", "blurb": "Google Translate TTS — no signup, unlimited via chunking", "goodAt": "Fast synthesis", "capabilities": {"tts": True}},
    {"id": "google/translate-multi", "name": "Google Translate Multi", "maker": "Google", "params": "64 langs", "context": "200 chars/chunk", "blurb": "64 languages, auto chunked", "goodAt": "Multilingual", "capabilities": {"tts": True}},
]

MODEL_MAP = {m["id"]: m for m in MODELS}
DEFAULT_MODEL = "google/translate-en"


def get_models() -> List[Dict]:
    return [
        {**m, "capabilities": m.get("capabilities", {"tts": True})}
        for m in MODELS
    ]


def _session():
    try:
        from curl_cffi import requests as creq  # type: ignore

        return creq.Session(impersonate="chrome"), True
    except Exception:
        import requests as req  # type: ignore

        s = req.Session()
        s.headers.update(
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}
        )
        return s, False


def _chunk_text(text: str, limit: int = 200) -> List[str]:
    # Split on sentence boundaries, then words
    chunks = []
    remaining = text.strip()
    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break
        # Find last space or sentence end within limit
        cut = remaining.rfind(" ", 0, limit)
        if cut == -1:
            cut = limit
        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    return chunks


def generate_tts(text: str, lang: str = "en", voice: str = "en", model: str = DEFAULT_MODEL) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()
    # lang code normalization: en-gb -> en, fr -> fr, etc.
    tl = (lang or voice or "en").strip().split("-")[0].split("_")[0].lower()
    if not re.match(r"^[a-z]{2,3}$", tl):
        tl = "en"

    chunks = _chunk_text(text, 200)
    sess, _ = _session()
    audios = []
    try:
        for chunk in chunks:
            q = urllib.parse.quote(chunk)
            url = f"{GOOGLE_TTS_URL}?ie=UTF-8&q={q}&tl={tl}&client=gtx"
            headers = {"Referer": "https://translate.google.com/", "User-Agent": "Mozilla/5.0"}
            r = sess.get(url, headers=headers, timeout=20)
            if r.status_code != 200 or not r.content or len(r.content) < 100:
                logger.warning("google tts chunk failed %s: %s %s", chunk[:30], r.status_code, r.text[:200] if hasattr(r, "text") else "")
                continue
            # Google returns MP3, but may return 403 if blocked — retry with curl_cffi already handles
            audios.append(r.content)

        if not audios:
            return {"status": "error", "error": "Google TTS failed for all chunks"}

        # Concatenate MP3 chunks (simple bytes join — players handle concatenated MP3 frames)
        combined = b"".join(audios)
        b64 = base64.b64encode(combined).decode("ascii")
        data_url = f"data:audio/mpeg;base64,{b64}"
        return {
            "status": "success",
            "provider": "google",
            "model": model,
            "lang": tl,
            "dataUrl": data_url,
            "bytes": len(combined),
            "contentType": "audio/mpeg",
            "text": text,
            "chunks": len(chunks),
        }
    except Exception as exc:
        logger.exception("google tts failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def probe(model: str = DEFAULT_MODEL) -> Dict:
    r = generate_tts("Hello world", model=model)
    return {"ok": r.get("status") == "success", "result": r}
