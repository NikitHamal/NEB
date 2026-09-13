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

SCRAPER_PROVIDERS = ('qwen', 'qwencloud', 'deepai', 'inception', 'k2think', 'poolside', 'motiftech', 'metaai', 'tryingopen', 'longcat', 'geminiweb', 'yqcloud', 'chatjimmy', 'unikey', 'lazypy', 'googletts', 'moetts', 'kokoro', 'chatterbox', 'fishaudio')


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
    # Keyless official presets: key sent when the caller has none, '' = none.
    default_key: str = ''
    # Extra HTTP headers merged into every call (e.g. a fixed User-Agent).
    extra_headers: dict = field(default_factory=dict)


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
        slug='llm7', label='LLM7 (llm7.io — free, anonymous)',
        format=FORMAT_OPENAI, base_url='https://api.llm7.io/v1',
        default_model='default',
        models=[
            ModelSpec('default', 'Default (auto)', 'Rotating capable model'),
            ModelSpec('fast', 'Fast', 'Low-latency tier'),
            ModelSpec('pro', 'Pro', 'Strongest tier'),
        ],
        context_window=128000, max_output_tokens=4000,
        key_required=False, default_key='unused',
        free_note='Anonymous: 10/min, 60/hr, 500K tokens/day — no key needed',
    ),
    ProviderPreset(
        slug='kilo', label='Kilo Gateway (kilo.ai — free :free models, anonymous)',
        format=FORMAT_OPENAI, base_url='https://api.kilo.ai/api/gateway',
        default_model='stepfun/step-3.7-flash:free',
        models=[
            ModelSpec('stepfun/step-3.7-flash:free', 'Step 3.7 Flash', 'Fast reasoning'),
            ModelSpec('nvidia/nemotron-3-ultra-550b-a55b:free', 'Nemotron 3 Ultra 550B'),
            ModelSpec('openrouter/free', 'OpenRouter Free', 'Best available free model'),
            ModelSpec('kilo-auto/free', 'Kilo Auto Free', 'Auto-routed free pool'),
            ModelSpec('poolside/laguna-s-2.1:free', 'Laguna S 2.1', '128K context'),
            ModelSpec('tencent/hy3:free', 'Tencent Hy3'),
        ],
        context_window=128000, max_output_tokens=4000,
        key_required=False,
        free_note='Anonymous: 200/hr per IP — no key needed',
    ),
    ProviderPreset(
        slug='zen', label='OpenCode Zen (opencode.ai — free -free models, anonymous)',
        format=FORMAT_OPENAI, base_url='https://opencode.ai/zen/v1',
        default_model='laguna-s-2.1-free',
        models=[
            ModelSpec('laguna-s-2.1-free', 'Laguna S 2.1', 'Clean answers · 128K'),
            ModelSpec('mimo-v2.5-free', 'MiMo V2.5'),
            ModelSpec('nemotron-3-ultra-free', 'Nemotron 3 Ultra'),
            ModelSpec('nemotron-3.5-lightning-free', 'Nemotron 3.5 Lightning'),
            ModelSpec('big-pickle', 'Big Pickle'),
            ModelSpec('ling-3.0-flash-fin-free', 'Ling 3.0 Flash'),
            ModelSpec('deepseek-v4-flash-free', 'DeepSeek V4 Flash', 'Saturates often — has fallbacks'),
        ],
        context_window=128000, max_output_tokens=4000,
        key_required=False, default_key='public',
        extra_headers={'User-Agent': 'opencode/1.0'},
        free_note='Anonymous shared pool (Bearer public) — retries advised',
    ),
]

SCRAPER_PRESETS: List[ProviderPreset] = [
    ProviderPreset(
        slug='qwencloud', label='Qwen Cloud (qwencloud.com — 11 models, free)', format=FORMAT_SCRAPER,
        base_url='https://www.qwencloud.com/try-ai', default_model='qwen3.8-max',
        models=[
            ModelSpec('qwen3.8-max', 'Qwen3.8 Max', 'Flagship · reasoning + budget control'),
            ModelSpec('qwen3.7-max', 'Qwen3.7 Max'),
            ModelSpec('qwen3.6-plus', 'Qwen3.6 Plus'),
            ModelSpec('qwen3.6-plus-2026-04-02', 'Qwen3.6 Plus (2026-04-02)'),
            ModelSpec('qwen3.7-plus', 'Qwen3.7 Plus'),
            ModelSpec('qwen3.5-plus', 'Qwen3.5 Plus'),
            ModelSpec('qwen3-max', 'Qwen3 Max'),
            ModelSpec('qwen-plus', 'Qwen Plus'),
            ModelSpec('qwen-flash', 'Qwen Flash', 'Fast'),
            ModelSpec('qwen3-coder-plus', 'Qwen3 Coder Plus', 'Coding flagship · tool calling'),
            ModelSpec('qwen3-coder-flash', 'Qwen3 Coder Flash', 'Fast coding'),
        ],
        context_window=262144, max_output_tokens=8000,
        key_required=False, official=False, scraper_module='qwencloud_proxy',
    ),
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
        slug='k2think', label='K2 Horizon (chat.ifm.ai)', format=FORMAT_SCRAPER,
        base_url='https://chat.ifm.ai', default_model='IFM/K2-Horizon-375B-A23B',
        models=[ModelSpec('IFM/K2-Horizon-375B-A23B', 'K2 Horizon 375B', 'Reasoning model (MBZUAI IFM)')],
        context_window=128000, max_output_tokens=8192,
        key_required=False, official=False, scraper_module='k2think_proxy',
    ),
    ProviderPreset(
        slug='poolside', label='Poolside (chat.poolside.ai)', format=FORMAT_SCRAPER,
        base_url='https://chat.poolside.ai', default_model='laguna-s-2.1',
        models=[ModelSpec('laguna-s-2.1', 'Laguna S 2.1', '128K context · agent coding'),
                ModelSpec('laguna-xs-2.1', 'Laguna XS 2.1', '128K context · fast')],
        context_window=128000, max_output_tokens=8192,
        key_required=False, official=False, scraper_module='poolside_proxy',
    ),
    ProviderPreset(
        slug='motiftech', label='Motif (chat.motiftech.io)', format=FORMAT_SCRAPER,
        base_url='https://chat.motiftech.io', default_model='motif-102b',
        models=[ModelSpec('motif-102b', 'Motif 3', 'Flagship (Korean-optimized) · 128K'),
                ModelSpec('motif-12-7b', 'Motif 12.7B', '128K context'),
                ModelSpec('motif-12-7b-reasoning', 'Motif 12.7B Reasoning', 'Deep thinking · 128K'),
                ModelSpec('motif-tiny', 'Motif Tiny', 'Fast')],
        context_window=128000, max_output_tokens=8192,
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
    ProviderPreset(
        slug='yqcloud', label='Yqcloud (chat9.yqcloud.top — free, no login)', format=FORMAT_SCRAPER,
        base_url='https://chat9.yqcloud.top', default_model='yqcloud-default',
        models=[
            ModelSpec('yqcloud-default', 'Yqcloud Chat', 'Free · web search'),
        ],
        context_window=32000, max_output_tokens=4000,
        key_required=False, official=False, scraper_module='yqcloud_proxy',
    ),
    ProviderPreset(
        slug='chatjimmy', label='ChatJimmy (chatjimmy.ai — Llama 3.1 8B, no login)', format=FORMAT_SCRAPER,
        base_url='https://chatjimmy.ai', default_model='llama3.1-8B',
        models=[
            ModelSpec('llama3.1-8B', 'Llama 3.1 8B'),
        ],
        context_window=32000, max_output_tokens=4000,
        key_required=False, official=False, scraper_module='chatjimmy_proxy',
    ),
    ProviderPreset(
        slug='unikey', label='Unikey (getunikey.ai — 12 models, free trial, no login)', format=FORMAT_SCRAPER,
        base_url='https://www.getunikey.ai', default_model='gpt-5.5',
        models=[
            ModelSpec('gpt-5.5', 'GPT 5.5'),
            ModelSpec('google/gemini-3.5-flash', 'Gemini 3.5 Flash'),
            ModelSpec('google/gemini-3.1-pro-preview', 'Gemini 3.1 Pro Preview'),
            ModelSpec('x-ai/grok-4.3', 'Grok 4.3'),
            ModelSpec('deepseek/deepseek-v4-pro', 'DeepSeek V4 Pro'),
            ModelSpec('deepseek/deepseek-v4-flash', 'DeepSeek V4 Flash'),
            ModelSpec('z-ai/glm-5.2', 'GLM 5.2'),
            ModelSpec('minimax/minimax-m3', 'MiniMax M3'),
            ModelSpec('moonshotai/kimi-k2.7-code', 'Kimi K2.7 Code'),
            ModelSpec('moonshotai/kimi-k3', 'Kimi K3'),
            ModelSpec('claude-opus-4-7', 'Claude Opus 4.7'),
            ModelSpec('claude-opus-4-8', 'Claude Opus 4.8'),
        ],
        context_window=32000, max_output_tokens=4000,
        key_required=False, official=False, scraper_module='unikey_proxy',
    ),
    ProviderPreset(
        slug='lazypy', label='LazyPy TTS (lazypy.ro — 11 services, Microsoft/Google)', format=FORMAT_SCRAPER,
        base_url='https://lazypy.ro/tts', default_model='lazypy/bing-translator',
        models=[
            ModelSpec('lazypy/bing-translator', 'LazyPy Bing (Microsoft)', '313 voices · 3000 chars · best quality'),
            ModelSpec('lazypy/google-translate', 'LazyPy Google', '64 voices · 200 chars'),
            ModelSpec('lazypy/ispeech', 'LazyPy iSpeech', '41 voices · 600 chars'),
        ],
        context_window=3000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='lazypy_proxy',
    ),
    ProviderPreset(
        slug='googletts', label='Google Translate TTS (direct, no proxy)', format=FORMAT_SCRAPER,
        base_url='https://translate.google.com', default_model='google/translate-en',
        models=[
            ModelSpec('google/translate-en', 'Google EN', '200 chars/chunk · unlimited via chunking'),
            ModelSpec('google/translate-multi', 'Google Multi (64 langs)', 'auto-chunked'),
        ],
        context_window=2000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='google_tts_proxy',
    ),
    ProviderPreset(
        slug='moetts', label='Moe TTS (skytnt/moe-tts — anime)', format=FORMAT_SCRAPER,
        base_url='https://skytnt-moe-tts.hf.space', default_model='moe/moe-tts',
        models=[
            ModelSpec('moe/moe-tts', 'Moe TTS', 'Anime voices · HF Space · free'),
        ],
        context_window=1000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='moe_tts_proxy',
    ),
    ProviderPreset(
        slug='kokoro', label='Kokoro TTS (hexgrad/Kokoro-82M — 82M)', format=FORMAT_SCRAPER,
        base_url='https://hexgrad-kokoro-tts.hf.space', default_model='kokoro/kokoro-82m',
        models=[
            ModelSpec('kokoro/kokoro-82m', 'Kokoro 82M', '82M · 8+ voices · very natural · no signup'),
            ModelSpec('kokoro/kokoro-82m-af-heart', 'Kokoro Heart', 'af_heart · warm female'),
            ModelSpec('kokoro/kokoro-82m-af-bella', 'Kokoro Bella', 'af_bella · bright female'),
        ],
        context_window=2000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='kokoro_proxy',
    ),
    ProviderPreset(
        slug='chatterbox', label='Chatterbox TTS (ResembleAI)', format=FORMAT_SCRAPER,
        base_url='https://resembleai-chatterbox.hf.space', default_model='chatterbox/chatterbox',
        models=[
            ModelSpec('chatterbox/chatterbox', 'Chatterbox', 'Expressive · reference audio · no signup'),
        ],
        context_window=3000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='chatterbox_proxy',
    ),
    ProviderPreset(
        slug='fishaudio', label='Fish Audio (fish.audio — S1)', format=FORMAT_SCRAPER,
        base_url='https://api.fish.audio', default_model='fishaudio/s1',
        models=[
            ModelSpec('fishaudio/s1', 'Fish S1', 'High quality · many voices · no signup demo'),
        ],
        context_window=2000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='fish_proxy',
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
