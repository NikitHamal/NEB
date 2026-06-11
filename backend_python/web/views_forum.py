"""Views Forum extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from api import services

def forum(request):
    import math
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    user_id = _get_user_id(request)
    sort = request.GET.get('sort', 'hot')
    category = request.GET.get('category', '')
    search = request.GET.get('q', '').strip()
    page_num = request.GET.get('page', 1)

    valid_sorts = ('hot', 'new', 'top', 'discussed')
    if sort not in valid_sorts:
        sort = 'hot'

    qs = Post.objects.select_related('user').filter(is_archived=False)

    if category:
        qs = qs.filter(category__iexact=category)
    if search:
        terms = [t for t in re.sub(r'[^\w\s]', ' ', search).split() if t]
        if terms:
            q = Q()
            for term in terms:
                q |= Q(title__icontains=term) | Q(content__icontains=term)
            qs = qs.filter(q)

    if sort == 'hot' and not search:
        # Hot-rank a capped window of the most recent 500 posts (minimal
        # fields), cache the ranked ID list for 60s, then paginate over the
        # ranked IDs and fetch page objects preserving order.
        hot_cache_key = f'forum_hot_ids:{(category or "all").strip().lower()}'
        ranked_ids = cache.get(hot_cache_key)
        if ranked_ids is None:
            window = list(
                qs.order_by('-created_at')
                .only('id', 'created_at', 'thumbs_up_count', 'reply_count', 'view_count')[:500]
            )
            _now = now_ms()
            window.sort(key=lambda p: _compute_hot_score(p, _now), reverse=True)
            ranked_ids = [p.id for p in window]
            cache.set(hot_cache_key, ranked_ids, 60)

        paginator = Paginator(ranked_ids, 20)
        try:
            page_obj = paginator.page(page_num)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.page(1)
        page_ids = list(page_obj.object_list)
        posts_by_id = {
            p.id: p for p in Post.objects.select_related('user').filter(pk__in=page_ids)
        }
        posts_qs = [posts_by_id[pid] for pid in page_ids if pid in posts_by_id]
        posts = _serialize_posts(posts_qs, user_id)
    else:
        if sort == 'new':
            qs = qs.order_by('-created_at')
        elif sort == 'top':
            qs = qs.order_by('-thumbs_up_count', '-created_at')
        elif sort == 'discussed':
            qs = qs.order_by('-reply_count', '-created_at')
        else:
            qs = qs.order_by('-created_at')

        paginator = Paginator(qs, 20)
        try:
            page_obj = paginator.page(page_num)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.page(1)

        posts_qs = list(page_obj.object_list)
        posts = _serialize_posts(posts_qs, user_id)

        if sort == 'hot' and posts_qs:
            _now = now_ms()
            scored = list(zip(posts_qs, posts))
            scored.sort(key=lambda x: _compute_hot_score(x[0], _now), reverse=True)
            posts = [s[1] for s in scored]

    category_counts = dict(
        Post.objects.values('category').annotate(cnt=Count('id')).values_list('category', 'cnt')
    )
    standard_categories = ['General', 'Science', 'Math', 'Exam Prep', 'Entrance Exams']
    categories_data = []
    for name in standard_categories:
        count = category_counts.get(name, 0)
        categories_data.append({
            'name': name,
            'count': count,
            'formatted_count': format_score(count),
        })
    for cat, cnt in category_counts.items():
        if cat not in standard_categories:
            categories_data.append({
                'name': cat,
                'count': cnt,
                'formatted_count': format_score(cnt),
            })
    categories_data = sorted(categories_data, key=lambda c: (-c['count'], c['name']))

    contributor_data = cache.get('forum_contributors')
    if contributor_data is None:
        contributor_data = _build_contributors_batch()[:10]
        cache.set('forum_contributors', contributor_data, 300)

    top_contributors = contributor_data[:3]
    sidebar_categories = categories_data[:5]
    has_more_categories = len(categories_data) > 5

    ctx = _ctx(request,
        posts=posts,
        categories_data=sidebar_categories,
        has_more_categories=has_more_categories,
        top_contributors=top_contributors,
        all_contributors=contributor_data,
        current_category=category,
        current_sort=sort,
        search_query=search,
        page_obj=page_obj,
    )

    if getattr(request, 'htmx', False):
        return render(request, 'web/_forum_main.html', ctx)

    return render(request, 'web/forum.html', ctx)

def forum_categories(request):
    category_counts = dict(
        Post.objects.values('category').annotate(cnt=Count('id')).values_list('category', 'cnt')
    )
    standard_categories = ['General', 'Science', 'Math', 'Exam Prep', 'Entrance Exams']
    categories_data = []
    for name in standard_categories:
        count = category_counts.get(name, 0)
        categories_data.append({
            'name': name,
            'count': count,
            'formatted_count': format_score(count),
        })
    for cat, cnt in category_counts.items():
        if cat not in standard_categories:
            categories_data.append({
                'name': cat,
                'count': cnt,
                'formatted_count': format_score(cnt),
            })
    categories_data = sorted(categories_data, key=lambda c: (-c['count'], c['name']))
    return render(request, 'web/forum_categories.html', _ctx(request,
        categories_data=categories_data
    ))

def leaderboard(request):
    contributor_data = cache.get('forum_contributors')
    if contributor_data is None:
        contributor_data = _build_contributors_batch()[:50]
        cache.set('forum_contributors', contributor_data, 300)
    return render(request, 'web/leaderboard.html', _ctx(request,
        contributors=contributor_data,
    ))

def forum_post(request, post_id):
    user_id = _get_user_id(request)
    try:
        post_obj = Post.objects.select_related('user').get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found")
    view_key = f'post_viewed_{post_id}'
    if not request.session.get(view_key):
        Post.objects.filter(pk=post_id).update(view_count=F('view_count') + 1)
        request.session[view_key] = True
        post_obj.view_count += 1
    post = _serialize_post(post_obj, user_id)
    reply_sort = request.GET.get('sort', 'oldest')
    if reply_sort not in ('oldest', 'newest', 'top'):
        reply_sort = 'oldest'
    if reply_sort == 'newest':
        replies_qs = Reply.objects.select_related('user', 'post').filter(post_id=post_id).order_by('-created_at')
    elif reply_sort == 'top':
        replies_qs = Reply.objects.select_related('user', 'post').filter(post_id=post_id).order_by('-thumbs_up_count', 'created_at')
    else:
        replies_qs = Reply.objects.select_related('user', 'post').filter(post_id=post_id).order_by('created_at')
    all_replies = _serialize_replies(replies_qs, user_id)
    top_level = []
    children_map = {}
    for r in all_replies:
        if not r['parentReplyId']:
            top_level.append(r)
        else:
            children_map.setdefault(r['parentReplyId'], []).append(r)
    is_following = False
    is_owner = False
    if user_id:
        is_owner = (user_id == post_obj.user_id)
        if not is_owner:
            is_following = Follow.objects.filter(follower_id=user_id, following_id=post_obj.user_id).exists()
    all_usernames = list(set(
        [post_obj.user.username] + [r['authorName'] for r in all_replies]
    ))
    ctx = _ctx(request, post=post, replies=all_replies, top_level_replies=top_level, children_map=children_map, post_id=post_id, is_owner=is_owner, is_following=is_following, post_author_id=post_obj.user_id, all_usernames=all_usernames, reply_sort=reply_sort)

    if getattr(request, 'htmx', False):
        return render(request, 'web/_forum_post_replies_section.html', ctx)

    return render(request, 'web/forum_post.html', ctx)

def create_post(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category = request.POST.get('category', '').strip()
        image_urls = []
        for i in range(3):
            img = request.FILES.get(f'image_{i}')
            if img:
                try:
                    url = save_post_image_upload(request, user, img, order=i)
                    image_urls.append(url)
                except Exception:
                    pass
        poll_question = request.POST.get('poll_question', '').strip()
        poll_options_raw = request.POST.getlist('poll_option[]')
        poll_option_correct = request.POST.getlist('poll_option_correct[]')
        poll_options = []
        for i, opt in enumerate(poll_options_raw):
            opt_text = opt.strip()
            if opt_text:
                is_correct = str(i) in poll_option_correct
                poll_options.append({'text': opt_text, 'is_correct': is_correct})
        poll_data = None
        if poll_question and len(poll_options) >= 2:
            poll_data = {
                'question': poll_question,
                'poll_type': request.POST.get('poll_type', 'voting'),
                'allow_multiple': request.POST.get('allow_multiple', '') == 'true',
                'explanation': request.POST.get('poll_explanation', '').strip(),
                'duration_ms': int(request.POST.get('poll_duration', '0') or '0'),
                'options': poll_options,
            }
        if title and content and category:
            result = services.create_post(user, title, content, category, image_urls=image_urls, poll_data=poll_data)
            if result and result.get('id'):
                _clear_page_cache()
                return redirect('web:forum_post', post_id=result['id'])
    categories = ['General', 'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Computer Science', 'Exam Tips']
    return render(request, 'web/create_post.html', _ctx(request, categories=categories))

def reply_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')
    try:
        post_obj = Post.objects.select_related('user').get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found")
    post = _serialize_post(post_obj, user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        parent_reply_id = request.POST.get('parent_reply_id', '') or None
        if content:
            services.create_reply(user, post_id, content, parent_reply_id)
            _clear_page_cache()
            return redirect('web:forum_post', post_id=post_id)
    return render(request, 'web/reply.html', _ctx(request, post=post, post_id=post_id))