"""Unified LLM provider layer for NEBians.

Public surface (keep small; everything else is internal):

- `api.llm.registry`       — provider/model presets (official + community).
- `api.llm.client`         — multi-format chat client (OpenAI/Anthropic/Gemini).
- `api.llm.credentials`    — per-user credential resolution + pickers catalog.
- `api.llm.runtime`        — background-agent session integration.

New services should import from here instead of growing their own provider
switch statements — that is the whole point of this package.
"""
from .client import ChatResult, LLMError, chat, quick_test  # noqa: F401
from .credentials import ResolvedProvider, catalog_for_user, resolve  # noqa: F401
from .registry import (  # noqa: F401
    FORMAT_ANTHROPIC, FORMAT_GEMINI, FORMAT_OPENAI, FORMAT_SCRAPER,
    OFFICIAL_PRESETS, SCRAPER_PRESETS, preset,
)
