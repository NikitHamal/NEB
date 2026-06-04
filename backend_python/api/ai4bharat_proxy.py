"""
AI4Bharat Arena proxy for the NEBians Android client ("Neby AI" tab).

Reverse-engineered from https://arena.ai4bharat.org/ (Indic LLM Arena).
The arena exposes a Django/DRF backend that:
  - accepts a `POST /auth/anonymous/` request to mint a guest token
  - allows 20 messages / 3 sessions per guest token
  - streams chat completions in a custom newline protocol
        a0:"<json-stringified-text-chunk>"
        ad:{"finishReason":"stop"|"error"}
  - embeds the model id as `modelId` INSIDE the assistant message object
  - is keyed by either `Authorization: Bearer <jwt>` or `X-Anonymous-Token: <uuid>`

This module provides a stable Python client and a Django-friendly anon-token
pool so the views layer doesn't have to reimplement the dance on every call.
"""
import json
import logging
import threading
import time
import uuid
from typing import Generator, Optional

import requests

logger = logging.getLogger(__name__)


# ========================= Configuration =========================

AI4BHARAT_API_URL = "https://backend.arena.ai4bharat.co"
ARENA_TENANT = ""  # tenant prefix is optional; leave empty for default arena

GUEST_MSG_LIMIT = 20
GUEST_SESSION_LIMIT = 3
TOKEN_POOL_SIZE = 12          # how many anon tokens to keep warm
TOKEN_WARN_BUDGET = 15        # retire a token when its msg count hits this
TOKEN_DEAD_BUDGET = 20        # server-enforced hard limit
REQUEST_TIMEOUT = 60          # seconds
STREAM_CHUNK_TIMEOUT = 30     # seconds; safety net per chunk


# ========================= Errors =========================

class ArenaError(Exception):
    """Generic arena API failure (non-2xx or unexpected payload)."""
    def __init__(self, message, status_code=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class ArenaAuthError(ArenaError):
    """The arena rejected our anonymous token (401/403/expired)."""


class ArenaRateLimit(ArenaError):
    """Per-token limits hit (20 msgs / 3 sessions)."""


# ========================= Anonymous token pool =========================

_token_pool_lock = threading.Lock()
_POOL_INDEX_KEY = 'arena:pool:index'
_TOKEN_KEY = 'arena:token:{}'
_TOKEN_TTL = 60 * 60 * 24 * 7   # 7 days, server allows this


def _token_key(token: str) -> str:
    return _TOKEN_KEY.format(token)


def _serialize_entry(entry: dict) -> str:
    return json.dumps(entry)


def _deserialize_entry(raw) -> Optional[dict]:
    if not raw:
        return None
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return None


def _read_pool():
    """Return the full list of token entries. Always returns a list (possibly empty)."""
    from django.core.cache import cache
    index = cache.get(_POOL_INDEX_KEY) or []
    if isinstance(index, str):
        try:
            index = json.loads(index)
        except ValueError:
            index = []
    if not isinstance(index, list):
        index = []
    entries = []
    for tid in index:
        entry = _deserialize_entry(cache.get(_token_key(tid)))
        if not entry:
            continue
        entries.append(entry)
    return entries


def _write_pool(entries):
    """Persist the entire token pool to cache (overwrites)."""
    from django.core.cache import cache
    cache.set(
        _POOL_INDEX_KEY,
        json.dumps([e['token'] for e in entries]),
        _TOKEN_TTL,
    )
    for e in entries:
        cache.set(_token_key(e['token']), _serialize_entry(e), _TOKEN_TTL)


def _new_anonymous_token(display_name: str = 'NebyAI') -> dict:
    """Mint a fresh anonymous token from /auth/anonymous/."""
    payload = {'display_name': display_name}
    try:
        r = requests.post(
            f"{AI4BHARAT_API_URL}/auth/anonymous/",
            json=payload,
            timeout=15,
        )
    except requests.RequestException as e:
        raise ArenaError(f"anonymous-auth transport error: {e}") from e

    if r.status_code != 200:
        raise ArenaError(
            f"anonymous-auth failed: {r.status_code} {r.text[:200]}",
            status_code=r.status_code, body=r.text,
        )
    data = r.json()
    token = data.get('anonymous_token') or (data.get('tokens') or {}).get('access')
    if not token:
        raise ArenaError(f"anonymous-auth response missing token: {data}")
    return {
        'token': token,
        'message_count': 0,
        'session_count': 0,
        'last_used_ms': 0,
        'is_dead': False,
        'minted_ms': int(time.time() * 1000),
    }


def _pick_healthy_entry(entries, require_low_budget: bool = True):
    """Pick the least-loaded live token. `require_low_budget` is True when
    we want a token that can still accept a brand-new session (msg<15, sess<2)."""
    candidates = [e for e in entries if not e.get('is_dead')]
    if require_low_budget:
        candidates = [
            e for e in candidates
            if e.get('message_count', 0) < TOKEN_WARN_BUDGET
            and e.get('session_count', 0) < GUEST_SESSION_LIMIT
        ]
    if not candidates:
        return None
    # score: lower is better. Spread load by message count.
    candidates.sort(key=lambda e: (
        e.get('message_count', 0),
        e.get('session_count', 0),
        e.get('last_used_ms', 0),
    ))
    return candidates[0]


def acquire_token(require_low_budget: bool = True) -> dict:
    """Return a healthy anon-token entry, minting a new one if the pool is dry.

    Thread-safe. The entry is NOT yet bound to a session — caller MUST call
    `commit_token_use(token, session_opened=False)` after deciding whether
    the call counted as a message (so we can update message_count accurately).
    """
    with _token_pool_lock:
        entries = _read_pool()
        entry = _pick_healthy_entry(entries, require_low_budget=require_low_budget)
        if entry:
            return entry
        # Pool dry or all tokens exhausted — mint a new one, up to pool cap.
        if len(entries) < TOKEN_POOL_SIZE:
            try:
                entry = _new_anonymous_token()
                entries.append(entry)
                _write_pool(entries)
                logger.info("Arena: minted new anon token (pool size %d)", len(entries))
                return entry
            except ArenaError as e:
                logger.error("Arena: anonymous token mint failed: %s", e)
                raise
        # Pool at cap AND all entries are out of budget — caller must rotate.
        raise ArenaRateLimit(
            "All arena anon tokens exhausted; retry after a backoff",
            status_code=429,
        )


def commit_token_use(token: str, *, message_used: bool = True, session_opened: bool = False):
    """Bump counters on the token entry. Called after every successful /messages/stream/."""
    with _token_pool_lock:
        entries = _read_pool()
        for e in entries:
            if e['token'] == token:
                if message_used:
                    e['message_count'] = e.get('message_count', 0) + 1
                if session_opened:
                    e['session_count'] = e.get('session_count', 0) + 1
                e['last_used_ms'] = int(time.time() * 1000)
                if e['message_count'] >= TOKEN_DEAD_BUDGET:
                    e['is_dead'] = True
                break
        _write_pool(entries)


def mark_token_dead(token: str):
    """Mark a token as dead after the arena rejected it (401/403/expired)."""
    with _token_pool_lock:
        entries = _read_pool()
        for e in entries:
            if e['token'] == token:
                e['is_dead'] = True
                e['last_used_ms'] = int(time.time() * 1000)
                break
        _write_pool(entries)


def pool_stats() -> dict:
    """Diagnostic snapshot of the anon-token pool (for /admin or debug)."""
    entries = _read_pool()
    live = [e for e in entries if not e.get('is_dead')]
    return {
        'total': len(entries),
        'live': len(live),
        'dead': len(entries) - len(live),
        'total_messages_used': sum(e.get('message_count', 0) for e in entries),
        'total_sessions_used': sum(e.get('session_count', 0) for e in entries),
    }


# ========================= Low-level API client =========================

def _headers(token: str) -> dict:
    return {
        'Content-Type': 'application/json',
        'X-Anonymous-Token': token,
    }


def _path(suffix: str) -> str:
    if ARENA_TENANT:
        return f"{AI4BHARAT_API_URL}/{ARENA_TENANT}{suffix}"
    return f"{AI4BHARAT_API_URL}{suffix}"


def list_models(token: str, model_type: str = 'LLM') -> list:
    """Return [{id, code, name, provider, capabilities, ...}] from /models/type/."""
    r = requests.get(
        _path(f"/models/type/?model_type={model_type}"),
        headers=_headers(token),
        timeout=15,
    )
    if r.status_code == 401:
        mark_token_dead(token)
        raise ArenaAuthError("anon token rejected on list_models", status_code=401)
    if r.status_code != 200:
        raise ArenaError(f"list_models failed: {r.status_code}", status_code=r.status_code, body=r.text)
    return r.json()


def create_session(token: str, model_id: str, mode: str = 'direct') -> dict:
    """Create an arena session and return the full session dict (with .id)."""
    payload = {
        'mode': mode,
        'model_a_id': model_id,
        'model_b_id': None,
        'session_type': 'LLM',
        'metadata': {},
    }
    r = requests.post(
        _path("/sessions/"),
        headers=_headers(token),
        json=payload,
        timeout=20,
    )
    if r.status_code in (401, 403):
        mark_token_dead(token)
        raise ArenaAuthError("anon token rejected on create_session", status_code=r.status_code)
    if r.status_code == 400 and 'limit' in r.text.lower():
        raise ArenaRateLimit("session limit reached for this anon token", status_code=400, body=r.text)
    if r.status_code != 201 and r.status_code != 200:
        raise ArenaError(
            f"create_session failed: {r.status_code} {r.text[:300]}",
            status_code=r.status_code, body=r.text,
        )
    return r.json()


def stream_chat(token: str, session_id: str, user_content: str, model_id: str,
                user_message_id: str, assistant_message_id: str,
                parent_message_ids: list, language: str = 'en',
                timeout: int = REQUEST_TIMEOUT) -> Generator[dict, None, None]:
    """Yield decoded chunks from `POST /messages/stream/`.

    Each yielded item is one of:
        {'type': 'content', 'text': '...'}      — a token of assistant text
        {'type': 'done',    'finishReason': 'stop'|'error', 'error'?: '...'}
        {'type': 'error',   'message': '...', 'status': int}
    """
    payload = {
        'session_id': session_id,
        'messages': [
            {
                'id': user_message_id,
                'role': 'user',
                'content': user_content,
                'parent_message_ids': parent_message_ids or [],
                'status': 'pending',
                'language': language,
            },
            {
                'id': assistant_message_id,
                'role': 'assistant',
                'content': '',
                'parent_message_ids': [user_message_id],
                'modelId': model_id,
                'status': 'pending',
            },
        ],
    }
    try:
        resp = requests.post(
            _path("/messages/stream/"),
            headers=_headers(token),
            json=payload,
            stream=True,
            timeout=timeout,
        )
    except requests.RequestException as e:
        yield {'type': 'error', 'message': f'stream transport error: {e}', 'status': 0}
        return

    if resp.status_code in (401, 403):
        mark_token_dead(token)
        yield {
            'type': 'error',
            'message': 'arena auth rejected (token dead)',
            'status': resp.status_code,
        }
        return
    if resp.status_code != 200:
        body = ''
        try:
            body = resp.text[:500]
        except Exception:
            pass
        yield {
            'type': 'error',
            'message': f'arena stream http {resp.status_code}: {body}',
            'status': resp.status_code,
        }
        return

    # CRITICAL: arena sends Content-Type: text/plain (no charset), so `requests`
    # falls back to ISO-8859-1 and corrupts every multi-byte UTF-8 character
    # (emoji, Devanagari, CJK, etc.) into mojibake like `ð\x9f\x91\x8b`.
    # Force UTF-8 decoding on the streaming response.
    resp.encoding = 'utf-8'

    try:
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith('a0:'):
                inner = line[3:]
                try:
                    yield {'type': 'content', 'text': json.loads(inner)}
                except json.JSONDecodeError:
                    # Server sometimes double-escapes or returns non-JSON garbage;
                    # best-effort: try unescaping backslash sequences.
                    try:
                        yield {'type': 'content', 'text': inner.encode().decode('unicode_escape')}
                    except Exception:
                        logger.warning("Arena: undecodable a0: chunk: %r", inner[:200])
            elif line.startswith('ad:'):
                inner = line[3:]
                try:
                    meta = json.loads(inner)
                except json.JSONDecodeError:
                    meta = {'finishReason': 'stop'}
                if meta.get('finishReason') == 'error':
                    yield {
                        'type': 'error',
                        'message': meta.get('error', 'arena returned finishReason=error'),
                        'status': 500,
                        'finishReason': 'error',
                    }
                else:
                    yield {
                        'type': 'done',
                        'finishReason': meta.get('finishReason', 'stop'),
                    }
                return
    finally:
        try:
            resp.close()
        except Exception:
            pass


def regenerate(token: str, assistant_message_id: str, timeout: int = REQUEST_TIMEOUT) -> Generator[dict, None, None]:
    """Yield decoded chunks from `POST /messages/{id}/regenerate/`."""
    try:
        resp = requests.post(
            _path(f"/messages/{assistant_message_id}/regenerate/"),
            headers=_headers(token),
            stream=True,
            timeout=timeout,
        )
    except requests.RequestException as e:
        yield {'type': 'error', 'message': f'regenerate transport error: {e}', 'status': 0}
        return

    if resp.status_code in (401, 403):
        mark_token_dead(token)
        yield {'type': 'error', 'message': 'arena auth rejected (token dead)', 'status': resp.status_code}
        return
    if resp.status_code != 200:
        yield {
            'type': 'error',
            'message': f'arena regenerate http {resp.status_code}: {resp.text[:300]}',
            'status': resp.status_code,
        }
        return

    # See stream_chat: force UTF-8 to avoid ISO-8859-1 mojibake.
    resp.encoding = 'utf-8'

    try:
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if line.startswith('a0:'):
                inner = line[3:]
                try:
                    yield {'type': 'content', 'text': json.loads(inner)}
                except json.JSONDecodeError:
                    try:
                        yield {'type': 'content', 'text': inner.encode().decode('unicode_escape')}
                    except Exception:
                        pass
            elif line.startswith('ad:'):
                inner = line[3:]
                try:
                    meta = json.loads(inner)
                except json.JSONDecodeError:
                    meta = {'finishReason': 'stop'}
                if meta.get('finishReason') == 'error':
                    yield {
                        'type': 'error',
                        'message': meta.get('error', 'arena returned finishReason=error'),
                        'status': 500,
                    }
                else:
                    yield {'type': 'done', 'finishReason': meta.get('finishReason', 'stop')}
                return
    finally:
        try:
            resp.close()
        except Exception:
            pass


# ========================= Convenience: model info helpers =========================

def fetch_models_for_client(token: str) -> list:
    """Return a lean list of LLM models ready to ship to the Android client."""
    raw = list_models(token, model_type='LLM')
    out = []
    for m in raw:
        out.append({
            'id': m.get('id'),
            'code': m.get('model_code'),
            'name': m.get('display_name'),
            'provider': m.get('provider'),
            'thinking': bool(m.get('is_thinking_model')),
            'random_only': bool(m.get('random_only')),
            'active': bool(m.get('is_active', True)),
        })
    return out


# ========================= New-message-ID helper =========================

def new_message_id() -> str:
    return str(uuid.uuid4())


# ========================= Non-streaming one-shot chat (for the bot) =========================

def simple_chat(user_message: str, model_id: str = None, system_prompt: str = '',
                 max_tokens: int = 500, timeout: int = 60) -> Optional[str]:
    """Convenience wrapper for the Neby bot — mint a token, create a session,
    send one message, return the full text (or None on failure).

    Picks the first healthy LLM model if `model_id` is not given. Designed to
    be called from a cron worker, so latency matters less than correctness.
    """
    entry = acquire_token(require_low_budget=False)
    models = fetch_models_for_client(entry['token'])
    if model_id is None:
        pick = next((m for m in models if m['active'] and not m['random_only']), None)
        if not pick:
            raise ArenaError('no active LLM model available from arena')
        model_id = pick['id']
        pick_name = pick['name']
    else:
        # Try to resolve display name (best-effort) for logs
        match = next((m for m in models if m['id'] == model_id), None)
        if not match:
            # Configured model_id not in the live arena catalog — this usually means
            # the admin picked a stale/fake UUID. Degrade gracefully to the first
            # active non-random model so the bot still responds instead of failing.
            fallback = next((m for m in models if m['active'] and not m['random_only']), None)
            if fallback:
                logger.warning(
                    "ai4bharat.simple_chat: configured model_id=%s not found in arena "
                    "(got %d models). Falling back to %s (%s). "
                    "Check the BotConfig admin page — the model UUID is likely stale.",
                    model_id, len(models), fallback['id'], fallback['name'],
                )
                model_id = fallback['id']
                pick_name = f"{fallback['name']} (fallback from {model_id[:12]}...)"
            else:
                raise ArenaError(
                    f"configured model_id={model_id} not found and no fallback available"
                )
        else:
            pick_name = match['name']

    sess = create_session(entry['token'], model_id)
    u, a = new_message_id(), new_message_id()
    full_content = user_message
    if system_prompt:
        full_content = f"[System Instructions]\n{system_prompt}\n\n[User Message]\n{user_message}"
    full = ''
    for chunk in stream_chat(
        token=entry['token'],
        session_id=sess['id'],
        user_content=full_content,
        model_id=model_id,
        user_message_id=u,
        assistant_message_id=a,
        parent_message_ids=[],
        timeout=timeout,
    ):
        if chunk['type'] == 'content':
            full += chunk['text']
        elif chunk['type'] == 'error':
            logger.error(f"ai4bharat.simple_chat: upstream error: {chunk['message']}")
            return None
    commit_token_use(entry['token'], message_used=True, session_opened=True)
    out = (full or '').strip()[:max_tokens * 4]   # rough char cap; tokens → ~4 chars
    logger.info(f"ai4bharat.simple_chat: model={pick_name} reply_chars={len(out)}")
    return out or None


# ========================= Self-test =========================

if __name__ == '__main__':  # `python -m api.ai4bharat_proxy`
    import sys
    print("== AI4Bharat proxy self-test ==")
    entry = acquire_token(require_low_budget=True)
    print(f"acquired token: {entry['token'][:12]}... (used {entry['message_count']} msgs)")
    models = fetch_models_for_client(entry['token'])
    print(f"models: {len(models)}")
    pick = next((m for m in models if not m['random_only'] and m['active']), models[0])
    print(f"picked: {pick['name']} ({pick['code']})")
    sess = create_session(entry['token'], pick['id'])
    print(f"session: {sess['id']}")
    u, a = new_message_id(), new_message_id()
    out = ''
    for chunk in stream_chat(entry['token'], sess['id'], 'Say hello in Hindi',
                              pick['id'], u, a, []):
        if chunk['type'] == 'content':
            out += chunk['text']
        elif chunk['type'] == 'done':
            print(f"DONE: {chunk}")
        elif chunk['type'] == 'error':
            print(f"ERR:  {chunk}", file=sys.stderr)
            sys.exit(1)
    commit_token_use(entry['token'], message_used=True, session_opened=True)
    print(f"---\n{out}\n---")
    print("pool stats:", pool_stats())
