"""Tools pages and scripts: no dash punctuation in copy, no shadows."""
import glob
import os
import re

from django.test import SimpleTestCase

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = ["tools_hub", "tools_tts", "tools_whisper", "doc_tools", "intelligence_tools", "result_checker", "results_guide"]
SCRIPTS = ["js/pages/result-checker.js", "js/pages/tools-tts.js", "js/pages/tools-whisper.js", "js/tools/intelligence-tools.js"]
STYLES = ["tools.css", "tools-tts-page.css", "tools-whisper-page.css", "result-checker-page.css"]


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class ToolsCopyTests(SimpleTestCase):
    def test_no_em_or_en_dash(self):
        paths = [os.path.join(HERE, "templates", "web", t + ".html") for t in TEMPLATES]
        paths += [os.path.join(HERE, "static", "web", s) for s in SCRIPTS]
        for p in paths:
            text = _read(p)
            self.assertNotIn("\u2014", text, p)
            self.assertNotIn("\u2013", text, p)

    def test_no_double_hyphen_in_visible_copy(self):
        for t in TEMPLATES:
            text = _read(os.path.join(HERE, "templates", "web", t + ".html"))
            text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
            text = re.sub(r"<(style|script)\b.*?</\1>", "", text, flags=re.S)
            text = re.sub(r"\{#.*?#\}|\{%.*?%\}|\{\{.*?\}\}", "", text, flags=re.S)
            text = re.sub(r"<[^>]+>", "", text)
            self.assertNotRegex(text, r"\s--\s", t)

    def test_no_box_shadow(self):
        for name in STYLES:
            found = glob.glob(os.path.join(HERE, "static", "web", "css", "**", name), recursive=True)
            self.assertTrue(found, name)
            for p in found:
                css = re.sub(r"/\*.*?\*/", "", _read(p), flags=re.S)
                self.assertNotRegex(css, r"box-shadow\s*:\s*(?![\s]*none)", p)
