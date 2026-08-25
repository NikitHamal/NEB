"""
Chatterbox TTS Proxy — https://huggingface.co/spaces/ResembleAI/Chatterbox

Gradio 6.3, api_name generate_tts_audio, 7 inputs -> 1 audio output.
Uses gradio_client for robust queue handling (ZeroGPU).

No signup, no key, unlimited (queue).
"""
from __future__ import annotations

import base64
import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

HF_SPACE = "ResembleAI/Chatterbox"
API_NAME = "/generate_tts_audio"

MODELS = [
    {"id": "chatterbox/chatterbox", "name": "Chatterbox", "maker": "ResembleAI", "params": "", "context": "300 chars", "blurb": "Expressive · reference audio · no signup", "goodAt": "Expressive speech", "capabilities": {"tts": True}},
]

MODEL_MAP = {m["id"]: m for m in MODELS}


def get_models() -> List[Dict]:
    return [{**m, "capabilities": m.get("capabilities", {"tts": True})} for m in MODELS]


def generate_tts(
    text: str,
    exaggeration: float = 0.5,
    temperature: float = 0.8,
    seed: int = 0,
    cfg: float = 0.5,
    vad_trimming: bool = False,
    reference_audio: Optional[str] = None,
) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()[:600]

    try:
        from gradio_client import Client, handle_file  # type: ignore

        client = Client(HF_SPACE, download_files=False)
        # For Chatterbox, reference audio is optional; we pass None
        result = client.predict(
            text,
            None,
            exaggeration,
            temperature,
            seed,
            cfg,
            vad_trimming,
            api_name=API_NAME,
        )
        # Result is a file path on HF server, or local temp file if download_files True
        # With download_files=False, result is a dict with url/path
        # Handle both: if result is str path, check if it's a file
        # gradio_client with download_files=False returns a dict like {"path":..., "url":...}
        # With default, it downloads to temp and returns local path string
        if isinstance(result, (list, tuple)):
            result = result[0] if result else None
        if not result:
            return {"status": "error", "error": "Chatterbox returned empty result"}

        # Handle dict with url/path
        if isinstance(result, dict):
            url = result.get("url") or result.get("path")
            if url and url.startswith("http"):
                # Need to download
                try:
                    from curl_cffi import requests as creq

                    sess = creq.Session(impersonate="chrome")
                except Exception:
                    import requests as req

                    sess = req.Session()
                try:
                    ar = sess.get(url, timeout=30)
                    if ar.status_code == 200 and ar.content:
                        b64 = base64.b64encode(ar.content).decode("ascii")
                        ct = ar.headers.get("content-type", "audio/wav")
                        return {"status": "success", "provider": "chatterbox", "audioUrl": url, "dataUrl": f"data:{ct};base64,{b64}", "bytes": len(ar.content), "contentType": ct, "text": text}
                finally:
                    try:
                        sess.close()
                    except Exception:
                        pass
            elif result.get("path"):
                p = Path(result["path"])
                if p.exists():
                    b = p.read_bytes()
                    b64 = base64.b64encode(b).decode("ascii")
                    return {"status": "success", "provider": "chatterbox", "dataUrl": f"data:audio/wav;base64,{b64}", "bytes": len(b), "contentType": "audio/wav", "text": text}
            return {"status": "error", "error": f"Chatterbox unexpected dict result: {str(result)[:300]}"}

        if isinstance(result, str):
            # Could be local temp file path or url or data
            if result.startswith("http"):
                try:
                    from curl_cffi import requests as creq

                    sess = creq.Session(impersonate="chrome")
                except Exception:
                    import requests as req

                    sess = req.Session()
                try:
                    ar = sess.get(result, timeout=30)
                    b64 = base64.b64encode(ar.content).decode("ascii")
                    return {"status": "success", "provider": "chatterbox", "audioUrl": result, "dataUrl": f"data:audio/wav;base64,{b64}", "bytes": len(ar.content), "text": text}
                finally:
                    try:
                        sess.close()
                    except Exception:
                        pass
            p = Path(result)
            if p.exists() and p.is_file():
                b = p.read_bytes()
                b64 = base64.b64encode(b).decode("ascii")
                return {"status": "success", "provider": "chatterbox", "dataUrl": f"data:audio/wav;base64,{b64}", "bytes": len(b), "contentType": "audio/wav", "text": text}
            # If result is already a dataUrl? Check
            if result.startswith("data:audio"):
                return {"status": "success", "provider": "chatterbox", "dataUrl": result, "bytes": len(result), "text": text}
            return {"status": "error", "error": f"Chatterbox file not found: {result[:200]}"}

        return {"status": "error", "error": f"Chatterbox unexpected result type {type(result)}: {str(result)[:300]}"}
    except Exception as exc:
        logger.exception("chatterbox generate failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}


def probe() -> Dict:
    r = generate_tts("Hello from Chatterbox TTS")
    return {"ok": r.get("status") == "success", "result": r}
