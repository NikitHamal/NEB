"""Profile photos are shrunk on upload (they used to be stored at full size, 1 to 1.4 MB)."""
from io import BytesIO
from types import SimpleNamespace
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, SimpleTestCase
from PIL import Image

from api.security import AVATAR_MAX_EDGE, optimize_avatar_image, save_profile_image_upload


class OptimizeAvatarImageTests(SimpleTestCase):
    def test_large_photo_is_scaled_to_the_edge_limit(self):
        out = optimize_avatar_image(Image.new('RGB', (3000, 2000), (10, 120, 200)))
        self.assertEqual(max(out.size), AVATAR_MAX_EDGE)
        self.assertEqual(out.size, (640, 427))
        self.assertEqual(out.mode, 'RGB')

    def test_small_photo_keeps_its_size(self):
        out = optimize_avatar_image(Image.new('RGB', (200, 200), (1, 2, 3)))
        self.assertEqual(out.size, (200, 200))

    def test_alpha_is_kept(self):
        out = optimize_avatar_image(Image.new('RGBA', (900, 900), (1, 2, 3, 40)))
        self.assertEqual(out.mode, 'RGBA')
        self.assertEqual(max(out.size), AVATAR_MAX_EDGE)

    def test_palette_png_with_transparency_keeps_alpha(self):
        img = Image.new('P', (50, 50))
        img.info['transparency'] = 0
        self.assertEqual(optimize_avatar_image(img).mode, 'RGBA')


class SaveProfileUploadTests(SimpleTestCase):
    def test_upload_is_stored_as_small_webp(self):
        buf = BytesIO()
        Image.effect_noise((1500, 1100), 40).save(buf, format='PNG')
        upload = SimpleUploadedFile('me.png', buf.getvalue(), content_type='image/png')
        saved = {}

        def fake_save(path, content):
            saved['path'] = path
            saved['data'] = content.read()
            return path

        with mock.patch('api.security.default_storage.save', side_effect=fake_save):
            url = save_profile_image_upload(RequestFactory().post('/'), SimpleNamespace(id='u1'), upload)
        self.assertTrue(url.endswith('.webp'))
        self.assertTrue(saved['path'].endswith('.webp'))
        img = Image.open(BytesIO(saved['data']))
        self.assertEqual(img.format, 'WEBP')
        self.assertLessEqual(max(img.size), AVATAR_MAX_EDGE)
        self.assertLess(len(saved['data']), len(buf.getvalue()))
