from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlencode

from django.urls import reverse

from api.background_agent.workspace import GitWorkspace

logger = logging.getLogger(__name__)


def _session_provider(session):
    """Provider block for session payloads — reflects the actual pick
    (Agnes/OpenAI/custom/qwen variants), not a hardcoded Qwen."""
    from api.llm.runtime import describe_session_llm
    llm = describe_session_llm(session)
    return {
        'id': session.bot_config_id,
        'name': llm['label'],
        'provider': llm['provider'],
        'model': llm['model'],
        'official': llm['official'],
        'thinkingMode': (session.llm_thinking_mode or 'auto').strip().lower(),
    }


def _branch_description(session):
    try:
        state = json.loads(session.agent_state or '{}')
        return str(state.get('branchDescription') or '').strip()
    except (TypeError, json.JSONDecodeError):
        return ''


def serialize_repo(repo):
    permissions = repo.get('permissions') or {}
    owner = repo.get('owner') or {}
    return {
        'id': repo.get('id'),
        'fullName': repo.get('full_name') or '',
        'name': repo.get('name') or '',
        'owner': owner.get('login') or '',
        'private': bool(repo.get('private')),
        'archived': bool(repo.get('archived')),
        'defaultBranch': repo.get('default_branch') or 'main',
        'description': repo.get('description') or '',
        'htmlUrl': repo.get('html_url') or '',
        'updatedAt': repo.get('updated_at') or '',
        'canPush': bool(permissions.get('push') or permissions.get('maintain') or permissions.get('admin')),
    }


def serialize_project(project):
    return {
        'id': str(project.id),
        'repoFullName': project.repo_full_name,
        'repoHtmlUrl': project.repo_html_url,
        'defaultBranch': project.default_branch,
        'preferredBaseBranch': project.preferred_base_branch or project.default_branch,
        'private': project.is_private,
        'status': project.status,
        'lastSyncedAt': project.last_synced_at,
        'lastError': project.last_error,
        'createdAt': project.created_at,
        'updatedAt': project.updated_at,
    }


def serialize_todos(session):
    try:
        todos = json.loads(getattr(session, 'todos_json', '') or '[]')
    except (TypeError, json.JSONDecodeError):
        return []
    if not isinstance(todos, list):
        return []
    clean = []
    for item in todos[:24]:
        if isinstance(item, dict) and item.get('content'):
            clean.append({'content': str(item['content'])[:220], 'status': str(item.get('status') or 'pending')})
    return clean


def serialize_session_summary(session):
    window = session.context_window_tokens or 131072
    return {
        'id': str(session.id),
        'projectId': str(session.project_id),
        'repoFullName': session.project.repo_full_name,
        'title': session.title,
        'goal': session.goal[:2000],
        'todos': serialize_todos(session),
        'sourceBranch': session.source_branch,
        'workBranch': session.work_branch,
        'branchDescription': _branch_description(session),
        'status': session.status,
        'progress': session.progress,
        'progressLabel': session.progress_label,
        'iteration': session.iteration,
        'maxIterations': session.max_iterations,
        'provider': _session_provider(session),
        'context': {
            'estimatedTokens': session.context_tokens_estimate,
            'windowTokens': window,
            'percent': min(100, round((session.context_tokens_estimate * 100) / max(1, window))),
            'compactions': session.context_compactions,
            'lastCompactionAt': session.last_compaction_at,
        },
        'summary': session.summary,
        'lastError': session.last_error,
        'createdAt': session.created_at,
        'startedAt': session.started_at,
        'updatedAt': session.updated_at,
        'completedAt': session.completed_at,
        'archived': bool(session.archived_at),
        'archivedAt': session.archived_at,
    }


def serialize_session_detail(session):
    data = serialize_session_summary(session)
    try:
        changed_files = json.loads(session.changed_files or '[]')
    except (TypeError, json.JSONDecodeError):
        changed_files = []
    diff = session.final_diff
    if session.workspace_path and Path(session.workspace_path).is_dir():
        try:
            workspace = GitWorkspace(session.project, session)
            changed_files = workspace.changed_files()
            diff = workspace.diff(max_chars=750000)
        except Exception:
            logger.debug('Could not build live background-agent diff for %s', session.id, exc_info=True)
    message_count = session.messages.count()
    messages = list(session.messages.prefetch_related('attachments').order_by('-created_at')[:250])
    messages.reverse()
    events = session.events.order_by('-id')[:200]
    actions = session.actions.order_by('-created_at')[:50]
    data.update({
        'baseSha': session.base_sha,
        'goal': session.goal,
        'headSha': session.head_sha,
        'changedFiles': changed_files,
        'diff': diff,
        'testSummary': session.test_summary,
        'messages': [serialize_message(message) for message in messages],
        'messageCount': message_count,
        'messagesTruncated': message_count > len(messages),
        'events': [serialize_event(event) for event in reversed(list(events))],
        'actions': [serialize_action(action) for action in actions],
        'artifacts': serialize_artifacts(session),
        'attachmentCount': session.attachments.count(),
        'workspaceReady': bool(session.workspace_path),
    })
    return data


def serialize_artifacts(session):
    return {
        artifact.kind: {
            'kind': artifact.kind,
            'fileName': artifact.file_name,
            'sizeBytes': artifact.size_bytes,
            'sha256': artifact.sha256,
            'downloadUrl': reverse('web:background_agent_download_artifact', args=[session.id, artifact.kind]),
        }
        for artifact in session.artifacts.all()
    }


def serialize_message(message):
    try:
        metadata = json.loads(message.metadata or '{}')
    except (TypeError, json.JSONDecodeError):
        metadata = {}
    attachments = []
    for attachment in message.attachments.all().order_by('created_at'):
        attachments.append({
            'id': attachment.id,
            'name': attachment.file_name,
            'kind': attachment.kind,
            'contentType': attachment.content_type,
            'sizeBytes': attachment.size_bytes,
            'extension': attachment.extension,
            'previewUrl': reverse('web:background_agent_session_preview', args=[message.session_id]) + '?' + urlencode({'attachment': attachment.id}),
        })
    return {
        'id': str(message.id),
        'role': message.role,
        'content': message.content,
        'label': metadata.get('label') or '',
        'metadata': metadata,
        'attachments': attachments,
        'createdAt': message.created_at,
    }


def serialize_event(event):
    try:
        payload = json.loads(event.payload or '{}')
    except (TypeError, json.JSONDecodeError):
        payload = {}
    return {
        'id': event.id,
        'type': event.event_type,
        'message': event.message,
        'payload': payload,
        'createdAt': event.created_at,
    }


def serialize_action(action):
    try:
        result = json.loads(action.result or '{}')
    except (TypeError, json.JSONDecodeError):
        result = {}
    return {
        'id': str(action.id),
        'action': action.action,
        'status': action.status,
        'result': result,
        'error': action.error,
        'createdAt': action.created_at,
        'startedAt': action.started_at,
        'completedAt': action.completed_at,
    }
