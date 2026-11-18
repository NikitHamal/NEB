"""Views Profile extracted from views.py."""
import json
from api import services
from api.models import (
    Bookmark,
    PaymentVerification,
    Post,
    Reply,
    Resource,
    ResourceLike,
    SellerBalance,
    User,
    UserPhoto,
    WithdrawalRequest,
)
from api.utils import now_ms, uuid_str
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from api.resource_catalog import upload_form_options
from . import api_client as api
from .view_helpers import (
    _avatar_url,
    _build_local_stats,
    _clear_page_cache,
    _ctx,
    _get_user_id,
    _rate_limit,
    _request_db_user,
    _serialize_posts,
    _serialize_replies,
    _serialize_resources,
    _user_achievement_badges,
    _user_badge_info,
    _viewer_for_locked_check,
    get_or_create_seller_balance,
)
from api.services import record_username_change
from api.view_helpers import _profile_incomplete, _can_view_locked_profile, _overlong_field_error
from api.models import Follow, FollowRequest, NEPAL_DISTRICTS, SocialLink, SocialLinkClick
from api.marketplace import get_payment_config
from api.utils import money_str
from api.social_links import (
    get_user_links, get_all_user_links, create_link as _create_social_link,
    update_link as _update_social_link, delete_link as _delete_social_link,
    reorder_links as _reorder_social_links,
)
from io import BytesIO
from pathlib import Path
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


def bookmarks(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    current_user = _request_db_user(request, user_id)
    if current_user is None:
        return redirect('web:login')

    bookmarks_qs = list(Bookmark.objects.filter(user_id=user_id).order_by('-created_at')[:200])
    post_ids = [b.target_id for b in bookmarks_qs if b.target_type == 'post']
    reply_ids = [b.target_id for b in bookmarks_qs if b.target_type == 'reply']
    resource_ids = [b.target_id for b in bookmarks_qs if b.target_type == 'resource']

    posts = {p.id: p for p in Post.objects.select_related('user').filter(id__in=post_ids)}
    replies = {r.id: r for r in Reply.objects.select_related('user', 'post').filter(id__in=reply_ids)}
    resources = {r.id: r for r in Resource.objects.filter(id__in=resource_ids)}

    items = []
    counts = {'all': 0, 'post': 0, 'reply': 0, 'resource': 0}
    for bm in bookmarks_qs:
        title = ''
        url = '#'
        excerpt = ''
        meta = ''
        if bm.target_type == 'post' and bm.target_id in posts:
            obj = posts[bm.target_id]
            title = obj.title or 'Untitled discussion'
            url = reverse('web:forum_post', kwargs={'post_id': obj.id})
            excerpt = obj.content or ''
            meta = f'{obj.user.display_name or obj.user.username} Â· {obj.reply_count} replies'
        elif bm.target_type == 'reply' and bm.target_id in replies:
            obj = replies[bm.target_id]
            title = f"Reply on {obj.post.title if obj.post else 'discussion'}"
            url = reverse('web:forum_post', kwargs={'post_id': obj.post_id}) + f"#reply-{obj.id}"
            excerpt = obj.content or ''
            meta = f'{obj.user.display_name or obj.user.username} Â· Reply'
        elif bm.target_type == 'resource' and bm.target_id in resources:
            obj = resources[bm.target_id]
            if obj.approval_status != 'approved' and obj.uploaded_by_id != user_id:
                continue
            title = obj.title or 'Untitled resource'
            url = reverse('web:reader', kwargs={'resource_id': obj.id})
            excerpt = obj.description or ''
            meta = f"{obj.subject or 'Resource'} Â· {obj.grade_level or 'All levels'}"
        else:
            continue
        counts['all'] += 1
        counts[bm.target_type] += 1
        items.append({
            'type': bm.target_type,
            'created_at': bm.created_at,
            'title': title,
            'url': url,
            'excerpt': excerpt,
            'meta': meta,
            'id': bm.target_id,
        })

    return render(request, 'web/bookmarks.html', _ctx(request,
        current_user=current_user,
        bookmark_items=items,
        bookmark_counts=counts,
    ))

def _cover_art_for(user):
    from api.cover_art import default_cover, is_valid_cover
    chosen = (getattr(user, 'cover_art', '') or '').strip()
    return chosen if chosen and is_valid_cover(chosen) else default_cover(user.username)


def _cover_choices():
    from api.cover_art import cover_rows
    return [{'id': r[0], 'layout': r[1], 'palette': r[2]} for r in cover_rows()]


@require_POST
def ajax_set_cover_art(request):
    """POST /ajax/profile/cover/ {cover: "cover-019" | ""}: the signed-in member picks a cover from the M3X art library."""
    from api.cover_art import is_valid_cover
    from .views_onboarding import _owner
    owner = _owner(request)
    if owner is None:
        return JsonResponse({'ok': False, 'error': 'Please sign in again.'}, status=401)
    try:
        data = json.loads(request.body or b'{}')
    except ValueError:
        data = {}
    cover = str(data.get('cover', '') if isinstance(data, dict) else '').strip()[:16]
    if not is_valid_cover(cover):
        return JsonResponse({'ok': False, 'error': 'That cover is not available.'}, status=400)
    owner.cover_art = cover
    owner.save(update_fields=['cover_art'])
    _clear_page_cache()
    return JsonResponse({'ok': True, 'cover': _cover_art_for(owner)})


def profile(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    viewer_user = _request_db_user(request, user_id)
    is_self = bool(viewer_user and viewer_user.pk == profile_user.pk)
    profile_private = not _can_view_locked_profile(viewer_user, profile_user)
    is_following_profile = False
    is_requested_profile = False
    if viewer_user and not is_self:
        is_following_profile = Follow.objects.filter(follower_id=viewer_user.pk, following_id=profile_user.pk).exists()
        is_requested_profile = FollowRequest.objects.filter(sender_id=viewer_user.pk, receiver_id=profile_user.pk).exists()

    badge_info = _user_badge_info(profile_user)

    # The cover role, and the word tracked into its bottom-right corner. Same
    # priority and same strings as the app's `bannerPresetFor`, because both
    # platforms feed them to the same generative art and a divergence here
    # would give one user two different covers.
    banner_role = 'MEMBER'
    banner_deco_text = 'nebian'
    if profile_user.is_bot:
        banner_role, banner_deco_text = 'BOT', 'neby ai'
    elif profile_user.is_admin:
        banner_role, banner_deco_text = 'ADMIN', 'admin'
    elif profile_user.moderator_level and profile_user.moderator_level > 0:
        banner_role, banner_deco_text = 'MODERATOR', 'moderator'
    elif profile_user.verification_level and profile_user.verification_level > 0:
        banner_role, banner_deco_text = 'VERIFIED', 'nebian'
    elif getattr(profile_user, 'role', '') == 'teacher':
        banner_role, banner_deco_text = 'TUTOR', 'tutor'
    elif getattr(profile_user, 'role', '') == 'institution':
        banner_role, banner_deco_text = 'INSTITUTION', 'institution'

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': _avatar_url(profile_user),
        'banner_url': profile_user.banner_url,
        'cover_art': _cover_art_for(profile_user),
        'banner_role': banner_role,
        'banner_deco_text': banner_deco_text,
        'display_name': profile_user.display_name,
        'role': profile_user.role,
        'dob': profile_user.dob,
        'gender': profile_user.gender,
        'class_level': profile_user.class_level,
        'class': profile_user.class_level,
        'subjects': profile_user.subjects,
        'teaching_subjects': profile_user.teaching_subjects,
        'institution_type': profile_user.institution_type,
        'pradesh': profile_user.pradesh,
        'district': profile_user.district,
        'school': profile_user.school,
        'school_username': profile_user.school_username,
        'bio': profile_user.bio,
        'headline': profile_user.headline,
        'is_locked': 1 if profile_user.is_locked else 0,
        'created_at': profile_user.created_at,
        'verification_level': profile_user.verification_level,
        'moderator_level': profile_user.moderator_level,
        'is_admin': profile_user.is_admin,
        'is_bot': profile_user.is_bot,
        'teacher_verified': profile_user.teacher_verified,
        'institution_verified': profile_user.institution_verified,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': badge_info,
        'achievement_info': _user_achievement_badges(profile_user),
    }

    from web.views_institutions_profile import school_context
    profile_data.update(school_context(profile_user))

    if profile_private:
        profile_data.update({
            'email': '', 'dob': '', 'gender': '', 'class_level': '', 'class': '',
            'subjects': '', 'pradesh': '', 'district': '', 'school': '', 'school_url': '', 'school_slug': '',
        })

    stats = _build_local_stats(profile_user, exclude_anonymous=True) if not profile_private else {
        'post_count': 0, 'reply_count': 0, 'likes_given': 0, 'likes_received': 0, 'contribution_score': 0,
    }

    follower_count = (getattr(profile_user, 'follower_count', 0) or 0) if not profile_private else 0
    following_count = (getattr(profile_user, 'following_count', 0) or 0) if not profile_private else 0
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = is_following_profile
    stats['is_requested'] = is_requested_profile
    stats['is_self'] = is_self

    if is_self:
        uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id, is_lead=True).count()
    else:
        uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved', is_lead=True).count()
    stats['uploaded_resources_count'] = uploaded_resources_count

    user_posts_qs = Post.objects.none() if profile_private else Post.objects.select_related('user').filter(user_id=profile_user.id, is_anonymous=False).order_by('-created_at')[:10]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    user_replies_qs = Reply.objects.none() if profile_private else Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id, is_anonymous=False, is_archived=False).order_by('-created_at')[:10]
    user_replies = _serialize_replies(user_replies_qs, user_id)

    user_resources = []
    if is_self:
        user_resources_qs = list(Resource.objects.filter(uploaded_by_id=profile_user.id, is_lead=True).order_by('-added_at')[:60])
    else:
        user_resources_qs = list(Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved', is_lead=True).order_by('-added_at')[:60])

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
            'file_url': r.file_url or '',
            'thumbnail_url': r.thumbnail_url or '',
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

    # Retrieve pending requests if profile is locked and it is the owner
    pending_requests = []
    pending_requests_count = 0
    if is_self and profile_user.is_locked:
        pending_requests_qs = FollowRequest.objects.select_related('sender').filter(receiver_id=profile_user.id).order_by('-created_at')
        pending_requests_count = pending_requests_qs.count()
        for req in pending_requests_qs:
            pending_requests.append({
                'id': req.id,
                'sender_id': req.sender.id,
                'sender_username': req.sender.username,
                'sender_display_name': req.sender.display_name or req.sender.username,
                'sender_photo': _avatar_url(req.sender),
            })

    seller_balance = None
    sales_history = []
    withdrawal_history = []
    if is_self:
        seller_balance = get_or_create_seller_balance(profile_user)
        sales_history = PaymentVerification.objects.filter(seller=profile_user).select_related('buyer', 'resource').order_by('-created_at')[:100]
        withdrawal_history = WithdrawalRequest.objects.filter(user=profile_user).order_by('-created_at')[:100]

    social_links_data = []
    if not profile_private and not profile_user.is_bot:
        social_links_data = get_user_links(profile_user.id)

    from api import profile_education as _pe
    from api.education_catalog import kinds_for
    portfolio = None
    if not profile_private and not profile_user.is_bot:
        portfolio = {
            'edu': _pe.education_summary(profile_user),
            'open_to': _pe.open_to_items(profile_user),
            'skills': _pe.skills_list(profile_user),
            'sections': _pe.portfolio_sections(profile_user),
            'kinds': kinds_for(profile_user.role),
            'teacher': _pe.teacher_summary(profile_user),
            'is_own': bool(viewer_user and getattr(viewer_user, 'id', None) == profile_user.id),
        }
        if portfolio['teacher']:
            past = sum(len(x['items']) for x in portfolio['sections'] if x['value'] == 'past_school')
            portfolio['teacher']['past'] = [i for x in portfolio['sections'] if x['value'] == 'past_school' for i in x['items']]
            portfolio['sections'] = [x for x in portfolio['sections'] if x['value'] != 'past_school']
            portfolio['teacher']['schools'] = past + (1 if portfolio['teacher']['school'] else 0)
            portfolio['teacher']['is_set'] = portfolio['teacher']['is_set'] or bool(past)
        if portfolio['teacher'] and portfolio['is_own']:
            from api.education_catalog import EMPLOYMENT, TEACH_LEVELS
            csv = lambda x: [i for i in (x or '').split(',') if i]
            portfolio['teacher_boot'] = {
                'school': profile_user.school or '', 'employment': profile_user.employment or '',
                'subjects': csv(profile_user.teaching_subjects), 'levels': csv(profile_user.teach_levels),
                'years': int(profile_user.experience_years or 0), 'headline': profile_user.headline or '',
                'optLevels': TEACH_LEVELS, 'optEmployment': EMPLOYMENT,
            }
    from .views_inst_folio import profile_extras
    extras = profile_extras(profile_user, is_self, bool(portfolio and (portfolio['sections'] or (portfolio['teacher'] or {}).get('past')))) if not profile_private else {'strength': None, 'inst': None}
    from api.profile_glance import build as build_glance
    overview = build_glance(profile_user) if not profile_private else {'glance': [], 'studying': None}
    return render(request, 'web/profile.html', _ctx(request,
        overview=overview,
        portfolio=portfolio, strength=extras['strength'], inst_folio=extras['inst'],
        profile_user=profile_data,
        cover_choices=_cover_choices() if is_self else [],
        cover_art=profile_data['cover_art'],
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
        pending_requests=pending_requests,
        pending_requests_count=pending_requests_count,
        social_links=social_links_data,
        social_links_json=json.dumps(social_links_data),
        seller_balance=seller_balance,
        sales_history=sales_history,
        withdrawal_history=withdrawal_history,
    ))


@require_POST
def ajax_request_withdrawal(request):
    """Allows sellers to submit withdrawal requests when minimum 1000 NPR threshold is met."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'status': 'error', 'error': 'Authentication required.'}, status=401)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'error': 'User not found.'}, status=404)

    from decimal import Decimal
    raw_amount = request.POST.get('amount', '0').strip()
    payout_method = request.POST.get('payout_method', 'esewa').strip().lower()
    payout_details = request.POST.get('payout_details', '').strip()

    # The model offers five; hardcoding three here quietly turned a ConnectIPS or
    # mobile-banking request into an eSewa one.
    if payout_method not in [choice[0] for choice in WithdrawalRequest.PAYOUT_METHODS]:
        payout_method = 'esewa'

    try:
        amount = Decimal(raw_amount)
    except Exception:
        return JsonResponse({'status': 'error', 'error': 'Invalid withdrawal amount.'}, status=400)

    # Decimal('nan') parses happily and then raises on every comparison below.
    if not amount.is_finite():
        return JsonResponse({'status': 'error', 'error': 'Invalid withdrawal amount.'}, status=400)

    # The studio advertises the configured floor, so this has to be the same
    # number -- a hardcoded Rs. 1,000 rejected requests the page invited.
    minimum = get_payment_config().withdraw_min or Decimal('1000.00')
    if amount < minimum:
        return JsonResponse(
            {'status': 'error', 'error': f'Minimum withdrawal threshold is Rs. {money_str(minimum)}.'},
            status=400,
        )

    if not payout_details:
        return JsonResponse({'status': 'error', 'error': 'Please provide payout account details (Account holder name, ID, or phone number).'}, status=400)

    seller_bal = get_or_create_seller_balance(user)
    if seller_bal.current_balance < amount:
        return JsonResponse({
            'status': 'error',
            'error': f'Insufficient balance. Your available balance is Rs. {seller_bal.current_balance:.2f}.'
        }, status=400)

    if WithdrawalRequest.objects.filter(user=user, status='pending').exists():
        return JsonResponse({'status': 'error', 'error': 'You already have a pending withdrawal request under review.'}, status=400)

    with transaction.atomic():
        # Debit with a guarded UPDATE rather than a read-modify-write. The same
        # row is credited by every payment approval, and a full-row save() here
        # would write back a balance read before that credit committed; the
        # `current_balance__gte` filter doubles as the check, so two requests
        # racing each other cannot both pass it.
        debited = (SellerBalance.objects
                   .filter(pk=seller_bal.pk, current_balance__gte=amount)
                   .update(current_balance=F('current_balance') - amount,
                           updated_at=now_ms()))
        if not debited:
            return JsonResponse({
                'status': 'error',
                'error': 'Insufficient balance. Please reload and try again.',
            }, status=400)
        WithdrawalRequest.objects.create(
            id=uuid_str(),
            user=user,
            amount=amount,
            payout_method=payout_method,
            payout_details=payout_details,
            status='pending',
            created_at=now_ms(),
        )

    seller_bal.refresh_from_db()
    return JsonResponse({
        'status': 'success',
        'message': f'Withdrawal request for Rs. {amount:.2f} submitted successfully!',
        'new_balance': float(seller_bal.current_balance)
    })

def profile_achievements(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    viewer_user = _request_db_user(request, user_id)
    if not _can_view_locked_profile(viewer_user, profile_user):
        return redirect('web:profile', username=username)

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': _avatar_url(profile_user),
        'banner_url': profile_user.banner_url,
        'display_name': profile_user.display_name,
        'role': profile_user.role,
        'dob': profile_user.dob,
        'gender': profile_user.gender,
        'class_level': profile_user.class_level,
        'class': profile_user.class_level,
        'subjects': profile_user.subjects,
        'teaching_subjects': profile_user.teaching_subjects,
        'institution_type': profile_user.institution_type,
        'pradesh': profile_user.pradesh,
        'district': profile_user.district,
        'school': profile_user.school,
        'bio': profile_user.bio,
        'is_locked': 1 if profile_user.is_locked else 0,
        'created_at': profile_user.created_at,
        'verification_level': profile_user.verification_level,
        'moderator_level': profile_user.moderator_level,
        'is_admin': profile_user.is_admin,
        'teacher_verified': profile_user.teacher_verified,
        'institution_verified': profile_user.institution_verified,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': _user_badge_info(profile_user),
        'achievement_info': _user_achievement_badges(profile_user),
    }

    stats = _build_local_stats(profile_user, exclude_anonymous=True)
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
        achievement_info=_user_achievement_badges(profile_user),
    ))


def _load_profile_card_font(weight='regular', size=32):
    from PIL import ImageFont
    base = Path(settings.BASE_DIR) / 'web/static/web/fonts'
    names = {
        'bold': 'poppins_bold.ttf',
        'semibold': 'poppins_medium.ttf',
        'medium': 'poppins_medium.ttf',
        'regular': 'poppins_regular.ttf',
    }
    try:
        return ImageFont.truetype(str(base / names.get(weight, 'poppins_regular.ttf')), size)
    except Exception:
        pass
    # Fallback to system fonts
    fallbacks = []
    if weight in ('bold', 'semibold'):
        fallbacks = [
            '/usr/share/fonts/urw-base35/NimbusSans-Bold.t1',
            '/usr/share/fonts/google-droid-sans-fonts/DroidSansFallbackFull.ttf',
        ]
    else:
        fallbacks = [
            '/usr/share/fonts/urw-base35/NimbusSans-Regular.t1',
            '/usr/share/fonts/google-droid-sans-fonts/DroidSansFallbackFull.ttf',
        ]
    for path in fallbacks:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _profile_card_avatar(user, size=152):
    from PIL import Image, ImageDraw, ImageOps
    img = Image.new('RGBA', (size, size), (239, 242, 246, 255))
    src = None
    url = (getattr(user, 'photo_url', '') or '').strip()

    def _load_local_media(media_path):
        try:
            rel = media_path.replace(settings.MEDIA_URL, '', 1).lstrip('/')
            src_path = Path(settings.MEDIA_ROOT) / rel
            if src_path.exists() and src_path.is_file():
                return Image.open(src_path).convert('RGBA')
        except Exception:
            return None
        return None

    if url:
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            media_url = settings.MEDIA_URL or '/media/'
            if url.startswith(media_url):
                src = _load_local_media(url)
            elif parsed.scheme in ('http', 'https') and parsed.path.startswith(media_url):
                src = _load_local_media(parsed.path)
            elif parsed.scheme == 'https':
                # Most social-card photos come from OAuth profile photos. Load them
                # only after NEBians' external URL validation and with a tiny cap.
                from api.security import validate_profile_photo_url
                import requests
                validate_profile_photo_url(url)
                resp = requests.get(
                    url,
                    timeout=2.5,
                    stream=True,
                    headers={'User-Agent': 'NEBians social card renderer'},
                )
                resp.raise_for_status()
                ctype = (resp.headers.get('content-type') or '').lower()
                if ctype.startswith('image/'):
                    max_bytes = 3 * 1024 * 1024
                    content = resp.raw.read(max_bytes + 1, decode_content=True)
                    if len(content) <= max_bytes:
                        src = Image.open(BytesIO(content)).convert('RGBA')
        except Exception:
            src = None

    if src:
        img = ImageOps.fit(src, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))
    else:
        d = ImageDraw.Draw(img)
        initial = (user.display_name or user.username or 'N')[:1].upper()
        f = _load_profile_card_font('bold', int(size * 0.43))
        bbox = d.textbbox((0, 0), initial, font=f)
        d.text(((size-(bbox[2]-bbox[0]))/2, (size-(bbox[3]-bbox[1]))/2-4), initial, font=f, fill=(0, 75, 212, 255))
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size-1, size-1), fill=255)
    out = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    out.paste(img, (0, 0), mask)
    return out


def profile_card_image(request, username):
    """Open Graph card PNG for a profile.

    The two-panel gradient card this used to draw is gone; profiles now use the
    same drawn card as the rest of the site (web/og_cards.py), so a shared
    profile looks like a shared resource looks like a shared thread. The URL
    stays because it is already in the wild.
    """
    if _rate_limit(request, 'profile_card_image', 30, 60, by_ip=True):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    from . import views_og
    try:
        spec = views_og._profile_card(username)
    except Http404:
        raise
    except Exception:
        raise Http404('Card unavailable')
    return views_og._render_response('profile', username, spec)


def ajax_profile_activity(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    viewer_user = _viewer_for_locked_check(user_id, profile_user)
    if not _can_view_locked_profile(viewer_user, profile_user):
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    user_posts_qs = Post.objects.select_related('user').filter(user_id=profile_user.id, is_anonymous=False).order_by('-created_at')[offset:offset+limit]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    total_count = Post.objects.filter(user_id=profile_user.id, is_anonymous=False).count()
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

    viewer_user = _viewer_for_locked_check(user_id, profile_user)
    if not _can_view_locked_profile(viewer_user, profile_user):
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    replies_qs = Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id, is_anonymous=False, is_archived=False).order_by('-created_at')[offset:offset+limit]
    replies = _serialize_replies(replies_qs, user_id)

    total_count = Reply.objects.filter(user_id=profile_user.id, is_anonymous=False, is_archived=False).count()
    has_more = (offset + len(replies)) < total_count

    return JsonResponse({
        'replies': replies,
        'has_more': has_more,
        'total_count': total_count
    })

def ajax_profile_resources(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    viewer_user = None
    if user_id:
        try:
            viewer_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            viewer_user = None
    if not _can_view_locked_profile(viewer_user, profile_user):
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    is_self = bool(viewer_user and viewer_user.pk == profile_user.pk)
    if is_self:
        resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id, is_lead=True).order_by('-added_at')[offset:offset+limit]
        total_count = Resource.objects.filter(uploaded_by_id=profile_user.id, is_lead=True).count()
    else:
        resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved', is_lead=True).order_by('-added_at')[offset:offset+limit]
        total_count = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved', is_lead=True).count()

    resources = _serialize_resources(resources_qs)
    has_more = (offset + len(resources)) < total_count

    return JsonResponse({
        'resources': resources,
        'has_more': has_more,
        'total_count': total_count
    })

def edit_profile(request):
    token = api.get_session_token(request)
    if not token:
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    user = api.get_session_user(request)
    if not user:
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    try:
        db_user = User.objects.get(id=user.get('id'))
    except User.DoesNotExist:
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    if not getattr(db_user, 'email_verified', False):
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    has_password = bool(db_user.password_hash)
    from api import education_catalog as _cat
    from api.profile_education import apply_education
    edu_init = {
        'status': db_user.edu_status or '', 'level': db_user.class_level or '',
        'program': db_user.edu_program or '', 'term': db_user.edu_term or '',
        'completed': db_user.edu_completed or '', 'headline': db_user.headline or '',
        'skills': db_user.skills or '', 'open_to': db_user.open_to or '',
    }
    edu_boot = {'catalog': _cat.catalog(), 'initial': {
        'status': edu_init['status'], 'level': edu_init['level'], 'program': edu_init['program'],
        'term': edu_init['term'], 'completed': edu_init['completed'],
        'skills': edu_init['skills'], 'openTo': edu_init['open_to']}}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        dob = request.POST.get('dob', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        gender = request.POST.get('gender', '').strip()
        role = request.POST.get('role', db_user.role).strip().lower()
        from api.education_catalog import canonical_level
        class_level = canonical_level(request.POST.get('class_level', ''))
        if role not in ('student', 'teacher', 'institution', 'explorer'):
            role = db_user.role or 'student'
        is_inst = role == 'institution'  # no date of birth or gender for an institution
        if is_inst:
            dob = gender = ''
        if not username or (not dob and not is_inst):
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error='Username and Date of Birth are required.'))
        if not display_name:
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error='Display Name is required.'))
        if not gender and not is_inst:
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error='Gender is required.'))
        if role == 'student' and not class_level:
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error='Class is required for students.'))
        if role == 'teacher' and not request.POST.get('teaching_subjects', '').strip():
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error='Teaching subjects are required for teachers.'))
        if role == 'institution' and not request.POST.get('school', '').strip():
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error='Institution name is required.'))
        overlong = _overlong_field_error(User, {
            'display_name': display_name,
            'gender': gender,
            'class_level': class_level,
            'pradesh': request.POST.get('pradesh', ''),
            'school': request.POST.get('school', '').strip(),
            'school_username': request.POST.get('school_username', '').strip(),
            'institution_type': request.POST.get('institution_type', ''),
            'dob': dob,
        })
        if overlong:
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error=overlong.data['error'] + '.'))
        if username != db_user.username:
            _v_err, _v_code = services.validate_username_change(db_user, username)
            if _v_err:
                return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error=_v_err.get('error', 'Username change failed.')))
            db_user.username = username
            record_username_change(db_user)
        else:
            db_user.username = username
        new_email = request.POST.get('email', '').strip() or db_user.email or ''
        if new_email and new_email.lower() != (db_user.email or '').lower():
            db_user.email_verified = False
        db_user.email = new_email
        db_user.display_name = display_name or db_user.display_name or ''
        db_user.role = role
        db_user.dob = dob
        db_user.gender = '' if is_inst else (gender or db_user.gender or '')
        db_user.class_level = class_level or db_user.class_level or ''
        db_user.subjects = request.POST.get('subjects', '') or db_user.subjects or ''
        db_user.teaching_subjects = request.POST.get('teaching_subjects', '') or db_user.teaching_subjects or ''
        db_user.institution_type = request.POST.get('institution_type', '') or db_user.institution_type or ''
        db_user.pradesh = request.POST.get('pradesh', '') or db_user.pradesh or ''
        district_val = request.POST.get('district', '').strip()
        if district_val and district_val not in NEPAL_DISTRICTS:
            district_val = ''
        db_user.district = district_val or db_user.district or ''
        from api.institutions import apply_school
        apply_school(db_user, request.POST.get('school_slug', ''), request.POST.get('school', ''),
                     request.POST.get('school_username', ''))
        db_user.bio = request.POST.get('bio', '').strip()
        db_user.is_locked = request.POST.get('is_locked') == 'on'
        edu_error = apply_education(db_user, request.POST)
        if edu_error:
            return render(request, 'web/edit_profile.html', _ctx(request, edu_boot=edu_boot, edu_init=edu_init, error=edu_error))
        db_user.save()
        _clear_page_cache()
        updated_data = {
            'id': db_user.id,
            'username': db_user.username,
            'email': db_user.email,
            'photo_url': db_user.photo_url,
            'display_name': db_user.display_name,
            'role': db_user.role,
            'dob': db_user.dob,
            'gender': db_user.gender,
            'class_level': db_user.class_level,
            'class': db_user.class_level,
            'subjects': db_user.subjects,
            'teaching_subjects': db_user.teaching_subjects,
            'institution_type': db_user.institution_type,
            'pradesh': db_user.pradesh,
            'district': db_user.district,
            'school': db_user.school,
            'school_username': db_user.school_username,
            'school_slug': db_user.school_slug,
            'bio': db_user.bio,
            'is_locked': 1 if db_user.is_locked else 0,
            'created_at': db_user.created_at,
        }
        api.set_session_auth(request, token, updated_data)
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url and next_url.startswith('/') and not next_url.startswith('//'):
            return redirect(next_url)
        return redirect('web:home')
    profile_incomplete = _profile_incomplete(db_user)
    subjects = upload_form_options()['subjects']
    existing_social_links = get_all_user_links(db_user.id)
    from api.models import SOCIAL_PLATFORMS
    return render(request, 'web/edit_profile.html', _ctx(request,
        edu_boot=edu_boot, edu_init=edu_init,
        has_password=has_password,
        profile_incomplete=profile_incomplete,
        subjects=subjects,
        existing_social_links=existing_social_links,
        existing_social_links_json=json.dumps(existing_social_links),
        social_platforms=SOCIAL_PLATFORMS,
    ))


def delete_account_page(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        db_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')

    from api.models import AccountDeletionRequest
    from api.utils import now_ms, uuid_str
    from datetime import datetime

    pending_request = AccountDeletionRequest.objects.filter(
        user=db_user,
        status=AccountDeletionRequest.STATUS_PENDING
    ).first()

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        if action == 'request':
            reason = request.POST.get('reason', '').strip()
            if not pending_request:
                created_at = now_ms()
                scheduled_delete_at = created_at + 30 * 24 * 60 * 60 * 1000  # 30 days in ms
                pending_request = AccountDeletionRequest.objects.create(
                    id=uuid_str(),
                    user=db_user,
                    reason=reason,
                    status=AccountDeletionRequest.STATUS_PENDING,
                    created_at=created_at,
                    scheduled_delete_at=scheduled_delete_at
                )
            # Render success page
            return render(request, 'web/delete_account_success.html', _ctx(request,
                scheduled_date=datetime.fromtimestamp(pending_request.scheduled_delete_at / 1000.0).strftime('%B %d, %Y')
            ))
        elif action == 'cancel':
            AccountDeletionRequest.objects.filter(
                user=db_user,
                status=AccountDeletionRequest.STATUS_PENDING
            ).delete()
            return redirect('web:delete_account')

    scheduled_date_str = None
    if pending_request:
        scheduled_date_str = datetime.fromtimestamp(pending_request.scheduled_delete_at / 1000.0).strftime('%B %d, %Y')

    return render(request, 'web/delete_account.html', _ctx(request,
        pending_request=pending_request,
        scheduled_date=scheduled_date_str
    ))


def settings_page(request):
    token = api.get_session_token(request)
    if not token:
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    user = api.get_session_user(request)
    if not user:
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    try:
        db_user = User.objects.get(id=user.get('id'))
    except User.DoesNotExist:
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    if not getattr(db_user, 'email_verified', False):
        return redirect(f"{reverse('web:login')}?next={request.get_full_path()}")
    has_password = bool(db_user.password_hash)

    from api.models import AccountDeletionRequest
    pending_request = AccountDeletionRequest.objects.filter(
        user=db_user,
        status=AccountDeletionRequest.STATUS_PENDING
    ).first()

    return render(request, 'web/settings.html', _ctx(request, has_password=has_password, pending_request=pending_request,
                                                       notify_new_resources=bool(db_user.notify_new_resources)))


@require_POST
def ajax_toggle_profile_visibility(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        db_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)

    try:
        data = json.loads(request.body)
        is_locked = bool(data.get('is_locked', False))
        db_user.is_locked = is_locked
        db_user.save()
        _clear_page_cache()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'status': 'ok', 'is_locked': db_user.is_locked})


@require_POST
def ajax_toggle_inline_images(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        db_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    try:
        data = json.loads(request.body)
        enabled = bool(data.get('enabled', True))
        db_user.enable_inline_images = enabled
        db_user.save(update_fields=['enable_inline_images'])
        try:
            sess = api.get_session_user(request)
            if sess:
                sess['enable_inline_images'] = enabled
                sess['enableInlineImages'] = enabled
                tok = api.get_session_token(request)
                if tok:
                    api.set_session_auth(request, tok, sess)
        except Exception:
            pass
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'status': 'ok', 'enabled': db_user.enable_inline_images})

def _require_auth_user(request):
    user_id = _get_user_id(request)
    if not user_id:
        return None, JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        return User.objects.get(pk=user_id), None
    except User.DoesNotExist:
        return None, JsonResponse({'error': 'User not found'}, status=404)


def ajax_social_links_list(request):
    user, err = _require_auth_user(request)
    if err:
        return err
    return JsonResponse({'links': get_all_user_links(user.id)})


def ajax_social_links_create(request):
    user, err = _require_auth_user(request)
    if err:
        return err
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    import json as _json
    try:
        data = _json.loads(request.body)
    except (ValueError, KeyError):
        data = request.POST
    platform = (data.get('platform') or 'website').strip().lower()
    url = (data.get('url') or '').strip()
    label = (data.get('label') or '').strip()
    try:
        link = _create_social_link(user.id, platform, url, label)
        _clear_page_cache()
        return JsonResponse({'ok': True, 'link': link})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def ajax_social_links_update(request, link_id):
    user, err = _require_auth_user(request)
    if err:
        return err
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    import json as _json
    try:
        data = _json.loads(request.body)
    except (ValueError, KeyError):
        data = request.POST
    try:
        link = _update_social_link(
            user.id, link_id,
            platform=data.get('platform'),
            url=data.get('url'),
            label=data.get('label'),
        )
        _clear_page_cache()
        return JsonResponse({'ok': True, 'link': link})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def ajax_social_links_delete(request, link_id):
    user, err = _require_auth_user(request)
    if err:
        return err
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        _delete_social_link(user.id, link_id)
        _clear_page_cache()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def ajax_social_links_reorder(request):
    user, err = _require_auth_user(request)
    if err:
        return err
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    import json as _json
    try:
        data = _json.loads(request.body)
        ordered_ids = data.get('ordered_ids', [])
    except (ValueError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not isinstance(ordered_ids, list):
        return JsonResponse({'error': 'ordered_ids must be a list'}, status=400)
    try:
        links = _reorder_social_links(user.id, ordered_ids)
        _clear_page_cache()
        return JsonResponse({'ok': True, 'links': links})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_POST
def ajax_social_links_track_click(request):
    from api.utils import now_ms
    from datetime import date
    import json as _json
    try:
        data = _json.loads(request.body)
    except (ValueError, KeyError):
        data = request.POST
    link_id = data.get('link_id')
    target_user_id = data.get('user_id')
    platform = (data.get('platform') or '').strip()
    url = (data.get('url') or '').strip()
    if not link_id or not target_user_id or not platform:
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    try:
        link = SocialLink.objects.get(id=link_id, user_id=target_user_id)
    except SocialLink.DoesNotExist:
        return JsonResponse({'error': 'Link not found'}, status=404)
    clicker_id = _get_user_id(request)
    if clicker_id is not None and str(clicker_id) == str(link.user_id):
        return JsonResponse({'ok': True})
    is_follower = None
    clicker_gender = ''
    clicker_age = None
    if clicker_id is not None:
        is_follower = Follow.objects.filter(follower_id=clicker_id, following_id=link.user_id).exists()
        try:
            clicker_user = User.objects.get(pk=clicker_id)
            clicker_gender = clicker_user.gender or ''
            if clicker_user.dob:
                try:
                    parts = clicker_user.dob.split('-')
                    if len(parts) == 3:
                        bd = date(int(parts[0]), int(parts[1]), int(parts[2]))
                        today = date.today()
                        clicker_age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
                except (ValueError, IndexError):
                    pass
        except User.DoesNotExist:
            pass
    clicker_country = (request.META.get('HTTP_CF_IPCOUNTRY') or '').strip().upper()
    SocialLinkClick.objects.create(
        link=link, user=link.user,
        clicker_id=str(clicker_id) if clicker_id is not None else None, platform=platform,
        url=url, created_at=now_ms(),
        is_follower=is_follower,
        clicker_country=clicker_country,
        clicker_gender=clicker_gender,
        clicker_age=clicker_age,
    )
    return JsonResponse({'ok': True})


def credits_page(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        current_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')

    from api.credit_views import check_and_reset_monthly_credits, WHATSAPP_CONTACT
    from api.models import NebyCreditTransaction
    current_user = check_and_reset_monthly_credits(current_user)

    transactions = NebyCreditTransaction.objects.filter(user=current_user).order_by('-created_at')[:30]

    ctx = _ctx(request)
    ctx.update({
        'title': 'Neby Credits — NEBians',
        'active_nav': 'credits',
        'current_user': current_user,
        'free_credits': current_user.free_credits,
        'ai_credits': current_user.ai_credits,
        'total_credits': current_user.free_credits + current_user.ai_credits,
        'nebians_points': current_user.nebians_points,
        'free_credits_month': current_user.free_credits_month,
        'whatsapp_contact': WHATSAPP_CONTACT,
        'transactions': transactions,
    })
    return render(request, 'web/credits.html', ctx)

