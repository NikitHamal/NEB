import json
import os

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from api.models import LazyDocMessage, LazyDocSession, User
from api.utils import now_ms, uuid_str
from . import lazy_agent
from .api_client import get_session_token
from .lazy_io import export_docx, export_pdf, extract_docx, extract_pdf_text, fix_html, text_to_html
from .view_helpers import _ctx, _rate_limit
from .views_canvas import _require_user, _canvas_credit_state, _spend_canvas_credit

MAX_UPLOAD = 8 * 1024 * 1024


def _get_user_or_none(request):
    token = get_session_token(request)
    if not token:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
    if token:
        from api.security import get_user_by_auth_token
        try:
            return get_user_by_auth_token(token)
        except User.DoesNotExist:
            pass
    uid = request.session.get('user_id')
    if uid:
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
    return None


def lazy_page(request):
    user = _get_user_or_none(request)
    if not user:
        login_url = reverse('web:login')
        return redirect(f"{login_url}?next=/lazy/")
    sessions = LazyDocSession.objects.filter(user=user)[:60]
    ctx = _ctx(request, hide_footer_links=True)
    ctx['sessions_json'] = json.dumps([_serialize_session(s) for s in sessions])
    unlimited, remaining, allowance = _canvas_credit_state(user)
    ctx['lazy_credits'] = {'unlimited': unlimited, 'remaining': max(0, remaining), 'allowance': allowance}
    return render(request, 'web/lazy.html', ctx)


def _serialize_session(s):
    return {
        'id': str(s.id),
        'title': s.title or 'New chat',
        'docTitle': s.doc_title or '',
        'messageCount': s.message_count,
        'hasDoc': bool(s.doc_html),
        'updatedAt': s.updated_at,
    }


def _serialize_message(m):
    meta = {}
    try:
        meta = json.loads(m.meta or '{}')
        if not isinstance(meta, dict):
            meta = {}
    except Exception:
        meta = {}
    atts = [a.get('name', '') for a in (meta.get('attachments') or []) if isinstance(a, dict)]
    return {
        'id': str(m.id),
        'role': m.role,
        'content': m.content or '',
        'tools': meta.get('tools') or [],
        'docUpdated': bool(meta.get('docUpdated')),
        'attachments': atts,
        'createdAt': m.created_at,
    }


def _owned(request, session_id):
    user, err = _require_user(request)
    if err:
        return None, None, err
    try:
        session = LazyDocSession.objects.get(id=session_id, user=user)
        return user, session, None
    except LazyDocSession.DoesNotExist:
        return None, None, JsonResponse({'error': 'Chat not found'}, status=404)


@require_GET
def ajax_lazy_sessions(request):
    user, err = _require_user(request)
    if err:
        return err
    rows = LazyDocSession.objects.filter(user=user)[:100]
    return JsonResponse({'sessions': [_serialize_session(s) for s in rows]})


@require_POST
def ajax_lazy_session_create(request):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'lazy_session_create', 20, 60):
        return JsonResponse({'error': 'Slow down'}, status=429)
    now = now_ms()
    session = LazyDocSession.objects.create(id=uuid_str(), user=user, title='New chat', created_at=now, updated_at=now)
    return JsonResponse({'session': _serialize_session(session)}, status=201)


@require_GET
def ajax_lazy_session_detail(request, session_id):
    user, session, err = _owned(request, session_id)
    if err:
        return err
    msgs = LazyDocMessage.objects.filter(session=session).order_by('created_at', 'id')[:200]
    data = _serialize_session(session)
    data['docHtml'] = session.doc_html or ''
    data['messages'] = [_serialize_message(m) for m in msgs]
    unlimited, remaining, allowance = _canvas_credit_state(user)
    data['credits'] = {'unlimited': unlimited, 'remaining': remaining, 'allowance': allowance}
    return JsonResponse(data)


@require_POST
def ajax_lazy_session_delete(request, session_id):
    user, session, err = _owned(request, session_id)
    if err:
        return err
    session.delete()
    return JsonResponse({'ok': True})


@require_POST
def ajax_lazy_doc_save(request, session_id):
    user, session, err = _owned(request, session_id)
    if err:
        return err
    if _rate_limit(request, 'lazy_doc_save', 90, 60):
        return JsonResponse({'error': 'Too many saves'}, status=429)
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        payload = {}
    html = str(payload.get('html') or '')[:120000]
    title = str(payload.get('title') or '')[:200]
    session.doc_html = fix_html(html) if html else ''
    if title:
        session.doc_title = title[:200]
    session.updated_at = now_ms()
    session.save(update_fields=['doc_html', 'doc_title', 'updated_at'])
    return JsonResponse({'ok': True, 'docTitle': session.doc_title})


@require_GET
def ajax_lazy_export(request, session_id):
    user, session, err = _owned(request, session_id)
    if err:
        return err
    fmt = (request.GET.get('format') or 'docx').lower()
    if fmt not in ('docx', 'pdf', 'html'):
        fmt = 'docx'
    html = session.doc_html
    if not html:
        return JsonResponse({'error': 'Document is empty'}, status=400)
    title = session.doc_title or session.title or 'document'
    safe = ''.join(ch if ch.isalnum() or ch in '-_' else '-' for ch in title)[:64].strip('-') or 'document'
    if fmt == 'html':
        resp = HttpResponse(html, content_type='text/html; charset=utf-8')
        resp['Content-Disposition'] = f'attachment; filename="{safe}.html"'
        return resp
    if fmt == 'docx':
        return export_docx(html, title, safe)
    return export_pdf(html, title, safe)


@require_POST
def ajax_lazy_upload(request):
    user, err = _require_user(request)
    if err:
        return err
    if _rate_limit(request, 'lazy_upload', 12, 60):
        return JsonResponse({'error': 'Upload cooling down'}, status=429)
    f = request.FILES.get('file')
    if f is None:
        return JsonResponse({'error': 'File required'}, status=400)
    name = (getattr(f, 'name', '') or '').lower()
    ext = os.path.splitext(name)[1]
    if ext not in ('.docx', '.pdf', '.txt'):
        return JsonResponse({'error': 'Supported: .docx, .pdf, .txt'}, status=400)
    if getattr(f, 'size', 0) > MAX_UPLOAD:
        return JsonResponse({'error': 'Max 8 MB'}, status=413)
    data = f.read(MAX_UPLOAD + 1)
    if len(data) > MAX_UPLOAD:
        return JsonResponse({'error': 'Max 8 MB'}, status=413)
    display_name = os.path.splitext(getattr(f, 'name', 'file'))[0][:80]
    try:
        if ext == '.docx':
            text, t = extract_docx(data)
        elif ext == '.txt':
            t = ''
            text = data.decode('utf-8', errors='replace')
        else:
            text, t = extract_pdf_text(data)
    except Exception as exc:
        return JsonResponse({'error': f'Could not read file: {exc}'}, status=400)
    if not (text or '').strip():
        return JsonResponse({'error': 'No readable text found'}, status=400)
    excerpt = ' '.join(text.split())[:16000]
    out = {'name': display_name, 'text': excerpt, 'chars': len(excerpt), 'suggestedTitle': (t or display_name)[:120]}
    if ext == '.txt' and text.strip():
        out['asDocumentHtml'] = text_to_html(text)[:60000]
    return JsonResponse(out)


@require_POST
def ajax_lazy_chat(request, session_id):
    user, session, err = _owned(request, session_id)
    if err:
        return err
    if _rate_limit(request, 'lazy_chat', 12, 60):
        return JsonResponse({'error': 'Lazy is cooling down — try again shortly.'}, status=429)
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        payload = {}
    text = str(payload.get('text') or '').strip()[:4000]
    if not text:
        return JsonResponse({'error': 'Message required'}, status=400)
    attachments = payload.get('attachments') if isinstance(payload.get('attachments'), list) else []
    clean_atts = []
    for a in attachments[:3]:
        if isinstance(a, dict) and a.get('name'):
            clean_atts.append({'name': str(a['name'])[:80], 'text': str(a.get('text') or '')[:16000]})
    ok, _, _ = _spend_canvas_credit(user)
    if not ok:
        return JsonResponse({'error': "You're out of Neby credits — top up on the Credits page.", 'need_credits': True}, status=402)

    now = now_ms()
    att_meta = {'attachments': [{'name': a['name']} for a in clean_atts]}
    if clean_atts:
        att_meta['attachmentText'] = "\n\n".join(f"[{a['name']}]\n{a['text']}" for a in clean_atts)[:30000]
    user_msg = LazyDocMessage.objects.create(
        id=uuid_str(), session=session, role='user', content=text,
        meta=json.dumps(att_meta, ensure_ascii=False), created_at=now,
    )
    if session.title in ('', 'New chat'):
        session.title = text.strip()[:48] or 'New chat'
    session.message_count = LazyDocMessage.objects.filter(session=session).count()
    session.updated_at = now
    session.save(update_fields=['title', 'message_count', 'updated_at'])
    new_title = session.title

    def event_stream():
        yield f"data: {json.dumps({'type': 'user', 'id': str(user_msg.id), 'title': new_title}, ensure_ascii=False)}\n\n"
        box = {}
        try:
            for frame in lazy_agent.stream_turn(session, user, text, box):
                yield f"data: {json.dumps(frame, ensure_ascii=False)}\n\n"
            turn = box.get('turn')
            if turn is None:
                raise RuntimeError('agent produced no result')
            assistant = lazy_agent.persist_turn(session, turn)
            unlimited2, remaining2, allowance = _canvas_credit_state(user)
            done = {
                'type': 'done', 'id': str(assistant.id), 'content': assistant.content,
                'tools': turn['tools'], 'docUpdated': turn['doc_updated'],
                'credits': {'unlimited': unlimited2, 'remaining': remaining2, 'allowance': allowance},
            }
            yield f"data: {json.dumps(done, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'type': 'error', 'message': str(exc)[:300]}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    resp = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    resp['Cache-Control'] = 'no-cache'
    resp['X-Accel-Buffering'] = 'no'
    return resp
