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
from api.models import Post, Resource, User
from django.core.cache import cache
from django.http import Http404, HttpResponse
from . import curriculum
from .view_helpers import _rate_limit

import hashlib
import re

from . import og_cards


SITE = 'https://nebians.consica.com.np'
_SAFE_KEY = re.compile(r'^[A-Za-z0-9._/-]{1,120}$')

# Bumped whenever the drawing changes rather than the words. The cache is keyed
# on what a card says, which is right for a title edit and wrong for a redesign:
# without this, a new renderer keeps serving the previous design for a day, and
# every scraper that already fetched the URL keeps its own copy for longer. The
# version goes into both the cache key and the URL, so a redesign is a new
# address to a crawler rather than a changed picture at the same one.
CARD_VERSION = 4

# Static pages. `kicker` sits above the title in the subject accent, `meta` is
# the dot-separated line under it, `hero` names a drawing in og_cards.HEROES.
PAGES = {
    # The address line at the foot already carries the domain, so the meta
    # line here does not repeat it.
    'default': {
        'kicker': 'NEBians', 'title': "Nepal's Learning Community",
        'meta': ('Free study material', 'Every subject, every level'), 'hero': 'mark',
    },
    'home': {
        'kicker': 'NEBians', 'title': "Nepal's Learning Community",
        'meta': ('Free study material', 'Every subject, every level'), 'hero': 'mark',
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
    'syllabus': {
        'kicker': 'Syllabus', 'title': 'The NEB syllabus, unit by unit',
        'meta': ('Class 8 to 12', 'With notes for every unit'), 'hero': 'books',
    },
    'interactive': {
        'kicker': 'Interactive', 'title': 'Physics, chemistry and code you can touch',
        'meta': ('Virtual labs', 'No install'), 'hero': 'flask',
    },
    'bookmarks': {
        'kicker': 'Saved', 'title': 'The things you meant to come back to',
        'meta': ('Bookmarks', 'Resources and threads'), 'hero': 'spark',
    },
    'achievements': {
        'kicker': 'Achievements', 'title': 'What you have earned so far',
        'meta': ('Badges', 'Milestones'), 'hero': 'spark',
    },
    'settings': {
        'kicker': 'Account', 'title': 'Your NEBians account',
        'meta': ('Profile', 'Preferences', 'Privacy'), 'hero': 'spark',
    },
    'credits': {
        'kicker': 'Credits', 'title': 'The people who built NEBians',
        'meta': ('NEBians',), 'hero': 'spark',
    },
    'notifications': {
        'kicker': 'Notifications', 'title': 'What happened while you were away',
        'meta': ('NEBians',), 'hero': 'spark',
    },
    'study-spaces': {
        'kicker': 'Study spaces', 'title': 'Study together, even apart',
        'meta': ('Shared rooms', 'Quizzes and flashcards'), 'hero': 'bubbles',
    },
}


def card_url(kind, key=''):
    """Absolute URL of a card, for the og:image tag."""
    key = str(key or '').strip('/')
    if not key:
        kind, key = 'page', 'default'
    return '%s/og/%s/%s.png?v=%d' % (SITE, kind, key, CARD_VERSION)


# ── What each kind puts on the card ───────────────────────────────────────

def _syllabus_grade_card(key):
    from . import syllabus_data
    grade = syllabus_data.grade_entry(key)
    if grade is None:
        raise Http404('No such grade')
    subjects = grade.get('subjects') or []
    units = sum(s.get('unit_count', 0) for s in subjects)
    school = grade.get('kind', 'school') == 'school'
    meta = ['%d subjects' % len(subjects)]
    if units:
        meta.append(('%d units' if school else '%d chapters') % units)
    return {
        'kicker': 'Syllabus' if school else 'Entrance preparation',
        'title': '%s syllabus' % grade.get('label', 'NEB') if school else grade.get('label', 'Entrance'),
        'meta': tuple(meta), 'hero': 'books', 'seed': 'grade-' + str(key),
    }


def _syllabus_subject_card(key):
    """key is `12/physics`, the pair the syllabus page takes."""
    from . import syllabus_data
    parts = [p for p in key.split('/') if p]
    if len(parts) != 2:
        raise Http404('No such subject')
    data = syllabus_data.subject(parts[0], parts[1])
    if not data:
        raise Http404('No such subject')
    school = data.get('kind', 'school') == 'school'
    meta = [data.get('grade_label') if school else data.get('short'),
            ('%d units' if school else '%d chapters') % (data.get('unit_count') or 0)]
    if data.get('questions'):
        meta.append('%d questions in the paper' % data['questions'])
    elif data.get('hours'):
        meta.append('%d hours' % data['hours'])
    return {
        'kicker': (data.get('grade_label') if school else '%s entrance' % data.get('short')) or 'Syllabus',
        'title': data.get('name') or 'Syllabus',
        'meta': tuple(m for m in meta if m),
        'subject': data.get('name') or '', 'hero': 'books',
        'seed': 'syl-' + str(key),
    }


def _syllabus_chapter_card(key):
    """key is `12/physics/3`."""
    from . import syllabus_data
    parts = [p for p in key.split('/') if p]
    if len(parts) != 3:
        raise Http404('No such chapter')
    data = syllabus_data.subject(parts[0], parts[1])
    if not data:
        raise Http404('No such chapter')
    try:
        no = int(parts[2])
    except ValueError:
        raise Http404('No such chapter')
    school = data.get('kind', 'school') == 'school'
    for unit in data.get('units') or []:
        if int(unit.get('no') or 0) == no:
            meta = [data.get('name') or '', (data.get('grade_label') if school else data.get('short')) or '']
            if unit.get('questions'):
                meta.append('%d questions in the paper' % unit['questions'])
            elif unit.get('hours'):
                meta.append('%d hours' % unit['hours'])
            return {
                'kicker': ('Unit %d' if school else 'Chapter %d') % no, 'title': unit.get('title') or 'Unit',
                'meta': tuple(m for m in meta if m),
                'subject': data.get('name') or '', 'hero': 'paper',
                'seed': 'unit-' + str(key),
            }
    raise Http404('No such chapter')





def _interactive_card(key):
    """key is `course-slug` or `course-slug/lesson-slug`."""
    from .interactive import get_course, get_lesson
    parts = [p for p in key.split('/') if p]
    if not parts:
        raise Http404('No such course')
    if len(parts) == 1:
        course = get_course(parts[0])
        if not course:
            raise Http404('No such course')
        return {
            'kicker': course.get('category_label') or 'Interactive',
            'title': course.get('title') or 'Interactive',
            'meta': tuple(m for m in (course.get('level'),
                                      '%d lessons' % (course.get('lesson_count') or 0))
                          if m)[:3],
            'subject': course.get('title') or '', 'hero': 'flask',
            'seed': 'i-' + key, 'accent': course.get('color') or '',
        }
    course, lesson, _, _ = get_lesson(parts[0], parts[1])
    if not course or not lesson:
        raise Http404('No such lesson')
    return {
        'kicker': course.get('title') or 'Interactive',
        'title': lesson.get('title') or 'Lesson',
        'meta': tuple(m for m in (course.get('category_label'),
                                  '%d min' % lesson.get('minutes')
                                  if lesson.get('minutes') else '') if m)[:3],
        'subject': course.get('title') or '', 'hero': 'flask',
        'seed': 'il-' + key, 'accent': course.get('color') or '',
    }


def _study_space_card(space_id):
    from api.models import StudySpace
    try:
        space = StudySpace.objects.only(
            'id', 'title', 'visibility', 'subject', 'study_level',
        ).get(id=space_id)
    except (StudySpace.DoesNotExist, ValueError):
        raise Http404('Space not found')
    if space.visibility != StudySpace.VISIBILITY_PUBLIC:
        raise Http404('Space not found')
    return {
        'kicker': 'Study space',
        'title': (space.title or '').strip() or 'A NEBians study space',
        'meta': tuple(m for m in (space.study_level, space.subject) if m)[:3],
        'subject': space.subject or '', 'hero': 'bubbles', 'seed': str(space.pk),
    }

def _page_card(key):
    spec = PAGES.get(key)
    if spec is None:
        raise Http404('No card for that page')
    return dict(spec)


def _faq_card():
    from . import faq as faq_data
    return {
        'kicker': 'Help centre', 'title': 'Questions, answered.',
        'meta': ('%d answers' % faq_data.question_count(), 'Nepal'),
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
    'syllabus': _syllabus_subject_card,
    'grade': _syllabus_grade_card,
    'chapter': _syllabus_chapter_card,
    'interactive': _interactive_card,
    'space': _study_space_card,
}


# ── The endpoint ──────────────────────────────────────────────────────────

def _render_response(kind, key, spec):
    """Draw, cache and serve. Caching is keyed on what the card says, not on
    when it was asked for, so an edit invalidates it and nothing else does."""
    avatar = spec.pop('avatar', None)
    sig_src = repr(sorted(spec.items())) + ('|photo' if avatar is not None else '')
    sig = hashlib.sha256(sig_src.encode('utf-8')).hexdigest()[:20]
    cache_key = 'og_card_png:v%d:%s:%s' % (CARD_VERSION, kind, sig)

    png = cache.get(cache_key)
    # A cached card is a PNG or it is nothing. Three og_card_png keys came back
    # with an empty payload on 2026-11-13, which raised EOFError in the cache
    # backend and 500ed this endpoint for a crawler; the cache layer now treats
    # that as a miss, and this guard keeps a zero-byte image from ever being
    # served if some other backend misbehaves the same way.
    if not isinstance(png, (bytes, bytearray)) or not png:
        png = None
    if png is None:
        img = og_cards.render(kind, spec.get('title') or 'NEBians',
                              meta=spec.get('meta', ()),
                              kicker=spec.get('kicker', ''),
                              subject=spec.get('subject', ''),
                              seed=spec.get('seed', '') or key,
                              hero=spec.get('hero', 'mark'),
                              avatar=avatar,
                              accent_hex=spec.get('accent', '') or '')
        png = og_cards.to_png(img)
        cache.set(cache_key, png, 24 * 3600)

    resp = HttpResponse(png, content_type='image/png')
    # A day in shared caches. Scrapers refetch rarely and the signature in the
    # cache key already handles edits on our side.
    resp['Cache-Control'] = 'public, max-age=86400'
    resp['X-Content-Type-Options'] = 'nosniff'
    # Fetchable, but not an image-search result of its own: the card is a
    # preview of a page, and a card outranking its page is a duplicate.
    resp['X-Robots-Tag'] = 'noindex'
    return resp


# Scrapers are this endpoint's whole audience, and a debugger session ("Scrape
# Again" a dozen times in a minute) looks exactly like an attack to a per-IP
# counter. Facebook answered our 429 by dropping the image from the preview, so
# known crawlers skip the limit and everyone else gets a generous one.
_CRAWLER_UA = re.compile(
    r'facebookexternalhit|twitterbot|linkedinbot|discordbot|telegrambot|whatsapp|'
    r'slackbot|redditbot|pinterest|googlebot|bingbot|applebot|embedly|iframely|'
    r'vkShare|W3C_Validator|preview|fetcher|crawler|spider|bot',
    re.I,
)


def og_card(request, kind, key):
    """GET /og/<kind>/<key>.png"""
    ua = request.META.get('HTTP_USER_AGENT', '') or ''
    if not _CRAWLER_UA.search(ua):
        if _rate_limit(request, 'og_card', 600, 60, by_ip=True):
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
    'syllabus_hub': 'syllabus',
    'interactive_hub': 'interactive',
    'bookmarks': 'bookmarks',
    'profile_achievements': 'achievements',
    'settings': 'settings',
    'edit_profile': 'settings',
    'password': 'settings',
    'change_password': 'settings',
    'credits': 'credits',
    'notifications': 'notifications',
    'study_space_page': 'study-spaces',
}

# Routes whose card is drawn from the thing the URL names.
_ROUTE_OBJECTS = {
    'reader': ('resource', lambda kw: kw.get('resource_id')),
    'forum_post': ('post', lambda kw: kw.get('post_id')),
    'news_detail': ('news', lambda kw: kw.get('slug')),
    'profile': ('profile', lambda kw: kw.get('username')),
    'subject_page': ('subject', lambda kw: '%s/%s' % (kw.get('grade_slug', ''),
                                                      kw.get('subject_slug', ''))),
    # The syllabus pages name their subject twice over -- once as a grade and a
    # subject, once as a grade and a unit -- so each gets its own builder.
    'syllabus_grade': ('grade', lambda kw: kw.get('grade', '')),
    'syllabus_subject': ('syllabus', lambda kw: '%s/%s' % (kw.get('grade', ''),
                                                           kw.get('subject', ''))),
    'syllabus_chapter': ('chapter', lambda kw: '%s/%s/%s' % (kw.get('grade', ''),
                                                             kw.get('subject', ''),
                                                             kw.get('unit_no', ''))),
    'syllabus_bank': ('syllabus', lambda kw: '%s/%s' % (kw.get('grade', ''),
                                                        kw.get('subject', ''))),
    'syllabus_guide': ('syllabus', lambda kw: '%s/%s' % (kw.get('grade', ''),
                                                         kw.get('subject', ''))),
    'interactive_course': ('interactive', lambda kw: kw.get('course_slug')),
    'interactive_lesson': ('interactive', lambda kw: '%s/%s' % (kw.get('course_slug', ''),
                                                                kw.get('lesson_slug', ''))),
    'study_space_page': ('space', lambda kw: kw.get('space_id')),
}

_ALT = {
    'resource': 'A NEBians card for this study resource',
    'post': 'A NEBians card for this discussion',
    'news': 'A NEBians card for this article',
    'profile': 'A NEBians profile card',
    'subject': 'A NEBians card for this subject',
    'page': "NEBians, Nepal's Learning Community",
    'syllabus': 'A NEBians syllabus card',
    'grade': 'A NEBians syllabus card',
    'chapter': 'A NEBians card for this unit',
    'course': 'A NEBians card for this course',
    'creator': 'A NEBians storefront card',
    'interactive': 'A NEBians interactive lesson card',
    'space': 'A NEBians study space card',
}


def og_image_context(request):
    """Template context: og_image_url and og_image_alt for the current route.

    Always returns a card, even for a route with no entry above: a page whose
    preview is generic is a missed opportunity, but a page with no og:image at
    all gets a bare link. `og_card_version` goes to the template so a fallback
    written in base.html can carry the same ?v= every other card does instead
    of a number that rots on the next redesign.
    """
    ctx = {'og_card_version': CARD_VERSION,
           'og_image_url': card_url('page', 'default'),
           'og_image_alt': _ALT['page']}

    match = getattr(request, 'resolver_match', None)
    name = getattr(match, 'url_name', '') if match else ''
    if not name:
        return ctx

    page = _ROUTE_PAGES.get(name)
    if page:
        ctx['og_image_url'] = card_url('page', page)
        return ctx

    obj = _ROUTE_OBJECTS.get(name)
    if obj:
        kind, key_of = obj
        key = (key_of(getattr(match, 'kwargs', {}) or {}) or '').strip('/')
        # Ids, slugs and usernames only. A key that needs escaping is a key
        # this route does not actually have, so stay on the default card.
        if key and _SAFE_KEY.match(key):
            ctx['og_image_url'] = card_url(kind, key)
            ctx['og_image_alt'] = _ALT.get(kind, _ALT['page'])
    return ctx
