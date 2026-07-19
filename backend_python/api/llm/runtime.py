"""Runtime glue between background-agent sessions and the LLM registry.

The runner stores a lightweight selection on each session:

- `llm_provider = ''`                         → legacy behavior (Qwen bot).
- `llm_provider = 'agnes'|'openai'|...`      → official preset (BYOK/admin/env key).
- `llm_provider = 'custom'` + `llm_model`    → reserved; custom providers are
  referenced through `llm_provider_id` instead.
"""
from __future__ import annotations

from typing import Optional

from .client import ChatResult, chat
from .credentials import ResolvedProvider, resolve
from .registry import is_official_slug


def resolve_session_provider(session) -> Optional[ResolvedProvider]:
    """Resolve what should actually be called for this session.

    Returns an official-format ResolvedProvider, or None when the session
    stays on the legacy community path (the runner's existing Qwen code).
    Community scraper picks never cross into the official client."""
    slug = (getattr(session, 'llm_provider', '') or '').strip().lower()
    if not slug:
        return None
    model = (getattr(session, 'llm_model', '') or '').strip()
    user_provider_id = (getattr(session, 'llm_provider_id', '') or '').strip()
    resolved = resolve(session.admin_user, slug, model=model, user_provider_id=user_provider_id)
    if resolved is None or not resolved.official:
        return None
    return resolved


def call_session_provider(session, resolved: ResolvedProvider, *, system_prompt: str,
                          user_prompt: str, max_tokens: int, timeout: int = 300) -> ChatResult:
    """One non-streaming call against the resolved official provider."""
    messages = []
    if system_prompt and system_prompt.strip():
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_prompt})
    return chat(
        format=resolved.format,
        base_url=resolved.base_url,
        api_key=resolved.api_key,
        model=resolved.model,
        messages=messages,
        max_tokens=max_tokens,
        timeout=timeout,
        temperature=0.2,
        provider=resolved.slug,
    )


def selection_payload(slug: str, model: str, user_provider_id: str = '') -> dict:
    """Normalize picker input from web/mobile clients."""
    slug = (slug or '').strip().lower()
    model = (model or '').strip()[:200]
    user_provider_id = (user_provider_id or '').strip()[:36]
    if slug == 'custom' and not user_provider_id:
        return {'llm_provider': '', 'llm_model': '', 'llm_provider_id': ''}
    if slug and slug != 'custom' and not is_official_slug(slug) and slug not in (
            'qwen', 'ai4bharat', 'egov', 'deepai', 'inception'):
        return {'llm_provider': '', 'llm_model': '', 'llm_provider_id': ''}
    return {
        'llm_provider': slug if slug != 'custom' else 'custom',
        'llm_model': model,
        'llm_provider_id': user_provider_id if slug == 'custom' else '',
    }
