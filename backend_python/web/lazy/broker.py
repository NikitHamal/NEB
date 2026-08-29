"""Run-scoped event bus connecting the agent thread to SSE subscribers.

The agent loop runs on a worker thread while one or more HTTP streams want to
watch it. This module owns that hand-off: publishers push plain dict frames,
subscribers get a queue that is pre-seeded with anything already published, and
a terminal frame freezes the run so late subscribers (a page reload, a second
tab) immediately catch up and close instead of hanging.

It also owns the cancellation flag, which is the only way a browser "Cancel"
actually stops work: the loop polls it between iterations and before dispatching
tool calls.
"""

import queue
import threading
import time

# How many frames of history a new subscriber is replayed. Generous enough that
# a reload mid-run reconstructs the whole activity panel.
BACKLOG_LIMIT = 600

# A run that finished is kept briefly so a reconnecting client can drain it.
FINISHED_TTL = 120.0

# A run that never produced a terminal frame is reaped to stop unbounded growth
# if a worker thread dies without cleaning up.
STALE_TTL = 3600.0

_lock = threading.RLock()
_runs = {}


class _RunChannel:
    """All state for one run: subscribers, backlog, terminal frame, cancel flag."""

    __slots__ = ('run_id', 'subscribers', 'backlog', 'terminal', 'cancelled',
                 'finished_at', 'last_event_at', 'seq')

    def __init__(self, run_id):
        self.run_id = run_id
        self.subscribers = []
        self.backlog = []
        self.terminal = None
        self.cancelled = False
        self.finished_at = 0.0
        self.last_event_at = time.time()
        self.seq = 0


def _channel(run_id, create=True):
    key = str(run_id)
    with _lock:
        chan = _runs.get(key)
        if chan is None and create:
            chan = _RunChannel(key)
            _runs[key] = chan
        return chan


# --------------------------------------------------------------------------
# Publishing
# --------------------------------------------------------------------------

def publish(run_id, frame):
    """Broadcast one frame to every live subscriber and append it to the backlog."""
    if not isinstance(frame, dict):
        return
    chan = _channel(run_id)
    if chan is None:
        return
    with _lock:
        chan.seq += 1
        chan.last_event_at = time.time()
        chan.backlog.append(frame)
        if len(chan.backlog) > BACKLOG_LIMIT:
            del chan.backlog[:len(chan.backlog) - BACKLOG_LIMIT]
        targets = list(chan.subscribers)
    for q in targets:
        _offer(q, frame)


def finish(run_id, frame):
    """Publish the terminal frame and mark the channel done.

    Idempotent: the loop, the view and the crash handler may all try to finish a
    run, and only the first one should win.
    """
    chan = _channel(run_id)
    if chan is None:
        return
    with _lock:
        if chan.terminal is not None:
            return
        chan.terminal = frame if isinstance(frame, dict) else {'type': 'done', 'ok': False}
        chan.finished_at = time.time()
        chan.last_event_at = chan.finished_at
        chan.backlog.append(chan.terminal)
        targets = list(chan.subscribers)
    for q in targets:
        _offer(q, chan.terminal)
        # Wake any subscriber parked on an empty queue so it sees the sentinel.
        _offer(q, {'type': '_end'})


def open_run(run_id):
    """Create (or reset) the channel for a run about to start."""
    with _lock:
        _runs[str(run_id)] = _RunChannel(str(run_id))


def close_run(run_id):
    """Drop a channel immediately."""
    with _lock:
        _runs.pop(str(run_id), None)


# --------------------------------------------------------------------------
# Subscribing
# --------------------------------------------------------------------------

def subscribe(run_id):
    """Return a queue pre-seeded with the backlog.

    If the run already finished, the terminal frame is at the end of the queue,
    so the consumer drains it and exits without ever blocking.
    """
    # create=False matters: an unknown run must not silently conjure a channel,
    # or the caller would block forever waiting on a run that will never publish.
    chan = _channel(run_id, create=False)
    if chan is None:
        # Unknown run (process restarted). Hand back a queue holding only a
        # terminal frame so the stream closes cleanly instead of hanging.
        q = queue.Queue()
        q.put({'type': 'done', 'ok': False, 'summary': '', 'artifacts': [],
               'error': 'Run expired. Refresh the page to see saved results.', 'stale': True})
        q.put({'type': '_end'})
        return q

    q = queue.Queue()
    with _lock:
        for frame in chan.backlog:
            q.put(frame)
        if chan.terminal is not None:
            q.put({'type': '_end'})
            return q
        chan.subscribers.append(q)
    return q


def unsubscribe(run_id, q):
    chan = _runs.get(str(run_id)) if _runs else None
    if not chan:
        return
    with _lock:
        try:
            chan.subscribers.remove(q)
        except ValueError:
            pass


def has_channel(run_id):
    """True when a live channel exists for this run (worker may still be going)."""
    return _runs.get(str(run_id)) is not None


def is_finished(run_id):
    chan = _runs.get(str(run_id))
    return bool(chan and chan.terminal is not None)


# --------------------------------------------------------------------------
# Cancellation
# --------------------------------------------------------------------------

def request_cancel(run_id):
    chan = _channel(run_id)
    if chan is None:
        return False
    with _lock:
        chan.cancelled = True
    return True


def is_cancelled(run_id):
    chan = _runs.get(str(run_id))
    return bool(chan and chan.cancelled)


# --------------------------------------------------------------------------
# Maintenance
# --------------------------------------------------------------------------

def active_count():
    with _lock:
        return len(_runs)


def reap():
    """Drop channels nobody is watching any more.

    A finished run lingers briefly so a reconnecting browser can drain its
    events; after that it is pure memory. Runs that never terminate are reaped
    on a much longer fuse in case the worker thread died mid-flight.
    """
    now = time.time()
    with _lock:
        dead = []
        for run_id, chan in _runs.items():
            if chan.subscribers:
                continue
            if chan.terminal is not None:
                if now - chan.finished_at > FINISHED_TTL:
                    dead.append(run_id)
            elif now - chan.last_event_at > STALE_TTL:
                dead.append(run_id)
        for run_id in dead:
            _runs.pop(run_id, None)
    return len(dead)


def _offer(q, frame, timeout=5):
    """Never let one stalled subscriber block or crash the agent thread."""
    try:
        q.put(frame, timeout=timeout)
    except (queue.Full, Exception):
        pass
