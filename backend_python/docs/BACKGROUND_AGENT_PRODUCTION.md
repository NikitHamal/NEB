# NEBians Background Agent — production deployment

The Background Agent is a **standalone product**, separate from the Django admin panel. It lives at `/backgroundagent` with its own login screen at `/backgroundagent/login`. Admins sign in with their **platform account** (`api.User`) using a username **or** email plus a password (only accounts with `is_admin` are admitted). The dashboard lists projects + sessions; each session opens on its own dedicated page at `/backgroundagent/session/<id>`. Sessions are database-backed and execute in a separate worker, so closing the browser does not stop a task.

## Authentication model

- Sign-in is independent of Django's `auth.User` / the `/admin/` staff login (left untouched) and of the public site's bearer-token auth.
- The signed-in admin is kept in the session and surfaced as `request.bg_admin`. GitHub OAuth credentials are bound to this same `api.User` account, so the same admin **does not re-authorize when signing in from another device**.
- The existing `/admin/` username login continues to work unchanged for the rest of the admin panel; the agent simply no longer appears in the admin sidebar.

## GitHub OAuth (single callback URL)

The agent authorizes with broad repository scopes (`repo workflow read:org user:email`) but reuses the **existing** `/auth/github/callback/` redirect URI (one registered URL in your GitHub OAuth App). The agent marks its request with a signed `bg::` state; the shared callback recognises it, exchanges the code, and stores the token against the signed-in admin's `BackgroundAgentCredential` — no NEBians account is created or changed.

## What the agent can do

The agent works on a dedicated task branch (never the base branch) and has a full toolset. There is **no iteration cap** — it keeps working until the goal is genuinely complete, it explicitly asks for input, an admin pauses/stops it, or an unrecoverable error occurs.

| Category | Tools |
| --- | --- |
| Read / explore | `list_files`, `read_file`, `search_text` |
| Edit | `edit_file`, `multi_edit` (robust search-and-replace, tolerant to whitespace drift, with helpful "closest match" errors), `write_file`, `apply_patch` (forgiving: 3-way → recount → GNU `patch --merge --fuzz`), `delete_file` |
| Filesystem | `copy_file`, `move_file`, `create_directory` |
| Git | `git_status`, `git_diff`, `git_log`, `git_stage`, `git_commit`, `git_push`, `git_pull`, `git_restore` |
| Validate | `run_command` (argv array, sandboxed) |

Every tool call renders as a **single clean line** in the transcript (e.g. `Read src/app.py`, `Edit api/models.py`, `Run python -m pytest`) with an expandable result panel — no more start/result/completed triple.

### Why `edit_file` is preferred over `apply_patch`
Raw unified patches require exact context, which is why "the patch tool almost always failed" — the model drifts on whitespace/line counts. `edit_file`/`multi_edit` use exact-byte matching first, then fall back to whitespace-normalised matching, and return the closest line range when the block can't be found so the agent can re-read and retry. `apply_patch` is still available and now tries three progressively more forgiving strategies before giving up.

## 1. Apply the database migrations

```bash
python manage.py migrate
```

Two background-agent migrations exist: `0083` creates the tables, and `0084` re-points the ownership fields (`admin_user`/`requested_by`) from Django's `auth.User` to the platform account model (`api.User`) so the agent authenticates platform admins and binds the GitHub credential to their account. GitHub OAuth tokens are encrypted with AES-GCM using key material derived from Django's `SECRET_KEY`. Keep that key stable; changing it invalidates retained credentials.

## 2. Configure GitHub OAuth

Create or reuse a GitHub OAuth App and set its callback URL to:

```text
https://YOUR_DOMAIN/backgroundagent/github/callback
```

Set `BACKGROUND_AGENT_GITHUB_CLIENT_ID` and `BACKGROUND_AGENT_GITHUB_CLIENT_SECRET`. The requested scopes are configured through `BACKGROUND_AGENT_GITHUB_SCOPES`. The default supports private repositories, workflow-file changes, organization repositories and email identity.

The OAuth flow stores the connection per Django staff user. The dashboard reflects the live connection state from the server on every load (no stale connect/authorize buttons when already authorized).

## 3. Build the execution sandbox

```bash
docker build -t nebians-background-agent-sandbox:latest docker/background-agent
```

Production defaults require Docker. Each model-issued command runs in an ephemeral container with:

- no network by default;
- all Linux capabilities dropped;
- a read-only root filesystem;
- CPU, memory and process limits;
- only the current worktree mounted read/write;
- Git metadata and repository history hidden from model-issued commands;
- credential-like files masked inside the sandbox and excluded from agent file tools, diffs, commits and artifacts.

Set `BACKGROUND_AGENT_DOCKER_NETWORK=bridge` only when a task must download dependencies. Local command execution is disabled by default because a host process is not a security boundary. It can be explicitly enabled for trusted local development with `BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION=True` and `BACKGROUND_AGENT_EXECUTION_BACKEND=local`.

## 4. Use persistent storage

Set `BACKGROUND_AGENT_ROOT` to a persistent path writable by the web and worker service, such as `/var/lib/nebians/background-agent`. The directory contains bare repository caches, isolated task worktrees and generated artifacts. Do not use ephemeral container storage unless the path is mounted as a persistent volume.

## 5. Run one or more durable workers

```bash
python manage.py run_background_agent_worker --interval 2
```

Multiple worker processes are supported. Database row locking prevents duplicate claims, and a per-project filesystem lock serializes Git mirror mutations. Stale sessions and actions are re-queued when a worker restarts.
Each process also writes a database heartbeat every ten seconds; the admin UI reports the queue as offline when no recent worker heartbeat is present.

## Frontend

- **Dashboard** (`/backgroundagent`): GitHub connection, project sidebar, composer (repository / base branch / provider — no iteration control), and a sessions list. Each session links to its own page.
- **Session page** (`/backgroundagent/session/<id>`): full-screen transcript with smart auto-scroll (sticks to bottom while you're reading the latest, stops if you scroll up to inspect history, and snaps to bottom again when the session completes), single-line tool rows with expandable results, Files / Diff / Deliver tabs, and push / pull-request controls.

Both screens are built on the project Material 3 design system (`material3.css`, Poppins, Material Symbols, the project `--md-primary` blue) and support light + dark themes.
