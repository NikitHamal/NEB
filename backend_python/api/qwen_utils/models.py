"""
Qwen model list — fetches the live model catalog from chat.qwen.ai /api/v2/models/
with 5-min Redis-backed caching. Returns rich capability metadata (vision, document,
video, audio, thinking, search, max_context_length, etc.) so the frontend can choose
the right model for each task.
"""
import json
import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)

QWEN_URL = "https://chat.qwen.ai"
_CACHE_KEY = "qwen:models:v2"
_CACHE_TTL = 300  # 5 minutes


def fetch_models(force_refresh=False):
    """Return a list of Qwen models with full capability metadata.

    Cache strategy:
        Redis cache → cache hit → return cached list
        cache miss  → call Qwen API → store in Redis → return

    Keyword Arguments:
        force_refresh -- bypass cache and re-fetch from upstream (default False)

    Returns:
        list of dicts, each with keys:
            id, name, object, owned_by,
            capabilities (dict of bool flags),
            max_context_length, max_thinking_generation_length,
            max_summary_generation_length, abilities, chat_type,
            modality, description, short_description,
            thinking_format, auto_thinking, auto_search,
            is_active, is_visitor_active

    Returns an empty list on error (logged, not raised).
    """
    if not force_refresh:
        cached = cache.get(_CACHE_KEY)
        if cached is not None:
            return cached

    try:
        from ..qwen_proxy import _get_session

        session, _ = _get_session()
        resp = session.get(
            f"{QWEN_URL}/api/v2/models/",
            timeout=30,
        )
        if resp.status_code != 200:
            logger.error("Qwen models fetch failed: %d %s", resp.status_code, resp.text[:300])
            return _fallback_models()

        data = resp.json()
        if not data.get("success"):
            logger.error("Qwen models fetch unsuccessful: %s", data.get("request_id"))
            return _fallback_models()

        raw_models = data.get("data", {}).get("data", [])
        models = [_extract_model_info(m) for m in raw_models]
        models = [m for m in models if m is not None]

        cache.set(_CACHE_KEY, models, _CACHE_TTL)
        return models

    except Exception as e:
        logger.error("Qwen models fetch exception: %s", e)
        return _fallback_models()


def _extract_model_info(raw):
    """Normalise a single model dict from the Qwen API into our standard shape."""
    info = raw.get("info") or {}
    meta = info.get("meta") or {}
    caps = meta.get("capabilities") or {}
    abilities = meta.get("abilities") or {}

    return {
        "id": raw.get("id"),
        "name": meta.get("name") or raw.get("name") or info.get("name"),
        "description": (meta.get("description") or ""),
        "short_description": (meta.get("short_description") or ""),
        "capabilities": {
            "vision": bool(caps.get("vision", False)),
            "document": bool(caps.get("document", False)),
            "video": bool(caps.get("video", False)),
            "audio": bool(caps.get("audio", False)),
            "thinking": bool(caps.get("thinking", False)),
            "reasoning_levels": ["low", "medium", "high"] if bool(caps.get("thinking", False)) else [],
            "search": bool(caps.get("search", False)),
            "citations": bool(caps.get("citations", False)),
        },
        "abilities": {
            "vision": abilities.get("vision", 0),
            "document": abilities.get("document", 0),
            "video": abilities.get("video", 0),
            "audio": abilities.get("audio", 0),
            "mcp": abilities.get("mcp", 0),
            "thinking": abilities.get("thinking", 0),
            "parse_url": abilities.get("parse_url", 0),
            "citations": abilities.get("citations", 0),
        },
        "max_context_length": meta.get("max_context_length", 131072),
        "max_thinking_generation_length": meta.get("max_thinking_generation_length", 0),
        "max_summary_generation_length": meta.get("max_summary_generation_length", 65536),
        "max_generation_length": meta.get("max_generation_length", 65536),
        "thinking_format": meta.get("thinking_format", "summary"),
        "auto_thinking": bool(meta.get("auto_thinking", False)),
        "auto_search": bool(meta.get("auto_search", False)),
        "chat_type": meta.get("chat_type", []),
        "modality": meta.get("modality", []),
        "mcp": meta.get("mcp", []),
        "is_active": bool(raw.get("is_active", True)) and bool(info.get("is_active", True)),
        "is_visitor_active": bool(raw.get("is_visitor_active", True)),
        "object": raw.get("object", "model"),
        "owned_by": raw.get("owned_by", "qwen"),
    }


def _fallback_models():
    """Hardcoded fallback when the upstream is unreachable."""
    return [
        {
            "id": "qwen3.8-max",
            "name": "Qwen3.8-Max",
            "capabilities": {"vision": True, "document": True, "video": True, "audio": True, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": True, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
        {
            "id": "qwen3.8-max-preview",
            "name": "Qwen3.8-Max-Preview",
            "capabilities": {"vision": True, "document": True, "video": True, "audio": True, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": True, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
        {
            "id": "qwen3.7-plus",
            "name": "Qwen3.7-Plus",
            "capabilities": {"vision": True, "document": True, "video": True, "audio": True, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": True, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
        {
            "id": "qwen3.7-max",
            "name": "Qwen3.7-Max",
            "capabilities": {"vision": False, "document": True, "video": False, "audio": False, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": False, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
        {
            "id": "qwen3.6-plus",
            "name": "Qwen3.6-Plus",
            "capabilities": {"vision": True, "document": True, "video": True, "audio": True, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": True, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
        {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5-Plus",
            "capabilities": {"vision": True, "document": True, "video": True, "audio": True, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": True, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
        {
            "id": "qwen3.5-flash",
            "name": "Qwen3.5-Flash",
            "capabilities": {"vision": True, "document": True, "video": True, "audio": True, "thinking": True, "reasoning_levels": ["low", "medium", "high"], "search": True, "citations": False},
            "max_context_length": 1000000,
            "is_active": True,
        },
    ]


_DEFAULT_MODEL = None


def get_default_model(force_refresh=False):
    """Return the best default Qwen model ID.

    Uses Django cache (default model key) so the first call triggers a
    `fetch_models()` but subsequent calls are instant.  The default-model
    cache is tied to the same 5-min TTL as the full model list.

    Prefers ``qwen3.8-max`` — the current final flagship. With the quota
    fix in the proxy (streams interrupted by upstream "high demand" are no
    longer accepted as valid output) it reliably keeps the background-agent
    JSON protocol intact with thinking on.
    """
    global _DEFAULT_MODEL

    cached_default = cache.get("qwen:default_model")
    if cached_default and not force_refresh:
        return cached_default

    default = "qwen3.8-max"
    try:
        models = fetch_models(force_refresh=force_refresh)
        for m in models:
            if m["id"] == "qwen3.8-max" and m["is_active"]:
                default = m["id"]
                break
    except Exception:
        pass

    cache.set("qwen:default_model", default, _CACHE_TTL)
    _DEFAULT_MODEL = default
    return default
