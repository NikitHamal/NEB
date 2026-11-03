"""The icon font is a subset. An icon used in a template but missing from it would render as
its name in plain text, so fail here instead; scripts/build_icon_font.py rebuilds the subset."""
import re
from pathlib import Path

from django.test import SimpleTestCase

WEB = Path(__file__).resolve().parent
ICON = re.compile(r'class="[^"]*material-symbols-outlined[^"]*"[^>]*>\s*([a-z][a-z0-9_]+)\s*</')


def font_names():
    return set((WEB / 'static/web/fonts/app/material-symbols-outlined.txt').read_text(encoding='utf-8').split())


class IconFontSubsetTests(SimpleTestCase):
    def test_every_literal_icon_is_in_the_font(self):
        included = font_names()
        missing = {}
        for path in list((WEB / 'templates').rglob('*.html')) + list((WEB / 'static/web/js').rglob('*.js')):
            for name in ICON.findall(path.read_text(encoding='utf-8', errors='ignore')):
                if name not in included:
                    missing.setdefault(name, path.name)
        self.assertFalse(missing, f'icons missing from the subset (run scripts/build_icon_font.py): {missing}')

    def test_icons_named_in_python_are_in_the_font(self):
        # The scan above reads markup. A chip list or a type map names the glyph in Python and
        # hands it to the same span, so nothing else would ever catch a missing one.
        from web.templatetags.web_extras import resource_type_icon
        from web.views_public import POPULAR_SEARCHES

        used = {icon for _label, icon in POPULAR_SEARCHES}
        used |= {resource_type_icon(kind) for kind in
                 ('pdf', 'note', 'notes', 'video', 'audio', 'image', 'link', 'textbook',
                  'paper', 'past paper', 'model paper', 'presentation', 'slides', 'document', '')}
        missing = sorted(used - font_names())
        self.assertFalse(missing, f'icons missing from the subset (run scripts/build_icon_font.py): {missing}')
