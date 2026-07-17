# Background Agent — Full Production Rework (execution plan)

Scope: the durable background coding agent (`/backgroundagent`). End-to-end, production-ready.

## Problems found (from code + screenshots)
1. **Theme mismatch** — page uses its own purple accent (`--ba-accent:#7563ff`) instead of the project Material‑3 blue (`--md-primary:#004ac6`). Bloatware copy ("Durable server‑side coding").
2. **Connect/Authorize logic** — even when authorized, connect/authorize CTAs can show. Needs single source of truth from server context + API.
3. **Add‑repo dialog** — broken flow/logic.
4. **Auto‑scroll** — conversation re-render fights the user; no clean "stick to bottom" + scroll‑on‑finish.
5. **Sessions cramped in one screen** — composer + sidebar + detail all in one page. Sessions should open in their own dedicated route/page.
6. **Patch tool almost always fails** — `git apply --whitespace=nowarn` is too strict (exact context required). No edit/search‑replace alternative.
7. **Max iterations** — present (hard cap). User wants it removed entirely.
8. **Tool rendering** — emits `tool.started` → result → `tool.completed` (3 rows). Should be ONE clean line: `Read …`, `Write …`, `Edit …`, `Delete …`, `Copy …`, `Move …`, `Create dir …`, `List …`, `Search …`, `Commit …`, `Stage …`, `Push …`, `Pull …`, etc.
9. **Limited toolset** — no edit/str_replace, copy, move, mkdir, git stage/commit/pull/push/log.

## Implementation
- **Backend tools** (`workspace.py` `ToolExecutor`): add `edit_file` (robust str_replace w/ fuzzy fallback), `multi_edit`, `copy_file`, `move_file`, `create_directory`, `git_stage`, `git_commit`, `git_push`, `git_pull`, `git_log`, `git_restore`. Make `apply_patch` robust (`--3way` → `--recount`/`--whitespace=fix` → GNU `patch --merge --fuzz`). Keep only credential/secret path guards (never leak tokens to the AI provider); relax everything else.
- **Labels** (new `labels.py`): single `tool_label()` used by runner (event/message) and mirrored in JS.
- **Runner** (`runner.py`): remove the iteration cap (loop until `final`/`needs_input`/control/error, with no-op stuck detection that is NOT an iteration limit). One clean `tool.executed`/`tool.failed` event + one tool message per call (with `metadata.label`). Updated system prompt documenting the full toolset.
- **Views** (`views_background_agent.py`): add dedicated session page route + serialise `label` on tool messages. Keep all existing endpoints.
- **URLs** (`web/urls.py`): add `backgroundagent/session/<id>` page route.
- **Templates**: rebuild `background_agent.html` (clean dashboard) + new `background_agent_session.html` (dedicated session screen), using Material‑3 tokens, Poppins, Material Symbols, project blue. Remove bloatware.
- **CSS**: rewrite `background-agent.css` on the design system; add session‑page styles.
- **JS**: split into dashboard (`background-agent.js`) + session (`background-agent-session.js`). Fix connect/disconnect, dialog, smart auto‑scroll, single‑line tool rendering, tabs, delivery.
- **Docs/tests**: update production doc + add tool/patch harness; list 10+ next steps.

## Validation
- `python manage.py check` (imports/urls/templates).
- Standalone harness exercising read/write/edit/multi_edit/copy/move/mkdir/delete/apply_patch/git tools against a real git worktree.
- `node --check` on both JS files.
