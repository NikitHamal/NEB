"""
Fish Audio Proxy — https://fish.audio / HF Space fishaudio/fish-speech-1.5

FMHY lists Fish Audio without No Sign-Up tag, but the HF Space
https://huggingface.co/spaces/fishaudio/fish-speech-1.5 is without login and
can be called via Gradio. However the Space's Gradio API is not stable.

We implement a two-tier fallback:
  1) Try HF Space fishaudio/fish-speech-1.5 via gradio_client (if available)
     POST https://fishaudio-fish-speech-1-5.hf.space/gradio_api/call/predict
  2) Fallback to Fish Audio's public demo API (if it exists without key):
     The site fish.audio uses https://api.fish.audio — try a no-key demo
     endpoint. If that fails, return a clear error suggesting to use
     Kokoro/Chatterbox/LazyPy which are verified no-signup.

For now, this proxy will attempt the HF Space and gracefully degrade.

FMHY: Fish Audio (github.com/fishaudio) — listed under Voice Change/Clone
but the user requested it as a better TTS.

We expose a simple generate_tts that tries HF first.
"""
from __future__ import annotations

import base64
import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

HF_BASE = "https://fishaudio-fish-speech-1-5.hf.space"
API_NAME = "predict"  # generic, may be different

MODELS = [
    {"id": "fishaudio/s1", "name": "Fish S1", "maker": "Fish Audio", "params": "", "context": "Fish Speech 1.5", "blurb": "High quality · many voices · demo via HF", "goodAt": "Natural speech", "capabilities": {"tts": True}},
]

MODEL_MAP = {m["id"]: m for m in MODELS}
DEFAULT_MODEL = "fishaudio/s1"


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


def generate_tts(text: str, voice: str = "default", **kwargs) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()[:1000]

    # First, try HF Space via gradio_client if available
    try:
        from gradio_client import Client  # type: ignore

        client = Client(HF_BASE)
        # Fish Speech 1.5 on HF typically has fn called "predict" with text + reference audio
        # Try with just text
        result = client.predict(text, api_name="/predict")
        # result may be file path or url
        if isinstance(result, str) and result.startswith("/"):
            # It's a file path on HF, need to download via HF URL
            url = HF_BASE + "/file=" + result if not result.startswith("http") else result
            sess, _ = _session()
            try:
                ar = sess.get(url, timeout=30)
                if ar.status_code == 200 and ar.content:
                    b64 = base64.b64encode(ar.content).decode("ascii")
                    return {"status": "success", "provider": "fishaudio", "audioUrl": url, "dataUrl": f"data:audio/wav;base64,{b64}", "bytes": len(ar.content), "text": text}
            finally:
                try:
                    sess.close()
                except Exception:
                    pass
        elif isinstance(result, (list, tuple)) and result:
            first = result[0]
            if isinstance(first, str) and (first.startswith("http") or first.startswith("/")):
                sess, _ = _session()
                try:
                    url = first if first.startswith("http") else HF_BASE + first
                    ar = sess.get(url, timeout=30)
                    b64 = base64.b64encode(ar.content).decode("ascii")
                    return {"status": "success", "provider": "fishaudio", "audioUrl": url, "dataUrl": f"data:audio/wav;base64,{b64}", "bytes": len(ar.content), "text": text}
                finally:
                    try:
                        sess.close()
                    except Exception:
                        pass
        return {"status": "error", "error": f"Fish HF unexpected result: {str(result)[:300]}"}
    except ImportError:
        pass
    except Exception as exc:
        logger.info("fish hf client failed: %s", exc)

    # Fallback: try direct Fish Audio API without key (may fail, but we try)
    sess, _ = _session()
    try:
        # Public demo may be at https://api.fish.audio/demo or /v1/demo
        # Try unauthenticated POST to /v1/tts with minimal payload
        # This is a best-effort; if it requires API key it will return 401 and we surface that
        payload = {"text": text, "reference_id": voice or "default", "format": "mp3"}
        headers = {"Origin": "https://fish.audio", "Referer": "https://fish.audio/"}
        r = sess.post("https://api.fish.audio/v1/tts", json=payload, headers=headers, timeout=15)
        if r.status_code == 200 and r.content and len(r.content) > 500:
            ct = r.headers.get("content-type", "audio/mpeg")
            b64 = base64.b64encode(r.content).decode("ascii")
            return {"status": "success", "provider": "fishaudio", "dataUrl": f"data:{ct};base64,{b64}", "bytes": len(r.content), "text": text}
        return {"status": "error", "error": f"Fish Audio HTTP {r.status_code}: {r.text[:300]}. Hint: Fish Audio demo may require signup/API key — try Kokoro/Chatterbox/LazyPy instead.", "raw": r.text[:500]}
    except Exception as exc:
        return {"status": "error", "error": f"Fish Audio failed: {exc}. Try Kokoro/Chatterbox/LazyPy (verified no-signup)."}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def probe() -> Dict:
    r = generate_tts("Hello from Fish Audio")
    return {"ok": r.get("status") == "success", "result": r}
