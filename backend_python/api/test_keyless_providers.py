"""Admin chat providers: the catalog lists only models an upstream really serves,
dead providers are retired, nothing is rerouted to another provider, and a
transient cooldown is retried quickly."""
import importlib
from unittest.mock import patch

from django.test import SimpleTestCase

from api.llm import registry


class CatalogTests(SimpleTestCase):
    def test_qwen4_is_only_the_id_the_gateway_serves(self):
        cat = registry.admin_catalog()
        ids = [m['id'] for e in cat['scrapers'] + cat['official'] for m in e['models']]
        self.assertEqual([i for i in ids if 'qwen4' in i], ['qwen4-max'])

    def test_qwen_lists_what_the_app_gateway_serves(self):
        p = registry.preset('qwen')
        self.assertEqual([m.id for m in p.models], ['qwen4-max', 'qwen3.8-max', 'qwen3.7-max', 'qwen3.7-plus',
                                                    'qwen3.8-omni-flash', 'qwen3.5-omni-plus'])
        self.assertEqual(p.default_model, 'qwen4-max')

    def test_dead_providers_are_hidden_from_the_admin_catalog(self):
        slugs = {e['slug'] for e in registry.admin_catalog()['scrapers']}
        self.assertNotIn('qwencloud', slugs)
        self.assertNotIn('tryingopen', slugs)
        self.assertNotIn('poolside', slugs)
        self.assertNotIn('zen', {e['slug'] for e in registry.admin_catalog()['official']})
        self.assertIn('deepai', slugs)

    def test_llm7_lists_only_the_anonymous_aliases(self):
        self.assertEqual({m.id for m in registry.preset('llm7').models}, {'default', 'fast'})


class NoFallbackTests(SimpleTestCase):
    def test_substitution_mesh_is_gone(self):
        with self.assertRaises(ImportError):
            importlib.import_module('api.keyless_fallback')

    def test_qwen_keeps_the_model_that_was_asked_for(self):
        from api import qwen_proxy
        self.assertEqual(qwen_proxy._normalize_qwen_web_model('qwen3.7-plus'), 'qwen3.7-plus')
        self.assertEqual(qwen_proxy._normalize_qwen_web_model('qwen3.8-flash'), 'qwen3.8-flash')


class CooldownTests(SimpleTestCase):
    def _run(self, attempts):
        from web import admin_chat_engine as eng
        calls = iter(attempts)
        with patch.object(eng, '_attempt', side_effect=lambda *a: iter(next(calls))), \
                patch.object(eng.time, 'sleep') as slept:
            return list(eng.run_turn('llm7', 'default', 'hi', [])), slept

    def test_rate_limit_is_retried_then_answers(self):
        out, slept = self._run([[{'type': 'error', 'message': 'HTTP 429 retry after 1 seconds'}],
                                [{'type': 'text', 'content': 'ok'}]])
        self.assertEqual([e['type'] for e in out], ['retry', 'text'])
        self.assertLessEqual(slept.call_args[0][0], 2.5)

    def test_hard_error_is_reported_without_retry(self):
        out, slept = self._run([[{'type': 'error', 'message': 'HTTP 401 invalid key'}]])
        self.assertEqual(out, [{'type': 'error', 'message': 'HTTP 401 invalid key'}])
        slept.assert_not_called()

    def test_gives_up_after_three_attempts(self):
        out, _ = self._run([[{'type': 'error', 'message': 'HTTP 429'}]] * 3)
        self.assertEqual(out[-1]['type'], 'error')
        self.assertEqual(len([e for e in out if e['type'] == 'retry']), 2)


class QwenAppGatewayTests(SimpleTestCase):
    def test_rate_limit_beats_the_word_token_in_the_body(self):
        from api import qwen_app
        self.assertEqual(qwen_app._classify(429, '{"detail":"too many tokens"}'), 'rate')
        self.assertEqual(qwen_app._classify(401, 'bad token'), 'auth')
        self.assertEqual(qwen_app._classify(200, '<script>..._____tmd_____/punish'), 'waf')

    def test_history_is_folded_into_one_prompt_with_the_last_turn_last(self):
        from api import qwen_app
        text = qwen_app._prompt([{'role': 'user', 'content': 'a'}, {'role': 'assistant', 'content': 'b'},
                                 {'role': 'user', 'content': 'c'}], '')
        self.assertTrue(text.endswith('[User]\nc'))
        self.assertIn('Assistant: b', text)

    def test_cooling_account_is_skipped_and_expired_token_is_not_usable(self):
        import base64, json, time
        from api import qwen_app_pool as pool
        def tok(exp):
            b = base64.urlsafe_b64encode(json.dumps({'exp': exp}).encode()).decode().rstrip('=')
            return 'h.%s.s' % b
        ok = {'email': 'a', 'token': tok(time.time() + 9 * 86400), 'cool_until': 0}
        self.assertTrue(pool.usable(ok))
        self.assertFalse(pool.usable(dict(ok, cool_until=time.time() + 60)))
        self.assertFalse(pool.usable(dict(ok, token=tok(time.time() + 60))))
        self.assertFalse(pool.usable(ok, exclude=('a',)))

    def test_rate_limited_account_rotates_to_the_next_one(self):
        from api import qwen_app
        accts = iter([{'email': 'a', 'token': 't', 'device': 'd'}, {'email': 'b', 'token': 't', 'device': 'd'}])
        def one(acct, *a):
            if acct['email'] == 'a':
                raise RuntimeError('rate|quota')
            yield {'type': 'text', 'content': 'hi'}
        with patch.object(qwen_app.pool, 'acquire', side_effect=lambda ex=(): next(accts)), \
                patch.object(qwen_app.pool, 'cool') as cool, patch.object(qwen_app, '_one', side_effect=one):
            out = list(qwen_app.stream_chat([{'role': 'user', 'content': 'x'}], 'qwen4-max'))
        self.assertEqual(out, [{'type': 'text', 'content': 'hi'}])
        cool.assert_called_once()
