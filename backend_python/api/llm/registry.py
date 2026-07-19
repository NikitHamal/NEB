"""Provider & model registry — the single source of truth for every LLM
backend NEBians can talk to.

Two families, kept deliberately distinct:

1. **Official API providers** (Agnes, OpenAI, Anthropic, Gemini, DeepSeek and
   any user-defined custom endpoint) — called through their official request
   formats by `api.llm.client`. Users can bring their own key (BYOK), or the
   site admin can share a key per provider; servers keep scraper models and
   official APIs fully separate.

2. **Community web models** (Qwen, AI4Bharat, eGov, DeepAI, Inception) —
   reverse-engineered web frontends that keep their existing proxies
   untouched. They are listed here only so every picker renders from one
   catalog.

Everything here is data — no service code — so future features (Neby bot,
background agent, arena, whatever comes next) import the same registry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

# Request formats the unified client knows how to speak.
FORMAT_OPENAI = 'openai'        # POST {base}/chat/completions (OpenAI-style)
FORMAT_ANTHROPIC = 'anthropic'  # POST {base}/v1/messages (Claude Messages API)
FORMAT_GEMINI = 'gemini'        # POST {base}/models/{model}:generateContent
FORMAT_SCRAPER = 'scraper'      # Existing NEBians web proxies (qwen & friends)

OFFICIAL_FORMATS = (FORMAT_OPENAI, FORMAT_ANTHROPIC, FORMAT_GEMINI)

SCRAPER_PROVIDERS = ('qwen', 'ai4bharat', 'egov', 'deepai', 'inception')


@dataclass(frozen=True)
class ModelSpec:
    id: str
    label: str
    note: str = ''


@dataclass(frozen=True)
class ProviderPreset:
    slug: str
    label: str
    format: str
    base_url: str
    default_model: str
    models: List[ModelSpec]
    context_window: int = 131072
    max_output_tokens: int = 6000
    key_env: str = ''                  # settings/env fallback, e.g. AGNES_API_KEY
    key_required: bool = True
    free_note: str = ''                # marketing note shown in pickers
    official: bool = True              # False => community web model (scraper)
    # Scraper presets keep their proxy module name for routing.
    scraper_module: str = ''


OFFICIAL_PRESETS: List[ProviderPreset] = [
    ProviderPreset(
        slug='agnes',
        label='Agnes (Sapiens AI)',
        format=FORMAT_OPENAI,
        base_url='https://apihub.agnes-ai.com/v1',
        default_model='agnes-2.0-flash',
        models=[
            ModelSpec('agnes-2.0-flash', 'Agnes 2.0 Flash', '512K ctx · agents, coding, vision'),
        ],
        context_window=512000,
        key_env='AGNES_API_KEY',
        free_note='Free during launch ($0 / 1M tokens)',
    ),
    ProviderPreset(
        slug='openai',
        label='OpenAI (ChatGPT)',
        format=FORMAT_OPENAI,
        base_url='https://api.openai.com/v1',
        default_model='gpt-5.4-mini',
        models=[
            ModelSpec('gpt-5.4-mini', 'GPT-5.4 Mini', 'Fast + cheap, great for agents'),
            ModelSpec('gpt-5.4-nano', 'GPT-5.4 Nano', 'Cheapest, high volume'),
            ModelSpec('gpt-5.5', 'GPT-5.5', 'Previous flagship'),
            ModelSpec('gpt-5.6-terra', 'GPT-5.6 Terra', 'Balanced newest flagship'),
            ModelSpec('gpt-5.6-sol', 'GPT-5.6 Sol', 'Strongest reasoning'),
            ModelSpec('gpt-5.6-luna', 'GPT-5.6 Luna', 'Budget newest'),
            ModelSpec('gpt-5.2-pro', 'GPT-5.2 Pro', 'Extreme accuracy (slow)'),
        ],
        context_window=400000,
        key_env='OPENAI_API_KEY',
    ),
    ProviderPreset(
        slug='anthropic',
        label='Anthropic (Claude)',
        format=FORMAT_ANTHROPIC,
        base_url='https://api.anthropic.com',
        default_model='claude-sonnet-5',
        models=[
            ModelSpec('claude-sonnet-5', 'Claude Sonnet 5', 'Best speed/intelligence mix'),
            ModelSpec('claude-opus-4-8', 'Claude Opus 4.8', 'Complex agentic coding'),
            ModelSpec('claude-haiku-4-5', 'Claude Haiku 4.5', 'Fastest'),
            ModelSpec('claude-fable-5', 'Claude Fable 5', 'Long-running agents'),
        ],
        context_window=1000000,
        key_env='ANTHROPIC_API_KEY',
    ),
    ProviderPreset(
        slug='gemini',
        label='Google Gemini',
        format=FORMAT_GEMINI,
        base_url='https://generativelanguage.googleapis.com/v1beta',
        default_model='gemini-3.5-flash',
        models=[
            ModelSpec('gemini-3.5-flash', 'Gemini 3.5 Flash', 'Newest fast model'),
            ModelSpec('gemini-3-flash-preview', 'Gemini 3 Flash (Preview)'),
            ModelSpec('gemini-2.5-flash', 'Gemini 2.5 Flash', 'Stable'),
            ModelSpec('gemini-2.5-pro', 'Gemini 2.5 Pro', 'Stable, strongest 2.5'),
        ],
        context_window=1000000,
        key_env='GEMINI_API_KEY',
    ),
    ProviderPreset(
        slug='deepseek',
        label='DeepSeek',
        format=FORMAT_OPENAI,
        base_url='https://api.deepseek.com/v1',
        default_model='deepseek-chat',
        models=[
            ModelSpec('deepseek-chat', 'DeepSeek Chat (V3)', 'Great coder, cheap'),
            ModelSpec('deepseek-reasoner', 'DeepSeek Reasoner (R1)', 'Chain-of-thought'),
        ],
        context_window=128000,
        key_env='DEEPSEEK_API_KEY',
    ),
]

SCRAPER_PRESETS: List[ProviderPreset] = [
    ProviderPreset(
        slug='qwen', label='Qwen (chat.qwen.ai)', format=FORMAT_SCRAPER,
        base_url='https://chat.qwen.ai/api/v2', default_model='qwen3.7-plus',
        models=[ModelSpec('qwen3.7-plus', 'Qwen 3.7 Plus', 'Current default')],
        key_required=False, official=False, scraper_module='qwen_proxy',
    ),
    ProviderPreset(
        slug='ai4bharat', label='AI4Bharat Arena', format=FORMAT_SCRAPER,
        base_url='https://backend.arena.ai4bharat.co', default_model='',
        models=[], key_required=False, official=False, scraper_module='ai4bharat_proxy',
    ),
    ProviderPreset(
        slug='egov', label='eGov Chat AI', format=FORMAT_SCRAPER,
        base_url='https://chat.gov.ph', default_model='AI1',
        models=[
            ModelSpec('AI1', 'eGov AI1'),
            ModelSpec('standard', 'Standard'),
        ],
        key_required=False, official=False, scraper_module='egov_proxy',
    ),
    ProviderPreset(
        slug='deepai', label='DeepAI (deepai.org)', format=FORMAT_SCRAPER,
        base_url='https://api.deepai.org', default_model='standard',
        models=[ModelSpec('standard', 'Standard')],
        key_required=False, official=False, scraper_module='deepai_proxy',
    ),
    ProviderPreset(
        slug='inception', label='Inception Labs (Mercury 2)', format=FORMAT_SCRAPER,
        base_url='https://api.inceptionlabs.ai/v1', default_model='mercury-2',
        models=[ModelSpec('mercury-2', 'Mercury 2')],
        key_required=False, official=False, scraper_module='inception_proxy',
    ),
]

ALL_PRESETS = {p.slug: p for p in OFFICIAL_PRESETS + SCRAPER_PRESETS}


def preset(slug: str) -> Optional[ProviderPreset]:
    return ALL_PRESETS.get((slug or '').strip().lower())


def is_official_slug(slug: str) -> bool:
    p = preset(slug)
    return bool(p and p.official)


def default_model_for(slug: str, override: str = '') -> str:
    p = preset(slug)
    if override:
        return override
    return p.default_model if p else override
