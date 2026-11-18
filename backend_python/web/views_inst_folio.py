"""The profile page's portfolio strength card and the institution portfolio editor (web).

`profile_extras` feeds the profile view; `ajax_inst_portfolio_save` is the one write endpoint, a thin
wrapper over `api.institution_profile.save` (the same validation the app uses).
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from api import institution_profile as ip
from api.models_institutions import Institution
from api.profile_strength import person_strength

from .view_helpers import _clear_page_cache
from .views_institutions_profile import folio_data

# portfolio key -> editor section id and the words on the next-step chip
SECTION_OF = {
    'about': ('about', 'About'), 'est': ('basics', 'Basics'), 'principal': ('basics', 'Basics'),
    'ownership': ('basics', 'Basics'), 'affiliations': ('basics', 'Basics'), 'levels': ('levels', 'Levels offered'),
    'teachers': ('numbers', 'Numbers'), 'students': ('numbers', 'Numbers'), 'facilities': ('facilities', 'Facilities'),
    'feeMin': ('fees', 'Fees'), 'phone': ('contact', 'Contact'), 'address': ('contact', 'Contact'),
    'branches': ('branches', 'Branches'), 'admissionOpen': ('admissions', 'Admissions'), 'socials': ('socials', 'Social links'),
}
WEIGHT = dict(ip.WEIGHTS)
FAC_ICON = {
    'library': 'local_library', 'science_lab': 'science', 'computer_lab': 'computer', 'hostel': 'bed',
    'transport': 'directions_bus', 'canteen': 'restaurant', 'sports': 'sports_soccer', 'wifi': 'wifi',
    'scholarship': 'paid', 'medical': 'medical_services', 'auditorium': 'theater_comedy', 'smart_class': 'cast_for_education',
    'swimming': 'pool', 'counselling': 'psychology', 'placement': 'work', 'ecd': 'child_care',
}


def _steps(missing):
    seen, out = set(), []
    for key in sorted(missing, key=lambda k: -WEIGHT.get(k, 0)):
        sid, label = SECTION_OF.get(key, (None, None))
        if sid and sid not in seen:
            seen.add(sid)
            out.append({'id': sid, 'label': label})
    return out[:4]


def _sentence(percent):
    if percent >= 90:
        return 'Complete. Students and parents get the full picture.'
    return 'The fuller your page, the higher you appear in Find a college.'


def profile_extras(profile_user, is_self, has_entries=None):
    """{'strength': ..., 'inst': ...}: what the profile adds on top of the portfolio card."""
    out = {'strength': None, 'inst': None}
    if profile_user.is_bot:
        return out
    if profile_user.role != 'institution':
        if is_self:
            out['strength'] = person_strength(profile_user, has_entries)
        return out
    inst = Institution.objects.filter(claimed_by=profile_user).first()
    if inst is None and profile_user.institution_verified:
        from api.institutions import heal_owner
        try:
            inst = heal_owner(profile_user)
        except Exception:
            inst = None
    if inst is None:
        out['inst'] = {'claimed': False, 'own': is_self}
        return out
    data = ip.get(inst)
    pay = ip.payload(inst, data)
    can_edit = bool(is_self and inst.verified)
    folio = folio_data(inst, data)
    inst_ctx = {
        'claimed': True, 'own': can_edit,
        'facility_rows': [{'label': l, 'icon': FAC_ICON.get(k, 'check_circle')} for k, l in ip.FACILITIES if k in (data.get('facilities') or [])], 'slug': inst.slug, 'verified': inst.verified, 'folio': folio,
        'boot': {'slug': inst.slug, 'details': data, 'est': inst.est or '', 'schema': ip.schema()},
    }
    if can_edit:
        out['strength'] = {'percent': pay['completeness'], 'steps': _steps(pay['missing']),
                           'sentence': _sentence(pay['completeness'])}
    out['inst'] = inst_ctx
    return out


@require_POST
def ajax_inst_portfolio_save(request):
    """POST /ajax/institution/portfolio/save/ {slug, ...fields} for the verified owner."""
    from .views_onboarding import _owner
    owner = _owner(request)
    if owner is None:
        return JsonResponse({'ok': False, 'error': 'Please sign in again.'}, status=401)
    try:
        data = json.loads(request.body or b'{}')
    except ValueError:
        data = {}
    if not isinstance(data, dict):
        return JsonResponse({'ok': False, 'error': 'That did not come through.'}, status=400)
    inst = ip.owned_by(owner, str(data.pop('slug', '')))
    if inst is None:
        return JsonResponse({'ok': False, 'error': 'Only the verified owner can edit this portfolio.'}, status=403)
    payload, error = ip.save(inst, data)
    if error:
        return JsonResponse({'ok': False, 'error': error}, status=400)
    _clear_page_cache()
    return JsonResponse({'ok': True, 'completeness': payload['completeness']})


@require_POST
def ajax_teacher_profile_save(request):
    """POST /ajax/teacher/profile/save/ {school?, teaching_subjects?, teach_levels?, employment?, experience_years?, headline?}.
    One section at a time, any field optional, for the signed-in teacher."""
    from api.profile_education import apply_education
    from .views_onboarding import _owner
    owner = _owner(request)
    if owner is None:
        return JsonResponse({'ok': False, 'error': 'Please sign in again.'}, status=401)
    if getattr(owner, 'role', '') != 'teacher':
        return JsonResponse({'ok': False, 'error': 'This editor is for teacher profiles.'}, status=403)
    try:
        data = json.loads(request.body or b'{}')
    except ValueError:
        data = {}
    if not isinstance(data, dict):
        return JsonResponse({'ok': False, 'error': 'That did not come through.'}, status=400)
    error = apply_education(owner, data)
    if error:
        return JsonResponse({'ok': False, 'error': error}, status=400)
    if 'school' in data:
        owner.school = ' '.join(str(data.get('school') or '').split())[:150]
    if 'teaching_subjects' in data:
        raw = data.get('teaching_subjects')
        parts = raw if isinstance(raw, (list, tuple)) else str(raw or '').split(',')
        seen, clean = set(), []
        for p in parts:
            p = ' '.join(str(p).split())[:40]
            if p and p.lower() not in seen:
                seen.add(p.lower())
                clean.append(p)
        owner.teaching_subjects = ','.join(clean[:20])
    owner.save()
    _clear_page_cache()
    return JsonResponse({'ok': True})
