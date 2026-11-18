"""Wave 20 Nepal side: five new verified colleges (CAFODAT, Sirjana College of Fine Arts, NCFST, Lalitpur Valley College, Nilgiri College),
13 non-overlapping verified official websites, BTech Food seat quotas, and provider links for thin routes (btech-food, bfa, mpharm, msw, mca, ca-route, plus2-education, bjmc).

Sources (read 19 November 2026): BTech Food Technology college and quota tables (edusanjal.com, collegesnepal.com, padmashreecollege.edu.np, cafodat.edu.np);
BFA colleges in Nepal (edusanjal.com, admissionnepal.com); MPharm universities in Nepal (edusanjal.com, collegesnepal.com); live HTTP verification of 13
official college domains (divyagyan.edu.np, xa.edu.np, gpkmc.edu.np, kavrecampus.edu.np, nbpi.edu.np, knpi.edu.np, novel.edu.np, dhulabaricampus.edu.np,
danfecollege.edu.np, gnc.edu.np, milton.edu.np, nist.edu.np, vsic.edu.np).
"""

PROVIDERS_ADD = [
    {'id': 'p-cafodat', 'name': 'College of Applied Food and Dairy Technology (CAFODAT)', 'kind': 'private', 'sector': 'private',
     'district': 'Lalitpur', 'place': 'Purnachandi, Jawalakhel, Lalitpur', 'website': 'https://cafodat.edu.np', 'seats': 48,
     'route_seats': {'btech-food': 48},
     'note': 'Purbanchal University affiliated food and dairy technology college in Lalitpur offering 4 year BTech in Food Technology (48 seats) and MSc in Nutrition and Dietetics.'},
    {'id': 'p-sirjana-arts', 'name': 'Sirjana College of Fine Arts', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Uttar Dhoka, Lazimpat, Kathmandu',
     'note': 'Founded in 2001 under Tribhuvan University affiliation in Lazimpat, Kathmandu; offers 4 year Bachelor of Fine Arts (BFA) in Painting, Traditional Nepali Painting, Sculpture, Graphic Communication, Classical Music (Vocal, Instrumental, Tabla) and Classical Dance, plus NEB +2 Humanities.'},
    {'id': 'p-ncfst', 'name': 'National College of Food Science and Technology (NCFST)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Khusibu, Nayabazar, Kathmandu', 'seats': 24,
     'route_seats': {'btech-food': 24},
     'note': 'Tribhuvan University (IOST) affiliated college in Khusibu, Kathmandu offering the 4 year BTech in Food Technology programme (24 seats).'},
    {'id': 'p-lvc', 'name': 'Lalitpur Valley College (LVC)', 'kind': 'private', 'sector': 'private',
     'district': 'Lalitpur', 'place': 'Jawalakhel, Lalitpur', 'seats': 24,
     'route_seats': {'btech-food': 24},
     'note': 'Tribhuvan University affiliated college in Jawalakhel, Lalitpur offering 4 year BTech in Food Technology (24 seats), BSc Microbiology and BBS.'},
    {'id': 'p-nilgiri', 'name': 'Nilgiri College', 'kind': 'private', 'sector': 'private',
     'district': 'Sunsari', 'place': 'Itahari, Sunsari', 'seats': 24,
     'route_seats': {'btech-food': 24},
     'note': 'Tribhuvan University affiliated college in Itahari, Sunsari offering 4 year BTech in Food Technology (24 seats) and BBS.'},
]

WHERE_ADD = {
    'btech-food': ['p-cafodat', 'p-goldengate', 'p-padmashree', 'p-nist-lainchour', 'p-birat-multiple', 'p-ncfst', 'p-lvc', 'p-nilgiri', 'p-w12-ce-sunsari-technical-college'],
    'bfa': ['p-sirjana-arts', 'p-ku-school'],
    'mpharm': ['p-shas-pu', 'p-purbanchal-uni', 'p-iom'],
    'msw': ['p-sxc', 'p-thames', 'p-padmakanya', 'p-pu'],
    'mca': ['p-cite', 'p-kantipur-intl'],
    'ca-route': ['p-cca', 'p-nca', 'p-seed', 'p-tbc'],
    'plus2-education': ['p-mahendra-ratna', 'p-saptagandaki', 'p-butwal-kalika', 'p-surkhet-mc', 'p-prithvi', 'p-thakurram', 'p-ilam'],
    'bjmc': ['p-sxc', 'p-thames', 'p-ku-school'],
}

ROUTE_SEATS = {
    'p-cct': {'btech-food': 48},
    'p-goldengate': {'btech-food': 24},
    'p-padmashree': {'btech-food': 24},
    'p-nist-lainchour': {'btech-food': 24},
    'p-birat-multiple': {'btech-food': 24},
}

PROVIDER_WEBSITES = {
    'p-dibya-gyan': 'https://www.divyagyan.edu.np',
    'p-xavier-academy': 'https://xa.edu.np',
    'p-gp-koirala': 'https://gpkmc.edu.np',
    'p-kavre-mc': 'https://kavrecampus.edu.np',
    'p-w12-banepa-pi': 'https://nbpi.edu.np',
    'p-w12-korea-nepal': 'https://knpi.edu.np',
    'p-novel': 'https://novel.edu.np',
    'p-dhulabari': 'https://dhulabaricampus.edu.np',
    'p-danfe': 'https://danfecollege.edu.np',
    'p-greenfield': 'https://gnc.edu.np',
    'p-milton': 'https://milton.edu.np',
    'p-nist-lainchour': 'https://nist.edu.np',
    'p-vs-intl': 'https://vsic.edu.np',
}
