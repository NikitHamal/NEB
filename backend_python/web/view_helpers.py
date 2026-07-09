import json
import logging
import os
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.signing import TimestampSigner
from django.db import transaction
from django.db.models import Q, Count, F
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse, Http404, HttpResponse, StreamingHttpResponse
from . import curriculum
from django.core.paginator import Paginator
from django.utils.html import escape

from api.models import User, Resource, ResourceRequest, ResourceRequestUpvote, Post, PostLike, PostImage, Poll, PollOption, PollVote, Reply, ReplyLike, Follow, UserPhoto, EditHistory, Bookmark, Notification, Report, BotConfig, TakedownRequest
from api.models import ResourceLike, ResourceComment, ResourceCommentLike
from api.serializers import UserSerializer, ResourceSerializer, PostSerializer, ReplySerializer
from api.security import (
    get_user_by_auth_token, hash_auth_token, issue_auth_token, revoke_auth_token,
    save_profile_image_upload, save_post_image_upload, validate_profile_photo_url,
    validate_resource_file_url, validate_and_save_resource_file,
)
from api.authentication import verify_google_token
from api.utils import now_ms, uuid_str
from api import services
from api import counters as _counters
from api import notifications as _notif
from api import cleanup as _cleanup
from api import realtime as _rt
from . import api_client as api

logger = logging.getLogger(__name__)

import math

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
    rtype_lower = (r.type or '').lower().strip()
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
    return {
        'id': r.id, 'title': r.title, 'description': r.description or '',
        'subject': r.subject, 'gradeLevel': r.grade_level, 'grade_level': r.grade_level,
        'faculty': r.faculty or '', 'program': r.program or '',
        'year': r.year or '', 'examType': r.exam_type or '', 'exam_type': r.exam_type or '',
        'pradesh': r.pradesh or '', 'district': r.district or '',
        'school': r.school or '',
        'tags': r.tags or '',
        'type': r.type, 'mediaType': media_type, 'media_type': media_type,
        'fileUrl': file_url, 'file_url': file_url,
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
    if getattr(user, 'role', 'student') == 'teacher' and getattr(user, 'teacher_verified', False):
        badge['type'] = 'teacher'
        badge['icon'] = 'school'
        badge['color'] = '#10B981'
        badge['label'] = 'Verified Teacher'
        return badge
    if getattr(user, 'role', 'student') == 'institution' and getattr(user, 'institution_verified', False):
        badge['type'] = 'institution'
        badge['icon'] = 'account_balance'
        badge['color'] = '#6366F1'
        badge['label'] = 'Verified Institution'
        return badge
    if getattr(user, 'role', 'student') == 'explorer':
        badge['type'] = 'explorer'
        badge['icon'] = 'travel_explore'
        badge['color'] = '#F59E0B'
        badge['label'] = 'Explorer'
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

def _serialize_post_images(post_id):
    images = PostImage.objects.filter(post_id=post_id).order_by('order', 'created_at')
    return [{'id': img.id, 'imageUrl': img.image_url, 'order': img.order} for img in images]

def _serialize_post_poll(post_id, user_id=None):
    try:
        poll = Poll.objects.get(post_id=post_id)
    except Poll.DoesNotExist:
        return None
    options = list(PollOption.objects.filter(poll=poll).order_by('order'))
    user_vote = None
    if user_id:
        vote = PollVote.objects.filter(poll=poll, user_id=user_id).select_related('option').first()
        if vote:
            user_vote = vote.option_id
    return {
        'id': poll.id,
        'question': poll.question,
        'pollType': poll.poll_type,
        'allowMultiple': poll.allow_multiple,
        'explanation': poll.explanation,
        'durationMs': poll.duration_ms,
        'totalVotes': poll.total_votes,
        'isExpired': poll.is_expired,
        'options': [{'id': o.id, 'text': o.text, 'isCorrect': o.is_correct, 'voteCount': o.vote_count, 'order': o.order} for o in options],
        'userVote': user_vote,
    }

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
    post_ids = [p.id for p in posts]
    all_images = {}
    for img in PostImage.objects.filter(post_id__in=post_ids).order_by('order', 'created_at'):
        all_images.setdefault(img.post_id, []).append({'id': img.id, 'imageUrl': img.image_url, 'order': img.order})
    all_polls = {}
    polls = list(Poll.objects.filter(post_id__in=post_ids))
    user_votes_by_poll = {}
    if user_id and polls:
        for v in PollVote.objects.filter(poll__post_id__in=post_ids, user_id=user_id):
            user_votes_by_poll.setdefault(v.poll_id, v.option_id)
    for poll in polls:
        opts = list(PollOption.objects.filter(poll=poll).order_by('order'))
        user_vote = user_votes_by_poll.get(poll.id)
        all_polls[poll.post_id] = {
            'id': poll.id, 'question': poll.question, 'pollType': poll.poll_type,
            'allowMultiple': poll.allow_multiple, 'explanation': poll.explanation,
            'durationMs': poll.duration_ms,
            'totalVotes': poll.total_votes, 'isExpired': poll.is_expired,
            'options': [{'id': o.id, 'text': o.text, 'isCorrect': o.is_correct, 'voteCount': o.vote_count, 'order': o.order} for o in opts],
            'userVote': user_vote,
        }
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
            'viewCount': p.view_count, 'view_count': p.view_count,
            'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
            'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
            'isThumbedUp': p.id in liked_ids,
            'isFollowingAuthor': p.user_id in followed_author_ids,
            'isBookmarked': p.id in bookmarked_ids,
            'images': all_images.get(p.id, []),
            'poll': all_polls.get(p.id),
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
        'images': _serialize_post_images(p.id),
        'poll': _serialize_post_poll(p.id, user_id),
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
    try:
        user = get_user_by_auth_token(token)
        cache.set(cache_key, user.id, 300)
        return user.id
    except User.DoesNotExist:
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

def _resolve_ws_public_url():
    """Resolve the public WebSocket URL (uncached).

    Priority:
       1. WS_PUBLIC_URL env var (explicit override)
       2. The current trycloudflare.com URL (read from cloudflared log files)
       3. ws_url.txt in the project directory (written by deploy/cron as fallback)
       4. Empty string (realtime.js falls back to same-origin /ws/).
    """
    explicit = os.environ.get('WS_PUBLIC_URL', '').strip()
    if explicit:
        return explicit
    import glob, re
    log_paths = sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True) + [
        '/home/consicac/nebians_api/logs/cloudflared.log',
        os.path.join(settings.BASE_DIR, 'ws_url.txt'),
    ]
    for path in log_paths:
        try:
            with open(path) as f:
                content = f.read()
            m = re.search(r'https://([a-z0-9-]+\.trycloudflare\.com)', content)
            if m:
                return 'wss://' + m.group(1) + '/ws/'
        except OSError:
            continue
    return ''

def _get_ws_public_url():
    """Return the public WebSocket URL, cached for 60s to avoid per-request file I/O.

    If the resolution returns an empty string, we do NOT cache it so the
    next request retries immediately (the log file may have been rotated).
    """
    url = cache.get('ws_public_url_resolved')
    if url is not None:
        return url
    url = _resolve_ws_public_url()
    if url:
        cache.set('ws_public_url_resolved', url, 60)
    return url

def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        first = forwarded.split(',')[0].strip()
        if first:
            return first
    return request.META.get('REMOTE_ADDR', '') or 'unknown'

def _rate_limit(request, scope, limit, window_seconds, by_ip=False):
    """Return True if over limit. Uses cache.add + incr (fixed window)."""
    if by_ip:
        ident = _client_ip(request)
    else:
        ident = _get_user_id(request) or _client_ip(request)
    key = f'rl:{scope}:{ident}'
    if cache.add(key, 1, window_seconds):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        # Key expired between add and incr — start a fresh window.
        cache.add(key, 1, window_seconds)
        return False
    return count > limit

def _get_distinct_subjects():
    """Distinct, comma-split, sorted subject names from the Resource table (cached 10 min)."""
    def _resolver():
        subjects = set()
        for s_str in Resource.objects.values_list('subject', flat=True).distinct():
            if s_str:
                for s in s_str.split(','):
                    s_stripped = s.strip()
                    if s_stripped:
                        subjects.add(s_stripped)
        return sorted(subjects)
    return cache.get_or_set('distinct_subjects', _resolver, 600)

def _ctx(request, **extra):
    token = api.get_session_token(request)
    user = api.get_session_user(request)
    if user:
        user = _normalize_user_data(user)
    dark_mode = request.session.get('theme') == 'dark'
    unread_notifications = 0
    if user and user.get('id'):
        _uid = user['id']

        def _load_unread():
            return (User.objects.filter(pk=_uid)
                    .values_list('unread_notification_count', flat=True).first()) or 0
        unread_notifications = cache.get_or_set(f'unread_count:{_uid}', _load_unread, 30)
    ws_url = _get_ws_public_url()
    # When using a cross-domain tunnel (trycloudflare.com), the browser cannot
    # send the session cookie cross-domain. Append a short-lived signed ticket
    # (NOT the auth token) so JWTAuthMiddleware can authenticate the WS
    # connection without leaking the bearer token in page HTML.
    if ws_url and token and user and user.get('id') and 'trycloudflare.com' in ws_url:
        ticket = TimestampSigner(salt='ws-ticket').sign(str(user['id']))
        separator = '&' if '?' in ws_url else '?'
        ws_url = f'{ws_url}{separator}ticket={ticket}'
    from api.models import NEPAL_DISTRICTS
    ctx = {
        'is_authenticated': bool(token),
        'user': user,
        'dark_mode': dark_mode,
        'unread_notifications': unread_notifications,
        'csp_nonce': getattr(request, 'csp_nonce', ''),
        'ws_url': ws_url,
        'nepal_districts': NEPAL_DISTRICTS,
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
    users = User.objects.filter(email_verified=True).order_by('-contribution_score').only(
        'id', 'username', 'display_name', 'photo_url',
        'contribution_score', 'post_count', 'reply_count',
        'likes_given_count', 'likes_received_count',
        'is_bot', 'is_admin', 'moderator_level', 'verification_level',
        'role', 'teacher_verified', 'institution_verified',
    )[:50]
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

def _compute_hot_score(post_or_dict, now_ms_val=None):
    """Reddit-style hot score: log2(engagement) + age_bonus.
    engagement = likes*3 + replies*2 + views*0.1
    age_bonus = (now - created_at) / 86400000  -> decays ~1pt/day
    """
    import math
    if now_ms_val is None:
        now_ms_val = now_ms()
    likes = getattr(post_or_dict, 'thumbs_up_count', None)
    replies = getattr(post_or_dict, 'reply_count', None)
    views = getattr(post_or_dict, 'view_count', None)
    created = getattr(post_or_dict, 'created_at', None)
    if likes is None:
        likes = post_or_dict.get('thumbs_up_count', 0) or 0
    if replies is None:
        replies = post_or_dict.get('reply_count', 0) or 0
    if views is None:
        views = post_or_dict.get('view_count', 0) or 0
    if created is None:
        created = post_or_dict.get('created_at', 0) or 0
    likes = likes or 0
    replies = replies or 0
    views = views or 0
    created = created or 0
    engagement = likes * 3 + replies * 2 + min(views, 1000) * 0.1
    age_hours = max(0, (now_ms_val - created) / 3600000)
    if engagement <= 0:
        score = -age_hours / 168.0
    else:
        score = math.log2(max(engagement, 1)) - age_hours / 168.0
    return score

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
            if not existing.email_verified:
                existing.email_verified = True
                existing.save(update_fields=['email_verified'])
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

def _clear_page_cache():
    cache.delete_many([
        'home_resources', 'home_posts', 'library_all_resources',
        'forum_all_posts', 'forum_contributors', 'admin_stats', 'sitemap_xml',
        'distinct_subjects', 'library_filter_options',
    ])

def parse_sections(text):
    """Parse markdown text into named sections based on ### or ## headers.
    
    Returns list of dicts: {'title': str, 'content': str, 'id': str, 'parsed_items': list}
    where id is a slug for anchor links and parsed_items contains Q&A pairs within the section.
    """
    if not text:
        return []
    sections = []
    current_title = None
    current_lines = []
    
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('### ') or stripped.startswith('## '):
            if current_title is not None or current_lines:
                content = '\n'.join(current_lines).strip()
                if content:
                    slug = re.sub(r'[^a-z0-9]+', '-', current_title.lower()).strip('-') if current_title else 'section'
                    sections.append({'title': current_title, 'content': content, 'id': slug, 'parsed_items': _parse_qa_items(content)})
                elif current_title:
                    pass
            current_title = stripped.lstrip('#').strip()
            current_lines = []
        else:
            current_lines.append(line)
    
    if current_title or current_lines:
        content = '\n'.join(current_lines).strip()
        if content:
            slug = re.sub(r'[^a-z0-9]+', '-', (current_title or 'section').lower()).strip('-')
            sections.append({'title': current_title or 'Overview', 'content': content, 'id': slug, 'parsed_items': _parse_qa_items(content)})
        elif current_title:
            pass
    
    if not sections and text.strip():
        sections.append({'title': 'Full Content', 'content': text.strip(), 'id': 'full-content', 'parsed_items': _parse_qa_items(text.strip())})
    
    return sections

def _parse_qa_items(text):
    """Parse a section's text into Q&A pairs based on #### headers.
    
    Each #### header becomes a question, and the text until the next #### becomes the answer.
    """
    items = []
    current_q = None
    current_a_lines = []
    
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#### '):
            if current_q:
                items.append({'question': current_q, 'answer': '\n'.join(current_a_lines).strip()})
            current_q = stripped.lstrip('#').strip()
            current_a_lines = []
        else:
            if current_q:
                current_a_lines.append(line)
    
    if current_q:
        items.append({'question': current_q, 'answer': '\n'.join(current_a_lines).strip()})
    
    return items

def parse_qas(text):
    """Parse markdown-formatted exercise content into structured sections.
    
    Handles two formats:
    1. Q:/A: prefixed blocks (legacy)
    2. Markdown headers (#### or ###) as question titles with following text as answers
    
    Returns list of dicts with 'question' and 'answer' keys.
    """
    if not text:
        return []
    
    blocks = []
    
    lines = text.split('\n')
    current_q = None
    current_a_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith('q:') or stripped.lower().startswith('q\uff1a'):
            if current_q:
                blocks.append({
                    'question': current_q,
                    'answer': '\n'.join(current_a_lines).strip()
                })
            current_q = stripped[2:].strip()
            current_a_lines = []
        elif stripped.lower().startswith('a:') or stripped.lower().startswith('a\uff1a'):
            current_a_lines.append(stripped[2:].strip())
        elif stripped.startswith('####') or stripped.startswith('### '):
            if current_q:
                blocks.append({
                    'question': current_q,
                    'answer': '\n'.join(current_a_lines).strip()
                })
            q_text = stripped.lstrip('#').strip()
            current_q = q_text
            current_a_lines = []
        else:
            if current_q:
                current_a_lines.append(line)
            else:
                if stripped:
                    current_q = stripped
                    current_a_lines = []
    
    if current_q:
        blocks.append({
            'question': current_q,
            'answer': '\n'.join(current_a_lines).strip()
        })
    
    return blocks

# Star imports from this module are intentional: split view modules need the
# same helper functions and imported framework symbols that the former monolith
# exposed as globals. Keep this broad to avoid changing runtime behavior.
__all__ = [
    name for name in globals()
    if not name.startswith('__') and name not in {'annotations'}
]