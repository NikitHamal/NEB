# Performance and realtime status

Single status doc for the "faster, lighter, realtime without Cloudflare" task. Pick up here; do not start a second doc.

## Realtime: Ably over SSE (no tunnel, no socket on our server)

Why: cPanel + LiteSpeed/LSAPI cannot proxy WebSockets, other apps share the box, and the Cloudflare quick tunnel
rotated its URL and died with the account. Now the server never holds a connection.

```
Django (any worker) --queue--> daemon thread --1 batched HTTPS POST--> Ably REST
Browser / Android  <---------- SSE (EventSource / OkHttp) ----------- Ably
Browser / Android  --GET /api/realtime/config/--> Django (HMAC only, no DB, no network)
```

- `api/realtime_ably.py`: self-signed Ably JWT (HS256, subscribe-only, `forum.public`, `post.*`, `resource.*`,
  `resource_request.*`, plus `user.<id>` for the signed-in user), non-blocking batched publisher (bounded queue 400,
  80 per POST, 4s timeout, circuit breaker opens 30s after 3 failures, thread re-created after an LSAPI fork).
- `api/realtime.py::_send` publishes to Ably first and skips Channels/Redis unless `WS_PUBLIC_URL` is set.
- `GET /api/realtime/config/` returns `{transport: "ably-sse"|"ws"|"none", sse_url, token, expires_in, user_channel, ws_url}`.
  Session cookie and `Authorization: Bearer` both resolve the user.
- `web/static/web/js/realtime.js`: no channels subscribed = no request at all; same-tick subscribes share one stream;
  a tab hidden for 30s drops its stream and resumes with `lastEvent`; token renewed at 80% of its life; backoff with jitter.
  Same `WS.subscribe/on/onHealth` API as before, so no page changed. Fires `neb:realtime-resync` after a gap > 110s.
- Android: `RealtimeClient.kt` reads the same config, streams SSE with OkHttp, restarts the stream when the channel set
  changes. Old WebSocket path stays for a configured `ws_url`.
- Canvas / study-space collaboration still needs a real WebSocket host (`WS_PUBLIC_URL`); it is not on Ably.

### To switch it on (one step, on the server)

1. Create a free Ably account, one app, and copy the root API key (`appId.keyId:secret`).
2. Put `ABLY_API_KEY=...` in `nebians_api/.env`, `touch tmp/restart.txt`. Nothing else.
3. Retire the old processes: remove the `@reboot` cron lines for `daphne` and `cloudflared`, `pkill` both once
   (frees roughly 100+ MB RAM and a Python process), delete `logs/cloudflared.log`.
Without the key everything stays quiet: pages are server-rendered and the unread badge keeps its existing poll.

Free plan limits (Ably): 6M messages/month, 200 concurrent connections, 200 channels. Only signed-in readers or pages
that subscribe open a stream, hidden tabs release theirs.

### More room: several free Ably apps (built, session 3)

Put more keys in `ABLY_API_KEYS=appA.k1:secret,appB.k2:secret` (comma separated; `ABLY_API_KEY` is still read and
merged, duplicates dropped). N apps = N x 200 connections and N x 6M messages.

- Publishing: every batch goes to every app (one POST each, in the one publisher thread), each app has its own circuit
  breaker, so a dead app never delays or drops events for the others.
- Reading: `/api/realtime/config/` signs the token with ONE app, picked by a stable hash of the user (or ip + agent for
  guests), and returns `shard` / `shards`. Same person, same app, so reconnects do not shuffle.
- Failover: `?shard=<n>` forces an app. `realtime.js` (and `RealtimeClient.kt`) move to the next app when the stream is
  refused (quota, outage) or errors 3 times without opening, and stay on the one that works.
- Cost: messages are published N times, but each app counts only its own, so the quota is per app, not shared.
- If Ably as a whole is the problem, a second provider (Pusher Channels / Supabase Realtime) fits behind
  `api/realtime_ably.py`: same publish-on-HTTP, subscribe-direct shape.

### Live behaviour added on top

- `neb:realtime-resync` (fired after a gap > 110s) now has listeners: base re-reads the unread badge, home and thread
  offer a one-tap refresh through `NebToast`. Before this nothing listened and a long hidden tab silently missed events.
- Home feed: `post.created` from someone else offers "New post / N new posts - Show" (never moves what you are reading),
  `post.deleted` removes the card.

## Fonts and first paint

Cause of "default font first, Poppins later": static files were served `max-age=60` with no versioned URLs, so every
visit revalidated every font and stylesheet; only 400/600 were preloaded (500/700 are used far more); the icon-font
preload URL differed from the CSS URL (fetched twice); KaTeX CSS and JS came from jsdelivr and blocked rendering.

- `nebians/storage.py` + `nebians/static_headers.py`: `{% static %}` adds `?v=<content hash>` to js/css; fonts stay
  un-versioned (preload must match CSS byte for byte, rename a font to change it); WhiteNoise sends
  `immutable, 1 year` for js/css/fonts/vendor, 7 days + stale-while-revalidate for images. Still plain filenames, no
  manifest, so the multi-worker LSAPI 404 problem cannot return.
- `base.html` preloads Poppins 400/500/600/700 latin and the icon font with the same URLs `fonts.css` requests.
- `Poppins Fallback` (Arial with size-adjust 112%, ascent/descent/line-gap overrides) is in the `--body/--display` stacks so
  a late swap does not move text. `poppins.css` is the Poppins-only face file for pages that do not load `fonts.css`.
- KaTeX is self-hosted (`web/vendor/katex`, all 19 woff2 + mhchem + auto-render), scripts are `defer`. No third-party
  host in `<head>` any more. canvas, desktop auth and admin no longer pull Poppins from Google.
- Brotli added to `requirements.txt` so `collectstatic` writes `.br` next to `.gz`.
- Per request: the WS URL is no longer read from Redis (it ran for every request including static).
- Tests: `web/test_static_cache.py`, `api/tests_realtime_ably.py`.

## Payload and cache weight (session 3)

- `nebians/minify.py` runs in `VersionedStaticFilesStorage.post_process` (i.e. `collectstatic`), rewriting STATIC_ROOT
  copies with rcssmin/rjsmin before the .gz/.br are written: CSS -28%, JS -14% compressed, sources untouched, vendor and
  `.min.` skipped, `STATIC_MINIFY=0` turns it off. Every minified script was `node --check`ed.
- Inline scripts were re-sent with every page view: home (84 KB), create post (45), whisper (67), tts (35), result checker
  (30) now live in `static/web/js/pages/` (versioned, immutable). Home HTML 110 KB -> 27 KB, which also makes the anon page
  cache 4x smaller in RAM. Inline CSS of whisper / tts / result checker moved to `css/pages/*-page.css`.
  `web/test_inline_budget.py` fails on any new inline script over 30 KB (known remaining: forum_post, profile,
  edit_profile, listed with caps so they can only shrink).
- 46 below-the-fold `<img>` tags got `loading="lazy" decoding="async"` (profile photo, login, canvas, study space,
  avatar editor excluded on purpose).
- Whisper / TTS pages: remixicon self-hosted (`web/vendor/remixicon`, woff2 only), Google Fonts link removed (base already
  ships Poppins).

## Not done / next candidates

- Material Symbols on canvas and admin still load from Google (needs the variable FILL axis; the local cut is static).
- `forum_post.html` (66 KB), `profile.html` (37 KB), `edit_profile.html` (27 KB), `subject_page.html`, `notifications.html` still carry big inline scripts with template tags: extract by passing the few values as `data-*` on `<body>` / a JSON script.
- Transformers.js (tts) and html2canvas (result checker) still load from jsdelivr, only on those tool pages and after click.
- Not verified against a live Ably account (no key in the sandbox): publisher and token are unit-tested, the SSE wire format
  follows Ably's SSE docs. First thing to check after setting the key: open /forum in two tabs, like a post, watch the other.
- Shard failover (server, web, Android) is unit-tested on the server only; the Android part has no Gradle build either.
- Android change was written without a Gradle build in the sandbox; CI `build-release` will compile it.
