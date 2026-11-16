"""Wave 12, part 2: three destinations (Czechia, Georgia, Bangladesh) and scholarships (Czech Government, NAWA Poland,
CTEVT special 2083/84 plus a rewrite of the CTEVT classified entry) into wave12.json (idempotent, owns its keys).

Sources: study-abroad.org (Czech costs 2026), edunepal.com (Czech visa route), studyabroadfromnepal.com (MBBS abroad, Georgia and
Bangladesh cost ranges; conversions near USD 1 = NPR 137), mbbs.bd (Bangladesh government seats 2025-26), Czech MEYS scholarship notice
2027/28 (call 21 Aug to 30 Sep 2026), NAWA call 2027 (20 May to 27 Jun 2026), CTEVT notices of 29 Baishakh and 2 Asar 2083 (via collegenp, edusanjal).
Run: python3 backend_python/tools/pathways/w12_abroad.py
"""
import json
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave12.json'
w = json.loads(FILE.read_text('utf-8')) if FILE.exists() else {}

w['abroad_add'] = [
    {'id': 'cz', 'country': 'Czechia', 'tuition': [0, 2500000], 'living': [1100000, 1800000],
     'exams': ['IELTS or an equal English test for English programmes', 'Czech at about B2 for free Czech taught programmes', 'University entrance test'],
     'intakes': 'Winter semester (September); some programmes take students in February',
     'fields': ['Engineering', 'Computer science', 'Medicine', 'Business'],
     'work': 'Not checked yet. Read the Ministry of the Interior (MV CR) rules for your permit before you count on part time work.',
     'note': ('Czech taught programmes at public universities are free for everyone; English taught ones cost CZK 100,000 to 400,000 a year '
              '(about NPR 6 to 24 lakh) and medicine about EUR 12,000 to 15,000. Living is CZK 15,000 to 25,000 a month. Visa fee CZK 2,500; '
              'the funds figure is about CZK 124,500 a year and changes. Nepali applicants book at the Czech Embassy in New Delhi. '
              'Foreign diplomas need recognition (nostrification).'),
     'scholarships': ['s-czech'], 'code': 'CZ', 'stay_back': '9 months to look for work after graduating on a job seeker permit'},
    {'id': 'ge', 'country': 'Georgia', 'tuition': [450000, 1100000], 'living': [350000, 650000],
     'exams': ['NEB +2 Science with Physics, Chemistry and Biology (about 50 percent) for medicine', 'English proficiency shown to the university'],
     'intakes': 'September and February', 'fields': ['Medicine (MD, 6 years)'],
     'work': 'Not checked yet. Confirm with the university before you plan any paid work.',
     'note': ('Mostly chosen for six year English medium MD programmes at about USD 4,000 to 8,000 a year (NPR 5.5 to 11 lakh), plus hostel '
              'NPR 1.5 to 3 lakh and living NPR 2 to 3.5 lakh a year. A Georgian MD counts for a licence in Nepal only if the Nepal Medical Council '
              'recognises that exact university, and you must pass the NMC licensing examination (NMCLE) after returning. Ask for recognition in writing first.'),
     'scholarships': [], 'code': 'GE'},
    {'id': 'bd', 'country': 'Bangladesh', 'tuition': [800000, 1400000], 'living': [150000, 300000],
     'exams': ['NEB +2 Science with Physics, Chemistry and Biology (about 50 percent or 2.4 GPA)', 'College admission test or interview'],
     'intakes': 'Usually once a year; each college sets its own dates', 'fields': ['Medicine (MBBS, 5 years and 1 year internship)', 'Dentistry'],
     'work': 'Not checked yet. Confirm with the college before you plan any paid work.',
     'note': ('Close to home, with seats set aside for Nepali students under the SAARC quota; government college seats are few and cheaper. '
              'A private MBBS costs about NPR 40 to 70 lakh in all. Bangladesh runs about 5,100 government MBBS seats in 37 colleges for its own students (2025-26). '
              'Check that the college is recognised by both BMDC and the Nepal Medical Council, then pass the NMCLE to practise in Nepal.'),
     'scholarships': [], 'code': 'BD'},
]

w['scholarships_add'] = [
    {'id': 's-czech', 'name': 'Czech Government Scholarship for developing countries', 'scope': 'abroad', 'levels': ['master', 'phd'],
     'by': 'Government of the Czech Republic (Ministry of Education and Ministry of Foreign Affairs)',
     'covers': 'Tuition, a monthly stipend of CZK 16,000 for a master and CZK 24,960 for a PhD, and health insurance; travel is not paid',
     'who': ('Citizens of a fixed list of countries only. The 2027-28 list named Bangladesh, Georgia, Ukraine, Cambodia, Ethiopia and others; '
             'Nepal was not on the lists read, so check the call before you spend time on it.'),
     'how': ('Online on the Study in Czechia portal with a motivation letter and the entrance tests; one application per person. '
             'The 2027-28 call ran from 21 August to 30 September 2026, then embassy checks until January 2027.'),
     'link': 'https://www.studyin.cz', 'country': 'cz', 'type': 'Government', 'open': [8, 9]},
    {'id': 's-nawa', 'name': 'NAWA Banach scholarship (Poland)', 'scope': 'abroad', 'levels': ['master'],
     'by': 'Polish National Agency for Academic Exchange (NAWA)',
     'covers': 'Tuition at public universities and a monthly scholarship set by each call (PLN 1,500 to 2,500 in recent calls)',
     'who': ('Citizens of listed countries only. The 2027 list in the source read had India, Indonesia, Vietnam and others and did not show Nepal, '
             'so confirm on nawa.gov.pl first.'),
     'how': 'You choose the Polish university and apply through the NAWA system. The 2027 call opened on 20 May and closed on 27 June 2026.',
     'link': 'https://nawa.gov.pl', 'country': 'pl', 'type': 'Government', 'open': [5, 6]},
    {'id': 's-ctevt-special', 'name': 'CTEVT special free scholarship (480 seats, 2083/84)', 'scope': 'nepal', 'levels': ['diploma'],
     'by': 'CTEVT', 'covers': ('Free study plus NPR 3,500 a month, NPR 1,500 a year for travel and NPR 2,500 a year for uniform; '
                              '457 diploma and 23 pre-diploma seats'),
     'who': ('Permanent residents who are Dalit, Muslim, poor, from the 22 listed indigenous groups, Haliya or Kamaiya, or from one of 78 local '
             'levels without technical education. SEE with GPA 2.0 for health and nursing, 1.6 for other programmes.'),
     'how': ('Free online form on ctevtexam.org.np (2083 Ashadh 4 to 18). Merit by SEE GPA, plus one mark for government or community school students, '
             'while institutional school marks count at 0.85.'),
     'link': 'https://ctevtexam.org.np', 'type': 'Government', 'open': [6, 7]},
]

w['scholarship_extra'] = {
    's-ctevt': {
        'covers': ('Free (classified) seats in diploma and PCL programmes at constituent, partnership and private institutes: 3,417 seats '
                   'in 34 programmes for 2083/84, half for the general group and half for target groups'),
        'who': ('SEE from a government or community school (or CTEVT pre-diploma) with GPA 2.0 for health programmes and 1.6 for others; '
                'women, Dalit, Janajati, Khas Arya, Madhesi, Tharu, Muslim, remote area and disability quotas apply. You may not have held a CTEVT scholarship before.'),
        'how': ('One programme in one province, filed on the ITMS online system (the 2083/84 form closed on Jestha 13). '
                'Seats per programme: Civil 640, General Medicine 446, Pharmacy 341, Agriculture Plant 261, Medical Laboratory 250. '
                'Schools may not charge scholarship students tuition, lab, registration or exam fees; recipients agree to serve where the government posts them.'),
        'open': [5, 6]},
}

FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print('abroad', len(w['abroad_add']), 'schol', len(w['scholarships_add']))
