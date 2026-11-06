import base64
import hashlib
import hmac
import json
import os
import time
from unittest import mock

from django.test import SimpleTestCase, TestCase

from api import realtime, realtime_ably

KEY = 'app123.keyABC:s3cr3t-value'


def _b64d(part):
    return base64.urlsafe_b64decode(part + '=' * (-len(part) % 4))


class AblyTokenTests(SimpleTestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {'ABLY_API_KEY': KEY}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_token_is_signed_hs256_with_key_name_and_subscribe_only_capability(self):
        token = realtime_ably.build_token('42', now=1_000)
        head, claims, sig = token.split('.')
        header = json.loads(_b64d(head))
        self.assertEqual(header['alg'], 'HS256')
        self.assertEqual(header['kid'], 'app123.keyABC')
        expected = hmac.new(b's3cr3t-value', f'{head}.{claims}'.encode(), hashlib.sha256).digest()
        self.assertEqual(_b64d(sig), expected)
        body = json.loads(_b64d(claims))
        self.assertEqual(body['exp'] - body['iat'], realtime_ably.TOKEN_TTL)
        cap = json.loads(body['x-ably-capability'])
        self.assertEqual(cap['user.42'], ['subscribe'])
        self.assertEqual(cap['forum.public'], ['subscribe'])
        for ops in cap.values():
            self.assertEqual(ops, ['subscribe'])

    def test_anonymous_token_has_no_user_channel(self):
        cap = json.loads(_b64d(realtime_ably.build_token(None).split('.')[1]))['x-ably-capability']
        self.assertFalse([c for c in json.loads(cap) if c.startswith('user.')])

    def test_disabled_without_key(self):
        with mock.patch.dict(os.environ, {'ABLY_API_KEY': ''}):
            self.assertFalse(realtime_ably.is_enabled())
            self.assertIsNone(realtime_ably.client_config('1'))
            self.assertFalse(realtime_ably.publish('forum.public', 'x', {}))

    def test_only_browser_channels_are_published(self):
        self.assertTrue(realtime_ably.handles('forum.public'))
        self.assertTrue(realtime_ably.handles('post.9'))
        self.assertTrue(realtime_ably.handles('user.9'))
        self.assertFalse(realtime_ably.handles('canvas.9'))
        self.assertFalse(realtime_ably.handles('studyspace.9'))


class AblyPublishTests(SimpleTestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {'ABLY_API_KEY': KEY}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_specs_group_messages_per_channel(self):
        specs = realtime_ably._Publisher.specs([
            ('forum.public', 'post.created', '{}'),
            ('post.1', 'reply.created', '{}'),
            ('forum.public', 'post.like_changed', '{}'),
        ])
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0]['channels'], ['forum.public'])
        self.assertEqual([m['name'] for m in specs[0]['messages']], ['post.created', 'post.like_changed'])

    def test_oversize_and_open_breaker_drop_events(self):
        pub = realtime_ably._Publisher()
        with mock.patch.object(pub, '_ensure_thread'):
            pub.enqueue('forum.public', 'big', {'x': 'y' * (realtime_ably.MAX_MESSAGE_BYTES + 10)})
            self.assertEqual(len(pub._queue), 0)
            pub.enqueue('forum.public', 'ok', {'a': 1})
            self.assertEqual(len(pub._queue), 1)
            pub._keys[KEY] = [0, time.time() + 60]
            pub.enqueue('forum.public', 'ok2', {'a': 2})
            self.assertEqual(len(pub._queue), 1)

    def test_queue_is_bounded(self):
        pub = realtime_ably._Publisher()
        with mock.patch.object(pub, '_ensure_thread'):
            for i in range(realtime_ably.MAX_QUEUE + 25):
                pub.enqueue('forum.public', 'e', {'i': i})
        self.assertEqual(len(pub._queue), realtime_ably.MAX_QUEUE)

    def test_breaker_opens_after_repeated_failures(self):
        pub = realtime_ably._Publisher()
        with mock.patch.object(realtime_ably, 'post_batch', side_effect=OSError('down')):
            for _ in range(realtime_ably.BREAKER_FAILS):
                pub._flush([('forum.public', 'e', '{}')])
        self.assertGreater(pub._keys[KEY][1], time.time())

    def test_send_publishes_to_ably_and_skips_channel_layer(self):
        with mock.patch.object(realtime_ably, 'publish', return_value=True) as pub, \
                mock.patch.object(realtime, 'get_channel_layer') as layer:
            realtime._send('forum.public', 'post.created', {'post_id': '1'})
        pub.assert_called_once()
        self.assertEqual(pub.call_args[0][:2], ('forum.public', 'post.created'))
        layer.assert_not_called()


class RealtimeConfigEndpointTests(TestCase):
    def test_config_returns_ably_stream_and_is_never_cached(self):
        with mock.patch.dict(os.environ, {'ABLY_API_KEY': KEY, 'ABLY_API_KEYS': '', 'WS_PUBLIC_URL': ''}):
            res = self.client.get('/api/realtime/config/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['transport'], 'ably-sse')
        self.assertIn('/event-stream', data['sse_url'])
        self.assertEqual(data['user_channel'], '')
        self.assertEqual(data['ws_url'], '')
        self.assertIn('no-store', res['Cache-Control'])

    def test_config_without_key_reports_no_transport(self):
        with mock.patch.dict(os.environ, {'ABLY_API_KEY': '', 'ABLY_API_KEYS': '', 'WS_PUBLIC_URL': ''}):
            data = self.client.get('/api/realtime/config/').json()
        self.assertEqual(data['transport'], 'none')
        self.assertNotIn('token', data)


KEY2 = 'app2.key2:secretsecretsecret2'


class AblyShardTests(SimpleTestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {'ABLY_API_KEY': KEY, 'ABLY_API_KEYS': KEY2 + ',' + KEY}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_keys_are_merged_and_deduplicated(self):
        self.assertEqual(realtime_ably.api_keys(), [KEY2, KEY])

    def test_user_lands_on_the_same_app_every_time(self):
        picks = {realtime_ably.client_config('42')['shard'] for _ in range(5)}
        self.assertEqual(len(picks), 1)
        self.assertEqual(realtime_ably.client_config('42')['shards'], 2)

    def test_users_spread_over_both_apps(self):
        picks = {realtime_ably.client_config(str(i))['shard'] for i in range(40)}
        self.assertEqual(picks, {0, 1})

    def test_explicit_shard_wins_for_failover_and_token_uses_that_key(self):
        cfg = realtime_ably.client_config('42', shard=1)
        self.assertEqual(cfg['shard'], 1)
        header = cfg['token'].split('.')[0]
        raw = base64.urlsafe_b64decode(header + '=' * (-len(header) % 4))
        self.assertEqual(json.loads(raw)['kid'], 'app123.keyABC')
        self.assertEqual(realtime_ably.client_config('42', shard=99)['shard'], realtime_ably.client_config('42')['shard'])

    def test_publish_goes_to_every_app_and_a_down_app_does_not_block_the_other(self):
        pub = realtime_ably._Publisher()
        sent = []

        def fake(specs, key=None):
            if key == KEY2:
                raise OSError('down')
            sent.append(key)

        with mock.patch.object(realtime_ably, 'post_batch', side_effect=fake):
            pub._flush([('forum.public', 'e', '{}')])
        self.assertEqual(sent, [KEY])
        self.assertEqual(pub._keys[KEY2][0], 1)
