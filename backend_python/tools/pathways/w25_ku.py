"""Wave 25: Kathmandu University "Affiliated and Extended Programs" table (ku.edu.np/affiliated-colleges, 32 institutions, each
with programme codes and starting year, read live in this session) diffed against the dataset.

The 10 medical, dental and nursing institutions on the list were already in the dataset with the right KU programmes.
Twenty institutions were missing and are added here. Two college sites were opened and the page text names KU and BIT:
ashoka.edu.np (Pokhara-8 Srijanachowk, BIT) and prativa.edu.np (Pokhara-4 Gairapatan, first BIT intake 2026).
Programme codes follow ku.edu.np/programs: BPH is Bachelor in Professional Hospitality (not public health), BBIS is Business
Information Systems. BHI, BES, BoSS and BDFin are kept as the KU codes because the table does not spell them out.
"""
KU = 'Kathmandu University affiliated and extended programs table (ku.edu.np/affiliated-colleges)'

# (suffix, name, kind, sector, district, place, website, programmes text, routes)
ROWS = [
    ('aspire', 'Aspire College', 'College', 'Private', 'Morang', 'Biratnagar', None,
     'BPH (Professional Hospitality) from 2022, BIT from 2024, B.Tech.Ed. IT and BHI from 2026', ['bit', 'bhm']),
    ('ashoka', 'Ashoka College of Engineering and Management', 'College', 'Private', 'Kaski', 'Pokhara-8, Srijanachowk', 'https://ashoka.edu.np',
     'BIT from 2026 (its own site says it offers the KU Bachelor of Information Technology; phone 9856081540)', ['bit']),
    ('bti', 'Butwal Technical Institute (BTI)', 'Institute', 'Private', 'Rupandehi', 'Butwal', None,
     'B.Tech.Ed. from 2022', []),
    ('glacier', 'Glacier College', 'College', 'Private', 'Kavrepalanchok', 'Banepa', None,
     'BPH (Professional Hospitality) from 2022', ['bhm']),
    ('janaki', 'Janaki College for Professional Studies', 'College', 'Private', 'Dhanusha', 'Dhanusha', None,
     'B.Tech.Ed. from 2022', []),
    ('janakpur-cc', 'Janakpur Community College', 'College', 'Community', 'Dhanusha', 'Janakpur', None,
     'BSW (Social Work) from 2026', ['bsw']),
    ('little-angels', "Little Angel's College of Management", 'College', 'Private', 'Lalitpur', 'Lalitpur', None,
     'BBA from 1999, BBIS from 2003 and BHTM (Hotel and Tourism Management) from 2010', ['bba', 'bhm']),
    ('naya-aayam', 'Naya Aayam Multidisciplinary Institute', 'Institute', 'Private', 'Kathmandu', 'New Baneshwor', None,
     'BES from 2026 (KU code, not spelled out in the table)', []),
    ('nwa', 'Nepal Western Academy', 'College', 'Private', 'Kailali', 'Dhangadhi', None,
     'BIT and BSW from 2026', ['bit', 'bsw']),
    ('national-ku', 'National College (Kathmandu University programmes)', 'College', 'Private', 'Kathmandu', 'Kathmandu', None,
     'BDevS (Development Studies) from 1999, BDFin from 2006 and BoSS from 2013. Not the same as the NCCS computer college.', ['ba-economics']),
    ('ncm', 'Nepal College of Management', 'College', 'Private', 'Kathmandu', 'Kathmandu', None,
     'BBA from 1999 and BHTM (Hotel and Tourism Management) from 2010', ['bba', 'bhm']),
    ('new-everest', 'New Everest College', 'College', 'Private', 'Morang', 'Biratnagar', None,
     'BIT from 2026', ['bit']),
    ('prativa', 'Prativa Business School', 'College', 'Private', 'Kaski', 'Pokhara-4, Gairapatan', 'https://prativa.edu.np',
     'BIT, first intake in 2026 (its site: entrance is the KUCAT-CBT, phone 061-570025)', ['bit']),
    ('radiant-ku', 'Radiant College (Rupandehi)', 'College', 'Private', 'Rupandehi', 'Rupandehi', None,
     'B.Tech.Ed. from 2024 and BIT from 2026. Not the Radiant Readers Academy of Lalitpur.', ['bit']),
    ('scti', 'Sindhuli Community Technical Institute (SCTI)', 'Institute', 'Community', 'Sindhuli', 'Sindhuli', None,
     'B.Tech.Ed. from 2022', []),
    ('south-city', 'South City College of Science and Technology', 'College', 'Private', 'Parsa', 'Birgunj', None,
     'BIT and B.Tech.Ed. IT from 2026', ['bit']),
    ('nathm-bardibas', 'Nepal Academy of Tourism and Hotel Management (NATHM), Bardibas', 'College', 'Public', 'Mahottari', 'Bardibas', None,
     'BHM from 2022 under KU, listed as a separate site from the NATHM campus in Kathmandu', ['bhm']),
    ('titi', 'Training Institute for Technical Instruction (TITI)', 'Institute', 'Public', 'Bhaktapur', 'Sanothimi', None,
     'B.Tech.Ed. since 2001, the oldest programme on the KU affiliated table', []),
    ('whitehouse-bt', 'WhiteHouse College of Business and Technology', 'College', 'Private', 'Jhapa', 'Birtamod', None,
     'BIT and B.Tech.Ed. IT from 2026 (WhiteHouse Education Foundation). Not Himalayan WhiteHouse International College.', ['bit']),
    ('nit-gaidakot', 'Nagarik Institute of Technology (NIT) College', 'College', 'Private', 'Nawalparasi East', 'Gaidakot', None,
     'BIT from 2026. The TU IoST table lists Nagarik College in Gaidakot; confirm with the college whether it is the same campus.', ['bit']),
]

PROVIDERS_ADD = []
WHERE_ADD = {}
for suf, name, kind, sector, dist, place, site, progs, routes in ROWS:
    pid = 'p-w25-ku-' + suf
    row = {'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': dist, 'place': place,
           'note': f'Kathmandu University affiliated institution. {KU} lists: {progs}. Confirm the intake, seats and fee with the college.'}
    if site:
        row['website'] = site
    PROVIDERS_ADD.append(row)
    for r in routes:
        WHERE_ADD.setdefault(r, []).append(pid)

PROVIDER_UPDATE = {
    'p-gate-college': {'note': 'Swiss-affiliated (HotellerieSuisse) hospitality academy in Mandikatar, Kathmandu offering the 4 year Bachelor in International Hospitality Management (BIHM / BHM) and professional culinary/barista diplomas. The KU affiliated table also lists it for BPH (Bachelor in Professional Hospitality) since 2020.'},
}
