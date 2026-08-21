import base64
import json
import logging
import random
import time
import uuid
from typing import Any, Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

DOCS_HOST = "https://docs.tembo.io"
SUBDOMAIN = "test-8862363a"
CONFIG_URL = f"{DOCS_HOST}/_mintlify/assistant/siteconfig"
MESSAGE_URL = f"{DOCS_HOST}/_mintlify/api-public/assistant/{SUBDOMAIN}/message"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
]


class TemboProvider:
    def __init__(self, subdomain: str = SUBDOMAIN):
        self.subdomain = subdomain
        self.trust_token: Optional[str] = None
        self.expires_at: int = 0
        self.thread_key = str(uuid.uuid4())
        self.thread_id = str(uuid.uuid4())

    def _get_headers(self) -> Dict[str, str]:
        ua = random.choice(USER_AGENTS)
        return {
            "User-Agent": ua,
            "Origin": DOCS_HOST,
            "Referer": f"{DOCS_HOST}/",
            "Content-Type": "application/json",
            "Accept": "text/event-stream, */*",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

    def _fetch_trust_token(self) -> Optional[str]:
        try:
            r = requests.get(CONFIG_URL, headers=self._get_headers(), timeout=10)
            if r.status_code == 200 and r.text.strip():
                self.trust_token = r.text.strip()
                try:
                    parts = self.trust_token.split(".")
                    if len(parts) >= 2:
                        payload_b64 = parts[1] + "=="
                        payload = json.loads(base64.b64decode(payload_b64.replace("-", "+").replace("_", "/")).decode())
                        self.expires_at = payload.get("exp", 0)
                except Exception:
                    self.expires_at = int(time.time()) + 3600
                return self.trust_token
        except Exception as exc:
            logger.warning(f"[TemboProvider] siteconfig fetch failed: {exc}")
        return None

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "tembo-assistant",
    ) -> Generator[Dict[str, Any], None, None]:
        if not self.trust_token or time.time() > (self.expires_at - 60):
            self._fetch_trust_token()

        formatted_messages = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role in ("user", "assistant", "system"):
                formatted_messages.append({"role": "user" if role == "system" else role, "content": content})

        body: Dict[str, Any] = {
            "messages": formatted_messages,
            "fp": self.subdomain,
            "threadId": self.thread_id,
            "threadKey": self.thread_key,
            "currentPath": "/",
        }
        if self.trust_token:
            body["_"] = self.trust_token

        headers = self._get_headers()

        try:
            resp = requests.post(MESSAGE_URL, headers=headers, json=body, stream=True, timeout=(10, 60))
            if resp.status_code == 200:
                for line in resp.iter_lines():
                    if not line:
                        continue
                    line_str = line.decode("utf-8", errors="replace") if isinstance(line, bytes) else line
                    if line_str.startswith("0:"):
                        try:
                            token = json.loads(line_str[2:])
                            if token:
                                yield {"type": "text", "content": token}
                        except Exception:
                            pass
                yield {"type": "done"}
                return
            else:
                # If HTTP error, try Playwright backend fallback
                try:
                    from api.tembo_proxy import _get_session
                    session = _get_session()
                    prompt = messages[-1].get("content", "") if messages else "Hello"
                    for token in session.stream_query(prompt):
                        yield {"type": "text", "content": token}
                    yield {"type": "done"}
                    return
                except Exception:
                    yield {"type": "error", "error": f"Tembo Assistant HTTP {resp.status_code}: {resp.text[:150]}"}
        except Exception as exc:
            yield {"type": "error", "error": f"Tembo Assistant stream exception: {exc}"}


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "tembo-assistant",
) -> Generator[Dict[str, Any], None, None]:
    provider = TemboProvider()
    yield from provider.stream_chat(messages, model=model)
