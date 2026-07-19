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
from .registry import (
    OFFICIAL_PRESETS, SCRAPER_PRESETS, ProviderPreset, preset, is_official_slug,
)


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


def _user_row(user, slug: str):
    if not user or not getattr(user, 'is_authenticated', False):
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
        if not (user and getattr(user, 'is_authenticated', False) and user_provider_id):
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
        if not bot:
            return None
        return ResolvedProvider(
            slug=slug, label=bot.display_name or bot.name or p.label, format=p.format,
            base_url=bot.api_url or p.base_url, api_key=bot.api_key or '',
            model=model or bot.model or p.default_model,
            context_window=p.context_window, max_output_tokens=p.max_output_tokens,
            source='scraper', official=False, preset=p, bot_config_id=bot.id,
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

    # --- Server environment key --------------------------------------------
    key = _env_key(slug)
    if key:
        return ResolvedProvider(
            slug=slug, label=p.label, format=p.format,
            base_url=p.base_url, api_key=key,
            model=model or p.default_model,
            context_window=p.context_window, max_output_tokens=p.max_output_tokens,
            source='env', official=True, preset=p, free_note=p.free_note,
        )
    return None


def _row_models(row) -> List[str]:
    try:
        models = json.loads(row.models_json or '[]')
        return [str(m).strip() for m in models if str(m).strip()]
    except (ValueError, TypeError):
        return []


def user_custom_provider(user, provider_id: str):
    if not (user and getattr(user, 'is_authenticated', False)):
        return None
    from api.models import UserLLMProvider
    return UserLLMProvider.objects.filter(pk=provider_id, user=user, provider='custom', enabled=True).first()


def catalog_for_user(user) -> dict:
    """Everything a picker needs: official presets (with availability), the
    community models, and the user's own custom providers. No secrets — only
    masked keys / availability flags."""
    from api.models import BotConfig, UserLLMProvider

    byok_rows = {}
    custom_rows = []
    if user and getattr(user, 'is_authenticated', False):
        for row in UserLLMProvider.objects.filter(user=user, enabled=True).order_by('-updated_at'):
            if row.provider == 'custom':
                custom_rows.append(row)
            else:
                byok_rows.setdefault(row.provider, row)

    bots_by_provider = {}
    for bot in BotConfig.objects.filter(enabled=True):
        bots_by_provider.setdefault(bot.provider, []).append(bot)

    official = []
    for p in OFFICIAL_PRESETS:
        byok = byok_rows.get(p.slug)
        bot = (bots_by_provider.get(p.slug) or [None])[0]
        env_key = _env_key(p.slug)
        available = bool(byok and (byok.api_key or byok.base_url)) or \
            bool(bot and (bot.api_key.strip() or bot.api_url.strip())) or bool(env_key)
        official.append({
            'slug': p.slug,
            'label': p.label,
            'format': p.format,
            'baseUrl': p.base_url,
            'contextWindow': p.context_window,
            'freeNote': p.free_note,
            'official': True,
            'available': available,
            'keySource': 'byok' if byok else ('bot' if bot and (bot.api_key.strip() or bot.api_url.strip()) else ('env' if env_key else '')),
            'keyMasked': _masked_row_key(byok) if byok else ('' if not bot else ('set' if bot.api_key.strip() else '')),
            'byokProviderId': str(byok.id) if byok else '',
            'defaultModel': byok.default_model if byok and byok.default_model else p.default_model,
            'models': [{'id': m.id, 'label': m.label, 'note': m.note} for m in p.models],
        })

    community = []
    for p in SCRAPER_PRESETS:
        bots = bots_by_provider.get(p.slug) or []
        models = [{'id': m.id, 'label': m.label, 'note': m.note} for m in p.models]
        for bot in bots:
            if bot.model and all(m['id'].lower() != bot.model.lower() for m in models):
                models.append({
                    'id': bot.model,
                    'label': bot.display_name or bot.name or bot.model,
                    'note': '',
                })
        community.append({
            'slug': p.slug,
            'label': p.label,
            'format': p.format,
            'baseUrl': p.base_url,
            'contextWindow': p.context_window,
            'freeNote': '',
            'official': False,
            'available': bool(bots),
            # Only Qwen community models can drive agent sessions today — the
            # other web models serve Neby bots/arena. Pickers must hide these
            # for agent tasks until a runner adapter exists for them.
            'selectableForAgent': p.slug == 'qwen',
            'keySource': 'scraper' if bots else '',
            'keyMasked': '',
            'byokProviderId': '',
            'defaultModel': bots[0].model if bots and bots[0].model else p.default_model,
            'models': models,
        })

    custom = []
    for row in custom_rows:
        models = _row_models(row)
        custom.append({
            'id': str(row.id),
            'slug': 'custom',
            'label': row.name or 'Custom provider',
            'format': row.api_format,
            'baseUrl': row.base_url,
            'contextWindow': row.context_window or 131072,
            'official': True,
            'available': bool(row.base_url.strip()),
            'keyMasked': _masked_row_key(row),
            'defaultModel': row.default_model or (models[0] if models else ''),
            'models': [{'id': m, 'label': m, 'note': ''} for m in models],
        })

    return {
        'official': official,
        'community': community,
        'custom': custom,
        'defaultSelection': default_selection(user),
    }


def default_selection(user) -> dict:
    """What an agent session gets when the user picks nothing: the legacy
    Qwen bot if configured, else the first available official provider."""
    from api.models import BotConfig
    qwen = BotConfig.objects.filter(enabled=True, provider='qwen').order_by('id').first()
    if qwen:
        return {'kind': 'community', 'slug': 'qwen', 'model': qwen.model or 'qwen3.7-plus'}
    for p in OFFICIAL_PRESETS:
        if resolve(user, p.slug):
            return {'kind': 'official', 'slug': p.slug, 'model': ''}
    return {'kind': 'community', 'slug': 'qwen', 'model': 'qwen3.7-plus'}


def _masked_row_key(row) -> str:
    if not row or not row.api_key:
        return ''
    try:
        from .crypto import mask_key, decrypt_key as _dec
        return mask_key(_dec(row.api_key))
    except Exception:
        return 'set'
