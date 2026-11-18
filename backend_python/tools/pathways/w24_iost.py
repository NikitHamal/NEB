"""Wave 24: TU Institute of Science and Technology affiliated colleges, read from the official table
https://iost.tu.edu.np/pages/our-affiliated-colleges-329 on 18 November 2026 (90 rows, serial numbers run to 91 and number 79 is not in the table: campus, location, bachelor and master programmes).

Only rows that add a programme the dataset did not link yet are used (B.Sc. general, Microbiology, Environmental Science, B.Tech Food).
CSIT only rows are skipped because wave 10 holds the 2083 CSIT quota list for 61 colleges. Rows whose campus could not be matched to one
institution with certainty (Dharan Multiple Campus, Jahari Campus, Rukum) were left out.
"""

SRC = 'TU IoST affiliated college table (iost.tu.edu.np, 18 Nov 2026)'

# existing provider id -> routes the IoST table lists for that campus
EXISTING = {
    'p-birat-multiple': ['bsc-microbiology', 'btech-food'],
    'p-birendra-memorial': ['bsc-microbiology'],
    'p-sunkoshi-sindhu': ['bsc-science'],
    'p-damak-mc': ['bsc-science', 'bsc-environment'],
    'p-gokuleshwor-darchula': ['bsc-science'],
    'p-goldengate': ['bsc-science', 'bsc-microbiology', 'btech-food'],
    'p-harikhetan': ['bsc-microbiology', 'bsc-environment'],
    'p-kailali': ['bsc-science'],
    'p-lvc': ['bsc-microbiology', 'btech-food'],
    'p-mmc-hetauda': ['bsc-science'],
    'p-model-multiple-janakpur': ['bsc-science', 'bsc-microbiology'],
    'p-mount-annapurna': ['bsc-microbiology'],
    'p-nist-lainchour': ['bsc-microbiology', 'btech-food'],
    'p-ncfst': ['btech-food'],
    'p-new-horizon-butwal': ['bsc-science'],
    'p-nilgiri': ['btech-food'],
    'p-nist-banepa': ['bsc-science'],
    'p-padmashree': ['btech-food'],
    'p-samv-bhaktapur': ['bsc-science', 'bsc-microbiology'],
    'p-saptagandaki': ['bsc-environment'],
    'p-sxc': ['bsc-science', 'bsc-microbiology'],
    'p-w12-ce-sunsari-technical-college': ['bsc-microbiology', 'btech-food'],
    'p-xavier-intl': ['bsc-microbiology', 'bsc-environment'],
}

# (suffix, name, district, place, website or None, IoST programme text, routes)
NEW = [
    ('aishwarya', 'Aishwarya Multiple Campus', 'Kailali', 'Dhangadhi', None, 'B.Sc. General', ['bsc-science']),
    ('balkumari', 'Balkumari College', 'Chitwan', 'Narayangadh', 'https://www.balkumaricollege.edu.np', 'B.Sc. Microbiology and Environmental Science', ['bsc-microbiology', 'bsc-environment']),
    ('bharawi', 'Bharawi Science College', 'Sunsari', 'Itahari', None, 'B.Sc. General', ['bsc-science']),
    ('canvas', 'Canvas International College', 'Kathmandu', 'Basundhara', None, 'B.Sc. General', ['bsc-science']),
    ('college-applied-sciences', 'College of Applied Sciences', 'Kathmandu', 'Anamnagar', None, 'B.Sc. Environmental Science and M.Sc. Environmental Science', ['bsc-environment']),
    ('dav-mgmt', 'D.A.V. College of Management', 'Lalitpur', 'Jawalakhel', 'https://davcollege.edu.np', 'B.Sc. General and Microbiology', ['bsc-science', 'bsc-microbiology']),
    ('gyandeep', 'Gyandeep College', 'Dang', 'Tulsipur', None, 'B.Sc. General', ['bsc-science']),
    ('jsm-lahan', 'J.S. Murarka Campus', 'Siraha', 'Lahan', None, 'B.Sc. General', ['bsc-science']),
    ('janapriya-mc', 'Janapriya Multiple College', 'Kaski', 'Pokhara', None, 'B.Sc. Microbiology and Environmental Science', ['bsc-microbiology', 'bsc-environment']),
    ('kamala-science', 'Kamala Science Campus', 'Sindhuli', 'Sindhuli', None, 'B.Sc. General', ['bsc-science']),
    ('kantipur-cms', 'Kantipur College of Medical Sciences', 'Kathmandu', 'Sitapaila', None, 'B.Sc. Microbiology and M.Sc. Microbiology', ['bsc-microbiology']),
    ('karnali-prabidhi', 'Karnali Prabidhi Campus', 'Kalikot', 'Sipkhana', None, 'B.Sc. General', ['bsc-science']),
    ('kcst', 'Kathmandu College of Science and Technology', 'Kathmandu', 'Naxal', None, 'B.Sc. Microbiology and M.Sc. Microbiology', ['bsc-microbiology']),
    ('khwopa-college', 'Khwopa College', 'Bhaktapur', 'Bhaktapur', None, 'General B.Sc. including Environmental Science, and M.Sc. Environmental Science', ['bsc-science', 'bsc-environment']),
    ('manilek', 'Manilek Campus', 'Baitadi', 'Baitadi', None, 'B.Sc. General', ['bsc-science']),
    ('nagarik-nawalparasi', 'Nagarik College', 'Nawalparasi East', 'Gaidakot', None, 'B.Tech Food Technology', ['btech-food']),
    ('national-multiple', 'National Multiple College', 'Lalitpur', 'Bakhundole', None, 'General B.Sc.', ['bsc-science']),
    ('padmodaya', 'Padmodaya Campus', 'Dang', 'Ghorahi', None, 'B.Sc. General', ['bsc-science']),
    ('pinnacle', 'Pinnacle College', 'Lalitpur', 'Lagankhel', None, 'B.Sc. Microbiology', ['bsc-microbiology']),
    ('pokhara-cst', 'Pokhara College of Science and Technology', 'Kaski', 'Pokhara', None, 'General B.Sc. including Microbiology, B.Tech Food Technology and M.Sc. Microbiology', ['bsc-science', 'bsc-microbiology', 'btech-food']),
    ('sahid-smriti-chitwan', 'Sahid Smriti Multiple Campus', 'Chitwan', 'Chitwan', None, 'B.Sc. General', ['bsc-science']),
    ('softech-lahan', 'Softech College', 'Siraha', 'Lahan', None, 'B.Sc. General including Microbiology', ['bsc-science', 'bsc-microbiology']),
    ('sukuna', 'Sukuna Multiple Campus', 'Morang', 'Morang', None, 'B.Sc. General', ['bsc-science']),
]

PROVIDERS_ADD = []
WHERE_ADD = {}
for suf, name, dist, place, site, progs, routes in NEW:
    pid = 'p-w24-iost-' + suf
    kind = 'Campus' if 'Campus' in name else 'College'
    p = {'id': pid, 'name': name, 'kind': kind, 'sector': 'Private', 'district': dist, 'place': place,
         'note': 'Tribhuvan University affiliated ' + kind.lower() + ' in ' + place + '. The TU Institute of Science and Technology '
                 'affiliated college table (iost.tu.edu.np, checked 18 Nov 2026) lists ' + progs + '. Confirm the intake and fee with the college.'}
    if site:
        p['website'] = site
    PROVIDERS_ADD.append(p)
    for r in routes:
        WHERE_ADD.setdefault(r, []).append(pid)
for pid, routes in EXISTING.items():
    for r in routes:
        WHERE_ADD.setdefault(r, []).append(pid)

