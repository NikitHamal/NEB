"""
Moe TTS Proxy — https://huggingface.co/spaces/skytnt/moe-tts

Gradio 4.36 Space. API prefix is EMPTY for this version (the /gradio_api
prefix only exists on Gradio 5.x / late 4.44+), so endpoints are:
  POST {base}/call/tts_fn          {"data": [text, speaker, speed, symbol_input]}
  GET  {base}/call/tts_fn/{event_id}   (SSE: data: [...] lines, last has audio)

Inputs (from /config dependency 0 -> components [8,9,10,13]):
  8  textbox  "Text (150 words limitation)"
  9  dropdown "Speaker"        — Japanese names, e.g. 絢地寧々
  10 slider   "Speed"          — default 1.0
  13 checkbox "Symbol input"   — default False

We read the config once (cached) to pick up the default speaker and the
api_prefix so a future Space upgrade doesn't 404 us again.

FMHY: Moe TTS / No Sign-Up.
"""
from __future__ import annotations

import base64
import logging
import time
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE = "https://skytnt-moe-tts.hf.space"
API_NAME = "tts_fn"

MODELS = [
    {"id": "moe/moe-tts", "name": "Moe TTS (Anime)", "maker": "skytnt", "params": "", "context": "~150 words", "blurb": "Moe TTS — Japanese anime voices, no signup", "goodAt": "Anime speech", "capabilities": {"tts": True}},
]

MODEL_MAP = {m["id"]: m for m in MODELS}
DEFAULT_MODEL = "moe/moe-tts"

_config_cache: Optional[Dict] = None
_config_ts: float = 0


def _session():
    try:
        from curl_cffi import requests as creq  # type: ignore

        return creq.Session(impersonate="chrome"), True
    except Exception:
        import requests as req  # type: ignore

        s = req.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"})
        return s, False


def _load_config(force: bool = False) -> Optional[Dict]:
    """Fetch /config once; returns {'prefix': str, 'speaker': str, 'speed': float, 'symbol': bool}"""
    global _config_cache, _config_ts
    if _config_cache and not force and time.time() - _config_ts < 3600:
        return _config_cache
    sess, _ = _session()
    try:
        r = sess.get(f"{BASE}/config", timeout=15)
        if r.status_code != 200:
            return _config_cache
        cfg = r.json()
        prefix = cfg.get("api_prefix") or ""
        comps = {c.get("id"): c for c in cfg.get("components", [])}
        speaker, speed, symbol = None, 1.0, False
        for dep in cfg.get("dependencies", []):
            if dep.get("api_name") == API_NAME:
                for cid in dep.get("inputs", []):
                    c = comps.get(cid)
                    if not c:
                        continue
                    props = c.get("props") or {}
                    ctype = c.get("type")
                    if ctype == "dropdown":
                        choices = props.get("choices") or []
                        vals = [(x[1] if isinstance(x, list) else x) for x in choices]
                        speaker = props.get("value") if props.get("value") in vals else (vals[0] if vals else None)
                    elif ctype == "slider":
                        try:
                            speed = float(props.get("value", 1.0))
                        except Exception:
                            speed = 1.0
                    elif ctype == "checkbox":
                        symbol = bool(props.get("value", False))
                break
        _config_cache = {"prefix": prefix, "speaker": speaker, "speed": speed, "symbol": symbol}
        _config_ts = time.time()
        return _config_cache
    except Exception as exc:
        logger.warning("moe config fetch failed: %s", exc)
        return _config_cache
    finally:
        try:
            sess.close()
        except Exception:
            pass


def get_models() -> List[Dict]:
    return [{**m, "capabilities": m.get("capabilities", {"tts": True})} for m in MODELS]


def _post_call(sess, data: List) -> Dict:
    """POST to /call/{name} trying both with and without the gradio_api prefix."""
    cfg = _load_config() or {}
    prefix = cfg.get("prefix", "")
    attempts = []
    if prefix:
        attempts.append(f"{BASE}{prefix}/call/{API_NAME}")
    attempts.append(f"{BASE}/call/{API_NAME}")
    if prefix:
        attempts.append(f"{BASE}/call/{API_NAME}")  # dedup guard below
    seen = []
    for url in attempts:
        if url in seen:
            continue
        seen.append(url)
        r = sess.post(url, json={"data": data}, headers={"Origin": BASE, "Referer": BASE + "/"}, timeout=(10, 30))
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                continue
        last = (r.status_code, r.text[:200])
    raise RuntimeError(f"Moe call failed: {last}")


def _poll_result(sess, event_id: str, max_seconds: int = 90) -> List:
    cfg = _load_config() or {}
    prefix = cfg.get("prefix", "")
    urls = []
    if prefix:
        urls.append(f"{BASE}{prefix}/call/{API_NAME}/{event_id}")
    urls.append(f"{BASE}/call/{API_NAME}/{event_id}")
    deadline = time.time() + max_seconds
    last_err = ""
    while time.time() < deadline:
        for url in urls:
            try:
                r = sess.get(url, timeout=15)
            except Exception as exc:
                last_err = str(exc)
                continue
            if r.status_code != 200:
                last_err = f"HTTP {r.status_code}"
                continue
            for line in r.text.splitlines():
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if not payload or payload == "[DONE]":
                    continue
                try:
                    import json as js

                    return js.loads(payload)
                except Exception:
                    continue
        time.sleep(1)
    raise RuntimeError(f"Moe poll timed out ({last_err})")


def _extract_audio_url(arr: List) -> Optional[str]:
    """Find the first audio FileData url in a gradio result array."""
    import json as js

    def walk(node):
        if isinstance(node, dict):
            if node.get("url"):
                return node["url"]
            if node.get("path"):
                return node["path"]
            for v in node.values():
                found = walk(v)
                if found:
                    return found
        elif isinstance(node, list):
            for v in node:
                found = walk(v)
                if found:
                    return found
        elif isinstance(node, str) and node.startswith("http"):
            return node
        return None

    return walk(arr)


def generate_tts(text: str, speaker: Optional[str] = None, speed: float = 1.0, symbol_input: bool = False, **kwargs) -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    text = text.strip()[:900]

    cfg = _load_config() or {}
    spk = speaker or cfg.get("speaker") or "絢地寧々"
    try:
        spd = float(speed) if speed else float(cfg.get("speed", 1.0))
    except Exception:
        spd = 1.0
    sym = bool(symbol_input if symbol_input is not None else cfg.get("symbol", False))

    sess, _ = _session()
    try:
        j = _post_call(sess, [text, spk, spd, sym])
        event_id = j.get("event_id") or j.get("eventId")
        if not event_id:
            if "data" in j:
                arr = j["data"]
                audio = _extract_audio_url(arr)
                if audio:
                    return _download(sess, audio, text, spk)
            return {"status": "error", "error": f"Moe no event_id: {str(j)[:300]}"}

        arr = _poll_result(sess, event_id)
        audio = _extract_audio_url(arr)
        if not audio:
            return {"status": "error", "error": f"Moe result had no audio: {str(arr)[:300]}"}
        return _download(sess, audio, text, spk)
    except Exception as exc:
        logger.exception("moe generate failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass


def _download(sess, audio: str, text: str, spk: str) -> Dict:
    url = audio
    if url.startswith("/"):
        cfg = _load_config() or {}
        prefix = cfg.get("prefix", "")
        # gradio 4.x serves files at {prefix}/file={path}
        url = f"{BASE}{prefix}/file={audio}" if "=" not in audio.split("/")[-1] else f"{BASE}{audio}"
    ar = sess.get(url, timeout=30)
    if ar.status_code != 200 or not ar.content:
        return {"status": "error", "error": f"Moe audio download failed HTTP {ar.status_code}"}
    ext = url.split("?")[0].split(".")[-1].lower()
    mime = "audio/wav" if ext == "wav" else "audio/mpeg"
    b64 = base64.b64encode(ar.content).decode("ascii")
    return {
        "status": "success",
        "provider": "moe",
        "service": "Moe TTS",
        "voice": spk,
        "audioUrl": url,
        "dataUrl": f"data:{mime};base64,{b64}",
        "bytes": len(ar.content),
        "contentType": mime,
        "text": text,
    }


def probe() -> Dict:
    r = generate_tts("Hello world")
    return {"ok": r.get("status") == "success", "result": r}
