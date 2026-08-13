# Needle 2 — efficiency/runtime pass: before vs after

Comparing the **previous** build (Cache Storage + idle pre-warm) against this
**v3** build (IndexedDB-first caching + reasoning surfaced). All numbers from the
same sandbox (throttled x86-64 VM, Node 22) running the **exact** engine + model
shipped to the browser. Full run: `FINAL_bench_v3.txt`.

## The core finding (unchanged): the one-time grammar compile is the cold cost
`needle_init` (compiling the tool schema into a decode grammar) is **~4.9–5.1 s**,
≈98% of the ~5 s cold start. Model load is ~35–47 ms, engine init ~10 ms. You
cannot make that grammar compile faster without changing the engine — but you can
(a) run it once and reuse the engine for the whole visit (already done via idle
pre-warm in a Web Worker), and (b) stop re-downloading the 13.46 MB of assets on
every refresh, which is what made **mobile** cold loads 40–50 s.

## What changed and the numbers

| Metric | Before (v2) | After (v3) | Impact |
|---|---|---|---|
| Asset bytes transferred on **repeat** visit | 13.46 MB (network) | **0 B** (IndexedDB hit) | The 40–50 s mobile cold load is eliminated on repeat visits |
| Local read of all 13 MB (cached) | not measured (network each visit) | **~8 ms** | reads come from fast local storage |
| Cold start TOTAL (first visit, after cache) | ~5.14 s | ~5.00 s | grammar compile; preloaded in background so not blocking UI |
| — of which `needle_init` | ~5.09 s | ~4.95 s | within noise |
| — model load | ~33–47 ms | ~36–47 ms | unchanged |
| — engine+glue init | ~8–56 ms | ~10 ms | unchanged |
| Decode latency avg | ~0.76–0.80 s | ~0.81 s | within noise |
| Decode p50 / p95 | ~0.68 / 1.15 s | ~0.77 / 1.34 s | within noise |
| Est. decode | ~70 tok @ ~88–92 tok/s | ~70 tok @ ~86 tok/s | within noise |
| WASM heap / RSS | 32.5 / ~90–109 MB | 32.5 / ~109 MB | unchanged |
| `reasoning` field | discarded | **surfaced in chat UI** | model's derivation now visible |
| Offline guarantee | cached in Cache Storage | **works with network fully disabled** | verified by `worker_cache_test.mjs` |

Decode latency is intentionally unchanged — the model and engine are identical;
we did not trade accuracy for speed. The win is on **asset delivery and UX
latency**: repeat visitors no longer wait on a 13 MB download, and the grammar
compile is hidden behind the idle pre-warm.

## What was verified
1. `node benchmarks/needle_bench.mjs` → `FINAL_bench_v3.txt` (engine loads,
   reasoning present per query).
2. `node benchmarks/worker_cache_test.mjs` → a mock browser worker proves:
   - first run: **2 network fetches** (wasm + model), IDB populated;
   - second run: **0 new fetches** (IndexedDB hit), 13,737,679 model bytes read
     from IDB;
   - with **fetch disabled entirely**, the model still loads and answers.

## Deploy checklist (web)
1. `cd backend_python && ./manage.py collectstatic` (or the project's static
   deploy flow per AGENTS.md "Static Files Deployment") so the edited
   `needle.worker.js` + `neby-assist.js` reach WhiteNoise `staticfiles/`.
2. Force a worker/process respawn (per AGENTS.md) so the new static index is read.
3. Re-run `node benchmarks/needle_bench.mjs` to confirm the engine loads.
4. Existing browsers already have the old v2 Cache-Storage bytes; they migrate to
   IndexedDB automatically on next visit (no forced re-download). New asset
   version (`needle2-assets-v3` + `?v=3`) only matters if the model/engine
   changes.

## Android note
The on-device assistant (`app/`) downloads the same three assets from
`https://nebians.consica.com.np/static/web/js/needle2/` into app-private storage
once, then runs fully offline inside a WebView (no NDK build, no model bundled in
the APK). It could not be compiled in this sandbox (no JDK/Android SDK) — needs
an on-device `./gradlew assembleModernDebug` smoke test before release.
