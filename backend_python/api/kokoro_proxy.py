"""
Kokoro TTS Proxy — https://huggingface.co/spaces/hexgrad/Kokoro-TTS

Gradio 5.24, queue join with fn_index.
Verified 2026-08-24 via curl_cffi:
  POST /gradio_api/queue/join {"data":[text, voice, speed, hardware], "fn_index":4, "session_hash":...}
  GET  /gradio_api/queue/data?session_hash=...  SSE -> process_completed with audio url

Inputs: text, voice (af_heart etc), speed 0.5-2.0, hardware bool (True for ZeroGPU)
"""
from __future__ import annotations

import base64
import logging
import time
import uuid
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE = "https://hexgrad-kokoro-tts.hf.space"
FN_INDEX = 4

MODELS = [
    {"id": "kokoro/kokoro-82m", "name": "Kokoro 82M", "maker": "hexgrad", "params": "82M", "context": "500 chars", "blurb": "82M · 8+ voices · very natural · no signup", "goodAt": "Natural speech", "capabilities": {"tts": True}},
    {"id": "kokoro/kokoro-82m-af-heart", "name": "Kokoro Heart", "maker": "hexgrad", "params": "af_heart", "context": "500 chars", "blurb": "Warm female", "goodAt": "Natural speech", "capabilities": {"tts": True}},
    {"id": "kokoro/kokoro-82m-af-bella", "name": "Kokoro Bella", "maker": "hexgrad", "params": "af_bella", "context": "500 chars", "blurb": "Bright female", "goodAt": "Natural speech", "capabilities": {"tts": True}},
]

MODEL_MAP = {m["id"]: m for m in MODELS}
DEFAULT_VOICE = "af_heart"


def get_models() -> List[Dict]:
    return [{**m, "capabilities": m.get("capabilities", {"tts": True})} for m in MODELS]


def _session():
    try:
        from curl_cffi import requests as creq  # type: ignore

        return creq.Session(impersonate="chrome"), True
    except Exception:
        import requests as req  # type: ignore

        s = req.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"})
        return s, False


def _voice_from_model(model_id: str) -> str:
    if "af_bella" in (model_id or ""):
        return "af_bella"
    if "af_heart" in (model_id or ""):
        return "af_heart"
    return DEFAULT_VOICE


def generate_tts(text: str, voice: Optional[str] = None, speed: float = 1.0, model: str = "kokoro/kokoro-82m", hardware: bool = True) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()[:1000]
    vo = (voice or _voice_from_model(model) or DEFAULT_VOICE).strip() or DEFAULT_VOICE
    try:
        sp = float(speed) if speed is not None else 1.0
    except Exception:
        sp = 1.0
    sp = max(0.5, min(2.0, sp))

    sess, _ = _session()
    session_hash = uuid.uuid4().hex[:11]
    try:
        payload = {"data": [text, vo, sp, bool(hardware)], "fn_index": FN_INDEX, "session_hash": session_hash}
        r = sess.post(f"{BASE}/gradio_api/queue/join", json=payload, headers={"Origin": BASE, "Referer": BASE + "/"}, timeout=(10, 30))
        if r.status_code != 200:
            return {"status": "error", "error": f"Kokoro queue join {r.status_code}: {r.text[:400]}"}
        try:
            j = r.json()
        except Exception:
            return {"status": "error", "error": f"Kokoro non-JSON join: {r.text[:400]}"}
        event_id = j.get("event_id") or j.get("eventId")
        if not event_id:
            return {"status": "error", "error": f"Kokoro no event_id: {str(j)[:400]}"}

        # Poll queue/data SSE
        for _ in range(80):
            time.sleep(1)
            pr = sess.get(f"{BASE}/gradio_api/queue/data?session_hash={session_hash}", headers={"Accept": "text/event-stream"}, timeout=15)
            if pr.status_code != 200:
                continue
            for line in pr.text.splitlines():
                if not line.startswith("data:"):
                    continue
                payload_str = line[5:].strip()
                if not payload_str or payload_str == "[DONE]":
                    continue
                try:
                    import json as js

                    msg = js.loads(payload_str)
                except Exception:
                    continue
                if msg.get("msg") == "process_completed":
                    out = msg.get("output", {})
                    data = out.get("data") if isinstance(out, dict) else None
                    if isinstance(data, list) and data:
                        # data[0] is FileData dict, data[1] is phonemes text
                        audio = _extract_audio(data)
                        if audio:
                            return _download(sess, audio, text, vo)
                    # Fallback: try to find any url in the whole msg
                    audio = _extract_audio(msg)
                    if audio:
                        return _download(sess, audio, text, vo)
                    return {"status": "error", "error": f"Kokoro completed but no audio: {str(msg)[:400]}"}
                elif msg.get("msg") in ("estimation", "process_starts", "log", "heartbeat"):
                    continue
                elif msg.get("msg") == "close_stream":
                    break
        return {"status": "error", "error": "Kokoro timeout (ZeroGPU queue busy, try again)"}
    except Exception as exc:
        logger.exception("kokoro generate failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def _extract_audio(node) -> Optional[str]:
    if isinstance(node, dict):
        if node.get("url"):
            return node["url"]
        if node.get("path") and node["path"].endswith((".wav", ".mp3")):
            return node["path"]
        for v in node.values():
            found = _extract_audio(v)
            if found:
                return found
    elif isinstance(node, list):
        for v in node:
            found = _extract_audio(v)
            if found:
                return found
    elif isinstance(node, str) and (node.startswith("http") or node.startswith("/gradio_api/file=") or node.endswith(".wav")):
        return node
    return None


def _download(sess, audio: str, text: str, voice: str) -> Dict:
    url = audio
    if url.startswith("/"):
        url = BASE + url
    # HF file URL may need prefix
    if url.startswith("/file="):
        url = BASE + url
    ar = sess.get(url, timeout=30)
    if ar.status_code != 200 or not ar.content or len(ar.content) < 500:
        return {"status": "error", "error": f"Kokoro download failed {ar.status_code}"}
    b64 = base64.b64encode(ar.content).decode("ascii")
    ct = ar.headers.get("content-type", "audio/wav")
    if "wav" not in ct:
        ct = "audio/wav"
    return {
        "status": "success",
        "provider": "kokoro",
        "voice": voice,
        "audioUrl": url,
        "dataUrl": f"data:{ct};base64,{b64}",
        "bytes": len(ar.content),
        "contentType": ct,
        "text": text,
    }


def probe() -> Dict:
    r = generate_tts("Hello from Kokoro TTS")
    return {"ok": r.get("status") == "success", "result": r}
