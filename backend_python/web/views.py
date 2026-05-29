import json
import logging

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, Http404

from . import api_client as api

logger = logging.getLogger(__name__)

ADMIN_TOKEN = 'nebians-admin-2024-secure-token'


def _ctx(request, **extra):
    token = api.get_session_token(request)
    user = api.get_session_user(request)
    ctx = {
        'is_authenticated': bool(token),
        'user': user,
        'auth_token': token,
    }
    ctx.update(extra)
    return ctx


def _admin_token(request):
    token = api.get_session_token(request)
    return token if token else ADMIN_TOKEN


# ---------------------------------------------------------------------------
# PUBLIC PAGES
# ---------------------------------------------------------------------------

def home(request):
    token = api.get_session_token(request)
    resources = api.get_resources(token=token) or []
    posts = api.get_posts(token=token) or []
    recent = resources[:10] if isinstance(resources, list) else []
    popular = sorted(resources, key=lambda r: r.get('view_count', 0), reverse=True)[:10] if isinstance(resources, list) else []
    recent_posts = posts[:5] if isinstance(posts, list) else []
    subjects = []
    seen = set()
    for r in (resources if isinstance(resources, list) else []):
        s = r.get('subject', '')
        if s and s not in seen:
            subjects.append(s)
            seen.add(s)
    return render(request, 'web/home.html', _ctx(request,
        recent_resources=recent,
        popular_resources=popular,
        recent_posts=recent_posts,
        subjects=subjects[:12],
    ))


def library(request):
    token = api.get_session_token(request)
    resources = api.get_resources(token=token) or []
    if not isinstance(resources, list):
        resources = []
    subject = request.GET.get('subject', '')
    grade = request.GET.get('grade', '')
    rtype = request.GET.get('type', '')
    filtered = resources
    if subject:
        filtered = [r for r in filtered if r.get('subject', '').lower() == subject.lower()]
    if grade:
        filtered = [r for r in filtered if r.get('grade_level', '').lower() == grade.lower()]
    if rtype:
        filtered = [r for r in filtered if r.get('type', '').lower() == rtype.lower()]
    all_subjects = sorted(set(r.get('subject', '') for r in resources if r.get('subject')))
    all_grades = sorted(set(r.get('grade_level', '') for r in resources if r.get('grade_level')))
    all_types = sorted(set(r.get('type', '') for r in resources if r.get('type')))
    return render(request, 'web/library.html', _ctx(request,
        resources=filtered,
        all_subjects=all_subjects,
        all_grades=all_grades,
        all_types=all_types,
        current_subject=subject,
        current_grade=grade,
        current_type=rtype,
    ))


def search(request):
    token = api.get_session_token(request)
    resources = api.get_resources(token=token) or []
    if not isinstance(resources, list):
        resources = []
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        ql = query.lower()
        results = [r for r in resources if ql in r.get('title', '').lower() or ql in r.get('description', '').lower() or ql in r.get('subject', '').lower()]
    return render(request, 'web/search.html', _ctx(request, query=query, results=results))


def forum(request):
    token = api.get_session_token(request)
    posts = api.get_posts(token=token) or []
    if not isinstance(posts, list):
        posts = []
    category = request.GET.get('category', '')
    if category:
        posts = [p for p in posts if p.get('category', '').lower() == category.lower()]
    categories = sorted(set(p.get('category', '') for p in posts if p.get('category')))
    return render(request, 'web/forum.html', _ctx(request,
        posts=posts,
        categories=categories,
        current_category=category,
    ))


def forum_post(request, post_id):
    token = api.get_session_token(request)
    posts = api.get_posts(token=token) or []
    post = None
    if isinstance(posts, list):
        for p in posts:
            if p.get('id') == post_id:
                post = p
                break
    replies = api.get_replies(token, post_id) or []
    if not isinstance(replies, list):
        replies = []
    return render(request, 'web/forum_post.html', _ctx(request, post=post, replies=replies, post_id=post_id))


def create_post(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category = request.POST.get('category', '').strip()
        if title and content and category:
            result = api.create_post(token, title, content, category)
            if result and result.get('id'):
                return redirect('web:forum_post', post_id=result['id'])
    categories = ['General', 'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Computer Science', 'Exam Tips']
    return render(request, 'web/create_post.html', _ctx(request, categories=categories))


def reply_post(request, post_id):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    posts = api.get_posts(token=token) or []
    post = None
    if isinstance(posts, list):
        for p in posts:
            if p.get('id') == post_id:
                post = p
                break
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        parent_reply_id = request.POST.get('parent_reply_id', '') or None
        if content:
            api.create_reply(token, post_id, content, parent_reply_id)
            return redirect('web:forum_post', post_id=post_id)
    return render(request, 'web/reply.html', _ctx(request, post=post, post_id=post_id))


def reader(request, resource_id):
    token = api.get_session_token(request)
    resources = api.get_resources(token=token) or []
    resource = None
    if isinstance(resources, list):
        for r in resources:
            if r.get('id') == resource_id:
                resource = r
                break
    return render(request, 'web/reader.html', _ctx(request, resource=resource, resource_id=resource_id))


def profile(request, username):
    token = api.get_session_token(request)
    profile_data = api.get_profile(token, username)
    if not profile_data:
        raise Http404("User not found")
    return render(request, 'web/profile.html', _ctx(request, profile_user=profile_data, username=username))


def edit_profile(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    user = api.get_session_user(request)
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username', '').strip(),
            'dob': request.POST.get('dob', '').strip(),
            'gender': request.POST.get('gender', ''),
            'classLevel': request.POST.get('class_level', ''),
            'subjects': request.POST.get('subjects', ''),
            'pradesh': request.POST.get('pradesh', ''),
            'district': request.POST.get('district', ''),
            'school': request.POST.get('school', ''),
            'isLocked': request.POST.get('is_locked') == 'on',
        }
        email = request.POST.get('email', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        if email:
            data['email'] = email
        if display_name:
            data['displayName'] = display_name
        result = api.update_profile(token, data)
        if result and result.get('status') == 'success':
            new_user = result.get('user', {})
            api.set_session_auth(request, token, new_user)
            return redirect('web:home')
    return render(request, 'web/edit_profile.html', _ctx(request))


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

def login_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    return render(request, 'web/login.html', _ctx(request))


@require_POST
def google_auth(request):
    try:
        data = json.loads(request.body)
        id_token = data.get('idToken', '')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    result = api.auth_google(id_token)
    if not result or result.get('status') != 'success':
        return JsonResponse({'error': 'Authentication failed'}, status=401)
    token = result.get('authToken', '')
    user = result.get('user', {})
    user['isNewUser'] = result.get('isNewUser', False)
    api.set_session_auth(request, token, user)
    return JsonResponse({'status': 'success', 'user': user, 'isNewUser': result.get('isNewUser', False)})


def logout(request):
    api.clear_session_auth(request)
    return redirect('web:home')


# ---------------------------------------------------------------------------
# AJAX ENDPOINTS
# ---------------------------------------------------------------------------

@require_POST
def ajax_like_post(request, post_id):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    result = api.like_post(token, post_id)
    if result:
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_like_reply(request, reply_id):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    result = api.like_reply(token, reply_id)
    if result:
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_create_reply(request, post_id):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentReplyId')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    result = api.create_reply(token, post_id, content, parent_id)
    if result:
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_create_post(request):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    result = api.create_post(token, data.get('title', ''), data.get('content', ''), data.get('category', ''))
    if result:
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_delete_post(request, post_id):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    result = api.delete_post(token, post_id)
    if result:
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


def ajax_check_username(request):
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'available': False})
    result = api.check_username(username)
    if result:
        return JsonResponse(result)
    return JsonResponse({'available': False})


# ---------------------------------------------------------------------------
# ADMIN PANEL
# ---------------------------------------------------------------------------

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == 'admin' and password == 'admin123':
            request.session['is_admin'] = True
            request.session['admin_user'] = 'admin'
            return redirect('web:admin_dashboard')
        return render(request, 'admin_panel/login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    request.session.pop('is_admin', None)
    request.session.pop('admin_user', None)
    return redirect('web:admin_login')


def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    stats = api.admin_get_stats(token) or {}
    return render(request, 'admin_panel/dashboard.html', {
        'is_admin': True,
        'stats': stats,
        'active_page': 'dashboard',
    })


def admin_users(request):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    users = api.admin_get_users(token) or []
    if not isinstance(users, list):
        users = []
    search = request.GET.get('q', '').strip()
    if search:
        users = [u for u in users if search.lower() in (u.get('username', '') + u.get('email', '') + u.get('display_name', '')).lower()]
    return render(request, 'admin_panel/users.html', {
        'is_admin': True,
        'users': users,
        'search': search,
        'active_page': 'users',
    })


def admin_user_detail(request, user_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    if request.method == 'POST':
        if request.POST.get('_method') == 'delete':
            api.admin_delete_user(token, user_id)
            return redirect('web:admin_users')
        data = {}
        for field in ['username', 'email', 'display_name', 'gender', 'class_level', 'subjects', 'pradesh', 'district', 'school']:
            val = request.POST.get(field, '').strip()
            if val:
                data[field] = val
        data['isLocked'] = request.POST.get('is_locked') == 'on'
        result = api.admin_update_user(token, user_id, data)
        if result:
            user_data = result
        else:
            user_data = api.admin_get_user(token, user_id) or {}
    else:
        user_data = api.admin_get_user(token, user_id) or {}
    return render(request, 'admin_panel/user_detail.html', {
        'is_admin': True,
        'user_detail': user_data,
        'active_page': 'users',
    })


def admin_resources(request):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'subject': request.POST.get('subject', '').strip(),
            'grade_level': request.POST.get('grade_level', '').strip(),
            'type': request.POST.get('type', '').strip(),
            'file_url': request.POST.get('file_url', '').strip(),
            'thumbnail_url': request.POST.get('thumbnail_url', '').strip(),
            'file_size': int(request.POST.get('file_size', '0')),
        }
        result = api.admin_create_resource(token, data)
        if not result:
            pass
    resources = api.admin_get_resources(token) or []
    if not isinstance(resources, list):
        resources = []
    search = request.GET.get('q', '').strip()
    if search:
        resources = [r for r in resources if search.lower() in r.get('title', '').lower()]
    return render(request, 'admin_panel/resources.html', {
        'is_admin': True,
        'resources': resources,
        'search': search,
        'active_page': 'resources',
    })


def admin_resource_edit(request, resource_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    if request.method == 'POST':
        data = {}
        for field in ['title', 'description', 'subject', 'grade_level', 'type', 'file_url', 'thumbnail_url']:
            val = request.POST.get(field, '').strip()
            if val:
                data[field] = val
        data['view_count'] = int(request.POST.get('view_count', '0'))
        result = api.admin_update_resource(token, resource_id, data)
        if result:
            return redirect('web:admin_resources')
    resources = api.admin_get_resources(token) or []
    resource = None
    if isinstance(resources, list):
        for r in resources:
            if r.get('id') == resource_id:
                resource = r
                break
    return render(request, 'admin_panel/resource_edit.html', {
        'is_admin': True,
        'resource': resource,
        'active_page': 'resources',
    })


def admin_resource_delete(request, resource_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    api.admin_delete_resource(token, resource_id)
    return redirect('web:admin_resources')


def admin_posts(request):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    posts = api.admin_get_posts(token) or []
    if not isinstance(posts, list):
        posts = []
    search = request.GET.get('q', '').strip()
    if search:
        posts = [p for p in posts if search.lower() in p.get('title', '').lower() or search.lower() in p.get('content', '').lower()]
    return render(request, 'admin_panel/posts.html', {
        'is_admin': True,
        'posts': posts,
        'search': search,
        'active_page': 'posts',
    })


def admin_post_detail(request, post_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    posts = api.admin_get_posts(token) or []
    post = None
    if isinstance(posts, list):
        for p in posts:
            if p.get('id') == post_id:
                post = p
                break
    replies = api.admin_get_replies(token, post_id) or []
    if not isinstance(replies, list):
        replies = []
    return render(request, 'admin_panel/post_detail.html', {
        'is_admin': True,
        'post': post,
        'replies': replies,
        'active_page': 'posts',
    })


def admin_post_delete(request, post_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    api.admin_delete_post(token, post_id)
    return redirect('web:admin_posts')


def admin_reply_delete(request, reply_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    api.admin_delete_reply(token, reply_id)
    return redirect('web:admin_posts')