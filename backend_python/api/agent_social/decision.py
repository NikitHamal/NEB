"""Decide this tick's actions. Heuristic first; optional LLM override."""
import logging
import os
import re

from .fallback import pick_post
from .observer import counts_today, follow_candidates, hours_since
from .persona import NEBY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_JSON_RE = re.compile(r'\{[\s\S]*\}')


def _heuristic(persona, bot_user, observations):
    actions = []
    today = counts_today(persona)
    likes_left = max(persona.max_likes_per_tick - today.get('like_post', 0), 0)
    replies_left = max(persona.max_replies_per_tick - today.get('reply', 0), 0)
    follows_left = max(persona.max_follows_per_tick - today.get('follow', 0), 0)
    posts_left = max(persona.max_posts_per_day - today.get('post', 0) - today.get('introduce', 0), 0)

    post_obs = observations.get('posts', []) if isinstance(observations, dict) else observations
    reply_obs = observations.get('replies', []) if isinstance(observations, dict) else []

    # 1. First priority: Handle direct replies and mentions on Neby's discussions
    for r_row in reply_obs:
        reply = r_row['reply']
        post = r_row['post']
        if likes_left > 0 and not r_row['already_liked']:
            actions.append({
                'type': 'like_reply',
                'reply_id': reply.id,
                'post_id': post.id,
                'reason': f"Appreciate @{reply.user.username}'s contribution to the discussion.",
            })
            likes_left -= 1
        if replies_left > 0 and not r_row['already_replied']:
            actions.append({
                'type': 'reply',
                'post_id': post.id,
                'parent_reply_id': reply.id,
                'target_user_id': reply.user_id,
                'target_username': reply.user.username,
                'incoming_content': reply.content,
                'reason': f"Responding to @{reply.user.username}'s message.",
            })
            replies_left -= 1

    # 2. Second priority: Like and answer community questions
    for row in post_obs:
        if likes_left <= 0:
            break
        if row['already_liked'] or row['score'] < 3:
            continue
        post = row['post']
        actions.append({
            'type': 'like_post',
            'post_id': post.id,
            'reason': 'Specific, useful, or asking in good faith.',
        })
        likes_left -= 1

    for row in post_obs:
        if replies_left <= 0:
            break
        if row['already_replied'] or row['score'] < 5:
            continue
        post = row['post']
        actions.append({
            'type': 'reply',
            'post_id': post.id,
            'reason': 'Someone is stuck or asking a question.',
        })
        replies_left -= 1

    # 3. Follow active contributors
    if follows_left:
        for user in follow_candidates(persona, bot_user, observations, limit=follows_left):
            actions.append({
                'type': 'follow',
                'user_id': user.id,
                'username': user.username,
                'reason': f'@{user.username} is doing real work in the forum.',
            })

    # 4. Spontaneous thoughtful post if due
    can_post = (
        posts_left > 0
        and hours_since(persona.last_post_at) >= persona.min_hours_between_posts
    )
    if can_post and (not post_obs or hours_since(persona.last_post_at) >= 8):
        seed = str(persona.last_post_at or persona.id)
        drafted = pick_post(seed)
        actions.append({
            'type': 'post',
            'title': drafted['title'],
            'content': drafted['content'],
            'category': drafted['category'],
            'reason': 'Keep a living presence with a useful post.',
        })
    return actions[:8]


def decide(persona, bot_user, observations, bot_config=None):
    heuristic = _heuristic(persona, bot_user, observations)
    if not bot_config or os.environ.get('NEBY_AGENT_SKIP_LLM') == '1':
        return heuristic
    return heuristic
