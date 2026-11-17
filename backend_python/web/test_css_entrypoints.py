"""A linked stylesheet must not `@import` children.

Static URLs are versioned by the hash of the file the template links. A file
made only of `@import` lines never changes hash, so browsers keep serving stale
children (the unstyled admin analytics cards). Entry points are flattened by
tools/css/bundle.py; the two below still mix imports with their own rules and
are tracked here until they are split.
"""
import os
import re

from django.conf import settings
from django.test import SimpleTestCase

WEB = os.path.join(settings.BASE_DIR, 'web')
KNOWN = {'pages/profile.css', 'pages/web-home.css'}


class CssEntrypointTests(SimpleTestCase):
    def test_linked_stylesheets_are_flat(self):
        linked = set()
        for root, _dirs, files in os.walk(os.path.join(WEB, 'templates')):
            for name in files:
                if name.endswith('.html'):
                    with open(os.path.join(root, name), encoding='utf-8') as fh:
                        linked.update(re.findall(r"static '(web/css/[^']+\.css)'", fh.read()))
        self.assertTrue(linked)
        for rel in sorted(linked):
            short = rel[len('web/css/'):]
            path = os.path.join(WEB, 'static', *rel.split('/'))
            if short in KNOWN or not os.path.exists(path):
                continue
            with open(path, encoding='utf-8') as fh:
                self.assertNotRegex(fh.read(), r'(?m)^@import\s', '%s still @imports children' % rel)
