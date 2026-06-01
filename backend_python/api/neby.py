"""
Neby AI Bot — detects @neby mentions and generates contextual replies.

This is an experimental feature. The entire system can be disabled via
BotConfig.enabled = False, which will cause all trigger checks to short-circuit
before making any API calls.

The AI proxy used is the same Qwen proxy from the AstroWeb project.
"""
import logging
import re
import time
import uuid

import requests
from django.db import transaction
from django.db.models import F

from .models import BotConfig, User, Post, Reply

logger = logging.getLogger(__name__)


def _now_ms():
    return int(time.time() * 1000)


def is_neby_enabled():
    """Quick check if Neby is enabled without hitting the DB every time.
    Uses Django cache for 60s TTL to avoid repeated DB reads on every post/reply.
    """
    from django.core.cache import cache
    cache_key = 'neby_enabled'
    val = cache.get(cache_key)
    if val is not None:
        return val
    try:
        config = BotConfig.get_config()
        enabled = config.enabled and bool(BotConfig.get_bot_user())
    except Exception:
        enabled = False
    cache.set(cache_key, enabled, 60)
    return enabled


def detect_mention(text, bot_username='neby'):
    """Check if text contains @bot_username mention. Returns True if mentioned."""
    pattern = re.compile(r'@' + re.escape(bot_username) + r'\b', re.IGNORECASE)
    return bool(pattern.search(text))


def _build_post_context(post, max_replies=10):
    """Build context string from a post and its recent replies for the AI prompt."""
    lines = []
    try:
        author_name = post.user.display_name or post.user.username
    except Exception:
        author_name = 'Unknown'
    lines.append(f"Post by {author_name} (in category: {post.category}):")
    lines.append(f"Title: {post.title}")
    lines.append(f"Content: {post.content}")
    lines.append("")
    replies = Reply.objects.filter(post=post, is_archived=False).select_related('user').order_by('created_at')[:max_replies]
    if replies:
        lines.append(f"Replies ({replies.count()} shown):")
        for r in replies:
            try:
                r_name = r.user.display_name or r.user.username
            except Exception:
                r_name = 'Unknown'
            lines.append(f"  {r_name}: {r.content}")
        lines.append("")
    lines.append("Please write a helpful reply to this post as Neby. Keep it concise and relevant to the NEB curriculum or the student's question.")
    return '\n'.join(lines)


def _build_reply_context(reply, max_context_replies=10):
    """Build context string when Neby is mentioned in a reply."""
    lines = []
    post = reply.post
    try:
        post_author = post.user.display_name or post.user.username
    except Exception:
        post_author = 'Unknown'
    try:
        reply_author = reply.user.display_name or reply.user.username
    except Exception:
        reply_author = 'Unknown'
    lines.append(f"Post by {post_author} (category: {post.category}):")
    lines.append(f"Title: {post.title}")
    lines.append(f"Content: {post.content}")
    lines.append("")
    recent_replies = Reply.objects.filter(
        post=post, is_archived=False, created_at__lt=reply.created_at
    ).select_related('user').order_by('-created_at')[:max_context_replies]
    if recent_replies:
        lines.append("Recent replies before this one:")
        for r in reversed(list(recent_replies)):
            try:
                r_name = r.user.display_name or r.user.username
            except Exception:
                r_name = 'Unknown'
            lines.append(f"  {r_name}: {r.content}")
        lines.append("")
    lines.append(f"{reply_author} just wrote (mentioning you): {reply.content}")
    lines.append("")
    lines.append("Please write a helpful reply as Neby. Keep it concise and relevant.")
    return '\n'.join(lines)


def call_ai_api(system_prompt, user_message, config=None):
    """Call the Qwen AI proxy API. Returns the assistant's response text or None on error."""
    if config is None:
        config = BotConfig.get_config()
    headers = {
        'Content-Type': 'application/json',
    }
    if config.api_key:
        headers['Authorization'] = f'Bearer {config.api_key}'
    payload = {
        'model': config.model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message},
        ],
        'stream': False,
        'max_tokens': config.response_max_length or 500,
    }
    try:
        resp = requests.post(
            config.api_url,
            json=payload,
            headers=headers,
            timeout=30,
        )
        if resp.status_code == 429:
            logger.warning('Neby AI API rate limited (429)')
            return None
        if resp.status_code != 200:
            logger.error(f'Neby AI API error: {resp.status_code} {resp.text[:500]}')
            return None
        data = resp.json()
        choices = data.get('choices', [])
        if not choices:
            logger.error(f'Neby AI API: no choices in response')
            return None
        content = choices[0].get('message', {}).get('content', '')
        if not content:
            reasoning = choices[0].get('message', {}).get('reasoning_content', '')
            if reasoning:
                content = reasoning
        return content.strip() if content else None
    except requests.Timeout:
        logger.error('Neby AI API timeout')
        return None
    except Exception as e:
        logger.error(f'Neby AI API exception: {e}')
        return None


def trigger_neby_reply_post(post):
    """Called after a new post is created. If @neby is mentioned, generate a reply asynchronously."""
    if not is_neby_enabled():
        return None
    config = BotConfig.get_config()
    bot_user = BotConfig.get_bot_user()
    if not bot_user:
        return None
    if not detect_mention(post.content, config.bot_username) and not detect_mention(post.title, config.bot_username):
        return None
    import threading
    post_id = post.id
    bot_user_id = bot_user.id
    config_id = config.id

    def _run():
        try:
            config = BotConfig.objects.get(pk=config_id)
            bot_user = User.objects.get(pk=bot_user_id)
            post = Post.objects.get(pk=post_id)
            context = _build_post_context(post, max_replies=config.max_context_replies)
            response_text = call_ai_api(config.system_prompt, context, config)
            if not response_text:
                return
            with transaction.atomic():
                reply = Reply.objects.create(
                    id=str(uuid.uuid4()),
                    post=post,
                    parent_reply_id=None,
                    user=bot_user,
                    content=response_text,
                    thumbs_up_count=0,
                    reply_count=0,
                    created_at=_now_ms(),
                )
                Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
            from . import counters as _counters
            _counters.increment_user_reply_count(bot_user.id)
            logger.info(f'Neby replied to post {post.id}')
        except Exception as e:
            logger.error(f'Neby async reply to post failed: {e}')

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return None


def trigger_neby_reply_reply(reply):
    """Called after a new reply is created. If @neby is mentioned, generate a reply asynchronously."""
    if not is_neby_enabled():
        return None
    config = BotConfig.get_config()
    bot_user = BotConfig.get_bot_user()
    if not bot_user:
        return None
    if not detect_mention(reply.content, config.bot_username):
        return None
    if reply.user_id == bot_user.id:
        return None
    import threading
    reply_id = reply.id
    post_id = reply.post_id
    parent_reply_id = reply.parent_reply_id
    bot_user_id = bot_user.id
    config_id = config.id

    def _run():
        try:
            config = BotConfig.objects.get(pk=config_id)
            bot_user = User.objects.get(pk=bot_user_id)
            reply = Reply.objects.select_related('post', 'user').get(pk=reply_id)
            context = _build_reply_context(reply, max_context_replies=config.max_context_replies)
            response_text = call_ai_api(config.system_prompt, context, config)
            if not response_text:
                return
            with transaction.atomic():
                neby_reply = Reply.objects.create(
                    id=str(uuid.uuid4()),
                    post_id=post_id,
                    parent_reply_id=parent_reply_id,
                    user=bot_user,
                    content=response_text,
                    thumbs_up_count=0,
                    reply_count=0,
                    created_at=_now_ms(),
                )
                Post.objects.filter(pk=post_id).update(reply_count=F('reply_count') + 1)
                Reply.objects.filter(pk=reply_id).update(reply_count=F('reply_count') + 1)
            from . import counters as _counters
            _counters.increment_user_reply_count(bot_user.id)
            logger.info(f'Neby replied to reply {reply_id}')
        except Exception as e:
            logger.error(f'Neby async reply to reply failed: {e}')

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return None