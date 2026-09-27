"""Marketplace pages on the web.

Three surfaces, all reading the same data the app reads:

* ``/marketplace/``          — the directory of creator storefronts.
* ``/marketplace/<slug>/``   — one storefront, rendered from its blocks.
* ``/marketplace/studio/``   — the owner's editor: page, courses, posts, earnings.
* ``/marketplace/course/<id>/`` — a course and its QR checkout.

Editing from the studio goes through the JSON endpoints at the bottom, which
call the same validators as the REST API (``api/creator_pages.py``). Nothing
about a page is trusted just because it arrived from our own form.
"""
import json
import uuid

from django.conf import settings
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from api.models import (
    CreatorCourse, CreatorPage, CreatorPost, PaymentVerification, Resource, SellerBalance,
    User, WithdrawalRequest,
)
from api.creator_pages import (
    BLOCK_LABELS, LAYOUTS, allowed_kinds, apply_course_fields, apply_page_update,
    apply_post_fields, block_schema, can_have_storefront, check_user_course_access,
    course_payload, listing_queryset, page_for_user, page_payload, post_payload,
    sanitize_accent, sync_course_resources, unique_course_slug, unique_page_slug,
)
from api.marketplace import get_payment_config, record_purchase, seller_sales
from api.utils import now_ms

from .view_helpers import *  # noqa: F401,F403


def _viewer(request):
    user_id = _get_user_id(request)
    if not user_id:
        return None
    return User.objects.filter(pk=user_id).first()


def commission_percent():
    """The platform fee a creator is shown before they set a price."""
    return get_payment_config().commission_percent


def _json_body(request):
    if request.content_type and 'application/json' in request.content_type:
        try:
            return json.loads(request.body.decode('utf-8') or '{}')
        except (ValueError, UnicodeDecodeError):
            return None
    return request.POST.dict()


# ---------------------------------------------------------------------------
# Public surfaces
# ---------------------------------------------------------------------------

def marketplace_shelf_context(request, query='', kind='', sort='featured', limit=12, course_limit=8):
    """Everything both marketplace surfaces need: the creator list, the newest
    offerings, the viewer's own page and whether they may build one.

    The library tab and the /marketplace/ directory render the same shelf, so
    they read it from here instead of assembling filters twice.
    """
    from django.db.models import Q

    viewer = _viewer(request)
    kind = (kind or '').strip().lower()
    if kind not in ('tutor', 'institute', 'admin'):
        kind = ''
    query = (query or '').strip()

    qs = listing_queryset(viewer, viewer_is_admin=True).filter(published=True)
    if kind:
        qs = qs.filter(kind=kind)
    if query:
        qs = qs.filter(Q(display_name__icontains=query) | Q(tagline__icontains=query) |
                       Q(about__icontains=query) | Q(subjects__icontains=query))
    if sort == 'name':
        qs = qs.order_by('display_name')
    elif sort == 'new':
        qs = qs.order_by('-created_at')
    elif sort == 'popular':
        qs = qs.order_by('-follower_count', '-view_count')
    elif sort == 'courses':
        qs = qs.order_by('-published_course_count', '-updated_at')
    else:
        qs = qs.order_by('-featured', '-updated_at')

    total = qs.count()
    creators = [page_payload(page, viewer, with_content=False) for page in qs[:limit]]

    courses = (CreatorCourse.objects
               .filter(status='published', page__published=True)
               .select_related('page')
               .order_by('-featured', '-sale_count', '-created_at')[:course_limit])
    featured = [dict(course_payload(course, viewer, include_purchase=False),
                     page_name=course.page.display_name,
                     page_slug=course.page.slug,
                     accent_hex=course.page.accent_hex) for course in courses]

    return {
        'creators': creators,
        'featured_courses': featured,
        'current_kind': kind,
        'query': query,
        'total_creators': total,
        'my_page': page_for_user(viewer, create=False) if viewer else None,
        'can_create': can_have_storefront(viewer),
    }


def directory(request):
    """Every published storefront, with the filters the app's tab offers."""
    viewer = _viewer(request)
    sort = (request.GET.get('sort') or 'featured').strip().lower()
    shelf = marketplace_shelf_context(request, query=request.GET.get('q', ''),
                                      kind=request.GET.get('kind', ''), sort=sort, limit=60)
    subject = (request.GET.get('subject') or '').strip()
    if subject:
        qs = listing_queryset(viewer, viewer_is_admin=True).filter(published=True, subjects__icontains=subject)
        shelf['creators'] = [page_payload(page, viewer, with_content=False) for page in qs[:60]]
        shelf['total_creators'] = qs.count()

    return render(request, 'web/marketplace.html', _ctx(request,
        creators=shelf['creators'],
        featured_courses=shelf['featured_courses'],
        current_kind=shelf['current_kind'],
        current_sort=sort,
        query=shelf['query'],
        subject=subject,
        total_creators=shelf['total_creators'],
        total_courses=CreatorCourse.objects.filter(status='published').count(),
        my_page=shelf['my_page'],
        can_create=shelf['can_create'],
        subjects=_subject_options(),
    ))


def _subject_options():
    from django.db.models import Count
    rows = (CreatorPage.objects.filter(published=True)
            .exclude(subjects='')
            .values_list('subjects', flat=True)[:200])
    seen = []
    for row in rows:
        for part in (row or '').split(','):
            part = part.strip()
            if part and part not in seen:
                seen.append(part)
    return seen[:24]


def creator(request, slug):
    """One storefront: its blocks in the owner's order, its courses and updates."""
    viewer = _viewer(request)
    page = CreatorPage.objects.select_related('user').filter(slug=slug).first()
    if page is None:
        raise Http404('This page does not exist')

    is_owner = bool(viewer and page.user_id == viewer.id)
    is_admin = bool(viewer and getattr(viewer, 'is_admin', False))
    if not page.published and not (is_owner or is_admin):
        raise Http404('This page is not published yet')

    if not is_owner:
        CreatorPage.objects.filter(pk=page.pk).update(view_count=page.view_count + 1)

    payload = page_payload(page, viewer)
    courses = [course_payload(course, viewer)
               for course in page.courses.all()
               if course.status == 'published' or is_owner or is_admin]

    blocks = payload.get('blocks') or []
    return render(request, 'web/marketplace_page.html', _ctx(request,
        creator=payload,
        accent=sanitize_accent(payload.get('accent_hex')),
        style=payload.get('style') or {},
        blocks=blocks,
        courses=courses,
        paid_courses=[c for c in courses if not c['is_free']],
        free_courses=[c for c in courses if c['is_free']],
        resources=payload.get('resources') or [],
        posts=payload.get('posts') or [],
        is_owner=is_owner,
        contact_rows=_contact_rows(payload),
    ))


def _contact_rows(payload):
    socials = payload.get('socials') or {}
    labels = {
        'website': 'Website', 'facebook': 'Facebook', 'instagram': 'Instagram',
        'youtube': 'YouTube', 'tiktok': 'TikTok', 'x': 'X', 'linkedin': 'LinkedIn',
        'github': 'GitHub', 'telegram': 'Telegram', 'viber': 'Viber',
        'whatsapp': 'WhatsApp', 'email': 'Email', 'phone': 'Phone',
    }
    rows = []
    for key, value in socials.items():
        if not value:
            continue
        if key == 'email':
            href = f'mailto:{value}'
        elif key == 'phone':
            href = f'tel:{value}'
        else:
            href = value
        rows.append({'key': key, 'label': labels.get(key, key.title()), 'href': href, 'value': value})
    return rows


def course_detail(request, course_id):
    """A course page, carrying its own QR checkout for locked viewers."""
    viewer = _viewer(request)
    course = (CreatorCourse.objects
              .select_related('page', 'page__user')
              .filter(pk=course_id)
              .first())
    if course is None:
        raise Http404('This course does not exist')

    is_owner = bool(viewer and course.page.user_id == viewer.id)
    is_admin = bool(viewer and getattr(viewer, 'is_admin', False))
    if course.status != 'published' and not (is_owner or is_admin):
        raise Http404('This course does not exist')

    if not is_owner:
        CreatorCourse.objects.filter(pk=course.pk).update(view_count=course.view_count + 1)

    if request.method == 'POST':
        if viewer is None:
            return redirect(f"{reverse('web:login')}?next={request.path}")
        if is_owner:
            messages.error(request, 'You own this course.')
            return redirect('web:marketplace_course', course_id=course.id)
        if course.is_free:
            return redirect('web:marketplace_course', course_id=course.id)

        transaction_id = (request.POST.get('transaction_id') or '').strip()
        proof = request.FILES.get('payment_proof')
        if not transaction_id and not proof:
            messages.error(request, 'Add a transaction reference or attach a payment screenshot.')
            return redirect('web:marketplace_course', course_id=course.id)

        if proof:
            from django.core.exceptions import ValidationError as DjangoValidationError
            from api.security import save_payment_proof_upload
            try:
                proof = save_payment_proof_upload(proof)
            except DjangoValidationError as exc:
                messages.error(request, ' '.join(exc.messages))
                return redirect('web:marketplace_course', course_id=course.id)

        proof_url = request.build_absolute_uri(settings.MEDIA_URL + str(proof)) if proof else ''
        record_purchase(viewer, course.page.user, course=course,
                        transaction_id=transaction_id, proof_file=proof, proof_url=proof_url)
        messages.success(request, 'Payment submitted. Your seat unlocks once our team verifies it.')
        return redirect('web:marketplace_course', course_id=course.id)

    has_access, reason, purchase = check_user_course_access(viewer, course)
    payload = course_payload(course, viewer)
    config = get_payment_config()
    return render(request, 'web/marketplace_course.html', _ctx(request,
        course=payload,
        creator=page_payload(course.page, viewer, with_content=False),
        accent=sanitize_accent(course.page.accent_hex),
        has_access=has_access,
        access_reason=reason,
        purchase=purchase,
        is_owner=is_owner,
        signed_in=viewer is not None,
        company_qr_url=config.company_qr_url,
        company_qr_caption=config.company_qr_caption,
        payment_instructions=config.payment_instructions,
        commission_percent=config.commission_percent,
        resources=[item.resource for item in course.course_resources.select_related('resource')
                   if item.resource and item.resource.approval_status == 'approved'][:12],
    ))


# ---------------------------------------------------------------------------
# Studio
# ---------------------------------------------------------------------------

def studio(request):
    """The owner's editor. Only teachers, institutes and admins get one."""
    viewer = _viewer(request)
    if viewer is None:
        return redirect(f"{reverse('web:login')}?next={request.path}")
    if not can_have_storefront(viewer):
        return render(request, 'web/marketplace_studio.html', _ctx(request,
            eligible=False,
            viewer_role=viewer.role,
        ), status=403)

    page = page_for_user(viewer, create=True)
    payload = page_payload(page, viewer)
    courses = page.courses.all()
    posts = page.page_posts.all()
    resources = (Resource.objects
                 .filter(uploaded_by=viewer, approval_status='approved')
                 .order_by('-added_at')[:100])

    config = get_payment_config()
    balance, _ = SellerBalance.objects.get_or_create(
        user=viewer,
        defaults={'total_earned': 0, 'total_withdrawn': 0, 'current_balance': 0, 'updated_at': now_ms()},
    )
    sales = seller_sales(viewer, limit=40)

    return render(request, 'web/marketplace_studio.html', _ctx(request,
        eligible=True,
        creator=payload,
        accent=sanitize_accent(payload.get('accent_hex')),
        block_schema=block_schema(),
        block_labels=BLOCK_LABELS,
        layouts=LAYOUTS,
        allowed_kinds=allowed_kinds(viewer),
        courses=[course_payload(course, viewer, include_purchase=False) for course in courses],
        course_resources={course.id: list(course.course_resources.values_list('resource_id', flat=True))
                          for course in courses},
        posts=[post_payload(post) for post in posts],
        resources=resources,
        balance=balance,
        sales=sales,
        commission_percent=config.commission_percent,
        withdraw_min=config.withdraw_min,
        company_qr_url=config.company_qr_url,
        withdrawals=WithdrawalRequest.objects.filter(user=viewer).order_by('-created_at')[:10],
        nebians_points=viewer.nebians_points or 0,
    ))


def _owned_page_or_none(request):
    viewer = _viewer(request)
    if viewer is None:
        return None, None, JsonResponse({'error': 'Please sign in again'}, status=401)
    if not can_have_storefront(viewer):
        return None, viewer, JsonResponse({'error': 'Marketplace pages are for teachers, institutes and admins.'}, status=403)
    page = page_for_user(viewer, create=True)
    return page, viewer, None


def ajax_page_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    page, viewer, error = _owned_page_or_none(request)
    if error:
        return error
    data = _json_body(request)
    if data is None:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    page, message = apply_page_update(page, data, allowed_kinds(viewer))
    if message:
        return JsonResponse({'error': message}, status=400)
    return JsonResponse({'ok': True, 'page': page_payload(page, viewer), 'message': 'Page saved'})


def ajax_course_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    page, viewer, error = _owned_page_or_none(request)
    if error:
        return error
    data = _json_body(request)
    if data is None:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    course_id = str(data.get('id') or '').strip()
    course = page.courses.filter(pk=course_id).first() if course_id else None
    if course_id and course is None:
        return JsonResponse({'error': 'Course not found'}, status=404)

    was_published = bool(course and course.status == 'published')
    was_new = course is None
    course, pending_ids, message = apply_course_fields(course, page, data)
    if message:
        return JsonResponse({'error': message}, status=400)

    now = now_ms()
    if was_new:
        course.id = str(uuid.uuid4())
        course.page = page
        course.created_at = now
    course.slug = unique_course_slug(page, course.slug or course.title, exclude_id=course.pk)
    course.updated_at = now
    if course.status == 'published' and not was_published:
        course.published_at = now
    course.save()
    if pending_ids is not None:
        sync_course_resources(course, page, pending_ids)

    return JsonResponse({'ok': True, 'course': course_payload(course, viewer, include_purchase=False),
                         'message': 'Course saved'})


def ajax_course_delete(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    page, viewer, error = _owned_page_or_none(request)
    if error:
        return error
    data = _json_body(request)
    course = page.courses.filter(pk=str((data or {}).get('id') or '')).first()
    if course is None:
        return JsonResponse({'error': 'Course not found'}, status=404)
    course.delete()
    return JsonResponse({'ok': True, 'message': 'Course removed'})


def ajax_post_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    page, viewer, error = _owned_page_or_none(request)
    if error:
        return error
    data = _json_body(request)
    if data is None:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    post_id = str(data.get('id') or '').strip()
    post = page.page_posts.filter(pk=post_id).first() if post_id else None
    if post_id and post is None:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post is None:
        if not str(data.get('body') or '').strip() and not str(data.get('title') or '').strip():
            return JsonResponse({'error': 'Write something first'}, status=400)
        post = CreatorPost(id=str(uuid.uuid4()), page=page, created_at=now_ms(), updated_at=now_ms())
    post, message = apply_post_fields(post, data)
    if message:
        return JsonResponse({'error': message}, status=400)
    CreatorPage.objects.filter(pk=page.pk).update(updated_at=now_ms())
    return JsonResponse({'ok': True, 'post': post_payload(post), 'message': 'Update posted'})


def ajax_post_delete(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    page, viewer, error = _owned_page_or_none(request)
    if error:
        return error
    data = _json_body(request)
    post = page.page_posts.filter(pk=str((data or {}).get('id') or '')).first()
    if post is None:
        return JsonResponse({'error': 'Post not found'}, status=404)
    post.delete()
    return JsonResponse({'ok': True, 'message': 'Update removed'})
