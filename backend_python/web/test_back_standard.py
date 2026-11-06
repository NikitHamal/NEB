"""One go-back affordance for every sub-page: the .neb-back circle that
web/partials/_back.html ships. These fail the moment a page grows its own."""
import uuid
from pathlib import Path

from django.test import TestCase

from api.models import Announcement

WEB = Path(__file__).resolve().parent

RETIRED = ('rd-back', 'cp-back', 'an-back', 'st-back', 'ss-back-btn', 'fp-back-btn',
           'cs-back', 'nd-back', 'nd-crumbs', 'profile-banner-back-btn')


def _templates():
    return [p for p in (WEB / 'templates').rglob('*.html')
            if not any(part.startswith('admin') for part in p.parts)]


class BackComponentTests(TestCase):
    def test_the_circle_ships_in_the_bundle(self):
        css = (WEB / 'static' / 'web' / 'css' / 'app.css').read_text(encoding='utf-8')
        for rule in ('.neb-back {', '.neb-back:hover', '.neb-back:active',
                     '.neb-back:focus-visible', '.neb-back-row-label', '.neb-back-on-art',
                     '.neb-back-block'):
            self.assertIn(rule, css, rule)

    def test_no_page_keeps_a_private_back_style(self):
        sources = [(p, p.read_text(encoding='utf-8')) for p in _templates()]
        sources += [(p, p.read_text(encoding='utf-8'))
                    for p in (WEB / 'static' / 'web' / 'css').rglob('*.css')]
        for path, text in sources:
            for name in RETIRED:
                self.assertNotIn(name, text, '%s still mentions %s' % (path, name))

    def test_every_page_that_asks_for_the_circle_gives_it_a_home(self):
        for path in _templates():
            if 'partials/_back.html' not in path.read_text(encoding='utf-8'):
                continue
            self.assertIn('as back_href', path.read_text(encoding='utf-8'),
                          '%s includes the back partial with no back_href' % path)

    def test_the_art_variant_is_only_for_cover_art(self):
        users = [p.name for p in _templates()
                 if 'partials' not in p.parts
                 and 'neb-back-on-art' in p.read_text(encoding='utf-8')]
        self.assertEqual(users, ['profile.html'])


class BackRenderTests(TestCase):
    def setUp(self):
        Announcement.objects.create(
            id=str(uuid.uuid4()), title='Terms change', slug='terms-change',
            summary='Read this.', content='Body.', category='notice',
            status='published', published_at=1_700_000_000_000)

    def test_a_detail_page_renders_one_circle(self):
        html = self.client.get('/app/news/terms-change/').content.decode()
        self.assertEqual(html.count('class="neb-back '), 1)
        self.assertIn('href="/app/news/"', html)
        self.assertIn('aria-label="Back to Blog"', html)
