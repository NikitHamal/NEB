# Needle 3 benchmarks — NEBians "Neby Local"

These harnesses execute the exact Needle 3 glue, WASM engine, CQ2 model, and tool schemas shipped by NEBians. They require Node 18+ and no third-party packages.

## Run

```bash
cd backend_python
node benchmarks/needle_bench.mjs
node benchmarks/needle_snapshot_bench.mjs
```

Use `MAX_TOKENS=256 node benchmarks/needle_bench.mjs` to compare the former 256-token cap. Production uses 128; all benchmark tool calls finish below the cap.

## What changed

The model download was not the main repeat-launch bottleneck. The exact breakdown on the sandbox is:

- engine instantiation: about 8 ms
- model load: about 35 ms
- tool grammar initialization: about 5.2 seconds
- tool decode: about 0.4–1.4 seconds

Caching only `needle3.cact` therefore still left almost all startup work on every refresh. The v3 worker now persists a versioned, tool-schema-keyed snapshot of the initialized 97.25 MB WASM heap in 2 MB IndexedDB chunks. On a later launch it instantiates the 0.65 MB engine and restores the snapshot without reading the model or recompiling the grammar. A corrupt, missing, quota-rejected, or version-mismatched snapshot automatically falls back to the normal verified cold path.

The snapshot is taken before any user query, so it contains the public model/runtime/tool state and no chat content. Model and engine binaries remain in Cache Storage on web. Android is unchanged and still ships the Needle 2 engine/assets pending a future APK update.

The former synthetic warm-up completion was removed. Repeating the same first query showed no material decode improvement, while warm-up added roughly 1.1 seconds of CPU time and battery use before the first real query.

## Latest results

Sandbox: Windows dev box, Node 24, 2026-09-18 (Needle 3 full 20-layer `needle3.cact`). Historical Needle 2 numbers live in `FINAL_bench.txt` and `snapshot_bench.txt`.

| Metric | Result |
|---|---:|
| Model | 33.70 MiB |
| Web engine + glue | 0.71 MiB |
| Cold initialized WASM heap | 97.25 MiB |
| Cold load + tool init | 6,046–12,548 ms |
| Persisted runtime restore, including disk read | 182 ms |
| Repeat-launch reduction | **97.0%** |
| Restored output equivalence | **7/7** |
| Expected tool routing | **7/7** |
| Grounded key arguments | **7/7** |
| Decode average / p50 / p95 | 2,502 / 2,348 / 3,721 ms |
| Browser runtime snapshot | 97.25 MiB |
| Android model added to base APK | **0 bytes** |
| Android engine/glue added to APK before packaging | 0.36 MiB (Needle 2, unchanged) |

The engine exposes a `reasoning` field on every tested response, and this Needle 3 model generated a non-null compact trace on 7/7 benchmark prompts. Web renders the trace when present and does not invent one when the engine returns `null`.

## Mobile interpretation

The Node result isolates engine behavior and snapshot correctness; it is not presented as a phone benchmark. The Android screen reports real setup time and per-response milliseconds on each user's device. First setup still includes the one-time cloud download and cold grammar build. Later app launches restore the initialized runtime locally and inference remains offline.

The Android download is resumable, SHA-256 verified, optional, and removable. The Android app is unchanged and still expects the Needle 2 model: exactly 13,737,679 bytes with SHA-256 `ca7950ac8aef26ed22d17f92c733c9374aa7f59f6c2abb0fe2ac320a04f3c3d8` (served from `web/js/needle2/`, now removed from the web deploy — see AGENTS.md).
