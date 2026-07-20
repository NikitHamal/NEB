"""
All API views for NEBians.
Endpoints:
  POST   /api/auth/google
  GET    /api/users/check-username?username=
  POST   /api/users/profile
  GET    /api/users/profile/<username>
  GET    /api/users/profile/<username>/stats
  POST   /api/users/<userId>/follow           (toggle follow/unfollow)
  GET    /api/users/<userId>/followers
  GET    /api/users/<userId>/following
  GET    /api/users/me/photos
  POST   /api/users/me/photos
  POST   /api/users/me/photos/<photoId>/activate
  GET    /api/resources
  GET    /api/posts          (via posts_endpoint dispatcher)
  POST   /api/posts          (via posts_endpoint dispatcher)
  DELETE /api/posts/<postId>
  POST   /api/posts/<postId>/like
  GET    /api/posts/<postId>/replies   (via replies_endpoint dispatcher)
  POST   /api/posts/<postId>/replies   (via replies_endpoint dispatcher)
  POST   /api/replies/<replyId>/like
  POST   /api/fcm/register
"""
import logging

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from django.db.models import Q, F
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .authentication import verify_google_token
from .security import (
    hash_password, verify_password, hash_verification_code, verify_verification_code,
    hash_auth_token, issue_auth_token, revoke_auth_token,
    validate_profile_photo_url, save_profile_image_upload,
    validate_external_https_url,
    validate_and_save_resource_file, validate_resource_file_url,
    save_resource_thumbnail_upload, maybe_autoset_video_thumbnail,
)
from .email_utils import send_verification_email
from .throttles import (
    AuthRateThrottle, ReportRateThrottle, SearchRateThrottle, UploadRateThrottle,
    VerificationRateThrottle, ViewIncrementRateThrottle, WriteActionRateThrottle,
    SignupRateThrottle,
)
from .models import User, Resource, ResourceLike, ResourceRequest, ResourceRequestUpvote, Post, PostLike, PostImage, Poll, PollOption, PollVote, Reply, ReplyLike, FCMToken, Follow, UserPhoto, EditHistory, Report, Bookmark, Notification
from .utils import now_ms, uuid_str
import uuid
_now_ms = now_ms
from . import services
from .serializers import (
    UserSerializer, UserPublicSerializer,
    ResourceSerializer, ResourceRequestSerializer, PostSerializer, ReplySerializer,
    UserPhotoSerializer, UserStatsSerializer, FollowSerializer,
    EditHistorySerializer, ReportSerializer, BookmarkSerializer,
    NotificationSerializer,
)
from . import counters as _counters
from . import notifications as _notif
from . import cleanup as _cleanup
from . import realtime as _rt

logger = logging.getLogger(__name__)

CODE_TTL_MS = 10 * 60 * 1000

CODE_RESEND_COOLDOWN_MS = 60 * 1000

MAX_CODE_ATTEMPTS = 5

MAX_POST_TITLE_LENGTH = 200

MAX_POST_CONTENT_LENGTH = 20_000

MAX_REPLY_CONTENT_LENGTH = 10_000

MAX_REPORT_DESCRIPTION_LENGTH = 2_000

def _profile_incomplete(user):
    """Check if user profile is missing mandatory fields."""
    if not user.display_name or not user.gender:
        return True
    if user.role == 'student' and not user.class_level:
        return True
    if user.role == 'teacher' and not user.teaching_subjects:
        return True
    if user.role == 'institution' and not user.school:
        return True
    # Explorers have no role-specific required fields.
    return False

def _is_mutual_follow(viewer, target_user):
    """True when viewer and target follow each other.

    Locked profiles stay private for everyone except the owner and mutual
    connections, matching the familiar Instagram/Facebook behavior.
    """
    if not viewer or not target_user:
        return False
    if getattr(viewer, 'pk', None) == getattr(target_user, 'pk', None):
        return False
    return (
        Follow.objects.filter(follower_id=viewer.pk, following_id=target_user.pk).exists()
        and Follow.objects.filter(follower_id=target_user.pk, following_id=viewer.pk).exists()
    )


def _can_view_locked_profile(viewer, target_user):
    """Owner and followers can view a locked profile. Unverified accounts are treated as locked."""
    if not target_user:
        return False
    is_locked = getattr(target_user, 'is_locked', False)
    is_verified = getattr(target_user, 'email_verified', True)
    if not is_locked and is_verified:
        return True
    if viewer and getattr(viewer, 'pk', None) == getattr(target_user, 'pk', None):
        return True
    if not viewer:
        return False
    return Follow.objects.filter(follower_id=viewer.pk, following_id=target_user.pk).exists()


def _get_user_from_request(request):
    """
    Returns the authenticated User object if the request is authenticated,
    otherwise None. Does NOT raise.
    """
    user = getattr(request, 'user', None)
    if isinstance(user, User):
        return user
    
    # Fallback to session auth token for web browser API requests
    token = request.session.get('auth_token') if hasattr(request, 'session') else None
    if token:
        try:
            from .security import get_user_by_auth_token
            return get_user_by_auth_token(token)
        except Exception:
            pass
    return None

def _require_user(request):
    """
    Returns (user, error_response) tuple. If user is authenticated, returns
    (user, None). Otherwise returns (None, Response with 401).
    """
    user = _get_user_from_request(request)
    if user is None:
        return None, Response({'error': 'Unauthorized — please sign in again'}, status=401)
    return user, None

def _require_verified_user(request):
    """
    Returns (user, error_response) tuple. If user is authenticated AND
    email_verified is True, returns (user, None). Otherwise returns (None, Response).
    """
    user, err = _require_user(request)
    if err:
        return None, err
    if not getattr(user, 'email_verified', False):
        return None, Response({'error': 'Please verify your email before doing that'}, status=403)
    return user, None

def _validate_text_length(value, max_length, field_name):
    if len(value) > max_length:
        return Response({'error': f'{field_name} must be {max_length} characters or fewer'}, status=400)
    return None

def _validate_password_strength(password):
    try:
        validate_password(password)
    except ValidationError as exc:
        return Response({'error': ' '.join(exc.messages)}, status=400)
    return None

def _issue_verification_code(user, purpose):
    code = User.generate_verification_code()
    now = now_ms()
    user.verification_code = hash_verification_code(code)
    user.verification_code_expires = now + CODE_TTL_MS
    user.verification_code_purpose = purpose
    user.verification_code_attempts = 0
    user.verification_code_last_sent_at = now
    user.save(update_fields=[
        'verification_code', 'verification_code_expires', 'verification_code_purpose',
        'verification_code_attempts', 'verification_code_last_sent_at'
    ])
    return code

def _verification_resend_blocked(user):
    last_sent = user.verification_code_last_sent_at or 0
    if not last_sent:
        # Legacy rows only had an expiry. Do not infer last-send time from expiry.
        return False
    return (now_ms() - last_sent) < CODE_RESEND_COOLDOWN_MS

def _verify_user_code(user, code, purpose):
    now = now_ms()
    if user.verification_code_expires < now:
        return False, Response({'error': 'Invalid or expired verification code'}, status=400)
    if user.verification_code_purpose and user.verification_code_purpose != purpose:
        if purpose == 'password_reset' and user.verification_code_purpose == 'set_password':
            pass
        elif purpose == 'set_password' and user.verification_code_purpose == 'password_reset':
            pass
        else:
            return False, Response({'error': 'Invalid or expired verification code'}, status=400)
    if user.verification_code_attempts >= MAX_CODE_ATTEMPTS:
        return False, Response({'error': 'Too many invalid attempts. Please request a new code.'}, status=429)
    if not verify_verification_code(code, user.verification_code or ''):
        User.objects.filter(pk=user.pk).update(verification_code_attempts=F('verification_code_attempts') + 1)
        return False, Response({'error': 'Invalid or expired verification code'}, status=400)
    return True, None

def _clear_verification_code(user):
    user.verification_code = None
    user.verification_code_expires = 0
    user.verification_code_purpose = ''
    user.verification_code_attempts = 0
    user.verification_code_last_sent_at = 0

def _paginated_response(request, queryset, serializer_class, *, context=None, default_page_size=50, max_page_size=100):
    paginator = PageNumberPagination()
    try:
        page_size = int(request.query_params.get('page_size', default_page_size))
    except (TypeError, ValueError):
        page_size = default_page_size
    paginator.page_size = max(1, min(page_size, max_page_size))
    page = paginator.paginate_queryset(queryset, request)

    ctx = context or {}
    user = _get_user_from_request(request)
    if user and page:
        if serializer_class == PostSerializer:
            ids = [p.id for p in page]
            ctx['liked_post_ids'] = set(PostLike.objects.filter(
                user=user, post_id__in=ids
            ).values_list('post_id', flat=True))
            ctx['bookmarked_post_ids'] = set(Bookmark.objects.filter(
                user=user, target_type='post', target_id__in=ids
            ).values_list('target_id', flat=True))
            ctx['user_poll_votes'] = dict(
                PollVote.objects.filter(
                    poll__post_id__in=ids, user=user
                ).values_list('poll_id', 'option_id')
            )
        elif serializer_class == ReplySerializer:
            ids = [r.id for r in page]
            ctx['liked_reply_ids'] = set(ReplyLike.objects.filter(
                user=user, reply_id__in=ids
            ).values_list('reply_id', flat=True))
            ctx['bookmarked_reply_ids'] = set(Bookmark.objects.filter(
                user=user, target_type='reply', target_id__in=ids
            ).values_list('target_id', flat=True))
        elif serializer_class == ResourceSerializer:
            ids = [r.id for r in page]
            ctx['liked_resource_ids'] = set(ResourceLike.objects.filter(
                user=user, resource_id__in=ids
            ).values_list('resource_id', flat=True))
            ctx['bookmarked_resource_ids'] = set(Bookmark.objects.filter(
                user=user, target_type='resource', target_id__in=[str(value) for value in ids]
            ).values_list('target_id', flat=True))

    serializer = serializer_class(page, many=True, context=ctx)
    return paginator.get_paginated_response(serializer.data)

def _link_oauth_user_model(email, user_pk, display_name, photo_url):
    """Link an OAuth user to an existing account by verified email.

    Instead of changing the existing account's PK (which is dangerous with InnoDB FKs),
    we transfer the OAuth identifiers to the existing account and delete the duplicate.
    This preserves all FK references to the existing account.
    """
    if not email:
        return None
    try:
        existing = User.objects.get(email__iexact=email)
        # Don't link to self
        if existing.pk == user_pk:
            return existing
        # Transfer display name and photo from OAuth account if existing doesn't have them
        update_fields = []
        if display_name and not existing.display_name:
            existing.display_name = display_name
            update_fields.append('display_name')
        if photo_url and not existing.photo_url:
            existing.photo_url = photo_url
            update_fields.append('photo_url')
        if not existing.auth_token:
            existing.auth_token = User.generate_token()
            update_fields.append('auth_token')
        if update_fields:
            existing.save(update_fields=update_fields)
        # Delete the OAuth-created duplicate account
        User.objects.filter(pk=user_pk).delete()
        return existing
    except User.DoesNotExist:
        return None
    except Exception:
        return None

def _build_stats(user):
    """
    Build the stats dict for a given User instance.
    Uses denormalized counters on the User model directly.
    """
    return {
        'username': user.username,
        'post_count': user.post_count,
        'reply_count': user.reply_count,
        'follower_count': user.follower_count,
        'following_count': user.following_count,
        'likes_received': user.likes_received_count,
        'likes_given': user.likes_given_count,
        'contribution_score': user.contribution_score,
    }

def _build_stats_batch(user_qs):
    """
    Build stats for a queryset of users using denormalized counters.
    Returns a dict mapping user_id -> stats dict.
    """
    result = {}
    for u in user_qs:
        result[u.id] = {
            'username': u.username,
            'display_name': u.display_name or u.username,
            'photo_url': u.photo_url or '',
            'post_count': u.post_count,
            'reply_count': u.reply_count,
            'follower_count': u.follower_count,
            'following_count': u.following_count,
            'likes_given': u.likes_given_count,
            'likes_received': u.likes_received_count,
            'contribution_score': u.contribution_score,
        }
    return result

def map_profile_grade(class_level):
    if not class_level:
        return None
    val = class_level.strip().lower()
    if val in ('11', 'grade 11', 'class 11'):
        return 'Class 11'
    elif val in ('12', 'grade 12', 'class 12'):
        return 'Class 12'
    elif val in ('10', 'see', 'class 10', 'class 10 / see'):
        return 'Class 10 / SEE'
    elif val in ('9', 'class 9'):
        return 'Class 9'
    elif val in ('8', 'class 8'):
        return 'Class 8'
    return class_level

def is_global_user(user):
    """Users who should see global/unfiltered content (no profile-based filtering)."""
    if not user:
        return True
    if user.role in ('teacher', 'institution', 'explorer'):
        return True
    if not user.class_level:
        return False
    cl = user.class_level.strip().lower()
    global_classes = {
        '+2', '+2 passout', 'passout', 'graduate', 'graduated',
        'bachelor', 'bachelors', 'bachelor\'s', 'ba', 'bsc', 'bbs',
        'master', 'masters', 'master\'s', 'ma', 'msc',
        'diploma', 'phd', 'ph.d', 'doctorate',
        'entrance prep', 'competitive exam', 'other', 'all',
    }
    if cl in global_classes:
        return True
    return False

# Star imports from this module are intentional: split view modules need the
# same helper functions and imported framework symbols that the former monolith
# exposed as globals. Keep this broad to avoid changing runtime behavior.
__all__ = [
    name for name in globals()
    if not name.startswith('__') and name not in {'annotations'}
] + ['is_global_user']
