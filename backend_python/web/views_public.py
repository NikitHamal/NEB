"""Views Public extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403

def _get_library_filter_options():
    """Cached distinct subject/grade/type/faculty/exam_type lists for filter UIs.

    Replaces the old pattern of caching 500 fully serialized resources just to
    derive these small option lists.
    """
    options = cache.get('library_filter_options')
    if options is None:
        rows = Resource.objects.filter(approval_status='approved').values_list(
            'subject', 'grade_level', 'type', 'faculty', 'exam_type'
        )[:500]
        subjects_set, grades_set, types_set, faculties_set, exam_types_set = set(), set(), set(), set(), set()
        for subj, grade, rtype, faculty, exam_type in rows:
            if subj:
                for s in subj.split(','):
                    s_stripped = s.strip()
                    if s_stripped:
                        subjects_set.add(s_stripped)
            if grade:
                grades_set.add(grade)
            if rtype:
                types_set.add(rtype)
            if faculty:
                faculties_set.add(faculty)
            if exam_type:
                exam_types_set.add(exam_type)
        options = {
            'subjects': sorted(subjects_set),
            'grades': sorted(grades_set),
            'types': sorted(types_set),
            'faculties': sorted(faculties_set),
            'exam_types': sorted(exam_types_set),
        }
        cache.set('library_filter_options', options, 180)
    return options

def manifest_json(request):
    from django.http import JsonResponse
    data = {
        'name': 'NEBians - Nepali Learning Community',
        'short_name': 'NEBians',
        'description': 'A Nepali learning community for students, teachers, and lifelong learners with resources, discussions, AI summaries, quizzes, flashcards, and mindmaps.',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#ffffff',
        'theme_color': '#004bd4',
        'icons': [
            {'src': '/static/web/img/n-logo-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/static/web/img/n-logo-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'},
        ],
    }
    response = JsonResponse(data)
    response['Content-Type'] = 'application/manifest+json'
    return response

def home(request):
    token = api.get_session_token(request)
    if token:
        user_data = api.get_session_user(request)
        if user_data and (not user_data.get('display_name') or not user_data.get('gender') or not user_data.get('class_level')):
            return redirect('web:edit_profile')
    user_id = _get_user_id(request)
    resources = cache.get('home_resources')
    if resources is None:
        resources = _serialize_resources(Resource.objects.filter(approval_status='approved', is_lead=True)[:50])
        cache.set('home_resources', resources, 60)
    user_profile = None
    if user_id:
        try:
            from api.models import User
            user_profile = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
    posts_qs = Post.objects.select_related('user').filter(is_archived=False, user__email_verified=True).order_by('-created_at')[:20]
    all_posts = _serialize_posts(posts_qs, user_id)
    import math as _math
    _now_ms = now_ms()
    def _post_hot(p):
        likes = p.get('thumbs_up_count', 0) or 0
        replies = p.get('reply_count', 0) or 0
        views = p.get('view_count', 0) or 0
        created = p.get('createdAt', 0) or 0
        engagement = likes * 3 + replies * 2 + min(views, 1000) * 0.1
        age_hours = max(0, (_now_ms - created) / 3600000)
        if engagement <= 0:
            return -age_hours / 168.0
        return _math.log2(max(engagement, 1)) - age_hours / 168.0
    all_posts.sort(key=_post_hot, reverse=True)

    if user_profile and not is_global_user(user_profile) and (user_profile.class_level or user_profile.subjects):
        grade_pref = (user_profile.class_level or '').strip().lower()
        subject_prefs = [s.strip().lower() for s in (user_profile.subjects or '').split(',') if s.strip()]
        
        def get_relevance_score(r):
            r_grade = (r.get('grade_level') or '').strip().lower()
            r_subject = (r.get('subject') or '').strip().lower()
            
            grade_match = (r_grade == grade_pref) if grade_pref else False
            subject_match = False
            if subject_prefs:
                for s in subject_prefs:
                    if s in r_subject:
                        subject_match = True
                        break
            if grade_match and subject_match:
                return 4
            elif grade_match:
                return 3
            elif subject_match:
                return 2
            else:
                return 1

        curated_resources = sorted(
            resources,
            key=lambda r: (get_relevance_score(r), r.get('view_count', 0)),
            reverse=True
        )
        trending_resources = curated_resources[:5]
    else:
        trending_resources = sorted(resources, key=lambda r: r.get('view_count', 0), reverse=True)[:5]
    trending_posts = all_posts[:3]
    subjects = []
    seen = set()
    for r in resources:
        s = r.get('subject', '')
        if s and s not in seen:
            subjects.append(s)
            seen.add(s)
    latest_news = cache.get('home_latest_news_v3')
    if latest_news is None:
        from api.models import Announcement
        news_qs = Announcement.objects.select_related('author').filter(
            status='published'
        ).order_by('-is_pinned', '-published_at')[:5]
        latest_news = []
        from .views_news import _serialize_announcement
        for a in news_qs:
            latest_news.append(_serialize_announcement(a))
        cache.set('home_latest_news_v3', latest_news, 120)
    home_stats = cache.get('home_stats_v2')
    if home_stats is None:
        home_stats = {
            'resources': Resource.objects.filter(approval_status='approved').count(),
            'members': User.objects.filter(email_verified=True, is_locked=False, is_bot=False).count(),
            'discussions': Post.objects.filter(is_archived=False, user__email_verified=True).count(),
            'replies': Reply.objects.filter(is_archived=False, user__email_verified=True).count(),
        }
        cache.set('home_stats_v2', home_stats, 600)
    return render(request, 'web/home.html', _ctx(request,
        trending_resources=trending_resources,
        trending_posts=trending_posts,
        subjects=subjects[:12],
        latest_news=latest_news,
        home_stats=home_stats,
        hide_footer_links=False,
    ))

def library(request):
    user_id = _get_user_id(request)
    user_profile = None
    if user_id:
        try:
            from api.models import User
            user_profile = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    subjects = [s.strip() for s in request.GET.getlist('subject') if s.strip()]
    grades = [g.strip() for g in request.GET.getlist('grade') if g.strip()]

    types = [t.strip() for t in request.GET.getlist('type') if t.strip()]
    faculties = [f.strip() for f in request.GET.getlist('faculty') if f.strip()]
    exam_types = [e.strip() for e in request.GET.getlist('exam_type') if e.strip()]
    sort_by = request.GET.get('sort', 'relevant')
    current_tab = request.GET.get('tab', 'digital')
    if current_tab not in ['digital', 'community', 'categories', 'interactive']:
        current_tab = 'digital'

    interactive_categories = []
    interactive_stats = None
    if current_tab == 'interactive':
        from . import interactive as interactive_catalog
        interactive_categories = interactive_catalog.get_courses_by_category()
        interactive_stats = interactive_catalog.get_stats()

    filtered = []
    page_obj = None

    if current_tab in ['digital', 'community']:
        is_lead_val = (current_tab == 'digital')
        qs = Resource.objects.filter(approval_status='approved', is_lead=is_lead_val, uploaded_by__email_verified=True)
        if subjects:
            q = Q()
            for s in subjects:
                q |= Q(subject__iexact=s)
            qs = qs.filter(q)
        if grades:
            q = Q()
            for g in grades:
                q |= Q(grade_level__iexact=g)
            qs = qs.filter(q)
        if types:
            q = Q()
            for t in types:
                q |= Q(type__iexact=t)
            qs = qs.filter(q)
        if faculties:
            q = Q()
            for f in faculties:
                q |= Q(faculty__iexact=f)
            qs = qs.filter(q)
        if exam_types:
            q = Q()
            for e in exam_types:
                q |= Q(exam_type__iexact=e)
            qs = qs.filter(q)
            
        user_profile = None
        if user_id:
            try:
                from api.models import User
                user_profile = User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass

        global_user = user_profile and is_global_user(user_profile)

        if user_profile and not global_user and (user_profile.class_level or user_profile.subjects):
            grade_pref = user_profile.class_level
            subject_prefs = [s.strip().lower() for s in (user_profile.subjects or '').split(',') if s.strip()]

            grade_match = Q(grade_level__iexact=grade_pref) if grade_pref else Q(pk__in=[])
            subject_match = Q(pk__in=[])
            if subject_prefs:
                q_subj = Q()
                for s in subject_prefs:
                    q_subj |= Q(subject__icontains=s)
                subject_match = q_subj

            from django.db.models import Case, When, Value, IntegerField
            qs = qs.annotate(
                relevance_score=Case(
                    When(grade_match & subject_match, then=Value(4)),
                    When(grade_match, then=Value(3)),
                    When(subject_match, then=Value(2)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            if sort_by == 'newest':
                qs = qs.order_by('-relevance_score', '-added_at')
            elif sort_by == 'oldest':
                qs = qs.order_by('-relevance_score', 'added_at')
            elif sort_by == 'liked':
                qs = qs.order_by('-relevance_score', '-like_count', '-added_at')
            elif sort_by == 'trending':
                qs = qs.order_by('-relevance_score', '-added_at')
            else:
                qs = qs.order_by('-relevance_score', '-view_count', '-added_at')
        else:
            if sort_by == 'newest':
                qs = qs.order_by('-added_at')
            elif sort_by == 'oldest':
                qs = qs.order_by('added_at')
            elif sort_by == 'liked':
                qs = qs.order_by('-like_count', '-added_at')
            elif sort_by == 'trending':
                qs = qs.order_by('-added_at')
            else:
                qs = qs.order_by('-view_count', '-added_at')
            
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        page_num = request.GET.get('page', 1)
        paginator = Paginator(qs, 12)
        try:
            page_obj = paginator.page(page_num)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.page(1)
        filtered = _serialize_resources(page_obj.object_list)

        if sort_by == 'trending' and filtered:
            import math
            _now = now_ms()
            def _resource_hot(r):
                likes = r.get('like_count', 0) or 0
                views = r.get('view_count', 0) or 0
                added = r.get('added_at', 0) or 0
                engagement = likes * 5 + min(views, 500) * 0.1
                age_hours = max(0, (_now - added) / 3600000)
                if engagement <= 0:
                    return -age_hours / 168.0
                return math.log2(max(engagement, 1)) - age_hours / 168.0
            filtered.sort(key=_resource_hot, reverse=True)

    filter_options = _get_library_filter_options()
    all_subjects = filter_options['subjects']
    all_grades = filter_options['grades']
    all_types = filter_options['types']
    all_faculties = filter_options['faculties']
    all_exam_types = filter_options['exam_types']
    
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]

    # Build Class syllabus category tree dynamically from SyllabusContent
    from collections import defaultdict
    from api.models import SyllabusContent
    categories_map = defaultdict(set)
    active_syllabus = SyllabusContent.objects.all().values('grade_level', 'subject')
    
    if active_syllabus.exists():
        for item in active_syllabus:
            grade = item['grade_level'].strip() if item['grade_level'] else ''
            if grade.lower() == 'grade 12':
                grade = 'Class 12'
            elif grade.lower() == 'grade 11':
                grade = 'Class 11'
            subject_str = item['subject']
            if grade and subject_str:
                for s in subject_str.split(','):
                    s_clean = s.strip()
                    if s_clean:
                        categories_map[grade].add(s_clean)
    else:
        # Fallback to CURRICULUM_MAP keys
        for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
            categories_map[g_val].add(s_val)
                    
    grade_order = {val: i for i, val in enumerate(education_levels)}
    categories_list = []
    for grade, subjs in categories_map.items():
        subjs_sorted = sorted(list(subjs))
        subjs_list = []
        for s in subjs_sorted:
            grade_slug = grade.lower().replace(' / see', '-see').replace(' ', '-')
            subject_slug = s.lower().replace(' ', '-')
            subjs_list.append({
                'name': s,
                'slug': subject_slug,
                'url': f"/subject/{grade_slug}/{subject_slug}/"
            })
        categories_list.append({
            'grade': grade,
            'subjects': subjs_list,
            'order': grade_order.get(grade, 999)
        })
    categories_list.sort(key=lambda x: x['order'])

    ctx = _ctx(request,
        resources=filtered,
        all_subjects=all_subjects,
        all_grades=all_grades,
        all_types=all_types,
        all_faculties=all_faculties,
        all_exam_types=all_exam_types,
        education_levels=education_levels,
        current_subjects=subjects,
        current_grades=grades,
        current_types=types,
        current_faculties=faculties,
        current_exam_types=exam_types,
        current_sort=sort_by,
        current_tab=current_tab,
        page_obj=page_obj,
        categories_list=categories_list,
        interactive_categories=interactive_categories,
        interactive_stats=interactive_stats,
    )

    if getattr(request, 'htmx', False) and current_tab in ['digital', 'community']:
        return render(request, 'web/_library_main.html', ctx)

    return render(request, 'web/library.html', ctx)

def search(request):
    user_id = _get_user_id(request)
    user_profile = None
    if user_id:
        try:
            from api.models import User
            user_profile = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    query = request.GET.get('q', '').strip()
    tab = request.GET.get('tab', 'all')
    subject = request.GET.get('subject', '')
    grade = request.GET.get('grade', '')
    rtype = request.GET.get('type', '')

    resource_results = []
    post_results = []
    user_results = []

    if query:
        from api.search import is_enabled as meilisearch_enabled, search_resources, search_posts, search_users
        use_meili = meilisearch_enabled()

        if use_meili:
            if tab in ('all', 'resources'):
                meili_res = search_resources(query, subject=subject, grade=grade, rtype=rtype, limit=30)
                if meili_res is not None:
                    res_ids = [h['id'] for h in meili_res]
                    res_map = {str(r.id): r for r in Resource.objects.filter(pk__in=res_ids)}
                    resource_results = []
                    for hit in meili_res:
                        r = res_map.get(hit['id'])
                        if r:
                            formatted = _serialize_resource(r)
                            formatted['highlight'] = hit.get('_formatted', {})
                            resource_results.append(formatted)
                else:
                    use_meili = False

            if tab in ('all', 'posts') and (use_meili or not meilisearch_enabled()):
                meili_posts = search_posts(query, category=subject, limit=20)
                if meili_posts is not None:
                    post_ids = [h['id'] for h in meili_posts]
                    post_map = {str(p.id): p for p in Post.objects.filter(pk__in=post_ids).select_related('user')}
                    post_results = []
                    for hit in meili_posts:
                        p = post_map.get(hit['id'])
                        if p:
                            formatted = _serialize_post(p, user_id)
                            formatted['highlight'] = hit.get('_formatted', {})
                            post_results.append(formatted)
                else:
                    use_meili = False

            if tab in ('all', 'users') and (use_meili or not meilisearch_enabled()):
                meili_users = search_users(query, limit=30)
                if meili_users is not None:
                    u_ids = [h['id'] for h in meili_users]
                    user_qs = User.objects.filter(pk__in=u_ids, email_verified=True)
                    user_results_list = _serialize_users_search(list(user_qs), user_id)
                    hit_map = {h['id']: h.get('_formatted', {}) for h in meili_users}
                    for item in user_results_list:
                        item['_highlight'] = hit_map.get(item['id'], {})
                    user_results = user_results_list
                else:
                    use_meili = False

        if not use_meili or not meilisearch_enabled():
            import re
            import operator
            from functools import reduce
            from django.db.models import Value, BooleanField, Case, When

            terms = [t for t in re.sub(r'[^\w\s]', ' ', query).split() if t]
            if terms:
                res_q_list = []
                for term in terms:
                    res_q_list.append(
                        Q(title__icontains=term) | Q(description__icontains=term) | Q(subject__icontains=term) |
                        Q(faculty__icontains=term) | Q(program__icontains=term) | Q(school__icontains=term) | Q(tags__icontains=term)
                    )
                resource_qs = Resource.objects.filter(
                    reduce(operator.and_, res_q_list),
                    approval_status='approved',
                    is_lead=True
                )
                exact_res_expr = Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__icontains=query) | Q(tags__icontains=query)
                resource_qs = resource_qs.annotate(
                    is_exact=Case(
                        When(exact_res_expr, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                ).order_by('-is_exact', '-added_at')

                post_q_list = []
                for term in terms:
                    post_q_list.append(
                        Q(title__icontains=term) | Q(content__icontains=term)
                    )
                post_qs = Post.objects.select_related('user').filter(
                    reduce(operator.and_, post_q_list)
                ).filter(is_archived=False)
                exact_post_expr = Q(title__icontains=query) | Q(content__icontains=query)
                post_qs = post_qs.annotate(
                    is_exact=Case(
                        When(exact_post_expr, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                ).order_by('-is_exact', '-created_at')
            else:
                resource_qs = Resource.objects.none()
                post_qs = Post.objects.none()

            if subject:
                resource_qs = resource_qs.filter(subject=subject)
                post_qs = post_qs.filter(category__iexact=subject)
            if grade:
                resource_qs = resource_qs.filter(grade_level=grade)
            if rtype:
                resource_qs = resource_qs.filter(type=rtype)

            if tab in ('all', 'resources'):
                resource_results = _serialize_resources(resource_qs[:30])
            if tab in ('all', 'posts'):
                post_results = _serialize_posts(post_qs[:20], user_id)
            if tab in ('all', 'users'):
                user_qs = User.objects.filter(
                    Q(username__icontains=query) | Q(display_name__icontains=query)
                ).filter(is_locked=False, email_verified=True).order_by('-follower_count', 'username')[:30]
                user_results = _serialize_users_search(user_qs, user_id)

    filter_options = _get_library_filter_options()
    all_subjects = filter_options['subjects']
    all_grades = filter_options['grades']
    all_types = filter_options['types']
    ctx = _ctx(request,
        query=query,
        tab=tab,
        resource_results=resource_results,
        post_results=post_results,
        user_results=user_results,
        all_subjects=all_subjects,
        all_grades=all_grades,
        all_types=all_types,
        current_subject=subject,
        current_grade=grade,
        current_type=rtype,
        meilisearch_enabled=meilisearch_enabled() if query else False,
    )
    if getattr(request, 'htmx', False):
        return render(request, 'web/_search_results.html', ctx)
    return render(request, 'web/search.html', ctx)


def ajax_instant_search(request):
    """AJAX endpoint for instant search with Meilisearch (or DB fallback)."""
    from django.http import JsonResponse
    query = request.GET.get('q', '').strip()[:100]
    tab = request.GET.get('tab', 'all')
    subject = request.GET.get('subject', '')
    grade = request.GET.get('grade', '')
    rtype = request.GET.get('type', '')
    if not query or len(query) < 2:
        return JsonResponse({'results': {'resources': [], 'posts': [], 'users': []}})
    user_id = _get_user_id(request)
    resources = []
    posts = []
    users = []
    from api.search import is_enabled as meilisearch_enabled, search_resources, search_posts, search_users
    use_meili = meilisearch_enabled()
    if use_meili:
        if tab in ('all', 'resources'):
            meili_res = search_resources(query, subject=subject, grade=grade, rtype=rtype, limit=10)
            if meili_res is not None:
                res_ids = [h['id'] for h in meili_res]
                res_map = {str(r.id): r for r in Resource.objects.filter(pk__in=res_ids)}
                for hit in meili_res:
                    r = res_map.get(hit['id'])
                    if r:
                        resources.append({'id': r.id, 'title': r.title, 'description': (r.description or '')[:200], 'subject': r.subject or '', 'type': r.type or '', 'grade_level': r.grade_level or '', 'url': f'/reader/{r.id}/', 'highlight': hit.get('_formatted', {})})
        if tab in ('all', 'posts'):
            meili_posts = search_posts(query, category=subject, limit=10)
            if meili_posts is not None:
                post_ids = [h['id'] for h in meili_posts]
                post_map = {str(p.id): p for p in Post.objects.filter(pk__in=post_ids).select_related('user')}
                for hit in meili_posts:
                    p = post_map.get(hit['id'])
                    if p:
                        posts.append({'id': p.id, 'title': p.title, 'content': p.content[:200], 'category': p.category or '', 'username': p.user.username if p.user else '', 'thumbs_up_count': p.thumbs_up_count, 'reply_count': p.reply_count, 'url': f'/forum/post/{p.id}/', 'highlight': hit.get('_formatted', {})})
        if tab in ('all', 'users'):
            meili_users = search_users(query, limit=10)
            if meili_users is not None:
                u_ids = [h['id'] for h in meili_users]
                for u in User.objects.filter(pk__in=u_ids, email_verified=True):
                    users.append({'id': u.id, 'username': u.username, 'displayName': u.display_name or u.username, 'photoUrl': u.photo_url, 'url': f'/profile/{u.username}/'})
    if not use_meili:
        import re
        import operator
        from functools import reduce
        terms = [t for t in re.sub(r'[^\w\s]', ' ', query).split() if t]
        if terms:
            if tab in ('all', 'resources'):
                res_q_list = [Q(title__icontains=t) | Q(description__icontains=t) | Q(subject__icontains=t) | Q(tags__icontains=t) for t in terms]
                qs = Resource.objects.filter(reduce(operator.and_, res_q_list), approval_status='approved', is_lead=True)[:10]
                for r in qs:
                    resources.append({'id': r.id, 'title': r.title, 'description': (r.description or '')[:200], 'subject': r.subject or '', 'type': r.type or '', 'grade_level': r.grade_level or '', 'url': f'/reader/{r.id}/'})
            if tab in ('all', 'posts'):
                post_q_list = [Q(title__icontains=t) | Q(content__icontains=t) for t in terms]
                qs = Post.objects.select_related('user').filter(reduce(operator.and_, post_q_list), is_archived=False)[:10]
                for p in qs:
                    posts.append({'id': p.id, 'title': p.title, 'content': p.content[:200], 'category': p.category or '', 'username': p.user.username if p.user else '', 'thumbs_up_count': p.thumbs_up_count, 'reply_count': p.reply_count, 'url': f'/forum/post/{p.id}/'})
            if tab in ('all', 'users'):
                qs = User.objects.filter(Q(username__icontains=query) | Q(display_name__icontains=query), is_locked=False, email_verified=True).order_by('-follower_count')[:10]
                for u in qs:
                    users.append({'id': u.id, 'username': u.username, 'displayName': u.display_name or u.username, 'photoUrl': u.photo_url, 'url': f'/profile/{u.username}/'})
    return JsonResponse({'results': {'resources': resources, 'posts': posts, 'users': users}})


def reader(request, resource_id):
    """Resource detail page — shows title, description, view/download/like actions, and comments."""
    user_id = _get_user_id(request)
    try:
        resource_obj = Resource.objects.select_related('uploaded_by').get(id=resource_id)
    except Resource.DoesNotExist:
        raise Http404("Resource not found")

    if resource_obj.approval_status != 'approved' and not _is_staff_admin(request):
        raise Http404("Resource not found")

    # Increment view count once per session
    view_key = f'resource_viewed_{resource_id}'
    if not request.session.get(view_key):
        Resource.objects.filter(pk=resource_id).update(view_count=F('view_count') + 1)
        request.session[view_key] = True
        resource_obj.view_count += 1  # update in-memory

    resource = _serialize_resource(resource_obj)

    # Validate file URL for "open in new tab" / download links
    raw_file_url = resource.get('file_url') or ''
    safe_file_url = ''
    file_url_error = ''
    if raw_file_url:
        media_prefix = settings.MEDIA_URL
        if raw_file_url.startswith(media_prefix) or (request and raw_file_url.startswith(request.build_absolute_uri(media_prefix))):
            safe_file_url = raw_file_url
        else:
            try:
                safe_file_url = validate_resource_file_url(raw_file_url)
            except ValidationError as exc:
                file_url_error = ' '.join(exc.messages)
    resource['safe_file_url'] = safe_file_url
    resource['file_url_error'] = file_url_error

    # Classify media type for template
    rtype_lower = (resource.get('type') or '').lower().strip()
    if rtype_lower == 'pdf':
        media_type = 'pdf'
    elif rtype_lower == 'video':
        media_type = 'video'
    elif rtype_lower == 'audio':
        media_type = 'audio'
    elif rtype_lower == 'image':
        media_type = 'image'
    else:
        media_type = 'document'
    resource['media_type'] = media_type

    # User-specific state: liked, bookmarked
    is_liked = False
    is_bookmarked = False
    if user_id:
        is_liked = ResourceLike.objects.filter(resource_id=resource_id, user_id=user_id).exists()
        is_bookmarked = Bookmark.objects.filter(
            user_id=user_id, target_type='resource', target_id=resource_id
        ).exists()

    # Load comments
    comments_qs = ResourceComment.objects.select_related('user').filter(
        resource_id=resource_id
    ).order_by('created_at')
    comments_list = list(comments_qs)
    liked_comment_ids = set()
    if user_id and comments_list:
        liked_comment_ids = set(ResourceCommentLike.objects.filter(
            comment_id__in=[c.id for c in comments_list], user_id=user_id
        ).values_list('comment_id', flat=True))
    all_comments = []
    for c in comments_list:
        c_data = {
            'id': c.id,
            'resourceId': c.resource_id,
            'authorId': c.user_id,
            'authorName': c.user.username if c.user else '',
            'authorPhoto': c.user.photo_url if c.user else '',
            'parentCommentId': c.parent_comment_id or '',
            'content': c.content,
            'likeCount': c.like_count,
            'replyCount': c.reply_count,
            'isEdited': c.is_edited,
            'createdAt': c.created_at,
            'isLiked': c.id in liked_comment_ids,
            'isOwner': (user_id and user_id == c.user_id),
        }
        all_comments.append(c_data)

    # Build tree: top-level and children
    top_level_comments = [c for c in all_comments if not c['parentCommentId']]
    children_map = {}
    for c in all_comments:
        if c['parentCommentId']:
            children_map.setdefault(c['parentCommentId'], []).append(c)

    # Related resources (same subject, excluding this one)
    related = Resource.objects.filter(
        subject__iexact=resource_obj.subject
    ).exclude(pk=resource_id).order_by('-view_count', '-added_at')[:4]
    related_resources = _serialize_resources(related)

    can_edit = bool(user_id and user_id == resource_obj.uploaded_by_id)

    # Fetch bundle files if it belongs to a group
    group_resources = []
    if resource_obj.upload_group_id:
        group_qs = Resource.objects.filter(
            upload_group_id=resource_obj.upload_group_id
        ).order_by('added_at')
        # Include resources that are pending or approved for staff, but only approved for normal users
        if not _is_staff_admin(request):
            group_qs = group_qs.filter(approval_status='approved')
        group_resources = _serialize_resources(group_qs)

    resource_files = group_resources if group_resources else [resource]

    return render(request, 'web/resource_detail.html', _ctx(request,
        resource=resource,
        resource_id=resource_id,
        is_liked=is_liked,
        is_bookmarked=is_bookmarked,
        can_edit=can_edit,
        comments=all_comments,
        top_level_comments=top_level_comments,
        children_map=children_map,
        comment_count=resource_obj.comment_count,
        related_resources=related_resources,
        group_resources=group_resources,
        resource_files=resource_files,
    ))

def resource_requests_page(request):
    """Public resource request listing page."""
    user_id = _get_user_id(request)
    user = None
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

    if request.method == 'POST' and request.POST.get('action') == 'create':
        title = request.POST.get('title', '').strip()
        if title:
            ResourceRequest.objects.create(
                id=uuid_str(),
                title=title,
                description=request.POST.get('description', '').strip(),
                subject=request.POST.get('subject', '').strip(),
                grade_level=request.POST.get('grade_level', '').strip(),
                faculty=request.POST.get('faculty', '').strip(),
                program=request.POST.get('program', '').strip(),
                year=request.POST.get('year', '').strip(),
                exam_type=request.POST.get('exam_type', '').strip(),
                pradesh=request.POST.get('pradesh', '').strip(),
                district=request.POST.get('district', '').strip(),
                tags=request.POST.get('tags', '').strip(),
                requested_by=user,
                requester_name=request.POST.get('requester_name', '').strip()[:100] if not user else '',
                requester_email=request.POST.get('requester_email', '').strip() if not user else '',
                created_at=now_ms(),
            )
        return redirect('web:resource_requests')

    status_filter = request.GET.get('status', 'open')
    qs = ResourceRequest.objects.select_related('requested_by').all()
    if status_filter:
        qs = qs.filter(status=status_filter)
    subject = request.GET.get('subject', '')
    if subject:
        qs = qs.filter(subject__iexact=subject)
    grade = request.GET.get('grade', '')
    if grade:
        qs = qs.filter(grade_level__iexact=grade)
    qs = qs.order_by('-upvote_count', '-created_at')

    upvoted_ids = set()
    if user_id:
        upvoted_ids = set(ResourceRequestUpvote.objects.filter(
            user_id=user_id, request_id__in=list(qs.values_list('id', flat=True)[:100])
        ).values_list('request_id', flat=True))

    all_subjects = sorted(set(ResourceRequest.objects.values_list('subject', flat=True)))
    all_grades = sorted(set(ResourceRequest.objects.values_list('grade_level', flat=True)))

    requests_data = []
    for req in qs[:50]:
        rd = {
            'id': req.id,
            'title': req.title,
            'description': req.description or '',
            'subject': req.subject,
            'grade_level': req.grade_level,
            'faculty': req.faculty or '',
            'program': req.program or '',
            'year': req.year or '',
            'exam_type': req.exam_type or '',
            'pradesh': req.pradesh or '',
            'district': req.district or '',
            'tags': req.tags or '',
            'status': req.status,
            'upvote_count': req.upvote_count,
            'is_upvoted': req.id in upvoted_ids,
            'created_at': req.created_at,
            'requested_by_name': req.requested_by.display_name or req.requested_by.username if req.requested_by else (req.requester_name or 'Anonymous'),
            'requested_by_photo': req.requested_by.photo_url if req.requested_by else '',
        }
        requests_data.append(rd)

    return render(request, 'web/resource_requests.html', _ctx(request,
        requests=requests_data,
        all_subjects=all_subjects,
        all_grades=all_grades,
        current_status=status_filter,
        current_subject=subject,
        current_grade=grade,
    ))

def upload_resource(request):
    """Standalone upload page — authenticated users upload with approval_status='pending'.
    Supports both file upload (primary) and URL (secondary)."""
    user_id = _get_user_id(request)
    user = None
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
    if user and not getattr(user, 'email_verified', False):
        user = None

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
    db_subjects = _get_distinct_subjects()
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
        if _rate_limit(request, 'upload_resource', 10, 3600, by_ip=True):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
            return render(request, 'web/upload.html', _ctx(request,
                subjects=subjects, education_levels=education_levels,
                exam_types=exam_types, pradesh_options=pradesh_options,
                resource_types=resource_types, common_tags=common_tags,
                errors=['Too many uploads. Please try again later.'],
                form_data=request.POST,
                is_authenticated=bool(user),
            ), status=429)
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
        thumbnail_url = request.POST.get('thumbnail_url', '').strip()

        uploaded_files = request.FILES.getlist('file')
        file_url = request.POST.get('file_url', '').strip()

        errors = []
        if len(uploaded_files) > 5:
            errors.append('You can upload at most 5 files per request.')
            uploaded_files = uploaded_files[:5]
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

            # If there were errors, clean up any successfully saved files
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
            created_resources = []
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
                        author_name=author_name,
                        source_type='user' if user else 'anonymous',
                        uploaded_by=user,
                        source_url=source_url,
                        source_label=source_label,
                        approval_status='pending',
                        upload_group_id=group_id,
                        is_lead=is_lead,
                    )
                    resource.save()
                    created_resources.append(resource)
            else:
                final_file_url = safe_file_url
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
                    file_url=final_file_url,
                    thumbnail_url=safe_thumbnail_url,
                    file_size=int(request.POST.get('file_size', '0')),
                    added_at=now_ms(),
                    author_name=author_name,
                    source_type='user' if user else 'anonymous',
                    uploaded_by=user,
                    source_url=source_url,
                    source_label=source_label,
                    approval_status='pending',
                    upload_group_id='',
                    is_lead=True,
                )
                resource.save()
                created_resources.append(resource)

            cache.delete_many(['home_resources', 'library_all_resources', 'library_filter_options', 'distinct_subjects'])
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect': reverse('web:upload_success')})
            return render(request, 'web/upload_success.html', _ctx(request,
                resource=_serialize_resource(created_resources[0]),
                is_anonymous=not bool(user),
                count=len(created_resources),
            ))

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        return render(request, 'web/upload.html', _ctx(request,
            subjects=subjects, education_levels=education_levels,
            exam_types=exam_types, pradesh_options=pradesh_options,
            resource_types=resource_types, common_tags=common_tags,
            errors=errors,
            form_data=request.POST,
            is_authenticated=bool(user),
        ))

    return render(request, 'web/upload.html', _ctx(request,
        subjects=subjects, education_levels=education_levels,
        exam_types=exam_types, pradesh_options=pradesh_options,
        resource_types=resource_types, common_tags=common_tags,
        is_authenticated=bool(user),
    ))

def upload_success(request):
    return render(request, 'web/upload_success.html', _ctx(request))

def edit_resource(request, resource_id):
    """Allow signed-in users who uploaded a resource to edit it."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        resource_obj = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        raise Http404("Resource not found")
    if resource_obj.uploaded_by_id != user_id:
        return redirect('web:reader', resource_id=resource_id)

    user = User.objects.get(pk=user_id)
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
    db_subjects = _get_distinct_subjects()
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
    exam_types_list = ['', 'Final', 'Midterm', 'Board', 'Entrance', 'SEE', 'Mock', 'Assignment', 'Notes', 'Reference', 'Other']
    pradesh_options = [
        'Province 1', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim',
    ]
    resource_types = ['PDF', 'Note', 'Video', 'Audio', 'Image', 'Link', 'Textbook', 'Past Paper', 'Model Paper', 'Guide', 'Solution', 'Presentation']

    if request.method == 'POST':
        resource_obj.title = request.POST.get('title', '').strip() or resource_obj.title
        resource_obj.subject = request.POST.get('subject', '').strip() or resource_obj.subject
        resource_obj.grade_level = request.POST.get('grade_level', '').strip()
        resource_obj.faculty = request.POST.get('faculty', '').strip()
        resource_obj.program = request.POST.get('program', '').strip()
        resource_obj.year = request.POST.get('year', '').strip()
        resource_obj.exam_type = request.POST.get('exam_type', '').strip()
        resource_obj.pradesh = request.POST.get('pradesh', '').strip()
        resource_obj.district = request.POST.get('district', '').strip()
        resource_obj.school = request.POST.get('school', '').strip()
        resource_obj.tags = request.POST.get('tags', '').strip()
        resource_obj.type = request.POST.get('type', '').strip() or resource_obj.type
        resource_obj.description = request.POST.get('description', '').strip()
        resource_obj.author_name = request.POST.get('author_name', '').strip()
        resource_obj.source_label = request.POST.get('source_label', '').strip()
        resource_obj.source_url = request.POST.get('source_url', '').strip()

        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
            if not err_resp and path:
                resource_obj.file = path
                resource_obj.file_url = request.build_absolute_uri(settings.MEDIA_URL + path)
                resource_obj.file_size = size

        file_url = request.POST.get('file_url', '').strip()
        if file_url and not uploaded_file:
            try:
                resource_obj.file_url = validate_resource_file_url(file_url)
            except Exception:
                pass

        thumbnail_url = request.POST.get('thumbnail_url', '').strip()
        if thumbnail_url:
            try:
                resource_obj.thumbnail_url = validate_resource_file_url(thumbnail_url)
            except Exception:
                pass
        elif request.POST.get('thumbnail_url') == '':
            resource_obj.thumbnail_url = ''

        resource_obj.approval_status = 'pending'
        resource_obj.save()
        cache.delete_many(['home_resources', 'library_all_resources', 'library_filter_options', 'distinct_subjects'])
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'redirect': reverse('web:reader', kwargs={'resource_id': resource_id})})
        return redirect('web:reader', resource_id=resource_id)

    resource = _serialize_resource(resource_obj)
    return render(request, 'web/edit_resource.html', _ctx(request,
        resource=resource,
        resource_id=resource_id,
        subjects=subjects,
        common_tags=common_tags,
        education_levels=education_levels,
        exam_types=exam_types_list,
        pradesh_options=pradesh_options,
        resource_types=resource_types,
        is_authenticated=True,
    ))

def subject_page(request, grade_slug, subject_slug):
    """Subject details page — groups resources by chapter and links Neby AI + forum."""
    grade_db_val = curriculum.get_grade_db_value(grade_slug)
    subject_db_val = curriculum.get_subject_db_value(subject_slug)
    
    # Query approved lead resources
    resources_qs = Resource.objects.filter(
        approval_status='approved',
        is_lead=True,
        grade_level__iexact=grade_db_val,
        subject__icontains=subject_db_val
    )
    
    # Fetch database syllabus content entries
    from api.models import SyllabusContent
    syllabus_entries = SyllabusContent.objects.filter(
        grade_level__iexact=grade_db_val,
        subject__iexact=subject_db_val
    ).order_by('order')
    
    grouped_resources = []
    chapter_map = {}
    
    if syllabus_entries.exists():
        for entry in syllabus_entries:
            ch_entry = {
                'id': entry.chapter_id,
                'name': entry.chapter_title,
                'keywords': [entry.chapter_title.lower(), entry.chapter_id.replace('-', ' ')],
                'notes': [],
                'solutions': [],
                'papers': [],
                'textbooks': [],
                'other': [],
                'count': 0,
                'syllabus_text': entry.text_content,
                'syllabus_sections': parse_sections(entry.text_content),
                'question_answers': entry.question_answers,
                'question_answers_parsed': parse_qas(entry.question_answers),
                'qa_sections': parse_sections(entry.question_answers),
            }
            grouped_resources.append(ch_entry)
            chapter_map[entry.chapter_id] = ch_entry
    else:
        # Fallback to predefined curriculum map
        chapters = curriculum.get_chapters_for_subject(grade_db_val, subject_db_val)
        for ch in chapters:
            ch_entry = {
                'id': ch['id'],
                'name': ch['name'],
                'keywords': ch['keywords'],
                'notes': [],
                'solutions': [],
                'papers': [],
                'textbooks': [],
                'other': [],
                'count': 0,
                'syllabus_text': '',
                'question_answers': '',
                'question_answers_parsed': []
            }
            grouped_resources.append(ch_entry)
            chapter_map[ch['id']] = ch_entry
        
    general_resources = {
        'id': 'general',
        'name': 'General & Reference Resources',
        'notes': [],
        'solutions': [],
        'papers': [],
        'textbooks': [],
        'other': [],
        'count': 0
    }
    
    total_count = 0
    for r in resources_qs:
        total_count += 1
        serialized = _serialize_resource(r)
        
        # Match to a chapter
        matched_ch_id = None
        # First match by tags exactly
        res_tags = [t.strip().lower() for t in (r.tags or '').split(',') if t.strip()]
        for ch in grouped_resources:
            if any(kw.lower() in res_tags for kw in ch['keywords']):
                matched_ch_id = ch['id']
                break
                
        # Substring search in tags, title or description if not matched yet
        if not matched_ch_id:
            r_title_lower = r.title.lower()
            r_desc_lower = (r.description or '').lower()
            r_tags_lower = (r.tags or '').lower()
            for ch in grouped_resources:
                if any(kw.lower() in r_title_lower or kw.lower() in r_desc_lower or kw.lower() in r_tags_lower for kw in ch['keywords']):
                    matched_ch_id = ch['id']
                    break
        
        target_group = chapter_map.get(matched_ch_id) if matched_ch_id else general_resources
        
        # Categorise resource type
        rtype_lower = (r.type or '').lower().strip()
        exam_type_lower = (r.exam_type or '').lower().strip()
        r_title_lower = r.title.lower()
        r_tags_lower = (r.tags or '').lower()
        
        is_solution = any(x in r_title_lower or x in r_tags_lower for x in ['solution', 'exercise', 'question answer', 'q&a', 'answers'])
        is_paper = exam_type_lower in ['board', 'final', 'mock', 'entrance', 'see'] or any(x in r_title_lower or x in r_tags_lower for x in ['past paper', 'model paper', 'question paper', 'exam paper'])
        
        if is_solution:
            target_group['solutions'].append(serialized)
        elif is_paper:
            target_group['papers'].append(serialized)
        elif rtype_lower == 'note' or exam_type_lower == 'notes':
            target_group['notes'].append(serialized)
        elif rtype_lower == 'textbook' or exam_type_lower == 'reference' or 'textbook' in r_title_lower:
            target_group['textbooks'].append(serialized)
        else:
            target_group['other'].append(serialized)
            
        target_group['count'] += 1
    
    # Query forum posts
    posts_qs = Post.objects.select_related('user').filter(
        Q(category__iexact=subject_db_val) | 
        Q(title__icontains=subject_db_val) | 
        Q(content__icontains=subject_db_val)
    ).filter(is_archived=False).order_by('-created_at')[:15]
    user_id = _get_user_id(request)
    posts = _serialize_posts(posts_qs, user_id)
    
    # Compile lists for drop-downs
    from api.models import SyllabusContent
    has_syllabus = SyllabusContent.objects.exists()
    
    active_subjects = set()
    if has_syllabus:
        # Driven solely by admin-created SyllabusContent
        for s_val in SyllabusContent.objects.filter(grade_level__iexact=grade_db_val).values_list('subject', flat=True).distinct():
            for s in s_val.split(','):
                s_clean = s.strip()
                if s_clean:
                    active_subjects.add(s_clean)
        # If no syllabus content exists for this specific grade, fall back to CURRICULUM_MAP
        if not active_subjects:
            for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
                if g_val.lower() == grade_db_val.lower():
                    active_subjects.add(s_val)
    else:
        # Fallback to CURRICULUM_MAP keys
        for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
            if g_val.lower() == grade_db_val.lower():
                active_subjects.add(s_val)
                
    subject_list = []
    for s in sorted(list(active_subjects)):
        slug = curriculum.slugify_tag(s)
        if slug:
            subject_list.append({
                'name': s,
                'slug': slug
            })

    active_grades = {grade_db_val}
    if has_syllabus:
        # Driven solely by admin-created SyllabusContent
        for g in SyllabusContent.objects.values_list('grade_level', flat=True).distinct():
            g_clean = g.strip() if g else ''
            if g_clean:
                if g_clean.lower() == 'grade 12':
                    g_clean = 'Class 12'
                elif g_clean.lower() == 'grade 11':
                    g_clean = 'Class 11'
                active_grades.add(g_clean)
    else:
        # Fallback to CURRICULUM_MAP keys
        for (g_val, s_val) in curriculum.CURRICULUM_MAP.keys():
            g_clean = g_val.strip()
            if g_clean:
                if g_clean.lower() == 'grade 12':
                    g_clean = 'Class 12'
                elif g_clean.lower() == 'grade 11':
                    g_clean = 'Class 11'
                active_grades.add(g_clean)
            
    education_levels = [
        'Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12',
        'Diploma', 'Bachelor', 'Master', 'PhD',
        'Entrance Prep', 'Competitive Exam', 'Other',
    ]
    grade_order = {val.lower(): i for i, val in enumerate(education_levels)}
    sorted_grades = sorted(list(active_grades), key=lambda x: grade_order.get(x.lower(), 999))
    
    grade_list = []
    for g in sorted_grades:
        grade_list.append({
            'name': g,
            'slug': g.lower().replace(' / see', '-see').replace(' ', '-')
        })
    
    ctx = _ctx(request,
        grade=grade_db_val,
        subject=subject_db_val,
        grade_slug=grade_slug,
        subject_slug=subject_slug,
        grouped_resources=grouped_resources,
        general_resources=general_resources,
        posts=posts,
        total_count=total_count,
        grade_list=grade_list,
        subject_list=subject_list,
        default_model='meta-llama/Llama-3-8b-instruct'
    )
    return render(request, 'web/subject_page.html', ctx)

def privacy_policy(request):
    return render(request, 'web/legal/privacy.html', _ctx(request))

def terms_of_service(request):
    return render(request, 'web/legal/terms.html', _ctx(request))

def copyright_takedown(request):
    errors = {}
    success = False
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        organization = request.POST.get('organization', '').strip()
        infringing_url = request.POST.get('infringing_url', '').strip()
        proof_of_ownership = request.POST.get('proof_of_ownership', '').strip()
        statement_good_faith = request.POST.get('statement_good_faith') == 'on'
        statement_accurate = request.POST.get('statement_accurate') == 'on'
        signature = request.POST.get('signature', '').strip()
        
        # Validations
        if not name:
            errors['name'] = 'Full Name is required.'
        if not email:
            errors['email'] = 'Email Address is required.'
        if not infringing_url:
            errors['infringing_url'] = 'Infringing URL on NEBians is required.'
        if not proof_of_ownership:
            errors['proof_of_ownership'] = 'Please describe the copyrighted work and proof of ownership.'
        if not statement_good_faith:
            errors['statement_good_faith'] = 'You must check this box to confirm good faith belief.'
        if not statement_accurate:
            errors['statement_accurate'] = 'You must check this box to confirm accuracy.'
        if not signature:
            errors['signature'] = 'Electronic signature signature is required.'
            
        if not errors:
            # Save the takedown request
            takedown = TakedownRequest(
                id=uuid.uuid4().hex,
                name=name,
                email=email,
                organization=organization,
                infringing_url=infringing_url,
                proof_of_ownership=proof_of_ownership,
                statement_good_faith=statement_good_faith,
                statement_accurate=statement_accurate,
                signature=signature,
                status='open',
                created_at=now_ms()
            )
            takedown.save()
            success = True
            
    ctx = _ctx(request)
    ctx.update({
        'errors': errors,
        'success': success,
        'form_data': request.POST if request.method == 'POST' and not success else {}
    })
    return render(request, 'web/takedown.html', ctx)

def sitemap_xml(request):
    """
    Generates a clean XML sitemap: public pages plus only approved resources,
    public non-archived forum posts, and unlocked real profiles.
    Search engines should not see private profiles, bots/test users, rejected
    uploads, placeholders, or low-value empty pages.
    """
    sitemap_content = cache.get('sitemap_xml')
    if sitemap_content is not None:
        return HttpResponse(sitemap_content, content_type='application/xml')

    from api.models import Resource, Post, User
    from django.utils import timezone
    from xml.sax.saxutils import escape as xml_escape

    base = 'https://nebians.consica.com.np'
    now = timezone.now().isoformat()
    urls = [
        {'loc': f'{base}/', 'changefreq': 'daily', 'priority': '1.0', 'lastmod': now},
        {'loc': f'{base}/library/', 'changefreq': 'daily', 'priority': '0.8', 'lastmod': now},
        {'loc': f'{base}/forum/', 'changefreq': 'daily', 'priority': '0.8', 'lastmod': now},
        {'loc': f'{base}/library/?tab=interactive', 'changefreq': 'weekly', 'priority': '0.8', 'lastmod': now},
    ]

    from . import interactive as interactive_catalog
    for course in interactive_catalog.get_all_courses():
        urls.append({'loc': f'{base}/interactive/{course["slug"]}/', 'changefreq': 'monthly', 'priority': '0.7', 'lastmod': now})
        for lesson in course.get('lessons', []):
            urls.append({'loc': f'{base}/interactive/{course["slug"]}/{lesson["slug"]}/', 'changefreq': 'monthly', 'priority': '0.6', 'lastmod': now})

    def _lastmod(ts):
        if isinstance(ts, int) and ts:
            return timezone.datetime.fromtimestamp(ts / 1000, tz=timezone.get_current_timezone()).isoformat()
        if hasattr(ts, 'isoformat') and ts:
            return ts.isoformat()
        return now

    def _clean_text(value):
        return (value or '').strip().lower()

    def _looks_low_quality(title, body=''):
        hay = (_clean_text(title) + ' ' + _clean_text(body)).strip()
        if len(_clean_text(title)) < 4:
            return True
        bad = ('test', 'demo', 'dummy', 'sample placeholder', 'lorem ipsum', 'asdf', 'untitled')
        return any(term in hay for term in bad)

    resources = (Resource.objects
                 .filter(approval_status='approved', is_lead=True)
                 .select_related('uploaded_by')
                 .order_by('-added_at')[:1500])
    for r in resources:
        if _looks_low_quality(r.title, r.description):
            continue
        uploader = getattr(r, 'uploaded_by', None)
        if uploader and (getattr(uploader, 'is_locked', False) or getattr(uploader, 'is_bot', False)):
            continue
        ts = getattr(r, 'updated_at', None) or getattr(r, 'added_at', None)
        urls.append({
            'loc': f'{base}/reader/{r.id}/',
            'changefreq': 'weekly',
            'priority': '0.6',
            'lastmod': _lastmod(ts),
        })

    posts = (Post.objects
             .filter(is_archived=False)
             .select_related('user')
             .order_by('-created_at')[:1000])
    for post in posts:
        author = getattr(post, 'user', None)
        if author and (getattr(author, 'is_locked', False) or getattr(author, 'is_bot', False)):
            continue
        if _looks_low_quality(post.title, post.content):
            continue
        urls.append({
            'loc': f'{base}/forum/post/{post.id}/',
            'changefreq': 'daily',
            'priority': '0.7',
            'lastmod': _lastmod(post.created_at),
        })

    users = (User.objects
             .filter(is_locked=False, is_bot=False, email_verified=True)
             .exclude(username='')
             .order_by('-contribution_score', 'username')[:500])
    for u in users:
        uname = (u.username or '').strip()
        if not uname or any(term in uname.lower() for term in ('test', 'demo', 'dummy', 'adminadmin')):
            continue
        urls.append({
            'loc': f'{base}/profile/{uname}/',
            'changefreq': 'weekly',
            'priority': '0.4',
            'lastmod': _lastmod(getattr(u, 'created_at', None)),
        })

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml_content += '  <url>\n'
        xml_content += f"    <loc>{xml_escape(u['loc'])}</loc>\n"
        xml_content += f"    <lastmod>{xml_escape(u['lastmod'])}</lastmod>\n"
        xml_content += f"    <changefreq>{u['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{u['priority']}</priority>\n"
        xml_content += '  </url>\n'
    xml_content += '</urlset>\n'

    cache.set('sitemap_xml', xml_content, 3600)
    return HttpResponse(xml_content, content_type='application/xml')

def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /admin-django/',
        'Disallow: /api/',
        'Disallow: /ajax/',
        'Disallow: /auth/',
        'Disallow: /login/',
        'Disallow: /logout/',
        'Disallow: /profile/edit/',
        '',
        'Sitemap: https://nebians.consica.com.np/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')

def custom_404(request, exception):
    return render(request, '404.html', _ctx(request), status=404)

def custom_500(request):
    return render(request, '500.html', _ctx(request), status=500)