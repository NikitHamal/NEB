"""Tests for the updated model catalog (Qwen 4, GPT-6, Claude 5.5, Gemini 4, DeepSeek V4.1)
and the universal keyless provider failover mesh."""
from unittest.mock import patch

from django.test import SimpleTestCase

from api import (
    chatjimmy_proxy,
    deepai_proxy,
    geminiweb_proxy,
    inception_proxy,
    k2think_proxy,
    keyless_fallback,
    longcat_proxy,
    motiftech_proxy,
    poolside_proxy,
    ptero_proxy,
    qwencloud_proxy,
    tryingopen_proxy,
    unikey_proxy,
    yqcloud_proxy,
)
from api.llm import client as llm_client
from api.llm import registry


class KeylessCatalogTests(SimpleTestCase):
    def test_qwen4_models_registered_in_qwen_and_qwencloud(self):
        qc = registry.preset('qwencloud')
        qw = registry.preset('qwen')
        self.assertEqual(qc.default_model, 'qwen4-max')
        self.assertEqual(qw.default_model, 'qwen4-max')
        qc_ids = [m.id for m in qc.models]
        qw_ids = [m.id for m in qw.models]
        for mid in ('qwen4-max', 'qwen4-max-preview', 'qwen4-plus', 'qwen4-flash', 'qwen4-27b', 'qwen3.8-max', 'qwen3.8-flash'):
            self.assertIn(mid, qc_ids)
            self.assertIn(mid, qw_ids)
            self.assertIn(mid, qwencloud_proxy.MODEL_MAP)

    def test_new_frontier_models_registered(self):
        self.assertIn('gpt-6-luna', [m.id for m in registry.preset('openai').models])
        self.assertIn('gpt-6-astra', [m.id for m in registry.preset('openai').models])
        self.assertIn('claude-sonnet-5-5', [m.id for m in registry.preset('anthropic').models])
        self.assertIn('claude-opus-5-5', [m.id for m in registry.preset('anthropic').models])
        self.assertIn('gemini-4-argon', [m.id for m in registry.preset('gemini').models])
        self.assertIn('gemini-3.8-flash', [m.id for m in registry.preset('gemini').models])
        self.assertIn('deepseek-v4.1-flash', [m.id for m in registry.preset('deepseek').models])
        self.assertIn('qwen/qwen4-max', tryingopen_proxy.MODEL_MAP)
        self.assertIn('deepseek-v4-flash:runware', ptero_proxy.MODEL_MAP)
        for mid in ('motif-102b', 'motif-12-7b', 'motif-12-7b-reasoning', 'motif-tiny'):
            self.assertIn(mid, motiftech_proxy.MODEL_MAP)
        for mid in ('standard', 'gpt-6-luna', 'claude-haiku-5-5', 'qwen3.8-flash', 'deepseek-v4.1-flash', 'glm-5.3-flash'):
            resolved, _ = deepai_proxy.resolve_model(mid)
            self.assertEqual(resolved, mid)

    def test_admin_catalog_excludes_tts_only_scrapers(self):
        cat = registry.admin_catalog()
        scraper_slugs = {e['slug'] for e in cat['scrapers']}
        self.assertIn('qwencloud', scraper_slugs)
        self.assertIn('tryingopen', scraper_slugs)
        self.assertIn('ptero', scraper_slugs)
        self.assertNotIn('kokoro', scraper_slugs)
        self.assertNotIn('lazypy', scraper_slugs)

    def test_ptero_legacy_models_map_cleanly(self):
        for old_id in ('mercury-2.5:free', 'qwen3.7-flash:free', 'deepseek-v4.1-flash:free'):
            mapped = ptero_proxy.LEGACY_MODELS[old_id]
            self.assertIn(mapped, ptero_proxy.MODEL_MAP)


class KeylessFallbackRoutingTests(SimpleTestCase):
    def test_model_family_matcher_picks_matching_models(self):
        self.assertEqual(keyless_fallback._pick_deepai_model('qwencloud', 'qwen4-max'), 'qwen3.8-flash')
        self.assertEqual(keyless_fallback._pick_deepai_model('tryingopen', 'deepseek/deepseek-v4.1-flash'), 'deepseek-v4.1-flash')
        self.assertEqual(keyless_fallback._pick_deepai_model('zen', 'glm-5.3-flash-free'), 'glm-5.3-flash')
        self.assertEqual(keyless_fallback._pick_deepai_model('openai', 'gpt-6-astra'), 'gpt-6-luna')
        self.assertEqual(keyless_fallback._pick_deepai_model('anthropic', 'claude-opus-5-5'), 'claude-haiku-5-5')
        self.assertEqual(keyless_fallback._pick_llm7_model('zen', 'deepseek-v4.1-flash-free'), 'DeepSeek-V4-Flash-0731')
        self.assertEqual(keyless_fallback._pick_unikey_model('anthropic', 'claude-opus-4-8'), 'claude-opus-4-8')

    def test_proxies_fall_back_seamlessly_when_primary_upstream_fails(self):
        msgs = [{'role': 'user', 'content': 'Say OK'}]
        with patch.object(keyless_fallback, '_try_deepai', return_value='Fallback OK'):
            # QwenCloud without UMIDTOKEN falls back seamlessly
            with patch.dict('os.environ', {'QWENCLOUD_UMIDTOKEN': ''}, clear=False):
                qwencloud_proxy._umidtoken_cache = None
                out = qwencloud_proxy.simple_chat('Say OK', model='qwen4-max')
                self.assertEqual(out, 'Fallback OK')

            # TryingOpen 403 falls back seamlessly
            with patch.object(tryingopen_proxy, '_stream_request', return_value=iter([{'type': 'error', 'error': 'HTTP 403'}])):
                out = tryingopen_proxy.simple_chat('Say OK', model='qwen/qwen4-max')
                self.assertEqual(out, 'Fallback OK')

            # Ptero failure falls back seamlessly
            with patch.object(ptero_proxy, '_post', return_value=(None, 403, 'HTTP 403')):
                out = ptero_proxy.simple_chat('Say OK', model='deepseek-v4-flash:runware')
                self.assertEqual(out, 'Fallback OK')

            # Keyless official preset (zen) 429 falls back seamlessly
            with patch.object(llm_client, '_openai_chat', side_effect=llm_client.LLMError('zen: HTTP 429', status=429, provider='zen')):
                res = llm_client.chat(
                    format='openai', base_url='https://opencode.ai/zen/v1',
                    api_key='public', model='deepseek-v4.1-flash-free',
                    messages=msgs, provider='zen',
                )
                self.assertEqual(res.text, 'Fallback OK')
