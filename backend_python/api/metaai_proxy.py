import json
import logging
import os
import re
import time
from typing import Any, Dict, Generator, List, Optional, Set, Tuple

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

MODELS = [
    {"id": "metaai-instant", "name": "Meta AI (Instant)", "reasoning": False, "vision": False, "web_search": True},
    {"id": "metaai-thinking", "name": "Meta AI (Thinking)", "reasoning": True, "vision": False, "web_search": True},
    {"id": "metaai-imagine", "name": "Meta AI Imagine (Image)", "reasoning": False, "vision": False, "web_search": False},
]

MODEL_MAP = {m["id"]: m for m in MODELS}

_BROWSER_SESSION = None


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


def _get_cookies() -> Dict[str, str]:
    datr = getattr(settings, "META_AI_DATR", "") or os.getenv("META_AI_DATR", "")
    ecto = getattr(settings, "META_AI_ECTO_1_SESS", "") or os.getenv("META_AI_ECTO_1_SESS", "")
    abra = getattr(settings, "META_AI_ABRA_SESS", "") or os.getenv("META_AI_ABRA_SESS", "")
    cookies = {}
    if datr:
        cookies["datr"] = datr
    if ecto:
        cookies["ecto_1_sess"] = ecto
    if abra:
        cookies["abra_sess"] = abra
    return cookies


def _get_access_token() -> str:
    token = getattr(settings, "META_AI_ACCESS_TOKEN", "") or os.getenv("META_AI_ACCESS_TOKEN", "")
    if token.startswith("ecto1:"):
        token = token[6:]
    return token


class _MetaAIPlaywrightSession:
    def __init__(self, cookies: Dict[str, str]):
        self.cookies = cookies
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.ready = False

    def start(self):
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )
        cookie_list = []
        for k, v in self.cookies.items():
            cookie_list.append({"name": k, "value": v, "domain": ".meta.ai", "path": "/"})
        if cookie_list:
            self.context.add_cookies(cookie_list)

        self.page = self.context.new_page()
        self.page.goto("https://www.meta.ai/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        self._dismiss_overlays()
        self.ready = True

    def _dismiss_overlays(self):
        for text in ["Dismiss", "Connect", "Accept all", "Accept", "Got it", "Close", "OK"]:
            try:
                btn = self.page.query_selector(f'button:has-text("{text}")')
                if btn and btn.is_visible():
                    btn.click()
                    time.sleep(0.5)
            except Exception:
                pass

    def prompt(self, message: str, thinking: bool = False, timeout: int = 90) -> Generator[Dict, None, None]:
        if not self.ready or not self.page:
            self.start()

        self._dismiss_overlays()

        typed = False
        selectors = [
            'textarea[data-testid="composer-input"]',
            'div[data-testid="composer-input"] [contenteditable]',
            'div[contenteditable="true"]',
            'textarea[placeholder*="Ask Meta"]',
            '[role="textbox"]',
            'textarea',
        ]
        for sel in selectors:
            try:
                el = self.page.query_selector(sel)
                if el:
                    el.scroll_into_view_if_needed(timeout=3000)
                    el.click(timeout=3000)
                    self.page.keyboard.type(message, delay=15)
                    time.sleep(0.3)
                    self.page.keyboard.press("Enter")
                    typed = True
                    break
            except Exception:
                continue

        if not typed:
            try:
                self.page.evaluate(f"""
                    () => {{
                        const ta = document.querySelector('textarea, [contenteditable="true"], [role="textbox"]');
                        if (ta) {{
                            ta.focus();
                            if (ta.tagName === 'TEXTAREA' || ta.tagName === 'INPUT') {{
                                ta.value = {json.dumps(message)};
                            }} else {{
                                ta.innerText = {json.dumps(message)};
                            }}
                            ta.dispatchEvent(new Event('input', {{bubbles: true}}));
                        }}
                    }}
                """)
                time.sleep(0.3)
                self.page.keyboard.press("Enter")
                typed = True
            except Exception as exc:
                yield {"type": "error", "error": f"Failed to input message: {exc}"}
                return

        last_len = 0
        stable_count = 0
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(0.5)
            text = self._extract_text()
            if text:
                if len(text) > last_len:
                    delta = text[last_len:]
                    last_len = len(text)
                    stable_count = 0
                    yield {"type": "text", "content": delta}
                elif len(text) == last_len and len(text) > 0:
                    stable_count += 1
                    if stable_count >= 6:
                        break
        yield {"type": "done"}

    def _extract_text(self) -> str:
        try:
            return self.page.evaluate("""
                () => {
                    const selectors = [
                        '[data-testid="agent-message"]',
                        '[data-testid="message-content"]',
                        '[class*="assistant-message"]',
                        '[class*="bot-message"]',
                        'div[role="region"] [class*="bubble"]',
                        'div[class*="markdown"]'
                    ];
                    for (const sel of selectors) {
                        const msgs = document.querySelectorAll(sel);
                        if (msgs.length > 0) {
                            const last = msgs[msgs.length - 1];
                            const t = last.textContent?.trim();
                            if (t) return t;
                        }
                    }
                    const articles = document.querySelectorAll('article, [role="article"]');
                    if (articles.length > 0) {
                        return articles[articles.length - 1].textContent?.trim() || '';
                    }
                    return '';
                }
            """) or ""
        except Exception:
            return ""

    def close(self):
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass
        self.ready = False


def _stream_direct_llama(messages: List[Dict[str, str]], model: str = "metaai-instant") -> Generator[Dict, None, None]:
    try:
        from api import k2think_proxy
        yield from k2think_proxy.stream_chat(messages, model="MBZUAI-IFM/K2-Think-v2")
    except Exception as exc:
        yield {"type": "error", "error": str(exc)}


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "metaai-instant",
) -> Generator[Dict, None, None]:
    cookies = _get_cookies()
    if os.getenv("META_AI_USE_BROWSER") == "1" and cookies.get("datr") and cookies.get("ecto_1_sess"):
        global _BROWSER_SESSION
        if _BROWSER_SESSION is None or not _BROWSER_SESSION.ready:
            try:
                _BROWSER_SESSION = _MetaAIPlaywrightSession(cookies)
                _BROWSER_SESSION.start()
            except Exception as exc:
                _BROWSER_SESSION = None

        if _BROWSER_SESSION and _BROWSER_SESSION.ready:
            last_msg = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
            if isinstance(last_msg, list):
                last_msg = "".join(str(p.get("text", "")) if isinstance(p, dict) else str(p) for p in last_msg)
            thinking = model == "metaai-thinking"
            try:
                for chunk in _BROWSER_SESSION.prompt(str(last_msg), thinking=thinking):
                    yield chunk
                return
            except Exception as exc:
                try:
                    _BROWSER_SESSION.close()
                except Exception:
                    pass
                _BROWSER_SESSION = None

    yield from _stream_direct_llama(messages, model=model)


def simple_chat(
    user_message: str,
    model: str = "metaai-instant",
    system_prompt: str = "",
    max_tokens: int = 4000,
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
            logger.error("Meta AI error: %s", chunk.get("error"))
    return "".join(collected) or None


def generate_image(prompt: str, timeout: int = 90) -> List[str]:
    cookies = _get_cookies()
    if not (cookies.get("datr") and cookies.get("ecto_1_sess")):
        return []
    global _BROWSER_SESSION
    if _BROWSER_SESSION is None or not _BROWSER_SESSION.ready:
        try:
            _BROWSER_SESSION = _MetaAIPlaywrightSession(cookies)
            _BROWSER_SESSION.start()
        except Exception:
            return []
    if not (_BROWSER_SESSION and _BROWSER_SESSION.ready):
        return []

    try:
        # Prompt imagine
        imagine_prompt = f"/imagine {prompt}" if not prompt.startswith("/imagine") else prompt
        for _ in _BROWSER_SESSION.prompt(imagine_prompt, timeout=timeout):
            pass
        # Extract images
        image_urls = []
        elements = _BROWSER_SESSION.page.query_selector_all('img[src]')
        for el in elements:
            src = el.get_attribute('src') or ''
            if 'fbcdn' in src and ('scontent' in src or 'lookaside' in src):
                if src not in image_urls:
                    image_urls.append(src)
        return image_urls
    except Exception as exc:
        logger.error("Meta AI image generation failed: %s", exc)
        return []
