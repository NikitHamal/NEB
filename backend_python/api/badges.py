"""Shared badge-info helper for API serializers.

Mirrors web.view_helpers._user_badge_info so API clients (Android app)
receive the exact same badge metadata as the web frontend.
"""

_MOD_LEVELS = {
    1: {'icon': 'local_police', 'color': '#1B9AF0', 'label': 'Community Mod'},
    2: {'icon': 'shield', 'color': '#00897B', 'label': 'Senior Mod'},
    3: {'icon': 'shield_with_heart', 'color': '#7B1FA2', 'label': 'Community Lead'},
}

_VER_LEVELS = {
    1: {'icon': 'verified', 'color': '#1B9AF0', 'label': 'Verified'},
    2: {'icon': 'verified', 'color': '#2E7D32', 'label': 'Expert Verified'},
    3: {'icon': 'verified', 'color': '#F59E0B', 'label': 'Premium Verified'},
    4: {'icon': 'verified', 'color': '#1a1a1a', 'label': 'Elite Verified'},
}


def user_badge_info(user):
    """Build the badge dict for a user. Priority:
    bot -> admin -> moderator -> teacher -> institution -> explorer -> verified -> None
    """
    if user is None:
        return None
    try:
        if user.is_bot:
            return {'type': 'bot', 'icon': 'smart_toy', 'color': '#7C4DFF', 'label': 'AI'}
        if user.is_admin:
            return {'type': 'admin', 'icon': 'crown', 'color': '#F59E0B', 'label': 'Admin'}
        if user.moderator_level and user.moderator_level > 0:
            info = _MOD_LEVELS.get(user.moderator_level, _MOD_LEVELS[1])
            return {'type': 'moderator', **info}
        role = getattr(user, 'role', 'student')
        if role == 'teacher':
            return {
                'type': 'teacher', 'icon': 'school', 'color': '#10B981',
                'label': 'Verified Teacher' if getattr(user, 'teacher_verified', False) else 'Teacher',
            }
        if role == 'institution':
            return {
                'type': 'institution', 'icon': 'account_balance', 'color': '#6366F1',
                'label': 'Verified Institution' if getattr(user, 'institution_verified', False) else 'Institution',
            }
        if role == 'explorer':
            return {'type': 'explorer', 'icon': 'travel_explore', 'color': '#F59E0B', 'label': 'Explorer'}
        if user.verification_level and user.verification_level > 0:
            info = _VER_LEVELS.get(user.verification_level, _VER_LEVELS[1])
            return {'type': 'verified', **info}
    except Exception:
        return None
    return None
