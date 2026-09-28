"""Creator marketplace — storefront lifecycle and the one write path.

One storefront per eligible account (teacher, institution or admin). A page is
made of *blocks*: an ordered list of section descriptors the owner arranges
freely, plus a small `style` overlay (hero treatment, corner radius, density)
and `socials`. The Django templates and the Android renderer both read exactly
this shape, which is what keeps a page looking like the same page in both
places instead of drifting into two designs.

The catalogue lives in `creator_pages_schema`, the sanitizers in
`creator_pages_sanitize`, eligibility and paid-course access in
`creator_pages_access`, and the JSON shapes in `creator_pages_payloads`. This
module owns slugs, page creation and `apply_*` — the single validation path the
REST API and the Django studio both call, so the two clients cannot disagree
about what a valid page or course is. Every public name from the four modules
is re-exported here; importers see one module.
"""
import uuid
from decimal import Decimal

from django.utils.text import slugify

from .creator_pages_access import (
    allowed_kinds, can_have_storefront, check_user_course_access, course_access_map,
    default_kind_for,
)
from .creator_pages_payloads import (
    course_payload, linked_resource_ids, listing_queryset, page_payload, post_payload,
)
from .creator_pages_sanitize import (
    sanitize_accent, sanitize_blocks, sanitize_include_list, sanitize_socials,
    sanitize_style, _text,
)
from .creator_pages_schema import (
    ACCENT_RE, BLOCK_FIELDS, BLOCK_LABELS, DEFAULT_BLOCKS, DENSITIES, ELIGIBLE_ROLES,
    FIELD_LABELS, HERO_STYLES, ITEM_FIELDS, ITEM_LABELS, LAYOUTS, LIST_FIELDS,
    MAX_BLOCKS, MAX_LIST_ITEMS, RADII, SOCIAL_KEYS, URL_FIELDS, block_schema,
)
from .models import (
    CreatorCourse, CreatorCourseResource, CreatorPage, Resource, User,
)
from .utils import now_ms

__all__ = [
    'ACCENT_RE', 'BLOCK_FIELDS', 'BLOCK_LABELS', 'DEFAULT_BLOCKS', 'DENSITIES',
    'ELIGIBLE_ROLES', 'FIELD_LABELS', 'HERO_STYLES', 'ITEM_FIELDS', 'ITEM_LABELS',
    'LAYOUTS', 'LIST_FIELDS', 'MAX_BLOCKS', 'MAX_LIST_ITEMS', 'PAGE_TEXT_FIELDS',
    'RADII', 'SOCIAL_KEYS', 'URL_FIELDS',
    'allowed_kinds', 'apply_course_fields', 'apply_page_update', 'apply_post_fields',
    'block_schema', 'can_have_storefront', 'check_user_course_access',
    'course_access_map', 'course_payload', 'default_kind_for', 'linked_resource_ids', 'listing_queryset', 'page_for_user',
    'page_payload', 'post_payload', 'sanitize_accent', 'sanitize_blocks',
    'sanitize_include_list', 'sanitize_socials', 'sanitize_style', 'slugify_creator',
    'sync_course_resources', 'unique_course_slug', 'unique_page_slug',
]


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
