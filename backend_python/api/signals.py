"""Private first-party signals: which kind of device an account or an
interaction came from.

Design goals (docs/ANALYTICS.md, "Private signals"):

* Internal only. No API serializer, template or export reads `ActorSignal`
  except the staff-guarded admin analytics code in `nebians.analytics.report`.
* Not reversible. No user id, IP address or raw user agent is stored. The
  `actor` column is an HMAC of the user id under a key derived from
  SECRET_KEY, so rows cannot be turned back into accounts by anyone holding
  only the database. Staff go the other way (user -> tag) when they need to.
* Coarse in the clear (device class, OS family, browser, app version, so the
  report can aggregate in SQL) and precise only inside `detail`, which is
  AES-GCM ciphertext (model, OS version, screen, language, timezone).
* Never in the way: every write is best effort, after commit, and swallows
  its own errors.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import threading
import time

from django.conf import settings
from django.db import transaction

_local = threading.local()
_AD = b'nebians-actor-signal-v1'
_KV_RE = re.compile(r'\s*;\s*')
_CLEAN_RE = re.compile(r'[^A-Za-z0-9 ._+\-/:,()]')


# --------------------------------------------------------------------------
# Keys, tags, encryption
# --------------------------------------------------------------------------

def _key(domain: str) -> bytes:
    return hashlib.sha256(f'{settings.SECRET_KEY}|sig|{domain}'.encode('utf-8')).digest()


def _tag(domain: str, value: str) -> str:
    mac = hmac.new(_key(domain), str(value).encode('utf-8', 'ignore'), hashlib.sha256).hexdigest()
    return mac[:20]


def actor_tag(user_id) -> str:
    """Keyed, one-way tag of an account. Stable, so a user's events line up."""
    return 'x' + _tag('actor', str(user_id))


def viewer_tag(user_id=None, *, day: str = '', ip: str = '', user_agent: str = '') -> str:
    """Viewer id for post reach. Members are stable; guests rotate daily."""
    if user_id:
        return 'v' + _tag('viewer', str(user_id))
    return 'g' + _tag('guest', f'{day}|{ip}|{user_agent}')


def seal(payload: dict) -> str:
    from Crypto.Cipher import AES
    raw = json.dumps(payload, separators=(',', ':'), ensure_ascii=True).encode('utf-8')
    cipher = AES.new(_key('detail'), AES.MODE_GCM)
    cipher.update(_AD)
    ct, tag = cipher.encrypt_and_digest(raw)
    return base64.urlsafe_b64encode(cipher.nonce + tag + ct).decode('ascii')


def unseal(blob: str) -> dict:
    if not blob:
        return {}
    try:
        from Crypto.Cipher import AES
        data = base64.urlsafe_b64decode(blob.encode('ascii'))
        nonce, tag, ct = data[:16], data[16:32], data[32:]
        cipher = AES.new(_key('detail'), AES.MODE_GCM, nonce=nonce)
        cipher.update(_AD)
        return json.loads(cipher.decrypt_and_verify(ct, tag).decode('utf-8'))
    except Exception:
        return {}


# --------------------------------------------------------------------------
# Reading the client
# --------------------------------------------------------------------------

def _clean(value, n: int) -> str:
    return _CLEAN_RE.sub('', str(value or ''))[:n].strip()


def parse_app_header(raw: str) -> dict:
    """`X-Neb-Device: v=1;app=1.4.0;build=52;os=Android 14;sdk=34;model=Pixel 7;...`"""
    out = {}
    for part in _KV_RE.split(raw or ''):
        if '=' not in part:
            continue
        k, v = part.split('=', 1)
        k = k.strip().lower()[:12]
        if k:
            out[k] = _clean(v, 48)
    return out


def _ua_versions(ua: str) -> dict:
    out = {}
    m = re.search(r'(?:Chrome|CriOS|Firefox|FxiOS|Edg|EdgA|OPR)/(\d+)', ua or '')
    if m:
        out['browser_ver'] = m.group(1)
    m = re.search(r'Android (\d+(?:\.\d+)?)', ua or '') or re.search(r'OS (\d+)[_\d]* like Mac', ua or '') \
        or re.search(r'Windows NT (\d+\.\d+)', ua or '') or re.search(r'Mac OS X (\d+[_\d]*)', ua or '')
    if m:
        out['os_ver'] = m.group(1).replace('_', '.')
    m = re.search(r';\s*([^;)]{2,40})\s+Build/', ua or '')
    if m:
        out['model'] = _clean(m.group(1), 40)
    return out


def describe(request) -> dict:
    """Coarse columns plus a private detail dict for one request."""
    from nebians.analytics import events, rules

    meta = request.META
    ua = meta.get('HTTP_USER_AGENT', '') or ''
    hdr = parse_app_header(meta.get('HTTP_X_NEB_DEVICE', ''))
    app_platform = (meta.get('HTTP_X_APP_PLATFORM') or hdr.get('platform') or '').lower()
    is_app = bool(hdr or app_platform or meta.get('HTTP_X_APP_VERSION'))
    if not is_app and (meta.get('HTTP_AUTHORIZATION', '') or '').startswith('Bearer '):
        is_app = True
    country, _city = events._geo_from_headers(meta)
    lang = _clean((meta.get('HTTP_ACCEPT_LANGUAGE', '') or '').split(',')[0], 12)

    if hdr:
        os_name = (hdr.get('os') or '').split(' ')[0].lower() or app_platform or 'android'
        os_family = 'ios' if os_name.startswith('ios') else ('android' if os_name.startswith('andr') else os_name[:16])
        tablet = hdr.get('tablet') in ('1', 'true')
        device_class = 'tablet' if tablet else 'mobile'
        browser = 'NEBians app'
        app_version = _clean(hdr.get('app') or meta.get('HTTP_X_APP_VERSION', ''), 16)
        detail = {k: hdr[k] for k in ('model', 'brand', 'os', 'sdk', 'screen', 'dpi', 'build', 'lang', 'tz', 'abi')
                  if hdr.get(k)}
    else:
        os_family = rules.detect_platform(ua) or (app_platform if app_platform in ('android', 'ios') else '')
        device_class = rules.device_class(ua)
        browser = 'NEBians app' if is_app else rules.browser_name(ua)
        app_version = _clean(meta.get('HTTP_X_APP_VERSION', ''), 16)
        detail = _ua_versions(ua)
    if lang and 'lang' not in detail:
        detail['lang'] = lang
    return {
        'source': 'app' if is_app else 'web',
        'device_class': device_class if device_class in ('mobile', 'tablet', 'desktop') else 'other',
        'os_family': os_family[:16],
        'browser': browser[:24],
        'app_version': app_version,
        'country': country[:60],
        'detail': detail,
        'ip': events.client_ip(request),
        'ua': ua,
    }


# --------------------------------------------------------------------------
# Recording
# --------------------------------------------------------------------------

def record(kind: str, request, user_id, *, ref: str = '', ref2: str = '') -> None:
    """Store one signal after the surrounding transaction commits."""
    if not request or not user_id:
        return
    try:
        info = describe(request)
    except Exception:
        return
    now = int(time.time() * 1000)
    actor = actor_tag(user_id)

    def _write():
        try:
            from .models import ActorSignal
            ActorSignal.objects.create(
                kind=kind, actor=actor, ref=str(ref or '')[:36], ref2=str(ref2 or '')[:36],
                source=info['source'], device_class=info['device_class'], os_family=info['os_family'],
                browser=info['browser'], app_version=info['app_version'], country=info['country'],
                detail=seal(info['detail']) if info['detail'] else '', created_at=now,
            )
        except Exception:
            pass

    try:
        transaction.on_commit(_write)
    except Exception:
        _write()


def current_request():
    return getattr(_local, 'request', None)


class SignalContextMiddleware:
    """Makes the current request reachable from model signal handlers."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.request = request
        try:
            return self.get_response(request)
        finally:
            _local.request = None


# --------------------------------------------------------------------------
# Model hooks (registered in ApiConfig.ready)
# --------------------------------------------------------------------------

def _post_of_poll(poll) -> str:
    if poll.post_id:
        return poll.post_id
    if poll.reply_id:
        from .models import Reply
        return Reply.objects.filter(pk=poll.reply_id).values_list('post_id', flat=True).first() or ''
    return ''


def register_hooks() -> None:
    from django.db.models.signals import post_save
    from .models import User, Post, Reply, PollVote, PollOption, PostLike, ReplyLike

    def on_user(sender, instance, created, **kw):
        if created:
            record('signup', current_request(), instance.pk)

    def on_post(sender, instance, created, **kw):
        if created:
            record('post', current_request(), instance.user_id, ref=instance.pk)

    def on_reply(sender, instance, created, **kw):
        if created:
            record('reply', current_request(), instance.user_id, ref=instance.post_id, ref2=instance.pk)

    def on_vote(sender, instance, created, **kw):
        if created:
            record('vote', current_request(), instance.user_id,
                   ref=_post_of_poll(instance.poll), ref2=instance.option_id)

    def on_option(sender, instance, created, **kw):
        if created and instance.added_by_id:
            record('option', current_request(), instance.added_by_id,
                   ref=_post_of_poll(instance.poll), ref2=instance.pk)

    def on_post_like(sender, instance, created, **kw):
        if created:
            record('like', current_request(), instance.user_id, ref=instance.post_id)

    def on_reply_like(sender, instance, created, **kw):
        if created:
            pid = Reply.objects.filter(pk=instance.reply_id).values_list('post_id', flat=True).first() or ''
            record('like', current_request(), instance.user_id, ref=pid, ref2=instance.reply_id)

    for model, fn in ((User, on_user), (Post, on_post), (Reply, on_reply), (PollVote, on_vote),
                      (PollOption, on_option), (PostLike, on_post_like), (ReplyLike, on_reply_like)):
        post_save.connect(fn, sender=model, weak=False, dispatch_uid=f'actor-signal-{model.__name__}')
