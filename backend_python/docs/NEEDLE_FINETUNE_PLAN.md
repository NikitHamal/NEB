# Needle 2 fine-tuning plan (NEBians Neby AI)

Goal: improve Neby AI's tool-calling accuracy on the NEB domain (resources,
notes, forum, navigation) by LoRA fine-tuning the frozen 45M base model, then
merging + quantizing to a new `.cact` that runs on the **same** WASM engine —
no engine re-compilation needed.

## Pipeline (from the official cactus-compute/needle repo)
```bash
pip install cactus-needle          # inference + finetune + build
# 1) (optional) synthesize training examples from the NEB tool schema
needle generate-data --tools neb_tools.json --num-samples 500 --output neb_data.jsonl
#    needs OPENROUTER_API_KEY.
# 2) LoRA fine-tune (base checkpoint auto-downloads from HF)
needle finetune neb_data.jsonl --epochs 3 --lora-rank 16 --lora-alpha 32 \
    --out neb_lora.pkl --generate 200
# 3) merge adapter + quantize to a tuned .cact (default 4-bit; --bits 2 smaller)
needle build checkpoints/needle2.pkl --lora neb_lora.pkl --out neb_needle.cact
# 4) smoke test the tuned model
python - <<'PY'
import needle
agent = needle.Needle(tools=TOOLS, weights="neb_needle.cact")
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
1. Back up `web/static/web/js/needle2/needle2.cact`.
2. Copy the tuned `neb_needle.cact` to `web/static/web/js/needle2/needle2.cact`.
   Same filename, same engine — nothing else changes.
3. In `needle.worker.js`, bump `RUNTIME_VERSION` and the `CACT_URL` query
   version. This invalidates the initialized IndexedDB snapshot and fetches the
   new model without evicting the unchanged WASM engine.
4. In Android `NeedleModelManager`, update `MODEL_SIZE_BYTES`, `MODEL_SHA256`,
   and the model URL query version. Bump the Android `snapshotNamespace` in
   `assets/needle2/bootstrap.html`, then copy the updated worker into app assets.
5. Redeploy static files (collectstatic + copy to public/static per AGENTS.md).
6. Re-run both `node benchmarks/needle_bench.mjs` and
   `node benchmarks/needle_snapshot_bench.mjs` to confirm quality, restored
   output equivalence, and latency.

## Quality gates before shipping a tuned model
- Accuracy on a held-out set of ~50 real user-style queries.
- Refusal rate on off-topic input stays sane (never fabricate a tool call).
- `confidence` distribution — set the UI threshold in `neby-assist.js`.
- Latency within ~10% of baseline (the +LoRA params are tiny; decode cost ~flat).
