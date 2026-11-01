import uuid

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from api.categories import normalize_category
from api.models import Post, Reply, User


def _user(username, **kw):
    display_name = kw.pop('display_name', username.title())
    role = kw.pop('role', 'student')
    return User.objects.create(
        id=str(uuid.uuid4()),
        username=username,
        email=f'{username}@example.com',
        email_verified=True,
        display_name=display_name,
        role=role,
        **kw,
    )


class HomeAndThreadTests(TestCase):
    def setUp(self):
        cache.clear()
        self.aarav = _user('aaravsharma', display_name='Aarav Sharma', contribution_score=340)
        self.sita = _user('sitapoudel', display_name='Dr. Sita Poudel', role='teacher',
                          teacher_verified=True, contribution_score=300)
        self.bot = _user('neby', display_name='Neby', is_bot=True, contribution_score=9999)
        self.post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.aarav,
            title='How should I prepare for rotational motion numericals?',
            content='I can follow the derivation but freeze when the axis changes.',
            category='Science', thumbs_up_count=12, view_count=340,
            reply_count=2, created_at=1_700_000_000_000,
        )
        top = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.sita,
            content='Start with the axis and mark every distance from it.',
            reply_count=1, thumbs_up_count=4, created_at=1_700_000_100_000,
        )
        Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.aarav,
            parent_reply=top, content='That was the missing piece.',
            reply_count=0, created_at=1_700_000_200_000,
        )

    def _logged_in(self, user):
        from api.security import issue_auth_token
        from api.serializers import UserSerializer
        session = self.client.session
        session['auth_token'] = issue_auth_token(user)
        session['user_data'] = dict(UserSerializer(user).data)
        session.save()

    def test_forum_index_and_categories_redirect_home(self):
        for name in ('web:forum', 'web:forum_categories'):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 301)
            self.assertEqual(response.url, reverse('web:home'))

    def test_thread_shows_total_replies_and_a_working_jump_action(self):
        response = self.client.get(reverse('web:forum_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'fp-section-count">2')
        self.assertContains(response, '1 threads')
        self.assertContains(response, 'data-action="jump-to-replies"')

    def test_unanswered_module_lists_a_thread_with_no_replies(self):
        open_post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.aarav,
            title='Why does a heavier object not fall faster in a vacuum?',
            content='The usual answer is not intuitive.',
            category='Science', reply_count=0, created_at=1_700_000_300_000,
        )
        response = self.client.get(reverse('web:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unanswered')
        self.assertContains(response, open_post.title)

    def test_view_counts_are_visible_only_to_the_author(self):
        anon_home = self.client.get(reverse('web:home'))
        self.assertNotContains(anon_home, 'visibility')
        anon_thread = self.client.get(reverse('web:forum_post', args=[self.post.id]))
        self.assertNotContains(anon_thread, 'fp-views')

        self._logged_in(self.aarav)
        own_home = self.client.get(reverse('web:home'))
        self.assertContains(own_home, 'visibility')
        own_thread = self.client.get(reverse('web:forum_post', args=[self.post.id]))
        self.assertContains(own_thread, 'fp-views')

    def test_category_aliases_fold_into_the_canonical_list(self):
        self.assertEqual(normalize_category('Mathematics'), 'Math')
        self.assertEqual(normalize_category('Exam/Test'), 'Exam Prep')
        self.assertEqual(normalize_category('Physics'), 'Science')
