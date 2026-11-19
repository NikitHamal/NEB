"""Wave 30 FAQs. Each answer names the page it was read from (19 Nov 2026)."""
from w30_sites import WEBSITES

FAQ_ADD = [
    {'id': 'fw30-1', 'topic': 'after10', 'q': 'How do I get a free Class 11 and 12 seat in Kathmandu Metropolitan City?',
     'a': ('Kathmandu Metropolitan City runs a scholarship exam for SEE graduates who want a free seat in an institutional school inside the city (notice for 2083, entrance.kathmandu.gov.np). '
           'The form was open from Jestha 1 to 10 and was free. You pick one subject (Science, Management, Humanities, Education or Law) and rank every school you would accept. '
           'The exam has 100 multiple choice questions on the Class 10 syllabus (maths 30, science 30, social 20, English 10, Nepali 10) in two hours, with a 40 percent pass mark and no negative marking. '
           'Seats are filled by merit: 35 percent community school students, 10 percent institutional school students, 19 percent city residents and 1 percent landfill area residents, and the rest is reserved for women, Janajati, Khas Arya, Madhesi, Dalit and other groups. '
           'Do not take admission anywhere before the result, because schools need not refund an earlier fee. Helpline 16600105511 or 1180.'),
     'go': ['plus2-science', 'plus2-management']},
    {'id': 'fw30-2', 'topic': 'after12', 'q': 'Is there a provincial government scholarship for Kathmandu University?',
     'a': ('Yes. Each province gives Kathmandu University tuition scholarships to its own residents, one student per programme, in July. The 2083 windows were Madhesh 2 to 22 July, Bagmati 2 to 16 July, Gandaki 10 to 30 July, Koshi 13 to 23 July and Lumbini 15 to 28 July (Edusanjal). '
           'The Madhesh list had six programmes: BE Mining, Chemical and Environmental Engineering, Health Informatics, BSc Environmental Science and BSc Agriculture, only for Science +2 graduates. Marks out of 100: GPA up to 60, hardship letter 10, community school up to 10, interview 20. '
           'It pays tuition only, so budget for the other fees. Watch the notice of your own province every June and July.'),
     'go': ['bsc-agri', 'bsc-environment']},
    {'id': 'fw30-3', 'topic': 'after12', 'q': 'What can I study at Mid-West University in Surkhet and its campuses?',
     'a': ('The 2083/84 bachelor admission notice (as printed on collegenp.com, 19 Nov 2026) lists: BA in English, International Relations, Journalism, Mathematics, Nepali, Sociology, Social Work, Economics and Rural Development; BBS; B.Ed. in seven subjects; BSc CSIT, BIT, BSc Environment and BSc biology and physical groups; BE Computer, Civil and Hydropower at Sano Surkhet; BSc Agriculture at Ramghat; and BA LL.B. '
           'Ten constituent campuses teach mostly BBS, B.Ed. and BA: Babai (Gulariya), Bageshwari (Kohalpur, with BSc and BBA), Bheri Gyanodaya (Jajarkot), Bheri (Gumi, Surkhet), Jaljala (Rolpa), Musikot Khalanga (Rukum), Narayan (Dailekh), Rara (Mugu), Tila Karnali (Kalikot) and Vidhyapur Janata (Surkhet). Rara and Tila Karnali list B.Ed. only. '
           'Global College International in Mid-Baneshwor, Kathmandu is the one affiliated college and runs BBA, BHM and BTTM. The notice gives phone numbers but no seats or fees.'),
     'go': ['bed', 'bbs', 'be-computer', 'bsc-csit', 'ba-llb']},
    {'id': 'fw30-4', 'topic': 'after12', 'q': 'How many Pokhara University scholarship seats were there in 2083 and how do I apply?',
     'a': ('The Pokhara University notice for 2083 lists 1,381 quotas: Science and Technology 558 (BE Civil 183, BE Computer 107, BCA 65, BE IT 53, B.Arch 39, BE Software 29, BICE 15), Management 777 (BBA 419, BBA Finance 104, BCSIT 94, BHM 115, BHCM 40, BTTM 5) and Humanities 46. '
           'The form ran from 9 to 28 June 2026 on scholarship.pu.edu.np and the 3 hour written exam was held in Pokhara. Another guide prints 1,328 seats; the notice figure is used here. 80 percent of seats go to community school SEE graduates. A scholarship waives tuition at the constituent or affiliated college you are placed in, so keep the grades the renewal rule asks for.'),
     'go': ['be-civil', 'bba', 'be-computer']},
    {'id': 'fw30-5', 'topic': 'after10', 'q': 'How many free CTEVT diploma seats does each province have?',
     'a': ('The CTEVT classified scholarship notice for 2083/84 lists 3,417 seats in 34 programmes (collegenp.com, Edusanjal): Bagmati 838, Madhesh 670, Koshi 609, Lumbini 604, Gandaki 264, Sudurpashchim 222 and Karnali 210. '
           'Civil Engineering alone has 640 seats and Nursing 189. Half the seats are for the general group and half for women, Dalit, Janajati, Khas Arya, Madhesi, Tharu, Muslim, remote area, disability and martyr family groups. '
           'You file one programme in one province, so pick the province where your SEE school is or where the seats are widest. Recipients agree to serve where the government posts them, and you cannot apply twice.'),
     'go': ['dip-civil-eng', 'pcl-nursing', 'dip-computer-eng']},
    {'id': 'fw30-6', 'topic': 'after10', 'q': 'Which private or NGO scholarships can I try after SEE?',
     'a': ('The Ncell SEE Scholarship supports 100 SEE graduates of 2082 through Class 11 and 12, with 12 months of free data and voice, and Project Shikshya adds 50 more. Candidates sit written exams and interviews in all seven provinces (announced 19 May 2026). '
           'HELP (Helambu Education and Livelihood Partnership) funds government school graduates with GPA 2.8 in science or 2.4 in management and has helped over 600 students; its bachelor scholarship is open only to former HELP scholars and pays NPR 550,000 over the course (a guide figure) for two students a year. '
           'Never pay an agent for a scholarship place: real programmes do not charge to apply.'),
     'go': ['plus2-science', 'plus2-management']},
    {'id': 'fw30-7', 'topic': 'general', 'q': 'How did you check the college websites you added?',
     'a': (f'A script built candidate addresses from each college name, kept only those that answer over valid HTTPS, and accepted a page only when its title or first screen names the college and the page mentions the district or town. '
           f'A person then read each result: {len(WEBSITES)} colleges got a website in wave 30, while pages for sale, ministry or hospital sites with similar names, shared sites for two colleges and a placeholder page were rejected. '
           'A name match is still not proof, so confirm the college and its affiliation with the university before you pay a fee.'),
     'go': []},
    {'id': 'fw30-8', 'topic': 'after12', 'q': 'Are there scholarships at Far Western University and Nepal Open University?',
     'a': ('Far Western University keeps scholarship seats equal to 10 percent of the approved seats of BSc CSIT and BBA at its affiliated campuses. In 2083 the exam moved to 2083/05/14 and the form deadline to 2083/05/13 because too few students had applied (notice of 2083/05/02, fwu.edu.np/scholarship). '
           'Nepal Open University took scholarship forms for MBA, MS in Development Management and Governance, BBS and LL.B. from 26 June to 16 July 2026 on its Student Panel. Dates change every year, so check the university notice board in Asar and Shrawan.'),
     'go': ['bbs', 'bba', 'llb']},
]
