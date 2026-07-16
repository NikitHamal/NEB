"""
Consica AI Bridge API — dedicated endpoint for the Consica Flutter app.

Provides a clean JSON-in / JSON-out interface backed by the Nebians
free-AI stack (Qwen → G4F → DeepSeek → EQing fallback chain).

Authentication: static shared secret via X-Consica-Key header.
Rate limiting:  10 requests/minute per IP (generous for a mobile app).

Endpoint:
    POST /api/consica-bridge/generate/
    {
      "system_prompt": "...",
      "user_prompt":   "...",
      "task_type":     "json" | "text"   (default: "json")
    }

Response:
    { "result": { ... } }   // parsed dict when task_type=json
    { "result": "..."   }   // raw text when task_type=text

Error:
    { "error": "reason", "code": "auth_failed|invalid_request|ai_error" }
"""
import json
import logging
import re
import time

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def _error(msg, code, status=400):
    return JsonResponse({'error': msg, 'code': code}, status=status)


def _validate_key(request):
    """Validate the shared secret header."""
    bridge_key = getattr(settings, 'CONSICA_BRIDGE_KEY', '')
    if not bridge_key:
        logger.error('CONSICA_BRIDGE_KEY is not configured in settings')
        return False
    provided = request.META.get('HTTP_X_CONSICA_KEY', '')
    # Constant-time comparison to prevent timing attacks
    import hmac
    return hmac.compare_digest(provided.encode(), bridge_key.encode())


# ── In-memory rate limiter (sliding window per IP) ────────────────────────────

_rate_store: dict = {}
_RATE_LIMIT = 10    # max requests
_RATE_WINDOW = 60   # per N seconds


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    window_start = now - _RATE_WINDOW
    bucket = _rate_store.setdefault(ip, [])
    _rate_store[ip] = [t for t in bucket if t > window_start]
    if len(_rate_store[ip]) >= _RATE_LIMIT:
        return True
    _rate_store[ip].append(now)
    return False


# ── AI fallback chain ─────────────────────────────────────────────────────────

def _call_qwen(system_prompt: str, user_prompt: str):
    """Primary: Qwen browser-spoof (no API key, no cost)."""
    try:
        from api.qwen_utils.client import QwenClient
        client = QwenClient()
        chat_id = client.create_chat()
        if not chat_id:
            return None
        result = client.send_message(
            chat_id,
            user_prompt,
            system_prompt=system_prompt,
        )
        return result
    except Exception as e:
        logger.warning('Consica bridge [Qwen]: %s', e)
        return None


def _call_neby_provider(system_prompt: str, user_prompt: str, provider: str, model: str):
    """Generic helper that uses neby.call_ai_api with an ephemeral config object."""
    try:
        from api.neby import call_ai_api

        class _Cfg:
            pass

        cfg = _Cfg()
        cfg.provider = provider
        cfg.model = model
        cfg.api_url = ''
        cfg.api_key = ''
        cfg.response_max_length = 3000
        return call_ai_api(system_prompt, user_prompt, config=cfg)
    except Exception as e:
        logger.warning('Consica bridge [%s]: %s', provider, e)
        return None


def _generate_with_fallback(system_prompt: str, user_prompt: str):
    """Try providers in priority order until one succeeds."""
    providers = [
        ('qwen_direct', None, None),
        ('inception',   'inception',  'mercury-2'),
    ]
    for name, provider, model in providers:
        if name == 'qwen_direct':
            result = _call_qwen(system_prompt, user_prompt)
        else:
            result = _call_neby_provider(system_prompt, user_prompt, provider, model)
        if result and result.strip():
            logger.info('Consica bridge: success via %s', name)
            return result.strip()
    return None


# ── JSON extraction ───────────────────────────────────────────────────────────

def _extract_json(text: str):
    """Extract JSON object or array from AI response (handles markdown fences)."""
    text = text.strip()
    # 1. Direct parse
    try:
        parsed = json.loads(text)
        if isinstance(parsed, (dict, list)):
            return parsed
    except json.JSONDecodeError:
        pass
    # 2. Strip markdown fences
    for pat in (r'```json\s*([\s\S]+?)\s*```', r'```\s*([\s\S]+?)\s*```'):
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                parsed = json.loads(m.group(1))
                if isinstance(parsed, (dict, list)):
                    return parsed
            except json.JSONDecodeError:
                pass
    # 3. Greedy brace/bracket search
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start != -1 and end > start:
            try:
                parsed = json.loads(text[start:end + 1])
                if isinstance(parsed, (dict, list)):
                    return parsed
            except json.JSONDecodeError:
                pass
    return None


# ── View ──────────────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def consica_generate(request):
    """
    POST /api/consica-bridge/generate/

    Headers:
        X-Consica-Key: <shared secret>
        Content-Type: application/json

    Body:
        system_prompt  str  (required)
        user_prompt    str  (required)
        task_type      str  "json" | "text"  (default: "json")
    """
    ip = _get_client_ip(request)

    # 1. Authenticate
    if not _validate_key(request):
        logger.warning('Consica bridge: auth failure from %s', ip)
        return _error('Unauthorized', 'auth_failed', status=401)

    # 2. Rate limit
    if _is_rate_limited(ip):
        return _error('Too many requests — please slow down', 'rate_limited', status=429)

    # 3. Parse body
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _error('Request body must be valid JSON', 'invalid_request', status=400)

    system_prompt = (body.get('system_prompt') or '').strip()
    user_prompt   = (body.get('user_prompt')   or '').strip()
    task_type     = (body.get('task_type')      or 'json').strip().lower()

    if not system_prompt or not user_prompt:
        return _error(
            'system_prompt and user_prompt are required',
            'invalid_request',
            status=400,
        )
    if len(system_prompt) > 20000 or len(user_prompt) > 8000:
        return _error('Prompt too long', 'invalid_request', status=400)

    # 4. Generate
    logger.info('Consica bridge: task=%s from %s', task_type, ip)
    raw = _generate_with_fallback(system_prompt, user_prompt)

    if not raw:
        logger.error('Consica bridge: all providers failed (IP=%s)', ip)
        return _error(
            'AI generation failed — all providers unavailable',
            'ai_error',
            status=503,
        )

    # 5. Return
    if task_type == 'text':
        return JsonResponse({'result': raw})

    # JSON mode — parse and return structured data
    parsed = _extract_json(raw)
    if parsed is not None:
        return JsonResponse({'result': parsed})

    # Fallback: raw text with a warning so Consica can still handle it
    logger.warning('Consica bridge: JSON extraction failed, returning raw (IP=%s)', ip)
    return JsonResponse({
        'result': raw,
        'parse_warning': 'AI response was not valid JSON — raw text returned',
    })
