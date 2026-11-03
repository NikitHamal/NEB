import time
import uuid

from django.test import TestCase

from api.models import Resource


class ViewerHasNoDownloadTests(TestCase):
    def setUp(self):
        self.rid = str(uuid.uuid4())
        Resource.objects.create(
            id=self.rid, title='Viewer fixture', description='d', subject='Physics', grade_level='Class 12',
            type='PDF', file_url='/media/resources/fixture.pdf', approval_status='approved',
            added_at=int(time.time() * 1000),
        )

    def test_resource_page_shows_the_file_in_page_and_offers_no_download(self):
        html = self.client.get('/app/reader/%s/' % self.rid).content.decode()
        self.assertIn('vw-stage', html)
        self.assertIn('toolbar=0', html)
        self.assertNotIn(' download', html.split('<main')[-1] if '<main' in html else html)
        self.assertNotIn('btn-download', html)

    def test_player_partial_has_no_download_link(self):
        from django.template.loader import render_to_string
        out = render_to_string('web/partials/nmp_player.html', {'resource': {'media_type': 'video', 'safe_file_url': '/x.mp4', 'title': 't'}})
        self.assertNotIn('download', out.lower().replace('nodownload', ''))
