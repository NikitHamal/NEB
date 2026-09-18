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

from api.models import User, Resource, ResourceRequest, ResourceRequestUpvote, Post, PostLike, PostImage, PostMedia, Poll, PollOption, PollVote, Reply, ReplyLike, Follow, UserPhoto, EditHistory, Bookmark, Notification, Report, BotConfig, TakedownRequest, BlogComment, BlogCommentLike, AiFeedback
from api.models import ResourceLike, ResourceComment, ResourceCommentLike, PaymentVerification, SellerBalance, WithdrawalRequest
from api.serializers import UserSerializer, ResourceSerializer, PostSerializer, ReplySerializer
from api.security import (
    get_user_by_auth_token, hash_auth_token, issue_auth_token, revoke_auth_token,
    save_profile_image_upload, save_post_image_upload, validate_profile_photo_url,
    validate_resource_file_url, validate_and_save_resource_file,
    save_resource_thumbnail_upload, maybe_autoset_video_thumbnail,
)

def _make_abs_url(path: str) -> str:
    if not path:
        return ''
    if path.startswith('http://') or path.startswith('https://'):
        return path
    domain = 'https://nebians.consica.com.np'
    return domain + (path if path.startswith('/') else '/' + path)
from api.authentication import verify_google_token
from api.utils import now_ms, uuid_str
from api import services
from api import counters as _counters
from api import notifications as _notif
from api import cleanup as _cleanup
from api import realtime as _rt
from api.view_helpers import map_profile_grade, is_global_user
from . import api_client as api

logger = logging.getLogger(__name__)

import math
from urllib.parse import urlparse, parse_qs, quote

_VIDEO_EXTS = ('.mp4', '.webm', '.mkv', '.mov', '.m4v', '.3gp', '.ogv', '.avi')
_AUDIO_EXTS = ('.mp3', '.wav', '.ogg', '.oga', '.flac', '.aac', '.m4a', '.opus', '.wma')
_IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg', '.avif')
_PDF_EXTS = ('.pdf',)
_MIME_BY_EXT = {
    '.mp4': 'video/mp4', '.webm': 'video/webm', '.mkv': 'video/x-matroska',
    '.mov': 'video/quicktime', '.m4v': 'video/x-m4v', '.3gp': 'video/3gpp',
    '.ogv': 'video/ogg', '.avi': 'video/x-msvideo',
    '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.ogg': 'audio/ogg',
    '.oga': 'audio/ogg', '.flac': 'audio/flac', '.aac': 'audio/aac',
    '.m4a': 'audio/mp4', '.opus': 'audio/opus', '.wma': 'audio/x-ms-wma',
}


def _url_path_lower(url):
    if not url:
        return ''
    try:
        return urlparse(url).path.lower()
    except Exception:
        return (url or '').lower().split('?')[0]


def _file_ext(url):
    path = _url_path_lower(url)
    if not path:
        return ''
    _, ext = os.path.splitext(path)
    return ext


def _youtube_id(url):
    if not url:
        return ''
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or '').lower()
        if host in ('youtu.be', 'www.youtu.be'):
            return (parsed.path or '').strip('/').split('/')[0]
        if 'youtube.com' in host or 'youtube-nocookie.com' in host:
            qs = parse_qs(parsed.query or '')
            if qs.get('v'):
                return qs['v'][0]
            parts = [p for p in (parsed.path or '').split('/') if p]
            if parts and parts[0] in ('embed', 'shorts', 'live', 'v') and len(parts) > 1:
                return parts[1]
    except Exception:
        return ''
    return ''


def _vimeo_id(url):
    if not url:
        return ''
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or '').lower()
        if 'vimeo.com' not in host:
            return ''
        parts = [p for p in (parsed.path or '').split('/') if p and p.isdigit()]
        return parts[0] if parts else ''
    except Exception:
        return ''


def _drive_file_id(url):
    if not url:
        return ''
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or '').lower()
        if 'drive.google.com' not in host and 'docs.google.com' not in host:
            return ''
        parts = [p for p in (parsed.path or '').split('/') if p]
        if 'd' in parts:
            i = parts.index('d')
            if i + 1 < len(parts):
                return parts[i + 1]
        qs = parse_qs(parsed.query or '')
        if qs.get('id'):
            return qs['id'][0]
    except Exception:
        return ''
    return ''


def classify_resource_media(rtype='', file_url=''):
    """Classify a resource for reader rendering.

    Returns dict with:
      media_type: pdf|video|audio|image|document
      provider: direct|youtube|vimeo|drive|external
      mime_type: best-effort MIME for <source type>
      embed_url: optional iframe/embed URL for hosted providers
    """
    t = (rtype or '').lower().strip()
    url = (file_url or '').strip()
    ext = _file_ext(url)
    host = ''
    try:
        host = (urlparse(url).hostname or '').lower()
    except Exception:
        host = ''

    yt = _youtube_id(url)
    if yt:
        return {
            'media_type': 'video',
            'provider': 'youtube',
            'mime_type': '',
            'embed_url': f'https://www.youtube-nocookie.com/embed/{yt}?rel=0&modestbranding=1&playsinline=1',
        }

    vim = _vimeo_id(url)
    if vim:
        return {
            'media_type': 'video',
            'provider': 'vimeo',
            'mime_type': '',
            'embed_url': f'https://player.vimeo.com/video/{vim}?title=0&byline=0&portrait=0',
        }

    drive_id = _drive_file_id(url)
    if drive_id:
        kind = 'document'
        if t == 'video' or ext in _VIDEO_EXTS:
            kind = 'video'
        elif t == 'audio' or ext in _AUDIO_EXTS:
            kind = 'audio'
        elif t == 'image' or ext in _IMAGE_EXTS:
            kind = 'image'
        elif t == 'pdf' or ext in _PDF_EXTS:
            kind = 'pdf'
        return {
            'media_type': kind,
            'provider': 'drive',
            'mime_type': _MIME_BY_EXT.get(ext, ''),
            'embed_url': f'https://drive.google.com/file/d/{drive_id}/preview',
        }

    if t == 'video' or ext in _VIDEO_EXTS:
        media_type = 'video'
    elif t == 'audio' or ext in _AUDIO_EXTS:
        media_type = 'audio'
    elif t == 'image' or ext in _IMAGE_EXTS:
        media_type = 'image'
    elif t == 'pdf' or ext in _PDF_EXTS:
        media_type = 'pdf'
    else:
        media_type = 'document'

    provider = 'direct'
    if url and media_type in ('video', 'audio', 'image') and ext not in (
        _VIDEO_EXTS + _AUDIO_EXTS + _IMAGE_EXTS
    ) and t not in ('video', 'audio', 'image'):
        provider = 'external'
    elif url and media_type in ('video', 'audio') and not ext and t in ('video', 'audio'):
        if host and host not in ('',):
            provider = 'direct'

    return {
        'media_type': media_type,
        'provider': provider,
        'mime_type': _MIME_BY_EXT.get(ext, ''),
        'embed_url': '',
    }


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
            uploaded_by_photo = _avatar_url(ub)
            uploaded_by_username = ub.username
    file_url = r.file_url or ''
    if r.file:
        file_url = r.file.url
    media = classify_resource_media(r.type, file_url)
    media_type = media['media_type']
    is_paid = bool(getattr(r, 'is_paid', False))
    raw_price = float(getattr(r, 'price', 0.0) or 0.0)
    price_formatted = f"Rs. {raw_price:.0f}" if raw_price.is_integer() else f"Rs. {raw_price:.2f}"
    return {
        'id': r.id, 'title': r.title, 'description': r.description or '',
        'subject': r.subject, 'gradeLevel': r.grade_level, 'grade_level': r.grade_level,
        'faculty': r.faculty or '', 'program': r.program or '',
        'year': r.year or '', 'examType': r.exam_type or '', 'exam_type': r.exam_type or '',
        'pradesh': r.pradesh or '', 'district': r.district or '',
        'school': r.school or '',
        'tags': r.tags or '',
        'type': r.type, 'mediaType': media_type, 'media_type': media_type,
        'mediaProvider': media['provider'], 'media_provider': media['provider'],
        'mimeType': media['mime_type'], 'mime_type': media['mime_type'],
        'embedUrl': media['embed_url'], 'embed_url': media['embed_url'],
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
        'isPaid': is_paid, 'is_paid': is_paid,
        'price': raw_price,
        'priceFormatted': price_formatted, 'price_formatted': price_formatted,
    }


def check_user_resource_access(user, resource_obj):
    """Determines whether a user has full access to view/download a paid or free resource.

    Returns tuple: (has_access: bool, access_reason: str, purchase_obj: PaymentVerification|None)
    access_reason can be: 'free', 'owner', 'admin', 'purchased', 'pending_verification', 'rejected', 'unpurchased'
    """
    if not resource_obj.is_paid:
        return True, 'free', None

    if not user or not user.is_authenticated:
        return False, 'unpurchased', None

    user_id = user.id if hasattr(user, 'id') else str(user)
    
    # Owner access
    if resource_obj.uploaded_by_id == user_id:
        return True, 'owner', None

    # Admin access
    if getattr(user, 'is_admin', False) or getattr(user, 'is_staff', False) or (isinstance(user, User) and (user.is_admin or user.is_locked is False and user.moderator_level >= 3)):
        return True, 'admin', None

    # Check buyer payment records
    purchase = PaymentVerification.objects.filter(buyer_id=user_id, resource_id=resource_obj.id).order_by('-created_at').first()
    if purchase:
        if purchase.status == 'approved':
            return True, 'purchased', purchase
        elif purchase.status == 'pending':
            return False, 'pending_verification', purchase
        elif purchase.status == 'rejected':
            return False, 'rejected', purchase

    return False, 'unpurchased', None


def get_or_create_seller_balance(user_obj):
    """Retrieves or initializes a SellerBalance record for a user."""
    balance, _ = SellerBalance.objects.get_or_create(user=user_obj, defaults={
        'total_earned': 0.00,
        'total_withdrawn': 0.00,
        'current_balance': 0.00,
        'updated_at': now_ms(),
    })
    return balance


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
        badge['label'] = 'Agent'
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

def _serialize_web_media_item(m):
    import json
    from api.security import get_video_qualities
    thumb = _make_abs_url(m.thumbnail_url)
    quals = []
    quals_json = '[]'
    if m.kind == 'video':
        quals = get_video_qualities(m.url)
        try:
            quals_json = json.dumps(quals)
        except Exception:
            quals_json = '[]'
    return {
        'id': m.id,
        'kind': m.kind,
        'url': m.url,
        'thumbnail_url': thumb,
        'thumbnailUrl': thumb,
        'qualities': quals,
        'qualities_json': quals_json,
        'name': m.name,
        'mimeType': m.mime_type,
        'sizeBytes': m.size_bytes,
        'order': m.order,
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
    all_media = {}
    for m in PostMedia.objects.filter(post_id__in=post_ids).order_by('order', 'created_at'):
        all_media.setdefault(m.post_id, []).append(_serialize_web_media_item(m))
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
        anon = bool(getattr(p, 'is_anonymous', False))
        result.append({
            'id': p.id, 'title': p.title, 'content': p.content, 'category': p.category,
            'authorName': 'Anonymous Nebian' if anon else p.user.username,
            'authorPhotoUrl': '' if anon else _avatar_url(p.user),
            'authorBadgeInfo': None if anon else _user_badge_info(p.user),
            'authorAchievements': [] if anon else _user_achievement_badges(p.user),
            'authorIsBot': False if anon else p.user.is_bot,
            'authorId': '' if anon else p.user_id,
            'isOwner': bool(user_id and p.user_id == user_id),
            'isAnonymous': anon,
            'thumbsUpCount': p.thumbs_up_count, 'thumbs_up_count': p.thumbs_up_count,
            'replyCount': p.reply_count, 'reply_count': p.reply_count,
            'viewCount': p.view_count, 'view_count': p.view_count,
            'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
            'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
            'isThumbedUp': p.id in liked_ids,
            'isFollowingAuthor': False if anon else p.user_id in followed_author_ids,
            'isBookmarked': p.id in bookmarked_ids,
            'images': all_images.get(p.id, []),
            'attachments': all_media.get(p.id, []),
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
    anon = bool(getattr(p, 'is_anonymous', False))
    media = [_serialize_web_media_item(m) for m in PostMedia.objects.filter(post_id=p.id).order_by('order', 'created_at')]
    return {
        'id': p.id, 'title': p.title, 'content': p.content, 'category': p.category,
        'authorName': 'Anonymous Nebian' if anon else p.user.username,
        'authorPhotoUrl': '' if anon else _avatar_url(p.user),
        'authorBadgeInfo': None if anon else _user_badge_info(p.user),
        'authorAchievements': [] if anon else _user_achievement_badges(p.user),
        'authorIsBot': False if anon else p.user.is_bot,
        'authorId': '' if anon else p.user_id,
        'isOwner': bool(user_id and p.user_id == user_id),
        'isAnonymous': anon,
        'thumbsUpCount': p.thumbs_up_count, 'thumbs_up_count': p.thumbs_up_count,
        'replyCount': p.reply_count, 'reply_count': p.reply_count,
        'viewCount': p.view_count, 'view_count': p.view_count,
        'createdAt': p.created_at, 'updatedAt': p.edited_at or p.created_at,
        'isEdited': p.is_edited, 'editedAt': p.edited_at, 'isArchived': p.is_archived,
        'isThumbedUp': is_thumbed_up,
        'isFollowingAuthor': False if anon else is_following_author,
        'isBookmarked': is_bookmarked,
        'images': _serialize_post_images(p.id),
        'attachments': media,
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
    all_media = {}
    reply_ids = [r.id for r in replies]
    for m in PostMedia.objects.filter(reply_id__in=reply_ids).order_by('order', 'created_at'):
        all_media.setdefault(m.reply_id, []).append(_serialize_web_media_item(m))
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
            c_anon = bool(getattr(c, 'is_anonymous', False))
            key = ('anon',) if c_anon else c.user_id
            if key not in seen:
                seen.add(key)
                child_authors.append({
                    'id': '' if c_anon else c.user_id,
                    'username': 'Anonymous Nebian' if c_anon else c.user.username,
                    'photoUrl': '' if c_anon else _avatar_url(c.user),
                })
        anon = bool(getattr(r, 'is_anonymous', False))
        result.append({
            'id': r.id, 'postId': r.post_id, 'postTitle': r.post.title if r.post else '', 'parentReplyId': r.parent_reply_id,
            'content': r.content,
            'authorName': 'Anonymous Nebian' if anon else r.user.username,
            'authorPhotoUrl': '' if anon else _avatar_url(r.user),
            'authorId': '' if anon else r.user_id,
            'authorBadgeInfo': None if anon else _user_badge_info(r.user),
            'authorAchievements': [] if anon else _user_achievement_badges(r.user),
            'authorIsBot': False if anon else r.user.is_bot,
            'isOwner': bool(user_id and r.user_id == user_id),
            'isAnonymous': anon,
            'thumbsUpCount': r.thumbs_up_count, 'childCount': total_descendants.get(r.id, len(children)),
            'viewCount': r.view_count,
            'childAuthors': child_authors,
            'createdAt': r.created_at,
            'isEdited': r.is_edited, 'editedAt': r.edited_at,
            'isArchived': r.is_archived,
            'isThumbedUp': r.id in liked_ids,
            'isFollowed': False if anon else r.user_id in followed_author_ids,
            'isBookmarked': r.id in bookmarked_ids,
            'attachments': all_media.get(r.id, []),
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
    anon = bool(getattr(r, 'is_anonymous', False))
    media = [{
        'id': m.id, 'kind': m.kind, 'url': m.url,
        'thumbnail_url': _make_abs_url(m.thumbnail_url), 'thumbnailUrl': _make_abs_url(m.thumbnail_url),
        'name': m.name, 'mimeType': m.mime_type, 'sizeBytes': m.size_bytes, 'order': m.order,
    } for m in r.media.all()]
    return {
        'id': r.id, 'postId': r.post_id, 'parentReplyId': r.parent_reply_id,
        'content': r.content,
        'authorName': 'Anonymous Nebian' if anon else r.user.username,
        'authorPhotoUrl': '' if anon else _avatar_url(r.user),
        'authorId': '' if anon else r.user_id,
        'authorBadgeInfo': None if anon else _user_badge_info(r.user),
        'authorAchievements': [] if anon else _user_achievement_badges(r.user),
        'authorIsBot': False if anon else r.user.is_bot,
        'isOwner': bool(user_id and r.user_id == user_id),
        'isAnonymous': anon,
        'thumbsUpCount': r.thumbs_up_count, 'childCount': r.reply_count,
        'viewCount': r.view_count,
        'createdAt': r.created_at,
        'isEdited': r.is_edited, 'editedAt': r.edited_at, 'isArchived': r.is_archived,
        'isThumbedUp': is_thumbed_up,
        'isBookmarked': is_bookmarked,
        'attachments': media,
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
       1. WS_PUBLIC_URL env var or settings.WS_PUBLIC_URL (explicit override — stable named tunnel)
       2. Most-recent trycloudflare.com URL by file mtime (ws_url.txt, start_ws_tunnel.log,
          cloudflared.log, /tmp/cf_quick*.log). We pick the NEWEST file that contains a
          URL, not the first match — ws_url.txt can be stale after a reboot while
          cloudflared.log already has the fresh URL.
       3. Empty string (realtime.js falls back to polling).
    """
    explicit = os.environ.get('WS_PUBLIC_URL', '').strip()
    if not explicit and hasattr(settings, 'WS_PUBLIC_URL'):
        explicit = (getattr(settings, 'WS_PUBLIC_URL', '') or '').strip()
    if explicit:
        return explicit
    import glob, re
    candidates = []
    log_paths = [
        '/home/consicac/nebians_api/logs/start_ws_tunnel.log',
        '/home/consicac/nebians_api/logs/cloudflared.log',
        os.path.join(settings.BASE_DIR, 'logs', 'cloudflared.log'),
        '/home/consicac/nebians_api/logs/cloudflared.log',
    ] + sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True)
    for path in log_paths:
        try:
            with open(path) as f:
                content = f.read()
            matches = re.findall(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)', content)
            if matches:
                host = matches[-1].rstrip('/').rstrip('/ws').rstrip('/')
                url = 'wss://' + host + '/ws/'
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    mtime = 0
                candidates.append((mtime, url))
        except OSError:
            continue
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    # Fallback: ws_url.txt (written by deploy as cache, not authoritative)
    try:
        ws_txt = os.path.join(settings.BASE_DIR, 'ws_url.txt')
        with open(ws_txt) as f:
            content = f.read().strip()
        if content:
            m = re.search(r'([a-z0-9-]+\.trycloudflare\.com)', content)
            if m:
                return 'wss://' + m.group(1) + '/ws/'
            if content.startswith('wss://'):
                return content.strip()
    except OSError:
        pass
    return ''

def _get_ws_public_url():
    """Return the public WebSocket URL, cached for 15s to avoid per-request file I/O.

    Empty results are NOT cached so the next request retries immediately and can
    pick up a freshly-started tunnel. Short TTL ensures a tunnel restart
    propagates within seconds instead of a minute. When the tunnel is down
    (see nebians.tunnel_health) an empty string is returned so clients use the
    polling fallback instead of hammering a dead host.
    """
    url = cache.get('ws_public_url_resolved')
    if url is None:
        url = _resolve_ws_public_url()
        if url:
            cache.set('ws_public_url_resolved', url, 15)
    if url:
        try:
            from nebians.tunnel_health import is_tunnel_healthy
            if not is_tunnel_healthy():
                return ''
        except Exception:
            pass
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
    badge_info = None
    if user:
        user = _normalize_user_data(user)
        if user.get('id'):
            db_user = User.objects.filter(pk=user['id']).first()
            if db_user:
                user['is_admin'] = db_user.is_admin
                user['verification_level'] = db_user.verification_level
                user['moderator_level'] = db_user.moderator_level
                user['enable_inline_images'] = getattr(db_user, 'enable_inline_images', True)
                user['enableInlineImages'] = getattr(db_user, 'enable_inline_images', True)
                if db_user.avatar_use_pp:
                    user['photo_url'] = _blobatar_url_for(db_user)
                    user['avatar_url'] = _blobatar_url_for(db_user)
                elif db_user.photo_url:
                    user['photo_url'] = db_user.photo_url
                    user['avatar_url'] = db_user.photo_url
                else:
                    user['photo_url'] = _blobatar_url_for(db_user)
                    user['avatar_url'] = _blobatar_url_for(db_user)
                badge_info = _user_badge_info(db_user)
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
        'badge_info': badge_info,
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
    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False) or getattr(user, 'is_admin', False):
            return True
    session = getattr(request, 'session', None)
    if session and (session.get('is_staff') or session.get('is_admin')):
        return True
    return False

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
        'photoUrl': _avatar_url(u),
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

def _build_local_stats(user, exclude_anonymous=False):
    post_count = getattr(user, 'post_count', None)
    reply_count = getattr(user, 'reply_count', None)
    follower_count = getattr(user, 'follower_count', None)
    following_count = getattr(user, 'following_count', None)
    likes_given = getattr(user, 'likes_given_count', None)
    likes_received = getattr(user, 'likes_received_count', None)
    contribution_score = getattr(user, 'contribution_score', None)
    if exclude_anonymous:
        post_count = Post.objects.filter(user_id=user.id, is_anonymous=False).count()
        reply_count = Reply.objects.filter(user_id=user.id, is_anonymous=False).count()
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
            'photo_url': _avatar_url(u),
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

def _link_oauth_user(request, email, user_pk, display_name, photo_url, provider_name, provider_verified=False):
    """Auto-link OAuth accounts by verified email.

    Links ONLY when the provider asserts a verified email AND the existing
    account already verified that email. This blocks pre-account-takeover via
    squatted (unverified) email signups: linking to an unverified account is
    refused, and the verified flag is never granted by linking.

    Returns (HttpResponseRedirect, linked: bool).
    """
    if email and provider_verified:
        try:
            existing = User.objects.get(email__iexact=email)
            if not existing.email_verified:
                logger.warning('%s: refusing OAuth link to unverified account (email=%s)', provider_name, email)
                return None, False
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
        'enableInlineImages': 'enable_inline_images',
    }
    for old_key, new_key in mapping.items():
        if old_key in user and new_key not in user:
            user[new_key] = user[old_key]
    
    # Ensure avatar_url is populated for base.html navbar compatibility
    if user.get('avatar_use_pp'):
        user['avatar_url'] = _blobatar_url_for(user)
    elif 'photo_url' in user:
        user['avatar_url'] = user['photo_url'] or _blobatar_url_for(user)
    elif 'photoUrl' in user:
        user['avatar_url'] = user['photoUrl'] or _blobatar_url_for(user)
    else:
        user['avatar_url'] = _blobatar_url_for(user)

    if 'enable_inline_images' not in user:
        user['enable_inline_images'] = True
    if 'enableInlineImages' not in user:
        user['enableInlineImages'] = user.get('enable_inline_images', True)

    return user


def _avatar_prefs_from(obj):
    from api.services import avatar_options_for
    if hasattr(obj, 'username'):
        return avatar_options_for(obj)
    prefs = {}
    try:
        hue = obj.get('avatar_hue', -1)
        tone = obj.get('avatar_tone', -1.0)
        bg = obj.get('avatar_bg', '') or ''
        anim = obj.get('avatar_anim', '') or ''
        shape = obj.get('avatar_shape', '') or ''
        expression = obj.get('avatar_expression', '') or ''
        color = obj.get('avatar_color', '') or ''
        bgcolor = obj.get('avatar_bg_color', '') or ''
        eyecolor = obj.get('avatar_eye_color', '') or ''
    except AttributeError:
        return prefs
    if hue >= 0:
        prefs['hue'] = int(hue)
    if tone >= 0:
        prefs['tone'] = float(tone)
    if bg:
        prefs['background'] = bg
    if anim:
        prefs['anim'] = anim
    if shape:
        prefs['shape'] = shape
    if expression:
        prefs['expression'] = expression
    if color:
        prefs['color'] = color
    if bgcolor:
        prefs['bgcolor'] = bgcolor
    if eyecolor:
        prefs['eyecolor'] = eyecolor
    return prefs


def _blobatar_url_for(user_or_username, prefs=None):
    from urllib.parse import quote as _q
    if prefs is None and not isinstance(user_or_username, str):
        prefs = _avatar_prefs_from(user_or_username)
        if isinstance(user_or_username, dict):
            username = user_or_username.get('username', '') or ''
        else:
            username = getattr(user_or_username, 'username', '') or ''
    else:
        username = user_or_username
    url = '/avatar/%s/' % _q((username or ''), safe='')
    if prefs:
        url += '?' + '&'.join('%s=%s' % (k, _q(str(v), safe='')) for k, v in sorted(prefs.items()))
    return url


def _avatar_url(u):
    from api.services import avatar_or_photo_url
    if hasattr(u, 'username'):
        return avatar_or_photo_url(u)
    if getattr(u, 'avatar_use_pp', False):
        return _blobatar_url_for(u)
    photo = getattr(u, 'photo_url', None) or getattr(u, 'photoUrl', None) or ''
    if photo:
        return photo
    return _blobatar_url_for(u)

def _clear_page_cache():
    cache.delete_many([
        'home_resources', 'home_posts', 'home_stats_v2', 'library_all_resources',
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