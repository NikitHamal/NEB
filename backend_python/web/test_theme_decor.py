import re
from pathlib import Path

from django.core.cache import cache
from django.test import TestCase

from api.models import SiteTheme
from web import site_themes

CSS = Path(__file__).resolve().parent / 'static/web/css/themes.css'


class ThemeDecorTests(TestCase):
    def setUp(self):
        cache.clear()
        SiteTheme.objects.create(key='tihar', is_forced=True)

    def test_landing_renders_tihar_lights_and_greeting(self):
        html = self.client.get('/').content.decode()
        self.assertIn('st-decor-tihar', html)
        self.assertIn('Happy Tihar', html)

    def test_diyo_motif_is_a_real_lamp_not_a_tiny_sprite(self):
        from django.template.loader import render_to_string
        html = render_to_string('themes/_motif.html', {'site_theme': site_themes.current()})
        self.assertIn('class="st-diya"', html)
        self.assertNotIn('st-motif-px', html)

    def test_theme_css_has_no_shadows_and_hangs_garland_under_the_nav(self):
        css = CSS.read_text(encoding='utf-8')
        self.assertFalse(re.search(r'box-shadow\s*:\s*[^n;]', css))
        self.assertIn('.hero>.st-decor .st-garland', css)
