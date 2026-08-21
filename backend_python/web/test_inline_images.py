import io
import tempfile
from PIL import Image
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from api import content_images
from api.models import User, ContentImage
from api.utils import now_ms


def _make_image_bytes(fmt='PNG', size=(32, 32), color=(255, 0, 0)):
    buf = io.BytesIO()
    img = Image.new('RGB', size, color)
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.getvalue()


class ContentImagesHelpersTest(TestCase):
    def test_extract_ids(self):
        self.assertEqual(content_images.extract_image_ids('hi [[img:5]] there [[img:12]]'), [5, 12])
        self.assertEqual(content_images.extract_image_ids('[[img:5]] [[img:5]]'), [5])
        self.assertEqual(content_images.extract_image_ids('no tokens'), [])

    def test_plain_text(self):
        self.assertEqual(content_images.plain_text('a [[img:1]] b'), 'a [image] b')

    def test_strip(self):
        self.assertEqual(content_images.strip_tokens('a [[img:1]] b'), 'a  b')

    def test_clean_keeps_only_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=tmp):
                img = _make_image_bytes()
                from django.core.files.base import ContentFile
                from django.core.files.uploadedfile import SimpleUploadedFile
                uf = SimpleUploadedFile('x.png', img, content_type='image/png')
                row = content_images.save_content_image(uf)
                raw = f'hello [[img:{row.id}]] and [[img:999999]] world'
                cleaned = content_images.clean_content(raw)
                self.assertIn(f'[[img:{row.id}]]', cleaned)
                self.assertNotIn('999999', cleaned)

    def test_token_roundtrip(self):
        inner = 'See this image: [[img:42]] and feel it.'
        tok = content_images.tokenize_for_markdown(inner)
        self.assertIn('ZQXIMG42ZQXEND', tok)
        html = content_images.detokenize_html(tok)
        self.assertIn('data-neb-img="42"', html)
        self.assertIn('neb-chip', html)

    def test_max_images_cap(self):
        self.assertEqual(content_images.MAX_IMAGES_PER_CONTENT, 8)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class InlineUploadViewTest(TestCase):
    def setUp(self):
        from api.security import hash_auth_token
        self.client = Client()
        self.raw_token = User.generate_token()
        self.user = User.objects.create(
            id='u_test_inline',
            username='test_inline_user',
            display_name='Tester',
            email='test_inline@example.com',
            email_verified=True,
            auth_token=hash_auth_token(self.raw_token),
            created_at=now_ms(),
        )
        s = self.client.session
        s['auth_token'] = self.raw_token
        s['user_data'] = {'id': self.user.id, 'username': self.user.username, 'email_verified': True, 'email': self.user.email}
        s.save()

    def test_upload_requires_auth(self):
        c = Client()
        img = _make_image_bytes()
        from django.core.files.uploadedfile import SimpleUploadedFile
        uf = SimpleUploadedFile('a.png', img, content_type='image/png')
        r = c.post(reverse('web:ajax_upload_inline_image'), {'image': uf})
        self.assertEqual(r.status_code, 401)

    def test_upload_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=tmp):
                img = _make_image_bytes()
                from django.core.files.uploadedfile import SimpleUploadedFile
                uf = SimpleUploadedFile('a.png', img, content_type='image/png')
                r = self.client.post(reverse('web:ajax_upload_inline_image'), {'image': uf})
                self.assertIn(r.status_code, (200, 201))
                data = r.json()
                self.assertIn('id', data)
                self.assertIn('url', data)

    def test_toggle_experimental(self):
        r = self.client.post(
            reverse('web:ajax_toggle_inline_images'),
            data='{"enabled": false}',
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.enable_inline_images)
        r2 = self.client.post(
            reverse('web:ajax_toggle_inline_images'),
            data='{"enabled": true}',
            content_type='application/json',
        )
        self.assertEqual(r2.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.enable_inline_images)
