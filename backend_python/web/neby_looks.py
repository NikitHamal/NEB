"""Pixel Neby's looks and states, as the server knows them.

The art lives in the apps (Android draws it in ``ui/pixel``; the web plays strips exported from
the same code into ``static/web/img/neby/<look>/<state>.png``). This module only names what
exists, says which look a site theme dresses Neby in, and resolves what is live: an admin's pick
from ``api.models.NebyConfig``, or "auto", which follows the festival theme.
"""
from __future__ import annotations

# key, label, group. Keep in step with NebyLook in PixelNebyLooks.kt.
LOOKS = [
    ('classic', 'Classic', 'Everyday'),
    ('dashain', 'Dashain', 'Festivals'), ('tihar', 'Tihar', 'Festivals'), ('holi', 'Holi', 'Festivals'),
    ('teej', 'Teej', 'Festivals'), ('losar', 'Losar', 'Festivals'), ('new-year', 'Nepali New Year', 'Festivals'),
    ('christmas', 'Christmas', 'Festivals'),
    ('monsoon', 'Monsoon', 'Seasons'), ('winter', 'Winter', 'Seasons'),
    ('topi', 'Dhaka topi', 'Everyday'), ('graduate', 'Graduate', 'Everyday'), ('astronaut', 'Astronaut', 'Fun'),
    ('wizard', 'Wizard', 'Fun'), ('headphones', 'Headphones', 'Fun'), ('scientist', 'Scientist', 'Everyday'),
    ('ninja', 'Ninja', 'Fun'), ('night', 'Night cap', 'Fun'), ('crown', 'Champion', 'Fun'),
]
LOOK_KEYS = {k for k, _, _ in LOOKS}
HAT_LOOKS = {'dashain', 'losar', 'new-year', 'christmas', 'monsoon', 'winter', 'topi', 'graduate', 'astronaut',
             'wizard', 'headphones', 'night', 'crown'}

# key -> (frames, ms per frame, group). Keep in step with NebyState in PixelNebyStates.kt.
STATES = {
    'idle': (16, 115, 'Everyday'), 'still': (1, 1000, 'Everyday'), 'blink': (6, 110, 'Everyday'),
    'look-around': (12, 130, 'Everyday'), 'think': (8, 160, 'Everyday'), 'talk': (8, 95, 'Everyday'),
    'listen': (8, 140, 'Everyday'), 'read': (14, 140, 'Everyday'), 'sleep': (12, 140, 'Everyday'),
    'wave': (10, 110, 'Feelings'), 'hop': (12, 72, 'Feelings'), 'wink': (10, 110, 'Feelings'),
    'love': (12, 110, 'Feelings'), 'kiss': (12, 110, 'Feelings'), 'laugh': (10, 80, 'Feelings'),
    'cool': (10, 120, 'Feelings'), 'surprised': (10, 80, 'Feelings'), 'sad': (12, 130, 'Feelings'),
    'dizzy': (12, 100, 'Feelings'), 'oops': (10, 100, 'Feelings'), 'success': (12, 80, 'Feelings'),
    'celebrate': (14, 85, 'Feelings'),
    'tika': (18, 120, 'Festivals'), 'kite': (16, 130, 'Festivals'), 'swing': (16, 90, 'Festivals'),
    'diyo': (12, 110, 'Festivals'), 'deusi': (12, 95, 'Festivals'), 'splash': (16, 90, 'Festivals'),
    'fireworks': (16, 100, 'Festivals'), 'namaste': (12, 120, 'Festivals'),
}

# which look each site theme dresses Neby in
THEME_LOOK = {'dashain': 'dashain', 'tihar': 'tihar', 'holi': 'holi', 'new-year': 'new-year',
              'monsoon': 'monsoon', 'winter': 'winter', 'exams': 'graduate'}
# and the animation that says hello in that season
THEME_STATE = {'dashain': 'tika', 'tihar': 'diyo', 'holi': 'splash', 'new-year': 'fireworks'}

AUTO = 'auto'


def for_theme(theme_key: str) -> str:
    return THEME_LOOK.get(theme_key, 'classic')


def resolve(theme_key: str) -> dict:
    """What Neby wears and does now. Never raises: a missing table means the classic Neby."""
    look, ambient, reactions = AUTO, True, True
    try:
        from api.models import NebyConfig
        row = NebyConfig.objects.order_by('-updated_at').first()
        if row:
            look, ambient, reactions = row.look, row.ambient, row.reactions
    except Exception:
        pass
    chosen = for_theme(theme_key) if look == AUTO or look not in LOOK_KEYS else look
    return {'look': chosen, 'mode': look if look in LOOK_KEYS else AUTO, 'ambient': ambient, 'reactions': reactions,
            'greet': THEME_STATE.get(theme_key) if look == AUTO else None, 'hat': chosen in HAT_LOOKS}
