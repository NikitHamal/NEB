# Needle 2 Local LLM Fine-Tuning & Reinforcement Learning (DPO/RLHF) for p5.js Art

This guide outlines the complete pipeline for fine-tuning, RL alignment (Direct Preference Optimization / DPO), and WASM model deployment of the Needle 2 local LLM (45M parameters) for p5.js artwork generation.

---

## 1. Dataset Generation
We generate synthetic structured JSONL training samples mapping natural language art requests to the `generate_p5_art` tool schema.

```bash
python backend_python/web/generate_p5_needle_dataset.py
```

Sample entry in `p5_needle_dataset.jsonl`:
```json
{
  "query": "paint a glowing cosmic nebula with p5.js",
  "tools": [{"name": "generate_p5_art", "parameters": {"prompt": "paint a glowing cosmic nebula", "style": "generative", "color_palette": "neon", "complexity": "high"}}],
  "answers": [{"name": "generate_p5_art", "arguments": {"prompt": "paint a glowing cosmic nebula", "style": "generative", "color_palette": "neon", "complexity": "high"}}],
  "reasoning": "User wants p5.js artwork of 'paint a glowing cosmic nebula'. Mapped to generate_p5_art with style='generative', color_palette='neon', complexity='high'."
}
```

---

## 2. LoRA Fine-Tuning (SFT)
Run supervised fine-tuning using `cactus-needle` CLI:

```bash
pip install cactus-needle

# LoRA fine-tune on p5.js dataset
needle finetune backend_python/web/p5_needle_dataset.jsonl \
    --epochs 4 \
    --lora-rank 16 \
    --lora-alpha 32 \
    --learning-rate 3e-4 \
    --out neb_p5_lora.pkl \
    --generate 200
```

---

## 3. Reinforcement Learning (DPO / RLHF Alignment)
To maximize artwork aesthetic quality, visual variety, and code correctness without runtime crashes:

1. **Reward Function Definition:**
   - **Syntax & Execution (+1.0):** Code compiles and renders in p5.js canvas without JavaScript runtime errors.
   - **Aesthetic Diversity (+0.5):** Uses non-trivial color palettes and noise/trigonometric motion (`noise()`, `sin()`, `cos()`).
   - **User Alignment (+0.5):** Correctly matches requested style (`fractal`, `mandala`, `landscape`, `flow field`).

2. **DPO (Direct Preference Optimization):**
   - Pair accepted completions $y_w$ (valid p5.js code rendering smooth 60 FPS animations) against rejected completions $y_l$ (blank screens, static points, syntax errors).
   - Train DPO loss with preference pairs:
     $$\mathcal{L}_{DPO} = -\log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)} \right)$$

---

## 4. WASM Build & Quantization
Merge LoRA adapter weights and quantize into `.cact` format for on-device browser WASM execution:

```bash
# Build quantized model (.cact)
needle build checkpoints/needle2.pkl --lora neb_p5_lora.pkl --out web/static/web/js/needle2/needle2.cact
```

---

## 5. Deployment & Quality Verification
1. Bump `RUNTIME_VERSION` in `web/static/web/js/needle2/needle.worker.js`.
2. Run benchmark harnesses to confirm latency and tool-calling accuracy:
   ```bash
   node backend_python/benchmarks/needle_bench.mjs
   node backend_python/benchmarks/needle_snapshot_bench.mjs
   ```
