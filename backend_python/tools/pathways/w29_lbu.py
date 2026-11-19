"""Wave 29: Lumbini Buddhist University (lbu.edu.np/our-campuses, the campus pages, fbscourses, fhss-courses, fdsas-courses,
read 19 Nov 2026) and Nepal Open University (nou.edu.np faculty pages, read 19 Nov 2026).

LBU lists 12 campuses. Nine have a place on their LBU page and become rows; Sulakshyan Kriti Campus (its page is a 404),
Lumbini International Academy of Science and Technology (no address on its page, phone 01) and the Thrangu Sekhar Institute
of Meditation (named only on a course) stay in the note of the university row. Course data: lbu_courses.json (scrape_lbu.py).
"""
CK = 'checked 19 Nov 2026'

# id, name, kind, sector, district, place, website, programmes (as the LBU page prints them), routes, extra note
CAMPUSES = [
    ('p-w29-lbu-city-butwal', 'LBU City Campus Butwal', 'Campus', 'Public', 'Rupandehi', 'Nayagaun, Butwal',
     'https://citycampus.lbu.edu.np',
     'BBA (120 credits), BTTM (120), BHTM Hospitality Tourism Management (120), BA LL.B. (220.5), BTCSOL Teaching Chinese to Speakers of Other Languages (166, with the Central Campus), MBA in Hospitality Management (66) and MIRPD Master in International Relations, Peace and Diplomacy (60)',
     ['bba', 'bttm', 'bhm', 'ba-llb', 'mba', 'ma'], "It is the university's own city campus in Butwal Nayagaun."),
    ('p-w29-lbu-tulsipur-metro', 'Tulsipur Metro College', 'College', 'Not stated', 'Dang', 'Tulsipur',
     'https://lbu.edu.np/tulsipur-metro-college/',
     'BBA (120 credits), BHTM Hospitality Tourism Management (120) and BA LL.B. (220.5)',
     ['bba', 'bhm', 'ba-llb'], 'The LBU page does not give a street address or the sector.'),
    ('p-w29-lbu-sdsas-devdaha', 'LBU School of Development Studies and Applied Sciences (Devdaha)', 'Campus', 'Public', 'Rupandehi',
     'Sittalnagar, Devdaha', 'https://lbu.edu.np/fdsas/',
     'M.Sc. in Agro-Forestry (63 credits) and Master in Development Studies (60); the Master of Arts in Translation and Interpreting (60) is taught at the Devdaha Education Development Project',
     ['msc-agri', 'ma'], 'The Devdaha Education Development Project is a collaboration between LBU and the South to North Water Diversion Metaverse Research Center.'),
    ('p-w29-lbu-sowa-rigpa', 'Sowa Rigpa International College', 'College', 'Not stated', 'Kathmandu',
     'Arubari Height, Gokarneshwor-15 (behind Boudhanath Stupa)', 'https://lbu.edu.np/sric/',
     'Bachelor of Sowa Rigpa Medicine and Surgery (BSRMS, 120 credits), the first degree in Sowa Rigpa (traditional Himalayan and Tibetan medicine) in Nepal by its own account; it has a clinic and pharmacy on site. Phone +977 1-4914082',
     [], 'There is no route for Sowa Rigpa in this app, so it is not linked to a course page.'),
    ('p-w29-lbu-aksheswar-art', 'Aksheswar Traditional Buddhist Art College', 'College', 'Not stated', 'Lalitpur',
     'Aksheswar Mahabihar, Pulchowk-3', 'https://lbu.edu.np/akshaswor/',
     'Bachelor in Traditional Buddhist Art (BTBA, 120 credits; Paubha painting and traditional statue making). Phone +977 9810039778',
     ['bfa'], 'No fee or seat count is given.'),
    ('p-w29-lbu-lotus', 'Lotus Buddhist Academic College', 'College', 'Not stated', 'Lalitpur', 'Khwayabahil',
     'https://lbu.edu.np/lotus/',
     'Master in Buddhist Studies (MBS) and Master in Applied Buddhism (MAB, 66 credits, lecture and online). Principal Dharma Sundar Bajracharya, 015549343',
     ['ma'], 'It is a part of the Lotus Research Centre.'),
    ('p-w29-lbu-boudha-multiple', 'Boudha Multiple Campus', 'Campus', 'Community', 'Kathmandu', 'Boudha',
     'https://lbu.edu.np/bmc/',
     'Master in Buddhism and Peace Studies (MBPS, 60 credits, 2 years, semester based) under LBU; the campus also runs Tribhuvan University programmes. Principal Dr. Mohan Khatiwada, 014915592',
     ['ma'], 'Community based, non-profit, established 2066 BS (LBU page).'),
    ('p-w29-lbu-lcbhs', 'Lumbini College of Buddhism and Himalayan Studies', 'College', 'Public', 'Kathmandu',
     'Chuchepati, Chabahil (Taragaon Regency premises)', 'https://lbu.edu.np/lcbhs/',
     'Master in Buddhism and Himalayan Studies (MBHS, 80 credits, 2 years full time, semester based). Principal Dr. Ramesh Kumar Dhungal',
     ['ma'], 'Established 2013, recognised by the University Grants Commission (LBU page).'),
    ('p-w29-lbu-sugata', 'Sugata Buddhist College', 'College', 'Community', 'Lalitpur', 'Rajshree Mahavihara (Ibabahi), Tangal, Patan',
     'https://lbu.edu.np/sbc/', 'Master in Mahayana Buddhism (MMB, 60 credits). Phone 01-5528795',
     ['ma'], 'Sister organisation of the Nepal Buddhist Council, established 2012, over 150 scholars produced by its own count.'),
    ('p-w29-lbu-theravada', 'Theravada Buddhist Academy', 'College', 'Not stated', 'Kathmandu', 'Vishwa Shanti Vihar, Meenbhawan',
     'https://lbu.edu.np/tba/', 'Master in Theravada Buddhism (MTB, 60 credits) and Master in Pali Buddhist Studies (MPBS, 60)',
     ['ma'], 'It works under the Vishwa Shanti Vihar.'),
]

LBU_NOTE = (f"LBU course lists ({CK}, lbu.edu.np) show 30 programmes. Central Campus Lumbini: Ph.D. in Buddhist Studies, Master's Degree by Dissertation "
            '(MDD), MA in Buddhism and Nepal Studies, MA in Bhot Buddhist Studies, MA in Archaeology and Buddhist Archaeological Sites, Master in Buddhist '
            'Studies, Bachelor of Buddhism and Social Work, BA (Rural Development), Bachelor in Bhot Buddhist Studies, BTCSOL, Certificate in Buddhist '
            'Meditation (30 credits, with Thrangu Sekhar Institute of Meditation) and a postgraduate diploma in Buddhism-informed psychosocial counselling. '
            'The university names 11 other campuses (3 collaborating institutions and 8 affiliated in Bagmati province). Sulakshyan Kriti Campus (Master in '
            'Buddhism and Sustainable Development, 60 credits) and the Lumbini International Academy of Science and Technology (M.Sc. in Construction '
            'Engineering and Management and in Disaster Risk Engineering and Management) are listed but their LBU pages give no address, so they have no row here.')
LBU_ROUTES = ['ma', 'bsw', 'ba', 'phd-route']

NOU_NOTE = (f'Nepal Open University faculty pages ({CK}, nou.edu.np). Management and Law: MBA, MSDMG (Master in Development Management and Governance), BBS, '
            'LL.B. and a PhD in Management. Social Sciences and Education: BA, B.Ed. (one year), MES, MMCS, a diploma (DLIM) and MPhil streams in '
            'English, Mathematics, Nepali and Health education, Education Studies, Economics, English, Sociology, Anthropology and Political Science. '
            'Science, Health and Technology: M.Phil. in ICT and Master in e-Governance on the programme table, with syllabus files for BIT, MIT, M.Sc. '
            'Environmental and Occupational Health, M.Sc. Natural Resource Development and Geoinformatics. Fees for the social sciences and education '
            'programmes are printed per credit: M.Phil. Rs 3,360, MES Rs 1,200, MMCS Rs 1,000, BA Rs 600, B.Ed. Rs 1,000 and DLIM Rs 680, plus a one-time '
            'admission fee (Rs 2,000, DLIM Rs 1,000), Rs 1,500 library a year and Rs 1,000 to 3,000 a semester exam fee. The entrance form fee is Rs 1,200 '
            'for MBA, Rs 1,000 for MSDMG and LL.B. and Rs 300 for BBS. The pages give no seat counts or total cost.')
NOU_ROUTES = ['ba', 'bed', 'bbs', 'llb', 'mba']
