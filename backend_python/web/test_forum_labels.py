import json
import uuid

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from api.models import Post, Reply, User
from api.security import issue_auth_token
from api.serializers import UserSerializer
from web import forum_labels


def _user(username, **kw):
    return User.objects.create(
        id=str(uuid.uuid4()), username=username, email=f'{username}@example.com',
        email_verified=True, display_name=username.title(), role=kw.pop('role', 'student'), **kw,
    )


def _login(client, user):
    session = client.session
    session['auth_token'] = issue_auth_token(user)
    session['user_data'] = dict(UserSerializer(user).data)
    session.save()


class ForumLabelTests(TestCase):
    def setUp(self):
        cache.clear()
        self.asker = _user('asker')
        self.helper = _user('helper')
        self.stranger = _user('stranger')
        self.admin = _user('boss', is_admin=True)
        self.post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.asker, title='Why is Zeff higher?', content='Explain.',
            category='Science', created_at=1_700_000_000_000,
        )
        self.a = self._reply('a', 'Think of nuclear charge.', 'answer')
        self.b = self._reply('b', 'Step 1, step 2.', 'solution')

    def _reply(self, key, content, kind):
        return Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.helper, content=content, kind=kind,
            created_at=1_700_000_000_000 + len(key),
        )

    def _label(self, reply, label):
        return self.client.post(
            reverse('web:ajax_label_reply', args=[reply.id]),
            data=json.dumps({'label': label}), content_type='application/json',
        )

    def test_asker_can_label_and_it_sticks(self):
        _login(self.client, self.asker)
        res = self._label(self.a, 'helpful')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['labelInfo']['key'], 'helpful')
        self.a.refresh_from_db()
        self.assertEqual(self.a.label, 'helpful')
        self.assertEqual(self.a.labeled_by_id, self.asker.id)
        self.assertTrue(self.a.labeled_at)

    def test_strangers_and_the_replier_cannot_label(self):
        for who in (self.stranger, self.helper):
            self.client.logout()
            _login(self.client, who)
            self.assertEqual(self._label(self.a, 'correct').status_code, 403)
        self.a.refresh_from_db()
        self.assertEqual(self.a.label, '')

    def test_admin_can_label_any_thread(self):
        _login(self.client, self.admin)
        self.assertEqual(self._label(self.a, 'spam').status_code, 200)

    def test_anonymous_is_rejected(self):
        self.assertEqual(self._label(self.a, 'correct').status_code, 401)

    def test_unknown_label_is_rejected(self):
        _login(self.client, self.asker)
        self.assertEqual(self._label(self.a, 'brilliant').status_code, 400)

    def test_only_one_accepted_answer_and_post_resolves(self):
        _login(self.client, self.asker)
        self._label(self.a, 'accepted')
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_resolved)
        self.assertEqual(self.post.accepted_reply_id, self.a.id)
        self._label(self.b, 'accepted')
        self.a.refresh_from_db()
        self.b.refresh_from_db()
        self.post.refresh_from_db()
        self.assertEqual(self.a.label, '')
        self.assertEqual(self.b.label, 'accepted')
        self.assertEqual(self.post.accepted_reply_id, self.b.id)

    def test_removing_accepted_reopens_the_post(self):
        _login(self.client, self.asker)
        self._label(self.a, 'accepted')
        res = self._label(self.a, '')
        self.assertEqual(res.status_code, 200)
        self.post.refresh_from_db()
        self.a.refresh_from_db()
        self.assertFalse(self.post.is_resolved)
        self.assertEqual(self.post.accepted_reply_id, '')
        self.assertEqual(self.a.label, '')
        self.assertEqual(self.a.labeled_at, 0)

    def test_kinds_are_sanitised(self):
        self.assertEqual(forum_labels.clean_kind('SOLUTION'), 'solution')
        self.assertEqual(forum_labels.clean_kind('<script>'), 'comment')
        self.assertEqual(forum_labels.clean_kind(None), 'comment')

    def test_thread_renders_chips_and_mark_button_for_asker_only(self):
        _login(self.client, self.asker)
        self._label(self.b, 'correct')
        cache.clear()
        html = self.client.get(reverse('web:forum_post', args=[self.post.id])).content.decode()
        self.assertIn('Solution', html)
        self.assertIn('fl-tone-good', html)
        self.assertIn(f'data-fl-open="{self.a.id}"', html)

        self.client.logout()
        _login(self.client, self.stranger)
        cache.clear()
        html = self.client.get(reverse('web:forum_post', args=[self.post.id])).content.decode()
        self.assertNotIn(f'data-fl-open="{self.a.id}"', html)
        self.assertIn('Correct', html)
