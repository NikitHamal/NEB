"""Wave 29 FAQs. Numbers are recomputed from lbu_courses.json and the wave 29 modules."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_courses = json.loads((HERE / 'lbu_courses.json').read_text(encoding='utf-8'))
_n = len(_courses)
FAQ_ADD = [
    {'id': 'fw29-1', 'topic': 'after12', 'q': 'Which colleges teach Buddhist studies and Sowa Rigpa in Nepal?',
     'a': (f'Lumbini Buddhist University lists {_n} programmes on lbu.edu.np (19 Nov 2026). The Central Campus in Lumbini runs the Ph.D. in Buddhist Studies, MA in Buddhism and Nepal Studies, '
           'MA in Bhot Buddhist Studies, MA in Archaeology and Buddhist Archaeological Sites, Bachelor of Buddhism and Social Work and BA in Rural Development. '
           'Affiliated colleges in the Kathmandu valley teach single masters: Sugata Buddhist College (Mahayana), Theravada Buddhist Academy (Theravada and Pali), '
           'Lotus Buddhist Academic College (Buddhist Studies, Applied Buddhism), Boudha Multiple Campus (Buddhism and Peace Studies) and Lumbini College of Buddhism '
           'and Himalayan Studies. Sowa Rigpa International College near Boudhanath offers the Bachelor of Sowa Rigpa Medicine and Surgery (120 credits).'),
     'go': ['ma', 'bfa']},
    {'id': 'fw29-2', 'topic': 'after12', 'q': 'Can I study hospitality, tourism or law in Butwal or Tulsipur with a public university degree?',
     'a': ('Yes, through Lumbini Buddhist University. Its City Campus Butwal lists BBA, BTTM, BHTM, BA LL.B., BTCSOL (Chinese teaching) and an MBA in Hospitality Management, and '
           'Tulsipur Metro College lists BBA, BHTM and BA LL.B. (lbu.edu.np, 19 Nov 2026). The pages give credits (120 for the bachelor programmes, 220.5 for BA LL.B.) but no fee or seat '
           'count, so ask each college for the current fee and intake.'),
     'go': ['bttm', 'bhm', 'ba-llb']},
    {'id': 'fw29-3', 'topic': 'after12', 'q': 'How much does Nepal Open University cost per credit?',
     'a': ('The Nepal Open University faculty page for Social Sciences and Education (nou.edu.np, 19 Nov 2026) prints tuition per credit: M.Phil. Rs 3,360, MES Rs 1,200, MMCS Rs 1,000, '
           'BA Rs 600, B.Ed. (one year) Rs 1,000 and the DLIM diploma Rs 680. Add a one-time admission fee (Rs 2,000, DLIM Rs 1,000), Rs 1,500 library fee a year and Rs 1,000 to 3,000 as the '
           'exam fee each semester. The entrance form costs Rs 1,200 for MBA, Rs 1,000 for MSDMG and LL.B. and Rs 300 for BBS. The Management and Law and Science pages print no tuition.'),
     'go': ['ba', 'bed', 'bbs']},
    {'id': 'fw29-4', 'topic': 'after12', 'q': 'Where can I study Sanskrit (Shastri and Acharya) in Nepal?',
     'a': ('Nepal Sanskrit University has its central office at Beljhundi, Dang, and its constituent and affiliated Vidyapeeths are spread across the country: Dharan (Pindeshwor), Salleri (B. P. Koirala), '
           'Janakpurdham (Janak Hajari), Matihani (Ya.La.), Kathmandu (Valmiki), Chudi (Bhanu), Gaidakot (Kalika), Pokhara (Bindabasini), Bijauri and Beljhundi in Dang, Khidim (Harihar), Ridi (Ruru), '
           'Keladighat (Radha Damodar) and Mahendranagar (Sharada). The university site did not answer on 19 Nov 2026, so the list comes from four aggregators that agree; ask the campus which '
           'programmes and intake it has this year.'),
     'go': ['sanskrit-gurukul', 'ba']},
    {'id': 'fw29-5', 'topic': 'abroad', 'q': 'How many hours can I work as a student in Sweden now?',
     'a': ('Since 11 June 2026 a higher education student on a new or extended permit may work at most 15 hours a week during term, with no limit in June, July and August, according to '
           'Migrationsverket as reported by KPMG and The Scholars Dream (19 Nov 2026). Permits granted before that date keep the old rules until their next extension. To extend you also need '
           '37.5 credits in the first year and 45 a year after. After a bachelor or master you can get a 12 month permit to look for work (12 to 18 months after a doctorate).'),
     'go': ['abroad-ms']},
    {'id': 'fw29-6', 'topic': 'abroad', 'q': 'Can I work or stay after graduating in Georgia, Kazakhstan, Kyrgyzstan, Uzbekistan or the Philippines?',
     'a': ('None of the five has a post-study job search permit that two or more sources agree on (read 19 Nov 2026). Kyrgyzstan (KSMA via studycountry.com) and the Philippines (Bureau of Immigration visa list) '
           'say a student visa gives no work right and a graduate needs an employer sponsored work permit; Uzbekistan and Kazakhstan guides say a work permit and an employer are needed too. For Georgia the guides disagree (one describes a 1 year permit). Plan your budget without student wages and check with the migration office.'),
     'go': ['abroad-ms']},
]
