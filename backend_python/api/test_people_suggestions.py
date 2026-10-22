"""GET /api/users/suggestions/ -- the server-side replacement for the app's
PeopleSuggestionRepository (see api/people_suggestions.py)."""
import random
import uuid

from django.core.cache import cache
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from api.models import Follow, FollowRequest, Post, User, UserAuthToken
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.services import avatar_or_photo_url
from api.utils import now_ms
from api.view_helpers import map_profile_grade

URL = '/api/users/suggestions/'


def make_user(username, **fields):
    defaults = dict(id=f'u-{username}', email=f'{username}@example.np', email_verified=True,
                    created_at=now_ms(), display_name=username.title())
    defaults.update(fields)
    return User.objects.create(username=username, **defaults)


def sign_in(user):
    raw = f'tok-{user.username}-{uuid.uuid4().hex}'
    now = now_ms()
    UserAuthToken.objects.create(id=str(uuid.uuid4()), user=user, token_hash=hash_auth_token(raw), created_at=now,
                                 last_used_at=now, revoked_at=0, expires_at=now + AUTH_TOKEN_TTL_MS)
    return {'HTTP_AUTHORIZATION': f'Bearer {raw}'}


def follow(a, b):
    Follow.objects.create(follower=a, following=b, created_at=now_ms())


def post(user, n=0, **fields):
    defaults = dict(id=str(uuid.uuid4()), title='Q', content='How?', category='Physics', created_at=now_ms() - n)
    defaults.update(fields)
    return Post.objects.create(user=user, **defaults)


def brute_force(viewer, limit):
    """The spec, evaluated naively over every user: [(username, follows_you, mutual_count, reason)]."""
    me = viewer.pk
    followees = set(Follow.objects.filter(follower_id=me).values_list('following_id', flat=True))
    followers = set(Follow.objects.filter(following_id=me).values_list('follower_id', flat=True))
    requested = set(FollowRequest.objects.filter(sender_id=me).values_list('receiver_id', flat=True))
    feed = set(Post.objects.filter(is_archived=False, is_anonymous=False, user__email_verified=True,
                                   user__is_bot=False).order_by('-created_at').values_list('user_id', flat=True)[:60])
    school = (viewer.school or '').strip().lower()

    def grade(value):
        return (map_profile_grade(value) or '').strip().lower()

    rows = []
    for u in User.objects.all():
        if u.pk == me or u.pk in followees or u.pk in requested:
            continue
        if u.is_locked or u.is_banned or u.is_bot or not u.email_verified:
            continue
        follows_you = u.pk in followers
        mutual = Follow.objects.filter(follower_id__in=followees, following_id=u.pk).count()
        same_school = bool(school) and (u.school or '').lower() == school
        same_class = bool(grade(viewer.class_level)) and grade(u.class_level) == grade(viewer.class_level)
        active = u.pk in feed
        if not (follows_you or mutual or same_school or same_class or active):
            continue
        score = (120 * follows_you + min(mutual, 4) * 28 + 34 * same_school + 16 * same_class + 12 * active
                 + min(u.follower_count, 60) // 5)
        reason = ('Follows you' if follows_you else '1 mutual connection' if mutual == 1
                  else f'{mutual} mutual connections' if mutual else 'From your school' if same_school
                  else 'In your class' if same_class else 'Active in the forum')
        rows.append((-score, u.username, follows_you, mutual, reason))
    rows.sort()
    return [(username, follows_you, mutual, reason) for _s, username, follows_you, mutual, reason in rows[:limit]]


class SuggestionsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.me = make_user('me', school='Alpha School', class_level='Class 12')
        cls.f1, cls.f2, cls.f3 = (make_user(n) for n in ('f1', 'f2', 'f3'))
        for f in (cls.f1, cls.f2, cls.f3):
            follow(cls.me, f)
        cls.fan = make_user('fan', class_level='11')
        follow(cls.fan, cls.me)
        cls.mutual2 = make_user('mutual2', verification_level=1)
        follow(cls.f1, cls.mutual2)
        follow(cls.f2, cls.mutual2)
        cls.mutual1 = make_user('mutual1')
        follow(cls.f3, cls.mutual1)
        cls.schoolmate = make_user('schoolmate', school='alpha school')
        cls.classmate = make_user('classmate', class_level='12', follower_count=60)
        cls.poster = make_user('poster', display_name='  ')
        post(cls.poster)
        # Strong signals, all of them excluded.
        for name, fields in (('locked', {'is_locked': True}), ('banned', {'is_banned': True}),
                             ('unverified', {'email_verified': False}), ('bot', {'is_bot': True})):
            u = make_user(name, school='Alpha School', **fields)
            follow(u, cls.me)
            post(u)
        cls.requested = make_user('requested', school='Alpha School')
        follow(cls.requested, cls.me)
        FollowRequest.objects.create(id=str(uuid.uuid4()), sender=cls.me, receiver=cls.requested, created_at=now_ms())
        follow(cls.f1, cls.me)  # f1 follows back but is followed: excluded
        cls.ghost = make_user('ghost')
        post(cls.ghost, is_anonymous=True)
        cls.retired = make_user('retired')
        post(cls.retired, is_archived=True)

    def setUp(self):
        cache.clear()
        self.client = Client()

    def results(self, user=None, query=''):
        headers = sign_in(user) if user else {}
        r = self.client.get(URL + query, **headers)
        self.assertEqual(r.status_code, 200)
        return r.json()['results']

    def test_signed_out_gets_an_empty_list(self):
        r = self.client.get(URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'results': []})

    def test_order_reasons_and_exclusions(self):
        got = self.results(self.me)
        self.assertEqual([r['username'] for r in got],
                         ['fan', 'mutual2', 'schoolmate', 'classmate', 'mutual1', 'poster'])
        by = {r['username']: r for r in got}
        self.assertEqual(by['fan']['reason'], 'Follows you')
        self.assertTrue(by['fan']['follows_you'])
        self.assertEqual(by['mutual2']['reason'], '2 mutual connections')
        self.assertEqual(by['mutual2']['mutual_count'], 2)
        self.assertEqual(by['mutual1']['reason'], '1 mutual connection')
        self.assertEqual(by['schoolmate']['reason'], 'From your school')
        self.assertEqual(by['classmate']['reason'], 'In your class')  # "12" is "Class 12"
        self.assertEqual(by['poster']['reason'], 'Active in the forum')
        self.assertFalse(by['poster']['follows_you'])
        self.assertEqual(by['poster']['mutual_count'], 0)
        self.assertEqual(got, [dict(r, id=str(r['id'])) for r in got])
        self.assertEqual(set(got[0]), {'id', 'username', 'display_name', 'photo_url', 'detail', 'reason',
                                       'follows_you', 'mutual_count'})

    def test_cards_match_the_popup(self):
        by = {r['username']: r for r in self.results(self.me)}
        for name in ('fan', 'mutual2', 'schoolmate', 'poster'):
            popup = self.client.get(f'/ajax/user-popup/{name}/', **sign_in(self.me)).json()
            self.assertEqual(by[name]['id'], popup['id'])
            self.assertEqual(by[name]['photo_url'], popup['photoUrl'])
            self.assertFalse(popup['isLocked'] or popup['isSelf'] or popup['isFollowing'])
        self.assertEqual(by['fan']['detail'], '11')                  # class level first
        self.assertEqual(by['mutual2']['detail'], 'Verified')        # then the badge label
        self.assertIsNone(by['schoolmate']['detail'])
        self.assertEqual(by['poster']['display_name'], 'poster')     # blank display name
        self.assertEqual(by['fan']['display_name'], 'Fan')
        self.assertEqual(by['fan']['photo_url'], avatar_or_photo_url(self.fan))

    def test_excluded_people_never_appear(self):
        names = {r['username'] for r in self.results(self.me, '?limit=30')}
        self.assertFalse(names & {'me', 'f1', 'f2', 'f3', 'locked', 'banned', 'unverified', 'bot', 'requested',
                                  'ghost', 'retired'})

    def test_mutual_connections_count_every_followee(self):
        star = make_user('star')
        for i in range(6):
            f = make_user(f'extra{i}')
            follow(self.me, f)
            follow(f, star)
        by = {r['username']: r for r in self.results(self.me)}
        self.assertEqual(by['star']['mutual_count'], 6)
        self.assertEqual(by['star']['reason'], '6 mutual connections')

    def test_limit(self):
        self.assertEqual(len(self.results(self.me, '?limit=2')), 2)
        self.assertEqual(len(self.results(self.me, '?limit=0')), 1)
        self.assertEqual(len(self.results(self.me, '?limit=abc')), 6)
        for i in range(40):
            make_user(f'mate{i:02d}', school='Alpha School')
        self.assertEqual(len(self.results(self.me)), 12)
        self.assertEqual(len(self.results(self.me, '?limit=500')), 30)

    def test_matches_the_spec_evaluated_naively(self):
        self.assertEqual([(r['username'], r['follows_you'], r['mutual_count'], r['reason'])
                          for r in self.results(self.me, '?limit=30')], brute_force(self.me, 30))


class SuggestionsAtScaleTests(TestCase):
    """A random graph: the LIMITed school/class lookup and the score must agree with the
    naive evaluation for any viewer and limit, in a fixed number of queries."""

    @classmethod
    def setUpTestData(cls):
        rng = random.Random(7)
        schools = ['Alpha', 'Beta', 'Gamma', '']
        classes = ['12', 'Class 12', '11', 'class 11', '10', 'SEE', 'Bachelor', '']
        users = []
        for i in range(140):
            users.append(User(id=f'r{i:03d}', username=f'{rng.choice("abcxyz")}{"_" if i % 3 else ""}{i:03d}',
                              email=f'r{i}@x.np', email_verified=rng.random() > 0.05, is_locked=rng.random() < 0.08,
                              is_banned=rng.random() < 0.03, is_bot=rng.random() < 0.03, created_at=1,
                              school=rng.choice(schools), class_level=rng.choice(classes),
                              follower_count=rng.choice([0, 3, 5, 12, 33, 59, 60, 140])))
        User.objects.bulk_create(users)
        pairs = set()
        for _ in range(900):
            a, b = rng.sample(range(140), 2)
            pairs.add((a, b))
        Follow.objects.bulk_create([Follow(follower=users[a], following=users[b], created_at=1) for a, b in pairs])
        reqs = {tuple(rng.sample(range(140), 2)) for _ in range(60)} - pairs
        FollowRequest.objects.bulk_create([FollowRequest(id=f'q{a}-{b}', sender=users[a], receiver=users[b], created_at=1)
                                           for a, b in reqs])
        Post.objects.bulk_create([Post(id=f'p{i}', user=rng.choice(users), title='t', content='c', category='General',
                                       is_anonymous=rng.random() < 0.1, is_archived=rng.random() < 0.05,
                                       created_at=1000 + i) for i in range(150)])
        cls.users = users

    def test_matches_the_naive_evaluation(self):
        from api.people_suggestions import suggest_people
        for viewer in self.users[:40]:
            for limit in (1, 3, 12, 30):
                got = [(r['username'], r['follows_you'], r['mutual_count'], r['reason'])
                       for r in suggest_people(viewer, limit)]
                self.assertEqual(got, brute_force(viewer, limit), f'{viewer.username} limit={limit}')

    def test_query_count_does_not_grow_with_the_graph(self):
        viewer = next(u for u in self.users if not (u.is_locked or u.is_banned or u.is_bot) and u.email_verified
                      and u.school and u.class_level and Follow.objects.filter(follower=u).exists()
                      and Follow.objects.filter(following=u).exists())
        headers = sign_in(viewer)
        client = Client()
        with CaptureQueriesContext(connection) as small:
            self.assertEqual(client.get(URL, **headers).status_code, 200)
        extra = [User(id=f'big{i}', username=f'big{i}', email_verified=True, created_at=1, school=viewer.school,
                      class_level=viewer.class_level) for i in range(300)]
        User.objects.bulk_create(extra)
        Follow.objects.bulk_create([Follow(follower=viewer, following=u, created_at=1) for u in extra[:60]]
                                   + [Follow(follower=u, following=v, created_at=1)
                                      for u in extra[:60] for v in extra[100:110]])
        with CaptureQueriesContext(connection) as big:
            self.assertEqual(client.get(URL, **headers).status_code, 200)
        self.assertLessEqual(len(big.captured_queries), 10, [q['sql'][:120] for q in big.captured_queries])
        self.assertEqual(len(small.captured_queries), len(big.captured_queries))
