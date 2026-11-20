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

## Android insights and richer beacons (this session)

* `ui/screens/analytics/ResourceInsightsScreen.kt` + `ResourceInsightsViewModel.kt` + `data/api/ResourceInsightsModels.kt`: one screen for both
  `GET /api/resources/<id>/insights/` (opened from the owner's "See insights" item in the resource menu) and `GET /api/uploads/insights/`
  (the "Library insights" button on Analytics). Route `library/insights?resourceId=` (optional arg), opened through `ResourceInsightsNav.open`.
  KPIs with change vs the previous period, tips, opens per day, list-to-download funnel, push alert reach, per-upload table, posts block,
  audience, classes, subjects, surfaces, devices, time on page, busiest hour, all-time totals.
* Resource detail now sends the surface (home, library, search, profile, related; taken from the previous nav entry), a dwell beacon when the
  screen is left (the server keeps the longest dwell of the day) and a share beacon on the share sheet.
* Not built locally (the Android build is too heavy for the sandbox): the GitHub Actions run is the check.

## Open / next

* The app sends list impressions for the Library grid (see `NOTIFICATIONS_ANALYTICS_STATUS.md`); search cards still do not.
* Resources opened from a push notification arrive with the notification surface only on web (`?src=push`); the app reports push taps
  through the push-opened endpoint.
