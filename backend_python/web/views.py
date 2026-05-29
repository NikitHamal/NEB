import json
import logging

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, Http404, HttpResponse

from . import api_client as api

logger = logging.getLogger(__name__)

ADMIN_TOKEN = getattr(settings, 'ADMIN_TOKEN', 'nebians-admin-2024-secure-token')
ADMIN_USERNAME = getattr(settings, 'ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = getattr(settings, 'ADMIN_PASSWORD', 'admin123')


def _ctx(request, **extra):
    token = api.get_session_token(request)
    user = api.get_session_user(request)
    if user:
        user = _normalize_user_data(user)
    dark_mode = request.session.get('theme') == 'dark'
    ctx = {
        'is_authenticated': bool(token),
        'user': user,
        'auth_token': token,
        'dark_mode': dark_mode,
    }
    ctx.update(extra)
    return ctx


def _admin_token(request):
    return ADMIN_TOKEN


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
    subject = request.GET.get('subject', '')
    grade = request.GET.get('grade', '')
    rtype = request.GET.get('type', '')
    params = {}
    if subject:
        params['subject'] = subject
    if grade:
        params['grade'] = grade
    if rtype:
        params['type'] = rtype
    filtered = api.get_resources(token=token, params=params) or []
    if not isinstance(filtered, list):
        filtered = []
    all_resources = api.get_resources(token=token) or []
    if not isinstance(all_resources, list):
        all_resources = []
    all_subjects = sorted(set(r.get('subject', '') for r in all_resources if r.get('subject')))
    all_grades = sorted(set(r.get('grade_level', '') for r in all_resources if r.get('grade_level')))
    all_types = sorted(set(r.get('type', '') for r in all_resources if r.get('type')))
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
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        search_data = api.search_all(token=token, query=query)
        if search_data and isinstance(search_data, dict):
            results = search_data.get('resources', [])
        elif not search_data:
            resources = api.get_resources(token=token) or []
            if isinstance(resources, list):
                ql = query.lower()
                results = [r for r in resources if ql in r.get('title', '').lower() or ql in r.get('description', '').lower() or ql in r.get('subject', '').lower()]
    return render(request, 'web/search.html', _ctx(request, query=query, results=results))


def forum(request):
    token = api.get_session_token(request)
    category = request.GET.get('category', '')
    params = {}
    if category:
        params['category'] = category
    posts = api.get_posts(token=token, params=params) or []
    if not isinstance(posts, list):
        posts = []
    all_posts = api.get_posts(token=token) or []
    if not isinstance(all_posts, list):
        all_posts = []
    categories = sorted(set(p.get('category', '') for p in all_posts if p.get('category')))
    return render(request, 'web/forum.html', _ctx(request,
        posts=posts,
        categories=categories,
        current_category=category,
    ))


def forum_post(request, post_id):
    token = api.get_session_token(request)
    post = api.get_post(token, post_id)
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
    post = api.get_post(token, post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        parent_reply_id = request.POST.get('parent_reply_id', '') or None
        if content:
            api.create_reply(token, post_id, content, parent_reply_id)
            return redirect('web:forum_post', post_id=post_id)
    return render(request, 'web/reply.html', _ctx(request, post=post, post_id=post_id))


def reader(request, resource_id):
    token = api.get_session_token(request)
    resource = api.get_resource(token, resource_id)
    return render(request, 'web/reader.html', _ctx(request, resource=resource, resource_id=resource_id))


def profile(request, username):
    token = api.get_session_token(request)
    profile_data = api.get_profile(token, username)
    if not profile_data or 'error' in profile_data:
        raise Http404("User not found")
    
    # Get profile stats (followers, following, contributions, is_following, is_self)
    stats = api.get_profile_stats(token, username) or {}
    
    # Get user photo history if the profile belongs to the signed-in user
    user_photos = []
    if token and stats.get('is_self'):
        user_photos = api.get_user_photos(token) or []
        
    return render(request, 'web/profile.html', _ctx(request, 
        profile_user=profile_data, 
        username=username,
        stats=stats,
        user_photos=user_photos
    ))



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
    user = _normalize_user_data(user)
    api.set_session_auth(request, token, user)
    return JsonResponse({'status': 'success', 'user': user, 'isNewUser': result.get('isNewUser', False)})


def _normalize_user_data(user):
    if not isinstance(user, dict):
        return user
    mapping = {
        'displayName': 'display_name',
        'photoUrl': 'photo_url',
        'isNewUser': 'is_new_user',
    }
    for old_key, new_key in mapping.items():
        if old_key in user and new_key not in user:
            user[new_key] = user[old_key]
    
    # Ensure avatar_url is populated for base.html navbar compatibility
    if 'photo_url' in user:
        user['avatar_url'] = user['photo_url']
    elif 'photoUrl' in user:
        user['avatar_url'] = user['photoUrl']
        
    return user



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


@require_POST
def ajax_set_theme(request):
    try:
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        request.session['theme'] = 'dark' if theme == 'dark' else 'light'
    except (json.JSONDecodeError, KeyError):
        pass
    return JsonResponse({'status': 'ok'})


@require_POST
def ajax_follow_user(request, user_id):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    result = api.follow_user(token, user_id)
    if result:
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@csrf_exempt
def ajax_user_photos(request):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    from api.models import User, UserPhoto
    try:
        current_user = User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        try:
            photos = UserPhoto.objects.filter(user=current_user)
            # Manual serialization to avoid DRF serializer context issues in vanilla Django views
            photos_data = []
            for photo in photos:
                photos_data.append({
                    'id': photo.id,
                    'url': photo.url,
                    'uploaded_at': photo.uploaded_at,
                    'is_current': photo.is_current,
                })
            return JsonResponse({'photos': photos_data})
        except Exception as e:
            logger.error("Failed to retrieve user photos: %s", e)
            return JsonResponse({'error': f"Failed to retrieve photos: {str(e)}"}, status=500)

    elif request.method == 'POST':
        import os
        import time
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.db import transaction

        file_obj = request.FILES.get('file')
        if file_obj:
            ext = os.path.splitext(file_obj.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                return JsonResponse({'error': 'Invalid image format. Only JPG, PNG, GIF, and WEBP are allowed.'}, status=400)

            filename = f"{current_user.id}_{int(time.time() * 1000)}{ext}"
            try:
                file_obj.seek(0)
            except Exception:
                pass
            
            try:
                path = default_storage.save(os.path.join('profile_photos', filename), ContentFile(file_obj.read()))
                url = request.build_absolute_uri(settings.MEDIA_URL + path)
            except Exception as e:
                logger.error("Failed to save uploaded file locally: %s", e)
                return JsonResponse({'error': f"Failed to save file on server (check write permissions): {str(e)}"}, status=500)
        else:
            # Fallback to URL
            url = ''
            content_type = request.META.get('CONTENT_TYPE', '')
            if 'application/json' in content_type:
                try:
                    data = json.loads(request.body)
                    url = data.get('url', '').strip()
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON request'}, status=400)
            else:
                url = request.POST.get('url', '').strip()

            if not url:
                return JsonResponse({'error': 'Either URL or file is required'}, status=400)

        try:
            with transaction.atomic():
                UserPhoto.objects.filter(user=current_user).update(is_current=False)
                photo = UserPhoto.objects.create(
                    user=current_user,
                    url=url,
                    uploaded_at=int(time.time() * 1000),
                    is_current=True,
                )
                current_user.photo_url = url
                current_user.save(update_fields=['photo_url'])
        except Exception as e:
            logger.error("Failed to save user photo database record: %s", e)
            return JsonResponse({'error': f"Database error (run migrations on live server): {str(e)}"}, status=500)

        # Update user in session
        try:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = url
                user_data['photoUrl'] = url
                api.set_session_auth(request, token, user_data)
        except Exception as e:
            logger.error("Failed to update user session avatar: %s", e)

        return JsonResponse({
            'id': photo.id,
            'url': url,
            'uploaded_at': photo.uploaded_at,
            'is_current': True
        }, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)






@require_POST
def ajax_activate_photo(request, photo_id):
    token = api.get_session_token(request)
    if not token:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    result = api.set_active_photo(token, photo_id)
    if result and result.get('success'):
        new_url = result.get('photo_url')
        if new_url:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = new_url
                user_data['photoUrl'] = new_url
                api.set_session_auth(request, token, user_data)
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)



# ---------------------------------------------------------------------------
# ADMIN PANEL
# ---------------------------------------------------------------------------

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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
    resource = api.admin_get_resource(token, resource_id) or {}
    return render(request, 'admin_panel/resource_edit.html', {
        'is_admin': True,
        'resource': resource,
        'active_page': 'resources',
    })


@require_POST
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
    post = api.admin_get_post(token, post_id)
    replies = api.admin_get_replies(token, post_id) or []
    if not isinstance(replies, list):
        replies = []
    return render(request, 'admin_panel/post_detail.html', {
        'is_admin': True,
        'post': post,
        'replies': replies,
        'active_page': 'posts',
    })


@require_POST
def admin_post_delete(request, post_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    api.admin_delete_post(token, post_id)
    return redirect('web:admin_posts')


@require_POST
def admin_reply_delete(request, reply_id):
    if not request.session.get('is_admin'):
        return redirect('web:admin_login')
    token = _admin_token(request)
    api.admin_delete_reply(token, reply_id)
    return redirect('web:admin_posts')


def sitemap_xml(request):
    """
    Generates a dynamic XML sitemap listing the homepage, library, forum,
    and all public resources and forum posts dynamically from the database.
    """
    from api.models import Resource, Post

    urls = [
        {'loc': 'https://nebians.consica.com.np/', 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': 'https://nebians.consica.com.np/library/', 'changefreq': 'daily', 'priority': '0.8'},
        {'loc': 'https://nebians.consica.com.np/forum/', 'changefreq': 'daily', 'priority': '0.8'},
        {'loc': 'https://nebians.consica.com.np/login/', 'changefreq': 'monthly', 'priority': '0.3'},
    ]

    # Add resources
    for r in Resource.objects.all():
        urls.append({
            'loc': f'https://nebians.consica.com.np/reader/{r.id}/',
            'changefreq': 'weekly',
            'priority': '0.6'
        })

    # Add posts
    for p in Post.objects.all():
        urls.append({
            'loc': f'https://nebians.consica.com.np/forum/post/{p.id}/',
            'changefreq': 'daily',
            'priority': '0.6'
        })

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml_content += '  <url>\n'
        xml_content += f"    <loc>{u['loc']}</loc>\n"
        xml_content += f"    <changefreq>{u['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{u['priority']}</priority>\n"
        xml_content += '  </url>\n'
    xml_content += '</urlset>\n'

    return HttpResponse(xml_content, content_type='application/xml')


def custom_404(request, exception):
    return render(request, '404.html', _ctx(request), status=404)


def custom_500(request):
    return render(request, '500.html', _ctx(request), status=500)