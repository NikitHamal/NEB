"""
Generic OpenAI-compatible chat-completions client.

Used by the admin panel's "Custom provider" mode — point at any URL that
accepts POST with the standard /v1/chat/completions body and returns the
standard response shape. Works with OpenAI, Together, Groq, OpenRouter,
local Ollama (with --openai-compat), LM Studio, vLLM, etc.

If the endpoint is OpenAI-compatible but lives at a different path (e.g.
`/v1/chat/completions` vs `/api/v2/chat/completions`), just put the full URL
in the admin's `api_url` field.
"""
import logging
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class CustomProviderError(Exception):
    pass


def call_custom(
    api_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_message: str,
    max_tokens: int = 500,
    timeout: int = 60,
) -> Optional[str]:
    """Send a chat-completion request to any OpenAI-compatible endpoint.

    Returns the assistant text or None on failure. Raises CustomProviderError
    only on configuration errors (missing URL / model). Network/HTTP errors
    are logged and return None so the caller (the bot) can record the
    failure without crashing.
    """
    if not api_url or not api_url.strip():
        raise CustomProviderError('api_url is required for custom provider')
    if not model or not model.strip():
        raise CustomProviderError('model is required for custom provider')

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if api_key and api_key.strip():
        headers['Authorization'] = f'Bearer {api_key.strip()}'

    messages = []
    if system_prompt and system_prompt.strip():
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_message})

    payload = {
        'model': model.strip(),
        'messages': messages,
        'max_tokens': max_tokens,
        'stream': False,
    }

    t0 = time.time()
    try:
        resp = requests.post(api_url.strip(), json=payload, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        logger.error(f"custom_provider: transport error: {e}")
        return None

    resp.encoding = 'utf-8'

    dt_ms = int((time.time() - t0) * 1000)
    if resp.status_code != 200:
        logger.error(
            f"custom_provider: HTTP {resp.status_code} from {api_url} in {dt_ms}ms: {resp.text[:300]}"
        )
        return None

    try:
        data = resp.json()
    except ValueError:
        logger.error(f"custom_provider: non-JSON response from {api_url}: {resp.text[:200]}")
        return None

    # OpenAI shape: choices[0].message.content
    try:
        content = data['choices'][0]['message']['content']
    except (KeyError, IndexError, TypeError):
        logger.error(f"custom_provider: unexpected response shape: {str(data)[:300]}")
        return None

    if not content:
        return None

    text = content.strip()
    logger.info(f"custom_provider: {api_url} model={model} reply_chars={len(text)} in {dt_ms}ms")
    return text
