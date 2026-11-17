"""SEO helpers for public, indexable NEBians pages.

Keep crawler-facing URLs constrained to clean public content. Private profiles,
locked/bot/test accounts, unapproved resources, and obvious placeholders are
filtered here before sitemap generation.
"""
from __future__ import annotations

import re
from typing import Dict, Iterable, Iterator, Optional
from urllib.parse import quote
from xml.sax.saxutils import escape as _xml_escape_text

_XML_ATTRIBUTE_ENTITIES = {'"': '&quot;', "'": '&apos;'}


def xml_escape(value, quote: bool = False) -> str:
    """XML-escape a value. ``quote`` also escapes quotes, for attributes."""
    return _xml_escape_text(str(value), _XML_ATTRIBUTE_ENTITIES if quote else None)

from django.utils import timezone

from api.models import Post, Resource, User

SITE_BASE_URL = 'https://nebians.consica.com.np'
# A sitemap file may hold at most 50,000 URLs and be at most 50 MB uncompressed.
# The caps below are per group, and the index splits each group into its own
# file, so no single document can cross the limit however big the site gets.
_MAX_RESOURCES = 50000
_MAX_POSTS = 50000
_MAX_PROFILES = 50000
SITEMAP_CHUNK = 40000

_PLACEHOLDER_TEXT_RE = re.compile(
    r'(^\s*(test|testing|untitled|new post|hello world)\s*\d*\s*$)'
    r'|\b(lorem ipsum|placeholder|dummy content|demo content|sample content|asdf|qwerty)\b',
    re.I,
)
_USERNAME_PLACEHOLDER_RE = re.compile(r'^(test|demo|dummy|sample|admin-test|user\d{1,4}|asdf|qwerty)([-_.]?\d+)?$', re.I)


def _to_lastmod(value, fallback: Optional[str] = None) -> str:
    if isinstance(value, (int, float)) and value > 0:
        try:
            return timezone.datetime.fromtimestamp(value / 1000, tz=timezone.get_current_timezone()).isoformat()
        except Exception:
            return fallback or timezone.now().isoformat()
    if hasattr(value, 'isoformat') and value:
        return value.isoformat()
    return fallback or timezone.now().isoformat()


def _contains_placeholder(value: str) -> bool:
    value = (value or '').strip()
    if not value:
        return False
    return bool(_PLACEHOLDER_TEXT_RE.search(value))


def is_test_or_private_user(user: Optional[User]) -> bool:
    if not user:
        return False
    username = (user.username or '').strip()
    display = (user.display_name or '').strip()
    email = (user.email or '').strip().lower()
    if getattr(user, 'is_locked', False) or getattr(user, 'is_bot', False):
        return True
    if not username or _USERNAME_PLACEHOLDER_RE.match(username):
        return True
    combined = ' '.join([username, display, email])
    return _contains_placeholder(combined)


def has_public_profile_signal(user: User) -> bool:
    """Avoid indexing empty signup shells even when the account is public."""
    if is_test_or_private_user(user):
        return False
    text_signal = any((
        (user.display_name or '').strip(),
        (user.bio or '').strip(),
        (user.school or '').strip(),
        (user.subjects or '').strip(),
        (user.teaching_subjects or '').strip(),
        (user.photo_url or '').strip(),
    ))
    activity_signal = any((
        (user.post_count or 0) > 0,
        (user.reply_count or 0) > 0,
        (user.follower_count or 0) > 0,
        (user.contribution_score or 0) > 0,
        (user.likes_received_count or 0) > 0,
    ))
    return bool(text_signal or activity_signal)


def is_indexable_resource(resource: Resource) -> bool:
    if resource.approval_status != 'approved':
        return False
    if resource.uploaded_by_id and is_test_or_private_user(getattr(resource, 'uploaded_by', None)):
        return False
    title = (resource.title or '').strip()
    if len(title) < 8 or _contains_placeholder(title):
        return False
    searchable_context = ' '.join([
        resource.description or '', resource.subject or '', resource.grade_level or '',
        resource.tags or '', resource.author_name or '', resource.source_label or '',
    ]).strip()
    if not searchable_context and not (resource.file or resource.file_url):
        return False
    if len((resource.description or '').strip()) < 8 and _contains_placeholder(searchable_context):
        return False
    return True


def is_indexable_post(post: Post) -> bool:
    if getattr(post, 'is_archived', False):
        return False
    if is_test_or_private_user(getattr(post, 'user', None)):
        return False
    title = (post.title or '').strip()
    content = (post.content or '').strip()
    if len(title) < 8 or _contains_placeholder(title):
        return False
    if len(content) < 40 and (post.reply_count or 0) <= 0:
        return False
    if _contains_placeholder(content[:120]):
        return False
    return True


# Static pages, with a priority that says what the site is actually for. No
# lastmod here: these are served from templates, and stamping them with "now"
# on every request is a lie that teaches a crawler to ignore lastmod entirely.
STATIC_PAGES = (
    ('/', 'daily', '1.0'),
    ('/about/', 'monthly', '0.8'),
    ('/app/past-papers/', 'daily', '0.9'),
    ('/app/model-questions/', 'daily', '0.9'),
    ('/app/online-learning/', 'weekly', '0.8'),
    ('/app/library/', 'daily', '0.9'),
    ('/app/syllabus/', 'weekly', '0.9'),
    ('/app/news/', 'daily', '0.7'),
    ('/app/marketplace/', 'weekly', '0.7'),
    ('/app/library/?tab=interactive', 'weekly', '0.7'),
    ('/app/results/', 'monthly', '0.6'),
    ('/app/results/check/', 'monthly', '0.6'),
    ('/app/faq/', 'monthly', '0.6'),
    ('/app/tools/', 'monthly', '0.5'),
    ('/app/requests/', 'weekly', '0.5'),
    ('/app/upload/', 'monthly', '0.4'),
    ('/privacy/', 'yearly', '0.3'),
    ('/terms/', 'yearly', '0.3'),
    ('/copyright-takedown/', 'yearly', '0.2'),
)


def _slug(value: str) -> str:
    value = (value or '').lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-')


def _syllabus_entries() -> Iterator[Dict[str, str]]:
    """The syllabus is the part of the site most likely to be searched for by
    name ("class 12 physics syllabus"), and it was not in the sitemap at all."""
    try:
        from web import syllabus_data
    except Exception:
        return
    index = syllabus_data.index()
    for grade in index.get('grades', []):
        grade_key = grade.get('grade') or ''
        if not grade_key:
            continue
        yield {
            'loc': f'{SITE_BASE_URL}/app/syllabus/{quote(str(grade_key), safe="")}/',
            'changefreq': 'monthly', 'priority': '0.8',
        }
        for subject in grade.get('subjects', []):
            subject_key = subject.get('subject') or ''
            if not subject_key:
                continue
            base = f'{SITE_BASE_URL}/app/syllabus/{quote(str(grade_key), safe="")}/{quote(str(subject_key), safe="")}/'
            yield {'loc': base, 'changefreq': 'monthly', 'priority': '0.8'}
            for unit in range(1, int(subject.get('unit_count') or 0) + 1):
                yield {'loc': base + 'unit-%d/' % unit,
                       'changefreq': 'monthly', 'priority': '0.6'}


def _interactive_entries() -> Iterator[Dict[str, str]]:
    try:
        from web import interactive
        courses = interactive.get_all_courses()
    except Exception:
        return
    for course in courses:
        slug = course.get('slug') or ''
        if not slug:
            continue
        yield {'loc': f'{SITE_BASE_URL}/app/interactive/{quote(str(slug), safe="")}/',
               'changefreq': 'monthly', 'priority': '0.7'}
        for lesson in course.get('lessons', []):
            lesson_slug = lesson.get('slug') or ''
            if lesson_slug:
                yield {
                    'loc': f'{SITE_BASE_URL}/app/interactive/{quote(str(slug), safe="")}/{quote(str(lesson_slug), safe="")}/',
                    'changefreq': 'monthly', 'priority': '0.5',
                }


def _subject_entries() -> Iterator[Dict[str, str]]:
    """Library subject pages: /app/subject/<grade>/<subject>/."""
    seen = set()
    try:
        from web import curriculum as _curriculum
        keys = list(_curriculum.CURRICULUM_MAP.keys())
    except Exception:
        keys = []
    for (grade_val, subject_val) in keys:
        grade_slug = _slug(grade_val)
        if '10' in grade_slug and 'see' in grade_slug:
            grade_slug = 'class-10-see'
        subject_slug = _slug(subject_val)
        if not grade_slug or not subject_slug or grade_slug == 'other':
            continue
        loc = f'{SITE_BASE_URL}/app/subject/{grade_slug}/{subject_slug}/'
        if loc in seen:
            continue
        seen.add(loc)
        yield {'loc': loc, 'changefreq': 'weekly', 'priority': '0.75'}

    try:
        rows = (Resource.objects.filter(approval_status='approved', is_lead=True)
                .values_list('grade_level', 'subject')[:2000])
        for grade, subjects in rows:
            for subject in (subjects or '').split(','):
                subject = subject.strip()
                if not subject:
                    continue
                grade_slug = _slug(grade)
                subject_slug = _slug(subject)
                loc = f'{SITE_BASE_URL}/app/subject/{grade_slug}/{subject_slug}/'
                if grade_slug and subject_slug and loc not in seen:
                    seen.add(loc)
                    yield {'loc': loc, 'changefreq': 'weekly', 'priority': '0.7'}
    except Exception:
        pass


def _storefront_entries() -> Iterator[Dict[str, str]]:
    """Published creator pages and their courses."""
    try:
        from api.models import CreatorCourse, CreatorPage
    except Exception:
        return
    try:
        pages = (CreatorPage.objects.filter(published=True)
                 .only('slug', 'updated_at')
                 .order_by('-updated_at')[:5000])
        for page in pages:
            if not page.slug:
                continue
            yield {
                'loc': f'{SITE_BASE_URL}/app/marketplace/{quote(page.slug, safe="")}/',
                'changefreq': 'weekly', 'priority': '0.6',
                'lastmod': _to_lastmod(page.updated_at),
            }
    except Exception:
        pass
    try:
        courses = (CreatorCourse.objects.filter(status='published')
                   .only('id', 'updated_at')
                   .order_by('-updated_at')[:5000])
        for course in courses:
            yield {
                'loc': f'{SITE_BASE_URL}/app/marketplace/course/{quote(str(course.id), safe="")}/',
                'changefreq': 'weekly', 'priority': '0.6',
                'lastmod': _to_lastmod(course.updated_at),
            }
    except Exception:
        pass


def sitemap_groups() -> Dict[str, Iterator[Dict[str, str]]]:
    """The sitemap, grouped into files that can each stay under the limit.

    A single urlset with every resource, thread and profile in it will one day
    cross 50,000 URLs, and a crawler that meets an oversized file discards it
    whole -- so the entries are grouped by what they are.
    """
    groups = {
        'pages': _static_and_syllabus_entries,
        'library': _resource_entries,
        'forum': _post_entries,
        'profiles': _profile_entries,
    }
    return {name: fn() for name, fn in groups.items()}


def sitemap_entries() -> Iterator[Dict[str, str]]:
    """Every public, indexable URL. Only for tooling -- the endpoint serves the
    grouped files through sitemap_groups()."""
    for entries in sitemap_groups().values():
        yield from entries


def _static_and_syllabus_entries() -> Iterator[Dict[str, str]]:
    for path, changefreq, priority in STATIC_PAGES:
        yield {'loc': SITE_BASE_URL + path, 'changefreq': changefreq,
               'priority': priority}
    yield from _syllabus_entries()
    yield from _interactive_entries()
    yield from _subject_entries()
    yield from _storefront_entries()
    yield from _news_entries()


def _news_entries() -> Iterator[Dict[str, str]]:
    try:
        from api.models import Announcement
        rows = (Announcement.objects.filter(status='published')
                .order_by('-published_at')
                .values_list('slug', 'published_at')[:5000])
        for slug, published_at in rows:
            if not slug:
                continue
            yield {
                'loc': f'{SITE_BASE_URL}/app/news/{quote(str(slug), safe="")}/',
                'changefreq': 'weekly', 'priority': '0.6',
                'lastmod': _to_lastmod(published_at),
            }
    except Exception:
        pass


def _resource_entries() -> Iterator[Dict[str, str]]:
    try:
        resources = (Resource.objects.filter(approval_status='approved')
                     .select_related('uploaded_by')
                     .order_by('-added_at')[:_MAX_RESOURCES])
    except Exception:
        return
    for resource in resources:
        if not is_indexable_resource(resource):
            continue
        yield {
            'loc': f'{SITE_BASE_URL}/app/reader/{quote(str(resource.id), safe="")}/',
            'changefreq': 'weekly', 'priority': '0.7',
            'lastmod': _to_lastmod(getattr(resource, 'updated_at', None)
                                   or resource.added_at),
        }


def _post_entries() -> Iterator[Dict[str, str]]:
    try:
        posts = (Post.objects.filter(is_archived=False)
                 .select_related('user')
                 .order_by('-created_at')[:_MAX_POSTS])
    except Exception:
        return
    for post in posts:
        if not is_indexable_post(post):
            continue
        yield {
            'loc': f'{SITE_BASE_URL}/app/forum/post/{quote(str(post.id), safe="")}/',
            'changefreq': 'weekly', 'priority': '0.6',
            'lastmod': _to_lastmod(post.edited_at or post.created_at),
        }


def _profile_entries() -> Iterator[Dict[str, str]]:
    try:
        users = (User.objects
                 .filter(is_locked=False, is_bot=False)
                 .order_by('-contribution_score', '-follower_count', '-created_at')[:_MAX_PROFILES])
    except Exception:
        return
    for user in users:
        if not has_public_profile_signal(user):
            continue
        yield {
            'loc': f'{SITE_BASE_URL}/app/profile/{quote(user.username, safe="")}/',
            'changefreq': 'weekly',
            'priority': '0.5' if (user.contribution_score or 0) > 0 else '0.3',
            'lastmod': _to_lastmod(user.created_at),
        }


def build_sitemap_xml(entries: Optional[Iterable[Dict[str, str]]] = None) -> str:
    entries = entries or sitemap_entries()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for entry in entries:
        lines.append('  <url>')
        lines.append(f"    <loc>{xml_escape(entry['loc'], quote=True)}</loc>")
        lastmod = entry.get('lastmod')
        if lastmod:
            lines.append(f"    <lastmod>{xml_escape(str(lastmod), quote=True)}</lastmod>")
        lines.append(f"    <changefreq>{xml_escape(entry.get('changefreq', 'weekly'), quote=True)}</changefreq>")
        lines.append(f"    <priority>{xml_escape(entry.get('priority', '0.5'), quote=True)}</priority>")
        lines.append('  </url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'
