"""LLM access helpers for the Lazy agent.

Wraps the project's existing routed `llm_chat` with the things an agent loop
needs: strict JSON extraction, bounded retries, and a model-tier split so cheap
calls (planning, classification) don't burn the strong provider.
"""

import json
import re

from .lazy_service_bridge import llm_chat

MAX_PARSE_ATTEMPTS = 2


def _strip_fences(raw):
    text = (raw or '').strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json|JSON)?\s*\n?', '', text)
        text = re.sub(r'\n?```\s*$', '', text).strip()
    return text


def extract_json(raw):
    """Pull the first balanced JSON object or array out of a model response.

    Deliberately tolerant: models wrap JSON in prose, emit leading labels, or
    append trailing commentary. We scan for the outermost balanced structure
    while respecting string literals so braces inside content don't break it.
    """
    text = _strip_fences(raw)
    if not text:
        return None

    start = None
    for idx, ch in enumerate(text):
        if ch in '{[':
            start = idx
            break
    if start is None:
        return None

    open_char = text[start]
    close_char = '}' if open_char == '{' else ']'
    depth = 0
    in_string = False
    escaped = False

    for idx in range(start, len(text)):
        ch = text[idx]
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                candidate = text[start:idx + 1]
                try:
                    return json.loads(candidate)
                except Exception:
                    # Try to recover by trimming to the last complete value.
                    trimmed = _salvage(candidate)
                    if trimmed is not None:
                        return trimmed
                    return None
    return None


def _salvage(candidate):
    """Last-resort repair for truncated JSON (common on long documents)."""
    for cut in range(len(candidate) - 1, 0, -1):
        snippet = candidate[:cut]
        if snippet[-1] not in '}])':
            continue
        for suffix in ('', ']', '}]', ']}', '}}'):
            try:
                return json.loads(snippet + suffix)
            except Exception:
                continue
    return None


def json_chat(user, system, prompt, max_tokens=2400, temperature=0.3,
              timeout=90, model_key='neby-pro', attempts=MAX_PARSE_ATTEMPTS):
    """Call the model and parse JSON, retrying once with a stricter reminder."""
    last_raw = ''
    for attempt in range(max(1, attempts)):
        reminder = ''
        if attempt:
            reminder = (
                '\n\nCRITICAL: Your previous reply was not valid JSON. '
                'Return ONLY a single JSON object. No prose, no markdown fences, '
                'no trailing text after the closing brace.'
            )
        raw = llm_chat(
            user, system, prompt + reminder,
            max_tokens=max_tokens, temperature=temperature,
            timeout=timeout, model_key=model_key,
        )
        last_raw = raw or ''
        data = extract_json(last_raw)
        if data is not None:
            return data, last_raw
    return None, last_raw


def text_chat(user, system, prompt, max_tokens=1600, temperature=0.5,
              timeout=90, model_key='neby-pro'):
    raw = llm_chat(
        user, system, prompt,
        max_tokens=max_tokens, temperature=temperature,
        timeout=timeout, model_key=model_key,
    )
    return (raw or '').strip()
