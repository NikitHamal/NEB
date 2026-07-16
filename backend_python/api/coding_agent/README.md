# Background Coding Agent

SOTA, Google-Jules-style autonomous coding agent that lives inside the NEBians admin
panel. Each session gets its own isolated branch in a cloned copy of a GitHub repo
the admin connects via OAuth, and runs in the background — close the browser or
walk away from Wi-Fi and the work continues until stopped.

## Highlights

- **Runs forever in the background** — state is persisted to the database, the
  worker daemon (`python manage.py run_coding_agent_worker`) polls every 4 s,
  even when the admin tab is closed.
- **Per-session branch, never `main`** — each session is checked out from the
  project's default branch and renamed to `agent/<task-slug>-<randid>`.
- **Stop / pause / resume** — admins pause, resume or stop the agent from the
  session detail page; the worker reads the DB state before every step.
- **Interrupt / follow-up** — admins post messages into the conversation at
  any moment; the agent picks them up on the next iteration without resetting
  context.
- **ZIP download of the diff** — pulls the unified diff, the commit log and a
  fresh copy of every changed file; ready to push manually or open as PR.
- **Manual push to GitHub** — `git push` against the same OAuth connection.
- **Open PR** — `POST /repos/owner/name/pulls` via the API; the session flips
  to `pr_opened` and the PR URL is shown in the UI.
- **Reuses every AI provider NEBians already has** — Qwen (`chat.qwen.ai`),
  AI4Bharat Arena, eGov Chat AI, DeepAI, Inception Labs Mercury 2, plus any
  custom OpenAI-compatible endpoint. The agent's prompt is tuned to each
  provider's quirks (long-context, vision etc).

## Why a prompt-based tool-call format

Most of the providers we support (all of them except the `custom` / OpenAI-compatible
mode, technically) refuse to honour OpenAI's `tools` JSON schema. The agent
therefore asks the model to emit fenced ```` ```tool ```` blocks with a YAML-ish
`name:` / `args:` layout, which we parse and execute locally. The block format
is documented in `constants.py:AGENT_DEFAULT_SYSTEM_PROMPT`. The runtime's
`_build_messages_for_provider` re-renders past tool calls/results in the same
shape on subsequent turns so the model stays in-distribution.

## Components

```
api/coding_agent/
├── apps.py                — app config (label = `coding_agent`)
├── models.py              — CodingAgentProject / Session / Message /
│                            ToolCall / FileChange / Event
├── constants.py           — tool spec, language model defaults, prompt rules
├── tool_parser.py         — tolerant YAML-ish ```tool fence parser
├── tools.py               — registered tools (read_file, edit_file,
│                            write_file, list_files, grep, find_files,
│                            run_shell, delete_file, rename_file,
│                            git_diff, git_log, git_commit, ask_user, done)
├── git_workspace.py       — cloning, branch creation, push, PR open
├── provider_adapter.py    — single call_for_agent() dispatch across providers
├── runtime.py             — AgentRuntime: bootstrap + step + per-call execution
├── worker.py              — advance_queued_sessions() poll loop
├── management/commands/
│   └── run_coding_agent_worker.py — daemon ("python manage.py run_coding_agent_worker")
├── realtime.py            — channel-layer broadcast helpers
├── urls.py                — admin pages + AJAX endpoints
├── views.py               — full page + JSON endpoints
└── (no migrations are nested here — see api/migrations/0083_coding_agent_models.py)
```

## Database tables (added in migration `0083_coding_agent_models.py`)

- `coding_agent_projects`     (~one row per connected GitHub repo)
- `coding_agent_sessions`     (~one row per task)
- `coding_agent_messages`     (every turn: system / user / assistant / tool)
- `coding_agent_tool_calls`   (every individual tool invocation, for audit + ZIP)
- `coding_agent_file_changes` (file-level CREATE/MODIFY/DELETE/RENAME rows)
- `coding_agent_events`       (timeline: status, tool, log, push, pr, interrupt)

## Configuration / prerequisites

The agent reuses **all the same OAuth credentials NEBians already uses for
GitHub login** — `settings.GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`. Set them
once and:

1. Admins go to `/admin/background-agent/`.
2. Click _Connect GitHub_ → standard OAuth flow → land back on _Add project_.
3. Pick a repo from the dropdown (or search GitHub).
4. (Optionally) override the provider/model for this project.
5. _Connect this repository_ → `CodingAgentProject` row created, repo cloned
   under `/tmp/coding_agent_workspaces/<owner>__<repo>` (override with the
   `CODING_AGENT_WORKSPACE_ROOT` env var).

No new service account, no SSH key handling, no new server config.

## Running the worker

```bash
cd /home/consicac/nebians_api
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate

python manage.py run_coding_agent_worker --interval 4 --max-sessions 2 --max-steps 6
```

The worker is crash-safe — it re-reads session status before every step; a
session that was running when the worker died appears as a stalled-running row
and is picked up the next cycle (with `last_activity_at < now - 90 s`).

Recommended cron / systemd:

```
@reboot  cd /home/consicac/nebians_api && \
  source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && \
  python manage.py run_coding_agent_worker --interval 4 >> \
  /home/consicac/nebians_api/logs/coding_agent_worker.log 2>&1
```

## Frontend

- `/admin/background-agent/`                  · project list
- `/admin/background-agent/projects/new/`     · connect a GitHub repo
- `/admin/background-agent/projects/<id>/`   · project detail + new session form
- `/admin/background-agent/sessions/<id>/`    · live session detail with chat,
-                                             timer, file changes, diff, push,
-                                             PR, ZIP download

The session detail page subscribes to the existing WebSocket channel layer
(`agent.<session_id>` and `agent.user.<user_id>`) — same Channels + Redis
backend as the rest of the site — so admins see tool events, status flips and
message additions in real time.

## Operational notes

- **Workspace cleanup** — `workspace_root()/owner__repo` is shared per project
  and reused across sessions, so re-running a session against the same repo
  does not re-clone.
- **Concurrency** — `git_workspace._lock_for()` ensures two sessions of the
  same project never collide. The worker advances sessions serially per poll
  cycle by default; bump `--max-sessions` if you need fan-out.
- **Token storage** — `Project.access_token` is a long-lived OAuth token scoped
  to the OAuth flow used at connect time (default `repo`). Rotate by hitting
  the _Refresh_ button on the project page (re-fetches repo metadata + runs a
  fresh `git fetch` from upstream).
- **PR body** — auto-generated; includes the task, list of changed files,
  model name, iteration count and session id.
- **Diff source for ZIP** — `git diff origin/<base>...<branch>`; callers get a
  unified patch + every changed file's current contents + the session JSON
  metadata, all bundled as `<repo>-<session>.zip`.
