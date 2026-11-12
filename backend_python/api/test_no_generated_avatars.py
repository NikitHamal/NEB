"""There are no generated avatars: a profile photo, or nothing (clients draw the initial)."""
from django.test import Client, TestCase

from api.models import User
from api.services import avatar_or_photo_url


class NoGeneratedAvatarTests(TestCase):
    def test_photo_is_returned_as_is(self):
        u = User(username='with_photo', photo_url='https://example.com/me.jpg')
        self.assertEqual(avatar_or_photo_url(u), 'https://example.com/me.jpg')

    def test_no_photo_is_empty(self):
        self.assertEqual(avatar_or_photo_url(User(username='plain', photo_url='')), '')
        self.assertEqual(avatar_or_photo_url(User(username='none', photo_url=None)), '')

    def test_old_generated_avatar_urls_count_as_no_photo(self):
        u = User(username='old', photo_url='/avatar/old/?shape=cloud')
        self.assertEqual(avatar_or_photo_url(u), '')

    def test_avatar_routes_are_gone(self):
        c = Client()
        for path in ('/avatar/sita/', '/app/my-avatar/', '/api/users/me/avatar/'):
            self.assertEqual(c.get(path).status_code, 404, path)

    def test_settings_has_no_avatar_row_or_version_line(self):
        from pathlib import Path
        html = (Path(__file__).resolve().parent.parent / 'web/templates/web/settings.html').read_text(encoding='utf-8')
        self.assertNotIn('my_avatar', html)
        self.assertNotIn('Version 1.0', html)
