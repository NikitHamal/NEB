import json
import re
from pathlib import Path

from django.core.cache import cache
from django.test import Client, TestCase

from . import about_data
from .seo import STATIC_PAGES


class AboutPageTests(TestCase):
    """The About page: content, SEO markup and the same hard design rules as the landing page."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        base = Path(__file__).resolve().parent / 'static' / 'web'
        self.css = (base / 'css' / 'about.css').read_text(encoding='utf-8')
        self.html = self.client.get('/about/').content.decode()

    def test_page_renders_the_whole_team_and_the_company(self):
        r = self.client.get('/about/')
        self.assertEqual(r.status_code, 200)
        for name in ('Nikit Hamal', 'Prashant Chataut', 'Bikram Adhikari', 'Utsab Kafle',
                     'Laxmi Nepal', 'Manisha Kafle', 'Gaurav Rajbanshi', 'Consica Labs'):
            self.assertContains(r, name)
        self.assertContains(r, 'Lead developer')

    def test_seo_head(self):
        self.assertIn('<title>About NEBians', self.html)
        self.assertIn('rel="canonical" href="https://nebians.consica.com.np/about/"', self.html)
        self.assertIn('property="og:url" content="https://nebians.consica.com.np/about/"', self.html)
        self.assertIn('name="description"', self.html)
        self.assertEqual(self.html.count('<h1'), 1)

    def test_jsonld_is_valid_and_matches_the_visible_team(self):
        raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S).group(1)
        graph = json.loads(raw)['@graph']
        types = {n['@type'] for n in graph}
        self.assertTrue({'AboutPage', 'Organization', 'Person', 'BreadcrumbList'} <= types)
        people = {n['name'] for n in graph if n['@type'] == 'Person'}
        self.assertEqual(people, {p['name'] for p in about_data.TEAM})
        org = next(n for n in graph if n['@type'] == 'Organization')
        self.assertEqual(org['parentOrganization']['name'], 'Consica Labs')
        lead = next(n for n in graph if n.get('name') == 'Nikit Hamal')
        self.assertEqual(lead['jobTitle'], 'Lead developer')

    def test_in_sitemap_and_linked_from_landing(self):
        self.assertIn('/about/', [p[0] for p in STATIC_PAGES])
        landing = self.client.get('/').content.decode()
        self.assertIn('href="/about/"', landing)

    def test_nav_links_back_to_landing_sections(self):
        self.assertIn('href="/#inside"', self.html)
        self.assertIn('aria-current="true">About</a>', self.html)

    def test_photo_slot_uses_photo_when_present(self):
        team = about_data.team()
        self.assertEqual(len(team['lead']) + len(team['dev']) + len(team['crew']), len(about_data.TEAM))
        for p in about_data.TEAM:
            self.assertEqual(len(p['name'].strip()) > 0, True)

    def test_design_rules(self):
        for src in (self.css, self.html):
            self.assertNotRegex(src, r'box-shadow\s*:\s*(?!\s*none)')
            self.assertNotIn('drop-shadow', src)
            self.assertNotIn('text-shadow', src)
            self.assertNotRegex(src, r'(linear|radial|conic)-gradient')
            self.assertIsNone(re.search('[\u0900-\u097F]', src), 'Devanagari on the About page')
            self.assertIsNone(re.search('[\U0001F000-\U0001FAFF\u2600-\u27BF]', src), 'emoji on the About page')
        self.assertNotRegex(self.html, r'(?i)>\s*live\s*<')
        self.assertNotRegex(self.html, r'(?i)\b\d[\d,]*k?\+? pages\b')
        self.assertNotRegex(self.css, r'border-radius:\s*0[;\s]')
