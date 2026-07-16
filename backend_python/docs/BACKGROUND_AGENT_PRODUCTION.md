# NEBians Background Agent — production deployment

The admin-only UI is available at `/backgroundagent`. Sessions are database-backed and execute in a separate worker, so browser closure or client disconnection does not stop a task.

## 1. Apply the database migration

```bash
python manage.py migrate
```

The feature adds project, session, message, event, artifact, credential and action tables. GitHub OAuth tokens are encrypted with AES-GCM using key material derived from Django's `SECRET_KEY`. Keep that key stable; changing it invalidates retained credentials.

## 2. Configure GitHub OAuth

Create or reuse a GitHub OAuth App and set its callback URL to:

```text
https://YOUR_DOMAIN/backgroundagent/github/callback
```

Set `BACKGROUND_AGENT_GITHUB_CLIENT_ID` and `BACKGROUND_AGENT_GITHUB_CLIENT_SECRET`. The requested scopes are configured through `BACKGROUND_AGENT_GITHUB_SCOPES`. The default supports private repositories, workflow-file changes, organization repositories and email identity.

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

Example systemd unit:

```ini
[Unit]
Description=NEBians Background Agent Worker
After=network-online.target docker.service
Requires=docker.service

[Service]
Type=simple
User=nebians
Group=nebians
WorkingDirectory=/srv/nebians/backend
EnvironmentFile=/srv/nebians/backend/.env
ExecStart=/srv/nebians/venv/bin/python manage.py run_background_agent_worker --interval 2 --recover-after 900
Restart=always
RestartSec=5
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
```

## 6. Operational notes

- The source branch is treated as a read-only base. Every task gets a generated `nebians-agent/...` branch.
- Push and pull-request creation are explicit asynchronous actions from the session UI.
- Changed-file ZIPs include a manifest and `changes.patch`; deleted files are represented in the patch and manifest.
- Provider output is never executed directly. Providers without native tool calling must return the strict JSON action protocol; malformed output moves the session to a safe waiting state.
- Keep the web process and workers on hosts that can see the same database and `BACKGROUND_AGENT_ROOT`.
- Monitor `background_agent_sessions.last_heartbeat_at`, failed actions, worker logs and disk usage. Apply normal artifact-retention and repository-cache cleanup policies for your deployment.
