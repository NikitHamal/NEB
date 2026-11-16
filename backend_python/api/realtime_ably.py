"""Hosted realtime transport (Ably) -- no tunnel, no long-lived socket on our box.

Why this exists
---------------
The app runs on shared cPanel (LiteSpeed + LSAPI) next to other sites. It cannot
hold thousands of open sockets, and LiteSpeed cannot proxy WebSockets. So the
server never keeps a connection open: it *publishes* events to Ably over one
short HTTPS request, and browsers *subscribe* straight to Ably (Server-Sent
Events, no SDK, ~0 KB of JS). Ably's free plan is 6M messages a month with 200
concurrent connections, and the cost to this server is one small POST per
batch of events.

Rules this module keeps
-----------------------
* Publishing never blocks a request: events go on a bounded in-memory queue and
  one daemon thread per process sends them in batches (one POST per flush).
* If Ably is slow or down, a circuit breaker drops events for 30s instead of
  piling up threads or memory. Realtime is best-effort; the database is truth.
* No ABLY_API_KEY -> everything here is a no-op and clients fall back quietly.
* Browsers only ever get a signed, short-lived, subscribe-only JWT scoped to the
  channels they may read. The API key never leaves the server.
"""
import base64
import collections
import hashlib
import hmac
import json
import logging
import os
import threading
import time
import urllib.parse
import urllib.request
import uuid

logger = logging.getLogger(__name__)

REST_HOST = os.environ.get('ABLY_REST_HOST', 'main.realtime.ably.net').strip() or 'main.realtime.ably.net'
# Ably refuses a key-authenticated publish that names no client (error 40161,
# "requires an identified client"), so every REST POST carries this id.
PUBLISH_CLIENT_ID = os.environ.get('ABLY_PUBLISH_CLIENT_ID', 'nebians-server').strip() or 'nebians-server'
TOKEN_TTL = 3600  # seconds; the client renews at ~80% of this
MAX_QUEUE = 400
MAX_BATCH = 80
MAX_MESSAGE_BYTES = 60_000  # Ably's per-message limit is 64 KiB on the free plan
FLUSH_WINDOW = 0.08  # coalesce bursts (a like + a reply) into one POST
PUBLISH_TIMEOUT = 4.0
BREAKER_FAILS = 3
BREAKER_SECONDS = 30.0

# Channel families a browser may read. Everything here is already public on the
# site (forum threads, resources); `user.<id>` is added for the signed-in user.
PUBLIC_CAPABILITY = {
    'forum.public': ['subscribe'],
    'post.*': ['subscribe'],
    'resource.*': ['subscribe'],
    'resource_request.*': ['subscribe'],
}


def api_keys():
    """Every configured Ably app key, in a stable order.

    `ABLY_API_KEYS` (comma or space separated) lists several free Ably apps; the
    legacy `ABLY_API_KEY` is folded in. Each app has its own free quota (200
    concurrent connections, 6M messages a month), so N apps = N times the room.
    Every event is published to all of them and each client reads from one.
    """
    raw = '%s,%s' % (os.environ.get('ABLY_API_KEYS', ''), os.environ.get('ABLY_API_KEY', ''))
    seen = []
    for part in raw.replace(' ', ',').replace(';', ',').split(','):
        part = part.strip()
        if part and ':' in part and part not in seen:
            seen.append(part)
    return seen


def _api_key():
    keys = api_keys()
    return keys[0] if keys else ''


def is_enabled():
    return bool(api_keys()) and os.environ.get('REALTIME_DISABLED', '') != '1'


def pick_shard(count, user_id=None, hint='', explicit=None):
    """Which app a client reads from: the one it asked for (failover), else a
    stable hash of the user (or ip+agent) so reconnects land on the same app."""
    if count <= 1:
        return 0
    if explicit is not None and 0 <= explicit < count:
        return explicit
    seed = ('u:%s' % user_id) if user_id else ('h:%s' % hint)
    return int(hashlib.sha1(seed.encode()).hexdigest()[:8], 16) % count


def handles(group):
    """True for the channels browsers read through Ably."""
    return (
        group == 'forum.public'
        or group.startswith(('post.', 'resource.', 'resource_request.', 'user.'))
    )


# ----------------------------------------------------------------- tokens

def _b64(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')


def build_token(user_id=None, now=None, key=None):
    """Self-signed Ably JWT (HS256, no network call). Subscribe-only."""
    key = key or _api_key()
    if ':' not in key:
        return None
    key_name, secret = key.split(':', 1)
    now = int(now if now is not None else time.time())
    capability = dict(PUBLIC_CAPABILITY)
    if user_id:
        capability['user.%s' % user_id] = ['subscribe']
    header = {'typ': 'JWT', 'alg': 'HS256', 'kid': key_name}
    claims = {
        'iat': now,
        'exp': now + TOKEN_TTL,
        'x-ably-capability': json.dumps(capability, separators=(',', ':')),
        # Ably refuses an unidentified client with error 40161, on subscribe as
        # well as publish, so an anonymous reader still gets its own id.
        'x-ably-clientId': str(user_id) if user_id else ('anon-%s' % uuid.uuid4().hex[:12]),
    }
    signing = '%s.%s' % (
        _b64(json.dumps(header, separators=(',', ':')).encode()),
        _b64(json.dumps(claims, separators=(',', ':')).encode()),
    )
    sig = hmac.new(secret.encode(), signing.encode(), hashlib.sha256).digest()
    return '%s.%s' % (signing, _b64(sig))


def client_config(user_id=None, shard=None, hint=''):
    """What a browser or the app needs to open the stream, or None if disabled.

    `shard` is the app index a client asks for after its current one failed
    (quota, outage); without it the client is spread by a stable hash.
    """
    if not is_enabled():
        return None
    keys = api_keys()
    index = pick_shard(len(keys), user_id, hint, shard)
    token = build_token(user_id, key=keys[index])
    if not token:
        return None
    return {
        'transport': 'ably-sse',
        'sse_url': 'https://%s/event-stream' % REST_HOST,
        'token': token,
        'expires_in': TOKEN_TTL,
        'user_channel': ('user.%s' % user_id) if user_id else '',
        'shard': index,
        'shards': len(keys),
    }


# -------------------------------------------------------------- publishing

class _Publisher:
    def __init__(self):
        self._queue = collections.deque()
        self._cond = threading.Condition()
        self._thread = None
        self._pid = None
        self._keys = {}

    def enqueue(self, channel, name, data):
        if not self._any_open():
            return
        try:
            body = json.dumps(data, separators=(',', ':'), default=str)
        except (TypeError, ValueError):
            return
        if len(body) > MAX_MESSAGE_BYTES:
            logger.info('realtime: dropped oversize %s (%d bytes)', name, len(body))
            return
        with self._cond:
            if len(self._queue) >= MAX_QUEUE:
                self._queue.popleft()
            self._queue.append((channel, name, body))
            self._ensure_thread()
            self._cond.notify()

    def _any_open(self):
        now = time.time()
        return any(now >= self._keys.get(k, [0, 0.0])[1] for k in api_keys())

    def _ensure_thread(self):
        # LSAPI forks workers: a thread started before the fork does not exist
        # in the child, so remember which pid started it.
        if self._thread and self._thread.is_alive() and self._pid == os.getpid():
            return
        self._pid = os.getpid()
        self._thread = threading.Thread(target=self._run, name='ably-publisher', daemon=True)
        self._thread.start()

    def _run(self):
        while True:
            with self._cond:
                while not self._queue:
                    self._cond.wait(timeout=60)
            time.sleep(FLUSH_WINDOW)
            with self._cond:
                batch = []
                while self._queue and len(batch) < MAX_BATCH:
                    batch.append(self._queue.popleft())
            if batch:
                self._flush(batch)

    @staticmethod
    def specs(batch):
        grouped = collections.OrderedDict()
        for channel, name, body in batch:
            grouped.setdefault(channel, []).append({'name': name, 'data': body})
        return [{'channels': [ch], 'messages': msgs} for ch, msgs in grouped.items()]

    def _flush(self, batch):
        """Send one batch to every configured app; a down app never blocks the rest."""
        specs = self.specs(batch)
        now = time.time()
        for key in api_keys():
            state = self._keys.setdefault(key, [0, 0.0])  # [fails, open_until]
            if now < state[1]:
                continue
            try:
                post_batch(specs, key)
                state[0] = 0
            except Exception as exc:  # noqa: BLE001 - never let the thread die
                state[0] += 1
                logger.warning('realtime: ably publish failed (%s): %s', state[0], exc)
                if state[0] >= BREAKER_FAILS:
                    state[1] = time.time() + BREAKER_SECONDS
                    state[0] = 0


def post_batch(specs, key=None):
    key = key or _api_key()
    url = 'https://%s/messages?clientId=%s' % (REST_HOST, urllib.parse.quote(PUBLISH_CLIENT_ID, safe=''))
    req = urllib.request.Request(
        url,
        data=json.dumps(specs, separators=(',', ':')).encode(),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(key.encode()).decode(),
        },
    )
    with urllib.request.urlopen(req, timeout=PUBLISH_TIMEOUT) as resp:  # noqa: S310
        resp.read(256)


_publisher = _Publisher()


def publish(group, event, data):
    """Queue one event for Ably. Cheap, non-blocking, never raises."""
    if not is_enabled() or not handles(group):
        return False
    try:
        _publisher.enqueue(group, event, data)
        return True
    except Exception:  # noqa: BLE001
        return False
