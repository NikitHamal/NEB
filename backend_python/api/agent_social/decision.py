"""Decide this tick's actions.

Likes and replies have NO hard daily caps. Neby engages on its own terms
based on what it hasn't already seen. The only hard limits kept are:
  - Posts: max_posts_per_day / min_hours_between_posts (set on persona)
  - Anti-spam: generous per-tick ceilings as a pure flood guard
  - Duplicate guard: already_liked / already_replied prevents re-engaging
"""
import logging
import os

from .observer import counts_today, follow_candidates, hours_since

logger = logging.getLogger(__name__)

TICK_LIKE_CAP = 30
TICK_REPLY_CAP = 20
TICK_FOLLOW_CAP = 5


def _heuristic(persona, bot_user, observations):
    actions = []
    today = counts_today(persona)
    posts_left = max(persona.max_posts_per_day - today.get('post', 0) - today.get('introduce', 0), 0)
    follows_left = min(max(persona.max_follows_per_tick - today.get('follow', 0), 0), TICK_FOLLOW_CAP)

    likes_this_tick = 0
    replies_this_tick = 0

    post_obs = observations.get('posts', []) if isinstance(observations, dict) else observations
    reply_obs = observations.get('replies', []) if isinstance(observations, dict) else []

    # 1. Handle all direct replies/mentions on Neby's posts — no daily cap, just flood guard
    for r_row in reply_obs:
        if likes_this_tick >= TICK_LIKE_CAP and replies_this_tick >= TICK_REPLY_CAP:
            break
        reply = r_row['reply']
        post = r_row['post']

        if not r_row['already_liked'] and likes_this_tick < TICK_LIKE_CAP:
            actions.append({
                'type': 'like_reply',
                'reply_id': reply.id,
                'post_id': post.id,
                'reason': f"@{reply.user.username} said something worth acknowledging.",
            })
            likes_this_tick += 1

        if not r_row['already_replied'] and replies_this_tick < TICK_REPLY_CAP:
            actions.append({
                'type': 'reply',
                'post_id': post.id,
                'parent_reply_id': reply.id,
                'target_user_id': reply.user_id,
                'target_username': reply.user.username,
                'incoming_content': reply.content,
                'reason': f"Neby's own call — responding to @{reply.user.username}.",
            })
            replies_this_tick += 1

    # 2. Community posts — like anything worth noticing, reply where Neby feels like it
    for row in post_obs:
        if likes_this_tick >= TICK_LIKE_CAP:
            break
        if row['already_liked'] or row['score'] < 2:
            continue
        post = row['post']
        actions.append({
            'type': 'like_post',
            'post_id': post.id,
            'reason': 'Post looks interesting or useful.',
        })
        likes_this_tick += 1

    for row in post_obs:
        if replies_this_tick >= TICK_REPLY_CAP:
            break
        if row['already_replied'] or row['score'] < 4:
            continue
        post = row['post']
        actions.append({
            'type': 'reply',
            'post_id': post.id,
            'reason': "Neby's call — worth contributing something.",
        })
        replies_this_tick += 1

    # 3. Follow active contributors (mild cap retained)
    if follows_left:
        for user in follow_candidates(persona, bot_user, observations, limit=follows_left):
            actions.append({
                'type': 'follow',
                'user_id': user.id,
                'username': user.username,
                'reason': f'@{user.username} is active and genuine.',
            })

    # 4. Spontaneous post — hard daily cap + cooldown fully retained
    can_post = (
        posts_left > 0
        and hours_since(persona.last_post_at) >= persona.min_hours_between_posts
    )
    if can_post and (not post_obs or hours_since(persona.last_post_at) >= 8):
        actions.append({
            'type': 'post',
            'reason': 'Spontaneously share a thought, question, or discussion with the community.',
        })

    # 5. Periodic Feature & Updates Blog Draft (e.g., if no announcement drafted in > 7 days)
    try:
        from api.models import Announcement
        from api.utils import now_ms
        latest_ann = Announcement.objects.order_by('-created_at').first()
        days_since_last_blog = (now_ms() - latest_ann.created_at) / (86400 * 1000) if latest_ann else 999
        if days_since_last_blog >= 7:
            actions.append({
                'type': 'draft_blog',
                'reason': 'Draft an informative feature update / spotlight blog post.',
            })
    except Exception:
        pass

    return actions


def decide(persona, bot_user, observations, bot_config=None):
    return _heuristic(persona, bot_user, observations)
