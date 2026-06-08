"""Views Profile extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from api.view_helpers import _profile_incomplete

def profile(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    is_self = bool(user_id and user_id == profile_user.id)
    profile_private = bool(profile_user.is_locked and not is_self)

    badge_info = _user_badge_info(profile_user)

    banner_type = ''
    banner_deco_text = 'nebian'
    banner_text_color = ''
    if not profile_user.banner_url:
        if profile_user.is_bot:
            banner_type = 'gradient-bot'
            banner_deco_text = 'neby ai'
            banner_text_color = 'rgba(255,255,255,0.25)'
        elif profile_user.is_admin:
            banner_type = 'gradient-admin'
            banner_deco_text = 'admin'
            banner_text_color = 'rgba(255,255,255,0.25)'
        elif profile_user.moderator_level and profile_user.moderator_level > 0:
            banner_type = 'gradient-moderator'
            banner_deco_text = 'moderator'
            banner_text_color = 'rgba(255,255,255,0.22)'
        elif profile_user.verification_level and profile_user.verification_level > 0:
            banner_type = 'gradient-verified'
            banner_deco_text = 'nebian'
            banner_text_color = 'rgba(255,255,255,0.20)'
        elif getattr(profile_user, 'role', '') == 'teacher':
            banner_type = 'gradient-tutor'
            banner_deco_text = 'tutor'
            banner_text_color = 'rgba(255,255,255,0.28)'
        elif getattr(profile_user, 'role', '') == 'institution':
            banner_type = 'gradient-institution'
            banner_deco_text = 'nebian'
            banner_text_color = 'rgba(255,255,255,0.25)'

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'banner_url': profile_user.banner_url,
        'banner_type': banner_type,
        'banner_deco_text': banner_deco_text,
        'banner_text_color': banner_text_color,
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
        'is_bot': profile_user.is_bot,
        'teacher_verified': profile_user.teacher_verified,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': badge_info,
        'achievement_info': _user_achievement_badges(profile_user),
    }

    if profile_private:
        profile_data.update({
            'email': '', 'dob': '', 'gender': '', 'class_level': '', 'class': '',
            'subjects': '', 'pradesh': '', 'district': '', 'school': '',
        })

    stats = _build_local_stats(profile_user) if not profile_private else {
        'post_count': 0, 'reply_count': 0, 'likes_given': 0, 'likes_received': 0, 'contribution_score': 0,
    }
    follower_count = profile_user.follower_count if (not profile_private and hasattr(profile_user, 'follower_count') and profile_user.follower_count > 0) else (Follow.objects.filter(following_id=profile_user.id).count() if not profile_private else 0)
    following_count = profile_user.following_count if (not profile_private and hasattr(profile_user, 'following_count') and profile_user.following_count > 0) else (Follow.objects.filter(follower_id=profile_user.id).count() if not profile_private else 0)
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = False
    stats['is_self'] = False
    if user_id:
        stats['is_self'] = is_self
        if not stats['is_self'] and not profile_private:
            stats['is_following'] = Follow.objects.filter(follower_id=user_id, following_id=profile_user.id).exists()

    if not profile_private:
        if is_self:
            uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id).count()
        else:
            uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').count()
    else:
        uploaded_resources_count = 0
    stats['uploaded_resources_count'] = uploaded_resources_count

    user_posts_qs = Post.objects.none() if profile_private else Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    user_replies_qs = Reply.objects.none() if profile_private else Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_replies = _serialize_replies(user_replies_qs, user_id)

    user_resources = []
    if not profile_private:
        if is_self:
            user_resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id).order_by('-added_at')
        else:
            user_resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').order_by('-added_at')

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

    return render(request, 'web/profile.html', _ctx(request,
        profile_user=profile_data,
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
        profile_user_json=json.dumps(profile_data),
    ))

def profile_achievements(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    if profile_user.is_locked and user_id != profile_user.id:
        return redirect('web:profile', username=username)

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
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
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': _user_badge_info(profile_user),
        'achievement_info': _user_achievement_badges(profile_user),
    }

    stats = _build_local_stats(profile_user)
    follower_count = profile_user.follower_count if hasattr(profile_user, 'follower_count') and profile_user.follower_count > 0 else Follow.objects.filter(following_id=profile_user.id).count()
    following_count = profile_user.following_count if hasattr(profile_user, 'following_count') and profile_user.following_count > 0 else Follow.objects.filter(follower_id=profile_user.id).count()
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

def ajax_profile_activity(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if profile_user.is_locked and user_id != profile_user.id:
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    user_posts_qs = Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[offset:offset+limit]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    total_count = Post.objects.filter(user_id=profile_user.id).count()
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

    if profile_user.is_locked and user_id != profile_user.id:
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    replies_qs = Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id).order_by('-created_at')[offset:offset+limit]
    replies = _serialize_replies(replies_qs, user_id)

    total_count = Reply.objects.filter(user_id=profile_user.id).count()
    has_more = (offset + len(replies)) < total_count

    return JsonResponse({
        'replies': replies,
        'has_more': has_more,
        'total_count': total_count
    })

def edit_profile(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    user = api.get_session_user(request)
    if not user:
        return redirect('web:login')
    try:
        db_user = User.objects.get(id=user.get('id'))
    except User.DoesNotExist:
        return redirect('web:login')
    has_password = bool(db_user.password_hash)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        dob = request.POST.get('dob', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        gender = request.POST.get('gender', '').strip()
        role = request.POST.get('role', db_user.role).strip().lower()
        class_level = request.POST.get('class_level', '').strip()
        if role not in ('student', 'teacher', 'institution', 'explorer'):
            role = db_user.role or 'student'
        if not username or not dob:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Username and Date of Birth are required.'))
        if not display_name:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Display Name is required.'))
        if not gender:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Gender is required.'))
        if role == 'student' and not class_level:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Class is required for students.'))
        if role == 'teacher' and not request.POST.get('teaching_subjects', '').strip():
            return render(request, 'web/edit_profile.html', _ctx(request, error='Teaching subjects are required for teachers.'))
        if role == 'institution' and not request.POST.get('school', '').strip():
            return render(request, 'web/edit_profile.html', _ctx(request, error='Institution name is required.'))
        conflict = User.objects.filter(username__iexact=username).exclude(pk=db_user.id).exists()
        if conflict:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Username already taken.'))
        db_user.username = username
        db_user.email = request.POST.get('email', '').strip() or db_user.email or ''
        db_user.display_name = display_name or db_user.display_name or ''
        db_user.role = role
        db_user.dob = dob
        db_user.gender = gender or db_user.gender or ''
        db_user.class_level = class_level or db_user.class_level or ''
        db_user.subjects = request.POST.get('subjects', '') or db_user.subjects or ''
        db_user.teaching_subjects = request.POST.get('teaching_subjects', '') or db_user.teaching_subjects or ''
        db_user.institution_type = request.POST.get('institution_type', '') or db_user.institution_type or ''
        db_user.pradesh = request.POST.get('pradesh', '') or db_user.pradesh or ''
        db_user.district = request.POST.get('district', '').strip() or db_user.district or ''
        db_user.school = request.POST.get('school', '').strip() or db_user.school or ''
        db_user.bio = request.POST.get('bio', '').strip()
        db_user.is_locked = request.POST.get('is_locked') == 'on'
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
            'bio': db_user.bio,
            'is_locked': 1 if db_user.is_locked else 0,
            'created_at': db_user.created_at,
        }
        api.set_session_auth(request, token, updated_data)
        return redirect('web:home')
    profile_incomplete = _profile_incomplete(db_user)
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
    return render(request, 'web/edit_profile.html', _ctx(request, has_password=has_password, profile_incomplete=profile_incomplete, subjects=subjects))
