"""Arena send flow shared by the Qwen and DeepAI endpoints (and the community stream)."""
import base64
import json
from unittest.mock import MagicMock, patch

from django.core.cache import cache
from django.test import TestCase

from api.models import ArenaChatAttachment, ArenaChatMessage, ArenaChatSession
from api.test_arena_simple_providers import _events, _user
from api.utils import now_ms, uuid_str


def _session(user, provider, **extra):
    return ArenaChatSession.objects.create(
        id=uuid_str(), user=user, provider=provider,
        arena_session_id=f'{provider}:x', arena_token_id='', qwen_chat_id='chat-1',
        model_id='m1', model_code='m1', model_display_name='M', title='T',
        is_active=True, message_count=0, last_message_at=0,
        created_at=now_ms(), updated_at=now_ms(), **extra,
    )


def _fake_qwen_session():
    return MagicMock(headers={}), {}


class ArenaTurnTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = _user('turn_user')

    def _post(self, path, body=None, **extra):
        return self.client.post(
            path, body or {}, content_type='application/json', **self.user.auth, **extra,
        )

    def _assert_reply_saved(self, sess, text, finish_reason='stop', error=''):
        rows = {m.role: m for m in sess.messages.all()}
        self.assertEqual(rows['assistant'].content, text)
        self.assertEqual(rows['assistant'].finish_reason, finish_reason)
        self.assertEqual(rows['assistant'].error, error)
        self.assertEqual(rows['assistant'].parent_id, rows['user'].id)
        return rows

    def test_deepai_reply_streams_and_persists_with_counters(self):
        sess = _session(self.user, 'deepai')
        chunks = [
            {'type': 'content', 'text': 'Hel'},
            {'type': 'content', 'text': 'lo'},
            {'type': 'done', 'finishReason': 'stop'},
        ]
        with patch('api.deepai_proxy.stream_chat', return_value=iter(chunks)):
            response = self._post(
                f'/api/neby-arena/deepai/sessions/{sess.id}/messages/sse/', {'content': 'hi'},
            )
            events = _events(response)
        self.assertEqual(events[-1], '[DONE]')
        header = json.loads(events[0])['choices'][0]['delta']
        deltas = [json.loads(e)['choices'][0]['delta'].get('content') for e in events[1:-2]]
        self.assertEqual(deltas, ['Hel', 'lo'])
        rows = self._assert_reply_saved(sess, 'Hello')
        self.assertEqual(header['messageId'], rows['assistant'].id)
        self.assertEqual(header['userMessageId'], rows['user'].id)
        sess.refresh_from_db()
        self.assertEqual(sess.message_count, 1)

    def test_deepai_upstream_error_is_recorded_without_counting_the_turn(self):
        sess = _session(self.user, 'deepai')
        with patch('api.deepai_proxy.stream_chat', return_value=iter([{'type': 'error', 'message': 'busy'}])):
            events = _events(self._post(
                f'/api/neby-arena/deepai/sessions/{sess.id}/messages/sse/', {'content': 'hi'},
            ))
        self.assertEqual(json.loads(events[1])['error']['message'], 'busy')
        self.assertEqual(events[-1], '[DONE]')
        self._assert_reply_saved(sess, '', error='busy')
        sess.refresh_from_db()
        self.assertEqual(sess.message_count, 0)

    def test_deepai_json_files_become_attachments_and_reach_the_model(self):
        sess = _session(self.user, 'deepai')
        uploaded = {'download_url': 'https://f/x.png', 'content_type': 'image/png', 'uuid': 'u-1',
                    'original_filename': 'x.png'}
        files = [
            {'name': 'x.png', 'data': base64.b64encode(b'png').decode()},
            {'name': 'evil.exe', 'data': base64.b64encode(b'x').decode()},
        ]
        with patch('api.deepai_proxy.upload_file_from_bytes', return_value=uploaded) as upload, \
                patch('api.deepai_proxy.stream_chat', return_value=iter([{'type': 'done'}])) as stream:
            _events(self._post(
                f'/api/neby-arena/deepai/sessions/{sess.id}/messages/sse/',
                {'content': 'see', 'files': files},
            ))
        upload.assert_called_once_with('x.png', b'png')
        self.assertEqual(stream.call_args.kwargs['attachment_uuids'], ['u-1'])
        attachment = ArenaChatAttachment.objects.get()
        self.assertEqual((attachment.file_name, attachment.show_type, attachment.file_class),
                         ('x.png', 'image', 'deepai'))

    def test_deepai_history_excludes_the_message_being_sent(self):
        sess = _session(self.user, 'deepai')
        with patch('api.deepai_proxy.stream_chat', return_value=iter([{'type': 'done'}])):
            _events(self._post(f'/api/neby-arena/deepai/sessions/{sess.id}/messages/sse/', {'content': 'one'}))
        with patch('api.deepai_proxy.stream_chat', return_value=iter([{'type': 'done'}])) as stream:
            _events(self._post(f'/api/neby-arena/deepai/sessions/{sess.id}/messages/sse/', {'content': 'two'}))
        self.assertEqual(stream.call_args.kwargs['history'],
                         [{'role': 'user', 'content': 'one'}, {'role': 'assistant', 'content': ''}])

    def test_qwen_reply_streams_and_persists(self):
        sess = _session(self.user, 'qwen')
        with patch('api.qwen_proxy._get_session', side_effect=_fake_qwen_session), \
                patch('api.qwen_proxy.get_midtoken', return_value=''), \
                patch('api.qwen_proxy.send_message', return_value='Answer') as send:
            events = _events(self._post(
                f'/api/neby-arena/qwen/sessions/{sess.id}/messages/sse/', {'content': 'q'},
            ))
        self.assertEqual(events[-1], '[DONE]')
        self.assertEqual(send.call_args.args[1:3], ('chat-1', 'q'))
        self._assert_reply_saved(sess, 'Answer')
        sess.refresh_from_db()
        self.assertEqual(sess.message_count, 1)

    def test_qwen_empty_reply_is_an_upstream_error(self):
        sess = _session(self.user, 'qwen')
        with patch('api.qwen_proxy._get_session', side_effect=_fake_qwen_session), \
                patch('api.qwen_proxy.get_midtoken', return_value=''), \
                patch('api.qwen_proxy.send_message', return_value=''):
            events = _events(self._post(
                f'/api/neby-arena/qwen/sessions/{sess.id}/messages/sse/', {'content': 'q'},
            ))
        self.assertEqual(json.loads(events[1])['error']['code'], 'upstream')
        self._assert_reply_saved(sess, '', finish_reason='error', error='Qwen returned an empty response')
        sess.refresh_from_db()
        self.assertEqual(sess.message_count, 0)

    def test_qwen_json_files_over_the_limit_are_rejected_before_anything_is_saved(self):
        sess = _session(self.user, 'qwen')
        files = [{'name': f'{i}.png', 'data': 'AA=='} for i in range(50)]
        response = self._post(
            f'/api/neby-arena/qwen/sessions/{sess.id}/messages/sse/', {'content': 'q', 'files': files},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ArenaChatMessage.objects.count(), 0)

    def test_endpoints_reject_foreign_provider_sessions_and_bad_content(self):
        deepai = _session(self.user, 'deepai')
        qwen = _session(self.user, 'qwen')
        wrong = self._post(f'/api/neby-arena/qwen/sessions/{deepai.id}/messages/sse/', {'content': 'x'})
        self.assertEqual(wrong.status_code, 400)
        self.assertIn('Qwen', wrong.json()['error'])
        empty = self._post(f'/api/neby-arena/qwen/sessions/{qwen.id}/messages/sse/', {'content': '  '})
        self.assertEqual(empty.status_code, 400)
        too_long = self._post(f'/api/neby-arena/qwen/sessions/{qwen.id}/messages/sse/', {'content': 'x' * 8001})
        self.assertEqual(too_long.status_code, 400)
        self.assertEqual(ArenaChatMessage.objects.count(), 0)

    def test_other_users_cannot_post_to_the_session(self):
        sess = _session(self.user, 'deepai')
        other = _user('turn_other')
        response = self.client.post(
            f'/api/neby-arena/deepai/sessions/{sess.id}/messages/sse/', {'content': 'x'},
            content_type='application/json', **other.auth,
        )
        self.assertEqual(response.status_code, 403)
