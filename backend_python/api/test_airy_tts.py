from unittest import mock

from django.test import TestCase

from api import airy_proxy as airy


def _fake_chunks(responses=None):
    """Replace the outbound call + pacing so tests never touch the network."""
    calls = []
    default = responses or []

    def fake(sess, text, voice_id, style, speed, language):
        calls.append({'text': text, 'voice': voice_id, 'style': style, 'speed': speed, 'language': language})
        frame = b'\xff\xf3\x64' + bytes(600)
        index = len(calls) - 1
        if index < len(default):
            return default[index]
        return frame, None, 1.0

    return calls, fake


class AiryChunkerTests(TestCase):
    def test_chunks_never_exceed_server_char_limit(self):
        text = ('The quick brown fox jumps over the lazy dog near the river. ' * 90).strip()
        chunks = airy.split_chunks(text)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), airy.CHAR_LIMIT)

    def test_punctuation_is_preserved_at_boundaries(self):
        text = 'He said "hello there my friend." Then she replied (fine thanks.) over and over.'
        rejoined = ' '.join(airy.split_chunks(text))
        for token in ['friend."', 'thanks.)', 'replied']:
            self.assertIn(token, rejoined)

    def test_oversized_run_without_spaces_is_hard_split(self):
        text = 'A' * (airy.CHAR_LIMIT + 25)
        chunks = airy.split_chunks(text)
        self.assertTrue(all(len(c) <= airy.CHAR_LIMIT for c in chunks))
        self.assertEqual(sum(len(c) for c in chunks), airy.CHAR_LIMIT + 25)

    def test_empty_text_yields_no_chunks(self):
        self.assertEqual(airy.split_chunks('   \n  '), [])

    def test_decimal_and_url_periods_are_not_sentence_breaks(self):
        chunks = airy.split_chunks('Pi is 3.14159 and see https://example.com/a.b.c today.')
        self.assertEqual(len(chunks), 1)
        self.assertIn('3.14159', chunks[0])


class AiryGenerateTests(TestCase):
    def setUp(self):
        patcher_v = mock.patch.object(airy, 'get_voices', return_value=[
            {'id': 'a597bb7a98fc9ec1', 'name': 'Silvia', 'gender': 'female', 'langs': ['en', 'ko'],
             'preview_en': '', 'preview_ko': ''},
            {'id': 'bdb7de5e2cdd3324', 'name': 'Rowan', 'gender': 'male', 'langs': ['en', 'ko'],
             'preview_en': '', 'preview_ko': ''},
        ])
        patcher_p = mock.patch.object(airy, '_pace', lambda: None)
        patcher_v.start()
        patcher_p.start()
        self.addCleanup(patcher_v.stop)
        self.addCleanup(patcher_p.stop)

    def test_short_text_uses_single_batch(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(airy, '_request_chunk', fake):
            result = airy.generate_tts('Hello there.')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(calls), 1)
        self.assertEqual(result['batches'], 1)
        self.assertEqual(result['provider'], 'airy')
        self.assertEqual(result['contentType'], 'audio/mpeg')
        self.assertTrue(result['dataUrl'].startswith('data:audio/mpeg;base64,'))

    def test_long_text_batches_and_concatenates(self):
        sentence = 'This sentence is deliberately long enough to force a batch boundary soon. '
        text = (sentence * 40).strip()
        expected = len(airy.split_chunks(text))
        self.assertGreater(expected, 1)
        calls, fake = _fake_chunks()
        with mock.patch.object(airy, '_request_chunk', fake):
            result = airy.generate_tts(text)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(calls), expected)
        self.assertEqual(result['batches'], expected)
        # Every batch must carry the same voice/style so the stitched MP3 is coherent.
        self.assertEqual(len({c['voice'] for c in calls}), 1)
        # Concatenation is byte-for-byte in order.
        frame = b'\xff\xf3\x64' + bytes(600)
        self.assertEqual(result['bytes'], len(frame) * expected)

    def test_text_beyond_budget_is_rejected_before_network(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(airy, '_request_chunk', fake):
            result = airy.generate_tts('word ' * (airy.MAX_TEXT))
        self.assertEqual(result['status'], 'error')
        self.assertIn('too long', result['error'])
        self.assertEqual(len(calls), 0)

    def test_invalid_style_and_language_fall_back_to_defaults(self):
        calls, fake = _fake_chunks()
        with mock.patch.object(airy, '_request_chunk', fake):
            airy.generate_tts('Hello.', style='screaming', language='de', speed=99)
        self.assertEqual(calls[0]['style'], 'normal')
        self.assertEqual(calls[0]['language'], 'en')
        self.assertEqual(calls[0]['speed'], 2.0)

    def test_voice_resolves_by_name_and_by_id(self):
        self.assertEqual(airy.resolve_voice('Rowan'), 'bdb7de5e2cdd3324')
        self.assertEqual(airy.resolve_voice('rowan'), 'bdb7de5e2cdd3324')
        self.assertEqual(airy.resolve_voice('a597bb7a98fc9ec1'), 'a597bb7a98fc9ec1')
        self.assertEqual(airy.resolve_voice(''), airy.DEFAULT_VOICE)

    def test_upstream_error_is_propagated(self):
        def fake(sess, text, voice_id, style, speed, language):
            return None, 'Airy 429: Studio rate limit of 12 requests per minute exceeded', 0.0
        with mock.patch.object(airy, '_request_chunk', fake):
            result = airy.generate_tts('Hello.')
        self.assertEqual(result['status'], 'error')
        self.assertIn('rate limit', result['error'])


class AiryAdminRoutingTests(TestCase):
    def test_media_view_routes_airy_provider_to_airy_proxy(self):
        from web import views_admin_media

        with mock.patch.object(
            airy, 'generate_tts', return_value={'status': 'success', 'provider': 'airy', 'bytes': 10,
                                                'dataUrl': 'data:audio/mpeg;base64,AA==', 'batches': 2}
        ) as gen:
            response = views_admin_media._run_tts({'provider': 'airy/airy-tts-v1', 'text': 'Hello there friend.', 'voice': 'Rowan'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(gen.call_args.kwargs['voice'], 'Rowan')

    def test_media_view_rejects_overlong_airy_text(self):
        from web import views_admin_media

        with mock.patch.object(airy, 'generate_tts') as gen:
            response = views_admin_media._run_tts({'provider': 'airy', 'text': 'A' * (airy.MAX_TEXT + 10)})
        self.assertEqual(response.status_code, 400)
        gen.assert_not_called()
