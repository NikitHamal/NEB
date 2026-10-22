import json
import os
from unittest import mock

from django.conf import settings
from django.test import Client, TestCase

ART = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'art')


class ArtLibraryTests(TestCase):
    def test_needs_staff(self):
        self.assertEqual(Client().get('/admin/art/').status_code, 302)

    def test_every_scene_in_every_look_is_listed_and_exists(self):
        manifest = json.load(open(os.path.join(ART, 'manifest.json'), encoding='utf-8'))
        n = 0
        for st in manifest['sets']:
            for it in st['items']:
                self.assertEqual(sorted(it['files']), ['flat', 'pixel', 'riso'], it['name'])
                for rel in it['files'].values():
                    with open(os.path.join(ART, rel), encoding='utf-8') as fh:
                        head = fh.read(200)
                    self.assertTrue(head.startswith('<svg xmlns="http://www.w3.org/2000/svg"'), rel)
                    n += 1
        self.assertGreaterEqual(n, 100)
        with mock.patch('web.views_admin_themes._require_staff_admin', return_value=None):
            page = Client().get('/admin/art/')
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'data-card-look="pixel"', count=n // 3)
        self.assertContains(page, '/static/web/art/covers/member-riso.svg')
