import json
import logging
import time
import uuid

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, Http404, HttpResponse

from api.models import User, Resource, Post, PostLike, Reply, ReplyLike, Follow, UserPhoto, EditHistory
from api.serializers import UserSerializer
from . import api_client as api

logger = logging.getLogger(__name__)

ADMIN_TOKEN = getattr(settings, 'ADMIN_TOKEN', 'nebians-admin-2024-secure-token')
ADMIN_USERNAME = getattr(settings, 'ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = getattr(settings, 'ADMIN_PASSWORD', 'admin123')


def _serialize_resource(r):
    return {
        'id': r.id, 'title': r.title, 'description': r.description or '',
        'subject': r.subject, 'gradeLevel': r.grade_level, 'grade_level': r.grade_level,
        'type': r.type, 'fileUrl': r.file_url, 'file_url': r.file_url,
        'thumbnailUrl': r.thumbnail_url, 'thumbnail_url': r.thumbnail_url,
        'fileSize': r.file_size, 'file_size': r.file_size,
        'addedAt': r.added_at, 'added_at': r.added_at, 'viewCount': r.view_count, 'view_count': r.view_count,
    }


def _serialize_posts(posts_qs, user_id=None):
    posts = list(posts_qs)
    liked_ids = set()
    followed_author_ids = set()
    if user_id and posts:
        liked_ids = set(PostLike.objects.filter(
            post_id__in=[p.id for p in posts], user_id=user_id
        ).values_list('post_id', flat=True))
        author_ids = set(p.user_id for p in posts if p.user_id != user_id)
        if author_ids:
            followed_author_ids = set(Follow.objects.filter(
                follower_id=user_id, following_id__in=author_ids
            ).values_list('following_id', flat=True))
    result = []
    for p in posts:
        result.append({
            'id': p.id, 'title': p.title, 'content': p.content, 'category': p.category,
            'authorName': p.user.username, 'authorPhotoUrl': p.user.photo_url,
            'authorBadge': getattr(p.user, 'badge', None),
            'authorId': p.user_id, 'thumbsUpCount': p.thumbs_up_count, 'thumbs_up_count': p.thumbs_up_count,
            'replyCount': p.reply_count, 'reply_count': p.reply_count,
            'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
            'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
            'isThumbedUp': p.id in liked_ids,
            'isFollowingAuthor': p.user_id in followed_author_ids,
        })
    return result


def _serialize_post(p, user_id=None):
    is_thumbed_up = False
    is_following_author = False
    if user_id:
        is_thumbed_up = PostLike.objects.filter(post_id=p.id, user_id=user_id).exists()
        if user_id != p.user_id:
            is_following_author = Follow.objects.filter(follower_id=user_id, following_id=p.user_id).exists()
    return {
        'id': p.id, 'title': p.title, 'content': p.content, 'category': p.category,
        'authorName': p.user.username, 'authorPhotoUrl': p.user.photo_url,
        'authorBadge': getattr(p.user, 'badge', None),
        'authorId': p.user_id, 'thumbsUpCount': p.thumbs_up_count, 'thumbs_up_count': p.thumbs_up_count,
        'replyCount': p.reply_count, 'reply_count': p.reply_count,
        'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
        'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
        'isThumbedUp': is_thumbed_up, 'isFollowingAuthor': is_following_author,
    }


def _serialize_replies(replies_qs, user_id=None):
    replies = list(replies_qs)
    liked_ids = set()
    followed_author_ids = set()
    if user_id and replies:
        liked_ids = set(ReplyLike.objects.filter(
            reply_id__in=[r.id for r in replies], user_id=user_id
        ).values_list('reply_id', flat=True))
        author_ids = set(r.user_id for r in replies if r.user_id != user_id)
        if author_ids:
            followed_author_ids = set(Follow.objects.filter(
                follower_id=user_id, following_id__in=author_ids
            ).values_list('following_id', flat=True))
    result = []
    for r in replies:
        result.append({
            'id': r.id, 'postId': r.post_id, 'parentReplyId': r.parent_reply_id,
            'content': r.content, 'authorName': r.user.username,
            'authorPhotoUrl': r.user.photo_url, 'authorId': r.user_id,
            'thumbsUpCount': r.thumbs_up_count, 'createdAt': r.created_at,
            'isEdited': r.is_edited, 'editedAt': r.edited_at,
            'isThumbedUp': r.id in liked_ids,
            'isFollowed': r.user_id in followed_author_ids,
        })
    return result


def _serialize_reply(r, user_id=None):
    is_thumbed_up = False
    if user_id:
        is_thumbed_up = ReplyLike.objects.filter(reply_id=r.id, user_id=user_id).exists()
    return {
        'id': r.id, 'postId': r.post_id, 'parentReplyId': r.parent_reply_id,
        'content': r.content, 'authorName': r.user.username,
        'authorPhotoUrl': r.user.photo_url, 'authorId': r.user_id,
        'thumbsUpCount': r.thumbs_up_count, 'createdAt': r.created_at,
        'isEdited': r.is_edited, 'editedAt': r.edited_at,
        'isThumbedUp': is_thumbed_up,
    }


def _get_user_id(request):
    token = _get_valid_token(request)
    if not token:
        return None
    cache_key = f'user_id_{token}'
    user_id = cache.get(cache_key)
    if user_id is None:
        try:
            user_id = User.objects.get(auth_token=token).id
            cache.set(cache_key, user_id, 300)
        except User.DoesNotExist:
            api.clear_session_auth(request)
            return None
    return user_id


def _get_valid_token(request):
    token = api.get_session_token(request)
    if not token:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
    if not token:
        return None
    try:
        User.objects.get(auth_token=token)
    except User.DoesNotExist:
        api.clear_session_auth(request)
        return None
    return token


def _ctx(request, **extra):
    token = api.get_session_token(request)
    user = api.get_session_user(request)
    logger.info("Session _ctx: token=%s, user=%s, session_keys=%s", token, user, list(request.session.keys()) if hasattr(request, 'session') else [])
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
    if token:
        user_data = api.get_session_user(request)
        if user_data and (not user_data.get('display_name') or not user_data.get('gender') or not user_data.get('class_level')):
            return redirect('web:edit_profile')
    user_id = _get_user_id(request)
    resources = cache.get('home_resources')
    if resources is None:
        resources = [_serialize_resource(r) for r in Resource.objects.all()[:50]]
        cache.set('home_resources', resources, 120)
    posts = cache.get('home_posts')
    if posts is None:
        posts_qs = Post.objects.select_related('user').order_by('-created_at')[:10]
        posts = _serialize_posts(posts_qs, user_id)
        cache.set('home_posts', posts, 60)
    elif user_id:
        liked_ids = set(PostLike.objects.filter(
            post_id__in=[p['id'] for p in posts], user_id=user_id
        ).values_list('post_id', flat=True))
        for p in posts:
            p['isThumbedUp'] = p['id'] in liked_ids
    recent = resources[:10]
    popular = sorted(resources, key=lambda r: r.get('view_count', 0), reverse=True)[:10]
    recent_posts = posts[:5]
    subjects = []
    seen = set()
    for r in resources:
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
    user_id = _get_user_id(request)
    subject = request.GET.get('subject', '')
    grade = request.GET.get('grade', '')
    rtype = request.GET.get('type', '')
    qs = Resource.objects.all()
    if subject:
        qs = qs.filter(subject=subject)
    if grade:
        qs = qs.filter(grade_level=grade)
    if rtype:
        qs = qs.filter(type=rtype)
    filtered = [_serialize_resource(r) for r in qs]
    all_resources = cache.get('library_all_resources')
    if all_resources is None:
        all_resources = [_serialize_resource(r) for r in Resource.objects.all()]
        cache.set('library_all_resources', all_resources, 180)
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
    user_id = _get_user_id(request)
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        qs = Resource.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__icontains=query)
        )[:50]
        results = [_serialize_resource(r) for r in qs]
    return render(request, 'web/search.html', _ctx(request, query=query, results=results))


def format_score(score):
    if score >= 1000:
        return f"{score/1000:.1f}k".replace(".0k", "k")
    return str(score)

def get_user_level_title(score):
    if score >= 2000:
        return "Level 5 Scholar"
    elif score >= 1000:
        return "Level 4 Tutor"
    elif score >= 500:
        return "Level 3 Helper"
    elif score >= 100:
        return "Level 2 Guide"
    else:
        return "Level 1 Novice"

def _build_local_stats(user):
    post_count = Post.objects.filter(user=user).count()
    reply_count = Reply.objects.filter(user=user).count()
    likes_given = (PostLike.objects.filter(user=user).count() +
                   ReplyLike.objects.filter(user=user).count())
    likes_received_posts = PostLike.objects.filter(post__user=user).count()
    likes_received_replies = ReplyLike.objects.filter(reply__user=user).count()
    likes_received = likes_received_posts + likes_received_replies
    
    contribution_score = (post_count * 3) + (reply_count * 2) + likes_given + (likes_received * 2)
    return {
        'post_count': post_count,
        'reply_count': reply_count,
        'likes_given': likes_given,
        'likes_received': likes_received,
        'contribution_score': contribution_score,
    }

def forum(request):
    user_id = _get_user_id(request)
    category = request.GET.get('category', '')
    qs = Post.objects.select_related('user').order_by('-created_at')
    if category:
        qs = qs.filter(category__iexact=category)
    posts = _serialize_posts(qs, user_id)

    all_posts = cache.get('forum_all_posts')
    if all_posts is None:
        all_posts_qs = Post.objects.select_related('user').order_by('-created_at')
        all_posts = _serialize_posts(all_posts_qs)
        cache.set('forum_all_posts', all_posts, 120)

    category_counts = dict(
        Post.objects.values('category').annotate(cnt=Count('id')).values_list('category', 'cnt')
    )
    standard_categories = ['General', 'Science', 'Math', 'Exam Prep', 'Entrance Exams']
    categories_data = []
    for name in standard_categories:
        count = category_counts.get(name, 0)
        categories_data.append({
            'name': name,
            'count': count,
            'formatted_count': format_score(count),
        })
    for cat, cnt in category_counts.items():
        if cat not in standard_categories:
            categories_data.append({
                'name': cat,
                'count': cnt,
                'formatted_count': format_score(cnt),
            })
    categories_data = sorted(categories_data, key=lambda c: (-c['count'], c['name']))

    contributor_data = cache.get('forum_contributors')
    if contributor_data is None:
        all_users = User.objects.all()
        contributors = []
        for u in all_users:
            stats = _build_local_stats(u)
            score = stats.get('contribution_score', 0)
            contributors.append({
                'username': u.username,
                'display_name': u.display_name or u.username,
                'photo_url': u.photo_url,
                'score': score,
                'formatted_score': format_score(score),
                'level': get_user_level_title(score),
            })
        contributors = sorted(contributors, key=lambda c: c['score'], reverse=True)
        contributor_data = contributors[:10]
        cache.set('forum_contributors', contributor_data, 120)

    top_contributors = contributor_data[:3]

    sidebar_categories = categories_data[:5]
    has_more_categories = len(categories_data) > 5

    return render(request, 'web/forum.html', _ctx(request,
        posts=posts,
        categories_data=sidebar_categories,
        has_more_categories=has_more_categories,
        top_contributors=top_contributors,
        all_contributors=contributor_data,
        current_category=category,
    ))


def forum_categories(request):
    category_counts = dict(
        Post.objects.values('category').annotate(cnt=Count('id')).values_list('category', 'cnt')
    )
    standard_categories = ['General', 'Science', 'Math', 'Exam Prep', 'Entrance Exams']
    categories_data = []
    for name in standard_categories:
        count = category_counts.get(name, 0)
        categories_data.append({
            'name': name,
            'count': count,
            'formatted_count': format_score(count),
        })
    for cat, cnt in category_counts.items():
        if cat not in standard_categories:
            categories_data.append({
                'name': cat,
                'count': cnt,
                'formatted_count': format_score(cnt),
            })
    categories_data = sorted(categories_data, key=lambda c: (-c['count'], c['name']))
    return render(request, 'web/forum_categories.html', _ctx(request,
        categories_data=categories_data
    ))


def leaderboard(request):
    contributor_data = cache.get('forum_contributors')
    if contributor_data is None:
        all_users = User.objects.all()
        contributors = []
        for u in all_users:
            stats = _build_local_stats(u)
            score = stats.get('contribution_score', 0)
            contributors.append({
                'username': u.username,
                'display_name': u.display_name or u.username,
                'photo_url': u.photo_url,
                'score': score,
                'formatted_score': format_score(score),
                'level': get_user_level_title(score),
            })
        contributors = sorted(contributors, key=lambda c: c['score'], reverse=True)
        contributor_data = contributors[:50]
        cache.set('forum_contributors', contributor_data, 120)
    return render(request, 'web/leaderboard.html', _ctx(request,
        contributors=contributor_data,
    ))





def forum_post(request, post_id):
    user_id = _get_user_id(request)
    try:
        post_obj = Post.objects.select_related('user').get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found")
    post = _serialize_post(post_obj, user_id)
    replies_qs = Reply.objects.select_related('user').filter(post_id=post_id).order_by('created_at')
    replies = _serialize_replies(replies_qs, user_id)
    is_following = False
    is_owner = False
    if user_id:
        is_owner = (user_id == post_obj.user_id)
        if not is_owner:
            is_following = Follow.objects.filter(follower_id=user_id, following_id=post_obj.user_id).exists()
    return render(request, 'web/forum_post.html', _ctx(request, post=post, replies=replies, post_id=post_id, is_owner=is_owner, is_following=is_following, post_author_id=post_obj.user_id))


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
                _clear_page_cache()
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
            _clear_page_cache()
            return redirect('web:forum_post', post_id=post_id)
    return render(request, 'web/reply.html', _ctx(request, post=post, post_id=post_id))


def reader(request, resource_id):
    try:
        resource_obj = Resource.objects.get(id=resource_id)
    except Resource.DoesNotExist:
        raise Http404("Resource not found")
    resource = _serialize_resource(resource_obj)
    return render(request, 'web/reader.html', _ctx(request, resource=resource, resource_id=resource_id))


def profile(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'display_name': profile_user.display_name,
        'dob': profile_user.dob,
        'gender': profile_user.gender,
        'class_level': profile_user.class_level,
        'class': profile_user.class_level,
        'subjects': profile_user.subjects,
        'pradesh': profile_user.pradesh,
        'district': profile_user.district,
        'school': profile_user.school,
        'bio': profile_user.bio,
        'is_locked': 1 if profile_user.is_locked else 0,
        'created_at': profile_user.created_at,
    }

    stats = _build_local_stats(profile_user)
    follower_count = Follow.objects.filter(following_id=profile_user.id).count()
    following_count = Follow.objects.filter(follower_id=profile_user.id).count()
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = False
    stats['is_self'] = False
    if user_id:
        stats['is_self'] = (user_id == profile_user.id)
        if not stats['is_self']:
            stats['is_following'] = Follow.objects.filter(follower_id=user_id, following_id=profile_user.id).exists()

    user_posts_qs = Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    user_photos = []
    if user_id and user_id == profile_user.id:
        user_photos = list(UserPhoto.objects.filter(user_id=profile_user.id).values('id', 'url', 'uploaded_at', 'is_current'))

    return render(request, 'web/profile.html', _ctx(request,
        profile_user=profile_data,
        username=username,
        stats=stats,
        user_photos=user_photos,
        user_posts=user_posts,
    ))


def profile_achievements(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'display_name': profile_user.display_name,
        'dob': profile_user.dob,
        'gender': profile_user.gender,
        'class_level': profile_user.class_level,
        'class': profile_user.class_level,
        'subjects': profile_user.subjects,
        'pradesh': profile_user.pradesh,
        'district': profile_user.district,
        'school': profile_user.school,
        'bio': profile_user.bio,
        'is_locked': 1 if profile_user.is_locked else 0,
        'created_at': profile_user.created_at,
    }

    stats = _build_local_stats(profile_user)
    follower_count = Follow.objects.filter(following_id=profile_user.id).count()
    following_count = Follow.objects.filter(follower_id=profile_user.id).count()
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = False
    stats['is_self'] = False
    if user_id:
        stats['is_self'] = (user_id == profile_user.id)
        if not stats['is_self']:
            stats['is_following'] = Follow.objects.filter(follower_id=user_id, following_id=profile_user.id).exists()

    return render(request, 'web/achievements.html', _ctx(request,
        profile_user=profile_data,
        username=username,
        stats=stats,
    ))


def ajax_profile_activity(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        offset = 0
        limit = 10

    user_posts_qs = Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[offset:offset+limit]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    total_count = Post.objects.filter(user_id=profile_user.id).count()
    has_more = (offset + len(user_posts)) < total_count

    return JsonResponse({
        'posts': user_posts,
        'has_more': has_more,
        'total_count': total_count
    })




def edit_profile(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    user = api.get_session_user(request)
    if not user:
        return redirect('web:login')
    try:
        db_user = User.objects.get(id=user.get('id'))
    except User.DoesNotExist:
        return redirect('web:login')
    has_password = bool(db_user.password_hash)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        dob = request.POST.get('dob', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        gender = request.POST.get('gender', '').strip()
        class_level = request.POST.get('class_level', '').strip()
        if not username or not dob:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Username and Date of Birth are required.'))
        if not display_name:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Display Name is required.'))
        if not gender:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Gender is required.'))
        if not class_level:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Class is required.'))
        conflict = User.objects.filter(username__iexact=username).exclude(pk=db_user.id).exists()
        if conflict:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Username already taken.'))
        db_user.username = username
        db_user.email = request.POST.get('email', '').strip() or db_user.email or ''
        db_user.display_name = display_name or db_user.display_name or ''
        db_user.dob = dob
        db_user.gender = gender or db_user.gender or ''
        db_user.class_level = class_level or db_user.class_level or ''
        db_user.subjects = request.POST.get('subjects', '') or db_user.subjects or ''
        db_user.pradesh = request.POST.get('pradesh', '') or db_user.pradesh or ''
        db_user.district = request.POST.get('district', '').strip() or db_user.district or ''
        db_user.school = request.POST.get('school', '').strip() or db_user.school or ''
        db_user.bio = request.POST.get('bio', '').strip()
        db_user.is_locked = request.POST.get('is_locked') == 'on'
        db_user.save()
        _clear_page_cache()
        updated_data = {
            'id': db_user.id,
            'username': db_user.username,
            'email': db_user.email,
            'photo_url': db_user.photo_url,
            'display_name': db_user.display_name,
            'dob': db_user.dob,
            'gender': db_user.gender,
            'class_level': db_user.class_level,
            'class': db_user.class_level,
            'subjects': db_user.subjects,
            'pradesh': db_user.pradesh,
            'district': db_user.district,
            'school': db_user.school,
            'bio': db_user.bio,
            'is_locked': 1 if db_user.is_locked else 0,
            'created_at': db_user.created_at,
        }
        api.set_session_auth(request, token, updated_data)
        return redirect('web:home')
    ctx = _ctx(request)
    ctx['error'] = ctx.get('error', None)
    profile_incomplete = not db_user.display_name or not db_user.gender or not db_user.class_level
    return render(request, 'web/edit_profile.html', _ctx(request, error=ctx.get('error', None), has_password=has_password, profile_incomplete=profile_incomplete))


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

def login_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    return render(request, 'web/login.html', _ctx(request,
        google_client_id=settings.GOOGLE_CLIENT_ID,
    ))


@require_POST
def google_auth(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Check for email auth token (from email login flow)
    email_auth_token = data.get('emailAuthToken')
    if email_auth_token:
        try:
            user = User.objects.get(auth_token=email_auth_token)
            token = user.auth_token
            user_data = _normalize_user_data(UserSerializer(user).data)
            user_data['isNewUser'] = data.get('emailUser', {}).get('isNewUser', False)
            profile_incomplete = not user.display_name or not user.gender or not user.class_level
            user_data['profileIncomplete'] = data.get('emailUser', {}).get('profileIncomplete', profile_incomplete)
            api.set_session_auth(request, token, user_data)
            return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': user_data.get('isNewUser', False), 'profileIncomplete': user_data.get('profileIncomplete', False)})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid auth token'}, status=401)

    id_token = data.get('idToken', '')
    if not id_token:
        logger.warning('google_auth: no idToken in request body. Keys: %s', list(data.keys()))
        return JsonResponse({'error': 'idToken is required'}, status=400)

    logger.info('google_auth: verifying token (length=%d, prefix=%s)', len(id_token), id_token[:20] if id_token else 'empty')
    result = api.auth_google(id_token)
    if not result or result.get('status') != 'success':
        logger.warning('google_auth: token verification failed. Result: %s', result)
        return JsonResponse({'error': result.get('error', 'Authentication failed') if result else 'Authentication failed'}, status=401)
    token = result.get('authToken', '')
    user = result.get('user', {})
    user['isNewUser'] = result.get('isNewUser', False)
    user = _normalize_user_data(user)
    api.set_session_auth(request, token, user)
    logger.info('google_auth: success for user=%s', user.get('username', user.get('email', 'unknown')))
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


def email_signup_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    return render(request, 'web/email_signup.html', _ctx(request))


def email_login_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    return render(request, 'web/email_login.html', _ctx(request))


def email_verify_page(request):
    return render(request, 'web/email_verify.html', _ctx(request))


def email_forgot_page(request):
    return render(request, 'web/email_forgot.html', _ctx(request))


def password_page(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    user = api.get_session_user(request)
    has_password = False
    if user:
        try:
            db_user = User.objects.get(id=user.get('id'))
            has_password = bool(db_user.password_hash)
        except User.DoesNotExist:
            pass
    return render(request, 'web/password_set.html', _ctx(request, has_password=has_password))


def change_password_page(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    return render(request, 'web/password_change.html', _ctx(request))


def privacy_policy(request):
    return render(request, 'web/legal/privacy.html', _ctx(request))


def terms_of_service(request):
    return render(request, 'web/legal/terms.html', _ctx(request))


# ---------------------------------------------------------------------------
# AJAX ENDPOINTS
# ---------------------------------------------------------------------------

def _clear_page_cache():
    cache.delete_many([
        'home_resources', 'home_posts', 'library_all_resources',
        'forum_all_posts', 'forum_contributors',
    ])


@require_POST
def ajax_like_post(request, post_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = api.like_post(token, post_id)
    if result:
        cache.delete_many(['home_posts', 'forum_all_posts'])
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_like_reply(request, reply_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = api.like_reply(token, reply_id)
    if result:
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_create_reply(request, post_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
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
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_create_post(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    result = api.create_post(token, data.get('title', ''), data.get('content', ''), data.get('category', ''))
    if result:
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_delete_post(request, post_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        post = Post.objects.get(pk=post_id)
        if post.user_id != user_id:
            return JsonResponse({'error': 'Forbidden'}, status=403)
        post.delete()
        _clear_page_cache()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)


@require_POST
def ajax_edit_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    now = int(time.time() * 1000)
    if 'title' in data:
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='post', target_id=post.id,
            field='title', old_value=post.title, new_value=data['title'].strip(),
            edited_by_id=user_id, edited_at=now
        )
        post.title = data['title'].strip()
    if 'content' in data:
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='post', target_id=post.id,
            field='content', old_value=post.content, new_value=data['content'].strip(),
            edited_by_id=user_id, edited_at=now
        )
        post.content = data['content'].strip()
    if 'category' in data:
        EditHistory.objects.create(
            id=str(uuid.uuid4()), target_type='post', target_id=post.id,
            field='category', old_value=post.category, new_value=data['category'].strip(),
            edited_by_id=user_id, edited_at=now
        )
        post.category = data['category'].strip()
    post.is_edited = True
    post.edited_at = now
    post.save()
    _clear_page_cache()
    return JsonResponse(_serialize_post(post, user_id))


@require_POST
def ajax_archive_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    post.is_archived = not post.is_archived
    post.save(update_fields=['is_archived'])
    _clear_page_cache()
    return JsonResponse({'success': True, 'isArchived': post.is_archived})


@require_POST
def ajax_edit_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    now = int(time.time() * 1000)
    EditHistory.objects.create(
        id=str(uuid.uuid4()), target_type='reply', target_id=reply.id,
        field='content', old_value=reply.content, new_value=content,
        edited_by_id=user_id, edited_at=now
    )
    reply.content = content
    reply.is_edited = True
    reply.edited_at = now
    reply.save()
    _clear_page_cache()
    return JsonResponse(_serialize_reply(reply, user_id))


@require_POST
def ajax_delete_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    post = reply.post
    reply.delete()
    post.reply_count = max(0, post.reply_count - 1)
    post.save(update_fields=['reply_count'])
    _clear_page_cache()
    return JsonResponse({'success': True})


def ajax_edit_history(request, target_type, target_id):
    if target_type not in ('post', 'reply'):
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    entries = EditHistory.objects.filter(target_type=target_type, target_id=target_id).select_related('edited_by')
    data = []
    for e in entries:
        data.append({
            'id': e.id, 'field': e.field, 'oldValue': e.old_value, 'newValue': e.new_value,
            'editedByUsername': e.edited_by.username, 'editedByPhotoUrl': e.edited_by.photo_url or '',
            'editedAt': e.edited_at,
        })
    return JsonResponse(data, safe=False)


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
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = api.follow_user(token, user_id)
    if result:
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@csrf_exempt
def ajax_user_photos(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)

    from api.models import UserPhoto
    try:
        current_user = User.objects.get(auth_token=token)
    except User.DoesNotExist:
        api.clear_session_auth(request)
        return JsonResponse({'error': 'Please log in again.'}, status=401)

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
def ajax_set_password(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    password = data.get('password', '')
    if not password or len(password) < 8:
        return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
    result = api._api_call('POST', '/auth/set-password/', token=token, data={'password': password})
    if result and result.get('status') == 'success':
        _clear_page_cache()
        user_data = api.get_session_user(request)
        if user_data:
            user_data['hasPassword'] = True
            api.set_session_auth(request, token, user_data)
        return JsonResponse({'status': 'success', 'message': 'Password set successfully'})
    return JsonResponse({'error': (result or {}).get('error', 'Failed to set password')}, status=400)


@require_POST
def ajax_change_password(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    current_password = data.get('currentPassword', '')
    new_password = data.get('newPassword', '')
    if not current_password or not new_password:
        return JsonResponse({'error': 'Current password and new password are required'}, status=400)
    result = api._api_call('POST', '/auth/change-password/', token=token, data={'currentPassword': current_password, 'newPassword': new_password})
    if result and result.get('status') == 'success':
        _clear_page_cache()
        new_token = result.get('authToken', token)
        user_data = api.get_session_user(request)
        if user_data:
            api.set_session_auth(request, new_token, user_data)
        return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})
    return JsonResponse({'error': (result or {}).get('error', 'Failed to change password')}, status=400)






@require_POST
def ajax_activate_photo(request, photo_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
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
    from api.models import Resource, Post, User
    from django.utils import timezone

    base = 'https://nebians.consica.com.np'
    now = timezone.now().isoformat()
    urls = [
        {'loc': f'{base}/', 'changefreq': 'daily', 'priority': '1.0', 'lastmod': now},
        {'loc': f'{base}/library/', 'changefreq': 'daily', 'priority': '0.8', 'lastmod': now},
        {'loc': f'{base}/forum/', 'changefreq': 'daily', 'priority': '0.8', 'lastmod': now},
        {'loc': f'{base}/search/', 'changefreq': 'weekly', 'priority': '0.5', 'lastmod': now},
    ]

    for r in Resource.objects.all():
        lastmod = r.updated_at.isoformat() if hasattr(r, 'updated_at') and r.updated_at else now
        urls.append({
            'loc': f'{base}/reader/{r.id}/',
            'changefreq': 'weekly',
            'priority': '0.6',
            'lastmod': lastmod,
        })

    for p in Post.objects.filter(is_archived=False).select_related('user')[:500]:
        lastmod = p.created_at.isoformat() if hasattr(p, 'created_at') and p.created_at else now
        urls.append({
            'loc': f'{base}/forum/post/{p.id}/',
            'changefreq': 'daily',
            'priority': '0.7',
            'lastmod': lastmod,
        })

    for u in User.objects.filter(is_locked=False)[:500]:
        if u.username:
            urls.append({
                'loc': f'{base}/profile/{u.username}/',
                'changefreq': 'weekly',
                'priority': '0.4',
                'lastmod': now,
            })

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml_content += '  <url>\n'
        xml_content += f"    <loc>{u['loc']}</loc>\n"
        xml_content += f"    <lastmod>{u['lastmod']}</lastmod>\n"
        xml_content += f"    <changefreq>{u['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{u['priority']}</priority>\n"
        xml_content += '  </url>\n'
    xml_content += '</urlset>\n'

    return HttpResponse(xml_content, content_type='application/xml')


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /admin-django/',
        'Disallow: /api/',
        'Disallow: /ajax/',
        'Disallow: /auth/',
        'Disallow: /login/',
        'Disallow: /profile/edit/',
        '',
        'Sitemap: https://nebians.consica.com.np/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def custom_404(request, exception):
    return render(request, '404.html', _ctx(request), status=404)


def custom_500(request):
    return render(request, '500.html', _ctx(request), status=500)