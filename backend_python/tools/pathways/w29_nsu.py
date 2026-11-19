"""Wave 29: Nepal Sanskrit University constituent and affiliated Vidyapeeths (campuses), 11 new rows.

nsu.edu.np did not answer from the sandbox on 19 Nov 2026 (the same note as wave 28), so the list is the one four independent
aggregators print identically: collegenp.com "List of NSU affiliated colleges" (address and phone), Edusanjal (affiliation page,
Nepal Sanskrit University), Justapedia and Falano College. Every row below appears in at least three of them. Programmes are not
printed per campus there, so each note says to confirm the intake; nothing here claims seats or fees.
Already in the dataset and left alone: p-valmiki (Balmiki, Kathmandu), p-ruru-gulmi (Ruru, Gulmi), p-kendriya-ayurveda (Central
Ayurved, Beljhundi), p-w26-npca-137 (Radha Damodar, Syangja).
"""
CK = 'checked 19 Nov 2026'
# id, name, district, place, phone (collegenp), note extra
ROWS = [
    ('p-w29-nsu-pindeshwor', 'Pindeshwor Sanskrit Vidyapeeth (Pindeshwor College)', 'Sunsari', 'Dharan', '025-529285', ''),
    ('p-w29-nsu-janata', 'Janata Sanskrit Vidyapeeth (Janata College)', 'Dang', 'Bijauri, Tulsipur', '082-411016', 'One aggregator also tags it as a CTEVT linked school.'),
    ('p-w29-nsu-vishwa-vidyalaya', 'Vishwa Vidyalaya Vidyapeeth (University Vidyapeeth)', 'Dang', 'Beljhundi, Tulsipur', '082-500022', 'It is at the university central office site.'),
    ('p-w29-nsu-kalika', 'Kalika Sanskrit Vidyapeeth', 'Nawalparasi East', 'Gaidakot', '078-502252', 'Lists give the district as Nawalpur or Nawalparasi.'),
    ('p-w29-nsu-harihar', 'Harihar Sanskrit Vidyapeeth', 'Arghakhanchi', 'Khidim', '077-690549', ''),
    ('p-w29-nsu-sharada', 'Sharada Sanskrit Vidyapeeth (Sharada College)', 'Kanchanpur', 'Mahendranagar', '099-521061', 'It is not the community Sharada Campus in Salyan.'),
    ('p-w29-nsu-bp-koirala', 'B. P. Koirala Sanskrit Vidyapeeth', 'Solukhumbu', 'Salleri', '038-690149', ''),
    ('p-w29-nsu-bhanu', 'Bhanu Sanskrit Vidyapeeth', 'Tanahu', 'Chudi', '065-690581', 'It is not Aadikavi Bhanubhakta Campus.'),
    ('p-w29-nsu-bindabasini', 'Bindabasini Sanskrit Vidyapeeth', 'Kaski', 'Bhimkali, Pokhara', '061-523352', ''),
    ('p-w29-nsu-yalana', 'Yagyavalkya Laxminarayan (Ya.La.) Sanskrit Vidyapeeth', 'Mahottari', 'Matihani', '044-540132', ''),
    ('p-w29-nsu-janak-hajari', 'Janak Hajari Sanskrit Vidyapeeth', 'Dhanusha', 'Janakpurdham', '041-520665', ''),
]
ROUTES = ['sanskrit-gurukul']
NOTE_ADD = {
    'p-valmiki': f'Also on the Nepal Sanskrit University affiliated campus list ({CK}; collegenp.com, Edusanjal), phone 01-4227193, Pardashani Marg.',
    'p-ruru-gulmi': f'Nepal Sanskrit University lists its Ruru Sanskrit College at Ridi, Rurukshetra, phone 079-400032 ({CK}; collegenp.com, Edusanjal).',
    'p-kendriya-ayurveda': f'Nepal Sanskrit University lists Central Ayurved College at Beljhundi, phone 082-423062 ({CK}; collegenp.com); Edusanjal places it at Bijauri, Tulsipur.',
    'p-w26-npca-137': f'Also on the Nepal Sanskrit University list as Radha Damodar Sanskrit Vidyapeeth, Keladighat, Chapakot ({CK}; Edusanjal, Gurubaa Learn).',
}
NSU_NOTE = (f'Nepal Sanskrit University (central office Beljhundi, phone 082-400057 and 082-400010, nsu.edu.np) is reported to have 12 constituent and 13 '
            f'affiliated Vidyapeeths. nsu.edu.np did not answer on 19 Nov 2026, so the campus rows come from collegenp.com, Edusanjal, Justapedia and Falano '
            'College, which print the same list; the university also names Mahesh Sanskrit Gurukulam and Paramananda Sanskrit Gurukul (Devghat, Tanahu) and Saraswati Sanskrit Vidyapeeth '
            '(Manigram, Rupandehi) on older lists, and some private Ayurveda colleges, which are not rows here because only one source named them.')
