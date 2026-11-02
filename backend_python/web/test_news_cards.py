"""The blog list and its cards: drawn banner art on the cover, no overlay chips,
one rhythm in the meta row."""
import uuid

from django.test import TestCase

from api.models import Announcement

NOW = 1_700_000_000_000


def _posts(category, n, **kwargs):
    return [Announcement(id=str(uuid.uuid4()), title='%s %d' % (category, i), slug='%s-%d' % (category, i),
                         summary='What changed and when.', content='Body.', category=category,
                         status='published', published_at=NOW - i, **kwargs) for i in range(n)]


class NewsCardTests(TestCase):
    def setUp(self):
        Announcement.objects.bulk_create(
            _posts('exam_results', 2, is_pinned=True) + _posts('update', 1) + _posts('event', 1))

    def test_covers_use_the_banner_art_and_carry_no_chips(self):
        html = self.client.get('/app/news/').content.decode()
        cards = html.count('class="news-card"')
        self.assertGreaterEqual(cards, 4)
        self.assertEqual(html.count('data-neb-art="banner"'), cards)
        for dead in ('news-category-badge', 'news-pin-badge', 'news-card-cover-icon',
                     'news-card-cover-placeholder'):
            self.assertNotIn(dead, html)

    def test_each_category_picks_its_own_family(self):
        html = self.client.get('/app/news/').content.decode()
        for subject in ('exam prep', 'computer', 'social studies'):
            self.assertIn('data-neb-subject="%s"' % subject, html)

    def test_pinned_is_marked_in_the_meta_row(self):
        html = self.client.get('/app/news/').content.decode()
        self.assertIn('class="news-card-pin"', html)
        self.assertIn('Pinned', html)

    def test_related_cards_share_the_cover(self):
        page = self.client.get('/app/news/exam_results-0/')
        self.assertContains(page, 'class="news-card news-card-compact"')
        self.assertContains(page, 'data-neb-art="banner"')
        self.assertNotContains(page, 'news-card-cover-placeholder')
