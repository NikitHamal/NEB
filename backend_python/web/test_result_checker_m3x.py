"""Result checker: the m3x rules (no gradient, shadow or emoji), and the markup the script drives."""
import os
import re

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "templates", "web", "result_checker.html")
CSS = os.path.join(HERE, "static", "web", "css", "pages", "result-checker-page.css")
JS = os.path.join(HERE, "static", "web", "js", "pages", "result-checker.js")
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2705\u274C]")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class ResultCheckerSourceTests(SimpleTestCase):
    def test_no_gradients_anywhere(self):
        for p in (PAGE, CSS, JS):
            self.assertNotRegex(_read(p), r"(linear|radial|conic)-?[gG]radient|createLinearGradient|createRadialGradient|Grad_cert", p)

    def test_no_shadows(self):
        css = re.sub(r"/\*.*?\*/", "", _read(CSS), flags=re.S)
        self.assertNotRegex(css, r"(box|text)-shadow\s*:\s*(?!\s*none)")
        self.assertNotRegex(css, r"drop-shadow")
        self.assertNotIn("shadowBlur", _read(JS))

    def test_no_emoji(self):
        for p in (PAGE, CSS, JS):
            self.assertEqual(EMOJI.findall(_read(p)), [], p)

    def test_no_hover_to_square(self):
        css = re.sub(r"/\*.*?\*/", "", _read(CSS), flags=re.S)
        before_print = css.split("@media print")[0]
        self.assertNotRegex(before_print, r"border-radius\s*:\s*0\s*[;!]")

    def test_template_has_no_inline_style_or_scrim_colours(self):
        html = _read(PAGE)
        self.assertNotRegex(html, r'\sstyle="')
        self.assertNotIn("rgba(", _read(CSS).split("@media print")[0])

    def test_script_hooks_exist_in_the_markup(self):
        html = _read(PAGE)
        js = _read(JS)
        for hook in re.findall(r"getElementById\('([^']+)'\)", js):
            self.assertIn('id="%s"' % hook, html, hook)


class ResultCheckerPageTests(TestCase):
    def test_page_renders_the_controls(self):
        res = self.client.get(reverse("web:result_check"))
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()
        for needle in ('id="rc-form"', 'data-exam="neb"', 'data-exam="see"', 'data-mode="bulk"',
                       'value="reexam"', 'id="rc-gradesheet-modal"', 'id="rc-share-modal"'):
            self.assertIn(needle, html)
        self.assertNotIn("Powered by", html)
