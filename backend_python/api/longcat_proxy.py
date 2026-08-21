"""Proxy for longcat.chat/t anonymous chat (Meituan LongCat, free, no login).

The web app talks to ``/api/v1/chat-completion-oversea-V2`` with a JSON body
carrying the flattened conversation (content + last messages). Requests must
carry an H5guard ``mtgsig`` header plus ``yodaReady/csecplatform/csecversion``
query params; the signature is produced by a tiny Node sidecar
(``h5guard_signer.js``, auto-spawned on demand) that runs the official
H5guard SDK in a headless VM. Responses are SSE lines with ``event.type`` of
``create|content|reason|search|finish|eventError``.

Anti-detection: curl_cffi Chrome TLS impersonation, fresh cookie jar warmed by
a GET of /t, per-identity proxy rotation (LONGCAT_PROXIES env, comma separated)
and exponential backoff on 429/5xx before failing over to the next identity.
"""
import json
import logging
import os
import random
import shutil
import socket
import subprocess
import tempfile
import threading
import time
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

LONGCAT_URL = "https://longcat.chat"
CHAT_ENDPOINT = f"{LONGCAT_URL}/api/v1/chat-completion-oversea-V2"
REQUEST_TIMEOUT = 300
MAX_RETRIES = 3

SIGNER_PORT = int(os.environ.get("H5GUARD_PORT", "8765"))
_SIGNER_LOCK = threading.Lock()
_SIGNER_PROC: Optional[subprocess.Popen] = None

MODELS = [
    {"id": "longcat/LongCat-2.0", "name": "LongCat 2.0 Flash", "reasoning": True, "vision": False,
     "web_search": True, "context_window": 128000},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"

_BROWSER_HEADERS = {
    "accept": "text/event-stream,application/json",
    "accept-language": "en-US",
    "content-type": "application/json",
    "x-requested-with": "XMLHttpRequest",
    "X-Client-Language": "en",
    "m-appkey": "fe_com.sankuai.friday.fe.longcat",
    "origin": LONGCAT_URL,
    "referer": f"{LONGCAT_URL}/t",
    "user-agent": _UA,
}


def get_models() -> List[Dict]:
    return [
        {
            "id": m["id"],
            "name": m["name"],
            "capabilities": {
                "chat": True,
                "stream": True,
                "vision": m.get("vision", False),
                "thinking": m.get("reasoning", False),
                "tools": False,
                "web_search": m.get("web_search", False),
            },
        }
        for m in MODELS
    ]


def _proxies() -> List[Optional[str]]:
    raw = os.environ.get("LONGCAT_PROXIES", "")
    items = [p.strip() for p in raw.split(",") if p.strip()]
    return items or [None]


def _sign_via_sidecar(url: str, method: str, body: str) -> Optional[Dict]:
    try:
        conn = http_post_json("127.0.0.1", SIGNER_PORT, {"url": url, "method": method, "body": body}, timeout=15)
        if conn and "error" not in conn:
            return conn
    except Exception:
        pass
    return None


def http_post_json(host: str, port: int, payload: dict, timeout: float = 15) -> Optional[dict]:
    import http.client

    try:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        body = json.dumps(payload)
        conn.request("POST", "/", body, {"Content-Type": "application/json"})
        resp = conn.getresponse()
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
        conn.close()
        return data
    except Exception:
        return None


def _spawn_signer() -> bool:
    global _SIGNER_PROC
    with _SIGNER_LOCK:
        if _SIGNER_PROC and _SIGNER_PROC.poll() is None:
            return True
        node = shutil.which("node")
        if not node:
            return False
        signer = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h5guard_signer.js")
        if not os.path.exists(signer):
            return False
        try:
            _SIGNER_PROC = subprocess.Popen(
                [node, signer],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=tempfile.gettempdir(),
            )
            deadline = time.time() + 20
            while time.time() < deadline:
                if _signer_alive():
                    return True
                time.sleep(0.4)
        except Exception as exc:
            logger.warning("H5guard signer spawn failed: %s", exc)
        return False


def _signer_alive() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        return s.connect_ex(("127.0.0.1", SIGNER_PORT)) == 0


def _signed_request(url: str, body_str: str) -> Optional[Dict]:
    """Return {'url':..., 'headers': {...}} with mtgsig + csec query params."""
    result = None
    if _signer_alive():
        result = _sign_via_sidecar(url, "POST", body_str)
    if not result and _spawn_signer():
        result = _sign_via_sidecar(url, "POST", body_str)
    if not result or "mtgsig" not in json.dumps(result.get("headers", {})):
        logger.warning("H5guard signing unavailable; falling back to unsigned request")
        return None
    return result


def _build_messages(messages: List[Dict[str, str]], content: str) -> List[Dict]:
    out = []
    for m in messages[-20:]:
        role = m.get("role", "user")
        text = m.get("content", "")
        if not isinstance(text, str) or not text:
            continue
        if role == "user":
            out.append({
                "role": "user",
                "events": [{"type": "userMsg", "content": text[:8000], "status": "FINISHED"}],
                "chatStatus": "FINISHED",
                "messageId": random.randint(10 ** 7, 10 ** 8),
                "idType": "custom",
            })
        elif role == "assistant":
            out.append({
                "role": "assistant",
                "events": [{"type": "content", "content": text[:8000], "status": "FINISHED"}],
                "chatStatus": "FINISHED",
                "messageId": random.randint(10 ** 7, 10 ** 8),
                "idType": "custom",
            })
    out.append({
        "role": "user",
        "events": [{"type": "userMsg", "content": content[:8000], "status": "FINISHED"}],
        "chatStatus": "FINISHED",
        "messageId": random.randint(10 ** 7, 10 ** 8),
        "idType": "custom",
    })
    out.append({
        "role": "assistant",
        "events": [],
        "chatStatus": "LOADING",
        "messageId": random.randint(10 ** 7, 10 ** 8),
        "idType": "custom",
    })
    return out


def _build_body(messages: List[Dict[str, str]], content: str, search_enabled: int = 0) -> Dict:
    return {
        "content": content[:8000],
        "agentId": "1",
        "messages": _build_messages(messages, content),
        "reasonEnabled": 1 if search_enabled else 0,
        "searchEnabled": search_enabled,
        "regenerate": 0,
    }


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "longcat/LongCat-2.0",
    proxy: Optional[str] = None,
) -> Generator[Dict, None, None]:
    if model not in MODEL_MAP:
        yield {"type": "error", "error": f"Unknown model '{model}'"}
        return

    history = [m for m in messages if m.get("role") != "system"]
    system_prefix = ""
    for m in messages:
        if m.get("role") == "system" and isinstance(m.get("content"), str):
            system_prefix = m["content"][:4000]
            break
    content = history[-1].get("content", "") if history else ""
    if system_prefix:
        content = f"{system_prefix}\n\n{content}"[:12000]
    history_wo_last = history[:-1] if history else []

    body = _build_body(history_wo_last, content)
    body_str = json.dumps(body)

    proxies = ([proxy] if proxy else []) or _proxies()
    last_error = "unknown error"

    for attempt in range(MAX_RETRIES):
        proxy_choice = proxies[attempt % len(proxies)]
        session = CurlSession(headers=dict(_BROWSER_HEADERS), impersonate="chrome", timeout=REQUEST_TIMEOUT)
        try:
            signed = _signed_request(CHAT_ENDPOINT, body_str)
            target_url = signed["url"] if signed else CHAT_ENDPOINT
            headers = dict(_BROWSER_HEADERS)
            if signed:
                headers.update(signed["headers"])
            try:
                session.get(f"{LONGCAT_URL}/t", headers={"user-agent": _UA}, timeout=30)
            except Exception:
                pass

            resp = session.post(target_url, data=body_str.encode("utf-8"), headers=headers,
                                stream=True, proxy=proxy_choice)
            if resp.status_code != 200:
                last_error = f"LongCat HTTP {resp.status_code}"
                logger.warning("%s (attempt %d)", last_error, attempt + 1)
                if resp.status_code == 429:
                    time.sleep(2 ** attempt + random.random())
                    continue
                if resp.status_code >= 500:
                    time.sleep(1 + random.random())
                    continue
                yield {"type": "error", "error": last_error}
                return

            saw_any = False
            buffer = ""
            try:
                for chunk_bytes in resp.iter_content():
                    if not chunk_bytes:
                        continue
                    buffer += chunk_bytes.decode("utf-8", errors="replace")
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip("\r")
                        if not line.startswith("data:"):
                            continue
                        raw = line[5:].strip()
                        if not raw:
                            continue
                        try:
                            ev = json.loads(raw)
                        except (json.JSONDecodeError, ValueError):
                            continue
                        event = ev.get("event") or {}
                        etype = event.get("type")
                        if etype == "content":
                            delta = event.get("content") or ""
                            if delta:
                                saw_any = True
                                yield {"type": "text", "content": delta}
                        elif etype in ("reason", "think"):
                            delta = event.get("content") or ""
                            if delta:
                                saw_any = True
                                yield {"type": "thought", "content": delta}
                        elif etype == "finish":
                            usage = event.get("usage") or {}
                            if usage:
                                yield {"type": "usage",
                                       "prompt_tokens": usage.get("inputTokens", 0),
                                       "completion_tokens": usage.get("outputTokens", 0)}
                        elif etype == "eventError":
                            msg = event.get("message") or "upstream error"
                            yield {"type": "error", "error": f"LongCat: {msg}"}
                            return
            except Exception as exc:
                if saw_any:
                    logger.warning("LongCat stream ended after content: %s", exc)
                    break
                last_error = f"stream failed: {exc}"
                continue

            if saw_any:
                yield {"type": "done", "finish_reason": "stop"}
                return
            last_error = "stream ended without content"
        except Exception as exc:
            last_error = f"request failed: {exc}"
            logger.warning("LongCat attempt %d failed: %s", attempt + 1, exc)
            time.sleep(1 + random.random())
        finally:
            try:
                session.close()
            except Exception:
                pass

    yield {"type": "error", "error": f"LongCat: {last_error}"}


def simple_chat(
    user_message: str,
    model: str = "longcat/LongCat-2.0",
    system_prompt: str = "",
    max_tokens: int = 500,
    **kwargs,
) -> Optional[str]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    collected = []
    for chunk in stream_chat(messages=messages, model=model):
        t = chunk.get("type")
        if t == "text":
            collected.append(chunk.get("content", ""))
        elif t == "error":
            logger.error("LongCat simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None


def probe() -> Dict:
    try:
        answer = simple_chat("Reply with the single word OK.", max_tokens=10)
        return {"ok": bool(answer), "answer": answer}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
