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

import math
import time

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Bookmark, Post, Resource
from .serializers import PostSerializer, ResourceSerializer
from .view_helpers import _get_user_from_request

_RECENT_POOL = 90  # candidates per side before scoring
_DECK_MIN = 12     # padding guarantees at least this many when content exists


def _user_interest_sets(user):
    """Categories/subjects the user has authored, bookmarked or replied in."""
    categories = set()
    subjects = set()
    if user is None:
        return categories, subjects
    try:
        for row in Post.objects.filter(user=user).order_by('-created_at')[:12].values_list('category', flat=True):
            if row:
                categories.add(row.strip().lower())
    except Exception:
        pass
    try:
        bookmarked_posts = Bookmark.objects.filter(user=user, target_type='post').order_by('-created_at')[:12]
        post_ids = [b.target_id for b in bookmarked_posts]
        for row in Post.objects.filter(id__in=post_ids).values_list('category', flat=True):
            if row:
                categories.add(row.strip().lower())
        bookmarked_resources = Bookmark.objects.filter(user=user, target_type='resource').order_by('-created_at')[:12]
        resource_ids = [b.target_id for b in bookmarked_resources]
        for row in Resource.objects.filter(id__in=resource_ids).values_list('subject', flat=True):
            if row:
                subjects.add(row.strip().lower())
    except Exception:
        pass
    try:
        for row in Resource.objects.filter(uploaded_by=user).order_by('-added_at')[:12].values_list('subject', flat=True):
            if row:
                subjects.add(row.strip().lower())
    except Exception:
        pass
    return categories, subjects


def _score_post(post, now_ms, categories):
    engagement = (post.thumbs_up_count or 0) * 3 + (post.reply_count or 0) * 2 + min(post.view_count or 0, 1000) * 0.05
    age_hours = max(0.0, (now_ms - (post.created_at or now_ms)) / 3600000.0)
    recency = max(0.0, 36.0 - age_hours / 4.0)
    relevance = 42.0 if (post.category or '').strip().lower() in categories else 0.0
    # log-damping keeps mega-threads from permanently owning the deck
    base = math.log2(1 + max(engagement, 0)) if engagement > 0 else 0.0
    return relevance + recency + base


def _score_resource(resource, now_ms, subjects):
    engagement = ((resource.like_count or 0) * 4 + (resource.comment_count or 0) * 2
                  + min(resource.view_count or 0, 1500) * 0.05)
    age_hours = max(0.0, (now_ms - (resource.added_at or now_ms)) / 3600000.0)
    recency = max(0.0, 36.0 - age_hours / 6.0)
    relevance = 46.0 if (resource.subject or '').strip().lower() in subjects else 0.0
    base = math.log2(1 + max(engagement, 0)) if engagement > 0 else 0.0
    return relevance + recency + base


def build_suggested_deck(user, limit=18):
    """Returns (deck, note) where deck is a list of (kind, obj) pairs with
    kind in {'post', 'resource'}. Never empty when the platform holds any
    content (padding falls back to most recent)."""
    now_ms = int(time.time() * 1000)
    categories, subjects = _user_interest_sets(user)

    post_pool = list(
        Post.objects.filter(is_archived=False, user__email_verified=True)
        .select_related('user').prefetch_related('images', 'media', 'poll')
        .order_by('-created_at')[:_RECENT_POOL]
    )
    resource_pool = list(
        Resource.objects.filter(approval_status='approved')
        .order_by('-added_at')[:_RECENT_POOL]
    )

    ranked_posts = sorted(post_pool, key=lambda p: _score_post(p, now_ms, categories), reverse=True)
    ranked_resources = sorted(resource_pool, key=lambda r: _score_resource(r, now_ms, subjects), reverse=True)

    # Interleave top-scored content so the deck mixes types naturally.
    deck = []
    top_posts = ranked_posts[:limit]
    top_resources = ranked_resources[:limit]
    i = j = 0
    while i < len(top_resources) or j < len(top_posts):
        if i < len(top_resources):
            deck.append(('resource', top_resources[i])); i += 1
        if j < len(top_posts):
            deck.append(('post', top_posts[j])); j += 1
        if len(deck) >= limit:
            break

    # Guarantee: never empty / never thin — pad with plain-recency leftovers.
    if len(deck) < _DECK_MIN:
        seen = {id(obj) for _, obj in deck}
        leftovers = ([('post', p) for p in ranked_posts if id(p) not in seen]
                     + [('resource', r) for r in ranked_resources if id(r) not in seen])
        leftovers.sort(key=lambda item: getattr(item[1], 'created_at', getattr(item[1], 'added_at', 0)), reverse=True)
        for item in leftovers:
            if len(deck) >= max(_DECK_MIN, min(limit, len(post_pool) + len(resource_pool))):
                break
            deck.append(item)

    note = ''
    if not deck:
        note = 'no_content'
    elif not categories and not subjects:
        note = 'explore'  # anonymous/brand-new users: popularity+recency mix
    return deck, note


def build_suggested_feed(user, limit=18, request=None):
    """Returns (items, note) — DRF-serialized cards for API clients. Never
    empty when the platform holds any content."""
    deck, note = build_suggested_deck(user, limit)
    serializer_context = {'request': request} if request is not None else {}
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
