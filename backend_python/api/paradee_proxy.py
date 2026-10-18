"""
Paradee TTS Proxy — https://huggingface.co/spaces/sahilmahendrakar/paradee

Kokoro-82M distilled to 8M params (~9 MB weights). Single voice (af_heart),
English, speed 0.5-2.0. Gradio 5 named-endpoint API, verified 2026-10-08:
  POST /gradio_api/call/v2/generate {"text": ..., "speed": ...} -> {"event_id": ...}
  GET  /gradio_api/call/generate/<event_id>  SSE -> event: complete, data: [FileData, phonemes, summary]
FileData.url is an absolute https://...hf.space/gradio_api/file=.../audio.wav (24 kHz).

Long inputs synthesize fine but slowly (~8x realtime, so 2000 chars ~= 27 s);
text is sentence-chunked and the WAV batches are PCM-concatenated, mirroring
the Airy proxy's batching contract (MAX_TEXT / MAX_CHUNKS / batches / durationSec).
"""
from __future__ import annotations

import base64
import io
import logging
import re
import struct
import time
import wave
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE = "https://sahilmahendrakar-paradee.hf.space"
SPACE_ID = "sahilmahendrakar/paradee"
DEFAULT_VOICE = "af_heart"

MODELS = [
    {"id": "paradee/paradee-8m", "name": "Paradee 8M", "maker": "sahilmahendrakar", "params": "8M", "context": "600 chars/batch", "blurb": "Kokoro-82M distilled to 8M · 9MB · ~8x realtime CPU · no signup", "goodAt": "Fast lightweight speech", "capabilities": {"tts": True}},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

CHUNK_TARGET = 600
MAX_CHUNKS = 8
MAX_TEXT = CHUNK_TARGET * MAX_CHUNKS

_WS = re.compile(r"[ \t]+")


def get_models() -> List[Dict]:
    return [{**m, "capabilities": m.get("capabilities", {"tts": True})} for m in MODELS]


def _session():
    try:
        from curl_cffi import requests as creq  # type: ignore

        return creq.Session(impersonate="chrome")
    except Exception:
        import requests as req  # type: ignore

        s = req.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"})
        return s


def _clamp_speed(speed) -> float:
    try:
        sp = float(speed) if speed is not None else 1.0
    except Exception:
        sp = 1.0
    return max(0.5, min(2.0, sp))


def _sentence_ends_here(text: str, i: int) -> Optional[int]:
    if text[i] not in ".!?":
        return None
    j = i + 1
    while j < len(text) and text[j] in "\"')]}":
        j += 1
    if j < len(text) and not text[j].isspace():
        return None
    return j


def _split_sentences(text: str) -> List[str]:
    out, start = [], 0
    for i, _ch in enumerate(text):
        end = _sentence_ends_here(text, i)
        if end is not None:
            piece = text[start:end].strip()
            if piece:
                out.append(piece)
            start = end
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return [s for s in out if s]


def split_chunks(text: str, limit: int = CHUNK_TARGET) -> List[str]:
    chunks: List[str] = []
    current = ""

    def flush() -> None:
        nonlocal current
        if current.strip():
            chunks.append(current.strip())
        current = ""

    for sentence in _split_sentences(text):
        if not sentence:
            continue
        if len(sentence) > limit:
            flush()
            while len(sentence) > limit:
                cut = sentence.rfind(" ", 0, limit)
                if cut <= 0:
                    cut = limit
                chunks.append(sentence[:cut].strip())
                sentence = sentence[cut:].strip()
            if sentence:
                current = sentence
            continue
        need = len(sentence) + (1 if current else 0)
        if len(current) + need > limit:
            flush()
        current = (current + " " + sentence).strip() if current else sentence
    flush()
    return [c for c in chunks if c]


def _read_wav_pcm(data: bytes) -> tuple:
    bio = io.BytesIO(data)
    with wave.open(bio, "rb") as w:
        params = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getcomptype(), w.getcompname())
        frames = w.readframes(w.getnframes())
    return params, frames


def concat_wav(blobs: List[bytes]) -> bytes:
    if not blobs:
        raise ValueError("no wav blobs")
    if len(blobs) == 1:
        return blobs[0]
    ref_params, _ = _read_wav_pcm(blobs[0])
    if ref_params[3] != "NONE":
        raise ValueError("compressed wav unsupported")
    parts = []
    total_frames = 0
    for b in blobs:
        params, frames = _read_wav_pcm(b)
        if params[:3] != ref_params[:3] or params[3] != "NONE":
            raise ValueError(f"wav param mismatch: {params} vs {ref_params}")
        parts.append(frames)
        total_frames += len(frames) // (ref_params[0] * ref_params[1])
    nchannels, sampwidth, framerate, _ct, _cn = ref_params
    bio = io.BytesIO()
    with wave.open(bio, "wb") as w:
        w.setnchannels(nchannels)
        w.setsampwidth(sampwidth)
        w.setframerate(framerate)
        w.writeframes(b"".join(parts))
    return bio.getvalue()


def wav_duration_sec(data: bytes) -> float:
    try:
        (nchannels, sampwidth, framerate, _ct, _cn), frames = _read_wav_pcm(data)
        nframes = len(frames) // max(1, nchannels * sampwidth)
        return nframes / float(framerate or 24000)
    except Exception:
        return 0.0


def _request_chunk(sess, text: str, speed: float, timeout: int = 150) -> bytes:
    r = sess.post(
        f"{BASE}/gradio_api/call/v2/generate",
        json={"text": text, "speed": speed},
        headers={"Origin": BASE, "Referer": BASE + "/"},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Paradee join {r.status_code}: {r.text[:300]}")
    try:
        event_id = r.json().get("event_id")
    except Exception:
        raise RuntimeError(f"Paradee non-JSON join: {r.text[:300]}")
    if not event_id:
        raise RuntimeError("Paradee no event_id")

    # Plain GET like the Kokoro proxy: the server closes the stream after the
    # terminal event, and this curl_cffi version has no iter_content.
    resp = sess.get(
        f"{BASE}/gradio_api/call/generate/{event_id}",
        headers={"Accept": "text/event-stream"},
        timeout=timeout,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Paradee stream {resp.status_code}")
    try:
        body = resp.text
    finally:
        try:
            resp.close()
        except Exception:
            pass
    for msg in body.split("\n\n"):
        if not msg.strip():
            continue
        kind, payload = _parse_sse(msg)
        if kind == "complete":
            url = _extract_file_url(payload)
            if not url:
                raise RuntimeError(f"Paradee completed but no audio: {msg[:300]}")
            return _download(sess, url)
        if kind == "error":
            raise RuntimeError(f"Paradee error: {payload[:300]}")
    raise RuntimeError("Paradee stream ended without completion")


def _parse_sse(msg: str) -> tuple:
    kind, data_lines = "", []
    for line in msg.splitlines():
        if line.startswith("event:"):
            kind = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:].strip())
    return kind, "\n".join(data_lines)


def _extract_file_url(payload: str) -> Optional[str]:
    try:
        import json as js

        data = js.loads(payload)
    except Exception:
        return None
    return _find_audio(data)


def _find_audio(node) -> Optional[str]:
    if isinstance(node, dict):
        url = node.get("url")
        if isinstance(url, str) and url:
            if url.startswith("/"):
                return BASE + url
            if url.startswith("http"):
                return url
        path = node.get("path")
        if isinstance(path, str) and path.endswith((".wav", ".mp3")) and not path.startswith("/tmp"):
            return path if path.startswith("http") else BASE + path
        for v in node.values():
            found = _find_audio(v)
            if found:
                return found
    elif isinstance(node, list):
        for v in node:
            found = _find_audio(v)
            if found:
                return found
    return None


def _download(sess, url: str) -> bytes:
    ar = sess.get(url, timeout=60)
    if ar.status_code != 200 or not ar.content or len(ar.content) < 500:
        raise RuntimeError(f"Paradee download failed {ar.status_code}")
    return bytes(ar.content)


def generate_tts(text: str, voice: Optional[str] = None, speed: float = 1.0, model: str = "paradee/paradee-8m") -> Dict:
    if not text or not text.strip():
        return {"status": "error", "error": "text required"}
    clean = _WS.sub(" ", text.replace("\r", "\n")).strip()
    if len(clean) > MAX_TEXT:
        return {"status": "error", "error": f"text too long for Paradee (max ~{MAX_TEXT} chars)"}
    sp = _clamp_speed(speed)

    chunks = split_chunks(clean)
    if len(chunks) > MAX_CHUNKS:
        return {"status": "error", "error": f"text too long for Paradee ({len(chunks)} batches needed, max {MAX_CHUNKS})"}

    sess = _session()
    try:
        blobs = []
        for i, chunk in enumerate(chunks):
            if i:
                time.sleep(1)
            blobs.append(_request_chunk(sess, chunk, sp))
        audio = concat_wav(blobs)
    except Exception as exc:
        logger.exception("paradee generate failed")
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    finally:
        try:
            sess.close()
        except Exception:
            pass

    b64 = base64.b64encode(audio).decode("ascii")
    return {
        "status": "success",
        "provider": "paradee",
        "service": "Paradee 8M (Kokoro distill)",
        "voice": DEFAULT_VOICE,
        "audioUrl": "",
        "dataUrl": f"data:audio/wav;base64,{b64}",
        "bytes": len(audio),
        "contentType": "audio/wav",
        "batches": len(blobs),
        "durationSec": round(wav_duration_sec(audio), 1),
        "text": clean,
    }


def probe() -> Dict:
    r = generate_tts("Hello from Paradee TTS")
    return {"ok": r.get("status") == "success", "result": r}
