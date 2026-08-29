"""
QwenFast proxy — reverse of https://qwenfast-demo.vercel.app

Vercel demo wraps a JarvisLabs notebook:
  GET  /api/metrics -> {ok, running, waiting, lifetimeTps, perStreamTps, specAcceptLength, ...}
  GET  /api/chat    -> {ok, base: "https://<hash>.notebooksn.jarvislabs.net", ms:0}
  POST /api/chat    -> OpenAI-compatible SSE streaming
     Body: {messages: [{role, content}, ...]}
     Headers: Content-Type: application/json + Origin/Referer: https://qwenfast-demo.vercel.app
     Response: text/event-stream with lines like
       data: {"id":"chatcmpl-...","choices":[{"delta":{"role":"assistant","content":"Hello"},"finish_reason":null}]}
       data: {"choices":[{"delta":{"content":"!"}}]}
       data: [DONE]

The demo is Qwen3.8-27B with speculative decoding (specAcceptLength ~2.94, ~49 t/s per stream).
No API key, just Origin check. Superfast.
"""
import json
import logging
import time
import requests

logger = logging.getLogger(__name__)

QWENFAST_URL = "https://qwenfast-demo.vercel.app/api/chat"
QWENFAST_METRICS_URL = "https://qwenfast-demo.vercel.app/api/metrics"

DEFAULT_MODEL = "qwen3.8-27b"
MODELS = [
    {"id": "qwen3.8-27b", "label": "Qwen 3.8 27B (Fast)", "note": "World's fastest Qwen3.8-27B · speculative decoding · ~49 t/s"},
]

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
    "Origin": "https://qwenfast-demo.vercel.app",
    "Referer": "https://qwenfast-demo.vercel.app/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/136.0.0.0 Safari/537.36",
}

TIMEOUT = 60


def _build_messages(system_prompt, user_message):
    msgs = []
    if system_prompt and system_prompt.strip():
        msgs.append({"role": "system", "content": system_prompt.strip()})
    msgs.append({"role": "user", "content": user_message})
    return msgs


def _parse_sse_response(response):
    """Yield content deltas from Vercel SSE."""
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if not data or data == "[DONE]":
            continue
        try:
            obj = json.loads(data)
        except Exception:
            continue
        choices = obj.get("choices") or []
        if not choices:
            continue
        delta = choices[0].get("delta") or {}
        content = delta.get("content")
        if content:
            yield content
        if choices[0].get("finish_reason"):
            break


def simple_chat(user_message, model=DEFAULT_MODEL, system_prompt="", max_tokens=800, timeout=TIMEOUT):
    """Blocking call — returns full text or None."""
    messages = _build_messages(system_prompt, user_message)
    body = {"messages": messages}
    if max_tokens:
        body["max_tokens"] = max_tokens
    try:
        resp = requests.post(QWENFAST_URL, json=body, headers=HEADERS, timeout=timeout, stream=True)
        if resp.status_code != 200:
            try:
                logger.warning(f"qwenfast: status {resp.status_code} {resp.text[:500]}")
            except Exception:
                pass
            return None
        parts = []
        for chunk in _parse_sse_response(resp):
            parts.append(chunk)
        text = "".join(parts).strip()
        if not text:
            logger.warning("qwenfast: empty response")
            return None
        logger.info(f"qwenfast: got {len(text)} chars")
        return text
    except Exception as e:
        logger.warning(f"qwenfast call failed: {e}")
        return None


def stream_chat(user_message, model=DEFAULT_MODEL, system_prompt="", max_tokens=800, timeout=TIMEOUT):
    """Generator yielding content chunks."""
    messages = _build_messages(system_prompt, user_message)
    body = {"messages": messages}
    if max_tokens:
        body["max_tokens"] = max_tokens
    try:
        resp = requests.post(QWENFAST_URL, json=body, headers=HEADERS, timeout=timeout, stream=True)
        if resp.status_code != 200:
            yield f"[error {resp.status_code}]"
            return
        for chunk in _parse_sse_response(resp):
            yield chunk
    except Exception as e:
        logger.warning(f"qwenfast stream failed: {e}")
        yield ""


def fetch_metrics(timeout=10):
    try:
        r = requests.get(QWENFAST_METRICS_URL, headers={"Accept":"application/json"}, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        logger.debug(f"qwenfast metrics failed: {e}")
    return None
