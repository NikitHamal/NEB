"""Style the whole static tree again would take minutes.

Whitenoise re-compresses every collected file on each run (6745
post-processed on 2026-11-17 for a 156-file delta), including the
51 MB of model weights that barely shrink. These tests pin the two
cheap paths in VersionedStaticFilesStorage: .cact is never compressed,
and a file whose compressed forms already match its bytes is skipped.

Run: ``python manage.py test nebians.test_storage_compression -v 2``
"""
import gzip
import os
import tempfile
from unittest import mock

from django.test import SimpleTestCase

from nebians.storage import VersionedStaticFilesStorage


class SkipCactTests(SimpleTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.storage = VersionedStaticFilesStorage(location=self.tmp.name, base_url='/static/')

    def tearDown(self):
        self.tmp.cleanup()

    def test_cact_is_never_compressed(self):
        compressor = self.storage.create_compressor()
        self.assertFalse(compressor.should_compress('model.cact'))
        self.assertFalse(compressor.should_compress('web/js/needle3/needle3.cact'))
        self.assertFalse(compressor.should_compress('MODEL.CACT'))
        self.assertTrue(compressor.should_compress('app.js'))
        self.assertTrue(compressor.should_compress('style.css'))

    def test_whitenoise_defaults_still_apply(self):
        # Merging must not replace the default skip list (images, fonts, ...).
        compressor = self.storage.create_compressor()
        self.assertFalse(compressor.should_compress('logo.png'))
        self.assertFalse(compressor.should_compress('font.woff2'))

    def test_post_process_writes_nothing_for_cact(self):
        with open(os.path.join(self.tmp.name, 'model.cact'), 'wb') as f:
            f.write(b'x' * 1000)
        with mock.patch('nebians.storage.minify.enabled', return_value=False):
            produced = list(self.storage.post_process({'model.cact': None}))
        self.assertEqual(produced, [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, 'model.cact.gz')))
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, 'model.cact.br')))


class IncrementalCompressionTests(SimpleTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.storage = VersionedStaticFilesStorage(location=self.tmp.name, base_url='/static/')
        self.css = os.path.join(self.tmp.name, 'style.css')
        self.base = 1700000000

    def tearDown(self):
        self.tmp.cleanup()

    def _write_css(self, text, mtime):
        with open(self.css, 'w') as f:
            f.write(text)
        os.utime(self.css, (mtime, mtime))

    def test_new_file_compressed_then_skipped_then_recompressed(self):
        text = 'body { color: red; } ' * 100
        self._write_css(text, self.base)
        with mock.patch('nebians.storage.minify.enabled', return_value=False):
            first = list(self.storage.post_process({'style.css': None}))
            self.assertTrue(first)
            gz = self.css + '.gz'
            self.assertTrue(os.path.exists(gz))
            with gzip.open(gz, 'rt') as f:
                self.assertEqual(f.read(), text)
            gz_mtime = os.path.getmtime(gz)
            second = list(self.storage.post_process({'style.css': None}))
            self.assertEqual(second, [])
            self.assertEqual(os.path.getmtime(gz), gz_mtime)
            new_text = 'body { color: blue; } ' * 100
            self._write_css(new_text, self.base + 100)
            third = list(self.storage.post_process({'style.css': None}))
            self.assertTrue(third)
            with gzip.open(gz, 'rt') as f:
                self.assertEqual(f.read(), new_text)
