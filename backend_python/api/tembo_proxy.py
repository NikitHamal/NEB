import json
import logging
import os
import queue
import sys
import threading
import time
from typing import Any, Dict, Generator, List, Optional

logger = logging.getLogger(__name__)

DOCS_HOST = "https://docs.tembo.io"
SUBDOMAIN = "test-8862363a"


class _TemboPlaywrightSession:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.ready = False
        self.lock = threading.Lock()

    def start(self):
        try:
            if sys.platform == "win32":
                import asyncio
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                except Exception:
                    pass
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            self.context = self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
            )
            self.page = self.context.new_page()
            self.page.goto(f"{DOCS_HOST}/", wait_until="networkidle", timeout=30000)
            self._ensure_assistant_open()
            self.ready = True
            logger.info("[TemboProxy] Playwright session initialized successfully.")
        except Exception as exc:
            logger.exception("[TemboProxy] Failed to initialize Playwright session: %s", exc)
            self.ready = False

    def _ensure_assistant_open(self):
        if not self.page.locator("textarea:visible").count():
            btn = self.page.locator("button:has-text('Assistant'), button[aria-label*='assistant' i]").first
            if btn.count():
                btn.click()
                try:
                    self.page.locator("textarea:visible").first.wait_for(state="visible", timeout=5000)
                except Exception:
                    pass

    def query(self, prompt: str) -> str:
        with self.lock:
            if not self.ready or not self.page or self.page.is_closed():
                self.start()
            if not self.ready or not self.page:
                return "[Error: Tembo Assistant session could not be established]"

            stream_q: queue.Queue = queue.Queue()

            def on_res(res):
                if "api-public/assistant" in res.url and res.status == 200:
                    try:
                        raw = res.body()
                        lines = raw.decode("utf-8", errors="replace").split("\n")
                        tokens = []
                        for l in lines:
                            if l.startswith("0:"):
                                try:
                                    tokens.append(json.loads(l[2:]))
                                except Exception:
                                    pass
                        ans = "".join(tokens)
                        stream_q.put(ans)
                    except Exception as e:
                        logger.warning("[TemboProxy] Body read error: %s", e)
                        stream_q.put("")

            self.page.on("response", on_res)

            try:
                self._ensure_assistant_open()

                txt = self.page.locator("textarea:visible").first
                txt.fill(prompt, force=True)
                time.sleep(0.2)
                txt.press("Enter")

                send_btn = self.page.locator(".chat-assistant-send-button").first
                if send_btn.count():
                    try:
                        send_btn.click(force=True, timeout=500)
                    except Exception:
                        pass

                try:
                    ans = stream_q.get(timeout=18)
                    return ans or "[No response generated]"
                except queue.Empty:
                    # Fallback to DOM evaluation
                    ans = self.page.evaluate("""() => {
                        const msgs = document.querySelectorAll('.markdown-rendered, [data-message-id]');
                        return msgs.length ? msgs[msgs.length - 1].innerText : '';
                    }""")
                    return ans or "[No response generated]"
            except Exception as exc:
                logger.exception("[TemboProxy] Query error: %s", exc)
                return f"[Tembo error: {exc}]"
            finally:
                try:
                    self.page.remove_listener("response", on_res)
                except Exception:
                    pass


_SESSION: Optional[_TemboPlaywrightSession] = None
_SESSION_INIT_LOCK = threading.Lock()


def _get_session() -> _TemboPlaywrightSession:
    global _SESSION
    if _SESSION is None:
        with _SESSION_INIT_LOCK:
            if _SESSION is None:
                _SESSION = _TemboPlaywrightSession()
                _SESSION.start()
    return _SESSION


def stream_chat(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None,
) -> Generator[Dict[str, Any], None, None]:
    session = _get_session()

    parts = []
    if system_prompt:
        parts.append(f"[System Instructions]\n{system_prompt}\n[End Instructions]\n")

    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system" and not system_prompt:
            parts.append(f"[System Instruction]\n{content}\n")
        elif role == "user":
            parts.append(f"User: {content}\n")
        elif role == "assistant":
            parts.append(f"Assistant: {content}\n")

    user_query = parts[-1] if parts else "Hello"
    full_prompt = "".join(parts) if len(parts) > 1 else user_query

    answer = session.query(full_prompt)
    if answer.startswith("[Error:") or answer.startswith("[Tembo error:"):
        yield {"type": "error", "error": answer}
        return
    yield {"type": "text", "content": answer}
    yield {"type": "done"}


def simple_chat(user_message: str, system_prompt: Optional[str] = None) -> str:
    full_text = ""
    messages = [{"role": "user", "content": user_message}]
    for chunk in stream_chat(messages, system_prompt=system_prompt):
        if chunk.get("type") == "text":
            full_text += chunk.get("content", "")
        elif chunk.get("type") == "error":
            logger.warning("[TemboProxy] simple_chat error: %s", chunk.get("error"))
            break
    return full_text.strip()
