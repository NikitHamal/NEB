# Qwen coding-agent harness

The background agent talks to `chat.qwen.ai` through a reverse-engineered
browser proxy. That path has **no native `tools` / function-calling field**.
Until this work, we papered over that with a custom JSON envelope
(`{"thought","actions","final"}`) that Qwen was never trained on.

That is the same class of gap the DeepSeek V4 Pro story is about: **Model +
Harness = Agent**. Vendor tables for V4-Pro-0813 moved Terminal-Bench 2.1
72.1 → 87.9 and DeepSWE 12.8 → 62.7; DeepSeek then open-sourced the harness
they used (`deepseek-ai/deepseek-harness`). Independent write-ups are
cautious about the exact deltas, but they agree on the mechanism: protocol,
observations, and the tool loop move agent scores as much as the weights.

## What we changed (Qwen first)

1. **In-distribution protocol.** Qwen-Agent / DashScope use Hermes/Nous XML:

   ```
   <tool_call>
   {"name": "read_file", "arguments": {"path": "src/app.py"}}
   </tool_call>
   ```

   The Qwen community path now advertises tools inside official `<tools>`
   tags and asks for that shape. `done` / `ask_user` replace the out-of-band
   `final` / `needs_input` flags.

2. **Parser is a superset.** One turn can be Hermes XML, Qwen `✿FUNCTION✿`
   markers, ```tool fences, or the legacy JSON envelope. Format repair now
   retries on `parse_ok` rather than a magic summary string.

3. **ACI observations.** Stored tool messages stay JSON (the session UI
   parses them). The *next* model prompt renders numbered file views and
   truncated, labelled results, wrapped in `<tool_response>` for Qwen.
   Prompt dumps of previous full model prompts (`kind=model_prompt`) are
   excluded from context.

4. **Loop.** Read-only tools in one turn run in parallel. Failed edits inject
   a one-line heal note. Repeated thought *or* identical tool sequences
   pause the session. Qwen output budget defaults to 8192.

5. **Tools.** `glob_files` plus `search_text(regex=, glob=)`. Live catalog
   stays at 17 advertised tools (Alibaba: keep the candidate set ≤ 20).

Official / BYOK providers still use the JSON envelope. Flip
`BACKGROUND_AGENT_QWEN_HARNESS=False` to disable the Qwen path.

## Files

- `api/background_agent/protocol.py` — multi-format parser
- `api/background_agent/qwen_harness/` — catalog, prompt, observe, recover, execute
- `api/test_qwen_harness.py` — parser, ACI, workspace, Hermes runner
- `benchmarks/qwen_harness_bench.py` — offline parse / token bench

```bash
DEBUG=1 DB_ENGINE=sqlite python manage.py test api.test_qwen_harness api.test_background_agent
DEBUG=1 DB_ENGINE=sqlite python benchmarks/qwen_harness_bench.py
```
