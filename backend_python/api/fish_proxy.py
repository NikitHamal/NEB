"""
Fish Audio proxy — Drama 3 expressive TTS.

Two tiers:
  1) Keyless: the official gradio Space https://fishaudio-drama-3.hf.space
     POST /gradio_api/call/perform {"data": [text, mode, voice, transcript,
          name, description, scene, temperature, top_p, top_k]}
     -> SSE /gradio_api/call/perform/<event_id> -> Audio (HLS playlist)
     -> concatenate the ADTS .aac segments into one stream.
     Emotion/special tags in the text work: [angry] [sad] [whispering]
     [laughing] [sighs] [pause] and friends.
  2) Official API (only when FISH_API_KEY is set in the environment):
     POST https://api.fish.audio/v1/tts with a model header — s2.1-pro-free
     (free per fish.audio/blog/tts-inference-optimization-s2-pro-free) or
     drama-3. Returns MP3 directly and needs no HLS assembly.
"""
from __future__ import annotations

import base64
import json
import logging
import os
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

SPACE_BASE = "https://fishaudio-drama-3.hf.space"
API_BASE = "https://api.fish.audio"
API_KEY_ENV = "FISH_API_KEY"
HF_TOKEN_ENV = "HF_TOKEN"

MAX_TEXT = 3000
MODES = ("Surprise", "Clone", "Design")
CLONE_VOICES = ("clone1", "clone2", "clone3")

MODELS = [
    {
        "id": "fishaudio/drama-3",
        "name": "Fish Audio Drama 3",
        "maker": "Fish Audio",
        "params": "expressive tags · voice design",
        "context": "emotion tags [laughing] [sad] [whispering], voice description",
        "blurb": "The most emotive Fish model — keyless via the official HF Space",
        "goodAt": "Expressive narration",
        "capabilities": {"tts": True, "expressive_tags": True, "voice_design": True},
    },
    {
        "id": "fishaudio/s2.1-pro-free",
        "name": "Fish Audio S2.1 Pro (free)",
        "maker": "Fish Audio",
        "params": "",
        "context": "official free API — requires FISH_API_KEY in the server .env",
        "blurb": "83 languages, no hard cap; free API key from fish.audio/app/api-keys",
        "goodAt": "Production TTS",
        "capabilities": {"tts": True, "requires_key": True},
    },
]

ALIASES = {
    "fishaudio/s1": "fishaudio/drama-3",
    "fishaudio/s1-mini": "fishaudio/drama-3",
    "fishaudio": "fishaudio/drama-3",
    "fish-s1": "fishaudio/drama-3",
    "": "fishaudio/drama-3",
}

DEFAULT_MODEL = "fishaudio/drama-3"
MODEL_MAP = {m["id"]: m for m in MODELS}


def get_models() -> List[Dict]:
    return [{**m, "capabilities": m.get("capabilities", {"tts": True})} for m in MODELS]


def _api_key() -> str:
    return (os.environ.get(API_KEY_ENV) or "").strip()


def _hf_token() -> str:
    return (os.environ.get(HF_TOKEN_ENV) or os.environ.get("HUGGINGFACE_TOKEN") or "").strip()


def _session():
    from curl_cffi import requests as creq

    sess = creq.Session(impersonate="chrome")
    token = _hf_token()
    if token:
        sess.headers["Authorization"] = f"Bearer {token}"
    return sess


def _resolve_model(model: Optional[str]) -> str:
    m = (model or "").strip()
    if m in MODEL_MAP:
        return m
    if m in ALIASES:
        return ALIASES[m]
    if m.startswith("fishaudio/"):
        return DEFAULT_MODEL
    return DEFAULT_MODEL


def _clamp(value, lo, hi, default):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return default
    return max(lo, min(hi, v))


def generate_tts(
    text: str,
    voice: str = "",
    model: Optional[str] = None,
    mode: str = "",
    description: str = "",
    scene: str = "",
    character: str = "",
    transcript: str = "",
    temperature=None,
    top_p=None,
    top_k=None,
    **kwargs,
) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()
    if len(text) > MAX_TEXT:
        return {"status": "error", "error": f"text too long for Drama 3 ({len(text)} chars, max {MAX_TEXT})"}

    resolved = _resolve_model(model)
    if resolved == "fishaudio/s2.1-pro-free":
        return _api_generate(text, voice=voice, api_model="s2.1-pro-free")

    space_result = _space_generate(
        text,
        voice=voice,
        mode=mode,
        description=description,
        scene=scene,
        character=character,
        transcript=transcript,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )
    if space_result.get("status") == "success":
        return space_result

    if _api_key():
        logger.info("fish space failed (%s) — trying official API", space_result.get("error"))
        api_result = _api_generate(text, voice=voice, api_model="drama-3")
        if api_result.get("status") == "success":
            return api_result
        return api_result

    space_result["error"] = (
        f"{space_result.get('error')} · HF Space quota: set {HF_TOKEN_ENV} (free HF account token) "
        f"in the server .env for more, or {API_KEY_ENV} for the official free API "
        "(fish.audio/app/api-keys)."
    )
    return space_result


def _space_generate(
    text: str,
    voice: str = "",
    mode: str = "",
    description: str = "",
    scene: str = "",
    character: str = "",
    transcript: str = "",
    temperature=None,
    top_p=None,
    top_k=None,
) -> Dict:
    chosen_mode = mode if mode in MODES else ("Design" if description.strip() else "Surprise")
    chosen_voice = voice if voice in CLONE_VOICES else "clone1"
    data = [
        text,
        chosen_mode,
        chosen_voice,
        transcript or "",
        character or "Narrator",
        description or "",
        scene or "",
        _clamp(temperature, 0.3, 1.3, 1.0),
        _clamp(top_p, 0.5, 1.0, 0.9),
        int(_clamp(top_k, 0, 100, 0)),
    ]

    result = _space_attempt(SPACE_BASE, data, voice=voice, description=description, mode=chosen_mode, text=text)
    if result.get("status") == "success":
        return result
    return {"status": "error", "error": result.get("error") or "space failed"}


def _space_attempt(base: str, data: List, voice: str, description: str, mode: str, text: str) -> Dict:
    sess = _session()
    try:
        r = sess.post(f"{base}/gradio_api/call/perform", json={"data": data}, timeout=60)
        if r.status_code != 200:
            return {"status": "error", "error": f"Space join HTTP {r.status_code}: {r.text[:200]}"}
        event_id = (r.json() or {}).get("event_id")
        if not event_id:
            return {"status": "error", "error": f"Space returned no event_id: {r.text[:200]}"}

        payload = _read_event(sess, base, event_id)
        if payload is None:
            return {"status": "error", "error": "Space stream ended without a result"}
        if isinstance(payload, dict) and payload.get("error"):
            return {"status": "error", "error": f"Space error: {str(payload['error'])[:300]}"}

        audio_url = _audio_url_from_payload(base, payload)
        if not audio_url:
            return {"status": "error", "error": f"Space returned no audio: {str(payload)[:300]}"}

        if audio_url.endswith(".m3u8"):
            blob, duration = _fetch_hls(sess, audio_url)
            content_type = "audio/aac"
        else:
            ar = sess.get(audio_url, timeout=300)
            if ar.status_code != 200 or not ar.content:
                return {"status": "error", "error": f"Audio fetch HTTP {ar.status_code}"}
            blob, duration = ar.content, None
            content_type = (ar.headers.get("content-type") or "audio/mpeg").split(";")[0]

        if len(blob) < 300:
            return {"status": "error", "error": f"Suspiciously small audio ({len(blob)} bytes)"}

        return {
            "status": "success",
            "provider": "fishaudio",
            "service": "hf-space",
            "model": "fishaudio/drama-3",
            "voice": (description or (voice if voice in CLONE_VOICES else "")) or f"{mode.lower()} voice",
            "dataUrl": f"data:{content_type};base64,{base64.b64encode(blob).decode('ascii')}",
            "bytes": len(blob),
            "contentType": content_type,
            "durationSec": duration,
            "text": text,
        }
    except Exception as exc:
        logger.info("fish space %s failed: %s", base, exc)
        return {"status": "error", "error": f"Space call failed: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def _read_event(sess, base: str, event_id: str):
    rr = sess.get(f"{base}/gradio_api/call/perform/{event_id}", timeout=900, stream=True)
    if rr.status_code != 200:
        return None
    pending_error = False
    for raw in rr.iter_lines():
        if not raw:
            continue
        line = raw.decode("utf-8", "replace").strip()
        if line.startswith("event:"):
            pending_error = line[6:].strip() == "error"
            continue
        if not line.startswith("data:"):
            continue
        body = line[5:].strip()
        if body == "[DONE]":
            return None
        try:
            parsed = json.loads(body)
        except Exception:
            continue
        if pending_error:
            if isinstance(parsed, dict):
                return {"error": parsed.get("error") or parsed}
            return {"error": parsed if isinstance(parsed, str) else "unknown error"}
        if isinstance(parsed, list):
            return parsed
    return None


def _audio_url_from_payload(base: str, payload) -> Optional[str]:
    if not isinstance(payload, list):
        return None
    for item in payload:
        if isinstance(item, dict):
            url = item.get("url") or item.get("path")
            if url and isinstance(url, str):
                if url.startswith("/"):
                    return urljoin(base + "/", url)
                return url
        elif isinstance(item, str) and item.startswith("http"):
            return item
    return None


def _fetch_hls(sess, playlist_url: str):
    pr = sess.get(playlist_url, timeout=120)
    if pr.status_code != 200:
        raise RuntimeError(f"playlist HTTP {pr.status_code}")
    playlist = pr.text
    segments = []
    duration = 0.0
    for line in playlist.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#EXTINF:"):
            try:
                duration += float(line[8:].split(",")[0])
            except ValueError:
                pass
            continue
        if line.startswith("#"):
            continue
        segments.append(urljoin(playlist_url, line))
    if not segments:
        raise RuntimeError("playlist had no segments")
    blob = bytearray()
    for seg_url in segments:
        sr = sess.get(seg_url, timeout=120)
        if sr.status_code != 200 or not sr.content:
            raise RuntimeError(f"segment HTTP {sr.status_code}")
        blob.extend(sr.content)
    return bytes(blob), round(duration, 2) if duration else None


def _api_generate(text: str, voice: str = "", api_model: str = "s2.1-pro-free") -> Dict:
    key = _api_key()
    if not key:
        return {
            "status": "error",
            "error": f"Official Fish API needs {API_KEY_ENV} in the server .env "
                     "(free key: fish.audio/app/api-keys)",
        }
    sess = _session()
    try:
        body = {"text": text, "format": "mp3"}
        if voice and re.fullmatch(r"[0-9a-fA-F]{32}", voice.strip()):
            body["reference_id"] = voice.strip()
        r = sess.post(
            f"{API_BASE}/v1/tts",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "model": api_model,
            },
            json=body,
            timeout=300,
        )
        if r.status_code != 200 or not r.content or len(r.content) < 300:
            return {"status": "error", "error": f"Official API HTTP {r.status_code}: {r.text[:250]}"}
        content_type = (r.headers.get("content-type") or "audio/mpeg").split(";")[0]
        return {
            "status": "success",
            "provider": "fishaudio",
            "service": "official-api",
            "model": f"fishaudio/{api_model}",
            "voice": voice or api_model,
            "dataUrl": f"data:{content_type};base64,{base64.b64encode(r.content).decode('ascii')}",
            "bytes": len(r.content),
            "contentType": content_type,
            "text": text,
        }
    except Exception as exc:
        return {"status": "error", "error": f"Official API failed: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def probe() -> Dict:
    r = generate_tts("Hello from Fish Audio Drama 3! [laughs] This is a probe.")
    return {"ok": r.get("status") == "success", "result": r}
