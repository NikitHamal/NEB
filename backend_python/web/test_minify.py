import os
import tempfile

from django.test import SimpleTestCase

from nebians import minify


class MinifyTests(SimpleTestCase):
    def setUp(self):
        if not minify.enabled():
            self.skipTest('rjsmin/rcssmin not installed')

    def test_css_and_js_shrink_and_keep_meaning(self):
        css = minify.minify_text('web/css/a.css', '/* c */\n.a {\n  color: red;\n  margin: 0 auto;\n}\n')
        self.assertEqual(css, '.a{color:red;margin:0 auto}')
        js = minify.minify_text('web/js/a.js', '// hi\nvar a = 1;\nvar s = "a  //  b";\n')
        self.assertIn('"a  //  b"', js)
        self.assertNotIn('// hi', js)

    def test_vendor_min_and_other_types_are_left_alone(self):
        text = '/* x */\n' * 5 + 'a{b:c}'
        self.assertIsNone(minify.minify_text('web/vendor/katex/katex.css', text))
        self.assertIsNone(minify.minify_text('web/js/htmx.min.js', text))
        self.assertIsNone(minify.minify_text('web/img/a.svg', text))

    def test_minify_file_rewrites_in_place_and_reports_savings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'x.css')
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write('/* long comment */\n.a {\n  color: red;\n}\n')
            saved = minify.minify_file(path, 'web/css/x.css')
            self.assertGreater(saved, 0)
            with open(path, encoding='utf-8') as fh:
                self.assertEqual(fh.read(), '.a{color:red}')
            self.assertEqual(minify.minify_file(path, 'web/css/x.css'), 0)  # idempotent
