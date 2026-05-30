# NEBians - Continuity Notes

**Last updated:** May 30, 2026

---

## Current Status

### Google Sign-In Migration (IN PROGRESS)
- **Status:** GIS button renders, but "origin not allowed" error from Google
- **What was done:**
  - Removed Firebase Auth (`signInWithRedirect`, `signInWithPopup`) from `login.html`
  - Replaced with Google Identity Services (GIS) using `google.accounts.id.initialize()` + `renderButton()`
  - Updated `views.py` to pass `google_client_id` instead of 6 Firebase config vars
  - Updated `authentication.py` to verify tokens against both `GOOGLE_CLIENT_ID` and `FIREBASE_PROJECT_ID`
  - Updated `.env` on server with correct `GOOGLE_CLIENT_ID`
  - Fixed `settings.py` to use `load_dotenv(override=True)` so `.env` values take effect
  - Rewrote `login.html` JS to use `.then()` callbacks (no `async/await`) to avoid syntax errors
  - Added all helper functions back (`showPanel`, `togglePassword`, `handleEmailLogin`, etc.)
- **What's blocked:**
  - Google returns "origin not allowed" error for client ID `68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com`
  - This client ID was created on May 30, 2026 — new OAuth clients can take hours to propagate
  - Authorized JavaScript origins ARE configured correctly in Google Cloud Console
  - OAuth consent screen IS in Production mode
- **How to test:**
  1. Go to `https://nebians.consica.com.np/login/` or `http://localhost:8000/login/`
  2. The Google "Continue with Google" button should render via GIS
  3. If Google still says "origin not allowed", wait a few more hours or verify the Google Cloud Console settings
  4. Check server logs: `ssh ... consicac@192.250.235.158 "grep -i 'auth\|google\|token' /home/consicac/nebians_api/logs/nebians.log | tail -20"`

### Light Mode Hover Fix (COMPLETE)
- Text buttons, outlined buttons, auth buttons in light mode had solid blue hover backgrounds
- Changed from `var(--md-primary-container)` (#2563EB) to `rgba(0, 74, 198, 0.08)` across:
  - `material3.css`: `.md-btn-text:hover`, `.md-btn-outlined:hover`
  - `app.css`: `.auth-text-btn:hover`, `.auth-link-btn:hover`

---

## Key Configuration Values

### Server
- **Host:** 192.250.235.158
- **User:** consicac
- **Project Dir:** /home/consicac/nebians_api/
- **Virtualenv:** /home/consicac/virtualenv/nebians_api/3.13/
- **Web Server:** Phusion Passenger (NOT gunicorn)
- **Restart:** `touch tmp/restart.txt` (NOT gunicorn restart)
- **Log:** `/home/consicac/nebians_api/logs/nebians.log`

### OAuth / Auth
- **Google OAuth Client ID:** `68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com`
- **Firebase Project ID:** `nebiansnepal`
- **Firebase Web App ID:** `1:68143624035:web:f04129d04b128b92e4ed56`
- **Firebase Sender ID:** `68143624035`

### .env on Server (as of May 30, 2026)
```
DEBUG=True
SECRET_KEY=local-dev-key-change-in-production
DB_ENGINE=mysql
GOOGLE_CLIENT_ID=68143624035-que25r0vmrke4agasr715j5u9p8gic2s.apps.googleusercontent.com
WEB_API_BASE_URL=https://nebians.consica.com.np/api
ALLOWED_HOSTS=nebians.consica.com.np,www.nebians.consica.com.np,localhost,127.0.0.1
```

---

## Things That Broke Before & How They Were Fixed

### 1. Firebase `redirect_uri_mismatch`
- **Cause:** Firebase Auth uses `signInWithRedirect` which requires redirect URIs configured in Firebase Console
- **Fix:** Replaced Firebase Auth with Google Identity Services (GIS) popup-based flow — no redirect URIs needed

### 2. GIS `initTokenClient` returned access_token, not ID token
- **Cause:** `initTokenClient()` returns OAuth access tokens, not JWT ID tokens
- **Fix:** Switched to `google.accounts.id.initialize()` + `renderButton()` which returns `response.credential` (JWT)

### 3. GIS "called multiple times" warning
- **Cause:** `initialize()` was called on page load AND on button click
- **Fix:** Only call `initialize()` once during `window.load` event

### 4. FedCM errors and "signal is aborted"
- **Cause:** Using `google.accounts.id.prompt()` triggers FedCM which has compatibility issues
- **Fix:** Removed `prompt()`, only use `renderButton()` for the button

### 5. `handleCredentialResponse` not found / "callback is not a function"
- **Cause:** GIS HTML `data-callback` attribute couldn't find the function, and `g_id_onload` HTML attribute conflicted with JS initialize
- **Fix:** Removed `g_id_onload` div, only use JS-based `initialize()` with `callback: handleCredentialResponse`

### 6. `await` syntax error in non-async function
- **Cause:** `handleCredentialResponse` called `await sendTokenToBackend()` but wasn't declared `async`
- **Fix:** Rewrote all auth JS using `.then()` callback pattern instead of `async/await`

### 7. `showPanel is not a function`
- **Cause:** During multiple edits, the `showPanel`, `togglePassword`, and email auth functions were accidentally deleted from the script block
- **Fix:** Rewrote entire `login.html` from scratch with all functions present

### 8. `.env` overriding `settings.py` with old values
- **Cause:** `load_dotenv()` without `override=True` doesn't override existing env vars. The `.env` on the server had the old `GOOGLE_CLIENT_ID` which took precedence over the new default in `settings.py`
- **Fix:** Changed to `load_dotenv(BASE_DIR / '.env', override=True)` and updated the `.env` file on the server

### 9. Passenger not picking up `.env` changes
- **Cause:** Phusion Passenger caches environment variables. `touch tmp/restart.txt` restarts the app but may use cached env
- **Fix:** Had to update `.env` file content AND use `override=True` in `load_dotenv()`. For stubborn cases, kill Passenger processes and let them respawn

### 10. `ALLOWED_HOSTS` missing `www` subdomain
- **Cause:** Server logs showed `Invalid HTTP_HOST header: 'www.nebians.consica.com.np'`
- **Fix:** Added `www.nebians.consica.com.np` to `ALLOWED_HOSTS` in both `settings.py` default and `.env`

---

## Deployment Checklist

When deploying changes to the backend:
1. SCP changed files to `/home/consicac/nebians_api/`
2. If you changed `settings.py` or `.env`, ALSO update the `.env` file on the server manually
3. Run: `collectstatic --noinput && migrate && touch tmp/restart.txt`
4. Verify by checking logs: `tail -20 /home/consicac/nebians_api/logs/nebians.log`
5. If auth changes, test login at `/login/`
6. If CSS changes, `collectstatic` is required (Passenger serves static files from `staticfiles/`)

### Quick Deploy Commands (PowerShell)
```powershell
$sshKey = "$env:TEMP\nebians_deploy_key.pem"
# Fix permissions (run once per session)
icacls $sshKey /inheritance:r /grant "${env:USERNAME}:R"

# Deploy a single file
scp -o StrictHostKeyChecking=no -i $sshKey "LOCAL_FILE" consicac@192.250.235.158:/home/consicac/nebians_api/REMOTE_PATH

# Full deploy
ssh -o StrictHostKeyChecking=no -i $sshKey consicac@192.250.235.158 "cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python manage.py collectstatic --noinput && python manage.py migrate && rm -rf tmp/* && touch tmp/restart.txt && echo 'DONE'"
```

---

## What NOT to Do

1. **NEVER use `signInWithRedirect` or `signInWithPopup` from Firebase Auth** — causes redirect_uri_mismatch
2. **NEVER use `google.accounts.oauth2.initTokenClient()`** — returns access tokens, not ID tokens
3. **NEVER use `google.accounts.id.prompt()`** — causes FedCM errors
4. **NEVER call `google.accounts.id.initialize()` more than once** — causes "called multiple times" warnings
5. **NEVER use `async/await` in GIS callback handlers** — use `.then()` pattern instead
6. **NEVER start/stop gunicorn** — server uses Phusion Passenger
7. **NEVER forget to update `.env` on server** — it overrides `settings.py` defaults
8. **NEVER forget `collectstatic --noinput`** — static files won't update without it
9. **NEVER use `var(--md-primary-container)` for hover backgrounds in light mode** — it's too saturated (#2563EB). Use `rgba(0, 74, 198, 0.08)` instead