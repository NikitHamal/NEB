"""Web surface for comment polls, member-added options, the insights endpoint and view beacons."""
import json
import uuid

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from api import polls, services
from api.models import Poll, Post, PostReach, Reply, User
from api.utils import now_ms


def _user(name):
    return User.objects.create(id=str(uuid.uuid4()), username=name, email=f'{name}@example.com',
                               email_verified=True, display_name=name.title())


class WebPollInsightsTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client.defaults['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36'
        self.author, self.reader = _user('author'), _user('reader')
        self.post = Post.objects.create(id=str(uuid.uuid4()), user=self.author, title='Which?', content='Pick',
                                        category='Science', created_at=now_ms())

    def _login(self, user):
        from api.security import issue_auth_token
        from api.serializers import UserSerializer
        s = self.client.session
        s['auth_token'] = issue_auth_token(user)
        s['user_data'] = dict(UserSerializer(user).data)
        s.save()

    def _post(self, url, body):
        return self.client.post(url, data=json.dumps(body), content_type='application/json')

    def test_comment_poll_roundtrip(self):
        self._login(self.reader)
        r = self._post(reverse('web:ajax_create_reply', args=[self.post.id]),
                       {'content': '', 'poll': {'question': 'Tea or coffee?', 'options': ['Tea', 'Coffee'],
                                                'allow_add_options': True}})
        self.assertEqual(r.status_code, 201, r.content)
        reply = Reply.objects.get(post=self.post)
        poll = Poll.objects.get(reply=reply)
        self.assertTrue(poll.allow_add_options)

        page = self.client.get(reverse('web:forum_post', args=[self.post.id]))
        self.assertContains(page, 'Tea or coffee?')
        self.assertContains(page, 'data-poll=')

        add = self._post(reverse('web:ajax_poll_option', args=[poll.id]), {'text': 'Juice'})
        self.assertEqual(add.status_code, 201, add.content)
        self.assertEqual([o['text'] for o in add.json()['options']], ['Tea', 'Coffee', 'Juice'])
        dup = self._post(reverse('web:ajax_poll_option', args=[poll.id]), {'text': 'juice'})
        self.assertEqual(dup.status_code, 409)
        back = self._post(reverse('web:ajax_poll_retract', args=[poll.id]), {})
        self.assertEqual(back.status_code, 200)
        self.assertEqual(back.json()['totalVotes'], 0)

    def test_no_nested_comment_poll_and_validation(self):
        self._login(self.reader)
        top = services.create_reply(self.reader, self.post.id, 'top')
        r = self._post(reverse('web:ajax_create_reply', args=[self.post.id]),
                       {'content': 'x', 'parentReplyId': top['id'], 'poll': {'options': ['A', 'B']}})
        self.assertEqual(r.status_code, 400)
        bad = self._post(reverse('web:ajax_create_reply', args=[self.post.id]), {'content': '', 'poll': {'options': ['A']}})
        self.assertEqual(bad.status_code, 400)

    def test_insights_are_author_only(self):
        url = reverse('web:ajax_post_insights', args=[self.post.id])
        self.assertEqual(self.client.get(url).status_code, 401)
        self._login(self.reader)
        self.assertEqual(self.client.get(url).status_code, 403)
        self._login(self.author)
        r = self.client.get(url + '?days=7')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['days'], 7)

    def test_view_beacon_counts_once_and_records_dwell(self):
        url = reverse('web:ajax_post_view', args=[self.post.id])
        self._login(self.reader)
        self.assertTrue(self._post(url, {'surface': 'feed'}).json()['counted'])
        self.assertFalse(self._post(url, {'dwell_ms': 9000}).json()['counted'])
        row = PostReach.objects.get(post=self.post)
        self.assertEqual((row.dwell_ms, row.surface), (9000, 'feed'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)

    def test_opening_the_page_counts_a_view_once(self):
        self._login(self.reader)
        for _ in range(3):
            self.client.get(reverse('web:forum_post', args=[self.post.id]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)

    def test_feed_card_shows_poll_and_insights_for_owner(self):
        data, _ = polls.clean_poll_input({'question': 'Feed poll?', 'options': ['A', 'B']})
        polls.create_poll(data, post=self.post)
        self._login(self.author)
        home = self.client.get(reverse('web:home'))
        self.assertContains(home, 'Feed poll?')
        self.assertContains(home, 'open-post-insights')
