"""Views Admin extracted from views.py."""
from decimal import Decimal
from .view_helpers import *  # noqa: F401,F403

def admin_pending_resources(request):
    """Admin page to approve/reject pending resources."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        resource_id = request.POST.get('resource_id', '').strip()
        action = request.POST.get('action', '').strip()
        try:
            resource_obj = Resource.objects.get(pk=resource_id)
            admin_user = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
                    admin_user = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    pass
            
            # Identify all resources in the same upload group (or just the resource itself if no group)
            if resource_obj.upload_group_id:
                group_resources = Resource.objects.filter(upload_group_id=resource_obj.upload_group_id)
            else:
                group_resources = [resource_obj]

            if action == 'approve':
                for r in group_resources:
                    r.approval_status = 'approved'
                    r.reviewed_by = admin_user
                    r.reviewed_at = now_ms()
                    r.rejection_reason = ''
                    r.save()
                    if r.uploaded_by_id:
                        _counters.increment_user_resource_approved(r.uploaded_by_id)
                        _notif.notify_resource_approved(r.id, r.uploaded_by_id)
            elif action == 'reject':
                reason = request.POST.get('reason', '').strip()[:500]
                for r in group_resources:
                    r.approval_status = 'rejected'
                    r.reviewed_by = admin_user
                    r.reviewed_at = now_ms()
                    r.rejection_reason = reason
                    r.save()
                    if r.uploaded_by_id:
                        _notif.notify_resource_rejected(r.id, r.uploaded_by_id, reason)
            
            cache.delete_many(['home_resources', 'library_all_resources'])
        except Resource.DoesNotExist:
            pass
        return redirect('web:admin_pending_resources')

    pending = list(Resource.objects.filter(approval_status='pending').select_related('uploaded_by').order_by('added_at'))
    
    # Group the pending resources by upload_group_id to show them as a single request card
    group_members_map = {}
    for r in pending:
        if r.upload_group_id:
            group_members_map.setdefault(r.upload_group_id, []).append(r)

    grouped_pending = []
    seen_groups = set()
    
    for r in pending:
        if r.upload_group_id:
            if r.upload_group_id in seen_groups:
                continue
            seen_groups.add(r.upload_group_id)
            
            group_members = group_members_map.get(r.upload_group_id, [])
            if not group_members:
                continue
                
            lead_r = next((m for m in group_members if m.is_lead), group_members[0])
            lead_data = _serialize_resource(lead_r)
            
            # List all file details in this group
            lead_data['group_files'] = [
                {
                    'id': m.id,
                    'title': m.title,
                    'file_url': m.file.url if m.file else m.file_url,
                    'file_name': os.path.basename(m.file.name) if m.file else 'External URL'
                } for m in group_members
            ]
            grouped_pending.append(lead_data)
        else:
            data = _serialize_resource(r)
            data['group_files'] = [
                {
                    'id': r.id,
                    'title': r.title,
                    'file_url': r.file.url if r.file else r.file_url,
                    'file_name': os.path.basename(r.file.name) if r.file else 'External URL'
                }
            ]
            grouped_pending.append(data)

    return render(request, 'admin_panel/pending_resources.html', {
        'is_admin': True,
        'pending_resources': grouped_pending,
        'active_page': 'pending_resources',
    })

def admin_resource_requests(request):
    """Admin page to manage resource requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        request_id = request.POST.get('request_id', '').strip()
        action = request.POST.get('action', '').strip()
        try:
            req = ResourceRequest.objects.get(pk=request_id)
            if action == 'fulfill':
                req.status = 'fulfilled'
                req.fulfilled_at = now_ms()
                resource_id = request.POST.get('resource_id', '').strip()
                if resource_id:
                    req.fulfilled_by_id = resource_id
                req.save()
            elif action == 'close':
                req.status = 'closed'
                req.save()
            elif action == 'reopen':
                req.status = 'open'
                req.save()
        except ResourceRequest.DoesNotExist:
            pass
        return redirect('web:admin_resource_requests')

    status_filter = request.GET.get('status', '')
    qs = ResourceRequest.objects.select_related('requested_by').all().order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    requests_data = []
    for req in qs[:100]:
        rd = {
            'id': req.id,
            'title': req.title,
            'description': req.description or '',
            'subject': req.subject,
            'grade_level': req.grade_level,
            'status': req.status,
            'upvote_count': req.upvote_count,
            'created_at': req.created_at,
            'requested_by_name': req.requested_by.display_name or req.requested_by.username if req.requested_by else (req.requester_name or 'Anonymous'),
            'requester_email': req.requester_email or '',
        }
        requests_data.append(rd)
    return render(request, 'admin_panel/resource_requests.html', {
        'is_admin': True,
        'requests': requests_data,
        'current_status': status_filter,
        'active_page': 'resource_requests',
    })

def admin_login(request):
    if _is_staff_admin(request):
        return redirect('web:admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_active and user.is_staff:
            django_login(request, user)
            return redirect('web:admin_dashboard')
        return render(request, 'admin_panel/login.html', {'error': 'Invalid staff credentials'})
    return render(request, 'admin_panel/login.html')

def admin_logout(request):
    django_logout(request)
    return redirect('web:admin_login')

def admin_dashboard(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    stats = cache.get('admin_stats')
    if stats is None:
        from django.db.models import Sum, Count, Avg
        _now = now_ms()
        seven_days_ago = _now - 7 * 86400000
        thirty_days_ago = _now - 30 * 86400000

        total_users = User.objects.count()
        total_resources = Resource.objects.count()
        total_posts = Post.objects.count()
        total_replies = Reply.objects.count()
        total_likes = Post.objects.aggregate(total=Sum('thumbs_up_count'))['total'] or 0
        total_reply_likes = Reply.objects.aggregate(total=Sum('thumbs_up_count'))['total'] or 0
        total_resource_views = Resource.objects.aggregate(total=Sum('view_count'))['total'] or 0
        total_post_views = Post.objects.aggregate(total=Sum('view_count'))['total'] or 0
        pending_resources = Resource.objects.filter(approval_status='pending').count()
        new_users_week = User.objects.filter(created_at__gte=seven_days_ago).count()
        new_users_month = User.objects.filter(created_at__gte=thirty_days_ago).count()
        new_posts_week = Post.objects.filter(created_at__gte=seven_days_ago).count()
        new_posts_month = Post.objects.filter(created_at__gte=thirty_days_ago).count()
        new_replies_week = Reply.objects.filter(created_at__gte=seven_days_ago).count()
        new_replies_month = Reply.objects.filter(created_at__gte=thirty_days_ago).count()
        new_resources_week = Resource.objects.filter(added_at__gte=seven_days_ago).count()
        new_resources_month = Resource.objects.filter(added_at__gte=thirty_days_ago).count()

        recent_users = list(User.objects.order_by('-created_at')[:10])
        top_posts = list(Post.objects.select_related('user').filter(is_archived=False).order_by('-thumbs_up_count')[:10])
        top_viewed_posts = list(Post.objects.select_related('user').filter(is_archived=False).order_by('-view_count')[:10])
        top_viewed_resources = list(Resource.objects.filter(approval_status='approved').order_by('-view_count')[:10])
        subject_counts_raw = Resource.objects.filter(approval_status='approved').values_list('subject').annotate(count=Count('id'))
        subject_counts_split = {}
        for subj_str, cnt in subject_counts_raw:
            for s in (subj_str or '').split(','):
                s = s.strip()
                if s:
                    subject_counts_split[s] = subject_counts_split.get(s, 0) + cnt
        subject_counts = dict(sorted(subject_counts_split.items(), key=lambda x: x[1], reverse=True)[:15])
        category_counts = dict(Post.objects.filter(is_archived=False).values_list('category').annotate(count=Count('id')).order_by('-count')[:10])
        resource_type_counts = dict(Resource.objects.filter(approval_status='approved').values_list('type').annotate(count=Count('id')).order_by('-count'))

        stats = {
            'total_users': total_users,
            'total_resources': total_resources,
            'total_posts': total_posts,
            'total_replies': total_replies,
            'total_likes': total_likes,
            'total_reply_likes': total_reply_likes,
            'total_resource_views': total_resource_views,
            'total_post_views': total_post_views,
            'pending_resources': pending_resources,
            'new_users_week': new_users_week,
            'new_users_month': new_users_month,
            'new_posts_week': new_posts_week,
            'new_posts_month': new_posts_month,
            'new_replies_week': new_replies_week,
            'new_replies_month': new_replies_month,
            'new_resources_week': new_resources_week,
            'new_resources_month': new_resources_month,
            'recent_users': recent_users,
            'top_posts': top_posts,
            'top_viewed_posts': top_viewed_posts,
            'top_viewed_resources': top_viewed_resources,
            'subject_counts': subject_counts,
            'category_counts': category_counts,
            'resource_type_counts': resource_type_counts,
        }
        cache.set('admin_stats', stats, 300)
    return render(request, 'admin_panel/dashboard.html', {
        'is_admin': True,
        'stats': stats,
        'active_page': 'dashboard',
    })

def admin_users(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    users_qs = User.objects.all().order_by('-created_at')
    search = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '').strip()
    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search) | Q(email__icontains=search) | Q(display_name__icontains=search)
        )
    if role_filter == 'teacher_verified':
        users_qs = users_qs.filter(role='teacher', teacher_verified=True)
    elif role_filter == 'institution_verified':
        users_qs = users_qs.filter(role='institution', institution_verified=True)
    elif role_filter in ('student', 'teacher', 'institution', 'explorer'):
        users_qs = users_qs.filter(role=role_filter)
    paginator = Paginator(users_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    users_data = [UserSerializer(u).data for u in page_obj]
    return render(request, 'admin_panel/users.html', {
        'is_admin': True,
        'users': users_data,
        'page_obj': page_obj,
        'search': search,
        'role_filter': role_filter,
        'active_page': 'users',
    })

def admin_user_detail(request, user_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        user_obj = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:admin_users')
    if request.method == 'POST':
        if request.POST.get('_method') == 'delete':
            user_obj.delete()
            return redirect('web:admin_users')
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user_obj.username:
            if User.objects.filter(username=new_username).exclude(pk=user_obj.pk).exists():
                return HttpResponse('Username already taken by another user.', status=409)
            user_obj.username = new_username
        for field in ['email', 'display_name', 'gender', 'class_level', 'subjects', 'pradesh', 'district', 'school', 'bio', 'photo_url', 'banner_url']:
            val = request.POST.get(field, '').strip()
            if val:
                setattr(user_obj, field, val)
        # Allow clearing these explicit-clear fields (e.g. to remove a photo)
        for clearable in ['bio', 'photo_url', 'banner_url']:
            if clearable in request.POST and not request.POST.get(clearable, '').strip():
                setattr(user_obj, clearable, None)
        # Handle direct image uploads (override URL field if a file is provided)
        from api.security import save_profile_image_upload, save_banner_image_upload
        photo_upload = request.FILES.get('photo_upload')
        if photo_upload:
            try:
                user_obj.photo_url = save_profile_image_upload(request, user_obj, photo_upload)
            except Exception as upload_err:
                return HttpResponse(f'Photo upload failed: {upload_err}', status=400)
        banner_upload = request.FILES.get('banner_upload')
        if banner_upload:
            try:
                user_obj.banner_url = save_banner_image_upload(request, user_obj, banner_upload)
            except Exception as upload_err:
                return HttpResponse(f'Banner upload failed: {upload_err}', status=400)
        user_obj.is_locked = request.POST.get('is_locked') == 'on'
        user_obj.verification_level = int(request.POST.get('verification_level', '0'))
        user_obj.moderator_level = int(request.POST.get('moderator_level', '0'))
        user_obj.is_admin = request.POST.get('is_admin') == 'on'
        user_obj.is_bot = request.POST.get('is_bot') == 'on'
        role = request.POST.get('role', '').strip()
        if role in ('student', 'teacher', 'institution', 'explorer'):
            user_obj.role = role
        user_obj.teacher_verified = request.POST.get('teacher_verified') == 'on'
        user_obj.institution_verified = request.POST.get('institution_verified') == 'on'
        user_obj.achievement_badges = request.POST.get('achievement_badges', '')
        user_obj.save()
    user_data = UserSerializer(user_obj).data
    achievement_badges_list = _user_achievement_badges(user_obj)
    from api.models import NEPAL_DISTRICTS
    return render(request, 'admin_panel/user_detail.html', {
        'is_admin': True,
        'user_detail': user_data,
        'achievement_badges_list': achievement_badges_list,
        'active_page': 'users',
        'nepal_districts': NEPAL_DISTRICTS,
    })

def admin_resources(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subject = request.POST.get('subject', '').strip()
        grade_level = request.POST.get('grade_level', '').strip()
        rtype = request.POST.get('type', '').strip() or 'PDF'
        file_url = request.POST.get('file_url', '').strip()
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        description = request.POST.get('description', '').strip()
        uploaded_file = request.FILES.get('file')
        tags = request.POST.get('tags', '').strip()
        faculty = request.POST.get('faculty', '').strip()
        program = request.POST.get('program', '').strip()
        year = request.POST.get('year', '').strip()
        exam_type = request.POST.get('exam_type', '').strip()
        pradesh = request.POST.get('pradesh', '').strip()
        district = request.POST.get('district', '').strip()
        school = request.POST.get('school', '').strip()
        author_name = request.POST.get('author_name', '').strip()
        source_url = request.POST.get('source_url', '').strip()
        source_label = request.POST.get('source_label', '').strip()

        file_path = ''
        file_size = 0
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp:
                file_path = path or ''
                file_size = size
                file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path) if file_path else ''

        if title and subject and (file_path or file_url):
            try:
                from api.security import validate_resource_file_url as _validate
                safe_url = ''
                if file_url and not file_path:
                    safe_url = _validate(file_url)
                elif file_url:
                    safe_url = file_url
                safe_thumb = ''
                if thumbnail_url:
                    safe_thumb = _validate(thumbnail_url)
                Resource.objects.create(
                    id=uuid_str(),
                    title=title,
                    description=description,
                    subject=subject,
                    grade_level=grade_level,
                    faculty=faculty,
                    program=program,
                    year=year,
                    exam_type=exam_type,
                    pradesh=pradesh,
                    district=district,
                    school=school,
                    tags=tags,
                    type=rtype,
                    file=file_path or None,
                    file_url=safe_url,
                    thumbnail_url=safe_thumb,
                    file_size=file_size or int(request.POST.get('file_size', '0')),
                    added_at=now_ms(),
                    view_count=0,
                    author_name=author_name,
                    source_url=source_url,
                    source_label=source_label,
                )
            except Exception:
                pass
    resources_qs = Resource.objects.all().order_by('-added_at')
    search = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    if search:
        resources_qs = resources_qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if status_filter in ('approved', 'pending', 'rejected'):
        resources_qs = resources_qs.filter(approval_status=status_filter)
    paginator = Paginator(resources_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    resources_data = [ResourceSerializer(r).data for r in page_obj]
    return render(request, 'admin_panel/resources.html', {
        'is_admin': True,
        'resources': resources_data,
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'pending_count': Resource.objects.filter(approval_status='pending').count(),
        'active_page': 'resources',
    })

def admin_resource_create(request):
    """Standalone admin resource creation page â€” full-featured form matching the public upload page."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    _default_subjects = [
        'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
        'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
        'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
        'Environment Science', 'Science', 'General Science', 'Life Science',
        'Physical Science', 'Earth Science', 'Applied Mathematics',
        'Business Mathematics', 'Statistics', 'Probability',
        'Microeconomics', 'Macroeconomics',
        'Financial Accounting', 'Cost Accounting', 'Auditing',
        'Marketing', 'Office Management', 'Hotel Management',
        'Computer Engineering', 'Electronics', 'Electrical Engineering',
        'Civil Engineering', 'Mechanical Engineering', 'Architecture',
        'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Botany', 'Zoology', 'Genetics', 'Ecology',
        'English Grammar', 'English Literature', 'Creative Writing',
        'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
        'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
        'Education', 'Pedagogy', 'Curriculum Development',
        'Law', 'Constitutional Law', 'International Law',
        'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
        'Agriculture', 'Forestry', 'Veterinary Science',
        'Management', 'Human Resource Management', 'Entrepreneurship',
        'Information Technology', 'Programming', 'Web Development',
        'Database Management', 'Networking', 'Cybersecurity',
        'Machine Learning', 'Artificial Intelligence', 'Data Science',
        'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
        'Digital Logic', 'Operating Systems', 'Software Engineering',
        'Surveying', 'Estimating & Costing', 'Building Construction',
        'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
        'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
    ]
    db_subjects = []
    for s_str in Resource.objects.values_list('subject', flat=True):
        if s_str:
            for s in s_str.split(','):
                s_stripped = s.strip()
                if s_stripped:
                    db_subjects.append(s_stripped)
    subjects = sorted(set(_default_subjects + db_subjects))
    common_tags = [
        'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
        'Important Questions', 'Numerical', 'Derivation', 'Formula Sheet',
        'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5',
        'Chapter 6', 'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10',
        'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5',
        'Class 11', 'Class 12', 'Grade 11', 'Grade 12',
        'Science', 'Management', 'Humanities', 'Education', 'Law',
        'Final Exam', 'Midterm', 'Internal Assessment', 'Practical',
        'Old Course', 'New Course', 'Revised Syllabus', 'Curriculum',
        'Textbook', 'Reference Book', 'Guide', 'Notes', 'Summary',
        'Objective Questions', 'Subjective Questions', 'MCQ', 'Long Answer',
        'Short Answer', 'Very Short Answer', 'Essay Type',
        '2080 BS', '2081 BS', '2082 BS', '2079 BS',
        '2078 BS', '2077 BS', '2076 BS',
        'Kathmandu', 'Pokhara', 'Chitwan', 'Biratnagar', 'Butwal',
        'HSEB', 'TU', 'KU', 'PU', 'CTEVT',
        'Entrance', 'IOE', 'IOM', 'CEEE', 'KUUMAT',
        'C Programming', 'Python', 'Java', 'Web Development',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Mechanics', 'Optics', 'Thermodynamics', 'Electricity',
        'Calculus', 'Algebra', 'Trigonometry', 'Geometry', 'Statistics',
        'Botany', 'Zoology', 'Ecology', 'Genetics',
        'Nepali', 'English', 'Social Studies',
    ]
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    exam_types = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']
    pradesh_options = [
        'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
    ]
    resource_types = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subject = request.POST.get('subject', '').strip()
        grade_level = request.POST.get('grade_level', '').strip()
        faculty = request.POST.get('faculty', '').strip()
        program = request.POST.get('program', '').strip()
        year = request.POST.get('year', '').strip()
        exam_type = request.POST.get('exam_type', '').strip()
        pradesh = request.POST.get('pradesh', '').strip()
        district = request.POST.get('district', '').strip()
        school = request.POST.get('school', '').strip()
        tags = request.POST.get('tags', '').strip()
        description = request.POST.get('description', '').strip()
        rtype = request.POST.get('type', 'PDF').strip() or 'PDF'
        author_name = request.POST.get('author_name', '').strip()
        source_url = request.POST.get('source_url', '').strip()
        source_label = request.POST.get('source_label', '').strip()
        source_type = request.POST.get('source_type', 'admin').strip() or 'admin'
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        view_count = int(request.POST.get('view_count', '0') or '0')
        approval_status = request.POST.get('approval_status', 'approved').strip() or 'approved'
        behalf_username = request.POST.get('behalf_username', '').strip().lstrip('@')
        behalf_user = None
        if behalf_username:
            try:
                behalf_user = User.objects.get(username__iexact=behalf_username)
            except User.DoesNotExist:
                errors.append(f"No platform user found with username '@{behalf_username}'.")

        # Marketplace: admins can list a resource as paid with a price.
        is_paid = request.POST.get('is_paid') in ['on', 'true', '1', True]
        try:
            price_val = Decimal(request.POST.get('price', '0').strip() or '0')
        except Exception:
            price_val = Decimal('0.00')
        if price_val < 0:
            price_val = Decimal('0.00')
        if not is_paid:
            price_val = Decimal('0.00')
        elif price_val <= 0:
            errors.append('Please set a valid price (greater than Rs. 0) for paid resources.')

        uploaded_files = request.FILES.getlist('file')
        file_url = request.POST.get('file_url', '').strip()

        errors = []
        if not title:
            errors.append('Title is required.')
        if not subject:
            errors.append('Subject is required.')
        if not uploaded_files and not file_url:
            errors.append('Please upload a file or provide a file URL.')

        saved_files = []
        if uploaded_files:
            for f in uploaded_files:
                path, size, err_resp = validate_and_save_resource_file(request, f)
                if err_resp:
                    errors.append(f"{f.name}: {err_resp['error']}")
                else:
                    saved_files.append({
                        'path': path or '',
                        'size': size,
                        'name': f.name
                    })

            if errors:
                from django.core.files.storage import default_storage
                for sf in saved_files:
                    if sf['path']:
                        try:
                            default_storage.delete(sf['path'])
                        except Exception:
                            pass

        safe_file_url = ''
        if not uploaded_files and file_url:
            try:
                safe_file_url = validate_resource_file_url(file_url)
            except Exception as exc:
                messages_list = getattr(exc, 'messages', [str(exc)])
                errors.append(' '.join(messages_list))

        safe_thumbnail_url = ''
        if thumbnail_url:
            try:
                safe_thumbnail_url = validate_resource_file_url(thumbnail_url)
            except Exception:
                errors.append('Invalid thumbnail URL.')

        if not errors:
            if source_type not in ('admin', 'user', 'anonymous', 'external'):
                source_type = 'admin'
            if approval_status not in ('approved', 'pending', 'rejected'):
                approval_status = 'approved'

            admin_user = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
                    admin_user = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    pass

            effective_uploader = behalf_user or admin_user
            if behalf_user:
                source_type = 'user'

            created_count = 0
            if saved_files:
                import os
                from django.conf import settings
                
                group_id = uuid_str() if len(saved_files) > 1 else ''
                
                for idx, sf in enumerate(saved_files):
                    res_title = title
                    is_lead = True
                    if len(saved_files) > 1:
                        if idx > 0:
                            is_lead = False
                            display_name = os.path.splitext(sf['name'])[0]
                            res_title = f"{title} - {display_name}"

                    final_file_url = request.build_absolute_uri(settings.MEDIA_URL + sf['path'])
                    resource = Resource(
                        id=uuid_str(),
                        title=res_title,
                        description=description,
                        subject=subject,
                        grade_level=grade_level,
                        faculty=faculty,
                        program=program,
                        year=year,
                        exam_type=exam_type,
                        pradesh=pradesh,
                        district=district,
                        school=school,
                        tags=tags,
                        type=rtype,
                        file=sf['path'] or None,
                        file_url=final_file_url,
                        thumbnail_url=safe_thumbnail_url,
                        file_size=sf['size'],
                        added_at=now_ms() + idx,
                        view_count=view_count,
                        author_name=author_name,
                        source_type=source_type,
                        uploaded_by=effective_uploader,
                        source_url=source_url,
                        source_label=source_label,
                        approval_status=approval_status,
                        reviewed_by=admin_user if approval_status == 'approved' else None,
                        reviewed_at=now_ms() if approval_status == 'approved' else None,
                        upload_group_id=group_id,
                        is_lead=is_lead,
                        is_paid=is_paid,
                        price=price_val,
                    )
                    resource.save()
                    created_count += 1
            else:
                resource = Resource(
                    id=uuid_str(),
                    title=title,
                    description=description,
                    subject=subject,
                    grade_level=grade_level,
                    faculty=faculty,
                    program=program,
                    year=year,
                    exam_type=exam_type,
                    pradesh=pradesh,
                    district=district,
                    school=school,
                    tags=tags,
                    type=rtype,
                    file=None,
                    file_url=safe_file_url,
                    thumbnail_url=safe_thumbnail_url,
                    file_size=0,
                    added_at=now_ms(),
                    view_count=view_count,
                    author_name=author_name,
                    source_type=source_type,
                    uploaded_by=effective_uploader,
                    source_url=source_url,
                    source_label=source_label,
                    approval_status=approval_status,
                    reviewed_by=admin_user if approval_status == 'approved' else None,
                    reviewed_at=now_ms() if approval_status == 'approved' else None,
                    upload_group_id='',
                    is_lead=True,
                    is_paid=is_paid,
                    price=price_val,
                )
                resource.save()
                created_count += 1

            cache.delete_many(['home_resources', 'library_all_resources'])
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect': reverse('web:admin_resources')})
            return redirect('web:admin_resources')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        return render(request, 'admin_panel/resource_create.html', {
            'is_admin': True,
            'active_page': 'resources',
            'subjects': subjects,
            'education_levels': education_levels,
            'exam_types': exam_types,
            'pradesh_options': pradesh_options,
            'resource_types': resource_types,
            'common_tags': common_tags,
            'source_types': Resource.SOURCE_TYPES,
            'approval_choices': Resource.APPROVAL_CHOICES,
            'errors': errors,
            'form_data': request.POST,
        })

    return render(request, 'admin_panel/resource_create.html', {
        'is_admin': True,
        'active_page': 'resources',
        'subjects': subjects,
        'education_levels': education_levels,
        'exam_types': exam_types,
        'pradesh_options': pradesh_options,
        'resource_types': resource_types,
        'common_tags': common_tags,
        'source_types': Resource.SOURCE_TYPES,
        'approval_choices': Resource.APPROVAL_CHOICES,
    })

def admin_resource_edit(request, resource_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        resource_obj = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return redirect('web:admin_resources')
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp and path:
                resource_obj.file = path
                resource_obj.file_url = request.build_absolute_uri(settings.MEDIA_URL + path)
                resource_obj.file_size = size
        for field in ['title', 'description', 'subject', 'grade_level', 'faculty', 'program', 'year', 'exam_type', 'pradesh', 'district', 'school', 'tags', 'type', 'author_name', 'source_url', 'source_label']:
            setattr(resource_obj, field, request.POST.get(field, '').strip())
        resource_obj.file_url = request.POST.get('file_url', '').strip()
        resource_obj.thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        st = request.POST.get('source_type', '').strip()
        if st in ('admin', 'user', 'anonymous', 'external'):
            resource_obj.source_type = st
        behalf_username = request.POST.get('behalf_username', '').strip().lstrip('@')
        if behalf_username:
            try:
                resource_obj.uploaded_by = User.objects.get(username__iexact=behalf_username)
                resource_obj.source_type = 'user'
            except User.DoesNotExist:
                pass
        elif request.POST.get('clear_behalf') == '1':
            resource_obj.uploaded_by = None
        if request.POST.get('view_count', '').strip():
            resource_obj.view_count = int(request.POST.get('view_count', '0'))
        # Marketplace: admins can toggle paid + price.
        is_paid = request.POST.get('is_paid') in ['on', 'true', '1', True]
        try:
            price_val = Decimal(request.POST.get('price', '0').strip() or '0')
        except Exception:
            price_val = Decimal('0.00')
        if price_val < 0:
            price_val = Decimal('0.00')
        resource_obj.is_paid = is_paid
        resource_obj.price = price_val if is_paid else Decimal('0.00')
        new_status = request.POST.get('approval_status', '').strip()
        if new_status in ('approved', 'pending', 'rejected'):
            old_status = resource_obj.approval_status
            resource_obj.approval_status = new_status
            resource_obj.reviewed_by = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                try:
                    resource_obj.reviewed_by = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    pass
            resource_obj.reviewed_at = now_ms()
            if new_status == 'rejected':
                resource_obj.rejection_reason = request.POST.get('rejection_reason', '').strip()[:500]
            else:
                resource_obj.rejection_reason = ''
            if old_status == 'pending' and new_status == 'approved' and resource_obj.uploaded_by_id:
                _counters.increment_user_resource_approved(resource_obj.uploaded_by_id)
                _notif.notify_resource_approved(resource_obj.id, resource_obj.uploaded_by_id)
            elif old_status == 'pending' and new_status == 'rejected' and resource_obj.uploaded_by_id:
                _notif.notify_resource_rejected(resource_obj.id, resource_obj.uploaded_by_id, resource_obj.rejection_reason)
        resource_obj.save()
        cache.delete_many(['home_resources', 'library_all_resources'])
        return redirect('web:admin_resources')
    _default_subjects = [
        'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
        'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
        'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
        'Environment Science', 'Science', 'General Science', 'Life Science',
        'Physical Science', 'Earth Science', 'Applied Mathematics',
        'Business Mathematics', 'Statistics', 'Probability',
        'Microeconomics', 'Macroeconomics',
        'Financial Accounting', 'Cost Accounting', 'Auditing',
        'Marketing', 'Office Management', 'Hotel Management',
        'Computer Engineering', 'Electronics', 'Electrical Engineering',
        'Civil Engineering', 'Mechanical Engineering', 'Architecture',
        'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Botany', 'Zoology', 'Genetics', 'Ecology',
        'English Grammar', 'English Literature', 'Creative Writing',
        'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
        'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
        'Education', 'Pedagogy', 'Curriculum Development',
        'Law', 'Constitutional Law', 'International Law',
        'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
        'Agriculture', 'Forestry', 'Veterinary Science',
        'Management', 'Human Resource Management', 'Entrepreneurship',
        'Information Technology', 'Programming', 'Web Development',
        'Database Management', 'Networking', 'Cybersecurity',
        'Machine Learning', 'Artificial Intelligence', 'Data Science',
        'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
        'Digital Logic', 'Operating Systems', 'Software Engineering',
        'Surveying', 'Estimating & Costing', 'Building Construction',
        'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
        'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
    ]
    db_subjects = []
    for s_str in Resource.objects.values_list('subject', flat=True):
        if s_str:
            for s in s_str.split(','):
                s_stripped = s.strip()
                if s_stripped:
                    db_subjects.append(s_stripped)
    subjects = sorted(set(_default_subjects + db_subjects))
    common_tags = [
        'Board Exam', 'SEE', 'Past Paper', 'Model Paper', 'Solution',
        'Important Questions', 'Numerical', 'Derivation', 'Formula Sheet',
        'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5',
        'Chapter 6', 'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10',
        'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5',
        'Class 11', 'Class 12', 'Grade 11', 'Grade 12',
        'Science', 'Management', 'Humanities', 'Education', 'Law',
        'Final Exam', 'Midterm', 'Internal Assessment', 'Practical',
        'Old Course', 'New Course', 'Revised Syllabus', 'Curriculum',
        'Textbook', 'Reference Book', 'Guide', 'Notes', 'Summary',
        'Objective Questions', 'Subjective Questions', 'MCQ', 'Long Answer',
        'Short Answer', 'Very Short Answer', 'Essay Type',
        '2080 BS', '2081 BS', '2082 BS', '2079 BS',
        '2078 BS', '2077 BS', '2076 BS',
        'Kathmandu', 'Pokhara', 'Chitwan', 'Biratnagar', 'Butwal',
        'HSEB', 'TU', 'KU', 'PU', 'CTEVT',
        'Entrance', 'IOE', 'IOM', 'CEEE', 'KUUMAT',
        'C Programming', 'Python', 'Java', 'Web Development',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Mechanics', 'Optics', 'Thermodynamics', 'Electricity',
        'Calculus', 'Algebra', 'Trigonometry', 'Geometry', 'Statistics',
        'Botany', 'Zoology', 'Ecology', 'Genetics',
        'Nepali', 'English', 'Social Studies',
    ]
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    exam_types = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']
    pradesh_options = [
        'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
    ]
    resource_types = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']
    resource_data = ResourceSerializer(resource_obj).data
    resource_data['rejection_reason'] = resource_obj.rejection_reason or ''
    if resource_obj.uploaded_by:
        resource_data['uploaded_by_name'] = resource_obj.uploaded_by.display_name or resource_obj.uploaded_by.username
        resource_data['uploaded_by_username'] = resource_obj.uploaded_by.username
        resource_data['uploaded_by_photo'] = resource_obj.uploaded_by.photo_url or ''
    else:
        resource_data['uploaded_by_name'] = ''
        resource_data['uploaded_by_username'] = ''
        resource_data['uploaded_by_photo'] = ''
    return render(request, 'admin_panel/resource_edit.html', {
        'is_admin': True,
        'resource': resource_data,
        'active_page': 'resources',
        'source_types': Resource.SOURCE_TYPES,
        'approval_choices': Resource.APPROVAL_CHOICES,
        'subjects': subjects,
        'common_tags': common_tags,
        'education_levels': education_levels,
        'exam_types': exam_types,
        'pradesh_options': pradesh_options,
        'resource_types': resource_types,
    })

@require_POST
def admin_resource_delete(request, resource_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        Resource.objects.get(pk=resource_id).delete()
    except Resource.DoesNotExist:
        pass
    return redirect('web:admin_resources')

def _admin_report_target_context(report):
    target = None
    target_url = ''
    admin_url = ''
    public_url = ''
    author_name = ''
    author_id = ''
    summary = ''
    title = ''
    exists = True
    try:
        if report.target_type == 'post':
            target = Post.objects.select_related('user').get(pk=report.target_id)
            title = target.title
            summary = target.content
            author_name = target.user.username if target.user else ''
            author_id = str(target.user_id or '')
            target_url = reverse('web:admin_post_detail', kwargs={'post_id': target.id})
            admin_url = target_url
            public_url = reverse('web:forum_post', kwargs={'post_id': target.id})
        elif report.target_type == 'reply':
            target = Reply.objects.select_related('user', 'post').get(pk=report.target_id)
            title = 'Reply on ' + (target.post.title if target.post else 'forum post')
            summary = target.content
            author_name = target.user.username if target.user else ''
            author_id = str(target.user_id or '')
            target_url = reverse('web:admin_post_detail', kwargs={'post_id': target.post_id})
            admin_url = target_url
            public_url = reverse('web:forum_post', kwargs={'post_id': target.post_id}) + '#reply-' + target.id
        elif report.target_type == 'resource':
            target = Resource.objects.select_related('uploaded_by').get(pk=report.target_id)
            title = target.title
            summary = target.description
            author_name = target.uploaded_by.username if target.uploaded_by else (target.author_name or '')
            author_id = str(target.uploaded_by_id or '')
            target_url = reverse('web:admin_resource_edit', kwargs={'resource_id': target.id})
            admin_url = target_url
            public_url = reverse('web:reader', kwargs={'resource_id': target.id})
        elif report.target_type == 'user':
            target = User.objects.get(pk=report.target_id)
            title = target.display_name or target.username
            summary = target.bio
            author_name = target.username
            author_id = str(target.id)
            target_url = reverse('web:admin_user_detail', kwargs={'user_id': target.id})
            admin_url = target_url
            public_url = reverse('web:profile', kwargs={'username': target.username})
    except Exception:
        exists = False
    return {
        'exists': exists,
        'title': title or report.target_id,
        'summary': (summary or '')[:500],
        'author_name': author_name,
        'author_id': author_id,
        'target_url': target_url,
        'admin_url': admin_url,
        'public_url': public_url,
    }


def admin_reports(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    status_filter = request.GET.get('status', '').strip()
    type_filter = request.GET.get('type', '').strip()
    search = request.GET.get('q', '').strip()
    qs = Report.objects.select_related('reporter', 'resolved_by').all().order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if type_filter:
        qs = qs.filter(target_type=type_filter)
    if search:
        qs = qs.filter(
            Q(id__icontains=search) |
            Q(target_id__icontains=search) |
            Q(description__icontains=search) |
            Q(reporter__username__icontains=search)
        )
    counts = {
        'open': Report.objects.filter(status='open').count(),
        'reviewing': Report.objects.filter(status='reviewing').count(),
        'resolved': Report.objects.filter(status='resolved').count(),
        'dismissed': Report.objects.filter(status='dismissed').count(),
        'total': Report.objects.count(),
    }
    paginator = Paginator(qs, 30)
    page_obj = paginator.get_page(request.GET.get('page'))
    reports = []
    for report in page_obj:
        reports.append({
            'report': report,
            'target': _admin_report_target_context(report),
        })
    return render(request, 'admin_panel/reports.html', {
        'is_admin': True,
        'active_page': 'reports',
        'reports': reports,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search': search,
        'counts': counts,
        'status_choices': Report.STATUS_CHOICES,
        'type_choices': [('post', 'Post'), ('reply', 'Reply'), ('resource', 'Resource'), ('user', 'User')],
    })


def admin_report_detail(request, report_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        report = Report.objects.select_related('reporter', 'resolved_by').get(pk=report_id)
    except Report.DoesNotExist:
        return redirect('web:admin_reports')

    if request.method == 'POST':
        status = request.POST.get('status', '').strip()
        if status in dict(Report.STATUS_CHOICES):
            report.status = status
            if status in ('resolved', 'dismissed'):
                report.resolved_at = now_ms()
                admin_user = None
                if hasattr(request, 'user') and request.user.is_authenticated:
                    try:
                        admin_user = User.objects.get(username=request.user.username)
                    except User.DoesNotExist:
                        admin_user = None
                report.resolved_by = admin_user
            elif status in ('open', 'reviewing'):
                report.resolved_at = 0
                report.resolved_by = None
            report.save()
        return redirect('web:admin_report_detail', report_id=report.id)

    return render(request, 'admin_panel/report_detail.html', {
        'is_admin': True,
        'active_page': 'reports',
        'report': report,
        'target': _admin_report_target_context(report),
        'status_choices': Report.STATUS_CHOICES,
    })

def admin_posts(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    posts_qs = Post.objects.select_related('user').all().order_by('-created_at')
    search = request.GET.get('q', '').strip()
    if search:
        posts_qs = posts_qs.filter(Q(title__icontains=search) | Q(content__icontains=search))
    paginator = Paginator(posts_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    posts_data = [PostSerializer(p, context={}).data for p in page_obj]
    return render(request, 'admin_panel/posts.html', {
        'is_admin': True,
        'posts': posts_data,
        'page_obj': page_obj,
        'search': search,
        'active_page': 'posts',
    })

def admin_post_detail(request, post_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    try:
        post_obj = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        return redirect('web:admin_posts')
    post_data = PostSerializer(post_obj, context={}).data
    replies_qs = Reply.objects.filter(post_id=post_id).select_related('user')
    replies_data = [ReplySerializer(r, context={}).data for r in replies_qs]
    from api.models import PostView
    viewers_qs = PostView.objects.filter(post_id=post_id).select_related('user').order_by('-viewed_at')[:50]
    viewers = [
        {
            'userId': v.user_id,
            'username': v.user.username,
            'displayName': v.user.display_name,
            'photoUrl': v.user.photo_url or '',
            'viewedAt': v.viewed_at,
        }
        for v in viewers_qs
    ]
    viewer_count = PostView.objects.filter(post_id=post_id).count()
    return render(request, 'admin_panel/post_detail.html', {
        'is_admin': True,
        'post': post_data,
        'replies': replies_data,
        'viewers': viewers,
        'viewer_count': viewer_count,
        'active_page': 'posts',
    })

@require_POST
def admin_post_delete(request, post_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.cleanup import delete_post_with_cleanup
    try:
        delete_post_with_cleanup(post_id)
    except Post.DoesNotExist:
        pass
    return redirect('web:admin_posts')

@require_POST
def admin_reply_delete(request, reply_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.cleanup import delete_reply_with_cleanup
    try:
        delete_reply_with_cleanup(reply_id)
    except Reply.DoesNotExist:
        pass
    return redirect('web:admin_posts')

def admin_bots(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    bots = BotConfig.objects.all().order_by('id')
    bot_list = []
    for bot in bots:
        bot_user = BotConfig.get_bot_user(bot)
        task_stats = {
            'pending': bot.tasks.filter(status='pending').count(),
            'processing': bot.tasks.filter(status='processing').count(),
            'done': bot.tasks.filter(status='done').count(),
            'failed': bot.tasks.filter(status='failed').count(),
        }
        bot_list.append({
            'config': bot,
            'user': bot_user,
            'task_stats': task_stats,
        })
    ctx = _ctx(request, active_page='bot', bot_list=bot_list)
    return render(request, 'admin_panel/bot_list.html', ctx)

def admin_bot_edit(request, bot_id=None):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig
    if bot_id:
        config = BotConfig.objects.filter(pk=bot_id).first()
        if not config:
            messages.error(request, 'Bot not found.')
            return redirect('/admin/bots/')
    else:
        config = None

    if request.method == 'POST':
        action = request.POST.get('action', 'save')
        if action == 'delete' and config:
            bot_username = config.bot_username
            config.delete()
            from django.core.cache import cache
            cache.delete('neby_enabled')
            messages.success(request, f'Bot @{bot_username} deleted.')
            return redirect('/admin/bots/')
        if not config:
            config = BotConfig()
        config.enabled = request.POST.get('enabled') == 'on'
        config.name = request.POST.get('name', config.name or 'Neby').strip()[:100] or 'Neby'
        config.bot_username = request.POST.get('bot_username', config.bot_username or 'neby').strip()[:50].lower() or 'neby'
        config.display_name = request.POST.get('display_name', '').strip()[:100]
        config.avatar_url = request.POST.get('avatar_url', '').strip()
        provider = (request.POST.get('provider') or 'qwen').strip().lower()
        from api.llm.registry import ALL_PRESETS
        allowed_providers = set(ALL_PRESETS.keys()) | {'custom'}
        if provider not in allowed_providers:
            provider = 'qwen'
        config.provider = provider
        config.api_url = request.POST.get('api_url', config.api_url).strip()
        config.api_key = request.POST.get('api_key', config.api_key).strip()
        model = (request.POST.get('model') or '').strip()
        if not model:
            model = (request.POST.get('model_select') or request.POST.get('model_text') or '').strip()
        if model:
            config.model = model[:200]
        elif not config.model:
            config.model = 'qwen3.8-max'
        try:
            raw_chain = json.loads(request.POST.get('fallback_chain') or '[]')
            if not isinstance(raw_chain, list):
                raw_chain = []
        except (ValueError, TypeError):
            raw_chain = []
        chain_allowed = allowed_providers
        clean_chain = []
        for entry in raw_chain[:5]:
            if not isinstance(entry, dict):
                continue
            provider = (entry.get('provider') or '').strip().lower()
            if provider not in chain_allowed:
                continue
            clean_chain.append({
                'provider': provider,
                'model': (entry.get('model') or '').strip()[:200],
                'api_url': (entry.get('api_url') or '').strip()[:2000],
                'api_key': (entry.get('api_key') or '').strip()[:2000],
            })
        config.fallback_chain = json.dumps(clean_chain, ensure_ascii=False)
        config.system_prompt = request.POST.get('system_prompt', config.system_prompt).strip()
        try:
            config.max_context_posts = int(request.POST.get('max_context_posts', config.max_context_posts))
        except (TypeError, ValueError):
            pass
        try:
            config.max_context_replies = int(request.POST.get('max_context_replies', config.max_context_replies))
        except (TypeError, ValueError):
            pass
        try:
            config.response_max_length = int(request.POST.get('response_max_length', config.response_max_length))
        except (TypeError, ValueError):
            pass
        # Validate bot_username uniqueness
        existing = BotConfig.objects.filter(bot_username__iexact=config.bot_username).exclude(pk=config.pk)
        if existing.exists():
            messages.error(request, f'A bot with username @{config.bot_username} already exists.')
            bot_user = BotConfig.get_bot_user(config) if config.pk else None
            ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user, is_new=not config.pk,
                       **_bot_provider_catalog_ctx())
            return render(request, 'admin_panel/bot_edit.html', ctx)
        config.save()
        from django.core.cache import cache
        cache.delete('neby_enabled')
        bot_user = BotConfig.get_bot_user(config)
        if bot_user:
            from api.agent_social.ensure import ensure_persona
            persona, _ = ensure_persona(
                config, bot_user,
                autonomy_enabled=request.POST.get('autonomy_enabled') == 'on',
                apply_neby_defaults=config.bot_username.lower() == 'neby',
            )
            persona.tagline = (request.POST.get('tagline') or '')[:200]
            persona.origin_story = (request.POST.get('origin_story') or '')[:4000]
            persona.voice_notes = (request.POST.get('voice_notes') or '')[:4000]
            goals_raw = (request.POST.get('goals_text') or '').strip()
            if goals_raw:
                persona.goals = [ln.strip('-• ').strip() for ln in goals_raw.splitlines() if ln.strip()]
            persona.autonomy_enabled = request.POST.get('autonomy_enabled') == 'on'
            try:
                persona.tick_interval_minutes = max(int(request.POST.get('tick_interval_minutes') or persona.tick_interval_minutes), 1)
            except (TypeError, ValueError):
                pass
            try:
                persona.max_posts_per_day = max(int(request.POST.get('max_posts_per_day') or persona.max_posts_per_day), 0)
            except (TypeError, ValueError):
                pass
            persona.save()
        messages.success(request, f'Bot "@{config.bot_username}" saved. Provider: {provider}.')
        return redirect(f'/admin/bots/{config.pk}/')

    bot_user = BotConfig.get_bot_user(config) if config else None
    persona = None
    if config:
        from api.agent_social.models import AgentPersona
        persona = AgentPersona.objects.filter(bot_config=config).first()
    ctx = _ctx(request, active_page='bot', config=config, bot_user=bot_user, is_new=config is None,
               persona=persona, goals_text='\n'.join((persona.goals if persona else [])),
               **_bot_provider_catalog_ctx())
    return render(request, 'admin_panel/bot_edit.html', ctx)


def _bot_provider_catalog_ctx():
    """Registry-driven provider catalog for the bot editor UI."""
    import json as _json
    from api.llm.registry import admin_catalog
    catalog = admin_catalog()
    scraper_options = [{'slug': e['slug'], 'label': e['label']} for e in catalog['scrapers']]
    official_options = [{'slug': e['slug'], 'label': e['label']} for e in catalog['official']]
    provider_config = {}
    for entry in catalog['scrapers'] + catalog['official']:
        provider_config[entry['slug']] = {
            'urlLabel': 'API URL',
            'urlHelp': f"{entry['label']} endpoint (leave default).",
            'urlDefault': entry['base_url'],
            'modelControl': 'select' if entry['models'] else 'text',
            'modelHelp': f"Pick a model (default: {entry['default_model']}).",
            'options': [{'value': m['id'], 'label': m['label']} for m in entry['models']],
        }
    provider_config['custom'] = {
        'urlLabel': 'API URL',
        'urlHelp': 'Full URL to any OpenAI-compatible /chat/completions endpoint.',
        'urlDefault': '',
        'modelControl': 'text',
        'modelHelp': 'Free-form model name as required by the provider.',
        'options': [],
    }
    return {
        'provider_options_scrapers': scraper_options,
        'provider_options_official': official_options,
        'provider_config_json': _json.dumps(provider_config),
    }

def admin_bot_create_user(request, bot_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.models import BotConfig, User
    config = get_object_or_404(BotConfig, pk=bot_id)
    if request.method == 'POST':
        username = config.bot_username
        display_name = request.POST.get('display_name') or config.display_name or config.name
        try:
            bot_user = User.objects.create(
                id=f'{username}-bot',
                username=username,
                display_name=display_name,
                is_bot=True,
                email_verified=True,
                created_at=now_ms(),
            )
            messages.success(request, f'Created bot user @{username} (id={bot_user.id}).')
        except Exception as e:
            messages.error(request, f'Failed to create bot user: {e}')
        return redirect(f'/admin/bots/{bot_id}/')
    ctx = _ctx(request, active_page='bot', config=config)
    return render(request, 'admin_panel/bot_create_user.html', ctx)


def admin_agent_activity(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    from api.agent_social.models import AgentAction
    actions = list(
        AgentAction.objects.select_related('persona', 'persona__bot_config').order_by('-created_at')[:120]
    )
    return render(request, 'admin_panel/agent_activity.html', _ctx(
        request, active_page='bot', recent_actions=actions,
    ))


def admin_agent_tick(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    if request.method != 'POST':
        return redirect('/admin/agents/activity/')
    from api.agent_social.heartbeat import tick_neby
    result = tick_neby(force=True, source='admin')
    messages.success(request, f'Heartbeat: {result}')
    return redirect('/admin/agents/activity/')

def admin_syllabus_list(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    
    from api.models import SyllabusContent
    syllabus_qs = SyllabusContent.objects.all().order_by('grade_level', 'subject', 'order')
    
    search = request.GET.get('q', '').strip()
    filter_grade = request.GET.get('grade', '').strip()
    filter_subject = request.GET.get('subject', '').strip()
    
    if search:
        syllabus_qs = syllabus_qs.filter(
            Q(grade_level__icontains=search) | 
            Q(subject__icontains=search) | 
            Q(chapter_title__icontains=search)
        )
    if filter_grade:
        syllabus_qs = syllabus_qs.filter(grade_level=filter_grade)
    if filter_subject:
        syllabus_qs = syllabus_qs.filter(subject__iexact=filter_subject)
    
    all_grades = list(SyllabusContent.objects.order_by('grade_level').values_list('grade_level', flat=True).distinct())
    all_subjects = list(SyllabusContent.objects.order_by('subject').values_list('subject', flat=True).distinct())
    total_count = SyllabusContent.objects.count()
    
    paginator = Paginator(syllabus_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/syllabus_list.html', {
        'is_admin': True,
        'page_obj': page_obj,
        'search': search,
        'filter_grade': filter_grade,
        'filter_subject': filter_subject,
        'all_grades': all_grades,
        'all_subjects': all_subjects,
        'total_count': total_count,
        'active_page': 'syllabus',
    })

def admin_syllabus_create(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    import uuid
    import time
    
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    
    grade_subjects = {
        'Class 8': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education'],
        'Class 9': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education', 'Account'],
        'Class 10 / SEE': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education', 'Account', 'Optional Mathematics'],
        'Class 11': ['English', 'Nepali', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Account', 'Economics', 'Business Studies', 'Business Mathematics', 'Hotel Management', 'Sociology', 'Mass Communication', 'Psychology', 'Education', 'Health & Physical Education'],
        'Class 12': ['English', 'Nepali', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Account', 'Economics', 'Business Studies', 'Business Mathematics', 'Hotel Management', 'Sociology', 'Mass Communication', 'Psychology', 'Education', 'Health & Physical Education'],
        'Diploma': ['Computer Engineering', 'Civil Engineering', 'Electrical Engineering', 'Electronics Engineering', 'Architecture', 'Mechanical Engineering', 'Pharmacy'],
        'Bachelor': ['Computer Science', 'Business Administration', 'Engineering', 'Medicine', 'Law', 'Education', 'Management', 'Humanities'],
        'Master': ['Computer Science', 'Business Administration', 'Engineering', 'Education', 'Management'],
        'PhD': ['Science', 'Engineering', 'Humanities', 'Management', 'Education'],
        'Entrance Prep': ['IIT JEE', 'NEET', 'CMAT', 'IOE Entrance', 'CEE Medical', 'Lok Sewa Aayog', 'Public Service Commission'],
        'Competitive Exam': ['Lok Sewa Aayog', 'Bank Exam', 'Nepal Police', 'Armed Police', 'Teacher Service Commission', 'Public Service Commission'],
        'Other': [],
    }
    
    existing_subjects = list(SyllabusContent.objects.order_by('subject').values_list('subject', flat=True).distinct())
    existing_ids = list(SyllabusContent.objects.values_list('chapter_id', flat=True))
    grade_subjects_json = json.dumps(grade_subjects)
    existing_ids_json = json.dumps(existing_ids)
    
    if request.method == 'POST':
        grade_level = request.POST.get('grade_level', '').strip()
        subject = request.POST.get('subject', '').strip()
        chapter_title = request.POST.get('chapter_title', '').strip()
        chapter_id = request.POST.get('chapter_id', '').strip()
        text_content = request.POST.get('text_content', '').strip()
        question_answers = request.POST.get('question_answers', '').strip()
        order_val = request.POST.get('order', '0').strip()
        
        if not grade_level or not subject or not chapter_title or not chapter_id:
            return render(request, 'admin_panel/syllabus_form.html', {
                'is_admin': True,
                'education_levels': education_levels,
                'grade_subjects_json': grade_subjects_json,
                'existing_subjects': existing_subjects,
                'existing_ids_json': existing_ids_json,
                'active_page': 'syllabus',
                'is_edit': False,
                'form_error': 'All required fields (Level, Subject, Chapter Title, Chapter ID) must be filled.',
                'form_data': request.POST,
            })
            
        if chapter_id in existing_ids:
            return render(request, 'admin_panel/syllabus_form.html', {
                'is_admin': True,
                'education_levels': education_levels,
                'grade_subjects_json': grade_subjects_json,
                'existing_subjects': existing_subjects,
                'existing_ids_json': existing_ids_json,
                'active_page': 'syllabus',
                'is_edit': False,
                'form_error': 'Chapter ID "{}" already exists. Please use a unique identifier.'.format(chapter_id),
                'form_data': request.POST,
            })
            
        _now = now_ms()
        try:
            order = int(order_val)
        except ValueError:
            order = 0
            
        syllabus_obj = SyllabusContent(
            id=uuid_str(),
            grade_level=grade_level,
            subject=subject,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            text_content=text_content,
            question_answers=question_answers,
            order=order,
            created_at=_now,
            updated_at=_now
        )
        syllabus_obj.save()
        return redirect('web:admin_syllabus_list')
        
    return render(request, 'admin_panel/syllabus_form.html', {
        'is_admin': True,
        'education_levels': education_levels,
        'grade_subjects_json': grade_subjects_json,
        'existing_subjects': existing_subjects,
        'existing_ids_json': existing_ids_json,
        'active_page': 'syllabus',
        'is_edit': False,
    })

def admin_syllabus_edit(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    import time
    
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    
    grade_subjects = {
        'Class 8': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education'],
        'Class 9': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education', 'Account'],
        'Class 10 / SEE': ['English', 'Nepali', 'Mathematics', 'Science', 'Social Studies', 'Health & Physical Education', 'Account', 'Optional Mathematics'],
        'Class 11': ['English', 'Nepali', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Account', 'Economics', 'Business Studies', 'Business Mathematics', 'Hotel Management', 'Sociology', 'Mass Communication', 'Psychology', 'Education', 'Health & Physical Education'],
        'Class 12': ['English', 'Nepali', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Account', 'Economics', 'Business Studies', 'Business Mathematics', 'Hotel Management', 'Sociology', 'Mass Communication', 'Psychology', 'Education', 'Health & Physical Education'],
        'Diploma': ['Computer Engineering', 'Civil Engineering', 'Electrical Engineering', 'Electronics Engineering', 'Architecture', 'Mechanical Engineering', 'Pharmacy'],
        'Bachelor': ['Computer Science', 'Business Administration', 'Engineering', 'Medicine', 'Law', 'Education', 'Management', 'Humanities'],
        'Master': ['Computer Science', 'Business Administration', 'Engineering', 'Education', 'Management'],
        'PhD': ['Science', 'Engineering', 'Humanities', 'Management', 'Education'],
        'Entrance Prep': ['IIT JEE', 'NEET', 'CMAT', 'IOE Entrance', 'CEE Medical', 'Lok Sewa Aayog', 'Public Service Commission'],
        'Competitive Exam': ['Lok Sewa Aayog', 'Bank Exam', 'Nepal Police', 'Armed Police', 'Teacher Service Commission', 'Public Service Commission'],
        'Other': [],
    }
    
    existing_subjects = list(SyllabusContent.objects.order_by('subject').values_list('subject', flat=True).distinct())
    existing_ids = list(SyllabusContent.objects.exclude(pk=entry_id).values_list('chapter_id', flat=True))
    grade_subjects_json = json.dumps(grade_subjects)
    existing_ids_json = json.dumps(existing_ids)
    
    if request.method == 'POST':
        grade_level = request.POST.get('grade_level', '').strip()
        subject = request.POST.get('subject', '').strip()
        chapter_title = request.POST.get('chapter_title', '').strip()
        chapter_id = request.POST.get('chapter_id', '').strip()
        text_content = request.POST.get('text_content', '').strip()
        question_answers = request.POST.get('question_answers', '').strip()
        order_val = request.POST.get('order', '0').strip()
        
        if not grade_level or not subject or not chapter_title or not chapter_id:
            return render(request, 'admin_panel/syllabus_form.html', {
                'is_admin': True,
                'syllabus': syllabus_obj,
                'education_levels': education_levels,
                'grade_subjects_json': grade_subjects_json,
                'existing_subjects': existing_subjects,
                'existing_ids_json': existing_ids_json,
                'active_page': 'syllabus',
                'is_edit': True,
                'form_error': 'All required fields (Level, Subject, Chapter Title, Chapter ID) must be filled.',
            })
            
        if chapter_id in existing_ids:
            return render(request, 'admin_panel/syllabus_form.html', {
                'is_admin': True,
                'syllabus': syllabus_obj,
                'education_levels': education_levels,
                'grade_subjects_json': grade_subjects_json,
                'existing_subjects': existing_subjects,
                'existing_ids_json': existing_ids_json,
                'active_page': 'syllabus',
                'is_edit': True,
                'form_error': 'Chapter ID "{}" already exists. Please use a unique identifier.'.format(chapter_id),
            })
            
        try:
            order = int(order_val)
        except ValueError:
            order = 0
            
        syllabus_obj.grade_level = grade_level
        syllabus_obj.subject = subject
        syllabus_obj.chapter_title = chapter_title
        syllabus_obj.chapter_id = chapter_id
        syllabus_obj.text_content = text_content
        syllabus_obj.question_answers = question_answers
        syllabus_obj.order = order
        syllabus_obj.updated_at = now_ms()
        syllabus_obj.save()
        return redirect('web:admin_syllabus_list')
        
    return render(request, 'admin_panel/syllabus_form.html', {
        'is_admin': True,
        'syllabus': syllabus_obj,
        'education_levels': education_levels,
        'grade_subjects_json': grade_subjects_json,
        'existing_subjects': existing_subjects,
        'existing_ids_json': existing_ids_json,
        'active_page': 'syllabus',
        'is_edit': True,
    })

def admin_syllabus_delete(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    if request.method == 'POST':
        syllabus_obj.delete()
        
    return redirect('web:admin_syllabus_list')

def admin_syllabus_preview(request, entry_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    try:
        syllabus_obj = SyllabusContent.objects.get(pk=entry_id)
    except SyllabusContent.DoesNotExist:
        return redirect('web:admin_syllabus_list')
        
    siblings = SyllabusContent.objects.filter(
        grade_level=syllabus_obj.grade_level,
        subject=syllabus_obj.subject
    ).order_by('order', 'chapter_title')
    
    return render(request, 'admin_panel/syllabus_preview.html', {
        'is_admin': True,
        'syllabus': syllabus_obj,
        'siblings': siblings,
        'active_page': 'syllabus',
    })

def admin_syllabus_import(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    import uuid
    
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    
    import_result = None
    
    if request.method == 'POST':
        json_data = request.POST.get('json_data', '').strip()
        overwrite = request.POST.get('overwrite', '') == 'on'
        
        if not json_data:
            import_result = {'success': False, 'message': 'No JSON data provided.'}
        else:
            try:
                data = json.loads(json_data)
                if isinstance(data, dict):
                    data = [data]
                if not isinstance(data, list):
                    import_result = {'success': False, 'message': 'JSON must be an array of chapter objects (or a single object).'}
                else:
                    created = 0
                    updated = 0
                    skipped = 0
                    errors = []
                    _now = now_ms()
                    
                    for i, item in enumerate(data):
                        grade = str(item.get('grade_level', '')).strip()
                        subject = str(item.get('subject', '')).strip()
                        title = str(item.get('chapter_title', '')).strip()
                        slug = str(item.get('chapter_id', item.get('slug', ''))).strip()
                        
                        if not grade or not subject or not title:
                            errors.append('Row {}: Missing required field (grade_level, subject, or chapter_title).'.format(i + 1))
                            skipped += 1
                            continue
                        if not slug:
                            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                        
                        content = str(item.get('text_content', '')).strip()
                        qa = str(item.get('question_answers', '')).strip()
                        order = int(item.get('order', 0))
                        
                        if overwrite:
                            existing = SyllabusContent.objects.filter(chapter_id=slug).first()
                            if existing:
                                existing.grade_level = grade
                                existing.subject = subject
                                existing.chapter_title = title
                                existing.text_content = content
                                existing.question_answers = qa
                                existing.order = order
                                existing.updated_at = _now
                                existing.save()
                                updated += 1
                                continue
                        
                        obj, created_flag = SyllabusContent.objects.get_or_create(
                            chapter_id=slug,
                            defaults={
                                'id': uuid_str(),
                                'grade_level': grade,
                                'subject': subject,
                                'chapter_title': title,
                                'text_content': content,
                                'question_answers': qa,
                                'order': order,
                                'created_at': _now,
                                'updated_at': _now,
                            }
                        )
                        if created_flag:
                            created += 1
                        else:
                            if overwrite:
                                obj.grade_level = grade
                                obj.subject = subject
                                obj.chapter_title = title
                                obj.text_content = content
                                obj.question_answers = qa
                                obj.order = order
                                obj.updated_at = _now
                                obj.save()
                                updated += 1
                            else:
                                skipped += 1
                                errors.append('Row {}: chapter_id "{}" already exists. Use overwrite to update.'.format(i + 1, slug))
                    
                    import_result = {
                        'success': True,
                        'created': created,
                        'updated': updated,
                        'skipped': skipped,
                        'errors': errors,
                        'total': len(data),
                        'message': 'Imported {} of {} chapters ({} created, {} updated, {} skipped).'.format(
                            created + updated, len(data), created, updated, skipped
                        ),
                    }
            except json.JSONDecodeError as e:
                import_result = {'success': False, 'message': 'Invalid JSON: {}'.format(str(e))}
    
    return render(request, 'admin_panel/syllabus_import.html', {
        'is_admin': True,
        'education_levels': education_levels,
        'import_result': import_result,
        'active_page': 'syllabus',
    })

def admin_syllabus_export(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
        
    from api.models import SyllabusContent
    
    grade = request.GET.get('grade', '').strip()
    subject = request.GET.get('subject', '').strip()
    
    qs = SyllabusContent.objects.all().order_by('grade_level', 'subject', 'order')
    if grade:
        qs = qs.filter(grade_level=grade)
    if subject:
        qs = qs.filter(subject__iexact=subject)
    
    data = []
    for item in qs:
        data.append({
            'grade_level': item.grade_level,
            'subject': item.subject,
            'chapter_id': item.chapter_id,
            'chapter_title': item.chapter_title,
            'text_content': item.text_content,
            'question_answers': item.question_answers,
            'order': item.order,
        })
    
    response = JsonResponse(data, safe=False, json_dumps_params={'indent': 2, 'ensure_ascii': False})
    response['Content-Disposition'] = 'attachment; filename="syllabus_export.json"'
    return response


# ==================== Study Spaces Admin ====================

def admin_study_spaces(request):
    """Admin: list all study spaces with stats, allow deletion."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    from api.models import StudySpace, StudyDocument

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        space_id = request.POST.get('space_id', '').strip()
        if action == 'delete' and space_id:
            try:
                StudySpace.objects.filter(id=space_id).delete()
            except Exception:
                pass
        return redirect('web:admin_study_spaces')

    search = request.GET.get('q', '').strip()
    spaces_qs = StudySpace.objects.select_related('user').order_by('-created_at')
    if search:
        spaces_qs = spaces_qs.filter(
            Q(title__icontains=search) |
            Q(user__username__icontains=search)
        )

    total_spaces = StudySpace.objects.count()
    total_documents = StudyDocument.objects.count()
    public_spaces = StudySpace.objects.filter(visibility='public').count()

    spaces = []
    for sp in spaces_qs[:100]:
        doc_count = sp.documents.count()
        member_count = sp.members.count()
        spaces.append({
            'id': sp.id,
            'name': sp.title,
            'owner': sp.user,
            'visibility': sp.visibility,
            'doc_count': doc_count,
            'member_count': member_count,
            'created_at': sp.created_at,
        })

    return render(request, 'admin_panel/study_spaces.html', {
        'is_admin': True,
        'active_page': 'study_spaces',
        'spaces': spaces,
        'search': search,
        'total_spaces': total_spaces,
        'total_documents': total_documents,
        'public_spaces': public_spaces,
    })


def admin_study_space_delete(request, space_id):
    """Admin: delete a single study space."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    from api.models import StudySpace
    if request.method == 'POST':
        StudySpace.objects.filter(id=space_id).delete()
    return redirect('web:admin_study_spaces')


def admin_deletions(request):
    """Admin view to list pending account deletion requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    from api.models import AccountDeletionRequest
    pending_requests = AccountDeletionRequest.objects.filter(status=AccountDeletionRequest.STATUS_PENDING).select_related('user').order_by('-created_at')

    return render(request, 'admin_panel/deletions.html', {
        'is_admin': True,
        'active_page': 'deletions',
        'pending_requests': pending_requests,
    })


def admin_process_deletion(request, request_id):
    """Admin view to execute (delete data) or reject/cancel a deletion request."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method != 'POST':
        return redirect('web:admin_deletions')

    from api.models import AccountDeletionRequest
    from api.services import delete_user_account

    try:
        del_request = AccountDeletionRequest.objects.get(pk=request_id)
    except AccountDeletionRequest.DoesNotExist:
        return redirect('web:admin_deletions')

    action = request.POST.get('action', '').strip()
    admin_user = getattr(request, 'user', None)

    if action == 'delete':
        # Execute the deletion service
        delete_user_account(del_request.user_id, completed_by=admin_user)
    elif action == 'reject':
        # Just delete the request so user is not deleted
        del_request.delete()

    return redirect('web:admin_deletions')


def admin_push_notifications(request):
    """Admin page to filter users and send targeted push notifications."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    import datetime
    from django.db.models import Q
    from django.http import JsonResponse
    from api.models import User, FCMToken

    # Parse parameters
    class_level = request.POST.get('class_level', '').strip() if request.method == 'POST' else request.GET.get('class_level', '').strip()
    gender = request.POST.get('gender', '').strip() if request.method == 'POST' else request.GET.get('gender', '').strip()
    min_age = request.POST.get('min_age', '').strip() if request.method == 'POST' else request.GET.get('min_age', '').strip()
    max_age = request.POST.get('max_age', '').strip() if request.method == 'POST' else request.GET.get('max_age', '').strip()
    pradesh = request.POST.get('pradesh', '').strip() if request.method == 'POST' else request.GET.get('pradesh', '').strip()
    district = request.POST.get('district', '').strip() if request.method == 'POST' else request.GET.get('district', '').strip()
    school = request.POST.get('school', '').strip() if request.method == 'POST' else request.GET.get('school', '').strip()
    usernames_or_ids = request.POST.get('usernames_or_ids', '').strip() if request.method == 'POST' else request.GET.get('usernames_or_ids', '').strip()

    title = request.POST.get('title', '').strip()
    body = request.POST.get('body', '').strip()

    # Build matching users query
    user_qs = User.objects.filter(is_bot=False)

    if class_level:
        user_qs = user_qs.filter(class_level__iexact=class_level)
    if gender:
        user_qs = user_qs.filter(gender__iexact=gender)
    if pradesh:
        user_qs = user_qs.filter(pradesh__icontains=pradesh)
    if district:
        user_qs = user_qs.filter(district__icontains=district)
    if school:
        user_qs = user_qs.filter(school__icontains=school)

    today = datetime.date.today()
    if min_age:
        try:
            min_age_val = int(min_age)
            limit_year = today.year - min_age_val
            dob_limit = f"{limit_year:04d}-{today.month:02d}-{today.day:02d}"
            user_qs = user_qs.filter(dob__lte=dob_limit).exclude(dob='')
        except ValueError:
            pass

    if max_age:
        try:
            max_age_val = int(max_age)
            limit_year = today.year - max_age_val - 1
            dob_limit = f"{limit_year:04d}-{today.month:02d}-{today.day:02d}"
            user_qs = user_qs.filter(dob__gte=dob_limit).exclude(dob='')
        except ValueError:
            pass

    if usernames_or_ids:
        items = [x.strip() for x in usernames_or_ids.split(',') if x.strip()]
        if items:
            user_qs = user_qs.filter(Q(username__in=items) | Q(id__in=items))

    matching_users_count = user_qs.count()
    matching_tokens_count = FCMToken.objects.filter(user__in=user_qs).count()

    # AJAX counter request
    if request.GET.get('count_only') == '1' or (request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET'):
        return JsonResponse({
            'matching_users': matching_users_count,
            'matching_tokens': matching_tokens_count,
        })

    success_message = None
    error_message = None

    if request.method == 'POST':
        if not title or not body:
            error_message = "Title and message body are required."
        else:
            tokens = list(FCMToken.objects.filter(user__in=user_qs).values_list('token', flat=True))
            if not tokens:
                error_message = f"No active devices/FCM tokens registered for the matching {matching_users_count} users."
            else:
                from api.fcm_utils import send_fcm_message
                send_fcm_message(
                    tokens=tokens,
                    title=title,
                    body=body,
                    data={
                        'verb': 'system',
                        'target_type': 'broadcast',
                        'target_id': '',
                    }
                )
                success_message = f"Successfully queued notification to {len(tokens)} active devices of {matching_users_count} targeted users."
                # Clear fields on success
                title = ""
                body = ""

    return render(request, 'admin_panel/push_notifications.html', {
        'is_admin': True,
        'active_page': 'push_notifications',
        'matching_users': matching_users_count,
        'matching_tokens': matching_tokens_count,
        'success_message': success_message,
        'error_message': error_message,
        'class_level': class_level,
        'gender': gender,
        'min_age': min_age,
        'max_age': max_age,
        'pradesh': pradesh,
        'district': district,
        'school': school,
        'usernames_or_ids': usernames_or_ids,
        'title_val': title,
        'body_val': body,
    })

# ─── Analytics ──────────────────────────────────────────────────────────────

def admin_analytics(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    import re as _re
    from datetime import datetime, timedelta
    from django.db.models import Count
    from django.core.cache import cache
    from api.models import PageView, DailyStat, User as UserModel
    from api import views_presence
    _now = now_ms()
    _today_start = _now - (_now % 86400000)
    _yesterday_start = _today_start - 86400000

    # ── Parse optional date range from query params ──
    date_from_str = request.GET.get('from', '').strip()
    date_to_str = request.GET.get('to', '').strip()
    is_custom_range = bool(date_from_str and date_to_str)
    if is_custom_range:
        try:
            dt_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            dt_to = datetime.strptime(date_to_str, '%Y-%m-%d')
            if dt_from > dt_to:
                dt_from, dt_to = dt_to, dt_from
            dt_to = dt_to + timedelta(days=1)  # inclusive end
            _range_start = int(dt_from.timestamp() * 1000)
            _range_end = int(dt_to.timestamp() * 1000)
            range_label = f'{dt_from.strftime("%b %d, %Y")} — {date_to_str}'
        except ValueError:
            is_custom_range = False
            _range_start = _today_start - 30 * 86400000
            _range_end = _today_start
            range_label = 'Last 30 Days'
    else:
        _range_start = _today_start - 30 * 86400000
        _range_end = _today_start
        range_label = 'Last 30 Days'

    _30d_ago = _today_start - 30 * 86400000

    # ── Today ──
    qs_today = PageView.objects.filter(created_at__gte=_today_start)
    today_visits = qs_today.count()
    today_unique = qs_today.values('session_key').distinct().count() if today_visits else 0
    today_new_users = UserModel.objects.filter(created_at__gte=_today_start).count()
    today_web = qs_today.filter(source='web').count()
    today_app = qs_today.filter(source='app').count()

    # ── Yesterday ──
    qs_yesterday = PageView.objects.filter(created_at__gte=_yesterday_start, created_at__lt=_today_start)
    yesterday_visits = qs_yesterday.count()

    # ── Range / today snapshot ──
    qs_range = PageView.objects.filter(created_at__gte=_range_start, created_at__lt=_range_end)
    range_visits = qs_range.count()
    range_unique = qs_range.values('session_key').distinct().count() if range_visits else 0
    range_web = qs_range.filter(source='web').count()
    range_app = qs_range.filter(source='app').count()

    # ── Session metrics (range) ──
    session_data_range = list(
        qs_range.values('session_key')
                .annotate(pages=Count('id'))
                .order_by()
    )
    range_sessions = len(session_data_range)
    range_bounce_count = sum(1 for s in session_data_range if s['pages'] == 1) if session_data_range else 0
    range_pages = sum(s['pages'] for s in session_data_range) if session_data_range else 0
    range_pages_per_session = round(range_pages / range_sessions, 1) if range_sessions else 0.0
    range_bounce_rate = round((range_bounce_count / range_sessions) * 100, 1) if range_sessions else 0.0

    range_days_count = max(1, (_range_end - _range_start) // 86400000)

    # ── Daily trend over range ──
    valid_days = []
    for i in range(range_days_count - 1, -1, -1):
        ds = _range_end - (i + 1) * 86400000
        if ds < _range_start:
            continue
        valid_days.append(ds)

    K = len(valid_days)
    if K > 0:
        ds_first = valid_days[0]
        total_span = K * 86400000
        from datetime import datetime as dtfmt
        day_labels = [dtfmt.utcfromtimestamp(ds / 1000).strftime('%a %m/%d') for ds in valid_days]

        pv_timestamps = list(PageView.objects.filter(created_at__gte=ds_first, created_at__lt=_range_end).values_list('created_at', flat=True))
        user_timestamps = list(UserModel.objects.filter(created_at__gte=ds_first, created_at__lt=_range_end).values_list('created_at', flat=True))
        post_timestamps = list(Post.objects.filter(created_at__gte=ds_first, created_at__lt=_range_end).values_list('created_at', flat=True))
        res_timestamps = list(Resource.objects.filter(added_at__gte=ds_first, added_at__lt=_range_end).values_list('added_at', flat=True))

        day_visits = [0] * K
        hourly_visits = [0] * 24
        for ts in pv_timestamps:
            offset = ts - ds_first
            if 0 <= offset < total_span:
                day_visits[int(offset // 86400000)] += 1
                hourly_visits[int((offset % 86400000) // 3600000)] += 1

        day_users = [0] * K
        for ts in user_timestamps:
            offset = ts - ds_first
            if 0 <= offset < total_span:
                day_users[int(offset // 86400000)] += 1

        day_posts = [0] * K
        for ts in post_timestamps:
            offset = ts - ds_first
            if 0 <= offset < total_span:
                day_posts[int(offset // 86400000)] += 1

        day_resources = [0] * K
        for ts in res_timestamps:
            offset = ts - ds_first
            if 0 <= offset < total_span:
                day_resources[int(offset // 86400000)] += 1

        hourly_labels = [f'{h:02d}:00' for h in range(24)]

        dow_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        dow_data = [0] * 7
        for k, ds in enumerate(valid_days):
            dow = dtfmt.utcfromtimestamp(ds / 1000).weekday()
            dow_data[dow] += day_visits[k]
    else:
        day_labels = []
        day_visits = []
        day_users = []
        day_posts = []
        day_resources = []
        hourly_labels = [f'{h:02d}:00' for h in range(24)]
        hourly_visits = [0] * 24
        dow_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        dow_data = [0] * 7

    # ── Peak hours (aggregated over range) ──
    peak_hour_labels = hourly_labels[:]
    peak_hour_data = hourly_visits[:]

    # ── Source breakdown (range) ──
    source_web = qs_range.filter(source='web').count()
    source_app = qs_range.filter(source='app').count()

    # ── Device class breakdown (range) ──
    device_data = list(
        qs_range.filter(source='web')
                .exclude(platform='')
                .values('platform')
                .annotate(count=Count('id'))
                .order_by('-count')
    )
    device_mobile = sum(d['count'] for d in device_data if d['platform'] in ('android', 'iphone', 'ios'))
    device_desktop = sum(d['count'] for d in device_data if d['platform'] in ('windows', 'mac', 'linux', 'chromeos'))
    device_tablet = sum(d['count'] for d in device_data if d['platform'] in ('ipad',))
    device_other = sum(d['count'] for d in device_data if d['platform'] not in ('android', 'iphone', 'ios', 'windows', 'mac', 'linux', 'chromeos', 'ipad'))

    platform_data = device_data

    # ── Demographics: country, city, gender ──
    # Country breakdown (from PageView geo data)
    country_qs = qs_range.exclude(country='').values('country').annotate(count=Count('id')).order_by('-count')[:15]
    country_data = list(country_qs)

    # City breakdown (from PageView geo data)
    city_qs = qs_range.exclude(city='').values('city').annotate(count=Count('id')).order_by('-count')[:15]
    city_data = list(city_qs)

    # Gender breakdown (join with User model for authenticated visitors)
    gender_counts = {'male': 0, 'female': 0, 'other': 0, 'unknown': 0}
    gender_qs = qs_range.filter(user_id__isnull=False).values('user_id').distinct()
    if gender_qs.exists():
        user_ids = list(gender_qs.values_list('user_id', flat=True))
        gender_map = dict(UserModel.objects.filter(id__in=user_ids).values_list('id', 'gender'))
        for uid in user_ids:
            g = gender_map.get(uid, '')
            if g == 'male':
                gender_counts['male'] += 1
            elif g == 'female':
                gender_counts['female'] += 1
            elif g == 'other':
                gender_counts['other'] += 1
            else:
                gender_counts['unknown'] += 1
    gender_data = [{'gender': k, 'count': v} for k, v in gender_counts.items()]

    # ── Referrer type breakdown (range) ──
    ref_direct = qs_range.filter(referrer_type='direct').count()
    ref_search = qs_range.filter(referrer_type='search').count()
    ref_social = qs_range.filter(referrer_type='social').count()
    ref_referral = qs_range.filter(referrer_type='referral').count()
    ref_internal = qs_range.filter(referrer_type='internal').count()

    _EXCLUDED_REFERRER_DOMAINS = (
        'accounts.google.com',
        'accounts.youtube.com',
        'login.facebook.com',
        'lm.facebook.com',
    )

    def _normalize_domain(domain):
        d = domain.lower().strip()
        prev = None
        while d != prev:
            prev = d
            d = _re.sub(r'^(www|m|l|web|en|api|fb|lm)\.', '', d)
        return d

    top_domains_raw = list(
        qs_range.exclude(referrer_type__in=['direct', 'internal', ''])
                .exclude(referrer_domain='')
                .values('referrer_domain')
                .annotate(count=Count('id'))
                .order_by('-count')[:50]
    )
    top_domains_map = {}
    for d in top_domains_raw:
        domain = d['referrer_domain']
        skip = False
        for ex in _EXCLUDED_REFERRER_DOMAINS:
            if ex in domain:
                skip = True
                break
        if skip:
            continue
        norm = _normalize_domain(domain)
        top_domains_map[norm] = top_domains_map.get(norm, 0) + d['count']
    top_domains = sorted(top_domains_map.items(), key=lambda x: -x[1])[:15]
    top_domains = [{'referrer_domain': k, 'count': v} for k, v in top_domains]

    top_pages = list(
        qs_range.exclude(path__startswith='/admin/')
                .exclude(path__startswith='/api/')
                .exclude(path__startswith='/ajax/')
                .values('path')
                .annotate(count=Count('id'))
                .order_by('-count')[:15]
    )

    referrer_details_raw = list(
        qs_range.exclude(referrer='')
                .values('referrer_domain', 'referrer_type')
                .annotate(count=Count('id'))
                .order_by('-count')[:50]
    )
    referrer_details_map = {}
    for d in referrer_details_raw:
        domain = d['referrer_domain'] or ''
        rtype = d['referrer_type'] or ''
        skip = False
        for ex in _EXCLUDED_REFERRER_DOMAINS:
            if ex in domain:
                skip = True
                break
        if skip:
            continue
        norm = _normalize_domain(domain) if domain else ''
        key = (norm, rtype)
        referrer_details_map[key] = referrer_details_map.get(key, 0) + d['count']
    referrer_details = sorted(
        [{'referrer_domain': k[0], 'referrer_type': k[1], 'count': v} for k, v in referrer_details_map.items()],
        key=lambda x: -x['count']
    )[:20]

    # ── Online users (always live) ──
    online_users, online_count = views_presence.get_online_users()
    online_user_details = []
    online_user_ids = [u['user_id'] for u in online_users]
    if online_user_ids:
        user_map = {str(u.id): u for u in UserModel.objects.filter(pk__in=online_user_ids).only('id', 'username', 'photo_url', 'role', 'display_name')}
        for u in online_users:
            usr = user_map.get(u['user_id'])
            if usr:
                online_user_details.append({
                    'user_id': u['user_id'],
                    'username': usr.username,
                    'display_name': usr.display_name or usr.username,
                    'photo_url': usr.photo_url,
                    'role': usr.role,
                    'screen': u.get('screen', ''),
                })

    # ── User stats ──
    total_users = UserModel.objects.count()
    total_pageviews = PageView.objects.count()
    today_users_active = qs_today.values('user_id').distinct().count()

    # ── DailyStat records (range) — auto-fill missing ──
    range_date_from = datetime.utcfromtimestamp(_range_start / 1000).date()
    range_date_to = datetime.utcfromtimestamp((_range_end - 1) / 1000).date()
    daily_stat_records = list(
        DailyStat.objects.filter(date__gte=range_date_from, date__lte=range_date_to)
        .order_by('-date')
    )
    existing_dates = {r.date for r in daily_stat_records}
    missing_dates = []
    d = range_date_from
    while d <= range_date_to:
        if d not in existing_dates:
            missing_dates.append(d)
        d += timedelta(days=1)
    if missing_dates:
        try:
            from api.management.commands.aggregate_daily_stats import aggregate_date as _agg_date
            for md in missing_dates:
                try:
                    _agg_date(md)
                except Exception:
                    pass
            daily_stat_records = list(
                DailyStat.objects.filter(date__gte=range_date_from, date__lte=range_date_to)
                .order_by('-date')
            )
        except ImportError:
            pass

    data = {
        'is_custom_range': is_custom_range,
        'date_from': date_from_str if is_custom_range else '',
        'date_to': date_to_str if is_custom_range else '',
        'range_label': range_label,
        'range_days': range_days_count,
        'total_users': total_users,
        'total_pageviews': total_pageviews,
        'today_visits': today_visits,
        'today_unique': today_unique,
        'today_new_users': today_new_users,
        'today_web': today_web,
        'today_app': today_app,
        'today_users_active': today_users_active,
        'yesterday_visits': yesterday_visits,
        'visit_delta': today_visits - yesterday_visits,
        'range_visits': range_visits,
        'range_unique': range_unique,
        'range_web': range_web,
        'range_app': range_app,
        'range_sessions': range_sessions,
        'range_bounce_count': range_bounce_count,
        'range_bounce_rate': range_bounce_rate,
        'range_pages_per_session': range_pages_per_session,
        'day_labels': day_labels,
        'day_visits': day_visits,
        'day_users': day_users,
        'day_posts': day_posts,
        'day_resources': day_resources,
        'hourly_labels': hourly_labels,
        'hourly_visits': hourly_visits,
        'peak_hour_labels': peak_hour_labels,
        'peak_hour_data': peak_hour_data,
        'dow_labels': dow_labels,
        'dow_data': dow_data,
        'source_web': source_web,
        'source_app': source_app,
        'device_mobile': device_mobile,
        'device_desktop': device_desktop,
        'device_tablet': device_tablet,
        'device_other': device_other,
        'ref_direct': ref_direct,
        'ref_search': ref_search,
        'ref_social': ref_social,
        'ref_referral': ref_referral,
        'ref_internal': ref_internal,
        'top_domains': top_domains,
        'top_pages': top_pages,
        'referrer_details': referrer_details,
        'platform_data': platform_data,
        # Demographics
        'country_data': country_data,
        'city_data': city_data,
        'gender_data': gender_data,
        'online_user_details': online_user_details,
        'online_count': online_count,
        'daily_stat_records': daily_stat_records,
        'has_data': total_pageviews > 0,
    }

    return render(request, 'admin_panel/analytics.html', {
        'is_admin': True,
        'active_page': 'analytics',
        **data,
    })


def admin_analytics_online_users(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return JsonResponse({'error': 'unauthorized'}, status=403)

    from api import views_presence
    from api.models import User as UserModel

    online_users, online_count = views_presence.get_online_users()
    online_user_ids = [u['user_id'] for u in online_users]
    user_map = {}
    if online_user_ids:
        for u in UserModel.objects.filter(pk__in=online_user_ids).only('id', 'username', 'photo_url', 'role', 'display_name'):
            user_map[str(u.id)] = {
                'username': u.username,
                'display_name': u.display_name or u.username,
                'photo_url': u.photo_url,
                'role': u.role,
            }
    details = []
    for u in online_users:
        usr = user_map.get(u['user_id'], {})
        details.append({
            'user_id': u['user_id'],
            'username': usr.get('username', '?'),
            'display_name': usr.get('display_name', '?'),
            'photo_url': usr.get('photo_url'),
            'role': usr.get('role', ''),
            'screen': u.get('screen', ''),
        })

    return JsonResponse({'online_count': online_count, 'users': details})


def admin_analytics_refresh(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return JsonResponse({'error': 'unauthorized'}, status=403)

    from api.models import PageView
    from api import views_presence
    _now = now_ms()
    _today_start = _now - (_now % 86400000)
    _yesterday_start = _today_start - 86400000

    qs_today = PageView.objects.filter(created_at__gte=_today_start)
    today_visits = qs_today.count()
    yesterday_visits = PageView.objects.filter(created_at__gte=_yesterday_start, created_at__lt=_today_start).count()

    online_users, online_count = views_presence.get_online_users()

    return JsonResponse({
        'today_visits': today_visits,
        'yesterday_visits': yesterday_visits,
        'visit_delta': today_visits - yesterday_visits,
        'online_count': online_count,
        'server_time': _now,
    })


def admin_analytics_export_csv(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    import csv
    from django.http import HttpResponse
    from api.models import DailyStat

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nebians_analytics_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Total Visits', 'Unique Visitors', 'New Users',
        'Web Visits', 'App Visits', 'Direct', 'Search', 'Social',
        'Referral', 'Internal', 'New Posts', 'New Resources', 'New Replies',
        'Avg Session Duration', 'Bounce Count', 'Total Sessions',
        'Pages Per Session', 'Peak Hour'
    ])

    for stat in DailyStat.objects.all().order_by('-date'):
        writer.writerow([
            stat.date.isoformat(), stat.total_visits, stat.unique_visitors,
            stat.new_users, stat.web_visits, stat.app_visits,
            stat.direct_visits, stat.search_visits, stat.social_visits,
            stat.referral_visits, stat.internal_visits,
            stat.new_posts, stat.new_resources, stat.new_replies,
            stat.avg_session_duration, stat.bounce_count,
            stat.total_sessions, stat.pages_per_session, stat.peak_hour,
        ])

    return response


def admin_hero_backgrounds(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    
    from api.models import HeroBackground
    import time
    from django.core.cache import cache
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'activate':
            bg_id = request.POST.get('bg_id')
            try:
                bg = HeroBackground.objects.get(id=bg_id)
                HeroBackground.objects.all().update(is_active=False)
                bg.is_active = True
                bg.save()
                cache.delete('active_hero_background_filename')
                messages.success(request, f"Background '{bg.name}' activated successfully.")
            except HeroBackground.DoesNotExist:
                messages.error(request, "Background not found.")
                
        elif action == 'delete':
            bg_id = request.POST.get('bg_id')
            try:
                bg = HeroBackground.objects.get(id=bg_id)
                if bg.is_active:
                    messages.error(request, "Cannot delete the active background.")
                else:
                    bg.delete()
                    messages.success(request, f"Background '{bg.name}' deleted successfully.")
            except HeroBackground.DoesNotExist:
                messages.error(request, "Background not found.")
                
        elif action == 'add':
            name = request.POST.get('name', '').strip()
            uploaded_file = request.FILES.get('background_file')
            
            if not name or not uploaded_file:
                messages.error(request, "Name and file are required.")
            else:
                filename = uploaded_file.name
                import os
                safe_filename = os.path.basename(filename)
                ext = os.path.splitext(safe_filename)[1].lower()
                
                if ext != '.svg':
                    messages.error(request, "Only SVG files (.svg) are allowed for hero backgrounds.")
                elif safe_filename != filename:
                    messages.error(request, "Invalid filename format.")
                else:
                    from django.conf import settings
                    file_content = uploaded_file.read()
                    
                    # 1. Write to local/repo static folder
                    local_dir = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'img')
                    os.makedirs(local_dir, exist_ok=True)
                    local_path = os.path.join(local_dir, safe_filename)
                    with open(local_path, 'wb') as f:
                        f.write(file_content)
                        
                    # 2. Write to public static folder for immediate serving (production)
                    public_dir = os.path.join(settings.BASE_DIR, 'public', 'static', 'web', 'img')
                    if os.path.exists(os.path.join(settings.BASE_DIR, 'public')):
                        os.makedirs(public_dir, exist_ok=True)
                        public_path = os.path.join(public_dir, safe_filename)
                        with open(public_path, 'wb') as f:
                            f.write(file_content)
                            
                    # 3. Write to staticfiles/ root
                    staticfiles_dir = os.path.join(settings.BASE_DIR, 'staticfiles', 'web', 'img')
                    if os.path.exists(staticfiles_dir):
                        staticfiles_path = os.path.join(staticfiles_dir, safe_filename)
                        with open(staticfiles_path, 'wb') as f:
                            f.write(file_content)
                    
                    try:
                        max_sort = HeroBackground.objects.order_by('-sort_order').first()
                        next_sort = (max_sort.sort_order + 1) if max_sort else 1
                        HeroBackground.objects.create(
                            name=name,
                            filename=safe_filename,
                            is_active=False,
                            sort_order=next_sort,
                            created_at=int(time.time() * 1000)
                        )
                        messages.success(request, f"Background '{name}' uploaded and added successfully.")
                    except Exception as e:
                        messages.error(request, f"Error adding background: {str(e)}")
        
        return redirect('/admin/hero-backgrounds/')

    backgrounds = HeroBackground.objects.all().order_by('sort_order', 'id')
    ctx = _ctx(request, active_page='hero_backgrounds', backgrounds=backgrounds)
    return render(request, 'admin_panel/hero_backgrounds.html', ctx)


def admin_pending_payments(request):
    """Admin page to verify buyer payment screenshots & transaction IDs."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    admin_user = None
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            admin_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            pass

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id', '').strip()
        action = request.POST.get('action', '').strip()
        reason = request.POST.get('reason', '').strip()[:500]

        try:
            payment_obj = PaymentVerification.objects.select_related('buyer', 'seller', 'resource').get(pk=payment_id)
            if action == 'approve' and payment_obj.status == 'pending':
                with transaction.atomic():
                    payment_obj.status = 'approved'
                    payment_obj.verified_at = now_ms()
                    payment_obj.verified_by = admin_user
                    payment_obj.admin_notes = reason
                    payment_obj.save()

                    # Credit seller balance
                    seller_bal = get_or_create_seller_balance(payment_obj.seller)
                    seller_bal.total_earned += payment_obj.seller_earnings
                    seller_bal.current_balance += payment_obj.seller_earnings
                    seller_bal.updated_at = now_ms()
                    seller_bal.save()

                    # Notify buyer and seller
                    _notif.create_notification(
                        recipient=payment_obj.buyer,
                        actor=admin_user or payment_obj.seller,
                        verb='payment_approved',
                        target=payment_obj.resource,
                        message=f"Your payment of Rs. {payment_obj.amount} for '{payment_obj.resource.title}' has been verified & approved! You now have full access."
                    )
                    _notif.create_notification(
                        recipient=payment_obj.seller,
                        actor=payment_obj.buyer,
                        verb='sale_credited',
                        target=payment_obj.resource,
                        message=f"You earned Rs. {payment_obj.seller_earnings} from the sale of '{payment_obj.resource.title}' to @{payment_obj.buyer.username}!"
                    )

            elif action == 'reject' and payment_obj.status == 'pending':
                payment_obj.status = 'rejected'
                payment_obj.verified_at = now_ms()
                payment_obj.verified_by = admin_user
                payment_obj.admin_notes = reason
                payment_obj.save()

                _notif.create_notification(
                    recipient=payment_obj.buyer,
                    actor=admin_user or payment_obj.seller,
                    verb='payment_rejected',
                    target=payment_obj.resource,
                    message=f"Your payment verification for '{payment_obj.resource.title}' was rejected. Reason: {reason or 'Invalid proof'}"
                )
        except PaymentVerification.DoesNotExist:
            pass

        return redirect('web:admin_pending_payments')

    pending_payments = PaymentVerification.objects.filter(status='pending').select_related('buyer', 'seller', 'resource').order_by('-created_at')
    processed_payments = PaymentVerification.objects.exclude(status='pending').select_related('buyer', 'seller', 'resource', 'verified_by').order_by('-verified_at')[:50]

    return render(request, 'admin_panel/payments.html', _ctx(request,
        active_page='payments',
        pending_payments=pending_payments,
        processed_payments=processed_payments,
    ))


def admin_withdrawals(request):
    """Admin view for processing seller earnings withdrawal requests."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    admin_user = None
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            admin_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            pass

    if request.method == 'POST':
        request_id = request.POST.get('request_id', '').strip()
        action = request.POST.get('action', '').strip()
        reason = request.POST.get('reason', '').strip()[:500]

        try:
            w_req = WithdrawalRequest.objects.select_related('user').get(pk=request_id)
            if action == 'approve' and w_req.status == 'pending':
                with transaction.atomic():
                    w_req.status = 'approved'
                    w_req.processed_at = now_ms()
                    w_req.processed_by = admin_user
                    w_req.admin_notes = reason
                    w_req.save()

                    # Update total_withdrawn in SellerBalance
                    seller_bal = get_or_create_seller_balance(w_req.user)
                    seller_bal.total_withdrawn += w_req.amount
                    seller_bal.updated_at = now_ms()
                    seller_bal.save()

                    _notif.create_notification(
                        recipient=w_req.user,
                        actor=admin_user,
                        verb='withdrawal_paid',
                        target=None,
                        message=f"Your withdrawal of Rs. {w_req.amount} via {w_req.get_payout_method_display()} has been processed & paid!"
                    )

            elif action == 'reject' and w_req.status == 'pending':
                with transaction.atomic():
                    w_req.status = 'rejected'
                    w_req.processed_at = now_ms()
                    w_req.processed_by = admin_user
                    w_req.admin_notes = reason
                    w_req.save()

                    # Refund balance back to seller
                    seller_bal = get_or_create_seller_balance(w_req.user)
                    seller_bal.current_balance += w_req.amount
                    seller_bal.updated_at = now_ms()
                    seller_bal.save()

                    _notif.create_notification(
                        recipient=w_req.user,
                        actor=admin_user,
                        verb='withdrawal_rejected',
                        target=None,
                        message=f"Your withdrawal request of Rs. {w_req.amount} was rejected. Amount has been refunded to your balance. Reason: {reason or 'Incorrect details'}"
                    )
        except WithdrawalRequest.DoesNotExist:
            pass

        return redirect('web:admin_withdrawals')

    pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').select_related('user').order_by('-created_at')
    processed_withdrawals = WithdrawalRequest.objects.exclude(status='pending').select_related('user', 'processed_by').order_by('-processed_at')[:50]

    return render(request, 'admin_panel/withdrawals.html', _ctx(request,
        active_page='withdrawals',
        pending_withdrawals=pending_withdrawals,
        processed_withdrawals=processed_withdrawals,
    ))