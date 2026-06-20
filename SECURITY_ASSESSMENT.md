# NEBians Security Assessment Report
**Target:** https://nebians.consica.com.np/
**Date:** 2026-06-20
**Tester:** Ethical security assessment (read-only, no destructive actions)
**Stack Detected:** Django + Django REST Framework, LiteSpeed web server, MySecureCloudHost cPanel server, Cloudflare Quick Tunnel for WebSocket

---

## Executive Summary

The site has solid baseline security (CSP, frame protection, X-Content-Type-Options, CSRF, parameterized queries) but contains **1 CRITICAL** and several **MEDIUM/LOW** issues. The most serious is an **authentication-bypass vulnerability on the WebSocket realtime channel** that allows any unauthenticated visitor to subscribe to any other user's private notification stream.

In the local workspace I also found **production secrets** (SSH private key to the prod server, Firebase admin key, Google OAuth client secret, Android release keystore). They are excluded from git, but they exist on disk and are at risk of accidental leak.

---

## CRITICAL Findings

### 1. WebSocket user-channel IDOR / auth bypass
**Severity:** CRITICAL
**Location:** `wss://towers-pest-kelly-skins.trycloudflare.com/ws/`

The realtime WebSocket accepts subscriptions to `user.<id>` for any id without checking that the connecting client owns that user.

Reproduction (`ws_idor_test.py`):
```
ws.subscribe("user.nikithamal")           -> {"type":"subscribed", ...}
ws.subscribe("user.d0cfb9b0-d569-…")      -> {"type":"subscribed", ...}
ws.subscribe("user.anyone")                -> {"type":"subscribed", ...}
ws.subscribe("user.test")                  -> {"type":"subscribed", ...}
```
- The `ready` event always reports `user_id: null` — the server has no way to identify the caller.
- Session cookie is **not** consulted.
- `Authorization: Bearer` is **not** consulted.
- Sending `action: "auth"` / `action: "publish"` / `action: "broadcast"` is correctly rejected.
- Subscribing to `*` or `user.*` is rejected (and `post.*` actually drops the connection), but specific `user.<id>` and `post.<id>` are accepted.

**Impact:** Any internet user can listen to private events (new follower, mention, reply, like, etc.) for any other user, as long as they know the target's UUID. UUIDs are leaked via the public search API (see Finding 4). The lack of WS auth also enables classic CSWSH (Cross-Site WebSocket Hijacking) — an attacker page on any origin can open this socket and snoop on a victim who has the session, because the WS server has no `Origin` allow-list either.

**Fix:** require a short-lived auth token (e.g. signed JWT minted at login) on the WS upgrade; reject any subscription whose `user.<id>` is not the authenticated user. Also enforce an `Origin` allow-list at the tunnel.

---

### 2. Production secrets present in the workspace
**Severity:** CRITICAL (infrastructure)
**Location:** local working directory

These files exist in the workspace (they are excluded by `.gitignore` so they are **not** in the public repo, but they are on disk and could be uploaded/shared):
- `.ssh_deploy_info.json` — full **RSA private key** for `consicac@192.250.235.158` (production server)
- `backend_python/.env` — production `.env` (likely contains DB creds, `SECRET_KEY`, etc.)
- `backend_python/firebase-service-account.json` — Firebase admin key
- `nebiansnepal-firebase-adminsdk-*.json` — Firebase admin key
- `client_secret_2_*.apps.googleusercontent.com.json` — Google OAuth client secret
- `nebians-release.keystore` — Android release signing key
- `app/google-services.json`, root `google-services.json` — Firebase config

The SSH key alone is enough to SSH into production as `consicac`.

**Fix:**
1. Treat the SSH key as **burned**. Generate a new one, remove the old one from `~/.ssh/authorized_keys` on the server, and never store it on disk again. Rotate any other secrets listed above.
2. Move all deployment secrets into a secrets manager (Doppler, GitHub Actions secrets, or a hardware token) and load them at deploy time.
3. Add a pre-commit hook or CI check that fails if any of these filenames appear in the workspace tree.

---

## MEDIUM Findings

### 3. Missing `Strict-Transport-Security` (HSTS)
Response headers on `https://nebians.consica.com.np/` do not include `Strict-Transport-Security`. Without HSTS, a network attacker can downgrade the first request to HTTP and steal the session cookie in some browser/mitm scenarios. Cookie already has `Secure; SameSite=Lax`, which mitigates the most common cases, but HSTS is still expected.

**Fix:** add `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` to the web server (or via Django middleware) and submit to the HSTS preload list.

### 4. User PII leaked via public search API
`GET /api/search/?q=<any>` returns three arrays — `resources`, `posts`, **`users`**. The `users` array contains the full public profile of any user whose name/username matches, including:
`id, username, display_name, photo_url, bio, school, class_level, follower_count, is_following, is_self, badge_info`

The leaked `id` is the same UUID used as the WS channel key (Finding 1), so this is the input to the IDOR.

**Fix:** decide whether `users` should be returned in the search response at all. If yes, gate it on auth and remove the `is_self` field (or only include `is_self` for the requesting user).

### 5. CSP allows `'unsafe-eval'`
```
script-src 'self' 'nonce-…' 'unsafe-eval' https://accounts.google.com https://www.gstatic.com https://cdn.jsdelivr.net
```
`'unsafe-eval'` permits `eval()` and `new Function(...)`, which weakens CSP. Combined with a single XSS sink, it can be a real bypass. The site already uses nonces, so `unsafe-eval` is likely only there for a single library — try to remove it.

**Fix:** drop `'unsafe-eval'` from `script-src`. If a library truly needs it, sandbox the offending script with `<script src=…> </script>` and a hash instead.

### 6. No rate limiting on signup
`POST /api/auth/email/signup/` happily creates a new account on every request. The verification endpoint **is** throttled (1 hour), but signup itself is not, allowing account spam and email-bombing of arbitrary addresses.

Reproduction: I successfully created `sectest1@nebians-test.com` (userId `a6d709e5-786a-4836-874e-164ebfa926e7`).

**Fix:** add a per-IP and per-email throttle (e.g. `django-ratelimit` 5/hour per IP, 1/hour per email). Add CAPTCHA if abuse persists.

### 7. WebSocket has no `Origin` allow-list
Although `mark as cannot publish` works on the WS, the WS itself accepts any `Origin` (including `null` and `https://evil.com`). Combined with Finding 1, a page on any origin can subscribe to and read private user events.

**Fix:** in the WS upgrade handler, reject requests whose `Origin` header is not `https://nebians.consica.com.np` (and any other allowed frontend).

### 8. HTTP version does not redirect to HTTPS
`http://nebians.consica.com.np/` returns `415` (Cloudflare block) instead of a `301` to HTTPS. A direct visit over HTTP just fails; some users may not realise why and try again, or be exposed to plain-text redirects.

**Fix:** ensure the web server (LiteSpeed) issues a 301 to HTTPS for plain HTTP.

---

## LOW / Informational

### 9. Server header exposes implementation
`Server: LiteSpeed` and `alt-svc` advertise the exact web server. After HSTS is added, also consider removing or genericising the `Server` header.

### 10. Many ports open on production host (192.250.235.158)
Open from outside: 21, 22, 80, 110, 143, 443, 465, 587, 993, 995, 2082, 2083, 2086, 2087, 2095, 2096. This is a cPanel/WHM server. FTP (21), POP3 (110/995), IMAP (143/993) are unlikely to be needed for a Django web app — close them at the firewall.

### 11. SPF present, no DMARC
DNS has an SPF record but no DMARC. Add `v=DMARC1; p=reject; rua=mailto:…` to harden against spoofed sender abuse.

### 12. Third-party scripts lack Subresource Integrity
`https://cdn.jsdelivr.net` and `https://accounts.google.com/gsi/client` are loaded without SRI. If jsdelivr (or its CDN upstream) is compromised, code runs in your origin. SRI is not possible for Google's scripts because they self-update, but jsdelivr ones are pin-able.

### 13. WebSocket accepts any `user.<string>`
It does not verify that `<string>` is a real user UUID, nor a real username. It returns `subscribed` for `user.whatever`. Cheap to fix: validate UUID format and look up the user before subscribing.

### 14. Search/SQLi was not exploitable
`/api/search/?q=test' OR 1=1--` did **not** error and behaved like a normal empty result. The backend is using the Django ORM with parameterised queries — this is good. No action required; flagged as a positive finding.

### 15. XSS in search query not reflected
`<script>alert(1)</script>` in `/api/search/?q=…` returns empty arrays and is never reflected in the response. Front-end also has a custom Markdown renderer with `rel="noopener noreferrer"` and a `safeClientUrl()` URL allow-list, which is good.

---

## Test artefacts (kept for re-validation)
- `ws_test.py` — initial WebSocket probe
- `ws_idor_test.py` — confirms any user channel can be subscribed
- `ws_idor_proof.py` — concurrent listeners on `user.*` + `post.*` + `forum.public`
- `ws_auth_test.py` — confirms session/Authorization headers are ignored
- `ws_cookie_test.py` — confirms session cookie does not change `user_id` in `ready`

To re-run: `pip install websocket-client` and execute any of the above.

---

## Suggested fix priority

1. **Burn & rotate** the SSH key (and other prod secrets). Add CI guard.
2. **Fix WebSocket auth** (signed token on upgrade + Origin allow-list + per-user authorisation on `user.*`).
3. **Add HSTS** header.
4. **Rate-limit signup** and **gate `/api/search/`** users result on auth.
5. **Tighten CSP** by removing `'unsafe-eval'`.
6. Close unused ports (21, 110, 143, 465, 587, 993, 995) at the firewall.
7. Add DMARC and consider SRI for jsdelivr assets.

