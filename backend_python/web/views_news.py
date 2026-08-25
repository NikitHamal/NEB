"""News / Announcements + interactive Results guide views."""
import json
import re
import unicodedata
from django.core.cache import cache
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from api import services
from api.models import Announcement, BlogComment, BlogCommentLike, Bookmark, User
from api.news_serializers import (
    CATEGORY_META,
    render_content_html,
    serialize_announcement as _serialize_announcement_base,
)
from api.utils import now_ms, uuid_str

from .view_helpers import _avatar_url, _ctx, _get_user_id, _user_badge_info


def _serialize_announcement(a, include_content=False):
    """Thin wrapper over the shared API serializer (web templates consume it)."""
    return _serialize_announcement_base(a, include_content=include_content)


def _slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or 'announcement'


def _unique_slug(base_slug, exclude_id=None):
    slug = base_slug
    n = 1
    qs = Announcement.objects.all()
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    while qs.filter(slug=slug).exists():
        n += 1
        slug = f'{base_slug}-{n}'
    return slug


def news_list(request):
    from django.core.paginator import Paginator

    category = request.GET.get('category', '').strip()
    tag = request.GET.get('tag', '').strip()
    try:
        page_num = max(1, int(request.GET.get('page', '1')))
    except (TypeError, ValueError):
        page_num = 1
    cache_key = f'news_list:v2:{category}:{tag}'
    all_items = cache.get(cache_key)
    if all_items is None:
        qs = Announcement.objects.select_related('author').filter(status='published')
        if category:
            qs = qs.filter(category=category)
        if tag:
            qs = qs.filter(tags__icontains=tag)
        qs = qs.order_by('-is_pinned', '-published_at')
        all_items = [_serialize_announcement(a) for a in qs[:300]]
        cache.set(cache_key, all_items, 120)
    paginator = Paginator(all_items, 12)
    page_obj = paginator.get_page(page_num)
    categories = [
        {'key': k, 'icon': v['icon'], 'label': v['label'], 'color': v['color']}
        for k, v in CATEGORY_META.items()
    ]

    def _page_url(p):
        params = {}
        if category:
            params['category'] = category
        if tag:
            params['tag'] = tag
        if p > 1:
            params['page'] = p
        query = '&'.join(f'{k}={v}' for k, v in params.items())
        return f'{request.path}?{query}' if query else request.path

    return render(request, 'web/news.html', _ctx(request,
        announcements=page_obj.object_list,
        page_obj=page_obj,
        page_urls={
            'prev': _page_url(page_obj.previous_page_number()) if page_obj.has_previous() else None,
            'next': _page_url(page_obj.next_page_number()) if page_obj.has_next() else None,
        },
        categories=categories,
        current_category=category,
        current_tag=tag,
    ))





def news_detail(request, slug):
    try:
        a = Announcement.objects.select_related('author').get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        raise Http404('Announcement not found')

    user_id = _get_user_id(request)

    view_key = f'ann_viewed_{a.id}'
    if not request.session.get(view_key):
        Announcement.objects.filter(pk=a.id).update(view_count=F('view_count') + 1)
        request.session[view_key] = True
        a.view_count += 1

    item = _serialize_announcement(a, include_content=True)

    # Serialize blog comments in forum–reply format
    top_level_replies, children_map, all_usernames = _serialize_blog_comments(a, user_id)

    related = Announcement.objects.filter(
        status='published', category=a.category
    ).exclude(pk=a.id).order_by('-published_at')[:4]
    related_items = [_serialize_announcement(r) for r in related]

    return render(request, 'web/news_detail.html', _ctx(request,
        announcement=item,
        related=related_items,
        top_level_replies=top_level_replies,
        children_map=children_map,
        all_usernames=all_usernames,
        comment_target_type='blog_comment',
    ))


def _blog_comment_dict(c, user_id, liked_ids, bookmarked_ids):
    """One comment in the exact forum-reply shape, plus legacy keys kept so
    older Android builds (author_name/text fields) keep rendering."""
    parent_id = c.parent_comment_id or ''
    return {
        'id': c.id,
        'authorId': c.author_id,
        'authorName': c.author.username,
        'authorPhotoUrl': _avatar_url(c.author),
        'authorBadgeInfo': _user_badge_info(c.author),
        'parentReplyId': parent_id,
        'parentCommentId': parent_id,
        'content': c.text,
        'thumbsUpCount': c.like_count,
        'childCount': c.reply_count,
        'isEdited': c.is_edited,
        'createdAt': c.created_at,
        'isThumbedUp': c.id in liked_ids,
        'isBookmarked': c.id in bookmarked_ids,
        'isOwner': bool(user_id and str(user_id) == str(c.author_id)),
        'isFollowed': False,
        'childAuthors': [],
        # Legacy durability for older app builds.
        'author_name': c.author.username,
        'author_initials': (c.author.username or 'N')[:2].upper(),
        'author_photo': _avatar_url(c.author),
        'text': c.text,
        'created_at': c.created_at,
    }


def _blog_comment_liked_bookmarked_ids(comments_list, user_id):
    if not (user_id and comments_list):
        return set(), set()
    liked_ids = set(BlogCommentLike.objects.filter(
        comment_id__in=[c.id for c in comments_list], user_id=user_id
    ).values_list('comment_id', flat=True))
    bookmarked_ids = set(Bookmark.objects.filter(
        user_id=user_id, target_type='blog_comment',
        target_id__in=[c.id for c in comments_list]
    ).values_list('target_id', flat=True))
    return liked_ids, bookmarked_ids


def _serialize_blog_comments(announcement, user_id=None):
    qs = BlogComment.objects.filter(announcement=announcement).select_related('author').order_by('created_at')
    comments_list = list(qs)
    liked_ids, bookmarked_ids = _blog_comment_liked_bookmarked_ids(comments_list, user_id)
    result = [_blog_comment_dict(c, user_id, liked_ids, bookmarked_ids) for c in comments_list]
    top_level = [r for r in result if not r['parentReplyId']]
    children_map = {}
    for r in result:
        pid = r['parentReplyId']
        if pid:
            children_map.setdefault(pid, []).append(r)
    all_usernames = list(set(r['authorName'] for r in result if r['authorName']))
    return top_level, children_map, all_usernames


@require_GET
def ajax_blog_comments(request, slug):
    try:
        announcement = Announcement.objects.get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Announcement not found'}, status=404)
    user_id = _get_user_id(request)
    comments_list = list(
        BlogComment.objects.filter(announcement=announcement).select_related('author').order_by('created_at')
    )
    liked_ids, bookmarked_ids = _blog_comment_liked_bookmarked_ids(comments_list, user_id)
    payload = [_blog_comment_dict(c, user_id, liked_ids, bookmarked_ids) for c in comments_list]
    return JsonResponse({'ok': True, 'comments': payload})


@require_POST
def ajax_blog_comment(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'ok': False, 'error': 'Please sign in to comment'}, status=401)
    try:
        payload = json.loads(request.body.decode('utf-8')) if request.content_type == 'application/json' else request.POST
    except (ValueError, UnicodeDecodeError):
        payload = request.POST
    slug = str(payload.get('slug', '')).strip()
    text = str(payload.get('text', '')).strip()
    parent_comment_id = payload.get('parentCommentId') or None
    if not slug or not text:
        return JsonResponse({'ok': False, 'error': 'Missing slug or text'}, status=400)
    if len(text) > 4000:
        return JsonResponse({'ok': False, 'error': 'Comment is too long'}, status=400)
    try:
        announcement = Announcement.objects.get(slug=slug, status='published')
        user = User.objects.get(pk=user_id)
    except Announcement.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Announcement not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'User not found'}, status=401)
    created = services.create_blog_comment(user, slug, text, parent_comment_id)
    if not created:
        return JsonResponse({'ok': False, 'error': 'Failed to create comment'}, status=500)
    try:
        fresh = BlogComment.objects.select_related('author').get(pk=created['id'])
        comment = _blog_comment_dict(fresh, user_id, set(), set())
    except BlogComment.DoesNotExist:
        comment = created
    return JsonResponse({
        'ok': True,
        'comment': comment,
    })


def results_guide(request):
    """Interactive step-by-step guide for checking NEB results + grade calculator."""
    pinned = Announcement.objects.filter(
        status='published', category='exam_results', is_pinned=True
    ).order_by('-published_at')[:1]
    recent_results_news = Announcement.objects.filter(
        status='published', category='exam_results'
    ).order_by('-published_at')[:6]

    pinned_item = _serialize_announcement(pinned[0]) if pinned else None
    recent_items = [_serialize_announcement(a) for a in recent_results_news]

    steps = [
        {
            'num': 1,
            'icon': 'badge',
            'title': 'Keep your credentials ready',
            'desc': 'Have your <strong>symbol number</strong>, <strong>date of birth</strong>, and (for class 12) your <strong>registration number</strong> on hand. These are printed on your admit card.',
        },
        {
            'num': 2,
            'icon': 'language',
            'title': 'Visit the official NEB website',
            'desc': 'Go to <a href="https://neb.gov.np" target="_blank" rel="noopener">neb.gov.np</a> and look for the "Results" section. Direct result links are also posted below in the Quick Links card.',
            'links': [
                {'label': 'NEB Official Site', 'url': 'https://neb.gov.np'},
                {'label': 'Class 12 Results', 'url': 'https://neb.gov.np/results/'},
                {'label': 'Class 11 Results', 'url': 'https://neb.gov.np/results/'},
            ],
        },
        {
            'num': 3,
            'icon': 'edit_note',
            'title': 'Enter your symbol number',
            'desc': 'Type your symbol number exactly as printed. Double-check the digits — a single wrong character will show "Record not found".',
        },
        {
            'num': 4,
            'icon': 'cake',
            'title': 'Select your date of birth',
            'desc': 'Pick your DOB in the calendar (BS or AD as the form requires). Make sure the year is correct — students often mix up the BS/AD year.',
        },
        {
            'num': 5,
            'icon': 'fact_check',
            'title': 'Submit and view your result',
            'desc': 'Click "Submit" / "View Result". Your subject-wise grades, GPA, and division will be displayed. Take a screenshot or print the page for your records.',
        },
        {
            'num': 6,
            'icon': 'sms',
            'title': 'Alternative: SMS / IVR',
            'desc': 'If the website is down due to traffic, you can get results via SMS. Type <code>NEB &lt;symbol_number&gt;</code> and send to <strong>1600</strong> (NTC) or use your telecom\'s result shortcode. IVR: dial 1600 and follow the voice prompts.',
        },
    ]

    grade_scale = [
        {'grade': 'A+', 'range': '90–100', 'gpa': '4.0', 'point': 'Outstanding'},
        {'grade': 'A',  'range': '80–89',  'gpa': '3.6', 'point': 'Excellent'},
        {'grade': 'B+', 'range': '70–79',  'gpa': '3.2', 'point': 'Very Good'},
        {'grade': 'B',  'range': '60–69',  'gpa': '2.8', 'point': 'Good'},
        {'grade': 'C+', 'range': '50–59',  'gpa': '2.4', 'point': 'Satisfactory'},
        {'grade': 'C',  'range': '40–49',  'gpa': '2.0', 'point': 'Acceptable'},
        {'grade': 'D+', 'range': '30–39',  'gpa': '1.6', 'point': 'Partially Acceptable'},
        {'grade': 'D',  'range': '20–29',  'gpa': '1.2', 'point': 'Insufficient'},
        {'grade': 'E',  'range': '0–19',   'gpa': '0.8', 'point': 'Very Insufficient'},
    ]

    quick_links = [
        {'label': 'NEB Official Website', 'url': 'https://neb.gov.np', 'icon': 'public'},
        {'label': 'Check Result Instantly', 'url': '/results/check/', 'icon': 'search'},
        {'label': 'Class 12 Result', 'url': 'https://neb.ntc.net.np/', 'icon': 'school'},
        {'label': 'SEE Result', 'url': 'https://see.ntc.net.np/', 'icon': 'school'},
        {'label': 'Examination Routine', 'url': 'https://neb.gov.np/routines/', 'icon': 'event'},
        {'label': 'Re-totaling / Re-evaluation', 'url': 'https://neb.gov.np/', 'icon': 'autorenew'},
    ]

    return render(request, 'web/results_guide.html', _ctx(request,
        pinned=pinned_item,
        recent_news=recent_items,
        steps=steps,
        grade_scale=grade_scale,
        quick_links=quick_links,
    ))