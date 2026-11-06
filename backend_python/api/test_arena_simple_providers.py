"""Arena chat for the guest-site providers: one flow, three providers."""
import json
import uuid
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from api.models import ArenaChatMessage, ArenaChatSession, User, UserAuthToken
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms

PROVIDERS = ('k2think', 'poolside', 'inception')


def _user(username):
    raw = f'raw-{username}-token'
    user = User.objects.create(
        id=f'u-{username}', username=username, email=f'{username}@example.com',
        email_verified=True, auth_token=hash_auth_token(raw), created_at=now_ms(),
        is_locked=False, is_banned=False,
    )
    UserAuthToken.objects.create(
        id=str(uuid.uuid4()), user=user, token_hash=hash_auth_token(raw),
        created_at=now_ms(), last_used_at=now_ms(), revoked_at=0,
        expires_at=now_ms() + AUTH_TOKEN_TTL_MS,
    )
    user.auth = {'HTTP_AUTHORIZATION': f'Bearer {raw}'}
    return user


def _events(response):
    body = b''.join(response.streaming_content).decode()
    return [
        part[len('data: '):] for part in body.split('\n\n') if part.startswith('data: ')
    ]


class SimpleProviderArenaTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = _user('arena_user')

    def _create(self, provider, **body):
        return self.client.post(
            f'/api/neby-arena/{provider}/sessions/', body,
            content_type='application/json', **self.user.auth,
        )

    def test_create_session_defaults_to_the_proxys_first_model(self):
        for provider in PROVIDERS:
            response = self._create(provider)
            self.assertEqual(response.status_code, 201, provider)
            session = response.json()['session']
            self.assertEqual(session['provider'], provider)
            self.assertTrue(session['modelId'])
            row = ArenaChatSession.objects.get(pk=session['id'])
            self.assertTrue(row.arena_session_id.startswith(f'{provider}:'))

    def test_models_endpoint_names_the_provider(self):
        response = self.client.get('/api/neby-arena/k2think/models/', **self.user.auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['provider'], 'k2think')
        self.assertTrue(response.json()['models'])

    def test_message_streams_and_persists_the_reply(self):
        for provider in PROVIDERS:
            session_id = self._create(provider).json()['session']['id']
            chunks = [
                {'type': 'text', 'content': 'Hel'},
                {'type': 'text', 'content': 'lo'},
                {'type': 'done', 'finish_reason': 'stop'},
            ]
            with patch(f'api.{provider}_proxy.stream_chat', return_value=iter(chunks)):
                response = self.client.post(
                    f'/api/neby-arena/{provider}/sessions/{session_id}/messages/',
                    {'content': 'hi'}, content_type='application/json', **self.user.auth,
                )
                events = _events(response)
            self.assertEqual(events[-1], '[DONE]', provider)
            texts = [
                json.loads(e)['choices'][0]['delta'].get('content')
                for e in events[:-1]
            ]
            self.assertEqual(''.join(t for t in texts if t), 'Hello', provider)
            reply = ArenaChatMessage.objects.get(session_id=session_id, role='assistant')
            self.assertEqual(reply.content, 'Hello')
            self.assertEqual(ArenaChatSession.objects.get(pk=session_id).message_count, 1)

    def test_upstream_error_is_reported_and_not_counted(self):
        session_id = self._create('poolside').json()['session']['id']
        chunks = [{'type': 'error', 'error': 'boom'}]
        with patch('api.poolside_proxy.stream_chat', return_value=iter(chunks)):
            response = self.client.post(
                f'/api/neby-arena/poolside/sessions/{session_id}/messages/',
                {'content': 'hi'}, content_type='application/json', **self.user.auth,
            )
            events = _events(response)
        self.assertEqual(json.loads(events[1])['error']['code'], 'upstream')
        self.assertEqual(events[-1], '[DONE]')
        self.assertEqual(ArenaChatSession.objects.get(pk=session_id).message_count, 0)

    def test_session_belongs_to_one_provider_and_one_user(self):
        session_id = self._create('k2think').json()['session']['id']
        wrong_provider = self.client.post(
            f'/api/neby-arena/poolside/sessions/{session_id}/messages/',
            {'content': 'hi'}, content_type='application/json', **self.user.auth,
        )
        self.assertEqual(wrong_provider.status_code, 400)
        stranger = _user('stranger')
        forbidden = self.client.post(
            f'/api/neby-arena/k2think/sessions/{session_id}/messages/',
            {'content': 'hi'}, content_type='application/json', **stranger.auth,
        )
        self.assertEqual(forbidden.status_code, 403)

    def test_inception_forwards_the_reasoning_effort(self):
        session_id = self._create('inception').json()['session']['id']
        with patch('api.inception_proxy.stream_chat', return_value=iter([])) as stream:
            response = self.client.post(
                f'/api/neby-arena/inception/sessions/{session_id}/messages/',
                {'content': 'hi', 'reasoningEffort': 'low'},
                content_type='application/json', **self.user.auth,
            )
            _events(response)
        self.assertEqual(stream.call_args.kwargs['reasoning_effort'], 'low')

    def test_empty_content_is_rejected(self):
        session_id = self._create('k2think').json()['session']['id']
        response = self.client.post(
            f'/api/neby-arena/k2think/sessions/{session_id}/messages/',
            {'content': '   '}, content_type='application/json', **self.user.auth,
        )
        self.assertEqual(response.status_code, 400)
