"""The one list of where a person in Nepal can be in their education.

Web onboarding, the web profile editor and `GET /api/education/catalog/` all
read this module, so a level or a course is added in exactly one place.

A person is described by four independent answers, because "class" alone
cannot say "I did +2, spent a year in BSc CSIT and left":

  status     what is happening right now (`STATUSES`)
  level      the level they are in, or the last one they were in (`LEVELS`)
  program    the course or stream at that level (`LEVELS[..]['programs']`)
  term       the year or semester inside it, always optional (`TERMS`)

plus `completed`, the highest level they actually finished, asked only when
status is not "studying".

`class_level` on the user row keeps storing the *level value*. The values for
school classes and the old broad levels are unchanged so resource filtering
and the Android app keep working; everything new is additive.
"""

STATUS_STUDYING = 'studying'
STATUS_BREAK = 'gap_year'
STATUS_DROPPED = 'dropped_out'
STATUS_COMPLETED = 'completed'
STATUS_PREPARING = 'preparing'
STATUS_WORKING = 'working'
STATUS_SELF = 'self_learning'
STATUS_ABROAD = 'abroad'

STATUSES = [
    {'value': STATUS_STUDYING, 'label': 'Studying', 'icon': 'school',
     'hint': 'Enrolled right now', 'ask_completed': False},
    {'value': STATUS_COMPLETED, 'label': 'Graduated', 'icon': 'workspace_premium',
     'hint': 'Finished this level', 'ask_completed': False},
    {'value': STATUS_PREPARING, 'label': 'Preparing', 'icon': 'edit_note',
     'hint': 'Entrance or exam prep', 'ask_completed': True},
    {'value': STATUS_BREAK, 'label': 'Taking a break', 'icon': 'pause_circle',
     'hint': 'Gap year', 'ask_completed': True},
    {'value': STATUS_DROPPED, 'label': 'Dropped out', 'icon': 'logout',
     'hint': 'Left before finishing', 'ask_completed': True},
    {'value': STATUS_WORKING, 'label': 'Working', 'icon': 'work',
     'hint': 'Learning beside a job', 'ask_completed': True},
    {'value': STATUS_SELF, 'label': 'Self-learning', 'icon': 'auto_stories',
     'hint': 'No class, still growing', 'ask_completed': True},
    {'value': STATUS_ABROAD, 'label': 'Studying abroad', 'icon': 'flight_takeoff',
     'hint': 'Outside Nepal', 'ask_completed': False},
]
STATUS_VALUES = [s['value'] for s in STATUSES]
# Everything except "studying" means the class-based resource filter would
# guess wrong, so these people see the full library.
GLOBAL_STATUSES = {s for s in STATUS_VALUES if s != STATUS_STUDYING}

# ---- programs ---------------------------------------------------------------

PLUS_TWO = [
    'Science (Physical)', 'Science (Biology)', 'Management', 'Humanities',
    'Education', 'Law', 'Hotel Management', 'Computer Science',
    'Engineering (Technical)', 'Agriculture', 'Hospitality & Tourism',
    'Fine Arts', 'Music',
]

TVET = [
    'Civil Engineering', 'Computer Engineering', 'Electrical Engineering',
    'Electronics Engineering', 'Mechanical Engineering', 'Automobile Engineering',
    'Architecture', 'Geomatics / Survey', 'Information Technology',
    'Agriculture (Plant Science)', 'Animal Science / Veterinary', 'Forestry',
    'Food Technology', 'Pharmacy', 'General Medicine (HA)', 'Staff Nurse / PCL Nursing',
    'ANM', 'Lab Technology', 'Dental Hygiene', 'Hotel Management', 'Hospitality',
    'Travel & Tourism', 'Fashion Design', 'Beautician', 'Plumbing & Electrical Trade',
]

BACHELORS = [
    # technology
    'BSc CSIT', 'BCA', 'BIT', 'BSc IT', 'BE Computer', 'BE Software', 'BE Civil',
    'BE Electronics & Communication', 'BE Electrical', 'BE Mechanical',
    'BE Architecture (B.Arch)', 'BE Aerospace', 'BE Chemical', 'BE Geomatics',
    'BE Industrial', 'BE Agriculture', 'BE Biomedical', 'BE Automobile',
    # management
    'BBS', 'BBA', 'BBM', 'BIM', 'BHM', 'BTTM', 'BBA-BI', 'BFSc (Finance)',
    'Bachelor of Business Studies (Hons)',
    # humanities & social
    'BA', 'BA (Hons)', 'BSW', 'BMS', 'BJMC (Journalism)', 'BFA', 'BPA',
    'BA Rural Development', 'Bachelor of Development Studies', 'BA English',
    'BA Sociology', 'BA Psychology', 'BA Nepali', 'BA Sanskrit', 'BA Economics',
    'BA Political Science',
    # education
    'BEd', 'BPEd', 'BEd (Science)', 'BEd (Mathematics)', 'BEd (English)',
    # science
    'BSc Physics', 'BSc Chemistry', 'BSc Mathematics', 'BSc Microbiology',
    'BSc Biotechnology', 'BSc Zoology', 'BSc Botany', 'BSc Statistics',
    'BSc Environmental Science', 'BSc Geology', 'BSc Food Technology',
    # health
    'MBBS', 'BDS', 'BSc Nursing', 'BNS', 'BPH', 'BPharm', 'BMLT', 'BPT',
    'BOptom', 'BAMS', 'BSc MIT', 'BSc Community Medicine', 'BSc Anesthesia',
    # agri
    'BSc Agriculture', 'BSc Forestry', 'BVSc & AH', 'BSc Horticulture',
    'BSc Dairy', 'BSc Fisheries',
    # law
    'LLB', 'BA LLB', 'BBA LLB',
]

MASTERS = [
    'MBS', 'MBA', 'MBM', 'MPA', 'MA English', 'MA Nepali', 'MA Economics',
    'MA Sociology', 'MA Political Science', 'MA Rural Development', 'MA Psychology',
    'MSW', 'MEd', 'MSc Physics', 'MSc Chemistry', 'MSc Mathematics', 'MSc Statistics',
    'MSc Computer Science', 'MSc CSIT', 'MCA', 'MIT', 'ME Computer', 'ME Civil',
    'ME Structural', 'ME Electrical', 'ME Electronics', 'MSc Environmental Science',
    'MSc Agriculture', 'MSc Forestry', 'MPH', 'MD / MS (Residency)', 'MDS',
    'MSc Nursing', 'MPharm', 'MPhil', 'LLM', 'MFA',
]

DOCTORATE = ['PhD', 'DM / MCh', 'Postdoctoral']

ENTRANCE_TARGETS = [
    'IOE entrance (Engineering)', 'MBBS / BDS entrance', 'Nursing / Paramedical entrance',
    'CMAT (Management)', 'CSIT entrance', 'BCA / BIT entrance', 'CTEVT entrance',
    'BEd entrance', 'Law entrance', 'Agriculture / Forestry entrance',
    'Masters entrance', 'Scholarship exam',
]

COMPETITIVE_TARGETS = [
    'Lok Sewa (Public Service)', 'Teacher Service Commission (TSC)',
    'Nepal Police / APF / Army', 'Banking & Finance exams', 'IELTS / PTE / TOEFL',
    'SAT / ACT', 'GRE / GMAT', 'CA / ACCA', 'License exam (NEC / NMC / NNC)',
    'Foreign study preparation',
]

SELF_LEARNER_FOCUS = [
    'Programming', 'Design', 'Languages', 'Business & Finance', 'Science',
    'Mathematics', 'Writing', 'Data & AI', 'Music & Arts', 'Skill training',
]

PROFESSIONAL_FIELDS = [
    'Teaching', 'Software / IT', 'Engineering', 'Healthcare', 'Business / Finance',
    'Government service', 'Banking', 'Media / Creative', 'Agriculture',
    'Entrepreneur', 'Freelancer', 'Other field',
]

ABROAD_LEVELS = [
    "Secondary / A-Levels / IB", "Bachelor's abroad", "Master's abroad",
    'PhD abroad', 'Language / foundation course',
]

_SCHOOL = [('Class %d' % n) for n in range(1, 8)]

# ---- levels ------------------------------------------------------------------
# `value` is what is stored in users.class. The strings that already existed
# ('Class 8', '11', '12', '+2 Passout', 'Diploma', 'Bachelors', 'Masters',
# 'PhD', 'Other') are untouched on purpose.

GROUP_SCHOOL = 'School'
GROUP_PLUS2 = '+2 and equivalent'
GROUP_TVET = 'Technical and diploma'
GROUP_UNI = 'University'
GROUP_PREP = 'Preparing'
GROUP_OTHER = 'Beyond the classroom'

TERM_NONE = 'none'
TERM_YEAR = 'year'
TERM_ANY = 'any'       # year or semester, the user chooses
TERM_PART = 'part'


def _level(value, label, group, icon, programs=None, program_label='', terms=TERM_NONE,
           program_required=False):
    return {
        'value': value, 'label': label, 'group': group, 'icon': icon,
        'programs': programs or [], 'program_label': program_label,
        'terms': terms, 'program_required': program_required,
    }


LEVELS = (
    [_level(c, c, GROUP_SCHOOL, 'backpack') for c in _SCHOOL]
    + [
        _level('Class 8', 'Class 8', GROUP_SCHOOL, 'backpack'),
        _level('Class 9', 'Class 9', GROUP_SCHOOL, 'backpack'),
        _level('Class 10 / SEE', 'Class 10 / SEE', GROUP_SCHOOL, 'workspace_premium'),
        _level('11', 'Class 11', GROUP_PLUS2, 'menu_book', PLUS_TWO, 'Stream'),
        _level('12', 'Class 12', GROUP_PLUS2, 'menu_book', PLUS_TWO, 'Stream'),
        _level('+2 Passout', '+2 passed', GROUP_PLUS2, 'verified', PLUS_TWO, 'Stream'),
        _level('A-Levels / IB', 'A-Levels / IB / other board', GROUP_PLUS2, 'public'),
        _level('TSLC', 'TSLC / technical SLC', GROUP_TVET, 'build', TVET, 'Trade', TERM_PART),
        _level('Diploma', 'Diploma (CTEVT)', GROUP_TVET, 'engineering', TVET, 'Diploma in',
               TERM_ANY),
        _level('Bachelors', "Bachelor's", GROUP_UNI, 'account_balance', BACHELORS, 'Course',
               TERM_ANY),
        _level('Masters', "Master's", GROUP_UNI, 'school', MASTERS, 'Course', TERM_ANY),
        _level('PhD', 'PhD / doctorate', GROUP_UNI, 'biotech', DOCTORATE, 'Degree',
               TERM_YEAR),
        _level('Entrance Prep', 'Entrance exam prep', GROUP_PREP, 'edit_note',
               ENTRANCE_TARGETS, 'Preparing for'),
        _level('Competitive Exam', 'Competitive exam prep', GROUP_PREP, 'target',
               COMPETITIVE_TARGETS, 'Preparing for'),
        _level('Abroad', 'Studying abroad', GROUP_OTHER, 'flight_takeoff', ABROAD_LEVELS,
               'Level', TERM_YEAR),
        _level('Self Learner', 'Self-learner', GROUP_OTHER, 'auto_stories',
               SELF_LEARNER_FOCUS, 'Focus'),
        _level('Professional', 'Working professional', GROUP_OTHER, 'work',
               PROFESSIONAL_FIELDS, 'Field'),
        _level('Other', 'Something else', GROUP_OTHER, 'more_horiz'),
    ]
)
LEVEL_VALUES = [lv['value'] for lv in LEVELS]
LEVEL_BY_VALUE = {lv['value']: lv for lv in LEVELS}
LEVEL_LABELS = {lv['value']: lv['label'] for lv in LEVELS}

# Levels that are not a class, so filtering by grade makes no sense for them.
GLOBAL_LEVELS = {
    '+2 passout', 'a-levels / ib', 'tslc', 'diploma', 'bachelors', 'masters', 'phd',
    'entrance prep', 'competitive exam', 'abroad', 'self learner', 'professional', 'other',
    'dropout', 'gap year',
}

TERMS = {
    'year': ['Year %d' % n for n in range(1, 6)],
    'semester': ['Semester %d' % n for n in range(1, 11)],
    'part': ['Part 1', 'Part 2', 'Part 3'],
    'finished': ['Final year', 'Thesis / project', 'Result waiting'],
}

# What a person is open to. Shown as tonal chips on the profile.
OPEN_TO = [
    {'value': 'study_partner', 'label': 'Study partner', 'icon': 'groups'},
    {'value': 'mentoring', 'label': 'Mentoring juniors', 'icon': 'volunteer_activism'},
    {'value': 'get_mentored', 'label': 'Finding a mentor', 'icon': 'person_search'},
    {'value': 'tutoring', 'label': 'Tutoring', 'icon': 'school'},
    {'value': 'collab', 'label': 'Project collab', 'icon': 'handshake'},
    {'value': 'internship', 'label': 'Internships', 'icon': 'badge'},
    {'value': 'freelance', 'label': 'Freelance work', 'icon': 'work'},
    {'value': 'hiring', 'label': 'Hiring', 'icon': 'campaign'},
    {'value': 'scholarship', 'label': 'Scholarship info', 'icon': 'workspace_premium'},
    {'value': 'notes_swap', 'label': 'Swapping notes', 'icon': 'swap_horiz'},
]
OPEN_TO_VALUES = [o['value'] for o in OPEN_TO]

ENTRY_KINDS = [
    {'value': 'education', 'label': 'Education', 'icon': 'school'},
    {'value': 'experience', 'label': 'Experience', 'icon': 'work'},
    {'value': 'project', 'label': 'Projects', 'icon': 'deployed_code'},
    {'value': 'achievement', 'label': 'Achievements', 'icon': 'emoji_events'},
    {'value': 'certificate', 'label': 'Certificates', 'icon': 'workspace_premium'},
    {'value': 'volunteering', 'label': 'Volunteering', 'icon': 'volunteer_activism'},
]
ENTRY_KIND_VALUES = [k['value'] for k in ENTRY_KINDS]

COMPLETED_LEVELS = [
    {'value': 'Class 10 / SEE', 'label': 'SEE (Class 10)'},
    {'value': '+2 Passout', 'label': '+2 / Class 12'},
    {'value': 'TSLC', 'label': 'TSLC'},
    {'value': 'Diploma', 'label': 'Diploma'},
    {'value': 'Bachelors', 'label': "Bachelor's"},
    {'value': 'Masters', 'label': "Master's"},
    {'value': 'PhD', 'label': 'PhD'},
]
COMPLETED_VALUES = [c['value'] for c in COMPLETED_LEVELS]


def catalog():
    """The JSON the clients render their pickers from."""
    return {
        'statuses': STATUSES,
        'levels': LEVELS,
        'terms': TERMS,
        'completed': COMPLETED_LEVELS,
        'openTo': OPEN_TO,
        'entryKinds': ENTRY_KINDS,
    }


def level_label(value):
    return LEVEL_LABELS.get(value or '', value or '')


def status_label(value):
    for s in STATUSES:
        if s['value'] == value:
            return s['label']
    return ''


def clean_choice(value, allowed, default=''):
    value = (value or '').strip()
    return value if value in allowed else default


def clean_csv(value, allowed=None, limit=20, item_len=40):
    """Comma list -> de-duplicated, trimmed, length-capped string."""
    if isinstance(value, (list, tuple)):
        parts = [str(p) for p in value]
    else:
        parts = str(value or '').split(',')
    seen, out = set(), []
    for p in parts:
        p = ' '.join(p.split())[:item_len]
        key = p.lower()
        if not p or key in seen:
            continue
        if allowed is not None and p not in allowed:
            continue
        seen.add(key)
        out.append(p)
        if len(out) >= limit:
            break
    return ','.join(out)
