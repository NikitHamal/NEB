# Push, library autopilot and reach analytics: status

Single status doc for this task. Read it first, update it in place, do not start a second one.
Design rules: M3 Expressive, no shadows, no emoji, no gradients, no backgrounds on role badges.

## Shipped (origin/main)

| Commit | What |
| --- | --- |
| c1cd893 | Push engine: `PushCampaign`, `PushDelivery`, `PushSettings`, `ResourceAlert`; `api/push_engine.py`, `api/push_audience.py`, `api/resource_alerts.py` (class + subject match, digest per person, daily cap, quiet hours, settle window, opt-out); `push_tick` command; prefs + push-opened endpoints |
| ff7ceea | Admin Push: compose (live audience + phone preview, test send, schedule), History (delivery / open / failure analytics), campaign detail funnel, Autopilot (rules, queue, by-hand announce) |
| 96619a2 | `notify_new_resources` switch on web settings and Android settings; push taps reported for open rate; `library_alerts` channel |

## This session (reach + insights)

* `api/resource_reach.py`: one row per viewer per local day (`ResourceReach`), list impressions (`ResourceImpression`),
  read / download / share flags. `Resource.view_count` and `download_count` only move for a new (resource, viewer, day)
  that is not the uploader and not a bot. A tap from a push (`?src=push`) marks the `PushDelivery` as clicked.
* `api/resource_insights.py`: `build()` per resource and `overview()` across an uploader's resources, same aggregate-only
  rules as post insights. Staff see every resource; uploaders only their own.
* Endpoints: `GET /api/resources/<id>/insights/`, `GET /api/uploads/insights/`, `POST /api/resources/<id>/view/`
  (surface, dwell_ms), `POST /api/resources/<id>/action/` (read|download|share), `POST /api/resources/impressions/`;
  web twins under `/ajax/resource/...`.
* Web: "See insights" on a resource you uploaded, `resource-reach.js` beacons, `resource-insights.js` sheet (reuses `.ins-*`).
* Admin Analytics: library reach section.
* Autopilot push URL now `/app/reader/<id>/?src=push` (the old `/reader/` path went through a legacy redirect).

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

* Android beacons for resource reach (view/dwell/download) are sent from the reader; the uploader insights screen in the app
  is still the web sheet only.
