"""Task queue management for the background coding agent.

Handles enqueueing tasks, status transitions, and WebSocket broadcasts.
Follows the same pattern as api/generation.py.
"""
import json
import logging

from django.core.cache import cache

from api.models import CodingTask, CodingActionLog, CodingTaskMessage
from api.utils import now_ms, uuid_str

logger = logging.getLogger(__name__)

TASK_TTL_MS = 48 * 60 * 60 * 1000  # 48 hours


def enqueue_task(project_id, title, goal, branch_name, created_by_id, provider='ai4bharat', model_id=''):
    """Create a queued coding task and return it."""
    task = CodingTask.objects.create(
        id=uuid_str(),
        project_id=project_id,
        title=title,
        goal=goal,
        branch_name=branch_name,
        status=CodingTask.STATUS_QUEUED,
        created_by_id=created_by_id,
        provider=provider,
        model_id=model_id,
        created_at=now_ms(),
        updated_at=now_ms(),
    )
    _notify_worker()
    logger.info('enqueue_task: task %s project=%s', task.id, project_id)
    return task


def get_pending_tasks(limit=3):
    """Return tasks that should be processed: queued or running (resumed)."""
    tasks = list(
        CodingTask.objects.filter(status=CodingTask.STATUS_QUEUED)
        .order_by('created_at')[:limit]
    )
    resumed = list(
        CodingTask.objects.filter(status=CodingTask.STATUS_RUNNING)
        .order_by('updated_at')[:limit]
    )
    return tasks + resumed


def mark_running(task):
    """Mark a task as running."""
    now = now_ms()
    CodingTask.objects.filter(pk=task.id).update(
        status=CodingTask.STATUS_RUNNING,
        started_at=now if not task.started_at else task.started_at,
        updated_at=now,
    )
    task.status = CodingTask.STATUS_RUNNING
    task.updated_at = now
    _broadcast(task, 'task.started', {})


def mark_paused(task, reason=''):
    """Mark a task as paused (e.g. waiting for user input)."""
    now = now_ms()
    CodingTask.objects.filter(pk=task.id).update(
        status=CodingTask.STATUS_PAUSED,
        paused_at=now,
        updated_at=now,
    )
    task.status = CodingTask.STATUS_PAUSED
    task.paused_at = now
    task.updated_at = now
    _broadcast(task, 'task.paused', {'reason': reason})


def mark_completed(task, pr_url='', pr_number=None):
    """Mark a task as completed."""
    now = now_ms()
    CodingTask.objects.filter(pk=task.id).update(
        status=CodingTask.STATUS_COMPLETED,
        completed_at=now,
        updated_at=now,
        pr_url=pr_url,
        pr_number=pr_number,
    )
    task.status = CodingTask.STATUS_COMPLETED
    task.completed_at = now
    task.updated_at = now
    task.pr_url = pr_url
    if pr_number:
        task.pr_number = pr_number
    _broadcast(task, 'task.completed', {'prUrl': pr_url, 'prNumber': pr_number})


def mark_failed(task, error):
    """Mark a task as failed."""
    now = now_ms()
    CodingTask.objects.filter(pk=task.id).update(
        status=CodingTask.STATUS_FAILED,
        completed_at=now,
        updated_at=now,
    )
    task.status = CodingTask.STATUS_FAILED
    task.completed_at = now
    task.updated_at = now
    _broadcast(task, 'task.failed', {'error': str(error)[:500]})


def mark_stopped(task):
    """Mark a task as stopped by user."""
    now = now_ms()
    CodingTask.objects.filter(pk=task.id).update(
        status=CodingTask.STATUS_STOPPED,
        completed_at=now,
        updated_at=now,
    )
    task.status = CodingTask.STATUS_STOPPED
    task.completed_at = now
    task.updated_at = now
    _broadcast(task, 'task.stopped', {})


def update_iteration(task, iteration, thought=''):
    """Update the iteration count and last thought."""
    CodingTask.objects.filter(pk=task.id).update(
        iteration=iteration,
        last_thought=thought[:2000],
        updated_at=now_ms(),
    )
    task.iteration = iteration
    task.last_thought = thought[:2000]
    task.updated_at = now_ms()
    _broadcast(task, 'task.progress', {'iteration': iteration, 'thought': thought[:300]})


def log_action(task, iteration, action_type, description='', file_path='', content_diff='', status='ok'):
    """Create an action log entry."""
    log = CodingActionLog.objects.create(
        id=uuid_str(),
        task_id=task.id,
        iteration=iteration,
        action_type=action_type,
        description=description[:2000],
        file_path=file_path[:500],
        content_diff=content_diff[:5000],
        status=status,
        created_at=now_ms(),
    )
    _broadcast(task, 'task.action', {
        'actionType': action_type,
        'description': description[:200],
        'filePath': file_path[:200],
        'status': status,
    })
    return log


def cancel_stale_tasks():
    """Cancel queued tasks older than TASK_TTL_MS."""
    cutoff = now_ms() - TASK_TTL_MS
    stale = CodingTask.objects.filter(
        status=CodingTask.STATUS_QUEUED,
        created_at__lt=cutoff,
    )
    count = stale.update(status=CodingTask.STATUS_STOPPED, completed_at=now_ms())
    if count:
        logger.info('cancel_stale_tasks: cancelled %d stale tasks', count)


def cleanup_old_tasks(days=30):
    """Delete old terminal tasks."""
    cutoff = now_ms() - (days * 24 * 60 * 60 * 1000)
    count = 0
    for status in (CodingTask.STATUS_COMPLETED, CodingTask.STATUS_FAILED, CodingTask.STATUS_STOPPED):
        count += CodingTask.objects.filter(status=status, completed_at__lt=cutoff).delete()[0]
    return count


def serialize_task(task):
    """Serialize a CodingTask for API responses."""
    return {
        'id': task.id,
        'projectId': task.project_id,
        'title': task.title,
        'goal': task.goal,
        'branchName': task.branch_name,
        'status': task.status,
        'provider': task.provider,
        'modelId': task.model_id,
        'iteration': task.iteration,
        'maxIterations': task.max_iterations,
        'lastThought': task.last_thought,
        'prUrl': task.pr_url,
        'prNumber': task.pr_number,
        'createdAt': task.created_at,
        'startedAt': task.started_at,
        'completedAt': task.completed_at,
        'pausedAt': task.paused_at,
        'updatedAt': task.updated_at,
    }


def serialize_message(msg):
    """Serialize a CodingTaskMessage for API responses."""
    actions = []
    if msg.tool_actions:
        try:
            actions = json.loads(msg.tool_actions)
        except (json.JSONDecodeError, TypeError):
            pass
    results = []
    if msg.tool_results:
        try:
            results = json.loads(msg.tool_results)
        except (json.JSONDecodeError, TypeError):
            pass
    return {
        'id': msg.id,
        'taskId': msg.task_id,
        'role': msg.role,
        'content': msg.content,
        'thoughts': msg.thoughts,
        'toolActions': actions,
        'toolResults': results,
        'statusFlag': msg.status_flag,
        'createdAt': msg.created_at,
    }


def serialize_action_log(log):
    """Serialize a CodingActionLog for API responses."""
    return {
        'id': log.id,
        'taskId': log.task_id,
        'iteration': log.iteration,
        'actionType': log.action_type,
        'description': log.description,
        'filePath': log.file_path,
        'contentDiff': log.content_diff,
        'status': log.status,
        'createdAt': log.created_at,
    }


def _notify_worker():
    """Ping the worker via cache signal."""
    try:
        cache.set('coding_agent:worker:ping', now_ms(), timeout=300)
    except Exception:
        pass


def _broadcast(task, event_name, data):
    """Broadcast a task event via WebSocket."""
    try:
        from api.realtime import _send
        group = f'codingagent.{task.id}'
        _send(group, event_name, data)
    except Exception as e:
        logger.debug('coding agent broadcast failed for task %s: %s', task.id, e)
