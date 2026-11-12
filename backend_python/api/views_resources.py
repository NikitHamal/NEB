"""Views Resources extracted from views.py."""
from decimal import Decimal
from django.conf import settings
import uuid
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Case, F, IntegerField, Q, Value, When
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import services
from .resource_catalog import EDUCATION_LEVELS
from .resource_form import (
    InvalidInput,
    discard_saved_files,
    media_url,
    read_file_url,
    read_listing_fields,
    read_request_fields,
    read_source_url,
    read_thumbnail,
)
from .models import Resource, ResourceRequest, ResourceRequestUpvote, User
from .security import maybe_autoset_video_thumbnail, validate_and_save_resource_file
from .serializers import ResourceRequestSerializer, ResourceSerializer
from .throttles import (
    SearchRateThrottle,
    UploadRateThrottle,
    ViewIncrementRateThrottle,
    WriteActionRateThrottle,
)
from .view_helpers import (
    _get_user_from_request,
    _now_ms,
    _paginated_response,
    _require_user,
    is_global_user,
    logger,
    parse_paid_fields,
    prime_for_serializers,
)
from .security import validate_forum_attachments
from .models import PaymentVerification

_SORT_ORDERS = {
    'newest': ('-added_at', '-view_count'),
    'oldest': ('added_at',),
    'liked': ('-like_count', '-added_at'),
    'trending': ('-view_count', '-like_count', '-added_at'),
}


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def resources_list(request):
    """GET /api/resources — public, paginated library feed with web-parity filters/sort.

    Android and the website both browse approved lead resources without forcing
    sign-in. Keep this endpoint cheap: filter in SQL, sort in SQL, and only
    serialize the requested page.
    """
    resources = Resource.objects.filter(approval_status='approved', is_lead=True).select_related('uploaded_by')

    subject = (request.query_params.get('subject') or '').strip()
    grade = (request.query_params.get('grade') or '').strip()
    rtype = (request.query_params.get('type') or '').strip()
    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'relevant').strip().lower()

    if subject:
        resources = resources.filter(subject__iexact=subject)
    if grade:
        from .education_catalog import level_match_values
        gq = Q()
        for v in level_match_values(grade) or [grade]:
            gq |= Q(grade_level__iexact=v)
        resources = resources.filter(gq)
    if rtype:
        resources = resources.filter(type__iexact=rtype)
    if search:
        resources = resources.filter(
            Q(title__icontains=search) | Q(description__icontains=search) |
            Q(subject__icontains=search) | Q(grade_level__icontains=search) |
            Q(faculty__icontains=search) | Q(program__icontains=search) |
            Q(school__icontains=search) | Q(tags__icontains=search)
        )

    user = request.user
    personalised = False
    if user and user.is_authenticated and not is_global_user(user):
        grade_pref = user.class_level
        subject_prefs = [s.strip().lower() for s in (user.subjects or '').split(',') if s.strip()]
        if grade_pref or subject_prefs:
            from .education_catalog import level_match_values
            grade_match = Q(pk__in=[])
            for v in level_match_values(grade_pref):
                grade_match |= Q(grade_level__iexact=v)
            subject_match = Q(pk__in=[])
            if subject_prefs:
                subject_match = Q()
                for s in subject_prefs:
                    subject_match |= Q(subject__icontains=s)
            resources = resources.annotate(
                relevance_score=Case(
                    When(grade_match & subject_match, then=Value(4)),
                    When(grade_match, then=Value(3)),
                    When(subject_match, then=Value(2)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            personalised = True

    order = _SORT_ORDERS.get(sort, _SORT_ORDERS['newest'])
    resources = resources.order_by(*(('-relevance_score',) if personalised else ()), *order)

    return _paginated_response(
        request,
        resources,
        ResourceSerializer,
        context={'request': request},
        default_page_size=50,
        max_page_size=100,
    )


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def syllabus_categories(request):
    """GET /api/syllabus/categories/ — compact syllabus accordion data for mobile.

    Mirrors the website Library → Syllabus tab: the syllabus exported from
    the NEBians books for Class 8, 10, 11 and 12.
    """
    from .views_syllabus import legacy_categories
    return Response({'categories': legacy_categories()})


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def syllabus_subject_detail(request, grade_slug, subject_slug):
    from .views_syllabus import legacy_subject_detail
    detail = legacy_subject_detail(grade_slug, subject_slug)
    if detail is not None:
        return Response(detail)
    from api.models import SyllabusContent
    try:
        from web import curriculum
        from web.view_helpers import parse_sections, parse_qas
    except Exception:
        curriculum = None
        parse_sections = None
        parse_qas = None

    def slugify(value):
        if curriculum is not None:
            return curriculum.slugify_tag(value)
        return (value or '').lower().replace(' / see', '-see').replace('/', '-').replace(' ', '-')

    if curriculum is not None:
        grade_db_val = curriculum.get_grade_db_value(grade_slug)
        subject_db_val = curriculum.get_subject_db_value(subject_slug)
    else:
        grade_db_val = (grade_slug or '').replace('-', ' ').title()
        subject_db_val = (subject_slug or '').replace('-', ' ').title()

    def sections(value):
        if parse_sections is None:
            return []
        return parse_sections(value or '')

    def qas(value):
        if parse_qas is None:
            return []
        return parse_qas(value or '')

    from .education_catalog import level_match_values
    grade_q = Q()
    for _v in level_match_values(grade_db_val) or [grade_db_val]:
        grade_q |= Q(grade_level__iexact=_v)
    resources_qs = Resource.objects.filter(
        grade_q,
        approval_status='approved',
        is_lead=True,
        subject__icontains=subject_db_val,
    )

    syllabus_entries = SyllabusContent.objects.filter(
        grade_q,
        subject__iexact=subject_db_val,
    ).order_by('order')

    grouped_resources = []
    chapter_map = {}

    if syllabus_entries.exists():
        from web.syllabus_rich import prepare_rich_content, syllabus_search_text
        for entry in syllabus_entries:
            qa_sections = sections(entry.question_answers)
            parsed_qas = qas(entry.question_answers)
            if not qa_sections and parsed_qas:
                qa_sections = [{
                    'title': 'Solved Q&As',
                    'content': entry.question_answers or '',
                    'id': 'solved-qas',
                    'parsed_items': parsed_qas,
                }]
            chapter = {
                'id': entry.chapter_id,
                'name': entry.chapter_title,
                'keywords': [entry.chapter_title.lower(), entry.chapter_id.replace('-', ' ')],
                'guide_sections': sections(entry.text_content),
                'rich_content': prepare_rich_content(entry),
                'source_resource_id': entry.source_resource_id,
                'source_label': entry.source_label,
                'search_text': syllabus_search_text(entry),
                'qa_sections': qa_sections,
                'notes': [],
                'solutions': [],
                'papers': [],
                'textbooks': [],
                'other': [],
                'count': 0,
            }
            grouped_resources.append(chapter)
            chapter_map[entry.chapter_id] = chapter
    elif curriculum is not None:
        for chapter_item in curriculum.get_chapters_for_subject(grade_db_val, subject_db_val):
            chapter = {
                'id': chapter_item['id'],
                'name': chapter_item['name'],
                'keywords': chapter_item['keywords'],
                'guide_sections': [],
                'rich_content': {'blocks': [], 'has_blocks': False, 'topics': [], 'learning_objectives': []},
                'source_resource_id': '',
                'source_label': '',
                'search_text': (chapter_item['name'] + ' ' + ' '.join(chapter_item.get('keywords', []))).lower(),
                'qa_sections': [],
                'notes': [],
                'solutions': [],
                'papers': [],
                'textbooks': [],
                'other': [],
                'count': 0,
            }
            grouped_resources.append(chapter)
            chapter_map[chapter_item['id']] = chapter

    general_resources = {
        'id': 'general',
        'name': 'General & Reference Resources',
        'keywords': [],
        'guide_sections': [],
        'qa_sections': [],
        'notes': [],
        'solutions': [],
        'papers': [],
        'textbooks': [],
        'other': [],
        'count': 0,
    }

    serializer_context = {'request': request}
    total_count = 0
    for resource in resources_qs:
        total_count += 1
        serialized = ResourceSerializer(resource, context=serializer_context).data
        matched_ch_id = None
        res_tags = [tag.strip().lower() for tag in (resource.tags or '').split(',') if tag.strip()]
        for chapter in grouped_resources:
            if any(keyword.lower() in res_tags for keyword in chapter.get('keywords', [])):
                matched_ch_id = chapter['id']
                break
        if not matched_ch_id:
            title = resource.title.lower()
            description = (resource.description or '').lower()
            tags = (resource.tags or '').lower()
            for chapter in grouped_resources:
                if any(keyword.lower() in title or keyword.lower() in description or keyword.lower() in tags for keyword in chapter.get('keywords', [])):
                    matched_ch_id = chapter['id']
                    break
        target = chapter_map.get(matched_ch_id) if matched_ch_id else general_resources
        resource_type = (resource.type or '').lower().strip()
        exam_type = (resource.exam_type or '').lower().strip()
        title = resource.title.lower()
        tags = (resource.tags or '').lower()
        is_solution = any(value in title or value in tags for value in ['solution', 'exercise', 'question answer', 'q&a', 'answers'])
        is_paper = exam_type in ['board', 'final', 'mock', 'entrance', 'see'] or any(value in title or value in tags for value in ['past paper', 'model paper', 'question paper', 'exam paper'])
        if is_solution:
            target['solutions'].append(serialized)
        elif is_paper:
            target['papers'].append(serialized)
        elif resource_type == 'note' or exam_type == 'notes':
            target['notes'].append(serialized)
        elif resource_type == 'textbook' or exam_type == 'reference' or 'textbook' in title:
            target['textbooks'].append(serialized)
        else:
            target['other'].append(serialized)
        target['count'] += 1

    if general_resources['count'] > 0:
        grouped_resources.append(general_resources)

    has_syllabus = SyllabusContent.objects.exists()
    active_subjects = set()
    if has_syllabus:
        for subject_value in SyllabusContent.objects.filter(grade_level__iexact=grade_db_val).values_list('subject', flat=True).distinct():
            for item in (subject_value or '').split(','):
                item = item.strip()
                if item:
                    active_subjects.add(item)
        if not active_subjects and curriculum is not None:
            for grade_value, subject_value in curriculum.CURRICULUM_MAP.keys():
                if grade_value.lower() == grade_db_val.lower():
                    active_subjects.add(subject_value)
    elif curriculum is not None:
        for grade_value, subject_value in curriculum.CURRICULUM_MAP.keys():
            if grade_value.lower() == grade_db_val.lower():
                active_subjects.add(subject_value)

    from .education_catalog import canonical_level
    active_grades = {grade_db_val}
    if has_syllabus:
        for grade_value in SyllabusContent.objects.values_list('grade_level', flat=True).distinct():
            item = canonical_level(grade_value)
            if item:
                active_grades.add(item)
    elif curriculum is not None:
        for grade_value, _ in curriculum.CURRICULUM_MAP.keys():
            item = canonical_level(grade_value)
            if item:
                active_grades.add(item)

    from .education_catalog import LEVEL_LABELS, LEVEL_VALUES
    grade_order = {canonical_level(v).lower(): index for index, v in enumerate(LEVEL_VALUES)}
    label_of = lambda v: LEVEL_LABELS.get(v, v)
    grade_list = [{'name': label_of(item), 'value': item, 'slug': slugify(label_of(item))}
                  for item in sorted(active_grades, key=lambda value: (grade_order.get(canonical_level(value).lower(), 999), value))]
    subject_list = [{'name': item, 'slug': slugify(item)} for item in sorted(active_subjects)]

    def clean_chapter(chapter):
        return {
            'id': chapter['id'],
            'name': chapter['name'],
            'guide_sections': chapter.get('guide_sections', []),
            'qa_sections': chapter.get('qa_sections', []),
            'notes': chapter.get('notes', []),
            'solutions': chapter.get('solutions', []),
            'papers': chapter.get('papers', []),
            'textbooks': chapter.get('textbooks', []),
            'other': chapter.get('other', []),
            'count': chapter.get('count', 0),
        }

    return Response({
        'grade': grade_db_val,
        'subject': subject_db_val,
        'grade_slug': slugify(LEVEL_LABELS.get(grade_db_val, grade_db_val)),
        'subject_slug': slugify(subject_db_val),
        'grade_list': grade_list,
        'subject_list': subject_list,
        'chapters': [clean_chapter(chapter) for chapter in grouped_resources],
        'total_count': total_count,
    })

def _detail_context(request, resource):
    """ResourceSerializer reads the like and bookmark state twice each (snake_case and
    camelCase fields), one EXISTS query per read; look each up once instead."""
    viewer = request.user if isinstance(getattr(request, 'user', None), User) else None
    ctx = {'request': request}
    ctx.update(prime_for_serializers(viewer, resources=[resource]))
    return ctx


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([AllowAny])
def resource_detail(request, resource_id):
    """GET /api/resources/<resourceId> — get a single resource.

    PUT/PATCH — the uploader edits their own resource (mirrors the website
    edit_resource page): metadata, link, file replacement and cover
    (upload/URL/clear). Edits go back through review (approval resets to
    pending) and video covers are auto-captured when cleared.
    """
    try:
        resource = Resource.objects.select_related('uploaded_by').get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)

    if request.method == 'GET':
        if resource.approval_status == 'approved':
            return Response(ResourceSerializer(resource, context=_detail_context(request, resource)).data)
        # Owners can still open their own pending/rejected resource (edit flow).
        viewer = _get_user_from_request(request)
        if viewer is not None and resource.uploaded_by_id == viewer.id:
            return Response(ResourceSerializer(resource, context=_detail_context(request, resource)).data)
        return Response({'error': 'Resource not found'}, status=404)

    # ----- owner edit -----
    user, err = _require_user(request)
    if err:
        return err
    if not user.email_verified:
        return Response({'error': 'Please verify your email first'}, status=403)
    if resource.uploaded_by_id != user.id:
        return Response({'error': 'You can only edit your own resources'}, status=403)

    data = request.data

    def _s(key):
        val = data.get(key)
        return val.strip() if isinstance(val, str) else ''

    if 'title' in data:
        if not _s('title'):
            return Response({'error': 'title cannot be empty'}, status=400)
        resource.title = _s('title')
    if 'subject' in data:
        if not _s('subject'):
            return Response({'error': 'subject cannot be empty'}, status=400)
        resource.subject = _s('subject')

    for field in ('description', 'grade_level', 'faculty', 'program', 'year',
                  'exam_type', 'pradesh', 'district', 'school', 'tags',
                  'author_name', 'source_label', 'source_url'):
        if field in data:
            setattr(resource, field, _s(field))

    if 'type' in data and _s('type'):
        resource.type = _s('type')

    try:
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if err_resp:
                return Response(err_resp, status=400)
            if path:
                resource.file = path
                resource.file_url = media_url(request, path)
                resource.file_size = size
        elif _s('file_url'):
            resource.file_url = read_file_url(_s('file_url'))

        thumbnail_url = read_thumbnail(request, data)
        if thumbnail_url is not None:
            resource.thumbnail_url = thumbnail_url
    except InvalidInput as exc:
        return Response({'error': exc.message}, status=400)

    # Marketplace: owner can toggle paid + price from the app/web edit form.
    if 'is_paid' in data or 'isPaid' in data or 'price' in data:
        is_paid, price_val = parse_paid_fields(data)
        resource.is_paid = is_paid
        resource.price = price_val

    resource.approval_status = 'pending'
    resource.save()
    if not resource.thumbnail_url:
        maybe_autoset_video_thumbnail(resource, request)
    cache.delete_many(['home_resources', 'library_all_resources', 'library_filter_options', 'distinct_subjects'])
    return Response(ResourceSerializer(resource, context={'request': request}).data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def resource_purchase(request, resource_id):
    """In-app purchase flow for a paid resource (Android parity with the web
    submit_payment_proof page).

    GET  — returns the viewer's access + purchase status and the price/seller,
           so the app can render the checkout sheet (locked viewers only).
    POST — buyer submits their QR payment proof: a `transaction_id` (text) and
           an optional `payment_proof` image. Creates/updates a pending
           PaymentVerification. Access is granted only after an admin approves.
    """
    try:
        resource_obj = Resource.objects.select_related('uploaded_by').get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)

    # Auth: the purchase sheet is buyer-scoped, so we need a real user.
    user, err = _require_user(request)
    if err:
        return err

    price_dec = resource_obj.price or Decimal('0.00')
    seller = resource_obj.uploaded_by or User.objects.filter(is_admin=True).first() or user

    def _status_payload():
        from web.view_helpers import check_user_resource_access
        has_access, _reason, purchase = check_user_resource_access(user, resource_obj)
        return {
            'status': 'ok',
            'is_paid': bool(resource_obj.is_paid),
            'price': ('%g' % float(price_dec)) if float(price_dec or 0) else '0',
            'has_access': bool(has_access),
            'purchase_status': getattr(purchase, 'status', '') if purchase else '',
            'purchase_id': getattr(purchase, 'id', '') if purchase else '',
            'seller_name': (seller.display_name or seller.username) if seller else '',
            'message': '',
        }

    if request.method == 'GET':
        return Response(_status_payload())

    # ----- POST: submit payment proof -----
    if not resource_obj.is_paid:
        return Response({'error': 'This resource is not paid'}, status=400)
    if resource_obj.uploaded_by_id == user.id:
        return Response({'error': 'You own this resource'}, status=400)

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

    from .marketplace import get_payment_config, compute_commission, seller_earnings_for
    _cfg = get_payment_config()
    commission_dec = compute_commission(price_dec, _cfg)
    earnings_dec = seller_earnings_for(price_dec, _cfg)

    existing_pending = PaymentVerification.objects.filter(buyer=user, resource=resource_obj, status='pending').first()
    if existing_pending:
        pv = existing_pending
        if transaction_id:
            pv.transaction_id = transaction_id
        if proof_file:
            pv.payment_proof = proof_file
            pv.payment_proof_url = request.build_absolute_uri(settings.MEDIA_URL + str(pv.payment_proof))
        pv.amount = price_dec
        pv.platform_commission = commission_dec
        pv.seller_earnings = earnings_dec
        pv.save()
    else:
        pv = PaymentVerification.objects.create(
            id=str(uuid.uuid4()),
            buyer=user,
            resource=resource_obj,
            seller=seller,
            amount=price_dec,
            platform_commission=commission_dec,
            seller_earnings=earnings_dec,
            payment_method='qr_code',
            transaction_id=transaction_id,
            payment_proof=proof_file,
            status='pending',
            created_at=_now_ms(),
        )
        if proof_file:
            pv.payment_proof_url = request.build_absolute_uri(settings.MEDIA_URL + str(pv.payment_proof))
            pv.save(update_fields=['payment_proof_url'])

    payload = _status_payload()
    payload['message'] = "Payment proof submitted! Your purchase is pending admin verification."
    return Response(payload, status=201)


def _resource_comment_payload(comment, viewer=None, liked_comment_ids=None):
    user = getattr(comment, 'user', None)
    is_liked = False
    if viewer:
        if liked_comment_ids is not None:
            is_liked = comment.id in liked_comment_ids
        else:
            from api.models import ResourceCommentLike
            is_liked = ResourceCommentLike.objects.filter(comment_id=comment.id, user_id=viewer.id).exists()
    author_name = user.username if user else 'Deleted user'
    if user:
        from .services import avatar_or_photo_url
        author_photo = avatar_or_photo_url(user) or ''
    else:
        author_photo = ''
    author_badge = None
    if user:
        from .badges import user_badge_info
        author_badge = user_badge_info(user)
    return {
        'id': comment.id,
        'resource_id': comment.resource_id,
        'resourceId': comment.resource_id,
        'user_id': comment.user_id,
        'authorId': comment.user_id or '',
        'user_name': author_name,
        'authorName': author_name,
        'user_photo_url': author_photo,
        'authorPhoto': author_photo,
        'parent_comment_id': comment.parent_comment_id,
        'parentCommentId': comment.parent_comment_id or '',
        'content': comment.content,
        'like_count': comment.like_count,
        'likeCount': comment.like_count,
        'reply_count': comment.reply_count,
        'replyCount': comment.reply_count,
        'is_liked': is_liked,
        'isLiked': is_liked,
        'is_edited': comment.is_edited,
        'isEdited': comment.is_edited,
        'created_at': comment.created_at,
        'createdAt': comment.created_at,
        'authorBadgeInfo': author_badge,
        'attachments': services._serialize_media_payload(
            comment.media.all() if hasattr(comment, 'media') else []
        ),
    }


@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def resource_like(request, resource_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        result = services.toggle_resource_like(user, resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    like_count = result.get('likeCount', result.get('like_count', 0))
    is_liked = result.get('isLiked', result.get('is_liked', False))
    return Response({
        'like_count': like_count,
        'likeCount': like_count,
        'is_liked': is_liked,
        'isLiked': is_liked,
    })


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def resource_comments(request, resource_id):
    from api.models import ResourceComment, ResourceCommentLike
    if request.method == 'GET':
        viewer = _get_user_from_request(request)
        comments = list(ResourceComment.objects.filter(resource_id=resource_id).select_related('user').prefetch_related('media').order_by('created_at'))
        liked_comment_ids = set()
        if viewer and comments:
            liked_comment_ids = set(
                ResourceCommentLike.objects.filter(
                    user_id=viewer.id,
                    comment_id__in=[comment.id for comment in comments]
                ).values_list('comment_id', flat=True)
            )
        return Response({'comments': [_resource_comment_payload(comment, viewer, liked_comment_ids) for comment in comments]})

    user = _get_user_from_request(request)
    content = (request.data.get('content') or '').strip()
    parent_id = request.data.get('parent_comment_id') or request.data.get('parentCommentId')
    try:
        attachments = validate_forum_attachments(request.data.get('attachments'))
    except ValidationError as exc:
        messages = exc.messages if hasattr(exc, 'messages') else [str(exc)]
        return Response({'error': messages[0] if messages else 'Invalid attachments'}, status=400)
    # Voice notes / attachments can be the entire comment.
    if not content and not attachments:
        return Response({'error': 'Content required'}, status=400)
    result = services.create_resource_comment(user, resource_id, content, parent_id, attachments=attachments)
    if not result:
        return Response({'error': 'Failed to create comment'}, status=400)
    comment = ResourceComment.objects.select_related('user').prefetch_related('media').get(pk=result['id'])
    return Response(_resource_comment_payload(comment, user), status=201)


@api_view(['DELETE'])
def resource_comment_detail(request, resource_id, comment_id):
    user, err = _require_user(request)
    if err:
        return err
    is_admin = bool(getattr(user, 'is_admin', False))
    ok = services.delete_resource_comment(user, comment_id, is_admin=is_admin)
    if ok:
        return Response({'success': True})
    return Response({'error': 'Permission denied or comment not found'}, status=403)


@api_view(['POST'])
def resource_comment_like(request, resource_id, comment_id):
    user, err = _require_user(request)
    if err:
        return err
    try:
        from api.models import ResourceComment
        result = services.toggle_resource_comment_like(user, comment_id)
    except ResourceComment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=404)
    return Response({
        'like_count': result['likeCount'],
        'likeCount': result['likeCount'],
        'is_liked': result['isLiked'],
        'isLiked': result['isLiked'],
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ViewIncrementRateThrottle])
def resource_view(request, resource_id):
    """POST /api/resources/<resourceId>/view {surface?, dwell_ms?} - one view per viewer per day."""
    from . import resource_reach
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    try:
        dwell = int(request.data.get('dwell_ms') or 0)
    except (TypeError, ValueError):
        dwell = 0
    out = resource_reach.record_view(
        request, resource, _get_user_from_request(request), surface=str(request.data.get('surface') or ''),
        dwell_ms=dwell, src=str(request.data.get('src') or ''))
    return Response({'view_count': out['view_count'], 'counted': out['counted']})


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ViewIncrementRateThrottle])
def resource_action(request, resource_id):
    """POST /api/resources/<resourceId>/action {action: read|download|share} - reach flags and the download count."""
    from . import resource_reach
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    out = resource_reach.record_action(request, resource, _get_user_from_request(request),
                                       str(request.data.get('action') or ''))
    return Response(out, status=200 if out.get('ok') or 'error' not in out else 400)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ViewIncrementRateThrottle])
def resource_impressions(request):
    """POST /api/resources/impressions {"ids": [...]} - resource cards that scrolled into view."""
    from . import resource_reach
    ids = request.data.get('ids') or []
    if not isinstance(ids, list):
        ids = []
    return Response({'recorded': resource_reach.record_impressions(request, ids)})


def _days_param(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 30


@api_view(['GET'])
def resource_insights(request, resource_id):
    """GET /api/resources/<id>/insights/?days=7|30|90 - the uploader and staff only."""
    from . import resource_insights as ins
    user, err = _require_user(request)
    if err:
        return err
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    if resource.uploaded_by_id != user.id and not getattr(user, 'is_admin', False):
        return Response({'error': 'Only the uploader can see these insights'}, status=403)
    return Response(ins.build(resource, days=_days_param(request.query_params.get('days', 30))))


@api_view(['GET'])
def uploads_insights(request):
    """GET /api/uploads/insights/?days=7|30|90 - everything the signed-in member has uploaded, plus their posts."""
    from . import resource_insights as ins
    user, err = _require_user(request)
    if err:
        return err
    return Response(ins.overview(user, days=_days_param(request.query_params.get('days', 30))))


def _declared_size(data):
    try:
        return int(float(data.get('file_size') or 0))
    except (ValueError, TypeError):
        return 0


def _create_pending_resource(request, uploader):
    """Shared by signed-in (uploader) and anonymous (None) uploads; the resource waits for review."""
    data = request.data
    fields = read_listing_fields(data)
    if not fields['title'] or not fields['subject']:
        return Response({'error': 'title and subject are required'}, status=400)

    file_path = ''
    try:
        source_url = read_source_url(data)
        uploaded_file = request.FILES.get('file')
        file_url = data.get('file_url', '').strip()
        if not uploaded_file and not file_url:
            return Response({'error': 'Either a file upload or file_url is required'}, status=400)

        file_size = 0
        if uploaded_file:
            path, file_size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if err_resp:
                return Response(err_resp, status=400)
            file_path = path or ''
            file_url = media_url(request, file_path)
        else:
            file_url = read_file_url(file_url)

        thumbnail_url = read_thumbnail(request, data) or ''
    except InvalidInput as exc:
        discard_saved_files([{'path': file_path}])
        return Response({'error': exc.message}, status=400)

    if uploader is None:
        origin = {'source_type': 'anonymous', 'author_name': data.get('requester_name', '').strip()[:100]}
    else:
        is_paid, price = parse_paid_fields(data)
        origin = {'source_type': 'user', 'uploaded_by': uploader, 'is_paid': is_paid, 'price': price}

    try:
        resource = Resource(
            **{**fields, **origin},
            id=str(uuid.uuid4()),
            file=file_path or None,
            file_url=file_url,
            thumbnail_url=thumbnail_url,
            file_size=file_size or _declared_size(data),
            added_at=_now_ms(),
            source_url=source_url,
            approval_status='pending',
        )
        resource.save()
        if not resource.thumbnail_url:
            maybe_autoset_video_thumbnail(resource, request)
        cache.delete_many(['home_resources', 'library_all_resources'])
        return Response(ResourceSerializer(resource).data, status=201)
    except Exception as exc:
        logger.exception("resource upload failed to save resource: %s", exc)
        return Response({'error': f'Failed to save resource: {str(exc)}'}, status=500)


@api_view(['POST'])
@throttle_classes([UploadRateThrottle])
def resource_upload(request):
    """POST /api/resources/upload — signed-in upload of a file or a file_url; pending review."""
    user, err = _require_user(request)
    if err:
        return err
    return _create_pending_resource(request, user)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([UploadRateThrottle])
def resource_upload_anonymous(request):
    """POST /api/resources/upload/anonymous — the same upload without sign-in."""
    return _create_pending_resource(request, None)



@api_view(['GET'])
@permission_classes([AllowAny])
def resource_requests_list(request):
    """GET /api/resource-requests/ — list open requests with optional filters."""
    qs = ResourceRequest.objects.select_related('requested_by').all()
    status_filter = request.query_params.get('status', 'open')
    if status_filter:
        qs = qs.filter(status=status_filter)
    subject = request.query_params.get('subject')
    if subject:
        qs = qs.filter(subject__iexact=subject)
    grade = request.query_params.get('grade')
    if grade:
        from .education_catalog import level_match_values
        gq = Q()
        for v in level_match_values(grade) or [grade]:
            gq |= Q(grade_level__iexact=v)
        qs = qs.filter(gq)
    qs = qs.order_by('-upvote_count', '-created_at')
    user = _get_user_from_request(request)
    upvoted_ids = set()
    if user:
        upvoted_ids = set(ResourceRequestUpvote.objects.filter(
            user=user, request_id__in=list(qs.values_list('id', flat=True)[:100])
        ).values_list('request_id', flat=True))
    return Response(ResourceRequestSerializer(
        qs[:50], many=True, context={'request': request, 'upvoted_request_ids': upvoted_ids}
    ).data)

def _save_resource_request(request, **requester):
    fields = read_request_fields(request.data)
    if not fields['title']:
        return Response({'error': 'title is required'}, status=400)
    req = ResourceRequest(id=str(uuid.uuid4()), **fields, created_at=_now_ms(), **requester)
    req.save()
    return Response(ResourceRequestSerializer(req, context={'request': request}).data, status=201)


@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def resource_request_create(request):
    """POST /api/resource-requests/ — create a resource request (authenticated)."""
    user, err = _require_user(request)
    if err:
        return err
    return _save_resource_request(request, requested_by=user)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([UploadRateThrottle])
def resource_request_create_anonymous(request):
    """POST /api/resource-requests/anonymous/ — create a resource request (anonymous)."""
    return _save_resource_request(
        request,
        requested_by=None,
        requester_name=request.data.get('requester_name', '').strip()[:100],
        requester_email=request.data.get('requester_email', '').strip(),
    )


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([WriteActionRateThrottle])
def resource_request_upvote(request, request_id):
    """POST /api/resource-requests/<request_id>/upvote — toggle upvote."""
    user, err = _require_user(request)
    if err:
        return err
    try:
        req = ResourceRequest.objects.get(pk=request_id)
    except ResourceRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)
    existing = ResourceRequestUpvote.objects.filter(request=req, user=user)
    if existing.exists():
        existing.delete()
        ResourceRequest.objects.filter(pk=request_id).update(upvote_count=F('upvote_count') - 1)
        req.refresh_from_db()
        return Response({'upvoted': False, 'upvote_count': req.upvote_count})
    else:
        ResourceRequestUpvote.objects.create(request=req, user=user)
        ResourceRequest.objects.filter(pk=request_id).update(upvote_count=F('upvote_count') + 1)
        req.refresh_from_db()
        return Response({'upvoted': True, 'upvote_count': req.upvote_count})
