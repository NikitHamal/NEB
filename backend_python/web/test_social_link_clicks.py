import json
import time
import uuid

from django.test import Client, TestCase

from api.models import SocialLink, SocialLinkClick, User
from api.security import issue_auth_token


def _make_user(username):
    return User.objects.create(
        id=str(uuid.uuid4()),
        username=username,
        email=f'{username}@example.com',
        email_verified=True,
        created_at=int(time.time() * 1000),
    )


class SocialLinkClickTests(TestCase):
    def setUp(self):
        self.owner = _make_user('link_owner')
        self.clicker = _make_user('link_clicker')
        self.raw_token = issue_auth_token(self.clicker)
        self.link = SocialLink.objects.create(
            id=str(uuid.uuid4()),
            user=self.owner,
            platform='instagram',
            url='https://instagram.com/link_owner',
            created_at=int(time.time() * 1000),
        )

    def _post(self, client):
        return client.post(
            '/ajax/social-links/track-click/',
            data=json.dumps({
                'link_id': self.link.id,
                'user_id': self.owner.id,
                'platform': self.link.platform,
                'url': self.link.url,
            }),
            content_type='application/json',
        )

    def _login_as_clicker(self):
        client = Client()
        session = client.session
        session['auth_token'] = self.raw_token
        session['user_data'] = {'id': self.clicker.id, 'username': self.clicker.username}
        session.save()
        return client

    def test_signed_in_click_is_recorded_with_uuid(self):
        resp = self._post(self._login_as_clicker())
        self.assertEqual(resp.status_code, 200)
        click = SocialLinkClick.objects.get()
        self.assertEqual(click.clicker_id, self.clicker.id)
        self.assertEqual(click.platform, 'instagram')

    def test_owner_clicking_own_link_is_not_recorded(self):
        token = issue_auth_token(self.owner)
        client = Client()
        session = client.session
        session['auth_token'] = token
        session['user_data'] = {'id': self.owner.id, 'username': self.owner.username}
        session.save()
        resp = self._post(client)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(SocialLinkClick.objects.count(), 0)

    def test_guest_click_is_recorded_without_clicker(self):
        resp = self._post(Client())
        self.assertEqual(resp.status_code, 200)
        click = SocialLinkClick.objects.get()
        self.assertIsNone(click.clicker_id)
