"""
DeepSeek Web Chat provider for Neby CLI.
Uses chat.deepseek.com web API with user token (no API key needed).
Falls back to official API if web token fails and API key is available.
"""
import base64
import json
import logging
import os
import random
import string
import struct
import time
import uuid
from typing import Any, Dict, Generator, List, Optional

import requests
try:
    from curl_cffi import requests as cffi_requests
    _CFFI_AVAILABLE = True
except ImportError:
    _CFFI_AVAILABLE = False
    cffi_requests = None

_IMPERSONATE = "chrome"

logger = logging.getLogger(__name__)

WEB_API_BASE = "https://chat.deepseek.com/api"
OFFICIAL_API_BASE = "https://api.deepseek.com"

WEB_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://chat.deepseek.com",
    "Referer": "https://chat.deepseek.com/",
    "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Chromium";v="148"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "X-App-Version": "2.0.0",
    "X-Client-Locale": "en_US",
    "X-Client-Platform": "web",
    "X-Client-Version": "2.0.0",
}

CONFIG_PATHS = [
    os.path.expanduser("~/.neby_config.json"),
    r"F:\flashy\config.json",
]

_session_cache: Dict[str, str] = {}  # token -> session_id
_last_msg_cache: Dict[str, Optional[str]] = {}  # token -> last_message_id


def _load_web_token() -> str:
    token = os.getenv("DEEPSEEK_WEB_TOKEN", "")
    if token:
        return token
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                t = cfg.get("deepseek_token", "")
                if t:
                    return t
            except Exception:
                pass
    return ""


def _load_api_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY", "")
    if key:
        return key
    config_path = os.path.expanduser("~/.neby_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            return cfg.get("deepseek_api_key", "")
        except Exception:
            pass
    return ""


def _random_cookie() -> str:
    ts = int(time.time() * 1000)
    fr_id = str(uuid.uuid4()).replace("-", "")
    chars = string.ascii_lowercase + string.digits
    return (
        f"intercom-HWWAFSESTIME={ts}; "
        f"HWWAFSESID={''.join(random.choice(chars) for _ in range(18))}; "
        f"_frid={fr_id}; _fr_ssid={fr_id}; _fr_pvid={fr_id}"
    )


def _validate_web_token(token: str) -> bool:
    try:
        req_fn = cffi_requests.get if _CFFI_AVAILABLE else requests.get
        kwargs = {"impersonate": _IMPERSONATE} if _CFFI_AVAILABLE else {}
        resp = req_fn(
            f"{WEB_API_BASE}/v0/users/current",
            headers={**WEB_HEADERS, "Authorization": f"Bearer {token}"},
            timeout=10,
            **kwargs,
        )
        if resp.status_code != 200:
            return False
        d = resp.json()
        return d.get("code", -1) == 0
    except Exception:
        return False


def _create_session(token: str) -> str:
    _session_cache.pop(token, None)  # always fresh session per conversation
    try:
        req_fn = cffi_requests.post if _CFFI_AVAILABLE else requests.post
        kwargs = {"impersonate": _IMPERSONATE} if _CFFI_AVAILABLE else {}
        resp = req_fn(
            f"{WEB_API_BASE}/v0/chat_session/create",
            headers={
                **WEB_HEADERS,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={},
            timeout=15,
            **kwargs,
        )
        d = resp.json()
        biz = d.get("data", {}).get("biz_data", {})
        sess = biz.get("chat_session", biz)
        sid = sess.get("id", "")
        if sid:
            _session_cache[token] = sid
            _last_msg_cache[token] = None
            logger.info(f"[DeepSeek Web] Created session: {sid[:12]}...")
            return sid
    except Exception as e:
        logger.error(f"[DeepSeek Web] Session create failed: {e}")
    return ""


def _get_pow_challenge(token: str) -> Optional[Dict]:
    try:
        req_fn = cffi_requests.post if _CFFI_AVAILABLE else requests.post
        kwargs = {"impersonate": _IMPERSONATE} if _CFFI_AVAILABLE else {}
        resp = req_fn(
            f"{WEB_API_BASE}/v0/chat/create_pow_challenge",
            headers={
                **WEB_HEADERS,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"target_path": "/api/v0/chat/completion"},
            timeout=15,
            **kwargs,
        )
        d = resp.json()
        return d.get("data", {}).get("biz_data", {}).get("challenge", None)
    except Exception:
        return None


def _solve_pow_python(challenge: Dict) -> Optional[str]:
    """
    Pure-Python PoW solver for DeepSeekHashV1.
    Algorithm: find integer N >= 0 such that
      sha3_256(f"{salt}_{expire_at}_{N}") < 2^256 / difficulty
    Then submit as JSON payload base64-encoded.
    Returns None on failure (too slow / timeout).
    """
    import hashlib
    algorithm = challenge.get("algorithm", "")
    challenge_str = challenge.get("challenge", "")
    salt = challenge.get("salt", "")
    difficulty = int(challenge.get("difficulty", 100000))
    expire_at = challenge.get("expire_at", 0)
    signature = challenge.get("signature", "")

    if algorithm != "DeepSeekHashV1":
        logger.warning(f"[DeepSeek PoW] Unsupported algorithm: {algorithm}")
        return None

    # Target: hash_int < 2^256 / difficulty
    target = (1 << 256) // max(1, difficulty)
    prefix = f"{salt}_{expire_at}_"

    logger.info(f"[DeepSeek PoW] Solving: difficulty={difficulty}, target_bits={target.bit_length()}")

    MAX_ITER = 500_000
    for n in range(MAX_ITER):
        attempt = f"{prefix}{n}"
        h = hashlib.sha3_256(attempt.encode()).digest()
        h_int = int.from_bytes(h, "big")
        if h_int < target:
            logger.info(f"[DeepSeek PoW] Solved at n={n}")
            payload = {
                "algorithm": algorithm,
                "challenge": challenge_str,
                "salt": salt,
                "answer": float(n),
                "signature": signature,
                "target_path": "/api/v0/chat/completion",
            }
            return base64.b64encode(
                json.dumps(payload, separators=(",", ":")).encode()
            ).decode()

    logger.warning(f"[DeepSeek PoW] No solution found in {MAX_ITER} iterations")
    return None


def _messages_to_prompt(messages: List[Dict]) -> str:
    blocks = []
    system_content = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if not content:
            continue
        if role == "system":
            system_content = content
        elif role == "assistant":
            blocks.append(f"<｜Assistant｜>{content}<｜end of sentence｜>")
        elif role == "user":
            text = content
            if system_content and not blocks:
                text = f"{system_content}\n\n{content}"
                system_content = ""
            blocks.append(f"<｜User｜>{text}")
        else:
            blocks.append(f"<｜User｜>{content}")
    if not blocks and system_content:
        blocks.append(f"<｜User｜>{system_content}")
    return "".join(blocks)


def _stream_via_flashy(
    messages: List[Dict],
    model: str,
    token: str,
) -> Generator[Dict, None, None]:
    """
    Bridge flashy's async DeepSeekProvider into a sync generator.
    flashy handles the correct Chrome TLS impersonation + PoW + session management.
    """
    import asyncio

    try:
        sys.path.insert(0, r"F:\flashy")
        sys.path.insert(0, r"F:\flashy\backend")
        from backend.providers.deepseek import DeepSeekProvider
    except ImportError as e:
        yield {"type": "error", "error": f"flashy DeepSeekProvider not available: {e}"}
        return

    model_type = "expert" if "pro" in model.lower() else "default"
    thinking_enabled = "pro" in model.lower()

    async def _run():
        p = DeepSeekProvider()
        chunks = []
        async for chunk in p.generate_stream(
            messages,
            model=model_type,
            token=token,
            thinking_enabled=thinking_enabled,
        ):
            chunks.append(chunk)
        return chunks

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            chunks = loop.run_until_complete(_run())
        finally:
            loop.close()
    except Exception as e:
        yield {"type": "error", "error": f"DeepSeek async error: {e}"}
        return

    for chunk in chunks:
        if "text" in chunk:
            yield {"type": "text", "content": chunk["text"]}
        elif "thought" in chunk:
            pass  # skip thinking tokens for now
        elif "error" in chunk:
            yield {"type": "error", "error": chunk["error"]}
            return

    yield {"type": "done"}


import sys


def _stream_via_flashy_streaming(
    messages: List[Dict],
    model: str,
    token: str,
) -> Generator[Dict, None, None]:
    """
    True streaming version using thread + queue bridge.
    """
    import asyncio
    import queue
    import threading

    try:
        sys.path.insert(0, r"F:\flashy")
        sys.path.insert(0, r"F:\flashy\backend")
        from backend.providers.deepseek import DeepSeekProvider
    except ImportError as e:
        yield {"type": "error", "error": f"flashy not available: {e}"}
        return

    model_type = "expert" if "pro" in model.lower() else "default"
    thinking_enabled = "pro" in model.lower()
    q: queue.Queue = queue.Queue()
    _SENTINEL = object()

    def run_async():
        async def _run():
            p = DeepSeekProvider()
            try:
                async for chunk in p.generate_stream(
                    messages,
                    model=model_type,
                    token=token,
                    thinking_enabled=thinking_enabled,
                ):
                    q.put(chunk)
            except Exception as e:
                q.put({"error": str(e)})
            finally:
                q.put(_SENTINEL)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_run())
        finally:
            loop.close()

    t = threading.Thread(target=run_async, daemon=True)
    t.start()

    while True:
        chunk = q.get(timeout=120)
        if chunk is _SENTINEL:
            break
        if "text" in chunk:
            yield {"type": "text", "content": chunk["text"]}
        elif "error" in chunk:
            yield {"type": "error", "error": chunk["error"]}
            return

    yield {"type": "done"}


def stream_chat(
    messages: List[Dict[str, str]],
    model: str = "deepseek-v4-flash",
    temperature: float = 0.6,
) -> Generator[Dict[str, Any], None, None]:
    """
    Main entry point.
    Priority: flashy web token > official API key.
    """
    web_token = _load_web_token()
    api_key = _load_api_key()

    if web_token:
        logger.info(f"[DeepSeek] Using flashy web stream for model={model}")
        yield from _stream_via_flashy_streaming(messages, model, web_token)
        return

    if api_key:
        logger.info(f"[DeepSeek] Using official API key for model={model}")
        yield from _stream_official_api(messages, model, api_key, temperature)
        return

    yield {
        "type": "error",
        "error": (
            "DeepSeek: No credentials found.\n"
            "  Option 1: Set DEEPSEEK_WEB_TOKEN (from chat.deepseek.com LocalStorage > userToken)\n"
            "  Option 2: Set DEEPSEEK_API_KEY env var or add 'deepseek_api_key' to ~/.neby_config.json"
        ),
    }



def _stream_official_api(
    messages: List[Dict],
    model: str,
    api_key: str,
    temperature: float = 0.6,
) -> Generator[Dict, None, None]:
    model_map = {
        "deepseek-v4-flash": "deepseek-v4-flash",
        "deepseek-v4-pro": "deepseek-v4-pro",
        "deepseek-v4": "deepseek-v4-flash",
        "flash": "deepseek-v4-flash",
        "pro": "deepseek-v4-pro",
    }
    model = model_map.get(model.lower(), model)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
    }
    try:
        with requests.post(
            f"{OFFICIAL_API_BASE}/chat/completions",
            json=payload,
            headers=headers,
            stream=True,
            timeout=(5, 90),
        ) as resp:
            if resp.status_code != 200:
                yield {"type": "error", "error": f"DeepSeek API HTTP {resp.status_code}: {resp.text[:200]}"}
                return
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        choices = chunk.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content") or delta.get("reasoning_content") or ""
                            if content:
                                yield {"type": "text", "content": content}
                    except Exception:
                        continue
            yield {"type": "done"}
    except Exception as e:
        yield {"type": "error", "error": str(e)}


