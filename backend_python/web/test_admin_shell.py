import re
from pathlib import Path

from django.core.cache import cache
from django.test import Client, TestCase

from api.models import User
from api.security import issue_auth_token
from web.templatetags.admin_extras import NAV_GROUPS

ADMIN_CSS = Path(__file__).resolve().parent / 'static' / 'web' / 'css' / 'admin'
ADMIN_TEMPLATES = Path(__file__).resolve().parent / 'templates' / 'admin_panel'


class AdminShellTests(TestCase):
    def setUp(self):
        cache.clear()
        admin = User.objects.create(id='u_shell', username='shell_admin', created_at=1, is_admin=True)
        self.client = Client()
        s = self.client.session
        s['auth_token'] = issue_auth_token(admin)
        s.save()

    def test_every_nav_page_renders_inside_the_shell(self):
        for _label, items in NAV_GROUPS:
            for key, url_name, _icon, text, _badge in items:
                from django.urls import reverse

                res = self.client.get(reverse('web:' + url_name))
                self.assertEqual(res.status_code, 200, url_name)
                html = res.content.decode()
                self.assertIn('id="adminDrawer"', html, url_name)
                self.assertRegex(html, r'class="admin-nav-item active"[^>]*data-nav="%s"' % re.escape(text.replace('&', '&amp;')), url_name)

    def test_native_dialogs_are_gone_from_admin_templates(self):
        for path in ADMIN_TEMPLATES.rglob('*.html'):
            src = path.read_text()
            self.assertNotRegex(src, r'(?<![\w.])confirm\(', path.name)
            self.assertNotRegex(src, r'(?<![\w.])alert\(', path.name)

    def test_no_box_shadow_in_admin(self):
        for path in list(ADMIN_CSS.glob('*.css')) + list(ADMIN_TEMPLATES.rglob('*.html')):
            for decl in re.findall(r'box-shadow\s*:\s*([^;}]+)', path.read_text()):
                self.assertEqual(decl.strip().replace('!important', '').strip(), 'none', '%s: %s' % (path.name, decl))

    def test_no_square_radius_in_admin_css(self):
        for path in ADMIN_CSS.glob('*.css'):
            for decl in re.findall(r'border-radius\s*:\s*([^;}]+)', path.read_text()):
                parts = decl.split('/')[0].split()
                self.assertFalse(all(p in ('0', '0px') for p in parts), '%s: %s' % (path.name, decl))
