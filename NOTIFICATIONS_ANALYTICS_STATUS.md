# Notifications and analytics: status

Single status doc for the autopilot / push console / resource analytics task. Read it first, update it in place.
Earlier shipped work is described in `PUSH_AUTOPILOT_STATUS.md` (engine, reach tables, Android insights); this file tracks what this task added on top.
Design rules: M3 Expressive, no shadows, no emoji, no gradients, no backgrounds on role badges, no helper text.

## Found already shipped (do not rebuild)

* `PushCampaign`, `PushDelivery`, `PushSettings`, `ResourceAlert` (`api/models.py`), `api/push_engine.py`, `api/push_audience.py`, `api/resource_alerts.py`.
* Smart coalescing: autopilot settles for N quiet minutes, then one digest per person per round; daily cap per person; quiet hours; opt-out `User.notify_new_resources` (default True) on web Settings and Android Settings, API `GET/PATCH /api/me/notification-prefs/`.
* Resources that predate the autopilot have no `ResourceAlert` row, so the 92 earlier uploads are never auto-fired.
* Open tracking: inbox open (web) via `mark_opened`, push tap (Android) via `POST /api/push/opened/`, resource open with `?src=push` marks the delivery clicked. First open wins (deduplicated).
* Resource reach: `ResourceReach` one row per viewer per local day, `ResourceImpression`, `api/resource_insights.py`, web sheet `resource-insights.js`, Android `ResourceInsightsScreen`.

## Milestone 1: autopilot and opt-out

Done this task:

* `resource_alerts.announce_unnotified()` and `unannounced_ids()`: one tap batch over every live, never announced resource (digest per person, no cap, no quiet hours).
* Admin Push > Autopilot: "Announce unnotified library uploads" card with confirm dialog (`action=announce_unnotified`).
* Digest copy names the level: "6 new Physics resources added for Class 12".
* Tests: `api.test_push_autopilot` (batch announce, digest title, backlog never auto sent).

## Milestone 2: console and history

Done this task:

* Compose (`admin_panel/push_notifications.html`, `js/admin-push.js`): audience modes All users, Class or level, Subject, Platform (Android app / Web only), Unnotified library. Hidden mode fields are disabled so they are never sent; live recipient tiles (people, Android, web only) update on every change; the unnotified mode shows the unannounced resource count and a sample digest, and its button reads Announce. No inline styles, no helper text.
* Trigger labels: `manual` Manual Admin, `library` Batch Digest, `autopilot` Autopilot Library (`push_stats.KIND_LABEL`).
* History (`push_history.html`): per campaign time, trigger, target class and subject, targeted, sent, delivered, failed, opened, clicked, CTR, resource views, status. Numbers come from `push_stats.rollup()` over `PushDelivery` rows. Sent = push or inbox row handed over, delivered = push accepted or inbox row present, CTR = clicked over delivered, views = notification-surface opens of the campaign's resources after it started.
* Tracking: Android tap `POST /api/push/opened/`; web inbox read marks opened; web inbox links for campaign rows now carry `?src=push` so the resource open counts as a notification view and marks the delivery clicked. Opens and clicks are first-write-wins per person.
* Tests: `web.test_admin_push_pages` (modes, platform split, batch, history, source link).

## Milestone 3: resource analytics

(see below, updated as it ships)

## Verify

```
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x PYTHONPATH=.
python3 manage.py test api.test_push_autopilot api.test_resource_reach web.test_admin_push_pages
```
