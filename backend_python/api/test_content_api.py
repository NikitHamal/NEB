"""Tests for the read-only content service used by the desktop app (api/content_api.py)."""
import json
import tempfile
from pathlib import Path
from unittest import mock

from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient

from . import content_api as C
from . import content_search


class ContentApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / 'syllabus').mkdir()
        (root / 'study' / '11-physics').mkdir(parents=True)
        (root / 'books').mkdir()
        (root / 'secret.json').write_text('{"secret": true}')
        (root / 'syllabus' / 'index.json').write_text(json.dumps({'grades': [{
            'grade': '11', 'label': 'Class 11', 'short': 'XI',
            'subjects': [{'subject': 'physics', 'name': 'Physics', 'color': '#00f'}]}]}))
        (root / 'syllabus' / '11-physics.json').write_text(json.dumps({'units': [
            {'no': 1, 'title': 'Mechanics', 'topics': ['Projectile motion', 'Vectors']}]}))
        (root / 'study' / '11-physics' / 'index.json').write_text('{"units": []}')
        (root / 'study' / '11-physics' / 'unit-01.json').write_text(json.dumps({
            'title': 'Mechanics', 'html': '<p>A <b>projectile</b> follows a parabola.</p>'}))
        (root / 'books' / 'NEBians-Physics-Grade-11.pdf').write_bytes(b'%PDF-1.4\n' + b'x' * 1000)
        patches = [
            mock.patch.object(C, 'SYLLABUS_DIR', root / 'syllabus'),
            mock.patch.object(C, 'STUDY_DIR', root / 'study'),
            mock.patch.object(C, 'BOOKS_DIR', root / 'books'),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        C._manifest_cache.update(at=0.0, value=None)
        C._books_cache.update(at=0.0, value=[])
        content_search._state.update(sig=None, docs=None)

    def tearDown(self):
        self.tmp.cleanup()

    def test_manifest_and_index_are_public(self):
        r = self.client.get('/api/content/manifest/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['chapters'], 1)
        self.assertEqual(r.json()['books'], 1)
        self.assertEqual(self.client.get('/api/content/index/').json()['grades'][0]['grade'], '11')

    def test_etag_revalidation(self):
        r = self.client.get('/api/content/syllabus/11-physics/')
        self.assertEqual(r.status_code, 200)
        tag = r['ETag']
        again = self.client.get('/api/content/syllabus/11-physics/', HTTP_IF_NONE_MATCH=tag)
        self.assertEqual(again.status_code, 304)

    def test_chapter_and_missing(self):
        self.assertEqual(self.client.get('/api/content/study/11-physics/unit-01/').status_code, 200)
        self.assertEqual(self.client.get('/api/content/study/11-physics/unit-09/').status_code, 404)
        self.assertEqual(self.client.get('/api/content/study/11-chemistry/index/').status_code, 404)

    def test_path_traversal_is_refused(self):
        for bad in ('..%2Fsecret', '..', '.%2e', '11-physics%2F..%2F..%2Fsecret', 'index', 'A-B', '%00'):
            self.assertEqual(self.client.get('/api/content/syllabus/%s/' % bad).status_code, 404, bad)
        for name in ('..%2Fsecret', 'unit-1', 'unit-01.json', 'UNIT-01'):
            self.assertEqual(self.client.get('/api/content/study/11-physics/%s/' % name).status_code, 404, name)
        self.assertIsNone(C.syllabus_path('../secret'))
        self.assertIsNone(C.study_path('11-physics', '../../secret'))
        self.assertIsNone(C.book_path('../secret'))

    def test_only_get_is_allowed(self):
        self.assertEqual(self.client.post('/api/content/manifest/', {}, format='json').status_code, 405)

    def test_search_finds_topics_and_chapter_text(self):
        hits = self.client.get('/api/content/search/', {'q': 'projectile'}).json()['hits']
        kinds = {h['kind'] for h in hits}
        self.assertIn('topic', kinds)
        self.assertIn('text', kinds)
        self.assertTrue(all(h['track'] == '11' and h['subject'] == 'physics' for h in hits))
        self.assertEqual(self.client.get('/api/content/search/', {'q': 'p'}).json()['hits'], [])
        self.assertEqual(self.client.get('/api/content/search/', {'q': 'zzzzqq'}).json()['hits'], [])

    def test_books_list_and_ranged_download(self):
        books = self.client.get('/api/content/books/').json()['books']
        self.assertEqual(books[0]['slug'], 'nebians-physics-grade-11')
        self.assertEqual(books[0]['grade'], '11')
        self.assertEqual(books[0]['subject'], 'Physics')
        url = '/api/content/books/nebians-physics-grade-11/file/'
        full = self.client.get(url)
        self.assertEqual(full.status_code, 200)
        self.assertEqual(len(b''.join(full.streaming_content)), 1009)
        part = self.client.get(url, HTTP_RANGE='bytes=9-18')
        self.assertEqual(part.status_code, 206)
        self.assertEqual(part['Content-Range'], 'bytes 9-18/1009')
        self.assertEqual(b''.join(part.streaming_content), b'x' * 10)
        self.assertEqual(self.client.get(url, HTTP_RANGE='bytes=5000-').status_code, 416)
        self.assertEqual(self.client.get('/api/content/books/nope/file/').status_code, 404)

    def test_range_parser(self):
        self.assertEqual(C.parse_range('bytes=0-9', 100), (0, 9))
        self.assertEqual(C.parse_range('bytes=90-', 100), (90, 99))
        self.assertEqual(C.parse_range('bytes=-10', 100), (90, 99))
        self.assertIsNone(C.parse_range('', 100))
        self.assertIsNone(C.parse_range('bytes=a-b', 100))
        self.assertIs(C.parse_range('bytes=200-300', 100), False)
