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

(see below, updated as it ships)

## Milestone 3: resource analytics

(see below, updated as it ships)

## Verify

```
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x PYTHONPATH=.
python3 manage.py test api.test_push_autopilot api.test_resource_reach web.test_admin_push_pages
```
