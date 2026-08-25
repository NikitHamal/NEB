"""Shared news/announcement serialization for web templates and the mobile JSON API."""
import re as _re

import markdown as _markdown
import nh3

from .services import avatar_or_photo_url

CATEGORY_META = {
    'exam_results': {'icon': 'fact_check', 'label': 'Exam Results', 'color': '#dc2626'},
    'notice':       {'icon': 'campaign',     'label': 'Notice',       'color': '#2563eb'},
    'event':        {'icon': 'event',       'label': 'Event',       'color': '#7c3aed'},
    'update':       {'icon': 'upgrade',     'label': 'Update',       'color': '#059669'},
    'alert':        {'icon': 'warning',     'label': 'Alert',        'color': '#d97706'},
    'general':      {'icon': 'info',        'label': 'General',      'color': '#6b7280'},
}

_MATH_PLACEHOLDER = '@@NEBMATH{}@@'
_MATH_RE = _re.compile(r'(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$|\\\([\s\S]+?\\\)|\\\[[\s\S]+?\\\])')


def render_content_html(md_text):
    """Render announcement markdown to sanitized HTML.

    LaTeX segments ($...$, $$...$$, \\(..\\), \\[..\\]) are shielded from the
    markdown parser so underscores/carets inside formulas are not eaten,
    then restored verbatim for client-side math rendering.
    """
    text = md_text or ''
    stash = []

    def _stash(m):
        stash.append(m.group(1))
        return _MATH_PLACEHOLDER.format(len(stash) - 1)

    text = _MATH_RE.sub(_stash, text)
    html = _markdown.markdown(text, extensions=['tables', 'fenced_code'])
    for i, seg in enumerate(stash):
        html = html.replace(_MATH_PLACEHOLDER.format(i), seg)
    return nh3.clean(
        html,
        tags={
            'a', 'b', 'blockquote', 'br', 'code', 'del', 'div', 'em', 'h1', 'h2',
            'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li', 'ol', 'p', 'pre',
            's', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'th',
            'thead', 'tr', 'ul',
        },
        attributes={
            'a': {'href', 'title'},
            'img': {'src', 'alt', 'title'},
            'code': {'class'},
            'span': {'class'},
            'div': {'class'},
            'th': {'align'},
            'td': {'align'},
        },
        url_schemes={'http', 'https', 'mailto'},
        link_rel='noopener noreferrer',
    )


def serialize_announcement(a, include_content=False):
    """Canonical announcement payload shared by web views and /api/news/."""
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
        'author_photo': avatar_or_photo_url(a.author) or '' if a.author else '',
        'published_at': a.published_at,
        'created_at': a.created_at,
        'view_count': a.view_count,
    }
    if include_content:
        raw = a.content or ''
        data['content'] = raw
        data['content_html'] = render_content_html(raw)
    return data
