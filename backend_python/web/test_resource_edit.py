"""Regressions for the three 500s that flooded the admin inbox on 2026-11-04.

1. `edit_resource` renders `_price_setter.html`, which needs
   `commission_percent`. `upload_resource` imported that helper locally and
   `edit_resource` did not, so every owner who pressed Edit got
   `NameError: name 'commission_percent' is not defined`.
2. A deploy replaced `base_landing.html` (which reads `seo`) while an old
   LSAPI worker still ran the old `landing` view (which did not pass it).
   `{{ seo.og_description|default:seo.description }}` resolves its default
   argument eagerly, so the missing key escaped as `VariableDoesNotExist`
   and the homepage answered 500.
3. The same deploy ran `collectstatic --clear`, so for a couple of seconds a
   running worker's static index named `.gz` files that had been deleted.
   WhiteNoise raises `FileNotFoundError` on those, which is a 500 and a mail
   per asset; it should be a 404.
"""
import uuid
from unittest import mock

from django.core.cache import cache
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.test import Client, TestCase
from django.test.client import RequestFactory
from whitenoise.middleware import WhiteNoiseMiddleware

from api.models import Resource, User
from api.security import issue_auth_token
from api.utils import now_ms
from nebians.middleware import ResilientWhiteNoiseMiddleware


def _user(user_id, username, **extra):
    return User.objects.create(
        id=user_id,
        username=username,
        role=User.ROLE_STUDENT,
        email=f'{username}@example.com',
        email_verified=True,
        created_at=now_ms(),
        is_locked=False,
        is_banned=False,
        **extra,
    )


class ResourceEditPageTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.owner = _user('u-edit-owner', 'edit_owner')
        self.resource = Resource.objects.create(
            id=str(uuid.uuid4()),
            title='Chapter notes',
            subject='Physics',
            type='Note',
            uploaded_by=self.owner,
            approval_status='approved',
            added_at=now_ms(),
        )
        session = self.client.session
        session['auth_token'] = issue_auth_token(self.owner)
        session.save()

    def test_owner_gets_the_edit_page(self):
        response = self.client.get(f'/app/resource/{self.resource.id}/edit/')
        self.assertEqual(response.status_code, 200, response.content[:400])

    def test_non_owner_is_sent_to_the_reader(self):
        stranger = _user('u-edit-stranger', 'edit_stranger')
        other = Client()
        session = other.session
        session['auth_token'] = issue_auth_token(stranger)
        session.save()

        response = other.get(f'/app/resource/{self.resource.id}/edit/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/app/reader/{self.resource.id}/', response['Location'])

    def test_anonymous_is_sent_to_login(self):
        response = Client().get(f'/app/resource/{self.resource.id}/edit/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])


class LandingShellResilienceTests(TestCase):
    """The public shell must render even when the view forgot its `seo` dict."""

    def test_shell_renders_without_seo_context(self):
        html = render_to_string('landing/base_landing.html', {})
        self.assertIn('<meta property="og:description"', html)
        self.assertIn('<meta name="twitter:description"', html)

    def test_shell_prefers_the_og_description(self):
        seo = {'title': 'T', 'description': 'D', 'og_description': 'O', 'path': '/'}
        html = render_to_string('landing/base_landing.html', {'seo': seo})
        self.assertIn('<meta property="og:description" content="O">', html)

    def test_shell_falls_back_to_the_description(self):
        seo = {'title': 'T', 'description': 'D', 'path': '/'}
        html = render_to_string('landing/base_landing.html', {'seo': seo})
        self.assertIn('<meta property="og:description" content="D">', html)
        self.assertIn('<meta name="twitter:description" content="D">', html)


class StaticDeployWindowTests(TestCase):
    """A static file that vanishes under a running worker is a 404, not a 500."""

    def test_missing_compressed_asset_does_not_raise(self):
        middleware = ResilientWhiteNoiseMiddleware(
            get_response=lambda request: HttpResponse('fell through'),
        )
        request = RequestFactory().get('/static/web/js/m3x.js')

        with mock.patch.object(WhiteNoiseMiddleware, '__call__', side_effect=FileNotFoundError('m3x.js.gz')):
            response = middleware(request)

        self.assertEqual(response.status_code, 404)

    def test_real_static_requests_still_serve(self):
        middleware = ResilientWhiteNoiseMiddleware(
            get_response=lambda request: HttpResponse('fell through'),
        )
        response = middleware(RequestFactory().get('/static/web/js/m3x.js'))
        self.assertEqual(response.status_code, 200)

    def test_a_views_file_error_is_still_a_server_error(self):
        def missing_media(request):
            raise FileNotFoundError('a media file the view needed')

        middleware = ResilientWhiteNoiseMiddleware(get_response=missing_media)
        with self.assertRaises(FileNotFoundError):
            middleware(RequestFactory().get('/app/reader/some-id/'))
