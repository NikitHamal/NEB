from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from unittest import mock
import os

from api.agent_social.actions import act_reply
from api.agent_social.auth import issue_agent_key
from api.agent_social.birth import announce_if_needed
from api.agent_social.ensure import ensure_neby
from api.agent_social.heartbeat import tick_neby
from api.agent_social.models import AgentAction, AgentPersona
from api.agent_social.observer import observe
from api.models import Follow, NebyTask, Post, PostLike, Reply, User
from api.neby import process_neby_task
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

    def _mention_thread(self):
        user, config, persona = ensure_neby()
        student_reply = Reply.objects.create(
            id=uuid_str(),
            post=self.question,
            parent_reply_id=None,
            user=self.student,
            content='@neby please explain this in simple words, sathi?',
            created_at=now_ms(),
        )
        return user, config, persona, student_reply

    def test_reply_mention_logs_agent_action(self):
        user, config, persona, student_reply = self._mention_thread()
        task = NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='pending',
            trigger='reply_mention',
            post_id=self.question.id,
            reply_id=student_reply.id,
            created_at=now_ms(),
        )
        with mock.patch('api.neby.call_ai_api', return_value='Sure, here is the simple idea.'):
            process_neby_task(task)
        task.refresh_from_db()
        self.assertEqual(task.status, 'done')
        self.assertTrue(
            Reply.objects.filter(parent_reply_id=student_reply.id, user=user, is_archived=False).exists()
        )
        self.assertTrue(
            AgentAction.objects.filter(
                persona=persona, action_type='reply', source='mention', status='done',
                target_id=student_reply.id,
            ).exists()
        )
        self.assertTrue(
            AgentAction.objects.filter(
                persona=persona, action_type='reply', source='mention', status='done',
                target_id=f'{self.question.id}:{student_reply.id}',
            ).exists()
        )

    def test_autonomous_skips_done_mention_task(self):
        user, config, persona, student_reply = self._mention_thread()
        Reply.objects.create(
            id=uuid_str(),
            post=self.question,
            parent_reply_id=student_reply.id,
            user=user,
            content='Archived mention reply.',
            is_archived=True,
            created_at=now_ms(),
        )
        NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='done',
            trigger='reply_mention',
            post_id=self.question.id,
            reply_id=student_reply.id,
            created_at=now_ms(),
            finished_at=now_ms(),
        )
        before = Reply.objects.filter(post=self.question).count()
        result = act_reply(
            persona, user, self.question, config,
            source='heartbeat', reason='regression',
            parent_reply_id=student_reply.id,
        )
        self.assertIsNone(result)
        self.assertEqual(Reply.objects.filter(post=self.question).count(), before)

    def test_autonomous_skips_mention_agent_action(self):
        user, config, persona, student_reply = self._mention_thread()
        AgentAction.objects.create(
            persona=persona, action_type='reply', status='done', source='mention',
            target_type='post', target_id=student_reply.id,
            content_preview='Mention reply.', reasoning='regression',
        )
        before = Reply.objects.filter(post=self.question).count()
        result = act_reply(
            persona, user, self.question, config,
            source='heartbeat', reason='regression',
            parent_reply_id=student_reply.id,
        )
        self.assertIsNone(result)
        self.assertEqual(Reply.objects.filter(post=self.question).count(), before)

    def test_observe_marks_done_mention_handled(self):
        user, config, persona, student_reply = self._mention_thread()
        NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='done',
            trigger='reply_mention',
            post_id=self.question.id,
            reply_id=student_reply.id,
            created_at=now_ms(),
            finished_at=now_ms(),
        )
        obs = observe(persona, user)
        row = next((r for r in obs['replies'] if r['reply'].id == student_reply.id), None)
        self.assertIsNotNone(row)
        self.assertTrue(row['already_replied'])

    def test_autonomous_skips_done_post_mention(self):
        user, config, persona = ensure_neby()
        Reply.objects.create(
            id=uuid_str(),
            post=self.question,
            parent_reply_id=None,
            user=user,
            content='Archived mention reply.',
            is_archived=True,
            created_at=now_ms(),
        )
        NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='done',
            trigger='post_mention',
            post_id=self.question.id,
            reply_id=None,
            created_at=now_ms(),
            finished_at=now_ms(),
        )
        before = Reply.objects.filter(post=self.question).count()
        result = act_reply(
            persona, user, self.question, config,
            source='heartbeat', reason='regression',
        )
        self.assertIsNone(result)
        self.assertEqual(Reply.objects.filter(post=self.question).count(), before)

    def test_observe_marks_done_post_mention_handled(self):
        user, config, persona = ensure_neby()
        NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='done',
            trigger='post_mention',
            post_id=self.question.id,
            reply_id=None,
            created_at=now_ms(),
            finished_at=now_ms(),
        )
        obs = observe(persona, user)
        row = next((r for r in obs['posts'] if r['post'].id == self.question.id), None)
        self.assertIsNotNone(row)
        self.assertTrue(row['already_replied'])

    def test_autonomous_proceeds_on_failed_task(self):
        user, config, persona, student_reply = self._mention_thread()
        NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='failed',
            trigger='reply_mention',
            post_id=self.question.id,
            reply_id=student_reply.id,
            error_message='No response from AI',
            created_at=now_ms(),
            finished_at=now_ms(),
        )
        before = Reply.objects.filter(post=self.question).count()
        result = act_reply(
            persona, user, self.question, config,
            source='heartbeat', reason='regression',
            parent_reply_id=student_reply.id,
        )
        self.assertIsNotNone(result)
        self.assertEqual(Reply.objects.filter(post=self.question).count(), before + 1)

    def test_autonomous_proceeds_on_personality_skip(self):
        user, config, persona, student_reply = self._mention_thread()
        NebyTask.objects.create(
            id=uuid_str(),
            bot_config=config,
            status='done',
            trigger='reply_mention',
            post_id=self.question.id,
            reply_id=student_reply.id,
            error_message='Ignored by personality (chose not to reply)',
            created_at=now_ms(),
            finished_at=now_ms(),
        )
        before = Reply.objects.filter(post=self.question).count()
        result = act_reply(
            persona, user, self.question, config,
            source='heartbeat', reason='regression',
            parent_reply_id=student_reply.id,
        )
        self.assertIsNotNone(result)
        self.assertEqual(Reply.objects.filter(post=self.question).count(), before + 1)

    def test_enqueue_skips_heartbeat_action(self):
        from api.neby import enqueue_neby_task
        user, config, persona = ensure_neby()
        AgentAction.objects.create(
            persona=persona, action_type='reply', status='done', source='heartbeat',
            target_type='post', target_id=self.question.id,
            content_preview='Autonomous reply.', reasoning='regression',
        )
        task = enqueue_neby_task('post_mention', self.question.id, bot_config=config)
        self.assertIsNone(task)

    def test_tick_skips_when_locked(self):
        from django.core.cache import cache
        user, config, persona = ensure_neby()
        persona.last_tick_at = 0
        persona.save(update_fields=['last_tick_at'])
        lock_key = f'agent_tick_lock:{persona.id}'
        cache.add(lock_key, now_ms(), timeout=60)
        try:
            result = tick_neby(source='heartbeat')
            self.assertTrue(result.get('ok'))
            self.assertEqual(result.get('skipped'), 'tick already running')
        finally:
            cache.delete(lock_key)
