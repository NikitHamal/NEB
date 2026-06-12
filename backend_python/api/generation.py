"""
Async generation job queue.

Views enqueue jobs and return 202 immediately. A background worker
polls for pending jobs and processes them. Results are stored in the
GenerationJob row and broadcast via WebSocket.

Architecture:
  - GenerationJob model stores status, params, result, error
  - enqueue() creates a job row, returns it
  - poll_next() fetches the oldest queued job (FIFO)
  - mark_* helpers update status and broadcast WS events
  - Frontend polls GET /ajax/study-space/<id>/generation/<job_id>/
    or receives WS events on the studyspace.<id> channel
"""
import json
import logging

from django.core.cache import cache

from api.models import GenerationJob
from api.utils import now_ms

logger = logging.getLogger(__name__)

JOB_TTL_MS = 24 * 60 * 60 * 1000  # 24 hours


def enqueue(job_type, user_id, space_id=None, document_id=None, params=None):
    """Create a queued GenerationJob and return it.

    params: dict stored as JSON (mode, count, etc.)
    """
    job = GenerationJob.objects.create(
        id=_job_id(),
        job_type=job_type,
        status=GenerationJob.STATUS_QUEUED,
        user_id=user_id,
        space_id=space_id,
        document_id=document_id,
        params=json.dumps(params or {}),
        created_at=now_ms(),
    )
    _notify_new_job(job)
    logger.info('enqueue: job %s type=%s user=%s space=%s', job.id, job_type, user_id, space_id)
    return job


def get_job(job_id):
    """Return a GenerationJob by id or None."""
    try:
        return GenerationJob.objects.get(pk=job_id)
    except GenerationJob.DoesNotExist:
        return None


def get_pending_jobs(limit=5):
    """Return the oldest queued jobs, ordered by created_at."""
    return list(
        GenerationJob.objects.filter(status=GenerationJob.STATUS_QUEUED)
        .order_by('created_at')[:limit]
    )


def mark_processing(job):
    """Mark a job as processing and broadcast started event."""
    now = now_ms()
    GenerationJob.objects.filter(pk=job.id).update(
        status=GenerationJob.STATUS_PROCESSING,
        started_at=now,
        progress=10,
    )
    job.status = GenerationJob.STATUS_PROCESSING
    job.started_at = now
    job.progress = 10
    _broadcast(job, 'generation.started', {'progress': 10})


def mark_progress(job, progress, message=''):
    """Update progress percentage and broadcast."""
    GenerationJob.objects.filter(pk=job.id).update(progress=progress)
    job.progress = progress
    _broadcast(job, 'generation.progress', {'progress': progress, 'message': message})


def mark_completed(job, result):
    """Mark a job as completed and broadcast the result."""
    now = now_ms()
    result_str = json.dumps(result, ensure_ascii=False) if isinstance(result, dict) else str(result)
    GenerationJob.objects.filter(pk=job.id).update(
        status=GenerationJob.STATUS_COMPLETED,
        result=result_str,
        progress=100,
        completed_at=now,
    )
    job.status = GenerationJob.STATUS_COMPLETED
    job.result = result_str
    job.progress = 100
    job.completed_at = now
    _broadcast(job, 'generation.completed', result)


def mark_failed(job, error):
    """Mark a job as failed and broadcast."""
    now = now_ms()
    GenerationJob.objects.filter(pk=job.id).update(
        status=GenerationJob.STATUS_FAILED,
        error=str(error)[:2000],
        completed_at=now,
    )
    job.status = GenerationJob.STATUS_FAILED
    job.error = str(error)[:2000]
    job.completed_at = now
    _broadcast(job, 'generation.failed', {'error': str(error)[:500]})


def cancel_stale_jobs():
    """Cancel queued jobs older than JOB_TTL_MS. Called by the worker periodically."""
    cutoff = now_ms() - JOB_TTL_MS
    stale = GenerationJob.objects.filter(
        status=GenerationJob.STATUS_QUEUED,
        created_at__lt=cutoff,
    )
    count = stale.update(status=GenerationJob.STATUS_CANCELLED, completed_at=now_ms())
    if count:
        logger.info('cancel_stale_jobs: cancelled %d stale jobs', count)


def cleanup_old_jobs(days=7):
    """Delete completed/failed/cancelled jobs older than N days."""
    cutoff = now_ms() - (days * 24 * 60 * 60 * 1000)
    count = 0
    for status in (GenerationJob.STATUS_COMPLETED, GenerationJob.STATUS_FAILED, GenerationJob.STATUS_CANCELLED):
        count += GenerationJob.objects.filter(status=status, completed_at__lt=cutoff).delete()[0]
    return count


def serialize_job(job):
    """Serialize a GenerationJob for API responses."""
    result = None
    if job.result:
        try:
            result = json.loads(job.result)
        except (json.JSONDecodeError, TypeError):
            result = job.result
    params = {}
    if job.params:
        try:
            params = json.loads(job.params)
        except (json.JSONDecodeError, TypeError):
            params = {}
    return {
        'id': job.id,
        'jobType': job.job_type,
        'status': job.status,
        'progress': job.progress,
        'params': params,
        'result': result,
        'error': job.error,
        'spaceId': job.space_id or '',
        'documentId': job.document_id or '',
        'createdAt': job.created_at,
        'startedAt': job.started_at,
        'completedAt': job.completed_at,
    }


def _job_id():
    from api.utils import uuid_str
    return uuid_str()


def _notify_new_job(job):
    """Ping the worker via cache signal so it wakes up immediately."""
    try:
        cache.set('generation:worker:ping', now_ms(), timeout=300)
    except Exception:
        pass


def _broadcast(job, event_name, data):
    """Broadcast a generation event on the study space WS channel."""
    try:
        from api.realtime import broadcast_generation_event
        broadcast_generation_event(job, event_name, data)
    except Exception as e:
        logger.warning('generation broadcast failed for job %s: %s', job.id, e)