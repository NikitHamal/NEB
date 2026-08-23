"""Admin views for the Announcement (news) system."""
from .view_helpers import *  # noqa: F401,F403
from .views_news import _slugify, _unique_slug, CATEGORY_META
from api.models import Announcement


def _clear_news_cache():
    """Clear all news-related cache keys (works on both Redis and LocMem)."""
    for key in ('home_latest_news', 'news_list::', 'news_list:exam_results:',
                'news_list:notice:', 'news_list:event:', 'news_list:update:',
                'news_list:alert:', 'news_list:general:'):
        cache.delete(key)
    if hasattr(cache, 'delete_pattern'):
        try:
            cache.delete_pattern('news_list:*')
        except Exception:
            pass


def _get_admin_user(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            return User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            pass
    return None


def admin_announcements(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        ann_id = request.POST.get('announcement_id', '').strip()
        if action == 'delete' and ann_id:
            try:
                Announcement.objects.get(pk=ann_id).delete()
                _clear_news_cache()
            except Announcement.DoesNotExist:
                pass
            return redirect('web:admin_announcements')
        if action == 'toggle_pin' and ann_id:
            try:
                ann = Announcement.objects.get(pk=ann_id)
                ann.is_pinned = not ann.is_pinned
                ann.save()
                _clear_news_cache()
            except Announcement.DoesNotExist:
                pass
            return redirect('web:admin_announcements')

    qs = Announcement.objects.select_related('author').all().order_by('-is_pinned', '-published_at', '-created_at')
    items = []
    for a in qs:
        meta = CATEGORY_META.get(a.category, CATEGORY_META['general'])
        items.append({
            'id': a.id,
            'title': a.title,
            'slug': a.slug,
            'category': a.category,
            'category_label': meta['label'],
            'category_icon': meta['icon'],
            'category_color': meta['color'],
            'status': a.status,
            'is_pinned': a.is_pinned,
            'published_at': a.published_at,
            'created_at': a.created_at,
            'view_count': a.view_count,
            'author_name': (a.author.display_name or a.author.username) if a.author else '—',
        })

    return render(request, 'admin_panel/announcements.html', {
        'is_admin': True,
        'active_page': 'announcements',
        'announcements': items,
    })


def admin_announcement_edit(request, announcement_id=None):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    is_edit = announcement_id is not None
    ann = None
    if is_edit:
        try:
            ann = Announcement.objects.get(pk=announcement_id)
        except Announcement.DoesNotExist:
            raise Http404('Announcement not found')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        errors = []
        if not title:
            errors.append('Title is required.')
        category = request.POST.get('category', 'general').strip()
        if category not in CATEGORY_META:
            category = 'general'
        summary = request.POST.get('summary', '').strip()[:500]
        content = request.POST.get('content', '').strip()
        status = request.POST.get('status', 'draft').strip()
        if status not in ('draft', 'published', 'archived'):
            status = 'draft'
        is_pinned = request.POST.get('is_pinned') == 'on'
        cover_image_url = request.POST.get('cover_image_url', '').strip()
        external_url = request.POST.get('external_url', '').strip()
        tags = request.POST.get('tags', '').strip()
        slug = request.POST.get('slug', '').strip()

        if errors:
            form_data = {
                'title': title, 'summary': summary, 'content': content, 'category': category,
                'status': status, 'is_pinned': is_pinned, 'cover_image_url': cover_image_url,
                'external_url': external_url, 'tags': tags, 'slug': slug,
            }
            return render(request, 'admin_panel/announcement_form.html', {
                'is_admin': True,
                'active_page': 'announcements',
                'is_edit': is_edit,
                'announcement': ann,
                'form_data': form_data,
                'categories': [{'key': k, 'label': v['label'], 'icon': v['icon']} for k, v in CATEGORY_META.items()],
                'errors': errors,
            })

        admin_user = _get_admin_user(request)
        if not slug:
            slug = _unique_slug(_slugify(title), exclude_id=ann.id if ann else None)
        else:
            slug = _slugify(slug)
            if Announcement.objects.exclude(pk=ann.id if ann else None).filter(slug=slug).exists():
                slug = _unique_slug(slug, exclude_id=ann.id if ann else None)

        was_published = (ann and ann.status == 'published')
        if not was_published and status == 'published':
            published_at = now_ms()
        elif ann:
            published_at = ann.published_at
        else:
            published_at = 0 if status != 'published' else now_ms()

        if is_edit:
            ann.title = title
            ann.slug = slug
            ann.summary = summary
            ann.content = content
            ann.category = category
            ann.status = status
            ann.is_pinned = is_pinned
            ann.cover_image_url = cover_image_url
            ann.external_url = external_url
            ann.tags = tags
            ann.author = admin_user
            ann.published_at = published_at
            ann.updated_at = now_ms()
            ann.save()
        else:
            ann = Announcement(
                id=uuid_str(),
                title=title,
                slug=slug,
                summary=summary,
                content=content,
                category=category,
                status=status,
                is_pinned=is_pinned,
                cover_image_url=cover_image_url,
                external_url=external_url,
                tags=tags,
                author=admin_user,
                published_at=published_at,
                created_at=now_ms(),
                updated_at=now_ms(),
            )
            ann.save()

        _clear_news_cache()
        return redirect('web:admin_announcements')

    form_data = {}
    if ann:
        form_data = {
            'title': ann.title, 'summary': ann.summary, 'content': ann.content,
            'category': ann.category, 'status': ann.status, 'is_pinned': ann.is_pinned,
            'cover_image_url': ann.cover_image_url, 'external_url': ann.external_url,
            'tags': ann.tags, 'slug': ann.slug,
        }

    return render(request, 'admin_panel/announcement_form.html', {
        'is_admin': True,
        'active_page': 'announcements',
        'is_edit': is_edit,
        'announcement': ann,
        'form_data': form_data,
        'categories': [{'key': k, 'label': v['label'], 'icon': v['icon']} for k, v in CATEGORY_META.items()],
        'errors': [],
    })


def admin_announcement_draft_neby(request):
    """AJAX endpoint to trigger Neby AI blog post drafting."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    import json
    try:
        data = json.loads(request.body.decode('utf-8')) if request.body else request.POST
    except Exception:
        data = request.POST

    source = (data.get('source') or 'git').strip().lower()
    prompt = (data.get('prompt') or '').strip()
    feature_id = (data.get('feature_id') or '').strip()
    publish = bool(data.get('publish', False))

    from api.agent_blog import services as blog_services

    ann = None
    if source == 'git':
        ann = blog_services.draft_blog_from_git(publish=publish)
    elif source == 'spotlight':
        ann = blog_services.draft_blog_from_spotlight(feature_id=feature_id or None, publish=publish)
    elif source == 'prompt' and prompt:
        ann = blog_services.draft_blog_from_prompt(prompt_text=prompt, publish=publish)
    else:
        ann = blog_services.draft_blog_from_git(publish=publish)

    if not ann:
        return JsonResponse({'error': 'Failed to generate blog draft with Neby. Please try again.'}, status=500)

    _clear_news_cache()
    from django.urls import reverse
    return JsonResponse({
        'success': True,
        'announcement_id': ann.id,
        'title': ann.title,
        'slug': ann.slug,
        'summary': ann.summary,
        'category': ann.category,
        'tags': ann.tags,
        'edit_url': reverse('web:admin_announcement_edit', kwargs={'announcement_id': ann.id}),
    })