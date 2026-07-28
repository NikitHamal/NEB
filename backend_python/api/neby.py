"""
Neby AI Bot — detects @mentions and generates contextual replies.

Supports multiple bots, each with its own BotConfig row. When a post or reply
mentions @username, the system finds the matching enabled BotConfig and
enqueues a NebyTask linked to that config.

Task queue architecture:
- Request cycle: detect_mention() → find matching BotConfig → enqueue_neby_task()
- Cron job: `python manage.py process_neby_tasks` picks up pending tasks,
  calls the AI, creates the reply, and marks the task done/failed.

This avoids blocking the request and avoids daemon threads that Passenger kills.
"""
import logging
import re

from django.db import transaction
from django.db.models import F

from .models import BotConfig, User, Post, Reply, NebyTask
from .utils import now_ms, uuid_str

logger = logging.getLogger(__name__)


def is_neby_enabled():
    from django.core.cache import cache
    cache_key = 'neby_enabled'
    val = cache.get(cache_key)
    if val is not None:
        return val
    try:
        enabled_bots = BotConfig.get_enabled_bots()
        enabled = False
        for config in enabled_bots:
            if BotConfig.get_bot_user(config):
                enabled = True
                break
    except Exception:
        enabled = False
    cache.set(cache_key, enabled, 60)
    return enabled


def detect_mention(text, bot_username='neby'):
    pattern = re.compile(r'@' + re.escape(bot_username) + r'\b', re.IGNORECASE)
    return bool(pattern.search(text))


def _find_matching_bots(text):
    """Find all enabled BotConfigs whose @username appears in the text."""
    configs = []
    for config in BotConfig.get_enabled_bots():
        if detect_mention(text, config.bot_username):
            configs.append(config)
    return configs


def enqueue_neby_task(trigger, post_id, reply_id=None, bot_config=None):
    """Create a pending NebyTask and return it. Called from request cycle."""
    if not is_neby_enabled():
        logger.debug('Neby: enqueue skipped (no enabled bots with users)')
        return None
    if bot_config is None:
        return None
    bot_user = BotConfig.get_bot_user(bot_config)
    if not bot_user:
        logger.debug(f'Neby: enqueue skipped (no user for @{bot_config.bot_username})')
        return None
    task = NebyTask.objects.create(
        id=uuid_str(),
        bot_config=bot_config,
        status='pending',
        trigger=trigger,
        post_id=post_id,
        reply_id=reply_id,
        created_at=now_ms(),
    )
    logger.info(f'Neby: enqueued {trigger} task {task.id} for bot @{bot_config.bot_username}, post {post_id}')
    return task


def enqueue_if_post_mention(post):
    """Check if a post mentions any enabled bot and enqueue tasks for each match."""
    text = f'{post.title} {post.content}'
    configs = _find_matching_bots(text)
    tasks = []
    for config in configs:
        bot_user = BotConfig.get_bot_user(config)
        if bot_user and post.user_id != bot_user.id:
            task = enqueue_neby_task('post_mention', post.id, bot_config=config)
            if task:
                tasks.append(task)
    return tasks


def enqueue_if_reply_mention(reply):
    """Check if a reply mentions any enabled bot and enqueue tasks for each match."""
    configs = _find_matching_bots(reply.content)
    tasks = []
    for config in configs:
        bot_user = BotConfig.get_bot_user(config)
        if bot_user and reply.user_id != bot_user.id:
            task = enqueue_neby_task('reply_mention', reply.post_id, reply_id=reply.id, bot_config=config)
            if task:
                tasks.append(task)
    return tasks


def _build_post_context(post, max_replies=10, bot_name='Neby'):
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
    lines.append(f"Please write a helpful reply to this post as {bot_name}. Keep it concise and relevant to the student's question.")
    return '\n'.join(lines), None


def _build_reply_context(reply, max_context_replies=10, bot_name='Neby'):
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
    reply_username = reply.user.username
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
    lines.append(f"Please write a helpful reply as {bot_name}. Keep it concise and relevant.")
    return '\n'.join(lines), reply_username


def call_ai_api(system_prompt, user_message, config=None):
    """Dispatch to the configured AI provider.

    Supports:
      - 'qwen'      → Qwen web chat (chat.qwen.ai), via qwen_proxy.call_qwen
      - 'egov'      → eGov Chat AI (Philippines), via egov_proxy.simple_chat
      - 'inception' → Inception Labs (Mercury 2 diffusion LLM)
      - 'custom'    → any OpenAI-compatible /chat/completions endpoint
      - 'agnes' / 'openai' / 'anthropic' / 'gemini' / 'deepseek'
                    → official APIs via the shared api.llm client
    Returns response text or None.
    """
    if config is None:
        config = BotConfig.objects.filter(enabled=True).first()
        if not config:
            return None
    provider = (config.provider or 'qwen').strip().lower()
    max_tokens = config.response_max_length or 500

    # Official API providers share one client; BotConfig carries the key,
    # base URL override and chosen model — the same registry Zeus sessions use.
    if provider in ('agnes', 'openai', 'anthropic', 'gemini', 'deepseek'):
        from api.llm import registry, client
        preset = registry.preset(provider)
        try:
            result = client.chat(
                format=preset.format if preset else registry.FORMAT_OPENAI,
                base_url=(config.api_url or '').strip() or (preset.base_url if preset else ''),
                api_key=config.api_key or '',
                model=(config.model or '').strip() or (preset.default_model if preset else ''),
                messages=(
                    ([{'role': 'system', 'content': system_prompt}] if system_prompt and system_prompt.strip() else [])
                    + [{'role': 'user', 'content': user_message}]
                ),
                max_tokens=max_tokens,
                timeout=120,
                temperature=0.7,
                provider=provider,
            )
            return result.text
        except client.LLMError as e:
            logger.error('neby: %s call failed: %s', provider, e)
            return None

    if provider == 'egov':
        from . import egov_proxy
        return egov_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'AI1',
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'deepai':
        from . import deepai_proxy
        return deepai_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'standard',
            system_prompt=system_prompt or '',
        )
    if provider == 'inception':
        from . import inception_proxy
        return inception_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'mercury-2',
            system_prompt=system_prompt or '',
            reasoning_effort=getattr(config, 'reasoning_effort', 'high'),
        )
    if provider == 'custom':
        from .custom_provider import call_custom
        return call_custom(
            api_url=config.api_url or '',
            api_key=config.api_key or '',
            model=config.model or '',
            system_prompt=system_prompt or '',
            user_message=user_message,
            max_tokens=max_tokens,
        )
    # default: qwen
    from .qwen_proxy import call_qwen
    model = config.model or 'qwen3.7-plus'
    return call_qwen(system_prompt, user_message, model=model, max_tokens=max_tokens)


def process_neby_task(task):
    """Execute a single NebyTask. Called by the management command."""
    config = task.bot_config
    if not config:
        try:
            config = BotConfig.objects.filter(enabled=True).first()
        except BotConfig.DoesNotExist:
            config = None
    if not config:
        task.status = 'failed'
        task.error_message = 'No bot config found'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    bot_user = BotConfig.get_bot_user(config)
    if not bot_user:
        task.status = 'failed'
        task.error_message = f'No bot user for @{config.bot_username}'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    task.status = 'processing'
    task.started_at = now_ms()
    task.attempts = F('attempts') + 1
    task.save(update_fields=['status', 'started_at', 'attempts'])
    task.refresh_from_db()

    try:
        if task.trigger == 'post_mention':
            _process_post_mention(task, config, bot_user)
        elif task.trigger == 'reply_mention':
            _process_reply_mention(task, config, bot_user)
        else:
            task.status = 'failed'
            task.error_message = f'Unknown trigger: {task.trigger}'
            task.finished_at = now_ms()
            task.save(update_fields=['status', 'error_message', 'finished_at'])
    except Exception as e:
        logger.error(f'Neby task {task.id} failed: {e}', exc_info=True)
        task.refresh_from_db()
        task.status = 'failed'
        task.error_message = str(e)[:2000]
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])


def _process_post_mention(task, config, bot_user):
    try:
        post = Post.objects.select_related('user').get(pk=task.post_id)
    except Post.DoesNotExist:
        task.status = 'failed'
        task.error_message = f'Post {task.post_id} not found'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    if not detect_mention(post.content, config.bot_username) and not detect_mention(post.title, config.bot_username):
        task.status = 'failed'
        task.error_message = f'No @{config.bot_username} mention found in post'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    bot_name = config.display_name or config.name or 'Neby'
    context, _ = _build_post_context(post, max_replies=config.max_context_replies, bot_name=bot_name)
    response_text = call_ai_api(config.system_prompt, context, config)
    if not response_text:
        task.status = 'failed'
        task.error_message = 'No response from AI'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    author_username = post.user.username
    if author_username and not response_text.startswith('@'):
        response_text = f'@{author_username} {response_text}'

    with transaction.atomic():
        reply = Reply.objects.create(
            id=uuid_str(),
            post=post,
            parent_reply_id=None,
            user=bot_user,
            content=response_text,
            thumbs_up_count=0,
            reply_count=0,
            created_at=now_ms(),
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)

    from . import counters as _counters
    _counters.increment_user_reply_count(bot_user.id)
    from . import notifications as _notif
    _notif.notify_new_reply(bot_user.id, post.id, reply.id)
    from . import realtime as _rt
    from .serializers import ReplySerializer
    _rt.broadcast_reply_created(post.id, ReplySerializer(reply).data)

    task.status = 'done'
    task.finished_at = now_ms()
    task.save(update_fields=['status', 'finished_at'])
    logger.info(f'Neby task {task.id}: bot @{config.bot_username} replied to post {post.id}')


def _process_reply_mention(task, config, bot_user):
    if not task.reply_id:
        task.status = 'failed'
        task.error_message = 'No reply_id for reply_mention task'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    try:
        reply = Reply.objects.select_related('post', 'user').get(pk=task.reply_id)
    except Reply.DoesNotExist:
        task.status = 'failed'
        task.error_message = f'Reply {task.reply_id} not found'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    if not detect_mention(reply.content, config.bot_username):
        task.status = 'failed'
        task.error_message = f'No @{config.bot_username} mention found in reply'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    if reply.user_id == bot_user.id:
        task.status = 'failed'
        task.error_message = 'Bot mentioned itself'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    bot_name = config.display_name or config.name or 'Neby'
    context, reply_username = _build_reply_context(reply, max_context_replies=config.max_context_replies, bot_name=bot_name)
    response_text = call_ai_api(config.system_prompt, context, config)
    if not response_text:
        task.status = 'failed'
        task.error_message = 'No response from AI'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    if reply_username and not response_text.startswith('@'):
        response_text = f'@{reply_username} {response_text}'

    with transaction.atomic():
        neby_reply = Reply.objects.create(
            id=uuid_str(),
            post_id=reply.post_id,
            parent_reply_id=reply.id,
            user=bot_user,
            content=response_text,
            thumbs_up_count=0,
            reply_count=0,
            created_at=now_ms(),
        )
        Post.objects.filter(pk=reply.post_id).update(reply_count=F('reply_count') + 1)
        Reply.objects.filter(pk=reply.id).update(reply_count=F('reply_count') + 1)

    from . import counters as _counters
    _counters.increment_user_reply_count(bot_user.id)
    from . import notifications as _notif
    _notif.notify_reply_to_reply(bot_user.id, reply.id, reply.post_id, neby_reply.id)
    if reply.user_id != reply.post.user_id:
        _notif.notify_new_reply(bot_user.id, reply.post_id, neby_reply.id)
    from . import realtime as _rt
    from .serializers import ReplySerializer
    _rt.broadcast_reply_created(reply.post_id, ReplySerializer(neby_reply).data)

    task.status = 'done'
    task.finished_at = now_ms()
    task.save(update_fields=['status', 'finished_at'])
    logger.info(f'Neby task {task.id}: bot @{config.bot_username} replied to reply {reply.id}')
