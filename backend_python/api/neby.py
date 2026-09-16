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
from django.db.models import F, Q

from .models import BotConfig, User, Post, Reply, NebyTask
from .utils import now_ms, uuid_str

logger = logging.getLogger(__name__)

_SPAM_RE = re.compile(r'(http[s]?://|www\.|buy now|click here|free money)', re.I)
_SHORT_RE = re.compile(r'^\s*(hi|hello|hey|ok|thanks|thank you|nice|\.+|!+|👍|🙏)+\s*$', re.I)


def _is_mention_low_quality(text):
    t = (text or '').strip()
    if len(t) < 3:
        return True
    if _SPAM_RE.search(t):
        return True
    return False


def _persona_block_for_mention(persona):
    lines = []
    if getattr(persona, 'tagline', ''):
        lines.append(f"Tagline: {persona.tagline}")
    if getattr(persona, 'traits', None):
        try:
            if persona.traits:
                lines.append(f"Traits: {', '.join(persona.traits)}")
        except Exception:
            pass
    if getattr(persona, 'goals', None):
        try:
            if persona.goals:
                lines.append(f"Goals: {'; '.join(persona.goals)}")
        except Exception:
            pass
    if getattr(persona, 'voice_notes', ''):
        lines.append(f"Voice: {persona.voice_notes[:300]}")
    return '\n'.join(lines) if lines else ''


def _should_reply_to_mention(persona, text, trigger):
    """Neby herself decides — via her LLM persona — whether to reply. No dice."""
    t = (text or '').strip()
    if _is_mention_low_quality(t):
        logger.info(f"neby mention decide: obvious spam/short, skip without LLM")
        return False
    if not persona:
        return True
    try:
        # Build persona-aware prompt
        system = (
            f"You are Neby, a peer on NEBians. { _persona_block_for_mention(persona) }\n\n"
            "Someone mentioned you. Decide as Neby — human-like, not a bot. "
            "You may stay quiet if it feels forced, spammy, or you have nothing genuine to add. "
            "Be warm but selective. Reply only when it feels natural.\n"
            "Return ONLY JSON: {\"should_reply\": true/false, \"reason\": \"1 sentence\"}"
        )
        user = f"Trigger: {trigger}\nMention text: {t[:600]}\n\nShould you reply?"
        # Use her own provider
        from api.models import BotConfig
        bot_config = None
        try:
            # persona -> bot_config
            bot_config = getattr(persona, 'bot_config', None)
            if bot_config is None:
                bot_config = BotConfig.objects.filter(pk=getattr(persona, 'bot_config_id', None)).first()
            if bot_config is None:
                bot_config = BotConfig.objects.filter(bot_username__iexact='neby').first()
        except Exception:
            bot_config = None
        text_resp = call_ai_api(system, user, bot_config)
        if not text_resp:
            logger.warning("neby mention decide: LLM empty, default to reply")
            return True
        import json as _json, re as _re
        m = _re.search(r'\{[\s\S]*\}', text_resp)
        if not m:
            logger.warning(f"neby mention decide: no JSON {text_resp[:300]}")
            return True
        data = _json.loads(m.group(0))
        should = bool(data.get('should_reply', True))
        reason = (data.get('reason') or '')[:120]
        logger.info(f"neby mention decide: trigger={trigger} should_reply={should} reason={reason}")
        return should
    except Exception as e:
        logger.warning(f"neby mention decide LLM failed: {e}, default reply")
        return True


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


def _has_existing_bot_reply(post_id, reply_id, bot_user):
    """Check if bot already replied to this post/reply."""
    if reply_id:
        return Reply.objects.filter(parent_reply_id=reply_id, user=bot_user, is_archived=False).exists()
    return Reply.objects.filter(post_id=post_id, parent_reply_id__isnull=True, user=bot_user, is_archived=False).exists()


def _has_pending_task(post_id, reply_id, bot_config):
    qs = NebyTask.objects.filter(status__in=('pending', 'processing'))
    if bot_config and bot_config.pk:
        qs = qs.filter(bot_config=bot_config)
    if reply_id:
        qs = qs.filter(reply_id=reply_id)
    else:
        qs = qs.filter(Q(reply_id__isnull=True) | Q(reply_id=''), post_id=post_id)
    return qs.exists()


_HANDLED_DONE_PREFIX = 'Bot already replied'


def _done_task_means_replied(qs):
    """A done task counts as handled only when a bot reply exists for the target."""
    return qs.filter(status='done').filter(
        Q(error_message='') | Q(error_message__isnull=True)
        | Q(error_message__startswith=_HANDLED_DONE_PREFIX)
    ).exists()


def done_handled_reply_ids():
    """Reply ids whose @mention was already answered (in-flight or done-with-reply)."""
    pending = set(
        NebyTask.objects.filter(status__in=('pending', 'processing'))
        .exclude(reply_id__isnull=True).exclude(reply_id='')
        .values_list('reply_id', flat=True)
    )
    done = set(
        NebyTask.objects.filter(status='done')
        .exclude(reply_id__isnull=True).exclude(reply_id='')
        .filter(
            Q(error_message='') | Q(error_message__isnull=True)
            | Q(error_message__startswith=_HANDLED_DONE_PREFIX)
        )
        .values_list('reply_id', flat=True)
    )
    return pending | done


def _post_level_tasks():
    return NebyTask.objects.filter(Q(reply_id__isnull=True) | Q(reply_id=''))


def done_handled_post_ids():
    """Post ids whose @mention was already answered (in-flight or done-with-reply)."""
    pending = set(
        _post_level_tasks().filter(status__in=('pending', 'processing'))
        .values_list('post_id', flat=True)
    )
    done = set(
        _post_level_tasks().filter(status='done')
        .filter(
            Q(error_message='') | Q(error_message__isnull=True)
            | Q(error_message__startswith=_HANDLED_DONE_PREFIX)
        )
        .values_list('post_id', flat=True)
    )
    return pending | done


def is_mention_handled(post_id, reply_id=None):
    """Shared cross-path ledger: True when a mention task already covers this target."""
    if reply_id:
        rid = str(reply_id).strip()
        if NebyTask.objects.filter(reply_id=rid, status__in=('pending', 'processing')).exists():
            return True
        return _done_task_means_replied(NebyTask.objects.filter(reply_id=rid))
    pid = str(post_id).strip()
    if _post_level_tasks().filter(post_id=pid, status__in=('pending', 'processing')).exists():
        return True
    return _done_task_means_replied(_post_level_tasks().filter(post_id=pid))


def _log_mention_action(config, target_ids, content_preview, reason):
    """Record a mention-path reply in the AgentAction ledger so autonomy skips it."""
    try:
        if config is None or not getattr(config, 'pk', None):
            logger.warning('neby: mention AgentAction skipped (no bot config)')
            return
        from api.agent_social.models import AgentAction, AgentPersona
        persona = AgentPersona.objects.filter(bot_config=config).first()
        if persona is None:
            logger.warning(f'neby: mention AgentAction skipped (no persona for @{config.bot_username})')
            return
        for tid in target_ids or []:
            tid = str(tid or '').strip()
            if not tid:
                continue
            AgentAction.objects.create(
                persona=persona,
                action_type='reply',
                status='done',
                source='mention',
                target_type='post',
                target_id=tid[:128],
                content_preview=(content_preview or '')[:400],
                reasoning=(reason or '')[:400],
            )
    except Exception:
        logger.warning('neby: failed to log mention AgentAction', exc_info=True)


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
    if _has_pending_task(post_id, reply_id, bot_config):
        logger.debug(f'Neby: enqueue skipped duplicate pending task for bot @{bot_config.bot_username}, post {post_id} reply {reply_id}')
        return None
    if _has_existing_bot_reply(post_id, reply_id, bot_user):
        logger.debug(f'Neby: enqueue skipped bot already replied for bot @{bot_config.bot_username}, post {post_id} reply {reply_id}')
        return None
    try:
        from api.agent_social.models import AgentAction
        target_key = str(reply_id).strip() if reply_id else str(post_id).strip()
        if reply_id:
            post_key = str(post_id).strip()
            if AgentAction.objects.filter(action_type='reply', target_id=target_key, status='done').exists():
                logger.debug(f'Neby: enqueue skipped AgentAction already replied for {target_key}')
                return None
            composite = f"{post_key}:{target_key}"
            if AgentAction.objects.filter(action_type='reply', target_id=composite, status='done').exists():
                return None
            if AgentAction.objects.filter(action_type='reply', target_id=composite[:64], status='done').exists():
                return None
        else:
            if AgentAction.objects.filter(action_type='reply', target_id=target_key, status='done').exists():
                return None
    except Exception:
        logger.warning('Neby: AgentAction dedup check failed; proceeding to enqueue', exc_info=True)
    with transaction.atomic():
        if _has_pending_task(post_id, reply_id, bot_config):
            return None
        if _has_existing_bot_reply(post_id, reply_id, bot_user):
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
        if getattr(post, 'is_anonymous', False):
            author_name = 'Anonymous Nebian'
        else:
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
                if getattr(r, 'is_anonymous', False):
                    r_name = 'Anonymous Nebian'
                else:
                    r_name = r.user.display_name or r.user.username
            except Exception:
                r_name = 'Unknown'
            lines.append(f"  {r_name}: {r.content}")
        lines.append("")
    lines.append(
        f"Please write a helpful reply to this post as {bot_name}. Keep it concise and relevant to the student's question. "
        "PRIVACY REQUIREMENT: If the post or any comment is from 'Anonymous Nebian', NEVER reveal or guess any real identity/username."
    )
    return '\n'.join(lines), None


def _build_reply_context(reply, max_context_replies=10, bot_name='Neby'):
    lines = []
    post = reply.post
    try:
        if getattr(post, 'is_anonymous', False):
            post_author = 'Anonymous Nebian'
        else:
            post_author = post.user.display_name or post.user.username
    except Exception:
        post_author = 'Unknown'
    try:
        if getattr(reply, 'is_anonymous', False):
            reply_author = 'Anonymous Nebian'
        else:
            reply_author = reply.user.display_name or reply.user.username
    except Exception:
        reply_author = 'Unknown'
    reply_username = None if getattr(reply, 'is_anonymous', False) else reply.user.username
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
                if getattr(r, 'is_anonymous', False):
                    r_name = 'Anonymous Nebian'
                else:
                    r_name = r.user.display_name or r.user.username
            except Exception:
                r_name = 'Unknown'
            lines.append(f"  {r_name}: {r.content}")
        lines.append("")
    lines.append(f"{reply_author} just wrote (mentioning you): {reply.content}")
    lines.append("")
    lines.append(
        f"Please write a helpful reply as {bot_name}. Keep it concise and relevant. "
        "PRIVACY REQUIREMENT: If the commenter is 'Anonymous Nebian', treat them as an anonymous member. NEVER mention or reveal their real name or personal username."
    )
    return '\n'.join(lines), reply_username


def _call_single_provider(system_prompt, user_message, config):
    """Dispatch a single provider call (no fallback). Returns text or None."""
    provider = (config.provider or 'qwen').strip().lower()
    max_tokens = config.response_max_length or 500

    # Official API providers share one client; BotConfig carries the key,
    # base URL override and chosen model — the same registry Zeus sessions use.
    from api.llm import registry, client
    if registry.is_official_slug(provider):
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

    if provider == 'qwencloud':
        from . import qwencloud_proxy
        return qwencloud_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'qwen3.8-max',
            system_prompt=system_prompt or '',
            thinking=False,
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
    if provider == 'k2think':
        from . import k2think_proxy
        return k2think_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'IFM/K2-Horizon-375B-A23B',
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'poolside':
        from . import poolside_proxy
        return poolside_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'laguna-s-2.1',
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'motiftech':
        from . import motiftech_proxy
        return motiftech_proxy.simple_chat(
            user_message=user_message,
            model=config.model or 'motif-102b',
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'tryingopen':
        from . import tryingopen_proxy
        # effort maps to thinking level; stored in BotConfig.model or api_url? Use config's extra?
        # We piggyback on api_key field for effort if needed, but default to balanced.
        effort = (getattr(config, 'effort', '') or 'balanced') if hasattr(config, 'effort') else 'balanced'
        return tryingopen_proxy.simple_chat(
            user_message=user_message,
            model=config.model or tryingopen_proxy.DEFAULT_MODEL,
            system_prompt=system_prompt or '',
            effort=effort,
            max_tokens=max_tokens,
        )
    if provider == 'longcat':
        from . import longcat_proxy
        return longcat_proxy.simple_chat(
            user_message=user_message,
            model=config.model or longcat_proxy.MODELS[0]["id"],
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'geminiweb' or not provider:
        from . import geminiweb_proxy
        return geminiweb_proxy.simple_chat(
            user_message=user_message,
            model=config.model if (config.model and 'gemini' in config.model) else geminiweb_proxy.MODELS[0]["id"],
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'yqcloud':
        from . import yqcloud_proxy
        return yqcloud_proxy.simple_chat(
            user_message=user_message,
            model=config.model or yqcloud_proxy.DEFAULT_MODEL,
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'chatjimmy':
        from . import chatjimmy_proxy
        return chatjimmy_proxy.simple_chat(
            user_message=user_message,
            model=config.model or chatjimmy_proxy.DEFAULT_MODEL,
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'unikey':
        from . import unikey_proxy
        return unikey_proxy.simple_chat(
            user_message=user_message,
            model=config.model or unikey_proxy.DEFAULT_MODEL,
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'ptero':
        from . import ptero_proxy
        return ptero_proxy.simple_chat(
            user_message=user_message,
            model=config.model or ptero_proxy.DEFAULT_MODEL,
            system_prompt=system_prompt or '',
            max_tokens=max_tokens,
        )
    if provider == 'qwen':
        from .qwen_proxy import call_qwen
        model = config.model or 'qwen3.8-max'
        return call_qwen(system_prompt, user_message, model=model, max_tokens=max_tokens)
    # default fallback: geminiweb
    from . import geminiweb_proxy
    return geminiweb_proxy.simple_chat(
        user_message=user_message,
        model=geminiweb_proxy.MODELS[0]["id"],
        system_prompt=system_prompt or '',
        max_tokens=max_tokens,
    )


def call_ai_api(system_prompt, user_message, config=None):
    """Dispatch to the configured AI provider, walking the bot's fallback
    chain when the primary provider fails.
    """
    if config is None:
        config = BotConfig.objects.filter(enabled=True).first()
        if not config:
            config = BotConfig(provider='geminiweb', model='geminiweb/gemini-flash-lite')
    try:
        text = _call_single_provider(system_prompt, user_message, config)
        if text:
            return text
    except Exception as exc:
        logger.warning('neby: primary provider %s failed: %s', config.provider, exc)
    
    fallbacks = config.get_fallback_chain()
    if not fallbacks:
        fallbacks = [
            {'provider': 'qwencloud', 'model': 'qwen3.8-max'},
            {'provider': 'motiftech', 'model': 'motif-102b'},
            {'provider': 'geminiweb', 'model': 'geminiweb/gemini-flash-lite'},
            {'provider': 'tryingopen', 'model': 'qwen/qwen3.8-27b'},
            {'provider': 'tryingopen', 'model': 'deepseek/deepseek-v4-flash-0731'},
            {'provider': 'tryingopen', 'model': 'z-ai/glm-5.3'},
            {'provider': 'poolside', 'model': 'laguna-s-2.1'},
            {'provider': 'k2think', 'model': 'IFM/K2-Horizon-375B-A23B'},
        ]
    for entry in fallbacks:
        provider = (entry.get('provider') or '').strip().lower()
        model_name = (entry.get('model') or '').strip()
        if not provider:
            continue
        if provider == config.provider and model_name == config.model:
            continue
        fallback_cfg = BotConfig(
            provider=provider,
            model=(entry.get('model') or '').strip(),
            api_url=(entry.get('api_url') or '').strip(),
            api_key=(entry.get('api_key') or '').strip(),
            response_max_length=config.response_max_length,
        )
        try:
            text = _call_single_provider(system_prompt, user_message, fallback_cfg)
            if text:
                logger.info('neby: fell back to provider %s (%s)', provider, fallback_cfg.model)
                return text
            logger.warning('neby: fallback %s returned empty', provider)
        except Exception as exc:
            logger.warning('neby: fallback %s failed: %s', provider, exc)
    return None


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

    if _has_existing_bot_reply(task.post_id, None, bot_user):
        task.status = 'done'
        task.error_message = f'{_HANDLED_DONE_PREFIX} to this post'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    if not detect_mention(post.content, config.bot_username) and not detect_mention(post.title, config.bot_username):
        task.status = 'failed'
        task.error_message = f'No @{config.bot_username} mention found in post'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    # Personality: not every mention gets a reply — be humane
    try:
        from api.agent_social.models import AgentPersona
        persona = AgentPersona.objects.filter(bot_config=config).first()
        if persona and not _should_reply_to_mention(persona, f"{post.title} {post.content}", 'post_mention'):
            task.status = 'done'
            task.error_message = 'Ignored by personality (chose not to reply)'
            task.finished_at = now_ms()
            task.save(update_fields=['status', 'error_message', 'finished_at'])
            logger.info(f"Neby task {task.id}: ignored post mention by personality")
            return
    except Exception as e:
        logger.warning(f"neby personality check failed: {e}")

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
        Post.objects.select_for_update().get(pk=post.pk)
        if _has_existing_bot_reply(task.post_id, None, bot_user):
            task.status = 'done'
            task.error_message = f'{_HANDLED_DONE_PREFIX} to this post (race)'
            task.finished_at = now_ms()
            task.save(update_fields=['status', 'error_message', 'finished_at'])
            return
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
    task.error_message = ''
    task.finished_at = now_ms()
    task.save(update_fields=['status', 'error_message', 'finished_at'])
    _log_mention_action(config, [post.id], response_text, f'Mention reply to post {post.id}')
    logger.info(f'Neby task {task.id}: bot @{config.bot_username} replied to post {post.id}')


def _process_reply_mention(task, config, bot_user):
    if not task.reply_id:
        task.status = 'failed'
        task.error_message = 'No reply_id for reply_mention task'
        task.finished_at = now_ms()
        task.save(update_fields=['status', 'error_message', 'finished_at'])
        return

    if _has_existing_bot_reply(task.post_id, task.reply_id, bot_user):
        task.status = 'done'
        task.error_message = f'{_HANDLED_DONE_PREFIX} to this reply'
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

    if _has_existing_bot_reply(task.post_id, task.reply_id, bot_user):
        task.status = 'done'
        task.error_message = f'{_HANDLED_DONE_PREFIX} to this reply'
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

    try:
        from api.agent_social.models import AgentPersona
        persona = AgentPersona.objects.filter(bot_config=config).first()
        if persona and not _should_reply_to_mention(persona, reply.content, 'reply_mention'):
            task.status = 'done'
            task.error_message = 'Ignored by personality (chose not to reply)'
            task.finished_at = now_ms()
            task.save(update_fields=['status', 'error_message', 'finished_at'])
            logger.info(f"Neby task {task.id}: ignored reply mention by personality")
            return
    except Exception as e:
        logger.warning(f"neby personality check failed: {e}")

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
        Reply.objects.select_for_update().get(pk=reply.id)
        if _has_existing_bot_reply(task.post_id, task.reply_id, bot_user):
            task.status = 'done'
            task.error_message = f'{_HANDLED_DONE_PREFIX} to this reply (race)'
            task.finished_at = now_ms()
            task.save(update_fields=['status', 'error_message', 'finished_at'])
            return
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
    task.error_message = ''
    task.finished_at = now_ms()
    task.save(update_fields=['status', 'error_message', 'finished_at'])
    _log_mention_action(
        config, [reply.id, f"{reply.post_id}:{reply.id}"],
        response_text, f'Mention reply to reply {reply.id}',
    )
    logger.info(f'Neby task {task.id}: bot @{config.bot_username} replied to reply {reply.id}')
