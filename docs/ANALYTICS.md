# Analytics (first-party, cookie-less)

Page views are recorded by our own code. Nothing is sent to a third party and no
cookie is set. Admin reads them at **Admin > Analytics** (`/admin/analytics/`).

```
nebians/analytics/rules.py    pure rules: bots, referrers, page keys, visitor ids
nebians/analytics/events.py   request -> event dict (middleware + /api/analytics/track/)
nebians/analytics/writer.py   bounded queue + worker thread: sessions, geo, INSERT
nebians/analytics/report.py   everything the admin page and CSV export read
web/views_admin_analytics.py  thin view: range + source filter, staff guard, CSV
web/templates/admin_panel/analytics.html + analytics/_kpi|_rank|_delta.html
web/static/web/js/admin-analytics.js   SVG trend chart, KPI<->chart link, scroll-spy
web/static/web/css/admin/03-analytics.css   all styles, scoped under `.an`
api/management/commands/backfill_analytics.py   migrate pre-rebuild rows
```

## Definitions

| Term | Meaning |
| --- | --- |
| Pageview | one successful, full-page HTML GET by a non-bot. Assets, `/api/`, `/admin/`, HTMX fragments and prefetches never count. Staff browsing is excluded. |
| Visitor | distinct `visitor_id`. Members are one stable hashed id. Logged-out visitors get a hash of (day, IP, user agent) that **rotates daily**, so a returning guest on another day counts again. |
| Visit | a session: one visitor, hits no more than 30 minutes apart. |
| Bounce | a visit with exactly one pageview. |
| Duration | last hit minus first hit, averaged over visits with 2+ pageviews. |
| Member | a signed-in account (`user_identifier`). |

Days are cut at local midnight in `settings.TIME_ZONE` (Asia/Kathmandu), not UTC.
Every change is compared with the previous period of equal length.

## Privacy

Raw IP, user agent and full URL are never stored. Referrers keep host + path only
(no query string). Country comes from edge headers (Cloudflare etc.). The remote
IP lookup is **off** unless `ANALYTICS_GEO_REMOTE=1`, because it would send every
visitor's IP to a third party.

## Request path and why it is shaped this way

`PageViewTrackingMiddleware` builds an event and calls `writer.submit()`, a
non-blocking queue put. A daemon worker drains the queue and does the INSERT, so
a slow database costs page views, never latency. The queue is bounded (512) and
drops on overflow.

Two production bugs this design now guards against (both have regression tests):

1. **Forked workers (LiteSpeed LSAPI, gunicorn --preload, uWSGI).** A forked child
   inherits the `Thread` object (`is_alive()` can still be True) but not the OS
   thread, and the inherited queue lock may belong to a thread that no longer
   exists. `writer._ensure_worker()` records the owning pid and rebuilds the
   lock, the queue and the thread when the pid changes. Symptom of regressing:
   the queue fills and nothing is ever written, with no error.
2. **Anonymous page cache.** `AnonPageCacheMiddleware` answers repeat hits on `/`,
   library, forum, news and FAQ with `X-Page-Cache: hit`. Those hits used to be
   skipped by tracking, which hid most logged-out traffic. They are counted now.

"Online now" and presence heartbeats are gone entirely (endpoints, model, the web
heartbeat script). Do not reintroduce a per-user polling heartbeat.

## Admin page

Filters live in the query string, so every view is linkable:
`?range=today|7d|30d|90d` or `?from=YYYY-MM-DD&to=YYYY-MM-DD` (max 366 days),
`&source=all|web|app`, `&refresh=1` to bypass the 60 s report cache.
Sections: Overview (KPIs, trend with previous-period overlay, hour x weekday heatmap,
visit funnel), Acquisition, Audience, Members, Content, Community growth. Community
growth comes from database counts and is shown even when there are no page views.
The CSV export (`/admin/analytics/export/csv/`) uses the same daily series as the
page, so the two cannot disagree.

The report is one dict from `report.build_report()`. To add a metric: compute it
there, render it with `_rank.html` / `_kpi.html`, add a test in `ReportTests`.
The cache key is versioned (`an:report:v2`); bump it when the report shape changes.

## Deploying

```
git pull && python manage.py migrate        # 0156_analytics_rebuild
python manage.py backfill_analytics         # once; safe to re-run
# restart the app (touch tmp/restart.txt on LiteSpeed/Passenger)
```
The admin page shows a notice while un-migrated rows exist in the selected range.

## Tests

```
cd backend_python
DB_ENGINE=sqlite SECRET_KEY=x DEBUG=1 python manage.py test api.test_admin_analytics web.test_page_cache
```
