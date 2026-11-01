import json
import uuid

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from api.models import Post, User
from api.security import issue_auth_token
from api.serializers import UserSerializer


class HomeComposerTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create(
            id=str(uuid.uuid4()), username='composeruser',
            email='composer@example.test', email_verified=True,
            display_name='Composer User', gender='Male', class_level='12',
            role='student',
        )
        Post.objects.create(
            id=str(uuid.uuid4()), user=self.user, title='Existing thread',
            content='Body', category='General', created_at=1_700_000_000_000,
        )

    def _login(self):
        session = self.client.session
        session['auth_token'] = issue_auth_token(self.user)
        session['user_data'] = dict(UserSerializer(self.user).data)
        session.save()

    def test_anonymous_home_has_no_composer(self):
        response = self.client.get(reverse('web:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'hf-composer-card')

    def test_authenticated_home_exposes_identity_and_categories(self):
        self._login()
        response = self.client.get(reverse('web:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="homePostForm"')
        self.assertContains(response, 'id="homePostIdentity"')
        self.assertContains(response, 'Post anonymously')
        self.assertContains(response, 'Entrance Exams')

    def test_composer_posts_both_anonymous_and_named(self):
        self._login()
        for anonymous in (True, False):
            response = self.client.post(
                '/ajax/post/',
                data=json.dumps({
                    'title': 'Composer contract test',
                    'content': 'Created by the home composer test.',
                    'category': 'General',
                    'images': [],
                    'poll': None,
                    'isAnonymous': anonymous,
                    'attachments': [],
                }),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 201)
            post = Post.objects.get(pk=response.json()['id'])
            self.assertEqual(post.is_anonymous, anonymous)
            self.assertEqual(post.user_id, self.user.id)

    def test_composer_posts_with_poll_and_media(self):
        self._login()
        poll_payload = {
            'question': 'Which subject is best?',
            'poll_type': 'voting',
            'allow_multiple': False,
            'duration_ms': 86400000,
            'options': [
                {'text': 'Physics', 'is_correct': False, 'index': 0},
                {'text': 'Math', 'is_correct': False, 'index': 1},
            ],
        }
        media_payload = [
            {'name': 'notes.pdf', 'url': '/media/forum_attachments/notes.pdf', 'size': 1024, 'kind': 'file', 'mime': 'application/pdf'}
        ]
        response = self.client.post(
            '/ajax/post/',
            data=json.dumps({
                'title': 'Poll Discussion Test',
                'content': 'Content with poll and pdf attached.',
                'category': 'Science',
                'images': [],
                'poll': poll_payload,
                'isAnonymous': False,
                'attachments': media_payload,
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        post_id = response.json()['id']
        post = Post.objects.get(pk=post_id)
        self.assertEqual(post.category, 'Science')
        self.assertIsNotNone(post.poll)
        self.assertEqual(post.poll.question, 'Which subject is best?')
        self.assertEqual(post.poll.options.count(), 2)
        self.assertEqual(post.media.count(), 1)
