"""The LSAPI parent warm-up must be safe: it never raises."""
from django.test import SimpleTestCase

from nebians import warmup


class WarmupTests(SimpleTestCase):
    def test_warm_does_not_raise(self):
        warmup.warm()

    def test_template_names_skip_admin_and_themes(self):
        names = warmup._template_names()
        self.assertIn('base.html', names)
        self.assertEqual(names[0], 'base.html')
        self.assertFalse([n for n in names if n.startswith(('admin_panel/', 'themes/'))])
