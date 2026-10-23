"""Intelligent mixed feed — "Suggested for you".

One endpoint, two audiences:
  * NEBians Android home ("Suggested for you" deck)
  * NEBians website home suggestion rail

Contract: the response `items` is NEVER empty as long as the platform has any
approved resource or non-archived post — scoring feeds relevance first, then
recency/popularity padding guarantees a full deck even for brand-new users or
thin catalogs. Only a literally empty platform yields zero items (with
`note: 'no_content'`).
"""
from __future__ import annotations

import copy
import math
import time
import uuid
from collections import Counter

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Bookmark, Post, Resource
from .serializers import PostSerializer, ResourceSerializer
from .view_helpers import _get_user_from_request

_RECENT_POOL = 90  # candidates per side before scoring
_DECK_MIN = 12     # padding guarantees at least this many when content exists
_POST_HALF_LIFE_H = 20.0       # a discussion's freshness halves every 20 hours
_RESOURCE_HALF_LIFE_H = 96.0   # a resource stays fresh about five times longer
_INTEREST_TTL = 600            # interests are recomputed at most every 10 minutes per user


def _norm(value):
    return (value or '').strip().lower()


def _user_interests(user):
    """How much the user cares about each forum category and subject, from what they wrote,
    bookmarked and uploaded (most recent first, so new interests weigh in quickly), plus their
    class. Weighted counts rather than a flat set: three Physics bookmarks say more than one.
    Cached per user for ten minutes, which takes six queries off every feed request."""
    if user is None:
        return Counter(), Counter(), ''
    from django.core.cache import cache
    key = f'feed_interests_v2:{user.id}'
    hit = cache.get(key)
    if hit is not None:
        return hit
    categories, subjects = Counter(), Counter()
    try:
        for row in Post.objects.filter(user=user).order_by('-created_at')[:12].values_list('category', flat=True):
            if row:
                categories[_norm(row)] += 2
        marks = list(Bookmark.objects.filter(user=user).order_by('-created_at').values_list('target_type', 'target_id')[:24])
        post_ids = [t for k, t in marks if k == 'post']
        resource_ids = [t for k, t in marks if k == 'resource']
        if post_ids:
            for row in Post.objects.filter(id__in=post_ids).values_list('category', flat=True):
                if row:
                    categories[_norm(row)] += 1
        if resource_ids:
            for row in Resource.objects.filter(id__in=resource_ids).values_list('subject', flat=True):
                if row:
                    subjects[_norm(row)] += 1
        for row in Resource.objects.filter(uploaded_by=user).order_by('-added_at')[:12].values_list('subject', flat=True):
            if row:
                subjects[_norm(row)] += 2
    except Exception:
        pass
    klass = ''.join(ch for ch in (getattr(user, 'class_level', '') or '') if ch.isdigit())
    result = (categories, subjects, klass)
    cache.set(key, result, _INTEREST_TTL)
    return result


def _user_interest_sets(user):
    """Back-compat: the interest keys as plain sets."""
    categories, subjects, _ = _user_interests(user)
    return set(categories), set(subjects)


def _affinity(weight):
    """Diminishing returns: the first signal counts most, the tenth adds little."""
    return 0.0 if weight <= 0 else 30.0 + 12.0 * math.log2(1 + weight)


def _post_base(post, now_ms):
    """The part of a post's score that is the same for everyone: freshness and engagement."""
    engagement = (post.thumbs_up_count or 0) * 3 + (post.reply_count or 0) * 2 + min(post.view_count or 0, 1000) * 0.05
    age_h = max(0.0, (now_ms - (post.created_at or now_ms)) / 3600000.0)
    fresh = 36.0 * 0.5 ** (age_h / _POST_HALF_LIFE_H)
    help_wanted = 6.0 if (post.reply_count or 0) == 0 and age_h < 48 else 0.0  # an unanswered question
    return fresh + math.log2(1 + max(engagement, 0)) + help_wanted


def _resource_base(resource, now_ms):
    engagement = ((resource.like_count or 0) * 4 + (resource.comment_count or 0) * 2
                  + min(resource.view_count or 0, 1500) * 0.05)
    age_h = max(0.0, (now_ms - (resource.added_at or now_ms)) / 3600000.0)
    fresh = 36.0 * 0.5 ** (age_h / _RESOURCE_HALF_LIFE_H)
    return fresh + math.log2(1 + max(engagement, 0))


def _score_post(post, now_ms, categories):
    """Kept for callers and tests: base plus interest, as a single number."""
    weight = categories.get(_norm(post.category), 0) if isinstance(categories, Counter) else (1 if _norm(post.category) in categories else 0)
    return _post_base(post, now_ms) + _affinity(weight)


def _score_resource(resource, now_ms, subjects):
    weight = subjects.get(_norm(resource.subject), 0) if isinstance(subjects, Counter) else (1 if _norm(resource.subject) in subjects else 0)
    return _resource_base(resource, now_ms) + _affinity(weight)


_POOLS_KEY = 'suggest_pools_v3'
_POOLS_STAMP_KEY = 'suggest_pools_v3:stamp'
_POOLS_TTL = 60
_local_pools = {}  # {'entry': (stamp, expires_at, pools)}: the shared entry this process last read


def _candidate_pools():
    """The newest posts and resources everyone's deck is ranked from, with each item's shared
    base score worked out once. Identical for every viewer, so cached for a minute; per request
    only the personal part (interest, class, diversity) is added.

    The pools pickle to ~400 KB, which every feed request used to fetch from the cache and
    unpickle. The shared entry now carries a stamp, also stored under its own tiny key: a
    process that already holds the entry with the current stamp (and not past its expiry)
    reuses it instead. Every request still sees exactly the entry the shared cache holds.
    The pooled objects are shared within a process, so build_suggested_deck() hands out
    copies of the ones it picks."""
    from django.core.cache import cache
    mine = _local_pools.get('entry')
    if mine is not None and time.time() < mine[1] and cache.get(_POOLS_STAMP_KEY) == mine[0]:
        return mine[2]
    entry = cache.get(_POOLS_KEY)
    if entry is None:
        now = time.time()
        now_ms = int(now * 1000)
        posts = list(
            Post.objects.filter(is_archived=False, user__email_verified=True)
            .select_related('user').prefetch_related('images', 'media', 'poll__options')
            .order_by('-created_at')[:_RECENT_POOL]
        )
        resources = list(
            Resource.objects.filter(approval_status='approved')
            .select_related('uploaded_by').order_by('-added_at')[:_RECENT_POOL]
        )
        pools = ([(p, _post_base(p, now_ms)) for p in posts], [(r, _resource_base(r, now_ms)) for r in resources])
        entry = (uuid.uuid4().hex, now + _POOLS_TTL, pools)
        cache.set(_POOLS_KEY, entry, _POOLS_TTL)
        cache.set(_POOLS_STAMP_KEY, entry[0], _POOLS_TTL)
    elif cache.get(_POOLS_STAMP_KEY) != entry[0]:
        cache.set(_POOLS_STAMP_KEY, entry[0], max(1, int(entry[1] - time.time())))
    _local_pools['entry'] = entry
    return entry[2]


def _diversify(ranked, key_of, author_of, limit):
    """Greedy re-rank: each pick costs the next item from the same topic or author a little, so
    one subject or one prolific poster cannot fill the deck. Ranked is [(score, obj)]."""
    picked, topics, authors = [], Counter(), Counter()
    pool = list(ranked)
    while pool and len(picked) < limit:
        best_i, best = 0, None
        for i, (score, obj) in enumerate(pool[:limit * 3]):
            adjusted = score - 7.0 * topics[key_of(obj)] - 10.0 * authors[author_of(obj)]
            if best is None or adjusted > best:
                best_i, best = i, adjusted
        score, obj = pool.pop(best_i)
        topics[key_of(obj)] += 1
        authors[author_of(obj)] += 1
        picked.append(obj)
    return picked, [obj for _, obj in pool]


def build_suggested_deck(user, limit=18):
    """Returns (deck, note) where deck is a list of (kind, obj) pairs with
    kind in {'post', 'resource'}. Never empty when the platform holds any
    content (padding falls back to most recent)."""
    categories, subjects, klass = _user_interests(user)
    post_pool, resource_pool = _candidate_pools()
    me = getattr(user, 'id', None)

    ranked_posts = sorted(
        ((base + _affinity(categories.get(_norm(p.category), 0)), p) for p, base in post_pool if p.user_id != me),
        key=lambda x: x[0], reverse=True)
    ranked_resources = sorted(
        ((base + _affinity(subjects.get(_norm(r.subject), 0))
          + (10.0 if klass and klass in (r.grade_level or '') else 0.0), r) for r, base in resource_pool),
        key=lambda x: x[0], reverse=True)

    top_posts, rest_posts = _diversify(ranked_posts, lambda p: _norm(p.category), lambda p: p.user_id, limit)
    top_resources, rest_resources = _diversify(ranked_resources, lambda r: _norm(r.subject), lambda r: r.uploaded_by_id, limit)

    # Interleave so the deck mixes types naturally.
    deck = []
    i = j = 0
    while (i < len(top_resources) or j < len(top_posts)) and len(deck) < limit:
        if i < len(top_resources):
            deck.append(('resource', top_resources[i])); i += 1
        if j < len(top_posts) and len(deck) < limit:
            deck.append(('post', top_posts[j])); j += 1

    # Guarantee: never empty / never thin, pad with plain-recency leftovers.
    if len(deck) < _DECK_MIN:
        seen = {id(obj) for _, obj in deck}
        leftovers = ([('post', p) for p in top_posts[j:] + rest_posts if id(p) not in seen]
                     + [('resource', r) for r in top_resources[i:] + rest_resources if id(r) not in seen])
        leftovers.sort(key=lambda item: getattr(item[1], 'created_at', None) or getattr(item[1], 'added_at', 0) or 0, reverse=True)
        cap = max(_DECK_MIN, min(limit, len(post_pool) + len(resource_pool)))
        for item in leftovers:
            if len(deck) >= cap:
                break
            deck.append(item)

    note = ''
    if not deck:
        note = 'no_content'
    elif not categories and not subjects:
        note = 'explore'  # anonymous/brand-new users: popularity+recency mix
    # The pooled objects are shared by every request in this process; callers get their own
    # copies to hang per-viewer state on (prime_for_serializers sets _viewer_* attributes).
    return [(kind, copy.copy(obj)) for kind, obj in deck], note


def build_suggested_feed(user, limit=18, request=None):
    """Returns (items, note) — DRF-serialized cards for API clients. Never
    empty when the platform holds any content."""
    deck, note = build_suggested_deck(user, limit)
    from .view_helpers import prime_for_serializers
    serializer_context = {'request': request} if request is not None else {}
    serializer_context.update(prime_for_serializers(
        user, posts=[o for k, o in deck if k == 'post'], resources=[o for k, o in deck if k == 'resource']))
    items = []
    for kind, obj in deck:
        if kind == 'post':
            items.append({'type': 'post', 'post': PostSerializer(obj, context=serializer_context).data})
        else:
            items.append({'type': 'resource', 'resource': ResourceSerializer(obj, context=serializer_context).data})
    return items, note


@api_view(['GET'])
@permission_classes([AllowAny])
def feed_suggested(request):
    """GET /api/feed/suggested/?limit=18 — see module docstring."""
    try:
        limit = int(request.GET.get('limit', 18) or 18)
    except (TypeError, ValueError):
        limit = 18
    limit = min(40, max(6, limit))
    user = _get_user_from_request(request)
    items, note = build_suggested_feed(user, limit=limit, request=request)
    return Response({
        'ok': True,
        'items': items,
        'count': len(items),
        'note': note,
        'generatedAt': int(time.time() * 1000),
    })
