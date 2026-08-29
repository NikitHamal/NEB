import json
import logging

from django.core.signing import TimestampSigner
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from api import code_realtime as rt
from api.llm.credentials import catalog_for_user
from api.models import CodeMessage, CodeSession, User

from .view_helpers import _avatar_url, _ctx, _get_ws_public_url, api

logger = logging.getLogger(__name__)

MAX_NAME_LEN = 120
MAX_MESSAGE_LEN = 48000
READ_CAP = 500000
WRITE_CAP = 2_000_000
CODE_TICKET_SALT = 'code-daemon'
CODE_TICKET_MAX_AGE = 60 * 60 * 24 * 30
VALID_EFFORTS = {'quick', 'balanced', 'deep', 'max'}
VALID_MODES = {'agent', 'ask', 'plan'}


def _is_admin_user(user, request=None) -> bool:
    if not user:
        return False
    if getattr(user, 'is_admin', False) or getattr(user, 'is_staff', False):
        return True
    if hasattr(user, 'moderator_level') and getattr(user, 'moderator_level', 0) >= 3 and not getattr(user, 'is_locked', False):
        return True
    if request and getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False) and (getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False) or getattr(request.user, 'is_admin', False)):
        return True
    return False


def _current_user(request):
    token = api.get_session_token(request)
    session_user = api.get_session_user(request) if token else None
    if session_user:
        try:
            return User.objects.get(pk=session_user.get('id')), session_user
        except User.DoesNotExist:
            pass
    if getattr(request, 'user', None) and request.user.is_authenticated:
        try:
            user = User.objects.filter(pk=request.user.pk).first() or User.objects.filter(username=request.user.username).first()
            if user:
                return user, {'id': str(user.id), 'username': user.username, 'is_admin': getattr(user, 'is_admin', False) or getattr(user, 'is_staff', False)}
        except Exception:
            pass
    return None, None


def _require_admin(request):
    user, session_user = _current_user(request)
    if not user:
        return None, JsonResponse({'error': 'Please log in again.'}, status=401)
    if not _is_admin_user(user, request):
        return None, JsonResponse({'error': 'Access restricted to administrators.'}, status=403)
    return user, None


def _session_owned(user, session_id):
    if not session_id:
        return None
    try:
        session = CodeSession.objects.get(pk=session_id)
    except CodeSession.DoesNotExist:
        return None
    return session if str(session.user_id) == str(user.id) else None


def _serialize_session(session):
    return {
        'id': session.id,
        'name': session.name,
        'provider': session.provider,
        'provider_id': getattr(session, 'provider_id', ''),
        'model': session.model,
        'effort': session.effort,
        'mode': getattr(session, 'mode', 'agent') or 'agent',
        'status': session.status,
        'error': session.error[:800],
        'workspace_label': session.workspace_label,
        'created_at': session.created_at,
        'updated_at': session.updated_at,
    }


def _serialize_message(message):
    return {
        'id': message.pk,
        'role': message.role,
        'content': message.content,
        'meta': message.meta or {},
        'created_at': message.created_at,
    }


DISALLOWED_MODEL_SUBSTRINGS = (
    'tts', 'whisper', 'audio', 'speech', 'voice',
    'flux', 'stable-diffusion', 'sdxl', 'dall-e', 'midjourney',
    'embedding', 'embed', 'realtime', 'moderation',
)


def _is_valid_code_model(model_id: str, label: str) -> bool:
    low = (str(model_id or '') + ' ' + str(label or '')).lower()
    return not any(sub in low for sub in DISALLOWED_MODEL_SUBSTRINGS)


PROVIDER_EFFORT_LEVELS = {
    'tryingopen': ['quick', 'balanced', 'deep'],
    'inception': ['low', 'medium', 'high'],
}


def _code_model_catalog(user):
    raw = catalog_for_user(user)
    groups = []
    for section in ('official', 'community'):
        for provider in raw.get(section) or []:
            available = bool(provider.get('available'))
            if not available:
                continue
            selectable = section == 'official' or provider.get('selectableForAgent', True)
            effort_levels = PROVIDER_EFFORT_LEVELS.get(provider.get('slug'), [])
            models = []
            for model in provider.get('models') or []:
                m_id = model.get('id') or ''
                m_label = model.get('label') or m_id
                if not _is_valid_code_model(m_id, m_label):
                    continue
                cw = model.get('context_window') or provider.get('contextWindow') or 131072
                models.append({
                    'value': f'{provider["slug"]}||{m_id}',
                    'provider': provider['slug'],
                    'provider_id': '',
                    'model': m_id,
                    'label': m_label,
                    'note': model.get('note') or provider.get('freeNote') or '',
                    'available': bool(selectable),
                    'context_window': int(cw),
                    'official': bool(provider.get('official')),
                    'effort_levels': list(effort_levels) if selectable else [],
                })
            if models:
                groups.append({
                    'provider': provider['slug'],
                    'title': provider.get('label') or provider['slug'],
                    'available': bool(selectable),
                    'effort_levels': list(effort_levels) if selectable else [],
                    'models': models,
                })
    for provider in raw.get('custom') or []:
        models = []
        custom_id = str(provider.get('id') or '')
        for model in provider.get('models') or []:
            m_id = model.get('id') or ''
            m_label = model.get('label') or m_id
            if not _is_valid_code_model(m_id, m_label):
                continue
            cw = model.get('context_window') or provider.get('contextWindow') or 131072
            models.append({
                'value': f'custom|{custom_id}|{m_id}',
                'provider': 'custom',
                'provider_id': custom_id,
                'model': m_id,
                'label': m_label or 'Custom model',
                'note': provider.get('label') or 'Custom provider',
                'available': bool(provider.get('available')),
                'context_window': int(cw),
                'official': True,
            })
        if models:
            groups.append({
                'provider': 'custom',
                'title': provider.get('label') or 'Custom provider',
                'available': bool(provider.get('available')),
                'models': models,
            })
    default = raw.get('defaultSelection') or {}
    return {
        'groups': groups,
        'default': {
            'provider': default.get('slug') or 'tryingopen',
            'provider_id': '',
            'model': default.get('model') or '',
        },
    }


def code_home(request, session_id=None):
    user, _ = _current_user(request)
    if not user:
        next_url = f"/code/{session_id}/" if session_id else "/code/"
        return redirect('%s?next=%s' % (reverse('web:login'), next_url))
    if not _is_admin_user(user, request):
        return HttpResponseForbidden("Access restricted to administrators.")
    sessions = list(CodeSession.objects.filter(user_id=str(user.id))[:80])
    presence = rt.get_presence(str(user.id))
    catalog = _code_model_catalog(user)
    safe_presence = {k: v for k, v in (presence or {}).items() if k != '_ch'}
    ctx = _ctx(
        request,
        code_sessions=[_serialize_session(s) for s in sessions],
        daemon_online=bool(presence),
        daemon_info=safe_presence,
        avatar_url=_avatar_url(user),
        code_sessions_json=json.dumps([_serialize_session(s) for s in sessions]),
        daemon_info_json=json.dumps(safe_presence),
        code_models_json=json.dumps(catalog),
    )
    ctx['page_title'] = 'Neby Code'
    ctx['initial_session_id'] = str(session_id or request.GET.get('session') or '')
    return render(request, 'web/code.html', ctx)


@require_POST
def ajax_code_create_session(request):
    user, err = _require_admin(request)
    if err:
        return err
    data = _body(request)
    now = rt.now_ms()
    workspace_label = str(data.get('workspace_label') or '').strip()[:300]
    if not workspace_label:
        presence = rt.get_presence(str(user.id)) or {}
        workspace_label = presence.get('workspace_label') or presence.get('cwd') or 'Default Workspace'
    session = CodeSession.objects.create(
        user_id=str(user.id),
        name=str(data.get('name') or '').strip()[:MAX_NAME_LEN] or 'New session',
        provider=str(data.get('provider') or '').strip().lower()[:40],
        provider_id=str(data.get('provider_id') or '').strip()[:40],
        model=str(data.get('model') or '').strip()[:200],
        effort=_effort(data.get('effort')),
        mode=_mode(data.get('mode')),
        workspace_label=workspace_label,
        created_at=now,
        updated_at=now,
    )
    return JsonResponse({'session': _serialize_session(session)})


@require_GET
def ajax_code_sessions(request):
    user, err = _require_admin(request)
    if err:
        return err
    sessions = CodeSession.objects.filter(user_id=str(user.id))[:80]
    presence = rt.get_presence(str(user.id))
    return JsonResponse({
        'sessions': [_serialize_session(s) for s in sessions],
        'daemon_online': bool(presence),
        'daemon_info': {k: v for k, v in (presence or {}).items() if k != '_ch'},
    })


@require_GET
def ajax_code_session_detail(request, session_id):
    user, err = _require_admin(request)
    if err:
        return err
    session = _session_owned(user, session_id)
    if not session:
        return JsonResponse({'error': 'Not found'}, status=404)
    after = _safe_int(request.GET.get('after'), 0)
    messages = CodeMessage.objects.filter(session=session)
    if after:
        messages = messages.filter(id__gt=after)
    messages = messages[:1200]
    return JsonResponse({
        'session': _serialize_session(session),
        'messages': [_serialize_message(m) for m in messages],
    })


@require_POST
def ajax_code_update_session(request, session_id):
    user, err = _require_admin(request)
    if err:
        return err
    session = _session_owned(user, session_id)
    if not session:
        return JsonResponse({'error': 'Not found'}, status=404)
    data = _body(request)
    fields = []
    if 'name' in data:
        session.name = str(data.get('name') or '').strip()[:MAX_NAME_LEN] or 'New session'
        fields.append('name')
    if 'provider' in data:
        session.provider = str(data.get('provider') or '').strip().lower()[:40]
        fields.append('provider')
    if 'provider_id' in data:
        session.provider_id = str(data.get('provider_id') or '').strip()[:40]
        fields.append('provider_id')
    if 'model' in data:
        session.model = str(data.get('model') or '').strip()[:200]
        fields.append('model')
    if 'effort' in data:
        session.effort = _effort(data.get('effort'))
        fields.append('effort')
    if 'mode' in data:
        session.mode = _mode(data.get('mode'))
        fields.append('mode')
    if 'workspace_label' in data:
        session.workspace_label = str(data.get('workspace_label') or '').strip()[:300]
        fields.append('workspace_label')
    if fields:
        session.updated_at = rt.now_ms()
        fields.append('updated_at')
        session.save(update_fields=fields)
    return JsonResponse({'session': _serialize_session(session)})


@require_POST
def ajax_code_send(request, session_id):
    user, err = _require_admin(request)
    if err:
        return err
    session = _session_owned(user, session_id)
    if not session:
        return JsonResponse({'error': 'Not found'}, status=404)
    if session.status in ('queued', 'running'):
        return JsonResponse({'error': 'Agent is already working on this session'}, status=409)
    if not rt.get_presence(str(user.id)):
        return JsonResponse({
            'error': 'Local machine is offline. Connect the Neby Code daemon first.',
            'code': 'daemon_offline',
        }, status=409)
    data = _body(request)
    content = str(data.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'Message is empty'}, status=400)
    if len(content) > MAX_MESSAGE_LEN:
        return JsonResponse({'error': 'Message is too long'}, status=413)
    session.provider = str(data.get('provider') or session.provider or '').strip().lower()[:40]
    session.provider_id = str(data.get('provider_id') or session.provider_id or '').strip()[:40]
    session.model = str(data.get('model') or session.model or '').strip()[:200]
    session.effort = _effort(data.get('effort') or session.effort)
    session.mode = _mode(data.get('mode') or session.mode)
    now = rt.now_ms()
    session.status = 'queued'
    session.error = ''
    session.cancel_flag = False
    session.updated_at = now
    session.save()
    message = CodeMessage.objects.create(session=session, role='user', content=content, created_at=now)
    rt.push_ui(session.id, 'user_enqueued', {'message_id': message.pk})
    return JsonResponse({'ok': True, 'message': _serialize_message(message), 'session': _serialize_session(session)})


@require_POST
def ajax_code_cancel(request, session_id):
    user, err = _require_admin(request)
    if err:
        return err
    session = _session_owned(user, session_id)
    if not session:
        return JsonResponse({'error': 'Not found'}, status=404)
    session.cancel_flag = True
    if session.status == 'queued':
        session.status = 'idle'
        session.save(update_fields=['cancel_flag', 'status'])
    else:
        session.save(update_fields=['cancel_flag'])
    return JsonResponse({'ok': True})


@require_POST
def ajax_code_delete_session(request, session_id):
    user, err = _require_admin(request)
    if err:
        return err
    session = _session_owned(user, session_id)
    if not session:
        return JsonResponse({'error': 'Not found'}, status=404)
    session.delete()
    return JsonResponse({'ok': True})


@require_GET
def ajax_code_status(request):
    user, err = _require_admin(request)
    if err:
        return err
    presence = rt.get_presence(str(user.id))
    return JsonResponse({
        'daemon_online': bool(presence),
        'info': {k: v for k, v in (presence or {}).items() if k != '_ch'},
    })


@require_GET
def ajax_code_token(request):
    user, err = _require_admin(request)
    if err:
        return err
    ticket = TimestampSigner(salt=CODE_TICKET_SALT).sign(str(user.id))
    ws_url = _get_ws_public_url() or ''
    command = f'python -m neby_code --workspace . --ws-url "{ws_url}" --ticket "{ticket}"' if ws_url else ''
    return JsonResponse({
        'ticket': ticket,
        'expires_in': CODE_TICKET_MAX_AGE,
        'ws_url': ws_url,
        'command': command,
    })


@require_POST
def ajax_code_fs(request):
    user, err = _require_admin(request)
    if err:
        return err
    data = _body(request)
    op = str(data.get('op') or '').strip().lower()
    actions = {
        'list': ('fs.list', 30), 'read': ('fs.read', 30), 'write': ('fs.write', 60),
        'tree': ('fs.tree', 45), 'mkdir': ('fs.mkdir', 30), 'delete': ('fs.delete', 45),
        'move': ('fs.move', 45), 'search': ('fs.search', 60), 'find': ('fs.find', 45),
        'info': ('fs.info', 20), 'edit': ('fs.edit', 60), 'patch': ('fs.patch', 90),
    }
    if op not in actions:
        return JsonResponse({'error': 'Unknown file operation'}, status=400)
    args = {k: v for k, v in data.items() if k not in ('op',) and v is not None}
    if op in ('write', 'edit'):
        largest = max(len(str(args.get(k) or '')) for k in ('content', 'old_text', 'new_text'))
        if largest > WRITE_CAP:
            return JsonResponse({'error': 'File edit is too large for the web IDE'}, status=413)
    action, timeout = actions[op]
    return _daemon_json(user, action, args, timeout)


@require_POST
def ajax_code_git(request):
    user, err = _require_admin(request)
    if err:
        return err
    data = _body(request)
    op = str(data.get('op') or 'status').strip().lower()
    actions = {'status': ('git.status', 30), 'diff': ('git.diff', 45), 'log': ('git.log', 30)}
    if op not in actions:
        return JsonResponse({'error': 'Unknown git operation'}, status=400)
    action, timeout = actions[op]
    args = {k: v for k, v in data.items() if k != 'op' and v is not None}
    return _daemon_json(user, action, args, timeout)


@require_POST
def ajax_code_term(request):
    user, err = _require_admin(request)
    if err:
        return err
    data = _body(request)
    session_id = str(data.get('session_id') or '')
    command = str(data.get('command') or '').strip()
    if not command or len(command) > 8000:
        return JsonResponse({'error': 'Invalid command'}, status=400)
    session = _session_owned(user, session_id) if session_id else None
    if session_id and not session:
        return JsonResponse({'error': 'Not found'}, status=404)
    timeout_sec = max(1, min(_safe_int(data.get('timeout_sec'), 900), 3600))
    result = rt.call_daemon(
        str(user.id), 'term.run',
        {'command': command, 'timeout_sec': timeout_sec, 'detached': True},
        timeout=15, session_id=session_id,
    )
    if not result.get('ok'):
        return _daemon_error(result)
    return JsonResponse({'data': result.get('data'), 'streamed': True})


def _daemon_json(user, action, args, timeout):
    try:
        result = rt.call_daemon(str(user.id), action, args, timeout=timeout)
    except Exception as exc:
        logger.exception('Neby Code daemon call failed: %s', exc)
        return JsonResponse({'error': 'Local daemon call failed'}, status=500)
    if not result.get('ok'):
        return _daemon_error(result)
    out = result.get('data')
    if isinstance(out, dict) and isinstance(out.get('content'), str):
        out['content'] = out['content'][:READ_CAP]
    return JsonResponse({'data': out})


def _daemon_error(result):
    error = result.get('error') or 'daemon_offline'
    offline = error in ('daemon_timeout', 'dispatch_failed', 'daemon_offline')
    friendly = 'Local machine is offline. Connect the Neby Code daemon first.' if offline else error
    return JsonResponse({'error': friendly, 'code': error, 'data': result.get('data')}, status=503 if offline else 400)


def _effort(value):
    value = str(value or 'balanced').strip().lower()
    return value if value in VALID_EFFORTS else 'balanced'


def _mode(value):
    value = str(value or 'agent').strip().lower()
    return value if value in VALID_MODES else 'agent'


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _body(request):
    try:
        data = json.loads(request.body or b'{}')
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}
