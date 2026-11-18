"""Wave 25: Far-Western University and Mid-West University constituent campuses that the dataset did not list yet.

Sources (opened live in this session):
- FWU Faculty of Education campus table (facultyeducation.fwu.edu.np/academic/campus.html): 16 rows, each with district,
  website and programmes (B.Ed., M.Ed., CSIT in Education, PBEd).
- FWU campus homepages (tikapur / treveni / ghanteshwar / sitaram / patan / durgalaxmi / manilek .fwu.edu.np, all HTTP 200);
  Tikapur homepage names BBA and B.Ed orientation programmes, Triveni homepage names a BBS and B.Ed scholarship notice.
- FWU campus list on fwu.edu.np/page/campuses.html (15 campuses) plus the Education table (adds Durgalaxmi, 16th).
- Mid-West University LMS (mulms.edu.np) lists Tila Karnali and Vidhyapur Janata campuses; Edusanjal and the MU admission
  notice for 2083/84 (collegenp.com) name the programmes of Bageshwari Multiple Campus.
Programmes are linked only where a named page lists them.
"""

FWU_NOTE = 'Constituent campus of Far-Western University. '

# (suffix, name, district, place, website, note, routes)
ROWS = [
    ('tikapur', 'Tikapur Multiple Campus (Far-Western University)', 'Kailali', 'Tikapur', 'https://tikapur.fwu.edu.np',
     FWU_NOTE + 'Established 2001. The FWU Faculty of Education list gives B.Ed., M.Ed. and PBEd, and the campus homepage announces BBA and B.Ed orientation programmes. Phone 091-560088.',
     ['bed', 'med', 'bba']),
    ('triveni', 'Triveni Multiple Campus (Far-Western University)', 'Dadeldhura', 'Jogbuda, Parshuram-12', 'https://treveni.fwu.edu.np',
     FWU_NOTE + 'Undergraduate campus in Parshuram Municipality-12. The FWU Education list gives B.Ed. and the campus site posts a scholarship notice for BBS and B.Ed. semesters.',
     ['bed', 'bbs']),
    ('ghanteshwar', 'Ghanteshwar Seti Mahakali Multiple Campus (Far-Western University)', 'Doti', 'Jorayal', 'https://ghanteshwar.fwu.edu.np',
     FWU_NOTE + 'The FWU Faculty of Education list gives B.Ed. at this Doti campus. Ask the campus about other programmes before applying.',
     ['bed']),
    ('sitaram', 'Sitaram Multiple Campus (Far-Western University)', 'Doti', 'Jijomandu', 'https://sitaram.fwu.edu.np',
     FWU_NOTE + 'The FWU Faculty of Education list gives B.Ed. at this Doti campus. Phone 094-524000.',
     ['bed']),
    ('patan-baitadi', 'Patan Multiple Campus, Baitadi (Far-Western University)', 'Baitadi', 'Patan', 'https://patan.fwu.edu.np',
     FWU_NOTE + 'Not the Patan Campus of Lalitpur. The FWU Faculty of Education list gives B.Ed. here. Phone 095-400034.',
     ['bed']),
    ('durgalaxmi', 'Durgalaxmi Multiple Campus (Far-Western University)', 'Kailali', 'Attariya', 'https://durgalaxmi.fwu.edu.np',
     FWU_NOTE + 'Sixteenth FWU campus on the Faculty of Education list (the main FWU campus page shows 15). Programmes: B.Ed., M.Ed. and CSIT in Education.',
     ['bed', 'med']),
    ('bageshwari', 'Bageshwari Multiple Campus (Mid-West University)', 'Banke', 'Kohalpur', None,
     'Constituent campus of Mid-West University, established 1992. Edusanjal lists B.Ed., BBS, BA, M.Ed., MA and MBS, and the MU 2083/84 bachelor admission notice lists BSc, BBS, BBA, B.Ed. and BA. Also runs +2 Management and Education under NEB. Phone 081-540076.',
     ['bed', 'bbs', 'ba', 'bba', 'med', 'mbs']),
    ('vidhyapur', 'Vidhyapur Janata Multiple Campus (Mid-West University)', 'Surkhet', 'Bidhyapur-4', None,
     'Constituent campus of Mid-West University listed on its LMS (mulms.edu.np). College portals show BBS and B.Ed. here; confirm the intake with the campus.',
     ['bed', 'bbs']),
]
# Existing providers that FWU lists for these programmes (FWU Faculty of Education table, checked live)
EXISTING = {
    'bed': ['p-w24-iost-manilek', 'p-fwu'],
    'med': ['p-badimalika-bajura', 'p-fwu', 'p-gokuleshwor-darchula', 'p-jagannath-baitadi', 'p-achham',
            'p-jayaprithvi-bajhang', 'p-kailali'],
}

PROVIDERS_ADD = []
WHERE_ADD = {}
for suf, name, dist, place, site, note, routes in ROWS:
    pid = 'p-w25-' + suf
    row = {'id': pid, 'name': name, 'kind': 'Campus', 'sector': 'Public', 'district': dist, 'place': place, 'note': note}
    if site:
        row['website'] = site
    PROVIDERS_ADD.append(row)
    for r in routes:
        WHERE_ADD.setdefault(r, []).append(pid)
for r, ids in EXISTING.items():
    WHERE_ADD.setdefault(r, []).extend(ids)

# Manilek Multiple Campus is on the FWU list (Melauli-04, Kanda, Baitadi, B.Ed.) and on the TU IoST table; wave 24 marked it Private.
PROVIDER_UPDATE = {
    'p-w24-iost-manilek': {
        'name': 'Manilek Multiple Campus (FWU and TU IoST)', 'sector': 'Public', 'place': 'Melauli-04, Kanda',
        'website': 'https://manilek.fwu.edu.np',
        'note': 'Far-Western University constituent campus (FWU Faculty of Education list: B.Ed.) that the TU Institute of Science and Technology table also lists for B.Sc. General. Confirm the intake and fee with the campus.',
    },
}
