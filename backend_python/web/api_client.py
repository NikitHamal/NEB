import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API_BASE = getattr(settings, 'WEB_API_BASE_URL', 'http://127.0.0.1:8000/api')


def _api_call(method, path, token=None, data=None, params=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    url = f'{API_BASE}{path}'
    try:
        if method == 'GET':
            resp = requests.get(url, headers=headers, params=params, timeout=15)
        elif method == 'POST':
            resp = requests.post(url, headers=headers, json=data, timeout=15)
        elif method == 'PATCH':
            resp = requests.patch(url, headers=headers, json=data, timeout=15)
        elif method == 'DELETE':
            resp = requests.delete(url, headers=headers, timeout=15)
        else:
            return None
        if resp.status_code == 204:
            return {'status': 'success'}
        return resp.json() if resp.content else None
    except Exception as e:
        logger.error('API call failed: %s %s -> %s', method, path, e)
        return None


def get_session_token(request):
    return request.session.get('auth_token')


def get_session_user(request):
    return request.session.get('user_data')


def set_session_auth(request, token, user_data):
    request.session['auth_token'] = token
    request.session['user_data'] = user_data
    request.session.modified = True


def clear_session_auth(request):
    request.session.pop('auth_token', None)
    request.session.pop('user_data', None)
    request.session.modified = True


def auth_google(id_token):
    return _api_call('POST', '/auth/google', data={'idToken': id_token})


def check_username(username):
    return _api_call('GET', '/users/check-username', params={'username': username})


def update_profile(token, profile_data):
    return _api_call('POST', '/users/profile', token=token, data=profile_data)


def get_profile(token, username=None):
    if username:
        return _api_call('GET', f'/users/profile/{username}', token=token)
    return None


def get_resources(token=None, params=None):
    return _api_call('GET', '/resources', token=token, params=params)


def get_resource(token=None, resource_id=None):
    if not resource_id:
        return None
    return _api_call('GET', f'/resources/{resource_id}', token=token)


def get_posts(token=None):
    return _api_call('GET', '/posts', token=token)


def get_post(token=None, post_id=None):
    if not post_id:
        return None
    return _api_call('GET', f'/posts/{post_id}', token=token)


def create_post(token, title, content, category):
    return _api_call('POST', '/posts', token=token, data={
        'title': title, 'content': content, 'category': category
    })


def delete_post(token, post_id):
    return _api_call('DELETE', f'/posts/{post_id}', token=token)


def like_post(token, post_id):
    return _api_call('POST', f'/posts/{post_id}/like', token=token)


def get_replies(token, post_id):
    return _api_call('GET', f'/posts/{post_id}/replies', token=token)


def create_reply(token, post_id, content, parent_reply_id=None):
    data = {'content': content}
    if parent_reply_id:
        data['parentReplyId'] = parent_reply_id
    return _api_call('POST', f'/posts/{post_id}/replies', token=token, data=data)


def like_reply(token, reply_id):
    return _api_call('POST', f'/replies/{reply_id}/like', token=token)


# Admin API calls
def admin_get_users(token, params=None):
    return _api_call('GET', '/admin/users', token=token, params=params)


def admin_get_user(token, user_id):
    return _api_call('GET', f'/admin/users/{user_id}', token=token)


def admin_update_user(token, user_id, data):
    return _api_call('PATCH', f'/admin/users/{user_id}', token=token, data=data)


def admin_delete_user(token, user_id):
    return _api_call('DELETE', f'/admin/users/{user_id}', token=token)


def admin_get_resources(token, params=None):
    return _api_call('GET', '/admin/resources', token=token, params=params)


def admin_get_resource(token, resource_id):
    return _api_call('GET', f'/admin/resources/{resource_id}', token=token)


def admin_create_resource(token, data):
    return _api_call('POST', '/admin/resources', token=token, data=data)


def admin_update_resource(token, resource_id, data):
    return _api_call('PATCH', f'/admin/resources/{resource_id}', token=token, data=data)


def admin_delete_resource(token, resource_id):
    return _api_call('DELETE', f'/admin/resources/{resource_id}', token=token)


def admin_get_posts(token, params=None):
    return _api_call('GET', '/admin/posts', token=token, params=params)


def admin_get_post(token, post_id):
    return _api_call('GET', f'/admin/posts/{post_id}', token=token)


def admin_delete_post(token, post_id):
    return _api_call('DELETE', f'/admin/posts/{post_id}', token=token)


def admin_get_replies(token, post_id):
    return _api_call('GET', f'/admin/posts/{post_id}/replies', token=token)


def admin_delete_reply(token, reply_id):
    return _api_call('DELETE', f'/admin/replies/{reply_id}', token=token)


def admin_get_stats(token):
    return _api_call('GET', '/admin/stats', token=token)