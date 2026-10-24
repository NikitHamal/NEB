"""Structured data for forum threads.

Google's "Discussion forum" rich result wants a DiscussionForumPosting with a
body, an author that has a url, and its replies. Search Console flagged three
gaps on this site: no text/image on the posting, no comment, and no url on the
author. Building the graph in Python rather than in the template is the fix for
the whole class of problem: json.dumps escapes properly, so a title containing
a quote or a backslash can no longer produce invalid JSON that a crawler
silently drops.
"""
from __future__ import annotations

import json
from typing import Iterable, Optional
from urllib.parse import quote

SITE = 'https://nebians.consica.com.np'
ORG_ID = SITE + '/#organization'

# The graph is a preview, not an archive: Google only reads the first few
# comments, and a 200-reply thread would put a megabyte of JSON in the page.
MAX_COMMENTS = 10


def ld_json(payload) -> str:
    """JSON for a <script type="application/ld+json"> block.

    json.dumps alone is not safe inside a script tag: a post whose text
    contains "</script>" would close the tag and spill the rest of the graph
    into the page. Escaping the angle brackets keeps the JSON valid and the
    document intact.
    """
    return (json.dumps(payload, ensure_ascii=False)
            .replace('<', '\\u003c').replace('>', '\\u003e')
            .replace('&', '\\u0026'))


def _iso(value) -> str:
    """Milliseconds since epoch into ISO 8601, or '' for a missing value.

    The serialisers hand around integer milliseconds; schema.org wants ISO.
    """
    if not value:
        return ''
    try:
        from datetime import datetime, timezone
        if isinstance(value, (int, float)):
            stamp = datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)
        else:
            stamp = value
        return stamp.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    except Exception:
        return ''


def profile_url(username: str) -> str:
    return '%s/app/profile/%s/' % (SITE, quote(str(username or ''), safe=''))


def _person_url(item: dict) -> str:
    """The profile URL for a post or reply author.

    Profile routes key on the username, not the id -- an id here would be a
    URL that 404s, which is worse than no URL at all to a crawler.
    """
    username = (item.get('authorUsername') or '').strip()
    return profile_url(username) if username else ''


def _author(name: str, url: str = '', image: str = '', anonymous: bool = False) -> dict:
    """A Person, or nothing identifying when the poster chose anonymity.

    An anonymous thread still needs an author node -- Google requires the field
    -- so it gets the site's name rather than a bare "Anonymous" that would
    read as a person called Anonymous.
    """
    if anonymous:
        return {'@type': 'Organization', 'name': 'NEBians', 'url': SITE}
    node = {'@type': 'Person', 'name': name or 'A NEBian'}
    if url:
        node['url'] = url
        node['@id'] = url + '#person'
    if image:
        node['image'] = image
    return node


def _comment(reply: dict, post_id) -> dict:
    url = '%s/app/forum/post/%s/#reply-%s' % (SITE, post_id, reply.get('id', ''))
    node = {
        '@type': 'Comment',
        'url': url,
        '@id': url,
        'text': (reply.get('content') or '').strip() or '(no text)',
        'datePublished': _iso(reply.get('createdAt')),
        'author': _author(
            reply.get('authorName') or '',
            _person_url(reply),
            reply.get('authorPhotoUrl') or '',
            anonymous=bool(reply.get('isAnonymous')),
        ),
    }
    if reply.get('isEdited') and reply.get('editedAt'):
        node['dateModified'] = _iso(reply['editedAt'])
    count = reply.get('thumbsUpCount') or 0
    if count:
        node['upvoteCount'] = int(count)
    return node


def thread_schema(post: dict, replies: Optional[Iterable[dict]] = None) -> dict:
    """The full DiscussionForumPosting graph for one thread."""
    post_id = post.get('id')
    url = '%s/app/forum/post/%s/' % (SITE, post_id)

    text = (post.get('content') or '').strip()
    # Google's critical error is "either text, image or video". A title-only
    # post would fail it, so the title is the body of last resort.
    if not text:
        text = (post.get('title') or '').strip() or 'A discussion on NEBians'

    images = [i.get('imageUrl') for i in (post.get('images') or []) if i.get('imageUrl')]
    for item in (post.get('attachments') or []):
        if (item.get('kind') or '') == 'image':
            src = item.get('url') or item.get('thumbnailUrl')
            if src:
                images.append(src)

    node = {
        '@context': 'https://schema.org',
        '@type': 'DiscussionForumPosting',
        '@id': url + '#post',
        'url': url,
        'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        'headline': (post.get('title') or 'Discussion')[:110],
        'text': text,
        'datePublished': _iso(post.get('createdAt')),
        'dateModified': _iso(post.get('editedAt') or post.get('createdAt')),
        'author': _author(
            post.get('authorName') or '',
            _person_url(post),
            post.get('authorPhotoUrl') or '',
            anonymous=bool(post.get('isAnonymous')),
        ),
        'publisher': {'@id': ORG_ID},
        'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website',
                     'name': 'NEBians', 'url': SITE},
    }
    if post.get('category'):
        node['about'] = {'@type': 'Thing', 'name': post['category']}
    if images:
        node['image'] = images if len(images) > 1 else images[0]

    stats = [
        ('https://schema.org/LikeAction', post.get('thumbsUpCount')),
        ('https://schema.org/CommentAction', post.get('replyCount')),
        ('https://schema.org/ViewAction', post.get('viewCount')),
    ]
    counters = [
        {'@type': 'InteractionCounter', 'interactionType': kind,
         'userInteractionCount': int(count)}
        for kind, count in stats if count
    ]
    if counters:
        node['interactionStatistic'] = counters

    reply_list = list(replies or [])
    if reply_list:
        node['comment'] = [_comment(r, post_id) for r in reply_list[:MAX_COMMENTS]]
        node['commentCount'] = len(reply_list)

    return node


def breadcrumb_schema(trail) -> dict:
    """trail is [(name, url), ...] in order, the last one being this page."""
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': name,
             **({'item': href} if href else {})}
            for i, (name, href) in enumerate(trail)
        ],
    }


def article_schema(item: dict, *, comment_count: int = 0) -> dict:
    """A BlogPosting for a news article.

    The same missing fields that broke the forum card were missing here:
    no datePublished, no image, and an author with no url. Google's article
    result wants all three, so they are built in one place.
    """
    slug = item.get('slug') or ''
    url = '%s/app/news/%s/' % (SITE, slug)
    body = (item.get('content') or '').strip()
    summary = (item.get('summary') or '').strip()

    node = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        '@id': url + '#article',
        'url': url,
        'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        'headline': (item.get('title') or 'NEBians')[:110],
        'description': (summary or item.get('title') or '')[:300],
        'datePublished': _iso(item.get('published_at') or item.get('created_at')),
        'dateModified': _iso(item.get('updated_at') or item.get('published_at')
                             or item.get('created_at')),
        'author': _author(item.get('author_name') or 'NEBians Team',
                          item.get('author_url') or ''),
        'publisher': {'@id': ORG_ID},
        'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website',
                     'name': 'NEBians', 'url': SITE},
        'inLanguage': 'en',
    }
    if body:
        node['articleBody'] = body[:5000]
    cover = (item.get('cover_image_url') or '').strip()
    if cover:
        node['image'] = cover if cover.startswith('http') else SITE + cover
    if item.get('tags'):
        node['keywords'] = item['tags']
    if item.get('category_label'):
        node['articleSection'] = item['category_label']
    if comment_count:
        node['commentCount'] = int(comment_count)
    return node
