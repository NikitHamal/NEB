import json
import logging
from dataclasses import dataclass

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response

from .models import ArenaChatMessage, ArenaChatSession, User
from .utils import now_ms, uuid_str

logger = logging.getLogger(__name__)


def require_user(request):
    user = getattr(request, 'user', None)
    if not isinstance(user, User):
        return None, Response(
            {'error': 'Unauthorized — please sign in'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return user, None


def get_owned_session(user, session_id):
    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return None, Response(
            {'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND,
        )
    if sess.user_id != user.id:
        return None, Response(
            {'error': 'Forbidden — not your session'},
            status=status.HTTP_403_FORBIDDEN,
        )
    return sess, None


def sse_format(obj):
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def sse_done_marker():
    return "data: [DONE]\n\n"


def sse_response(stream):
    response = StreamingHttpResponse(stream, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


def sse_error(message, code='upstream'):
    return sse_format({'error': {'message': message, 'code': code}})


def sse_text_delta(text):
    return sse_format({'choices': [{'index': 0, 'delta': {'content': text}}]})


def validated_content(request, max_chars):
    content = (request.data.get('content') or '').strip()
    if not content:
        return None, Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(content) > max_chars:
        return None, Response(
            {'error': f'Message too long (max {max_chars} chars)'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return content, None


def require_provider_session(user, session_id, provider, label):
    sess, err = get_owned_session(user, session_id)
    if err:
        return None, err
    if sess.provider != provider:
        return None, Response(
            {'error': f'This endpoint only works with {label} sessions.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return sess, None


@dataclass
class Turn:
    """One user message plus the assistant reply streamed back for it."""
    sess: ArenaChatSession
    user_msg_id: str
    asst_msg_id: str
    started_at: int

    @classmethod
    def begin(cls, sess, content):
        user_msg_id = uuid_str()
        ArenaChatMessage.objects.create(
            id=user_msg_id, session=sess, role='user',
            content=content, parent_id='',
            arena_message_id='', finish_reason='', error='',
            duration_ms=0, created_at=now_ms(),
        )
        return cls(sess, user_msg_id, uuid_str(), now_ms())

    def user_message(self):
        return ArenaChatMessage.objects.get(pk=self.user_msg_id)

    def create_assistant_row(self):
        ArenaChatMessage.objects.create(
            id=self.asst_msg_id, session=self.sess, role='assistant',
            content='', parent_id=self.user_msg_id,
            arena_message_id='', finish_reason='', error='',
            duration_ms=0, created_at=self.started_at,
        )

    def header(self):
        return sse_format({
            'choices': [{
                'index': 0,
                'delta': {
                    'role': 'assistant',
                    'messageId': self.asst_msg_id,
                    'userMessageId': self.user_msg_id,
                },
            }],
        })

    def open(self):
        """SSE header, then the assistant row the stream will fill in."""
        yield self.header()
        self.create_assistant_row()

    def close(self, text, finish_reason, error_text, bump_counter=True):
        """Persist the reply and counters; yield the closing SSE events."""
        try:
            ArenaChatMessage.objects.filter(pk=self.asst_msg_id).update(
                content=text,
                finish_reason=finish_reason,
                error=error_text[:200],
                duration_ms=max(0, now_ms() - self.started_at),
                arena_message_id=self.asst_msg_id,
            )
        except Exception as e:
            logger.exception("Failed to finalize assistant row: %s", e)

        if not error_text:
            if bump_counter:
                try:
                    ArenaChatSession.objects.filter(pk=self.sess.id).update(
                        message_count=self.sess.message_count + 1,
                        last_message_at=now_ms(),
                        updated_at=now_ms(),
                    )
                    self.sess.message_count += 1
                    self.sess.last_message_at = now_ms()
                except Exception as e:
                    logger.warning("Counter commit failed: %s", e)
            yield sse_format({
                'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}],
            })
        yield sse_done_marker()
