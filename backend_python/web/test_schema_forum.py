"""Structured data.

The graph is built in Python so that json.dumps does the escaping, and so that
Google's required fields cannot be quietly missing -- which is exactly how the
site ended up with three Search Console errors on forum threads.
"""
import json
import unittest

from web import schema_forum


POST = {
    'id': 'abc-123',
    'title': 'Why does integration by parts work?',
    'content': 'I can follow the formula but not why it is true.',
    'category': 'Mathematics',
    'authorName': 'nikit',
    'authorId': 'u-1',
    'authorUsername': 'nikit',
    'authorPhotoUrl': 'https://nebians.consica.com.np/media/av.png',
    'isAnonymous': False,
    'createdAt': 1730000000000,
    'editedAt': None,
    'isEdited': False,
    'thumbsUpCount': 4,
    'replyCount': 1,
    'viewCount': 120,
    'images': [],
    'attachments': [],
}

REPLY = {
    'id': 'r-1',
    'content': 'It is the product rule, integrated.',
    'authorName': 'sita',
    'authorId': 'u-2',
    'authorUsername': 'sita',
    'authorPhotoUrl': '',
    'isAnonymous': False,
    'createdAt': 1730000600000,
    'isEdited': False,
    'thumbsUpCount': 2,
}


class ThreadSchemaTests(unittest.TestCase):
    def build(self, **overrides):
        post = dict(POST)
        post.update(overrides)
        return schema_forum.thread_schema(post, [REPLY])

    def test_it_is_a_discussion_forum_posting(self):
        node = self.build()
        self.assertEqual(node['@type'], 'DiscussionForumPosting')
        self.assertEqual(node['@context'], 'https://schema.org')

    def test_the_body_is_present(self):
        # Search Console: "Either text, image or video should be specified" --
        # a critical error, and the one that was stopping the rich result.
        self.assertEqual(self.build()['text'], POST['content'])

    def test_a_title_only_post_still_has_a_body(self):
        node = self.build(content='', title='Just a title')
        self.assertEqual(node['text'], 'Just a title')

    def test_an_empty_post_still_has_a_body(self):
        node = self.build(content='', title='')
        self.assertTrue(node['text'])

    def test_an_image_post_carries_its_image(self):
        node = self.build(images=[{'imageUrl': 'https://x/y.jpg'}])
        self.assertEqual(node['image'], 'https://x/y.jpg')

    def test_an_image_attachment_counts_as_an_image(self):
        node = self.build(attachments=[{'kind': 'image', 'url': 'https://x/a.png'}])
        self.assertEqual(node['image'], 'https://x/a.png')

    def test_a_pdf_attachment_is_not_an_image(self):
        node = self.build(attachments=[{'kind': 'file', 'url': 'https://x/a.pdf'}])
        self.assertNotIn('image', node)

    def test_the_author_has_a_url(self):
        # Search Console: Missing field "url" (in "author").
        self.assertTrue(self.build()['author']['url'].startswith('https://'))

    def test_the_author_url_is_the_username_route(self):
        # Profile pages key on the username. An id here is a URL that 404s.
        self.assertIn('/app/profile/nikit/', self.build()['author']['url'])

    def test_an_author_without_a_username_gets_no_url(self):
        node = self.build(authorUsername='')
        self.assertNotIn('url', node['author'])

    def test_replies_become_comments(self):
        # Search Console: Missing field "comment".
        node = self.build()
        self.assertEqual(len(node['comment']), 1)
        comment = node['comment'][0]
        self.assertEqual(comment['@type'], 'Comment')
        self.assertEqual(comment['text'], REPLY['content'])
        self.assertTrue(comment['url'].startswith('https://'))
        self.assertTrue(comment['author']['url'].startswith('https://'))

    def test_the_comment_count_is_the_real_one(self):
        post = dict(POST)
        node = schema_forum.thread_schema(post, [REPLY] * 25)
        # Google reads a preview; a 200-reply thread should not put a megabyte
        # of JSON in the page.
        self.assertEqual(len(node['comment']), schema_forum.MAX_COMMENTS)
        self.assertEqual(node['commentCount'], 25)

    def test_a_thread_with_no_replies_has_no_comment_key(self):
        node = schema_forum.thread_schema(dict(POST), [])
        self.assertNotIn('comment', node)

    def test_an_anonymous_post_does_not_leak_a_username(self):
        node = self.build(isAnonymous=True, authorName='Anonymous Nebian')
        # The author node is still required, so anonymity is expressed by
        # pointing at the site instead of at a person -- never at a profile.
        self.assertEqual(node['author']['@type'], 'Organization')
        self.assertNotIn('/app/profile/', node['author']['url'])
        self.assertNotIn('@id', node['author'])

    def test_dates_are_iso(self):
        node = self.build()
        self.assertTrue(node['datePublished'].endswith('Z'))
        self.assertIn('T', node['datePublished'])

    def test_a_missing_date_does_not_crash(self):
        node = self.build(createdAt=None)
        self.assertEqual(node['datePublished'], '')

    def test_counters_only_appear_when_non_zero(self):
        node = self.build(viewCount=0)
        kinds = [c['interactionType'] for c in node['interactionStatistic']]
        self.assertNotIn('https://schema.org/ViewAction', kinds)

    def test_a_title_with_a_quote_survives_json(self):
        node = self.build(title='The "best" answer \\ what?')
        self.assertIn('"best"', json.loads(json.dumps(node))['headline'])


class BreadcrumbTests(unittest.TestCase):
    def test_the_last_crumb_has_no_link(self):
        crumb = schema_forum.breadcrumb_schema([
            ('Home', 'https://nebians.consica.com.np/'),
            ('Forum', 'https://nebians.consica.com.np/app/forum/'),
            ('This thread', ''),
        ])
        items = crumb['itemListElement']
        self.assertEqual([i['position'] for i in items], [1, 2, 3])
        self.assertNotIn('item', items[-1])
        self.assertIn('item', items[0])


if __name__ == '__main__':
    unittest.main()
