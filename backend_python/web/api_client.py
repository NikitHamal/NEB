"""
Session management helpers for the web frontend.

The web views no longer make HTTP API roundtrips for data operations — they
call api.services and model managers directly. This module is only responsible
for reading/writing the Django session (auth_token and user_data keys).
"""
import logging

logger = logging.getLogger(__name__)


def get_session_token(request):
    return request.session.get('auth_token')


def get_session_user(request):
    user_data = request.session.get('user_data')
    if isinstance(user_data, dict) and 'gender' not in user_data:
        token = request.session.get('auth_token')
        if token:
            try:
                from api.security import get_user_by_auth_token
                from api.serializers import UserSerializer
                from web.view_helpers import _normalize_user_data
                user = get_user_by_auth_token(token)
                rebuilt = _normalize_user_data(UserSerializer(user).data)
                request.session['user_data'] = rebuilt
                request.session.modified = True
                try:
                    request.session.save()
                except Exception:
                    pass
                return rebuilt
            except Exception:
                pass
    return user_data


def set_session_auth(request, token, user_data):
    request.session['auth_token'] = token
    request.session['user_data'] = user_data
    request.session.modified = True
    try:
        request.session.save()
    except Exception as e:
        logger.error("Failed to explicitly save session: %s", e)


def clear_session_auth(request):
    request.session.pop('auth_token', None)
    request.session.pop('user_data', None)
    request.session.modified = True
    try:
        request.session.save()
    except Exception as e:
        logger.error("Failed to explicitly clear session: %s", e)