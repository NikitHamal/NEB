"""Scan the forum for things an autonomous agent might care about."""
from datetime import timedelta

from django.db.models import Q

from api.models import Follow, Post, PostLike, Reply, ReplyLike, User
from api.utils import now_ms

from .models import AgentAction

QUESTION_RE = r'\?|\b(help|stuck|how do|how to|why does|anyone|please|exam|neb|board)\b'


def _day_start_ms():
    import time
    now = time.time()
    return int((now - (now % 86400)) * 1000)


def already_acted(persona, action_type, target_id):
    if not target_id:
        return False
    return AgentAction.objects.filter(
        persona=persona,
        action_type=action_type,
        target_id=str(target_id),
        status='done',
    ).exists()


def counts_today(persona):
    since = _day_start_ms()
    qs = AgentAction.objects.filter(persona=persona, status='done', created_at__gte=since)
    return {
        'post': qs.filter(action_type='post').count(),
        'reply': qs.filter(action_type='reply').count(),
        'like_post': qs.filter(action_type='like_post').count(),
        'follow': qs.filter(action_type='follow').count(),
        'introduce': qs.filter(action_type='introduce').count(),
    }


def observe(persona, bot_user, window_hours=720, limit=100):
    since = now_ms() - int(window_hours * 3600 * 1000)

    # 1. Observe incoming replies on posts created by bot or mentioning bot
    my_post_ids = set(Post.objects.filter(user=bot_user, is_archived=False).values_list('id', flat=True))
    replied_post_ids = set(Reply.objects.filter(user=bot_user, is_archived=False).values_list('post_id', flat=True))
    relevant_post_ids = my_post_ids | replied_post_ids

    incoming_replies = list(
        Reply.objects.filter(
            Q(post_id__in=relevant_post_ids) | Q(content__icontains=f"@{bot_user.username}") | Q(content__icontains="neby"),
            is_archived=False,
            is_anonymous=False,
            created_at__gte=since,
        )
        .exclude(user_id=bot_user.id)
        .select_related('user', 'post')
        .order_by('-created_at')[:200]
    )

    liked_reply_ids = set(
        ReplyLike.objects.filter(user=bot_user, reply_id__in=[r.id for r in incoming_replies])
        .values_list('reply_id', flat=True)
    )

    scored_replies = []
    for r in incoming_replies:
        if getattr(r.user, 'is_bot', False):
            continue
        score = 8
        if r.post_id in my_post_ids:
            score += 6
        if f"@{bot_user.username}".lower() in r.content.lower() or "neby" in r.content.lower():
            score += 5
        scored_replies.append({
            'reply': r,
            'post': r.post,
            'score': score,
            'already_liked': r.id in liked_reply_ids or already_acted(persona, 'like_reply', r.id),
            'already_replied': already_acted(persona, 'reply', r.id) or already_acted(persona, 'reply', f"{r.post_id}:{r.id}"),
            'already_following_author': False,
        })
    scored_replies.sort(key=lambda row: -row['score'])

    # 2. Observe community posts across the forum
    posts = list(
        Post.objects.filter(
            is_archived=False,
            is_anonymous=False,
            user__email_verified=True,
            created_at__gte=since,
        )
        .exclude(user_id=bot_user.id)
        .select_related('user')
        .order_by('-created_at')[:limit]
    )

    liked_ids = set(
        PostLike.objects.filter(user=bot_user, post_id__in=[p.id for p in posts])
        .values_list('post_id', flat=True)
    )
    replied_ids = set(
        Reply.objects.filter(user=bot_user, post_id__in=[p.id for p in posts], is_archived=False)
        .values_list('post_id', flat=True)
    )
    following_ids = set(
        Follow.objects.filter(follower=bot_user).values_list('following_id', flat=True)
    )

    scored = []
    for post in posts:
        if getattr(post.user, 'is_bot', False):
            continue
        score = 0
        blob = f"{post.title} {post.content}".lower()
        if '?' in blob:
            score += 4
        if any(w in blob for w in ('help', 'stuck', 'exam', 'neb', 'please', 'how', 'why')):
            score += 3
        if post.reply_count == 0:
            score += 3
        elif post.reply_count <= 2:
            score += 1
        if post.category in (persona.preferred_categories or []):
            score += 2
        age_h = max((now_ms() - post.created_at) / 3600000, 0.2)
        score += max(0, 3 - age_h / 6)
        scored.append({
            'post': post,
            'score': score,
            'already_liked': post.id in liked_ids,
            'already_replied': post.id in replied_ids or already_acted(persona, 'reply', post.id),
            'already_following_author': post.user_id in following_ids,
        })
    scored.sort(key=lambda row: -row['score'])

    return {
        'posts': scored[:limit],
        'replies': scored_replies[:50],
    }


def follow_candidates(persona, bot_user, observations, limit=5):
    out = []
    seen = set()
    post_obs = observations.get('posts', []) if isinstance(observations, dict) else observations
    reply_obs = observations.get('replies', []) if isinstance(observations, dict) else []
    for row in (reply_obs + post_obs):
        user = row.get('reply', row.get('post', None))
        user = getattr(user, 'user', None)
        if not user or user.id in seen or user.id == bot_user.id:
            continue
        if getattr(user, 'is_bot', False) or user.is_locked:
            continue
        if row.get('already_following_author'):
            continue
        if already_acted(persona, 'follow', user.id):
            continue
        seen.add(user.id)
        out.append(user)
        if len(out) >= limit:
            break
    return out


def hours_since(ms_ts):
    if not ms_ts:
        return 10**6
    return (now_ms() - ms_ts) / 3600000.0
