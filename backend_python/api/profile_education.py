"""Reading, validating and saving the education situation and the portfolio.

Shared by the web onboarding, the web profile editor and the JSON API so the
rules (what a status needs, which values are allowed, how long things may be)
live once. Nothing here touches a request.
"""
import re
import time

from . import education_catalog as cat
from .models import ProfileEntry

MAX_ENTRIES_PER_KIND = 25
_DATE = re.compile(r'^\d{4}(-(0[1-9]|1[0-2]))?$')
_FIELD_ALIASES = {
    'status': ('eduStatus', 'edu_status', 'status'),
    'level': ('classLevel', 'class_level', 'class', 'level'),
    'program': ('eduProgram', 'edu_program', 'program'),
    'term': ('eduTerm', 'edu_term', 'term'),
    'completed': ('eduCompleted', 'edu_completed', 'completed'),
    'headline': ('headline',),
    'skills': ('skills',),
    'open_to': ('openTo', 'open_to'),
    'teach_levels': ('teachLevels', 'teach_levels'),
    'experience_years': ('experienceYears', 'experience_years'),
    'employment': ('employment',),
}
EMPLOYMENT_VALUES = ('full_time', 'part_time', 'tutor', 'freelance', 'visiting')
TEACH_LEVEL_VALUES = ('preprimary', 'basic_1_5', 'basic_6_8', 'secondary_9_10', 'plus_two', 'a_level',
                      'diploma', 'bachelor', 'master', 'phd', 'coaching')


def _pick(data, key):
    """(present, value) for a field under any of its camel/snake spellings."""
    for name in _FIELD_ALIASES[key]:
        if name in data:
            return True, data.get(name)
    return False, None


def _text(value, limit):
    return ' '.join(str(value or '').split())[:limit]


def apply_education(user, data):
    """Copy education + portfolio-header fields from `data` onto `user`.

    Only fields present in `data` are touched, so an older client that never
    heard of them cannot blank them. Returns an error string or None. The
    caller saves the user.
    """
    present, status = _pick(data, 'status')
    if present:
        status = (status or '').strip()
        if status and status not in cat.STATUS_VALUES:
            return 'Choose one of the listed situations.'
        user.edu_status = status

    present, level = _pick(data, 'level')
    if present:
        level = (level or '').strip()
        # Old clients send free text ('Class 11'); keep whatever is stored.
        user.class_level = level[:40]

    present, program = _pick(data, 'program')
    if present:
        user.edu_program = _text(program, 100)

    present, term = _pick(data, 'term')
    if present:
        user.edu_term = _text(term, 40)

    present, completed = _pick(data, 'completed')
    if present:
        completed = (completed or '').strip()
        if completed and completed not in cat.COMPLETED_VALUES:
            return 'Choose one of the listed levels you completed.'
        user.edu_completed = completed

    # Program and term mean nothing without a level, and a level that has no
    # programs cannot carry one.
    level_def = cat.LEVEL_BY_VALUE.get(user.class_level or '')
    if level_def is not None and not level_def['programs'] and not level_def['program_label']:
        user.edu_program = ''
    if level_def is not None and level_def['terms'] == cat.TERM_NONE:
        user.edu_term = ''
    if user.edu_status not in {s['value'] for s in cat.STATUSES if s['ask_completed']}:
        user.edu_completed = ''

    present, headline = _pick(data, 'headline')
    if present:
        user.headline = _text(headline, 120)
    present, skills = _pick(data, 'skills')
    if present:
        user.skills = cat.clean_csv(skills, limit=15, item_len=30)
    present, open_to = _pick(data, 'open_to')
    if present:
        user.open_to = cat.clean_csv(open_to, allowed=cat.OPEN_TO_VALUES, limit=10)
    present, levels = _pick(data, 'teach_levels')
    if present:
        user.teach_levels = cat.clean_csv(levels, allowed=list(TEACH_LEVEL_VALUES), limit=11)
    present, years = _pick(data, 'experience_years')
    if present:
        try:
            user.experience_years = max(0, min(int(years or 0), 60))
        except (TypeError, ValueError):
            return 'Years of experience must be a number.'
    present, employment = _pick(data, 'employment')
    if present:
        employment = (employment or '').strip()
        user.employment = employment if employment in EMPLOYMENT_VALUES else ''
    return None


def education_summary(user):
    """What the profile prints under the name. A dict of display strings."""
    level = cat.level_label(user.class_level)
    status = cat.status_label(user.edu_status)
    program = user.edu_program or ''
    term = user.edu_term or ''
    completed = cat.level_label(user.edu_completed) if user.edu_completed else ''
    if level.startswith('Class'):
        parts = [level, program]
    else:
        parts = [program or level, term]
    parts = [p for p in parts if p]
    return {
        'status': user.edu_status or '',
        'status_label': status,
        'level_label': level,
        'program': program,
        'term': term,
        'completed_label': completed,
        'line': ' · '.join(parts),
        'is_set': bool(user.class_level or user.edu_status),
    }


def open_to_items(user):
    labels = {o['value']: o for o in cat.OPEN_TO}
    return [labels[k] for k in (user.open_to or '').split(',') if k in labels]


def skills_list(user):
    return [s for s in (user.skills or '').split(',') if s]


# ---- portfolio entries -------------------------------------------------------

def entry_to_dict(e):
    return {
        'id': e.id, 'kind': e.kind, 'title': e.title, 'org': e.org,
        'start': e.start, 'end': e.end, 'isCurrent': e.is_current,
        'description': e.description, 'url': e.url,
    }


def _clean_date(value):
    value = (value or '').strip()
    return value if _DATE.match(value) else ''


def _clean_url(value):
    value = (value or '').strip()
    if not value:
        return ''
    if not re.match(r'^https?://', value, re.I):
        value = 'https://' + value
    return value[:300] if re.match(r'^https?://[^\s/]+\.[^\s]+$', value, re.I) else None


def clean_entry(data):
    """(fields, error) from a posted entry."""
    kind = (data.get('kind') or '').strip()
    if kind not in cat.ENTRY_KIND_VALUES:
        return None, 'Pick what kind of entry this is.'
    title = _text(data.get('title'), 150)
    if not title:
        return None, 'A title is required.'
    url = _clean_url(data.get('url'))
    if url is None:
        return None, 'That link does not look right.'
    current = str(data.get('isCurrent', data.get('is_current', ''))).lower() in ('1', 'true', 'on', 'yes')
    start = _clean_date(data.get('start'))
    end = '' if current else _clean_date(data.get('end'))
    if start and end and end < start:
        return None, 'The end date is before the start date.'
    return {
        'kind': kind, 'title': title, 'org': _text(data.get('org'), 150),
        'start': start, 'end': end, 'is_current': current,
        'description': str(data.get('description') or '').strip()[:600], 'url': url,
    }, None


def create_entry(user, data):
    fields, err = clean_entry(data)
    if err:
        return None, err
    taken = ProfileEntry.objects.filter(user=user, kind=fields['kind']).count()
    if taken >= MAX_ENTRIES_PER_KIND:
        return None, 'That section is full. Remove one first.'
    return ProfileEntry.objects.create(
        user=user, position=taken, created_at=int(time.time() * 1000), **fields), None


def update_entry(entry, data):
    fields, err = clean_entry({**entry_to_dict(entry), **data})
    if err:
        return None, err
    for k, v in fields.items():
        setattr(entry, k, v)
    entry.save()
    return entry, None


def portfolio_sections(user):
    """Entries grouped by kind, empty kinds left out, in catalog order."""
    rows = list(ProfileEntry.objects.filter(user=user))
    out = []
    for kind in cat.ENTRY_KINDS:
        items = [entry_to_dict(r) for r in rows if r.kind == kind['value']]
        items.sort(key=lambda i: (not i['isCurrent'], -(int((i['end'] or i['start'] or '0')[:4] or 0))))
        if items:
            out.append({**kind, 'items': items})
    return out
