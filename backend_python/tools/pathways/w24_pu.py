"""Wave 24: Pokhara University affiliated colleges, read from the official pu.edu.np college lists on 18 November 2026.

Sources: https://pu.edu.np/schools-and-colleges/affiliated-colleges/ (58 affiliated colleges with address), and the faculty lists
https://pu.edu.np/academics/faculties/fms/colleges/ (Management Studies), .../fst/schools-colleges/ (Science and Technology),
.../fhs/schools-colleges/ (Health Sciences), .../fhss/schools-colleges/ (Humanities and Social Sciences).
Programmes are only listed when the college's own website (opened live, title checked) names them; otherwise the note says the
college is on the PU faculty list and asks the student to confirm the intake.
"""

FAC = {
    'FMS': 'Faculty of Management Studies',
    'FST': 'Faculty of Science and Technology',
    'FHS': 'Faculty of Health Sciences',
    'FHSS': 'Faculty of Humanities and Social Sciences',
}

# (suffix, name, district, place, website or None, faculties, programmes seen on the college website, route ids to link)
ROWS = [
    ('schems', 'School of Environmental Science and Management (SchEMS)', 'Kathmandu', 'Devkota Sadak, Mid Baneshwor', None, ['FMS', 'FST'], None, []),
    ('brihaspati', 'Brihaspati College', 'Rupandehi', 'Goligadh-9, Siddharthanagar, Bhairahawa', None, ['FMS'], None, ['bba']),
    ('pokhara-mgmt', 'Pokhara College of Management', 'Kaski', 'Gyanmarg, Nadipur, Pokhara-3', None, ['FMS'], None, ['bba']),
    ('vs-niketan', 'V.S. Niketan College', 'Kathmandu', 'Minbhawan', 'https://vsniketan.edu.np', ['FMS'], 'BBA', ['bba']),
    ('la-grandee', 'LA Grandee International College', 'Kaski', 'Simalchour-8, Pokhara', 'https://lagrandee.edu.np', ['FMS'], 'BBA and BPH', ['bba', 'bph']),
    ('brixton', 'Brixton College', 'Kanchanpur', 'BDN 6, Aithpur', None, ['FMS'], None, ['bba']),
    ('excel-business', 'Excel Business College', 'Kathmandu', 'Lakhechaur Marg, Thapagaun, New Baneshwor', None, ['FMS'], None, ['bba']),
    ('atlantic', 'Atlantic International College', 'Kathmandu', 'Galkopakha, Thamel', 'https://atlantic.edu.np', ['FMS'], 'BBA, BBA-BI, BBA-Finance and MBA', ['bba', 'bba-bi', 'mba']),
    ('axis', 'Axis College', 'Rupandehi', 'Tilottama-3, Janakinagar', None, ['FMS'], None, ['bba']),
    ('liberty', 'Liberty College', 'Kathmandu', 'Anamnagar', 'https://libertycollege.edu.np', ['FMS'], 'BBA, BBA-F, BCSIT and BHM', ['bba', 'bhm']),
    ('siddhartha-intl', 'Siddhartha International College', 'Rupandehi', 'Kalika Path, Butwal-9', None, ['FMS'], None, ['bba']),
    ('camad', 'Camad College', 'Kathmandu', 'Sukedhara (Ring Road)', None, ['FMS', 'FHSS'], None, ['bba']),
    ('citizen', 'Citizen College', 'Lalitpur', 'Satdobato, next to the swimming pool', None, ['FMS'], None, ['bba']),
    ('saim', 'SAIM College', 'Kathmandu', 'Devkota Sadak, Old Baneshwor', 'https://saim.edu.np', ['FMS'], 'BBA, BCSIT and MBA', ['bba', 'mba']),
    ('kshitiz-intl', 'Kshitiz International College', 'Rupandehi', 'Kalikanagar, Butwal-10', None, ['FMS'], None, ['bba']),
    ('quest', 'Quest International College', 'Lalitpur', 'Gwarko Chowk', 'https://quest.edu.np', ['FMS'], 'BBA, BHM, BCSIT and MBA', ['bba', 'bhm', 'mba']),
    ('alpine', 'Alpine Management College', 'Banke', 'Nepalgunj-13, Surkhet Road', None, ['FMS'], None, ['bba']),
    ('platinum', 'Platinum Management College', 'Kathmandu', 'Kalikasthan, Dillibazar', None, ['FMS'], None, ['bba']),
    ('amity', 'Amity College', 'Kanchanpur', 'Mahendranagar-6', 'https://www.amitycollege.edu.np', ['FMS'], 'BBA', ['bba']),
    ('victoria', 'Victoria International College', 'Dang', 'Ghorahi Sub-Metropolitan-15', None, ['FMS'], None, ['bba']),
    ('nwmec', 'Nepal Western Management and Engineering College', 'Kailali', 'Dhangadhi Municipality, Ward 2', None, ['FMS'], None, ['bba']),
    ('ritz', 'Ritz College of Engineering and Management', 'Lalitpur', 'Balkumari-9', 'https://ritzcollege.edu.np', ['FMS'], None, ['bba']),
    ('srds', 'Sahid Ramnath Dahal Smriti College', 'Kathmandu', 'Balaju Chowk', None, ['FMS'], None, ['bba']),
    ('boston', 'Boston International College', 'Chitwan', 'Hakim Chowk, Bharatpur-10', None, ['FMS'], None, ['bba']),
    ('butwal-model', 'Butwal Model College', 'Rupandehi', 'Padsari-8, Kataiya', 'https://butwalmodel.edu.np', ['FMS', 'FHSS'], 'BBA, BHM and MBA', ['bba', 'bhm', 'mba']),
    ('apollo', 'Apollo International College', 'Kathmandu', 'Lakhechaur Marga, Mid Baneshwor', None, ['FMS'], None, ['bba']),
    ('rajdhani', 'Rajdhani Model College', 'Kathmandu', 'Devkota Sadak, Pipalbot, Old Baneshwor', None, ['FMS'], None, ['bba']),
    ('atharva', 'Atharva Business College', 'Kathmandu', 'Bansbari', 'https://atharvacollege.edu.np', ['FMS'], None, ['bba']),
    ('shubhashree', 'Shubhashree College of Management', 'Kathmandu', 'Kanti Marga, New Baneshwor', 'https://shubhashreecollege.edu.np', ['FMS'], 'BBA, BCSIT and BHM', ['bba', 'bhm']),
    ('medhavi', 'Medhavi College', 'Kathmandu', 'Shankhamul', 'https://medhavicollege.edu.np', ['FMS'], 'BBA, BCSIT, BHM, MBA and MCSIT', ['bba', 'bhm', 'mba']),
    ('valley-state', 'Valley State College', 'Chitwan', 'Bharatpur-9, Basanta Chowk', None, ['FMS'], None, ['bba']),
    ('imperial', 'Imperial Business College', 'Kathmandu', 'Hattisar, Kamaladi (the all-college list says Thapagaun, New Baneshwor)', None, ['FMS'], None, ['bba']),
    ('central-college', 'Central College', 'Kathmandu', 'Sinamangal-9', None, ['FMS'], None, ['bba']),
    ('cem-nepalgunj', 'College of Engineering and Management, Nepalgunj', 'Banke', 'Nepalgunj-13, Sheetalnagar', None, ['FST'], None, []),
    ('mbman', 'Madan Bhandari Memorial Academy Nepal', 'Morang', 'Urlabari-3, Mangalbare', None, ['FST'], None, []),
    ('iacer', 'Institute of Advance Communication Education and Research Center', 'Kathmandu', 'Baneshwor Heights, Tanka Prasad Marg', None, ['FHSS'], None, []),
]

PROVIDERS_ADD = []
WHERE_ADD = {}
for suf, name, dist, place, site, facs, progs, routes in ROWS:
    pid = 'p-w24-pu-' + suf
    fac = ' and '.join(FAC[f] for f in facs)
    note = ('Pokhara University affiliated college at ' + place + ', listed by pu.edu.np under its ' + fac + ' (checked 18 Nov 2026). ')
    if progs:
        note += 'The college website names ' + progs + '. Confirm the current intake and fee with the college.'
    else:
        note += 'The programme list differs by college, so confirm the intake and fee with the college before applying.'
    p = {'id': pid, 'name': name, 'kind': 'College', 'sector': 'Private', 'district': dist, 'place': place.split(' (')[0], 'note': note}
    if site:
        p['website'] = site
    PROVIDERS_ADD.append(p)
    for r in routes:
        WHERE_ADD.setdefault(r, []).append(pid)

# existing providers whose own websites name the programme (opened live on 18 Nov 2026)
WHERE_EXISTING = {
    'bba': ['p-uniglobe'],
    'mba': ['p-uniglobe'],
}
PU_FACULTY_NOTE = {
    'p-nec': 'Listed by pu.edu.np under its Faculty of Science and Technology.',
    'p-gces': 'Listed by pu.edu.np under its Faculty of Science and Technology.',
    'p-pec': 'Listed by pu.edu.np under its Faculty of Science and Technology.',
    'p-universal': 'Listed by pu.edu.np under its Faculties of Science and Technology, Management Studies and Health Sciences.',
    'p-crimson': 'Listed by pu.edu.np under its Faculties of Science and Technology, Management Studies and Health Sciences.',
    'p-cosmos': 'Listed by pu.edu.np under its Faculties of Science and Technology and Management Studies.',
}
