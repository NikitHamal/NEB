"""The public landing page at ``/`` and the redirects for pages that moved to ``/app/``.

The landing page is its own small document: no base.html, no app bundles, one CSS file,
one deferred JS file, self-hosted fonts. The only data it shows is the live forum threads,
cached, so it is cheap to serve.
"""
from django.core.cache import cache
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET

from api.models import Post

from .view_helpers import _get_user_id

LEGACY_PREFIXES = (
    'library', 'forum', 'marketplace', 'interactive', 'subject', 'search', 'news', 'results',
    'tools', 'reader', 'resource', 'upload', 'requests', 'profile', 'settings', 'bookmarks',
    'analytics', 'credits', 'code', 'my-avatar', 'past-papers', 'model-questions',
    'online-learning', 'faq', 'lazy', 'study-space', 'study-lab', 'canvas', 'notifications',
)

GRADES = [
    {'key': 'class-8', 'label': 'Class 8', 'exam': 'BLE',
     'subjects': ['Science', 'Mathematics', 'English', 'Nepali', 'Social Studies', 'Computer Science']},
    {'key': 'class-10', 'label': 'Class 10', 'exam': 'SEE',
     'subjects': ['Science', 'Mathematics', 'Optional Mathematics', 'English', 'Nepali', 'Social Studies',
                  'Accountancy', 'Economics']},
    {'key': 'class-11', 'label': 'Class 11', 'exam': 'NEB',
     'subjects': ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science', 'English', 'Nepali']},
    {'key': 'class-12', 'label': 'Class 12', 'exam': 'NEB',
     'subjects': ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science', 'English', 'Nepali']},
    {'key': 'bachelor', 'label': 'Bachelor', 'exam': 'TU · KU · PU',
     'subjects': ['Nursing', 'Engineering', 'Management', 'Computer Science']},
]
for _g in GRADES:
    _g['subjects'] = [{'name': n, 'slug': n.lower().replace(' & ', '-').replace(' ', '-')} for n in _g['subjects']]


def _live_discussions():
    data = cache.get('landing_posts_v2')
    if data is None:
        rows = (Post.objects.select_related('user')
                .filter(is_archived=False, is_anonymous=False, user__email_verified=True)
                .order_by('-reply_count', '-created_at')
                .only('id', 'title', 'category', 'reply_count', 'thumbs_up_count',
                      'user__username', 'user__display_name')[:4])
        data = [{
            'id': p.id, 'title': p.title, 'category': p.category or 'General',
            'replies': p.reply_count or 0, 'likes': p.thumbs_up_count or 0,
            'name': (p.user.display_name or p.user.username) if p.user else 'A member',
            'initial': ((p.user.display_name or p.user.username or 'N')[:1] if p.user else 'N').upper(),
        } for p in rows]
        cache.set('landing_posts_v2', data, 600)
    return data


@require_GET
def landing(request):
    ctx = {
        'signed_in': bool(_get_user_id(request)),
        'discussions': _live_discussions(),
        'grades': GRADES,
    }
    response = render(request, 'landing/landing.html', ctx)
    if not ctx['signed_in']:
        response['Cache-Control'] = 'private, max-age=60'
    return response


def legacy_redirect(request, path):
    target = '/app/' + path
    if request.META.get('QUERY_STRING'):
        target += '?' + request.META['QUERY_STRING']
    response = HttpResponsePermanentRedirect(target)
    response.status_code = 308
    return response
