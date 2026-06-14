# Imunify360 Temporary IP Block Fallback Plan

## Problem summary
Users sometimes hit a temporary Imunify360 / CloudLinux hosting security block on shared cPanel. Browser may show a “wait one moment / page is loading” challenge page, but the Android app expects JSON and immediately shows the generic error card. The app cannot bypass Imunify360; the host controls the block. The fix is to (1) reduce false-positive triggers, (2) ask the host for the safest shared-hosting mitigation, and (3) make the app treat host-security responses as a temporary protected-server state instead of a broken API error.

## Root cause hypothesis
- Android OkHttp/Retrofit requests receive the Imunify360 HTML challenge or a non-JSON 403/429/503/52x response.
- Retrofit’s JSON converter then fails or the repository surfaces `e.message`, so UI shows a raw/generic error card.
- Browser can show the hosting provider loading/challenge page because it can render/execute the page; the app cannot.

## Implementation plan

### 1. Add centralized API error classification
Files to edit:
- `app/src/main/java/com/neb/ians/data/api/ApiService.kt`
- New helper file under `app/src/main/java/com/neb/ians/data/api/` (for example `ApiErrorMapper.kt`)

Behavior:
- Detect non-JSON responses (`text/html`, challenge markers, “wait one moment”, “Imunify360”, CloudLinux markers).
- Detect temporary hosting blocks: HTTP `403`, `429`, `503`, `520`, `522`, `524` when body is not API JSON.
- Return a user-friendly message such as:
  - `NEBians server is temporarily protected by the hosting security filter. Please wait a few minutes and try again.`
  - Add: `If it keeps happening, switch networks or contact support.`
- Keep normal API errors intact:
  - `401` remains sign-in/session issue.
  - `403` JSON remains permission/auth issue.
  - `429` JSON remains app rate-limit message.
  - `503` JSON from Neby AI pool remains AI-worker busy message.

### 2. Make Retrofit robust against HTML challenge pages
Files to edit:
- `app/src/main/java/com/neb/ians/data/api/ApiService.kt`

Changes:
- Add a stable app User-Agent header, for example `NEBians-Android/1.0.0`, so requests do not look like generic bot traffic.
- Add an OkHttp interceptor that peeks at failed non-JSON responses and throws a typed `ApiClientException` with status code and friendly reason.
- Avoid swallowing response bodies in normal successful JSON calls.

### 3. Replace raw exception messages in UI ViewModels
Files to edit:
- `app/src/main/java/com/neb/ians/ui/screens/home/HomeViewModel.kt`
- `app/src/main/java/com/neb/ians/ui/screens/library/LibraryViewModel.kt`
- `app/src/main/java/com/neb/ians/ui/screens/forum/ForumViewModel.kt`
- `app/src/main/java/com/neb/ians/ui/screens/search/SearchViewModel.kt`
- Other affected ViewModels if they display `e.message` directly.

Changes:
- Use the new API error mapper instead of `e.message ?: fallback`.
- For host-security errors, show one friendly card with “Retry later” and no technical dump.
- For load-more failures, keep existing content visible and show a small retry banner instead of replacing the whole screen.

### 4. Improve error card UX
File to edit:
- `app/src/main/java/com/neb/ians/ui/components/ShimmerEffects.kt`

Changes:
- Add optional subtitle/detail text for temporary hosting blocks.
- Add a second action button where useful:
  - `Retry now`
  - `Use offline cache` if cached data exists for that screen.
- Make retry button text context-aware, e.g. `Try again later` for Imunify360 blocks.

### 5. Add cached-data fallback where feasible
Files to edit:
- `app/src/main/java/com/neb/ians/ui/screens/library/LibraryScreen.kt`
- `app/src/main/java/com/neb/ians/ui/screens/library/LibraryViewModel.kt`
- `app/src/main/java/com/neb/ians/ui/screens/forum/ForumScreen.kt`
- `app/src/main/java/com/neb/ians/ui/screens/forum/ForumViewModel.kt`

Changes:
- If the network fails with a host-security/temporary error and the screen already has cached items, keep showing those items.
- Show a small banner at the top: `Live data is temporarily unavailable. Showing last saved results.`
- Disable infinite scroll while the temporary block is active.

### 6. Reduce retry storms
Files to edit:
- `app/src/main/java/com/neb/ians/data/realtime/RealtimeClient.kt`
- Search/refresh ViewModels with debounced queries.

Changes:
- For host-security errors, back off longer: 1 min, 5 min, 15 min, then manual retry.
- Avoid automatic retries on every keystroke/search character during a block.
- Keep WebSocket reconnect behavior exponential, but do not let unread-count polling repeatedly trigger the same block.

### 7. Download/PDF fallback
File to edit:
- `app/src/main/java/com/neb/ians/util/ResourceDownloadManager.kt`

Changes:
- Detect HTML challenge responses when downloading resources.
- Mark download as failed with a friendly host-security message instead of silently setting progress to `-1`.

## Host/shared-cPanel mitigation plan

### Ask Babal Host for
1. Unblock the affected client IPs temporarily when reports come in.
2. Check Imunify360 logs for NEBians false positives and lower the false-positive threshold for this domain if possible.
3. Confirm whether they can whitelist the app/API path or a stable mobile User-Agent. On shared cPanel this is often limited, but it is worth asking.
4. Confirm whether a dedicated IP / higher hosting tier is available later if the app grows.

### Important reality check
- If Imunify360 blocks a user’s IP, the app cannot bypass it from client code.
- Shared cPanel hosting usually cannot provide a per-app bypass for all mobile clients.
- Browser seeing a challenge page while the app sees JSON parsing failure is expected behavior.

## Free/low-cost workarounds if shared hosting remains unstable
1. Keep the app local-first and cache-heavy so temporary origin blocks are tolerable.
2. Put read-only public content on a free static edge host (Firebase Hosting, Cloudflare Pages, GitHub Pages) and sync small metadata/API responses there.
3. Use a free serverless backend for critical API paths later (Cloudflare Workers, Supabase Edge Functions, Firebase Functions) if budget allows.
4. Use Cloudflare in front of the origin only if the hosting plan/DNS allows it. If origin requests then come from Cloudflare IPs, Imunify may treat them differently, but this requires host/DNS cooperation.
5. VPS remains the cleanest long-term fix, but not required for an immediate UX mitigation.

## Validation
- Simulate a non-JSON 403 HTML response locally and verify the app shows the friendly host-security card.
- Verify normal API `401`, `403`, `429`, and `503` JSON responses still show their existing specific messages.
- Test library/forum home screens with cached data + simulated host-security failure.
- Test resource download failure body detection.
- Build `assembleModernDebug` or equivalent before deployment.
