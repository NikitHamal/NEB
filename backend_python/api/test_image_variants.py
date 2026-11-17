"""Small list copies of stored images: naming, lookup and writing."""
import os
import tempfile
from io import BytesIO

from django.test import SimpleTestCase, override_settings
from PIL import Image

from api import image_variants as iv


class VariantNameTests(SimpleTestCase):
    def test_original_and_resized_copy_share_one_list_copy(self):
        self.assertEqual(iv.variant_name('abc.png', iv.AVATAR), 'abc_s.webp')
        self.assertEqual(iv.variant_name('abc_o.webp', iv.AVATAR), 'abc_s.webp')
        self.assertEqual(iv.variant_name('abc.webp', iv.AVATAR), 'abc_s.webp')

    def test_a_list_copy_has_no_copy(self):
        self.assertIsNone(iv.variant_name('abc_s.webp', iv.AVATAR))
        self.assertIsNone(iv.variant_name('res_x_c.webp', iv.COVER))


class VariantUrlTests(SimpleTestCase):
    def setUp(self):
        iv._CACHE.clear()
        self.tmp = tempfile.TemporaryDirectory()
        os.makedirs(os.path.join(self.tmp.name, 'profile_photos'))
        os.makedirs(os.path.join(self.tmp.name, 'resource_thumbnails'))
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(iv._CACHE.clear)

    def test_unknown_urls_pass_through(self):
        self.assertEqual(iv.variant_url(''), '')
        self.assertEqual(iv.variant_url('https://lh3.googleusercontent.com/a/x=s96-c'),
                         'https://lh3.googleusercontent.com/a/x=s96-c')
        self.assertEqual(iv.variant_url('/media/profile_photos/a/b.png'), '/media/profile_photos/a/b.png')

    def test_missing_copy_returns_the_original(self):
        with override_settings(MEDIA_ROOT=self.tmp.name):
            url = 'https://nebians.consica.com.np/media/profile_photos/u1_abc_o.webp'
            self.assertEqual(iv.variant_url(url), url)

    def test_existing_copy_is_preferred_and_query_dropped(self):
        with override_settings(MEDIA_ROOT=self.tmp.name):
            open(os.path.join(self.tmp.name, 'profile_photos', 'u1_abc_s.webp'), 'wb').write(b'x')
            url = 'https://nebians.consica.com.np/media/profile_photos/u1_abc_o.webp?v=2'
            self.assertEqual(iv.variant_url(url),
                             'https://nebians.consica.com.np/media/profile_photos/u1_abc_s.webp')

    def test_cover_copy(self):
        with override_settings(MEDIA_ROOT=self.tmp.name):
            open(os.path.join(self.tmp.name, 'resource_thumbnails', 'res_q_c.webp'), 'wb').write(b'x')
            self.assertEqual(iv.variant_url('/media/resource_thumbnails/res_q.jpg'),
                             '/media/resource_thumbnails/res_q_c.webp')


class WriteVariantTests(SimpleTestCase):
    def test_large_image_gets_a_smaller_capped_copy(self):
        with tempfile.TemporaryDirectory() as root:
            src = os.path.join(root, 'u_big.png')
            Image.effect_noise((900, 700), 60).convert('RGB').save(src, format='PNG')
            saved = iv.write_variant(src, iv.AVATAR, root)
            self.assertGreater(saved, 0)
            with Image.open(os.path.join(root, 'u_big_s.webp')) as im:
                self.assertEqual(im.format, 'WEBP')
                self.assertEqual(max(im.size), iv.AVATAR[2])
            self.assertEqual(iv.write_variant(src, iv.AVATAR, root), 0)  # second run: nothing to do

    def test_tiny_image_keeps_its_original(self):
        with tempfile.TemporaryDirectory() as root:
            src = os.path.join(root, 'u_tiny.webp')
            Image.new('RGB', (40, 40), (5, 5, 5)).save(src, format='WEBP')
            self.assertEqual(iv.write_variant(src, iv.AVATAR, root), 0)
            self.assertFalse(os.path.exists(os.path.join(root, 'u_tiny_s.webp')))

    def test_broken_file_reports_failure(self):
        with tempfile.TemporaryDirectory() as root:
            src = os.path.join(root, 'u_bad.jpg')
            open(src, 'wb').write(b'not an image')
            self.assertEqual(iv.write_variant(src, iv.AVATAR, root), -1)
