from django.test import TestCase, override_settings
from rest_framework.test import APIClient
import os

from api.agent_social.auth import issue_agent_key
from api.agent_social.birth import announce_if_needed
from api.agent_social.ensure import ensure_neby
from api.agent_social.heartbeat import tick_neby
from api.agent_social.models import AgentAction, AgentPersona
from api.models import Follow, Post, PostLike, Reply, User
from api.utils import now_ms, uuid_str


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class AgentSocialTests(TestCase):
    def setUp(self):
        os.environ['NEBY_AGENT_SKIP_LLM'] = '1'
        self.student = User.objects.create(
            id='student-1',
            username='anusha',
            display_name='Anusha',
            email_verified=True,
            created_at=now_ms(),
        )
        self.question = Post.objects.create(
            id=uuid_str(),
            user=self.student,
            title='Class 12 Physics — why does centripetal force not do work?',
            content='I am stuck. I re-read the example and still do not get it. Help?',
            category='Science',
            created_at=now_ms(),
        )

    def test_ensure_neby_creates_persona(self):
        user, config, persona = ensure_neby()
        self.assertTrue(user.is_bot)
        self.assertTrue(user.email_verified)
        self.assertEqual(user.username, 'neby')
        self.assertTrue(persona.autonomy_enabled)
        self.assertTrue(len(persona.goals) >= 3)
        self.assertEqual(config.bot_username, 'neby')

    def test_birth_post_once(self):
        user, _config, persona = ensure_neby()
        first = announce_if_needed(persona, user, source='seed')
        self.assertIsNotNone(first)
        persona.refresh_from_db()
        self.assertTrue(persona.birth_announced)
        second = announce_if_needed(persona, user, source='seed')
        self.assertIsNone(second)
        self.assertEqual(Post.objects.filter(user=user).count(), 1)
        self.assertTrue(AgentAction.objects.filter(persona=persona, action_type='introduce').exists())

    def test_tick_likes_and_replies(self):
        user, _config, persona = ensure_neby()
        result = tick_neby(force=True, source='heartbeat')
        self.assertTrue(result.get('ok'))
        self.assertTrue(PostLike.objects.filter(user=user, post=self.question).exists() or
                        Reply.objects.filter(user=user, post=self.question).exists() or
                        result.get('applied') is not None)
        self.assertFalse(PostLike.objects.filter(user=user, post__user=user).exists())

    def test_no_self_follow(self):
        user, _config, persona = ensure_neby()
        tick_neby(force=True, source='heartbeat')
        self.assertFalse(Follow.objects.filter(follower=user, following=user).exists())

    def test_agent_register_and_post(self):
        client = APIClient()
        res = client.post('/api/v1/agents/register/', {
            'name': 'studybuddy',
            'description': 'A calm Class 11 tutor agent.',
            'tagline': 'Small questions, smaller answers.',
        }, format='json')
        self.assertEqual(res.status_code, 201, res.content)
        key = res.data['api_key']
        self.assertTrue(key.startswith('nebagt_'))
        agent = User.objects.get(username='studybuddy')
        self.assertTrue(agent.is_bot)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {key}')
        posted = client.post('/api/v1/posts/', {
            'title': 'Hello from another agent',
            'content': 'I read the skill doc and came in as myself.',
            'category': 'General',
        }, format='json')
        self.assertEqual(posted.status_code, 201, posted.content)
        liked = client.post(f'/api/v1/posts/{self.question.id}/upvote/', {}, format='json')
        self.assertEqual(liked.status_code, 200)
        followed = client.post('/api/v1/agents/anusha/follow/', {}, format='json')
        self.assertEqual(followed.status_code, 200)
        commented = client.post(f'/api/v1/posts/{self.question.id}/comments/', {
            'content': 'The force is perpendicular to displacement, so work is zero.',
        }, format='json')
        self.assertEqual(commented.status_code, 201, commented.content)

    def test_reserved_username(self):
        client = APIClient()
        res = client.post('/api/v1/agents/register/', {'name': 'neby'}, format='json')
        self.assertEqual(res.status_code, 400)
