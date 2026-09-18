# Needle 3 fine-tuning plan (NEBians Neby AI)

Goal: improve Neby AI's tool-calling accuracy on the NEB domain (resources,
notes, forum, navigation) by LoRA fine-tuning the frozen 121M (20-layer) base
model, then merging to a new `.cact` that runs on the **same** WASM engine —
no engine re-compilation needed.

## Pipeline (from the official cactus-compute/needle repo)
```bash
pip install "cactus-needle[train]"   # runtime + JAX training deps
export OPENROUTER_API_KEY=sk-or-...
# 1) (optional) synthesize training examples from the NEB tool schema
needle generate-data --tools neb_tools.json --num-samples 500 --output neb_data.jsonl
# 2) LoRA fine-tune at the full 20 layers (base checkpoint auto-downloads from HF)
needle finetune neb_data.jsonl --epochs 3 --lora-rank 16 --lora-alpha 32 \
    --generate 200
# 3) merge adapter + export a tuned .cact (local export is 4-bit;
#    the shipped 2-bit model comes from the Cactus Platform).
#    --layers N optionally slices a smaller 2..20-layer rung.
needle build checkpoints/needle3.safetensors \
    --lora checkpoints/needle_lora.safetensors --out neb_needle3.cact
# 4) smoke test the tuned model
python - <<'PY'
import needle
agent = needle.Needle(tools=TOOLS, weights="neb_needle3.cact")
print(agent.complete("find physics notes for class 12"))
PY
```
## Data format (JSONL)
```json
{"query":"find physics notes for class 12",
 "tools":[{"name":"find_notes","parameters":{...}}],
 "answers":[{"name":"find_notes","arguments":{"subject":"Physics","grade_level":"Class 12","exam_type":"Notes"}}],
 "reasoning":"'physics' -> subject; 'class 12' -> grade; 'notes' -> type"}
```
Off-topic rows use `"answers": []` (teaches refusal).

## NEB tool schema (neb_tools.json)
Use exactly the 5 tools shipped in `web/static/web/js/neby-assist.js`
(`NEBY_TOOLS`): `search_resources`, `find_notes`, `get_forum_posts`,
`navigate_to`, `get_subjects`. Refer to that file for the authoritative JSON.
The engine compiles the same schema at runtime, so fine-tune on the identical
grammar to close the train/serve gap.

## Deploying a tuned model (browser)
1. Back up `web/static/web/js/needle3/needle3.cact`.
2. Copy the tuned `neb_needle3.cact` to `web/static/web/js/needle3/needle3.cact`.
   Same filename, same engine — nothing else changes.
3. In `needle.worker.js`, bump `RUNTIME_VERSION` and the `CACT_URL` query
   version. This invalidates the initialized IndexedDB snapshot and fetches the
   new model without evicting the unchanged WASM engine.
4. Redeploy static files (collectstatic per AGENTS.md).
5. Re-run both `node benchmarks/needle_bench.mjs` and
   `node benchmarks/needle_snapshot_bench.mjs` to confirm quality, restored
   output equivalence, and latency.

Android is intentionally left on Needle 2 for now; it will get its own
tuned-model/model-swap pass with the next APK.

## Tuned-model caveats (Needle 3)
- An agent constructed with `weights=` reports `confidence` as **None**
  (fine-tuning does not update the calibration head). `neby-assist.js` routes
  on `confidence >= 0.35`, so a tuned model needs an alternate routing rule
  (e.g. act on `function_calls`, confirm on `suppressed_calls`) before shipping.
- The engine cannot unload weights: once a tuned `.cact` is bound, a base-model
  agent in the same process raises instead of answering. Keep tuned and base
  agents in separate processes.
- `needle.Needle(tools=[...], generation=2)` keeps running Needle 2 for
  existing deployments (this is how the unchanged Android runtime stays
  compatible).

## Quality gates before shipping a tuned model
- Accuracy on a held-out set of ~50 real user-style queries.
- Refusal rate on off-topic input stays sane (never fabricate a tool call).
- `confidence` distribution — set the UI threshold in `neby-assist.js`.
- Latency within ~10% of baseline (the +LoRA params are tiny; decode cost ~flat).
