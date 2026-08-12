# Needle 2 (WASM) benchmark — NEBians "Neby AI"

Runs the **exact** engine + model shipped to the browser
(`web/static/web/js/needle2/{needle.js,needle.wasm,needle2.cact}`) in Node.js to
measure load time, grammar-compile time, per-query decode latency and memory.
The engine is the official upstream build (identical byte sizes to the
`Cactus-Compute/needle2` HuggingFace `wasm/` + `needle2.cact` release, so results
are representative of a desktop browser — minus network).

## Run
```bash
node benchmarks/needle_bench.mjs            # max_new_tokens = 256 (old default)
env MAX_TOKENS=128 node benchmarks/needle_bench.mjs   # new cap used by the site
```
No third-party deps. Node 18+ with WebAssembly (Node 22 tested).

## What it measures
- Asset transfer size (glue + wasm + model = 13.46 MB)
- Engine/glue instantiation, model `needle_load`, tool grammar `needle_init`
- WASM heap + process RSS
- End-to-end `needle_complete` latency and decoded bytes-per-second for a set of
  realistic NEB queries (single turn, reset between turns — like the site)

## TL;DR results (sandbox: throttled x86-64 VM, Node 22)
- **Grammar compile (`needle_init`) ≈ 5.0 s** — ≈98% of the ~5.0 s cold start.
  Model load is only ~30–60 ms and engine init ~10–20 ms.
- Decode: tool call completed in **~336–1,310 ms** (avg ~0.81 s, p50 ~0.76 s) for
  the 7 realistic tool-calling queries; ~**270–560 byte-tokens/s** decode.
- WASM heap **32.5 MB**, process RSS ~90–97 MB.
- Capping `max_new_tokens` at 128 vs 256 changes **nothing** for real tool calls
  (results are byte-identical, latency within noise) — it only bounds runaway.
- gzip on the CQ2-bit model only saves 5% (94.9% incompressible) → not worthwhile.

## Why the site now feels faster
Browsers are bottlenecked by the ~5 s one-time grammar compile, not throughput.
The integration now **starts loading + initing + warming the engine in the
background** (idle callback + first-user-gesture fallback) in a Web Worker, so the
5 s grammar compile happens while the user is reading the page, not after they
click the assistant. The worker stays alive for the whole visit.
