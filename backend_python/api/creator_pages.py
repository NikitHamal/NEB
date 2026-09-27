"""Creator marketplace — the data layer behind the storefront pages.

One storefront per eligible account (teacher, institution or admin). A page is
made of *blocks*: an ordered list of section descriptors the owner arranges
freely, plus a small `style` overlay (hero treatment, corner radius, density)
and `socials`. The Django templates and the Android renderer both read exactly
this shape, which is what keeps a page looking like the same page in both
places instead of drifting into two designs.

Every value coming from a client passes a sanitizer here before it is stored:
unknown block types are dropped, unknown keys inside a known block are dropped,
strings are trimmed and capped, and every URL must be http(s) or a site-relative
path. That is the whole reason a page can be "fully customizable" without
becoming a stored-XSS surface.
"""
import re
import uuid
from decimal import Decimal

from django.utils.text import slugify

from .models import (
    CreatorPage, CreatorCourse, CreatorCourseResource, CreatorPost,
    PaymentVerification, Resource, User,
)
from .utils import now_ms

ELIGIBLE_ROLES = (User.ROLE_TEACHER, User.ROLE_INSTITUTION)

MAX_BLOCKS = 24
MAX_LIST_ITEMS = 24
ACCENT_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

LAYOUTS = ('editorial', 'spotlight', 'grid', 'classic')
HERO_STYLES = ('plain', 'art', 'cover')
RADII = ('soft', 'round', 'sharp')
DENSITIES = ('comfortable', 'compact')

BLOCK_FIELDS = {
    'hero': ('title', 'subtitle', 'cta_label', 'cta_url', 'image_url'),
    'about': ('title', 'body'),
    'stats': ('title',),
    'courses': ('title', 'subtitle'),
    'resources': ('title', 'subtitle'),
    'posts': ('title', 'subtitle'),
    'showcase': ('title', 'subtitle'),
    'gallery': ('title', 'subtitle'),
    'testimonials': ('title',),
    'faq': ('title',),
    'schedule': ('title',),
    'contact': ('title', 'body'),
    'links': ('title',),
    'cta': ('title', 'subtitle', 'cta_label', 'cta_url'),
    'documents': ('title', 'subtitle'),
}

LIST_FIELDS = {
    'stats': 'items',
    'showcase': 'items',
    'gallery': 'images',
    'testimonials': 'items',
    'faq': 'items',
    'schedule': 'items',
    'links': 'items',
}

ITEM_FIELDS = {
    'stats': ('label', 'value', 'icon'),
    'showcase': ('title', 'subtitle', 'image_url', 'link_url', 'badge'),
    'testimonials': ('name', 'role', 'quote', 'avatar_url'),
    'faq': ('q', 'a'),
    'schedule': ('day', 'time', 'title', 'note'),
    'links': ('label', 'url', 'icon'),
}

URL_FIELDS = ('cta_url', 'image_url', 'link_url', 'url', 'media_url', 'promo_url')

SOCIAL_KEYS = (
    'website', 'facebook', 'instagram', 'youtube', 'tiktok', 'x', 'linkedin',
    'github', 'telegram', 'viber', 'whatsapp', 'email', 'phone',
)

DEFAULT_BLOCKS = [
    {'type': 'hero', 'title': '', 'subtitle': '', 'cta_label': 'Browse offerings',
     'cta_url': '', 'image_url': ''},
    {'type': 'about', 'title': 'About',
     'body': 'Tell students who you are, what you teach and how you teach it.'},
    {'type': 'courses', 'title': 'Courses and classes',
     'subtitle': 'Paid and free offerings'},
    {'type': 'resources', 'title': 'Resources', 'subtitle': 'Notes, papers and guides'},
    {'type': 'contact', 'title': 'Get in touch', 'body': ''},
]


# --------------------------------------------------------------------------
# Eligibility
# --------------------------------------------------------------------------

def can_have_storefront(user):
    if user is None:
        return False
    if getattr(user, 'is_admin', False):
        return True
    if getattr(user, 'is_banned', False) or getattr(user, 'is_locked', False):
        return False
    return getattr(user, 'role', '') in ELIGIBLE_ROLES


def allowed_kinds(user):
    if user is None:
        return []
    if getattr(user, 'is_admin', False):
        return ['admin', 'institute', 'tutor']
    if getattr(user, 'role', '') == User.ROLE_INSTITUTION:
        return ['institute', 'tutor']
    return ['tutor']


def default_kind_for(user):
    kinds = allowed_kinds(user)
    return kinds[0] if kinds else 'tutor'


# --------------------------------------------------------------------------
# Sanitizers
# --------------------------------------------------------------------------

def _text(value, limit=400):
    if value is None:
        return ''
    if not isinstance(value, str):
        value = str(value)
    return value.strip()[:limit]


def _clean_url(value):
    if not isinstance(value, str):
        return ''
    value = value.strip()
    if not value:
        return ''
    if value.startswith('/') and not value.startswith('//'):
        return value[:600]
    if re.match(r'^https?://', value, re.IGNORECASE):
        return value[:600]
    return ''


def _bool(value):
    return value in (True, 'true', 'True', 'on', '1', 1, 'yes')


def sanitize_accent(value):
    value = (value or '').strip()
    return value.upper() if ACCENT_RE.match(value) else '#004BD4'


def sanitize_style(raw):
    if not isinstance(raw, dict):
        return {}
    style = {
        'hero': raw.get('hero') if raw.get('hero') in HERO_STYLES else 'art',
        'radius': raw.get('radius') if raw.get('radius') in RADII else 'round',
        'density': raw.get('density') if raw.get('density') in DENSITIES else 'comfortable',
        'show_stats': _bool(raw.get('show_stats')),
        'show_contact': _bool(raw.get('show_contact', True)),
        'show_verified': raw.get('show_verified') is not False,
    }
    columns = raw.get('gallery_columns')
    try:
        style['gallery_columns'] = min(4, max(2, int(columns))) if columns else 3
    except (TypeError, ValueError):
        style['gallery_columns'] = 3
    return style


def sanitize_socials(raw):
    if not isinstance(raw, dict):
        return {}
    socials = {}
    for key in SOCIAL_KEYS:
        value = raw.get(key)
        if not isinstance(value, str) or not value.strip():
            continue
        value = value.strip()
        if key in ('email', 'phone'):
            socials[key] = _text(value, 120)
            continue
        clean = _clean_url(value)
        if clean:
            socials[key] = clean
    return socials


def _sanitize_items(block_type, raw):
    key = LIST_FIELDS.get(block_type)
    if not key:
        return None
    if key == 'images':
        if not isinstance(raw, list):
            return []
        return [_clean_url(item) for item in raw if _clean_url(item)][:MAX_LIST_ITEMS]
    if not isinstance(raw, list):
        return []
    fields = ITEM_FIELDS.get(block_type, ())
    items = []
    for entry in raw[:MAX_LIST_ITEMS]:
        if not isinstance(entry, dict):
            continue
        item = {}
        for field in fields:
            value = entry.get(field)
            item[field] = _clean_url(value) if field in URL_FIELDS else _text(value, 800)
        if any(item.values()):
            items.append(item)
    return items


def sanitize_blocks(raw):
    if not isinstance(raw, list):
        return []
    blocks = []
    for entry in raw[:MAX_BLOCKS]:
        if not isinstance(entry, dict):
            continue
        block_type = _text(entry.get('type'), 20).lower()
        if block_type not in BLOCK_FIELDS:
            continue
        block = {'id': _text(entry.get('id'), 40) or uuid.uuid4().hex[:10], 'type': block_type,
                 'enabled': entry.get('enabled') is not False}
        for field in BLOCK_FIELDS[block_type]:
            value = entry.get(field)
            block[field] = _clean_url(value) if field in URL_FIELDS else _text(value, 4000 if field == 'body' else 300)
        items = _sanitize_items(block_type, entry.get(LIST_FIELDS.get(block_type)) if LIST_FIELDS.get(block_type) else None)
        if items is not None:
            block[LIST_FIELDS[block_type]] = items
        blocks.append(block)
    return blocks


def sanitize_include_list(raw):
    if isinstance(raw, str):
        raw = [part for part in raw.split('\n')]
    if not isinstance(raw, list):
        return []
    return [_text(item, 160) for item in raw[:20] if _text(item, 160)]


# --------------------------------------------------------------------------
# Slugs
# --------------------------------------------------------------------------

def slugify_creator(value, fallback='creator'):
    base = slugify(value or '')[:70].strip('-')
    return base or f'{fallback}-{uuid.uuid4().hex[:6]}'


def unique_page_slug(base, exclude_id=None):
    candidate = base
    suffix = 1
    qs = CreatorPage.objects.all()
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    while qs.filter(slug=candidate).exists():
        suffix += 1
        candidate = f'{base[:70]}-{suffix}'
    return candidate


def unique_course_slug(page, base, exclude_id=None):
    candidate = slugify(base or 'course')[:80].strip('-') or f'course-{uuid.uuid4().hex[:6]}'
    qs = CreatorCourse.objects.filter(page=page)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    suffix = 1
    while qs.filter(slug=candidate).exists():
        suffix += 1
        candidate = f'{base[:76]}-{suffix}'
    return candidate


# --------------------------------------------------------------------------
# Page lifecycle
# --------------------------------------------------------------------------

def page_for_user(user, create=False):
    if user is None:
        return None
    page = CreatorPage.objects.filter(user=user).first()
    if page or not create or not can_have_storefront(user):
        return page
    display = (getattr(user, 'display_name', '') or user.username or 'Nebian').strip()
    return CreatorPage.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        kind=default_kind_for(user),
        slug=unique_page_slug(slugify_creator(display, 'creator')),
        display_name=display[:120],
        tagline=_default_tagline(user),
        about=_text(getattr(user, 'bio', ''), 4000),
        avatar_url=_text(getattr(user, 'photo_url', ''), 600),
        cover_url=_text(getattr(user, 'banner_url', ''), 600),
        subjects=_text(getattr(user, 'teaching_subjects', '') or getattr(user, 'subjects', ''), 400),
        location=', '.join(part for part in [getattr(user, 'district', ''), getattr(user, 'pradesh', '')] if part)[:120],
        blocks=sanitize_blocks(DEFAULT_BLOCKS),
        style=sanitize_style({}),
        created_at=now_ms(),
        updated_at=now_ms(),
    )


def _default_tagline(user):
    role = getattr(user, 'role', '')
    if getattr(user, 'is_admin', False):
        return 'The NEBians team'
    if role == User.ROLE_INSTITUTION:
        return 'An institute on NEBians'
    return 'A teacher on NEBians'


# --------------------------------------------------------------------------
# Access control
# --------------------------------------------------------------------------

def check_user_course_access(user, course):
    """Mirror of check_user_resource_access() for paid courses.

    Returns (has_access, reason, purchase|None) with the same reasons so a
    client can render one purchase state machine for both kinds."""
    if course is None:
        return False, 'missing', None
    if course.is_free or not course.price or Decimal(course.price) <= 0:
        return True, 'free', None
    if user is None:
        return False, 'unpurchased', None
    if course.page_id and course.page.user_id == getattr(user, 'id', None):
        return True, 'owner', None
    if getattr(user, 'is_admin', False):
        return True, 'admin', None
    purchase = (PaymentVerification.objects
                .filter(buyer_id=user.id, course_id=course.id)
                .order_by('-created_at')
                .first())
    if purchase:
        if purchase.status == 'approved':
            return True, 'purchased', purchase
        if purchase.status == 'pending':
            return False, 'pending_verification', purchase
        if purchase.status == 'rejected':
            return False, 'rejected', purchase
    return False, 'unpurchased', None


# --------------------------------------------------------------------------
# Payloads
# --------------------------------------------------------------------------

def _account_payload(user):
    if user is None:
        return None
    return {
        'id': user.id,
        'username': user.username,
        'display_name': user.display_name or user.username,
        'photo_url': user.photo_url or '',
        'role': getattr(user, 'role', ''),
        'verified': bool(getattr(user, 'teacher_verified', False) or getattr(user, 'institution_verified', False)),
    }


def course_payload(course, viewer=None, include_purchase=True):
    has_access, reason, purchase = check_user_course_access(viewer, course)
    payload = {
        'id': course.id,
        'page_id': course.page_id,
        'page_slug': getattr(course.page, 'slug', ''),
        'page_name': getattr(course.page, 'display_name', ''),
        'title': course.title,
        'slug': course.slug,
        'summary': course.summary or '',
        'description': course.description or '',
        'cover_url': course.cover_url or '',
        'promo_url': course.promo_url or '',
        'is_free': bool(course.is_free),
        'price': _money(course.price),
        'level': course.level or '',
        'duration_label': course.duration_label or '',
        'lesson_count': course.lesson_count or 0,
        'seat_limit': course.seat_limit or 0,
        'includes': list(course.includes or []),
        'tags': course.tag_list,
        'status': course.status,
        'featured': bool(course.featured),
        'enrollment_count': course.enrollment_count or 0,
        'view_count': course.view_count or 0,
        'sale_count': course.sale_count or 0,
        'rating': float(course.rating or 0),
        'rating_count': course.rating_count or 0,
        'created_at': course.created_at or 0,
        'updated_at': course.updated_at or 0,
    }
    if include_purchase:
        payload['has_access'] = bool(has_access)
        payload['access_reason'] = reason
        payload['purchase_status'] = getattr(purchase, 'status', '') if purchase else ''
        payload['purchase_id'] = getattr(purchase, 'id', '') if purchase else ''
    return payload


def post_payload(post):
    return {
        'id': post.id,
        'title': post.title or '',
        'body': post.body or '',
        'media_url': post.media_url or '',
        'link_url': post.link_url or '',
        'pinned': bool(post.pinned),
        'published': bool(post.published),
        'like_count': post.like_count or 0,
        'created_at': post.created_at or 0,
    }


def _money(value):
    try:
        amount = float(value or 0)
    except (TypeError, ValueError):
        return '0'
    return ('%g' % amount) if amount else '0'


def page_payload(page, viewer=None, include_drafts=False, with_content=True):
    owner_viewing = viewer is not None and page.user_id == getattr(viewer, 'id', None)
    only_published = not (owner_viewing or (viewer is not None and getattr(viewer, 'is_admin', False)))
    courses = page.courses.all()
    if only_published:
        courses = courses.filter(status='published')
    payload = {
        'id': page.id,
        'slug': page.slug,
        'kind': page.kind,
        'display_name': page.display_name,
        'tagline': page.tagline or '',
        'about': page.about or '',
        'avatar_url': page.avatar_url or '',
        'cover_url': page.cover_url or '',
        'accent_hex': page.accent_hex or '#004BD4',
        'layout': page.layout,
        'style': page.style or {},
        'blocks': page.blocks or [],
        'socials': page.socials or {},
        'contact_email': page.contact_email or '',
        'contact_phone': page.contact_phone or '',
        'location': page.location or '',
        'subjects': page.subject_list,
        'languages': page.language_list,
        'verified': bool(page.verified),
        'featured': bool(page.featured),
        'published': bool(page.published),
        'accepting_students': bool(page.accepting_students),
        'follower_count': page.follower_count or 0,
        'view_count': page.view_count or 0,
        'course_count': _course_count(page),
        'is_mine': bool(owner_viewing),
        'owner': _account_payload(page.user),
        'url': f'/marketplace/{page.slug}/',
    }
    if not with_content:
        return payload
    course_list = [course_payload(course, viewer, include_purchase=False) for course in courses]
    payload['courses'] = course_list
    payload['course_count'] = len(course_list)
    payload['paid_course_count'] = sum(1 for c in course_list if not c['is_free'])
    resources = (Resource.objects
                 .filter(uploaded_by_id=page.user_id, approval_status='approved')
                 .order_by('-added_at')[:24])
    payload['resources'] = [_resource_payload(r) for r in resources]
    posts = page.page_posts.all()
    if only_published:
        posts = posts.filter(published=True)
    payload['posts'] = [post_payload(p) for p in posts[:12]]
    return payload


def _course_count(page):
    annotated = getattr(page, 'published_course_count', None)
    if annotated is not None:
        return annotated
    return page.courses.filter(status='published').count()


def _resource_payload(resource):
    return {
        'id': resource.id,
        'title': resource.title,
        'subject': resource.subject or '',
        'type': resource.type or '',
        'grade_level': resource.grade_level or '',
        'thumbnail_url': resource.thumbnail_url or '',
        'is_paid': bool(resource.is_paid),
        'price': _money(resource.price),
        'view_count': resource.view_count or 0,
        'added_at': resource.added_at or 0,
    }


def listing_queryset(viewer=None, viewer_is_admin=False):
    """Every storefront a viewer may browse, with the published-course count
    annotated so a card never costs a query of its own."""
    from django.db.models import Count, Q as _Q

    qs = (CreatorPage.objects
          .select_related('user')
          .annotate(published_course_count=Count('courses', filter=_Q(courses__status='published'), distinct=True)))
    is_admin = viewer_is_admin or (viewer is not None and getattr(viewer, 'is_admin', False))
    if not is_admin:
        qs = qs.filter(published=True)
    return qs


def linked_resource_ids(page):
    return list(CreatorCourseResource.objects.filter(course__page=page).values_list('resource_id', flat=True))


# --------------------------------------------------------------------------
# Writes — one validation path for the REST API and the Django studio
# --------------------------------------------------------------------------

PAGE_TEXT_FIELDS = (('tagline', 180), ('about', 4000), ('location', 120), ('contact_phone', 40))


def apply_page_update(page, data, allowed=None):
    """Apply a page payload from either client. Returns (page, error_message).

    `allowed` is the set of page kinds the account may use; passing it is what
    stops an institute from relabelling itself as NEBians Official. It is a
    required argument in spirit — every caller passes the viewer's own kinds.
    """
    if not isinstance(data, dict):
        return page, 'Invalid payload'

    def _has(key):
        return key in data

    if _has('display_name'):
        name = str(data.get('display_name') or '').strip()
        if not name:
            return page, 'Your page needs a name'
        page.display_name = name[:120]

    if _has('slug'):
        base = slugify_creator(str(data.get('slug') or ''), 'creator')
        page.slug = unique_page_slug(base, exclude_id=page.pk)

    if _has('kind'):
        kind = str(data.get('kind') or '').strip().lower()
        if kind not in ('tutor', 'institute', 'admin'):
            return page, 'Unknown page kind'
        if allowed is not None and kind not in allowed:
            return page, 'You cannot create that kind of page'
        page.kind = kind

    for field, limit in PAGE_TEXT_FIELDS:
        if _has(field):
            setattr(page, field, str(data.get(field) or '').strip()[:limit])

    if _has('contact_email'):
        email = str(data.get('contact_email') or '').strip()[:254]
        if email and '@' not in email:
            return page, 'Enter a valid contact email'
        page.contact_email = email

    for field in ('avatar_url', 'cover_url'):
        if _has(field):
            value = str(data.get(field) or '').strip()
            setattr(page, field, value[:600] if value.startswith(('http://', 'https://', '/')) else '')

    if _has('accent_hex'):
        page.accent_hex = sanitize_accent(data.get('accent_hex'))

    if _has('layout'):
        layout = str(data.get('layout') or '').strip().lower()
        if layout in LAYOUTS:
            page.layout = layout

    if _has('style'):
        page.style = sanitize_style(data.get('style'))
    if _has('blocks'):
        page.blocks = sanitize_blocks(data.get('blocks'))
    if _has('socials'):
        page.socials = sanitize_socials(data.get('socials'))

    for field in ('subjects', 'languages'):
        if _has(field):
            raw = data.get(field)
            if isinstance(raw, list):
                raw = ','.join(str(part) for part in raw)
            setattr(page, field, str(raw or '').strip()[:400])

    for field in ('published', 'accepting_students'):
        if _has(field):
            setattr(page, field, data.get(field) in (True, 'true', 'True', 'on', '1', 1))

    if page.published and not page.display_name:
        return page, 'Add a name before publishing'

    page.updated_at = now_ms()
    page.save()
    return page, None


def apply_course_fields(course, page, data):
    """Create or update a course. Returns (course, pending_resource_ids, error).

    Resource links come back as ids rather than being written here, because a
    course that has not been saved yet has no primary key to attach them to.
    """
    if not isinstance(data, dict):
        return course, None, 'Invalid payload'

    new_course = course is None
    if new_course:
        course = CreatorCourse()
    pending_resource_ids = None

    def _has(key):
        return key in data

    if _has('title'):
        title = str(data.get('title') or '').strip()
        if not title:
            return None, None, 'Give the course a title'
        course.title = title[:180]
    if new_course and not (course.title or '').strip():
        return None, None, 'Give the course a title'

    if _has('slug'):
        course.slug = slugify_creator(str(data.get('slug') or '') or course.title, 'course')

    for field, limit in (('summary', 300), ('level', 60), ('duration_label', 60), ('tags', 300)):
        if _has(field):
            setattr(course, field, str(data.get(field) or '').strip()[:limit])

    if _has('description'):
        course.description = str(data.get('description') or '').strip()[:20000]

    for field in ('cover_url', 'promo_url'):
        if _has(field):
            value = str(data.get(field) or '').strip()
            setattr(course, field, value[:600] if value.startswith(('http://', 'https://', '/')) else '')

    if _has('is_free'):
        course.is_free = data.get('is_free') in (True, 'true', 'True', 'on', '1', 1)

    if _has('price'):
        raw = str(data.get('price') or '0').strip() or '0'
        try:
            price = Decimal(raw)
        except Exception:
            return None, None, 'Enter a valid price'
        if price < 0:
            return None, None, 'Price cannot be negative'
        if price > Decimal('1000000'):
            return None, None, 'That price looks wrong'
        course.price = price

    if course.is_free:
        course.price = Decimal('0.00')
    elif (course.price or 0) <= 0:
        publish_intent = _has('status') and str(data.get('status')).lower() == 'published'
        if publish_intent or _has('is_free'):
            return None, None, 'A paid course needs a price above Rs. 0'

    for field, limit in (('lesson_count', 999), ('seat_limit', 100000)):
        if _has(field):
            try:
                value = int(data.get(field) or 0)
            except (TypeError, ValueError):
                return None, None, f'Invalid {field.replace("_", " ")}'
            setattr(course, field, max(0, min(limit, value)))

    if _has('sort_order'):
        try:
            course.sort_order = int(data.get('sort_order') or 0)
        except (TypeError, ValueError):
            course.sort_order = 0

    if _has('includes'):
        course.includes = sanitize_include_list(data.get('includes'))

    if _has('status'):
        status_value = str(data.get('status') or '').strip().lower()
        if status_value not in ('draft', 'published', 'archived'):
            return None, None, 'Unknown course status'
        if status_value == 'published' and (not course.is_free) and (course.price or 0) <= 0:
            return None, None, 'A paid course needs a price above Rs. 0'
        course.status = status_value

    if _has('featured'):
        course.featured = data.get('featured') in (True, 'true', 'True', 'on', '1', 1)

    if _has('resource_ids'):
        ids = data.get('resource_ids') or []
        if isinstance(ids, str):
            ids = [part for part in ids.split(',') if part.strip()]
        pending_resource_ids = [str(item) for item in ids if str(item).strip()]
        if not new_course:
            sync_course_resources(course, page, pending_resource_ids)
            pending_resource_ids = None

    return course, pending_resource_ids, None


def sync_course_resources(course, page, resource_ids):
    valid = list(Resource.objects.filter(id__in=resource_ids, uploaded_by_id=page.user_id).values_list('id', flat=True))
    CreatorCourseResource.objects.filter(course=course).exclude(resource_id__in=valid).delete()
    existing = set(CreatorCourseResource.objects.filter(course=course).values_list('resource_id', flat=True))
    for order, resource_id in enumerate(valid):
        if resource_id in existing:
            CreatorCourseResource.objects.filter(course=course, resource_id=resource_id).update(sort_order=order)
        else:
            CreatorCourseResource.objects.create(course=course, resource_id=resource_id, sort_order=order)


def apply_post_fields(post, data):
    if not isinstance(data, dict):
        return post, 'Invalid payload'
    for field, limit in (('title', 180), ('body', 20000)):
        if field in data:
            setattr(post, field, str(data.get(field) or '').strip()[:limit])
    for field in ('media_url', 'link_url'):
        if field in data:
            value = str(data.get(field) or '').strip()
            setattr(post, field, value[:600] if value.startswith(('http://', 'https://', '/')) else '')
    for field in ('pinned', 'published'):
        if field in data:
            setattr(post, field, data.get(field) in (True, 'true', 'True', 'on', '1', 1))
    post.updated_at = now_ms()
    post.save()
    return post, None


BLOCK_LABELS = {
    'hero': 'Hero', 'about': 'About', 'stats': 'Numbers', 'courses': 'Courses',
    'resources': 'Resources', 'posts': 'Updates', 'showcase': 'Showcase',
    'gallery': 'Gallery', 'testimonials': 'Testimonials', 'faq': 'FAQ',
    'schedule': 'Schedule', 'contact': 'Contact', 'links': 'Links', 'cta': 'Call to action',
    'documents': 'Documents',
}

FIELD_LABELS = {
    'title': 'Heading', 'subtitle': 'Subheading', 'body': 'Text',
    'cta_label': 'Button label', 'cta_url': 'Button link', 'image_url': 'Image URL',
    'items': 'Items', 'images': 'Image URLs',
}

ITEM_LABELS = {
    'label': 'Label', 'value': 'Value', 'icon': 'Icon', 'title': 'Title',
    'subtitle': 'Subtitle', 'image_url': 'Image URL', 'link_url': 'Link',
    'badge': 'Badge', 'name': 'Name', 'role': 'Role', 'quote': 'Quote',
    'avatar_url': 'Avatar URL', 'q': 'Question', 'a': 'Answer', 'day': 'Day',
    'time': 'Time', 'note': 'Note', 'url': 'Link',
}


def block_schema():
    """The block catalogue the studio editor and the app builder both render."""
    schema = []
    for block_type, fields in BLOCK_FIELDS.items():
        list_key = LIST_FIELDS.get(block_type)
        schema.append({
            'type': block_type,
            'label': BLOCK_LABELS.get(block_type, block_type.title()),
            'fields': [{'key': f, 'label': FIELD_LABELS.get(f, f.replace('_', ' ').title()),
                        'multiline': f == 'body', 'url': f in URL_FIELDS}
                       for f in fields],
            'list_key': list_key,
            'item_fields': [{'key': f, 'label': ITEM_LABELS.get(f, f.replace('_', ' ').title()),
                             'url': f in URL_FIELDS}
                            for f in ITEM_FIELDS.get(block_type, ())],
            'item_hint': 'One image URL per line' if block_type == 'gallery' else '',
        })
    return schema
