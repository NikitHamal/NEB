"""The institution portfolio: what a claimed school, college or institute fills in, and how complete it is.

One schema drives the web form, the Android form, validation and the completeness score, so a new
field is added here once. Nothing is required except what the claim already collected; the owner
fills the rest whenever they like, and `completeness` (0 to 100) decides who is listed first in
Find a college.
"""
import re

from .models_institutions import Institution, InstitutionProfile
from .utils import now_ms

LEVELS = [
    ('preprimary', 'Pre-primary'), ('basic_1_5', 'Basic 1 to 5'), ('basic_6_8', 'Basic 6 to 8'),
    ('secondary_9_10', 'Secondary 9 to 10'), ('plus_two', '+2 / Class 11 to 12'),
    ('a_level', 'A Level'), ('diploma', 'Diploma / TSLC'), ('bachelor', "Bachelor's"),
    ('master', "Master's"), ('phd', 'PhD'), ('coaching', 'Entrance coaching'),
]
STREAMS = [('science', 'Science'), ('management', 'Management'), ('humanities', 'Humanities'),
           ('education', 'Education'), ('law', 'Law'), ('technical', 'Technical')]
FACILITIES = [
    ('library', 'Library'), ('science_lab', 'Science lab'), ('computer_lab', 'Computer lab'),
    ('hostel', 'Hostel'), ('transport', 'Transport'), ('canteen', 'Canteen'),
    ('sports', 'Sports ground'), ('wifi', 'Wi-Fi'), ('scholarship', 'Scholarships'),
    ('medical', 'Medical room'), ('auditorium', 'Auditorium'), ('smart_class', 'Smart classrooms'),
    ('swimming', 'Swimming pool'), ('counselling', 'Counselling'), ('placement', 'Placement cell'),
    ('ecd', 'Child care'),
]
OWNERSHIP = [('community', 'Community'), ('private', 'Private'), ('public', 'Public'),
             ('trust', 'Trust or NGO')]
MEDIUMS = [('english', 'English'), ('nepali', 'Nepali'), ('bilingual', 'Both')]
GENDER_MIX = [('co_ed', 'Co-ed'), ('boys', 'Boys only'), ('girls', 'Girls only')]
AFFILIATIONS = [('neb', 'NEB'), ('tu', 'Tribhuvan University'), ('ku', 'Kathmandu University'),
                ('pu', 'Pokhara University'), ('pu_p', 'Purbanchal University'),
                ('ctevt', 'CTEVT'), ('cambridge', 'Cambridge'), ('ib', 'IB'), ('other', 'Other')]

_LIMITS = {'about': 1200, 'motto': 120, 'principal': 120, 'principalTitle': 60, 'address': 200,
           'phone': 40, 'email': 120, 'feeNote': 200, 'admissionNote': 300, 'regNo': 80}
_COUNTS = {'teachers': 5000, 'staff': 5000, 'students': 100000, 'classrooms': 2000}
_CHOICE = {'levels': LEVELS, 'streams': STREAMS, 'facilities': FACILITIES, 'mediums': MEDIUMS,
           'affiliations': AFFILIATIONS}
_ONE = {'ownership': OWNERSHIP, 'genderMix': GENDER_MIX}
_SOCIAL = ('facebook', 'instagram', 'youtube', 'tiktok', 'x', 'linkedin')

# (key, weight). Weights add to 100; the score is the share that is filled.
WEIGHTS = [
    ('about', 12), ('est', 8), ('levels', 10), ('principal', 6), ('teachers', 6), ('students', 8),
    ('facilities', 10), ('feeMin', 10), ('phone', 8), ('address', 5), ('affiliations', 5),
    ('branches', 4), ('admissionOpen', 3), ('socials', 3), ('ownership', 2),
]


def schema():
    """Option lists for the forms (one request on app start)."""
    def opts(rows):
        return [{'value': v, 'label': l} for v, l in rows]
    return {
        'levels': opts(LEVELS), 'streams': opts(STREAMS), 'facilities': opts(FACILITIES),
        'ownership': opts(OWNERSHIP), 'mediums': opts(MEDIUMS), 'genderMix': opts(GENDER_MIX),
        'affiliations': opts(AFFILIATIONS), 'socials': list(_SOCIAL),
        'limits': {**_LIMITS, **_COUNTS},
    }


def _text(value, limit):
    return ' '.join(str(value or '').split())[:limit]


def _count(value, maximum):
    try:
        n = int(str(value).replace(',', '').strip())
    except (TypeError, ValueError):
        return None
    return n if 0 <= n <= maximum else None


def _picks(value, rows):
    allowed = {v for v, _l in rows}
    items = value if isinstance(value, list) else str(value or '').split(',')
    out = []
    for item in items:
        item = str(item).strip()
        if item in allowed and item not in out:
            out.append(item)
    return out


def _url(value):
    value = str(value or '').strip()[:200]
    if not value:
        return ''
    if not re.match(r'^https?://', value, re.I):
        value = 'https://' + value
    return value if re.match(r'^https?://[^\s/]+\.[^\s]+$', value, re.I) else None


def clean(data, current=None):
    """(profile dict, est year or None, error). Only keys present in `data` change `current`."""
    out = dict(current or {})
    est = None
    for key, limit in _LIMITS.items():
        if key in data:
            out[key] = _text(data.get(key), limit)
    for key, cap in _COUNTS.items():
        if key in data:
            n = _count(data.get(key), cap)
            if n is None and str(data.get(key) or '').strip():
                return None, None, 'Check the number for %s.' % key
            out[key] = n
    for key in ('feeMin', 'feeMax'):
        if key in data:
            n = _count(data.get(key), 100000000)
            if n is None and str(data.get(key) or '').strip():
                return None, None, 'Check the fee amount.'
            out[key] = n
    if out.get('feeMin') and out.get('feeMax') and out['feeMax'] < out['feeMin']:
        return None, None, 'The highest fee is below the lowest fee.'
    for key, rows in _CHOICE.items():
        if key in data:
            out[key] = _picks(data.get(key), rows)
    for key, rows in _ONE.items():
        if key in data:
            picked = _picks(data.get(key), rows)
            out[key] = picked[0] if picked else ''
    if 'admissionOpen' in data:
        out['admissionOpen'] = str(data.get('admissionOpen')).lower() in ('1', 'true', 'on', 'yes')
    if 'est' in data:
        year = str(data.get('est') or '').strip()
        if year and not (re.match(r'^\d{4}$', year) and 1850 <= int(year) <= 2100):
            return None, None, 'Use a four digit year.'
        est = year
    if 'branches' in data:
        rows = data.get('branches') if isinstance(data.get('branches'), list) else []
        out['branches'] = [{'name': _text(b.get('name'), 100), 'place': _text(b.get('place'), 100),
                            'phone': _text(b.get('phone'), 40)}
                           for b in rows[:12] if isinstance(b, dict) and _text(b.get('name'), 100)]
    if 'programs' in data:
        rows = data.get('programs') if isinstance(data.get('programs'), list) else []
        out['programs'] = [{'name': _text(p.get('name'), 100), 'level': _text(p.get('level'), 40),
                            'seats': _count(p.get('seats'), 5000), 'fee': _count(p.get('fee'), 100000000)}
                           for p in rows[:30] if isinstance(p, dict) and _text(p.get('name'), 100)]
    if 'socials' in data:
        raw = data.get('socials') if isinstance(data.get('socials'), dict) else {}
        socials = {}
        for key in _SOCIAL:
            if raw.get(key):
                link = _url(raw.get(key))
                if link is None:
                    return None, None, 'That %s link does not look right.' % key
                socials[key] = link
        out['socials'] = socials
    return out, est, None


def _filled(key, inst, data):
    if key == 'est':
        return bool(inst.est)
    if key == 'phone':
        return bool(data.get('phone') or inst.phone)
    value = data.get(key)
    if key == 'feeMin':
        return bool(value or data.get('programs'))
    return bool(value)


def completeness(inst, data):
    return sum(w for key, w in WEIGHTS if _filled(key, inst, data or {}))


def missing(inst, data):
    return [key for key, _w in WEIGHTS if not _filled(key, inst, data or {})]


def get(inst):
    row = InstitutionProfile.objects.filter(institution=inst).first()
    return row.data if row else {}


def save(inst, data):
    """Validate `data`, store it, return (payload, error)."""
    cur = get(inst)
    merged, est, err = clean(data, cur)
    if err:
        return None, err
    if est is not None:
        inst.est = est
        inst.save(update_fields=['est', 'search_text'])
    score = completeness(inst, merged)
    InstitutionProfile.objects.update_or_create(
        institution=inst, defaults={'data': merged, 'completeness': score, 'updated_at': now_ms()})
    return payload(inst, merged, score), None


def payload(inst, data=None, score=None):
    data = get(inst) if data is None else data
    score = completeness(inst, data) if score is None else score
    return {'details': data, 'completeness': score, 'missing': missing(inst, data)}


def owned_by(user, slug):
    """The claimed institution a signed-in user may edit, or None."""
    return Institution.objects.filter(slug=slug, claimed_by=user, verified=True).first()
