"""The sitemap.

The rules that matter are protocol rules: 50,000 URLs per file, and a lastmod
that means something. Both were being violated.
"""
import unittest


def _configure():
    """seo.py imports the models, which import settings. Point Django at a
    throwaway configuration rather than a database."""
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY='test-only-key-for-seo-tests-0123456789abcdef0123',
            ALLOWED_HOSTS=['*'],
            INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth', 'api'],
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
            USE_TZ=True,
            ADMIN_API_SALT='test-only-salt',
        )
        import django
        django.setup()


_configure()


from web import seo  # noqa: E402


class SitemapShapeTests(unittest.TestCase):
    def test_there_are_four_groups(self):
        self.assertEqual(sorted(seo.sitemap_groups()),
                         ['forum', 'library', 'pages', 'profiles'])

    def test_static_pages_make_no_freshness_claim(self):
        # These are rendered from templates. Stamping them with "now" on every
        # request teaches a crawler that lastmod is noise. A syllabus chapter and
        # a news post are database rows, so their modification time means something.
        for entry in seo._static_and_syllabus_entries():
            loc = entry['loc']
            if loc.endswith('/') and 'syllabus' not in loc and '/app/news/' not in loc:
                self.assertNotIn('lastmod', entry,
                                 '%s claims a modification time' % loc)

    def test_no_entry_fabricates_a_lastmod(self):
        for entry in seo._static_and_syllabus_entries():
            if 'lastmod' in entry:
                self.assertTrue(str(entry['lastmod']).strip())

    def test_every_url_is_absolute(self):
        for entry in seo._static_and_syllabus_entries():
            self.assertTrue(entry['loc'].startswith('https://nebians.consica.com.np'))

    def test_the_syllabus_is_in_the_pages_file(self):
        locs = [e['loc'] for e in seo._static_and_syllabus_entries()]
        self.assertIn(seo.SITE_BASE_URL + '/app/syllabus/', locs)

    def test_a_group_under_the_limit_serialises(self):
        xml = seo.build_sitemap_xml([
            {'loc': 'https://x/a', 'changefreq': 'daily', 'priority': '1.0'},
        ])
        self.assertIn('<urlset', xml)
        self.assertIn('<loc>https://x/a</loc>', xml)

    def test_the_serialiser_escapes_xml(self):
        xml = seo.build_sitemap_xml([
            {'loc': 'https://x/a?b=1&c=2', 'changefreq': 'daily', 'priority': '1.0'},
        ])
        self.assertIn('&amp;', xml)

    def test_the_serialiser_escapes_quotes(self):
        xml = seo.build_sitemap_xml([
            {'loc': 'https://x/a?q="b"&c=2', 'changefreq': 'daily', 'priority': '1.0'},
        ])
        self.assertIn('&quot;b&quot;', xml)
        self.assertIn('&amp;', xml)

    def test_library_and_forum_have_separate_caps_under_the_protocol_limit(self):
        self.assertLessEqual(seo._MAX_RESOURCES, 50000)
        self.assertLessEqual(seo._MAX_POSTS, 50000)
        self.assertLessEqual(seo._MAX_PROFILES, 50000)


class IndexabilityTests(unittest.TestCase):
    def test_a_placeholder_resource_is_not_indexable(self):
        class R:
            approval_status = 'approved'
            uploaded_by_id = None
            title = 'test'
            description = ''
            subject = ''
            grade_level = ''
            tags = ''
            author_name = ''
            source_label = ''
            file = None
            file_url = ''
        self.assertFalse(seo.is_indexable_resource(R()))

    def test_an_unapproved_resource_is_not_indexable(self):
        class R:
            approval_status = 'pending'
            uploaded_by_id = None
            title = 'Class 12 Physics Notes Complete'
            description = 'Complete notes'
            subject = 'Physics'
            grade_level = 'Class 12'
            tags = ''
            author_name = ''
            source_label = ''
            file = 'x'
            file_url = ''
        self.assertFalse(seo.is_indexable_resource(R()))

    def test_a_short_empty_post_is_not_indexable(self):
        class P:
            is_archived = False
            user = None
            title = 'hi'
            content = 'ok'
            reply_count = 0
        self.assertFalse(seo.is_indexable_post(P()))


if __name__ == '__main__':
    unittest.main()
