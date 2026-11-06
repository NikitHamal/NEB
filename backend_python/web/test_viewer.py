import time
import uuid

from django.template.loader import render_to_string
from django.test import TestCase

from api.models import Resource


def make(title, **kw):
    base = dict(id=str(uuid.uuid4()), title=title, description='d', subject='Physics', grade_level='Class 12',
                type='PDF', approval_status='approved', added_at=int(time.time() * 1000))
    base.update(kw)
    return Resource.objects.create(**base)


class ViewerCoverTests(TestCase):
    def page(self, r):
        return self.client.get('/app/reader/%s/' % r.id).content.decode()

    def test_pdf_is_not_opened_on_arrival(self):
        html = self.page(make('P', file_url='/media/resources/fixture.pdf'))
        self.assertIn('data-vw-read', html)
        self.assertIn('data-kind="pdf"', html)
        self.assertNotIn('<iframe', html)
        self.assertNotIn('btn-download', html)

    def test_download_leads_to_the_app_not_the_file(self):
        html = self.page(make('P', file_url='/media/resources/fixture.pdf'))
        self.assertIn('get-app-dialog', html)
        self.assertIn('play.google.com/store/apps/details?id=com.neb.ians', html)
        self.assertNotIn(' download=', html)
        self.assertIn('Coming soon', html)

    def test_kinds(self):
        cases = {
            'image': dict(file_url='/media/x/a.png', type='Image'),
            'audio': dict(file_url='/media/x/a.mp3', type='Audio'),
            'video': dict(file_url='/media/x/a.mp4', type='Video'),
            'embed': dict(file_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', type='Video'),
            'document': dict(file_url='/media/x/a.docx', type='Note'),
            'none': dict(file_url='', type='Note'),
        }
        for kind, kw in cases.items():
            html = self.page(make(kind, **kw))
            self.assertIn('data-kind="%s"' % kind, html, kind)

    def test_embed_uses_the_hosted_player_url_only(self):
        html = self.page(make('Y', file_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', type='Video'))
        self.assertIn('youtube-nocookie.com/embed/dQw4w9WgXcQ', html)

    def test_bundle_lists_every_file(self):
        gid = str(uuid.uuid4())
        lead = make('Lead', file_url='/media/x/a.pdf', upload_group_id=gid)
        make('Second', file_url='/media/x/a.mp3', type='Audio', upload_group_id=gid, is_lead=False)
        html = self.page(lead)
        self.assertIn('vw-parts', html)
        self.assertIn('Second', html)

    def test_paid_resource_stays_locked(self):
        html = self.page(make('Paid', file_url='/media/x/a.pdf', is_paid=True, price=99))
        self.assertIn('data-kind="locked"', html)
        self.assertNotIn('data-vw-read', html)
        self.assertNotIn('a.pdf', html.split('rd-paid-lock-box')[0])

    def test_player_partial_has_no_download_link(self):
        out = render_to_string('web/partials/nmp_player.html', {'resource': {'media_type': 'video', 'safe_file_url': '/x.mp4', 'title': 't'}})
        self.assertNotIn('download', out.lower().replace('nodownload', ''))


class PdfReaderAssetsTests(TestCase):
    def test_reader_assets_ship_and_are_wired(self):
        from pathlib import Path
        js = Path(__file__).parent / 'static' / 'web' / 'js'
        for name in ('pdf-reader.js', 'vendor/pdfjs/pdf.min.mjs', 'vendor/pdfjs/pdf.worker.min.mjs'):
            self.assertTrue((js / name).exists(), name)
        html = self.client.get('/app/reader/%s/' % make('P', file_url='/media/resources/fixture.pdf').id).content.decode()
        self.assertIn('web/js/pdf-reader.js', html)
        self.assertIn('NebPdf', (js / 'resource-viewer.js').read_text())

    def test_menus_are_portaled_and_emoji_follows_focus(self):
        from pathlib import Path
        web = Path(__file__).parent
        self.assertIn('portalMenu(menu)', (web / 'static/web/js/neb-overlays.js').read_text())
        home = (web / 'static/web/js/pages/home.js').read_text(encoding='utf-8')
        self.assertIn('emojiTarget', home)
        self.assertNotIn('contentInput.selectionStart', home.split('function insertEmoji')[1].split('if (emojiBtn')[0])
