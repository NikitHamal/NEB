"""The icon font is a subset. An icon used in a template but missing from it would render as
its name in plain text, so fail here instead; scripts/build_icon_font.py rebuilds the subset."""
import re
from pathlib import Path

from django.test import SimpleTestCase

WEB = Path(__file__).resolve().parent
ICON = re.compile(r'class="[^"]*material-symbols-outlined[^"]*"[^>]*>\s*([a-z][a-z0-9_]+)\s*</')


class IconFontSubsetTests(SimpleTestCase):
    def test_every_literal_icon_is_in_the_font(self):
        included = set((WEB / 'static/web/fonts/app/material-symbols-outlined.txt').read_text().split())
        missing = {}
        for path in list((WEB / 'templates').rglob('*.html')) + list((WEB / 'static/web/js').rglob('*.js')):
            for name in ICON.findall(path.read_text(encoding='utf-8', errors='ignore')):
                if name not in included:
                    missing.setdefault(name, path.name)
        self.assertFalse(missing, f'icons missing from the subset (run scripts/build_icon_font.py): {missing}')
