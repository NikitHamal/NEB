"""
Neby AI Bot — detects @neby mentions and generates contextual replies.

This is an experimental feature. The entire system can be disabled via
BotConfig.enabled = False, which will cause all trigger checks to short-circuit
before making any API calls.

The AI calls go directly to chat.qwen.ai using our own browser session spoofing
(qwen_proxy module). No external proxy or API key needed.
"""
import logging
import re
import time
import uuid

from django.db import transaction
from django.db.models import F

from .models import BotConfig, User, Post, Reply

logger = logging.getLogger(__name__)


def _now_ms():
    return int(time.time() * 1000)


def is_neby_enabled():
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
    pattern = re.compile(r'@' + re.escape(bot_username) + r'\b', re.IGNORECASE)
    return bool(pattern.search(text))


def _build_post_context(post, max_replies=10):
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
    lines.append("Please write a helpful reply to this post as Neby. Keep it concise and relevant to the student's question.")
    return '\n'.join(lines), None


def _build_reply_context(reply, max_context_replies=10):
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
    return '\n'.join(lines), reply_author


def call_ai_api(system_prompt, user_message, config=None):
    """Call Qwen AI directly via our own proxy. Returns response text or None."""
    from .qwen_proxy import call_qwen
    if config is None:
        config = BotConfig.get_config()
    model = config.model or 'qwen3.6-plus'
    max_tokens = config.response_max_length or 500
    return call_qwen(system_prompt, user_message, model=model, max_tokens=max_tokens)


def trigger_neby_reply_post(post):
    if not is_neby_enabled():
        logger.debug('Neby: trigger skipped (not enabled)')
        return None
    config = BotConfig.get_config()
    bot_user = BotConfig.get_bot_user()
    if not bot_user:
        logger.debug('Neby: trigger skipped (no bot user)')
        return None
    if not detect_mention(post.content, config.bot_username) and not detect_mention(post.title, config.bot_username):
        return None
    logger.info(f'Neby: @mention detected in post {post.id}, generating reply')
    try:
        context, _ = _build_post_context(post, max_replies=config.max_context_replies)
        response_text = call_ai_api(config.system_prompt, context, config)
        if not response_text:
            logger.warning(f'Neby: no response from AI for post {post.id}')
            return None
        try:
            author_display = post.user.display_name or post.user.username
        except Exception:
            author_display = None
        if author_display and not response_text.startswith('@'):
            response_text = f'@{author_display} {response_text}'
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
        from . import notifications as _notif
        _notif.notify_new_reply(bot_user.id, post.id, reply.id)
        logger.info(f'Neby replied to post {post.id}')
        return reply
    except Exception as e:
        logger.error(f'Neby reply to post failed: {e}', exc_info=True)
        return None


def trigger_neby_reply_reply(reply):
    if not is_neby_enabled():
        logger.debug('Neby: trigger skipped (not enabled)')
        return None
    config = BotConfig.get_config()
    bot_user = BotConfig.get_bot_user()
    if not bot_user:
        logger.debug('Neby: trigger skipped (no bot user)')
        return None
    if not detect_mention(reply.content, config.bot_username):
        return None
    if reply.user_id == bot_user.id:
        return None
    logger.info(f'Neby: @mention detected in reply {reply.id}, generating reply')
    try:
        reply_obj = Reply.objects.select_related('post', 'user').get(pk=reply.id)
        context, reply_author = _build_reply_context(reply_obj, max_context_replies=config.max_context_replies)
        response_text = call_ai_api(config.system_prompt, context, config)
        if not response_text:
            logger.warning(f'Neby: no response from AI for reply {reply.id}')
            return None
        if reply_author and not response_text.startswith('@'):
            response_text = f'@{reply_author} {response_text}'
        with transaction.atomic():
            neby_reply = Reply.objects.create(
                id=str(uuid.uuid4()),
                post_id=reply.post_id,
                parent_reply_id=reply.id,
                user=bot_user,
                content=response_text,
                thumbs_up_count=0,
                reply_count=0,
                created_at=_now_ms(),
            )
            Post.objects.filter(pk=reply.post_id).update(reply_count=F('reply_count') + 1)
            Reply.objects.filter(pk=reply.id).update(reply_count=F('reply_count') + 1)
        from . import counters as _counters
        _counters.increment_user_reply_count(bot_user.id)
        from . import notifications as _notif
        _notif.notify_reply_to_reply(bot_user.id, reply.id, reply.post_id, neby_reply.id)
        if reply.user_id != reply_obj.post.user_id:
            _notif.notify_new_reply(bot_user.id, reply.post_id, neby_reply.id)
        logger.info(f'Neby replied to reply {reply.id}')
        return neby_reply
    except Exception as e:
        logger.error(f'Neby reply to reply failed: {e}', exc_info=True)
        return None