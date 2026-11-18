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

SCRAPER_PROVIDERS = ('qwen', 'qwencloud', 'deepai', 'inception', 'k2think', 'poolside', 'motiftech', 'metaai', 'tryingopen', 'longcat', 'geminiweb', 'yqcloud', 'chatjimmy', 'unikey', 'ptero', 'lazypy', 'googletts', 'moetts', 'kokoro', 'paradee', 'chatterbox', 'fishaudio', 'airy', 'smallest')


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
        default_model='gpt-6-luna',
        models=[
            ModelSpec('gpt-6-luna', 'GPT-6 Luna', 'Fast multimodal newest tier'),
            ModelSpec('gpt-6-astra', 'GPT-6 Astra', '1M context · flagship reasoning'),
            ModelSpec('gpt-6.1-sol', 'GPT-6.1 Sol', 'Deep reasoning & coding'),
            ModelSpec('gpt-6.1-terra', 'GPT-6.1 Terra', 'Balanced frontier'),
            ModelSpec('gpt-6.2-sol', 'GPT-6.2 Sol', 'Latest Sol reasoning'),
            ModelSpec('gpt-5.6-terra', 'GPT-5.6 Terra', 'Balanced 5.6 flagship'),
            ModelSpec('gpt-5.6-sol', 'GPT-5.6 Sol', 'Strongest 5.6 reasoning'),
            ModelSpec('gpt-5.6-luna', 'GPT-5.6 Luna', 'Budget 5.6'),
            ModelSpec('gpt-5.5', 'GPT-5.5', 'Previous flagship'),
            ModelSpec('gpt-5.4-mini', 'GPT-5.4 Mini', 'Fast + cheap, great for agents'),
            ModelSpec('gpt-5.4-nano', 'GPT-5.4 Nano', 'Cheapest, high volume'),
            ModelSpec('gpt-5.2-pro', 'GPT-5.2 Pro', 'Extreme accuracy (slow)'),
        ],
        context_window=1000000,
        key_env='OPENAI_API_KEY',
    ),
    ProviderPreset(
        slug='anthropic',
        label='Anthropic (Claude)',
        format=FORMAT_ANTHROPIC,
        base_url='https://api.anthropic.com',
        default_model='claude-sonnet-5-5',
        models=[
            ModelSpec('claude-sonnet-5-5', 'Claude Sonnet 5.5', 'Newest speed/intelligence mix'),
            ModelSpec('claude-opus-5-5', 'Claude Opus 5.5', 'Frontier agentic coding & research'),
            ModelSpec('claude-haiku-5-5', 'Claude Haiku 5.5', 'Fastest multimodal 5.5'),
            ModelSpec('claude-opus-5', 'Claude Opus 5', 'Deep reasoning'),
            ModelSpec('claude-sonnet-5', 'Claude Sonnet 5', 'Balanced 5.0'),
            ModelSpec('claude-fable-5-2', 'Claude Fable 5.2', 'Long-horizon autonomous agents'),
            ModelSpec('claude-fable-5', 'Claude Fable 5', 'Long-running agents'),
            ModelSpec('claude-opus-4-8', 'Claude Opus 4.8', 'Complex agentic coding'),
            ModelSpec('claude-haiku-4-5', 'Claude Haiku 4.5', 'Fast legacy tier'),
        ],
        context_window=1000000,
        key_env='ANTHROPIC_API_KEY',
    ),
    ProviderPreset(
        slug='gemini',
        label='Google Gemini',
        format=FORMAT_GEMINI,
        base_url='https://generativelanguage.googleapis.com/v1beta',
        default_model='gemini-3.8-flash',
        models=[
            ModelSpec('gemini-4-argon', 'Gemini 4 Argon', 'Newest frontier reasoning'),
            ModelSpec('gemini-3.8-flash', 'Gemini 3.8 Flash', 'Newest high-speed multimodal'),
            ModelSpec('gemini-3.6-flash', 'Gemini 3.6 Flash', 'Fast multimodal'),
            ModelSpec('gemini-3.5-flash', 'Gemini 3.5 Flash', 'Stable 3.5 flash'),
            ModelSpec('gemini-3.1-pro', 'Gemini 3.1 Pro', 'Pro reasoning & coding'),
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
        default_model='deepseek-v4.1-flash',
        models=[
            ModelSpec('deepseek-v4.1-flash', 'DeepSeek V4.1 Flash', 'Newest 284B MoE · 1M ctx'),
            ModelSpec('deepseek-v4-pro', 'DeepSeek V4 Pro', '1.7T full-scale V4 · 1M ctx'),
            ModelSpec('deepseek-v4-flash', 'DeepSeek V4 Flash', 'Fast coding & agents'),
            ModelSpec('deepseek-chat', 'DeepSeek Chat (V3)', 'Great coder, cheap'),
            ModelSpec('deepseek-reasoner', 'DeepSeek Reasoner (R1)', 'Chain-of-thought'),
        ],
        context_window=1000000,
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
            ModelSpec('DeepSeek-V4-Flash-0731', 'DeepSeek V4 Flash', '400K ctx · reasoning + tools'),
            ModelSpec('glm-5.3-flash', 'GLM 5.3 Flash', 'Z.ai fast reasoning'),
            ModelSpec('mimo-v2.6-flash', 'MiMo V2.6 Flash', 'Xiaomi fast reasoning'),
            ModelSpec('minimax-m3', 'MiniMax M3', 'Pro tier · 427B'),
            ModelSpec('minimax-m2.7', 'MiniMax M2.7', 'Fast tier'),
            ModelSpec('kimi-k2.7-code', 'Kimi K2.7 Code', 'Moonshot coding specialist'),
            ModelSpec('gemma4:31b', 'Gemma 4 31B', 'Google open model'),
            ModelSpec('gpt-oss:120b', 'GPT-OSS 120B', 'OpenAI 120B open weights'),
            ModelSpec('gpt-oss:20b', 'GPT-OSS 20B', 'OpenAI 20B open weights'),
            ModelSpec('codestral-latest', 'Codestral Latest', 'Mistral code model'),
        ],
        context_window=400000, max_output_tokens=4000,
        key_required=False, default_key='unused',
        free_note='Anonymous: 10/min, 60/hr, 500K tokens/day — no key needed',
    ),
    ProviderPreset(
        slug='kilo', label='Kilo Gateway (kilo.ai — free :free models, anonymous)',
        format=FORMAT_OPENAI, base_url='https://api.kilo.ai/api/gateway',
        default_model='kilo-auto/free',
        models=[
            ModelSpec('kilo-auto/free', 'Kilo Auto Free', 'Auto-routed free pool'),
            ModelSpec('openrouter/free', 'OpenRouter Free', 'Best available free model'),
            ModelSpec('nvidia/nemotron-3-ultra-550b-a55b:free', 'Nemotron 3 Ultra 550B', '550B MoE'),
            ModelSpec('nvidia/nemotron-3.5-super-vl:free', 'Nemotron 3.5 Super VL', '120B MoE · vision'),
            ModelSpec('nvidia/nemotron-3.5-lightning:free', 'Nemotron 3.5 Lightning', 'Fast 30B MoE'),
            ModelSpec('nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free', 'Nemotron 3 Nano Omni', 'Reasoning'),
            ModelSpec('baidu/ernie-5.5-flash-preview:free', 'ERNIE 5.5 Flash Preview', 'Baidu flagship'),
            ModelSpec('cohere/north-mini-code:free', 'Cohere North Mini Code', 'Coding specialist'),
            ModelSpec('reflection/beam-free', 'Reflection Beam 1.0', 'Reasoning & coding'),
            ModelSpec('particle-ai/particle-1:free', 'Particle-1', 'Particle AI'),
            ModelSpec('dots-studio/dots-3-note-preview:free', 'Dots 3 Note Preview', 'Dots Studio'),
            ModelSpec('liquid/lfm-3-1.7b:free', 'Liquid LFM3 1.7B', 'Compact fast model'),
            ModelSpec('stealth/glyph-cluster', 'Glyph Cluster', 'Stealth free model'),
        ],
        context_window=262144, max_output_tokens=4000,
        key_required=False,
        free_note='Anonymous: 200/hr per IP — no key needed',
    ),
    ProviderPreset(
        slug='zen', label='OpenCode Zen (opencode.ai — free -free models, anonymous)',
        format=FORMAT_OPENAI, base_url='https://opencode.ai/zen/v1',
        default_model='deepseek-v4.1-flash-free',
        models=[
            ModelSpec('deepseek-v4.1-flash-free', 'DeepSeek V4.1 Flash', 'Fast coding & reasoning'),
            ModelSpec('glm-5.3-flash-free', 'GLM 5.3 Flash', 'Z.ai 320B MoE'),
            ModelSpec('mimo-v2.6-flash-free', 'MiMo V2.6 Flash', 'Xiaomi fast reasoning'),
            ModelSpec('longcat-2.5-free', 'LongCat 2.5', 'Meituan 1.6T MoE'),
            ModelSpec('inkling-2-small-free', 'Inkling 2 Small', 'Thinking Machines'),
            ModelSpec('beam-free', 'Reflection Beam', 'Reasoning & tool use'),
            ModelSpec('nemotron-3.5-super-vl-free', 'Nemotron 3.5 Super VL', 'NVIDIA 120B VL'),
            ModelSpec('nemotron-3.5-lightning-free', 'Nemotron 3.5 Lightning', 'NVIDIA fast MoE'),
            ModelSpec('hy4-flash-free', 'Tencent Hy4 Flash', 'Hunyuan 4 Flash'),
            ModelSpec('flint-40b-free', 'Flint 40B', '40B reasoning'),
            ModelSpec('iceman-free', 'Iceman', 'Fast general model'),
            ModelSpec('big-pickle', 'Big Pickle', '200K context · reasoning'),
        ],
        context_window=200000, max_output_tokens=4000,
        key_required=False, default_key='public',
        extra_headers={'User-Agent': 'opencode/1.0'},
        free_note='Anonymous shared pool (Bearer public) — automatic keyless fallback',
    ),
]

SCRAPER_PRESETS: List[ProviderPreset] = [
    ProviderPreset(
        slug='qwencloud', label='Qwen Cloud (qwencloud.com — Qwen 4 & 3.8, free)', format=FORMAT_SCRAPER,
        base_url='https://www.qwencloud.com/try-ai', default_model='qwen4-max',
        models=[
            ModelSpec('qwen4-max', 'Qwen4 Max', 'Newest 2.4T flagship · 1M context · vision + reasoning'),
            ModelSpec('qwen4-max-preview', 'Qwen4 Max (Preview)', '1M context · reasoning'),
            ModelSpec('qwen4-plus', 'Qwen4 Plus', 'Balanced Qwen4 tier'),
            ModelSpec('qwen4-flash', 'Qwen4 Flash', 'Fast Qwen4 tier'),
            ModelSpec('qwen4-27b', 'Qwen4 27B', 'Open-weight 27B · 262K context'),
            ModelSpec('qwen3.8-max', 'Qwen3.8 Max', 'Flagship · reasoning + budget control'),
            ModelSpec('qwen3.8-flash', 'Qwen3.8 Flash', 'Fast multimodal · Qwen4 architecture'),
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
        context_window=1000000, max_output_tokens=8000,
        key_required=False, official=False, scraper_module='qwencloud_proxy',
    ),
    ProviderPreset(
        slug='qwen', label='Qwen (chat.qwen.ai — Qwen 4 & 3.8)', format=FORMAT_SCRAPER,
        base_url='https://chat.qwen.ai/api/v2', default_model='qwen4-max',
        models=[
            ModelSpec('qwen4-max', 'Qwen 4 Max', 'Newest 2.4T flagship · 1M context'),
            ModelSpec('qwen4-max-preview', 'Qwen 4 Max (Preview)', '1M context · vision + thinking'),
            ModelSpec('qwen4-plus', 'Qwen 4 Plus', 'Balanced next-gen Qwen 4'),
            ModelSpec('qwen4-flash', 'Qwen 4 Flash', 'Fast next-gen Qwen 4'),
            ModelSpec('qwen4-27b', 'Qwen 4 27B', '27B dense · 262K context'),
            ModelSpec('qwen3.8-max', 'Qwen 3.8 Max', 'GA flagship · 1M context'),
            ModelSpec('qwen3.8-max-preview', 'Qwen 3.8 Max (Preview)'),
            ModelSpec('qwen3.8-flash', 'Qwen 3.8 Flash', 'Fast multimodal'),
            ModelSpec('qwen3.7-plus', 'Qwen 3.7 Plus', 'Stable'),
            ModelSpec('qwen3.7-max', 'Qwen 3.7 Max'),
            ModelSpec('qwen3.6-plus', 'Qwen 3.6 Plus'),
            ModelSpec('qwen3.5-plus', 'Qwen 3.5 Plus'),
        ],
        context_window=1000000,
        key_required=False, official=False, scraper_module='qwen_proxy',
    ),
    ProviderPreset(
        slug='deepai', label='DeepAI (deepai.org — 10 free models)', format=FORMAT_SCRAPER,
        base_url='https://api.deepai.org', default_model='standard',
        models=[
            ModelSpec('standard', 'DeepAI Standard', 'Fast & reliable · vision'),
            ModelSpec('gpt-6-luna', 'GPT-6 Luna', 'OpenAI fast multimodal · free'),
            ModelSpec('claude-haiku-5-5', 'Claude Haiku 5.5', 'Anthropic fast multimodal · free'),
            ModelSpec('qwen3.8-flash', 'Qwen 3.8 Flash', 'Alibaba multimodal · free'),
            ModelSpec('deepseek-v4.1-flash', 'DeepSeek V4.1 Flash', 'Coding & agents · free'),
            ModelSpec('glm-5.3-flash', 'GLM 5.3 Flash', 'Z.ai 320B MoE · vision + thinking · free'),
            ModelSpec('tencent-hy3', 'Tencent Hy3', 'Hunyuan 3 · free'),
            ModelSpec('gemma-4', 'Gemma 4', 'Google compact multimodal · free'),
            ModelSpec('llama-3.3-70b-instruct', 'Llama 3.3 70B Instruct', 'Meta 70B · free'),
            ModelSpec('llama-3.1-8b-instant', 'Llama 3.1 8B Instant', 'Ultra-fast · free'),
        ],
        key_required=False, official=False, scraper_module='deepai_proxy',
    ),
    ProviderPreset(
        slug='inception', label='Inception Labs (Mercury 3)', format=FORMAT_SCRAPER,
        base_url='https://api.inceptionlabs.ai/v1', default_model='mercury-3',
        models=[ModelSpec('mercury-3', 'Mercury 3')],
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
        slug='tryingopen', label='TryingOpen (tryingopen.com — 30+ open models, free)', format=FORMAT_SCRAPER,
        base_url='https://www.tryingopen.com/api/open', default_model='qwen/qwen3.8-27b',
        models=[
            ModelSpec('qwen/qwen4-max', 'Qwen4 Max', 'Alibaba · 2.4T · vision + reasoning · 1M'),
            ModelSpec('qwen/qwen4-27b', 'Qwen4 27B', 'Alibaba · 27B · vision + tools · 262k'),
            ModelSpec('qwen/qwen3.8-27b', 'Qwen3.8 27B', 'Default · vision + tools · 262k'),
            ModelSpec('qwen/qwen3.8-flash', 'Qwen3.8 Flash', 'Alibaba · fast multimodal · 1M'),
            ModelSpec('qwen/qwen3.8-2.4t-a95b', 'Qwen3.8 2.4T', 'Largest Qwen 3.8 · 95B active · 1M'),
            ModelSpec('qwen/qwen3.6-27b', 'Qwen3.6 27B', 'Vision + tools · 262k'),
            ModelSpec('deepseek/deepseek-v4.1-flash', 'DeepSeek V4.1 Flash', 'DeepSeek · 284B · coding & agents · 1M'),
            ModelSpec('deepseek/deepseek-v4.1-flash-1017', 'DeepSeek V4.1 Flash 1017', 'DeepSeek · Oct 17 · 1M'),
            ModelSpec('deepseek/deepseek-v4-flash-0731', 'DeepSeek V4 Flash', 'DeepSeek · 284B (13B active) · 1M'),
            ModelSpec('deepseek/deepseek-v4-pro-0813', 'DeepSeek V4 Pro', 'DeepSeek · 1.7T full V4 · 1M'),
            ModelSpec('z-ai/glm-5.3', 'GLM 5.3', 'Z.ai · reasoning · 1M'),
            ModelSpec('z-ai/glm-5.3-flash', 'GLM 5.3 Flash', 'Z.ai · 320B MoE · vision · 1M'),
            ModelSpec('z-ai/glm-5.2', 'GLM 5.2', 'Z.ai · multi-step · 1M'),
            ModelSpec('nvidia/nemotron-3.5-super-vl', 'Nemotron 3.5 Super VL', 'NVIDIA · 120B MoE · vision · 1M'),
            ModelSpec('nvidia/nemotron-3-ultra-550b-a55b', 'Nemotron 3 Ultra 550B', 'NVIDIA · 550B MoE · 1M'),
            ModelSpec('nvidia/nemotron-3.5-lightning', 'Nemotron 3.5 Lightning', 'NVIDIA · 3B active · 1M · ultra-cheap'),
            ModelSpec('xiaomi/mimo-v2.6-pro', 'MiMo V2.6 Pro', 'Xiaomi · flagship reasoning · 262k'),
            ModelSpec('xiaomi/mimo-v2.6-flash', 'MiMo V2.6 Flash', 'Xiaomi · fast reasoning · 262k'),
            ModelSpec('reflection/beam-1.0-501b-a23b', 'Beam 1.0', 'Reflection · 501B MoE · 262k'),
            ModelSpec('mistralai/mistral-large-4-0', 'Mistral Large 4', 'Mistral · frontier open · 262k'),
            ModelSpec('mistralai/mistral-small-2603', 'Mistral Small 4', 'Mistral · 119B · vision · 262k'),
            ModelSpec('tencent/hy4-preview', 'Tencent Hy4 Preview', 'Tencent · Hunyuan 4 · 262k'),
            ModelSpec('meta/muse-spark-open', 'Muse Spark Open', 'Meta · Superintelligence Labs · 262k'),
            ModelSpec('meta/muse-glimmer-30b', 'Muse Glimmer 30B', 'Meta · 30B · vision · 131k'),
            ModelSpec('moonshotai/kimi-k3', 'Kimi K3', 'Moonshot · 2.8T · vision · 1M'),
            ModelSpec('minimax/minimax-m3', 'MiniMax M3', 'MiniMax · multimodal · 427B · 1M'),
            ModelSpec('thinkingmachines/inkling', 'Inkling', 'Thinking Machines · 975B (41B active) · 1M'),
            ModelSpec('thinkingmachines/inkling-small', 'Inkling Small', 'Thinking Machines · 276B (12B active) · 524k'),
            ModelSpec('openai/gpt-oss-120b', 'GPT-OSS 120B', 'OpenAI · 120B open weights · 128k'),
            ModelSpec('google/gemma-4-31b-it', 'Gemma 4 31B', 'Google · vision · 262k'),
            ModelSpec('google/gemma-4-26b-a4b-it', 'Gemma 4 26B', 'Google · MoE 3.8B active · vision · 262k'),
            ModelSpec('google/gemma-4-e2b-it', 'Gemma 4 E2B', 'Google · 2B compact · vision · 128k'),
            ModelSpec('inclusionai/ling-3.0-flash-vl', 'Ling 3.0 Flash VL', 'InclusionAI · vision · 128k'),
            ModelSpec('liquid/lfm-2.5-24b-a2b', 'Liquid LFM2.5 24B', 'Liquid AI · 24B MoE · 128k'),
        ],
        context_window=1000000, max_output_tokens=8000,
        key_required=False, official=False, scraper_module='tryingopen_proxy',
    ),
    ProviderPreset(
        slug='longcat', label='LongCat (longcat.chat — free, no login)', format=FORMAT_SCRAPER,
        base_url='https://longcat.chat/api/v1/chat-completion-oversea-V2', default_model='longcat/LongCat-2.5',
        models=[
            ModelSpec('longcat/LongCat-2.5', 'LongCat 2.5',
                      'Meituan · 1.6T MoE (48B active) · thinking + web search · 128k'),
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
        slug='ptero', label='Ptero (ptero.pro — 5 models, free, no login)', format=FORMAT_SCRAPER,
        base_url='https://ptero.pro', default_model='deepseek-v4-flash:runware',
        models=[
            ModelSpec('deepseek-v4-flash:runware', 'DeepSeek V4 Flash', 'Default · vision + coding'),
            ModelSpec('minimax-m3.1-flash:runware', 'MiniMax M3.1 Flash', 'Fast multimodal'),
            ModelSpec('qwen3.7-flash:minirouter', 'Qwen 3.7 Flash', 'Fast Qwen'),
            ModelSpec('glm-5.3-flash', 'GLM 5.3 Flash', 'Z.ai 320B MoE'),
            ModelSpec('kimi-k3:apinex', 'Kimi K3', 'Moonshot 2.8T flagship'),
        ],
        context_window=32000, max_output_tokens=4000,
        key_required=False, official=False, scraper_module='ptero_proxy',
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
        slug='paradee', label='Paradee TTS (Kokoro-82M distilled to 8M)', format=FORMAT_SCRAPER,
        base_url='https://sahilmahendrakar-paradee.hf.space', default_model='paradee/paradee-8m',
        models=[
            ModelSpec('paradee/paradee-8m', 'Paradee 8M', '8M · 9MB · af_heart · ~8x realtime CPU · no signup'),
        ],
        context_window=4800, max_output_tokens=0,
        key_required=False, official=False, scraper_module='paradee_proxy',
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
        slug='fishaudio', label='Fish Audio (fish.audio — Drama 3)', format=FORMAT_SCRAPER,
        base_url='https://api.fish.audio', default_model='fishaudio/drama-3',
        models=[
            ModelSpec('fishaudio/drama-3', 'Fish Audio Drama 3', 'Expressive — emotion tags, voice design · keyless via HF Space'),
            ModelSpec('fishaudio/s2.1-pro-free', 'Fish Audio S2.1 Pro (free)', 'Official free API — needs FISH_API_KEY on the server'),
        ],
        context_window=3000, max_output_tokens=0,
        key_required=False, official=False, scraper_module='fish_proxy',
    ),
    ProviderPreset(
        slug='airy', label='Airy TTS (airy.so — airy-tts-v1)', format=FORMAT_SCRAPER,
        base_url='https://api.airy.so', default_model='airy/airy-tts-v1',
        models=[
            ModelSpec('airy/airy-tts-v1', 'Airy TTS v1', '104 voices · en+ko · 640 chars/batch, auto-chunked'),
        ],
        context_window=4800, max_output_tokens=0,
        key_required=False, official=False, scraper_module='airy_proxy',
    ),
    ProviderPreset(
        slug='smallest', label='Smallest AI (smallest.ai — Lightning v3.1 Pro)', format=FORMAT_SCRAPER,
        base_url='https://api.smallest.ai', default_model='smallest/lightning-v3.1-pro',
        models=[
            ModelSpec('smallest/lightning-v3.1-pro', 'Lightning v3.1 Pro', '269 voices · 31 languages · needs SMALLEST_API_KEY'),
            ModelSpec('smallest/lightning-v3.1-pro-10-26', 'Lightning v3.1 Pro (Oct 26 preview)', 'Newest checkpoint · en/es/hi · preview ID retires 2026-12-28'),
            ModelSpec('smallest/lightning-v3.1', 'Lightning v3.1', '234 voices · 20 languages · retires 2026-11-30'),
        ],
        context_window=2400, max_output_tokens=0,
        key_env='SMALLEST_API_KEY',
        key_required=False, official=False, scraper_module='smallest_proxy',
    ),
]

ALL_PRESETS = {p.slug: p for p in OFFICIAL_PRESETS + SCRAPER_PRESETS}


def preset(slug: str) -> Optional[ProviderPreset]:
    return ALL_PRESETS.get((slug or '').strip().lower())


def is_official_slug(slug: str) -> bool:
    p = preset(slug)
    return bool(p and p.official)


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
        'scrapers': [_entry(p) for p in SCRAPER_PRESETS if p.max_output_tokens > 0],
        'official': [_entry(p) for p in OFFICIAL_PRESETS],
    }
