"""One autonomous tick: observe, decide, act."""
import logging

from django.core.cache import cache

from api.utils import now_ms

from .actions import apply_decision, log_action
from .birth import announce_if_needed
from .decision import decide
from .ensure import ensure_neby
from .observer import hours_since, observe

logger = logging.getLogger(__name__)

TICK_LOCK_TIMEOUT = 900


def _run_tick(persona, bot_user, config, source):
    birth = None
    if not persona.birth_announced:
        birth = announce_if_needed(persona, bot_user, source=source)
        persona.refresh_from_db()

    observations = observe(persona, bot_user)
    planned = decide(persona, bot_user, observations, bot_config=config)
    applied = apply_decision(persona, bot_user, planned, bot_config=config, source=source)

    persona.last_tick_at = now_ms()
    persona.save(update_fields=['last_tick_at', 'updated_at'])
    watched_count = (len(observations.get('posts', [])) + len(observations.get('replies', []))) if isinstance(observations, dict) else len(observations)
    log_action(
        persona, 'tick', source=source,
        reasoning=f'{len(applied)} action(s); {watched_count} item(s) watched',
        content_preview=', '.join(kind for kind, _ in applied) or 'quiet',
    )
    logger.info(
        'agent tick @%s applied=%s birth=%s',
        bot_user.username, applied, bool(birth),
    )
    return {
        'ok': True,
        'username': bot_user.username,
        'birth_post_id': (birth or {}).get('id') if birth else None,
        'applied': applied,
        'watched': watched_count,
    }


def tick_persona(persona, *, force=False, source='heartbeat'):
    from api.models import BotConfig, User

    config = persona.bot_config
    bot_user = persona.get_user()
    if bot_user is None:
        bot_user = BotConfig.get_bot_user(config)
        if bot_user:
            persona.user_id = bot_user.id
            persona.save(update_fields=['user_id', 'updated_at'])
    if bot_user is None:
        return {'ok': False, 'error': 'no bot user'}
    if not persona.autonomy_enabled and not force:
        return {'ok': False, 'error': 'autonomy disabled', 'username': bot_user.username}

    interval_ms = max(int(persona.tick_interval_minutes or 12), 1) * 60 * 1000
    if not force and persona.last_tick_at and (now_ms() - persona.last_tick_at) < interval_ms:
        return {'ok': True, 'skipped': 'too soon', 'username': bot_user.username}

    lock_key = f'agent_tick_lock:{persona.id}'
    have_lock = bool(force)
    if not force:
        try:
            have_lock = bool(cache.add(lock_key, now_ms(), timeout=TICK_LOCK_TIMEOUT))
        except Exception:
            logger.warning('agent tick lock unavailable; proceeding unlocked', exc_info=True)
            have_lock = True
        if not have_lock:
            logger.info('agent tick @%s skipped: another tick in progress', bot_user.username)
            return {'ok': True, 'skipped': 'tick already running', 'username': bot_user.username}
    try:
        return _run_tick(persona, bot_user, config, source)
    finally:
        if have_lock and not force:
            try:
                cache.delete(lock_key)
            except Exception:
                pass


def tick_neby(*, force=False, source='heartbeat'):
    _user, _config, persona = ensure_neby(autonomy_enabled=True)
    return tick_persona(persona, force=force, source=source)


def tick_all(*, force=False, source='heartbeat'):
    from .models import AgentPersona
    results = []
    qs = AgentPersona.objects.select_related('bot_config').filter(autonomy_enabled=True)
    for persona in qs:
        try:
            results.append(tick_persona(persona, force=force, source=source))
        except Exception as exc:
            logger.exception('agent tick failed for persona %s', persona.id)
            results.append({'ok': False, 'error': str(exc)[:200], 'persona_id': persona.id})
    if not results:
        results.append(tick_neby(force=force, source=source))
    return results
