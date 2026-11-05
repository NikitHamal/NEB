# Insights, devices, polls: task status

Brief: upgrade admin analytics, per-post insights (web + Android), private device signals, polls in comments with member-added options, new m3x poll cards on web and Android. Nothing is built locally; Android is verified by the GitHub Actions run.

## Done
- [x] Backend core (`api/polls.py`, `api/post_reach.py`, `api/post_insights.py`, `api/signals.py`, migration `0160`): comment polls, add-an-option, retract vote, unique daily post views, impressions, private device signals, insights payload. Tests: `api.test_post_insights_polls`.

- [x] Web: m3x poll card (`_poll_card.html`, `poll-card.js`, `m3x/app-poll.css`) on post page, feed rows and comments; comment poll builder; insights sheet (`post-insights.js`, menu item "See insights"); view/impression beacons (`post-reach.js`). Tests: `web.test_polls_insights`.

- [x] Admin analytics: Devices and sign-ups (by device, system, app, activation, interactions matrix, app versions/models, recent sign-ups), Posts and polls (reach, readers by device, poll stats).

## Next
- [ ] Android: device header, poll card, comment poll builder, insights screen, view beacons

- docs/ANALYTICS.md covers private signals, reach/insights and polls.
