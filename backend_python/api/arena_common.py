import json

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response

from .models import ArenaChatSession, User


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
