"""Zero-config web research: search + page extraction.

No API keys. Search goes through DuckDuckGo's HTML endpoint; pages are fetched
with a browser-impersonating TLS profile (curl_cffi, already a dependency) and
boiled down to readable text with BeautifulSoup.

Everything is defensive by design: research is best-effort, and a search that
fails must degrade to an empty result the agent can route around, never raise.
"""

import re
import time

from django.core.cache import cache

MAX_PAGE_CHARS = 24000
FETCH_TIMEOUT = 25
SEARCH_TIMEOUT = 20
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'

_BLOCK_TAGS = (
    'script', 'style', 'noscript', 'svg', 'canvas', 'iframe', 'form',
    'nav', 'header', 'footer', 'aside', 'template', 'button', 'select',
)

_CACHE_PREFIX = 'lazyresearch:v1:'
CACHE_TTL = 1800


def _cache_key(key):
    """Memcached rejects spaces and long keys, so hash the raw key."""
    import hashlib
    digest = hashlib.md5(key.encode('utf-8', 'ignore')).hexdigest()
    return f'{_CACHE_PREFIX}{digest}'


def _cache_get(key):
    try:
        return cache.get(_cache_key(key))
    except Exception:
        return None


def _cache_set(key, value, ttl=CACHE_TTL):
    try:
        cache.set(_cache_key(key), value, ttl)
    except Exception:
        pass


def _session():
    try:
        from curl_cffi import requests as cffi_requests
        return cffi_requests.Session(impersonate='chrome')
    except Exception:
        import requests
        session = requests.Session()
        session.headers.update({'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9'})
        return session


def clean_html(html, base_url=''):
    """Reduce a page to readable text, dropping chrome and boilerplate."""
    try:
        from bs4 import BeautifulSoup
    except Exception:
        return _crude_text(html)

    soup = BeautifulSoup(html or '', 'html.parser')
    for tag in soup(list(_BLOCK_TAGS)):
        tag.decompose()

    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'tr', 'br']):
        tag.insert_before('\n')

    text = soup.get_text(separator=' ')
    text = re.sub(r'[ \t\r\f\v]+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    lines = [ln.strip() for ln in text.split('\n')]
    lines = [ln for ln in lines if len(ln) > 1]
    return '\n'.join(lines)[:MAX_PAGE_CHARS]


def _crude_text(html):
    text = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', html or '')
    text = re.sub(r'(?s)<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;?', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()[:MAX_PAGE_CHARS]


def _absolute(href, base):
    if not href:
        return ''
    href = href.strip()
    if href.startswith('//'):
        return 'https:' + href
    if href.startswith('http'):
        return href
    if href.startswith('/') and base:
        from urllib.parse import urlparse
        parts = urlparse(base)
        return f'{parts.scheme}://{parts.netloc}{href}'
    return href


def _decode_ddg_href(href):
    """DuckDuckGo wraps outbound links in a redirect carrying the real URL."""
    if 'uddg=' not in (href or ''):
        return href
    from urllib.parse import parse_qs, unquote, urlparse
    try:
        qs = parse_qs(urlparse(href).query)
        if 'uddg' in qs:
            return unquote(qs['uddg'][0])
    except Exception:
        pass
    return href


def _search_duckduckgo(session, query, max_results):
    resp = session.post(
        'https://html.duckduckgo.com/html/',
        data={'q': query, 'kl': 'wt-wt'},
        timeout=SEARCH_TIMEOUT,
        headers={'User-Agent': UA},
    )
    if resp.status_code >= 400:
        raise RuntimeError(f'ddg status {resp.status_code}')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text or '', 'html.parser')
    out = []
    seen = set()
    for node in soup.select('.result, .web-result'):
        link = node.select_one('a.result__a, a.result-link')
        if not link:
            continue
        href = _decode_ddg_href(link.get('href') or '')
        href = _absolute(href, 'https://duckduckgo.com/')
        if not href.startswith('http') or href in seen:
            continue
        snippet_node = node.select_one('.result__snippet, .result-snippet')
        title = (link.get_text(' ', strip=True) or '').strip()
        if not title:
            continue
        seen.add(href)
        out.append({
            'title': title[:220],
            'url': href,
            'snippet': re.sub(r'\s+', ' ', (snippet_node.get_text(' ', strip=True) or ''))[:400],
        })
        if len(out) >= max_results:
            break
    return out


def _search_lite(session, query, max_results):
    resp = session.get(
        'https://lite.duckduckgo.com/lite/',
        params={'q': query},
        timeout=SEARCH_TIMEOUT,
        headers={'User-Agent': UA},
    )
    if resp.status_code >= 400:
        raise RuntimeError(f'lite status {resp.status_code}')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text or '', 'html.parser')
    out, seen = [], set()
    for link in soup.select('a[href]'):
        href = _decode_ddg_href(link.get('href') or '')
        if not href.startswith('http') or href in seen:
            continue
        title = (link.get_text(' ', strip=True) or '').strip()
        if len(title) < 12:
            continue
        seen.add(href)
        out.append({'title': title[:220], 'url': href, 'snippet': ''})
        if len(out) >= max_results:
            break
    return out


def web_search(query, max_results=6):
    """Search the web. Returns {'ok', 'query', 'results': [...], 'error'}."""
    query = (query or '').strip()
    if not query:
        return {'ok': False, 'query': query, 'results': [], 'error': 'empty query'}
    try:
        max_results = max(1, min(10, int(max_results)))
    except Exception:
        max_results = 6

    cache_key = f"search:{query.lower()}:{max_results}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    payload = {'ok': False, 'query': query, 'results': [], 'error': ''}
    try:
        session = _session()
        last_error = ''
        for strategy in (_search_duckduckgo, _search_lite):
            try:
                results = strategy(session, query, max_results)
                if results:
                    payload = {'ok': True, 'query': query, 'results': results, 'error': ''}
                    _cache_set(cache_key, payload)
                    return payload
            except Exception as exc:
                last_error = f'{strategy.__name__}: {exc}'
                continue
        payload['error'] = last_error or 'no results from any backend'
    except Exception as exc:
        payload['error'] = f'search unavailable: {exc}'

    return payload


def web_fetch(url, max_chars=8000, extract='text'):
    """Fetch a URL and return readable text. Returns {'ok','url','title','text','error'}."""
    url = (url or '').strip()
    if not url:
        return {'ok': False, 'url': url, 'text': '', 'error': 'empty url'}
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        max_chars = max(500, min(MAX_PAGE_CHARS, int(max_chars)))
    except Exception:
        max_chars = 8000

    cache_key = f"fetch:{url}:{max_chars}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    payload = {'ok': False, 'url': url, 'title': '', 'text': '', 'error': ''}
    started = time.time()
    try:
        session = _session()
        resp = session.get(url, timeout=FETCH_TIMEOUT, headers={'User-Agent': UA}, allow_redirects=True)
        ctype = (resp.headers.get('Content-Type') or '').lower()
        if resp.status_code >= 400:
            payload['error'] = f'HTTP {resp.status_code}'
            return payload

        if 'pdf' in ctype or url.lower().endswith('.pdf'):
            text = _pdf_text(getattr(resp, 'content', b''))
            payload.update({'ok': bool(text), 'title': url.rsplit('/', 1)[-1], 'text': text[:max_chars]})
            if not text:
                payload['error'] = 'could not extract PDF text'
            _cache_set(cache_key, payload)
            return payload

        html = resp.text or ''
        title = ''
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            if soup.title and soup.title.string:
                title = soup.title.string.strip()[:220]
        except Exception:
            pass

        text = clean_html(html, url)
        payload.update({
            'ok': bool(text),
            'title': title,
            'text': text[:max_chars],
            'elapsedMs': int((time.time() - started) * 1000),
        })
        if not text:
            payload['error'] = 'page had no extractable text'
        _cache_set(cache_key, payload)
        return payload
    except Exception as exc:
        payload['error'] = f'fetch failed: {exc}'
        return payload


def _pdf_text(raw):
    try:
        import io
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        parts = []
        for page in reader.pages[:40]:
            try:
                parts.append(page.extract_text() or '')
            except Exception:
                continue
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(parts)).strip()
    except Exception:
        return ''


def research_pack(query, max_results=6, fetch_top=3, per_page_chars=6000):
    """Convenience used by the document engine: search, then read the best pages."""
    search = web_search(query, max_results=max_results)
    sources = []
    for item in (search.get('results') or [])[:max(1, fetch_top)]:
        page = web_fetch(item['url'], max_chars=per_page_chars)
        if page.get('ok') and page.get('text'):
            sources.append({
                'title': item.get('title') or page.get('title') or item['url'],
                'url': item['url'],
                'snippet': item.get('snippet') or '',
                'text': page['text'],
            })
    return {'query': query, 'search_ok': search.get('ok'), 'sources': sources}
