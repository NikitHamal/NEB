"""Cloudflare quick-tunnel health gate.

The public WebSocket URL is only useful while cloudflared actually holds an
edge connection. When the tunnel is down (e.g. outbound 7844 blocked, stale
URL after restart), advertising the URL makes every client hammer a dead host
and fills browser consoles with connection errors.

is_tunnel_healthy() tails the newest cloudflared log and lets the latest
marker win: a recent ERR/dial-failure with no later successful registration
means unhealthy. Anything ambiguous (no logs, no markers) returns True so a
monitoring blind spot never disables realtime by itself. Verdicts are cached
briefly per process.
"""
from __future__ import annotations

import glob
import os
import re
import time

_TTL_SECONDS = 45
_last = {'ts': 0.0, 'ok': True}

_SUCCESS = re.compile(
    r'Registered tunnel connection|connection registered|'
    r'Updated to .*trycloudflare\.com|INF .* 200 .*trycloudflare',
    re.IGNORECASE,
)
_ERROR = re.compile(
    r'\bERR\b|error=|Unable to establish|Serve tunnel error|'
    r'connection refused|failed to|Retrying connection|'
    r'UnregisterTunnelConnection|Lost connection',
    re.IGNORECASE,
)
_HOST = re.compile(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)')


def _candidate_logs(base_dir=''):
    paths = [
        '/home/consicac/nebians_api/logs/cloudflared.log',
        '/home/consicac/nebians_api/logs/cloudflared_live.log',
        '/home/consicac/nebians_api/logs/start_ws_tunnel.log',
    ]
    if base_dir:
        paths.append(os.path.join(base_dir, 'logs', 'cloudflared.log'))
    paths += sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True)
    return paths


def _probe():
    newest_mtime = -1.0
    newest_lines = []
    for path in _candidate_logs():
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            continue
        if mtime <= newest_mtime:
            continue
        try:
            with open(path, 'r', errors='ignore') as fh:
                content = fh.read()
        except OSError:
            continue
        if not _HOST.search(content):
            continue
        newest_mtime = mtime
        newest_lines = content.splitlines()[-40:]
    if not newest_lines:
        return True
    for line in reversed(newest_lines):
        if _SUCCESS.search(line):
            return True
        if _ERROR.search(line):
            return False
    return True


def is_tunnel_healthy():
    now = time.monotonic()
    if now - _last['ts'] < _TTL_SECONDS:
        return _last['ok']
    try:
        ok = _probe()
    except Exception:
        ok = True
    _last.update(ts=now, ok=ok)
    return ok
