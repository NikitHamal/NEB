"""Wave 12, part 4: MBBS destinations (Kyrgyzstan, Kazakhstan, Philippines), the TU 2083 entrance round and 5 FAQs.

Keys owned: abroad_more, route_exam, faq_more (in wave12.json). Sources: studyabroadfromnepal.com MBBS cost comparison (total tuition for the
course, living per year, read 2026; approximate), TU Faculty of Management CMAT notice of Ashadh 1, 2083, and the TU entrance schedule 2083
(BCA, BIT and BSc CSIT dates and fees as published by the faculties and collected by nacolnist.edu.np and collegenp.com).
Run: python3 backend_python/tools/pathways/w12_more.py
"""
import json
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave12.json'
w = json.loads(FILE.read_text('utf-8')) if FILE.exists() else {}

REC = ('Check that the exact university is recognised by the Nepal Medical Council before you pay, and plan to pass the NMC licensing '
       'examination (NMCLE) after you return. Figures are approximate and the guide says to confirm fees in writing.')
w['abroad_more'] = [
    {'id': 'kg', 'country': 'Kyrgyzstan', 'tuition': [400000, 700000], 'living': [150000, 300000],
     'exams': ['NEB +2 Science with Physics, Chemistry and Biology', 'University admission process'], 'intakes': 'Mostly September',
     'fields': ['Medicine (5 years and 1 year internship)'], 'work': 'Not checked yet. Confirm with the university.',
     'note': 'Among the cheapest MBBS countries for Nepali students: about NPR 20 to 35 lakh for the whole course. Quality varies widely between institutions. ' + REC,
     'scholarships': [], 'code': 'KG'},
    {'id': 'kz', 'country': 'Kazakhstan', 'tuition': [500000, 900000], 'living': [200000, 350000],
     'exams': ['NEB +2 Science with Physics, Chemistry and Biology', 'University admission process'], 'intakes': 'Mostly September',
     'fields': ['Medicine (5 years and 1 year internship)'], 'work': 'Not checked yet. Confirm with the university.',
     'note': 'About NPR 25 to 45 lakh for the whole MBBS course. Quality varies widely between institutions. ' + REC,
     'scholarships': [], 'code': 'KZ'},
    {'id': 'ph', 'country': 'Philippines', 'tuition': [500000, 850000], 'living': [250000, 450000],
     'exams': ['NEB +2 Science', 'NMAT or the school test for the MD stage'], 'intakes': 'Usually June or August',
     'fields': ['Medicine (a pre-medical bachelor, then a 4 year Doctor of Medicine)'], 'work': 'Not checked yet. Confirm with the university.',
     'note': 'A US style route: a pre-medical bachelor (often BS Biology) first, then four years of MD, taught in English, about NPR 30 to 50 lakh in all. ' + REC,
     'scholarships': [], 'code': 'PH'},
]

w['route_exam'] = {
    'bca': 'TU FoHSS BCA entrance. 2083 round: forms from 29 June (Asadh 15) to 5 August 2026 (Rs 1,500), test 16 August 2026',
    'bit': 'TU IoST BIT entrance. 2083 round: forms from 25 July to 7 August 2026 (Rs 1,850), test 15 August 2026',
    'bsc-csit': 'TU IoST BSc CSIT entrance. 2083 round: forms from 22 July to 1 August 2026 (Rs 1,950), test 9 August 2026',
    'bba': 'TU CMAT. 2083 round: forms 15 June to 4 August 2026 (Rs 1,000), test 8 August 2026 at 8:00 AM',
    'bbm': 'TU CMAT. 2083 round: forms 15 June to 4 August 2026 (Rs 1,000), test 8 August 2026 at 8:00 AM',
    'bhm': 'TU CMAT. 2083 round: forms 15 June to 4 August 2026 (Rs 1,000), test 8 August 2026 at 8:00 AM',
    'bttm': 'TU CMAT. 2083 round: forms 15 June to 4 August 2026 (Rs 1,000), test 8 August 2026 at 8:00 AM',
    'bpa': 'TU CMAT. 2083 round: forms 15 June to 4 August 2026 (Rs 1,000), test 8 August 2026 at 8:00 AM',
    'bim': 'TU CMAT (BITM). 2083 round: forms 15 June to 4 August 2026 (Rs 1,000), test 8 August 2026 at 8:00 AM',
}

F = [
    ('after12', 'When were the TU entrance exams for 2083/84?', ['bsc-csit', 'bca', 'bit', 'bba'],
     'TU ran them close together in 2026. CMAT (BBA, BBM, BITM, BPA, BHM, BTTM, BBA-F, BMS): forms 15 June to 4 August, fee Rs 1,000, test 8 August at 8:00 AM. BSc CSIT: forms 22 July to 1 August (double fee to 5 August), Rs 1,950, test 9 August. BIT: forms 25 July to 7 August, Rs 1,850, test 15 August. BCA: forms 29 June to 5 August, Rs 1,500, test 16 August. All tests start at 8:00 AM and fees are not refunded, so confirm your eligibility first.'),
    ('after12', 'Who can sit CMAT and do I need Management in +2?', ['bba', 'bbm', 'bhm'],
     'No. Any stream (Management, Science or Humanities) can apply for BBA, BBM, BITM, BPA, BHM, BTTM and BBA-F. The 2083 notice asked for a pass in Grade 11 and 12 with at least D in theory and C in practical in each subject and CGPA 1.8, or second division. You apply online and the campus you choose must verify the form in person before the deadline (3:00 PM on 5 August 2026 in the 2083 round).'),
    ('abroad', 'Which countries are the cheapest for MBBS and what is the catch?', ['mbbs'],
     'Planning ranges for the whole course: Kyrgyzstan NPR 20 to 35 lakh, Kazakhstan 25 to 45 lakh, China 30 to 55 lakh, the Philippines 30 to 50 lakh (pre-med plus 4 year MD), Russia 35 to 60 lakh, Georgia 35 to 65 lakh and Bangladesh 40 to 70 lakh. Living costs add NPR 1.5 to 5 lakh a year. The catch is recognition: only colleges recognised by the Nepal Medical Council lead to a licence, and you still sit the NMCLE at home. Quality differs a lot inside Kyrgyzstan and Kazakhstan.'),
    ('abroad', 'What is the Philippines MD route?', ['mbbs'],
     'The Philippines follows a US system. You first finish a pre-medical bachelor (often BS Biology), then a four year Doctor of Medicine taught in English. Budget about NPR 30 to 50 lakh in all, plus NPR 2.5 to 4.5 lakh a year for living, and include the pre-med years in the plan. As elsewhere, only a Nepal Medical Council recognised school gives you a path to a licence.'),
]
w['faq_more'] = [{'id': f'fw12-m{i}', 'topic': t, 'q': q, 'go': g, 'a': a} for i, (t, q, g, a) in enumerate(F, 1)]

FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(len(w['abroad_more']), len(w['route_exam']), len(w['faq_more']))
