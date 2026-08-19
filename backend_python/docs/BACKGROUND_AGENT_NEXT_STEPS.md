# Background Agent — 10+ next steps

Built on the production rework. Ordered roughly by impact → effort. Each item is scoped to the background agent itself.

## 1. Real-time streaming over WebSockets (replace 2.5s polling)
The app already runs Channels + Daphne. Today the session page polls `/events?after=` every 2.5s. Add a `background_agent.<session_id>` channel group and have `events.emit()` fan out a small payload; the page subscribes and renders deltas as they happen (token-by-token provider streaming if the provider supports SSE/streaming). Drops perceived latency from "a few seconds" to live.

## 2. Token-by-token model streaming in the transcript
Thread `call_ai_api` through a streaming path for providers that support it (Qwen/custom OpenAI-compatible). Surface a live "Agent is thinking…" line that fills in as tokens arrive, then collapse into the final thought. Pairs naturally with #1.

## 3. Provider-native function calling for models that support it
Qwen (web proxy, no native `tools` field) now uses the official Hermes/Nous `<tool_call>` protocol plus ACI observations — see `docs/QWEN_HARNESS.md`. Remaining work: optional `BotConfig` capability flag so official OpenAI-style providers send the toolset natively and skip JSON-format-repair.

## 4. Editor-backed diffs in the Files tab (syntax-highlighted, per-file)
Replace the plain file list + raw unified blob with a per-file, syntax-highlighted, side-by-side or unified view (e.g. a vendored `diff2html` or a small custom renderer). Add "jump to file" from a tool row. Currently the Files tab is a flat list and the Diff tab is one giant `<pre>`.

## 5. Inline file previews from tool rows
When a tool row is `Read`/`Edit`/`Write <path>`, make the path clickable to open a side panel showing that file's current content at the referenced lines (highlighted). This turns the transcript into a navigable work history instead of expandable blobs.

## 6. Workspace file browser (tree + open-on-GitHub)
Add a fifth tab, "Workspace", with a lazily-loaded tree of the task worktree (reuse the `list_files` tool against the server-side tree) so admins can browse exactly what the agent produced before deciding to push/open a PR.

## 7. Costs, tokens, and duration analytics
Track per-iteration prompt/completion token counts and wall-clock per session (new columns on `BackgroundAgentSession` + per-message metadata). Surface a compact summary card (iterations, tokens, cost estimate, total time) on the session header. Helps budget and compare providers.

## 8. Parallel actions within a turn
`_run_actions` runs a turn's actions sequentially. Read-only actions (`list_files`, `read_file`, `search_text`, `git_status`, `git_log`) could run concurrently (bounded thread pool) to cut latency on inspection-heavy turns. Keep mutations serial.

## 9. Auto-recovery from malformed tool calls
When a tool fails (e.g. `edit_file` "old_text not found"), the runner already continues; add an optional "self-heal" micro-turn: inject a concise system note ("your last edit failed because X; re-read the file and retry") so the model corrects in the next iteration instead of sometimes spiraling.

## 10. Configurable autonomy + safety policies per project
Let each project declare an autonomy profile: which tools are enabled, whether `run_command` may run, whether auto-push / auto-PR on completion is allowed, and branch-naming conventions. Store on `BackgroundAgentProject`; enforce in `ToolExecutor.execute` and `actions.process_action`.

## 11. Search + filter across sessions; per-project grouping on the dashboard
As session volume grows, add status/keyword filtering and group sessions by project on the dashboard (collapsible project sections with their sessions underneath). Add a simple search box.

## 12. Notifications when a session completes/fails
The worker already emits `session.completed`/`session.failed`. Wire those to the existing notification + FCM pipeline (or an in-admin toast/badge) so admins don't have to watch the page. Include a deep link to the session page.

## 13. Retry/resume a failed session with a one-click "retry from here"
Failed sessions currently require a new follow-up. Add a "Retry" control that re-queues from the last good durable state (`agent_state`) without losing the transcript, and surfaces the original error inline for context.

## 14. Pluggable sandbox backends (Firecracker / gVisor / nsjail)
The Docker sandbox is solid but heavyweight per command. For high-throughput deployments, add an nsjail or Firecracker microVM backend behind the same `BACKGROUND_AGENT_EXECUTION_BACKEND` switch for faster cold-starts while keeping the jail guarantees.

## 15. Observability: worker metrics + a small status dashboard
Emit Prometheus-style counters (sessions claimed, actions processed, tool success rate, mean iteration count, provider latency) and a `/backgroundagent/status` page showing worker health, queue depth, and recent failures — useful once multiple workers are running.
