"""
Lazypy TTS Proxy — https://lazypy.ro/tts/

Reverse-engineered from assets/js/tts.js and request_tts.php
- Endpoint: POST https://lazypy.ro/tts/request_tts.php
  Body: application/x-www-form-urlencoded service=...&voice=...&text=...
  Services: StreamElements, Streamlabs, TikTok, Cerence, Acapela, Oddcast,
            VoiceForge, Cepstral, Bing Translator, Google Translate, iSpeech
  Voices: via /assets/js/voices.json (205 StreamElements, 313 Bing, 64 Google, etc.)
- Response: {"success":true,"audio_url":"https://lazypy.ro/tts/assets/audio/...mp3", ...}
  On failure: {"success":false,"error_msg":"..."}

Verified 2026-08-24:
  Bing Translator (Microsoft Azure via Bing) — 3000 chars, 313 voices, works
    POST service=Bing%20Translator&voice=ar-EG-SalmaNeural&text=Hello -> success
  Google Translate — 200 chars, 64 voices, works
  iSpeech — 600 chars, 41 voices, works
  TikTok — currently "Couldn't load speech"
  StreamElements — 401 Unauthorized (needs API key)

We proxy 3 reliable no-signup unlimited services:
  - Bing Translator (best quality, 3000 chars)
  - Google Translate (200 chars, fallback)
  - iSpeech (600 chars)

No auth, no key, unlimited. We cache audio files locally via the returned audio_url
which is hosted on lazypy.ro and may expire, so we fetch bytes and return dataUrl.

FMHY notes: LazyPy / No Sign-Up — listed as reliable.
"""
from __future__ import annotations

import base64
import logging
import random
import time
import urllib.parse
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE = "https://lazypy.ro/tts"
REQUEST_URL = f"{BASE}/request_tts.php"
VOICES_URL = f"{BASE}/assets/js/voices.json"

VALID_SERVICES = ("Bing Translator", "Google Translate", "iSpeech", "Acapela", "Oddcast")
DEFAULT_SERVICE = "Bing Translator"
DEFAULT_VOICE = {
    "Bing Translator": "en-US-JennyNeural",
    "Google Translate": "en-gb",
    "iSpeech": "usenglishfemale",
}

TIMEOUT = (10, 60)

# Simple voice map for quick validation — fetched live on first call
_voices_cache: Optional[Dict] = None
_voices_ts: float = 0


def _session():
    try:
        from curl_cffi import requests as creq  # type: ignore

        return creq.Session(impersonate="chrome"), True
    except Exception:
        import requests as req  # type: ignore

        s = req.Session()
        s.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            }
        )
        return s, False


def get_voices() -> Dict:
    global _voices_cache, _voices_ts
    if _voices_cache and time.time() - _voices_ts < 3600:
        return _voices_cache
    sess, _ = _session()
    try:
        r = sess.get(VOICES_URL, timeout=15)
        if r.status_code == 200:
            _voices_cache = r.json()
            _voices_ts = time.time()
            return _voices_cache
    except Exception as exc:
        logger.warning("lazypy get_voices failed: %s", exc)
    finally:
        try:
            sess.close()
        except Exception:
            pass
    return _voices_cache or {}


def get_models() -> List[Dict]:
    voices = get_voices()
    models = []
    for svc in VALID_SERVICES:
        if svc in voices:
            count = len(voices[svc].get("voices", []))
            models.append(
                {
                    "id": f"lazypy/{svc.lower().replace(' ', '-')}",
                    "name": f"LazyPy {svc}",
                    "maker": "LazyPy",
                    "params": f"{count} voices",
                    "context": f"{voices[svc].get('charLimit', 0)} chars",
                    "blurb": f"{svc} via lazypy.ro — no signup, free.",
                    "goodAt": "Natural speech",
                    "capabilities": {"tts": True, "stream": False},
                }
            )
    if not models:
        # fallback hardcoded
        models = [
            {"id": "lazypy/bing-translator", "name": "LazyPy Bing (Microsoft)", "maker": "LazyPy", "params": "313 voices", "context": "3000 chars", "blurb": "Microsoft Azure via Bing — best quality, no signup", "goodAt": "Natural speech", "capabilities": {"tts": True}},
            {"id": "lazypy/google-translate", "name": "LazyPy Google", "maker": "LazyPy", "params": "64 voices", "context": "200 chars", "blurb": "Google Translate TTS — no signup", "goodAt": "Quick synthesis", "capabilities": {"tts": True}},
            {"id": "lazypy/ispeech", "name": "LazyPy iSpeech", "maker": "LazyPy", "params": "41 voices", "context": "600 chars", "blurb": "iSpeech — no signup", "goodAt": "Clear speech", "capabilities": {"tts": True}},
        ]
    return models


MODEL_MAP = {m["id"]: m for m in get_models()}
DEFAULT_MODEL = "lazypy/bing-translator"


def _service_from_model(model_id: str) -> str:
    mid = (model_id or "").lower()
    if "google" in mid:
        return "Google Translate"
    if "ispeech" in mid:
        return "iSpeech"
    if "bing" in mid or "microsoft" in mid or "edge" in mid:
        return "Bing Translator"
    return DEFAULT_SERVICE


def _voice_for_service(service: str, voice: Optional[str]) -> str:
    if voice:
        return voice
    return DEFAULT_VOICE.get(service, "en-US-JennyNeural")


def generate_tts(text: str, voice: Optional[str] = None, service: Optional[str] = None, model: str = DEFAULT_MODEL) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()
    if len(text) > 5000:
        return {"status": "error", "error": "text too long (max 5000 chars)"}

    svc = service or _service_from_model(model)
    if svc not in VALID_SERVICES:
        svc = DEFAULT_SERVICE
    vid = _voice_for_service(svc, voice)

    # Service char limits
    limits = {"Bing Translator": 3000, "Google Translate": 200, "iSpeech": 600, "Acapela": 2000, "Oddcast": 600}
    lim = limits.get(svc, 3000)
    if len(text) > lim:
        # Truncate for single-request services; caller should chunk if needed
        text = text[:lim]

    sess, _ = _session()
    try:
        payload = f"service={urllib.parse.quote(svc)}&voice={urllib.parse.quote(vid)}&text={urllib.parse.quote(text)}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://lazypy.ro",
            "Referer": "https://lazypy.ro/tts/",
        }
        r = sess.post(REQUEST_URL, data=payload, headers=headers, timeout=TIMEOUT)
        if r.status_code != 200:
            return {"status": "error", "error": f"Lazypy HTTP {r.status_code}: {r.text[:400]}"}
        try:
            data = r.json()
        except Exception:
            return {"status": "error", "error": f"Lazypy non-JSON: {r.text[:400]}"}

        if not data.get("success") or not data.get("audio_url"):
            return {"status": "error", "error": data.get("error_msg") or data.get("info") or "Lazypy generation failed", "raw": data}

        audio_url = data["audio_url"]
        if audio_url.startswith("/"):
            audio_url = "https://lazypy.ro" + audio_url
        elif audio_url.startswith("//"):
            audio_url = "https:" + audio_url

        # Fetch audio bytes and encode as dataUrl
        try:
            ar = sess.get(audio_url, timeout=30)
            if ar.status_code == 200 and ar.content:
                b64 = base64.b64encode(ar.content).decode("ascii")
                # Guess mime from url ext
                ext = audio_url.split(".")[-1].split("?")[0].lower()
                mime = "audio/mpeg" if ext == "mp3" else "audio/wav" if ext == "wav" else "audio/mpeg"
                data_url = f"data:{mime};base64,{b64}"
                return {
                    "status": "success",
                    "provider": "lazypy",
                    "service": svc,
                    "voice": vid,
                    "audioUrl": audio_url,
                    "dataUrl": data_url,
                    "bytes": len(ar.content),
                    "contentType": mime,
                    "text": text,
                }
        except Exception as exc:
            logger.info("lazypy audio download failed, returning url only: %s", exc)

        return {
            "status": "success",
            "provider": "lazypy",
            "service": svc,
            "voice": vid,
            "audioUrl": audio_url,
            "text": text,
        }
    except Exception as exc:
        logger.exception("lazypy generate failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def probe(model: str = DEFAULT_MODEL) -> Dict:
    r = generate_tts("Hello world", model=model)
    return {"ok": r.get("status") == "success", "result": r}
