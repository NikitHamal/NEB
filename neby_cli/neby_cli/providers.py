import json
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
        "provider": "longcat",
        "label": "LongCat (longcat.chat — free, no login)",
        "type": "reverse",
        "models": [
            {"id": "longcat/LongCat-2.0", "name": "LongCat 2.0 Flash", "desc": "Meituan · reasoning + search · 128k"},
        ],
        "default_model": "longcat/LongCat-2.0",
    },
    {
        "provider": "geminiweb",
        "label": "Gemini Web (gemini.google.com — anonymous)",
        "type": "reverse",
        "models": [
            {"id": "geminiweb/gemini-flash-lite", "name": "Gemini Flash Lite (Web)", "desc": "Google · anonymous web tier · no login"},
        ],
        "default_model": "geminiweb/gemini-flash-lite",
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
        "provider": "tembo",
        "label": "Tembo AI (docs.tembo.io)",
        "type": "reverse",
        "models": [
            {"id": "tembo-assistant", "name": "Tembo Docs Assistant", "desc": "Postgres & Tembo AI specialized assistant"},
        ],
        "default_model": "tembo-assistant",
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


def _extract_images_from_messages(messages: List[Dict]) -> List[Dict]:
    images = []
    for m in messages:
        content = m.get("content")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "") if isinstance(part.get("image_url"), dict) else part.get("image_url", "")
                    if url.startswith("data:"):
                        try:
                            header, b64 = url.split(",", 1)
                            mime = header.split(";")[0].split(":")[1] if ":" in header else "image/png"
                            import base64, tempfile, os
                            raw = base64.b64decode(b64)
                            fd, path = tempfile.mkstemp(suffix=".png", prefix="neby_img_")
                            os.write(fd, raw)
                            os.close(fd)
                            images.append({"path": path, "mime_type": mime, "base64": b64, "filename": os.path.basename(path)})
                        except Exception:
                            pass
                    elif url:
                        images.append({"path": url, "mime_type": "image/png", "filename": os.path.basename(url)})
    return images


def _get_text_from_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                texts.append(part.get("text", ""))
            elif isinstance(part, dict) and part.get("type") == "image_url":
                texts.append("[image]")
        return "\n".join(texts)
    return str(content or "")


def stream_chat(
    messages: List[Dict[str, str]],
    provider: str = "metaai",
    model: str = "metaai-instant",
    images: Optional[List[Dict]] = None,
    effort: Optional[str] = None,
) -> Generator[Dict, None, None]:
    provider = (provider or "").strip().lower()
    if images is None:
        images = _extract_images_from_messages(messages)
    file_paths = [img.get("path") for img in images if img.get("path")] if images else []

    if provider == "metaai":
        from api import metaai_proxy
        yield from metaai_proxy.stream_chat(messages, model=model or "metaai-instant", images=images)
        return

    elif provider == "qwen":
        from api import qwen_proxy
        user_msg = _get_text_from_content(next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), ""))
        sys_msg = _get_text_from_content(next((m.get("content", "") for m in messages if m.get("role") == "system"), ""))
        try:
            res = qwen_proxy.call_qwen(system_prompt=sys_msg, user_message=user_msg, model=model or "qwen3.8-max", file_paths=file_paths or None)
            if res:
                yield {"type": "text", "content": res}
            yield {"type": "done"}
        except Exception as exc:
            yield {"type": "error", "error": str(exc)}
        return

    elif provider == "tembo":
        from .tembo_provider import stream_chat as tembo_stream
        yield from tembo_stream(messages, model=model or "tembo-assistant")
        return

    elif provider == "poolside":
        from api import poolside_proxy
        yield from poolside_proxy.stream_chat(messages, model=model or "laguna-s-2.1")
        return

    elif provider == "longcat":
        from api import longcat_proxy
        yield from longcat_proxy.stream_chat(messages, model=model or "longcat/LongCat-2.0")
        return

    elif provider == "geminiweb":
        from api import geminiweb_proxy
        yield from geminiweb_proxy.stream_chat(messages, model=model or "geminiweb/gemini-flash-lite")
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
        user_msg = _get_text_from_content(next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), ""))
        sys_msg = _get_text_from_content(next((m.get("content", "") for m in messages if m.get("role") == "system"), ""))
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

    # Fallback to Meta AI
    from api import metaai_proxy
    yield from metaai_proxy.stream_chat(messages, model=model or "metaai-instant", images=images)
