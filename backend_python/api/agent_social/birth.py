"""First-run introduction post — Neby's birth announcement."""
import logging

from .actions import act_post
from .fallback import birth_post

logger = logging.getLogger(__name__)


def announce_if_needed(persona, bot_user, source='seed'):
    if persona.birth_announced:
        return None
    from .models import AgentAction
    if AgentAction.objects.filter(persona=persona, action_type='introduce', status='done').exists():
        persona.birth_announced = True
        persona.save(update_fields=['birth_announced', 'updated_at'])
        return None
    payload = birth_post()
    result = act_post(
        persona, bot_user,
        payload['title'], payload['content'], payload['category'],
        source=source,
        reason='Birth announcement — first autonomous post.',
    )
    if not result:
        logger.warning('neby birth post failed for %s', bot_user.username)
        return None
    from .models import AgentAction
    AgentAction.objects.filter(
        persona=persona, action_type='post', target_id=result.get('id'),
    ).update(action_type='introduce')
    persona.birth_announced = True
    persona.save(update_fields=['birth_announced', 'updated_at'])
    logger.info('neby birth announced: post %s', result.get('id'))
    return result
