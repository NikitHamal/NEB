"""Qwen chat through the Android app gateway (keyless, any server IP).

Models come straight from the gateway's own list, so Qwen4 appears exactly as
long as Alibaba serves it to a free account, under the id it serves it with.
A turn that hits an account's quota cools that account for a while and goes on
with the next account of the same pool, never to another model or provider.
"""
import json
import threading
import time

import requests

from . import qwen_app_pool as pool

_models = {'at': 0, 'data': []}
_RATE = ('ratelimit', 'rate_limit', 'rate limit', 'quota', 'too many', 'limit exceeded', 'usage limit')
_AUTH = ('unauthorized', 'unauthenticated', 'token', 'login', 'expired', 'invalid_auth')


def raw_models(force=False):
    """The gateway's own model rows, cached 10 min."""
    if _models['data'] and not force and time.time() - _models['at'] < 600:
        return _models['data']
    acct = pool.acquire()
    r = requests.get(pool.BASE + '/models/', headers=pool.headers(acct['token'], acct['device']), timeout=20)
    rows = (r.json().get('data') or {}).get('data') or []
    if rows:
        _models.update(at=time.time(), data=rows)
    return rows or _models['data']


def list_models(force=False):
    """[{id, name, thinking, vision, search}] as the gateway serves them."""
    out = []
    for m in raw_models(force):
        meta = (m.get('info') or {}).get('meta') or {}
        cap = meta.get('capabilities') or {}
        out.append({'id': m['id'], 'name': m.get('name') or m['id'], 'thinking': bool((meta.get('abilities') or {}).get('thinking')),
                    'vision': bool(cap.get('vision')), 'search': bool(cap.get('search'))})
    return out


def _prompt(messages, system):
    turns = [m for m in messages if m.get('content')]
    last = turns[-1]['content'] if turns else ''
    earlier = turns[:-1]
    parts = []
    if system:
        parts.append('[System]\n' + system)
    if earlier:
        parts.append('[Conversation so far]\n' + '\n'.join(
            '%s: %s' % ('Assistant' if m.get('role') == 'assistant' else 'User', m['content']) for m in earlier))
    return ('\n\n'.join(parts) + '\n\n[User]\n' + last) if parts else last


def _payload(chat_id, model, text, thinking, search):
    ts = int(time.time())
    return {'stream': True, 'incremental_output': True, 'chat_id': chat_id, 'chat_mode': 'normal', 'model': model,
            'version': '2.1', 'timestamp': ts, 'share_id': '', 'origin_branch_message_id': '',
            'messages': [{'chat_type': 't2t', 'content': text, 'role': 'user', 'timestamp': ts, 'sub_chat_type': 't2t',
                          'models': [model], 'user_action': 'chat', 'extra': {'meta': {'subChatType': 't2t'}},
                          'feature_config': {'output_schema': 'phase', 'thinking_enabled': bool(thinking),
                                             'thinking_format': 'summary', 'auto_thinking': False,
                                             'auto_search': bool(search)}}]}


def _classify(status, body):
    low = (body or '').lower()
    if '_____tmd_____' in low or 'rgv587' in low or 'x5secdata' in low:
        return 'waf'
    if status == 429 or any(k in low for k in _RATE):
        return 'rate'
    if status in (401, 403) or (status >= 400 and any(k in low for k in _AUTH)):
        return 'auth'
    return 'other'


def _forget(acct, chat_id):
    def run():
        try:
            requests.delete('%s/chats/%s' % (pool.BASE, chat_id), headers=pool.headers(acct['token'], acct['device']), timeout=8)
        except Exception:
            pass
    threading.Thread(target=run, daemon=True).start()


def _one(acct, model, text, thinking, search):
    """Events of one attempt on one account. Raises RuntimeError('kind|message') before any text."""
    hdr = lambda **x: pool.headers(acct['token'], acct['device'], **x)
    r = requests.post(pool.BASE + '/chats/new', json={'chat_mode': 'normal', 'project_id': ''}, headers=hdr(), timeout=25)
    j = r.json() if 'json' in r.headers.get('content-type', '') else {}
    if not j.get('success'):
        raise RuntimeError('%s|%s' % (_classify(r.status_code, r.text[:400]), (r.text or '')[:200]))
    chat_id = j['data']['id']
    try:
        resp = requests.post('%s/chat/completions?chat_id=%s' % (pool.BASE, chat_id), json=_payload(chat_id, model, text, thinking, search),
                             headers=hdr(**{'Accept': '*/*,text/event-stream', 'Content-Type': 'application/json; charset=UTF-8'}),
                             stream=True, timeout=(15, 90))
        if 'event-stream' not in resp.headers.get('content-type', ''):
            body = resp.text[:500]
            raise RuntimeError('%s|%s' % (_classify(resp.status_code, body), body[:200]))
        seen_thoughts, got = 0, False
        for raw in resp.iter_lines(decode_unicode=True):
            if not raw or not raw.startswith('data:'):
                continue
            try:
                d = json.loads(raw[5:].strip())
            except ValueError:
                continue
            err = d.get('error') or ((d.get('data') or {}).get('code') if d.get('success') is False else None)
            if err:
                msg = json.dumps(d)[:300]
                if got:
                    yield {'type': 'error', 'message': msg}
                    return
                raise RuntimeError('%s|%s' % (_classify(429 if 'limit' in msg.lower() else 0, msg), msg))
            delta = ((d.get('choices') or [{}])[0]).get('delta') or {}
            phase, content = delta.get('phase'), delta.get('content') or ''
            if phase == 'thinking_summary':
                items = ((delta.get('extra') or {}).get('summary_thought') or {}).get('content') or []
                for t in items[seen_thoughts:]:
                    yield {'type': 'thought', 'content': t + '\n'}
                seen_thoughts = max(seen_thoughts, len(items))
            elif phase == 'think' and content:
                yield {'type': 'thought', 'content': content}
            elif phase in ('search', 'image_search'):
                res = (delta.get('extra') or {}).get('search_result')
                if res:
                    yield {'type': 'search', 'content': '', 'results': res}
            elif phase == 'answer' and content:
                got = True
                yield {'type': 'text', 'content': content}
        if not got:
            raise RuntimeError('rate|Qwen returned an empty answer')
    finally:
        _forget(acct, chat_id)


def stream_chat(messages, model='qwen3.8-max', thinking=False, search=False, system=''):
    """Yield {'type': 'text'|'thought'|'search'|'error'}. Rotates accounts only before the first text."""
    text = _prompt(messages, system)
    tried, last = [], 'Qwen did not answer'
    for _ in range(4):
        try:
            acct = pool.acquire(tried)
        except Exception as exc:
            yield {'type': 'error', 'message': str(exc)}
            return
        tried.append(acct['email'])
        started = False
        try:
            for ev in _one(acct, model, text, thinking, search):
                started = started or ev['type'] == 'text'
                yield ev
            return
        except RuntimeError as exc:
            kind, _, msg = str(exc).partition('|')
            last = msg or str(exc)
            if started:
                yield {'type': 'error', 'message': last}
                return
            if kind == 'auth':
                if not pool.renew(acct['email']):
                    pass
                tried.remove(acct['email'])
            elif kind == 'rate':
                pool.cool(acct['email'], 600)
            elif kind == 'waf':
                pool.cool(acct['email'], 60)
            else:
                yield {'type': 'error', 'message': last}
                return
        except requests.RequestException as exc:
            last = 'Qwen gateway unreachable: %s' % str(exc)[:160]
            if started:
                yield {'type': 'error', 'message': last}
                return
    yield {'type': 'error', 'message': last}


def ask(messages, model='qwen3.8-max', thinking=False, system=''):
    """Whole answer as text ('' when the pool could not produce one)."""
    out = []
    for ev in stream_chat(messages, model, thinking, False, system):
        if ev['type'] == 'text':
            out.append(ev['content'])
        elif ev['type'] == 'error' and not out:
            return ''
    return ''.join(out)
