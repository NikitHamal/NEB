"""Avatar + profile endpoints the desktop client relies on for profile pictures."""
from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import User
from .security import issue_auth_token


@override_settings(REST_FRAMEWORK={'DEFAULT_THROTTLE_CLASSES': [], 'DEFAULT_THROTTLE_RATES': {}})
class AvatarProfileTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = User.objects.create(pk='u-avatar', username='sita', email='s@example.com', created_at=1)
        self.token = issue_auth_token(self.user)

    def auth(self):
        return {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_blobatar_svg_is_public_cacheable_and_a_real_image(self):
        r = self.client.get('/avatar/sita/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r['Content-Type'].startswith('image/svg+xml'))
        self.assertIn(b'<svg', r.content)
        self.assertIn('max-age', r['Cache-Control'])
        # conditional request: the desktop cache revalidates cheaply
        again = self.client.get('/avatar/sita/', HTTP_IF_NONE_MATCH=r['ETag'])
        self.assertEqual(again.status_code, 304)

    def test_avatar_name_is_length_limited(self):
        self.assertEqual(self.client.get('/avatar/' + 'x' * 201 + '/').status_code, 400)

    def test_my_avatar_requires_a_token(self):
        self.assertIn(self.client.get('/api/users/me/avatar/').status_code, (401, 403))

    def test_my_avatar_returns_a_url_not_a_filesystem_path(self):
        r = self.client.get('/api/users/me/avatar/', **self.auth())
        self.assertEqual(r.status_code, 200)
        url = r.json()['avatar_url']
        self.assertTrue(url)
        self.assertNotIn('/home/', url)
        self.assertNotIn('\\', url)
        self.assertTrue(url.startswith(('http', '/')))

    def test_avatar_url_is_fetchable(self):
        url = self.client.get('/api/users/me/avatar/', **self.auth()).json()['avatar_url']
        path = url.split('://', 1)[-1]
        path = '/' + path.split('/', 1)[1] if not url.startswith('/') else url
        r = self.client.get(path)
        self.assertEqual(r.status_code, 200)
        self.assertIn('image', r['Content-Type'])
