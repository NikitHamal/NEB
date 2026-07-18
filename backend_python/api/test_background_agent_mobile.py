import json
import tempfile
from pathlib import Path

from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from api.background_agent.crypto import encrypt_secret
from api.models import (
    BackgroundAgentCredential,
    BackgroundAgentDeviceToken,
    BackgroundAgentProject,
    BackgroundAgentSession,
    BotConfig,
)
from api.test_background_agent import create_api_user, login_background_admin
from api.utils import now_ms, uuid_str


@override_settings(BACKGROUND_AGENT_ROOT=Path(tempfile.gettempdir()) / 'nebians-agent-mobile-tests')
class BackgroundAgentMobileApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = create_api_user('mobile-agent-admin')
        self.client = Client()

    def pair_device(self):
        response = self.client.post(
            reverse('bg_mobile_pair_start'),
            data=json.dumps({'deviceName': 'Zeus test device'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        payload = response.json()
        web = Client()
        login_background_admin(web, self.admin)
        approved = web.post(reverse('web:background_agent_mobile_authorize'), {'code': payload['userCode']})
        self.assertEqual(approved.status_code, 200)
        token_response = self.client.post(
            reverse('bg_mobile_pair_token'),
            data=json.dumps({'deviceCode': payload['deviceCode']}),
            content_type='application/json',
        )
        self.assertEqual(token_response.status_code, 200)
        return token_response.json()['accessToken']

    def auth(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def create_project_and_session(self, status='completed'):
        credential = BackgroundAgentCredential.objects.create(
            admin_user=self.admin,
            github_login='mobile-admin',
            encrypted_access_token=encrypt_secret('github-token'),
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        project = BackgroundAgentProject.objects.create(
            id=uuid_str(),
            admin_user=self.admin,
            credential=credential,
            repo_full_name='example/mobile',
            clone_url='https://github.com/example/mobile.git',
            default_branch='main',
            preferred_base_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        provider = BotConfig.objects.create(
            name='Qwen 3.7 Plus',
            enabled=True,
            bot_username='mobile-qwen-provider',
            provider='qwen',
            model='qwen3.7-plus',
        )
        session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=self.admin,
            bot_config=provider,
            title='Mobile task',
            goal='Complete a secure mobile task',
            source_branch='main',
            status=status,
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        return project, session


    def test_pairing_uses_https_public_url(self):
        response = self.client.post(
            reverse('bg_mobile_pair_start'),
            data=json.dumps({'deviceName': 'Zeus test device'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['verificationUrl'].startswith('https://testserver/'))

    def test_archived_state_returns_only_archived_sessions(self):
        token = self.pair_device()
        project, current = self.create_project_and_session()
        archived = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=self.admin,
            bot_config=current.bot_config,
            title='Archived mobile task',
            goal='Complete another secure mobile task',
            source_branch='main',
            status='completed',
            archived_at=now_ms(),
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        response = self.client.get(reverse('bg_mobile_state') + '?archived=1', **self.auth(token))
        self.assertEqual(response.status_code, 200)
        ids = {item['id'] for item in response.json()['sessions']}
        self.assertEqual(ids, {archived.id})
        self.assertNotIn(current.id, ids)

    def test_device_pairing_issues_hashed_persistent_token(self):
        token = self.pair_device()
        self.assertTrue(token.startswith('nba_'))
        device = BackgroundAgentDeviceToken.objects.get(admin_user=self.admin)
        self.assertNotEqual(device.token_hash, token)
        response = self.client.get(reverse('bg_mobile_me'), **self.auth(token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['username'], self.admin.username)

    def test_missing_or_revoked_token_is_rejected(self):
        self.assertEqual(self.client.get(reverse('bg_mobile_me')).status_code, 401)
        token = self.pair_device()
        self.assertEqual(self.client.post(reverse('bg_mobile_revoke'), **self.auth(token)).status_code, 200)
        self.assertEqual(self.client.get(reverse('bg_mobile_me'), **self.auth(token)).status_code, 401)

    def test_archive_restore_and_delete_session(self):
        token = self.pair_device()
        _, session = self.create_project_and_session()
        url = reverse('bg_mobile_session_lifecycle', args=[session.id])
        archived = self.client.post(url, json.dumps({'action': 'archive'}), content_type='application/json', **self.auth(token))
        self.assertEqual(archived.status_code, 200)
        session.refresh_from_db()
        self.assertGreater(session.archived_at, 0)
        restored = self.client.post(url, json.dumps({'action': 'restore'}), content_type='application/json', **self.auth(token))
        self.assertEqual(restored.status_code, 200)
        session.refresh_from_db()
        self.assertEqual(session.archived_at, 0)
        deleted = self.client.delete(url, **self.auth(token))
        self.assertEqual(deleted.status_code, 200)
        self.assertFalse(BackgroundAgentSession.objects.filter(pk=session.id).exists())

    def test_active_session_cannot_be_archived_or_deleted(self):
        token = self.pair_device()
        _, session = self.create_project_and_session(status='running')
        url = reverse('bg_mobile_session_lifecycle', args=[session.id])
        response = self.client.post(url, json.dumps({'action': 'archive'}), content_type='application/json', **self.auth(token))
        self.assertEqual(response.status_code, 409)
        response = self.client.delete(url, **self.auth(token))
        self.assertEqual(response.status_code, 409)
