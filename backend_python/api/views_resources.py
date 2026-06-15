"""Views Resources extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403

@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def resources_list(request):
    """GET /api/resources — public, paginated library feed with web-parity filters/sort.

    Android and the website both browse approved lead resources without forcing
    sign-in. Keep this endpoint cheap: filter in SQL, sort in SQL, and only
    serialize the requested page.
    """
    resources = Resource.objects.filter(approval_status='approved', is_lead=True)

    subject = (request.query_params.get('subject') or '').strip()
    grade = (request.query_params.get('grade') or '').strip()
    rtype = (request.query_params.get('type') or '').strip()
    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'relevant').strip().lower()

    if subject:
        resources = resources.filter(subject__iexact=subject)
    if grade:
        resources = resources.filter(grade_level__iexact=grade)
    if rtype:
        resources = resources.filter(type__iexact=rtype)
    if search:
        resources = resources.filter(
            Q(title__icontains=search) | Q(description__icontains=search) |
            Q(subject__icontains=search) | Q(grade_level__icontains=search) |
            Q(faculty__icontains=search) | Q(program__icontains=search) |
            Q(school__icontains=search) | Q(tags__icontains=search)
        )

    if sort == 'newest':
        resources = resources.order_by('-added_at', '-view_count')
    elif sort == 'oldest':
        resources = resources.order_by('added_at')
    elif sort == 'liked':
        resources = resources.order_by('-like_count', '-added_at')
    elif sort == 'trending':
        resources = resources.order_by('-view_count', '-like_count', '-added_at')
    else:
        resources = resources.order_by('-added_at', '-view_count')

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

    Mirrors the website Library → Syllabus tab, driven by admin-created
    SyllabusContent when present and falling back to CURRICULUM_MAP.
    """
    from collections import defaultdict
    from api.models import SyllabusContent
    try:
        from web import curriculum
    except Exception:
        curriculum = None

    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    categories_map = defaultdict(set)
    active_syllabus = SyllabusContent.objects.all().values('grade_level', 'subject')

    if active_syllabus.exists():
        for item in active_syllabus:
            grade = (item.get('grade_level') or '').strip()
            if grade.lower() == 'grade 12':
                grade = 'Class 12'
            elif grade.lower() == 'grade 11':
                grade = 'Class 11'
            subject_str = item.get('subject') or ''
            if grade and subject_str:
                for subj in subject_str.split(','):
                    subj = subj.strip()
                    if subj:
                        categories_map[grade].add(subj)
    elif curriculum is not None:
        for (grade, subj) in getattr(curriculum, 'CURRICULUM_MAP', {}).keys():
            if grade and subj:
                categories_map[grade].add(subj)

    def _slug(value):
        return (value or '').lower().replace(' / see', '-see').replace('/', '-').replace(' ', '-')

    grade_order = {value: idx for idx, value in enumerate(education_levels)}
    categories = []
    for grade, subjects in categories_map.items():
        subject_items = []
        for subj in sorted(subjects):
            subject_items.append({
                'name': subj,
                'slug': _slug(subj),
                'url': f"/subject/{_slug(grade)}/{_slug(subj)}/",
            })
        categories.append({
            'grade': grade,
            'subjects': subject_items,
            'order': grade_order.get(grade, 999),
        })
    categories.sort(key=lambda item: item['order'])
    return Response({'categories': categories})

@api_view(['GET'])
def resource_detail(request, resource_id):
    """GET /api/resources/<resourceId> — get a single resource (authenticated)."""
    user, err = _require_user(request)
    if err:
        return err
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    if resource.approval_status != 'approved':
        return Response({'error': 'Resource not found'}, status=404)
    return Response(ResourceSerializer(resource).data)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ViewIncrementRateThrottle])
def resource_view(request, resource_id):
    """POST /api/resources/<resourceId>/view — increment view_count."""
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)
    Resource.objects.filter(pk=resource_id).update(view_count=F('view_count') + 1)
    return Response({'view_count': resource.view_count + 1})

@api_view(['POST'])
@throttle_classes([UploadRateThrottle])
def resource_upload(request):
    """POST /api/resources/upload — authenticated user uploads a resource.
    Requires auth. Accepts either a file upload or a file_url.
    Resource is created with approval_status='pending'."""
    user, err = _require_user(request)
    if err:
        return err

    data = request.data
    title = data.get('title', '').strip()
    subject = data.get('subject', '').strip()

    if not title or not subject:
        return Response({'error': 'title and subject are required'}, status=400)

    uploaded_file = request.FILES.get('file')
    file_url = data.get('file_url', '').strip()

    if not uploaded_file and not file_url:
        return Response({'error': 'Either a file upload or file_url is required'}, status=400)

    file_path = ''
    file_size = 0
    if uploaded_file:
        path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
        if err_resp:
            return Response(err_resp, status=400)
        file_path = path or ''
        file_size = size
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path) if file_path else ''

    if not uploaded_file and file_url:
        try:
            file_url = validate_resource_file_url(file_url)
        except Exception as exc:
            messages_list = getattr(exc, 'messages', [str(exc)])
            return Response({'error': ' '.join(messages_list)}, status=400)

    thumbnail_url = data.get('thumbnail_url', '').strip()
    if thumbnail_url:
        try:
            thumbnail_url = validate_resource_file_url(thumbnail_url)
        except Exception as exc:
            messages_list = getattr(exc, 'messages', [str(exc)])
            return Response({'error': ' '.join(messages_list)}, status=400)

    resource = Resource(
        id=str(uuid.uuid4()),
        title=title,
        description=data.get('description', '').strip(),
        subject=subject,
        grade_level=data.get('grade_level', '').strip(),
        faculty=data.get('faculty', '').strip(),
        program=data.get('program', '').strip(),
        year=data.get('year', '').strip(),
        exam_type=data.get('exam_type', '').strip(),
        pradesh=data.get('pradesh', '').strip(),
        district=data.get('district', '').strip(),
        school=data.get('school', '').strip(),
        tags=data.get('tags', '').strip(),
        type=data.get('type', 'PDF').strip() or 'PDF',
        file=file_path or None,
        file_url=file_url,
        thumbnail_url=thumbnail_url or '',
        file_size=file_size or int(data.get('file_size') or 0),
        added_at=_now_ms(),
        author_name=data.get('author_name', '').strip(),
        source_type='user',
        uploaded_by=user,
        source_label=data.get('source_label', '').strip(),
        source_url=data.get('source_url', '').strip(),
        approval_status='pending',
    )
    resource.save()
    cache.delete_many(['home_resources', 'library_all_resources'])
    return Response(ResourceSerializer(resource).data, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([UploadRateThrottle])
def resource_upload_anonymous(request):
    """POST /api/resources/upload/anonymous — anonymous resource upload.
    No auth required. Accepts either a file upload or a file_url.
    Resource is created with approval_status='pending'."""
    data = request.data
    title = data.get('title', '').strip()
    subject = data.get('subject', '').strip()

    if not title or not subject:
        return Response({'error': 'title and subject are required'}, status=400)

    uploaded_file = request.FILES.get('file')
    file_url = data.get('file_url', '').strip()

    if not uploaded_file and not file_url:
        return Response({'error': 'Either a file upload or file_url is required'}, status=400)

    file_path = ''
    file_size = 0
    if uploaded_file:
        path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
        if err_resp:
            return Response(err_resp, status=400)
        file_path = path or ''
        file_size = size
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path) if file_path else ''

    if not uploaded_file and file_url:
        try:
            file_url = validate_resource_file_url(file_url)
        except Exception as exc:
            messages_list = getattr(exc, 'messages', [str(exc)])
            return Response({'error': ' '.join(messages_list)}, status=400)

    thumbnail_url = data.get('thumbnail_url', '').strip()
    if thumbnail_url:
        try:
            thumbnail_url = validate_resource_file_url(thumbnail_url)
        except Exception as exc:
            messages_list = getattr(exc, 'messages', [str(exc)])
            return Response({'error': ' '.join(messages_list)}, status=400)

    requester_name = data.get('requester_name', '').strip()[:100]
    resource = Resource(
        id=str(uuid.uuid4()),
        title=title,
        description=data.get('description', '').strip(),
        subject=subject,
        grade_level=data.get('grade_level', '').strip(),
        faculty=data.get('faculty', '').strip(),
        program=data.get('program', '').strip(),
        year=data.get('year', '').strip(),
        exam_type=data.get('exam_type', '').strip(),
pradesh=data.get('pradesh', '').strip(),
        district=data.get('district', '').strip(),
        school=data.get('school', '').strip(),
        tags=data.get('tags', '').strip(),
        type=data.get('type', 'PDF').strip() or 'PDF',
        file=file_path or None,
        file_url=file_url,
        thumbnail_url=thumbnail_url or '',
        file_size=file_size or int(data.get('file_size') or 0),
        added_at=_now_ms(),
        author_name=requester_name,
        source_type='anonymous',
        approval_status='pending',
        source_label=data.get('source_label', '').strip(),
        source_url=data.get('source_url', '').strip(),
    )
    resource.save()
    cache.delete_many(['home_resources', 'library_all_resources'])
    return Response(ResourceSerializer(resource).data, status=201)

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
        qs = qs.filter(grade_level__iexact=grade)
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

@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def resource_request_create(request):
    """POST /api/resource-requests/ — create a resource request (authenticated)."""
    user, err = _require_user(request)
    if err:
        return err
    title = request.data.get('title', '').strip()
    if not title:
        return Response({'error': 'title is required'}, status=400)
    req = ResourceRequest(
        id=str(uuid.uuid4()),
        title=title,
        description=request.data.get('description', '').strip(),
        subject=request.data.get('subject', '').strip(),
        grade_level=request.data.get('grade_level', '').strip(),
        faculty=request.data.get('faculty', '').strip(),
        program=request.data.get('program', '').strip(),
        year=request.data.get('year', '').strip(),
        exam_type=request.data.get('exam_type', '').strip(),
        pradesh=request.data.get('pradesh', '').strip(),
        district=request.data.get('district', '').strip(),
        tags=request.data.get('tags', '').strip(),
        requested_by=user,
        created_at=_now_ms(),
    )
    req.save()
    return Response(ResourceRequestSerializer(req, context={'request': request}).data, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([UploadRateThrottle])
def resource_request_create_anonymous(request):
    """POST /api/resource-requests/anonymous/ — create a resource request (anonymous)."""
    title = request.data.get('title', '').strip()
    if not title:
        return Response({'error': 'title is required'}, status=400)
    req = ResourceRequest(
        id=str(uuid.uuid4()),
        title=title,
        description=request.data.get('description', '').strip(),
        subject=request.data.get('subject', '').strip(),
        grade_level=request.data.get('grade_level', '').strip(),
        faculty=request.data.get('faculty', '').strip(),
        program=request.data.get('program', '').strip(),
        year=request.data.get('year', '').strip(),
        exam_type=request.data.get('exam_type', '').strip(),
        pradesh=request.data.get('pradesh', '').strip(),
        district=request.data.get('district', '').strip(),
        tags=request.data.get('tags', '').strip(),
        requested_by=None,
        requester_name=request.data.get('requester_name', '').strip()[:100],
        requester_email=request.data.get('requester_email', '').strip(),
        created_at=_now_ms(),
    )
    req.save()
    return Response(ResourceRequestSerializer(req, context={'request': request}).data, status=201)

@api_view(['POST'])
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
