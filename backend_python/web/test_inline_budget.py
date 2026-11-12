"""Big inline <script> bodies are re-sent, uncached, with every page view.

Anything large belongs in static/web/js/pages/ (versioned, immutable, compressed
once). Pages still over the line are listed here so they can only shrink.
"""
import re
from pathlib import Path

from django.test import SimpleTestCase

TEMPLATES = Path(__file__).resolve().parent / 'templates'
LIMIT = 30_000
KNOWN_LARGE = {
    'web/forum_post.html': 70_000,
    'web/profile.html': 40_000,
    'web/edit_profile.html': 30_000,
}


class InlineScriptBudgetTests(SimpleTestCase):
    def test_no_template_grows_a_new_large_inline_script(self):
        offenders = []
        for path in TEMPLATES.rglob('*.html'):
            rel = path.relative_to(TEMPLATES).as_posix()
            text = path.read_text(encoding='utf-8', errors='ignore')
            for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', text, re.S):
                if 'src=' in m.group(1) or 'ld+json' in m.group(1):
                    continue
                size = len(m.group(2))
                if size > KNOWN_LARGE.get(rel, LIMIT):
                    offenders.append('%s: %d bytes' % (rel, size))
        self.assertEqual(offenders, [], 'move the script to static/web/js/pages/')
