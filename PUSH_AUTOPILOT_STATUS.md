# Push, library autopilot and reach analytics: status

Single status doc for this task. Read it first, update it in place, do not start a second one.
Design rules: M3 Expressive, no shadows, no emoji, no gradients, no backgrounds on role badges.

## Shipped (origin/main)

| Commit | What |
| --- | --- |
| c1cd893 | Push engine: `PushCampaign`, `PushDelivery`, `PushSettings`, `ResourceAlert`; `api/push_engine.py`, `api/push_audience.py`, `api/resource_alerts.py` (class + subject match, digest per person, daily cap, quiet hours, settle window, opt-out); `push_tick` command; prefs + push-opened endpoints |
| ff7ceea | Admin Push: compose (live audience + phone preview, test send, schedule), History (delivery / open / failure analytics), campaign detail funnel, Autopilot (rules, queue, by-hand announce) |
| 96619a2 | `notify_new_resources` switch on web settings and Android settings; push taps reported for open rate; `library_alerts` channel |

## Reach + insights (shipped)

| Commit | What |
| --- | --- |
| 87146b0 | Icon font subset rebuilt (`edit_square`, `phone_android`, `auto_mode` were missing from the admin push pages) |
| 2dc768a | `api/resource_reach.py` (one row per viewer per local day, reads / downloads / shares, list impressions; `view_count` and `download_count` only move for a new non-owner, non-bot viewer-day; a tap from a push marks the `PushDelivery` clicked), `api/resource_insights.py` (`build()` per resource, `overview()` for an uploader plus their posts), API + web endpoints, `resource-reach.js` beacons, `resource-insights.js` sheet, "See insights" on your own resource, "Library insights" on Analytics, autopilot push URL now `/app/reader/<id>/?src=push` |
| 149cb6c | Admin Analytics "Library" section (`nebians/analytics/report_library.py`), post reach rows survive racing requests, report cache `v4` |
| this one | Android beacons (view with login, read, download) and docs |

Endpoints: `GET /api/resources/<id>/insights/?days=7|30|90` (uploader or staff), `GET /api/uploads/insights/` (signed-in member),
`POST /api/resources/<id>/view/` (surface, src, dwell_ms), `POST /api/resources/<id>/action/` (read|download|share),
`POST /api/resources/impressions/`; web twins under `/ajax/resource/...` and `/ajax/uploads/insights/`.
Downloads only happen in the app (the web Download button opens the get-the-app dialog), so `downloads` is an app number.

## Rules to keep

* Autopilot only sees resources that go live from now on (post_save hook). The 92 older uploads have no `ResourceAlert`
  row; announce them by hand in Admin > Push > Autopilot > "Never announced" (digest per person, caps respected or not
  as you choose in the preview).
* Opt-out is `User.notify_new_resources` (default True), switch on web Settings and Android Settings.
* Never show a person's name next to a delivery or a view. Aggregates only.

## Verify

```
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x PYTHONPATH=.
python3 manage.py test api.test_push_autopilot api.test_resource_reach web.test_admin_push_pages
```

## Open / next

* Android has no insights screen for uploaders yet. The payloads are ready (`/api/uploads/insights/`, `/api/resources/<id>/insights/`);
  mirror `ui/screens/analytics/PostInsightsScreen.kt`. Never build locally, push and read the GitHub Actions run.
* The app does not send the list surface (`library`, `search`) or dwell time for resources yet, only view / read / download.
* Share taps in the app are not reported (web reports them).
