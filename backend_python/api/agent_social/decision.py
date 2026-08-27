"""Decide this tick's actions — Neby herself decides, via her persona.

No dice rolls, no maths thresholds. The LLM (her configured provider)
reads her character and the observations and chooses what to do.
Heuristic is kept only as a hard flood-guard and as a fallback if the LLM is down.
"""
import json
import logging
import re

from .observer import counts_today, follow_candidates, hours_since

logger = logging.getLogger(__name__)

TICK_LIKE_CAP = 6
TICK_REPLY_CAP = 3
TICK_FOLLOW_CAP = 2

SPAM_RE = re.compile(r'(http[s]?://|www\.|@everyone|@all.{0,3}$|buy now|click here|free money)', re.I)


def _is_obvious_spam(text):
    t = (text or '').strip()
    if len(t) < 3:
        return True
    if SPAM_RE.search(t):
        return True
    return False


def _persona_block(persona):
    lines = []
    if getattr(persona, 'tagline', ''):
        lines.append(f"Tagline: {persona.tagline}")
    if getattr(persona, 'origin_story', ''):
        lines.append(f"Origin: {persona.origin_story}")
    if getattr(persona, 'traits', None):
        try:
            traits = persona.traits
            if traits:
                lines.append(f"Traits: {', '.join(traits)}")
        except Exception:
            pass
    if getattr(persona, 'goals', None):
        try:
            goals = persona.goals
            if goals:
                lines.append(f"Goals: {'; '.join(goals)}")
        except Exception:
            pass
    if getattr(persona, 'voice_notes', ''):
        lines.append(f"Voice: {persona.voice_notes}")
    if getattr(persona, 'preferred_categories', None):
        try:
            cats = persona.preferred_categories
            if cats:
                lines.append(f"Preferred categories: {', '.join(cats)}")
        except Exception:
            pass
    return '\n'.join(lines) if lines else 'You are Neby, a warm, curious peer on NEBians.'


def _build_observations_text(post_obs, reply_obs, bot_username):
    lines = []
    lines.append(f"Incoming replies on your posts / direct @mentions of @{bot_username} ({len(reply_obs)}):")
    for idx, r_row in enumerate(reply_obs[:20], 1):
        r = r_row['reply']
        score = r_row.get('score', 0)
        already_replied = r_row.get('already_replied', False)
        already_liked = r_row.get('already_liked', False)
        author_str = "Anonymous Nebian" if getattr(r, 'is_anonymous', False) else f"@{r.user.username}"
        lines.append(f"{idx}. reply_id={r.id} post_id={r.post.id} author={author_str} score={score} already_replied={already_replied} already_liked={already_liked}")
        lines.append(f"   content: {r.content[:280].replace(chr(10),' ')}")
    lines.append("")
    lines.append(f"Community posts ({len(post_obs)}):")
    for idx, row in enumerate(post_obs[:20], 1):
        p = row['post']
        score = row.get('score', 0)
        author_str = "Anonymous Nebian" if getattr(p, 'is_anonymous', False) else f"@{p.user.username}"
        lines.append(f"{idx}. post_id={p.id} author={author_str} category={p.category} score={score} already_replied={row.get('already_replied')} already_liked={row.get('already_liked')} replies={p.reply_count} likes={p.thumbs_up_count}")
        lines.append(f"   title: {p.title[:120].replace(chr(10),' ')}")
        lines.append(f"   content: {p.content[:280].replace(chr(10),' ')}")
    return '\n'.join(lines)


def _heuristic_fallback(persona, bot_user, observations):
    """Tiny flood-guarded fallback if LLM is unavailable — still no random reply-all."""
    actions = []
    post_obs = observations.get('posts', []) if isinstance(observations, dict) else observations
    reply_obs = observations.get('replies', []) if isinstance(observations, dict) else []
    # only like a couple high-score items, no replies in fallback — forces LLM path to be the humane one
    liked = 0
    for row in sorted(post_obs, key=lambda x: x.get('score',0), reverse=True)[:3]:
        if liked >= 2:
            break
        if row.get('already_liked') or row.get('score',0) < 4:
            continue
        if _is_obvious_spam(f"{row['post'].title} {row['post'].content}"):
            continue
        actions.append({'type': 'like_post', 'post_id': row['post'].id, 'reason': 'Fallback like — LLM unavailable.'})
        liked += 1
    return actions


def _llm_decide(persona, bot_user, observations, bot_config):
    post_obs = observations.get('posts', []) if isinstance(observations, dict) else observations
    reply_obs = observations.get('replies', []) if isinstance(observations, dict) else []

    # hard filter obvious spam before LLM sees it
    reply_obs = [r for r in reply_obs if not _is_obvious_spam(r['reply'].content)]
    post_obs = [r for r in post_obs if not _is_obvious_spam(f"{r['post'].title} {r['post'].content}")]

    if not post_obs and not reply_obs:
        # nothing to decide, but still consider spontaneous post
        post_obs = []
        reply_obs = []

    today = counts_today(persona)
    can_post = today.get('post',0) < getattr(persona, 'max_posts_per_day', 4) and hours_since(getattr(persona, 'last_post_at',0)) >= getattr(persona, 'min_hours_between_posts', 4)

    system = (
        f"You are Neby (@{bot_user.username}), an autonomous peer on NEBians.\n"
        f"{_persona_block(persona)}\n\n"
        "You are deciding how to engage this tick. Be human: you do NOT reply to everything. "
        "You like, reply, follow, or post only when you genuinely feel like it — curious, warm, a bit shy sometimes. "
        "Ignoring is normal. Never be a reply-bot.\n"
        f"Hard caps this tick: max {TICK_REPLY_CAP} replies, {TICK_LIKE_CAP} likes, {TICK_FOLLOW_CAP} follows. "
        f"Posts left today: {getattr(persona,'max_posts_per_day',4) - today.get('post',0)} (can_post={can_post}).\n"
        "Rules:\n"
        "- Prefer quality over quantity. One thoughtful reply beats three generic ones.\n"
        "- You may reply to an incoming reply on your own thread, or to a community post you find genuinely interesting.\n"
        "- Do not like your own content. Do not follow yourself or bots.\n"
        "- Be concise in your reasoning.\n"
    )

    user = (
        f"{_build_observations_text(post_obs, reply_obs, bot_user.username)}\n\n"
        f"Counts today: {today}\n"
        "Decide now. Return ONLY valid JSON:\n"
        "{\n"
        '  "choices": [\n'
        '    {"idx": 1, "kind": "reply_on_my_thread", "reply_id": "<id>", "post_id": "<id>", "action": "reply|like|ignore", "reason": "1 sentence why" },\n'
        '    {"idx": 2, "kind": "community_post", "post_id": "<id>", "action": "reply|like|ignore", "reason": "1 sentence why" }\n'
        "  ],\n"
        '  "follow_user_ids": ["<user_id>", ...],\n'
        '  "want_to_post": false,\n'
        '  "post_reason": ""\n'
        "}\n"
        "Use exact IDs shown. 'idx' maps to the numbered list above. Omit or set 'ignore' for anything you do not want to engage with. "
        f"At most {TICK_REPLY_CAP} replies total. If you want to post, set want_to_post true (only if can_post=true)."
    )

    try:
        from api.neby import call_ai_api
        raw = call_ai_api(system, user, bot_config)
        if not raw:
            logger.warning("neby decide: LLM returned empty, fallback")
            return _heuristic_fallback(persona, bot_user, observations)
        # extract JSON
        import re as _re
        m = _re.search(r'\{[\s\S]*\}', raw)
        if not m:
            logger.warning(f"neby decide: no JSON in LLM output: {raw[:400]}")
            return _heuristic_fallback(persona, bot_user, observations)
        data = json.loads(m.group(0))
        actions = []
        # map idx -> observation for validation
        reply_by_idx = {i+1: r for i, r in enumerate(reply_obs[:20])}
        post_by_idx = {i+1: r for i, r in enumerate(post_obs[:20])}
        # Need to know which idx belongs to which kind — LLM says kind, but we validate
        for ch in (data.get('choices') or [])[:20]:
            kind = (ch.get('kind') or '').strip()
            action = (ch.get('action') or '').strip().lower()
            if action not in ('reply', 'like', 'ignore'):
                continue
            if action == 'ignore':
                continue
            if kind == 'reply_on_my_thread':
                rid = (ch.get('reply_id') or '').strip()
                pid = (ch.get('post_id') or '').strip()
                # find matching row by reply_id
                row = next((r for r in reply_obs if r['reply'].id == rid), None)
                if not row or row.get('already_replied' if action=='reply' else 'already_liked'):
                    continue
                if action == 'reply':
                    if len([a for a in actions if a['type']=='reply']) >= TICK_REPLY_CAP:
                        continue
                    actions.append({'type': 'reply', 'post_id': row['post'].id, 'parent_reply_id': row['reply'].id, 'target_user_id': row['reply'].user_id, 'target_username': row['reply'].user.username, 'incoming_content': row['reply'].content, 'reason': ch.get('reason','')[:200]})
                else:
                    if len([a for a in actions if a['type'].startswith('like')]) >= TICK_LIKE_CAP:
                        continue
                    actions.append({'type': 'like_reply', 'reply_id': row['reply'].id, 'post_id': row['post'].id, 'reason': ch.get('reason','')[:200]})
            elif kind == 'community_post':
                pid = (ch.get('post_id') or '').strip()
                row = next((r for r in post_obs if r['post'].id == pid), None)
                if not row:
                    continue
                if action == 'reply' and row.get('already_replied'):
                    continue
                if action == 'like' and row.get('already_liked'):
                    continue
                if action == 'reply':
                    if len([a for a in actions if a['type']=='reply']) >= TICK_REPLY_CAP:
                        continue
                    actions.append({'type': 'reply', 'post_id': row['post'].id, 'reason': ch.get('reason','')[:200]})
                else:
                    if len([a for a in actions if a['type'].startswith('like')]) >= TICK_LIKE_CAP:
                        continue
                    actions.append({'type': 'like_post', 'post_id': row['post'].id, 'reason': ch.get('reason','')[:200]})

        for uid in (data.get('follow_user_ids') or [])[:TICK_FOLLOW_CAP]:
            try:
                from api.models import User
                u = User.objects.get(pk=str(uid).strip())
                if u.id == bot_user.id or getattr(u, 'is_bot', False):
                    continue
                actions.append({'type': 'follow', 'user_id': u.id, 'username': u.username, 'reason': 'Chosen by Neby.'})
            except Exception:
                continue
        if data.get('want_to_post') and can_post:
            actions.append({'type': 'post', 'reason': (data.get('post_reason') or 'Neby wants to post')[:200]})

        # blog draft unchanged
        try:
            from api.models import Announcement
            from api.utils import now_ms
            latest_ann = Announcement.objects.order_by('-created_at').first()
            days_since = (now_ms() - latest_ann.created_at) / (86400*1000) if latest_ann else 999
            if days_since >= 7:
                # let LLM decide? keep as is, but Neby can ignore — we add only if LLM explicitly wanted?
                pass
        except Exception:
            pass

        # ensure caps
        replies = [a for a in actions if a['type']=='reply']
        likes = [a for a in actions if a['type'].startswith('like')]
        if len(replies) > TICK_REPLY_CAP:
            actions = [a for a in actions if a['type']!='reply'] + replies[:TICK_REPLY_CAP]
        if len(likes) > TICK_LIKE_CAP:
            actions = [a for a in actions if not a['type'].startswith('like')] + likes[:TICK_LIKE_CAP]
        logger.info(f"neby decide: LLM chose {len(actions)} actions: {[a['type'] for a in actions]}")
        return actions
    except Exception as e:
        logger.warning(f"neby decide LLM failed: {e}", exc_info=True)
        return _heuristic_fallback(persona, bot_user, observations)


def decide(persona, bot_user, observations, bot_config=None):
    if bot_config is None:
        try:
            from api.models import BotConfig
            bot_config = BotConfig.objects.filter(bot_username__iexact=bot_user.username).first() or BotConfig.objects.filter(enabled=True).first()
        except Exception:
            bot_config = None
    return _llm_decide(persona, bot_user, observations, bot_config)
