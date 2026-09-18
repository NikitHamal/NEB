"""Admin media test — TTS (Airy/LazyPy/Google/Moe/Kokoro/Chatterbox/Fish)

Session-authenticated (staff) AJAX endpoint so the admin panel can test
without Bearer tokens:
  POST /ajax/admin/media/tts/           {provider, text, voice, service, lang, speaker}
  GET  /ajax/admin/media/airy-voices/   Airy voice catalogue (?refresh=1)
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from api.llm.registry import SCRAPER_PRESETS

from .view_helpers import _require_staff_admin


def admin_media_test(request):
    resp = _require_staff_admin(request)
    if resp:
        return resp

    tts_presets = [p for p in SCRAPER_PRESETS if p.slug in ("lazypy", "googletts", "moetts", "kokoro", "chatterbox", "fishaudio", "airy")]

    tts_models = []
    for p in tts_presets:
        for m in p.models:
            tts_models.append({"id": m.id, "label": m.label, "provider": p.slug, "note": m.note})
    # Add Inception Mercury TTS (separate, uses chat.inceptionlabs.ai /api/tts)
    tts_models.append({"id": "inception/mercury-tts", "label": "Mercury TTS (Inception)", "provider": "inception", "note": "Diffusion TTS — streaming mp3, 5000 chars"})

    from django.shortcuts import render

    # Voice scenarios for Inception voice mode
    voice_scenarios = []
    try:
        from api.inception_proxy import get_voice_config
        cfg = get_voice_config()
        if cfg and cfg.get("scenarios"):
            for sc in cfg["scenarios"]:
                voice_scenarios.append({"id": sc.get("id"), "name": sc.get("name"), "description": sc.get("description","")[:120]})
    except Exception:
        pass

    return render(
        request,
        "admin_panel/media_test.html",
        {
            "is_admin": True,
            "active_page": "media_test",
            "tts_models": tts_models,
            "tts_models_json": json.dumps(tts_models),
            "voice_scenarios": voice_scenarios,
            "voice_scenarios_json": json.dumps(voice_scenarios),
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

    # Inception Mercury TTS — separate diffusion TTS (audio/mpeg stream)
    if provider.startswith("inception") or "mercury" in provider:
        try:
            from api.inception_proxy import synthesize
            import base64
            data = synthesize(text)
            if not data:
                return JsonResponse({"error": "Inception TTS empty"}, status=502)
            b64 = base64.b64encode(data).decode()
            data_url = f"data:audio/mpeg;base64,{b64}"
            return JsonResponse({
                "status": "success",
                "provider": "inception",
                "service": "Mercury TTS",
                "voice": "mercury-2",
                "dataUrl": data_url,
                "bytes": len(data),
                "contentType": "audio/mpeg",
                "text": text,
            })
        except Exception as exc:
            return JsonResponse({"error": f"{type(exc).__name__}: {exc}"}, status=502)

    try:
        if provider.startswith("airy"):
            from api.airy_proxy import MAX_TEXT, generate_tts as airy_tts

            if len(text) > MAX_TEXT:
                return JsonResponse({"error": f"Airy batches {MAX_TEXT} chars max (got {len(text)})"}, status=400)
            result = airy_tts(
                text=text,
                voice=voice,
                style=payload.get("style") or "normal",
                speed=payload.get("speed") or 1.0,
                language=payload.get("lang") or payload.get("language") or "en",
            )
        elif provider.startswith("lazypy") or provider in ("bing", "microsoft", "edge"):
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
            "batches": result.get("batches"),
            "durationSec": result.get("durationSec"),
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


@require_GET
def ajax_admin_media_airy_voices(request):
    """Airy voice catalogue (104 voices) for the media-test picker."""
    resp = _require_staff_admin(request)
    if resp:
        return JsonResponse({"error": "staff only"}, status=403)
    try:
        from api.airy_proxy import CHAR_LIMIT, MAX_CHUNKS, MAX_TEXT, STYLES, get_voices

        voices = get_voices(refresh=bool(request.GET.get("refresh")))
        return JsonResponse({
            "status": "success",
            "voices": voices,
            "styles": list(STYLES),
            "charLimit": CHAR_LIMIT,
            "maxChunks": MAX_CHUNKS,
            "maxText": MAX_TEXT,
        })
    except Exception as exc:
        return JsonResponse({"error": f"{type(exc).__name__}: {exc}", "voices": []}, status=502)


@require_POST
def ajax_admin_media_image(request):
    resp = _require_staff_admin(request)
    if resp:
        return JsonResponse({"error": "staff only"}, status=403)
    return JsonResponse({"error": "Image test not implemented yet."}, status=501)


@require_POST
def ajax_admin_media_stt(request):
    """Inception STT — upload audio/webm, return transcript."""
    resp = _require_staff_admin(request)
    if resp:
        return JsonResponse({"error": "staff only"}, status=403)
    f = request.FILES.get("file") or request.FILES.get("audio")
    if not f:
        return JsonResponse({"error": "audio file required (field 'file')"}, status=400)
    data = f.read()
    if len(data) < 1200:
        return JsonResponse({"error": "audio too short (<1200 bytes)"}, status=400)
    if len(data) > 8 * 1024 * 1024:
        return JsonResponse({"error": "audio too large (max 8MB)"}, status=400)
    try:
        from api.inception_proxy import transcribe
        text = transcribe(data, mime=f.content_type or "audio/webm", filename=f.name or "audio.webm")
        if text is None:
            return JsonResponse({"error": "STT failed (upstream)"}, status=502)
        return JsonResponse({"status": "success", "text": text, "bytes": len(data)})
    except Exception as exc:
        return JsonResponse({"error": f"{type(exc).__name__}: {exc}"}, status=502)


@require_POST
def ajax_admin_media_voice(request):
    """Inception full voice pipeline: STT(optional) + Mercury chat + TTS, or text-in voice-out."""
    resp = _require_staff_admin(request)
    if resp:
        return JsonResponse({"error": "staff only"}, status=403)
    # Accept either JSON or multipart
    try:
        if request.content_type and "application/json" in request.content_type:
            payload = json.loads(request.body or "{}")
            text = (payload.get("text") or payload.get("message") or "").strip()
            scenario_id = (payload.get("scenarioId") or payload.get("scenario") or "").strip() or None
            audio_bytes = None
        else:
            text = (request.POST.get("text") or request.POST.get("message") or "").strip()
            scenario_id = (request.POST.get("scenarioId") or request.POST.get("scenario") or "").strip() or None
            f = request.FILES.get("file") or request.FILES.get("audio")
            audio_bytes = f.read() if f else None
            if audio_bytes and len(audio_bytes) < 1200:
                return JsonResponse({"error": "audio too short"}, status=400)
    except Exception as exc:
        return JsonResponse({"error": f"bad request: {exc}"}, status=400)

    # If audio provided, transcribe first (STT)
    stt_text = ""
    if audio_bytes:
        try:
            from api.inception_proxy import transcribe
            stt_text = transcribe(audio_bytes, mime="audio/webm") or ""
            if not stt_text:
                return JsonResponse({"error": "STT empty — try clearer audio"}, status=502)
            text = stt_text
        except Exception as exc:
            return JsonResponse({"error": f"STT failed: {exc}"}, status=502)

    if not text:
        return JsonResponse({"error": "text or audio required"}, status=400)
    if len(text) > 4000:
        text = text[:4000]

    # Chat via Mercury (voice turn if scenario, else plain chat)
    try:
        from api.inception_proxy import voice_turn, stream_chat
        import base64
        # Choose voice pipeline if scenario given, else plain Mercury chat
        if scenario_id:
            # Full voice turn with tool streaming
            chunks = []
            for ev in voice_turn([{"role": "user", "content": text}], scenario_id=scenario_id):
                if ev.get("type") == "text":
                    chunks.append(ev.get("content",""))
                elif ev.get("type") == "error":
                    return JsonResponse({"error": ev.get("error")}, status=502)
            reply_text = "".join(chunks).strip()
        else:
            # Plain Mercury chat (voiceMode False, but we will TTS the result)
            from api.inception_proxy import simple_chat
            reply_text = simple_chat(text) or ""
        if not reply_text:
            return JsonResponse({"error": "Mercury empty"}, status=502)
        # TTS the reply
        from api.inception_proxy import synthesize
        audio = synthesize(reply_text)
        if not audio:
            return JsonResponse({"status": "success", "text": reply_text, "sttText": stt_text, "audioUrl": None, "warning": "TTS empty"})
        b64 = base64.b64encode(audio).decode()
        data_url = f"data:audio/mpeg;base64,{b64}"
        return JsonResponse({
            "status": "success",
            "sttText": stt_text,
            "text": reply_text,
            "dataUrl": data_url,
            "bytes": len(audio),
            "contentType": "audio/mpeg",
            "scenarioId": scenario_id,
        })
    except Exception as exc:
        return JsonResponse({"error": f"{type(exc).__name__}: {exc}"}, status=502)
