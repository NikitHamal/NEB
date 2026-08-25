"""
AstroWeb LLM Bridge — secure, streaming, OpenAI-compatible proxy to the
NEBians LLM registry.

Auth:   X-AstroWeb-Bridge-Key  (constant-time compare vs ASTROWEB_BRIDGE_KEY)
        Accepts X-Consica-Key as alias so one secret can serve both apps during migration.

Rate:   10 req/min per IP (sliding window, per-isolate).

Endpoints (mounted under /api/astroweb-bridge/):
    GET  /models/                       Unified model catalog from registry
    POST /v1/chat/completions          OpenAI-compatible chat (stream + non-stream)
    POST /chat/                        Alias (same)

The models list is public (readable without auth) so AstroWeb can render
pickers before the user authenticates. The chat endpoint requires auth +
rate limiting.

All 17 NEBians presets are exposed. Official providers use the shared
api.llm client (server env keys); scrapers use their existing proxy
modules. No browser secret is ever involved — AstroWeb's Cloudflare Worker
holds the bridge key.
"""
import hmac
import importlib
import json
import logging
import time
from typing import Dict, List, Optional

from django.conf import settings
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("api.astroweb_bridge")

_RATE_STORE: Dict[str, List[float]] = {}
_RATE_LIMIT = 10
_RATE_WINDOW = 60


def _client_ip(request) -> str:
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    win = now - _RATE_WINDOW
    b = [t for t in _RATE_STORE.get(ip, []) if t > win]
    if len(b) >= _RATE_LIMIT:
        _RATE_STORE[ip] = b
        return True
    b.append(now)
    _RATE_STORE[ip] = b
    return False


def _bridge_key() -> str:
    k = (getattr(settings, "ASTROWEB_BRIDGE_KEY", "") or "").strip()
    if k:
        return k
    return (getattr(settings, "CONSICA_BRIDGE_KEY", "") or "").strip()


def _validate_key(request) -> bool:
    expected = _bridge_key()
    if not expected:
        logger.error("ASTROWEB_BRIDGE_KEY not configured")
        return False
    provided = (
        request.META.get("HTTP_X_ASTROWEB_BRIDGE_KEY", "")
        or request.META.get("HTTP_X_CONSICA_KEY", "")
        or request.headers.get("X-AstroWeb-Bridge-Key", "")
        or request.headers.get("X-Consica-Key", "")
    )
    if not provided:
        return False
    return hmac.compare_digest(provided.encode(), expected.encode())


def _cors_json(body, status=200):
    resp = JsonResponse(body, status=status, json_dumps_params={"ensure_ascii": False})
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Access-Control-Allow-Headers"] = "content-type, authorization, x-astroweb-bridge-key, x-consica-key"
    resp["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


# ── Models ───────────────────────────────────────────────────────────

# Providers hidden from the AstroWeb bridge (private / token-costly).
# They remain available inside NEBians (admin bots, Neby, CLI).
ASTROWEB_HIDDEN_PROVIDERS = {"metaai"}


def _catalog() -> List[Dict]:
    from api.llm.registry import ALL_PRESETS

    out = []
    for slug, preset in ALL_PRESETS.items():
        if slug in ASTROWEB_HIDDEN_PROVIDERS:
            continue
        for m in preset.models:
            out.append({
                "id": m.id,
                "name": m.label,
                "note": m.note or "",
                "provider": preset.slug,
                "label": preset.label,
                "context_window": preset.context_window,
                "max_output_tokens": preset.max_output_tokens,
                "official": preset.official,
                "format": preset.format,
            })
    return out


@csrf_exempt
def astroweb_models(request):
    if request.method == "OPTIONS":
        r = JsonResponse({})
        r["Access-Control-Allow-Origin"] = "*"
        r["Access-Control-Allow-Headers"] = "content-type, authorization, x-astroweb-bridge-key, x-consica-key"
        r["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return r
    if request.method != "GET":
        return _cors_json({"error": "method_not_allowed"}, status=405)
    models = _catalog()
    resp = _cors_json({"models": models, "count": len(models)})
    return resp


# ── Dispatch helpers ──────────────────────────────────────────────────

def _find_preset(model_id: str):
    from api.llm.registry import ALL_PRESETS

    mid = (model_id or "").strip()
    if not mid:
        return None, None
    for slug, preset in ALL_PRESETS.items():
        if slug in ASTROWEB_HIDDEN_PROVIDERS:
            continue
        for spec in preset.models:
            if spec.id == mid or spec.id.lower() == mid.lower():
                return preset, spec
    low = mid.lower()
    for slug, preset in ALL_PRESETS.items():
        if slug in ASTROWEB_HIDDEN_PROVIDERS:
            continue
        if low.startswith(slug + "/") or low == slug:
            return preset, (preset.models[0] if preset.models else None)
    return None, None


def _messages_to_prompt(messages: List[Dict]) -> tuple:
    sys_parts, user_parts = [], []
    for m in messages or []:
        role = (m.get("role") or "user").strip().lower()
        content = m.get("content") or ""
        if isinstance(content, list):
            content = "".join(
                p.get("text", "") if isinstance(p, dict) else str(p) for p in content
            )
        content = str(content or "")
        if role == "system":
            if content.strip():
                sys_parts.append(content.strip())
        elif role == "tool":
            name = m.get("name") or m.get("tool_call_id") or "tool"
            user_parts.append(f'<tool_result name="{name}">\n{content}\n</tool_result>')
        elif role == "assistant" and m.get("tool_calls"):
            tcs = m.get("tool_calls") or []
            extra = []
            for tc in tcs:
                fn = tc.get("function") or {}
                n = fn.get("name") or tc.get("name") or "unknown"
                a = fn.get("arguments") or "{}"
                if isinstance(a, dict):
                    a = json.dumps(a)
                extra.append(f'««TOOL_CALL»» {json.dumps({"name": n, "arguments": json.loads(a) if isinstance(a, str) else a})} ««/TOOL_CALL»»')
            user_parts.append(content + ("\n" + "\n".join(extra) if extra else ""))
        else:
            prefix = "Assistant" if role == "assistant" else "User"
            user_parts.append(f"{prefix}: {content}" if messages and len(messages) > 1 else content)
    system_prompt = "\n\n".join(sys_parts)
    user_prompt = "\n\n".join(user_parts) if user_parts else (messages[-1].get("content", "") if messages else "")
    return system_prompt, user_prompt


def _check_waf_body(text: str) -> bool:
    return any(k in text for k in ("RGV587_ERROR", "_____tmd_____", "x5secdata"))


# ── Chat ──────────────────────────────────────────────────────────────

@csrf_exempt
def astroweb_chat_completions(request):
    if request.method == "OPTIONS":
        r = JsonResponse({})
        r["Access-Control-Allow-Origin"] = "*"
        r["Access-Control-Allow-Headers"] = "content-type, authorization, x-astroweb-bridge-key, x-consica-key"
        r["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return r
    if request.method not in ("POST", "GET"):
        return _cors_json({"error": "method_not_allowed"}, status=405)

    ip = _client_ip(request)
    if not _validate_key(request):
        logger.warning("AstroWeb bridge auth failure from %s", ip)
        return _cors_json({"error": "Unauthorized", "code": "auth_failed"}, status=401)
    if _is_rate_limited(ip):
        return _cors_json({"error": "Too many requests — please slow down", "code": "rate_limited"}, status=429)

    if request.method == "GET":
        return astroweb_models(request)

    try:
        body = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _cors_json({"error": "Request body must be valid JSON", "code": "invalid_request"}, status=400)

    model = (body.get("model") or "").strip()
    messages = body.get("messages") or []
    stream = bool(body.get("stream"))
    tools = body.get("tools") if isinstance(body.get("tools"), list) else None
    max_tokens = int(body.get("max_tokens") or 2048)
    temperature = float(body.get("temperature") or 0.7)
    system_prompt_override = (body.get("system_prompt") or "").strip()
    user_prompt_override = (body.get("user_prompt") or "").strip()

    if user_prompt_override and not messages:
        messages = [{"role": "user", "content": user_prompt_override}]
        if system_prompt_override:
            messages = [{"role": "system", "content": system_prompt_override}] + messages
    elif system_prompt_override and messages:
        messages = [{"role": "system", "content": system_prompt_override}] + list(messages)

    if not messages or not isinstance(messages, list):
        return _cors_json({"error": "messages (array) is required", "code": "invalid_request"}, status=400)

    if not model:
        return _cors_json({"error": "model is required", "code": "invalid_request"}, status=400)

    preset, spec = _find_preset(model)
    if not preset:
        logger.warning("AstroWeb bridge: unknown model '%s' from %s, returning 400", model, ip)
        return _cors_json({"error": f"Unknown model '{model}'", "code": "unknown_model"}, status=400)

    real_model = spec.id if spec else preset.default_model
    logger.info("AstroWeb bridge: model=%s -> %s/%s stream=%s from %s", model, preset.slug, real_model, stream, ip)

    if stream:
        return _chat_stream_response(preset, real_model, messages, tools, max_tokens, temperature, ip)
    else:
        return _chat_nonstream_response(preset, real_model, messages, tools, max_tokens, temperature, ip)


def _chat_nonstream_response(preset, real_model: str, messages: List[Dict], tools, max_tokens: int, temperature: float, ip: str):
    text, tool_calls, meta = _call_once(preset, real_model, messages, tools, max_tokens, temperature)
    if text is None and not tool_calls:
        logger.error("AstroWeb bridge: all providers failed (%s) ip=%s", real_model, ip)
        return _cors_json({"error": "AI generation failed — all providers unavailable", "code": "ai_error"}, status=503)
    choice: Dict = {"index": 0, "message": {"role": "assistant", "content": text or ""}, "finish_reason": "stop"}
    if tool_calls:
        choice["message"]["tool_calls"] = tool_calls
    body = {
        "id": f"astroweb-{int(time.time()*1000)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": real_model,
        "choices": [choice],
        "usage": {"prompt_tokens": meta.get("prompt_tokens", 0), "completion_tokens": meta.get("completion_tokens", 0), "total_tokens": meta.get("total_tokens", 0)},
    }
    resp = JsonResponse(body, json_dumps_params={"ensure_ascii": False})
    resp["Access-Control-Allow-Origin"] = "*"
    return resp


def _chat_stream_response(preset, real_model: str, messages: List[Dict], tools, max_tokens: int, temperature: float, ip: str):
    def gen():
        saw_any = False
        tool_acc: Dict[int, Dict] = {}
        last_meta: Dict = {}

        try:
            for chunk in _stream_once(preset, real_model, messages, tools, max_tokens, temperature):
                ctype = chunk.get("type")
                if ctype == "text":
                    saw_any = True
                    data = {"choices": [{"index": 0, "delta": {"content": chunk.get("content", "")}, "finish_reason": None}], "model": real_model}
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                elif ctype == "reasoning":
                    saw_any = True
                    data = {"choices": [{"index": 0, "delta": {"reasoning_content": chunk.get("content", "")}, "finish_reason": None}], "model": real_model}
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                elif ctype == "tool_call":
                    for tc in chunk.get("tool_calls") or chunk.get("calls") or []:
                        idx = tc.get("index", 0)
                        if idx not in tool_acc:
                            tool_acc[idx] = {"id": tc.get("id") or f"call_{idx}", "type": "function", "function": {"name": "", "arguments": ""}}
                        fn = tc.get("function") or {}
                        if fn.get("name"):
                            tool_acc[idx]["function"]["name"] += fn["name"]
                        if fn.get("arguments"):
                            tool_acc[idx]["function"]["arguments"] += fn["arguments"] if isinstance(fn["arguments"], str) else json.dumps(fn["arguments"])
                    data = {"choices": [{"index": 0, "delta": {"tool_calls": chunk.get("tool_calls") or chunk.get("calls") or []}, "finish_reason": None}], "model": real_model}
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                elif ctype == "error":
                    data = {"error": {"message": chunk.get("error", "upstream error"), "type": "upstream_error"}}
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                    break
                elif ctype == "done":
                    last_meta = chunk
                    break
                elif ctype == "meta":
                    last_meta = chunk.get("meta") or chunk
        except Exception as exc:
            logger.exception("AstroWeb bridge stream error: %s", exc)
            yield f"data: {json.dumps({'error': {'message': str(exc)}})}\n\n"

        if tool_acc:
            for idx in sorted(tool_acc.keys()):
                tc = tool_acc[idx]
                data = {"choices": [{"index": 0, "delta": {"tool_calls": [{"index": idx, **tc}]}, "finish_reason": None}], "model": real_model}
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

        if not saw_any and not tool_acc and not last_meta.get("error"):
            data = {"error": {"message": "AI stream ended without content", "type": "no_content"}}
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

        finish = {"choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}], "model": real_model}
        if last_meta.get("usage"):
            finish["usage"] = last_meta["usage"]
        yield f"data: {json.dumps(finish, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    resp = StreamingHttpResponse(gen(), content_type="text/event-stream")
    resp["Cache-Control"] = "no-cache"
    resp["X-Accel-Buffering"] = "no"
    resp["Access-Control-Allow-Origin"] = "*"
    resp["Access-Control-Allow-Headers"] = "content-type, authorization, x-astroweb-bridge-key, x-consica-key"
    return resp


# ── Unified one-shot / streaming dispatcher ──────────────────────────

def _call_once(preset, real_model: str, messages: List[Dict], tools, max_tokens: int, temperature: float):
    if not preset.official:
        text, tcs, meta = _call_scraper_once(preset, real_model, messages, tools, max_tokens)
        return text, tcs, meta
    return _call_official_once(preset, real_model, messages, tools, max_tokens, temperature)


def _stream_once(preset, real_model: str, messages: List[Dict], tools, max_tokens: int, temperature: float):
    if not preset.official:
        yield from _call_scraper_stream(preset, real_model, messages, tools, max_tokens)
        return
    yield from _call_official_stream(preset, real_model, messages, tools, max_tokens, temperature)


def _call_scraper_once(preset, real_model: str, messages: List[Dict], tools, max_tokens: int):
    mod_name = preset.scraper_module
    try:
        mod = importlib.import_module(f"api.{mod_name}")
    except ImportError as e:
        logger.error("AstroWeb bridge: no proxy module api.%s: %s", mod_name, e)
        return None, None, {}
    sys_prompt, user_prompt = _messages_to_prompt(messages)
    if mod_name == "qwen_proxy":
        try:
            text = mod.call_qwen(sys_prompt, user_prompt, model=real_model, max_tokens=max_tokens)
            return (text or "").strip() or None, None, {}
        except Exception as e:
            logger.warning("AstroWeb bridge [qwen] once failed: %s", e)
            return None, None, {}
    try:
        if hasattr(mod, "simple_chat"):
            kwargs = {}
            import inspect as _ins
            sig = _ins.signature(mod.simple_chat)
            if "system_prompt" in sig.parameters:
                kwargs["system_prompt"] = sys_prompt
            if "max_tokens" in sig.parameters:
                kwargs["max_tokens"] = max_tokens
            text = mod.simple_chat(user_message=user_prompt, model=real_model, **kwargs)
            return (text or "").strip() or None, None, {}
    except Exception as e:
        logger.warning("AstroWeb bridge [%s] once failed: %s", preset.slug, e)
    return None, None, {}


def _call_scraper_stream(preset, real_model: str, messages: List[Dict], tools, max_tokens: int):
    mod_name = preset.scraper_module
    try:
        mod = importlib.import_module(f"api.{mod_name}")
    except ImportError as e:
        yield {"type": "error", "error": f"No proxy for {preset.slug}: {e}"}
        return
    if mod_name == "qwen_proxy":
        text, tcs, _ = _call_scraper_once(preset, real_model, messages, tools, max_tokens)
        if text:
            yield {"type": "text", "content": text}
        elif tcs:
            yield {"type": "tool_call", "tool_calls": tcs}
        else:
            yield {"type": "error", "error": "Qwen returned empty response"}
        yield {"type": "done"}
        return
    scraper_messages = messages
    gen = None
    try:
        if hasattr(mod, "stream_chat"):
            import inspect as _ins
            sig = _ins.signature(mod.stream_chat)
            kwargs: Dict = {"messages": scraper_messages, "model": real_model}
            if "effort" in sig.parameters and preset.slug == "tryingopen":
                kwargs["effort"] = "balanced"
            if "system_prompt" in sig.parameters:
                sys_prompt, _ = _messages_to_prompt(messages)
                if sys_prompt and "system_prompt" not in kwargs:
                    kwargs["system_prompt"] = sys_prompt
            gen = mod.stream_chat(**{k: v for k, v in kwargs.items() if k in sig.parameters})
        elif hasattr(mod, "simple_chat"):
            text, tcs, _ = _call_scraper_once(preset, real_model, messages, tools, max_tokens)
            if text:
                yield {"type": "text", "content": text}
            if tcs:
                yield {"type": "tool_call", "tool_calls": tcs}
            yield {"type": "done"}
            return
        else:
            yield {"type": "error", "error": f"No streaming entry for {preset.slug}"}
            return
    except Exception as e:
        yield {"type": "error", "error": f"{preset.slug} dispatch failed: {e}"}
        return
    if gen is None:
        yield {"type": "error", "error": f"No stream from {preset.slug}"}
        return
    try:
        for chunk in gen:
            ctype = chunk.get("type")
            if ctype in ("text", "content"):
                yield {"type": "text", "content": chunk.get("content") or chunk.get("text") or ""}
            elif ctype in ("reasoning", "reasoning_content", "think"):
                yield {"type": "reasoning", "content": chunk.get("content") or chunk.get("reasoning") or chunk.get("text") or ""}
            elif ctype in ("tool_call", "tool_calls"):
                yield {"type": "tool_call", "tool_calls": chunk.get("tool_calls") or chunk.get("calls") or chunk.get("tool_calls") or []}
            elif ctype == "error":
                yield {"type": "error", "error": chunk.get("error") or chunk.get("message") or "upstream error"}
                return
            elif ctype == "done":
                yield {"type": "done"}
                return
            elif ctype == "meta":
                yield {"type": "meta", "meta": chunk.get("meta") or {}}
    except Exception as e:
        yield {"type": "error", "error": f"{preset.slug} stream failed: {e}"}


def _call_official_once(preset, real_model: str, messages: List[Dict], tools, max_tokens: int, temperature: float):
    from api.llm import client as llm_client

    api_key = _official_api_key(preset.slug)
    if not api_key:
        logger.warning("AstroWeb bridge: no key for official %s (model %s)", preset.slug, real_model)
        return None, None, {}
    kwargs = {}
    if tools:
        kwargs["tools"] = tools
    try:
        result = llm_client.chat(
            format=preset.format,
            base_url=preset.base_url,
            api_key=api_key,
            model=real_model,
            messages=messages,
            max_tokens=max_tokens,
            timeout=120,
            temperature=temperature,
            provider=preset.slug,
            **kwargs,
        )
        tool_calls = None
        raw = getattr(result, "raw", {}) or {}
        if isinstance(raw, dict) and raw.get("tool_calls"):
            tool_calls = raw["tool_calls"]
        return result.text, tool_calls, {"prompt_tokens": result.input_tokens, "completion_tokens": result.output_tokens, "total_tokens": result.input_tokens + result.output_tokens}
    except Exception as e:
        logger.warning("AstroWeb bridge [official %s] failed: %s", preset.slug, e)
        return None, None, {}


def _call_official_stream(preset, real_model: str, messages: List[Dict], tools, max_tokens: int, temperature: float):
    from api.llm import client as llm_client

    api_key = _official_api_key(preset.slug)
    if not api_key:
        yield {"type": "error", "error": f"No API key configured for {preset.slug}"}
        return
    kwargs = {}
    if tools:
        kwargs["tools"] = tools
    try:
        for chunk in llm_client.chat_stream(
            format=preset.format,
            base_url=preset.base_url,
            api_key=api_key,
            model=real_model,
            messages=messages,
            max_tokens=max_tokens,
            timeout=180,
            temperature=temperature,
            provider=preset.slug,
            **kwargs,
        ):
            ctype = chunk.get("type")
            if ctype == "text":
                yield {"type": "text", "content": chunk.get("content") or chunk.get("text") or ""}
            elif ctype == "reasoning":
                yield {"type": "reasoning", "content": chunk.get("content") or ""}
            elif ctype == "tool_call":
                yield {"type": "tool_call", "tool_calls": chunk.get("tool_calls") or []}
            elif ctype == "done":
                yield {"type": "done", "usage": chunk.get("usage")}
                return
            elif ctype == "error":
                yield {"type": "error", "error": chunk.get("error") or "upstream error"}
                return
    except Exception as e:
        yield {"type": "error", "error": f"{preset.slug} stream failed: {e}"}


def _official_api_key(slug: str) -> str:
    slug = (slug or "").strip().lower()
    keys = getattr(settings, "LLM_PROVIDER_KEYS", {}) or {}
    k = (keys.get(slug) or "").strip()
    if k:
        return k
    import os as _os
    env_map = {"agnes": "AGNES_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "gemini": "GEMINI_API_KEY", "deepseek": "DEEPSEEK_API_KEY", "agentrouter": "AGENTROUTER_API_KEY", "empero": "EMPERO_API_KEY"}
    env_name = env_map.get(slug, "")
    if env_name:
        k = (_os.environ.get(env_name) or "").strip()
        if k:
            return k
    if slug == "empero":
        return "free"
    return ""
