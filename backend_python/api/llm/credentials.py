"""Credential resolution + catalog assembly.

Priority order for an official provider call, per user:

1. **Custom provider row** (`UserLLMProvider.provider == 'custom'`) — fully
   user-defined name/URL/key/models (BYOK any OpenAI/Anthropic/Gemini-style
   endpoint).
2. **User BYOK row** (`UserLLMProvider.provider == <preset slug>`) — the
   user's own key for a known provider, overrides everything below.
3. **Admin bot config** (`BotConfig` with the same provider) — the site
   administrator can share a key/config with everyone (e.g. a free Agnes key
   so every NEBian gets Agnes out of the box).
4. **Server environment** (`settings.LLM_PROVIDER_KEYS[<slug>]`, populated
   from `<SLUG>_API_KEY` env vars).

Scraper/community providers resolve to their BotConfig exactly as before —
nothing in this module changes how Qwen & friends are called.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from django.conf import settings

from .crypto import decrypt_key
from .registry import OFFICIAL_PRESETS, ProviderPreset, preset


@dataclass
class ResolvedProvider:
    slug: str                 # preset slug, or 'custom'
    label: str                # display name (bot name / custom name)
    format: str               # openai | anthropic | gemini | scraper
    base_url: str
    api_key: str
    model: str
    context_window: int
    max_output_tokens: int
    source: str               # custom | byok | bot | env | scraper | unavailable
    official: bool
    extra_headers: dict = field(default_factory=dict)
    preset: Optional[ProviderPreset] = None
    user_provider_id: str = ''
    bot_config_id: int = 0
    free_note: str = ''


def _env_key(slug: str) -> str:
    keys = getattr(settings, 'LLM_PROVIDER_KEYS', {}) or {}
    key = (keys.get(slug) or '').strip()
    if key:
        return key
    p = preset(slug)
    if p and p.key_env:
        return (os.environ.get(p.key_env, '') or '').strip()
    return ''


def _real_user(user):
    """Normalize to a persisted platform user.

    Background-agent admins (mobile + website) are plain ``api.User`` model
    instances — NOT Django auth users, so they have no ``is_authenticated``
    attribute. Gate on ``pk`` instead. (Previously the is_authenticated check
    silently dropped every BYOK row and sessions fell back to Qwen.)"""
    if user is None or not getattr(user, 'pk', None):
        return None
    return user


def _user_row(user, slug: str):
    user = _real_user(user)
    if user is None:
        return None
    from api.models import UserLLMProvider
    return UserLLMProvider.objects.filter(
        user=user, provider=slug, enabled=True
    ).order_by('id').first()


def resolve(user, slug: str, model: str = '', user_provider_id: str = '') -> Optional[ResolvedProvider]:
    """Resolve the best concrete provider for `user` asking for `slug`.

    `slug 'custom'` requires `user_provider_id` pointing at the user's row.
    Returns None when nothing can serve the request.
    """
    from api.models import BotConfig, UserLLMProvider
    slug = (slug or '').strip().lower()

    # --- User-defined custom endpoint -------------------------------------
    if slug == 'custom':
        user = _real_user(user)
        if user is None or not user_provider_id:
            return None
        row = UserLLMProvider.objects.filter(
            pk=user_provider_id, user=user, provider='custom', enabled=True
        ).first()
        if not row:
            return None
        models = _row_models(row)
        return ResolvedProvider(
            slug='custom', label=row.name or 'Custom provider', format=row.api_format,
            base_url=row.base_url.strip(), api_key=decrypt_key(row.api_key),
            model=model or row.default_model or (models[0] if models else ''),
            context_window=row.context_window or 131072,
            max_output_tokens=row.max_output_tokens or 4096,
            source='custom', official=True, user_provider_id=str(row.id),
        )

    p = preset(slug)
    if not p:
        return None

    # --- Community web models: unchanged behavior --------------------------
    if not p.official:
        bot_qs = BotConfig.objects.filter(enabled=True, provider=slug)
        if slug == 'qwen' and model:
            bot = bot_qs.filter(model__iexact=model).first() or bot_qs.first()
        else:
            bot = bot_qs.first()
        if not bot and slug not in ('k2think', 'poolside', 'motiftech', 'tryingopen', 'longcat', 'geminiweb', 'metaai'):
            return None
        return ResolvedProvider(
            slug=slug, label=(bot.display_name or bot.name or p.label) if bot else p.label, format=p.format,
            base_url=(bot.api_url or p.base_url) if bot else p.base_url, api_key=(bot.api_key or '') if bot else '',
            model=model or (bot.model if bot else '') or p.default_model,
            context_window=p.context_window, max_output_tokens=p.max_output_tokens,
            source='scraper', official=False, preset=p, bot_config_id=bot.id if bot else None,
        )

    # --- Official: user BYOK row -------------------------------------------
    row = _user_row(user, slug)
    if row:
        return ResolvedProvider(
            slug=slug, label=f'{p.label} (your key)', format=p.format,
            base_url=(row.base_url or p.base_url).strip(),
            api_key=decrypt_key(row.api_key),
            model=model or row.default_model or p.default_model,
            context_window=row.context_window or p.context_window,
            max_output_tokens=row.max_output_tokens or p.max_output_tokens,
            source='byok', official=True, preset=p, user_provider_id=str(row.id),
            free_note=p.free_note,
        )

    # --- Admin-shared BotConfig --------------------------------------------
    bot = BotConfig.objects.filter(enabled=True, provider=slug).first()
    if bot and (bot.api_key.strip() or bot.api_url.strip()):
        return ResolvedProvider(
            slug=slug, label=bot.display_name or bot.name or p.label, format=p.format,
            base_url=(bot.api_url or p.base_url).strip(),
            api_key=bot.api_key or '',
            model=model or bot.model or p.default_model,
            context_window=p.context_window, max_output_tokens=p.max_output_tokens,
            source='bot', official=True, preset=p, bot_config_id=bot.id,
            free_note=p.free_note,
        )

    # --- Server environment key or free preset -----------------------------
    key = _env_key(slug)
    if key or not p.key_required:
        return ResolvedProvider(
            slug=slug, label=p.label, format=p.format,
            base_url=p.base_url, api_key=key or p.default_key or '',
            model=model or p.default_model,
            context_window=p.context_window, max_output_tokens=p.max_output_tokens,
            source='env' if key else 'free', official=True,
            extra_headers=dict(p.extra_headers or {}),
            preset=p, free_note=p.free_note,
        )
    return None


def _row_models(row) -> List[str]:
    try:
        models = json.loads(row.models_json or '[]')
        return [str(m).strip() for m in models if str(m).strip()]
    except (ValueError, TypeError):
        return []


def _qwen_live_models(bots=None):
    """Merge the live catalog from chat.qwen.ai (via the existing 5-minute
    cached fetcher). Returns (models, default_id). Never raises — fails soft
    so the picker always renders, worst case with the static preset list.

    Custom BotConfig model slugs are excluded from auth requirements anyway;
    every fetched model id is a first-class upstream id the runner can pass
    to the Qwen web session directly."""
    try:
        from api.qwen_utils.models import fetch_models as _fetch
        raw = _fetch() or []
    except Exception:
        return [], None
    models = []
    default_id = None
    for m in raw:
        if not m.get('is_active', True):
            continue
        mid = (m.get('id') or '').strip()
        if not mid:
            continue
        caps = m.get('capabilities') or {}
        note = ' · '.join(bit for bit, on in (
            ('thinking', caps.get('thinking')),
            ('vision', caps.get('vision')),
            ('search', caps.get('search')),
        ) if on)
        models.append({'id': mid, 'label': m.get('name') or mid, 'note': note})
        if default_id is None and caps.get('document') and caps.get('vision'):
            default_id = mid
    return models, default_id


def default_selection(user) -> dict:
    """What an agent session gets when the user picks nothing: the user's
    first saved BYOK key for an official provider, else the legacy Qwen
    bot if configured, else the first env-configured official provider."""
    from api.models import BotConfig, UserLLMProvider
    live_default = None
    try:
        from api.qwen_utils.models import get_default_model
        live_default = get_default_model()
    except Exception:
        pass

    user_obj = _real_user(user)
    if user_obj is not None:
        byok = UserLLMProvider.objects.filter(
            user=user_obj, enabled=True,
        ).exclude(provider='custom').order_by('-updated_at').first()
        if byok and byok.api_key:
            from .registry import preset as _preset
            p = _preset(byok.provider)
            if p and p.official:
                return {
                    'kind': 'official', 'slug': byok.provider,
                    'model': byok.default_model or p.default_model or live_default or '',
                }

    qwen = BotConfig.objects.filter(enabled=True, provider='qwen').order_by('id').first()
    if qwen:
        return {'kind': 'community', 'slug': 'qwen', 'model': qwen.model or live_default or 'qwen3.8-max'}
    for p in OFFICIAL_PRESETS:
        if resolve(user, p.slug):
            return {'kind': 'official', 'slug': p.slug, 'model': ''}
    return {'kind': 'community', 'slug': 'qwen', 'model': live_default or 'qwen3.8-max'}


def _masked_row_key(row) -> str:
    if not row or not row.api_key:
        return ''
    try:
        from .crypto import mask_key, decrypt_key as _dec
        return mask_key(_dec(row.api_key))
    except Exception:
        return 'set'
