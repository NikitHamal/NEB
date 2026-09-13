"""Make sure Neby the user, BotConfig, and AgentPersona exist."""
from api.models import BotConfig, User
from api.utils import now_ms

from .models import AgentPersona
from .persona import (
    NEBY_BIO, NEBY_CATEGORIES, NEBY_DISPLAY_NAME, NEBY_GOALS,
    NEBY_ORIGIN, NEBY_SYSTEM_PROMPT, NEBY_TAGLINE, NEBY_TRAITS,
    NEBY_USERNAME, NEBY_VOICE,
)


def ensure_bot_user(username=NEBY_USERNAME, display_name=NEBY_DISPLAY_NAME):
    username = (username or NEBY_USERNAME).strip().lower()
    display_name = (display_name or username.capitalize()).strip()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'id': f'{username}-bot',
            'display_name': display_name,
            'is_bot': True,
            'email_verified': True,
            'bio': NEBY_BIO if username == NEBY_USERNAME else '',
            'created_at': now_ms(),
            'role': User.ROLE_EXPLORER,
        },
    )
    changed = False
    if not user.is_bot:
        user.is_bot = True
        changed = True
    if not user.email_verified:
        user.email_verified = True
        changed = True
    if username == NEBY_USERNAME and not (user.bio or '').strip():
        user.bio = NEBY_BIO
        changed = True
    if display_name and user.display_name != display_name:
        user.display_name = display_name
        changed = True
    if changed:
        user.save()
    return user, created


def ensure_bot_config(username=NEBY_USERNAME, display_name=NEBY_DISPLAY_NAME, enabled=True):
    username = (username or NEBY_USERNAME).strip().lower()
    default_chain = (
        '[{"provider": "qwencloud", "model": "qwen3.8-max"}, '
        '{"provider": "motiftech", "model": "motif-102b"}, '
        '{"provider": "tryingopen", "model": "qwen/qwen3.8-27b"}, '
        '{"provider": "tryingopen", "model": "deepseek/deepseek-v4-flash-0731"}, '
        '{"provider": "tryingopen", "model": "z-ai/glm-5.3"}, '
        '{"provider": "geminiweb", "model": "geminiweb/gemini-flash-lite"}, '
        '{"provider": "poolside", "model": "laguna-s-2.1"}, '
        '{"provider": "k2think", "model": "IFM/K2-Horizon-375B-A23B"}]'
    )
    config, created = BotConfig.objects.get_or_create(
        bot_username__iexact=username,
        defaults={
            'name': display_name or username.capitalize(),
            'bot_username': username,
            'display_name': display_name or username.capitalize(),
            'provider': 'qwencloud',
            'model': 'qwen3.8-max',
            'fallback_chain': default_chain,
            'enabled': enabled,
            'system_prompt': NEBY_SYSTEM_PROMPT if username == NEBY_USERNAME else '',
        },
    )
    changed = False
    if created:
        pass
    else:
        if not config.provider:
            config.provider = 'qwen'
            config.model = 'qwen3.8-max'
            changed = True
        if not (config.fallback_chain or '').strip():
            config.fallback_chain = default_chain
            changed = True
        if username == NEBY_USERNAME and not (config.system_prompt or '').strip():
            config.system_prompt = NEBY_SYSTEM_PROMPT
            changed = True
    if enabled and not config.enabled:
        config.enabled = True
        changed = True
    if changed:
        config.save()
    return config, created


def ensure_persona(config, user, *, autonomy_enabled=True, apply_neby_defaults=True):
    persona = AgentPersona.objects.filter(bot_config=config).first()
    created = False
    if persona is None:
        persona = AgentPersona(bot_config=config, user_id=user.id)
        created = True
        if apply_neby_defaults and config.bot_username.lower() == NEBY_USERNAME:
            persona.tagline = NEBY_TAGLINE
            persona.origin_story = NEBY_ORIGIN
            persona.goals = NEBY_GOALS
            persona.traits = NEBY_TRAITS
            persona.preferred_categories = NEBY_CATEGORIES
            persona.voice_notes = NEBY_VOICE
            persona.autonomy_enabled = autonomy_enabled
        else:
            persona.autonomy_enabled = autonomy_enabled
        persona.save()
    else:
        changed = False
        if persona.user_id != user.id:
            persona.user_id = user.id
            changed = True
        if apply_neby_defaults and config.bot_username.lower() == NEBY_USERNAME:
            if not persona.tagline:
                persona.tagline = NEBY_TAGLINE
                changed = True
            if not persona.origin_story:
                persona.origin_story = NEBY_ORIGIN
                changed = True
            if not persona.goals:
                persona.goals = NEBY_GOALS
                changed = True
            if not persona.traits:
                persona.traits = NEBY_TRAITS
                changed = True
            if not persona.preferred_categories:
                persona.preferred_categories = NEBY_CATEGORIES
                changed = True
            if not persona.voice_notes:
                persona.voice_notes = NEBY_VOICE
                changed = True
        if changed:
            persona.save()
    return persona, created


def ensure_neby(*, autonomy_enabled=True):
    user, _ = ensure_bot_user()
    config, _ = ensure_bot_config()
    persona, _ = ensure_persona(config, user, autonomy_enabled=autonomy_enabled)
    return user, config, persona
