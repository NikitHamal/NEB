"""Asynchronous post-run actions: push, PR creation, refresh and artifacts."""
from __future__ import annotations

import json
import logging

from api.background_agent.crypto import decrypt_secret
from api.background_agent.events import emit
from api.background_agent.github import GitHubClient
from api.background_agent.workspace import GitWorkspace
from api.models import BackgroundAgentAction
from api.utils import now_ms

logger = logging.getLogger(__name__)


def process_action(action: BackgroundAgentAction):
    if action.status != 'processing':
        action.status = 'processing'
        action.started_at = now_ms()
        action.save(update_fields=['status', 'started_at'])
    session = action.session
    workspace = GitWorkspace(session.project, session)
    try:
        payload = json.loads(action.payload or '{}')
    except (TypeError, json.JSONDecodeError):
        payload = {}
    try:
        event_type = ''
        event_message = ''
        if action.action == 'push':
            result = workspace.push()
            output = {'branch': session.work_branch, 'stdout': result.get('stdout', '')[-4000:]}
            event_type = 'github.pushed'
            event_message = f'Pushed {session.work_branch}'
        elif action.action == 'open_pr':
            workspace.push()
            client = GitHubClient(decrypt_secret(session.project.credential.encrypted_access_token))
            title = payload.get('title') or session.title or session.goal[:120]
            body = payload.get('body') or _default_pr_body(session)
            pr = client.find_open_pull_request(
                session.project.repo_full_name,
                head=session.work_branch,
                base=session.source_branch,
            )
            already_open = bool(pr)
            if not pr:
                pr = client.create_pull_request(
                    session.project.repo_full_name,
                    title=title,
                    head=session.work_branch,
                    base=session.source_branch,
                    body=body,
                    draft=bool(payload.get('draft', False)),
                )
            output = {
                'number': pr.get('number'),
                'url': pr.get('html_url'),
                'state': pr.get('state'),
                'draft': pr.get('draft', False),
                'alreadyOpen': already_open,
            }
            event_type = 'github.pr_found' if already_open else 'github.pr_opened'
            label = 'already open' if already_open else 'opened'
            event_message = f"Pull request #{pr.get('number')} {label}"
        elif action.action == 'refresh':
            workspace.ensure_mirror()
            output = {'syncedAt': session.project.last_synced_at}
            event_type = 'repository.refreshed'
            event_message = 'Repository mirror refreshed'
        elif action.action == 'artifacts':
            output = workspace.build_artifacts()
            event_type = 'artifacts.rebuilt'
            event_message = 'Download artifacts rebuilt'
        else:
            raise ValueError(f'Unknown action: {action.action}')
        action.status = 'completed'
        action.result = json.dumps(output, ensure_ascii=False)
        action.completed_at = now_ms()
        action.save(update_fields=['status', 'result', 'completed_at'])
        emit(session, event_type, event_message, output)
    except Exception as exc:
        logger.exception('Background agent action %s failed', action.id)
        action.status = 'failed'
        action.error = str(exc)[:8000]
        action.completed_at = now_ms()
        action.save(update_fields=['status', 'error', 'completed_at'])
        emit(session, 'action.failed', str(exc)[:1000], {'action': action.action})


def _default_pr_body(session):
    changed = []
    try:
        changed = json.loads(session.changed_files or '[]')
    except (TypeError, json.JSONDecodeError):
        pass
    changed_block = '\n'.join(f'- `{path}`' for path in changed[:100]) or '- No tracked changes listed'
    return f'''## Summary
{session.summary or session.goal}

## Changed files
{changed_block}

## Validation
{session.test_summary or 'See the agent activity log for commands and results.'}

---
Created by the NEBians Background Agent from `{session.source_branch}` into `{session.work_branch}`.
'''
