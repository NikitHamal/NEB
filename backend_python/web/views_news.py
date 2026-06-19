"""News / Announcements + interactive Results guide views."""
import re
import unicodedata
from django.core.cache import cache
from django.db.models import F
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from api.models import Announcement
from api.utils import now_ms, uuid_str

from .view_helpers import _ctx, _get_user_id, _is_staff_admin


CATEGORY_META = {
    'exam_results': {'icon': 'fact_check', 'label': 'Exam Results', 'color': '#dc2626'},
    'notice':       {'icon': 'campaign',     'label': 'Notice',       'color': '#2563eb'},
    'event':        {'icon': 'event',       'label': 'Event',        'color': '#7c3aed'},
    'update':       {'icon': 'upgrade',     'label': 'Update',       'color': '#059669'},
    'alert':        {'icon': 'warning',     'label': 'Alert',        'color': '#d97706'},
    'general':      {'icon': 'info',        'label': 'General',      'color': '#6b7280'},
}


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


def _serialize_announcement(a, include_content=False):
    meta = CATEGORY_META.get(a.category, CATEGORY_META['general'])
    data = {
        'id': a.id,
        'title': a.title,
        'slug': a.slug,
        'summary': a.summary or '',
        'category': a.category,
        'category_icon': meta['icon'],
        'category_label': meta['label'],
        'category_color': meta['color'],
        'is_pinned': a.is_pinned,
        'cover_image_url': a.cover_image_url or '',
        'external_url': a.external_url or '',
        'tags': a.tags or '',
        'author_name': (a.author.display_name or a.author.username) if a.author else 'NEBians Team',
        'author_photo': (a.author.photo_url or '') if a.author else '',
        'published_at': a.published_at,
        'created_at': a.created_at,
        'view_count': a.view_count,
    }
    if include_content:
        data['content'] = a.content or ''
    return data


def news_list(request):
    category = request.GET.get('category', '').strip()
    tag = request.GET.get('tag', '').strip()
    cache_key = f'news_list:{category}:{tag}'
    items = cache.get(cache_key)
    if items is None:
        qs = Announcement.objects.select_related('author').filter(status='published')
        if category:
            qs = qs.filter(category=category)
        if tag:
            qs = qs.filter(tags__icontains=tag)
        qs = qs.order_by('-is_pinned', '-published_at')
        items = [_serialize_announcement(a) for a in qs[:60]]
        cache.set(cache_key, items, 120)
    categories = [
        {'key': k, 'icon': v['icon'], 'label': v['label'], 'color': v['color']}
        for k, v in CATEGORY_META.items()
    ]
    return render(request, 'web/news.html', _ctx(request,
        announcements=items,
        categories=categories,
        current_category=category,
        current_tag=tag,
    ))


def news_detail(request, slug):
    try:
        a = Announcement.objects.select_related('author').get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        raise Http404('Announcement not found')

    view_key = f'ann_viewed_{a.id}'
    if not request.session.get(view_key):
        Announcement.objects.filter(pk=a.id).update(view_count=F('view_count') + 1)
        request.session[view_key] = True
        a.view_count += 1

    item = _serialize_announcement(a, include_content=True)

    related = Announcement.objects.filter(
        status='published', category=a.category
    ).exclude(pk=a.id).order_by('-published_at')[:4]
    related_items = [_serialize_announcement(r) for r in related]

    return render(request, 'web/news_detail.html', _ctx(request,
        announcement=item,
        related=related_items,
    ))


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