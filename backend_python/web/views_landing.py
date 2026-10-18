"""The public landing page at ``/`` and the redirects for pages that moved to ``/app/``.

The landing page is its own small document: no base.html, no app bundles, one CSS file,
one deferred JS file, self-hosted fonts. The only data it shows is the live forum threads,
cached, so it is cheap to serve.
"""
import re
from datetime import datetime, timezone as dt_timezone

from django.core.cache import cache
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.timesince import timesince
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET

from api.models import Post
from api.services import AVATAR_FIELDS, avatar_or_photo_url

from .view_helpers import _get_user_id

LEGACY_PREFIXES = (
    'library', 'forum', 'marketplace', 'interactive', 'subject', 'search', 'news', 'results',
    'tools', 'reader', 'resource', 'upload', 'requests', 'profile', 'settings', 'bookmarks',
    'analytics', 'credits', 'code', 'my-avatar', 'past-papers', 'model-questions',
    'online-learning', 'faq', 'lazy', 'study-space', 'study-lab', 'canvas', 'notifications',
)

# Every level the library serves. The landing page lists them; each opens the library on it.
LEVELS = [
    {'name': 'School', 'detail': 'Class 1 to 10 · BLE · SEE', 'query': 'grade=Class+10'},
    {'name': 'Plus two', 'detail': 'Class 11 and 12 · Science, Management, Humanities, Law, Education', 'query': 'grade=Class+12'},
    {'name': 'Diploma', 'detail': 'CTEVT and technical programmes', 'query': 'q=Diploma'},
    {'name': "Bachelor's", 'detail': 'Engineering, Medicine, Nursing, Management, IT, Arts', 'query': 'grade=Bachelor'},
    {'name': "Master's", 'detail': 'TU, KU, PU and beyond', 'query': 'q=Master'},
    {'name': 'Entrance', 'detail': 'Medical, engineering and university entrance preparation', 'query': 'q=Entrance'},
]



def _excerpt(text, limit=170):
    """Plain text from a post body: no HTML, no markdown marks, no LaTeX delimiters."""
    plain = strip_tags(text or '')
    plain = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', plain)
    plain = re.sub(r'[`*_#>~|]|\$\$?|\\[()\[\]]', '', plain)
    plain = re.sub(r'\s+', ' ', plain).strip()
    return plain if len(plain) <= limit else plain[:limit].rsplit(' ', 1)[0] + '…'


def _live_discussions():
    data = cache.get('landing_posts_v3')
    if data is None:
        rows = (Post.objects.select_related('user')
                .filter(is_archived=False, is_anonymous=False, user__email_verified=True)
                .order_by('-reply_count', '-created_at')
                .only('id', 'title', 'content', 'category', 'reply_count', 'thumbs_up_count', 'view_count',
                      'created_at', 'user__display_name', *('user__' + f for f in AVATAR_FIELDS))[:4])
        now = timezone.now()
        data = []
        for p in rows:
            name = (p.user.display_name or p.user.username) if p.user else 'A member'
            when = datetime.fromtimestamp((p.created_at or 0) / 1000, tz=dt_timezone.utc)
            data.append({
                'id': p.id, 'title': p.title, 'excerpt': _excerpt(p.content),
                'category': p.category or 'General',
                'replies': p.reply_count or 0, 'likes': p.thumbs_up_count or 0, 'views': p.view_count or 0,
                'ago': timesince(when, now).split(',')[0],
                'name': name, 'initial': (name[:1] or 'N').upper(),
                'avatar': avatar_or_photo_url(p.user) if p.user else '',
            })
        cache.set('landing_posts_v3', data, 600)
    return data


@require_GET
def landing(request):
    ctx = {
        'signed_in': bool(_get_user_id(request)),
        'discussions': _live_discussions(),
        'levels': LEVELS,
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
