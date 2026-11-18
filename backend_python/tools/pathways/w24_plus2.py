"""Wave 24: seven +2 institutions confirmed on their own websites (opened live on 18 November 2026; page text checked for +2, NEB or
Grade 11 and for the streams and address). Streams are only linked when the page names them.
Pages: ria.edu.np (Reliance International Academy, NEB affiliated since 2060 BS), nss.edu.np (National School of Sciences, Science and
Management streams), hillpoint.edu.np (+2 Science, Management, Hotel Management and Fine Art), motherland.edu.np (+2 Science and
Management), radiant.edu.np (+2 courses), skyrider.edu.np (+2 pre-registration), caribbean.edu.np (+2 Science and Management).
"""

# (suffix, name, kind, district, place, website, note, routes)
ROWS = [
    ('ria', 'Reliance International Academy (RIA +2)', 'School', 'Kathmandu', 'Saraswatinagar, Chabahil', 'https://ria.edu.np',
     'English medium +2 school affiliated to NEB since 2060 BS (school established 2050 BS). Science and Management streams are on the website; confirm seats and fees with the school.',
     ['plus2-science', 'plus2-management']),
    ('nss', 'National School of Sciences', 'School', 'Kathmandu', 'Lainchour', 'https://nss.edu.np',
     'NEB +2 school at Lainchour that is part of the NIST Foundation. The website names Science and Management streams; confirm seats and fees with the school.',
     ['plus2-science', 'plus2-management']),
    ('hillpoint', 'Hill Point Secondary School', 'School', 'Kaski', 'Pokhara-12',  'https://hillpoint.edu.np',
     'Pokhara school with +2 Science, Management, Hotel Management and Fine Art programmes named on its website; confirm the current intake with the school.',
     ['plus2-science', 'plus2-management']),
    ('motherland', 'Motherland Secondary School', 'School', 'Kaski', 'Masbar, Pokhara-7', 'https://motherland.edu.np',
     'Pokhara school with +2 Science and Management streams named on its website; confirm seats and fees with the school.',
     ['plus2-science', 'plus2-management']),
    ('radiant', "Radiant Readers' Academy", 'School', 'Lalitpur', 'Sanepa-2', 'https://radiant.edu.np',
     "Lalitpur school (established 2056 BS) whose website lists +2 courses including Science and Management; confirm seats and fees with the school.",
     ['plus2-science', 'plus2-management']),
    ('skyrider', 'Skyrider Higher Secondary Boarding English School', 'School', 'Chitwan', 'Ratnanagar', 'https://skyrider.edu.np',
     'Chitwan boarding school that runs a +2 programme with online pre-registration on its website. Ask the school which streams are open this year.',
     []),
]
EXISTING = {'plus2-science': ['p-caribbean'], 'plus2-management': ['p-caribbean']}

PROVIDERS_ADD = []
WHERE_ADD = {}
for suf, name, kind, dist, place, site, note, routes in ROWS:
    pid = 'p-w24-plus2-' + suf
    PROVIDERS_ADD.append({'id': pid, 'name': name, 'kind': kind, 'sector': 'Private', 'district': dist, 'place': place,
                          'website': site, 'note': note})
    for r in routes:
        WHERE_ADD.setdefault(r, []).append(pid)
for r, ids in EXISTING.items():
    WHERE_ADD.setdefault(r, []).extend(ids)
