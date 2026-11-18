"""Wave 23: student work and post-study stay rules read on the official European Commission EU Immigration Portal
(home-affairs.ec.europa.eu/policies/migration-and-asylum/eu-immigration-portal/student-<country>_en, read in this session)
and, for Poland, the Study in Poland portal. Each country says which page it came from.

Corrections: the Lithuania note used to say the Commission page allows 40 hours a week; the page now says 20 hours a week
in term time (not for doctoral students) and 12 months of job search after graduation. Czechia: the Commission page gives
free access to the labour market, so the old 20 hour agency claim is dropped from the headline number.
"""
EC = 'European Commission EU Immigration Portal'

ABROAD_UPDATE = {
    'lt': {
        'work': f'Up to 20 hours a week in term time, not counted in the university summer holiday and not applied to doctoral students ({EC}, Lithuania page). You need the temporary residence permit before you work: with only a national D visa you may not work during studies.',
        'work_hours': 20,
        'stay_back': '12 months on a temporary residence permit for job search or self-employment after graduation',
    },
    'lv': {
        'work': f'Up to 20 hours a week in term and up to 40 hours a week in study holidays; graduate and postgraduate students may work up to 40 hours a week ({EC}, Latvia page).',
        'stay_back': 'Up to 9 months on a temporary residence permit to seek employment or start a business, applied for inside Latvia',
    },
    'mt': {
        'work': f'Students on courses at MQRIC level 5 and above may work up to 20 hours a week outside study time with an employment licence issued by Jobsplus; short courses at levels 1 to 4 also have a 20 hour cap ({EC}, Malta page).',
        'stay_back': 'A residence permit of at least 9 months to seek employment or set up a business, plus an employment licence to work',
    },
    'cz': {
        'work': f'A long term study visa or permit lets you work without an Employee Card, Blue Card or work permit, with free access to the labour market while the permit is valid ({EC}, Czechia page). Studies must stay the main purpose of your stay.',
        'stay_back': '9 months on a residence permit to seek employment or start a business; it cannot be renewed (Ministry of the Interior rule on the EC page)',
    },
    'pl': {
        'stay_back': 'Up to 9 months on a temporary residence permit to look for work or start a business, only for graduates of Polish full time higher education (Study in Poland and EC Poland page)',
    },
    'at': {
        'stay_back': f'12 more months of legal stay to seek employment after graduation, applied for before the student permit ends ({EC}, Austria page)',
    },
    'be': {
        'stay_back': f'Up to 12 months extension after studies to look for work or set up a company ({EC}, Belgium page)',
    },
    'se': {
        'stay_back': 'Up to 12 months on a residence permit to look for work or start a business after a completed bachelor or master programme (Migrationsverket rule, as quoted by EnglishJobsSweden in September 2026); it cannot be extended',
    },
    'cy': {
        'work': f'Up to 20 hours a week, only in listed sectors such as restaurants, cleaning, health and social care, agriculture and manufacturing, and the employment contract must be certified by the Department of Labour ({EC}, Cyprus page).',
        'work_hours': 20,
    },
    'ro': {
        'work': f'Part time work without a separate work authorisation for up to 4 hours a day ({EC}, Romania page). After graduation you can extend your stay only with a full time work contract related to your field of study.',
    },
}

# Master level routes that had no next step: the official PhD and MPhil routes stay open after them.
ROUTE_NEXT = {
    'mbs': ['mphil', 'phd-route'],
    'med': ['mphil', 'phd-route'],
    'mtech': ['phd-route'],
    'mca': ['phd-route'],
    'msc-nursing': ['phd-route'],
    'mpharm': ['phd-route'],
    'msc-agri': ['phd-route'],
    'msw': ['mphil', 'phd-route'],
    'llm': ['phd-route'],
}
