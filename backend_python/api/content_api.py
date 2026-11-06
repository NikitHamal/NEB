"""Read-only study-content service for the desktop app (and anything else that wants the library over HTTP).

The content is the same JSON the website reader already renders:
    web/data/syllabus/index.json              the tracks and their subjects
    web/data/syllabus/<track>-<subject>.json  one syllabus
    web/data/study/<track>-<subject>/{index,unit-NN,bank-NN,guide}.json
plus the book PDFs in NEB_BOOKS_DIR (default <repo>/notes/pdf).

Nothing here takes a path from the client. Every identifier is matched against a strict pattern, and the
resolved file must be an existing regular file inside its data directory.
"""
import hashlib
import os
import re
import threading
import time
from pathlib import Path

from django.conf import settings

DATA_ROOT = Path(settings.BASE_DIR) / 'web' / 'data'
SYLLABUS_DIR = DATA_ROOT / 'syllabus'
STUDY_DIR = DATA_ROOT / 'study'
BOOKS_DIR = Path(os.environ.get('NEB_BOOKS_DIR') or (Path(settings.BASE_DIR).parent / 'notes' / 'pdf'))

KEY_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
CHAPTER_RE = re.compile(r'^(?:unit-\d{2,3}|bank-\d{2,3}|guide|index)$')
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9.\-]{0,160}$')
MAX_KEY = 80


def _safe_child(parent: Path, *parts: str):
    try:
        candidate = parent.joinpath(*parts).resolve()
        root = parent.resolve()
    except (OSError, ValueError):
        return None
    if root not in candidate.parents:
        return None
    return candidate if candidate.is_file() else None


def syllabus_index_path():
    return _safe_child(SYLLABUS_DIR, 'index.json')


def syllabus_path(key: str):
    if not key or len(key) > MAX_KEY or not KEY_RE.match(key) or key == 'index':
        return None
    return _safe_child(SYLLABUS_DIR, key + '.json')


def study_path(key: str, name: str):
    if not key or len(key) > MAX_KEY or not KEY_RE.match(key) or not CHAPTER_RE.match(name or ''):
        return None
    return _safe_child(STUDY_DIR, key, name + '.json')


def etag_for(path: Path) -> str:
    st = path.stat()
    return '"%x-%x"' % (st.st_mtime_ns // 1000, st.st_size)


_manifest_lock = threading.Lock()
_manifest_cache = {'at': 0.0, 'value': None}


def _signature() -> str:
    h = hashlib.sha1()
    for base in (SYLLABUS_DIR, STUDY_DIR):
        if not base.is_dir():
            continue
        for root, _dirs, files in os.walk(base):
            for f in sorted(files):
                if f.endswith('.json'):
                    st = os.stat(os.path.join(root, f))
                    h.update(('%s:%d:%d;' % (f, st.st_mtime_ns // 1000, st.st_size)).encode())
    return h.hexdigest()[:16]


def manifest() -> dict:
    now = time.time()
    with _manifest_lock:
        if _manifest_cache['value'] and now - _manifest_cache['at'] < 60:
            return _manifest_cache['value']
        chapters = subjects = 0
        if STUDY_DIR.is_dir():
            for d in STUDY_DIR.iterdir():
                if d.is_dir():
                    subjects += 1
                    chapters += sum(1 for f in d.glob('*.json') if f.name != 'index.json')
        value = {
            'schema': 1,
            'version': _signature(),
            'generatedAt': int(now),
            'subjects': subjects,
            'chapters': chapters,
            'books': len(list_books()),
            'assetBase': '/static/web/',
            'desktop': {
                'latest': os.environ.get('DESKTOP_LATEST_VERSION', ''),
                'minimum': os.environ.get('DESKTOP_MIN_VERSION', ''),
                'downloadUrl': os.environ.get('DESKTOP_DOWNLOAD_URL', ''),
                'notes': os.environ.get('DESKTOP_RELEASE_NOTES', ''),
            },
        }
        _manifest_cache.update(at=now, value=value)
        return value


_TRACK_PREFIX = re.compile(r'^(cee|ioe|bca|csit|bit|bbs|bbm)-', re.I)


def _book_meta(path: Path) -> dict:
    base = path.stem
    if base.lower().startswith('nebians-'):
        base = base[len('nebians-'):]
    grade = track = ''
    subject = base
    m = re.search(r'-grade-(\d+)$', base, re.I)
    if m:
        grade = track = m.group(1)
        subject = base[:m.start()]
    else:
        t = _TRACK_PREFIX.match(base)
        if t:
            track = t.group(1).lower()
            subject = re.sub(r'^entrance-', '', base[t.end():], flags=re.I)
    st = path.stat()
    return {
        'slug': path.stem.lower(),
        'title': base.replace('-', ' '),
        'subject': subject.replace('-', ' ').strip(),
        'track': track,
        'grade': grade,
        'size': st.st_size,
        'updatedAt': int(st.st_mtime),
    }


_books_lock = threading.Lock()
_books_cache = {'at': 0.0, 'value': []}


def list_books() -> list:
    now = time.time()
    with _books_lock:
        if _books_cache['at'] and now - _books_cache['at'] < 120:
            return _books_cache['value']
        out = []
        if BOOKS_DIR.is_dir():
            for p in sorted(BOOKS_DIR.glob('*.pdf'), key=lambda x: x.name.lower()):
                if p.is_file() and SLUG_RE.match(p.stem.lower()):
                    out.append(_book_meta(p))
        _books_cache.update(at=now or 1.0, value=out)
        return out


def book_path(slug: str):
    if not slug or not SLUG_RE.match(slug):
        return None
    if slug not in {b['slug'] for b in list_books()}:
        return None
    for p in BOOKS_DIR.glob('*.pdf'):
        if p.stem.lower() == slug:
            return _safe_child(BOOKS_DIR, p.name)
    return None


def parse_range(header: str, size: int):
    """`bytes=a-b` -> (start, end) inclusive; None = serve everything; False = unsatisfiable."""
    m = re.match(r'^bytes=(\d*)-(\d*)$', (header or '').strip())
    if not m or (not m.group(1) and not m.group(2)):
        return None
    if m.group(1):
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else size - 1
    else:
        start, end = max(size - int(m.group(2)), 0), size - 1
    end = min(end, size - 1)
    if start > end or start >= size:
        return False
    return start, end
