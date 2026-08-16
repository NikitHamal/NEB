"""Unified official-API chat client.

Speaks the three dominant wire formats — OpenAI chat-completions (also used
by Agnes AI, DeepSeek and every OpenAI-compatible custom endpoint), the
Anthropic Messages API, and the Google Gemini generateContent API — and
normalizes everything into one `ChatResult`.

Deliberately transport-only: no business logic, no ORM imports, so any
current or future NEBians service (background agent runner, Neby bot, arena
judges, …) can call it with plain functions.

Message convention: a list of {'role': 'system'|'user'|'assistant',
'content': str}. Helpers convert to each provider's native shape.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import requests

from .registry import FORMAT_ANTHROPIC, FORMAT_GEMINI, FORMAT_OPENAI

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Raised when an official provider call fails. `retryable` hints whether
    trying again (rate limit / 5xx / network) is worthwhile."""

    def __init__(self, message: str, *, status: int = 0, retryable: bool = True, provider: str = ''):
        super().__init__(message)
        self.status = status
        self.retryable = retryable
        self.provider = provider


@dataclass
class ChatResult:
    text: str
    model: str
    provider: str
    duration_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning: str = ''  # upstream chain-of-thought, when the API exposes it
    raw: dict = field(default_factory=dict)


def _emotionless_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Ensure roles are valid and content is a plain string."""
    out = []
    for m in messages or []:
        role = (m.get('role') or 'user').strip().lower()
        if role not in ('system', 'user', 'assistant'):
            role = 'user'
        content = m.get('content')
        if isinstance(content, list):
            content = ''.join(p.get('text', '') if isinstance(p, dict) else str(p) for p in content)
        out.append({'role': role, 'content': str(content or '')})
    return out


def _split_system(messages: List[Dict[str, str]]):
    system_parts: List[str] = []
    convo: List[Dict[str, str]] = []
    for m in messages:
        if m['role'] == 'system':
            if m['content'].strip():
                system_parts.append(m['content'].strip())
        else:
            convo.append(m)
    # Anthropic and Gemini treat system separately; OpenAI keeps it in-band.
    return '\n\n'.join(system_parts), convo


def _http_post_json(url: str, *, headers: dict, payload: dict, timeout: int, provider: str) -> dict:
    t0 = time.time()
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        raise LLMError(f'{provider}: network error: {e}', provider=provider)
    resp.encoding = 'utf-8'
    if resp.status_code != 200:
        detail = resp.text[:400]
        retryable = resp.status_code in (408, 409, 425, 429, 500, 502, 503, 504)
        raise LLMError(
            f'{provider}: HTTP {resp.status_code}: {detail}',
            status=resp.status_code, retryable=retryable, provider=provider,
        )
    try:
        return resp.json()
    except ValueError:
        raise LLMError(f'{provider}: non-JSON response: {resp.text[:200]}', provider=provider)


def _openai_chat(*, base_url: str, api_key: str, model: str, messages: List[Dict[str, str]],
                 max_tokens: int, timeout: int, temperature: float, provider: str) -> ChatResult:
    url = base_url.rstrip('/')
    if not url.endswith('/chat/completions'):
        url += '/chat/completions'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    if api_key.strip():
        headers['Authorization'] = f'Bearer {api_key.strip()}'
    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'stream': False,
    }
    t0 = time.time()
    data = _http_post_json(url, headers=headers, payload=payload, timeout=timeout, provider=provider)
    if isinstance(data.get('error'), dict) and data['error']:
        raise LLMError(f"{provider}: {data['error'].get('message') or data['error']}", provider=provider)
    try:
        message = data['choices'][0]['message']
        content = message.get('content')
    except (KeyError, IndexError, TypeError, AttributeError):
        raise LLMError(f'{provider}: unexpected response shape: {str(data)[:300]}', provider=provider)
    if isinstance(content, list):  # content-parts style
        content = ''.join(p.get('text', '') if isinstance(p, dict) else str(p) for p in content)
    text = (content or '').strip()
    if not text:
        raise LLMError(f'{provider}: empty completion', provider=provider)
    # OpenAI-compatible reasoning channels (DeepSeek, Agnes, Qwen-API, etc.).
    reasoning = message.get('reasoning_content') or message.get('reasoning') or ''
    if isinstance(reasoning, list):
        reasoning = ''.join(
            p.get('text', '') if isinstance(p, dict) else str(p) for p in reasoning
        )
    usage = data.get('usage') or {}
    return ChatResult(
        text=text, model=data.get('model') or model, provider=provider,
        duration_ms=int((time.time() - t0) * 1000),
        input_tokens=int(usage.get('prompt_tokens') or 0),
        output_tokens=int(usage.get('completion_tokens') or 0),
        reasoning=str(reasoning or '').strip(),
        raw=data,
    )


def _anthropic_chat(*, base_url: str, api_key: str, model: str, messages: List[Dict[str, str]],
                    max_tokens: int, timeout: int, temperature: float, provider: str) -> ChatResult:
    url = base_url.rstrip('/')
    if not url.endswith('/v1/messages'):
        url = url.rstrip('/')
        url += '/v1/messages' if not url.endswith('/v1') else '/messages'
    system, convo = _split_system(messages)
    if not convo:
        convo = [{'role': 'user', 'content': 'Hello'}]
    if convo[0]['role'] != 'user':  # Anthropic requires user-first
        convo = [{'role': 'user', 'content': '(continue)'}] + convo
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': api_key.strip(),
        'anthropic-version': '2023-06-01',
    }
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'messages': [{'role': m['role'] if m['role'] != 'system' else 'user', 'content': m['content']} for m in convo],
    }
    if system:
        payload['system'] = system
    t0 = time.time()
    data = _http_post_json(url, headers=headers, payload=payload, timeout=timeout, provider=provider)
    if data.get('type') == 'error' or data.get('error'):
        err = data.get('error') or {}
        raise LLMError(f"{provider}: {err.get('message') or err}", status=data.get('status') or 0, provider=provider)
    parts = data.get('content') or []
    text = ''.join(p.get('text', '') for p in parts if isinstance(p, dict) and p.get('type') == 'text').strip()
    if not text:
        raise LLMError(f'{provider}: empty completion', provider=provider)
    # Anthropic extended-thinking blocks, when present.
    reasoning = '\n\n'.join(
        (p.get('thinking') or p.get('text') or '').strip()
        for p in parts if isinstance(p, dict) and p.get('type') == 'thinking'
    ).strip()
    usage = data.get('usage') or {}
    return ChatResult(
        text=text, model=data.get('model') or model, provider=provider,
        duration_ms=int((time.time() - t0) * 1000),
        input_tokens=int(usage.get('input_tokens') or 0),
        output_tokens=int(usage.get('output_tokens') or 0),
        reasoning=reasoning,
        raw=data,
    )


def _gemini_chat(*, base_url: str, api_key: str, model: str, messages: List[Dict[str, str]],
                 max_tokens: int, timeout: int, temperature: float, provider: str) -> ChatResult:
    url = f"{base_url.rstrip('/')}/models/{model}:generateContent"
    system, convo = _split_system(messages)
    contents = []
    for m in convo:
        role = 'model' if m['role'] == 'assistant' else 'user'
        contents.append({'role': role, 'parts': [{'text': m['content']}]})
    if not contents:
        contents = [{'role': 'user', 'parts': [{'text': 'Hello'}]}]
    headers = {'Content-Type': 'application/json', 'x-goog-api-key': api_key.strip()}
    payload: dict = {
        'contents': contents,
        'generationConfig': {'maxOutputTokens': max_tokens, 'temperature': temperature},
    }
    if system:
        payload['systemInstruction'] = {'parts': [{'text': system}]}
    t0 = time.time()
    data = _http_post_json(url, headers=headers, payload=payload, timeout=timeout, provider=provider)
    if data.get('error'):
        err = data['error']
        raise LLMError(f"{provider}: {err.get('message') or err}", status=err.get('code') or 0, provider=provider)
    try:
        parts = data['candidates'][0]['content']['parts']
    except (KeyError, IndexError, TypeError):
        raise LLMError(f'{provider}: unexpected response shape: {str(data)[:300]}', provider=provider)
    text = ''.join(p.get('text', '') for p in parts if isinstance(p, dict)).strip()
    if not text:
        raise LLMError(f'{provider}: empty completion (possibly blocked)', provider=provider)
    usage = data.get('usageMetadata') or {}
    return ChatResult(
        text=text, model=model, provider=provider,
        duration_ms=int((time.time() - t0) * 1000),
        input_tokens=int(usage.get('promptTokenCount') or 0),
        output_tokens=int(usage.get('candidatesTokenCount') or 0),
        raw=data,
    )


def chat(*, format: str, base_url: str, api_key: str, model: str,
         messages: List[Dict[str, str]], max_tokens: int = 4096,
         timeout: int = 180, temperature: float = 0.2,
         provider: str = '') -> ChatResult:
    """One entry point for every official-format provider."""
    fmt = (format or FORMAT_OPENAI).strip().lower()
    provider = provider or fmt
    model = (model or '').strip()
    if not model:
        raise LLMError(f'{provider}: a model id is required', retryable=False, provider=provider)
    if not (base_url or '').strip():
        raise LLMError(f'{provider}: a base URL is required', retryable=False, provider=provider)
    messages = _emotionless_messages(messages)
    if not messages:
        raise LLMError(f'{provider}: no messages supplied', retryable=False, provider=provider)
    try:
        if fmt == FORMAT_ANTHROPIC:
            return _anthropic_chat(base_url=base_url, api_key=api_key, model=model, messages=messages,
                                   max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=provider)
        if fmt == FORMAT_GEMINI:
            return _gemini_chat(base_url=base_url, api_key=api_key, model=model, messages=messages,
                                max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=provider)
        if fmt == FORMAT_OPENAI:
            return _openai_chat(base_url=base_url, api_key=api_key, model=model, messages=messages,
                                max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=provider)
    except LLMError:
        raise
    except Exception as e:  # safety net — never leak tracebacks to callers
        raise LLMError(f'{provider}: {e}', provider=provider)
    raise LLMError(f'unsupported API format: {fmt}', retryable=False, provider=provider)


def quick_test(*, format: str, base_url: str, api_key: str, model: str,
               provider: str = '', timeout: int = 30) -> ChatResult:
    """Minimal round-trip used by 'Test connection' buttons everywhere."""
    return chat(
        format=format, base_url=base_url, api_key=api_key, model=model,
        messages=[{'role': 'user', 'content': 'Reply with exactly: OK'}],
        max_tokens=16, timeout=timeout, temperature=0.0, provider=provider,
    )


# ── Streaming ────────────────────────────────────────────────────────────────
# `chat_stream()` is a generator yielding incremental chunks so long-running
# calls (background agent turns, Neby cloud chat, …) can stream live instead
# of blocking until the full completion arrives.
#
# Yield contract (each value is a dict):
#   {'type': 'reasoning', 'content': str}  — incremental chain-of-thought delta
#   {'type': 'text',      'content': str}  — incremental answer delta
#   {'type': 'done', 'model': str, 'input_tokens': int, 'output_tokens': int,
#    'reasoning': str}                     — final summary, always last
#
# If the caller abandons the generator early (client disconnect), the
# underlying response is closed by `finally`.

def _openai_stream(*, base_url: str, api_key: str, model: str, messages: List[Dict[str, str]],
                   max_tokens: int, timeout: int, temperature: float, provider: str):
    url = base_url.rstrip('/')
    if not url.endswith('/chat/completions'):
        url += '/chat/completions'
    headers = {'Content-Type': 'application/json', 'Accept': 'text/event-stream'}
    if api_key.strip():
        headers['Authorization'] = f'Bearer {api_key.strip()}'
    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'stream': True,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout, stream=True)
    except requests.RequestException as e:
        raise LLMError(f'{provider}: network error: {e}', provider=provider)
    if resp.status_code != 200:
        detail = resp.text[:400]
        retryable = resp.status_code in (408, 409, 425, 429, 500, 502, 503, 504)
        raise LLMError(
            f'{provider}: HTTP {resp.status_code}: {detail}',
            status=resp.status_code, retryable=retryable, provider=provider,
        )
    out_model = model
    reasoning_parts: List[str] = []
    text_parts: List[str] = []
    usage: dict = {}
    try:
        for raw in resp.iter_lines(decode_unicode=True):
            if raw is None:
                continue
            line = raw.strip()
            if not line.startswith('data:'):
                continue
            data = line[5:].strip()
            if not data or data == '[DONE]':
                continue
            try:
                chunk = json.loads(data)
            except ValueError:
                continue
            if isinstance(chunk.get('error'), dict) and chunk['error']:
                raise LLMError(f"{provider}: {chunk['error'].get('message') or chunk['error']}", provider=provider)
            if chunk.get('model'):
                out_model = chunk['model']
            if chunk.get('usage'):
                usage = chunk['usage']
            choices = chunk.get('choices') or []
            if not choices:
                continue
            delta = choices[0].get('delta') or {}
            r = delta.get('reasoning_content') or delta.get('reasoning') or ''
            if r:
                reasoning_parts.append(r)
                yield {'type': 'reasoning', 'content': r}
            c = delta.get('content')
            if isinstance(c, list):
                c = ''.join(p.get('text', '') if isinstance(p, dict) else str(p) for p in c)
            if c:
                text_parts.append(c)
                yield {'type': 'text', 'content': c}
            if choices[0].get('finish_reason') is not None:
                break
    finally:
        resp.close()
    yield {'type': 'done', 'model': out_model,
           'input_tokens': int(usage.get('prompt_tokens') or 0),
           'output_tokens': int(usage.get('completion_tokens') or 0),
           'reasoning': ''.join(reasoning_parts).strip()}


def _anthropic_stream(*, base_url: str, api_key: str, model: str, messages: List[Dict[str, str]],
                      max_tokens: int, timeout: int, temperature: float, provider: str):
    url = base_url.rstrip('/')
    if not url.endswith('/v1/messages'):
        url = url.rstrip('/')
        url += '/v1/messages' if not url.endswith('/v1') else '/messages'
    system, convo = _split_system(messages)
    if not convo:
        convo = [{'role': 'user', 'content': 'Hello'}]
    if convo[0]['role'] != 'user':
        convo = [{'role': 'user', 'content': '(continue)'}] + convo
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
        'x-api-key': api_key.strip(),
        'anthropic-version': '2023-06-01',
    }
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'stream': True,
        'messages': [{'role': m['role'] if m['role'] != 'system' else 'user', 'content': m['content']} for m in convo],
    }
    if system:
        payload['system'] = system
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout, stream=True)
    except requests.RequestException as e:
        raise LLMError(f'{provider}: network error: {e}', provider=provider)
    if resp.status_code != 200:
        detail = resp.text[:400]
        retryable = resp.status_code in (408, 409, 425, 429, 500, 502, 503, 504)
        raise LLMError(
            f'{provider}: HTTP {resp.status_code}: {detail}',
            status=resp.status_code, retryable=retryable, provider=provider,
        )
    out_model = model
    reasoning_parts: List[str] = []
    text_parts: List[str] = []
    usage: dict = {}
    try:
        for raw in resp.iter_lines(decode_unicode=True):
            if raw is None:
                continue
            line = raw.strip()
            if not line.startswith('data:'):
                continue
            data = line[5:].strip()
            if not data:
                continue
            try:
                event = json.loads(data)
            except ValueError:
                continue
            etype = event.get('type')
            if etype == 'error':
                err = event.get('error') or {}
                raise LLMError(f"{provider}: {err.get('message') or err}", provider=provider)
            if etype == 'message_start':
                out_model = (event.get('message') or {}).get('model') or out_model
            elif etype == 'message_delta':
                usage = event.get('usage') or usage
            elif etype == 'content_block_delta':
                delta = event.get('delta') or {}
                if delta.get('type') == 'thinking_delta':
                    r = delta.get('thinking') or ''
                    reasoning_parts.append(r)
                    yield {'type': 'reasoning', 'content': r}
                elif delta.get('type') == 'text_delta':
                    c = delta.get('text') or ''
                    text_parts.append(c)
                    yield {'type': 'text', 'content': c}
            elif etype == 'message_stop':
                break
    finally:
        resp.close()
    yield {'type': 'done', 'model': out_model,
           'input_tokens': int(usage.get('input_tokens') or 0),
           'output_tokens': int(usage.get('output_tokens') or 0),
           'reasoning': ''.join(reasoning_parts).strip()}


def _gemini_stream(*, base_url: str, api_key: str, model: str, messages: List[Dict[str, str]],
                   max_tokens: int, timeout: int, temperature: float, provider: str):
    url = f"{base_url.rstrip('/')}/models/{model}:streamGenerateContent?alt=sse"
    system, convo = _split_system(messages)
    contents = []
    for m in convo:
        role = 'model' if m['role'] == 'assistant' else 'user'
        contents.append({'role': role, 'parts': [{'text': m['content']}]})
    if not contents:
        contents = [{'role': 'user', 'parts': [{'text': 'Hello'}]}]
    headers = {'Content-Type': 'application/json', 'x-goog-api-key': api_key.strip()}
    payload: dict = {
        'contents': contents,
        'generationConfig': {'maxOutputTokens': max_tokens, 'temperature': temperature},
    }
    if system:
        payload['systemInstruction'] = {'parts': [{'text': system}]}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout, stream=True)
    except requests.RequestException as e:
        raise LLMError(f'{provider}: network error: {e}', provider=provider)
    if resp.status_code != 200:
        detail = resp.text[:400]
        retryable = resp.status_code in (408, 409, 425, 429, 500, 502, 503, 504)
        raise LLMError(
            f'{provider}: HTTP {resp.status_code}: {detail}',
            status=resp.status_code, retryable=retryable, provider=provider,
        )
    usage: dict = {}
    text_parts: List[str] = []
    try:
        for raw in resp.iter_lines(decode_unicode=True):
            if raw is None:
                continue
            line = raw.strip()
            if not line:
                continue
            if line.startswith('data:'):
                line = line[5:].strip()
            if not line or line == '[DONE]':
                continue
            try:
                chunk = json.loads(line)
            except ValueError:
                continue
            if chunk.get('error'):
                err = chunk['error']
                raise LLMError(f"{provider}: {err.get('message') or err}", status=err.get('code') or 0, provider=provider)
            if chunk.get('usageMetadata'):
                usage = chunk['usageMetadata']
            parts = []
            try:
                parts = chunk['candidates'][0]['content']['parts']
            except (KeyError, IndexError, TypeError):
                pass
            c = ''.join(p.get('text', '') for p in parts if isinstance(p, dict))
            if c:
                text_parts.append(c)
                yield {'type': 'text', 'content': c}
    finally:
        resp.close()
    yield {'type': 'done', 'model': model,
           'input_tokens': int(usage.get('promptTokenCount') or 0),
           'output_tokens': int(usage.get('candidatesTokenCount') or 0),
           'reasoning': ''}


def chat_stream(*, format: str, base_url: str, api_key: str, model: str,
                messages: List[Dict[str, str]], max_tokens: int = 4096,
                timeout: int = 180, temperature: float = 0.2,
                provider: str = ''):
    """Streaming twin of `chat()` — same validation, incremental yields.

    The generator yields dicts (see contract above) and always finishes with
    a {'type': 'done', ...} summary. Raises LLMError on failure, exactly like
    `chat()`.
    """
    fmt = (format or FORMAT_OPENAI).strip().lower()
    provider = provider or fmt
    model = (model or '').strip()
    if not model:
        raise LLMError(f'{provider}: a model id is required', retryable=False, provider=provider)
    if not (base_url or '').strip():
        raise LLMError(f'{provider}: a base URL is required', retryable=False, provider=provider)
    messages = _emotionless_messages(messages)
    if not messages:
        raise LLMError(f'{provider}: no messages supplied', retryable=False, provider=provider)
    try:
        if fmt == FORMAT_ANTHROPIC:
            yield from _anthropic_stream(base_url=base_url, api_key=api_key, model=model, messages=messages,
                                         max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=provider)
        elif fmt == FORMAT_GEMINI:
            yield from _gemini_stream(base_url=base_url, api_key=api_key, model=model, messages=messages,
                                      max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=provider)
        elif fmt == FORMAT_OPENAI:
            yield from _openai_stream(base_url=base_url, api_key=api_key, model=model, messages=messages,
                                      max_tokens=max_tokens, timeout=timeout, temperature=temperature, provider=provider)
        else:
            raise LLMError(f'unsupported API format: {fmt}', retryable=False, provider=provider)
    except LLMError:
        raise
    except Exception as e:  # safety net — never leak tracebacks to callers
        raise LLMError(f'{provider}: {e}', provider=provider)
