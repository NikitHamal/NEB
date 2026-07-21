"""CI auto-fix watcher.

For every project with ``autofix_enabled`` set, new *failed* GitHub Actions
runs are turned into background-agent repair sessions: the failing job log
is captured, a task is queued with the log attached, and the normal worker
pipeline works the fix and pushes the branch on completion.

Guards against runaway loops:
  * one session per failing workflow run (unique ``run_id``)
  * one session per ``head_sha`` (re-runs of the same commit are skipped)
  * max DAILY_LIMIT auto-fix sessions per project per 24h
  * no new session while the project already has an active one
"""
from __future__ import annotations

import logging

from django.conf import settings
from django.db import transaction

from api.background_agent.crypto import decrypt_secret
from api.background_agent.events import add_message, emit
from api.background_agent.github import GitHubClient, GitHubError
from api.models import (
    BackgroundAgentAutofixRun,
    BackgroundAgentProject,
    BackgroundAgentSession,
    BotConfig,
)
from api.utils import now_ms, uuid_str

logger = logging.getLogger(__name__)

ACTIVE_SESSION_STATUSES = ('queued', 'preparing', 'running')
LOG_TAIL_CHARS = 6000
DAILY_LIMIT = 3

# Matches the provider resolution the mobile API uses for user-created tasks.
# Any enabled qwen bot counts (bot_config is nullable and only feeds the
# legacy default) — never pinned to one hardcoded model id, and BYOK-only
# setups still count as a usable backend via default_model_state().
def _provider() -> BotConfig | None:
    return BotConfig.objects.filter(enabled=True, provider='qwen').first()


def _backend_usable(admin) -> bool:
    """True when *some* LLM backend can serve an autofix session (qwen bot,
    legacy provider row, or a resolvable official/BYOK preset)."""
    try:
        from api.llm.runtime import default_model_state
        return bool(default_model_state(admin).get('configured'))
    except Exception:
        return _provider() is not None


def scan_failed_runs(max_sessions: int = 3) -> int:
    """One scan over every auto-fix-enabled project. Returns sessions queued."""
    created = 0
    projects = BackgroundAgentProject.objects.filter(autofix_enabled=True).select_related('credential', 'admin_user')
    for project in projects:
        if created >= max_sessions:
            break
        try:
            created += _scan_project(project)
        except Exception:  # noqa: BLE001
            logger.exception('autofix scan failed for project %s', project.repo_full_name)
    return created


@transaction.atomic
def _queue_autofix_session(project, run: dict, provider, goal: str, now: int) -> BackgroundAgentSession:
    run_id = int(run.get('id') or 0)
    workflow = (run.get('name') or 'workflow').strip()[:255]
    branch = (run.get('head_branch') or project.preferred_base_branch or project.default_branch).strip()[:255]
    session = BackgroundAgentSession.objects.create(
        id=uuid_str(),
        project=project,
        admin_user=project.admin_user,
        bot_config=provider,
        title=f'Auto-fix CI: {workflow}'[:255],
        goal=goal,
        source_branch=branch,
        status='paused',
        context_window_tokens=int(getattr(settings, 'BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS', 131072)),
        created_at=now,
        updated_at=now,
    )
    add_message(session, 'user', goal, {'kind': 'initial_goal', 'source': 'autofix'})
    session.status = 'queued'
    session.progress_label = 'Queued for CI auto-fix'
    session.updated_at = now
    session.save(update_fields=['status', 'progress_label', 'updated_at'])
    emit(session, 'session.queued', 'Auto-fix task queued from a failing CI run', {
        'repository': project.repo_full_name,
        'runId': run_id,
        'workflow': workflow,
        'branch': branch,
    })
    BackgroundAgentAutofixRun.objects.create(
        id=uuid_str(),
        project=project,
        run_id=run_id,
        head_sha=(run.get('head_sha') or '')[:64],
        branch=branch,
        workflow_name=workflow,
        session=session,
        created_at=now,
    )
    return session


def _scan_project(project) -> int:
    credential = project.credential
    if not credential or not credential.is_connected:
        return 0
    try:
        token = decrypt_secret(credential.encrypted_access_token)
    except ValueError:
        return 0
    provider = _provider()
    if not _backend_usable(project.admin_user):
        logger.warning('autofix: no usable LLM backend; skipping %s', project.repo_full_name)
        return 0

    client = GitHubClient(token)
    ignore_branch = (project.preferred_base_branch or project.default_branch or '').strip().lower()
    try:
        runs = client.list_workflow_runs(project.repo_full_name, status_filter='failure', per_page=10)
    except GitHubError as exc:
        logger.info('autofix: workflow runs unavailable for %s: %s', project.repo_full_name, exc)
        return 0
    if not runs:
        return 0

    now = now_ms()
    day_ago = now - 86_400_000
    for run in runs:
        run_id = int(run.get('id') or 0)
        head_sha = (run.get('head_sha') or '').strip()
        branch = (run.get('head_branch') or '').strip().lower()
        if not run_id:
            continue
        if branch == ignore_branch:
            continue
        if BackgroundAgentAutofixRun.objects.filter(project=project, run_id=run_id).exists():
            continue
        if head_sha and BackgroundAgentAutofixRun.objects.filter(project=project, head_sha=head_sha).exists():
            continue
        if BackgroundAgentAutofixRun.objects.filter(project=project, created_at__gte=day_ago).count() >= DAILY_LIMIT:
            break
        if BackgroundAgentSession.objects.filter(
            project=project, archived_at=0, status__in=ACTIVE_SESSION_STATUSES
        ).exists():
            break

        failing_jobs: list[dict] = []
        log_tail = ''
        try:
            jobs = client.list_run_jobs(project.repo_full_name, run_id)
            failing_jobs = [
                job for job in jobs
                if (job.get('conclusion') or '').lower() in ('failure', 'timed_out')
            ]
            target = failing_jobs[0] if failing_jobs else (jobs[0] if jobs else None)
            if target:
                log_tail = client.get_job_log_text(project.repo_full_name, int(target.get('id') or 0))[-LOG_TAIL_CHARS:]
        except GitHubError as exc:
            logger.info('autofix: job logs unavailable for run %s: %s', run_id, exc)

        goal = _build_goal(project, run, failing_jobs, log_tail)
        _queue_autofix_session(project, run, provider, goal, now)
        logger.info('autofix: queued repair session for %s run %s', project.repo_full_name, run_id)
        return 1
    return 0


def _build_goal(project, run: dict, failing_jobs: list[dict], log_tail: str) -> str:
    workflow = (run.get('name') or 'workflow').strip()
    branch = (run.get('head_branch') or project.preferred_base_branch or project.default_branch).strip()
    run_url = run.get('html_url') or ''
    job_lines = '\n'.join(
        f'- {job.get("name", "job")}: {job.get("conclusion") or job.get("status") or "unknown"}'
        for job in failing_jobs[:5]
    ) or '- (failing jobs could not be enumerated)'

    return f"""A GitHub Actions run failed for {project.repo_full_name}. Fix the failure and make CI green again.

## Failure context
- Workflow: {workflow}
- Branch: {branch}
- Run: {run_url}

## Failing jobs
{job_lines}

## Raw log (tail of the first failing job)
```
{log_tail.strip() if log_tail.strip() else '(log unavailable - inspect the workflow file and recent changes instead)'}
```

## Your task
1. Study the workflow file(s) under .github/workflows and the log above to find the ROOT cause (do not patch symptoms).
2. Apply the minimal, correct fix.
3. If a quick local validation exists (build, tests, lint - whatever this repo supports and is fast), run it.
4. Do NOT modify the workflow file just to silence the failure; only change it if the workflow itself is genuinely broken.
5. Finish with a summary - the branch is pushed automatically and CI will re-run.

This task was created automatically by Zeus auto-fix."""
