"""Creator marketplace — the JSON shapes the web and the app both read.

One payload builder per object. The REST API returns these verbatim and the
Django views hand the same dicts to their templates, which is what keeps a
storefront looking like the same storefront in both places.
"""
from .creator_pages_access import check_user_course_access
from .creator_themes import palette as _palette
from .models import CreatorPage, CreatorCourseResource, Resource
from .utils import money_str as _money


def theme_payload(style, accent_hex=''):
    """A creator's look with the colours already worked out.

    The renderers get hex, not a palette name. That is deliberate: if Android
    carried its own copy of the palette table, the day somebody nudged one hex
    in Python would be the day the same page looked different on a phone. There
    is one table, it lives in `creator_themes.py`, and this is where it is read.

    `accent_hex` still wins when the creator has picked their own colour -- the
    palette is a starting point, not a cage. It is compared against the
    palette's *light* accent to decide whether it is a choice at all, because
    that is the value `apply_page_update` writes when a creator picks a palette
    and nothing else. Without that comparison a dark Ink page would wear the
    near-black accent meant for its light ramp, and nothing on it would be
    visible.
    """
    style = style or {}
    scheme = style.get('scheme') if style.get('scheme') in ('light', 'dark') else 'light'
    colours = dict(_palette(style.get('palette'), scheme))
    custom = (accent_hex or '').strip().upper()
    if custom and custom != _palette(style.get('palette'), 'light')['accent'].upper():
        colours['accent'] = custom
    return {
        'palette': style.get('palette') or 'indigo',
        'scheme': scheme,
        'font': style.get('font') or 'sans',
        'pattern': style.get('pattern') or 'none',
        'card': style.get('card') or 'elevated',
        'radius': style.get('radius') or 'round',
        'density': style.get('density') or 'comfortable',
        'width': style.get('width') or 'standard',
        'hero': style.get('hero') or 'art',
        'colors': colours,
    }


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


def course_payload(course, viewer=None, include_purchase=True, access=None, resource_ids=None):
    """One offering as JSON.

    `access` takes a pre-resolved (has_access, reason, purchase) triple from
    `course_access_map()` so a list of offerings costs one purchase query
    instead of one per card; without it the check runs here, and when the
    caller does not want purchase state it does not run at all.

    `resource_ids` is the notes attached to this offering. It is only ever sent
    to the owner, and it has to be sent: an editor that cannot see the current
    attachments will save an empty list over them, and `sync_course_resources`
    reads an empty list as "detach everything". Pass `[]` to say "no
    attachments" and leave it `None` to leave the key out."""
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
    if resource_ids is not None:
        payload['resource_ids'] = list(resource_ids)
    if include_purchase:
        has_access, reason, purchase = access or check_user_course_access(viewer, course)
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
        'theme': theme_payload(page.style, page.accent_hex),
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
    links = course_resource_map(page) if not only_published else {}
    course_list = [
        course_payload(course, viewer, include_purchase=False,
                       resource_ids=links.get(course.id) if not only_published else None)
        for course in courses
    ]
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


def course_resource_map(page):
    """`{course_id: [resource_id, ...]}` for one storefront, in one query, so a
    studio listing its offerings does not pay a query per card."""
    links = {}
    rows = (CreatorCourseResource.objects
            .filter(course__page=page)
            .order_by('sort_order')
            .values_list('course_id', 'resource_id'))
    for course_id, resource_id in rows:
        links.setdefault(course_id, []).append(resource_id)
    return links
