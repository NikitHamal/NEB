"""Everything the admin Analytics page shows, computed from `PageView`.

One entry point, `build_report(range, source)`. The view stays thin, the
template only renders what this returns, and the CSV export reuses the same
daily series, so the page and the export cannot disagree.

Definitions (also in docs/ANALYTICS.md):
  pageview   one real, full-page HTML hit by a non-bot
  visitor    distinct visitor_id. Signed-in people are one stable id; logged-out
             visitors rotate daily, so a returning guest on another day counts again
  visit      a session: one visitor, hits no more than 30 minutes apart
  bounce     a visit with exactly one pageview
  duration   last hit minus first hit, averaged over visits with 2+ pageviews
  member     a signed-in account (user_identifier)
Days are cut at local midnight in settings.TIME_ZONE (Asia/Kathmandu), not UTC.
"""
from __future__ import annotations

import time
from datetime import date, datetime, timedelta, timezone as dt_timezone
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.cache import cache
from django.db.models import BigIntegerField, Count, ExpressionWrapper, F, Max, Min, Q
from django.db.models.functions import Mod

from . import report_devices, rules
from .rules import MS_DAY, MS_HOUR

PRESETS = {'today': 1, '7d': 7, '30d': 30, '90d': 90}
DEFAULT_RANGE = '7d'
MAX_CUSTOM_DAYS = 366
CACHE_SECONDS = 60
DOW = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
CHANNEL_LABELS = {
    'direct': 'Direct', 'search': 'Search', 'social': 'Social', 'email': 'Email',
    'ai': 'AI assistants', 'referral': 'Referral sites', 'campaign': 'Campaigns',
}


# --------------------------------------------------------------------------
# Time ranges
# --------------------------------------------------------------------------

def _tz() -> ZoneInfo:
    return ZoneInfo(settings.TIME_ZONE)


def tz_offset_ms() -> int:
    off = datetime.now(_tz()).utcoffset() or timedelta(0)
    return int(off.total_seconds() * 1000)


def _floor_day(ms: int, off: int) -> int:
    """UTC ms of the local midnight at or before `ms`."""
    return ms + off - ((ms + off) % MS_DAY) - off


def _local_midnight(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=_tz()).timestamp() * 1000)


def _local_dt(ms: int, off: int) -> datetime:
    return datetime.fromtimestamp((ms + off) / 1000, tz=dt_timezone.utc)


def _fmt_day(d: datetime) -> str:
    return f'{d.day} {d.strftime("%b")}'


def resolve_range(params, now_ms: int | None = None) -> dict:
    """Parse ?range=today|7d|30d|90d or ?from=YYYY-MM-DD&to=YYYY-MM-DD."""
    off = tz_offset_ms()
    now = now_ms if now_ms is not None else int(time.time() * 1000)
    tomorrow = _floor_day(now, off) + MS_DAY

    key = (params.get('range') or '').strip()
    start = end = None
    if params.get('from') and params.get('to'):
        try:
            d1 = date.fromisoformat(params['from'].strip())
            d2 = date.fromisoformat(params['to'].strip())
            if d1 > d2:
                d1, d2 = d2, d1
            start = _local_midnight(d1)
            end = min(_local_midnight(d2) + MS_DAY, tomorrow)
            if end <= start:
                start = end = None
            elif (end - start) // MS_DAY > MAX_CUSTOM_DAYS:
                start = end - MAX_CUSTOM_DAYS * MS_DAY
            key = 'custom'
        except ValueError:
            start = end = None
    if start is None:
        key = key if key in PRESETS else DEFAULT_RANGE
        end = tomorrow
        start = end - PRESETS[key] * MS_DAY

    days = (end - start) // MS_DAY
    span = end - start
    s, e = _local_dt(start, off), _local_dt(end - 1, off)
    if key == 'today':
        label = 'Today'
    elif key in PRESETS:
        label = f'Last {days} days'
    else:
        label = f'{_fmt_day(s)} – {_fmt_day(e)} {e.year}'
    return {
        'key': key, 'label': label, 'start': start, 'end': end, 'days': days,
        'prev_start': start - span, 'prev_end': start, 'off': off,
        'unit': 'hour' if days == 1 else 'day',
        'from': s.date().isoformat() if key == 'custom' else '',
        'to': e.date().isoformat() if key == 'custom' else '',
    }


# --------------------------------------------------------------------------
# Formatting helpers
# --------------------------------------------------------------------------

def fmt_num(n) -> str:
    n = int(round(n or 0))
    if n >= 1_000_000:
        return f'{n / 1_000_000:.1f}'.rstrip('0').rstrip('.') + 'M'
    if n >= 100_000:
        return f'{n / 1000:.0f}k'
    if n >= 10_000:
        return f'{n / 1000:.1f}'.rstrip('0').rstrip('.') + 'k'
    return f'{n:,}'


def fmt_duration(seconds: float) -> str:
    s = int(round(seconds or 0))
    if s <= 0:
        return '0s'
    m, sec = divmod(s, 60)
    if m >= 60:
        h, m = divmod(m, 60)
        return f'{h}h {m}m'
    return f'{m}m {sec:02d}s' if m else f'{sec}s'


def delta(cur, prev, *, rate: bool = False, lower_is_better: bool = False) -> dict:
    """Change versus the previous period, ready to render."""
    if rate:
        diff = round((cur or 0) - (prev or 0), 1)
        if abs(diff) < 0.05:
            return {'text': 'no change', 'dir': 'flat', 'good': None}
        up = diff > 0
        text = f'{"+" if up else "−"}{abs(diff):.1f} pts'
    else:
        if not prev and not cur:
            return {'text': 'no data', 'dir': 'flat', 'good': None}
        if not prev:
            return {'text': 'new', 'dir': 'up', 'good': not lower_is_better}
        pct = (cur - prev) / prev * 100
        if abs(pct) < 0.05:
            return {'text': 'no change', 'dir': 'flat', 'good': None}
        up = pct > 0
        text = f'{"+" if up else "−"}{abs(pct):.1f}%' if abs(pct) < 1000 else f'{"+" if up else "−"}{abs(pct):.0f}%'
    return {'text': text, 'dir': 'up' if up else 'down', 'good': (up != lower_is_better)}


def _rank(rows, total: int, limit: int | None = None) -> list[dict]:
    """[(name, count, **extra)] -> rows with share and bar width."""
    rows = [r for r in rows if r['count'] > 0]
    rows.sort(key=lambda r: -r['count'])
    if limit:
        rows = rows[:limit]
    top = rows[0]['count'] if rows else 0
    out = []
    for r in rows:
        r = dict(r)
        r['display'] = fmt_num(r['count'])
        r['pct'] = round(r['count'] / total * 100, 1) if total else 0.0
        r['width'] = round(r['count'] / top * 100, 1) if top else 0.0
        out.append(r)
    return out


def _spark(values: list[int], w: int = 100, h: int = 32, pad: int = 3) -> dict:
    """SVG polyline + area points for a tiny trend line (viewBox 0 0 w h)."""
    n = len(values)
    if n < 2:
        return {'line': '', 'area': ''}
    top = max(values) or 1
    pts = [(i * w / (n - 1), h - pad - (v / top) * (h - 2 * pad)) for i, v in enumerate(values)]
    line = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return {'line': line, 'area': f'0,{h} {line} {w},{h}'}


def _bars(values: list[int], fulls: list[str]) -> list[dict]:
    """Bar heights (percent of the tallest) with a hover label for each bucket."""
    top = max(values) if values else 0
    return [
        {'v': v, 'h': (max(round(v / top * 100), 6) if v and top else 0), 'tip': f'{fulls[i]}: {v:,}'}
        for i, v in enumerate(values)
    ]


# --------------------------------------------------------------------------
# Query helpers
# --------------------------------------------------------------------------

def _base(start: int, end: int, source: str):
    from api.models import PageView

    qs = PageView.objects.filter(created_at__gte=start, created_at__lt=end, is_bot=False).exclude(visitor_id='')
    if source in ('web', 'app'):
        qs = qs.filter(source=source)
    return qs


def _bucket(field: str, unit: str, off: int):
    size = MS_HOUR if unit == 'hour' else MS_DAY
    local = ExpressionWrapper(F(field) + off, output_field=BigIntegerField())
    return ExpressionWrapper(local - Mod(local, size), output_field=BigIntegerField())


def _bucket_starts(rng: dict, unit: str, *, previous: bool = False) -> list[int]:
    """Local-time bucket starts (ms, shifted by the tz offset) covering the range."""
    off = rng['off']
    size = MS_HOUR if unit == 'hour' else MS_DAY
    start = rng['prev_start'] if previous else rng['start']
    end = rng['prev_end'] if previous else rng['end']
    first = start + off
    first -= first % size
    out, t = [], first
    while t < end + off:
        out.append(t)
        t += size
    return out


def _series_from_rows(rows: dict, buckets: list[int]) -> list[int]:
    return [int(rows.get(b, 0)) for b in buckets]


def _traffic_series(qs, rng: dict, unit: str, buckets: list[int]) -> dict:
    rows = (
        qs.annotate(b=_bucket('created_at', unit, rng['off'])).values('b')
        .annotate(pv=Count('id'), vis=Count('visitor_id', distinct=True),
                  visits=Count('id', filter=Q(is_entry=True)))
        .order_by('b')
    )
    pv, vis, visits = {}, {}, {}
    for r in rows:
        b = int(r['b'])
        pv[b], vis[b], visits[b] = r['pv'], r['vis'], r['visits']
    return {
        'pageviews': _series_from_rows(pv, buckets),
        'visitors': _series_from_rows(vis, buckets),
        'visits': _series_from_rows(visits, buckets),
    }


def _model_series(model, field: str, rng: dict, unit: str, buckets: list[int]) -> list[int]:
    rows = (
        model.objects.filter(**{f'{field}__gte': rng['start'], f'{field}__lt': rng['end']})
        .annotate(b=_bucket(field, unit, rng['off'])).values('b')
        .annotate(n=Count('pk')).order_by('b')
    )
    return _series_from_rows({int(r['b']): r['n'] for r in rows}, buckets)


def _labels(buckets: list[int], unit: str) -> tuple[list[str], list[str]]:
    short, full = [], []
    for b in buckets:
        d = datetime.fromtimestamp(b / 1000, tz=dt_timezone.utc)
        if unit == 'hour':
            short.append(f'{d.hour:02d}:00')
            full.append(f'{d.strftime("%a")}, {_fmt_day(d)}, {d.hour:02d}:00 – {(d.hour + 1) % 24:02d}:00')
        else:
            short.append(_fmt_day(d))
            full.append(f'{d.strftime("%a")}, {_fmt_day(d)} {d.year}')
    return short, full


def _session_stats(qs) -> dict:
    """Visits, bounces and duration from one streamed GROUP BY session."""
    rows = (
        qs.values('session_id')
        .annotate(n=Count('id'), span=ExpressionWrapper(Max('created_at') - Min('created_at'), output_field=BigIntegerField()))
        .values_list('n', 'span')
    )
    sessions = bounces = multi = 0
    dur_total = 0
    for n, span in rows.iterator(chunk_size=5000):
        sessions += 1
        if n == 1:
            bounces += 1
        else:
            multi += 1
            dur_total += span or 0
    return {
        'sessions': sessions,
        'bounces': bounces,
        'bounce_rate': round(bounces / sessions * 100, 1) if sessions else 0.0,
        'avg_duration': (dur_total / multi / 1000) if multi else 0.0,
    }


def _totals(qs, start: int, end: int) -> dict:
    from api.models import User

    agg = qs.aggregate(
        pv=Count('id'),
        visitors=Count('visitor_id', distinct=True),
        members=Count('user_identifier', filter=~Q(user_identifier=''), distinct=True),
    )
    t = _session_stats(qs)
    t.update(
        pageviews=agg['pv'], visitors=agg['visitors'], members=agg['members'],
        pages_per_visit=round(agg['pv'] / t['sessions'], 2) if t['sessions'] else 0.0,
        new_accounts=User.objects.filter(created_at__gte=start, created_at__lt=end).count(),
    )
    return t


def _entry_groups(entry_qs, *fields):
    return entry_qs.values(*fields).annotate(count=Count('id'))


# --------------------------------------------------------------------------
# Sections of the report
# --------------------------------------------------------------------------

def _kpis(cur: dict, prev: dict, series: dict, growth: dict) -> list[dict]:
    def card(key, label, icon, value, raw, d, spark=None):
        sp = _spark(spark or [])
        return {'key': key, 'label': label, 'icon': icon, 'value': value, 'raw': raw, 'delta': d,
                'spark_line': sp['line'], 'spark_area': sp['area']}

    return [
        card('visitors', 'Visitors', 'group', fmt_num(cur['visitors']), cur['visitors'],
             delta(cur['visitors'], prev['visitors']), series['visitors']),
        card('visits', 'Visits', 'login', fmt_num(cur['sessions']), cur['sessions'],
             delta(cur['sessions'], prev['sessions']), series['visits']),
        card('pageviews', 'Pageviews', 'visibility', fmt_num(cur['pageviews']), cur['pageviews'],
             delta(cur['pageviews'], prev['pageviews']), series['pageviews']),
        card('bounce', 'Bounce rate', 'logout', f'{cur["bounce_rate"]:g}%', cur['bounce_rate'],
             delta(cur['bounce_rate'], prev['bounce_rate'], rate=True, lower_is_better=True)),
        card('duration', 'Visit duration', 'timer', fmt_duration(cur['avg_duration']), cur['avg_duration'],
             delta(cur['avg_duration'], prev['avg_duration'])),
        card('accounts', 'New accounts', 'person_add', fmt_num(cur['new_accounts']), cur['new_accounts'],
             delta(cur['new_accounts'], prev['new_accounts']), growth['accounts']),
    ]


def _heatmap(qs, off: int) -> dict:
    rows = (
        qs.annotate(b=_bucket('created_at', 'hour', off)).values('b')
        .annotate(n=Count('id')).order_by('b')
    )
    grid = [[0] * 24 for _ in range(7)]
    for r in rows:
        d = datetime.fromtimestamp(int(r['b']) / 1000, tz=dt_timezone.utc)
        grid[d.weekday()][d.hour] += r['n']
    top = max((v for row in grid for v in row), default=0)
    peak = None
    out_rows = []
    for di, row in enumerate(grid):
        cells = []
        for h, v in enumerate(row):
            if v and (peak is None or v > peak['count']):
                peak = {'day': DOW[di], 'hour': h, 'count': v}
            cells.append({
                'v': v, 'a': round(v / top, 2) if top else 0,
                'tip': f'{DOW[di]} {h:02d}:00 · {v:,} pageviews',
            })
        out_rows.append({'day': DOW[di], 'cells': cells})
    if peak:
        peak['label'] = f'{peak["day"]} {peak["hour"]:02d}:00–{(peak["hour"] + 1) % 24:02d}:00'
    return {'rows': out_rows, 'peak': peak, 'hours': list(range(24)), 'has_data': top > 0}


def _channels(entry_qs, total_visits: int) -> list[dict]:
    counts: dict[str, int] = {}
    for r in _entry_groups(entry_qs, 'referrer_type'):
        # An entry whose referrer is the site itself is someone coming back
        # after 30+ idle minutes: direct, not an acquisition.
        k = r['referrer_type'] if r['referrer_type'] in CHANNEL_LABELS else 'direct'
        counts[k] = counts.get(k, 0) + r['count']
    rows = [{'key': k, 'name': CHANNEL_LABELS[k], 'count': v} for k, v in counts.items()]
    return _rank(rows, total_visits)


def _sources(entry_qs, total_visits: int) -> list[dict]:
    counts: dict[tuple, int] = {}
    for r in _entry_groups(entry_qs.exclude(referrer_type__in=['direct', 'internal', '']), 'referrer_name', 'referrer_type', 'referrer_domain'):
        name = r['referrer_name'] or r['referrer_domain'] or 'Unknown'
        k = (name, r['referrer_type'], r['referrer_domain'] if r['referrer_type'] == 'referral' else '')
        counts[k] = counts.get(k, 0) + r['count']
    rows = [{'name': k[0], 'channel': k[1], 'channel_label': CHANNEL_LABELS.get(k[1], k[1]),
             'domain': k[2], 'count': v} for k, v in counts.items()]
    return _rank(rows, total_visits, 12)


def _landing(entry_qs, total_visits: int) -> list[dict]:
    counts: dict[str, int] = {}
    for r in _entry_groups(entry_qs, 'page_key'):
        counts[r['page_key']] = counts.get(r['page_key'], 0) + r['count']
    rows = []
    for key, v in counts.items():
        page = rules.classify_page(key)
        rows.append({'name': page.label, 'key': key, 'count': v})
    return _rank(rows, total_visits, 8)


def _campaigns(entry_qs, total_visits: int) -> list[dict]:
    rows = []
    for r in _entry_groups(entry_qs.exclude(utm_campaign=''), 'utm_campaign', 'utm_source', 'utm_medium'):
        sub = ' · '.join(x for x in (r['utm_source'], r['utm_medium']) if x)
        rows.append({'name': r['utm_campaign'], 'sub': sub, 'count': r['count']})
    return _rank(rows, total_visits, 8)


def _funnel(qs, cur: dict) -> list[dict]:
    app_sessions = qs.filter(page_key__startswith='/app/').values('session_id').distinct().count()
    login_sessions = qs.filter(page_key='/login/').values('session_id').distinct().count()
    base = cur['sessions']
    steps = [
        ('Visits', base),
        ('Opened the app', app_sessions),
        ('Reached sign-in', login_sessions),
        ('New accounts', cur['new_accounts']),
    ]
    out = []
    for name, n in steps:
        out.append({
            'name': name, 'count': n, 'display': fmt_num(n),
            'pct': round(n / base * 100, 1) if base else 0.0,
            'width': round(min(n, base) / base * 100, 1) if base else 0.0,
        })
    return out


def _demographics(qs) -> dict:
    from api.models import User

    members = User.objects.filter(id__in=qs.exclude(user_identifier='').values('user_identifier'))
    total = members.count()

    def group(field, label_map=None, limit=8):
        rows = []
        for r in members.values(field).annotate(count=Count('id')):
            raw = (r[field] or '').strip()
            name = (label_map or {}).get(raw.lower(), raw if raw.isupper() or raw.isdigit() else raw.title()) if raw else 'Not set'
            rows.append({'name': name, 'count': r['count']})
        merged: dict[str, int] = {}
        for r in rows:
            merged[r['name']] = merged.get(r['name'], 0) + r['count']
        return _rank([{'name': k, 'count': v} for k, v in merged.items()], total, limit)

    return {
        'total': total,
        'classes': group('class_level', {}, 10),
        'gender': group('gender', {'male': 'Male', 'female': 'Female', 'other': 'Other'}),
        'roles': group('role'),
        'provinces': group('pradesh', {}, 8),
    }


def _retention(qs, rng: dict, cur: dict) -> dict:
    from api.models import PageView

    now = int(time.time() * 1000)
    win_end = min(rng['end'], now)

    def active(days):
        return (
            PageView.objects.filter(created_at__gte=win_end - days * MS_DAY, created_at__lt=win_end, is_bot=False)
            .exclude(user_identifier='').values('user_identifier').distinct().count()
        )

    dau, wau, mau = active(1), active(7), active(30)
    prev_users = (
        PageView.objects.filter(created_at__gte=rng['prev_start'], created_at__lt=rng['prev_end'], is_bot=False)
        .exclude(user_identifier='').values('user_identifier')
    )
    returning = qs.exclude(user_identifier='').filter(user_identifier__in=prev_users).values('user_identifier').distinct().count()
    members = cur['members']
    return {
        'dau': dau, 'wau': wau, 'mau': mau,
        'stickiness': round(dau / mau * 100, 1) if mau else 0.0,
        'returning': returning, 'members': members,
        'returning_pct': round(returning / members * 100, 1) if members else 0.0,
    }


def _content(qs) -> dict:
    from api.models import Post, Resource

    page_rows = list(
        qs.values('page_key').annotate(n=Count('id'), v=Count('visitor_id', distinct=True)).order_by('-n')[:3000]
    )
    total_pv = sum(r['n'] for r in page_rows) or 0
    sections: dict[str, int] = {}
    pages = []
    for r in page_rows:
        page = rules.classify_page(r['page_key'])
        sections[page.section] = sections.get(page.section, 0) + r['n']
        pages.append({'name': page.label, 'key': r['page_key'], 'section': page.section,
                      'count': r['n'], 'visitors': r['v'], 'visitors_display': fmt_num(r['v'])})
    top_pages = _rank(pages, total_pv, 12)

    def top_titles(page_key, model, href, limit=6):
        rows = list(qs.filter(page_key=page_key).values('path').annotate(n=Count('id')).order_by('-n')[:limit * 3])
        ids = {}
        for r in rows:
            ident = r['path'].strip('/').split('/')[-1]
            ids[ident] = ids.get(ident, 0) + r['n']
        titles = dict(model.objects.filter(pk__in=list(ids)).values_list('pk', 'title'))
        out = [{'name': (titles[i] or 'Untitled')[:90], 'count': n, 'id': i, 'href': href.format(i)}
               for i, n in ids.items() if i in titles]
        return _rank(out, sum(ids.values()), limit)

    return {
        'sections': _rank([{'name': k, 'count': v} for k, v in sections.items()], total_pv, 10),
        'pages': top_pages,
        'threads': top_titles('/app/forum/post/*/', Post, '/app/forum/post/{}/'),
        'resources': top_titles('/app/resource/*/', Resource, '/app/resource/{}/'),
    }


def _audience(entry_qs, total_visits: int) -> dict:
    def grouped(field, label=None, limit=None, skip_blank=True):
        counts: dict[str, int] = {}
        for r in _entry_groups(entry_qs, field):
            raw = r[field] or ''
            if skip_blank and not raw:
                continue
            name = label(raw) if label else raw
            counts[name] = counts.get(name, 0) + r['count']
        return _rank([{'name': k, 'count': v} for k, v in counts.items()], total_visits, limit)

    os_names = {'ios': 'iOS', 'mac': 'macOS', 'chromeos': 'ChromeOS', 'android': 'Android',
                'windows': 'Windows', 'linux': 'Linux'}
    devices = grouped('device_class', lambda v: v.capitalize())
    geo_known = entry_qs.exclude(country='').count()
    member_visits = entry_qs.exclude(user_identifier='').count()
    return {
        'devices': devices,
        'os': grouped('platform', lambda v: os_names.get(v, v.capitalize()), 8),
        'browsers': grouped('browser', None, 8),
        'surfaces': grouped('source', lambda v: 'Mobile app' if v == 'app' else 'Website'),
        'countries': grouped('country', None, 10),
        'cities': grouped('city', None, 10),
        'geo_known_pct': round(geo_known / total_visits * 100) if total_visits else 0,
        'members_visits': member_visits,
        'guest_visits': max(total_visits - member_visits, 0),
        'members_pct': round(member_visits / total_visits * 100, 1) if total_visits else 0.0,
        'guests_pct': round((total_visits - member_visits) / total_visits * 100, 1) if total_visits else 0.0,
    }


def _donut(rows: list[dict]) -> str:
    """CSS conic-gradient stops for a share chart."""
    if not rows:
        return 'conic-gradient(var(--md-surface-container-high) 0 100%)'
    stops, acc = [], 0.0
    for i, r in enumerate(rows):
        end = acc + r['pct']
        stops.append(f'var(--an-c{(i % 6) + 1}) {acc:.2f}% {end:.2f}%')
        acc = end
    if acc < 99.9:
        stops.append(f'var(--md-surface-container-high) {acc:.2f}% 100%')
    return 'conic-gradient(' + ', '.join(stops) + ')'


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def build_report(rng: dict, source: str = 'all', *, use_cache: bool = True) -> dict:
    ck = f'an:report:v3:{rng["start"]}:{rng["end"]}:{source}'
    if use_cache:
        hit = cache.get(ck)
        if hit is not None:
            return hit

    from api.models import PageView, Post, Reply, Resource, User

    unit = rng['unit']
    qs = _base(rng['start'], rng['end'], source)
    prev_qs = _base(rng['prev_start'], rng['prev_end'], source)
    entry_qs = qs.filter(is_entry=True)

    cur = _totals(qs, rng['start'], rng['end'])
    prev = _totals(prev_qs, rng['prev_start'], rng['prev_end'])

    buckets = _bucket_starts(rng, unit)
    prev_buckets = _bucket_starts(rng, unit, previous=True)
    short, full = _labels(buckets, unit)
    series = _traffic_series(qs, rng, unit, buckets)
    prev_series = _traffic_series(prev_qs, {**rng, 'start': rng['prev_start'], 'end': rng['prev_end']}, unit, prev_buckets)

    growth_defs = (
        ('accounts', 'New accounts', 'person_add', User, 'created_at'),
        ('threads', 'Forum threads', 'forum', Post, 'created_at'),
        ('resources', 'Resources shared', 'library_books', Resource, 'added_at'),
        ('replies', 'Replies', 'chat_bubble', Reply, 'created_at'),
    )
    growth_series, growth_cards = {}, []
    for key, label, icon, model, field in growth_defs:
        s = _model_series(model, field, rng, unit, buckets)
        growth_series[key] = s
        prev_total = model.objects.filter(**{f'{field}__gte': rng['prev_start'], f'{field}__lt': rng['prev_end']}).count()
        total = sum(s)
        growth_cards.append({'key': key, 'label': label, 'icon': icon, 'total': total,
                             'value': fmt_num(total), 'delta': delta(total, prev_total), 'series': s,
                             'bars': _bars(s, full)})

    total_visits = cur['sessions']
    channels = _channels(entry_qs, total_visits)
    audience = _audience(entry_qs, total_visits)
    retention = _retention(qs, rng, cur)

    legacy = PageView.objects.filter(
        created_at__gte=rng['prev_start'], created_at__lt=rng['end'], visitor_id='', is_bot=False
    ).exists()

    report = {
        'range': rng,
        'source': source,
        'has_data': cur['pageviews'] > 0,
        'needs_backfill': legacy,
        'kpis': _kpis(cur, prev, series, growth_series),
        'totals': cur,
        'trend': {
            'unit': unit, 'labels': short, 'fulls': full, **series,
            'prev': {k: v for k, v in prev_series.items()},
            'prev_label': 'Previous period',
        },
        'growth': growth_cards,
        'heatmap': _heatmap(qs, rng['off']),
        'channels': channels,
        'channels_donut': _donut(channels),
        'sources': _sources(entry_qs, total_visits),
        'landing': _landing(entry_qs, total_visits),
        'campaigns': _campaigns(entry_qs, total_visits),
        'funnel': _funnel(qs, cur),
        'audience': audience,
        'devices_donut': _donut(audience['devices']),
        'demographics': _demographics(qs),
        'retention': retention,
        'content': _content(qs),
        'devices': report_devices.build(rng, source),
        'generated_at': int(time.time() * 1000),
    }
    report['chart_json'] = {
        'trend': report['trend'],
        'growth': {c['key']: c['series'] for c in growth_cards},
        'labels': {'short': short, 'full': full},
    }
    if use_cache:
        cache.set(ck, report, CACHE_SECONDS)
    return report


def daily_rows(rng: dict, source: str = 'all') -> list[dict]:
    """Rows for the CSV export: one per day (or hour for 'today')."""
    from api.models import Post, Reply, Resource, User

    unit = rng['unit']
    qs = _base(rng['start'], rng['end'], source)
    buckets = _bucket_starts(rng, unit)
    traffic = _traffic_series(qs, rng, unit, buckets)
    accounts = _model_series(User, 'created_at', rng, unit, buckets)
    threads = _model_series(Post, 'created_at', rng, unit, buckets)
    resources = _model_series(Resource, 'added_at', rng, unit, buckets)
    replies = _model_series(Reply, 'created_at', rng, unit, buckets)
    out = []
    for i, b in enumerate(buckets):
        d = datetime.fromtimestamp(b / 1000, tz=dt_timezone.utc)
        out.append({
            'period': d.strftime('%Y-%m-%d %H:00') if unit == 'hour' else d.strftime('%Y-%m-%d'),
            'visitors': traffic['visitors'][i], 'visits': traffic['visits'][i],
            'pageviews': traffic['pageviews'][i], 'new_accounts': accounts[i],
            'threads': threads[i], 'resources': resources[i], 'replies': replies[i],
        })
    return out
