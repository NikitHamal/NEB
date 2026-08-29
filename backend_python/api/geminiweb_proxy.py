"""Proxy for gemini.google.com anonymous chat (free Flash-Lite, no login).

Google's Gemini web app allows unsigned visitors to chat with the default
Flash-Lite model. The flow is:

1. ``GET /app`` — collect cookies (NID/COMPASS) and parse WIZ_global_data for
   ``FdrFJe`` (f.sid) and the current ``bl`` build id.
2. ``POST /_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate``
   with form-encoded ``f.req=[null,"<inner-json>"]``. The inner JSON carries
   the prompt, locale and an empty conversation token (anonymous chats do not
   need the big client-side state blob).
3. The response is a ``)]}'``-prefixed stream of length-prefixed JSON chunks;
   answer text lives in nested ``rc_*`` arrays, conversation/response ids in
   ``c_*/r_*`` pairs (kept per session for multi-turn context).

Anti-detection: curl_cffi Chrome TLS impersonation, fresh cookie jar per
identity, proxy rotation via GEMINIWEB_PROXIES env and exponential backoff on
429/5xx before failing over to the next identity.
"""
import json
import logging
import os
import random
import re
import time
import urllib.parse
import uuid
from typing import Dict, Generator, List, Optional

from curl_cffi.requests import Session as CurlSession

logger = logging.getLogger(__name__)

BASE_URL = "https://gemini.google.com"
APP_PATH = "/app"
STREAM_ENDPOINT = "/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
REQUEST_TIMEOUT = 300
MAX_RETRIES = 3

MODELS = [
    {"id": "geminiweb/gemini-flash-lite", "name": "Gemini Flash Lite (Web)", "reasoning": False,
     "vision": False, "web_search": True, "context_window": 32000},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"


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
    raw = os.environ.get("GEMINIWEB_PROXIES", "")
    items = [p.strip() for p in raw.split(",") if p.strip()]
    return items or [None]


class _GeminiSession:
    """One warmed browser identity: cookies + f.sid + bl."""

    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy
        self.session = CurlSession(impersonate="chrome", timeout=REQUEST_TIMEOUT)
        self.fsid = ""
        self.bl = "boq_assistant-bard-web-server_20260827.05_p0"
        self.conversation_id = ""
        self.response_id = ""
        self.reqid = random.randint(100000, 999999)
        self.warmed = False

    def warm(self) -> bool:
        try:
            resp = self.session.get(
                BASE_URL + APP_PATH,
                headers={"user-agent": _UA, "accept": "text/html"},
                proxy=self.proxy,
                timeout=60,
            )
            if resp.status_code != 200:
                logger.warning("GeminiWeb warm GET failed: %s", resp.status_code)
                return False
            html = resp.text
            m = re.search(r'"FdrFJe":"([0-9\-]+)"', html)
            if m:
                self.fsid = m.group(1)
            m = re.search(r"(boq_assistant-bard-web-server_[0-9._p]+)", html)
            if m:
                self.bl = m.group(1)
            m = re.search(r'"SNlM0e":"([^"]+)"', html)
            self._snlm0e = m.group(1) if m else ""
            self.warmed = bool(self.fsid)
            if not self.fsid:
                logger.warning("GeminiWeb warm: FdrFJe not found")
            return self.warmed
        except Exception as exc:
            logger.warning("GeminiWeb warm error: %s", exc)
            return False

    def _build_inner(self, prompt: str) -> str:
        ctx_part = [self.conversation_id, self.response_id] if self.conversation_id else []
        return json.dumps([
            [prompt, 0, None, None, None, None, 0],
            ["en-US"],
            ["", "", "", None, None, None, None, None, None, ""],
            "",
            uuid.uuid4().hex,
            None,
            [0],
            1,
            None,
            None,
            1,
            0,
        ] + ([ctx_part] if False else []))

    def send(self, prompt: str) -> Generator[Dict, None, None]:
        self.reqid += 100000
        inner = self._build_inner(prompt)
        freq = json.dumps([None, inner])
        url = (
            f"{BASE_URL}{STREAM_ENDPOINT}?bl={self.bl}&f.sid={self.fsid}"
            f"&hl=en-US&_reqid={self.reqid}&rt=c"
        )
        snlm0e = getattr(self, '_snlm0e', '')
        if snlm0e:
            url += f"&at={urllib.parse.quote(snlm0e, safe='')}"
        headers = {
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "origin": BASE_URL,
            "referer": f"{BASE_URL}/",
            "user-agent": _UA,
            "x-same-domain": "1",
        }
        resp = self.session.post(
            url,
            data=f"f.req={urllib.parse.quote(freq, safe='')}&".encode("utf-8"),
            headers=headers,
            proxy=self.proxy,
            stream=True,
        )
        if resp.status_code != 200:
            txt = ""
            try:
                txt = resp.text[:500] if hasattr(resp, 'text') else ""
            except Exception:
                pass
            if "400" in txt or resp.status_code == 400:
                yield {"type": "error", "error": "GeminiWeb rejected the request (400). Retrying may help; if persistent the page format may have changed."}
            else:
                yield {"type": "error", "error": f"GeminiWeb HTTP {resp.status_code}: {txt[:300]}"}
            return

        buffer = b""
        saw_any = False
        prev_text = ""
        try:
            for chunk in resp.iter_content():
                if not chunk:
                    continue
                buffer += chunk
                text = buffer.decode("utf-8", errors="replace")
                while "\n" in text:
                    line, text = text.split("\n", 1)
                    line = line.strip("\r")
                    if not line or line.startswith(")]}'"):
                        continue
                    if line.isdigit():
                        continue
                    if not line.startswith("["):
                        continue
                    for ev in self._parse_chunk(line):
                        if ev.get("type") == "text":
                            snap = ev["content"]
                            if snap.startswith(prev_text):
                                delta = snap[len(prev_text):]
                            elif not prev_text:
                                delta = snap
                            else:
                                delta = ""
                            prev_text = snap if len(snap) > len(prev_text) else prev_text
                            if delta:
                                saw_any = True
                                yield {"type": "text", "content": delta}
                        else:
                            yield ev
                buffer = text.encode("utf-8", errors="replace")
        except Exception as exc:
            if not saw_any:
                yield {"type": "error", "error": f"GeminiWeb stream failed: {exc}"}
                return

        if not saw_any:
            yield {"type": "error", "error": "GeminiWeb stream ended without content"}
            return
        yield {"type": "done", "finish_reason": "stop"}

    def _parse_chunk(self, line: str) -> List[Dict]:
        out: List[Dict] = []
        try:
            arr = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            return out
        if not isinstance(arr, list):
            return out
        for entry in arr:
            if not isinstance(entry, list) or not entry or entry[0] != "wrb.fr":
                continue
            inner_raw = entry[2] if len(entry) > 2 else None
            if not isinstance(inner_raw, str):
                continue
            try:
                inner = json.loads(inner_raw)
            except (json.JSONDecodeError, ValueError):
                continue
            if not isinstance(inner, list) or len(inner) < 5:
                continue
            ids = inner[1]
            if isinstance(ids, list) and len(ids) >= 2:
                cid, rid = ids[0], ids[1]
                if isinstance(cid, str) and cid.startswith("c_"):
                    self.conversation_id = cid
                if isinstance(rid, str) and rid.startswith("r_"):
                    self.response_id = rid
            body = inner[4]
            if not isinstance(body, list):
                continue
            for part in body:
                if isinstance(part, list) and part and isinstance(part[0], str) and part[0].startswith("rc_"):
                    texts = part[1]
                    if isinstance(texts, list):
                        best = ""
                        for t in texts:
                            if isinstance(t, str) and len(t) > len(best):
                                best = t
                        if best.strip():
                            out.append({"type": "text", "content": best})
        return out

    def close(self):
        try:
            self.session.close()
        except Exception:
            pass


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "geminiweb/gemini-flash-lite",
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
    prompt = history[-1].get("content", "") if history else ""
    if system_prefix:
        prompt = f"{system_prefix}\n\n{prompt}"[:12000]
    # Anonymous web chat has no reliable server-side history replay; include a
    # compact transcript so multi-turn prompts keep their context.
    if len(history) > 1:
        transcript = []
        for m in history[:-1][-10:]:
            role = "User" if m.get("role") == "user" else "Assistant"
            content = m.get("content", "")
            if isinstance(content, str) and content.strip():
                transcript.append(f"{role}: {content[:2000]}")
        if transcript:
            prompt = "Previous conversation:\n" + "\n".join(transcript) + f"\n\nUser: {prompt}"

    proxies = ([proxy] if proxy else []) or _proxies()
    last_error = "unknown error"

    for attempt in range(MAX_RETRIES):
        proxy_choice = proxies[attempt % len(proxies)]
        gsession = _GeminiSession(proxy=proxy_choice)
        try:
            if not gsession.warm():
                last_error = "could not warm session (page fetch failed)"
                continue
            got_error = None
            for ev in gsession.send(prompt):
                if ev.get("type") == "error":
                    got_error = ev.get("error")
                    break
                yield ev
            if got_error is None:
                return
            last_error = got_error
            if "429" in got_error or "HTTP 5" in got_error:
                time.sleep(2 ** attempt + random.random())
                continue
            if "400" in got_error and attempt == 0:
                time.sleep(1 + random.random())
                continue
            yield {"type": "error", "error": got_error}
            return
        except Exception as exc:
            last_error = f"request failed: {exc}"
            logger.warning("GeminiWeb attempt %d failed: %s", attempt + 1, exc)
            time.sleep(1 + random.random())
        finally:
            gsession.close()

    yield {"type": "error", "error": f"GeminiWeb: {last_error}"}


def simple_chat(
    user_message: str,
    model: str = "geminiweb/gemini-flash-lite",
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
            logger.error("GeminiWeb simple_chat error: %s", chunk.get("error"))
            return None
    return "".join(collected) or None


def probe() -> Dict:
    try:
        answer = simple_chat("Reply with the single word OK.", max_tokens=10)
        return {"ok": bool(answer), "answer": answer}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
