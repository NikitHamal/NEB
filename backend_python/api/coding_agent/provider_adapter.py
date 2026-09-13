"""Provider adapter — call AI providers uniformly for the agent."""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .constants import PROVIDER_DEFAULT_MODEL, PROVIDER_MAX_OUTPUT_TOKENS

logger = logging.getLogger(__name__)


@dataclass
class ProviderCompletion:
    text: str
    provider: str
    model: str
    duration_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    error: Optional[str] = None


class ProviderError(Exception):
    pass


def _truncate_to(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + '\n\n[... truncated ' + str(len(text) - limit) + ' chars ...]'


def _safe_json_chat(api_url: str, api_key: str, model: str, messages: List[Dict[str, str]], max_tokens: int, timeout: int) -> ProviderCompletion:
    import requests

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if api_key and api_key.strip():
        headers['Authorization'] = 'Bearer ' + api_key.strip()
    payload = {
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': 0.2,
        'stream': False,
    }
    t0 = time.time()
    try:
        resp = requests.post(api_url.rstrip('/'), json=payload, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        raise ProviderError('network error: ' + str(e))
    dt_ms = int((time.time() - t0) * 1000)
    if resp.status_code != 200:
        raise ProviderError('HTTP ' + str(resp.status_code) + ': ' + resp.text[:300])
    try:
        data = resp.json()
    except ValueError:
        raise ProviderError('non-JSON response from ' + api_url)
    try:
        text = data['choices'][0]['message']['content']
    except (KeyError, IndexError, TypeError):
        raise ProviderError('unexpected response shape: ' + str(data)[:300])
    if isinstance(text, list):
        text = ''.join([p.get('text', '') if isinstance(p, dict) else str(p) for p in text])
    return ProviderCompletion(
        text=(text or '').strip(),
        provider='custom',
        model=model,
        duration_ms=dt_ms,
        input_tokens=int((data.get('usage') or {}).get('prompt_tokens') or 0),
        output_tokens=int((data.get('usage') or {}).get('completion_tokens') or 0),
    )


def _call_qwen(messages: List[Dict[str, str]], model: str, max_tokens: int, timeout: int) -> ProviderCompletion:
    from api import qwen_proxy
    from api.neby import call_ai_api
    from api.models import BotConfig

    cfg = BotConfig.objects.filter(provider='qwen').first()
    target_model = model or (cfg.model if cfg and cfg.model else 'qwen3.8-max')
    system = ''
    user = ''
    file_paths: List[str] = []
    
    for m in messages:
        if m['role'] == 'system' and not system:
            system = m['content']
        elif m['role'] == 'user':
            user += '\n' + m['content']
            if 'attachments' in m and isinstance(m['attachments'], list):
                for att in m['attachments']:
                    if isinstance(att, dict) and att.get('path'):
                        file_paths.append(att['path'])
            elif 'file_paths' in m and isinstance(m['file_paths'], list):
                file_paths.extend(m['file_paths'])
        elif m['role'] == 'assistant':
            user += '\n\n[Previous assistant turn]: ' + m['content']
            
    user = user.strip()
    t0 = time.time()
    text = None
    
    try:
        text = qwen_proxy.call_qwen(
            system_prompt=system,
            user_message=user,
            model=target_model,
            max_tokens=max_tokens,
            file_paths=file_paths if file_paths else None,
        )
    except Exception as e:
        logger.warning("Direct qwen_proxy call failed: %s. Falling back to call_ai_api.", e)
        
    if not text:
        text = call_ai_api(system, user, cfg)
        
    dt_ms = int((time.time() - t0) * 1000)
    if not text:
        raise ProviderError('Qwen backend returned no text (rate limited?)')
    return ProviderCompletion(
        text=text,
        provider='qwen',
        model=target_model,
        duration_ms=dt_ms,
        input_tokens=len(user) // 4,
        output_tokens=len(text) // 4,
    )


def _call_inception(messages: List[Dict[str, str]], model: str, max_tokens: int) -> ProviderCompletion:
    from api.inception_proxy import simple_chat

    sys = ''
    user_parts: List[str] = []
    for m in messages:
        if m['role'] == 'system':
            sys += '\n' + m['content']
        elif m['role'] == 'user':
            user_parts.append(m['content'])
        elif m['role'] == 'assistant':
            user_parts.append('\n[Previous assistant]: ' + m['content'])
    sys = sys.strip()
    user_msg = '\n\n'.join(user_parts).strip()
    t0 = time.time()
    text = simple_chat(
        user_message=user_msg,
        model=model or 'mercury-2',
        system_prompt=sys,
        max_tokens=max_tokens,
    )
    dt_ms = int((time.time() - t0) * 1000)
    if not text:
        raise ProviderError('Inception returned no text')
    return ProviderCompletion(
        text=text,
        provider='inception',
        model=model or 'mercury-2',
        duration_ms=dt_ms,
        input_tokens=len(user_msg) // 4,
        output_tokens=len(text) // 4,
    )


def _call_deepai(messages: List[Dict[str, str]], model: str, max_tokens: int) -> ProviderCompletion:
    from api.deepai_proxy import simple_chat

    sys = ''
    user_parts: List[str] = []
    for m in messages:
        if m['role'] == 'system':
            sys += '\n' + m['content']
        elif m['role'] == 'user':
            user_parts.append(m['content'])
        elif m['role'] == 'assistant':
            user_parts.append('\n[Previous assistant]: ' + m['content'])
    sys = sys.strip()
    user_msg = '\n\n'.join(user_parts).strip()
    t0 = time.time()
    text = simple_chat(
        user_message=user_msg,
        model=model or 'standard',
        system_prompt=sys,
    )
    dt_ms = int((time.time() - t0) * 1000)
    if not text:
        raise ProviderError('DeepAI returned no text')
    return ProviderCompletion(
        text=text,
        provider='deepai',
        model=model or 'standard',
        duration_ms=dt_ms,
        input_tokens=len(user_msg) // 4,
        output_tokens=len(text) // 4,
    )


def _call_qwencloud(messages: List[Dict[str, str]], model: str, max_tokens: int) -> ProviderCompletion:
    from api.qwencloud_proxy import simple_chat

    sys = ''
    user_parts: List[str] = []
    for m in messages:
        if m['role'] == 'system':
            sys += '\n' + m['content']
        elif m['role'] == 'user':
            user_parts.append(m['content'])
        elif m['role'] == 'assistant':
            user_parts.append('\n[Assistant prev]: ' + m['content'])
    sys = sys.strip()
    user_msg = '\n\n'.join(user_parts).strip()
    t0 = time.time()
    text = simple_chat(
        user_message=user_msg,
        model=model or 'qwen3-coder-plus',
        system_prompt=sys,
    )
    dt_ms = int((time.time() - t0) * 1000)
    if not text or text.startswith('[Error]'):
        raise ProviderError(f'QwenCloud returned no text: {text[:120]}')
    return ProviderCompletion(
        text=text,
        provider='qwencloud',
        model=model or 'qwen3-coder-plus',
        duration_ms=dt_ms,
        input_tokens=len(user_msg) // 4,
        output_tokens=len(text) // 4,
    )


def call_for_agent(
    provider: str,
    model: str,
    messages: List[Dict[str, str]],
    *args: Any,
    api_url: str = '',
    api_key: str = '',
    timeout: int = 180,
    **kwargs: Any,
) -> ProviderCompletion:
    provider = (provider or 'qwen').strip().lower()
    if not model:
        model = PROVIDER_DEFAULT_MODEL.get(provider, model)
    max_tokens = PROVIDER_MAX_OUTPUT_TOKENS.get(provider, 4096)
    truncated = _truncate_messages(messages)
    try:
        if provider == 'qwen':
            return _call_qwen(truncated, model, max_tokens, timeout)
        if provider == 'inception':
            return _call_inception(truncated, model, max_tokens)
        if provider == 'deepai':
            return _call_deepai(truncated, model, max_tokens)
        if provider == 'qwencloud':
            return _call_qwencloud(truncated, model, max_tokens)
        if provider == 'custom':
            return _safe_json_chat(api_url, api_key, model, truncated, max_tokens, timeout)
    except ProviderError:
        raise
    except Exception as e:
        raise ProviderError(str(e))
    raise ProviderError('unknown provider: ' + provider)


def _truncate_messages(messages: List[Dict[str, str]], char_budget: int = 60_000) -> List[Dict[str, str]]:
    total = sum(len(m['content']) for m in messages)
    if total <= char_budget:
        return messages
    keep_recent = char_budget // 2
    out: List[Dict[str, str]] = []
    used = 0
    for m in reversed(messages):
        c = m['content']
        if used + len(c) > keep_recent and m['role'] != 'system':
            if out and out[-1]['role'] != 'system':
                out[-1] = {'role': out[-1]['role'], 'content': c[:keep_recent - used] + '\n[... truncated ...]'}
            continue
        out.append(m)
        used += len(c)
    out.reverse()
    head = messages[0:1] if messages and messages[0]['role'] == 'system' else []
    return head + out


def call_plain(provider: str, model: str, system_prompt: str, user_message: str, **kwargs: Any) -> str:
    completion = call_for_agent(
        provider=provider,
        model=model,
        messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_message}],
        **kwargs,
    )
    return completion.text


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)
