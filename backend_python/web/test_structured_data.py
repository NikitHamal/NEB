"""Every page that emits JSON-LD must emit JSON a crawler can parse.

Search Console reported "Parsing error: Missing '}' or object member name" on a
forum thread (first detected 2026-11-05). The graph was valid: web.schema_forum
builds it in Python and json.dumps escapes it. The bug was rendering. The
templates insert the string with {{ ... }}, Django autoescaped it, and browsers
do not decode HTML entities inside a <script> element, so Google read

    {&quot;@context&quot;: &quot;https://schema.org&quot;, ...

and dropped the rich result. The same escaped output was on every forum thread,
news article and syllabus page; Search Console only reported the URL it
crawled.

ld_json() now returns a SafeString, so these tests render the real pages and
parse every block the way a crawler does.
"""
import json
import re
import uuid

from django.core.cache import cache
from django.test import TestCase

from api.models import Announcement, Post, Reply, User

BLOCK = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


def _blocks(response):
    html = response.content.decode('utf-8')
    return BLOCK.findall(html)


class StructuredDataPagesTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = User.objects.create(
            id=str(uuid.uuid4()), username='schema-author', email='schema@example.com',
            email_verified=True, display_name='Schema Author', role='student',
        )
        self.post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.user,
            title='Why does integration by parts work?',
            content='I can follow the formula, but not the idea behind it.',
            category='Mathematics', created_at=1_700_000_000_000,
        )
        Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.user,
            content='It is the product rule, integrated.', created_at=1_700_000_060_000,
        )
        self.article = Announcement.objects.create(
            id=str(uuid.uuid4()), title='SEE exam form notice',
            slug='see-form-notice', summary='Forms open this week.',
            content='Fill the form at your school.', category='notice',
            status='published', published_at=1_700_000_000_000,
            source_key='neb', source_name='National Examinations Board',
            source_official=True, source_guid='notice-1',
        )
        self.pages = {
            'forum thread': '/app/forum/post/%s/' % self.post.id,
            'news article': '/app/news/%s/' % self.article.slug,
            'syllabus subject': '/app/syllabus/11/physics/',
            'syllabus chapter': '/app/syllabus/11/physics/unit-3/',
        }

    def _assert_blocks_parse(self, label, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, label)
        blocks = _blocks(response)
        self.assertTrue(blocks, '%s has no JSON-LD at all' % label)
        for index, block in enumerate(blocks):
            try:
                json.loads(block)
            except ValueError as exc:
                self.fail('%s block %d is not valid JSON: %s\n%s' % (label, index, exc, block[:200]))

    def test_every_page_emits_parseable_json_ld(self):
        for label, url in self.pages.items():
            with self.subTest(page=label):
                self._assert_blocks_parse(label, url)

    def test_no_block_contains_html_entities(self):
        # &quot; is the exact signature of the autoescaping bug: browsers do not
        # decode it inside a script element, so the block is dead weight.
        for label, url in self.pages.items():
            for block in _blocks(self.client.get(url)):
                self.assertNotIn('&quot;', block, label)

    def test_the_forum_thread_keeps_google_required_fields(self):
        # The rich result is only offered when the posting has text and an
        # author with a url; this is the same page Search Console flagged.
        blocks = _blocks(self.client.get(self.pages['forum thread']))
        posting = next(b for b in blocks if 'DiscussionForumPosting' in b)
        node = json.loads(posting)
        self.assertTrue(node['text'])
        self.assertTrue(node['author']['url'])
        self.assertEqual(node['commentCount'], 1)

    def test_a_title_with_a_quote_or_tag_cannot_break_the_block(self):
        # json.dumps escapes the quotes and ld_json escapes the angle brackets,
        # so the nastiest title a user can type still parses.
        self.post.title = 'A "quoted" title with <b>tags</b> & amp</script>'
        self.post.save(update_fields=['title'])
        self._assert_blocks_parse('forum thread', self.pages['forum thread'])
