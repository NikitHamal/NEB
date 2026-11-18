"""Admin chat providers: the catalog lists only models an upstream really serves,
dead providers are retired, nothing is rerouted to another provider, and a
transient cooldown is retried quickly."""
import importlib
from unittest.mock import patch

from django.test import SimpleTestCase

from api.llm import registry


class CatalogTests(SimpleTestCase):
    def test_no_invented_qwen4_ids_anywhere_in_the_catalog(self):
        cat = registry.admin_catalog()
        ids = [m['id'] for e in cat['scrapers'] + cat['official'] for m in e['models']]
        self.assertFalse([i for i in ids if 'qwen4' in i])

    def test_qwen_lists_what_chat_qwen_serves_to_guests(self):
        p = registry.preset('qwen')
        self.assertEqual([m.id for m in p.models], ['qwen3.8-max', 'qwen3.7-plus'])
        self.assertEqual(p.default_model, 'qwen3.8-max')

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
