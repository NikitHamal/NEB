from unittest import mock

from django.test import TestCase

from api import smallest_proxy as smallest


def _fake_chunks(responses=None):
    """Replace the outbound call + pacing so tests never touch the network."""
    calls = []
    default = responses or []

    def fake(sess, text, voice_id, pool, speed, language, sample_rate):
        calls.append({'text': text, 'voice': voice_id, 'pool': pool, 'speed': speed,
                      'language': language, 'sample_rate': sample_rate})
        frame = b'\xff\xfb\x90' + bytes(600)
        index = len(calls) - 1
        if index < len(default):
            return default[index]
        return frame, None, 0.0

    return calls, fake


_PRO_VOICES = [
    {'id': 'kelsey', 'name': 'Kelsey', 'gender': 'female', 'accent': 'american',
     'age': 'young', 'langs': ['en'], 'usecases': [], 'recommended': []},
    {'id': 'blake', 'name': 'Blake', 'gender': 'male', 'accent': 'american',
     'age': 'young', 'langs': ['en'], 'usecases': [], 'recommended': []},
    {'id': 'magnus', 'name': 'Magnus', 'gender': 'male', 'accent': 'american',
     'age': 'young', 'langs': ['en'], 'usecases': [], 'recommended': []},
]


class SmallestChunkerTests(TestCase):
    def test_chunks_never_exceed_server_char_limit(self):
        text = ('The quick brown fox jumps over the lazy dog near the river. ' * 90).strip()
        chunks = smallest.split_chunks(text)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), smallest.CHUNK_LIMIT)

    def test_punctuation_is_preserved_at_boundaries(self):
        text = 'He said "hello there my friend." Then she replied (fine thanks.) over and over.'
        rejoined = ' '.join(smallest.split_chunks(text))
        for token in ['friend."', 'thanks.)', 'replied']:
            self.assertIn(token, rejoined)

    def test_oversized_run_without_spaces_is_hard_split(self):
        text = 'A' * (smallest.CHUNK_LIMIT + 25)
        chunks = smallest.split_chunks(text)
        self.assertTrue(all(len(c) <= smallest.CHUNK_LIMIT for c in chunks))
        self.assertEqual(sum(len(c) for c in chunks), smallest.CHUNK_LIMIT + 25)

    def test_empty_text_yields_no_chunks(self):
        self.assertEqual(smallest.split_chunks('   \n  '), [])

    def test_decimal_and_url_periods_are_not_sentence_breaks(self):
        chunks = smallest.split_chunks('Pi is 3.14159 and see https://example.com/a.b.c today.')
        self.assertEqual(len(chunks), 1)
        self.assertIn('3.14159', chunks[0])

    def test_devanagari_text_chunks_without_losing_characters(self):
        text = ('नेपाल एक सुन्दर देश हो। यहाँ हिमाल, पहाड र तराई सबै छन्। ' * 40).strip()
        chunks = smallest.split_chunks(text)
        self.assertTrue(all(len(c) <= smallest.CHUNK_LIMIT for c in chunks))
        self.assertEqual(' '.join(chunks).replace(' ', ''), text.replace(' ', ''))


class SmallestPoolTests(TestCase):
    def test_known_pool_ids_resolve_to_themselves(self):
        for pool_id in smallest.POOLS:
            self.assertEqual(smallest.resolve_pool(pool_id), pool_id)

    def test_unknown_smallest_ids_fall_back_to_pro(self):
        self.assertEqual(smallest.resolve_pool('smallest'), 'smallest/lightning-v3.1-pro')
        self.assertEqual(smallest.resolve_pool(''), 'smallest/lightning-v3.1-pro')
        self.assertEqual(smallest.resolve_pool('lightning'), 'smallest/lightning-v3.1-pro')

    def test_preview_and_legacy_ids_are_recognised(self):
        self.assertEqual(smallest.resolve_pool('smallest/lightning-v3.1-pro-10-26'),
                         'smallest/lightning-v3.1-pro-10-26')
        self.assertEqual(smallest.resolve_pool('smallest/lightning-v3.1'),
                         'smallest/lightning-v3.1')

    def test_every_pool_carries_its_own_upstream_model_and_catalogue(self):
        seen_models = set()
        for pool_id, pool in smallest.POOLS.items():
            self.assertTrue(pool['model'])
            self.assertTrue(pool['voices_url'].startswith('https://api.smallest.ai'))
            self.assertNotIn(pool['model'], seen_models)
            seen_models.add(pool['model'])


class SmallestGenerateTests(TestCase):
    def setUp(self):
        super().setUp()
        patcher_v = mock.patch.object(smallest, 'get_voices', return_value=_PRO_VOICES)
        patcher_p = mock.patch.object(smallest, '_pace', lambda: None)
        patcher_k = mock.patch.dict('os.environ', {'SMALLEST_API_KEY': 'test-key'})
        patcher_v.start()
        patcher_p.start()
        patcher_k.start()
        self.addCleanup(patcher_v.stop)
        self.addCleanup(patcher_p.stop)
        self.addCleanup(patcher_k.stop)

    def test_short_text_uses_single_batch(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(smallest, '_request_chunk', fake):
            result = smallest.generate_tts('Hello there.')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(calls), 1)
        self.assertEqual(result['batches'], 1)
        self.assertEqual(result['provider'], 'smallest')
        self.assertEqual(result['contentType'], 'audio/mpeg')
        self.assertTrue(result['dataUrl'].startswith('data:audio/mpeg;base64,'))
        self.assertEqual(calls[0]['pool'], 'smallest/lightning-v3.1-pro')

    def test_long_text_batches_and_concatenates(self):
        sentence = 'This sentence is deliberately long enough to force a batch boundary soon. '
        text = (sentence * 20).strip()
        self.assertLessEqual(len(text), smallest.MAX_TEXT)
        expected = len(smallest.split_chunks(text))
        self.assertGreater(expected, 1)
        calls, fake = _fake_chunks()
        with mock.patch.object(smallest, '_request_chunk', fake):
            result = smallest.generate_tts(text)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(calls), expected)
        self.assertEqual(result['batches'], expected)
        self.assertEqual(len({c['voice'] for c in calls}), 1)
        frame = b'\xff\xfb\x90' + bytes(600)
        self.assertEqual(result['bytes'], len(frame) * expected)

    def test_text_beyond_budget_is_rejected_before_network(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(smallest, '_request_chunk', fake):
            result = smallest.generate_tts('word ' * smallest.MAX_TEXT)
        self.assertEqual(result['status'], 'error')
        self.assertIn('too long', result['error'])
        self.assertEqual(len(calls), 0)

    def test_missing_api_key_is_reported_before_network(self):
        calls, fake = _fake_chunks()
        with mock.patch.dict('os.environ', {'SMALLEST_API_KEY': ''}):
            with mock.patch.object(smallest, '_request_chunk', fake):
                result = smallest.generate_tts('Hello.')
        self.assertEqual(result['status'], 'error')
        self.assertIn('SMALLEST_API_KEY', result['error'])
        self.assertEqual(len(calls), 0)

    def test_invalid_language_speed_and_rate_fall_back_to_defaults(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(smallest, '_request_chunk', fake):
            smallest.generate_tts('Hello.', language='ne', speed=99, sample_rate=12345)
        self.assertEqual(calls[0]['language'], 'en')
        self.assertEqual(calls[0]['speed'], 2.0)
        self.assertEqual(calls[0]['sample_rate'], 24000)

    def test_supported_language_codes_pass_through(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(smallest, '_request_chunk', fake):
            result = smallest.generate_tts('नमस्ते दोस्तहरु।', language='hi')
        self.assertEqual(calls[0]['language'], 'hi')
        self.assertEqual(result['language'], 'hi')

    def test_voice_resolves_by_name_by_id_and_defaults_per_pool(self):
        self.assertEqual(smallest.resolve_voice('Kelsey', 'smallest/lightning-v3.1-pro'), 'kelsey')
        self.assertEqual(smallest.resolve_voice('kelsey'), 'kelsey')
        self.assertEqual(smallest.resolve_voice(''), 'kelsey')
        with mock.patch.object(smallest, 'get_voices',
                               return_value=[v for v in _PRO_VOICES if v['id'] == 'magnus']):
            self.assertEqual(smallest.resolve_voice('', 'smallest/lightning-v3.1'), 'magnus')

    def test_pool_choice_changes_the_upstream_model_field(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(smallest, '_request_chunk', fake):
            result = smallest.generate_tts('Hello.', model='smallest/lightning-v3.1')
        self.assertEqual(result['model'], 'smallest/lightning-v3.1')
        self.assertEqual(calls[0]['pool'], 'smallest/lightning-v3.1')

    def test_upstream_error_is_propagated(self):
        def fake(sess, text, voice_id, pool, speed, language, sample_rate):
            return None, 'Smallest AI 429: rate limited', 0.0
        with mock.patch.object(smallest, '_request_chunk', fake):
            result = smallest.generate_tts('Hello.')
        self.assertEqual(result['status'], 'error')
        self.assertIn('rate limited', result['error'])

    def test_mid_stream_failure_reports_the_batch_it_died_on(self):
        sentence = 'This sentence is deliberately long enough to force a batch boundary soon. '
        text = (sentence * 20).strip()
        self.assertGreater(len(smallest.split_chunks(text)), 1)
        state = {'n': 0}

        def fake(sess, chunk, voice_id, pool, speed, language, sample_rate):
            state['n'] += 1
            if state['n'] == 2:
                return None, 'Smallest AI 500: upstream', 0.0
            return b'\xff\xfb\x90' + bytes(600), None, 0.0

        with mock.patch.object(smallest, '_request_chunk', side_effect=fake):
            result = smallest.generate_tts(text)
        self.assertEqual(result['status'], 'error')
        self.assertIn('500', result['error'])
        self.assertEqual(result.get('raw'), 'batch 2/%d' % len(smallest.split_chunks(text)))


class SmallestStitchTests(TestCase):
    def test_id3_tag_and_junk_are_dropped_from_stitched_chunks(self):
        frame = b'\xff\xfb\x90' + bytes(600)
        tag = b'ID3\x04\x00\x00\x00\x00\x00\x00' + bytes(40)
        self.assertEqual(smallest._strip_container(tag + frame), frame)
        self.assertEqual(smallest._strip_container(b'garbage' + frame), frame)
        self.assertEqual(smallest._strip_container(frame), frame)

    def test_stitched_audio_keeps_every_frame(self):
        frame = b'\xff\xfb\x90' + bytes(600)
        pieces = [frame, smallest._strip_container(b'ID3\x04\x00\x00\x00\x00\x00\x00' + frame)]
        self.assertEqual(b''.join(pieces), frame * 2)


class SmallestAdminRoutingTests(TestCase):
    def test_media_view_routes_smallest_provider_to_smallest_proxy(self):
        from web import views_admin_media

        with mock.patch.object(
            smallest, 'generate_tts',
            return_value={'status': 'success', 'provider': 'smallest', 'bytes': 10,
                          'dataUrl': 'data:audio/mpeg;base64,AA==', 'batches': 2}
        ) as gen:
            response = views_admin_media._run_tts({'provider': 'smallest/lightning-v3.1-pro',
                                                   'text': 'Hello there friend.', 'voice': 'Kelsey'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(gen.call_args.kwargs['voice'], 'Kelsey')
        self.assertEqual(gen.call_args.kwargs['model'], 'smallest/lightning-v3.1-pro')

    def test_media_view_rejects_overlong_smallest_text(self):
        from web import views_admin_media

        with mock.patch.object(smallest, 'generate_tts') as gen:
            response = views_admin_media._run_tts({'provider': 'smallest',
                                                   'text': 'A' * (smallest.MAX_TEXT + 10)})
        self.assertEqual(response.status_code, 400)
        gen.assert_not_called()

    def test_voices_endpoint_returns_the_public_catalogue(self):
        import json as _json

        from api.models import User
        from api.security import issue_auth_token
        from django.test import Client

        admin = User.objects.create(id='adm', username='adm', created_at=1, is_admin=True, email='a@x.com')
        client = Client()
        sess = client.session
        sess['auth_token'] = issue_auth_token(admin)
        sess.save()

        with mock.patch.object(smallest, 'get_voices', return_value=_PRO_VOICES):
            response = client.get('/ajax/admin/media/smallest-voices/?pool=smallest/lightning-v3.1-pro')
        self.assertEqual(response.status_code, 200)
        payload = _json.loads(response.content)
        self.assertEqual(len(payload['voices']), 3)
        self.assertEqual(payload['pool'], 'smallest/lightning-v3.1-pro')
        self.assertEqual(len(payload['pools']), 3)
        self.assertTrue(payload['keyRequired'])
        self.assertIn('en', payload['languages'])
        self.assertIn(24000, payload['sampleRates'])

    def test_voices_endpoint_needs_a_staff_session(self):
        import json as _json

        from django.test import Client

        response = Client().get('/ajax/admin/media/smallest-voices/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(_json.loads(response.content)['error'], 'staff only')

    def test_media_test_page_lists_the_smallest_pools(self):
        from api.models import User
        from api.security import issue_auth_token
        from django.test import Client

        admin = User.objects.create(id='adm2', username='adm2', created_at=1, is_admin=True, email='a2@x.com')
        client = Client()
        sess = client.session
        sess['auth_token'] = issue_auth_token(admin)
        sess.save()

        response = client.get('/admin/media-test/')
        self.assertEqual(response.status_code, 200)
        for option in ('smallest/lightning-v3.1-pro', 'smallest/lightning-v3.1-pro-10-26',
                       'smallest/lightning-v3.1', 'smallest-opts', 'smallest-voice', 'smallest-rate'):
            self.assertContains(response, option)
