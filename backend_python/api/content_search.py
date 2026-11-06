"""Search over the library for the desktop app: subjects, units, topics (instant) and chapter text (lazy index)."""
import html as _html
import json
import re
import threading

from . import content_api as C

_lock = threading.Lock()
_state = {'sig': None, 'docs': None}
_TAG = re.compile(r'<[^>]+>')
_WS = re.compile(r'\s+')


def _plain(markup: str) -> str:
    return _WS.sub(' ', _html.unescape(_TAG.sub(' ', markup or ''))).strip()


def _load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _build(fulltext: bool):
    docs = []
    index = _load_json(C.syllabus_index_path()) if C.syllabus_index_path() else None
    for track in (index or {}).get('grades', []):
        for subj in track.get('subjects', []):
            key = '%s-%s' % (track.get('grade'), subj.get('subject'))
            base = {
                'track': str(track.get('grade', '')), 'subject': subj.get('subject', ''),
                'subjectName': subj.get('name', ''), 'trackLabel': track.get('short') or track.get('label', ''),
                'color': subj.get('color', ''),
            }
            docs.append(dict(base, kind='subject', chapterKind=None, no=0, title=subj.get('name', ''),
                             snippet=track.get('label', ''), text=(subj.get('name', '') + ' ' + subj.get('name_ne', '')).lower(), w=6))
            p = C.syllabus_path(key)
            syl = _load_json(p) if p else None
            for unit in (syl or {}).get('units', []):
                no = int(unit.get('no') or 0)
                title = unit.get('title', '')
                docs.append(dict(base, kind='unit', chapterKind='unit', no=no, title=title,
                                 snippet=subj.get('name', ''), text=title.lower(), w=5))
                for topic in unit.get('topics', []) or []:
                    docs.append(dict(base, kind='topic', chapterKind='unit', no=no, title=str(topic),
                                     snippet='%s · %s' % (subj.get('name', ''), title), text=str(topic).lower(), w=3))
            if fulltext:
                d = C.STUDY_DIR / key
                if d.is_dir():
                    for f in sorted(d.glob('*.json')):
                        if f.name == 'index.json':
                            continue
                        ch = _load_json(f)
                        if not ch:
                            continue
                        m = re.match(r'^(unit|bank)-(\d+)$', f.stem)
                        kind, no = (m.group(1), int(m.group(2))) if m else ('guide', 0)
                        docs.append(dict(base, kind='text', chapterKind=kind, no=no,
                                         title=ch.get('title', f.stem), snippet='', raw=_plain(ch.get('html', '')), w=1))
    for d in docs:
        if 'raw' in d:
            d['text'] = d['raw'].lower()
    return docs


def _docs():
    import os
    sig = C.manifest()['version']
    with _lock:
        if _state['sig'] != sig:
            _state['docs'] = _build(os.environ.get('CONTENT_SEARCH_FULLTEXT', '1') != '0')
            _state['sig'] = sig
        return _state['docs']


def _snippet(raw: str, low: str, pos: int, n: int) -> str:
    a = max(0, pos - 60)
    b = min(len(raw), pos + n + 100)
    s = raw[a:b].strip()
    return ('…' if a else '') + s + ('…' if b < len(raw) else '')


def search(query: str, limit: int = 40):
    q = _WS.sub(' ', (query or '').strip().lower())[:80]
    if len(q) < 2:
        return []
    terms = [t for t in q.split(' ') if t][:6]
    hits = []
    for d in _docs():
        text = d['text']
        if not all(t in text for t in terms):
            continue
        pos = text.find(terms[0])
        score = d['w'] * 10
        if d['kind'] != 'text':
            if text == q:
                score += 40
            elif text.startswith(q):
                score += 20
            elif pos == 0 or text[pos - 1:pos] == ' ':
                score += 8
        else:
            score += min(text.count(terms[0]), 12)
        hits.append((score, d, pos))
    hits.sort(key=lambda x: (-x[0], x[1]['title']))
    out = []
    for score, d, pos in hits[:limit]:
        item = {k: d[k] for k in ('kind', 'track', 'subject', 'subjectName', 'trackLabel', 'color', 'chapterKind', 'no', 'title')}
        item['snippet'] = _snippet(d['raw'], d['text'], pos, len(terms[0])) if d['kind'] == 'text' else d['snippet']
        item['score'] = score
        out.append(item)
    return out
