"""The blog autopilot: dates, sanitising, dedupe, and how an imported post renders.
Everything is offline; the network adapters are replaced with canned items."""
from datetime import datetime, timezone
from unittest import mock

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from api.models import Announcement, NewsSyncState
from services import news_sources as ns
from services import news_sync


def _day(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime('%Y-%m-%d')


class BikramSambatTests(TestCase):
    def test_known_dates(self):
        self.assertEqual(_day(ns.parse_bs('२०८३।०७।१२')), '2026-10-29')
        self.assertEqual(_day(ns.parse_bs('१२ कात्तिक, २०८३')), '2026-10-29')
        self.assertEqual(_day(ns.parse_bs('२०८३ कार्तिक ११ गते मंगलबार १३:१५:२९ बजे')), '2026-10-28')
        self.assertEqual(_day(ns.parse_bs('2083-01-01')), '2026-04-14')

    def test_garbage_is_zero(self):
        self.assertEqual(ns.parse_bs('no date here'), 0)
        self.assertEqual(ns.parse_bs('२०८३।१३।४०'), 0)


class RelevanceTests(TestCase):
    def test_headline_or_two_keywords(self):
        self.assertTrue(ns.is_education('SEE results published', ''))
        self.assertTrue(ns.is_education('Probe widens', 'fake academic certificates at a university'))
        self.assertFalse(ns.is_education('Oil Corporation finishes ERP', 'a university data centre'))


class SanitiseTests(TestCase):
    def test_script_and_handlers_removed_links_absolute(self):
        html = ('<p onclick="x()">Hi <a href="/a.pdf">file</a></p><script>alert(1)</script>'
                '<img src="/i.png" onerror="y()"><h1>Big</h1>')
        out = news_sync.clean_body(html, 'https://moest.gov.np/content/1/x/')
        self.assertNotIn('script', out)
        self.assertNotIn('onclick', out)
        self.assertNotIn('onerror', out)
        self.assertIn('href="https://moest.gov.np/a.pdf"', out)
        self.assertIn('src="https://moest.gov.np/i.png"', out)
        self.assertIn('<h2>Big</h2>', out)
        self.assertIn('rel="noopener nofollow"', out)

    def test_empty_paragraphs_dropped(self):
        self.assertEqual(news_sync.clean_body('<p>&nbsp;</p><p>Real</p>', 'https://x.np/'), '<p>Real</p>')


def _official(guid='7', title='SEE form notice', ts=None):
    return ns.Item(guid=guid, title=title, url='https://neb.gov.np/detail/' + guid,
                   published_at=ts or 0, category='notice',
                   attachments=[ns.attachment('https://neb.gov.np/f/Notice-1.pdf', 'Official notice')])


class ImportTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.src = dict(ns.SOURCE_BY_KEY['neb'])

    def _run(self, items):
        self.src['list'] = lambda s: items
        with mock.patch.object(news_sync.ns, 'SOURCES', [self.src]):
            return news_sync.run_sync()

    def test_imports_once_and_formats(self):
        now = news_sync.now_ms()
        r = self._run([_official(ts=now - 3600_000)])
        self.assertEqual(r[0]['new'], 1)
        a = Announcement.objects.get(source_key='neb')
        self.assertEqual((a.status, a.category, a.source_official), ('published', 'notice', True))
        self.assertEqual(a.source_name, 'National Examinations Board')
        self.assertEqual(a.attachments[0]['kind'], 'pdf')
        self.assertIn('Official', a.tags)
        # Second run: nothing new, nothing duplicated.
        self.assertEqual(self._run([_official(ts=now - 3600_000)])[0]['new'], 0)
        self.assertEqual(Announcement.objects.filter(source_key='neb').count(), 1)

    def test_archived_post_is_not_resurrected(self):
        now = news_sync.now_ms()
        self._run([_official(ts=now)])
        Announcement.objects.update(status='archived')
        self._run([_official(ts=now)])
        self.assertEqual(Announcement.objects.filter(status='published').count(), 0)

    def test_old_and_failing_items_are_skipped(self):
        old = news_sync.now_ms() - news_sync.MAX_AGE_MS - 86400_000
        r = self._run([_official('1', ts=old)])
        self.assertEqual(r[0]['new'], 0)

        def boom(s):
            raise RuntimeError('site down')
        before = NewsSyncState.objects.get(key='neb').last_ok_at
        self.src['list'] = boom
        with mock.patch.object(news_sync.ns, 'SOURCES', [self.src]):
            r = news_sync.run_sync()
        self.assertTrue(r[0]['status'].startswith('failed'))
        self.assertEqual(NewsSyncState.objects.get(key='neb').last_ok_at, before)

    def test_disabled_source_is_skipped_unless_forced(self):
        NewsSyncState.objects.create(key='neb', enabled=False)
        self.assertEqual(self._run([_official(ts=news_sync.now_ms())]), [])

    def test_nepali_title_gets_a_safe_slug(self):
        self._run([_official('9', 'सूचना', ts=news_sync.now_ms())])
        self.assertEqual(Announcement.objects.get(source_key='neb').slug, 'neb-notice-9')

    def test_news_item_is_an_excerpt_not_the_article(self):
        src = dict(ns.SOURCE_BY_KEY['kathmandupost'])
        item = ns.Item(guid='g1', title='Schools reopen', url='https://kathmandupost.com/a',
                       published_at=news_sync.now_ms(), summary='Short <b>standfirst</b>.', category='news')
        src['list'] = lambda s: [item]
        src['detail'] = None
        with mock.patch.object(news_sync.ns, 'SOURCES', [src]):
            news_sync.run_sync()
        a = Announcement.objects.get(source_key='kathmandupost')
        self.assertEqual((a.category, a.source_official), ('news', False))
        self.assertNotIn('<b>', a.content)


class RenderTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        now = news_sync.now_ms()
        self.a = Announcement.objects.create(
            id='a1', title='SEE form notice', slug='see-form-notice', status='published', category='notice',
            published_at=now, created_at=now, updated_at=now, source_key='neb', source_guid='7',
            source_name='National Examinations Board', source_official=True,
            external_url='https://neb.gov.np/detail/7',
            attachments=[{'name': 'Official notice', 'url': 'https://neb.gov.np/f/n.pdf', 'kind': 'pdf'},
                         {'name': 'bad', 'url': 'javascript:alert(1)', 'kind': 'pdf'}])

    def test_list_credits_the_source_with_verified_mark(self):
        html = self.client.get(reverse('web:news_list')).content.decode()
        self.assertIn('National Examinations Board', html)
        self.assertIn('src-verified', html)

    def test_detail_shows_files_and_source_card_only_for_real_urls(self):
        html = self.client.get(reverse('web:news_detail', args=['see-form-notice'])).content.decode()
        self.assertIn('nd-file', html)
        self.assertIn('https://neb.gov.np/f/n.pdf', html)
        self.assertNotIn('javascript:alert', html)
        self.assertIn('nd-source', html)
        self.assertIn('Open original', html)

    def test_news_category_tab_exists(self):
        html = self.client.get(reverse('web:news_list')).content.decode()
        self.assertIn('?category=news', html)
