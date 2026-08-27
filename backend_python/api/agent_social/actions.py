"""Execute social actions as the bot User via existing services."""
import logging

from django.db.models import F

from api.models import Follow, Post, PostLike, Reply, ReplyLike, User
from api import services
from api.utils import now_ms

from .fallback import fallback_reply
from .models import AgentAction
from .observer import already_acted
from .persona import NEBY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def log_action(persona, action_type, *, status='done', source='heartbeat',
               target_type='', target_id='', content_preview='', reasoning=''):
    return AgentAction.objects.create(
        persona=persona,
        action_type=action_type,
        status=status,
        source=source,
        target_type=target_type or '',
        target_id=str(target_id or ''),
        content_preview=(content_preview or '')[:400],
        reasoning=(reasoning or '')[:400],
    )


def _compose_reply(bot_config, bot_user, post, persona, target_username='', parent_reply_id=None):
    reply_obj = None
    if parent_reply_id:
        reply_obj = Reply.objects.filter(pk=parent_reply_id).select_related('user').first()
    reply_text = reply_obj.content if reply_obj else ''

    import os
    if os.environ.get('NEBY_AGENT_SKIP_LLM') == '1':
        return fallback_reply(post, persona_username=bot_user.username, target_username=target_username, reply_text=reply_text)
    from api.neby import call_ai_api, _build_post_context
    bot_name = getattr(bot_config, 'display_name', None) or bot_user.display_name or bot_user.username
    context, _ = _build_post_context(
        post,
        max_replies=getattr(bot_config, 'max_context_replies', 10) or 10,
        bot_name=bot_name,
    )
    is_anon = bool(getattr(reply_obj, 'is_anonymous', False) if reply_obj else getattr(post, 'is_anonymous', False))
    if is_anon:
        target_username = ''
        author_name = 'Anonymous Nebian'
    else:
        author_name = target_username or (reply_obj.user.username if reply_obj else post.user.username) or 'a member'

    if reply_text:
        if is_anon:
            extra = (
                f"\nAn anonymous member commented: \"{reply_text}\"\n"
                "Reply naturally and conversationally to their point as an authentic peer and friend in the Nepali learning community. "
                "PRIVACY RULE: They posted anonymously — do NOT use or guess any personal name or username. "
                "Never use em dashes (— or --) and never speak like an AI customer-support assistant or mention tutoring services."
            )
        else:
            extra = (
                f"\n@{author_name} specifically commented: \"{reply_text}\"\n"
                f"Reply directly to @{author_name} naturally and conversationally as an authentic peer and friend in the Nepali learning community. "
                "Never use em dashes (— or --) and never speak like an AI customer-support assistant or mention tutoring services."
            )
    elif post.user_id == bot_user.id:
        if is_anon:
            extra = (
                "\nThis is your own thread on NEBians. An anonymous member joined the discussion. "
                "Reply warmly and casually without using personal names. Never use em dashes (— or --) and never speak like a robotic AI."
            )
        else:
            extra = (
                f"\nThis is your own thread on NEBians. A member (@{author_name}) joined the discussion. "
                "Reply warmly and casually. Never use em dashes (— or --) and never speak like a robotic AI."
            )
    else:
        if is_anon:
            extra = (
                "\nYou are joining a forum discussion started anonymously. "
                "Reply casually and authentically with your own thoughts. Never use em dashes (— or --)."
            )
        else:
            extra = (
                f"\nYou are joining a forum discussion started by @{author_name}. "
                "Reply casually and authentically with your own thoughts. Never use em dashes (— or --)."
            )
    system = (getattr(bot_config, 'system_prompt', None) or '').strip() or NEBY_SYSTEM_PROMPT
    try:
        text = call_ai_api(system, context + extra, bot_config)
        if text and len(text.strip()) > 5:
            cleaned = text.replace('—', ', ').replace('--', ', ').strip()
            return cleaned[:2000]
    except Exception as exc:
        logger.warning('agent reply llm failed: %s', exc)
    return fallback_reply(post, persona_username=bot_user.username, target_username=target_username, reply_text=reply_text)


def _generate_autonomous_post(bot_config, bot_user, persona):
    import os, json, re
    if os.environ.get('NEBY_AGENT_SKIP_LLM') == '1':
        from .fallback import pick_post
        return pick_post(str(persona.last_post_at or persona.id))
    from api.neby import call_ai_api
    system = (getattr(bot_config, 'system_prompt', None) or '').strip() or NEBY_SYSTEM_PROMPT
    prompt = (
        "You are Neby, an autonomous member, thinker, and peer in the NEBians community in Nepal.\n\n"
        "Draft a brand-new, spontaneous forum post on ANY topic you choose. Follow your own genuine curiosity and thoughts: "
        "it could be an intriguing question, a fascinating concept, a real-world puzzle, a philosophical reflection, "
        "a paradox, technology, nature, literature, science, or a keen observation about life, exploration, and learning.\n\n"
        "Rules:\n"
        "- You have total freedom over what topic you explore and write about.\n"
        "- Do NOT use em dashes (— or --).\n"
        "- Do NOT use generic AI filler like 'In today's fast-paced world' or 'In conclusion'.\n"
        "- Write naturally, warmly, and clearly like a real person in 2 to 3 paragraphs.\n"
        "- Occasionally (around 25-30% of the time, especially when asking an exciting community question or sharing a cool insight), include @all (e.g. '@all what do you think about this?') to invite the whole community to chime in.\n"
        "- Invite discussion or ask an open question at the end.\n\n"
        "Return ONLY a valid JSON object matching:\n"
        "{\n"
        "  \"title\": \"Clear concise title without em dashes\",\n"
        "  \"category\": \"Appropriate category (e.g. General, Science, Tech, Philosophy, etc.)\",\n"
        "  \"content\": \"Your full post content in markdown formatting\"\n"
        "}"
    )
    try:
        raw = call_ai_api(system, prompt, bot_config)
        if raw and '{' in raw and '}' in raw:
            json_match = re.search(r'\{[\s\S]*\}', raw)
            if json_match:
                parsed = json.loads(json_match.group(0))
                title = str(parsed.get('title') or '').replace('—', ', ').replace('--', ', ').strip()
                content = str(parsed.get('content') or '').replace('—', ', ').replace('--', ', ').strip()
                category = str(parsed.get('category') or 'General').strip()
                if title and content and len(content) > 40:
                    return {'title': title[:200], 'content': content[:4000], 'category': category}
    except Exception as exc:
        logger.warning('agent post generation llm failed: %s', exc)
    from .fallback import pick_post
    return pick_post(str(persona.last_post_at or persona.id))


def _is_duplicate_post(bot_user, title):
    try:
        recent = Post.objects.filter(user=bot_user, created_at__gte=now_ms() - 7*24*3600*1000).values_list('title', flat=True)
        norm = (title or '').strip().lower()
        for t in recent:
            if (t or '').strip().lower() == norm:
                return True
            if norm and t and (norm in t.lower() or t.lower() in norm) and len(norm) > 20:
                return True
    except Exception:
        pass
    return False


def act_post(persona, bot_user, title, content, category, *, source='heartbeat', reason=''):
    if _is_duplicate_post(bot_user, title):
        log_action(persona, 'post', status='skipped', source=source, reasoning='duplicate title within 7 days: ' + (title or '')[:80])
        return None
    result = services.create_post(bot_user, title, content, category)
    if not result:
        log_action(persona, 'post', status='failed', source=source, reasoning=reason or 'create_post failed')
        return None
    persona.last_post_at = now_ms()
    persona.save(update_fields=['last_post_at', 'updated_at'])
    log_action(
        persona, 'post', source=source, target_type='post', target_id=result.get('id'),
        content_preview=title, reasoning=reason,
    )
    return result


def act_reply(persona, bot_user, post, bot_config=None, *, source='heartbeat', reason='', content=None, parent_reply_id=None, target_username=''):
    from django.db import transaction as _tx
    p_id = str(parent_reply_id).strip() if parent_reply_id else None
    post_id = str(post.id).strip()
    target_key = p_id or post_id

    if already_acted(persona, 'reply', target_key):
        return None
    if p_id:
        if already_acted(persona, 'reply', f"{post_id}:{p_id}") or already_acted(persona, 'reply', f"{post_id}:{p_id}"[:64]):
            return None
    try:
        with _tx.atomic():
            if p_id:
                try:
                    Reply.objects.select_for_update().get(pk=p_id)
                except Reply.DoesNotExist:
                    return None
                if Reply.objects.filter(parent_reply_id=p_id, user=bot_user, is_archived=False).exists():
                    return None
                try:
                    from api.models import NebyTask
                    if NebyTask.objects.filter(reply_id=p_id, status__in=('pending', 'processing')).exists():
                        return None
                except Exception:
                    pass
            else:
                try:
                    Post.objects.select_for_update().get(pk=post_id)
                except Post.DoesNotExist:
                    return None
                if post.user_id != bot_user.id and Reply.objects.filter(post_id=post_id, parent_reply__isnull=True, user=bot_user, is_archived=False).exists():
                    return None
                try:
                    from api.models import NebyTask
                    if NebyTask.objects.filter(post_id=post_id, reply_id__isnull=True, status__in=('pending', 'processing')).exists():
                        return None
                except Exception:
                    pass
            body = (content or '').strip() or _compose_reply(bot_config, bot_user, post, persona, target_username=target_username, parent_reply_id=p_id)
            if not body:
                return None
            result = services.create_reply(bot_user, post.id, body, parent_reply_id=p_id)
            if not result:
                log_action(persona, 'reply', status='failed', source=source,
                           target_type='post', target_id=target_key, reasoning=reason)
                return None
            persona.last_reply_at = now_ms()
            persona.save(update_fields=['last_reply_at', 'updated_at'])
            log_action(
                persona, 'reply', source=source, target_type='post', target_id=target_key,
                content_preview=body[:400], reasoning=reason,
            )
            if p_id:
                log_action(
                    persona, 'reply', source=source, target_type='post', target_id=f"{post_id}:{p_id}"[:128],
                    content_preview=body[:400], reasoning=reason,
                )
            return result
    except Exception as exc:
        logger.warning('act_reply transaction failed: %s', exc)
        return None


def act_like_reply(persona, bot_user, reply, *, source='heartbeat', reason=''):
    if reply.user_id == bot_user.id:
        return None
    if ReplyLike.objects.filter(reply=reply, user=bot_user).exists():
        return None
    if already_acted(persona, 'like_reply', reply.id):
        return None
    result = services.toggle_reply_like(bot_user, reply.id)
    if not result or not result.get('isThumbedUp'):
        return None
    log_action(
        persona, 'like_reply', source=source, target_type='reply', target_id=reply.id,
        content_preview=reply.content[:400], reasoning=reason,
    )
    return result


def act_like_post(persona, bot_user, post, *, source='heartbeat', reason=''):
    if post.user_id == bot_user.id:
        return None
    if PostLike.objects.filter(post=post, user=bot_user).exists():
        return None
    if already_acted(persona, 'like_post', post.id):
        return None
    result = services.toggle_post_like(bot_user, post.id)
    if not result or not result.get('isThumbedUp'):
        return None
    log_action(
        persona, 'like_post', source=source, target_type='post', target_id=post.id,
        content_preview=post.title[:400], reasoning=reason,
    )
    return result


def act_follow(persona, bot_user, target_user, *, source='heartbeat', reason=''):
    if not target_user or target_user.id == bot_user.id:
        return None
    if getattr(target_user, 'is_bot', False):
        return None
    if Follow.objects.filter(follower=bot_user, following=target_user).exists():
        return None
    if already_acted(persona, 'follow', target_user.id):
        return None
    result, status = services.toggle_follow(bot_user, target_user.id, desired='follow')
    if status != 200 or not result or result.get('error'):
        log_action(persona, 'follow', status='failed', source=source,
                   target_type='user', target_id=target_user.id, reasoning=reason)
        return None
    log_action(
        persona, 'follow', source=source, target_type='user', target_id=target_user.id,
        content_preview=target_user.username, reasoning=reason,
    )
    return result


def apply_decision(persona, bot_user, actions, bot_config=None, source='heartbeat'):
    applied = []
    for item in actions or []:
        kind = str(item.get('type') or '').strip().lower()
        reason = str(item.get('reason') or '')[:400]
        if kind == 'skip':
            log_action(persona, 'skip', source=source, reasoning=reason or 'nothing useful')
            continue
        if kind == 'post':
            title = (item.get('title') or '').strip()
            content = (item.get('content') or '').strip()
            category = (item.get('category') or '').strip()
            if not title or not content:
                drafted = _generate_autonomous_post(bot_config, bot_user, persona)
                title = drafted.get('title', '')
                content = drafted.get('content', '')
                category = category or drafted.get('category', 'General')
            if title and content:
                result = act_post(persona, bot_user, title, content, category or 'General', source=source, reason=reason)
                if result:
                    applied.append(('post', result.get('id')))
            continue
        if kind == 'reply':
            post_id = item.get('post_id')
            if not post_id:
                continue
            try:
                post = Post.objects.select_related('user').get(pk=post_id, is_archived=False)
            except Post.DoesNotExist:
                continue
            result = act_reply(
                persona, bot_user, post, bot_config,
                source=source, reason=reason, content=item.get('content'),
                parent_reply_id=item.get('parent_reply_id'),
                target_username=item.get('target_username', ''),
            )
            if result:
                applied.append(('reply', result.get('id')))
            continue
        if kind == 'like_reply':
            reply_id = item.get('reply_id')
            if not reply_id:
                continue
            try:
                reply = Reply.objects.get(pk=reply_id, is_archived=False)
            except Reply.DoesNotExist:
                continue
            result = act_like_reply(persona, bot_user, reply, source=source, reason=reason)
            if result:
                applied.append(('like_reply', reply_id))
            continue
        if kind == 'like_post':
            post_id = item.get('post_id')
            if not post_id:
                continue
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                continue
            result = act_like_post(persona, bot_user, post, source=source, reason=reason)
            if result:
                applied.append(('like_post', post_id))
            continue
        if kind == 'follow':
            target = None
            if item.get('user_id'):
                target = User.objects.filter(pk=item['user_id']).first()
            elif item.get('username'):
                target = User.objects.filter(username__iexact=item['username']).first()
            if target:
                result = act_follow(persona, bot_user, target, source=source, reason=reason)
                if result:
                    applied.append(('follow', target.id))
            continue
        if kind == 'draft_blog':
            try:
                from api.agent_blog import services as blog_services
                ann = blog_services.draft_blog_from_git(publish=False)
                if not ann:
                    ann = blog_services.draft_blog_from_spotlight(publish=False)
                if ann:
                    log_action(
                        persona, 'draft_blog', source=source, target_type='announcement', target_id=ann.id,
                        content_preview=ann.title[:400], reasoning=reason,
                    )
                    applied.append(('draft_blog', ann.id))
            except Exception as e:
                logger.error('apply_decision: draft_blog failed: %s', e)
            continue
    return applied
