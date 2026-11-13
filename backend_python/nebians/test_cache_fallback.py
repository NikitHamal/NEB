"""An unreadable cached value must cost a cache miss, not a 500.

2026-11-13: three og_card_png keys in Redis held an empty payload (STRLEN 0).
Django's cache client unpickles what it reads, so an empty payload raised
EOFError, which is not a transport error and so went straight through
ResilientRedisCache and 500ed /og/chapter/8/mathematics/19.png for a crawler,
which also mailed the owner.

The values were corrupted outside this code (a Redis reload of a truncated
string after a restart would do it), so the backend cannot prevent them. What it
can do is refuse to fail on them: drop the poison key and report a miss, which
every caller already knows how to handle.
"""
from unittest import mock

import redis.exceptions
from django.test import SimpleTestCase

from nebians.cache_fallback import ResilientRedisCache

EOF = EOFError('Ran out of input')


class FakeClient:
    """Stands in for Django's RedisCacheClient.

    That client is where deserialisation happens, so a corrupt payload raises
    from get()/get_many() and never reaches our code as bytes. Values here are
    either the decoded object, None for a missing key, or an exception to raise.
    """

    def __init__(self, mapping):
        self.mapping = dict(mapping)

    @staticmethod
    def _bare(redis_key):
        # Django prefixes the version (':1:key'), and these keys contain colons
        # of their own, so strip exactly that prefix and nothing else.
        return redis_key.split(':', 2)[-1]

    def get(self, redis_key, default=None):
        value = self.mapping.get(self._bare(redis_key))
        if isinstance(value, Exception):
            raise value
        return default if value is None else value

    def get_many(self, redis_keys):
        return {key: self.get(key) for key in redis_keys}

    def delete(self, redis_key):
        return self.mapping.pop(self._bare(redis_key), None) is not None


class CacheBase(SimpleTestCase):
    def setUp(self):
        # No connection is ever made: the fake client answers directly.
        self.cache = ResilientRedisCache('redis://127.0.0.1:1/0', {})

    def with_client(self, mapping):
        client = FakeClient(mapping)
        return client, mock.patch.object(self.cache, '_cache', client)


class CorruptValueTests(CacheBase):
    def test_an_empty_value_is_a_miss(self):
        _, patched = self.with_client({'og_card_png:v4:chapter:x': EOF})
        with patched:
            self.assertEqual(self.cache.get('og_card_png:v4:chapter:x', 'default'), 'default')

    def test_every_shape_of_unreadable_payload_is_a_miss(self):
        for exc in (EOF, ValueError('invalid literal for int() with base 10: b""'),
                    __import__('pickle').UnpicklingError('bad pickle')):
            with self.subTest(exc=exc):
                _, patched = self.with_client({'k': exc})
                with patched:
                    self.assertIsNone(self.cache.get('k'))

    def test_the_poisoned_key_is_removed_so_the_next_request_regenerates(self):
        client, patched = self.with_client({'og_card_png:v4:chapter:x': EOF})
        with patched:
            self.cache.get('og_card_png:v4:chapter:x')
        self.assertNotIn('og_card_png:v4:chapter:x', client.mapping)

    def test_a_healthy_value_still_comes_back(self):
        _, patched = self.with_client({'k': {'a': 1}})
        with patched:
            self.assertEqual(self.cache.get('k'), {'a': 1})

    def test_a_missing_key_still_returns_the_default(self):
        _, patched = self.with_client({})
        with patched:
            self.assertEqual(self.cache.get('k', 'fallback'), 'fallback')

    def test_get_many_survives_one_bad_value_and_keeps_the_rest(self):
        # A batch read cannot say which key failed, so the fallback re-reads one
        # at a time; get() drops the poison and the healthy values survive.
        _, patched = self.with_client({'good': {'a': 1}, 'bad': EOF})
        with patched:
            found = self.cache.get_many(['good', 'bad', 'missing'])
        self.assertEqual(found, {'good': {'a': 1}})


class OtherFailuresTests(CacheBase):
    def test_a_transport_error_still_degrades_quietly(self):
        _, patched = self.with_client({'k': redis.exceptions.ConnectionError('down')})
        with patched:
            self.assertEqual(self.cache.get('k', 'fallback'), 'fallback')

    def test_a_real_bug_is_not_swallowed(self):
        # Only transport failures and unreadable payloads are forgiven.
        _, patched = self.with_client({'k': KeyError('boom')})
        with patched:
            with self.assertRaises(KeyError):
                self.cache.get('k')
