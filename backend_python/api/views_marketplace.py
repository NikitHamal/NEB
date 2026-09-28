"""Marketplace API — creator storefronts, their courses and their dashboard.

Reader endpoints (creators list, a page, a course, stats) are public. Everything
under ``marketplace/me/`` is owner-scoped and requires a signed-in account that
is eligible for a storefront (teacher, institution or admin). Buying a course
uses the same QR-proof flow as a paid library resource, so a buyer learns one
checkout and an admin verifies one queue.

All write validation lives in ``api/creator_pages.py`` so the Django studio and
this API can never disagree about what a valid page or course looks like.
"""
from decimal import Decimal

from django.conf import settings
from django.db.models import Q, F

from .view_helpers import *  # noqa: F401,F403
from .models import (
    CreatorPage, CreatorCourse, CreatorPost,
    PaymentVerification, Resource,
)
from .creator_pages import (
    can_have_storefront, allowed_kinds, page_for_user, page_payload, course_payload,
    post_payload, listing_queryset, unique_page_slug, unique_course_slug,
    check_user_course_access, course_access_map, LAYOUTS,
    apply_page_update, apply_course_fields, apply_post_fields, sync_course_resources,
)
from .marketplace import get_payment_config, record_purchase, seller_sales


def _money(value):
    try:
        amount = float(value or 0)
    except (TypeError, ValueError):
        return '0'
    return ('%g' % amount) if amount else '0'


def _viewer(request):
    return _get_user_from_request(request)


def _int_param(request, key, default, low, high):
    try:
        value = int(request.GET.get(key, default))
    except (TypeError, ValueError):
        return default
    return max(low, min(high, value))


# ---------------------------------------------------------------------------
# Public reader endpoints
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def marketplace_creators(request):
    """The marketplace directory: every published storefront."""
    viewer = _viewer(request)
    qs = listing_queryset(viewer)

    kind = (request.GET.get('kind') or '').strip().lower()
    if kind in ('tutor', 'institute', 'admin'):
        qs = qs.filter(kind=kind)

    query = (request.GET.get('q') or '').strip()
    if query:
        qs = qs.filter(
            Q(display_name__icontains=query) | Q(tagline__icontains=query) |
            Q(about__icontains=query) | Q(subjects__icontains=query) |
            Q(slug__icontains=query)
        )

    subject = (request.GET.get('subject') or '').strip()
    if subject:
        qs = qs.filter(subjects__icontains=subject)

    if request.GET.get('mine') in ('1', 'true') and viewer is not None:
        qs = qs.filter(user=viewer)

    sort = (request.GET.get('sort') or 'featured').strip().lower()
    if sort == 'new':
        qs = qs.order_by('-created_at')
    elif sort == 'popular':
        qs = qs.order_by('-follower_count', '-view_count')
    elif sort == 'name':
        qs = qs.order_by('display_name')
    elif sort == 'courses':
        qs = qs.order_by('-published_course_count', '-updated_at')
    else:
        qs = qs.order_by('-featured', '-updated_at')

    page_number = _int_param(request, 'page', 1, 1, 1000)
    page_size = _int_param(request, 'page_size', 12, 1, 48)
    total = qs.count()
    start = (page_number - 1) * page_size
    rows = qs[start:start + page_size]

    return Response({
        'creators': [page_payload(page, viewer, with_content=False) for page in rows],
        'total': total,
        'page': page_number,
        'page_size': page_size,
        'has_more': start + page_size < total,
        'you_are_eligible': can_have_storefront(viewer),
        'your_kinds': allowed_kinds(viewer),
        'layouts': list(LAYOUTS),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def marketplace_stats(request):
    """Small counters for the marketplace header in the library."""
    published = CreatorPage.objects.filter(published=True)
    courses = CreatorCourse.objects.filter(status='published')
    return Response({
        'creators': published.count(),
        'tutors': published.filter(kind='tutor').count(),
        'institutes': published.filter(kind='institute').count(),
        'courses': courses.count(),
        'paid_courses': courses.filter(is_free=False).count(),
        'free_courses': courses.filter(is_free=True).count(),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def marketplace_creator_detail(request, slug):
    viewer = _viewer(request)
    page = CreatorPage.objects.select_related('user').filter(slug=slug).first()
    if page is None:
        return Response({'error': 'This page does not exist'}, status=404)

    is_owner = viewer is not None and page.user_id == getattr(viewer, 'id', None)
    is_admin = viewer is not None and getattr(viewer, 'is_admin', False)
    if not page.published and not (is_owner or is_admin):
        return Response({'error': 'This page is not published yet'}, status=404)

    if not is_owner:
        CreatorPage.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)
        page.view_count = (page.view_count or 0) + 1

    return Response(page_payload(page, viewer))


@api_view(['GET'])
@permission_classes([AllowAny])
def marketplace_course_detail(request, course_id):
    viewer = _viewer(request)
    course = (CreatorCourse.objects
              .select_related('page', 'page__user')
              .filter(pk=course_id)
              .first())
    if course is None:
        return Response({'error': 'This course does not exist'}, status=404)
    is_owner = viewer is not None and course.page.user_id == getattr(viewer, 'id', None)
    is_admin = viewer is not None and getattr(viewer, 'is_admin', False)
    if course.status != 'published' and not (is_owner or is_admin):
        return Response({'error': 'This course does not exist'}, status=404)
    if not is_owner:
        CreatorCourse.objects.filter(pk=course.pk).update(view_count=F('view_count') + 1)
    payload = course_payload(course, viewer)
    payload['page'] = page_payload(course.page, viewer, with_content=False)
    # Approved material only, same as the web course page: a note still in the
    # moderation queue is not part of the offering yet.
    payload['resources'] = [{
        'id': item.resource_id,
        'title': item.resource.title,
        'subject': item.resource.subject or '',
        'type': item.resource.type or '',
        'thumbnail_url': item.resource.thumbnail_url or '',
        'is_paid': bool(item.resource.is_paid),
    } for item in course.course_resources.select_related('resource')
        if item.resource and item.resource.approval_status == 'approved']
    return Response(payload)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def marketplace_course_purchase(request, course_id):
    """Course checkout, identical in shape to /resources/<id>/purchase/."""
    user, err = _require_user(request)
    if err:
        return err

    course = (CreatorCourse.objects
              .select_related('page', 'page__user')
              .filter(pk=course_id)
              .first())
    if course is None or (course.status != 'published' and course.page.user_id != user.id):
        return Response({'error': 'This course does not exist'}, status=404)

    price_dec = Decimal(course.price or 0)
    seller = course.page.user
    cfg = get_payment_config()

    def _status_payload():
        has_access, reason, purchase = check_user_course_access(user, course)
        return {
            'status': 'ok',
            'target_type': 'course',
            'target_id': course.id,
            'title': course.title,
            'is_paid': (not course.is_free) and price_dec > 0,
            'price': _money(price_dec),
            'seller_name': (seller.display_name or seller.username) if seller else '',
            'has_access': bool(has_access),
            'access_reason': reason,
            'purchase_status': getattr(purchase, 'status', '') if purchase else '',
            'purchase_id': getattr(purchase, 'id', '') if purchase else '',
            'commission_percent': _money(cfg.commission_percent),
            'message': '',
        }

    if request.method == 'GET':
        return Response(_status_payload())

    if course.is_free or price_dec <= 0:
        return Response({'error': 'This course is free — just open it'}, status=400)
    if seller is not None and seller.id == user.id:
        return Response({'error': 'You own this course'}, status=400)

    transaction_id = (request.data.get('transaction_id') or '').strip()
    proof_file = request.FILES.get('payment_proof')
    if not transaction_id and not proof_file:
        return Response({'error': 'Please provide a transaction reference or upload a payment screenshot.'}, status=400)

    if proof_file:
        from api.security import save_payment_proof_upload
        from django.core.exceptions import ValidationError as DjangoValidationError
        try:
            proof_file = save_payment_proof_upload(proof_file)
        except DjangoValidationError as exc:
            return Response({'error': ' '.join(exc.messages)}, status=400)

    proof_url = ''
    if proof_file and request is not None:
        proof_url = request.build_absolute_uri(settings.MEDIA_URL + str(proof_file))
    record_purchase(user, seller, course=course, transaction_id=transaction_id,
                    proof_file=proof_file, proof_url=proof_url)

    result = _status_payload()
    result['message'] = 'Payment proof submitted. Your seat unlocks once an admin verifies it.'
    return Response(result, status=201)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def marketplace_courses(request):
    """Published offerings across the marketplace, newest and best first.

    The app's marketplace shelf shows a row of these above the creator list; the
    web shelf builds the same row from the ORM. Keeping the shape identical is
    what lets one card component render both.
    """
    viewer = _viewer(request)
    qs = (CreatorCourse.objects
          .filter(status='published', page__published=True)
          .select_related('page'))

    kind = (request.GET.get('kind') or '').strip().lower()
    if kind in ('tutor', 'institute', 'admin'):
        qs = qs.filter(page__kind=kind)

    query = (request.GET.get('q') or '').strip()
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(summary__icontains=query) |
                       Q(tags__icontains=query) | Q(page__display_name__icontains=query))

    paid_only = request.GET.get('pricing')
    if paid_only == 'paid':
        qs = qs.filter(is_free=False)
    elif paid_only == 'free':
        qs = qs.filter(is_free=True)

    sort = (request.GET.get('sort') or 'featured').strip().lower()
    if sort == 'new':
        qs = qs.order_by('-created_at')
    elif sort == 'price':
        qs = qs.order_by('is_free', 'price')
    elif sort == 'popular':
        qs = qs.order_by('-sale_count', '-enrollment_count')
    else:
        qs = qs.order_by('-featured', '-sale_count', '-created_at')

    limit = _int_param(request, 'limit', 12, 1, 48)
    total = qs.count()
    rows = qs[:limit]

    rows = list(rows)
    access = course_access_map(viewer, rows)
    courses = []
    for course in rows:
        payload = course_payload(course, viewer, access=access.get(course.id))
        payload['page_name'] = course.page.display_name
        payload['page_slug'] = course.page.slug
        payload['accent_hex'] = course.page.accent_hex
        courses.append(payload)

    return Response({
        'courses': courses,
        'total': total,
        'has_more': total > len(courses),
    })


# ---------------------------------------------------------------------------
# Owner endpoints
# ---------------------------------------------------------------------------

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@throttle_classes([WriteActionRateThrottle])
def marketplace_me_page(request):
    user, err = _require_user(request)
    if err:
        return err

    if not can_have_storefront(user):
        return Response({
            'error': 'Marketplace pages are for teachers, institutes and admins.',
            'eligible': False,
            'your_kinds': [],
        }, status=403)

    page = page_for_user(user, create=True)
    if request.method == 'GET':
        return Response({
            'eligible': True,
            'your_kinds': allowed_kinds(user),
            'layouts': list(LAYOUTS),
            'page': page_payload(page, user),
        })

    page, error = apply_page_update(page, request.data, allowed_kinds(user))
    if error:
        return Response({'error': error}, status=400)
    return Response({'page': page_payload(page, user), 'message': 'Page saved'})


@api_view(['GET', 'POST'])
@throttle_classes([WriteActionRateThrottle])
def marketplace_me_courses(request):
    user, err = _require_user(request)
    if err:
        return err
    page = page_for_user(user, create=True)
    if page is None:
        return Response({'error': 'Marketplace pages are for teachers, institutes and admins.'}, status=403)

    if request.method == 'GET':
        return Response({
            'courses': [course_payload(course, user, include_purchase=False) for course in page.courses.all()],
            'page_slug': page.slug,
        })

    course, pending_resource_ids, error = apply_course_fields(None, page, request.data)
    if error:
        return Response({'error': error}, status=400)

    now = now_ms()
    course.id = str(uuid.uuid4())
    course.page = page
    course.slug = unique_course_slug(page, course.slug or course.title)
    course.created_at = now
    course.updated_at = now
    course.published_at = now if course.status == 'published' else 0
    course.save()
    if pending_resource_ids is not None:
        sync_course_resources(course, page, pending_resource_ids)
    return Response({'course': course_payload(course, user, include_purchase=False)}, status=201)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@throttle_classes([WriteActionRateThrottle])
def marketplace_me_course(request, course_id):
    user, err = _require_user(request)
    if err:
        return err
    page = page_for_user(user, create=False)
    if page is None:
        return Response({'error': 'You do not have a marketplace page yet'}, status=403)
    course = CreatorCourse.objects.filter(pk=course_id, page=page).first()
    if course is None:
        return Response({'error': 'Course not found'}, status=404)

    if request.method == 'GET':
        return Response({'course': course_payload(course, user, include_purchase=False)})

    if request.method == 'DELETE':
        course.delete()
        return Response({'message': 'Course removed'})

    was_published = course.status == 'published'
    previous_slug = course.slug
    course, pending_resource_ids, error = apply_course_fields(course, page, request.data)
    if error:
        return Response({'error': error}, status=400)
    if course.slug != previous_slug:
        course.slug = unique_course_slug(page, course.slug, exclude_id=course.pk)
    course.updated_at = now_ms()
    if course.status == 'published' and not was_published:
        course.published_at = course.updated_at
    course.save()
    if pending_resource_ids is not None:
        sync_course_resources(course, page, pending_resource_ids)
    return Response({'course': course_payload(course, user, include_purchase=False), 'message': 'Course saved'})


@api_view(['GET', 'POST'])
@throttle_classes([WriteActionRateThrottle])
def marketplace_me_posts(request):
    user, err = _require_user(request)
    if err:
        return err
    page = page_for_user(user, create=False)
    if page is None:
        return Response({'error': 'You do not have a marketplace page yet'}, status=403)

    if request.method == 'GET':
        return Response({'posts': [post_payload(post) for post in page.page_posts.all()]})

    data = request.data if isinstance(request.data, dict) else {}
    if not str(data.get('body') or '').strip() and not str(data.get('title') or '').strip():
        return Response({'error': 'Write something first'}, status=400)

    now = now_ms()
    post = CreatorPost(id=str(uuid.uuid4()), page=page, created_at=now, updated_at=now)
    post, error = apply_post_fields(post, data)
    if error:
        return Response({'error': error}, status=400)
    CreatorPage.objects.filter(pk=page.pk).update(updated_at=now)
    return Response({'post': post_payload(post)}, status=201)


@api_view(['PATCH', 'DELETE'])
@throttle_classes([WriteActionRateThrottle])
def marketplace_me_post(request, post_id):
    user, err = _require_user(request)
    if err:
        return err
    page = page_for_user(user, create=False)
    if page is None:
        return Response({'error': 'You do not have a marketplace page yet'}, status=403)
    post = CreatorPost.objects.filter(pk=post_id, page=page).first()
    if post is None:
        return Response({'error': 'Post not found'}, status=404)
    if request.method == 'DELETE':
        post.delete()
        return Response({'message': 'Post removed'})
    post, error = apply_post_fields(post, request.data)
    if error:
        return Response({'error': error}, status=400)
    return Response({'post': post_payload(post), 'message': 'Post saved'})


@api_view(['GET'])
def marketplace_dashboard(request):
    """The seller's own view: wallet, sales, verification queue and page health."""
    user, err = _require_user(request)
    if err:
        return err

    if not can_have_storefront(user):
        return Response({
            'error': 'Marketplace pages are for teachers, institutes and admins.',
            'eligible': False,
            'your_kinds': [],
        }, status=403)

    from .models import SellerBalance, WithdrawalRequest
    bal = getattr(user, 'seller_balance', None)
    if bal is None:
        bal, _ = SellerBalance.objects.get_or_create(
            user=user,
            defaults={'total_earned': 0, 'total_withdrawn': 0, 'current_balance': 0, 'updated_at': now_ms()},
        )

    sales = seller_sales(user)

    approved = [sale for sale in sales if sale['status'] == 'approved']
    page = CreatorPage.objects.filter(user=user).first()
    cfg = get_payment_config()
    return Response({
        'eligible': can_have_storefront(user),
        'your_kinds': allowed_kinds(user),
        'has_page': page is not None,
        'page_slug': page.slug if page else '',
        'page_published': bool(page.published) if page else False,
        'wallet': {
            'currency': 'NPR',
            'current_balance': _money(bal.current_balance),
            'total_earned': _money(bal.total_earned),
            'total_withdrawn': _money(bal.total_withdrawn),
            'withdraw_min': _money(cfg.withdraw_min),
            'pending_withdrawals': WithdrawalRequest.objects.filter(user=user, status='pending').count(),
        },
        'commission_percent': _money(cfg.commission_percent),
        'nebians_points': user.nebians_points or 0,
        'stats': {
            'total_sales': len(sales),
            'approved_sales': len(approved),
            'pending_sales': len([s for s in sales if s['status'] == 'pending']),
            'paid_courses': CreatorCourse.objects.filter(page=page, is_free=False).count() if page else 0,
            'published_courses': CreatorCourse.objects.filter(page=page, status='published').count() if page else 0,
            'resources': Resource.objects.filter(uploaded_by=user, approval_status='approved').count(),
        },
        'sales': sales,
    })
