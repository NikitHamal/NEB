"""An uploaded file must show up as `file_url`, or the apps have no Read button for it."""
from django.test import Client, TestCase

from api.models import Resource
from api.utils import now_ms


class ResourceFileUrlTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = now_ms()
        Resource.objects.create(id='fu-file', title='Stored', subject='Physics', grade_level='Class 12', type='PDF',
                                approval_status='approved', added_at=now, source_type='admin', file='resources/2026/01/a.pdf')
        Resource.objects.create(id='fu-link', title='Linked', subject='Physics', grade_level='Class 12', type='PDF',
                                approval_status='approved', added_at=now, source_type='admin',
                                file_url='https://example.com/b.pdf')

    def test_uploaded_file_fills_file_url(self):
        data = Client().get('/api/resources/fu-file').json()
        self.assertTrue(data['file_url'].endswith('resources/2026/01/a.pdf'))
        self.assertEqual(data['file_url'], data['fileUrl'])

    def test_link_stays_as_is(self):
        data = Client().get('/api/resources/fu-link').json()
        self.assertEqual(data['file_url'], 'https://example.com/b.pdf')
