import logging
import os
import sys
from typing import Dict, Generator, List, Optional

# Ensure backend_python is available for proxies
BACKEND_DIR = r"F:\NEB\backend_python"
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nebians.settings")
    import django
    django.setup()
except Exception:
    pass

logger = logging.getLogger(__name__)

CATALOG = [
    {
        "provider": "metaai",
        "label": "Meta AI (meta.ai)",
        "type": "reverse",
        "models": [
            {"id": "metaai-instant", "name": "Meta AI (Instant)", "desc": "Fast chat mode"},
            {"id": "metaai-thinking", "name": "Meta AI (Thinking)", "desc": "Deep reasoning mode"},
        ],
        "default_model": "metaai-instant",
    },
    {
        "provider": "qwen",
        "label": "Qwen (chat.qwen.ai)",
        "type": "reverse",
        "models": [
            {"id": "qwen3.8-max", "name": "Qwen 3.8 Max", "desc": "Latest flagship coder"},
            {"id": "qwen3.7-plus", "name": "Qwen 3.7 Plus", "desc": "Balanced flagship"},
            {"id": "qwen3.5-plus", "name": "Qwen 3.5 Plus", "desc": "Fast reasoning"},
        ],
        "default_model": "qwen3.8-max",
    },
    {
        "provider": "poolside",
        "label": "Poolside (chat.poolside.ai)",
        "type": "reverse",
        "models": [
            {"id": "laguna-s-2.1", "name": "Laguna S 2.1", "desc": "Code intelligence"},
            {"id": "laguna-xs-2.1", "name": "Laguna XS 2.1", "desc": "Fast coding model"},
        ],
        "default_model": "laguna-s-2.1",
    },
    {
        "provider": "k2think",
        "label": "K2 Think (k2think.ai)",
        "type": "reverse",
        "models": [
            {"id": "MBZUAI-IFM/K2-Think-v2", "name": "K2 Think V2", "desc": "Reasoning model"},
        ],
        "default_model": "MBZUAI-IFM/K2-Think-v2",
    },
    {
        "provider": "motiftech",
        "label": "Motif (chat.motiftech.io)",
        "type": "reverse",
        "models": [
            {"id": "motif-102b", "name": "Motif 3 (102B)", "desc": "Large Korean/multilingual"},
            {"id": "motif-12-7b-reasoning", "name": "Motif 12.7B Reasoning", "desc": "Reasoning coder"},
        ],
        "default_model": "motif-102b",
    },
    {
        "provider": "deepai",
        "label": "DeepAI (deepai.org)",
        "type": "reverse",
        "models": [
            {"id": "gpt-4.1-nano", "name": "DeepAI GPT-4.1 Nano", "desc": "Fast free tier model"},
            {"id": "deepseek-v3.2", "name": "DeepSeek V3.2", "desc": "Coding & reasoning"},
            {"id": "gemini-2.5-flash-lite", "name": "Gemini 2.5 Flash Lite", "desc": "Fast reasoning"},
        ],
        "default_model": "gpt-4.1-nano",
    },
    {
        "provider": "deepseek",
        "label": "DeepSeek (api.deepseek.com)",
        "type": "api",
        "models": [
            {"id": "deepseek-v4-flash", "name": "DeepSeek V4 Flash", "desc": "High speed flagship model"},
            {"id": "deepseek-v4-pro", "name": "DeepSeek V4 Pro", "desc": "Advanced coding & reasoning"},
            {"id": "deepseek-v4", "name": "DeepSeek V4", "desc": "Balanced general intelligence"},
        ],
        "default_model": "deepseek-v4-flash",
    },
    {
        "provider": "openai",
        "label": "OpenAI / Custom BYOK",
        "type": "api",
        "models": [
            {"id": "gpt-5.4-mini", "name": "GPT-5.4 Mini", "desc": "Fast agentic model"},
            {"id": "gpt-5.5", "name": "GPT-5.5", "desc": "Flagship model"},
        ],
        "default_model": "gpt-5.4-mini",
    },
    {
        "provider": "empero",
        "label": "Empero (free.empero.org — Qwen3.8 27B free)",
        "type": "api",
        "models": [
            {"id": "Qwen/Qwen3.8-27B-FP8", "name": "Qwen 3.8 27B (FP8)", "desc": "Free hosted · reasoning · 131k"},
            {"id": "qwen3.8-27b", "name": "Qwen 3.8 27B", "desc": "Alias for Qwen3.8-27B-FP8"},
        ],
        "default_model": "Qwen/Qwen3.8-27B-FP8",
    },
    {
        "provider": "anthropic",
        "label": "Anthropic (Claude)",
        "type": "api",
        "models": [
            {"id": "claude-sonnet-5", "name": "Claude Sonnet 5", "desc": "Leading agentic coder"},
        ],
        "default_model": "claude-sonnet-5",
    },
]


def list_providers() -> List[Dict]:
    return CATALOG


def get_default_provider() -> Dict:
    return CATALOG[0]


def stream_chat(
    messages: List[Dict[str, str]],
    provider: str = "metaai",
    model: str = "metaai-instant",
) -> Generator[Dict, None, None]:
    provider = (provider or "").strip().lower()
    
    if provider == "metaai":
        from api import metaai_proxy
        yield from metaai_proxy.stream_chat(messages, model=model or "metaai-instant")
        return
        
    elif provider == "qwen":
        from api import qwen_proxy
        user_msg = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
        sys_msg = next((m.get("content", "") for m in messages if m.get("role") == "system"), "")
        try:
            res = qwen_proxy.call_qwen(system_prompt=sys_msg, user_message=user_msg, model=model or "qwen3.8-max")
            if res:
                yield {"type": "text", "content": res}
            yield {"type": "done"}
        except Exception as exc:
            yield {"type": "error", "error": str(exc)}
        return

    elif provider == "poolside":
        from api import poolside_proxy
        yield from poolside_proxy.stream_chat(messages, model=model or "laguna-s-2.1")
        return

    elif provider == "k2think":
        from api import k2think_proxy
        yield from k2think_proxy.stream_chat(messages, model=model or "MBZUAI-IFM/K2-Think-v2")
        return

    elif provider == "motiftech":
        from api import motiftech_proxy
        yield from motiftech_proxy.stream_chat(messages, model=model or "motif-102b")
        return

    elif provider == "deepai":
        from api import deepai_proxy
        user_msg = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
        sys_msg = next((m.get("content", "") for m in messages if m.get("role") == "system"), "")
        try:
            res = deepai_proxy.chat(user_message=user_msg, system_prompt=sys_msg, model=model or "gpt-4.1-nano")
            if res:
                yield {"type": "text", "content": res}
            yield {"type": "done"}
        except Exception as exc:
            yield {"type": "error", "error": str(exc)}
        return

    elif provider == "deepseek":
        from .deepseek_provider import stream_chat as deepseek_stream
        yield from deepseek_stream(messages, model=model or "deepseek-v4-flash")
        return

    elif provider == "empero":
        from api.llm import client as llm_client
        target_model = model or "Qwen/Qwen3.8-27B-FP8"
        try:
            for chunk in llm_client.chat_stream(
                format="openai",
                base_url="https://free.empero.org/v1",
                api_key="free",
                model=target_model,
                messages=messages,
                provider="empero",
                max_tokens=8192,
            ):
                if chunk.get("type") == "reasoning":
                    yield {"type": "reasoning", "content": chunk.get("content", "")}
                elif chunk.get("type") == "text":
                    yield {"type": "text", "content": chunk.get("content", "")}
                elif chunk.get("type") == "done":
                    yield {"type": "done"}
        except Exception as exc:
            yield {"type": "error", "error": f"Empero stream error: {exc}"}
        return

    # Fallback to Meta AI
    from api import metaai_proxy
    yield from metaai_proxy.stream_chat(messages, model=model or "metaai-instant")
