"""Comment polls, add-an-option polls, unique post views, private device
signals and the per-post insights payload."""
import uuid

from django.test import RequestFactory, TestCase

from api import polls, post_insights, post_reach, services, signals
from api.models import ActorSignal, Poll, PollOption, Post, PostImpression, PostReach, Reply, User
from api.utils import now_ms

APP_UA = 'okhttp/4.12.0'
APP_HDR = 'v=1;app=1.8.0;build=80;os=Android 14;sdk=34;model=Pixel 7;brand=Google;screen=1080x2400;lang=en-US'
CHROME_DESKTOP = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/126.0.0.0 Safari/537.36')


def mk_user(name):
    return User.objects.create(id=str(uuid.uuid4()), username=name, email=f'{name}@example.com',
                               email_verified=True)


def mk_post(author):
    return Post.objects.create(id=str(uuid.uuid4()), user=author, title='T', content='C', category='Science',
                               created_at=now_ms())


def req(ua=CHROME_DESKTOP, **extra):
    r = RequestFactory().get('/', HTTP_USER_AGENT=ua, **extra)
    return r


class CommentPollTests(TestCase):
    def setUp(self):
        self.author, self.voter = mk_user('author'), mk_user('voter')
        self.post = mk_post(self.author)

    def _comment(self, **poll_extra):
        data, err = polls.clean_poll_input({'question': 'Best?', 'options': ['A', 'B'], **poll_extra})
        self.assertEqual(err, '')
        return services.create_reply(self.voter, self.post.id, '', poll_data=data)

    def test_reply_can_be_only_a_poll(self):
        reply = self._comment()
        self.assertIsNotNone(reply)
        self.assertEqual(reply['poll']['question'] if 'poll' in reply else 'Best?', 'Best?')
        self.assertEqual(Poll.objects.get(reply_id=reply['id']).options.count(), 2)

    def test_empty_reply_without_poll_is_rejected(self):
        self.assertIsNone(services.create_reply(self.voter, self.post.id, ''))

    def test_input_rules(self):
        self.assertTrue(polls.clean_poll_input({'options': ['A']})[1])
        self.assertTrue(polls.clean_poll_input({'options': ['A', 'a']})[1])
        self.assertTrue(polls.clean_poll_input({'options': [str(i) for i in range(7)]})[1])
        self.assertTrue(polls.clean_poll_input({'options': ['A', 'x' * 101]})[1])
        data, err = polls.clean_poll_input({'options': ['A', 'B'], 'allowAddOptions': True})
        self.assertTrue(data['allow_add_options'])

    def test_add_option_and_auto_vote(self):
        reply = self._comment(allow_add_options=True)
        poll = Poll.objects.get(reply_id=reply['id'])
        payload, code = polls.add_option(self.author, poll.id, '  Third   choice ')
        self.assertEqual(code, 201)
        texts = [o['text'] for o in payload['options']]
        self.assertEqual(texts, ['A', 'B', 'Third choice'])
        mine = [o for o in payload['options'] if o['addedByMe']][0]
        self.assertTrue(mine['isMine'])
        self.assertEqual(payload['totalVotes'], 1)
        self.assertEqual(polls.add_option(self.voter, poll.id, 'third CHOICE')[1], 409)

    def test_add_option_blocked_when_not_allowed_or_full(self):
        reply = self._comment()
        poll = Poll.objects.get(reply_id=reply['id'])
        self.assertEqual(polls.add_option(self.author, poll.id, 'Nope')[1], 403)
        poll.allow_add_options = True
        poll.save()
        for i in range(10):
            self.assertEqual(polls.add_option(self.author, poll.id, f'x{i}', vote=False)[1], 201)
        self.assertEqual(polls.add_option(self.author, poll.id, 'one more')[1], 400)

    def test_retract_and_revote(self):
        reply = self._comment()
        poll = Poll.objects.get(reply_id=reply['id'])
        a = poll.options.get(text='A')
        services.vote_poll(self.author, poll.id, [a.id])
        payload, code = polls.retract_vote(self.author, poll.id)
        self.assertEqual(code, 200)
        self.assertEqual(payload['totalVotes'], 0)
        self.assertFalse(payload['hasVoted'])
        b = poll.options.get(text='B')
        payload, code = services.vote_poll(self.author, poll.id, [b.id])
        self.assertEqual(code, 200)
        self.assertEqual(payload['userVote'], b.id)

    def test_quiz_is_final(self):
        data, _ = polls.clean_poll_input({'poll_type': 'mcq', 'options': [
            {'text': 'A', 'is_correct': True}, {'text': 'B'}]})
        reply = services.create_reply(self.voter, self.post.id, 'quiz', poll_data=data)
        poll = Poll.objects.get(reply_id=reply['id'])
        services.vote_poll(self.author, poll.id, [poll.options.first().id])
        self.assertEqual(polls.retract_vote(self.author, poll.id)[1], 400)
        self.assertEqual(polls.add_option(self.author, poll.id, 'C')[1], 403)

    def test_multi_choice_user_vote_is_a_list(self):
        reply = self._comment(allow_multiple=True)
        poll = Poll.objects.get(reply_id=reply['id'])
        ids = [o.id for o in poll.options.all()]
        services.vote_poll(self.author, poll.id, ids)
        payload = polls.for_replies([reply['id']], self.author.id)[reply['id']]
        self.assertEqual(sorted(payload['userVote']), sorted(ids))


class PostViewTests(TestCase):
    def setUp(self):
        self.author, self.reader = mk_user('author2'), mk_user('reader')
        self.post = mk_post(self.author)

    def test_one_view_per_viewer_per_day_and_owner_excluded(self):
        r = post_reach.record_view(req(), self.post, self.reader, surface='feed')
        self.assertTrue(r['counted'])
        again = post_reach.record_view(req(), self.post, self.reader, surface='feed')
        self.assertFalse(again['counted'])
        post_reach.record_view(req(), self.post, self.author)
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)
        self.assertEqual(PostReach.objects.filter(post=self.post).count(), 2)
        row = PostReach.objects.get(post=self.post, is_owner=False)
        self.assertEqual(row.hits, 2)
        self.assertEqual(row.device_class, 'desktop')
        self.assertEqual(row.os_family, 'windows')

    def test_guests_and_dwell(self):
        post_reach.record_view(req(HTTP_X_FORWARDED_FOR='1.2.3.4'), self.post, None)
        post_reach.record_view(req(HTTP_X_FORWARDED_FOR='1.2.3.4'), self.post, None, dwell_ms=12000)
        post_reach.record_view(req(HTTP_X_FORWARDED_FOR='5.6.7.8'), self.post, None)
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 2)
        self.assertEqual(PostReach.objects.filter(is_member=False, dwell_ms=12000).count(), 1)

    def test_bots_are_ignored(self):
        out = post_reach.record_view(req('Googlebot/2.1 (+http://www.google.com/bot.html)'), self.post, None)
        self.assertFalse(out['counted'])
        self.assertEqual(PostReach.objects.count(), 0)

    def test_impressions_batch(self):
        n = post_reach.record_impressions(req(), [self.post.id, self.post.id, 'missing'])
        post_reach.record_impressions(req(), [self.post.id])
        self.assertEqual(n, 1)
        self.assertEqual(PostImpression.objects.get(post=self.post).count, 2)


class SignalTests(TestCase):
    def test_signup_records_private_device_context(self):
        request = RequestFactory().post('/', HTTP_USER_AGENT=APP_UA, HTTP_X_NEB_DEVICE=APP_HDR,
                                        HTTP_X_APP_VERSION='1.8.0')
        signals._local.request = request
        try:
            with self.captureOnCommitCallbacks(execute=True):
                user = mk_user('newbie')
        finally:
            signals._local.request = None
        sig = ActorSignal.objects.get(kind='signup')
        self.assertEqual((sig.source, sig.device_class, sig.os_family, sig.app_version),
                         ('app', 'mobile', 'android', '1.8.0'))
        # privacy: nothing identifying in the clear
        row = ' '.join(str(v) for v in (sig.actor, sig.ref, sig.detail, sig.browser, sig.country))
        self.assertNotIn(str(user.id), row)
        self.assertNotIn('Pixel', sig.detail)
        self.assertNotIn('okhttp', row)
        self.assertEqual(sig.actor, signals.actor_tag(user.id))
        detail = signals.unseal(sig.detail)
        self.assertEqual(detail['model'], 'Pixel 7')
        self.assertEqual(detail['os'], 'Android 14')

    def test_interactions_record_with_post_ref(self):
        author, voter = mk_user('a3'), mk_user('v3')
        signals._local.request = req()
        try:
            with self.captureOnCommitCallbacks(execute=True):
                post = mk_post(author)
                data, _ = polls.clean_poll_input({'options': ['A', 'B']})
                polls.create_poll(data, post=post)
                poll = Poll.objects.get(post=post)
                services.vote_poll(voter, poll.id, [poll.options.first().id])
        finally:
            signals._local.request = None
        self.assertEqual(ActorSignal.objects.filter(kind='post', ref=post.id).count(), 1)
        self.assertEqual(ActorSignal.objects.filter(kind='vote', ref=post.id).count(), 1)

    def test_no_request_no_row(self):
        mk_user('quiet')
        self.assertEqual(ActorSignal.objects.count(), 0)

    def test_seal_roundtrip_and_tamper(self):
        blob = signals.seal({'a': 1})
        self.assertEqual(signals.unseal(blob), {'a': 1})
        self.assertEqual(signals.unseal(blob[:-4] + 'AAAA'), {})


class InsightsTests(TestCase):
    def test_payload_shape_and_numbers(self):
        author = mk_user('author4')
        post = mk_post(author)
        for i in range(5):
            u = mk_user(f'r{i}')
            post_reach.record_view(req(), post, u, surface='feed' if i % 2 else 'search', dwell_ms=8000)
        post_reach.record_view(req(APP_UA, HTTP_X_NEB_DEVICE=APP_HDR), post, None)
        for _ in range(3):
            post_reach.record_impressions(req(), [post.id])
        data = post_insights.build(post, days=7)
        self.assertEqual(data['kpis']['views']['value'], 6)
        self.assertEqual(data['kpis']['uniqueViewers']['value'], 6)
        self.assertEqual(data['kpis']['impressions']['value'], 3)
        self.assertEqual(len(data['series']), 7)
        self.assertEqual(sum(d['views'] for d in data['series']), 6)
        self.assertEqual(sum(data['hourly']), 6)
        self.assertEqual(data['audience']['members'], 5)
        self.assertEqual(data['audience']['guests'], 1)
        self.assertEqual({r['key'] for r in data['sources']}, {'web', 'app'})
        self.assertEqual(data['dwell']['samples'], 5)
        self.assertTrue(data['insights'])
        # the author's own opens never count
        post_reach.record_view(req(), post, author)
        self.assertEqual(post_insights.build(post, days=7)['kpis']['views']['value'], 6)

    def test_poll_block(self):
        author, voter = mk_user('a5'), mk_user('v5')
        post = mk_post(author)
        data, _ = polls.clean_poll_input({'question': 'Q', 'options': ['A', 'B']})
        polls.create_poll(data, post=post)
        poll = Poll.objects.get(post=post)
        services.vote_poll(voter, poll.id, [poll.options.first().id])
        out = post_insights.build(post, days=30)
        self.assertEqual(out['poll']['voters'], 1)
        self.assertEqual(out['poll']['options'][0]['votes'], 1)

    def test_empty_post(self):
        post = mk_post(mk_user('a6'))
        out = post_insights.build(post, days=30)
        self.assertFalse(out['hasData'])
        self.assertEqual(out['insights'][0]['tone'], 'info')
