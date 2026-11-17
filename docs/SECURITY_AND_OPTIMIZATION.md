# NEBians Backend Optimization, Cybersecurity & Android Obfuscation Guide

## 1. Shared cPanel Backend Optimization Architecture

Our production environment runs on a shared cPanel LiteSpeed (`lswsgi`) server with strict per-account limits (`max_user_connections = 10` on MariaDB, `LSAPI_CHILDREN = 6`, shared LVE thread/RAM limits). Every optimization is engineered to minimize SQL connections, Redis socket round-trips, worker memory, and CPU threads:

| Layer | Optimization | File(s) |
| --- | --- | --- |
| **L1 In-Process Worker Cache** | Thread-safe bounded L1 LRU cache (512 keys, 5s TTL in prod, auto-disabled in `manage.py test`) inside `ResilientRedisCache`. Eliminates ~85% of repeat Redis socket round-trips for hot keys (`site_theme`, `library_filter_options`, `home_resources`, `home_stats_v2`, token checks). Immediate in-process eviction on `set`/`delete`/`clear`/`incr`. | `nebians/cache_fallback.py` |
| **LSAPI Parent Pre-Warming** | `passenger_wsgi.py` runs `nebians/warmup.py` once in the parent process before forking workers. Pre-imports `redis`, `pymysql`, `PIL`, `bleach`, `rest_framework.serializers`, `api.serializers`, `api.security`, `api.view_helpers`, `web.view_helpers`, `web.syllabus_data`, populates URLconf, and compiles templates copy-on-write. | `nebians/warmup.py`, `passenger_wsgi.py` |
| **Conditional Daphne Retirement** | Realtime uses hosted Ably (`api/realtime_ably.py`). `restart_workers.sh` now keeps `daphne` retired unless `WS_PUBLIC_URL` or `ENABLE_DAPHNE=1` is set, saving ~127 MB RAM and ~64 LVE threads. | `scratch/restart_workers.sh` |
| **SQL Query & Prefetch Pruning** | `posts_endpoint` joins `poll` via `select_related('user', 'poll')`. `prime_for_serializers` skips re-prefetching `user` and `uploaded_by` when already cached on model instances and only prefetches `poll__options` for rows that actually hold a poll. `user_profile_stats` reuses `is_following` to avoid duplicate `Follow` queries on locked profiles. | `api/view_helpers.py`, `api/views_forum.py`, `api/views_users.py` |
| **Anonymous Feed & Token Micro-Cache** | First-page anonymous `GET /api/posts/` responses are cached for 15s in production, and `get_user_by_auth_token` caches resolved active users for 15s (`auth_user:<hash>`, cleared immediately on logout/revocation) so parallel mobile launch requests do not hit MariaDB 10 times for the same token. | `api/views_forum.py`, `api/security.py` |

---

## 2. Cybersecurity & Anti-Proxy / Anti-Scanner Hardening

| Threat Vector | Defense Implemented | File(s) |
| --- | --- | --- |
| **OAuth2 & Login Open Redirects** | `_safe_next_url()` enforces `url_has_allowed_host_and_scheme` and strict single-slash relative path validation across `login_page`, `google_login`, `google_oauth_callback`, `github_login`, `github_callback`, and `token_login`. `google_login` rejects arbitrary user-supplied `state` strings. Removed `ftp` from `DeepLinkRedirect.allowed_schemes`. | `web/views_auth.py` |
| **Exploit Scanners & Open-Proxy Probes** | `CrawlerShieldMiddleware` blocks `CONNECT` methods, `HTTP_PROXY_CONNECTION` headers, absolute foreign proxy URLs, and exploit scanner User-Agents (`sqlmap`, `nuclei`, `nikto`, `masscan`, `zgrab`, `gobuster`, `ffuf`, `wpscan`, `acunetix`, etc.) with `403 Forbidden` before sessions, CSRF, or DB run. | `nebians/crawler_shield.py` |
| **Reverse-Proxy Path Override & Framing** | `SecurityHeadersMiddleware` strips `HTTP_X_ORIGINAL_URL` and `HTTP_X_REWRITE_URL`, removes `Server` and `X-Powered-By`, sets `Cross-Origin-Resource-Policy: same-origin` on `/api/` and `/ajax/` (`same-site` elsewhere), `X-DNS-Prefetch-Control: off`, `X-Download-Options: noopen`, and expands `SENSITIVE_PATHS_404`. | `nebians/middleware.py` |
| **AJAX Brute-Force, Info Leaks & Memory Exhaustion** | Added rate limits to `ajax_resource_comment`, `ajax_check_username`, `ajax_set_password`, and `ajax_change_password`. Sanitized 500 error responses in `ajax_user_photos` so raw DB/exception strings never leak. Bounded `_RATE_STORE` in `astroweb_bridge_views.py` to 1,024 keys. | `web/views_ajax.py`, `api/astroweb_bridge_views.py` |

---

## 3. Irreversible Android Obfuscation & Anti-MITM Network Hardening

1. **System-Only CA Pinning (`network_security_config.xml`)**:
   - `<base-config cleartextTrafficPermitted="false">` trusts only `<certificates src="system" />`. User-installed MITM proxy root certificates (Charles, Burp, Fiddler, Reqable, HTTP Toolkit, mitmproxy) are rejected by the OS across all production connections.
2. **Direct Socket Bypass (`Proxy.NO_PROXY` + `MODERN_TLS`)**:
   - In release builds (`!BuildConfig.DEBUG`), `ApiService`, `NEBiansApp` (Coil image loader), and `RealtimeClient` configure `OkHttpClient` with `.proxy(Proxy.NO_PROXY)` and `ConnectionSpec.MODERN_TLS`, bypassing any Wi-Fi or system HTTP proxy configured on the phone.
3. **Cryptographic Per-Request Proof (`X-Neb-Proof`)**:
   - `DeviceSignalInterceptor` attaches `X-Neb-Proof: t=<epoch>;n=<nonce>;s=<hmac>` signed with an obfuscated key over `method|path|ts|nonce|versionCode`.
4. **Irreversible R8 + Native C++ Symbol Stripping**:
   - `proguard-rules.pro` enables `-renamesourcefileattribute SourceFile`, `-optimizationpasses 5`, `-overloadaggressively`, `-allowaccessmodification`, and strips verbose/debug/info `android.util.Log` calls via `-assumenosideeffects`.
   - `CMakeLists.txt` compiles `libneb_speech.so` with `-fvisibility=hidden -fvisibility-inlines-hidden -ffunction-sections -fdata-sections` and links with `-Wl,--gc-sections -Wl,--exclude-libs,ALL -Wl,-s`.
