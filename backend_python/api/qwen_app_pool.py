"""Keyless Qwen accounts for the Android app gateway of chat.qwen.ai.

The web door (guest, Baxia captcha) is blocked for every server IP. The app
door (`X-Platform: android`, `source: app`, static `app_waf`) is not, but it
needs an account. Accounts are made over plain HTTPS in about 8 s: a
throw-away mailbox (0mail.tech), signup, the activation link, sign in. Nothing
touches the database; the pool is one small JSON file next to the code, shared
by every worker through a file lock.
"""
import base64
import fcntl
import hashlib
import json
import logging
import os
import random
import re
import string
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

BASE = 'https://chat.qwen.ai/api/v2'
MAIL = 'https://api.0mail.tech/v1'
UA = ('Dalvik/2.1.0 (Linux; U; Android 15; 25028RN03A Build/AP3A.240905.015.A2) AliApp(QWENCHAT/2.5.1) '
      'AppType/Release AplusBridgeLite,Dalvik/2.1.0 (Linux; U; Android 15; 25028RN03A Build/AP3A.240905.015.A2)')
APP_WAF = os.environ.get('QWEN_APP_WAF') or 'Z9Tr56YmQpXcO2K_d_3nAbJvRqMLFW8HTNjvRguWHEowM1xY'
TARGET = 3            # usable accounts kept warm
MAX_POOL = 8
_BAD_MAIL = {'cfdevelopment.online'}   # Qwen silently drops mail to these


def headers(token=None, device='', **extra):
    h = {'User-Agent': UA, 'Connection': 'Keep-Alive', 'Accept': 'application/json', 'X-Platform': 'android',
         'source': 'app', 'Accept-Language': 'en-US', 'Cache-Control': 'no-store', 'app_waf': APP_WAF,
         'x-request-id': str(uuid.uuid4()),
         'x-device-id': device or 'ai' + hashlib.md5(uuid.uuid4().bytes).hexdigest()}
    h.update(extra)
    if token:
        h['Authorization'] = 'Bearer ' + token
    return h


def _path():
    explicit = os.environ.get('QWEN_POOL_FILE')
    for p in ([Path(explicit)] if explicit else []) + [Path(__file__).resolve().parent.parent / '.qwen_pool.json',
                                                       Path(tempfile.gettempdir()) / 'neb_qwen_pool.json']:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists() or os.access(p.parent, os.W_OK):
                return p
        except OSError:
            continue
    return Path(tempfile.gettempdir()) / 'neb_qwen_pool.json'


@contextmanager
def _flock(name, blocking=True):
    fh = open(str(_path()) + '.' + name, 'a+')
    try:
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        except OSError:
            yield False
            return
        yield True
    finally:
        try:
            fcntl.flock(fh, fcntl.LOCK_UN)
        finally:
            fh.close()


def load():
    try:
        data = json.loads(_path().read_text('utf-8'))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save(items):
    p = _path()
    tmp = p.with_suffix('.tmp%d' % os.getpid())
    tmp.write_text(json.dumps(items), 'utf-8')
    os.replace(tmp, p)


def _update(fn):
    with _flock('state'):
        items = load()
        out = fn(items)
        _save(items)
        return out


def jwt_exp(token):
    try:
        body = token.split('.')[1]
        return json.loads(base64.urlsafe_b64decode(body + '=' * (-len(body) % 4))).get('exp', 0)
    except Exception:
        return 0


def usable(a, exclude=()):
    now = time.time()
    return (a.get('token') and a['email'] not in exclude and a.get('cool_until', 0) <= now
            and jwt_exp(a['token']) > now + 86400)


def cool(email, seconds):
    def fn(items):
        for a in items:
            if a['email'] == email:
                a['cool_until'] = time.time() + seconds
    _update(fn)


def drop(email):
    def fn(items):
        items[:] = [a for a in items if a['email'] != email]
    _update(fn)


def _mail_inbox(sess):
    h = {'X-Session-Id': sess}
    domains = requests.get(MAIL + '/domains', headers=h, timeout=15).json()
    ok = [d['domain'] for d in domains if d.get('available') and not d.get('premium') and d['domain'] not in _BAD_MAIL]
    if not ok:
        raise RuntimeError('temporary mail has no open domain')
    r = requests.post(MAIL + '/inboxes', json={'domain': random.choice(ok)}, headers=h, timeout=15)
    r.raise_for_status()
    return r.json()


def _signin(email, password, device):
    r = requests.post(BASE + '/auths/signin', json={'email': email, 'password': hashlib.sha256(password.encode()).hexdigest()},
                      headers=headers(device=device), timeout=30)
    j = r.json()
    if not j.get('success'):
        raise RuntimeError('Qwen sign in refused: %s' % str(j.get('data'))[:160])
    return j['data']['token']


def provision():
    """Create, activate and sign in one account. Returns the account dict."""
    sess, device = str(uuid.uuid4()), 'ai' + hashlib.md5(uuid.uuid4().bytes).hexdigest()
    inbox = _mail_inbox(sess)
    email = inbox['address']
    password = 'Aa1!' + ''.join(random.choices(string.ascii_letters + string.digits, k=14))
    r = requests.post(BASE + '/auths/signup', json={
        'email': email, 'password': hashlib.sha256(password.encode()).hexdigest(), 'name': 'Neb ' + email[:5]},
        headers=headers(device=device), timeout=30)
    j = r.json()
    if not j.get('success'):
        raise RuntimeError('Qwen signup refused: %s' % str(j.get('data') or r.text)[:160])
    link = None
    for _ in range(30):
        time.sleep(1.2)
        try:
            msgs = requests.get('%s/inboxes/%s/messages' % (MAIL, inbox['id']), headers={'X-Session-Id': sess}, timeout=15).json()
        except Exception:
            continue
        for m in msgs if isinstance(msgs, list) else []:
            hit = re.search(r'https?://[^"\'<>\s]*auths/activate[^"\'<>\s]*', m.get('body') or '')
            if hit:
                link = hit.group(0).replace('&amp;', '&')
                break
        if link:
            break
    if not link:
        raise RuntimeError('Qwen activation mail never arrived')
    requests.get(link, headers=headers(device=device), allow_redirects=False, timeout=30)
    token = _signin(email, password, device)
    try:
        requests.delete('%s/inboxes/%s' % (MAIL, inbox['id']), headers={'X-Session-Id': sess}, timeout=8)
    except Exception:
        pass
    logger.info('Qwen app account ready: %s', email)
    return {'email': email, 'password': password, 'device': device, 'token': token, 'created': time.time(),
            'cool_until': 0, 'used': 0}


def _add():
    acct = provision()
    def fn(items):
        items.append(acct)
        items.sort(key=lambda a: a.get('created', 0))
        del items[:-MAX_POOL]
    _update(fn)
    return acct


_topping = threading.Event()


def top_up():
    """Keep TARGET usable accounts warm; one thread per process, one provisioner per host."""
    if _topping.is_set():
        return
    def run():
        _topping.set()
        try:
            while sum(1 for a in load() if usable(a)) < TARGET:
                with _flock('make', blocking=False) as got:
                    if not got:
                        return
                    _add()
        except Exception as exc:
            logger.warning('Qwen pool top-up stopped: %s', exc)
        finally:
            _topping.clear()
    threading.Thread(target=run, daemon=True).start()


def acquire(exclude=()):
    """The least recently used usable account; makes one (about 8 s) when none is."""
    deadline = time.time() + 75
    while True:
        pick = []
        def fn(items):
            ok = sorted((a for a in items if usable(a, exclude)), key=lambda a: a.get('used', 0))
            if ok:
                ok[0]['used'] = time.time()
                pick.append(dict(ok[0]))
        _update(fn)
        if pick:
            if sum(1 for a in load() if usable(a)) < TARGET:
                top_up()
            return pick[0]
        with _flock('make', blocking=False) as got:
            if got:
                try:
                    return dict(_add())
                except Exception as exc:
                    if time.time() > deadline:
                        raise RuntimeError('Qwen account could not be created: %s' % exc)
                    time.sleep(1.5)
                    continue
        if time.time() > deadline:
            raise RuntimeError('Qwen account pool is busy, try again')
        time.sleep(1.5)


def renew(email):
    """Sign in again with the stored password; drops the account if that fails."""
    acct = next((a for a in load() if a['email'] == email), None)
    if not acct:
        return None
    try:
        tok = _signin(email, acct['password'], acct['device'])
    except Exception:
        drop(email)
        return None
    def fn(items):
        for a in items:
            if a['email'] == email:
                a['token'] = tok
    _update(fn)
    return dict(acct, token=tok)
