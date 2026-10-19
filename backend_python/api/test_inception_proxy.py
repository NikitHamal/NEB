"""Offline tests for the Inception (Mercury 3) proxy surface — no network."""
from django.test import SimpleTestCase

from api import inception_proxy as inc


class InceptionModelTests(SimpleTestCase):
    def test_mercury_3_is_the_only_listed_model(self):
        self.assertEqual([m["id"] for m in inc.MODELS], ["mercury-3"])
        self.assertEqual(inc.MODELS[0]["name"], "Mercury 3")

    def test_mercury_3_defaults_everywhere(self):
        import inspect
        for fn in (inc.stream_chat, inc.simple_chat):
            sig = inspect.signature(fn)
            self.assertEqual(sig.parameters["model"].default, "mercury-3")

    def test_legacy_mercury_2_resolves_to_mercury_3(self):
        self.assertEqual(inc.LEGACY_MODELS["mercury-2"], "mercury-3")

    def test_unknown_model_rejected_without_network(self):
        chunks = list(inc.stream_chat(messages=[{"role": "user", "content": "hi"}], model="mercury-9"))
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["type"], "error")
        self.assertIn("Unknown model", chunks[0]["error"])

    def test_legacy_model_passes_the_map_check(self):
        # mercury-2 is accepted (aliased) — it fails later on the network, not on the id.
        self.assertIn("mercury-2", inc.LEGACY_MODELS)
        self.assertNotIn("mercury-2", inc.MODEL_MAP)

    def test_get_models_advertises_mercury_3_with_reasoning_levels(self):
        models = inc.get_models()
        self.assertEqual(len(models), 1)
        caps = models[0]["capabilities"]
        self.assertEqual(models[0]["id"], "mercury-3")
        self.assertTrue(caps["thinking"])
        self.assertTrue(caps["web_search"])
        self.assertIn("instant", caps["reasoning_levels"])
        self.assertIn("high", caps["reasoning_levels"])
