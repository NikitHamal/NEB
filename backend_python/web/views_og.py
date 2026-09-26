"""The Open Graph card endpoint.

One URL per shareable thing: /og/<kind>/<key>.png. A scraper that has never
seen the page asks for the card by that URL alone, so everything the card says
has to be reconstructible from the key -- which is why the static pages live in
a table here rather than being passed in from the view that renders the page.

Drawing is in web/og_cards.py and has no Django in it. This module is the part
that knows about the database, the cache and the rate limiter.

Cards are cached under a signature of the values that went into them, so an
edited title produces a new cache entry instead of a stale card, and the old
entry expires on its own.
"""
from .view_helpers import *  # noqa: F401,F403

import hashlib
import re

from . import og_cards


SITE = 'https://nebians.consica.com.np'
_SAFE_KEY = re.compile(r'^[A-Za-z0-9._/-]{1,120}$')

# Static pages. `kicker` sits above the title in the subject accent, `meta` is
# the dot-separated line under it, `hero` names a drawing in og_cards.HEROES.
PAGES = {
    'default': {
        'kicker': 'NEBians', 'title': "Nepal's Learning Community",
        'meta': ('Free study material', 'nebians.consica.com.np'), 'hero': 'mark',
    },
    'home': {
        'kicker': 'NEBians', 'title': "Nepal's Learning Community",
        'meta': ('Free study material', 'nebians.consica.com.np'), 'hero': 'mark',
    },
    'library': {
        'kicker': 'Library', 'title': 'Every paper, note and book in one place',
        'meta': ('Free to read', 'Free to download'), 'hero': 'books',
    },
    'past-papers': {
        'kicker': 'Past papers', 'title': 'NEB past question papers',
        'meta': ('Class 11 and 12', 'Every subject'), 'hero': 'paper',
    },
    'model-questions': {
        'kicker': 'Model questions', 'title': 'NEB model questions and solutions',
        'meta': ('Every grade', 'With worked solutions'), 'hero': 'paper',
    },
    'forum': {
        'kicker': 'Forum', 'title': 'Ask anything. Someone has sat this exam.',
        'meta': ('Students', 'Teachers'), 'hero': 'bubbles',
    },
    'leaderboard': {
        'kicker': 'Forum', 'title': 'The people who keep NEBians running',
        'meta': ('Leaderboard',), 'hero': 'bubbles',
    },
    'news': {
        'kicker': 'Blog', 'title': 'NEB news, notices and results',
        'meta': ('Updated as it happens',), 'hero': 'paper',
    },
    'study-lab': {
        'kicker': 'Study Lab', 'title': 'Turn any document into a way to study',
        'meta': ('Summaries', 'Quizzes', 'Flashcards'), 'hero': 'flask',
    },
    'canvas': {
        'kicker': 'Canvas', 'title': 'Think out loud on an infinite board',
        'meta': ('AI study canvas',), 'hero': 'graph',
    },
    'tools': {
        'kicker': 'Tools', 'title': 'Small tools that save a long evening',
        'meta': ('Free', 'No sign-up to try'), 'hero': 'flask',
    },
    'results': {
        'kicker': 'Results', 'title': 'Check your NEB and SEE result',
        'meta': ('Symbol number', 'Full gradesheet'), 'hero': 'paper',
    },
    'requests': {
        'kicker': 'Requests', 'title': 'Ask for the notes nobody has uploaded yet',
        'meta': ('Resource requests',), 'hero': 'bubbles',
    },
    'upload': {
        'kicker': 'Contribute', 'title': 'Share the notes that got you through it',
        'meta': ('Free to upload',), 'hero': 'books',
    },
    'online-learning': {
        'kicker': 'Online learning', 'title': 'Learn online, free, from anywhere in Nepal',
        'meta': ('Open to everyone',), 'hero': 'books',
    },
    'privacy': {
        'kicker': 'Legal', 'title': 'Privacy policy', 'meta': ('NEBians',), 'hero': 'paper',
    },
    'terms': {
        'kicker': 'Legal', 'title': 'Terms of service', 'meta': ('NEBians',), 'hero': 'paper',
    },
    'copyright': {
        'kicker': 'Legal', 'title': 'Copyright and takedown',
        'meta': ('NEBians',), 'hero': 'paper',
    },
}


def card_url(kind, key=''):
    """Absolute URL of a card, for the og:image tag."""
    key = str(key or '').strip('/')
    return '%s/og/%s/%s.png' % (SITE, kind, key) if key else '%s/og/page/default.png' % SITE


# ── What each kind puts on the card ───────────────────────────────────────

def _page_card(key):
    spec = PAGES.get(key)
    if spec is None:
        raise Http404('No card for that page')
    return dict(spec)


def _faq_card():
    from . import faq as faq_data
    return {
        'kicker': 'Help centre', 'title': 'Questions, answered.',
        'meta': ('%d answers' % faq_data.question_count(), 'nebians.consica.com.np'),
        'hero': 'question',
    }


# Resource types that are a question paper rather than a set of notes. The
# drawing follows the kicker, not the other way round.
_PAPERY = ('paper', 'question', 'model', 'exam', 'solution', 'mock')


def _resource_card(resource_id):
    try:
        res = Resource.objects.only(
            'id', 'title', 'subject', 'grade_level', 'type', 'exam_type',
            'year', 'approval_status',
        ).get(id=resource_id)
    except Resource.DoesNotExist:
        raise Http404('Resource not found')
    if res.approval_status != 'approved':
        raise Http404('Resource not found')

    subject = (res.subject or '').split(',')[0].strip()
    kicker = (res.exam_type or res.type or 'Resource').strip()
    if kicker.lower() in ('pdf', 'note', 'notes', 'document'):
        kicker = 'Notes' if 'note' in kicker.lower() else 'Resource'
    meta = [p for p in (res.grade_level, subject, res.year) if p]
    hero = 'paper' if any(w in kicker.lower() for w in _PAPERY) else 'books'
    return {
        'kicker': kicker, 'title': res.title, 'meta': tuple(meta[:3]),
        'subject': subject, 'hero': hero, 'seed': res.id,
    }


def _post_card(post_id):
    try:
        post = Post.objects.only(
            'id', 'title', 'category', 'reply_count', 'is_archived',
        ).get(id=post_id)
    except Post.DoesNotExist:
        raise Http404('Post not found')
    if post.is_archived:
        raise Http404('Post not found')

    replies = post.reply_count or 0
    meta = [post.category] if post.category else []
    if replies:
        meta.append('%d repl%s' % (replies, 'y' if replies == 1 else 'ies'))
    return {
        'kicker': 'Forum', 'title': post.title, 'meta': tuple(meta),
        'subject': post.category or '', 'hero': 'bubbles', 'seed': post.id,
    }


def _news_card(slug):
    from api.models import Announcement
    try:
        item = Announcement.objects.only(
            'id', 'title', 'slug', 'category', 'status',
        ).get(slug=slug)
    except Announcement.DoesNotExist:
        raise Http404('Article not found')
    if item.status != 'published':
        raise Http404('Article not found')

    label = dict(Announcement.CATEGORY_CHOICES).get(item.category, 'Blog')
    return {
        'kicker': label, 'title': item.title, 'meta': ('NEBians blog',),
        'hero': 'paper', 'seed': item.slug,
    }


def _subject_card(key):
    """key is `class-12/physics`, the same pair the subject page takes."""
    parts = [p for p in key.split('/') if p]
    if len(parts) != 2:
        raise Http404('No such subject')
    grade = curriculum.get_grade_db_value(parts[0])
    subject = curriculum.get_subject_db_value(parts[1])
    if not grade or not subject:
        raise Http404('No such subject')
    return {
        'kicker': grade, 'title': subject, 'meta': (grade, 'Notes, papers, solutions'),
        'subject': subject, 'hero': 'books', 'seed': key,
    }


def _profile_card(username):
    from .views_profile import _profile_card_avatar
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User not found')

    # A locked profile gets a card with a name on it and nothing else. The page
    # behind it is gated; the preview should not be the way round that.
    locked = bool(getattr(user, 'is_locked', False))

    avatar = None
    if not locked and (getattr(user, 'photo_url', '') or '').strip():
        try:
            avatar = _profile_card_avatar(user, og_cards.HERO_R * 2 * og_cards.SS)
        except Exception:
            # A card without a photo is a card; a 500 on an og:image is not.
            avatar = None

    meta = ['@' + (user.username or 'nebian')]
    if not locked:
        posts = getattr(user, 'post_count', 0) or 0
        followers = getattr(user, 'follower_count', 0) or 0
        if posts:
            meta.append('%s post%s' % (_short_count(posts), '' if posts == 1 else 's'))
        if followers:
            meta.append('%s follower%s' % (_short_count(followers),
                                           '' if followers == 1 else 's'))
    return {
        'kicker': 'Profile',
        'title': user.display_name or user.username or 'NEBian',
        'meta': tuple(meta[:3]), 'hero': 'avatar', 'avatar': avatar,
        'seed': user.username or '',
    }


def _short_count(n):
    if n >= 1000000:
        return ('%.1f' % (n / 1000000.0)).rstrip('0').rstrip('.') + 'm'
    if n >= 1000:
        return ('%.1f' % (n / 1000.0)).rstrip('0').rstrip('.') + 'k'
    return str(n)


KINDS = {
    'page': _page_card,
    'resource': _resource_card,
    'post': _post_card,
    'news': _news_card,
    'subject': _subject_card,
    'profile': _profile_card,
}


# ── The endpoint ──────────────────────────────────────────────────────────

def _render_response(kind, key, spec):
    """Draw, cache and serve. Caching is keyed on what the card says, not on
    when it was asked for, so an edit invalidates it and nothing else does."""
    avatar = spec.pop('avatar', None)
    sig_src = repr(sorted(spec.items())) + ('|photo' if avatar is not None else '')
    sig = hashlib.sha256(sig_src.encode('utf-8')).hexdigest()[:20]
    cache_key = 'og_card_png:%s:%s' % (kind, sig)

    png = cache.get(cache_key)
    if png is None:
        img = og_cards.render(kind, spec.get('title') or 'NEBians',
                              meta=spec.get('meta', ()),
                              kicker=spec.get('kicker', ''),
                              subject=spec.get('subject', ''),
                              seed=spec.get('seed', '') or key,
                              hero=spec.get('hero', 'mark'),
                              avatar=avatar)
        png = og_cards.to_png(img)
        cache.set(cache_key, png, 24 * 3600)

    resp = HttpResponse(png, content_type='image/png')
    # A day in shared caches. Scrapers refetch rarely and the signature in the
    # cache key already handles edits on our side.
    resp['Cache-Control'] = 'public, max-age=86400'
    resp['X-Content-Type-Options'] = 'nosniff'
    return resp


def og_card(request, kind, key):
    """GET /og/<kind>/<key>.png"""
    if _rate_limit(request, 'og_card', 120, 60, by_ip=True):
        return HttpResponse(status=429)

    key = (key or '').strip('/')
    if key.endswith('.png'):
        key = key[:-4]

    if kind == 'page' and key == 'faq':
        spec = _faq_card()
    else:
        builder = KINDS.get(kind)
        if builder is None:
            raise Http404('No such card')
        try:
            spec = builder(key)
        except Http404:
            raise
        except Exception:
            raise Http404('No such card')

    return _render_response(kind, key, spec)


# ── Wiring the cards into every page ──────────────────────────────────────
# A context processor rather than a line in each of forty views: the card a
# page wants is a function of the route, and the route is something the
# processor can see. A view that wants something else just puts og_image_url
# in its own context -- the processor leaves an existing value alone.

_ROUTE_PAGES = {
    'home': 'home',
    'library': 'library',
    'past_papers': 'past-papers',
    'model_questions': 'model-questions',
    'online_learning': 'online-learning',
    'faq': 'faq',
    'forum': 'forum',
    'forum_categories': 'forum',
    'create_post': 'forum',
    'leaderboard': 'leaderboard',
    'news_list': 'news',
    'results_guide': 'results',
    'result_check': 'results',
    'tools_hub': 'tools',
    'doc_tools': 'tools',
    'intelligence_tools': 'tools',
    'whisper_tool': 'tools',
    'tts_tool': 'tools',
    'study_lab': 'study-lab',
    'canvas': 'canvas',
    'upload_resource': 'upload',
    'resource_requests': 'requests',
    'privacy_policy': 'privacy',
    'terms_of_service': 'terms',
    'copyright_takedown': 'copyright',
    'search': 'library',
    'interactive_hub': 'study-lab',
}

# Routes whose card is drawn from the thing the URL names.
_ROUTE_OBJECTS = {
    'reader': ('resource', lambda kw: kw.get('resource_id')),
    'forum_post': ('post', lambda kw: kw.get('post_id')),
    'news_detail': ('news', lambda kw: kw.get('slug')),
    'profile': ('profile', lambda kw: kw.get('username')),
    'subject_page': ('subject', lambda kw: '%s/%s' % (kw.get('grade_slug', ''),
                                                      kw.get('subject_slug', ''))),
}

_ALT = {
    'resource': 'A NEBians card for this study resource',
    'post': 'A NEBians card for this discussion',
    'news': 'A NEBians card for this article',
    'profile': 'A NEBians profile card',
    'subject': 'A NEBians card for this subject',
    'page': "NEBians — Nepal's Learning Community",
}


def og_image_context(request):
    """Template context: og_image_url and og_image_alt for the current route."""
    match = getattr(request, 'resolver_match', None)
    name = getattr(match, 'url_name', '') if match else ''
    if not name:
        return {}

    page = _ROUTE_PAGES.get(name)
    if page:
        return {'og_image_url': card_url('page', page), 'og_image_alt': _ALT['page']}

    obj = _ROUTE_OBJECTS.get(name)
    if obj:
        kind, key_of = obj
        key = (key_of(getattr(match, 'kwargs', {}) or {}) or '').strip('/')
        # Ids, slugs and usernames only. A key that needs escaping is a key
        # this route does not actually have, so fall through to the default.
        if key and _SAFE_KEY.match(key):
            return {'og_image_url': card_url(kind, key), 'og_image_alt': _ALT[kind]}
    return {}
