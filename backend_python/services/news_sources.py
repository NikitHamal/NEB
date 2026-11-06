"""Where the blog's auto-imported stories come from.

Two kinds of source, both read-only and both fixed in code (nothing a visitor
types ever becomes a URL we fetch):

* official -- government and exam-board notices. These are public documents,
  so the notice itself (title, date, body, PDF links) is republished in full.
* news -- education stories from newspaper RSS feeds, kept only when they are
  about schooling. We keep the headline, an excerpt and the picture, and send
  the reader to the publisher for the rest.

An adapter turns one listing into `Item`s. Fetching details, sanitising and
saving is `services/news_sync.py`'s job.
"""
import logging
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from urllib.parse import urljoin, urlparse

import requests

logger = logging.getLogger('nebians.services.news_sources')

USER_AGENT = 'Mozilla/5.0 (compatible; NEBiansBot/1.0; +https://nebians.consica.com.np)'
TIMEOUT = 15
MAX_BYTES = 3 * 1024 * 1024


@dataclass
class Item:
    guid: str
    title: str
    url: str
    published_at: int = 0          # ms since epoch, 0 = unknown (the importer uses "now")
    summary: str = ''
    body_html: str = ''            # raw, sanitised by the importer
    cover: str = ''
    attachments: list = field(default_factory=list)   # [{'name', 'url', 'kind'}]
    category: str = ''
    needs_detail: bool = False     # the listing is not enough, fetch `url`


# ── http ─────────────────────────────────────────────────────────────

def fetch(url):
    """GET `url` as text. Raises on HTTP errors, caps the body at MAX_BYTES."""
    resp = requests.get(url, headers={'User-Agent': USER_AGENT, 'Accept-Language': 'en,ne;q=0.8'},
                        timeout=TIMEOUT, stream=True)
    try:
        resp.raise_for_status()
        data = b''
        for chunk in resp.iter_content(65536):
            data += chunk
            if len(data) > MAX_BYTES:
                break
    finally:
        resp.close()
    if len(data) > MAX_BYTES:
        raise ValueError('response too large')
    enc = None
    if 'charset' in resp.headers.get('content-type', '').lower():
        enc = resp.encoding
    if not enc:
        head = data[:2048].decode('ascii', 'ignore').lower()
        m = re.search(r'charset=["\']?([a-z0-9_-]+)', head)
        enc = m.group(1) if m else 'utf-8'
    try:
        return data.decode(enc, 'replace')
    except LookupError:
        return data.decode('utf-8', 'replace')


# ── text helpers ─────────────────────────────────────────────────────

_TAG = re.compile(r'<[^>]+>')
_WS = re.compile(r'\s+')


def text_of(html):
    return _WS.sub(' ', unescape(_TAG.sub(' ', html or ''))).strip()


def extract_block(html, marker, tag='div'):
    """Inner HTML of the first <tag> whose opening tag contains `marker`,
    found by counting nested tags (no HTML parser needed for these pages)."""
    m = re.search(r'<%s\b[^>]*%s[^>]*>' % (tag, re.escape(marker)), html)
    if not m:
        return ''
    depth, pos = 1, m.end()
    opener = re.compile(r'<%s\b' % tag)
    closer = re.compile(r'</%s\s*>' % tag)
    while depth:
        o, c = opener.search(html, pos), closer.search(html, pos)
        if not c:
            return html[m.end():]
        if o and o.start() < c.start():
            depth += 1
            pos = o.end()
        else:
            depth -= 1
            pos = c.end()
            if not depth:
                return html[m.end():c.start()]
    return ''


def meta_content(html, prop):
    for pat in (r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]*content=["\']([^"\']*)["\']',
                r'<meta[^>]+content=["\']([^"\']*)["\'][^>]*(?:property|name)=["\']%s["\']'):
        m = re.search(pat % re.escape(prop), html, re.I)
        if m:
            return unescape(m.group(1)).strip()
    return ''


DOC_EXT = re.compile(r'\.(pdf|docx?|xlsx?|pptx?|zip)(?:[?#][^"\'\s<>]*)?$', re.I)


def attachment(url, name=''):
    path = urlparse(url).path
    ext = path.rsplit('.', 1)[-1].lower() if '.' in path else ''
    kind = {'pdf': 'pdf', 'doc': 'doc', 'docx': 'doc', 'xls': 'sheet', 'xlsx': 'sheet',
            'ppt': 'slides', 'pptx': 'slides', 'zip': 'zip'}.get(ext, 'file')
    clean = url.split('#', 1)[0]
    if not name:
        name = path.rsplit('/', 1)[-1] or 'Attachment'
    return {'name': name[:120], 'url': clean, 'kind': kind}


def find_documents(html, base):
    seen, out = set(), []
    for m in re.finditer(r'(?:href|src|data-src|file|url)\s*[=:]\s*["\']([^"\']+)["\']', html):
        u = urljoin(base, unescape(m.group(1)).strip())
        key = u.split('#')[0]
        if not u.startswith('http') or not DOC_EXT.search(u) or key in seen:
            continue
        seen.add(key)
        out.append(attachment(u))
    return out


# ── Bikram Sambat -> AD ──────────────────────────────────────────────
# Month lengths straight from the official calendar (Baisakh..Chait). 2078-01-01
# BS fell on 2021-04-14 AD. Dates outside the table fall back to "now".

BS_YEARS = {
    2078: (31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30),
    2079: (31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30),
    2080: (31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30),
    2081: (31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31),
    2082: (31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30),
    2083: (31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30),
    2084: (31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30),
    2085: (31, 32, 31, 32, 30, 31, 30, 30, 29, 30, 30, 30),
    2086: (30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30),
    2087: (31, 31, 32, 31, 31, 31, 30, 29, 30, 30, 30, 30),
    2088: (30, 31, 32, 32, 30, 31, 30, 30, 29, 30, 30, 30),
    2089: (30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30),
    2090: (30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30),
}
_BS_EPOCH = datetime(2021, 4, 14, tzinfo=timezone.utc)

BS_MONTHS = {
    'बैशाख': 1, 'वैशाख': 1, 'बैसाख': 1, 'जेठ': 2, 'असार': 3, 'अषाढ': 3, 'साउन': 4, 'श्रावण': 4,
    'भदौ': 5, 'भाद्र': 5, 'असोज': 6, 'आश्विन': 6, 'कात्तिक': 7, 'कार्तिक': 7, 'कातिक': 7,
    'मंसिर': 8, 'मङ्सिर': 8, 'पौष': 9, 'पुष': 9, 'माघ': 10, 'फागुन': 11, 'फाल्गुन': 11,
    'चैत': 12, 'चैत्र': 12,
}
_DIGITS = str.maketrans('०१२३४५६७८९', '0123456789')


def bs_to_ms(year, month, day, hh=12, mm=0, ss=0):
    """BS y/m/d -> ms since epoch (Nepal time -> UTC), or 0 when out of range."""
    if year not in BS_YEARS or not 1 <= month <= 12 or not 1 <= day <= BS_YEARS[year][month - 1]:
        return 0
    days = sum(sum(BS_YEARS[y]) for y in range(2078, year)) + sum(BS_YEARS[year][:month - 1]) + day - 1
    base = _BS_EPOCH.timestamp() + days * 86400 + hh * 3600 + mm * 60 + ss - (5 * 3600 + 45 * 60)
    return int(base * 1000)


def parse_bs(text):
    """Find a Bikram Sambat date in `text`: "१२ कात्तिक, २०८३", "२०८३ कार्तिक ११ गते
    मंगलबार १३:१५:२९ बजे" or "२०८३।०७।१२" / "2083-07-12". Returns ms or 0."""
    t = (text or '').translate(_DIGITS)
    hh = mm = ss = None
    tm = re.search(r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?', t)
    if tm and int(tm.group(1)) < 24 and int(tm.group(2)) < 60:
        hh, mm, ss = int(tm.group(1)), int(tm.group(2)), int(tm.group(3) or 0)
    names = '|'.join(sorted(map(re.escape, BS_MONTHS), key=len, reverse=True))
    y = m = d = None
    r = re.search(r'(\d{4})\s*(%s)\s*(\d{1,2})' % names, t)
    if r:
        y, m, d = int(r.group(1)), BS_MONTHS[r.group(2)], int(r.group(3))
    else:
        r = re.search(r'(\d{1,2})\s*(%s)[\s,]*(\d{4})' % names, t)
        if r:
            d, m, y = int(r.group(1)), BS_MONTHS[r.group(2)], int(r.group(3))
        else:
            r = re.search(r'\b(20\d\d)\s*[।\-/.]\s*(\d{1,2})\s*[।\-/.]\s*(\d{1,2})\b', t)
            if r:
                y, m, d = int(r.group(1)), int(r.group(2)), int(r.group(3))
    if not y:
        return 0
    if hh is None:
        return bs_to_ms(y, m, d)
    return bs_to_ms(y, m, d, hh, mm, ss)


# ── title -> category ────────────────────────────────────────────────

_RESULT = re.compile(r'result|नतिजा|परिणाम', re.I)


def official_category(title):
    return 'exam_results' if _RESULT.search(title or '') else 'notice'


EDU_WORDS = re.compile(
    r'\b(school|schools|student|students|teacher|teachers|education|educational|curriculum|'
    r'exam|exams|examination|examinations|scholarship|scholarships|university|universities|'
    r'campus|college|colleges|see|neb|class (?:10|11|12|ten|eleven|twelve)|grade (?:10|11|12)|'
    r'tribhuvan|tu|ku|ctevt|professors?|lecturers?|syllabus|literacy|classroom|academic|'
    r'education minister|vice[- ]chancellor|public service commission)\b',
    re.I)


def is_education(title, description=''):
    """About schooling: a keyword in the headline, or two different ones in the
    standfirst (one stray "university" in a story about an oil company is not enough)."""
    if EDU_WORDS.search(title or ''):
        return True
    return len({m.group(0).lower() for m in EDU_WORDS.finditer(description or '')}) >= 2


# ── adapters ─────────────────────────────────────────────────────────

def neb_listing(src):
    """neb.gov.np home page. Every notice is a link to /detail/<id>, followed by
    its publish date and PDF button until the next link. Menu links are short, so
    a title of 20+ characters is what separates a notice from navigation."""
    base = src['url']
    html = fetch(base)
    links = [m for m in re.finditer(r'<a[^>]+href="(https?://[^"]*?/detail/(\d+))"[^>]*>\s*([^<]{20,400}?)\s*</a>', html)]
    items = {}
    for n, m in enumerate(links):
        gid = m.group(2)
        end = links[n + 1].start() if n + 1 < len(links) else m.end() + 2500
        block = html[m.end():min(end, m.end() + 2500)]
        t = text_of(m.group(3))
        when = re.search(r'प्रकाशित मिति\s*([^<]+)', block)
        doc = re.search(r'href="([^"]+\.(?:pdf|docx?|xlsx?)[^"]*)"', block, re.I)
        atts = [attachment(urljoin(base, doc.group(1)), 'Official notice')] if doc else []
        ts = parse_bs(when.group(1)) if when else 0
        if not ts and doc:
            f = re.search(r'-(20\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.', doc.group(1))
            if f:
                y, mo, d, hh, mi, ss = map(int, f.groups())
                ts = int(datetime(y, mo, d, hh, mi, ss, tzinfo=timezone.utc).timestamp() * 1000) - 20700000
        old = items.get(gid)
        if old:      # the same notice is listed in several tabs, some with less detail
            old.published_at = old.published_at or ts
            old.attachments = old.attachments or atts
            continue
        items[gid] = Item(guid=gid, title=t, url=m.group(1), published_at=ts,
                          attachments=atts, category=official_category(t))
    # Undated links are static publications (handbooks, frameworks), not news.
    out = sorted((i for i in items.values() if i.published_at), key=lambda i: int(i.guid), reverse=True)
    if not out:
        raise ValueError('no notices found')
    return out[:src.get('limit', 25)]


def giwms_listing(src):
    """Government sites on the shared GIWMS platform (moest.gov.np, moecdc.gov.np):
    listing pages carry /content/<id>/<slug>/ links, newest id first. The listing
    has no dates or files, so each item needs its detail page."""
    items, seen = [], set()
    for page in src['pages']:
        url = urljoin(src['url'], page)
        try:
            html = fetch(url)
        except Exception as e:
            logger.warning('news source %s page %s: %s', src['key'], page, e)
            continue
        for m in re.finditer(r'href="\s*(/content/(\d+)/[^"\s]*)\s*"[^>]*>\s*([^<]{3,400}?)\s*<', html):
            cid = m.group(2)
            if cid in seen:
                continue
            seen.add(cid)
            t = text_of(m.group(3))
            items.append(Item(guid=cid, title=t, url=urljoin(src['url'], m.group(1)),
                              category=official_category(t), needs_detail=True))
    if not items:
        raise ValueError('no items found')
    items.sort(key=lambda i: int(i.guid), reverse=True)
    return items[:src.get('limit', 20)]


def giwms_detail(item):
    html = fetch(item.url)
    h1 = re.search(r'<h1[^>]*news__title[^>]*>(.*?)</h1>', html, re.S)
    if h1 and text_of(h1.group(1)):
        item.title = text_of(h1.group(1))
    meta = extract_block(html, 'meta date', 'div')
    item.published_at = parse_bs(text_of(meta)) or parse_bs(item.title)
    body = extract_block(html, 'details__desc', 'div')
    # Placeholder bodies on these sites are a lone "." or "-".
    item.body_html = body if len(text_of(body)) > 3 else ''
    # The PDF is handed to a flipbook script, outside the article block.
    flip = re.search(r"var pdf = ['\"]([^'\"]+)", html)
    main = extract_block(html, 'detail__page-inner-seperator', 'div') or html
    docs = find_documents(main + (' href="%s"' % flip.group(1) if flip else ''), item.url)
    for n, d in enumerate(docs, 1):
        d['name'] = 'Official document' if len(docs) == 1 else 'Document %d' % n
    item.attachments = docs
    fig = extract_block(html, 'detail__page-inner-image', 'div')
    img = re.search(r'<figure[^>]*>.*?<img[^>]+src="([^"]+)"', fig, re.S)
    if img and 'static/assets' not in img.group(1):
        item.cover = urljoin(item.url, img.group(1))
    return item


def _local(tag):
    return tag.rsplit('}', 1)[-1]


def _child_text(el, *names):
    for c in el:
        if _local(c.tag) in names and (c.text or '').strip():
            return c.text.strip()
    return ''


def _parse_date(raw):
    raw = (raw or '').strip()
    if not raw:
        return 0
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
        except ValueError:
            return 0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def rss_listing(src):
    xml = fetch(src['url'])
    head = xml[:4096].upper()
    if '<!ENTITY' in head:
        raise ValueError('feed declares entities')
    root = ET.fromstring(xml.encode('utf-8'))
    items = []
    for el in root.iter():
        if _local(el.tag) not in ('item', 'entry'):
            continue
        title = text_of(_child_text(el, 'title'))
        link = _child_text(el, 'link')
        if not link:
            for c in el:
                if _local(c.tag) == 'link' and c.get('href'):
                    link = c.get('href')
                    break
        desc = _child_text(el, 'description', 'summary')
        encoded = _child_text(el, 'encoded', 'content')
        if not title or not link or not link.startswith('http'):
            continue
        if src.get('only_education', True) and not is_education(title, text_of(desc)):
            continue
        cover = ''
        for c in el.iter():
            n = _local(c.tag)
            if n in ('content', 'thumbnail', 'enclosure') and c.get('url') and \
                    (c.get('type', 'image').startswith('image') or c.get('medium') == 'image' or n == 'thumbnail'):
                cover = c.get('url')
                break
        if not cover:
            im = re.search(r'<img[^>]+src=["\']([^"\']+)', unescape(encoded or desc or ''))
            cover = im.group(1) if im else ''
        guid = _child_text(el, 'guid', 'id') or link
        items.append(Item(
            guid=guid[:300], title=title, url=link,
            published_at=_parse_date(_child_text(el, 'pubDate', 'published', 'updated', 'date')),
            summary=text_of(unescape(desc))[:500], cover=cover, category='news', needs_detail=True,
        ))
    return items


def news_detail(item):
    """Best effort: the article page's social card gives a picture and a clean
    standfirst when the feed had none. Never fatal."""
    if item.cover and len(item.summary) >= 40:
        return item
    try:
        html = fetch(item.url)
    except Exception:
        return item
    if not item.cover:
        item.cover = meta_content(html, 'og:image')
    if len(item.summary) < 40:
        item.summary = meta_content(html, 'og:description')[:500] or item.summary
    return item


# ── registry ─────────────────────────────────────────────────────────

SOURCES = [
    {'key': 'neb', 'name': 'National Examinations Board', 'official': True,
     'url': 'https://neb.gov.np/', 'list': neb_listing, 'detail': None, 'tag': 'NEB'},
    {'key': 'moest', 'name': 'Ministry of Education', 'official': True,
     'url': 'https://moest.gov.np/', 'list': giwms_listing, 'detail': giwms_detail, 'tag': 'MoEST',
     'pages': ['/category/1710', '/category/1712', '/category/1704', '/category/1973'], 'limit': 20},
    {'key': 'cdc', 'name': 'Curriculum Development Centre', 'official': True,
     'url': 'https://moecdc.gov.np/', 'list': giwms_listing, 'detail': giwms_detail, 'tag': 'CDC',
     'pages': ['/'], 'limit': 10},
    {'key': 'kathmandupost', 'name': 'The Kathmandu Post', 'official': False,
     'url': 'https://kathmandupost.com/rss', 'list': rss_listing, 'detail': news_detail, 'tag': 'Kathmandu Post'},
    {'key': 'onlinekhabar', 'name': 'Onlinekhabar English', 'official': False,
     'url': 'https://english.onlinekhabar.com/feed', 'list': rss_listing, 'detail': news_detail,
     'tag': 'Onlinekhabar'},
    {'key': 'risingnepal', 'name': 'The Rising Nepal', 'official': False,
     'url': 'https://risingnepaldaily.com/rss', 'list': rss_listing, 'detail': news_detail,
     'tag': 'Rising Nepal'},
]
SOURCE_BY_KEY = {s['key']: s for s in SOURCES}
