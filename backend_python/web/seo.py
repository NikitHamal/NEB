"""SEO helpers for public, indexable NEBians pages.

Keep crawler-facing URLs constrained to clean public content. Private profiles,
locked/bot/test accounts, unapproved resources, and obvious placeholders are
filtered here before sitemap generation.
"""
from __future__ import annotations

import re
from html import escape as xml_escape
from typing import Dict, Iterable, Iterator, Optional
from urllib.parse import quote

from django.utils import timezone

from api.models import Post, Resource, User

SITE_BASE_URL = 'https://nebians.consica.com.np'
_MAX_RESOURCES = 50000
_MAX_POSTS = 20000
_MAX_PROFILES = 20000

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


def sitemap_entries() -> Iterator[Dict[str, str]]:
    now = timezone.now().isoformat()
    yield {'loc': f'{SITE_BASE_URL}/', 'changefreq': 'daily', 'priority': '1.0', 'lastmod': now}
    yield {'loc': f'{SITE_BASE_URL}/library/', 'changefreq': 'daily', 'priority': '0.9', 'lastmod': now}
    yield {'loc': f'{SITE_BASE_URL}/forum/', 'changefreq': 'daily', 'priority': '0.8', 'lastmod': now}
    yield {'loc': f'{SITE_BASE_URL}/search/', 'changefreq': 'weekly', 'priority': '0.4', 'lastmod': now}

    resources = (Resource.objects
                 .filter(approval_status='approved')
                 .select_related('uploaded_by')
                 .order_by('-added_at')[:_MAX_RESOURCES])
    for resource in resources:
        if not is_indexable_resource(resource):
            continue
        ts = getattr(resource, 'updated_at', None) or resource.added_at
        yield {
            'loc': f'{SITE_BASE_URL}/reader/{quote(str(resource.id), safe="")}/',
            'changefreq': 'weekly',
            'priority': '0.7',
            'lastmod': _to_lastmod(ts, now),
        }

    posts = (Post.objects
             .filter(is_archived=False)
             .select_related('user')
             .order_by('-created_at')[:_MAX_POSTS])
    for post in posts:
        if not is_indexable_post(post):
            continue
        yield {
            'loc': f'{SITE_BASE_URL}/forum/post/{quote(str(post.id), safe="")}/',
            'changefreq': 'weekly',
            'priority': '0.6',
            'lastmod': _to_lastmod(post.edited_at or post.created_at, now),
        }

    users = (User.objects
             .filter(is_locked=False, is_bot=False)
             .order_by('-contribution_score', '-follower_count', '-created_at')[:_MAX_PROFILES])
    for user in users:
        if not has_public_profile_signal(user):
            continue
        yield {
            'loc': f'{SITE_BASE_URL}/profile/{quote(user.username, safe="")}/',
            'changefreq': 'weekly',
            'priority': '0.5' if (user.contribution_score or 0) > 0 else '0.3',
            'lastmod': _to_lastmod(user.created_at, now),
        }


def build_sitemap_xml(entries: Optional[Iterable[Dict[str, str]]] = None) -> str:
    entries = entries or sitemap_entries()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for entry in entries:
        lines.append('  <url>')
        lines.append(f"    <loc>{xml_escape(entry['loc'], quote=True)}</loc>")
        lines.append(f"    <lastmod>{xml_escape(entry.get('lastmod') or timezone.now().isoformat(), quote=True)}</lastmod>")
        lines.append(f"    <changefreq>{xml_escape(entry.get('changefreq', 'weekly'), quote=True)}</changefreq>")
        lines.append(f"    <priority>{xml_escape(entry.get('priority', '0.5'), quote=True)}</priority>")
        lines.append('  </url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'
