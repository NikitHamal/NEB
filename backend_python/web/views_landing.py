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
    'analytics', 'credits', 'my-avatar', 'past-papers', 'model-questions',
    'online-learning', 'faq', 'study-space', 'study-lab', 'canvas', 'notifications',
)

# Every level the library serves. The landing page lets a visitor pick one and shows where to
# start in it: ``items`` are (label, library query string) pairs, ``query`` opens the whole level.
LEVELS = [
    {'key': 'school', 'name': 'School', 'sub': 'Class 1 to 10, BLE and SEE', 'query': 'grade=Class+10',
     'items': [('Class 8', 'grade=Class+8'), ('Class 9', 'grade=Class+9'), ('Class 10', 'grade=Class+10'),
               ('Science', 'grade=Class+10&q=Science'), ('Mathematics', 'grade=Class+10&q=Mathematics'),
               ('English', 'grade=Class+10&q=English'), ('Social Studies', 'grade=Class+10&q=Social'),
               ('Computer', 'grade=Class+8&q=Computer')]},
    {'key': 'plus-two', 'name': 'Plus two', 'sub': 'Class 11 and 12, every stream', 'query': 'grade=Class+12',
     'items': [('Physics', 'grade=Class+12&q=Physics'), ('Chemistry', 'grade=Class+12&q=Chemistry'),
               ('Biology', 'grade=Class+12&q=Biology'), ('Mathematics', 'grade=Class+12&q=Mathematics'),
               ('Accountancy', 'grade=Class+12&q=Accountancy'), ('Economics', 'grade=Class+12&q=Economics'),
               ('Computer Science', 'grade=Class+12&q=Computer'), ('English', 'grade=Class+12&q=English')]},
    {'key': 'diploma', 'name': 'Diploma', 'sub': 'CTEVT and technical programmes', 'query': 'q=Diploma',
     'items': [('Civil', 'q=Diploma+Civil'), ('Computer', 'q=Diploma+Computer'), ('Electrical', 'q=Diploma+Electrical'),
               ('Pharmacy', 'q=Diploma+Pharmacy'), ('Health', 'q=Diploma+Health'), ('Agriculture', 'q=Diploma+Agriculture')]},
    {'key': 'bachelors', 'name': "Bachelor's", 'sub': 'Engineering, Medicine, Management, IT and more', 'query': 'grade=Bachelor',
     'items': [('BCA', 'q=BCA'), ('BBS', 'q=BBS'), ('BBA', 'q=BBA'), ('Engineering', 'q=Engineering'),
               ('Nursing', 'q=Nursing'), ('MBBS', 'q=MBBS'), ('BSc CSIT', 'q=CSIT')]},
    {'key': 'masters', 'name': "Master's", 'sub': 'TU, KU, PU and beyond', 'query': 'q=Master',
     'items': [('MBS', 'q=MBS'), ('MBA', 'q=MBA'), ('MEd', 'q=MEd'), ('MSc', 'q=MSc'), ('MA', 'q=MA')]},
    {'key': 'entrance', 'name': 'Entrance', 'sub': 'Medical, engineering and university entrance', 'query': 'q=Entrance',
     'items': [('IOE', 'q=IOE'), ('CEE', 'q=CEE'), ('BCA entrance', 'q=BCA+entrance'), ('CMAT', 'q=CMAT'),
               ('Model questions', 'q=Model+questions')]},
]

# The subjects that scroll past under the hero.
SUBJECTS = ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'English', 'Accountancy', 'Economics',
            'Computer Science', 'Social Studies', 'Nepali', 'Law', 'Education', 'Nursing', 'Engineering']

# The study books we write ourselves, one per class.
BOOK_CLASSES = ['8', '10', '11', '12']


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


LANDING_SEO = {
    'title': 'NEBians — Study materials. Study mates.',
    'description': 'Free notes, past papers and solved study books for every class, field and level in Nepal, and a forum where students answer each other.',
    'og_description': "Free notes, past papers and solved study books for every class, field and level, and a forum where Nepal's students help each other.",
    'path': '/',
}

ABOUT_SEO = {
    'title': 'About NEBians — Nepal\'s open learning community by Consica Labs',
    'description': 'NEBians is a free study platform for Nepal: notes, past papers, solved study books and a student forum for every class and level. Meet the team at Consica Labs.',
    'og_description': 'Free notes, past papers and a student forum for every level in Nepal. Meet the team behind NEBians at Consica Labs.',
    'path': '/about/',
}


@require_GET
def landing(request):
    from .views_og import CARD_VERSION
    ctx = {
        'signed_in': bool(_get_user_id(request)),
        'discussions': _live_discussions(),
        'levels': LEVELS,
        'subjects': SUBJECTS,
        'book_classes': BOOK_CLASSES,
        # The landing page carries its own head rather than using base.html,
        # so it has to name the card itself. Taking the version from the
        # renderer means a redesign bumps the URL here too.
        'og_card_version': CARD_VERSION,
        'seo': LANDING_SEO,
    }
    response = render(request, 'landing/landing.html', ctx)
    if not ctx['signed_in']:
        response['Cache-Control'] = 'private, max-age=60'
    return response


@require_GET
def about(request):
    from . import about_data
    from .views_og import CARD_VERSION
    ctx = {
        'signed_in': bool(_get_user_id(request)),
        'seo': ABOUT_SEO,
        'jsonld': about_data.jsonld(ABOUT_SEO),
        'team': about_data.team(),
        'pillars': about_data.PILLARS,
        'steps': about_data.STEPS,
        'promises': about_data.PROMISES,
        'anchor': '/',
        'current': 'about',
        'og_card_version': CARD_VERSION,
    }
    response = render(request, 'landing/about.html', ctx)
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
