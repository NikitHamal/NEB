# Needle 2 benchmarks — NEBians "Neby Local"

These harnesses execute the exact Needle 2 glue, WASM engine, CQ2 model, and tool schemas shipped by NEBians. They require Node 18+ and no third-party packages.

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

Caching only `needle2.cact` therefore still left almost all startup work on every refresh. The v3 worker now persists a versioned, tool-schema-keyed snapshot of the initialized 32.6 MB WASM heap in 2 MB IndexedDB chunks. On a later launch it instantiates the 0.30 MB engine and restores the snapshot without reading the model or recompiling the grammar. A corrupt, missing, quota-rejected, or version-mismatched snapshot automatically falls back to the normal verified cold path.

The snapshot is taken before any user query, so it contains the public model/runtime/tool state and no chat content. Model and engine binaries remain in Cache Storage on web. Android stores the optional model in `noBackupFilesDir`; the APK only includes the 0.36 MB WASM engine and glue.

The former synthetic warm-up completion was removed. Repeating the same first query showed no material decode improvement, while warm-up added roughly 1.1 seconds of CPU time and battery use before the first real query.

## Latest results

Sandbox: throttled x86-64 VM, Node 22, 2026-08-13. See `FINAL_bench.txt` and `snapshot_bench.txt` for full raw output.

| Metric | Result |
|---|---:|
| Model | 13.10 MiB |
| Web engine + glue | 0.36 MiB |
| Cold initialized WASM heap | 32.63 MiB |
| Cold load + tool init | 5,116–5,284 ms |
| Persisted runtime restore, including disk read | 49 ms |
| Repeat-launch reduction | **99.0%** |
| Restored output equivalence | **7/7** |
| Expected tool routing | **7/7** |
| Grounded key arguments | **7/7** |
| Decode average / p50 / p95 | 819 / 727 / 1,529 ms |
| Browser runtime snapshot | 32.63 MiB |
| Android model added to base APK | **0 bytes** |
| Android engine/glue added to APK before packaging | 0.36 MiB |

The engine exposes a `reasoning` field on every tested response, but this shipped model generated a non-null compact trace on 2/7 benchmark prompts. Both web and Android render the trace when present; they do not invent one when the engine returns `null`.

## Mobile interpretation

The Node result isolates engine behavior and snapshot correctness; it is not presented as a phone benchmark. The Android screen reports real setup time and per-response milliseconds on each user's device. First setup still includes the one-time cloud download and cold grammar build. Later app launches restore the initialized runtime locally and inference remains offline.

The Android download is resumable, SHA-256 verified, optional, and removable. The expected model is exactly 13,737,679 bytes with SHA-256 `ca7950ac8aef26ed22d17f92c733c9374aa7f59f6c2abb0fe2ac320a04f3c3d8`.
