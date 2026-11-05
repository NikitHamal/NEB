# Insights, devices, polls: task status

Brief: upgrade admin analytics, per-post insights (web + Android), private device signals, polls in comments with member-added options, new m3x poll cards on web and Android. Nothing is built locally; Android is verified by the GitHub Actions run.

## Done
- [x] Backend core (`api/polls.py`, `api/post_reach.py`, `api/post_insights.py`, `api/signals.py`, migration `0160`): comment polls, add-an-option, retract vote, unique daily post views, impressions, private device signals, insights payload. Tests: `api.test_post_insights_polls`.

- [x] Web: m3x poll card (`_poll_card.html`, `poll-card.js`, `m3x/app-poll.css`) on post page, feed rows and comments; comment poll builder; insights sheet (`post-insights.js`, menu item "See insights"); view/impression beacons (`post-reach.js`). Tests: `web.test_polls_insights`.

- [x] Admin analytics: Devices and sign-ups (by device, system, app, activation, interactions matrix, app versions/models, recent sign-ups), Posts and polls (reach, readers by device, poll stats).

- [x] Android (session 9, verified by the GitHub Actions run, never built locally):
  - `DeviceSignalInterceptor` sends one `X-Neb-Device` header (app, build, OS, SDK, model, brand, screen, dpi, language, timezone, ABI, tablet). Only to our own host. No advertising id, no serial.
  - `NebPollCard` (m3x): tonal 28 dp card, choice rows, result bars with the leading option in the stronger container, quiz right/wrong tones, "Add option" for open polls, "Change vote". `NebPollPreview` on feed rows.
  - Comment poll builder (`CommentPollBuilder`) in the main comment bar, with "Let others add options"; the post poll builder got the same switch.
  - Comment polls render inside `CommentCard` through the same view model as the post poll.
  - `PostInsightsScreen` (route `forum/post/{postId}/insights`): KPIs with change, views per day, tips, audience, sources, devices and actions by device, time on post, hours, countries, poll results, all-time. Opened from "See insights" in the post menu (owner only).
  - Reach beacons: view with surface hint and dwell on leave (`PostReachHints`), batched feed impressions (`TrackPostImpressions`) in Home and Forum.

## Next
- [x] CI run 42034617550 (`assembleModernRelease` and bundle) passed on a74ce61.
- [ ] On-device visual pass of the poll card and insights screen (needs the app-screens workflow).
