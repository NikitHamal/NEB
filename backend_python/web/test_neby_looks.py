"""Pixel Neby's looks: what is live, what the apps are told, and that every strip exists."""
import os

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase

from api.models import NebyConfig, SiteTheme
from web import neby_looks, site_themes


class NebyLookTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_auto_follows_the_festival(self):
        self.assertEqual(neby_looks.resolve('everyday')['look'], 'classic')
        SiteTheme.objects.create(key='dashain', is_forced=True)
        site_themes.invalidate()
        neby = site_themes.current()['neby']
        self.assertEqual(neby['look'], 'dashain')
        self.assertEqual(neby['greet'], 'tika')

    def test_an_admin_pick_wins(self):
        NebyConfig.objects.create(look='astronaut', ambient=False)
        live = neby_looks.resolve('dashain')
        self.assertEqual((live['look'], live['mode'], live['ambient'], live['greet']), ('astronaut', 'astronaut', False, None))

    def test_unknown_look_falls_back(self):
        NebyConfig.objects.create(look='not-a-look')
        self.assertEqual(neby_looks.resolve('tihar')['look'], 'tihar')

    def test_api_tells_the_app(self):
        NebyConfig.objects.create(look='topi', reactions=False)
        data = self.client.get('/api/site-theme/').json()
        self.assertEqual(data['neby'], {'look': 'topi', 'ambient': True, 'reactions': False})

    def test_every_look_has_every_state_on_disk(self):
        root = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'img', 'neby')
        missing = [f'{look}/{state}' for look, _, _ in neby_looks.LOOKS for state in neby_looks.STATES
                   if not os.path.exists(os.path.join(root, look, f'{state}.png'))]
        self.assertEqual(missing, [])
