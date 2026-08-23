"""Provider & model registry — the single source of truth for every LLM
backend NEBians can talk to.

Two families, kept deliberately distinct:

1. **Official API providers** (Agnes, OpenAI, Anthropic, Gemini, DeepSeek and
   any user-defined custom endpoint) — called through their official request
   formats by `api.llm.client`. Users can bring their own key (BYOK), or the
   site admin can share a key per provider; servers keep scraper models and
   official APIs fully separate.

2. **Community web models** (Qwen, eGov, DeepAI, Inception) —
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

SCRAPER_PROVIDERS = ('qwen', 'egov', 'deepai', 'inception', 'k2think', 'poolside', 'motiftech', 'metaai', 'tryingopen', 'longcat', 'geminiweb')


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
    ProviderPreset(
        slug='agentrouter',
        label='AgentRouter',
        format=FORMAT_OPENAI,
        base_url='https://agentrouter.org/v1',
        default_model='gpt-5.5',
        models=[
            ModelSpec('gpt-5.5', 'GPT-5.5', 'Fast general-purpose'),
            ModelSpec('claude-opus-4-6', 'Claude Opus 4.6', 'Strong coding & reasoning'),
            ModelSpec('claude-opus-4-8', 'Claude Opus 4.8', 'Latest Claude flagship'),
            ModelSpec('claude-haiku-4-5', 'Claude Haiku 4.5', 'Fastest Claude'),
            ModelSpec('glm-5.2', 'GLM-5.2'),
        ],
        context_window=200000,
        key_env='AGENTROUTER_API_KEY',
    ),
]

SCRAPER_PRESETS: List[ProviderPreset] = [
    ProviderPreset(
        slug='qwen', label='Qwen (chat.qwen.ai)', format=FORMAT_SCRAPER,
        base_url='https://chat.qwen.ai/api/v2', default_model='qwen3.8-max',
        models=[ModelSpec('qwen3.8-max', 'Qwen 3.8 Max', 'Latest flagship'),
                ModelSpec('qwen3.8-max-preview', 'Qwen 3.8 Max (Preview)'),
                ModelSpec('qwen3.7-plus', 'Qwen 3.7 Plus', 'Stable'),
                ModelSpec('qwen3.7-max', 'Qwen 3.7 Max'),
                ModelSpec('qwen3.6-plus', 'Qwen 3.6 Plus'),
                ModelSpec('qwen3.5-plus', 'Qwen 3.5 Plus')],
        context_window=1000000,
        key_required=False, official=False, scraper_module='qwen_proxy',
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
    ProviderPreset(
        slug='k2think', label='K2 Think (k2think.ai)', format=FORMAT_SCRAPER,
        base_url='https://www.k2think.ai', default_model='MBZUAI-IFM/K2-Think-v2',
        models=[ModelSpec('MBZUAI-IFM/K2-Think-v2', 'K2 Think V2', 'Reasoning model (MBZUAI)')],
        context_window=32000, max_output_tokens=6000,
        key_required=False, official=False, scraper_module='k2think_proxy',
    ),
    ProviderPreset(
        slug='poolside', label='Poolside (chat.poolside.ai)', format=FORMAT_SCRAPER,
        base_url='https://chat.poolside.ai', default_model='laguna-s-2.1',
        models=[ModelSpec('laguna-s-2.1', 'Laguna S 2.1'),
                ModelSpec('laguna-xs-2.1', 'Laguna XS 2.1')],
        context_window=32000, max_output_tokens=6000,
        key_required=False, official=False, scraper_module='poolside_proxy',
    ),
    ProviderPreset(
        slug='motiftech', label='Motif (chat.motiftech.io)', format=FORMAT_SCRAPER,
        base_url='https://chat.motiftech.io', default_model='motif-102b',
        models=[ModelSpec('motif-102b', 'Motif 3', 'Flagship (Korean-optimized)'),
                ModelSpec('motif-12-7b', 'Motif 12.7B'),
                ModelSpec('motif-12-7b-reasoning', 'Motif 12.7B Reasoning'),
                ModelSpec('motif-tiny', 'Motif Tiny')],
        context_window=32000, max_output_tokens=6000,
        key_required=False, official=False, scraper_module='motiftech_proxy',
    ),
    ProviderPreset(
        slug='metaai', label='Meta AI (meta.ai)', format=FORMAT_SCRAPER,
        base_url='https://www.meta.ai', default_model='metaai-instant',
        models=[
            ModelSpec('metaai-instant', 'Meta AI (Instant)', 'Fast chat mode'),
            ModelSpec('metaai-thinking', 'Meta AI (Thinking)', 'Deep reasoning mode'),
            ModelSpec('metaai-imagine', 'Meta AI Imagine', 'Text-to-image generator'),
        ],
        context_window=128000, max_output_tokens=4000,
        key_required=False, official=False, scraper_module='metaai_proxy',
    ),
    ProviderPreset(
        slug='tryingopen', label='TryingOpen (tryingopen.com — 16 open models, free)', format=FORMAT_SCRAPER,
        base_url='https://www.tryingopen.com/api/open', default_model='qwen/qwen3.8-27b',
        models=[
            ModelSpec('qwen/qwen3.8-27b', 'Qwen3.8 27B', 'Default · vision + tools · 262k'),
            ModelSpec('qwen/qwen3.6-27b', 'Qwen3.6 27B', 'Vision + tools · 262k'),
            ModelSpec('qwen/qwen3.8-2.4t-a95b', 'Qwen3.8 2.4T', 'Largest Qwen · 95B active · 1M'),
            ModelSpec('nvidia/nemotron-3.5-lightning', 'Nemotron 3.5 Lightning', 'NVIDIA · 3B active · 1M · ultra-cheap'),
            ModelSpec('z-ai/glm-5.3', 'GLM 5.3', 'Z.ai · reasoning · 1M'),
            ModelSpec('z-ai/glm-5.2', 'GLM 5.2', 'Z.ai · multi-step · 1M'),
            ModelSpec('moonshotai/kimi-k3', 'Kimi K3', 'Moonshot · 2.8T · vision · 1M'),
            ModelSpec('minimax/minimax-m3', 'MiniMax M3', 'MiniMax · multimodal · 427B · 1M'),
            ModelSpec('deepseek/deepseek-v4-flash-0731', 'DeepSeek V4 Flash', 'DeepSeek · 284B (13B active) · 1M'),
            ModelSpec('deepseek/deepseek-v4-pro-0813', 'DeepSeek V4 Pro', 'DeepSeek · 1.7T full V4 · 1M'),
            ModelSpec('google/gemma-4-31b-it', 'Gemma 4 31B', 'Google · vision · 262k'),
            ModelSpec('google/gemma-4-26b-a4b-it', 'Gemma 4 26B', 'Google · MoE 3.8B active · vision · 262k'),
            ModelSpec('mistralai/mistral-small-2603', 'Mistral Small 4', 'Mistral · 119B · vision · 262k · cheap'),
            ModelSpec('meta/muse-glimmer-30b', 'Muse Glimmer 30B', 'Meta · 30B · vision · 131k'),
            ModelSpec('thinkingmachines/inkling-small', 'Inkling Small', 'Thinking Machines · 276B (12B active) · 524k'),
            ModelSpec('thinkingmachines/inkling', 'Inkling', 'Thinking Machines · 975B (41B active) · 1M'),
        ],
        context_window=1000000, max_output_tokens=8000,
        key_required=False, official=False, scraper_module='tryingopen_proxy',
    ),
    ProviderPreset(
        slug='longcat', label='LongCat (longcat.chat — free, no login)', format=FORMAT_SCRAPER,
        base_url='https://longcat.chat/api/v1/chat-completion-oversea-V2', default_model='longcat/LongCat-2.0',
        models=[
            ModelSpec('longcat/LongCat-2.0', 'LongCat 2.0 Flash', 'Meituan · reasoning + web search · 128k'),
        ],
        context_window=128000, max_output_tokens=8000,
        key_required=False, official=False, scraper_module='longcat_proxy',
    ),
    ProviderPreset(
        slug='geminiweb', label='Gemini Web (gemini.google.com — anonymous Flash-Lite)', format=FORMAT_SCRAPER,
        base_url='https://gemini.google.com/app', default_model='geminiweb/gemini-flash-lite',
        models=[
            ModelSpec('geminiweb/gemini-flash-lite', 'Gemini Flash Lite (Web)', 'Google · anonymous web tier · no login'),
        ],
        context_window=32000, max_output_tokens=4000,
        key_required=False, official=False, scraper_module='geminiweb_proxy',
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


def admin_catalog() -> dict:
    """Provider/model catalog for admin UIs (bot editor + admin AI chat).

    Single source of truth: every picker renders from this so a new proxy
    only needs a preset here to show up everywhere.
    """
    def _entry(p: ProviderPreset) -> dict:
        return {
            'slug': p.slug,
            'label': p.label,
            'official': p.official,
            'base_url': p.base_url,
            'default_model': p.default_model,
            'key_required': p.key_required,
            'models': [
                {'id': m.id, 'label': (f'{m.label} ({m.note})' if m.note else m.label)}
                for m in p.models
            ],
        }

    return {
        'scrapers': [_entry(p) for p in SCRAPER_PRESETS],
        'official': [_entry(p) for p in OFFICIAL_PRESETS],
    }
