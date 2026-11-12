from django.test import SimpleTestCase

from web.templatetags.web_extras import mention_links


class ForumCodeRenderingTests(SimpleTestCase):
    def test_fenced_block_becomes_pre(self):
        html = str(mention_links("```python\nx = 1\n```"))
        self.assertIn('<pre><code class="language-python">', html)

    def test_mentions_still_link_outside_code(self):
        html = str(mention_links("thanks @bob"))
        self.assertIn('/app/profile/bob/', html)

    def test_decorators_inside_code_are_not_mentions(self):
        html = str(mention_links("```python\n@cache\ndef f(): pass\n```\nuse `@x` here"))
        self.assertNotIn('/app/profile/cache/', html)
        self.assertNotIn('/app/profile/x/', html)
        self.assertIn('@cache', html)
