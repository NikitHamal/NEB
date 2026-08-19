"""Runtime glue between background-agent sessions and the LLM registry.

The runner stores a lightweight selection on each session:

- `llm_provider = ''`                         → legacy behavior (Qwen bot).
- `llm_provider = 'agnes'|'openai'|...`      → official preset (BYOK/admin/env key).
- `llm_provider = 'custom'` + `llm_model`    → reserved; custom providers are
  referenced through `llm_provider_id` instead.
"""
from __future__ import annotations

from typing import Optional

from .client import ChatResult, chat, chat_stream
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


def call_session_provider_stream(session, resolved: ResolvedProvider, *, system_prompt: str,
                                 user_prompt: str, max_tokens: int, timeout: int = 300):
    """Streaming twin of `call_session_provider()`.

    Yields the `chat_stream()` chunk dicts: {'type': 'reasoning'|'text'|
    'done', ...} so callers can relay deltas live (Redis pub/sub, SSE, ...)
    instead of waiting for the full completion."""
    messages = []
    if system_prompt and system_prompt.strip():
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_prompt})
    yield from chat_stream(
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
            'qwen', 'egov', 'deepai', 'inception', 'k2think', 'poolside', 'motiftech', 'metaai'):
        return {'llm_provider': '', 'llm_model': '', 'llm_provider_id': ''}
    return {
        'llm_provider': slug if slug != 'custom' else 'custom',
        'llm_model': model,
        'llm_provider_id': user_provider_id if slug == 'custom' else '',
    }


# ---------------------------------------------------------------------------
# Display helpers — one source of truth for "which model is this session using"
# so the topbar, serializers, mobile API and runner never disagree.
# ---------------------------------------------------------------------------

from .registry import preset as _preset  # noqa: E402


def model_display_label(slug: str, model: str = '') -> str:
    """Pretty label for a (slug, model) pair — 'Agnes · agnes-2.0-flash',
    'Qwen 3.8 Max Preview', etc. Community slugs use live upstream names when
    the 5-minute cached catalog has them."""
    slug = (slug or '').strip().lower()
    model = (model or '').strip()
    if not slug or slug == 'qwen':
        if not model:
            return 'Qwen (default)'
        name = ''
        try:
            from api.qwen_utils.models import fetch_models
            for m in fetch_models() or []:
                if (m.get('id') or '').lower() == model.lower():
                    name = m.get('name') or ''
                    break
        except Exception:
            name = ''
        return name or f'Qwen ({model})'
    p = _preset(slug)
    if p:
        label = p.label
        if model and model.lower() not in p.label.lower():
            label = f'{p.label} · {model}'
        return label
    if slug == 'custom':
        return f'Custom · {model}' if model else 'Custom provider'
    return f'{slug} · {model}' if model else slug


def describe_session_llm(session) -> dict:
    """Lightweight LLM summary for a session (no DB hits)."""
    slug = (getattr(session, 'llm_provider', '') or '').strip().lower()
    model = (getattr(session, 'llm_model', '') or '').strip()
    if not slug:
        live = ''
        try:
            from api.qwen_utils.models import get_default_model
            live = get_default_model()
        except Exception:
            pass
        model = live or 'qwen3.8-max'
        label = model_display_label('qwen', model) + ' (default)'
        return {'provider': 'qwen', 'model': model, 'label': label, 'official': False}
    p = _preset(slug)
    return {
        'provider': slug,
        'model': model or (p.default_model if p else ''),
        'label': model_display_label(slug, model) if p or slug == 'custom'
                 else (f'{slug} · {model}' if model else slug),
        'official': bool(p and p.official) or slug == 'custom',
    }


def default_llm_label(user) -> str:
    """Label for what a *new* session would use if the user picks nothing."""
    from .credentials import default_selection  # lazy: avoids import cycle
    try:
        sel = default_selection(user)
    except Exception:
        live = ''
        try:
            from api.qwen_utils.models import get_default_model
            live = get_default_model()
        except Exception:
            pass
        return model_display_label('qwen', live or 'qwen3.8-max')
    return model_display_label(sel.get('slug') or 'qwen', sel.get('model') or '')


def default_model_state(user, provider=None) -> dict:
    """`model` summary for the dashboard/mobile state endpoints: what a
    session gets when the picker is left on 'server default'.
    Live/community-aware (never pinned to a specific Qwen version) and
    `configured` reflects *any* usable backend (qwen bot, legacy provider
    object, or a resolvable official preset)."""
    from .credentials import default_selection, resolve as _resolve
    from .registry import OFFICIAL_PRESETS
    try:
        sel = default_selection(user)
        slug = sel.get('slug') or 'qwen'
        model = sel.get('model') or ''
        label = model_display_label(slug, model)
    except Exception:
        slug, model, label = 'qwen', 'qwen3.8-max', 'Qwen 3.8 Max'
    try:
        label = default_llm_label(user) or label
    except Exception:
        pass
    configured = bool(provider)
    if not configured:
        try:
            from api.models import BotConfig  # lazy: Django apps must be ready
            configured = BotConfig.objects.filter(enabled=True, provider='qwen').exists()
        except Exception:
            configured = False
    if not configured:
        try:
            configured = any(_resolve(user, p.slug) for p in OFFICIAL_PRESETS)
        except Exception:
            configured = False
    if not model:
        try:
            from api.qwen_utils.models import get_default_model
            model = get_default_model() or 'qwen3.8-max'
        except Exception:
            model = 'qwen3.8-max'
    return {'provider': slug, 'model': model, 'label': label, 'configured': configured}
