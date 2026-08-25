"""
Unified TTS views — exposes Lazypy/Bing, Google Translate, Moe, Chatterbox, etc.
"""
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

from .throttles import ArenaChatRateThrottle


def _require_user(request):
    from .views import _require_user as _ru

    return _ru(request)


@api_view(["GET"])
@throttle_classes([ArenaChatRateThrottle])
def tts_models(request):
    user = _require_user(request)
    if isinstance(user, Response):
        return user
    from .chatterbox_proxy import get_models as ch_models
    from .fish_proxy import get_models as fish_models
    from .google_tts_proxy import get_models as g_models
    from .kokoro_proxy import get_models as k_models
    from .lazypy_proxy import get_models as lz_models
    from .moe_tts_proxy import get_models as moe_models

    return Response(
        {
            "tts": lz_models() + g_models() + moe_models() + k_models() + ch_models() + fish_models(),
            "image": [],
        }
    )


@api_view(["POST"])
@throttle_classes([ArenaChatRateThrottle])
def tts_generate(request):
    user = _require_user(request)
    if isinstance(user, Response):
        return user

    provider = (request.data.get("provider") or request.data.get("model") or "lazypy").strip().lower()
    text = (request.data.get("text") or request.data.get("prompt") or "").strip()
    if not text:
        return Response({"error": "text required"}, status=400)
    if len(text) > 5000:
        return Response({"error": "text too long (max 5000)"}, status=400)

    # Route by provider string
    if provider.startswith("lazypy") or provider in ("bing", "microsoft", "edge"):
        from .lazypy_proxy import generate_tts

        voice = request.data.get("voice")
        service = request.data.get("service") or "Bing Translator"
        if "google" in provider:
            service = "Google Translate"
        elif "ispeech" in provider:
            service = "iSpeech"
        result = generate_tts(text=text, voice=voice, service=service)
    elif provider.startswith("google"):
        from .google_tts_proxy import generate_tts as google_tts

        lang = request.data.get("lang") or request.data.get("voice") or "en"
        result = google_tts(text=text, lang=lang)
    elif provider.startswith("moe"):
        from .moe_tts_proxy import generate_tts as moe_tts

        speaker = request.data.get("voice") or request.data.get("speaker") or "Hoshino"
        result = moe_tts(text=text, speaker=speaker)
    elif provider.startswith("kokoro"):
        from .kokoro_proxy import generate_tts as kokoro_tts

        result = kokoro_tts(
            text=text,
            voice=request.data.get("voice") or request.data.get("speaker"),
            speed=request.data.get("speed") or 1.0,
            model=provider,
        )
    elif provider.startswith("chatterbox"):
        from .chatterbox_proxy import generate_tts as ch_tts

        result = ch_tts(
            text=text,
            exaggeration=request.data.get("exaggeration") or 0.5,
            temperature=request.data.get("temperature") or 0.8,
            seed=request.data.get("seed") or 0,
        )
    elif provider.startswith("fish"):
        from .fish_proxy import generate_tts as fish_tts

        result = fish_tts(text=text, voice=request.data.get("voice") or "default")
    else:
        # Default to Lazypy Bing (most reliable)
        from .lazypy_proxy import generate_tts

        result = generate_tts(text=text, voice=request.data.get("voice"))

    if result.get("status") != "success":
        return Response({"error": result.get("error", "TTS failed"), "raw": result.get("raw")}, status=502)

    # Return only safe fields
    return Response(
        {
            "status": "success",
            "provider": result.get("provider"),
            "service": result.get("service"),
            "voice": result.get("voice"),
            "audioUrl": result.get("audioUrl"),
            "dataUrl": result.get("dataUrl"),
            "bytes": result.get("bytes"),
            "contentType": result.get("contentType", "audio/mpeg"),
            "text": result.get("text"),
        }
    )
