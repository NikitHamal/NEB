"""
FreeGPT chat proxy for the NEBians app ("Neby AI" tab).

Reverse-engineered from https://standalone.freegpt.win:3001/ (EasyChat v2.16.1,
based on ChatGPT-Next-Web, backed by OneAPI).

The site uses an OpenAI-compatible API with:
  - Chat endpoint: POST {base}/v1/chat/completions  (SSE streaming)
  - Models endpoint: GET  {base}/v1/models           (no auth required)
  - Auth: Bearer token with "nk-" prefix (shared access code)
  - Anti-bot: WASM PoW challenge headers (x-secure-*)

WASM PoW challenge system:
  1. Fetch challenge from GET /api/challenge (with uuid + x-origin headers)
  2. Response: {challengeId, challenge, difficulty, issuedAt, expiresAt, version}
  3. Solve: find nonce N where SHA-256(challenge + N) starts with difficulty zero hex chars
  4. Send x-secure-* headers with chat requests

Access code auth:
  - The site requires a shared access code (entered by user in UI)
  - Sent as: Authorization: Bearer nk-{accessCode}
  - Without auth: 401 error

Two routes available:
  - Domestic:  https://standalone.freegpt.win:3001
  - International: https://7fa179251cde.freegpt.tech
"""

import hashlib
import json
import logging
import secrets
import time
from typing import Dict, Generator, List, Optional

import requests

logger = logging.getLogger(__name__)

DOMESTIC_BASE = "https://standalone.freegpt.win:3001"
INTERNATIONAL_BASE = "https://7fa179251cde.freegpt.tech"
DEFAULT_BASE = DOMESTIC_BASE
REQUEST_TIMEOUT = 120

_uuid = None
_challenge_cache = None
_challenge_ts = 0


def _generate_uuid() -> str:
    shortid_chars = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    now = time.localtime()
    date_str = f"{now.tm_year % 100:02d}{now.tm_mon:02d}{now.tm_mday:02d}"
    random_part = "".join(secrets.choice(shortid_chars) for _ in range(16))
    full = f"R5{date_str}{random_part}"
    checksum = sum(ord(c) for c in full) % 10
    return f"{full}{checksum}"


def _solve_pow(challenge: str, difficulty: int) -> tuple:
    nonce = 0
    target = "0" * difficulty
    while nonce < 10_000_000:
        payload = f"{challenge}{nonce}"
        h = hashlib.sha256(payload.encode()).hexdigest()
        if h.startswith(target):
            return nonce, h
        nonce += 1
    raise ValueError(f"Could not solve PoW with difficulty {difficulty}")


def _get_uuid() -> str:
    global _uuid
    if not _uuid:
        _uuid = _generate_uuid()
    return _uuid


def _get_pow_headers(base_url: str = DEFAULT_BASE) -> Dict[str, str]:
    global _challenge_cache, _challenge_ts
    now = time.time()
    if _challenge_cache and now - _challenge_ts < 240:
        return _challenge_cache

    try:
        resp = requests.get(
            f"{base_url}/api/challenge",
            headers={
                "Accept": "application/json",
                "uuid": _get_uuid(),
                "x-origin": base_url,
            },
            timeout=15,
            verify=False,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.warning(f"Failed to get PoW challenge: {e}")
        return {}

    challenge = data["challenge"]
    difficulty = data["difficulty"]
    challenge_id = data["challengeId"]
    expires_at = str(data["expiresAt"])
    version = data["version"]

    nonce, hash_result = _solve_pow(challenge, difficulty)
    timestamp = str(int(time.time() * 1000))

    headers = {
        "x-secure-challenge-id": challenge_id,
        "x-secure-challenge-expires-at": expires_at,
        "x-secure-challenge-version": version,
        "x-secure-signature": hash_result,
        "x-secure-fingerprint": _get_uuid(),
        "x-secure-pow-seed-nonce": "0",
        "x-secure-pow-nonce": str(nonce),
        "x-secure-pow-hash": hash_result,
        "x-secure-pow-difficulty": str(difficulty),
        "x-secure-timestamp": timestamp,
        "x-secure-nonce": str(nonce),
        "x-secure-version": version,
    }

    _challenge_cache = headers
    _challenge_ts = now
    return headers


def get_models(base_url: str = DEFAULT_BASE) -> List[Dict]:
    try:
        resp = requests.get(
            f"{base_url}/v1/models",
            headers={"Accept": "application/json"},
            timeout=30,
            verify=False,
        )
        resp.raise_for_status()
        data = resp.json()
        models = []
        for m in data.get("data", []):
            mid = m.get("id", "")
            mname = mid.replace("-", " ").replace("_", " ").title()
            models.append({
                "id": mid,
                "name": mname,
                "vision": any(v in mid.lower() for v in ["vision", "vl", "image", "-4o", "4.1", "opus", "sonnet"]),
                "thinking": any(t in mid.lower() for t in ["thinking", "reasoner", "think"]),
            })
        return models
    except Exception as e:
        logger.warning(f"Failed to fetch models: {e}")
        return []


def stream_chat(
    messages: List[Dict[str, str]],
    model: str,
    access_code: str = "",
    base_url: str = DEFAULT_BASE,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
) -> Generator[Dict, None, None]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "uuid": _get_uuid(),
        "x-origin": base_url,
        "model": model,
    }

    if access_code:
        headers["Authorization"] = f"Bearer nk-{access_code}"

    pow_headers = _get_pow_headers(base_url)
    headers.update(pow_headers)

    payload = {
        "messages": messages,
        "stream": True,
        "model": model,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if top_p is not None:
        payload["top_p"] = top_p

    try:
        resp = requests.post(
            f"{base_url}/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            verify=False,
            stream=True,
        )
    except Exception as e:
        yield {"error": f"Connection error: {e}"}
        return

    if resp.status_code == 401:
        body = resp.content.decode("utf-8", errors="replace")
        yield {"error": f"Auth required: {body[:200]}"}
        return
    if resp.status_code == 403:
        body = resp.content.decode("utf-8", errors="replace")
        yield {"error": f"Forbidden: {body[:200]}"}
        return
    if resp.status_code == 429:
        yield {"error": "Rate limited. Please try again later."}
        return
    if resp.status_code != 200:
        body = resp.content.decode("utf-8", errors="replace")
        yield {"error": f"HTTP {resp.status_code}: {body[:200]}"}
        return

    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        data_str = line[6:]
        if data_str.strip() == "[DONE]":
            return
        try:
            chunk = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        choices = chunk.get("choices", [])
        if not choices:
            continue
        delta = choices[0].get("delta", {})
        content = delta.get("content", "")
        if content:
            yield {"text": content}
        reasoning = delta.get("reasoning_content", "")
        if reasoning:
            yield {"thinking": reasoning}


def chat(
    messages: List[Dict[str, str]],
    model: str,
    access_code: str = "",
    base_url: str = DEFAULT_BASE,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
) -> Dict:
    full_text = ""
    full_thinking = ""
    for chunk in stream_chat(messages, model, access_code, base_url, temperature, max_tokens, top_p):
        if "error" in chunk:
            return chunk
        if "text" in chunk:
            full_text += chunk["text"]
        if "thinking" in chunk:
            full_thinking += chunk["thinking"]
    result = {"text": full_text}
    if full_thinking:
        result["thinking"] = full_thinking
    return result


def simple_chat(
    prompt: str,
    model: str = "gpt-5-nano",
    access_code: str = "",
    base_url: str = DEFAULT_BASE,
) -> str:
    result = chat(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        access_code=access_code,
        base_url=base_url,
    )
    if "error" in result:
        return f"Error: {result['error']}"
    return result.get("text", "")


class FreeGPTError(Exception):
    pass