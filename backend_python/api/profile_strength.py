"""Portfolio strength for a person: the same weights as the Android profile and the Profile concept.

One list per account type drives the score and the next steps. Nothing is required; the number only
reflects how much the person chose to share. Institutions use `institution_profile.completeness`.
"""
from .models import ProfileEntry


def _has(value):
    return bool(str(value or '').strip())


def _gaps(u, has_entries):
    """(label, weight, filled, tappable)."""
    role = u.role
    if role == 'teacher':
        return [
            ('Current school', 15, _has(u.school), True), ('Type of work', 5, _has(u.employment), True),
            ('Subjects', 15, _has(u.teaching_subjects), True), ('Levels', 12, _has(u.teach_levels), True),
            ('Experience', 10, (u.experience_years or 0) > 0, True), ('Headline', 8, _has(u.headline), True),
            ('About', 8, _has(u.bio), True), ('Skills', 5, _has(u.skills), True),
            ('Past schools', 22, has_entries, False),
        ]
    if role == 'explorer':
        return [('Headline', 30, _has(u.headline), True), ('About', 30, _has(u.bio), True),
                ('Skills', 20, _has(u.skills), True), ('Open to', 20, _has(u.open_to), True)]
    return [
        ('Class or program', 12, _has(u.class_level) or _has(u.edu_program), True),
        ('School or college', 12, _has(u.school), True), ('Headline', 12, _has(u.headline), True),
        ('About', 10, _has(u.bio), True), ('Skills', 12, _has(u.skills), True),
        ('Open to', 10, _has(u.open_to), True), ('Achievements and projects', 22, has_entries, False),
    ]


def person_strength(u, has_entries=None):
    """{'percent', 'steps': [labels], 'sentence'} for the owner's card. Pass `has_entries` when the caller
    already loaded the portfolio, so the page spends no extra query."""
    if has_entries is None:
        has_entries = ProfileEntry.objects.filter(user=u).exists()
    gaps = _gaps(u, has_entries)
    total = sum(g[1] for g in gaps) or 1
    percent = sum(g[1] for g in gaps if g[2]) * 100 // total
    steps = [g[0] for g in sorted(gaps, key=lambda g: -g[1]) if not g[2] and g[3]][:4]
    sentence = ('Complete. People get the full picture of you.' if percent >= 90
                else 'Add what you like, whenever you like. Nothing is forced.')
    return {'percent': percent, 'steps': steps, 'sentence': sentence}
