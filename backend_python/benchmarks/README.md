# Needle 2 (WASM) benchmark — NEBians "Neby AI"

Runs the **exact** engine + model shipped to the browser
(`web/static/web/js/needle2/{needle.js,needle.wasm,needle2.cact}`) in Node.js to
measure load time, grammar-compile time, per-query decode latency, memory, and
the cost of a **local** (IndexedDB cache-hit) read of the model bytes. The engine
is the official upstream build (identical byte sizes to the
`Cactus-Compute/needle2` HuggingFace `wasm/` + `needle2.cact` release, so results
are representative of a desktop browser — minus network).

## Run
```bash
node benchmarks/needle_bench.mjs            # max_new_tokens = 128 (matches the site)
env MAX_TOKENS=256 node benchmarks/needle_bench.mjs   # compare against the old default
```
No third-party deps. Node 18+ with WebAssembly (Node 22 tested).

## What it measures
- Asset transfer size (glue + wasm + model = 13.46 MB)
- **Local read** of all assets — represents the IndexedDB "cache hit" the worker
  uses after the first visit (no network). In this sandbox it's a `readFileSync`
  of the exact bytes the worker would read out of IndexedDB: ~8 ms for all 13 MB.
- Engine/glue instantiation, model `needle_load`, tool grammar `needle_init`
- WASM heap + process RSS
- End-to-end `needle_complete` latency and decoded bytes-per-second for a set of
  realistic NEB queries (single turn, reset between turns — like the site)
- `reasoning` — the per-turn derivation the model emits (now surfaced in the UI)

## Why it's fast now (the current implementation)
1. **IndexedDB caching (new).** `needle.worker.js` stores `needle.wasm` +
   `needle2.cact` in IndexedDB on the first visit. Every later visit reads the
   ~13 MB straight out of local storage (~8 ms) instead of re-downloading over
   the network — this is what was making cold loads take 40–50s on phones
   (13 MB over a mobile link + WASM/grammar compile on a phone CPU). Cache
   Storage is kept as a legacy/fallback layer and old v2 caches migrate to IDB
   automatically.
2. **Idle pre-warm.** `neby-assist.js` starts the worker on
   `requestIdleCallback` + first-user-gesture fallback, so the ~5 s one-time
   grammar compile (`needle_init`) runs in a background Web Worker while the
   user is still reading the page. The worker stays alive for the whole visit.
3. **Reasoning surfaced.** Every tool call now shows the model's `reasoning`
   (a collapsible "Model reasoning" block) in the chat UI.

## TL;DR results (sandbox: throttled x86-64 VM, Node 22 — see FINAL_bench_v3.txt)
- **Local (cached) read of all 13 MB: ~8 ms** — vs. a full 13.46 MB network
  transfer on the first visit (the dominant cost on mobile).
- Grammar compile (`needle_init`) ≈ 4.9 s — ≈98% of the ~5.0 s cold start.
  Model load only ~35 ms, engine init ~10 ms.
- Decode: tool call completed in ~367–1,344 ms (avg ~0.81 s, p50 ~0.77 s) for
  the 7 realistic tool-calling queries; ~86–111 byte-tokens/s decode.
- WASM heap 32.5 MB, process RSS ~109 MB.
- `max_new_tokens` 128 vs 256 → byte-identical tool calls; 128 bounds runaway.
- gzip on the CQ2-bit model saves only ~5% (94.9% incompressible) → not shipped.

## Full result files
- `FINAL_bench_v3.txt` — current run after the IndexedDB + reasoning pass.
- `FINAL_bench.txt` / `bench_128.txt` / `bench_256.txt` — prior runs for
  comparison.

## Worker cache test
`benchmarks/` also contains a Node harness that mocks a browser worker
(IndexedDB + Cache Storage + fetch) and verifies the caching state machine:
first run fetches once, subsequent runs hit IndexedDB, and the model still loads
and answers with networking fully disabled.
