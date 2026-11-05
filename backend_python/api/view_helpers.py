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

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import F
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .security import (
    hash_verification_code, verify_verification_code,
)
from .models import User, ResourceLike, Post, PostLike, PollVote, ReplyLike, Follow, Bookmark
from .utils import now_ms
_now_ms = now_ms
from .serializers import (
    ResourceSerializer, PostSerializer,
    ReplySerializer,
)

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
    if getattr(user, 'is_banned', False):
        return None, Response({'error': 'This account has been banned'}, status=403)
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

def _overlong_field_error(model, values):
    for name, value in values.items():
        if not value:
            continue
        limit = model._meta.get_field(name).max_length
        if limit and len(str(value)) > limit:
            label = name.replace('_', ' ').capitalize()
            return Response({
                'error': f'{label} must be {limit} characters or fewer',
                'field': name,
            }, status=400)
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

def prime_for_serializers(user, posts=(), resources=(), replies=()):
    """Batch everything PostSerializer / ResourceSerializer / ReplySerializer read per row.

    Relations come in one query per relation instead of one per row, and the viewer's
    like/bookmark/vote state comes back as a serializer context (posts, replies) or as
    ``_viewer_*`` attributes (resources). Returns the context to merge."""
    from django.db.models import prefetch_related_objects
    ctx = {}
    posts, resources, replies = list(posts), list(resources), list(replies)
    if posts:
        prefetch_related_objects(posts, 'user', 'images', 'media', 'poll__options')
    if replies:
        prefetch_related_objects(replies, 'user', 'media')
    if resources:
        prefetch_related_objects(resources, 'uploaded_by')
    if not user:
        return ctx
    if posts:
        ids = [p.id for p in posts]
        ctx['liked_post_ids'] = set(PostLike.objects.filter(user=user, post_id__in=ids).values_list('post_id', flat=True))
        ctx['bookmarked_post_ids'] = set(Bookmark.objects.filter(user=user, target_type='post', target_id__in=ids)
                                         .values_list('target_id', flat=True))
        # The polls were prefetched above, so a page without one needs no vote lookup.
        if any(_may_have_poll(p) for p in posts):
            _votes = {}
            for _pid, _oid in PollVote.objects.filter(poll__post_id__in=ids, user=user).values_list('poll_id', 'option_id'):
                _votes.setdefault(_pid, set()).add(_oid)
            ctx['user_poll_votes'] = _votes
        else:
            ctx['user_poll_votes'] = {}
    if resources:
        rids = [r.pk for r in resources]
        liked = set(ResourceLike.objects.filter(user=user, resource_id__in=rids).values_list('resource_id', flat=True))
        marked = set(Bookmark.objects.filter(user=user, target_type='resource', target_id__in=[str(i) for i in rids])
                     .values_list('target_id', flat=True))
        for r in resources:
            r._viewer_liked = r.pk in liked
            r._viewer_bookmarked = str(r.pk) in marked
        ctx['liked_resource_ids'] = liked
        ctx['bookmarked_resource_ids'] = marked
        # Paid cards look up the viewer's purchases one card at a time (two queries each);
        # batch them when a page holds more than one.
        if sum(1 for r in resources if r.is_paid) > 1:
            from web.view_helpers import prefetch_resource_purchases
            prefetch_resource_purchases(user, resources)
    return ctx


def _may_have_poll(post):
    """False only when the post's (prefetched) poll relation is cached as empty. Never queries."""
    rel = Post._meta.get_field('poll')
    return not rel.is_cached(post) or rel.get_cached_value(post) is not None


def _page_size(request, default_page_size, max_page_size):
    try:
        page_size = int(request.query_params.get('page_size', default_page_size))
    except (TypeError, ValueError):
        page_size = default_page_size
    return max(1, min(page_size, max_page_size))


def _serialize_page(request, page, serializer_class, context):
    ctx = context or {}
    user = _get_user_from_request(request)
    if page:
        if serializer_class == PostSerializer:
            ctx.update(prime_for_serializers(user, posts=page))
        elif serializer_class == ResourceSerializer:
            ctx.update(prime_for_serializers(user, resources=page))
        elif serializer_class == ReplySerializer:
            ctx.update(prime_for_serializers(user, replies=page))
            if user:
                ids = [r.id for r in page]
                ctx['liked_reply_ids'] = set(ReplyLike.objects.filter(
                    user=user, reply_id__in=ids
                ).values_list('reply_id', flat=True))
                ctx['bookmarked_reply_ids'] = set(Bookmark.objects.filter(
                    user=user, target_type='reply', target_id__in=ids
                ).values_list('target_id', flat=True))
    return serializer_class(page, many=True, context=ctx).data


def _paginated_response(request, queryset, serializer_class, *, context=None, default_page_size=50, max_page_size=100):
    paginator = PageNumberPagination()
    paginator.page_size = _page_size(request, default_page_size, max_page_size)
    page = paginator.paginate_queryset(queryset, request)
    return paginator.get_paginated_response(_serialize_page(request, page, serializer_class, context))


def _page_rows(request, queryset, page_size, peek=False):
    """The rows of one PageNumberPagination page, without the COUNT(*) behind its total.

    For callers that never send the total to the client. Pages are numbered the same way
    and a bad or out-of-range ?page= gets the same 404 ("Invalid page."): a page past the
    end is exactly a page with no rows, other than page 1.

    With ``peek`` it reads one row past the page and returns ``(rows, has_more)``, which
    tells the client whether another page exists without counting the table."""
    from rest_framework.exceptions import NotFound
    raw = request.query_params.get(PageNumberPagination.page_query_param) or 1
    if raw in PageNumberPagination.last_page_strings:
        paginator = PageNumberPagination()  # 'last' needs the total
        paginator.page_size = page_size
        rows = paginator.paginate_queryset(queryset, request)
        return (rows, False) if peek else rows
    invalid = NotFound(PageNumberPagination.invalid_page_message.format(page_number=raw, message=''))
    try:
        number = int(raw)
    except (TypeError, ValueError):
        raise invalid
    if number < 1:
        raise invalid
    bottom = (number - 1) * page_size
    if bottom + page_size > 2 ** 62:
        raise invalid  # past the end of any table; an OFFSET this large would be a DB error
    rows = list(queryset[bottom:bottom + page_size + (1 if peek else 0)])
    if not rows and number > 1:
        raise invalid
    if peek:
        return rows[:page_size], len(rows) > page_size
    return rows


def _page_results(request, queryset, serializer_class, *, context=None, default_page_size=50, max_page_size=100):
    """``_paginated_response(...).data['results']`` without counting the whole result set."""
    page = _page_rows(request, queryset, _page_size(request, default_page_size, max_page_size))
    return _serialize_page(request, page, serializer_class, context)

def _link_oauth_user_model(email, user_pk, display_name, photo_url, provider_verified=True):
    """Link an OAuth user to an existing account by verified email.

    Instead of changing the existing account's PK (which is dangerous with InnoDB FKs),
    we transfer the OAuth identifiers to the existing account and delete the duplicate.
    This preserves all FK references to the existing account.

    Links ONLY when the provider asserts a verified email AND the existing
    account already verified that email (blocks pre-account-takeover via
    squatted unverified signups).
    """
    if not email or not provider_verified:
        return None
    try:
        existing = User.objects.get(email__iexact=email)
        # Don't link to self
        if existing.pk == user_pk:
            return existing
        if getattr(existing, 'is_banned', False):
            return None
        if not existing.email_verified:
            return None
        # Transfer display name and photo from OAuth account if existing doesn't have them
        update_fields = []
        if display_name and not existing.display_name:
            existing.display_name = display_name
            update_fields.append('display_name')
        if photo_url and not existing.photo_url:
            existing.photo_url = photo_url
            update_fields.append('photo_url')
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

def _global_statuses():
    from .education_catalog import GLOBAL_STATUSES
    return GLOBAL_STATUSES

def is_global_user(user):
    """Users who should see global/unfiltered content (no profile-based filtering)."""
    if not user:
        return True
    if user.role in ('teacher', 'institution', 'explorer'):
        return True
    if (getattr(user, 'edu_status', '') or '') in _global_statuses():
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
    from .education_catalog import GLOBAL_LEVELS, GLOBAL_STATUSES
    if cl in GLOBAL_LEVELS or (getattr(user, 'edu_status', '') or '') in GLOBAL_STATUSES:
        return True
    return False

def parse_paid_fields(data):
    """Parse is_paid + price from request data (multipart form or JSON).

    Accepts both snake_case ('is_paid'/'price') and camelCase ('isPaid').
    Returns (is_paid: bool, price: Decimal). A non-paid resource always
    normalises price to 0.00; a negative/invalid price falls back to 0.00.
    """
    from decimal import Decimal, InvalidOperation

    def _truthy(key):
        return data.get(key) in ('on', 'true', '1', 1, True, 'yes')

    is_paid = _truthy('is_paid') or _truthy('isPaid')
    raw_price = data.get('price')
    if isinstance(raw_price, (int, float)):
        raw_price = str(raw_price)
    raw_price = ((raw_price or '0') or '0').strip() or '0'
    try:
        price_val = Decimal(raw_price)
    except (InvalidOperation, ValueError, TypeError):
        price_val = Decimal('0.00')
    if price_val < 0:
        price_val = Decimal('0.00')
    if not is_paid:
        price_val = Decimal('0.00')
    return is_paid, price_val


# Star imports from this module are intentional: split view modules need the
# same helper functions and imported framework symbols that the former monolith
# exposed as globals. Keep this broad to avoid changing runtime behavior.
__all__ = [
    name for name in globals()
    if not name.startswith('__') and name not in {'annotations'}
] + ['is_global_user']
