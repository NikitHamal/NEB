import json
import logging
import time
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Count, F
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, Http404, HttpResponse
from django.utils.html import escape

from api.models import User, Resource, ResourceRequest, ResourceRequestUpvote, Post, PostLike, Reply, ReplyLike, Follow, UserPhoto, EditHistory, Bookmark, Notification, Report
from api.models import ResourceLike, ResourceComment, ResourceCommentLike
from api.serializers import UserSerializer
from api.security import (
    get_user_by_auth_token, hash_auth_token, issue_auth_token, revoke_auth_token,
    save_profile_image_upload, validate_profile_photo_url,
    validate_resource_file_url, validate_and_save_resource_file,
)
from api.authentication import verify_google_token
from api import services
from api import counters as _counters
from api import notifications as _notif
from api import cleanup as _cleanup
from . import api_client as api

logger = logging.getLogger(__name__)

def _serialize_resource(r, _uploaded_by_map=None):
    source_type = r.source_type or 'admin'
    source_label = r.source_label or ''
    uploaded_by_name = ''
    uploaded_by_photo = ''
    uploaded_by_username = ''
    if r.uploaded_by_id and source_type == 'user':
        ub = None
        if _uploaded_by_map and r.uploaded_by_id in _uploaded_by_map:
            ub = _uploaded_by_map[r.uploaded_by_id]
        elif hasattr(r, 'uploaded_by') and r.uploaded_by:
            ub = r.uploaded_by
        if ub:
            uploaded_by_name = ub.display_name or ub.username
            uploaded_by_photo = ub.photo_url or ''
            uploaded_by_username = ub.username
    file_url = r.file_url or ''
    if r.file:
        file_url = r.file.url
    return {
        'id': r.id, 'title': r.title, 'description': r.description or '',
        'subject': r.subject, 'gradeLevel': r.grade_level, 'grade_level': r.grade_level,
        'faculty': r.faculty or '', 'program': r.program or '',
        'year': r.year or '', 'examType': r.exam_type or '', 'exam_type': r.exam_type or '',
        'pradesh': r.pradesh or '', 'district': r.district or '',
        'school': r.school or '',
        'tags': r.tags or '',
        'type': r.type, 'fileUrl': file_url, 'file_url': file_url,
        'thumbnailUrl': r.thumbnail_url, 'thumbnail_url': r.thumbnail_url,
        'fileSize': r.file_size, 'file_size': r.file_size,
        'addedAt': r.added_at, 'added_at': r.added_at,
        'viewCount': r.view_count, 'view_count': r.view_count,
        'likeCount': r.like_count, 'like_count': r.like_count,
        'commentCount': r.comment_count, 'comment_count': r.comment_count,
        'authorName': r.author_name, 'author_name': r.author_name,
        'sourceType': source_type, 'source_type': source_type,
        'sourceUrl': r.source_url, 'source_url': r.source_url,
        'sourceLabel': source_label, 'source_label': source_label,
        'uploadedByName': uploaded_by_name, 'uploaded_by_name': uploaded_by_name,
        'uploadedByPhoto': uploaded_by_photo, 'uploaded_by_photo': uploaded_by_photo,
        'uploadedByUsername': uploaded_by_username,
        'approvalStatus': r.approval_status, 'approval_status': r.approval_status,
    }


def _serialize_resources(resources_qs):
    resources = list(resources_qs)
    user_source_ids = [r.uploaded_by_id for r in resources if r.uploaded_by_id and (r.source_type or 'admin') == 'user']
    uploaded_by_map = {}
    if user_source_ids:
        for u in User.objects.filter(id__in=set(user_source_ids)):
            uploaded_by_map[u.id] = u
    return [_serialize_resource(r, _uploaded_by_map=uploaded_by_map) for r in resources]


def _user_badge_info(user):
    """Build badge dict for a user (verification, moderator, admin, bot, achievements)."""
    badge = {}
    if user.is_bot:
        badge['type'] = 'bot'
        badge['icon'] = 'smart_toy'
        badge['color'] = '#7C4DFF'
        badge['label'] = 'AI'
        return badge
    if user.is_admin:
        badge['type'] = 'admin'
        badge['icon'] = 'crown'
        badge['color'] = '#F59E0B'
        badge['label'] = 'Admin'
        return badge
    if user.moderator_level and user.moderator_level > 0:
        mod_levels = {
            1: {'icon': 'local_police', 'color': '#1B9AF0', 'label': 'Community Mod'},
            2: {'icon': 'shield', 'color': '#00897B', 'label': 'Senior Mod'},
            3: {'icon': 'shield_with_heart', 'color': '#7B1FA2', 'label': 'Community Lead'},
        }
        info = mod_levels.get(user.moderator_level, mod_levels[1])
        badge['type'] = 'moderator'
        badge['icon'] = info['icon']
        badge['color'] = info['color']
        badge['label'] = info['label']
        return badge
    if user.verification_level and user.verification_level > 0:
        ver_levels = {
            1: {'icon': 'verified', 'color': '#1B9AF0', 'label': 'Verified'},
            2: {'icon': 'verified', 'color': '#2E7D32', 'label': 'Expert Verified'},
            3: {'icon': 'verified', 'color': '#F59E0B', 'label': 'Premium Verified'},
            4: {'icon': 'verified', 'color': '#1a1a1a', 'label': 'Elite Verified'},
        }
        info = ver_levels.get(user.verification_level, ver_levels[1])
        badge['type'] = 'verified'
        badge['icon'] = info['icon']
        badge['color'] = info['color']
        badge['label'] = info['label']
        return badge
    return None


def _user_achievement_badges(user):
    """Parse comma-separated achievement badge keys into a list of dicts."""
    if not user.achievement_badges:
        return []
    ACHIEVEMENT_MAP = {
        'top_contributor': {'icon': 'emoji_events', 'color': '#F59E0B', 'label': 'Top Contributor'},
        'helpful': {'icon': 'volunteer_activism', 'color': '#EC407A', 'label': 'Helpful'},
        'scholar': {'icon': 'school', 'color': '#1B9AF0', 'label': 'Scholar'},
        'streak': {'icon': 'local_fire_department', 'color': '#FF6D00', 'label': 'Streak'},
        'first_post': {'icon': 'rocket_launch', 'color': '#2E7D32', 'label': 'First Post'},
        '100_likes': {'icon': 'favorite', 'color': '#E53935', 'label': '100 Likes'},
        'bookworm': {'icon': 'auto_stories', 'color': '#00897B', 'label': 'Bookworm'},
        'problem_solver': {'icon': 'lightbulb', 'color': '#F9A825', 'label': 'Problem Solver'},
    }
    result = []
    for key in user.achievement_badges.split(','):
        key = key.strip()
        if key in ACHIEVEMENT_MAP:
            info = ACHIEVEMENT_MAP[key]
            result.append({'key': key, 'icon': info['icon'], 'color': info['color'], 'label': info['label']})
    return result


def _serialize_posts(posts_qs, user_id=None):
    posts = list(posts_qs)
    liked_ids = set()
    followed_author_ids = set()
    bookmarked_ids = set()
    if user_id and posts:
        liked_ids = set(PostLike.objects.filter(
            post_id__in=[p.id for p in posts], user_id=user_id
        ).values_list('post_id', flat=True))
        author_ids = set(p.user_id for p in posts if p.user_id != user_id)
        if author_ids:
            followed_author_ids = set(Follow.objects.filter(
                follower_id=user_id, following_id__in=author_ids
            ).values_list('following_id', flat=True))
        bookmarked_ids = set(Bookmark.objects.filter(
            user_id=user_id, target_type='post',
            target_id__in=[p.id for p in posts]
        ).values_list('target_id', flat=True))
    result = []
    for p in posts:
        result.append({
            'id': p.id, 'title': p.title, 'content': p.content, 'category': p.category,
            'authorName': p.user.username, 'authorPhotoUrl': p.user.photo_url,
            'authorBadgeInfo': _user_badge_info(p.user),
            'authorAchievements': _user_achievement_badges(p.user),
            'authorIsBot': p.user.is_bot,
            'authorId': p.user_id, 'thumbsUpCount': p.thumbs_up_count, 'thumbs_up_count': p.thumbs_up_count,
            'replyCount': p.reply_count, 'reply_count': p.reply_count,
            'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
            'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
            'isThumbedUp': p.id in liked_ids,
            'isFollowingAuthor': p.user_id in followed_author_ids,
            'isBookmarked': p.id in bookmarked_ids,
        })
    return result


def _serialize_post(p, user_id=None, _liked_ids=None, _followed_ids=None, _bookmarked_ids=None):
    is_thumbed_up = False
    is_following_author = False
    is_bookmarked = False
    if user_id:
        if _liked_ids is not None:
            is_thumbed_up = p.id in _liked_ids
        else:
            is_thumbed_up = PostLike.objects.filter(post_id=p.id, user_id=user_id).exists()
        if _followed_ids is not None:
            is_following_author = p.user_id in _followed_ids
        elif user_id != p.user_id:
            is_following_author = Follow.objects.filter(follower_id=user_id, following_id=p.user_id).exists()
        if _bookmarked_ids is not None:
            is_bookmarked = p.id in _bookmarked_ids
        else:
            is_bookmarked = Bookmark.objects.filter(user_id=user_id, target_type='post', target_id=p.id).exists()
    return {
        'id': p.id, 'title': p.title, 'content': p.content, 'category': p.category,
        'authorName': p.user.username, 'authorPhotoUrl': p.user.photo_url,
        'authorBadgeInfo': _user_badge_info(p.user),
        'authorAchievements': _user_achievement_badges(p.user),
        'authorIsBot': p.user.is_bot,
        'authorId': p.user_id, 'thumbsUpCount': p.thumbs_up_count, 'thumbs_up_count': p.thumbs_up_count,
        'replyCount': p.reply_count, 'reply_count': p.reply_count,
        'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
        'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
        'isThumbedUp': is_thumbed_up, 'isFollowingAuthor': is_following_author,
        'isBookmarked': is_bookmarked,
    }


def _serialize_replies(replies_qs, user_id=None):
    replies = list(replies_qs)
    liked_ids = set()
    followed_author_ids = set()
    bookmarked_ids = set()
    if user_id and replies:
        liked_ids = set(ReplyLike.objects.filter(
            reply_id__in=[r.id for r in replies], user_id=user_id
        ).values_list('reply_id', flat=True))
        author_ids = set(r.user_id for r in replies if r.user_id != user_id)
        if author_ids:
            followed_author_ids = set(Follow.objects.filter(
                follower_id=user_id, following_id__in=author_ids
            ).values_list('following_id', flat=True))
        bookmarked_ids = set(Bookmark.objects.filter(
            user_id=user_id, target_type='reply',
            target_id__in=[r.id for r in replies]
        ).values_list('target_id', flat=True))
    child_reply_ids = {}
    for r in replies:
        if r.parent_reply_id:
            child_reply_ids.setdefault(r.parent_reply_id, []).append(r)
    total_descendants = {}
    def _count_descendants(rid):
        if rid in total_descendants:
            return total_descendants[rid]
        children = child_reply_ids.get(rid, [])
        count = len(children)
        for c in children:
            count += _count_descendants(c.id)
        total_descendants[rid] = count
        return count
    for r in replies:
        if r.id not in total_descendants:
            _count_descendants(r.id)
    result = []
    for r in replies:
        children = child_reply_ids.get(r.id, [])
        child_authors = []
        seen = set()
        all_descendants = []
        stack = list(children)
        while stack:
            c = stack.pop()
            all_descendants.append(c)
            stack.extend(child_reply_ids.get(c.id, []))
        for c in all_descendants[:3]:
            if c.user_id not in seen:
                seen.add(c.user_id)
                child_authors.append({
                    'id': c.user_id,
                    'username': c.user.username,
                    'photoUrl': c.user.photo_url,
                })
        result.append({
            'id': r.id, 'postId': r.post_id, 'postTitle': r.post.title if r.post else '', 'parentReplyId': r.parent_reply_id,
            'content': r.content, 'authorName': r.user.username,
            'authorPhotoUrl': r.user.photo_url, 'authorId': r.user_id,
            'authorBadgeInfo': _user_badge_info(r.user),
            'authorAchievements': _user_achievement_badges(r.user),
            'authorIsBot': r.user.is_bot,
            'thumbsUpCount': r.thumbs_up_count, 'childCount': total_descendants.get(r.id, len(children)),
            'childAuthors': child_authors,
            'createdAt': r.created_at,
            'isEdited': r.is_edited, 'editedAt': r.edited_at,
            'isArchived': r.is_archived,
            'isThumbedUp': r.id in liked_ids,
            'isFollowed': r.user_id in followed_author_ids,
            'isBookmarked': r.id in bookmarked_ids,
        })
    return result


def _serialize_reply(r, user_id=None, _liked_ids=None, _bookmarked_ids=None):
    is_thumbed_up = False
    is_bookmarked = False
    if user_id:
        if _liked_ids is not None:
            is_thumbed_up = r.id in _liked_ids
        else:
            is_thumbed_up = ReplyLike.objects.filter(reply_id=r.id, user_id=user_id).exists()
        if _bookmarked_ids is not None:
            is_bookmarked = r.id in _bookmarked_ids
        else:
            is_bookmarked = Bookmark.objects.filter(user_id=user_id, target_type='reply', target_id=r.id).exists()
    return {
        'id': r.id, 'postId': r.post_id, 'parentReplyId': r.parent_reply_id,
        'content': r.content, 'authorName': r.user.username,
        'authorPhotoUrl': r.user.photo_url, 'authorId': r.user_id,
        'authorBadgeInfo': _user_badge_info(r.user),
        'authorAchievements': _user_achievement_badges(r.user),
        'authorIsBot': r.user.is_bot,
        'thumbsUpCount': r.thumbs_up_count, 'childCount': r.reply_count,
        'createdAt': r.created_at,
        'isEdited': r.is_edited, 'editedAt': r.edited_at, 'isArchived': r.is_archived,
        'isThumbedUp': is_thumbed_up,
        'isBookmarked': is_bookmarked,
    }


def _get_user_id(request):
    token = _get_valid_token(request)
    if not token:
        return None
    cache_key = f'user_id_{hash_auth_token(token)}'
    user_id = cache.get(cache_key)
    if user_id is not None:
        return user_id
    return None


def _get_valid_token(request):
    token = api.get_session_token(request)
    if not token:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
    if not token:
        return None
    cache_key = f'valid_token:{hash_auth_token(token)}'
    if cache.get(cache_key):
        return token
    try:
        user = get_user_by_auth_token(token)
        cache.set(cache_key, True, 300)
        cache.set(f'user_id_{hash_auth_token(token)}', user.id, 300)
        return token
    except User.DoesNotExist:
        api.clear_session_auth(request)
        return None


def _ctx(request, **extra):
    token = api.get_session_token(request)
    user = api.get_session_user(request)
    if user:
        user = _normalize_user_data(user)
    dark_mode = request.session.get('theme') == 'dark'
    unread_notifications = 0
    if user and user.get('id'):
        try:
            db_user = User.objects.get(pk=user['id'])
            unread_notifications = getattr(db_user, 'unread_notification_count', 0) or 0
        except User.DoesNotExist:
            pass
    ctx = {
        'is_authenticated': bool(token),
        'user': user,
        'dark_mode': dark_mode,
        'unread_notifications': unread_notifications,
        'csp_nonce': getattr(request, 'csp_nonce', ''),
    }
    ctx.update(extra)
    return ctx


def _admin_token(request):
    # Custom admin pages authenticate through Django's staff session. Server-side
    # admin API calls are additionally protected with a short-lived signed header
    # generated in web.api_client, so no shared bearer token is exposed.
    return None


def _is_staff_admin(request):
    return bool(getattr(request, 'user', None) and request.user.is_authenticated and request.user.is_staff)


def _require_staff_admin(request):
    return None if _is_staff_admin(request) else redirect('web:admin_login')


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
        resources = _serialize_resources(Resource.objects.filter(approval_status='approved')[:50])
        cache.set('home_resources', resources, 60)
    posts = cache.get('home_posts')
    if posts is None:
        posts_qs = Post.objects.select_related('user').order_by('-created_at')[:10]
        posts = _serialize_posts(posts_qs, user_id)
        cache.set('home_posts', posts, 120)
    elif user_id:
        liked_ids = set(PostLike.objects.filter(
            post_id__in=[p['id'] for p in posts], user_id=user_id
        ).values_list('post_id', flat=True))
        for p in posts:
            p['isThumbedUp'] = p['id'] in liked_ids
    recent = resources[:5]
    popular = sorted(resources, key=lambda r: r.get('view_count', 0), reverse=True)[:5]
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
        hide_footer_links=True,
    ))


def library(request):
    user_id = _get_user_id(request)
    subjects = [s.strip() for s in request.GET.getlist('subject') if s.strip()]
    grades = [g.strip() for g in request.GET.getlist('grade') if g.strip()]
    types = [t.strip() for t in request.GET.getlist('type') if t.strip()]
    faculties = [f.strip() for f in request.GET.getlist('faculty') if f.strip()]
    exam_types = [e.strip() for e in request.GET.getlist('exam_type') if e.strip()]
    sort_by = request.GET.get('sort', 'relevant')
    qs = Resource.objects.filter(approval_status='approved')
    if subjects:
        q = Q()
        for s in subjects:
            q |= Q(subject__iexact=s)
        qs = qs.filter(q)
    if grades:
        q = Q()
        for g in grades:
            q |= Q(grade_level__iexact=g)
        qs = qs.filter(q)
    if types:
        q = Q()
        for t in types:
            q |= Q(type__iexact=t)
        qs = qs.filter(q)
    if faculties:
        q = Q()
        for f in faculties:
            q |= Q(faculty__iexact=f)
        qs = qs.filter(q)
    if exam_types:
        q = Q()
        for e in exam_types:
            q |= Q(exam_type__iexact=e)
        qs = qs.filter(q)
    if sort_by == 'newest':
        qs = qs.order_by('-added_at')
    elif sort_by == 'oldest':
        qs = qs.order_by('added_at')
    else:
        qs = qs.order_by('-view_count', '-added_at')
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    page_num = request.GET.get('page', 1)
    paginator = Paginator(qs, 12)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    filtered = _serialize_resources(page_obj.object_list)
    all_resources = cache.get('library_all_resources')
    if all_resources is None:
        all_resources = _serialize_resources(Resource.objects.filter(approval_status='approved')[:500])
        cache.set('library_all_resources', all_resources, 180)
    all_subjects = sorted(list(set(s.strip() for r in all_resources if r.get('subject') for s in r.get('subject', '').split(',') if s.strip())))
    all_grades = sorted(set(r.get('grade_level', '') for r in all_resources if r.get('grade_level')))
    all_types = sorted(set(r.get('type', '') for r in all_resources if r.get('type')))
    all_faculties = sorted(set(r.get('faculty', '') for r in all_resources if r.get('faculty')))
    all_exam_types = sorted(set(r.get('exam_type', '') for r in all_resources if r.get('exam_type')))
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    return render(request, 'web/library.html', _ctx(request,
        resources=filtered,
        all_subjects=all_subjects,
        all_grades=all_grades,
        all_types=all_types,
        all_faculties=all_faculties,
        all_exam_types=all_exam_types,
        education_levels=education_levels,
        current_subjects=subjects,
        current_grades=grades,
        current_types=types,
        current_faculties=faculties,
        current_exam_types=exam_types,
        current_sort=sort_by,
        page_obj=page_obj,
    ))


def _serialize_users_search(users, viewer_id=None):
    followed_ids = set()
    if viewer_id:
        user_ids = [u.id for u in users if u.id != viewer_id]
        if user_ids:
            followed_ids = set(Follow.objects.filter(
                follower_id=viewer_id, following_id__in=user_ids
            ).values_list('following_id', flat=True))
    return [_serialize_user_search_single(u, viewer_id, followed_ids) for u in users]


def _serialize_user_search_single(u, viewer_id=None, _followed_ids=None):
    is_self = bool(viewer_id and str(viewer_id) == str(u.id))
    is_following = False
    if viewer_id and not is_self:
        if _followed_ids is not None:
            is_following = u.id in _followed_ids
        else:
            is_following = Follow.objects.filter(
                follower_id=viewer_id, following_id=u.id
            ).exists()
    return {
        'id': u.id,
        'username': u.username,
        'displayName': u.display_name or u.username,
        'photoUrl': u.photo_url,
        'bio': u.bio or '',
        'classLevel': u.class_level or '',
        'school': u.school or '',
        'isAdmin': bool(u.is_admin),
        'moderatorLevel': u.moderator_level or 0,
        'verificationLevel': u.verification_level or 0,
        'badgeInfo': _user_badge_info(u),
        'followerCount': getattr(u, 'follower_count', 0) or 0,
        'isFollowing': is_following,
        'isSelf': is_self,
    }


def search(request):
    user_id = _get_user_id(request)
    query = request.GET.get('q', '').strip()
    tab = request.GET.get('tab', 'all')
    subject = request.GET.get('subject', '')
    grade = request.GET.get('grade', '')
    rtype = request.GET.get('type', '')
    resource_results = []
    post_results = []
    user_results = []
    all_subjects = []
    all_grades = []
    all_types = []
    if query:
        resource_qs = Resource.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__icontains=query) | Q(faculty__icontains=query) | Q(program__icontains=query) | Q(school__icontains=query) | Q(tags__icontains=query),
            approval_status='approved'
        )
        post_qs = Post.objects.select_related('user').filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).filter(is_archived=False)
        if subject:
            resource_qs = resource_qs.filter(subject=subject)
            post_qs = post_qs.filter(category__iexact=subject)
        if grade:
            resource_qs = resource_qs.filter(grade_level=grade)
        if rtype:
            resource_qs = resource_qs.filter(type=rtype)
        if tab in ('all', 'resources'):
            resource_results = _serialize_resources(resource_qs[:30])
        if tab in ('all', 'posts'):
            post_results = _serialize_posts(post_qs[:20], user_id)
        if tab in ('all', 'users'):
            user_qs = User.objects.filter(
                Q(username__icontains=query) | Q(display_name__icontains=query)
            ).filter(is_locked=False).order_by('-follower_count', 'username')[:30]
            user_results = _serialize_users_search(user_qs, user_id)
    all_resources = cache.get('library_all_resources')
    if all_resources is None:
        all_resources = _serialize_resources(Resource.objects.filter(approval_status='approved')[:500])
        cache.set('library_all_resources', all_resources, 180)
    all_subjects = sorted(list(set(s.strip() for r in all_resources if r.get('subject') for s in r.get('subject', '').split(',') if s.strip())))
    all_grades = sorted(set(r.get('grade_level', '') for r in all_resources if r.get('grade_level')))
    all_types = sorted(set(r.get('type', '') for r in all_resources if r.get('type')))
    return render(request, 'web/search.html', _ctx(request,
        query=query,
        tab=tab,
        resource_results=resource_results,
        post_results=post_results,
        user_results=user_results,
        all_subjects=all_subjects,
        all_grades=all_grades,
        all_types=all_types,
        current_subject=subject,
        current_grade=grade,
        current_type=rtype,
    ))


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
    post_count = getattr(user, 'post_count', None)
    reply_count = getattr(user, 'reply_count', None)
    follower_count = getattr(user, 'follower_count', None)
    following_count = getattr(user, 'following_count', None)
    likes_given = getattr(user, 'likes_given_count', None)
    likes_received = getattr(user, 'likes_received_count', None)
    contribution_score = getattr(user, 'contribution_score', None)
    needs_fallback = any(v is None for v in [post_count, reply_count, follower_count, following_count, likes_given, likes_received, contribution_score])
    if needs_fallback:
        fallback = _build_local_stats_fallback(user.id)
        post_count = post_count if post_count is not None else fallback.get('post_count', 0)
        reply_count = reply_count if reply_count is not None else fallback.get('reply_count', 0)
        follower_count = follower_count if follower_count is not None else fallback.get('follower_count', 0)
        following_count = following_count if following_count is not None else fallback.get('following_count', 0)
        likes_given = likes_given if likes_given is not None else fallback.get('likes_given', 0)
        likes_received = likes_received if likes_received is not None else fallback.get('likes_received', 0)
        contribution_score = contribution_score if contribution_score is not None else fallback.get('contribution_score', 0)
    return {
        'post_count': post_count,
        'reply_count': reply_count,
        'likes_given': likes_given,
        'likes_received': likes_received,
        'contribution_score': contribution_score,
    }


def _build_local_stats_fallback(user_id):
    stats = User.objects.filter(pk=user_id).annotate(
        _post_count=Count('posts', distinct=True),
        _reply_count=Count('replies', distinct=True),
        _follower_count=Count('followers_set', distinct=True),
        _following_count=Count('following_set', distinct=True),
        _likes_given=Count('post_likes', distinct=True) + Count('reply_likes', distinct=True),
    ).values(
        '_post_count', '_reply_count', '_follower_count', '_following_count', '_likes_given',
    ).first()
    if not stats:
        return {}
    likes_received = (PostLike.objects.filter(post__user_id=user_id).count() +
                      ReplyLike.objects.filter(reply__user_id=user_id).count() +
                      ResourceLike.objects.filter(resource__uploaded_by_id=user_id).count())
    approved_resource_count = Resource.objects.filter(uploaded_by_id=user_id, approval_status='approved').count()
    pc = stats['_post_count'] or 0
    rc = stats['_reply_count'] or 0
    lg = stats['_likes_given'] or 0
    contribution_score = (pc * 3) + (rc * 2) + lg + (likes_received * 2) + (approved_resource_count * 10)
    return {
        'post_count': pc,
        'reply_count': rc,
        'follower_count': stats['_follower_count'] or 0,
        'following_count': stats['_following_count'] or 0,
        'likes_given': lg,
        'likes_received': likes_received,
        'contribution_score': contribution_score,
    }


def _build_contributors_batch():
    users = User.objects.all()
    contributors = []
    for u in users:
        score = getattr(u, 'contribution_score', None)
        if score is None:
            pc = getattr(u, 'post_count', 0) or 0
            rc = getattr(u, 'reply_count', 0) or 0
            lg = getattr(u, 'likes_given_count', 0) or 0
            lr = getattr(u, 'likes_received_count', 0) or 0
            score = (pc * 3) + (rc * 2) + lg + (lr * 2)
        contributors.append({
            'username': u.username,
            'display_name': u.display_name or u.username,
            'photo_url': u.photo_url,
            'score': score,
            'formatted_score': format_score(score),
            'level': get_user_level_title(score),
            'badgeInfo': _user_badge_info(u),
        })
    contributors.sort(key=lambda c: c['score'], reverse=True)
    return contributors

def forum(request):
    user_id = _get_user_id(request)
    category = request.GET.get('category', '')
    qs = Post.objects.select_related('user').order_by('-created_at')
    if category:
        qs = qs.filter(category__iexact=category)
    posts = _serialize_posts(qs[:50], user_id)

    all_posts = cache.get('forum_all_posts')
    if all_posts is None:
        all_posts_qs = Post.objects.select_related('user').order_by('-created_at')[:100]
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
        contributor_data = _build_contributors_batch()[:10]
        cache.set('forum_contributors', contributor_data, 300)

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
        contributor_data = _build_contributors_batch()[:50]
        cache.set('forum_contributors', contributor_data, 300)
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
    all_replies = _serialize_replies(replies_qs, user_id)
    top_level = []
    children_map = {}
    for r in all_replies:
        if not r['parentReplyId']:
            top_level.append(r)
        else:
            children_map.setdefault(r['parentReplyId'], []).append(r)
    is_following = False
    is_owner = False
    if user_id:
        is_owner = (user_id == post_obj.user_id)
        if not is_owner:
            is_following = Follow.objects.filter(follower_id=user_id, following_id=post_obj.user_id).exists()
    all_usernames = list(set(
        [post_obj.user.username] + [r['authorName'] for r in all_replies]
    ))
    return render(request, 'web/forum_post.html', _ctx(request, post=post, replies=all_replies, top_level_replies=top_level, children_map=children_map, post_id=post_id, is_owner=is_owner, is_following=is_following, post_author_id=post_obj.user_id, all_usernames=all_usernames))


def create_post(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category = request.POST.get('category', '').strip()
        if title and content and category:
            result = services.create_post(user, title, content, category)
            if result and result.get('id'):
                _clear_page_cache()
                return redirect('web:forum_post', post_id=result['id'])
    categories = ['General', 'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Computer Science', 'Exam Tips']
    return render(request, 'web/create_post.html', _ctx(request, categories=categories))


def reply_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')
    try:
        post_obj = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found")
    post = _serialize_post(post_obj, user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        parent_reply_id = request.POST.get('parent_reply_id', '') or None
        if content:
            services.create_reply(user, post_id, content, parent_reply_id)
            _clear_page_cache()
            return redirect('web:forum_post', post_id=post_id)
    return render(request, 'web/reply.html', _ctx(request, post=post, post_id=post_id))


def reader(request, resource_id):
    """Resource detail page — shows title, description, view/download/like actions, and comments."""
    user_id = _get_user_id(request)
    try:
        resource_obj = Resource.objects.select_related('uploaded_by').get(id=resource_id)
    except Resource.DoesNotExist:
        raise Http404("Resource not found")

    if resource_obj.approval_status != 'approved' and not _is_staff_admin(request):
        raise Http404("Resource not found")

    # Increment view count once per session
    view_key = f'resource_viewed_{resource_id}'
    if not request.session.get(view_key):
        Resource.objects.filter(pk=resource_id).update(view_count=F('view_count') + 1)
        request.session[view_key] = True
        resource_obj.view_count += 1  # update in-memory

    resource = _serialize_resource(resource_obj)

    # Validate file URL for "open in new tab" / download links
    raw_file_url = resource.get('file_url') or ''
    safe_file_url = ''
    file_url_error = ''
    if raw_file_url:
        media_prefix = settings.MEDIA_URL
        if raw_file_url.startswith(media_prefix) or (request and raw_file_url.startswith(request.build_absolute_uri(media_prefix))):
            safe_file_url = raw_file_url
        else:
            try:
                safe_file_url = validate_resource_file_url(raw_file_url)
            except ValidationError as exc:
                file_url_error = ' '.join(exc.messages)
    resource['safe_file_url'] = safe_file_url
    resource['file_url_error'] = file_url_error

    # Classify media type for template
    rtype_lower = (resource.get('type') or '').lower().strip()
    if rtype_lower == 'pdf':
        media_type = 'pdf'
    elif rtype_lower == 'video':
        media_type = 'video'
    elif rtype_lower == 'audio':
        media_type = 'audio'
    elif rtype_lower == 'image':
        media_type = 'image'
    else:
        media_type = 'document'
    resource['media_type'] = media_type

    # User-specific state: liked, bookmarked
    is_liked = False
    is_bookmarked = False
    if user_id:
        is_liked = ResourceLike.objects.filter(resource_id=resource_id, user_id=user_id).exists()
        is_bookmarked = Bookmark.objects.filter(
            user_id=user_id, target_type='resource', target_id=resource_id
        ).exists()

    # Load comments
    comments_qs = ResourceComment.objects.select_related('user').filter(
        resource_id=resource_id
    ).order_by('created_at')
    comments_list = list(comments_qs)
    liked_comment_ids = set()
    if user_id and comments_list:
        liked_comment_ids = set(ResourceCommentLike.objects.filter(
            comment_id__in=[c.id for c in comments_list], user_id=user_id
        ).values_list('comment_id', flat=True))
    all_comments = []
    for c in comments_list:
        c_data = {
            'id': c.id,
            'resourceId': c.resource_id,
            'authorId': c.user_id,
            'authorName': c.user.username if c.user else '',
            'authorPhoto': c.user.photo_url if c.user else '',
            'parentCommentId': c.parent_comment_id or '',
            'content': c.content,
            'likeCount': c.like_count,
            'replyCount': c.reply_count,
            'isEdited': c.is_edited,
            'createdAt': c.created_at,
            'isLiked': c.id in liked_comment_ids,
            'isOwner': (user_id and user_id == c.user_id),
        }
        all_comments.append(c_data)

    # Build tree: top-level and children
    top_level_comments = [c for c in all_comments if not c['parentCommentId']]
    children_map = {}
    for c in all_comments:
        if c['parentCommentId']:
            children_map.setdefault(c['parentCommentId'], []).append(c)

    # Related resources (same subject, excluding this one)
    related = Resource.objects.filter(
        subject__iexact=resource_obj.subject
    ).exclude(pk=resource_id).order_by('-view_count', '-added_at')[:4]
    related_resources = _serialize_resources(related)

    can_edit = bool(user_id and user_id == resource_obj.uploaded_by_id)

    return render(request, 'web/resource_detail.html', _ctx(request,
        resource=resource,
        resource_id=resource_id,
        is_liked=is_liked,
        is_bookmarked=is_bookmarked,
        can_edit=can_edit,
        comments=all_comments,
        top_level_comments=top_level_comments,
        children_map=children_map,
        comment_count=resource_obj.comment_count,
        related_resources=related_resources,
    ))


def profile(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    is_self = bool(user_id and user_id == profile_user.id)
    profile_private = bool(profile_user.is_locked and not is_self)

    badge_info = _user_badge_info(profile_user)

    banner_type = ''
    banner_deco_text = 'nebian'
    banner_text_color = ''
    if not profile_user.banner_url:
        if profile_user.is_bot:
            banner_type = 'gradient-bot'
            banner_deco_text = 'neby ai'
            banner_text_color = 'rgba(255,255,255,0.25)'
        elif profile_user.is_admin:
            banner_type = 'gradient-admin'
            banner_deco_text = 'admin'
            banner_text_color = 'rgba(255,255,255,0.25)'
        elif profile_user.moderator_level and profile_user.moderator_level > 0:
            banner_type = 'gradient-moderator'
            banner_deco_text = 'moderator'
            banner_text_color = 'rgba(255,255,255,0.22)'
        elif profile_user.verification_level and profile_user.verification_level > 0:
            banner_type = 'gradient-verified'
            banner_deco_text = 'nebian'
            banner_text_color = 'rgba(255,255,255,0.20)'

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'banner_url': profile_user.banner_url,
        'banner_type': banner_type,
        'banner_deco_text': banner_deco_text,
        'banner_text_color': banner_text_color,
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
        'verification_level': profile_user.verification_level,
        'moderator_level': profile_user.moderator_level,
        'is_admin': profile_user.is_admin,
        'is_bot': profile_user.is_bot,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': badge_info,
        'achievement_info': _user_achievement_badges(profile_user),
    }

    if profile_private:
        profile_data.update({
            'email': '', 'dob': '', 'gender': '', 'class_level': '', 'class': '',
            'subjects': '', 'pradesh': '', 'district': '', 'school': '',
        })

    stats = _build_local_stats(profile_user) if not profile_private else {
        'post_count': 0, 'reply_count': 0, 'likes_given': 0, 'likes_received': 0, 'contribution_score': 0,
    }
    follower_count = profile_user.follower_count if (not profile_private and hasattr(profile_user, 'follower_count') and profile_user.follower_count > 0) else (Follow.objects.filter(following_id=profile_user.id).count() if not profile_private else 0)
    following_count = profile_user.following_count if (not profile_private and hasattr(profile_user, 'following_count') and profile_user.following_count > 0) else (Follow.objects.filter(follower_id=profile_user.id).count() if not profile_private else 0)
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = False
    stats['is_self'] = False
    if user_id:
        stats['is_self'] = is_self
        if not stats['is_self'] and not profile_private:
            stats['is_following'] = Follow.objects.filter(follower_id=user_id, following_id=profile_user.id).exists()

    if not profile_private:
        if is_self:
            uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id).count()
        else:
            uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').count()
    else:
        uploaded_resources_count = 0
    stats['uploaded_resources_count'] = uploaded_resources_count

    user_posts_qs = Post.objects.none() if profile_private else Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    user_replies_qs = Reply.objects.none() if profile_private else Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_replies = _serialize_replies(user_replies_qs, user_id)

    user_resources = []
    if not profile_private:
        if is_self:
            user_resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id).order_by('-added_at')
        else:
            user_resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').order_by('-added_at')

        liked_res_ids = set()
        if user_id and user_resources_qs:
            liked_res_ids = set(ResourceLike.objects.filter(
                resource_id__in=[r.id for r in user_resources_qs], user_id=user_id
            ).values_list('resource_id', flat=True))

        for r in user_resources_qs:
            user_resources.append({
                'id': r.id,
                'title': r.title,
                'description': r.description or '',
                'subject': r.subject,
                'grade_level': r.grade_level,
                'type': r.type,
                'file_size': r.file_size,
                'added_at': r.added_at,
                'view_count': r.view_count,
                'like_count': r.like_count,
                'comment_count': r.comment_count,
                'approval_status': r.approval_status,
                'rejection_reason': r.rejection_reason or '',
                'is_liked': r.id in liked_res_ids,
            })

    user_photos = []
    if user_id and user_id == profile_user.id:
        user_photos = list(UserPhoto.objects.filter(user_id=profile_user.id).values('id', 'url', 'uploaded_at', 'is_current'))

    return render(request, 'web/profile.html', _ctx(request,
        profile_user=profile_data,
        username=username,
        stats=stats,
        user_photos=user_photos,
        user_posts=user_posts,
        user_replies=user_replies,
        user_resources=user_resources,
        profile_private=profile_private,
        badge_info=profile_data.get('badge_info'),
        badge_info_json=json.dumps(profile_data.get('badge_info')),
        achievement_info_json=json.dumps(profile_data.get('achievement_info', [])),
    ))


def profile_achievements(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    if profile_user.is_locked and user_id != profile_user.id:
        return redirect('web:profile', username=username)

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'banner_url': profile_user.banner_url,
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
        'verification_level': profile_user.verification_level,
        'moderator_level': profile_user.moderator_level,
        'is_admin': profile_user.is_admin,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': _user_badge_info(profile_user),
        'achievement_info': _user_achievement_badges(profile_user),
    }

    stats = _build_local_stats(profile_user)
    follower_count = profile_user.follower_count if hasattr(profile_user, 'follower_count') and profile_user.follower_count > 0 else Follow.objects.filter(following_id=profile_user.id).count()
    following_count = profile_user.following_count if hasattr(profile_user, 'following_count') and profile_user.following_count > 0 else Follow.objects.filter(follower_id=profile_user.id).count()
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
        achievement_info=_user_achievement_badges(profile_user),
    ))


def ajax_profile_activity(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if profile_user.is_locked and user_id != profile_user.id:
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
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


def ajax_profile_replies(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if profile_user.is_locked and user_id != profile_user.id:
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    replies_qs = Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id).order_by('-created_at')[offset:offset+limit]
    replies = _serialize_replies(replies_qs, user_id)

    total_count = Reply.objects.filter(user_id=profile_user.id).count()
    has_more = (offset + len(replies)) < total_count

    return JsonResponse({
        'replies': replies,
        'has_more': has_more,
        'total_count': total_count
    })




def upload_resource(request):
    """Standalone upload page — authenticated users upload with approval_status='pending'.
    Supports both file upload (primary) and URL (secondary)."""
    user_id = _get_user_id(request)
    user = None
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

    _default_subjects = [
        'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
        'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
        'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
        'Environment Science', 'Science', 'General Science', 'Life Science',
        'Physical Science', 'Earth Science', 'Applied Mathematics',
        'Business Mathematics', 'Statistics', 'Probability',
        'Microeconomics', 'Macroeconomics',
        'Financial Accounting', 'Cost Accounting', 'Auditing',
        'Marketing', 'Office Management', 'Hotel Management',
        'Computer Engineering', 'Electronics', 'Electrical Engineering',
        'Civil Engineering', 'Mechanical Engineering', 'Architecture',
        'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Botany', 'Zoology', 'Genetics', 'Ecology',
        'English Grammar', 'English Literature', 'Creative Writing',
        'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
        'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
        'Education', 'Pedagogy', 'Curriculum Development',
        'Law', 'Constitutional Law', 'International Law',
        'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
        'Agriculture', 'Forestry', 'Veterinary Science',
        'Management', 'Human Resource Management', 'Entrepreneurship',
        'Information Technology', 'Programming', 'Web Development',
        'Database Management', 'Networking', 'Cybersecurity',
        'Machine Learning', 'Artificial Intelligence', 'Data Science',
        'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
        'Digital Logic', 'Operating Systems', 'Software Engineering',
        'Surveying', 'Estimating & Costing', 'Building Construction',
        'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
        'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
    ]
    db_subjects = []
    for s_str in Resource.objects.values_list('subject', flat=True):
        if s_str:
            for s in s_str.split(','):
                s_stripped = s.strip()
                if s_stripped:
                    db_subjects.append(s_stripped)
    subjects = sorted(set(_default_subjects + db_subjects))
    common_tags = [
        'NEB', 'SEE', 'Board Exam', 'Past Paper', 'Model Paper', 'Solution',
        'Important Questions', 'Numerical', 'Derivation', 'Formula Sheet',
        'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5',
        'Chapter 6', 'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10',
        'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5',
        'Class 11', 'Class 12', 'Grade 11', 'Grade 12',
        'Science', 'Management', 'Humanities', 'Education', 'Law',
        'Final Exam', 'Midterm', 'Internal Assessment', 'Practical',
        'Old Course', 'New Course', 'Revised Syllabus', 'Curriculum',
        'Textbook', 'Reference Book', 'Guide', 'Notes', 'Summary',
        'Objective Questions', 'Subjective Questions', 'MCQ', 'Long Answer',
        'Short Answer', 'Very Short Answer', 'Essay Type',
        '2080 BS', '2081 BS', '2082 BS', '2079 BS',
        '2078 BS', '2077 BS', '2076 BS',
        'Kathmandu', 'Pokhara', 'Chitwan', 'Biratnagar', 'Butwal',
        'HSEB', 'TU', 'KU', 'PU', 'CTEVT',
        'Entrance', 'IOE', 'IOM', 'CEEE', 'KUUMAT',
        'C Programming', 'Python', 'Java', 'Web Development',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Mechanics', 'Optics', 'Thermodynamics', 'Electricity',
        'Calculus', 'Algebra', 'Trigonometry', 'Geometry', 'Statistics',
        'Botany', 'Zoology', 'Ecology', 'Genetics',
        'Nepali', 'English', 'Social Studies',
    ]
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    exam_types = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']
    pradesh_options = [
        'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
    ]
    resource_types = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subject = request.POST.get('subject', '').strip()
        grade_level = request.POST.get('grade_level', '').strip()
        faculty = request.POST.get('faculty', '').strip()
        program = request.POST.get('program', '').strip()
        year = request.POST.get('year', '').strip()
        exam_type = request.POST.get('exam_type', '').strip()
        pradesh = request.POST.get('pradesh', '').strip()
        district = request.POST.get('district', '').strip()
        school = request.POST.get('school', '').strip()
        tags = request.POST.get('tags', '').strip()
        description = request.POST.get('description', '').strip()
        rtype = request.POST.get('type', 'PDF').strip() or 'PDF'
        author_name = request.POST.get('author_name', '').strip()
        source_url = request.POST.get('source_url', '').strip()
        source_label = request.POST.get('source_label', '').strip()
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()

        uploaded_file = request.FILES.get('file')
        file_url = request.POST.get('file_url', '').strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not subject:
            errors.append('Subject is required.')
        if not uploaded_file and not file_url:
            errors.append('Please upload a file or provide a file URL.')

        file_path = ''
        file_size = 0

        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if err_resp:
                errors.append(err_resp['error'])
            else:
                file_path = path or ''
                file_size = size

        safe_file_url = ''
        if not uploaded_file and file_url:
            try:
                safe_file_url = validate_resource_file_url(file_url)
            except Exception as exc:
                messages_list = getattr(exc, 'messages', [str(exc)])
                errors.append(' '.join(messages_list))

        safe_thumbnail_url = ''
        if thumbnail_url:
            try:
                safe_thumbnail_url = validate_resource_file_url(thumbnail_url)
            except Exception:
                errors.append('Invalid thumbnail URL.')

        if not errors:
            final_file_url = ''
            if file_path:
                final_file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
            elif safe_file_url:
                final_file_url = safe_file_url

            resource = Resource(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                subject=subject,
                grade_level=grade_level,
                faculty=faculty,
                program=program,
                year=year,
                exam_type=exam_type,
                pradesh=pradesh,
                district=district,
                school=school,
                tags=tags,
                type=rtype,
                file=file_path or None,
                file_url=final_file_url,
                thumbnail_url=safe_thumbnail_url,
                file_size=file_size or int(request.POST.get('file_size', '0')),
                added_at=int(time.time() * 1000),
                author_name=author_name,
                source_type='user' if user else 'anonymous',
                uploaded_by=user,
                source_url=source_url,
                source_label=source_label,
                approval_status='pending',
            )
            resource.save()
            cache.delete_many(['home_resources', 'library_all_resources'])
            return render(request, 'web/upload_success.html', _ctx(request,
                resource=_serialize_resource(resource),
                is_anonymous=not bool(user),
            ))

        return render(request, 'web/upload.html', _ctx(request,
            subjects=subjects, education_levels=education_levels,
            exam_types=exam_types, pradesh_options=pradesh_options,
            resource_types=resource_types, common_tags=common_tags,
            errors=errors,
            form_data=request.POST,
            is_authenticated=bool(user),
        ))

    return render(request, 'web/upload.html', _ctx(request,
        subjects=subjects, education_levels=education_levels,
        exam_types=exam_types, pradesh_options=pradesh_options,
        resource_types=resource_types, common_tags=common_tags,
        is_authenticated=bool(user),
    ))


def edit_resource(request, resource_id):
    """Allow signed-in users who uploaded a resource to edit it."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        resource_obj = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        raise Http404("Resource not found")
    if resource_obj.uploaded_by_id != user_id:
        return redirect('web:reader', resource_id=resource_id)

    user = User.objects.get(pk=user_id)
    _default_subjects = [
        'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
        'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
        'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
        'Environment Science', 'Science', 'General Science', 'Life Science',
        'Physical Science', 'Earth Science', 'Applied Mathematics',
        'Business Mathematics', 'Statistics', 'Probability',
        'Microeconomics', 'Macroeconomics',
        'Financial Accounting', 'Cost Accounting', 'Auditing',
        'Marketing', 'Office Management', 'Hotel Management',
        'Computer Engineering', 'Electronics', 'Electrical Engineering',
        'Civil Engineering', 'Mechanical Engineering', 'Architecture',
        'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Botany', 'Zoology', 'Genetics', 'Ecology',
        'English Grammar', 'English Literature', 'Creative Writing',
        'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
        'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
        'Education', 'Pedagogy', 'Curriculum Development',
        'Law', 'Constitutional Law', 'International Law',
        'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
        'Agriculture', 'Forestry', 'Veterinary Science',
        'Management', 'Human Resource Management', 'Entrepreneurship',
        'Information Technology', 'Programming', 'Web Development',
        'Database Management', 'Networking', 'Cybersecurity',
        'Machine Learning', 'Artificial Intelligence', 'Data Science',
        'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
        'Digital Logic', 'Operating Systems', 'Software Engineering',
        'Surveying', 'Estimating & Costing', 'Building Construction',
        'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
        'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
    ]
    db_subjects = []
    for s_str in Resource.objects.values_list('subject', flat=True):
        if s_str:
            for s in s_str.split(','):
                s_stripped = s.strip()
                if s_stripped:
                    db_subjects.append(s_stripped)
    subjects = sorted(set(_default_subjects + db_subjects))
    common_tags = [
        'NEB', 'SEE', 'Board Exam', 'Past Paper', 'Model Paper', 'Solution',
        'Important Questions', 'Numerical', 'Derivation', 'Formula Sheet',
        'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5',
        'Chapter 6', 'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10',
        'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5',
        'Class 11', 'Class 12', 'Grade 11', 'Grade 12',
        'Science', 'Management', 'Humanities', 'Education', 'Law',
        'Final Exam', 'Midterm', 'Internal Assessment', 'Practical',
        'Old Course', 'New Course', 'Revised Syllabus', 'Curriculum',
        'Textbook', 'Reference Book', 'Guide', 'Notes', 'Summary',
        'Objective Questions', 'Subjective Questions', 'MCQ', 'Long Answer',
        'Short Answer', 'Very Short Answer', 'Essay Type',
        '2080 BS', '2081 BS', '2082 BS', '2079 BS',
        '2078 BS', '2077 BS', '2076 BS',
        'Kathmandu', 'Pokhara', 'Chitwan', 'Biratnagar', 'Butwal',
        'HSEB', 'TU', 'KU', 'PU', 'CTEVT',
        'Entrance', 'IOE', 'IOM', 'CEEE', 'KUUMAT',
        'C Programming', 'Python', 'Java', 'Web Development',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Mechanics', 'Optics', 'Thermodynamics', 'Electricity',
        'Calculus', 'Algebra', 'Trigonometry', 'Geometry', 'Statistics',
        'Botany', 'Zoology', 'Ecology', 'Genetics',
        'Nepali', 'English', 'Social Studies',
    ]
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    exam_types_list = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']
    pradesh_options = [
        'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
    ]
    resource_types = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']

    if request.method == 'POST':
        resource_obj.title = request.POST.get('title', '').strip() or resource_obj.title
        resource_obj.subject = request.POST.get('subject', '').strip() or resource_obj.subject
        resource_obj.grade_level = request.POST.get('grade_level', '').strip()
        resource_obj.faculty = request.POST.get('faculty', '').strip()
        resource_obj.program = request.POST.get('program', '').strip()
        resource_obj.year = request.POST.get('year', '').strip()
        resource_obj.exam_type = request.POST.get('exam_type', '').strip()
        resource_obj.pradesh = request.POST.get('pradesh', '').strip()
        resource_obj.district = request.POST.get('district', '').strip()
        resource_obj.school = request.POST.get('school', '').strip()
        resource_obj.tags = request.POST.get('tags', '').strip()
        resource_obj.type = request.POST.get('type', '').strip() or resource_obj.type
        resource_obj.description = request.POST.get('description', '').strip()
        resource_obj.author_name = request.POST.get('author_name', '').strip()
        resource_obj.source_label = request.POST.get('source_label', '').strip()
        resource_obj.source_url = request.POST.get('source_url', '').strip()

        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp and path:
                resource_obj.file = path
                resource_obj.file_url = request.build_absolute_uri(settings.MEDIA_URL + path)
                resource_obj.file_size = size

        file_url = request.POST.get('file_url', '').strip()
        if file_url and not uploaded_file:
            try:
                resource_obj.file_url = validate_resource_file_url(file_url)
            except Exception:
                pass

        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        if thumbnail_url:
            try:
                resource_obj.thumbnail_url = validate_resource_file_url(thumbnail_url)
            except Exception:
                pass
        elif request.POST.get('thumbnail_url') == '':
            resource_obj.thumbnail_url = ''

        resource_obj.approval_status = 'pending'
        resource_obj.save()
        cache.delete_many(['home_resources', 'library_all_resources'])
        return redirect('web:reader', resource_id=resource_id)

    resource = _serialize_resource(resource_obj)
    return render(request, 'web/edit_resource.html', _ctx(request,
        resource=resource,
        resource_id=resource_id,
        subjects=subjects,
        common_tags=common_tags,
        education_levels=education_levels,
        exam_types=exam_types_list,
        pradesh_options=pradesh_options,
        resource_types=resource_types,
        is_authenticated=True,
    ))


def resource_requests_page(request):
    """Public resource request listing page."""
    user_id = _get_user_id(request)
    user = None
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

    if request.method == 'POST' and request.POST.get('action') == 'create':
        title = request.POST.get('title', '').strip()
        if title:
            ResourceRequest.objects.create(
                id=str(uuid.uuid4()),
                title=title,
                description=request.POST.get('description', '').strip(),
                subject=request.POST.get('subject', '').strip(),
                grade_level=request.POST.get('grade_level', '').strip(),
                faculty=request.POST.get('faculty', '').strip(),
                program=request.POST.get('program', '').strip(),
                year=request.POST.get('year', '').strip(),
                exam_type=request.POST.get('exam_type', '').strip(),
                pradesh=request.POST.get('pradesh', '').strip(),
                district=request.POST.get('district', '').strip(),
                tags=request.POST.get('tags', '').strip(),
                requested_by=user,
                requester_name=request.POST.get('requester_name', '').strip()[:100] if not user else '',
                requester_email=request.POST.get('requester_email', '').strip() if not user else '',
                created_at=int(time.time() * 1000),
            )
        return redirect('web:resource_requests')

    status_filter = request.GET.get('status', 'open')
    qs = ResourceRequest.objects.select_related('requested_by').all()
    if status_filter:
        qs = qs.filter(status=status_filter)
    subject = request.GET.get('subject', '')
    if subject:
        qs = qs.filter(subject__iexact=subject)
    grade = request.GET.get('grade', '')
    if grade:
        qs = qs.filter(grade_level__iexact=grade)
    qs = qs.order_by('-upvote_count', '-created_at')

    upvoted_ids = set()
    if user_id:
        upvoted_ids = set(ResourceRequestUpvote.objects.filter(
            user_id=user_id, request_id__in=list(qs.values_list('id', flat=True)[:100])
        ).values_list('request_id', flat=True))

    all_subjects = sorted(set(ResourceRequest.objects.values_list('subject', flat=True)))
    all_grades = sorted(set(ResourceRequest.objects.values_list('grade_level', flat=True)))

    requests_data = []
    for req in qs[:50]:
        rd = {
            'id': req.id,
            'title': req.title,
            'description': req.description or '',
            'subject': req.subject,
            'grade_level': req.grade_level,
            'faculty': req.faculty or '',
            'program': req.program or '',
            'year': req.year or '',
            'exam_type': req.exam_type or '',
            'pradesh': req.pradesh or '',
            'district': req.district or '',
            'tags': req.tags or '',
            'status': req.status,
            'upvote_count': req.upvote_count,
            'is_upvoted': req.id in upvoted_ids,
            'created_at': req.created_at,
            'requested_by_name': req.requested_by.display_name or req.requested_by.username if req.requested_by else (req.requester_name or 'Anonymous'),
            'requested_by_photo': req.requested_by.photo_url if req.requested_by else '',
        }
        requests_data.append(rd)

    return render(request, 'web/resource_requests.html', _ctx(request,
        requests=requests_data,
        all_subjects=all_subjects,
        all_grades=all_grades,
        current_status=status_filter,
        current_subject=subject,
        current_grade=grade,
    ))


def admin_pending_resources(request):
    """Admin page to approve/reject pending resources."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        resource_id = request.POST.get('resource_id', '').strip()
        action = request.POST.get('action', '').strip()
        try:
            resource_obj = Resource.objects.get(pk=resource_id)
            admin_user = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
                    admin_user = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    pass
            if action == 'approve':
                resource_obj.approval_status = 'approved'
                resource_obj.reviewed_by = admin_user
                resource_obj.reviewed_at = int(time.time() * 1000)
                resource_obj.rejection_reason = ''
                resource_obj.save()
                if resource_obj.uploaded_by_id:
                    _counters.increment_user_resource_approved(resource_obj.uploaded_by_id)
                    _notif.notify_resource_approved(resource_obj.id, resource_obj.uploaded_by_id)
            elif action == 'reject':
                resource_obj.approval_status = 'rejected'
                resource_obj.reviewed_by = admin_user
                resource_obj.reviewed_at = int(time.time() * 1000)
                resource_obj.rejection_reason = request.POST.get('reason', '').strip()[:500]
                resource_obj.save()
                if resource_obj.uploaded_by_id:
                    _notif.notify_resource_rejected(resource_obj.id, resource_obj.uploaded_by_id, resource_obj.rejection_reason)
            cache.delete_many(['home_resources', 'library_all_resources'])
        except Resource.DoesNotExist:
            pass
        return redirect('web:admin_pending_resources')

    pending = Resource.objects.filter(approval_status='pending').order_by('added_at')
    pending_data = [_serialize_resource(r) for r in pending]
    return render(request, 'admin_panel/pending_resources.html', {
        'is_admin': True,
        'pending_resources': pending_data,
        'active_page': 'resources',
    })


def admin_resource_requests(request):
    """Admin page to manage resource requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        request_id = request.POST.get('request_id', '').strip()
        action = request.POST.get('action', '').strip()
        try:
            req = ResourceRequest.objects.get(pk=request_id)
            if action == 'fulfill':
                req.status = 'fulfilled'
                req.fulfilled_at = int(time.time() * 1000)
                resource_id = request.POST.get('resource_id', '').strip()
                if resource_id:
                    req.fulfilled_by_id = resource_id
                req.save()
            elif action == 'close':
                req.status = 'closed'
                req.save()
            elif action == 'reopen':
                req.status = 'open'
                req.save()
        except ResourceRequest.DoesNotExist:
            pass
        return redirect('web:admin_resource_requests')

    status_filter = request.GET.get('status', '')
    qs = ResourceRequest.objects.select_related('requested_by').all().order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    requests_data = []
    for req in qs[:100]:
        rd = {
            'id': req.id,
            'title': req.title,
            'description': req.description or '',
            'subject': req.subject,
            'grade_level': req.grade_level,
            'status': req.status,
            'upvote_count': req.upvote_count,
            'created_at': req.created_at,
            'requested_by_name': req.requested_by.display_name or req.requested_by.username if req.requested_by else (req.requester_name or 'Anonymous'),
            'requester_email': req.requester_email or '',
        }
        requests_data.append(rd)
    return render(request, 'admin_panel/resource_requests.html', {
        'is_admin': True,
        'requests': requests_data,
        'current_status': status_filter,
        'active_page': 'resource_requests',
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
    return render(request, 'web/login.html', _ctx(request))


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
            user = get_user_by_auth_token(email_auth_token)
            token = email_auth_token
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

    logger.info('google_auth: verifying token (length=%d)', len(id_token))
    google_info = verify_google_token(id_token)
    if not google_info:
        logger.warning('google_auth: Google token verification failed')
        return JsonResponse({'error': 'Invalid Google ID Token'}, status=401)
    user_id = google_info['userId']
    email = google_info.get('email') or ''
    display_name = google_info.get('displayName') or ''
    photo_url = google_info.get('photoUrl') or ''
    try:
        db_user = User.objects.get(pk=user_id)
        token = issue_auth_token(db_user)
        user_data = _normalize_user_data(UserSerializer(db_user).data)
        user_data['isNewUser'] = False
        api.set_session_auth(request, token, user_data)
        logger.info('google_auth: existing user signed in: %s', db_user.username or db_user.id)
        return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': False})
    except User.DoesNotExist:
        pass
    if email:
        try:
            existing = User.objects.get(email__iexact=email)
            token = issue_auth_token(existing)
            user_data = _normalize_user_data(UserSerializer(existing).data)
            user_data['isNewUser'] = False
            api.set_session_auth(request, token, user_data)
            logger.info('google_auth: linked %s to existing user %s (email=%s)', user_id, existing.id, email)
            return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': False})
        except User.DoesNotExist:
            pass
    auth_token = User.generate_token()
    temp_username = f"user_{user_id[:8]}"
    db_user = User(
        pk=user_id,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        created_at=int(time.time() * 1000)
    )
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()
    token = auth_token
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    user_data['isNewUser'] = True
    api.set_session_auth(request, token, user_data)
    logger.info('google_auth: new user created: %s (temp_username=%s)', user_id, temp_username)
    return JsonResponse({'status': 'success', 'user': user_data, 'isNewUser': True})


def _link_oauth_user(request, email, user_pk, display_name, photo_url, provider_name):
    """Auto-link OAuth accounts by verified email.

    If a user with the same verified email already exists, log them into that
    account instead of creating a new one. This prevents duplicate accounts
    when the same person signs in via different providers.

    Returns (HttpResponseRedirect, linked: bool).
    """
    if email:
        try:
            existing = User.objects.get(email__iexact=email)
            token = issue_auth_token(existing)
            user_data = _normalize_user_data(UserSerializer(existing).data)
            user_data['isNewUser'] = False
            api.set_session_auth(request, token, user_data)
            logger.info('%s: linked %s to existing user %s (email=%s)', provider_name, user_pk, existing.id, email)
            return redirect('web:home'), True
        except User.DoesNotExist:
            pass
    return None, False


@require_GET
def _https_redirect_uri(request, path):
    """Build an HTTPS redirect URI, even when behind a proxy that terminates SSL."""
    host = request.get_host()
    return f'https://{host}{path}'


def google_login(request):
    """Kick off Google OAuth2 redirect flow — fully custom button, no GIS chrome."""
    client_id = settings.GOOGLE_CLIENT_ID
    if not client_id:
        return HttpResponse('Google OAuth is not configured.', status=501)
    redirect_uri = _https_redirect_uri(request, '/auth/google/callback/')
    state = request.GET.get('state', '')
    authorize_url = (
        f'https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&response_type=code'
        f'&scope=openid+email+profile'
        f'&prompt=select_account'
        f'&access_type=online'
    )
    if state:
        authorize_url += f'&state={state}'
    return redirect(authorize_url)


def google_oauth_callback(request):
    """Handle Google OAuth2 code → exchange for tokens → verify id_token → login/signup."""
    state = request.GET.get('state', '')
    is_mobile = state == 'mobile_google'
    code = request.GET.get('code')
    if not code:
        if is_mobile:
            return redirect('nebians://auth-callback?error=cancelled')
        messages.error(request, 'Google sign-in was cancelled.')
        return redirect('web:login')
    redirect_uri = _https_redirect_uri(request, '/auth/google/callback/')
    try:
        import requests as _req
        token_resp = _req.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            },
            timeout=10,
        )
        token_data = token_resp.json()
    except Exception as e:
        logger.error('google_oauth_callback: token exchange failed: %s', e)
        if is_mobile:
            return redirect('nebians://auth-callback?error=token_exchange_failed')
        messages.error(request, 'Google sign-in failed. Please try again.')
        return redirect('web:login')
    id_token = token_data.get('id_token')
    if not id_token:
        logger.error('google_oauth_callback: no id_token in response: %s', token_data)
        if is_mobile:
            return redirect('nebians://auth-callback?error=no_id_token')
        messages.error(request, 'Google sign-in failed. Please try again.')
        return redirect('web:login')
    google_info = verify_google_token(id_token)
    if not google_info:
        if is_mobile:
            return redirect('nebians://auth-callback?error=token_verification_failed')
        messages.error(request, 'Google token verification failed.')
        return redirect('web:login')
    user_id = google_info['userId']
    email = google_info.get('email') or ''
    display_name = google_info.get('displayName') or ''
    photo_url = google_info.get('photoUrl') or ''
    try:
        db_user = User.objects.get(pk=user_id)
        token = issue_auth_token(db_user)
        user_data = _normalize_user_data(UserSerializer(db_user).data)
        user_data['isNewUser'] = False
        api.set_session_auth(request, token, user_data)
        logger.info('google_oauth_callback: existing user signed in: %s', db_user.username or db_user.id)
        if is_mobile:
            return redirect(f'nebians://auth-callback?authToken={token}&isNewUser=false&username={db_user.username}')
        return redirect('web:home')
    except User.DoesNotExist:
        pass
    redirect_result, linked = _link_oauth_user(request, email, user_id, display_name, photo_url, 'google_oauth_callback')
    if linked:
        if is_mobile:
            linked_token = api.get_session_token(request) or ''
            return redirect(f'nebians://auth-callback?authToken={linked_token}&isNewUser=false')
        return redirect_result
    auth_token = User.generate_token()
    temp_username = f"user_{user_id[:8]}"
    db_user = User(
        pk=user_id,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        created_at=int(time.time() * 1000)
    )
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()
    token = auth_token
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    user_data['isNewUser'] = True
    api.set_session_auth(request, token, user_data)
    logger.info('google_oauth_callback: new user created: %s (temp_username=%s)', user_id, temp_username)
    if is_mobile:
        return redirect(f'nebians://auth-callback?authToken={auth_token}&isNewUser=true')
    return redirect('web:edit_profile')


def github_login(request):
    """Redirect user to GitHub OAuth authorization page."""
    client_id = settings.GITHUB_CLIENT_ID
    if not client_id:
        return HttpResponse('GitHub OAuth is not configured.', status=501)
    redirect_uri = _https_redirect_uri(request, '/auth/github/callback/')
    state = request.GET.get('mobile', '')
    if state == '1':
        state = 'mobile_github'
    else:
        state = ''
    authorize_url = (
        f'https://github.com/login/oauth/authorize'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&scope=read:user,user:email'
    )
    if state:
        authorize_url += f'&state={state}'
    return redirect(authorize_url)


@require_GET
def github_callback(request):
    """Handle GitHub OAuth callback — exchange code for token, fetch user, create/login."""
    state = request.GET.get('state', '')
    is_mobile = state == 'mobile_github'
    code = request.GET.get('code')
    if not code:
        if is_mobile:
            return redirect('nebians://auth-callback?error=cancelled')
        return HttpResponse('Missing authorization code.', status=400)
    redirect_uri = _https_redirect_uri(request, '/auth/github/callback/')
    token_url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    try:
        import requests as _req
        resp = _req.post(token_url, json=data, headers=headers, timeout=10)
        token_data = resp.json()
    except Exception as e:
        logger.error('github_callback: token exchange failed: %s', e)
        if is_mobile:
            return redirect('nebians://auth-callback?error=token_exchange_failed')
        return HttpResponse('Failed to exchange authorization code.', status=502)
    access_token = token_data.get('access_token')
    if not access_token:
        if is_mobile:
            return redirect('nebians://auth-callback?error=no_access_token')
        return HttpResponse('Failed to get access token from GitHub.', status=502)
    try:
        user_resp = _req.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
            timeout=10,
        )
        github_user = user_resp.json()
    except Exception as e:
        logger.error('github_callback: user fetch failed: %s', e)
        if is_mobile:
            return redirect('nebians://auth-callback?error=user_fetch_failed')
        return HttpResponse('Failed to fetch GitHub user info.', status=502)
    github_id = str(github_user.get('id', ''))
    if not github_id:
        if is_mobile:
            return redirect('nebians://auth-callback?error=no_user_id')
        return HttpResponse('Could not retrieve GitHub user ID.', status=502)
    email = github_user.get('email') or ''
    if not email:
        try:
            emails_resp = _req.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'},
                timeout=10,
            )
            emails = emails_resp.json()
            for e in emails:
                if e.get('primary') and e.get('verified'):
                    email = e['email']
                    break
            if not email:
                for e in emails:
                    if e.get('verified'):
                        email = e['email']
                        break
        except Exception:
            pass
    display_name = github_user.get('name') or github_user.get('login', '')
    photo_url = github_user.get('avatar_url') or ''
    user_pk = f'github_{github_id}'
    try:
        db_user = User.objects.get(pk=user_pk)
        token = issue_auth_token(db_user)
        user_data = _normalize_user_data(UserSerializer(db_user).data)
        user_data['isNewUser'] = False
        api.set_session_auth(request, token, user_data)
        logger.info('github_callback: existing user signed in: %s', db_user.username or db_user.id)
        if is_mobile:
            return redirect(f'nebians://auth-callback?authToken={token}&isNewUser=false&username={db_user.username}')
        return redirect('web:home')
    except User.DoesNotExist:
        pass
    redirect_result, linked = _link_oauth_user(request, email, user_pk, display_name, photo_url, 'github_callback')
    if linked:
        if is_mobile:
            linked_token = api.get_session_token(request) or ''
            return redirect(f'nebians://auth-callback?authToken={linked_token}&isNewUser=false')
        return redirect_result
    auth_token = User.generate_token()
    temp_username = f"github_{github_id[:8]}"
    base_username = temp_username
    suffix = 1
    while User.objects.filter(username=temp_username).exists():
        temp_username = f"{base_username}_{suffix}"
        suffix += 1
    db_user = User(
        pk=user_pk,
        username=temp_username,
        email=email,
        display_name=display_name,
        photo_url=photo_url,
        created_at=int(time.time() * 1000),
    )
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()
    token = auth_token
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    user_data['isNewUser'] = True
    api.set_session_auth(request, token, user_data)
    logger.info('github_callback: new user created: %s', user_pk)
    if is_mobile:
        return redirect(f'nebians://auth-callback?authToken={auth_token}&isNewUser=true')
    return redirect('web:edit_profile')


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
    token = api.get_session_token(request)
    if token:
        revoke_auth_token(token)
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
        'forum_all_posts', 'forum_contributors', 'admin_stats', 'sitemap_xml',
    ])


@require_POST
def ajax_like_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_post_like(user, post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    cache.delete_many(['home_posts', 'forum_all_posts'])
    return JsonResponse(result)


@require_POST
def ajax_like_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_reply_like(user, reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    return JsonResponse(result)


@require_POST
def ajax_create_reply(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentReplyId')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    if len(content) > 10000:
        return JsonResponse({'error': 'Content must be 10000 characters or fewer'}, status=400)
    result = services.create_reply(user, post_id, content, parent_id)
    if result:
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_like_resource(request, resource_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_resource_like(user, resource_id)
    except Resource.DoesNotExist:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    return JsonResponse(result)


@require_POST
def ajax_like_resource_comment(request, comment_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        result = services.toggle_resource_comment_like(user, comment_id)
    except ResourceComment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    return JsonResponse(result)


@require_POST
def ajax_resource_comment(request, resource_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentCommentId')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    result = services.create_resource_comment(user, resource_id, content, parent_id)
    if result:
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
def ajax_delete_resource_comment(request, comment_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    is_admin = bool(user.is_admin)
    ok = services.delete_resource_comment(user, comment_id, is_admin=is_admin)
    if ok:
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Permission denied or comment not found'}, status=403)


@require_POST
def ajax_create_post(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    category = data.get('category', '').strip()
    if len(title) > 200:
        return JsonResponse({'error': 'Title must be 200 characters or fewer'}, status=400)
    if len(content) > 20000:
        return JsonResponse({'error': 'Content must be 20000 characters or fewer'}, status=400)
    result = services.create_post(user, title, content, category)
    if result:
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Missing fields'}, status=400)


@require_POST
def ajax_bookmark_toggle(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    target_type = data.get('target_type', '').strip()
    target_id = data.get('target_id', '').strip()
    if target_type not in ('post', 'reply', 'resource'):
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    if not target_id:
        return JsonResponse({'error': 'target_id required'}, status=400)
    if target_type == 'post':
        if not Post.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Post not found'}, status=404)
    elif target_type == 'reply':
        if not Reply.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Reply not found'}, status=404)
    elif target_type == 'resource':
        if not Resource.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Resource not found'}, status=404)
    existing = Bookmark.objects.filter(user=user, target_type=target_type, target_id=target_id).first()
    if existing:
        existing.delete()
        return JsonResponse({'isBookmarked': False})
    Bookmark.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        target_type=target_type,
        target_id=target_id,
        created_at=int(time.time() * 1000),
    )
    return JsonResponse({'isBookmarked': True})


@require_POST
def ajax_bookmark_check(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'isBookmarked': False})
    target_type = request.GET.get('target_type', '').strip()
    target_id = request.GET.get('target_id', '').strip()
    is_bookmarked = Bookmark.objects.filter(
        user_id=user_id, target_type=target_type, target_id=target_id
    ).exists()
    return JsonResponse({'isBookmarked': is_bookmarked})


@require_POST
def ajax_report(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    target_type = data.get('target_type', '').strip()
    target_id = data.get('target_id', '').strip()
    reason = data.get('reason', 'other').strip()
    description = data.get('description', '').strip()
    valid_types = {'post', 'reply', 'user', 'resource'}
    if target_type not in valid_types:
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    if not target_id:
        return JsonResponse({'error': 'target_id required'}, status=400)
    if reason not in dict(Report.REASON_CHOICES):
        return JsonResponse({'error': 'Invalid reason'}, status=400)
    if len(description) > 2000:
        return JsonResponse({'error': 'Description must be 2000 characters or fewer'}, status=400)
    report = Report.objects.create(
        id=str(uuid.uuid4()),
        reporter=user,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        description=description,
        status='open',
        created_at=int(time.time() * 1000),
    )
    logger.info("ajax_report: user %s reported %s/%s (reason=%s)", user.username, target_type, target_id, reason)
    return JsonResponse({'success': True, 'id': report.id})


@require_POST
def ajax_archive_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    reply.is_archived = not reply.is_archived
    reply.save(update_fields=['is_archived'])
    _clear_page_cache()
    return JsonResponse({'success': True, 'isArchived': reply.is_archived})


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
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    try:
        _cleanup.delete_post_with_cleanup(post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    _clear_page_cache()
    return JsonResponse({'success': True})


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
    try:
        _cleanup.delete_reply_with_cleanup(reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
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


def ajax_reply_thread(request, reply_id):
    user_id = _get_user_id(request)
    try:
        parent = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    parent_data = _serialize_reply(parent, user_id)
    parent_data['authorFollowed'] = False
    if user_id and parent.user_id != user_id:
        parent_data['authorFollowed'] = Follow.objects.filter(
            follower_id=user_id, following_id=parent.user_id
        ).exists()
    all_descendants = Reply.objects.select_related('user').filter(
        post_id=parent.post_id, parent_reply__isnull=False
    ).order_by('created_at')
    all_replies = _serialize_replies(all_descendants, user_id)
    id_to_reply = {r['id']: r for r in all_replies}
    children_map = {}
    for r in all_replies:
        pid = r['parentReplyId']
        children_map.setdefault(pid, []).append(r)
    def build_tree(parent_id):
        children = children_map.get(parent_id, [])
        for child in children:
            child['children'] = build_tree(child['id'])
        return children
    thread_replies = build_tree(reply_id)
    return JsonResponse({
        'parent': parent_data,
        'replies': thread_replies,
    }, safe=False)


def ajax_user_popup(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    is_private = bool(u.is_locked)
    data = {
        'id': u.id,
        'username': u.username,
        'displayName': u.display_name or u.username,
        'photoUrl': u.photo_url or '',
        'bio': '' if is_private else (u.bio or ''),
        'classLevel': '' if is_private else (u.class_level or ''),
        'isLocked': u.is_locked,
        'badgeInfo': _user_badge_info(u),
    }
    if not is_private:
        data['postCount'] = getattr(u, 'post_count', 0) or 0 or Post.objects.filter(user=u).count()
        data['replyCount'] = getattr(u, 'reply_count', 0) or 0 or Reply.objects.filter(user=u).count()
        data['followerCount'] = getattr(u, 'follower_count', 0) or 0 or Follow.objects.filter(following=u).count()
    else:
        data['postCount'] = 0
        data['replyCount'] = 0
        data['followerCount'] = 0
    user_id = _get_user_id(request)
    if user_id:
        data['isFollowing'] = Follow.objects.filter(follower_id=user_id, following_id=u.id).exists()
        data['isSelf'] = (user_id == u.id)
    else:
        data['isFollowing'] = False
        data['isSelf'] = False
    return JsonResponse(data)


def ajax_user_search(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse([], safe=False)
    users = User.objects.filter(
        username__icontains=q
    ).values('id', 'username', 'display_name', 'photo_url')[:8]
    results = []
    for u in users:
        results.append({
            'id': u['id'],
            'username': u['username'],
            'displayName': u['display_name'] or u['username'],
            'photoUrl': u['photo_url'] or '',
        })
    return JsonResponse(results, safe=False)


def ajax_check_username(request):
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'available': False})
    result = services.check_username_available(username)
    return JsonResponse(result)


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
    user_id_obj = _get_user_id(request)
    if not user_id_obj:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id_obj)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = services.toggle_follow(user, user_id)
    if isinstance(result, tuple):
        return JsonResponse(result[0], status=result[1])
    return JsonResponse(result)


def ajax_user_photos(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)

    from api.models import UserPhoto
    try:
        current_user = get_user_by_auth_token(token)
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
        from django.db import transaction

        file_obj = request.FILES.get('file')
        if file_obj:
            try:
                url = save_profile_image_upload(request, current_user, file_obj)
            except ValidationError as exc:
                return JsonResponse({'error': ' '.join(exc.messages)}, status=400)
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
                url = validate_profile_photo_url(url)
            except ValidationError as exc:
                return JsonResponse({'error': ' '.join(exc.messages)}, status=400)

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
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    password = data.get('password', '')
    if not password or len(password) < 8:
        return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
    result, status_code = services.set_password(user, password)
    if result.get('status') == 'success':
        _clear_page_cache()
        user_data = _normalize_user_data(UserSerializer(user).data)
        user_data['hasPassword'] = True
        api.set_session_auth(request, api.get_session_token(request), user_data)
        return JsonResponse({'status': 'success', 'message': 'Password set successfully'})
    return JsonResponse({'error': result.get('error', 'Failed to set password')}, status=status_code or 400)


@require_POST
def ajax_change_password(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    current_password = data.get('currentPassword', '')
    new_password = data.get('newPassword', '')
    if not current_password or not new_password:
        return JsonResponse({'error': 'Current password and new password are required'}, status=400)
    result, status_code = services.change_password(user, current_password, new_password)
    if result.get('status') == 'success':
        _clear_page_cache()
        new_token = result.get('authToken') or api.get_session_token(request)
        user_data = _normalize_user_data(UserSerializer(user).data)
        api.set_session_auth(request, new_token, user_data)
        return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})
    return JsonResponse({'error': result.get('error', 'Failed to change password')}, status=status_code or 400)






@require_POST
def ajax_activate_photo(request, photo_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    result = services.activate_photo(user, photo_id)
    if result:
        new_url = result.get('photo_url') or result.get('url')
        if new_url:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = new_url
                user_data['photoUrl'] = new_url
                token = api.get_session_token(request)
                if token:
                    api.set_session_auth(request, token, user_data)
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)



# ---------------------------------------------------------------------------
# ADMIN PANEL
# ---------------------------------------------------------------------------

def admin_login(request):
    if _is_staff_admin(request):
        return redirect('web:admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_active and user.is_staff:
            django_login(request, user)
            return redirect('web:admin_dashboard')
        return render(request, 'admin_panel/login.html', {'error': 'Invalid staff credentials'})
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    django_logout(request)
    return redirect('web:admin_login')


def admin_dashboard(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    stats = cache.get('admin_stats')
    if stats is None:
        from django.db.models import Sum
        total_users = User.objects.count()
        total_resources = Resource.objects.count()
        total_posts = Post.objects.count()
        total_replies = Reply.objects.count()
        total_likes = Post.objects.aggregate(total=Sum('thumbs_up_count'))['total'] or 0
        seven_days_ago = int((time.time() - 7 * 86400) * 1000)
        new_users_week = User.objects.filter(created_at__gte=seven_days_ago).count()
        new_posts_week = Post.objects.filter(created_at__gte=seven_days_ago).count()
        stats = {
            'total_users': total_users,
            'total_resources': total_resources,
            'pending_resources': Resource.objects.filter(approval_status='pending').count(),
            'total_posts': total_posts,
            'total_replies': total_replies,
            'total_likes': total_likes,
            'new_users_week': new_users_week,
            'new_posts_week': new_posts_week,
        }
        cache.set('admin_stats', stats, 60)
    return render(request, 'admin_panel/dashboard.html', {
        'is_admin': True,
        'stats': stats,
        'active_page': 'dashboard',
    })


def admin_users(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    users_qs = User.objects.all().order_by('-created_at')
    search = request.GET.get('q', '').strip()
    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search) | Q(email__icontains=search) | Q(display_name__icontains=search)
        )
    paginator = Paginator(users_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    users_data = [UserSerializer(u).data for u in page_obj]
    return render(request, 'admin_panel/users.html', {
        'is_admin': True,
        'users': users_data,
        'page_obj': page_obj,
        'search': search,
        'active_page': 'users',
    })


def admin_user_detail(request, user_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        user_obj = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:admin_users')
    if request.method == 'POST':
        if request.POST.get('_method') == 'delete':
            user_obj.delete()
            return redirect('web:admin_users')
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user_obj.username:
            if User.objects.filter(username=new_username).exclude(pk=user_obj.pk).exists():
                return HttpResponse('Username already taken by another user.', status=409)
            user_obj.username = new_username
        for field in ['email', 'display_name', 'gender', 'class_level', 'subjects', 'pradesh', 'district', 'school', 'bio', 'photo_url', 'banner_url']:
            val = request.POST.get(field, '').strip()
            if val:
                setattr(user_obj, field, val)
        # Allow clearing these explicit-clear fields (e.g. to remove a photo)
        for clearable in ['bio', 'photo_url', 'banner_url']:
            if clearable in request.POST and not request.POST.get(clearable, '').strip():
                setattr(user_obj, clearable, None)
        # Handle direct image uploads (override URL field if a file is provided)
        from api.security import save_profile_image_upload, save_banner_image_upload
        photo_upload = request.FILES.get('photo_upload')
        if photo_upload:
            try:
                user_obj.photo_url = save_profile_image_upload(request, user_obj, photo_upload)
            except Exception as upload_err:
                return HttpResponse(f'Photo upload failed: {upload_err}', status=400)
        banner_upload = request.FILES.get('banner_upload')
        if banner_upload:
            try:
                user_obj.banner_url = save_banner_image_upload(request, user_obj, banner_upload)
            except Exception as upload_err:
                return HttpResponse(f'Banner upload failed: {upload_err}', status=400)
        user_obj.is_locked = request.POST.get('is_locked') == 'on'
        user_obj.verification_level = int(request.POST.get('verification_level', '0'))
        user_obj.moderator_level = int(request.POST.get('moderator_level', '0'))
        user_obj.is_admin = request.POST.get('is_admin') == 'on'
        user_obj.is_bot = request.POST.get('is_bot') == 'on'
        user_obj.achievement_badges = request.POST.get('achievement_badges', '')
        user_obj.save()
    user_data = UserSerializer(user_obj).data
    achievement_badges_list = _user_achievement_badges(user_obj)
    return render(request, 'admin_panel/user_detail.html', {
        'is_admin': True,
        'user_detail': user_data,
        'achievement_badges_list': achievement_badges_list,
        'active_page': 'users',
    })


def admin_resources(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subject = request.POST.get('subject', '').strip()
        grade_level = request.POST.get('grade_level', '').strip()
        rtype = request.POST.get('type', '').strip() or 'PDF'
        file_url = request.POST.get('file_url', '').strip()
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        description = request.POST.get('description', '').strip()
        uploaded_file = request.FILES.get('file')

        file_path = ''
        file_size = 0
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp:
                file_path = path or ''
                file_size = size
                file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path) if file_path else ''

        if title and subject and (file_path or file_url):
            try:
                from api.security import validate_resource_file_url as _validate
                safe_url = ''
                if file_url and not file_path:
                    safe_url = _validate(file_url)
                elif file_url:
                    safe_url = file_url
                safe_thumb = ''
                if thumbnail_url:
                    safe_thumb = _validate(thumbnail_url)
                Resource.objects.create(
                    id=str(uuid.uuid4()),
                    title=title,
                    description=description,
                    subject=subject,
                    grade_level=grade_level,
                    faculty=request.POST.get('faculty', '').strip(),
                    program=request.POST.get('program', '').strip(),
                    year=request.POST.get('year', '').strip(),
                    exam_type=request.POST.get('exam_type', '').strip(),
                    pradesh=request.POST.get('pradesh', '').strip(),
                    district=request.POST.get('district', '').strip(),
                    school=request.POST.get('school', '').strip(),
                    tags=request.POST.get('tags', '').strip(),
                    type=rtype,
                    file=file_path or None,
                    file_url=safe_url,
                    thumbnail_url=safe_thumb,
                    file_size=file_size or int(request.POST.get('file_size', '0')),
                    added_at=int(time.time() * 1000),
                    view_count=0,
                )
            except Exception:
                pass
    resources_qs = Resource.objects.all().order_by('-added_at')
    search = request.GET.get('q', '').strip()
    if search:
        resources_qs = resources_qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    paginator = Paginator(resources_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    resources_data = [ResourceSerializer(r).data for r in page_obj]
    return render(request, 'admin_panel/resources.html', {
        'is_admin': True,
        'resources': resources_data,
        'page_obj': page_obj,
        'search': search,
        'active_page': 'resources',
    })


def admin_resource_edit(request, resource_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        resource_obj = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return redirect('web:admin_resources')
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp and path:
                resource_obj.file = path
                resource_obj.file_url = request.build_absolute_uri(settings.MEDIA_URL + path)
                resource_obj.file_size = size
        for field in ['title', 'description', 'subject', 'grade_level', 'faculty', 'program', 'year', 'exam_type', 'pradesh', 'district', 'school', 'tags', 'type', 'author_name', 'source_url', 'source_label']:
            setattr(resource_obj, field, request.POST.get(field, '').strip())
        resource_obj.file_url = request.POST.get('file_url', '').strip()
        resource_obj.thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        st = request.POST.get('source_type', '').strip()
        if st in ('admin', 'user', 'anonymous', 'external'):
            resource_obj.source_type = st
        if request.POST.get('view_count', '').strip():
            resource_obj.view_count = int(request.POST.get('view_count', '0'))
        resource_obj.save()
        cache.delete_many(['home_resources', 'library_all_resources'])
        return redirect('web:admin_resources')
_default_subjects = [
        'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
        'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
        'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
        'Environment Science', 'Science', 'General Science', 'Life Science',
        'Physical Science', 'Earth Science', 'Applied Mathematics',
        'Business Mathematics', 'Statistics', 'Probability',
        'Microeconomics', 'Macroeconomics',
        'Financial Accounting', 'Cost Accounting', 'Auditing',
        'Marketing', 'Office Management', 'Hotel Management',
        'Computer Engineering', 'Electronics', 'Electrical Engineering',
        'Civil Engineering', 'Mechanical Engineering', 'Architecture',
        'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Botany', 'Zoology', 'Genetics', 'Ecology',
        'English Grammar', 'English Literature', 'Creative Writing',
        'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
        'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
        'Education', 'Pedagogy', 'Curriculum Development',
        'Law', 'Constitutional Law', 'International Law',
        'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
        'Agriculture', 'Forestry', 'Veterinary Science',
        'Management', 'Human Resource Management', 'Entrepreneurship',
        'Information Technology', 'Programming', 'Web Development',
        'Database Management', 'Networking', 'Cybersecurity',
        'Machine Learning', 'Artificial Intelligence', 'Data Science',
        'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
        'Digital Logic', 'Operating Systems', 'Software Engineering',
        'Surveying', 'Estimating & Costing', 'Building Construction',
        'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
        'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
    ]
    db_subjects = []
    for s_str in Resource.objects.values_list('subject', flat=True):
        if s_str:
            for s in s_str.split(','):
                s_stripped = s.strip()
                if s_stripped:
                    db_subjects.append(s_stripped)
    subjects = sorted(set(_default_subjects + db_subjects))
    common_tags = [
        'NEB', 'SEE', 'Board Exam', 'Past Paper', 'Model Paper', 'Solution',
        'Important Questions', 'Numerical', 'Derivation', 'Formula Sheet',
        'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5',
        'Chapter 6', 'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10',
        'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5',
        'Class 11', 'Class 12', 'Grade 11', 'Grade 12',
        'Science', 'Management', 'Humanities', 'Education', 'Law',
        'Final Exam', 'Midterm', 'Internal Assessment', 'Practical',
        'Old Course', 'New Course', 'Revised Syllabus', 'Curriculum',
        'Textbook', 'Reference Book', 'Guide', 'Notes', 'Summary',
        'Objective Questions', 'Subjective Questions', 'MCQ', 'Long Answer',
        'Short Answer', 'Very Short Answer', 'Essay Type',
        '2080 BS', '2081 BS', '2082 BS', '2079 BS',
        '2078 BS', '2077 BS', '2076 BS',
        'Kathmandu', 'Pokhara', 'Chitwan', 'Biratnagar', 'Butwal',
        'HSEB', 'TU', 'KU', 'PU', 'CTEVT',
        'Entrance', 'IOE', 'IOM', 'CEEE', 'KUUMAT',
        'C Programming', 'Python', 'Java', 'Web Development',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Mechanics', 'Optics', 'Thermodynamics', 'Electricity',
        'Calculus', 'Algebra', 'Trigonometry', 'Geometry', 'Statistics',
        'Botany', 'Zoology', 'Ecology', 'Genetics',
        'Nepali', 'English', 'Social Studies',
    ]
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    exam_types = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']
    pradesh_options = [
        'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
    ]
    resource_types = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']
    from api.serializers import ResourceSerializer
    resource_data = ResourceSerializer(resource_obj).data
    return render(request, 'admin_panel/resource_edit.html', {
        'is_admin': True,
        'resource': resource_data,
        'active_page': 'resources',
        'source_types': Resource.SOURCE_TYPES,
        'subjects': subjects,
        'common_tags': common_tags,
        'education_levels': education_levels,
        'exam_types': exam_types,
        'pradesh_options': pradesh_options,
        'resource_types': resource_types,
    })


@require_POST
def admin_resource_delete(request, resource_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        Resource.objects.get(pk=resource_id).delete()
    except Resource.DoesNotExist:
        pass
    return redirect('web:admin_resources')


def admin_posts(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    posts_qs = Post.objects.select_related('user').all().order_by('-created_at')
    search = request.GET.get('q', '').strip()
    if search:
        posts_qs = posts_qs.filter(Q(title__icontains=search) | Q(content__icontains=search))
    paginator = Paginator(posts_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    posts_data = [PostSerializer(p, context={}).data for p in page_obj]
    return render(request, 'admin_panel/posts.html', {
        'is_admin': True,
        'posts': posts_data,
        'page_obj': page_obj,
        'search': search,
        'active_page': 'posts',
    })


def admin_post_detail(request, post_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        post_obj = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        return redirect('web:admin_posts')
    from api.serializers import PostSerializer, ReplySerializer
    post_data = PostSerializer(post_obj, context={}).data
    replies_qs = Reply.objects.filter(post_id=post_id).select_related('user')
    replies_data = [ReplySerializer(r, context={}).data for r in replies_qs]
    return render(request, 'admin_panel/post_detail.html', {
        'is_admin': True,
        'post': post_data,
        'replies': replies_data,
        'active_page': 'posts',
    })


@require_POST
def admin_post_delete(request, post_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        Post.objects.get(pk=post_id).delete()
    except Post.DoesNotExist:
        pass
    return redirect('web:admin_posts')


@require_POST
def admin_reply_delete(request, reply_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        reply = Reply.objects.get(pk=reply_id)
        post_id = reply.post_id
        reply.delete()
        Post.objects.filter(pk=post_id, reply_count__gt=0).update(reply_count=F('reply_count') - 1)
    except Reply.DoesNotExist:
        pass
    return redirect('web:admin_posts')


# ---------------------------------------------------------------------------
# NOTIFICATIONS (web views)
# ---------------------------------------------------------------------------

def notifications(request):
    """Full-page notification center."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    notifs = Notification.objects.filter(recipient_id=user_id).select_related('actor')[:50]
    VERB_LABELS = {
        'like_post': 'liked your post',
        'like_reply': 'liked your reply',
        'like_resource': 'liked your resource',
        'like_resource_comment': 'liked your comment',
        'reply': 'replied to your post',
        'reply_reply': 'replied to your comment',
        'resource_comment': 'commented on your resource',
        'resource_comment_reply': 'replied to your comment',
        'follow': 'started following you',
        'mention': 'mentioned you',
        'resource_approved': '',
        'resource_rejected': '',
        'system': '',
    }
    notif_data = []
    for n in notifs:
        actor_name = n.actor.username if n.actor else None
        safe_actor_name = escape(actor_name) if actor_name else None
        actor_photo = n.actor.photo_url if n.actor else None
        actor_id_val = n.actor_id if n.actor else None
        actor_badge = _user_badge_info(n.actor) if n.actor else None
        verb_label = VERB_LABELS.get(n.verb, n.verb)
        if n.verb == 'system':
            text = escape(n.message or 'System notification')
        elif safe_actor_name:
            text = f'<strong>{safe_actor_name}</strong> <span class="notif-verb">{escape(verb_label)}</span>'
        else:
            text = f'<span class="notif-verb">{escape(verb_label)}</span>'
        url = '#'
        if n.verb == 'follow' and actor_name:
            url = f'/profile/{actor_name}/'
        elif n.verb in ('resource_approved', 'resource_rejected') and n.target_type == 'resource' and n.target_id:
            url = f'/resource/{n.target_id}/'
        elif n.target_type == 'resource' or n.reference_type == 'resource':
            resource_id = n.target_id if n.target_type == 'resource' else n.reference_id
            url = f'/resource/{resource_id}/'
        elif n.target_type == 'resource_comment':
            resource_id = n.reference_id if n.reference_type == 'resource' else ''
            if resource_id:
                url = f'/resource/{resource_id}/'
        elif n.target_type == 'post' or n.reference_type == 'post':
            post_id = n.target_id if n.target_type == 'post' else n.reference_id
            url = f'/forum/post/{post_id}/'
        elif n.target_type == 'reply':
            post_id = n.reference_id if n.reference_type == 'post' else ''
            if post_id:
                url = f'/forum/post/{post_id}/'
        notif_data.append({
            'id': n.id,
            'verb': n.verb,
            'targetType': n.target_type,
            'targetId': n.target_id,
            'referenceType': n.reference_type,
            'referenceId': n.reference_id,
            'message': n.message,
            'isRead': n.is_read,
            'createdAt': n.created_at,
            'actorName': actor_name,
            'actorPhotoUrl': actor_photo,
            'actorId': actor_id_val,
            'actorBadgeInfo': actor_badge,
            'text': text,
            'url': url,
        })
    return render(request, 'web/notifications.html', _ctx(request, notifications=notif_data))


def ajax_notifications(request):
    """AJAX: list notifications for current user."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    offset = (page - 1) * page_size
    notifs = Notification.objects.filter(recipient_id=user_id).select_related('actor').order_by('-created_at')
    total = notifs.count()
    notifs_page = notifs[offset:offset + page_size]
    results = []
    for n in notifs_page:
        actor_badge = _user_badge_info(n.actor) if n.actor else None
        results.append({
            'id': n.id,
            'verb': n.verb,
            'targetType': n.target_type,
            'targetId': n.target_id,
            'referenceType': n.reference_type,
            'referenceId': n.reference_id,
            'message': n.message,
            'isRead': n.is_read,
            'createdAt': n.created_at,
            'actorName': n.actor.username if n.actor else None,
            'actorPhotoUrl': n.actor.photo_url if n.actor else None,
            'actorId': n.actor_id if n.actor else None,
            'actorBadgeInfo': actor_badge,
        })
    return JsonResponse({
        'results': results,
        'total': total,
        'page': page,
        'hasMore': (offset + page_size) < total,
    })


@require_POST
def ajax_notifications_mark_read(request):
    """AJAX: mark specific or all notifications as read."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}
    mark_all = data.get('mark_all', False)
    notification_ids = data.get('notification_ids', [])
    if mark_all:
        count = Notification.objects.filter(recipient_id=user_id, is_read=False).update(is_read=True)
        _counters.reset_user_unread_notification_count(user_id)
        return JsonResponse({'success': True, 'marked_count': count})
    if notification_ids:
        notifs = Notification.objects.filter(recipient_id=user_id, pk__in=notification_ids, is_read=False)
        count = notifs.update(is_read=True)
        unread = Notification.objects.filter(recipient_id=user_id, is_read=False).count()
        User.objects.filter(pk=user_id).update(unread_notification_count=unread)
        return JsonResponse({'success': True, 'marked_count': count})
    return JsonResponse({'error': 'Provide notification_ids or mark_all=true'}, status=400)


def ajax_notifications_unread_count(request):
    """AJAX: get unread notification count for current user."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'count': 0})
    try:
        user = User.objects.get(pk=user_id)
        count = getattr(user, 'unread_notification_count', 0) or 0
    except User.DoesNotExist:
        count = 0
    return JsonResponse({'count': count})


def sitemap_xml(request):
    """
    Generates a dynamic XML sitemap listing the homepage, library, forum,
    and all public resources and forum posts dynamically from the database.
    Cached for 1 hour.
    """
    sitemap_content = cache.get('sitemap_xml')
    if sitemap_content is not None:
        return HttpResponse(sitemap_content, content_type='application/xml')

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
        ts = r.updated_at if hasattr(r, 'updated_at') and r.updated_at else r.added_at
        if isinstance(ts, int) and ts:
            lastmod = timezone.datetime.fromtimestamp(ts / 1000, tz=timezone.get_current_timezone()).isoformat()
        elif hasattr(ts, 'isoformat') and ts:
            lastmod = ts.isoformat()
        else:
            lastmod = now
        urls.append({
            'loc': f'{base}/reader/{r.id}/',
            'changefreq': 'weekly',
            'priority': '0.6',
            'lastmod': lastmod,
        })

    for p in Post.objects.filter(is_archived=False).select_related('user')[:500]:
        ts = p.created_at
        if isinstance(ts, int) and ts:
            lastmod = timezone.datetime.fromtimestamp(ts / 1000, tz=timezone.get_current_timezone()).isoformat()
        elif hasattr(ts, 'isoformat') and ts:
            lastmod = ts.isoformat()
        else:
            lastmod = now
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

    cache.set('sitemap_xml', xml_content, 3600)
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


def admin_bot_config(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    config = BotConfig.get_config()
    if request.method == 'POST':
        config.enabled = request.POST.get('enabled') == 'on'
        config.bot_username = request.POST.get('bot_username', config.bot_username).strip() or 'neby'
        config.api_url = request.POST.get('api_url', config.api_url).strip()
        config.api_key = request.POST.get('api_key', config.api_key).strip()
        config.model = request.POST.get('model', config.model).strip() or 'qwen3.6-plus'
        config.system_prompt = request.POST.get('system_prompt', config.system_prompt).strip()
        try:
            config.max_context_posts = int(request.POST.get('max_context_posts', config.max_context_posts))
        except (TypeError, ValueError):
            pass
        try:
            config.max_context_replies = int(request.POST.get('max_context_replies', config.max_context_replies))
        except (TypeError, ValueError):
            pass
        try:
            config.response_max_length = int(request.POST.get('response_max_length', config.response_max_length))
        except (TypeError, ValueError):
            pass
config.save()
        from django.core.cache import cache
        cache.delete('neby_enabled')
        messages.success(request, 'Bot configuration updated.')
        return redirect('/admin/bot/')
    bot_user = BotConfig.get_bot_user()
    ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user)
    return render(request, 'admin_panel/bot_config.html', ctx)
