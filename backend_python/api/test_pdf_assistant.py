"""PDF assistant tests: the Qwen-to-Neby-chain fallback.

The assistant used to hard-502 whenever Qwen's anonymous browser session pool
ran dry — which it does in bulk, because the pool refill fails against
chat.qwen.ai. These tests pin the degrade-to-fallback behaviour:

* ``test_qwen_failure_falls_back_to_the_neby_chain`` — Qwen returns nothing,
  the Neby chain answers, the caller sees 200 and a credit is still spent.
* ``test_qwen_answer_skips_the_fallback`` — a healthy Qwen never calls out.
* ``test_total_failure_still_502s`` — nothing answers, the error is honest.
* ``test_private_profile_can_use_the_assistant`` — ``is_locked`` is the user's
  own private-profile toggle, not a ban; it used to answer 401 "Please sign in".

Run: ``python manage.py test api.test_pdf_assistant -v 2``
"""
import uuid
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from api.models import Resource, User, UserAuthToken
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms

PDF_ASSISTANT_URL = '/api/resources/{resource_id}/pdf-assistant/'


def _user(username):
    raw = f'raw-{username}-token'
    user = User.objects.create(
        id=f'u-{username}',
        username=username,
        email=f'{username}@example.com',
        email_verified=True,
        auth_token=hash_auth_token(raw),
        created_at=now_ms(),
        is_locked=False,
        is_banned=False,
        free_credits=2,
        ai_credits=0,
    )
    UserAuthToken.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        token_hash=hash_auth_token(raw),
        created_at=now_ms(),
        last_used_at=now_ms(),
        revoked_at=0,
        expires_at=now_ms() + AUTH_TOKEN_TTL_MS,
    )
    user.raw_token = raw
    return user


class PdfAssistantFallbackTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = _user('reader')
        self.resource = Resource.objects.create(
            id=str(uuid.uuid4()),
            title='Health and Physical Education',
            subject='Health',
            grade_level='9',
            type='PDF',
            approval_status='approved',
            uploaded_by=self.user,
            source_type='user',
            added_at=now_ms(),
        )
        cache.set(f'pdf-ai-context:{self.resource.id}', 'Chapter one: nutrition and diet.' * 50)

    def _post(self, prompt='Summarize chapter one'):
        return self.client.post(
            PDF_ASSISTANT_URL.format(resource_id=self.resource.id),
            data={'prompt': prompt},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.user.raw_token}',
        )

    def test_qwen_failure_falls_back_to_the_neby_chain(self):
        with patch('api.qwen_utils.client.QwenClient.simple_chat', return_value=(None, 'qwen pool empty')) as qwen, \
                patch('api.neby.call_ai_api', return_value='Fallback tutor answer') as chain:
            response = self._post()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['answer'], 'Fallback tutor answer')
        self.assertTrue(qwen.called)
        self.assertTrue(chain.called)
        self.user.refresh_from_db()
        # the monthly reset tops the account up to 10 first, then the answer
        # spends one
        self.assertEqual(self.user.free_credits, 9)

    def test_qwen_answer_skips_the_fallback(self):
        with patch('api.qwen_utils.client.QwenClient.simple_chat', return_value=('Qwen answer', None)), \
                patch('api.neby.call_ai_api') as chain:
            response = self._post()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['answer'], 'Qwen answer')
        chain.assert_not_called()

    def test_total_failure_still_502s(self):
        with patch('api.qwen_utils.client.QwenClient.simple_chat', return_value=(None, 'qwen pool empty')), \
                patch('api.neby.call_ai_api', return_value=None):
            response = self._post()
        self.assertEqual(response.status_code, 502)
        self.user.refresh_from_db()
        self.assertEqual(self.user.free_credits, 10)

    def test_fallback_chain_exception_is_swallowed(self):
        with patch('api.qwen_utils.client.QwenClient.simple_chat', return_value=(None, 'qwen pool empty')), \
                patch('api.neby.call_ai_api', side_effect=RuntimeError('registry exploded')):
            response = self._post()
        self.assertEqual(response.status_code, 502)

    def test_prompt_is_required(self):
        response = self._post(prompt='')
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_is_rejected(self):
        response = self.client.post(
            PDF_ASSISTANT_URL.format(resource_id=self.resource.id),
            data={'prompt': 'hello'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)


class PrivateProfileTests(TestCase):
    """A private profile (is_locked) is a privacy choice, not a signed-out session."""

    def setUp(self):
        cache.clear()
        self.user = _user('private')
        self.user.is_locked = True
        self.user.save(update_fields=['is_locked'])

    def test_private_profile_can_use_the_assistant(self):
        response = self.client.post(
            PDF_ASSISTANT_URL.format(resource_id=uuid.uuid4()),
            data={'prompt': '', 'history': []},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.user.raw_token}',
        )
        self.assertEqual(response.status_code, 400)

    def test_private_profile_can_read_its_credit_balance(self):
        response = self.client.get('/api/credits/balance/', HTTP_AUTHORIZATION=f'Bearer {self.user.raw_token}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_credits', response.json())

