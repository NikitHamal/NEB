"""Wave 21 Nepal side: nine new verified institutions (IST College, GATE College, Silver Mountain School of Hotel Management,
Mid-Valley International College, South Asian School of Tourism and Hotel Management SASTHM, College of Biomedical Engineering and
Applied Sciences COBEAS, Valmiki Vidyapeeth NSU, Sainik Awasiya Mahavidyalaya Bhaktapur, Nepal Police School Sanga), 26 thin-route
provider expansions, seat quotas, and 15 live-verified official HTTPS websites.

Sources (read 19 November 2026): Edusanjal and ISMT BHM, biomedical engineering and Sanskrit campus directories (edusanjal.com, ismt.edu.np);
live HTTP 200 and HTML <title> verification across 22 official Nepal institution domains (istcollege.edu.np, gate.edu.np, silvermountain.edu.np,
midvalley.edu.np, sasthm.edu.np, bsamv.edu.np, nps.edu.np, nma.gov.np, brnc.tu.edu.np, bnc.tu.edu.np, nnc.tu.edu.np, ponc.tu.edu.np, bmc.tu.edu.np,
omcampus.edu.np, chelsea.edu.np, sirjanacollege.edu.np, nilgiricollege.edu.np, bpmpi.edu.np, pts.edu.np, kgpi.edu.np, npi.edu.np, aranikocollege.edu.np).
"""

PROVIDERS_ADD = [
    {'id': 'p-ist-college', 'name': 'International School of Tourism and Hotel Management (IST College)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Gyaneshwor, Kathmandu', 'website': 'https://istcollege.edu.np',
     'note': 'Hospitality and tourism college in Gyaneshwor, Kathmandu (established 2003 with Salzburg University of Applied Sciences / Silk Road University affiliation) offering Bachelor in Hotel Management (BHM) and Bachelor in Travel and Tourism Management (BTTM).'},
    {'id': 'p-gate-college', 'name': 'Global Academy of Tourism and Hospitality Education (GATE College)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Mandikatar, Kathmandu', 'website': 'https://gate.edu.np',
     'note': 'Swiss-affiliated (HotellerieSuisse) hospitality academy in Mandikatar, Kathmandu offering the 4 year Bachelor in International Hospitality Management (BIHM / BHM) and professional culinary/barista diplomas.'},
    {'id': 'p-silver-mountain', 'name': 'Silver Mountain School of Hotel Management (SMSH)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Lainchaur, Kathmandu', 'website': 'https://silvermountain.edu.np',
     'note': 'Hospitality management college in Lainchaur, Kathmandu affiliated with Queen Margaret University (UK) and American Hospitality Academy offering BA in International Hospitality and Tourism Management (BHM / BTTM) and culinary arts.'},
    {'id': 'p-mid-valley', 'name': 'Mid-Valley International College (MVIC)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Gyaneshwor, Kathmandu', 'website': 'https://midvalley.edu.np',
     'note': 'Gyaneshwor, Kathmandu college affiliated with HELP University (Malaysia) and City and Guilds (UK) offering Bachelor of Hospitality Management (Hons), Bachelor of Business (Finance / Marketing) and Bachelor of Information Technology (Hons).'},
    {'id': 'p-sasthm', 'name': 'South Asian School of Tourism and Hotel Management (SASTHM)', 'kind': 'private', 'sector': 'private',
     'district': 'Morang', 'place': 'Biratnagar, Morang', 'website': 'https://sasthm.edu.np', 'seats': 80,
     'route_seats': {'bhm': 80},
     'note': 'Established in 2000 in Biratnagar, Morang under Purbanchal University affiliation; offers 4 year Bachelor of Hotel Management (BHM, 80 seats), BBA and MBA.'},
    {'id': 'p-cobeas', 'name': 'College of Biomedical Engineering and Applied Sciences (COBEAS)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Dhapasi / Hadigaun, Kathmandu', 'seats': 60,
     'route_seats': {'be-biomedical': 60},
     'note': 'Established in 2005 under Purbanchal University affiliation in Kathmandu as Nepal pioneer biomedical engineering college; offers the 4 year BE in Biomedical Engineering (60 seats).'},
    {'id': 'p-valmiki', 'name': 'Valmiki Vidyapeeth (Valmiki Campus, Nepal Sanskrit University)', 'kind': 'public', 'sector': 'public',
     'district': 'Kathmandu', 'place': 'Exhibition Road, Kathmandu',
     'note': 'Constituent campus of Nepal Sanskrit University on Exhibition Road, Kathmandu offering Uttarmadhyama (+2 Sanskrit), Shastri (BA Sanskrit, Jyotish, Veda, Vyakarana, Sahitya, Darshan), Acharya (MA Sanskrit) and Yoga/Naturopathy training.'},
    {'id': 'p-samv-bhaktapur', 'name': 'Sainik Awasiya Mahavidyalaya (Bhaktapur)', 'kind': 'public', 'sector': 'public',
     'district': 'Bhaktapur', 'place': 'Sallaghari, Bhaktapur', 'website': 'https://bsamv.edu.np',
     'note': 'Flagship residential school operated under the Nepali Army Welfare Fund in Sallaghari, Bhaktapur offering Class 6 to 12 (SEE and NEB +2 Science, Management and Humanities) with structured sports, cadet discipline and TU BSc/BBA programmes.'},
    {'id': 'p-nps-sanga', 'name': 'Nepal Police School (Sanga)', 'kind': 'public', 'sector': 'public',
     'district': 'Kavrepalanchok', 'place': 'Sanga, Kavrepalanchok', 'website': 'https://nps.edu.np',
     'note': 'Residential school established in 1983 AD under the Nepal Police Welfare Fund in Sanga, Kavrepalanchok offering secondary SEE and NEB +2 Science and Management with athletics and cadet training.'},
]

WHERE_ADD = {
    'be-biomedical': ['p-cobeas'],
    'bfd-design': ['p-kantipur-intl'],
    'dip-forestry': ['p-kafcol', 'p-jiri-tech', 'p-w12-seti-ti'],
    'msc-agri': ['p-tu-kirtipur', 'p-purbanchal-uni'],
    'bhm': ['p-ist-college', 'p-gate-college', 'p-silver-mountain', 'p-mid-valley', 'p-sasthm', 'p-padmashree', 'p-kantipur-intl', 'p-padmakanya', 'p-saraswati-mc'],
    'bttm': ['p-ist-college', 'p-silver-mountain', 'p-kantipur-intl', 'p-tu-kirtipur', 'p-pu'],
    'aviation-cabin-crew': ['p-naa', 'p-haa', 'p-ist-college', 'p-gate-college', 'p-silver-mountain'],
    'sports-cadet-school': ['p-samv-bhaktapur', 'p-nps-sanga', 'p-w12-ce-budhanilkantha-secondary-school', 'p-sxc'],
    'sanskrit-gurukul': ['p-valmiki', 'p-kendriya-ayurveda', 'p-lbu'],
    'skill-training': ['p-bset', 'p-jiri-tech', 'p-w12-bheri-ti', 'p-w12-rapti-ti', 'p-w12-karnali-ti', 'p-w12-seti-ti', 'p-w12-lahan-ti', 'p-w12-pokhara-ti'],
    'pre-diploma': ['p-w12-bheri-ti', 'p-w12-rapti-ti', 'p-w12-karnali-ti', 'p-w12-seti-ti', 'p-w12-lahan-ti', 'p-w12-pokhara-ti', 'p-w12-panauti-ti'],
    'dip-geomatics': ['p-eastern-coe', 'p-w12-damak-pi', 'p-w12-bharatpur-pi', 'p-w12-pokhara-ti', 'p-w12-bheri-ti'],
    'pcl-dental': ['p-kmc-health', 'p-om-health', 'p-koshi-health', 'p-modern-tech', 'p-valley-tech'],
    'pcl-ayurveda-physio': ['p-kendriya-ayurveda', 'p-nsu', 'p-ayurved', 'p-koshi-health'],
    'pcl-cmlt': ['p-om-health', 'p-koshi-health', 'p-modern-tech', 'p-valley-tech', 'p-npi-narayani'],
    'pcl-ophthalmic': ['p-himalaya-eye', 'p-bpkihs', 'p-nams', 'p-w12-bheri-ti'],
    'bpa': ['p-shankerdev', 'p-mmamc', 'p-prithvi', 'p-mu', 'p-pu'],
    'mpa': ['p-mmamc', 'p-prithvi', 'p-mu', 'p-pu'],
    'msc-nursing': ['p-pokhara-nursing', 'p-pahs', 'p-pu-medicine', 'p-shas-pu'],
    'mpharm': ['p-cist', 'p-valley-tech', 'p-kusms'],
    'llm': ['p-pu', 'p-mu', 'p-fwu', 'p-prithvi'],
    'bba-bi': ['p-ace-mgt', 'p-uniglobe', 'p-united-academy'],
    'bsc-geology': ['p-amrit', 'p-mmamc', 'p-siddhanath'],
    'ba-psychology': ['p-tu-kirtipur', 'p-thames', 'p-prithvi'],
    'bsw': ['p-thames', 'p-trichandra', 'p-damak-mc', 'p-bhaktapur-mc'],
    'msc-urban-struct': ['p-ncit', 'p-nec', 'p-khwopa-eng', 'p-pu-soe'],
}

ROUTE_SEATS = {
    'p-kafcol': {'dip-forestry': 40},
    'p-kantipur-intl': {'bfd-design': 30, 'bhm': 60},
    'p-padmakanya': {'bhm': 44},
    'p-saraswati-mc': {'bhm': 44},
}

PROVIDER_WEBSITES = {
    'p-biratnagar-nursing': 'https://brnc.tu.edu.np',
    'p-birgunj-nursing': 'https://bnc.tu.edu.np',
    'p-nepalgunj-nursing': 'https://nnc.tu.edu.np',
    'p-pokhara-nursing': 'https://ponc.tu.edu.np',
    'p-bhairahawa-mc': 'https://bmc.tu.edu.np',
    'p-om-health': 'https://www.omcampus.edu.np',
    'p-chelsea': 'https://www.chelsea.edu.np',
    'p-sirjana-arts': 'https://sirjanacollege.edu.np',
    'p-nilgiri': 'https://nilgiricollege.edu.np',
    'p-w12-bp-memorial': 'https://bpmpi.edu.np',
    'p-w12-panauti-ti': 'https://pts.edu.np',
    'p-w12-kaligandaki-pi': 'https://kgpi.edu.np',
    'p-npi-narayani': 'https://npi.edu.np',
    'p-araniko-mc': 'https://aranikocollege.edu.np',
    'p-nma': 'https://nma.gov.np',
}
