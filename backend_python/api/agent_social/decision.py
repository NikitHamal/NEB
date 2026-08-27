"""Decide this tick's actions — humane, personality-driven.

Neby is a peer, not a bot. She chooses to engage, not to spam.
- Low per-tick caps, randomization, and per-user de-dupe keep it human.
- Personality (traits/goals/voice) and content quality gate replies.
- Direct @mentions are high-priority but not 100% (she may stay quiet).
- Community posts: only high-score + random + curiosity match.
"""
import logging
import random
import re

from .observer import counts_today, follow_candidates, hours_since

logger = logging.getLogger(__name__)

TICK_LIKE_CAP = 6
TICK_REPLY_CAP = 3
TICK_FOLLOW_CAP = 2

SPAM_RE = re.compile(r'(http[s]?://|www\.|@everyone|@all.{0,3}$|buy now|click here|free money)', re.I)
SHORT_RE = re.compile(r'^\s*(hi|hello|hey|ok|thanks|thank you|nice|sanchai|k cha|\.+|!+|👍|🙏)+\s*$', re.I)


def _is_low_quality(text):
    t = (text or '').strip()
    if len(t) < 8:
        return True
    if SHORT_RE.match(t):
        return True
    if SPAM_RE.search(t):
        return True
    if len(t.split()) < 2 and '?' not in t:
        return True
    return False


def _reply_probability_for_reply_row(persona, r_row):
    """Probability Neby feels like replying to an incoming reply on her thread."""
    content = (r_row['reply'].content or '')
    score = r_row.get('score', 0)
    traits = [s.lower() for s in (persona.traits or [])]
    # base: 65% for direct replies on her posts, lower if already many replies today
    base = 0.65
    if '?' in content:
        base += 0.15
    if len(content.strip()) > 60:
        base += 0.08
    if any(w in content.lower() for w in ('help', 'please', 'how', 'why', 'exam', 'neb')):
        base += 0.07
    if _is_low_quality(content):
        base -= 0.35
    if score >= 12:
        base += 0.10
    if 'curious' in traits or 'curious' in ' '.join(traits):
        if '?' in content:
            base += 0.05
    # recent burst: if she replied very recently (<15 min), be quieter
    if hours_since(getattr(persona, 'last_reply_at', 0)) < 0.25:
        base -= 0.20
    return max(0.08, min(0.92, base))


def _reply_probability_for_post_row(persona, row):
    content = f"{row['post'].title} {row['post'].content}"
    score = row.get('score', 0)
    base = 0.18
    if score >= 6:
        base = 0.30
    if score >= 8:
        base = 0.42
    if _is_low_quality(content):
        return 0.02
    if len((row['post'].content or '').strip()) < 25:
        base -= 0.10
    traits = [s.lower() for s in (persona.traits or [])]
    cats = [c.lower() for c in (persona.preferred_categories or [])]
    if cats and row['post'].category and row['post'].category.lower() in cats:
        base += 0.12
    if any(w in content.lower() for w in ('help', 'stuck', 'please', 'how to', 'why does')):
        base += 0.10
    if hours_since(getattr(persona, 'last_reply_at', 0)) < 0.5:
        base -= 0.12
    return max(0.05, min(0.75, base))


def _heuristic(persona, bot_user, observations):
    actions = []
    today = counts_today(persona)
    posts_left = max(persona.max_posts_per_day - today.get('post', 0) - today.get('introduce', 0), 0)
    follows_left = min(max(persona.max_follows_per_tick - today.get('follow', 0), 0), TICK_FOLLOW_CAP)

    likes_this_tick = 0
    replies_this_tick = 0
    replied_users_this_tick = set()

    post_obs = observations.get('posts', []) if isinstance(observations, dict) else observations
    reply_obs = observations.get('replies', []) if isinstance(observations, dict) else []

    # 1. Direct replies/mentions on Neby's posts — selective, not every single one
    for r_row in reply_obs:
        if replies_this_tick >= TICK_REPLY_CAP and likes_this_tick >= TICK_LIKE_CAP:
            break
        reply = r_row['reply']
        post = r_row['post']
        if reply.user_id in replied_users_this_tick:
            continue

        if not r_row['already_liked'] and likes_this_tick < TICK_LIKE_CAP:
            # like is more generous than reply (~75% if not spam)
            if not _is_low_quality(reply.content) and random.random() < 0.75:
                actions.append({
                    'type': 'like_reply',
                    'reply_id': reply.id,
                    'post_id': post.id,
                    'reason': f"@{reply.user.username} said something worth acknowledging.",
                })
                likes_this_tick += 1

        if not r_row['already_replied'] and replies_this_tick < TICK_REPLY_CAP:
            if r_row.get('already_liked') is False or True:
                p = _reply_probability_for_reply_row(persona, r_row)
                if random.random() < p:
                    actions.append({
                        'type': 'reply',
                        'post_id': post.id,
                        'parent_reply_id': reply.id,
                        'target_user_id': reply.user_id,
                        'target_username': reply.user.username,
                        'incoming_content': reply.content,
                        'reason': f"Neby chose to reply to @{reply.user.username} (p={p:.2f}).",
                    })
                    replies_this_tick += 1
                    replied_users_this_tick.add(reply.user_id)
                else:
                    logger.info(f"neby decide: skipped reply to {reply.id} p={p:.2f}")

    # 2. Community posts — likes sparingly, replies rarely and only when curious
    random.shuffle(post_obs)
    for row in post_obs:
        if likes_this_tick >= TICK_LIKE_CAP:
            break
        if row['already_liked'] or row['score'] < 2:
            continue
        if row['post'].user_id in replied_users_this_tick:
            continue
        if _is_low_quality(f"{row['post'].title} {row['post'].content}"):
            continue
        if random.random() < 0.35:
            actions.append({
                'type': 'like_post',
                'post_id': row['post'].id,
                'reason': 'Post looks interesting or useful.',
            })
            likes_this_tick += 1

    # sort again by score for reply selection after shuffle
    post_obs_sorted = sorted(post_obs, key=lambda r: r.get('score', 0), reverse=True)
    for row in post_obs_sorted:
        if replies_this_tick >= TICK_REPLY_CAP:
            break
        if row['already_replied'] or row['score'] < 4:
            continue
        if row['post'].user_id in replied_users_this_tick:
            continue
        p = _reply_probability_for_post_row(persona, row)
        if random.random() < p:
            actions.append({
                'type': 'reply',
                'post_id': row['post'].id,
                'reason': f"Neby felt curious about this (score={row.get('score')}, p={p:.2f}).",
            })
            replies_this_tick += 1
            replied_users_this_tick.add(row['post'].user_id)

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
