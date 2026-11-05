from django.test import SimpleTestCase

from api import inception_proxy, k2think_proxy, poolside_proxy
from api.model_catalog import model_catalog


class ModelCatalogTests(SimpleTestCase):
    MODELS = [
        {'id': 'a', 'name': 'A', 'vision': True, 'reasoning': True, 'web_search': True},
        {'id': 'b', 'name': 'B'},
    ]

    def test_flags_come_from_the_model_rows(self):
        a, b = model_catalog(self.MODELS)
        self.assertEqual(a['capabilities'], {
            'chat': True, 'stream': True, 'vision': True, 'thinking': True,
            'tools': False, 'web_search': True,
        })
        self.assertEqual((b['id'], b['name']), ('b', 'B'))
        self.assertFalse(b['capabilities']['vision'] or b['capabilities']['thinking'])

    def test_vision_can_be_forced_and_reasoning_levels_added(self):
        a, b = model_catalog(self.MODELS, vision=False, reasoning_levels=True)
        self.assertFalse(a['capabilities']['vision'])
        self.assertEqual(b['capabilities']['reasoning_levels'], [])

    def test_every_chat_proxy_serves_its_models_through_it(self):
        for proxy in (k2think_proxy, poolside_proxy, inception_proxy):
            ids = [m['id'] for m in proxy.get_models()]
            self.assertEqual(ids, [m['id'] for m in proxy.MODELS], proxy.__name__)
