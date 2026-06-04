import json
import logging
import os
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
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, Http404, HttpResponse, StreamingHttpResponse
from . import curriculum
from django.core.paginator import Paginator
from django.utils.html import escape

from api.models import User, Resource, ResourceRequest, ResourceRequestUpvote, Post, PostLike, Reply, ReplyLike, Follow, UserPhoto, EditHistory, Bookmark, Notification, Report, BotConfig, TakedownRequest
from api.models import ResourceLike, ResourceComment, ResourceCommentLike
from api.serializers import UserSerializer, ResourceSerializer, PostSerializer, ReplySerializer
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
from api import realtime as _rt
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
    if getattr(user, 'class_level', '') == 'Teacher':
        badge['type'] = 'teacher'
        badge['icon'] = 'school'
        badge['color'] = '#10B981'
        badge['label'] = 'Teacher'
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
        'viewCount': p.view_count, 'view_count': p.view_count,
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
            'viewCount': r.view_count,
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
        'viewCount': r.view_count,
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


def _get_ws_public_url():
    """Return the public WebSocket URL for clients to connect to.

    Priority:
      1. WS_PUBLIC_URL env var (explicit override)
      2. The current trycloudflare.com URL (read from /tmp/cf_quick*.log)
         — used when running behind a Cloudflare quick tunnel.
      3. Empty string (realtime.js falls back to same-origin /ws/).
    """
    explicit = os.environ.get('WS_PUBLIC_URL', '').strip()
    if explicit:
        return explicit
    try:
        import glob
        for path in sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True):
            try:
                with open(path) as f:
                    content = f.read()
                import re
                m = re.search(r'https://([a-z0-9-]+\.trycloudflare\.com)', content)
                if m:
                    url = 'wss://' + m.group(1) + '/ws/'
                    return url
            except OSError:
                continue
    except Exception:  # noqa: BLE001
        pass
    return ''


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
    ws_url = _get_ws_public_url()
    # When using a cross-domain tunnel (trycloudflare.com), the browser cannot
    # send the session cookie cross-domain. Append the auth token as a query
    # param so JWTAuthMiddleware can authenticate the WS connection.
    if ws_url and token and 'trycloudflare.com' in ws_url:
        separator = '&' if '?' in ws_url else '?'
        ws_url = f'{ws_url}{separator}token={token}'
    ctx = {
        'is_authenticated': bool(token),
        'user': user,
        'dark_mode': dark_mode,
        'unread_notifications': unread_notifications,
        'csp_nonce': getattr(request, 'csp_nonce', ''),
        'ws_url': ws_url,
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
        resources = _serialize_resources(Resource.objects.filter(approval_status='approved', is_lead=True)[:50])
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
    current_tab = request.GET.get('tab', 'digital')
    if current_tab not in ['digital', 'community', 'categories']:
        current_tab = 'digital'

    filtered = []
    page_obj = None

    if current_tab in ['digital', 'community']:
        is_lead_val = (current_tab == 'digital')
        qs = Resource.objects.filter(approval_status='approved', is_lead=is_lead_val)
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

    # Build Class syllabus category tree dynamically from SyllabusContent
    from collections import defaultdict
    from api.models import SyllabusContent
    categories_map = defaultdict(set)
    active_syllabus = SyllabusContent.objects.all().values('grade_level', 'subject')
    
    if active_syllabus.exists():
        for item in active_syllabus:
            grade = item['grade_level'].strip() if item['grade_level'] else ''
            if grade.lower() == 'grade 12':
                grade = 'Class 12'
            elif grade.lower() == 'grade 11':
                grade = 'Class 11'
            subject_str = item['subject']
            if grade and subject_str:
                for s in subject_str.split(','):
                    s_clean = s.strip()
                    if s_clean:
                        categories_map[grade].add(s_clean)
    else:
        # Fallback to CURRICULUM_MAP keys
        for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
            categories_map[g_val].add(s_val)
                    
    grade_order = {val: i for i, val in enumerate(education_levels)}
    categories_list = []
    for grade, subjs in categories_map.items():
        subjs_sorted = sorted(list(subjs))
        subjs_list = []
        for s in subjs_sorted:
            grade_slug = grade.lower().replace(' / see', '-see').replace(' ', '-')
            subject_slug = s.lower().replace(' ', '-')
            subjs_list.append({
                'name': s,
                'slug': subject_slug,
                'url': f"/subject/{grade_slug}/{subject_slug}/"
            })
        categories_list.append({
            'grade': grade,
            'subjects': subjs_list,
            'order': grade_order.get(grade, 999)
        })
    categories_list.sort(key=lambda x: x['order'])

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
        current_tab=current_tab,
        page_obj=page_obj,
        categories_list=categories_list,
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
        import re
        import operator
        from functools import reduce
        from django.db.models import Value, BooleanField, Case, When

        terms = [t for t in re.sub(r'[^\w\s]', ' ', query).split() if t]
        if terms:
            res_q_list = []
            for term in terms:
                res_q_list.append(
                    Q(title__icontains=term) | Q(description__icontains=term) | Q(subject__icontains=term) |
                    Q(faculty__icontains=term) | Q(program__icontains=term) | Q(school__icontains=term) | Q(tags__icontains=term)
                )
            resource_qs = Resource.objects.filter(
                reduce(operator.and_, res_q_list),
                approval_status='approved',
                is_lead=True
            )
            exact_res_expr = Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__icontains=query) | Q(tags__icontains=query)
            resource_qs = resource_qs.annotate(
                is_exact=Case(
                    When(exact_res_expr, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).order_by('-is_exact', '-added_at')

            post_q_list = []
            for term in terms:
                post_q_list.append(
                    Q(title__icontains=term) | Q(content__icontains=term)
                )
            post_qs = Post.objects.select_related('user').filter(
                reduce(operator.and_, post_q_list)
            ).filter(is_archived=False)
            exact_post_expr = Q(title__icontains=query) | Q(content__icontains=query)
            post_qs = post_qs.annotate(
                is_exact=Case(
                    When(exact_post_expr, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).order_by('-is_exact', '-created_at')
        else:
            resource_qs = Resource.objects.none()
            post_qs = Post.objects.none()

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
    view_key = f'post_viewed_{post_id}'
    if not request.session.get(view_key):
        Post.objects.filter(pk=post_id).update(view_count=F('view_count') + 1)
        request.session[view_key] = True
        post_obj.view_count += 1
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

    # Fetch bundle files if it belongs to a group
    group_resources = []
    if resource_obj.upload_group_id:
        group_qs = Resource.objects.filter(
            upload_group_id=resource_obj.upload_group_id
        ).order_by('added_at')
        # Include resources that are pending or approved for staff, but only approved for normal users
        if not _is_staff_admin(request):
            group_qs = group_qs.filter(approval_status='approved')
        group_resources = _serialize_resources(group_qs)

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
        group_resources=group_resources,
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
        'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
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

        uploaded_files = request.FILES.getlist('file')
        file_url = request.POST.get('file_url', '').strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not subject:
            errors.append('Subject is required.')
        if not uploaded_files and not file_url:
            errors.append('Please upload a file or provide a file URL.')

        saved_files = []
        if uploaded_files:
            for f in uploaded_files:
                path, size, err_resp = validate_and_save_resource_file(request, f)
                if err_resp:
                    errors.append(f"{f.name}: {err_resp['error']}")
                else:
                    saved_files.append({
                        'path': path or '',
                        'size': size,
                        'name': f.name
                    })

            # If there were errors, clean up any successfully saved files
            if errors:
                from django.core.files.storage import default_storage
                for sf in saved_files:
                    if sf['path']:
                        try:
                            default_storage.delete(sf['path'])
                        except Exception:
                            pass

        safe_file_url = ''
        if not uploaded_files and file_url:
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
            created_resources = []
            if saved_files:
                import os
                from django.conf import settings
                
                group_id = str(uuid.uuid4()) if len(saved_files) > 1 else ''
                
                for idx, sf in enumerate(saved_files):
                    res_title = title
                    is_lead = True
                    if len(saved_files) > 1:
                        if idx > 0:
                            is_lead = False
                            display_name = os.path.splitext(sf['name'])[0]
                            res_title = f"{title} - {display_name}"

                    final_file_url = request.build_absolute_uri(settings.MEDIA_URL + sf['path'])
                    resource = Resource(
                        id=str(uuid.uuid4()),
                        title=res_title,
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
                        file=sf['path'] or None,
                        file_url=final_file_url,
                        thumbnail_url=safe_thumbnail_url,
                        file_size=sf['size'],
                        added_at=int(time.time() * 1000) + idx,
                        author_name=author_name,
                        source_type='user' if user else 'anonymous',
                        uploaded_by=user,
                        source_url=source_url,
                        source_label=source_label,
                        approval_status='pending',
                        upload_group_id=group_id,
                        is_lead=is_lead,
                    )
                    resource.save()
                    created_resources.append(resource)
            else:
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
                    file=None,
                    file_url=final_file_url,
                    thumbnail_url=safe_thumbnail_url,
                    file_size=int(request.POST.get('file_size', '0')),
                    added_at=int(time.time() * 1000),
                    author_name=author_name,
                    source_type='user' if user else 'anonymous',
                    uploaded_by=user,
                    source_url=source_url,
                    source_label=source_label,
                    approval_status='pending',
                    upload_group_id='',
                    is_lead=True,
                )
                resource.save()
                created_resources.append(resource)

            cache.delete_many(['home_resources', 'library_all_resources'])
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect': reverse('web:upload_success')})
            return render(request, 'web/upload_success.html', _ctx(request,
                resource=_serialize_resource(created_resources[0]),
                is_anonymous=not bool(user),
                count=len(created_resources),
            ))

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

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


def upload_success(request):
    return render(request, 'web/upload_success.html', _ctx(request))


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
        'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
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
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'redirect': reverse('web:reader', kwargs={'resource_id': resource_id})})
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
            
            # Identify all resources in the same upload group (or just the resource itself if no group)
            if resource_obj.upload_group_id:
                group_resources = Resource.objects.filter(upload_group_id=resource_obj.upload_group_id)
            else:
                group_resources = [resource_obj]

            if action == 'approve':
                for r in group_resources:
                    r.approval_status = 'approved'
                    r.reviewed_by = admin_user
                    r.reviewed_at = int(time.time() * 1000)
                    r.rejection_reason = ''
                    r.save()
                    if r.uploaded_by_id:
                        _counters.increment_user_resource_approved(r.uploaded_by_id)
                        _notif.notify_resource_approved(r.id, r.uploaded_by_id)
            elif action == 'reject':
                reason = request.POST.get('reason', '').strip()[:500]
                for r in group_resources:
                    r.approval_status = 'rejected'
                    r.reviewed_by = admin_user
                    r.reviewed_at = int(time.time() * 1000)
                    r.rejection_reason = reason
                    r.save()
                    if r.uploaded_by_id:
                        _notif.notify_resource_rejected(r.id, r.uploaded_by_id, reason)
            
            cache.delete_many(['home_resources', 'library_all_resources'])
        except Resource.DoesNotExist:
            pass
        return redirect('web:admin_pending_resources')

    pending = Resource.objects.filter(approval_status='pending').order_by('added_at')
    
    # Group the pending resources by upload_group_id to show them as a single request card
    grouped_pending = []
    seen_groups = set()
    
    for r in pending:
        if r.upload_group_id:
            if r.upload_group_id in seen_groups:
                continue
            seen_groups.add(r.upload_group_id)
            
            # Fetch all pending resources in this group
            group_members = list(Resource.objects.filter(
                upload_group_id=r.upload_group_id, 
                approval_status='pending'
            ).order_by('added_at'))
            
            if not group_members:
                continue
                
            lead_r = next((m for m in group_members if m.is_lead), group_members[0])
            lead_data = _serialize_resource(lead_r)
            
            # List all file details in this group
            lead_data['group_files'] = [
                {
                    'id': m.id,
                    'title': m.title,
                    'file_url': m.file.url if m.file else m.file_url,
                    'file_name': os.path.basename(m.file.name) if m.file else 'External URL'
                } for m in group_members
            ]
            grouped_pending.append(lead_data)
        else:
            data = _serialize_resource(r)
            data['group_files'] = [
                {
                    'id': r.id,
                    'title': r.title,
                    'file_url': r.file.url if r.file else r.file_url,
                    'file_name': os.path.basename(r.file.name) if r.file else 'External URL'
                }
            ]
            grouped_pending.append(data)

    return render(request, 'admin_panel/pending_resources.html', {
        'is_admin': True,
        'pending_resources': grouped_pending,
        'active_page': 'pending_resources',
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
    profile_incomplete = not db_user.display_name or not db_user.gender or not db_user.class_level
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
    return render(request, 'web/edit_profile.html', _ctx(request, has_password=has_password, profile_incomplete=profile_incomplete, subjects=subjects))


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------

def login_page(request):
    if api.get_session_token(request):
        return redirect('web:home')
    stats = cache.get('login_stats')
    if stats is None:
        from django.db.models import Sum
        total_resources = Resource.objects.filter(approval_status='approved').count()
        total_users = User.objects.count()
        total_posts = Post.objects.filter(is_archived=False).count()
        recent_resources = list(Resource.objects.filter(approval_status='approved').select_related('uploaded_by').order_by('-added_at')[:3].values('title', 'subject', 'type', 'added_at'))
        for r in recent_resources:
            r['type_label'] = dict(Resource.EXAM_TYPES).get(r.get('type', ''), r.get('type', 'PDF'))
        stats = {
            'total_resources': total_resources,
            'total_users': total_users,
            'total_posts': total_posts,
            'recent_resources': recent_resources,
        }
        cache.set('login_stats', stats, 300)
    return render(request, 'web/login.html', _ctx(request, login_stats=stats))


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
    return redirect('/login/?panel=email-signup')


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


def copyright_takedown(request):
    errors = {}
    success = False
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        organization = request.POST.get('organization', '').strip()
        infringing_url = request.POST.get('infringing_url', '').strip()
        proof_of_ownership = request.POST.get('proof_of_ownership', '').strip()
        statement_good_faith = request.POST.get('statement_good_faith') == 'on'
        statement_accurate = request.POST.get('statement_accurate') == 'on'
        signature = request.POST.get('signature', '').strip()
        
        # Validations
        if not name:
            errors['name'] = 'Full Name is required.'
        if not email:
            errors['email'] = 'Email Address is required.'
        if not infringing_url:
            errors['infringing_url'] = 'Infringing URL on NEBians is required.'
        if not proof_of_ownership:
            errors['proof_of_ownership'] = 'Please describe the copyrighted work and proof of ownership.'
        if not statement_good_faith:
            errors['statement_good_faith'] = 'You must check this box to confirm good faith belief.'
        if not statement_accurate:
            errors['statement_accurate'] = 'You must check this box to confirm accuracy.'
        if not signature:
            errors['signature'] = 'Electronic signature signature is required.'
            
        if not errors:
            # Save the takedown request
            takedown = TakedownRequest(
                id=uuid.uuid4().hex,
                name=name,
                email=email,
                organization=organization,
                infringing_url=infringing_url,
                proof_of_ownership=proof_of_ownership,
                statement_good_faith=statement_good_faith,
                statement_accurate=statement_accurate,
                signature=signature,
                status='open',
                created_at=int(time.time() * 1000)
            )
            takedown.save()
            success = True
            
    ctx = _ctx(request)
    ctx.update({
        'errors': errors,
        'success': success,
        'form_data': request.POST if request.method == 'POST' and not success else {}
    })
    return render(request, 'web/takedown.html', ctx)



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
    _rt.broadcast_reply_deleted(reply.post_id, reply_id, deleted_by='archive')
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
    _rt.broadcast_post_deleted(post_id)
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
    _rt.broadcast_post_updated(post.id, {
        'title': post.title, 'content': post.content, 'category': post.category,
        'is_edited': True, 'edited_at': now,
    })
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
    _rt.broadcast_post_deleted(post_id)
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
    _rt.broadcast_reply_updated(reply.post_id, reply.id, {
        'content': reply.content, 'is_edited': True, 'edited_at': now,
    })
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
    _rt.broadcast_reply_deleted(reply.post_id, reply_id, deleted_by=str(user_id))
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
        from django.db.models import Sum, Count, Avg
        now_ms = int(time.time() * 1000)
        seven_days_ago = int((time.time() - 7 * 86400) * 1000)
        thirty_days_ago = int((time.time() - 30 * 86400) * 1000)

        total_users = User.objects.count()
        total_resources = Resource.objects.count()
        total_posts = Post.objects.count()
        total_replies = Reply.objects.count()
        total_likes = Post.objects.aggregate(total=Sum('thumbs_up_count'))['total'] or 0
        total_reply_likes = Reply.objects.aggregate(total=Sum('thumbs_up_count'))['total'] or 0
        total_resource_views = Resource.objects.aggregate(total=Sum('view_count'))['total'] or 0
        total_post_views = Post.objects.aggregate(total=Sum('view_count'))['total'] or 0
        pending_resources = Resource.objects.filter(approval_status='pending').count()
        new_users_week = User.objects.filter(created_at__gte=seven_days_ago).count()
        new_users_month = User.objects.filter(created_at__gte=thirty_days_ago).count()
        new_posts_week = Post.objects.filter(created_at__gte=seven_days_ago).count()
        new_posts_month = Post.objects.filter(created_at__gte=thirty_days_ago).count()
        new_replies_week = Reply.objects.filter(created_at__gte=seven_days_ago).count()
        new_replies_month = Reply.objects.filter(created_at__gte=thirty_days_ago).count()
        new_resources_week = Resource.objects.filter(added_at__gte=seven_days_ago).count()
        new_resources_month = Resource.objects.filter(added_at__gte=thirty_days_ago).count()

        recent_users = list(User.objects.order_by('-created_at')[:10])
        top_posts = list(Post.objects.select_related('user').filter(is_archived=False).order_by('-thumbs_up_count')[:10])
        top_viewed_posts = list(Post.objects.select_related('user').filter(is_archived=False).order_by('-view_count')[:10])
        top_viewed_resources = list(Resource.objects.filter(approval_status='approved').order_by('-view_count')[:10])
        subject_counts_raw = Resource.objects.filter(approval_status='approved').values_list('subject').annotate(count=Count('id'))
        subject_counts_split = {}
        for subj_str, cnt in subject_counts_raw:
            for s in (subj_str or '').split(','):
                s = s.strip()
                if s:
                    subject_counts_split[s] = subject_counts_split.get(s, 0) + cnt
        subject_counts = dict(sorted(subject_counts_split.items(), key=lambda x: x[1], reverse=True)[:15])
        category_counts = dict(Post.objects.filter(is_archived=False).values_list('category').annotate(count=Count('id')).order_by('-count')[:10])
        resource_type_counts = dict(Resource.objects.filter(approval_status='approved').values_list('type').annotate(count=Count('id')).order_by('-count'))

        stats = {
            'total_users': total_users,
            'total_resources': total_resources,
            'total_posts': total_posts,
            'total_replies': total_replies,
            'total_likes': total_likes,
            'total_reply_likes': total_reply_likes,
            'total_resource_views': total_resource_views,
            'total_post_views': total_post_views,
            'pending_resources': pending_resources,
            'new_users_week': new_users_week,
            'new_users_month': new_users_month,
            'new_posts_week': new_posts_week,
            'new_posts_month': new_posts_month,
            'new_replies_week': new_replies_week,
            'new_replies_month': new_replies_month,
            'new_resources_week': new_resources_week,
            'new_resources_month': new_resources_month,
            'recent_users': recent_users,
            'top_posts': top_posts,
            'top_viewed_posts': top_viewed_posts,
            'top_viewed_resources': top_viewed_resources,
            'subject_counts': subject_counts,
            'category_counts': category_counts,
            'resource_type_counts': resource_type_counts,
        }
        cache.set('admin_stats', stats, 300)
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
        tags = request.POST.get('tags', '').strip()
        faculty = request.POST.get('faculty', '').strip()
        program = request.POST.get('program', '').strip()
        year = request.POST.get('year', '').strip()
        exam_type = request.POST.get('exam_type', '').strip()
        pradesh = request.POST.get('pradesh', '').strip()
        district = request.POST.get('district', '').strip()
        school = request.POST.get('school', '').strip()
        author_name = request.POST.get('author_name', '').strip()
        source_url = request.POST.get('source_url', '').strip()
        source_label = request.POST.get('source_label', '').strip()

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
                    file_url=safe_url,
                    thumbnail_url=safe_thumb,
                    file_size=file_size or int(request.POST.get('file_size', '0')),
                    added_at=int(time.time() * 1000),
                    view_count=0,
                    author_name=author_name,
                    source_url=source_url,
                    source_label=source_label,
                )
            except Exception:
                pass
    resources_qs = Resource.objects.all().order_by('-added_at')
    search = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    if search:
        resources_qs = resources_qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if status_filter in ('approved', 'pending', 'rejected'):
        resources_qs = resources_qs.filter(approval_status=status_filter)
    paginator = Paginator(resources_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    resources_data = [ResourceSerializer(r).data for r in page_obj]
    return render(request, 'admin_panel/resources.html', {
        'is_admin': True,
        'resources': resources_data,
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'pending_count': Resource.objects.filter(approval_status='pending').count(),
        'active_page': 'resources',
    })


def admin_resource_create(request):
    """Standalone admin resource creation page — full-featured form matching the public upload page."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

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
        'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
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
        source_type = request.POST.get('source_type', 'admin').strip() or 'admin'
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        view_count = int(request.POST.get('view_count', '0') or '0')
        approval_status = request.POST.get('approval_status', 'approved').strip() or 'approved'

        uploaded_files = request.FILES.getlist('file')
        file_url = request.POST.get('file_url', '').strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not subject:
            errors.append('Subject is required.')
        if not uploaded_files and not file_url:
            errors.append('Please upload a file or provide a file URL.')

        saved_files = []
        if uploaded_files:
            for f in uploaded_files:
                path, size, err_resp = validate_and_save_resource_file(request, f)
                if err_resp:
                    errors.append(f"{f.name}: {err_resp['error']}")
                else:
                    saved_files.append({
                        'path': path or '',
                        'size': size,
                        'name': f.name
                    })

            if errors:
                from django.core.files.storage import default_storage
                for sf in saved_files:
                    if sf['path']:
                        try:
                            default_storage.delete(sf['path'])
                        except Exception:
                            pass

        safe_file_url = ''
        if not uploaded_files and file_url:
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
            if source_type not in ('admin', 'user', 'anonymous', 'external'):
                source_type = 'admin'
            if approval_status not in ('approved', 'pending', 'rejected'):
                approval_status = 'approved'

            admin_user = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
                    admin_user = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    pass

            created_count = 0
            if saved_files:
                import os
                from django.conf import settings
                
                group_id = str(uuid.uuid4()) if len(saved_files) > 1 else ''
                
                for idx, sf in enumerate(saved_files):
                    res_title = title
                    is_lead = True
                    if len(saved_files) > 1:
                        if idx > 0:
                            is_lead = False
                            display_name = os.path.splitext(sf['name'])[0]
                            res_title = f"{title} - {display_name}"

                    final_file_url = request.build_absolute_uri(settings.MEDIA_URL + sf['path'])
                    resource = Resource(
                        id=str(uuid.uuid4()),
                        title=res_title,
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
                        file=sf['path'] or None,
                        file_url=final_file_url,
                        thumbnail_url=safe_thumbnail_url,
                        file_size=sf['size'],
                        added_at=int(time.time() * 1000) + idx,
                        view_count=view_count,
                        author_name=author_name,
                        source_type=source_type,
                        uploaded_by=admin_user,
                        source_url=source_url,
                        source_label=source_label,
                        approval_status=approval_status,
                        reviewed_by=admin_user if approval_status == 'approved' else None,
                        reviewed_at=int(time.time() * 1000) if approval_status == 'approved' else None,
                        upload_group_id=group_id,
                        is_lead=is_lead,
                    )
                    resource.save()
                    created_count += 1
            else:
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
                    file=None,
                    file_url=safe_file_url,
                    thumbnail_url=safe_thumbnail_url,
                    file_size=0,
                    added_at=int(time.time() * 1000),
                    view_count=view_count,
                    author_name=author_name,
                    source_type=source_type,
                    uploaded_by=admin_user,
                    source_url=source_url,
                    source_label=source_label,
                    approval_status=approval_status,
                    reviewed_by=admin_user if approval_status == 'approved' else None,
                    reviewed_at=int(time.time() * 1000) if approval_status == 'approved' else None,
                    upload_group_id='',
                    is_lead=True,
                )
                resource.save()
                created_count += 1

            cache.delete_many(['home_resources', 'library_all_resources'])
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect': reverse('web:admin_resources')})
            return redirect('web:admin_resources')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        return render(request, 'admin_panel/resource_create.html', {
            'is_admin': True,
            'active_page': 'resources',
            'subjects': subjects,
            'education_levels': education_levels,
            'exam_types': exam_types,
            'pradesh_options': pradesh_options,
            'resource_types': resource_types,
            'common_tags': common_tags,
            'source_types': Resource.SOURCE_TYPES,
            'approval_choices': Resource.APPROVAL_CHOICES,
            'errors': errors,
            'form_data': request.POST,
        })

    return render(request, 'admin_panel/resource_create.html', {
        'is_admin': True,
        'active_page': 'resources',
        'subjects': subjects,
        'education_levels': education_levels,
        'exam_types': exam_types,
        'pradesh_options': pradesh_options,
        'resource_types': resource_types,
        'common_tags': common_tags,
        'source_types': Resource.SOURCE_TYPES,
        'approval_choices': Resource.APPROVAL_CHOICES,
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
        new_status = request.POST.get('approval_status', '').strip()
        if new_status in ('approved', 'pending', 'rejected'):
            old_status = resource_obj.approval_status
            resource_obj.approval_status = new_status
            resource_obj.reviewed_by = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
                    resource_obj.reviewed_by = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    pass
            resource_obj.reviewed_at = int(time.time() * 1000)
            if new_status == 'rejected':
                resource_obj.rejection_reason = request.POST.get('rejection_reason', '').strip()[:500]
            else:
                resource_obj.rejection_reason = ''
            if old_status == 'pending' and new_status == 'approved' and resource_obj.uploaded_by_id:
                _counters.increment_user_resource_approved(resource_obj.uploaded_by_id)
                _notif.notify_resource_approved(resource_obj.id, resource_obj.uploaded_by_id)
            elif old_status == 'pending' and new_status == 'rejected' and resource_obj.uploaded_by_id:
                _notif.notify_resource_rejected(resource_obj.id, resource_obj.uploaded_by_id, resource_obj.rejection_reason)
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
        'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
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
    resource_data = ResourceSerializer(resource_obj).data
    resource_data['rejection_reason'] = resource_obj.rejection_reason or ''
    if resource_obj.uploaded_by:
        resource_data['uploaded_by_name'] = resource_obj.uploaded_by.display_name or resource_obj.uploaded_by.username
    else:
        resource_data['uploaded_by_name'] = ''
    return render(request, 'admin_panel/resource_edit.html', {
        'is_admin': True,
        'resource': resource_data,
        'active_page': 'resources',
        'source_types': Resource.SOURCE_TYPES,
        'approval_choices': Resource.APPROVAL_CHOICES,
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
            url = f'/reader/{n.target_id}/'
        elif n.target_type == 'resource' or n.reference_type == 'resource':
            resource_id = n.target_id if n.target_type == 'resource' else n.reference_id
            url = f'/reader/{resource_id}/'
        elif n.target_type == 'resource_comment':
            resource_id = n.reference_id if n.reference_type == 'resource' else ''
            if resource_id:
                url = f'/reader/{resource_id}/'
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
        'Disallow: /logout/',
        'Disallow: /profile/edit/',
        '',
        'Sitemap: https://nebians.consica.com.np/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def custom_404(request, exception):
    return render(request, '404.html', _ctx(request), status=404)


def custom_500(request):
    return render(request, '500.html', _ctx(request), status=500)


def admin_bots(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    bots = BotConfig.objects.all().order_by('id')
    bot_list = []
    for bot in bots:
        bot_user = BotConfig.get_bot_user(bot)
        task_stats = {
            'pending': bot.tasks.filter(status='pending').count(),
            'processing': bot.tasks.filter(status='processing').count(),
            'done': bot.tasks.filter(status='done').count(),
            'failed': bot.tasks.filter(status='failed').count(),
        }
        bot_list.append({
            'config': bot,
            'user': bot_user,
            'task_stats': task_stats,
        })
    ctx = _ctx(request, active_page='bot', bot_list=bot_list)
    return render(request, 'admin_panel/bot_list.html', ctx)


def admin_bot_edit(request, bot_id=None):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    if bot_id:
        config = BotConfig.objects.filter(pk=bot_id).first()
        if not config:
            messages.error(request, 'Bot not found.')
            return redirect('/admin/bots/')
    else:
        config = None

    if request.method == 'POST':
        action = request.POST.get('action', 'save')
        if action == 'delete' and config:
            bot_username = config.bot_username
            config.delete()
            from django.core.cache import cache
            cache.delete('neby_enabled')
            messages.success(request, f'Bot @{bot_username} deleted.')
            return redirect('/admin/bots/')
        if not config:
            config = BotConfig()
        config.enabled = request.POST.get('enabled') == 'on'
        config.name = request.POST.get('name', config.name or 'Neby').strip()[:100] or 'Neby'
        config.bot_username = request.POST.get('bot_username', config.bot_username or 'neby').strip()[:50].lower() or 'neby'
        config.display_name = request.POST.get('display_name', '').strip()[:100]
        config.avatar_url = request.POST.get('avatar_url', '').strip()
        provider = (request.POST.get('provider') or 'qwen').strip().lower()
        if provider not in ('qwen', 'ai4bharat', 'custom'):
            provider = 'qwen'
        config.provider = provider
        config.api_url = request.POST.get('api_url', config.api_url).strip()
        config.api_key = request.POST.get('api_key', config.api_key).strip()
        model = (request.POST.get('model') or '').strip()
        if not model:
            model = (request.POST.get('model_select') or request.POST.get('model_text') or '').strip()
        if model:
            config.model = model[:200]
        elif not config.model:
            config.model = 'qwen3.6-plus'
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
        # Validate bot_username uniqueness
        existing = BotConfig.objects.filter(bot_username__iexact=config.bot_username).exclude(pk=config.pk)
        if existing.exists():
            messages.error(request, f'A bot with username @{config.bot_username} already exists.')
            bot_user = BotConfig.get_bot_user(config) if config.pk else None
            ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user, is_new=not config.pk)
            return render(request, 'admin_panel/bot_edit.html', ctx)
        config.save()
        from django.core.cache import cache
        cache.delete('neby_enabled')
        messages.success(request, f'Bot "@{config.bot_username}" saved. Provider: {provider}.')
        return redirect(f'/admin/bots/{config.pk}/')

    bot_user = BotConfig.get_bot_user(config) if config else None
    ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user, is_new=config is None)
    return render(request, 'admin_panel/bot_edit.html', ctx)


def admin_bot_create_user(request, bot_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    config = BotConfig.objects.filter(pk=bot_id).first()
    if not config:
        messages.error(request, 'Bot not found.')
        return redirect('/admin/bots/')
    existing_user = BotConfig.get_bot_user(config)
    if existing_user:
        messages.info(request, f'User @{config.bot_username} already exists (id={existing_user.id}).')
        return redirect(f'/admin/bots/{bot_id}/')
    if request.method == 'POST':
        username = config.bot_username
        display_name = config.display_name or config.name or username.capitalize()
        user_id = f'{username}-bot'
        try:
            bot_user = User.objects.create(
                id=user_id,
                username=username,
                display_name=display_name,
                is_bot=True,
                email_verified=True,
                created_at=int(time.time() * 1000),
            )
            messages.success(request, f'Created bot user @{username} (id={bot_user.id}).')
        except Exception as e:
            messages.error(request, f'Failed to create bot user: {e}')
        return redirect(f'/admin/bots/{bot_id}/')
    ctx = _ctx(request, active_page='bot', config=config)
    return render(request, 'admin_panel/bot_create_user.html', ctx)


# ---------------------------------------------------------------------------
# SUBJECT PAGES & NEBY AI INTEGRATION
# ---------------------------------------------------------------------------

def parse_qas(text):
    """Parse a block of text containing Q&A pairs into a list of dictionaries."""
    if not text:
        return []
    blocks = []
    current_q = None
    current_a = []
    
    lines = text.split('\n')
    for line in lines:
        line_stripped = line.strip()
        is_new_q = False
        if line_stripped.lower().startswith('q:') or line_stripped.lower().startswith('question'):
            is_new_q = True
        elif line_stripped.startswith('Q') and len(line_stripped) > 1:
            first_word = line_stripped.split()[0] if line_stripped.split() else ''
            if len(first_word) > 1 and (first_word[1].isdigit() or first_word[1] in ['.', ':', ' ']):
                is_new_q = True
        
        if is_new_q:
            if current_q:
                blocks.append({
                    'question': current_q,
                    'answer': '\n'.join(current_a).strip()
                })
            current_q = line_stripped
            current_a = []
        else:
            if current_q:
                current_a.append(line)
            else:
                if line_stripped:
                    current_q = line_stripped
                    current_a = []
    if current_q:
        blocks.append({
            'question': current_q,
            'answer': '\n'.join(current_a).strip()
        })
    return blocks


def subject_page(request, grade_slug, subject_slug):
    """Subject details page — groups resources by chapter and links Neby AI + forum."""
    grade_db_val = curriculum.get_grade_db_value(grade_slug)
    subject_db_val = curriculum.get_subject_db_value(subject_slug)
    
    # Query approved lead resources
    resources_qs = Resource.objects.filter(
        approval_status='approved',
        is_lead=True,
        grade_level__iexact=grade_db_val,
        subject__icontains=subject_db_val
    )
    
    # Fetch database syllabus content entries
    from api.models import SyllabusContent
    syllabus_entries = SyllabusContent.objects.filter(
        grade_level__iexact=grade_db_val,
        subject__iexact=subject_db_val
    ).order_by('order')
    
    grouped_resources = []
    chapter_map = {}
    
    if syllabus_entries.exists():
        for entry in syllabus_entries:
            ch_entry = {
                'id': entry.chapter_id,
                'name': entry.chapter_title,
                'keywords': [entry.chapter_title.lower(), entry.chapter_id.replace('-', ' ')],
                'notes': [],
                'solutions': [],
                'papers': [],
                'textbooks': [],
                'other': [],
                'count': 0,
                'syllabus_text': entry.text_content,
                'question_answers': entry.question_answers,
                'question_answers_parsed': parse_qas(entry.question_answers)
            }
            grouped_resources.append(ch_entry)
            chapter_map[entry.chapter_id] = ch_entry
    else:
        # Fallback to predefined curriculum map
        chapters = curriculum.get_chapters_for_subject(grade_db_val, subject_db_val)
        for ch in chapters:
            ch_entry = {
                'id': ch['id'],
                'name': ch['name'],
                'keywords': ch['keywords'],
                'notes': [],
                'solutions': [],
                'papers': [],
                'textbooks': [],
                'other': [],
                'count': 0,
                'syllabus_text': '',
                'question_answers': '',
                'question_answers_parsed': []
            }
            grouped_resources.append(ch_entry)
            chapter_map[ch['id']] = ch_entry
        
    general_resources = {
        'id': 'general',
        'name': 'General & Reference Resources',
        'notes': [],
        'solutions': [],
        'papers': [],
        'textbooks': [],
        'other': [],
        'count': 0
    }
    
    total_count = 0
    for r in resources_qs:
        total_count += 1
        serialized = _serialize_resource(r)
        
        # Match to a chapter
        matched_ch_id = None
        # First match by tags exactly
        res_tags = [t.strip().lower() for t in (r.tags or '').split(',') if t.strip()]
        for ch in grouped_resources:
            if any(kw.lower() in res_tags for kw in ch['keywords']):
                matched_ch_id = ch['id']
                break
                
        # Substring search in tags, title or description if not matched yet
        if not matched_ch_id:
            r_title_lower = r.title.lower()
            r_desc_lower = (r.description or '').lower()
            r_tags_lower = (r.tags or '').lower()
            for ch in grouped_resources:
                if any(kw.lower() in r_title_lower or kw.lower() in r_desc_lower or kw.lower() in r_tags_lower for kw in ch['keywords']):
                    matched_ch_id = ch['id']
                    break
        
        target_group = chapter_map.get(matched_ch_id) if matched_ch_id else general_resources
        
        # Categorise resource type
        rtype_lower = (r.type or '').lower().strip()
        exam_type_lower = (r.exam_type or '').lower().strip()
        r_title_lower = r.title.lower()
        r_tags_lower = (r.tags or '').lower()
        
        is_solution = any(x in r_title_lower or x in r_tags_lower for x in ['solution', 'exercise', 'question answer', 'q&a', 'answers'])
        is_paper = exam_type_lower in ['board', 'final', 'mock', 'entrance', 'see'] or any(x in r_title_lower or x in r_tags_lower for x in ['past paper', 'model paper', 'question paper', 'exam paper'])
        
        if is_solution:
            target_group['solutions'].append(serialized)
        elif is_paper:
            target_group['papers'].append(serialized)
        elif rtype_lower == 'note' or exam_type_lower == 'notes':
            target_group['notes'].append(serialized)
        elif rtype_lower == 'textbook' or exam_type_lower == 'reference' or 'textbook' in r_title_lower:
            target_group['textbooks'].append(serialized)
        else:
            target_group['other'].append(serialized)
            
        target_group['count'] += 1
    
    # Query forum posts
    posts_qs = Post.objects.select_related('user').filter(
        Q(category__iexact=subject_db_val) | 
        Q(title__icontains=subject_db_val) | 
        Q(content__icontains=subject_db_val)
    ).filter(is_archived=False).order_by('-created_at')[:15]
    user_id = _get_user_id(request)
    posts = _serialize_posts(posts_qs, user_id)
    
    # Compile lists for drop-downs
    from api.models import SyllabusContent
    has_syllabus = SyllabusContent.objects.exists()
    
    active_subjects = set()
    if has_syllabus:
        # Driven solely by admin-created SyllabusContent
        for s_val in SyllabusContent.objects.filter(grade_level__iexact=grade_db_val).values_list('subject', flat=True).distinct():
            for s in s_val.split(','):
                s_clean = s.strip()
                if s_clean:
                    active_subjects.add(s_clean)
        # If no syllabus content exists for this specific grade, fall back to CURRICULUM_MAP
        if not active_subjects:
            for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
                if g_val.lower() == grade_db_val.lower():
                    active_subjects.add(s_val)
    else:
        # Fallback to CURRICULUM_MAP keys
        for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
            if g_val.lower() == grade_db_val.lower():
                active_subjects.add(s_val)
                
    subject_list = []
    for s in sorted(list(active_subjects)):
        slug = curriculum.slugify_tag(s)
        if slug:
            subject_list.append({
                'name': s,
                'slug': slug
            })

    active_grades = {grade_db_val}
    if has_syllabus:
        # Driven solely by admin-created SyllabusContent
        for g in SyllabusContent.objects.values_list('grade_level', flat=True).distinct():
            g_clean = g.strip() if g else ''
            if g_clean:
                if g_clean.lower() == 'grade 12':
                    g_clean = 'Class 12'
                elif g_clean.lower() == 'grade 11':
                    g_clean = 'Class 11'
                active_grades.add(g_clean)
    else:
        # Fallback to CURRICULUM_MAP keys
        for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
            g_clean = g_val.strip()
            if g_clean:
                if g_clean.lower() == 'grade 12':
                    g_clean = 'Class 12'
                elif g_clean.lower() == 'grade 11':
                    g_clean = 'Class 11'
                active_grades.add(g_clean)
            
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    grade_order = {val.lower(): i for i, val in enumerate(education_levels)}
    sorted_grades = sorted(list(active_grades), key=lambda x: grade_order.get(x.lower(), 999))
    
    grade_list = []
    for g in sorted_grades:
        grade_list.append({
            'name': g,
            'slug': g.lower().replace(' / see', '-see').replace(' ', '-')
        })
    
    ctx = _ctx(request,
        grade=grade_db_val,
        subject=subject_db_val,
        grade_slug=grade_slug,
        subject_slug=subject_slug,
        grouped_resources=grouped_resources,
        general_resources=general_resources,
        posts=posts,
        total_count=total_count,
        grade_list=grade_list,
        subject_list=subject_list,
        default_model='meta-llama/Llama-3-8b-instruct'
    )
    return render(request, 'web/subject_page.html', ctx)


def ajax_arena_sessions(request):
    """Session-based AJAX wrapper for listing or creating AI4Bharat Arena sessions."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    from api import ai4bharat_proxy as arena
    from api.models import ArenaChatSession

    if request.method == 'GET':
        sessions = ArenaChatSession.objects.filter(user=user, is_active=True).order_by('-updated_at')[:100]
        return JsonResponse({
            'sessions': [
                {
                    'id': s.id,
                    'title': s.title,
                    'modelId': s.model_id,
                    'modelCode': s.model_code,
                    'modelName': s.model_display_name,
                    'messageCount': s.message_count,
                    'createdAt': s.created_at,
                    'updatedAt': s.updated_at,
                    'lastMessageAt': s.last_message_at,
                }
                for s in sessions
            ]
        })
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        model_id = (data.get('modelId') or '').strip()
        title = (data.get('title') or '').strip()[:200]
        if not model_id:
            return JsonResponse({'error': 'modelId is required'}, status=400)
            
        try:
            entry = arena.acquire_token(require_low_budget=True)
        except arena.ArenaRateLimit:
            return JsonResponse({'error': 'AI pool capacity reached', 'code': 'pool_exhausted'}, status=503)
        except arena.ArenaError as e:
            logger.error("ajax_arena_sessions create: token mint failed: %s", e)
            return JsonResponse({'error': 'AI service temporarily unavailable'}, status=503)
            
        model_meta = None
        try:
            all_models = arena.list_models(entry['token'])
            model_meta = next((m for m in all_models if m.get('id') == model_id), None)
        except Exception:
            pass
            
        try:
            remote = arena.create_session(entry['token'], model_id)
        except arena.ArenaAuthError:
            try:
                fresh = arena._new_anonymous_token()
                remote = arena.create_session(fresh['token'], model_id)
                entry = fresh
            except Exception as e:
                logger.error("ajax_arena_sessions create fallback failed: %s", e)
                return JsonResponse({'error': 'AI service temporarily unavailable'}, status=503)
        except arena.ArenaRateLimit as e:
            return JsonResponse({'error': str(e), 'code': 'pool_exhausted'}, status=503)
        except arena.ArenaError as e:
            logger.error("ajax_arena_sessions create failed: %s", e)
            return JsonResponse({'error': 'Could not start AI session — try again'}, status=502)
            
        now = int(time.time() * 1000)
        sess = ArenaChatSession.objects.create(
            id=str(uuid.uuid4()),
            user=user,
            arena_session_id=remote['id'],
            arena_token_id=entry['token'],
            model_id=model_id,
            model_code=(model_meta or {}).get('model_code', ''),
            model_display_name=(model_meta or {}).get('display_name', ''),
            title=title or 'New chat',
            is_active=True,
            message_count=0,
            last_message_at=0,
            created_at=now,
            updated_at=now,
        )
        arena.commit_token_use(entry['token'], message_used=False, session_opened=True)
        
        return JsonResponse({
            'session': {
                'id': sess.id,
                'title': sess.title,
                'modelId': sess.model_id,
                'modelCode': sess.model_code,
                'modelName': sess.model_display_name,
                'messageCount': 0,
                'createdAt': sess.created_at,
                'updatedAt': sess.updated_at,
            }
        }, status=201)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def ajax_arena_session_detail(request, session_id):
    """Session-based AJAX wrapper for getting, updating or deleting a chat session."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    from api.models import ArenaChatSession

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
        
    if sess.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
        
    if request.method == 'GET':
        msgs = list(sess.messages.order_by('created_at'))
        return JsonResponse({
            'session': {
                'id': sess.id,
                'title': sess.title,
                'modelId': sess.model_id,
                'modelCode': sess.model_code,
                'modelName': sess.model_display_name,
                'messageCount': sess.message_count,
                'createdAt': sess.created_at,
                'updatedAt': sess.updated_at,
                'lastMessageAt': sess.last_message_at,
                'isActive': sess.is_active,
            },
            'messages': [
                {
                    'id': m.id,
                    'role': m.role,
                    'content': m.content,
                    'parentId': m.parent_id,
                    'arenaMessageId': m.arena_message_id,
                    'finishReason': m.finish_reason,
                    'error': m.error,
                    'durationMs': m.duration_ms,
                    'createdAt': m.created_at,
                }
                for m in msgs
            ]
        })
        
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        new_title = data.get('title')
        if new_title is not None:
            sess.title = str(new_title).strip()[:200]
        if 'isActive' in data:
            sess.is_active = bool(data.get('isActive'))
        sess.updated_at = int(time.time() * 1000)
        sess.save(update_fields=['title', 'is_active', 'updated_at'])
        return JsonResponse({'ok': True, 'title': sess.title, 'isActive': sess.is_active})
        
    elif request.method == 'DELETE':
        sess.delete()
        return JsonResponse({'ok': True})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def ajax_arena_send_message(request, session_id):
    """Session-based AJAX wrapper for sending a message and streaming the SSE response."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    from api.models import ArenaChatSession

    try:
        sess = ArenaChatSession.objects.get(pk=session_id)
    except ArenaChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
        
    if sess.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    content = (data.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'content is required'}, status=400)
    if len(content) > 8000:
        return JsonResponse({'error': 'Message too long (max 8000 chars)'}, status=400)
        
    from api.arena_views import _stream_send
    
    gen = _stream_send(sess, content)
    response = StreamingHttpResponse(gen, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


def ajax_arena_regenerate(request, message_id):
    """Session-based AJAX wrapper for regenerating the last assistant response."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    from api.models import ArenaChatMessage

    try:
        target = ArenaChatMessage.objects.select_related('session').get(pk=message_id)
    except ArenaChatMessage.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
        
    if target.session.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
        
    if target.role != 'assistant':
        return JsonResponse({'error': 'Only assistant messages can be regenerated'}, status=400)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    from api.arena_views import _stream_regenerate
    
    gen = _stream_regenerate(target.session, target.id)
    response = StreamingHttpResponse(gen, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    response['Connection'] = 'keep-alive'
    return response


def admin_syllabus_list(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    
    from api.models import SyllabusContent
    syllabus_qs = SyllabusContent.objects.all().order_by('grade_level', 'subject', 'order')
    
    search = request.GET.get('q', '').strip()
    if search:
        syllabus_qs = syllabus_qs.filter(
            Q(grade_level__icontains=search) | 
            Q(subject__icontains=search) | 
            Q(chapter_title__icontains=search)
        )
        
    paginator = Paginator(syllabus_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/syllabus_list.html', {
        'is_admin': True,
        'page_obj': page_obj,
        'search': search,
        'active_page': 'syllabus',
    })


def admin_syllabus_create(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    import uuid
    import time
    
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    
    if request.method == 'POST':
        grade_level = request.POST.get('grade_level', '').strip()
        subject = request.POST.get('subject', '').strip()
        chapter_title = request.POST.get('chapter_title', '').strip()
        chapter_id = request.POST.get('chapter_id', '').strip()
        text_content = request.POST.get('text_content', '').strip()
        question_answers = request.POST.get('question_answers', '').strip()
        order_val = request.POST.get('order', '0').strip()
        
        if not grade_level or not subject or not chapter_title or not chapter_id:
            return HttpResponse('Missing required fields.', status=400)
            
        now_ms = int(time.time() * 1000)
        try:
            order = int(order_val)
        except ValueError:
            order = 0
            
        syllabus_obj = SyllabusContent(
            id=str(uuid.uuid4()),
            grade_level=grade_level,
            subject=subject,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            text_content=text_content,
            question_answers=question_answers,
            order=order,
            created_at=now_ms,
            updated_at=now_ms
        )
        syllabus_obj.save()
        return redirect('web:admin_syllabus_list')
        
    return render(request, 'admin_panel/syllabus_form.html', {
        'is_admin': True,
        'education_levels': education_levels,
        'active_page': 'syllabus',
        'is_edit': False,
    })


def admin_syllabus_edit(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    import time
    
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    
    if request.method == 'POST':
        grade_level = request.POST.get('grade_level', '').strip()
        subject = request.POST.get('subject', '').strip()
        chapter_title = request.POST.get('chapter_title', '').strip()
        chapter_id = request.POST.get('chapter_id', '').strip()
        text_content = request.POST.get('text_content', '').strip()
        question_answers = request.POST.get('question_answers', '').strip()
        order_val = request.POST.get('order', '0').strip()
        
        if not grade_level or not subject or not chapter_title or not chapter_id:
            return HttpResponse('Missing required fields.', status=400)
            
        try:
            order = int(order_val)
        except ValueError:
            order = 0
            
        syllabus_obj.grade_level = grade_level
        syllabus_obj.subject = subject
        syllabus_obj.chapter_title = chapter_title
        syllabus_obj.chapter_id = chapter_id
        syllabus_obj.text_content = text_content
        syllabus_obj.question_answers = question_answers
        syllabus_obj.order = order
        syllabus_obj.updated_at = int(time.time() * 1000)
        syllabus_obj.save()
        return redirect('web:admin_syllabus_list')
        
    return render(request, 'admin_panel/syllabus_form.html', {
        'is_admin': True,
        'syllabus': syllabus_obj,
        'education_levels': education_levels,
        'active_page': 'syllabus',
        'is_edit': True,
    })


def admin_syllabus_delete(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    if request.method == 'POST':
        syllabus_obj.delete()
        
    return redirect('web:admin_syllabus_list')

