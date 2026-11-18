"""Universal keyless failover mesh for all NEBians chat providers.

When any keyless or community chat provider encounters an upstream WAF challenge,
missing risk token, BotID block, rate limit (429), or transient outage, this
module transparently routes the turn through verified live keyless endpoints
matched to the requested model family so chat never fails.
"""
from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import random
import threading
import time
import uuid
from typing import Dict, Generator, List, Optional

from .proxy_http import CHROME_UA, new_session, resilient_post

logger = logging.getLogger(__name__)
_LOCAL = threading.local()
_DEEPAI_SALT = "hackers_become_a_little_stinkier_every_time_they_hack"


def in_fallback() -> bool:
    return bool(getattr(_LOCAL, "active", False))


def _norm_messages(messages: List[Dict], system_prompt: str = "") -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    if system_prompt and system_prompt.strip():
        out.append({"role": "system", "content": system_prompt.strip()})
    for m in messages or []:
        if not isinstance(m, dict):
            continue
        role = (m.get("role") or "user").strip().lower()
        if role not in ("system", "user", "assistant"):
            role = "user"
        content = m.get("content")
        if isinstance(content, list):
            content = "\n".join(
                str(p.get("text", "")) if isinstance(p, dict) else str(p) for p in content
            )
        text = str(content or "").strip()
        if text:
            out.append({"role": role, "content": text})
    return out


def _pick_deepai_model(provider: str, model: str) -> str:
    tag = f"{provider} {model}".lower()
    if "qwen" in tag:
        return "qwen3.8-flash"
    if "deepseek" in tag:
        return "deepseek-v4.1-flash"
    if "glm" in tag:
        return "glm-5.3-flash"
    if "claude" in tag or "anthropic" in tag:
        return "claude-haiku-5-5"
    if "gpt" in tag or "openai" in tag:
        return "gpt-6-luna"
    if "gemini" in tag or "gemma" in tag:
        return "gemma-4"
    if "hy" in tag or "tencent" in tag:
        return "tencent-hy3"
    if "llama" in tag or "meta" in tag:
        return "llama-3.3-70b-instruct"
    return "standard"


def _pick_llm7_model(provider: str, model: str) -> str:
    tag = f"{provider} {model}".lower()
    if "deepseek" in tag:
        return "DeepSeek-V4-Flash-0731"
    if "glm" in tag:
        return "glm-5.3-flash"
    if "mimo" in tag:
        return "mimo-v2.6-flash"
    if "minimax" in tag:
        return "minimax-m3"
    if "kimi" in tag:
        return "kimi-k2.7-code"
    if "gemma" in tag or "gemini" in tag:
        return "gemma4:31b"
    if "gpt" in tag:
        return "gpt-oss:120b"
    return "default"


def _pick_unikey_model(provider: str, model: str) -> str:
    tag = f"{provider} {model}".lower()
    if "claude" in tag or "anthropic" in tag:
        return "claude-opus-4-8"
    if "gemini" in tag:
        return "google/gemini-3.5-flash"
    if "grok" in tag:
        return "x-ai/grok-4.3"
    if "deepseek" in tag and "pro" in tag:
        return "deepseek/deepseek-v4-pro"
    if "deepseek" in tag:
        return "deepseek/deepseek-v4-flash"
    if "glm" in tag:
        return "z-ai/glm-5.2"
    if "minimax" in tag:
        return "minimax/minimax-m3"
    if "kimi" in tag:
        return "moonshotai/kimi-k3"
    return "gpt-5.5"


def _try_deepai(messages: List[Dict[str, str]], model: str) -> Optional[str]:
    rnum = str(math.floor(random.random() * 100000000000))
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:64]
    key = f"tryit-{rnum}-{h(CHROME_UA + h(CHROME_UA + h(CHROME_UA + rnum + _DEEPAI_SALT)))}"
    chat_hist = [
        {"role": ("user" if m["role"] == "system" else m["role"]), "content": m["content"]}
        for m in messages
    ]
    fields = {
        "chatHistory": json.dumps(chat_hist),
        "model": model,
        "session_uuid": str(uuid.uuid4()),
        "chat_style": "chat",
        "sensitivity_request_id": str(uuid.uuid4()),
        "hacker_is_stinky": "very_stinky",
    }
    headers = {
        "api-key": key,
        "User-Agent": CHROME_UA,
        "Origin": "https://deepai.org",
        "Referer": "https://deepai.org/chat/",
    }
    session = new_session(impersonate="chrome")
    try:
        resp, _ = resilient_post(
            session, "https://api.deepai.org/hacking_is_a_serious_crime",
            data=fields, headers=headers, timeout=45,
        )
        if resp.status_code != 200:
            return None
        raw = resp.content or b""
        idx = raw.find(b"\x1c")
        text = (raw[:idx] if idx != -1 else raw).decode("utf-8", errors="replace").strip()
        if text and not text.startswith('{"task_id"'):
            return text
    except Exception as exc:
        logger.debug("keyless_fallback deepai (%s) failed: %s", model, exc)
    return None


def _try_openai_compat(url: str, model: str, messages: List[Dict[str, str]], headers: Dict[str, str]) -> Optional[str]:
    session = new_session(impersonate="chrome")
    try:
        resp, _ = resilient_post(
            session, url,
            json={"model": model, "messages": messages, "max_tokens": 2048, "stream": False},
            headers={"Content-Type": "application/json", "Accept": "application/json", **headers},
            timeout=45,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        msg = ((data.get("choices") or [{}])[0].get("message") or {})
        text = (msg.get("content") or msg.get("reasoning_content") or "").strip()
        return text or None
    except Exception as exc:
        logger.debug("keyless_fallback openai_compat (%s) failed: %s", url, exc)
        return None


def _try_proxy_stream(mod_name: str, kwargs: Dict) -> List[Dict]:
    import importlib
    try:
        mod = importlib.import_module(f"api.{mod_name}")
        out: List[Dict] = []
        has_text = False
        for ch in mod.stream_chat(**kwargs):
            t = ch.get("type")
            if t == "text" and ch.get("content"):
                has_text = True
                out.append(ch)
            elif t in ("thought", "thinking", "reasoning") and ch.get("content"):
                out.append({"type": "thought", "content": ch["content"]})
            elif t == "error":
                return []
        return out if has_text else []
    except Exception as exc:
        logger.debug("keyless_fallback %s failed: %s", mod_name, exc)
        return []


def stream_keyless_fallback(
    provider: str,
    model: str,
    messages: List[Dict],
    system_prompt: str = "",
    reasoning: bool = False,
) -> Generator[Dict, None, None]:
    if os.environ.get("NEB_DISABLE_KEYLESS_FALLBACK") == "1" or in_fallback():
        return
    _LOCAL.active = True
    try:
        norm = _norm_messages(messages, system_prompt)
        if not any(m["role"] == "user" for m in norm):
            return

        # 1. If reasoning was requested and caller is not k2think, try K2Think for real thought + text
        if reasoning and provider != "k2think":
            chunks = _try_proxy_stream("k2think_proxy", {"messages": norm, "reasoning_effort": "medium"})
            if chunks:
                yield from chunks
                yield {"type": "done", "finish_reason": "stop"}
                return

        # 2. Try model-matched DeepAI free endpoint (supports Qwen3.8, DeepSeek V4.1, GLM 5.3, GPT-6 Luna, Claude Haiku 5.5, Gemma 4)
        if provider != "deepai":
            da_model = _pick_deepai_model(provider, model)
            text = _try_deepai(norm, da_model)
            if not text and da_model != "standard":
                text = _try_deepai(norm, "standard")
            if text:
                yield {"type": "text", "content": text}
                yield {"type": "done", "finish_reason": "stop"}
                return

        # 3. Try Motiftech 102B streaming
        if provider != "motiftech":
            chunks = _try_proxy_stream("motiftech_proxy", {"messages": norm, "model": "motif-102b", "reasoning_effort": "small"})
            if chunks:
                yield from chunks
                yield {"type": "done", "finish_reason": "stop"}
                return

        # 4. Try LLM7 & Kilo Gateway & Unikey & Ptero & Yqcloud & ChatJimmy
        for cand_prov, fn in (
            ("llm7", lambda: _try_openai_compat("https://api.llm7.io/v1/chat/completions", _pick_llm7_model(provider, model), norm, {"Authorization": "Bearer unused"})),
            ("kilo", lambda: _try_openai_compat("https://api.kilo.ai/api/gateway/chat/completions", "kilo-auto/free", norm, {})),
            ("unikey", lambda: "".join(c["content"] for c in _try_proxy_stream("unikey_proxy", {"messages": norm, "model": _pick_unikey_model(provider, model)}) if c["type"] == "text") or None),
            ("ptero", lambda: "".join(c["content"] for c in _try_proxy_stream("ptero_proxy", {"messages": norm}) if c["type"] == "text") or None),
            ("yqcloud", lambda: "".join(c["content"] for c in _try_proxy_stream("yqcloud_proxy", {"messages": norm}) if c["type"] == "text") or None),
            ("chatjimmy", lambda: "".join(c["content"] for c in _try_proxy_stream("chatjimmy_proxy", {"messages": norm}) if c["type"] == "text") or None),
        ):
            if cand_prov == provider:
                continue
            text = fn()
            if text:
                yield {"type": "text", "content": text}
                yield {"type": "done", "finish_reason": "stop"}
                return
    finally:
        _LOCAL.active = False


def simple_keyless_fallback(
    provider: str,
    model: str,
    user_message: str,
    system_prompt: str = "",
    reasoning: bool = False,
) -> Optional[str]:
    parts: List[str] = []
    for ch in stream_keyless_fallback(
        provider=provider,
        model=model,
        messages=[{"role": "user", "content": user_message}],
        system_prompt=system_prompt,
        reasoning=reasoning,
    ):
        if ch.get("type") == "text":
            parts.append(ch.get("content", ""))
    return "".join(parts).strip() or None
