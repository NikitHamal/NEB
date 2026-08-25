"""Admin media test — TTS (LazyPy/Google/Moe/Kokoro/Chatterbox/Fish)

Session-authenticated (staff) AJAX endpoint so the admin panel can test
without Bearer tokens:
  POST /ajax/admin/media/tts/     {provider, text, voice, service, lang, speaker}
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from api.llm.registry import SCRAPER_PRESETS

from .view_helpers import _require_staff_admin


def admin_media_test(request):
    resp = _require_staff_admin(request)
    if resp:
        return resp

    tts_presets = [p for p in SCRAPER_PRESETS if p.slug in ("lazypy", "googletts", "moetts", "kokoro", "chatterbox", "fishaudio")]

    tts_models = []
    for p in tts_presets:
        for m in p.models:
            tts_models.append({"id": m.id, "label": m.label, "provider": p.slug, "note": m.note})

    from django.shortcuts import render

    return render(
        request,
        "admin_panel/media_test.html",
        {
            "is_admin": True,
            "active_page": "media_test",
            "tts_models": tts_models,
            "tts_models_json": json.dumps(tts_models),
        },
    )


def _run_tts(payload):
    provider = (payload.get("provider") or payload.get("model") or "lazypy").strip().lower()
    text = (payload.get("text") or payload.get("prompt") or "").strip()
    if not text:
        return JsonResponse({"error": "text required"}, status=400)
    if len(text) > 5000:
        return JsonResponse({"error": "text too long (max 5000)"}, status=400)

    voice = (payload.get("voice") or "").strip() or None

    try:
        if provider.startswith("lazypy") or provider in ("bing", "microsoft", "edge"):
            from api.lazypy_proxy import generate_tts

            service = payload.get("service") or "Bing Translator"
            if "google" in provider:
                service = "Google Translate"
            elif "ispeech" in provider:
                service = "iSpeech"
            result = generate_tts(text=text, voice=voice, service=service)
        elif provider.startswith("google"):
            from api.google_tts_proxy import generate_tts as google_tts

            lang = (payload.get("lang") or voice or "en")
            result = google_tts(text=text, lang=lang)
        elif provider.startswith("moe"):
            from api.moe_tts_proxy import generate_tts as moe_tts

            result = moe_tts(text=text, speaker=(payload.get("speaker") or voice or "Hoshino"))
        elif provider.startswith("kokoro"):
            from api.kokoro_proxy import generate_tts as kokoro_tts

            result = kokoro_tts(
                text=text,
                voice=voice,
                speed=payload.get("speed") or 1.0,
                model=payload.get("provider") or provider,
            )
        elif provider.startswith("chatterbox"):
            from api.chatterbox_proxy import generate_tts as ch_tts

            result = ch_tts(text=text)
        elif provider.startswith("fish"):
            from api.fish_proxy import generate_tts as fish_tts

            result = fish_tts(text=text, voice=voice)
        else:
            from api.lazypy_proxy import generate_tts

            result = generate_tts(text=text, voice=voice)
    except Exception as exc:
        return JsonResponse({"error": f"{type(exc).__name__}: {exc}"}, status=502)

    if result.get("status") != "success":
        return JsonResponse({"error": result.get("error", "TTS failed"), "raw": result.get("raw")}, status=502)

    return JsonResponse(
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


@require_POST
def ajax_admin_media_tts(request):
    resp = _require_staff_admin(request)
    if resp:
        return JsonResponse({"error": "staff only"}, status=403)
    try:
        payload = json.loads(request.body or "{}")
    except Exception:
        payload = request.POST.dict()
    return _run_tts(payload)


@require_POST
def ajax_admin_media_image(request):
    resp = _require_staff_admin(request)
    if resp:
        return JsonResponse({"error": "staff only"}, status=403)
    return JsonResponse({"error": "Image test not implemented yet."}, status=501)
