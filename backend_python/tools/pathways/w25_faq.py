"""Wave 25 FAQs (fw25-1 to fw25-8), each tied to a source named in the answer."""
FWU = 'the FWU Faculty of Education campus table (facultyeducation.fwu.edu.np) and the FWU campus pages'
MU = 'the Mid-West University LMS and the MU 2083/84 bachelor admission notice'
EC = 'the European Commission EU Immigration Portal'

FAQ_ADD = [
    {'id': 'fw25-1', 'topic': 'after12', 'q': 'How many constituent campuses does Far-Western University have, and where are they?',
     'a': f'FWU lists 15 constituent campuses on its campus page and the Faculty of Education table adds Durgalaxmi Multiple Campus (Attariya, Kailali). They are Central (Mahendranagar), Tikapur and Kailali Multiple (Kailali), Durgalaxmi (Kailali), Triveni (Dadeldhura), Ghanteshwar Seti Mahakali and Sitaram (Doti), Darchula and Gokuleshwor (Darchula), Bajura and Badimalika (Bajura), Jayaprithivi (Bajhang), Janata (Achham), and Manilek, Patan and Jagannath (Baitadi) (source: {FWU}).', 'go': ['bed', 'bbs']},
    {'id': 'fw25-2', 'topic': 'after12', 'q': 'Where can I study B.Ed. in the far west of Nepal?',
     'a': f'FWU lists B.Ed. at its central department in Mahendranagar and at Badimalika, Bajura, Darchula, Durgalaxmi, Ghanteshwar Seti Mahakali, Gokuleshwor, Jagannath, Janata, Jayaprithivi, Kailali, Manilek, Patan, Sitaram, Tikapur and Triveni campuses (source: {FWU}). Ask each campus for current fees and intake.', 'go': ['bed']},
    {'id': 'fw25-3', 'topic': 'afterbach', 'q': 'Which Far-Western University campuses offer M.Ed.?',
     'a': f'The FWU Faculty of Education table gives M.Ed. at the central department, Bajura, Darchula, Durgalaxmi, Gokuleshwor, Jagannath, Janata, Jayaprithivi, Kailali and Tikapur campuses. Kailali and Tikapur also list PBEd, and the central department lists PBEd too (source: {FWU}).', 'go': ['med']},
    {'id': 'fw25-4', 'topic': 'after12', 'q': 'Is Patan Multiple Campus in Baitadi the same as Patan Campus in Lalitpur?',
     'a': f'No. Patan Multiple Campus in Baitadi is a Far-Western University constituent campus that the FWU Education table lists for B.Ed. Patan Campus in Lalitpur is a Tribhuvan University campus in Kathmandu valley (source: {FWU}).', 'go': ['bed']},
    {'id': 'fw25-5', 'topic': 'after12', 'q': 'Which Mid-West University campuses are in Surkhet and Banke?',
     'a': f'Mid-West University has its central schools at Birendranagar, Surkhet, plus constituent campuses including Bheri Multiple (Gumi) and Vidhyapur Janata (Bidhyapur-4) in Surkhet, and Bageshwari Multiple Campus in Kohalpur, Banke. Others are Narayan (Dailekh), Tila Karnali (Kalikot), Rara (Mugu), Musikot Khalanga (West Rukum), Bheri Gyanodaya (Jajarkot), Babai (Bardiya) and Jaljala (Rolpa) (source: {MU}).', 'go': ['bbs', 'bed']},
    {'id': 'fw25-6', 'topic': 'abroad', 'q': 'Can I work after studies in Spain, Hungary, Romania and Cyprus?',
     'a': f'Spain gives a 12 month job searching residence permit after you complete studies. Romania extends residence by 9 months after graduation to look for a job. Cyprus gives one year, but only to master or PhD graduates. Hungary lets graduates apply for a permit to look for a job or start a business without stating the duration on the page (source: {EC}, student page of each country).', 'go': []},
    {'id': 'fw25-7', 'topic': 'abroad', 'q': 'How many hours can a student work in Hungary?',
     'a': f'Two official sources differ. {EC} says up to 30 hours a week in the study period and full time for up to 90 days a year outside it. The Study in Hungary FAQ says 24 hours a week in term and up to 90 days or 66 working days outside term. Plan with 24 hours and confirm with your university career office.', 'go': []},
    {'id': 'fw25-8', 'topic': 'abroad', 'q': 'Do students in Estonia and Norway have a working hour limit?',
     'a': f'Estonia has no weekly hour limit for students at higher education institutions as long as work does not interfere with studies ({EC}, Estonia page). Norway lets a study permit holder work up to 20 hours a week, including remote work, and full time during holidays (UDI study permit page).', 'go': []},
]
