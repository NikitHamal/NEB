# Backend: what the desktop app uses, and what was added

The desktop app talks to the **same Django API as the Android app** (`backend_python/api`, base URL
`https://nebians.consica.com.np/`). Nothing about the existing endpoints changed. One feature was added.

## New: browser hand-off sign-in (Google / GitHub on desktop)

A desktop binary can't hold an OAuth client secret or reliably receive a custom-scheme redirect on every OS,
and the Android `idToken` / `code` flows need Google/GitHub client registrations tied to the Android app.
The *website* already signs people in with Google, GitHub and email — so the desktop asks the website to vouch for the user.

```
desktop                              backend                              browser
verifier = 32 random bytes (never leaves the process)
challenge = b64url(sha256(verifier))
POST /api/auth/desktop/start/ {challenge, device}  ->  {state, loginUrl, expiresIn, interval}
open loginUrl ------------------------------------------------------------>  /desktop-auth/?state=…
                                                                 signed out? -> /login/?next=… (Google / GitHub / email)
                                                                 consent page "Sign in to NEBians Desktop?"  [Cancel] [Allow]
                               cache[state] = approved(user id)  <-- POST /desktop-auth/ (session + CSRF)
POST /api/auth/desktop/poll/ {state, verifier}  -> 202 pending … -> 200 {authToken, isNewUser, user}
```

| File | Role |
|---|---|
| `api/desktop_auth.py` | protocol core: create / approve / deny / redeem, PKCE checks, sanitising |
| `api/views_desktop_auth.py` | `POST /api/auth/desktop/start/`, `POST /api/auth/desktop/poll/` |
| `web/views_desktop_auth.py` + `web/templates/web/desktop_auth.html` | consent page `/desktop-auth/` |
| `api/test_desktop_auth.py` | 10 tests (flow, replay, wrong verifier, malformed input, deny, banned user, CSRF, login redirect) |

### Security properties
* The bearer token never appears in a URL, redirect, browser, log line or the cache — only the user id is parked, and only after an authenticated, **CSRF-protected** POST from the signed-in web session.
* Collecting the token needs the `verifier`, which never leaves the desktop process. Someone who sees the login URL (only `state`) can't redeem it. Wrong verifiers are refused without consuming the request.
* `state` = 256 bits, valid 10 minutes, consumed on first successful poll, can be approved once (no re-approval / hijack).
* The token is minted by `issue_auth_token` at redemption time (hashed at rest like every other session); banned users get 403.
* Both API endpoints use the existing `AuthRateThrottle`. The consent page sends `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store` (clickjacking / leakage).
* Device names are stripped to a safe charset before being displayed.

### Deployment notes
* **The cache must be shared between workers** (Redis — already the production default in `settings.py`). With the per-process `LocMemCache` fallback, `start` and `poll` could land on different workers.
* No new settings, migrations, or OAuth console changes are needed: it reuses the website's existing Google/GitHub login.
* `loginUrl` is built from `SITE_URL`/`PUBLIC_SITE_URL` if set, otherwise from the request host.

### Tested for real
`scripts/e2e-handoff.py` + `cargo test live_handoff -- --ignored` run the real Rust client against a real `runserver`: signed-out visitor is redirected to login → the site's session is established → consent page → Allow → the client receives the session → that bearer token is accepted by `api/notifications/unread-count/` → a bogus token is rejected → a second redemption is refused. (Output in BUILD.md.)

## Existing endpoints the desktop app uses
`auth/email/{login,signup,verify,resend,forgot,reset-password}/`, `auth/change-password/`, `auth/logout/`,
`users/profile/` (POST) & `users/profile/<username>/` (GET), `users/check-username/`,
`posts/` (GET/POST), `posts/<id>/` , `posts/<id>/like/`, `posts/<id>/replies/` (GET/POST), `posts/<id>/view/`,
`bookmarks/toggle/`, `notifications/`, `notifications/mark-read/`, `notifications/unread-count/`.
Response shapes were taken from the Android `ApiService.kt` DTOs. Point the app at another deployment with
`NEB_API_BASE=https://your-host/ nebians`.
