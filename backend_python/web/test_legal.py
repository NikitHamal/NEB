"""Tests for Privacy Policy, Terms of Service, Copyright Takedown, M3X rules,
and exact cross-platform text parity across Web, Android, and Desktop."""
from __future__ import annotations

import json
import re
from pathlib import Path

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from api.models import TakedownRequest
from . import legal_data
from .seo import STATIC_PAGES

WEB_DIR = Path(__file__).resolve().parent
REPO_ROOT = WEB_DIR.parent.parent

PRIVACY_TPL = WEB_DIR / 'templates' / 'web' / 'legal' / 'privacy.html'
TERMS_TPL = WEB_DIR / 'templates' / 'web' / 'legal' / 'terms.html'
DOC_PARTIAL = WEB_DIR / 'templates' / 'web' / 'legal' / '_document.html'
TAKEDOWN_TPL = WEB_DIR / 'templates' / 'web' / 'takedown.html'
LEGAL_CSS = WEB_DIR / 'static' / 'web' / 'css' / 'pages' / 'web-legal.css'
TAKEDOWN_CSS = WEB_DIR / 'static' / 'web' / 'css' / 'pages' / 'web-takedown.css'
ANDROID_LEGAL = REPO_ROOT / 'app' / 'src' / 'main' / 'java' / 'com' / 'neb' / 'ians' / 'ui' / 'screens' / 'legal' / 'LegalContent.kt'
ANDROID_SCREEN = REPO_ROOT / 'app' / 'src' / 'main' / 'java' / 'com' / 'neb' / 'ians' / 'ui' / 'screens' / 'legal' / 'LegalScreen.kt'
ANDROID_SHEET = REPO_ROOT / 'app' / 'src' / 'main' / 'java' / 'com' / 'neb' / 'ians' / 'ui' / 'screens' / 'auth' / 'AuthLegalSheet.kt'
DESKTOP_LEGAL = REPO_ROOT / 'desktop' / 'src' / 'screens' / 'legal_data.rs'

EMOJI_RE = re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B50\u2705\u274C]')


def _parse_kotlin_sections(block: str) -> list[dict]:
    """Parse LegalSection("N", "Title", listOf("p1", ...)) blocks from LegalContent.kt."""
    sections = []
    sec_re = re.compile(
        r'LegalSection\(\s*"(\d+)"\s*,\s*"([^"]+)"\s*,\s*listOf\((.*?)\)\s*\)',
        re.S,
    )
    str_re = re.compile(r'"((?:[^"\\]|\\.)*)"')
    for num, title, body in sec_re.findall(block):
        paras = [
            s.replace('\\"', '"').replace('$SUPPORT_EMAIL', legal_data.SUPPORT_EMAIL)
            for s in str_re.findall(body)
        ]
        sections.append({'number': num, 'title': title, 'paragraphs': paras})
    return sections


def _parse_rust_sections(block: str) -> list[dict]:
    """Parse Section { n: "N", title: "Title", paras: &[ ... ] } blocks from legal_data.rs."""
    sections = []
    sec_re = re.compile(
        r'Section\s*\{\s*n:\s*"(\d+)"\s*,\s*title:\s*"([^"]+)"\s*,\s*paras:\s*&\[(.*?)\]\s*\}',
        re.S,
    )
    str_re = re.compile(r'"((?:[^"\\]|\\.)*)"')
    for num, title, body in sec_re.findall(block):
        paras = [s.replace('\\"', '"') for s in str_re.findall(body)]
        sections.append({'number': num, 'title': title, 'paragraphs': paras})
    return sections


class LegalM3XSourceTests(SimpleTestCase):
    def test_templates_and_css_have_no_inline_styles_shadows_gradients_or_emojis(self):
        for tpl in (PRIVACY_TPL, TERMS_TPL, DOC_PARTIAL, TAKEDOWN_TPL):
            src = tpl.read_text(encoding='utf-8')
            self.assertNotRegex(src, r'\sstyle="', f'inline style in {tpl.name}')
            self.assertEqual(EMOJI_RE.findall(src), [], f'emoji in {tpl.name}')

        for css_file in (LEGAL_CSS, TAKEDOWN_CSS):
            raw = css_file.read_text(encoding='utf-8')
            clean = re.sub(r'/\*.*?\*/', '', raw, flags=re.S)
            self.assertNotRegex(clean, r'(box|text)-shadow\s*:\s*(?!\s*none)', css_file.name)
            self.assertNotIn('drop-shadow', clean, css_file.name)
            self.assertNotRegex(clean, r'(linear|radial|conic)-gradient', css_file.name)
            self.assertNotRegex(clean, r'border-radius\s*:\s*0\s*[;!]', css_file.name)
            self.assertNotIn('9999px', clean, css_file.name)
            self.assertEqual(EMOJI_RE.findall(raw), [], css_file.name)

    def test_android_legal_files_follow_m3x_rules(self):
        for kt_file in (ANDROID_LEGAL, ANDROID_SCREEN, ANDROID_SHEET):
            src = kt_file.read_text(encoding='utf-8')
            self.assertEqual(EMOJI_RE.findall(src), [], kt_file.name)
            self.assertNotIn('Icons.Default.Close', src, kt_file.name)
        self.assertIn('LegalDocSwitcher', ANDROID_SCREEN.read_text(encoding='utf-8'))
        self.assertIn('LegalDocSwitcher', ANDROID_SHEET.read_text(encoding='utf-8'))

    def test_web_android_and_desktop_legal_content_are_in_lockstep(self):
        kt_src = ANDROID_LEGAL.read_text(encoding='utf-8')
        rs_src = DESKTOP_LEGAL.read_text(encoding='utf-8')

        self.assertEqual(kt_src.count(f'lastUpdated = "{legal_data.LAST_UPDATED}"'), 2)
        self.assertEqual(rs_src.count(f'updated: "{legal_data.LAST_UPDATED}"'), 2)

        kt_privacy_part, kt_terms_part = kt_src.split('val termsOfService = LegalDocument', 1)
        rs_privacy_part, rs_terms_part = rs_src.split('pub static TERMS: Doc', 1)

        kt_privacy = _parse_kotlin_sections(kt_privacy_part)
        kt_terms = _parse_kotlin_sections(kt_terms_part)
        rs_privacy = _parse_rust_sections(rs_privacy_part)
        rs_terms = _parse_rust_sections(rs_terms_part)

        web_privacy = [
            {'number': s['number'], 'title': s['title'], 'paragraphs': s['paragraphs']}
            for s in legal_data.PRIVACY_SECTIONS
        ]
        web_terms = [
            {'number': s['number'], 'title': s['title'], 'paragraphs': s['paragraphs']}
            for s in legal_data.TERMS_SECTIONS
        ]

        self.assertEqual(len(web_privacy), 10)
        self.assertEqual(len(web_terms), 14)
        self.assertEqual(kt_privacy, web_privacy)
        self.assertEqual(kt_terms, web_terms)
        self.assertEqual(rs_privacy, web_privacy)
        self.assertEqual(rs_terms, web_terms)


class LegalPagesRenderTests(TestCase):
    def test_privacy_policy_page_renders_all_sections_and_jsonld(self):
        res = self.client.get(reverse('web:privacy_policy'))
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()
        self.assertIn(legal_data.LAST_UPDATED, html)
        self.assertIn('class="neb-back ', html)
        self.assertNotIn('**', html)
        import html as html_lib
        for sec in legal_data.PRIVACY_SECTIONS:
            self.assertIn(html_lib.escape(sec['title']), html)
            self.assertIn(f'id="sec-{sec["id"]}"', html)
        self.assertIn('HMAC-SHA256', html)
        self.assertIn('AES-GCM', html)
        self.assertIn('RECORD_AUDIO', html)
        self.assertIn('30-day grace period', html)

        ld_blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
        graph = json.loads(ld_blocks[-1])['@graph']
        self.assertEqual(graph[0]['@type'], 'WebPage')
        self.assertEqual(graph[0]['url'], 'https://nebians.consica.com.np/privacy/')

    def test_terms_of_service_page_renders_all_sections_and_links(self):
        import html as html_lib
        res = self.client.get(reverse('web:terms_of_service'))
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()
        self.assertIn(legal_data.LAST_UPDATED, html)
        self.assertIn('class="neb-back ', html)
        self.assertNotIn('**', html)
        for sec in legal_data.TERMS_SECTIONS:
            self.assertIn(html_lib.escape(sec['title']), html)
            self.assertIn(f'id="sec-{sec["id"]}"', html)
        self.assertIn('href="/copyright-takedown/"', html)
        self.assertIn('Copyright Act, 2059', html)
        self.assertIn('NPR 1,000', html)
        self.assertIn('GitHub', html)

    def test_app_prefixed_legal_urls_redirect_permanently(self):
        for src, dst in (
            ('/app/privacy/', '/privacy/'),
            ('/app/terms/', '/terms/'),
            ('/app/copyright/', '/copyright-takedown/'),
        ):
            res = self.client.get(src)
            self.assertEqual(res.status_code, 301, src)
            self.assertEqual(res['Location'], dst)

    def test_sitemap_lists_canonical_legal_urls(self):
        paths = [p[0] for p in STATIC_PAGES]
        self.assertIn('/privacy/', paths)
        self.assertIn('/terms/', paths)
        self.assertIn('/copyright-takedown/', paths)
        self.assertNotIn('/app/privacy/', paths)
        self.assertNotIn('/app/terms/', paths)

    def test_login_page_links_to_terms_and_privacy(self):
        res = self.client.get(reverse('web:login'))
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()
        self.assertIn('href="/terms/"', html)
        self.assertIn('href="/privacy/"', html)

    def test_copyright_takedown_renders_and_submits(self):
        get_res = self.client.get(reverse('web:copyright_takedown'))
        self.assertEqual(get_res.status_code, 200)
        self.assertIn('Copyright Takedown Request', get_res.content.decode())

        post_res = self.client.post(reverse('web:copyright_takedown'), {
            'name': 'Ram Bahadur',
            'email': 'ram@example.com',
            'organization': 'Sunrise Publications',
            'infringing_url': 'https://nebians.consica.com.np/app/reader/res-123/',
            'proof_of_ownership': 'Author and publisher of the original textbook.',
            'statement_good_faith': 'on',
            'statement_accurate': 'on',
            'signature': 'Ram Bahadur',
        })
        self.assertEqual(post_res.status_code, 200)
        self.assertIn('Takedown Request Submitted', post_res.content.decode())
        self.assertEqual(TakedownRequest.objects.filter(email='ram@example.com').count(), 1)
