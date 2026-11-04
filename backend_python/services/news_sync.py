"""Autopilot for the blog: pull official notices and education news into
`Announcement` rows, formatted like any other post.

* `run_sync()` is the whole job. Safe to run twice at once and safe to re-run: an
  item is identified by (source_key, source_guid), so nothing is created twice,
  and a post an admin archived or edited is never touched again.
* `maybe_autosync()` is the autopilot. The middleware calls it on web requests; it
  claims the next run with one atomic UPDATE (so several workers never overlap)
  and does the work on a background thread, so no visitor waits for it.
* `python manage.py sync_news` runs it from cron or by hand.
"""
import logging
import re
import threading
import time
import unicodedata
from html import escape
from urllib.parse import urljoin

import bleach
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, connection

from api.models import Announcement, NewsSyncState
from api.utils import now_ms, uuid_str

from . import news_sources as ns

logger = logging.getLogger('nebians.services.news_sync')

SCHEDULER_KEY = '_scheduler'
MAX_NEW_PER_SOURCE = 12          # per run; a first run fills the page, later runs only add what is new
MAX_AGE_MS = 240 * 86400 * 1000  # older than ~8 months is archive, not news
RUN_BUDGET_SECONDS = 150

ALLOWED_TAGS = ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'blockquote',
                'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'figure', 'figcaption', 'hr']
ALLOWED_ATTRS = {'a': ['href', 'title'], 'img': ['src', 'alt'], 'td': ['colspan', 'rowspan'], 'th': ['colspan', 'rowspan']}


# ── formatting ───────────────────────────────────────────────────────

def _absolutize(html, base):
    return re.sub(r'(href|src)="([^"]*)"',
                  lambda m: '%s="%s"' % (m.group(1), urljoin(base, m.group(2).strip())), html)


def _external_links(attrs, new=False):
    href = attrs.get((None, 'href'), '')
    if href.startswith('http'):
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'rel')] = 'noopener nofollow'
    return attrs


def clean_body(html, base):
    """Source markup -> the small, safe subset the blog's article styles cover."""
    if not html:
        return ''
    html = re.sub(r'(?is)<(script|style|iframe|form|noscript)\b.*?</\1>', '', html)
    html = re.sub(r'(?is)<!--.*?-->', '', html)
    html = _absolutize(html, base)
    html = re.sub(r'(?i)<h1\b', '<h2', html)
    html = re.sub(r'(?i)</h1>', '</h2>', html)
    out = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS,
                       protocols=['http', 'https', 'mailto'], strip=True)
    out = bleach.linkify(out, callbacks=[_external_links])
    out = re.sub(r'<p>(\s|&nbsp;|<br\s*/?>)*</p>', '', out)       # empty paragraphs
    out = re.sub(r'(\s*<br\s*/?>){3,}', '<br><br>', out)
    return out.strip()


def excerpt(text, limit=220):
    text = ns.text_of(text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(' ', 1)[0].rstrip(' ,;:-')
    return cut + '…'


def _slug(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')[:90]


def _unique_slug(base):
    slug, n = base, 1
    while Announcement.objects.filter(slug=slug).exists():
        n += 1
        slug = '%s-%d' % (base, n)
    return slug


def build_content(src, item, body):
    """The post body. Notices carry their own text; stories are an excerpt that
    hands the reader to the publisher (we do not republish newspaper articles)."""
    if src['official']:
        return body
    if item.summary:
        return '<p>%s</p>' % escape(item.summary)
    return ''


# ── one item ─────────────────────────────────────────────────────────

def import_item(src, item, now):
    """Create the Announcement for `item`. Returns it, or None when skipped."""
    if src.get('detail') and item.needs_detail:
        src['detail'](item)
    if not item.title:
        return None
    published = item.published_at or now
    if published > now:
        published = now
    if now - published > MAX_AGE_MS:
        return None
    body = clean_body(item.body_html, item.url)
    content = build_content(src, item, body)
    summary = excerpt(item.summary or (body if src['official'] else ''), 220)
    if src['official'] and summary and summary.startswith(item.title[:40]):
        summary = ''
    base = _slug(item.title) or '%s-notice-%s' % (src['key'], _slug(item.guid)[-24:] or uuid_str()[:8])
    tags = ', '.join(t for t in (src['tag'], 'Official' if src['official'] else '') if t)
    try:
        return Announcement.objects.create(
            id=uuid_str(), title=item.title[:255], slug=_unique_slug(base),
            summary=summary[:500], content=content, category=item.category or 'notice',
            status='published', is_pinned=False,
            cover_image_url=item.cover or '', external_url=item.url, tags=tags,
            published_at=published, created_at=now, updated_at=now,
            source_key=src['key'], source_name=src['name'], source_guid=item.guid[:300],
            source_official=bool(src['official']), attachments=item.attachments or [],
        )
    except IntegrityError:
        return None      # another worker imported it a moment ago


def sync_source(src, now=None, deadline=None):
    now = now or now_ms()
    state, _ = NewsSyncState.objects.get_or_create(key=src['key'])
    new = 0
    status = 'ok'
    try:
        items = src['list'](src)
        known = set(Announcement.objects.filter(source_key=src['key'], source_guid__in=[i.guid[:300] for i in items])
                    .values_list('source_guid', flat=True))
        fresh = [i for i in items if i.guid[:300] not in known]
        # Oldest first so the newest story ends up with the newest creation order.
        fresh = fresh[:MAX_NEW_PER_SOURCE]
        for item in reversed(fresh):
            if deadline and time.monotonic() > deadline:
                status = 'ok (time budget reached, rest next run)'
                break
            try:
                if import_item(src, item, now):
                    new += 1
            except Exception as e:     # one broken page must not sink the batch
                logger.warning('news item %s/%s skipped: %s', src['key'], item.guid, e)
    except Exception as e:
        status = ('failed: %s' % e)[:290]
        logger.warning('news source %s failed: %s', src['key'], e)
    state.last_run_at = now
    state.last_status = status
    state.last_new = new
    if status.startswith('ok'):
        state.last_ok_at = now
    state.total_imported += new
    state.save()
    return {'key': src['key'], 'new': new, 'status': status}


def run_sync(only=None, force=False):
    """Run every enabled source (or just `only`). `force` ignores the enabled flag."""
    started = time.monotonic()
    deadline = started + RUN_BUDGET_SECONDS
    results = []
    for src in ns.SOURCES:
        if only and src['key'] not in only:
            continue
        state = NewsSyncState.objects.filter(key=src['key']).first()
        if state and not state.enabled and not force:
            continue
        results.append(sync_source(src, deadline=deadline))
    if any(r['new'] for r in results):
        _bust_news_cache()
    return results


def _bust_news_cache():
    keys = ['news_list::']
    keys += ['news_list:%s:' % c for c, _ in Announcement.CATEGORY_CHOICES]
    cache.delete_many(keys)


# ── autopilot ────────────────────────────────────────────────────────

_local_next_check = 0.0
_thread_lock = threading.Lock()


def interval_ms():
    return int(getattr(settings, 'NEWS_SYNC_INTERVAL_MIN', 120)) * 60 * 1000


def claim_run(now=None):
    """True for exactly one caller per interval, across every worker process."""
    now = now or now_ms()
    NewsSyncState.objects.get_or_create(key=SCHEDULER_KEY, defaults={'enabled': True})
    claimed = NewsSyncState.objects.filter(key=SCHEDULER_KEY, last_run_at__lt=now - interval_ms()) \
        .update(last_run_at=now)
    return bool(claimed)


def _worker():
    try:
        run_sync()
    except Exception:
        logger.exception('news autosync crashed')
    finally:
        connection.close()


def maybe_autosync():
    """Cheap to call on every request: one float compare, and a DB check at most
    every five minutes per process."""
    global _local_next_check
    if not getattr(settings, 'NEWS_AUTOSYNC', True):
        return False
    t = time.monotonic()
    if t < _local_next_check:
        return False
    with _thread_lock:
        if time.monotonic() < _local_next_check:
            return False
        _local_next_check = time.monotonic() + 300
    try:
        if not claim_run():
            return False
    except Exception:       # table missing during a deploy, DB hiccup: try later
        return False
    threading.Thread(target=_worker, name='news-autosync', daemon=True).start()
    return True
