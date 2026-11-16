"""The welcome flow a new member walks through after verifying their account.

One page (`/welcome/`) drives every step in the browser; one endpoint
(`/welcome/save/`) validates the whole answer and writes it. Role, education
and the portfolio header are all decided here, explicitly, so nobody is left on
the default Student role by accident (Google and GitHub sign-ups used to be).
"""
import re
from datetime import date

import json
from api import services
from api.models import User
from api.serializers import UserSerializer
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from . import api_client as api
from .view_helpers import _clear_page_cache, _ctx, _normalize_user_data
from api import education_catalog as cat
from api.models import NEPAL_DISTRICTS
from api.profile_education import apply_education
from api.services import record_username_change
from api.view_helpers import _profile_incomplete

PRADESH = [
    ('1', 'Koshi'), ('2', 'Madhesh'), ('3', 'Bagmati'), ('4', 'Gandaki'),
    ('5', 'Lumbini'), ('6', 'Karnali'), ('7', 'Sudurpashchim'),
]
ROLES = [
    {'value': 'student', 'label': 'Student', 'icon': 'school', 'shape': 'cookie-9',
     'sub': 'Learn, ask and save resources'},
    {'value': 'teacher', 'label': 'Teacher', 'icon': 'menu_book', 'shape': 'clover',
     'sub': 'Teach, guide and share'},
    {'value': 'institution', 'label': 'Institution', 'icon': 'account_balance', 'shape': 'gem',
     'sub': 'A school, college or academy'},
    {'value': 'explorer', 'label': 'Explorer', 'icon': 'explore', 'shape': 'slanted',
     'sub': 'Here to look around'},
]
ROLE_VALUES = [r['value'] for r in ROLES]
INSTITUTION_TYPES = [
    {'value': 'school', 'label': 'School'}, {'value': 'college', 'label': 'College'},
    {'value': 'academy', 'label': 'Academy'}, {'value': 'other', 'label': 'Other'},
]
GENDERS = ['Male', 'Female', 'Other']
SUBJECT_SUGGESTIONS = [
    'Compulsory English', 'Compulsory Nepali', 'Compulsory Mathematics', 'Science', 'Social Studies',
    'Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science', 'Accountancy',
    'Economics', 'Business Studies', 'Hotel Management', 'Sociology', 'Psychology',
    'History', 'Geography', 'Education', 'Law', 'Programming', 'Web Development',
    'Data Science', 'Artificial Intelligence', 'Networking', 'Civil Engineering',
    'Electronics', 'Mechanical Engineering', 'Anatomy', 'Nursing', 'Pharmacy',
    'Agriculture', 'Statistics', 'Finance', 'Marketing', 'Management', 'English Literature',
    'Nepali Literature', 'Sanskrit', 'Health & Physical Education', 'Environment Science',
]
_AUTO_USERNAME = re.compile(r'^user_[0-9a-f]{8}$')


def _safe_next(request):
    nxt = request.GET.get('next') or request.POST.get('next') or ''
    return nxt if nxt.startswith('/') and not nxt.startswith('//') else ''


def _initial(db_user, complete):
    return {
        'role': db_user.role if complete else '',
        'username': db_user.username,
        'autoUsername': bool(_AUTO_USERNAME.match(db_user.username or '')),
        'displayName': db_user.display_name or '',
        'dob': db_user.dob or '',
        'gender': db_user.gender or '',
        'status': db_user.edu_status or '',
        'level': db_user.class_level or '',
        'program': db_user.edu_program or '',
        'term': db_user.edu_term or '',
        'completed': db_user.edu_completed or '',
        'subjects': db_user.subjects or '',
        'teachingSubjects': db_user.teaching_subjects or '',
        'institutionType': db_user.institution_type or '',
        'school': db_user.school or '',
        'pradesh': db_user.pradesh or '',
        'district': db_user.district or '',
        'headline': db_user.headline or '',
        'skills': db_user.skills or '',
        'openTo': db_user.open_to or '',
        'bio': db_user.bio or '',
        'photo': db_user.photo_url or '',
    }


def _session_db_user(request):
    token = api.get_session_token(request)
    if not token:
        return None, None
    session_user = api.get_session_user(request)
    if not session_user:
        return token, None
    return token, User.objects.filter(id=session_user.get('id')).first()


def onboarding_page(request):
    token, db_user = _session_db_user(request)
    here = f"{reverse('web:login')}?next={request.get_full_path()}"
    if not token or db_user is None or not db_user.email_verified:
        return redirect(here)
    complete = not _profile_incomplete(db_user)
    boot = {
        'catalog': cat.catalog(),
        'roles': ROLES,
        'institutionTypes': INSTITUTION_TYPES,
        'genders': GENDERS,
        'pradesh': [{'value': v, 'label': l} for v, l in PRADESH],
        'districts': NEPAL_DISTRICTS,
        'subjects': SUBJECT_SUGGESTIONS,
        'initial': _initial(db_user, complete),
        'saveUrl': reverse('web:onboarding_save'),
        'next': _safe_next(request),
        'profileUrl': reverse('web:profile', args=[db_user.username]),
    }
    return render(request, 'web/onboarding.html', _ctx(request, boot=boot, is_redo=complete,
                                                      dob=db_user.dob or '', gender=db_user.gender or ''))


def _fail(message, field=''):
    return JsonResponse({'ok': False, 'error': message, 'field': field}, status=400)


def _parse_dob(raw):
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', raw or '')
    if not m:
        return None
    try:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None
    today = date.today()
    age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    return d if 4 <= age <= 100 else None


@require_POST
def onboarding_save(request):
    token, db_user = _session_db_user(request)
    if not token or db_user is None:
        return JsonResponse({'ok': False, 'error': 'Please sign in again.'}, status=401)
    try:
        data = json.loads(request.body or b'{}')
    except ValueError:
        return _fail('That did not come through. Try again.')
    if not isinstance(data, dict):
        return _fail('That did not come through. Try again.')

    def s(key, limit):
        return ' '.join(str(data.get(key) or '').split())[:limit]

    role = s('role', 20).lower()
    if role not in ROLE_VALUES:
        return _fail('Choose what you are here as.', 'role')
    display_name = s('displayName', 150)
    if not display_name:
        return _fail('Add the name people will see.', 'displayName')
    dob, gender = '', ''
    if role != 'institution':  # an institution has no date of birth or gender
        dob = s('dob', 10)
        if _parse_dob(dob) is None:
            return _fail('Pick a real date of birth.', 'dob')
        gender = s('gender', 20)
        if gender not in GENDERS:
            return _fail('Pick one of the options.', 'gender')

    username = s('username', 50)
    if username and username != db_user.username:
        err, _code = services.validate_username_change(db_user, username)
        if err:
            return _fail(err.get('error', 'That username will not work.'), 'username')
        db_user.username = username
        record_username_change(db_user)

    teaching = cat.clean_csv(data.get('teachingSubjects'), limit=20, item_len=40)
    institution_type = s('institutionType', 30)
    school = s('school', 200)
    level = s('level', 40)
    if role == 'student' and not level:
        return _fail('Tell us where you are in your education.', 'level')
    if role == 'teacher' and not teaching:
        return _fail('Pick at least one subject you teach.', 'teachingSubjects')
    if role == 'institution':
        if not school:
            return _fail('Your institution needs a name.', 'school')
        if institution_type not in {t['value'] for t in INSTITUTION_TYPES}:
            return _fail('Pick the kind of institution.', 'institutionType')
    if level and level not in cat.LEVEL_VALUES:
        return _fail('Pick one of the listed levels.', 'level')
    pradesh = s('pradesh', 2)
    if pradesh not in {v for v, _l in PRADESH}:
        pradesh = ''
    district = s('district', 100)
    if district not in NEPAL_DISTRICTS:
        district = ''

    db_user.role = role
    db_user.display_name = display_name
    db_user.dob = dob
    db_user.gender = gender
    db_user.subjects = cat.clean_csv(data.get('subjects'), limit=30, item_len=40)
    db_user.teaching_subjects = teaching if role == 'teacher' else ''
    db_user.institution_type = institution_type if role == 'institution' else ''
    db_user.school = school
    db_user.pradesh = pradesh
    db_user.district = district
    db_user.bio = str(data.get('bio') or '').strip()[:500]
    edu_error = apply_education(db_user, {
        'level': level, 'status': s('status', 20), 'program': s('program', 100),
        'term': s('term', 40), 'completed': s('completed', 40),
        'headline': s('headline', 120), 'skills': data.get('skills'),
        'open_to': data.get('openTo'),
    })
    if edu_error:
        return _fail(edu_error, 'status')
    db_user.save()
    _clear_page_cache()
    user_data = _normalize_user_data(UserSerializer(db_user).data)
    api.set_session_auth(request, token, user_data)
    return JsonResponse({
        'ok': True,
        'next': _safe_next(request) or (data.get('next') if str(data.get('next') or '').startswith('/')
                                         and not str(data.get('next')).startswith('//') else ''),
        'profileUrl': reverse('web:profile', args=[db_user.username]),
    })


def _owner(request):
    token, db_user = _session_db_user(request)
    return db_user if token and db_user is not None else None


@require_POST
def portfolio_entry_save(request):
    """POST /ajax/portfolio/save/ {id?, kind, title, ...} for the signed-in owner."""
    from api.models import ProfileEntry
    from api.profile_education import create_entry, entry_to_dict, update_entry
    owner = _owner(request)
    if owner is None:
        return JsonResponse({'ok': False, 'error': 'Please sign in again.'}, status=401)
    try:
        data = json.loads(request.body or b'{}')
    except ValueError:
        data = {}
    if not isinstance(data, dict):
        return _fail('That did not come through.')
    if data.get('id'):
        entry = ProfileEntry.objects.filter(pk=data.get('id'), user=owner).first()
        if entry is None:
            return JsonResponse({'ok': False, 'error': 'That entry is gone.'}, status=404)
        entry, error = update_entry(entry, data)
    else:
        entry, error = create_entry(owner, data)
    if error:
        return _fail(error)
    _clear_page_cache()
    return JsonResponse({'ok': True, 'entry': entry_to_dict(entry)})


@require_POST
def portfolio_entry_delete(request):
    from api.models import ProfileEntry
    owner = _owner(request)
    if owner is None:
        return JsonResponse({'ok': False, 'error': 'Please sign in again.'}, status=401)
    try:
        entry_id = int(json.loads(request.body or b'{}').get('id'))
    except (ValueError, TypeError, AttributeError):
        return _fail('That did not come through.')
    ProfileEntry.objects.filter(pk=entry_id, user=owner).delete()
    _clear_page_cache()
    return JsonResponse({'ok': True})
