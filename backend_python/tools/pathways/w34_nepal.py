"""Wave 34 Nepal side. Read on 2026-11-19.
CTEVT diploma and PCL classified scholarship: the full notice text of 2083/01/29 on collegenp.com (programme by province table, 3,417 grand total,
Rs 1,000 form, 2083/04/13 closing). The 34 programme totals add up to 3,414, three below the printed 3,417, so one row may be misprinted.
CTEVT pre-diploma classified scholarship 2083/84: edusanjal.com (Rs 500 form, 1,065 seats in 16 programmes, opened 2083 Baisakh 28 or 29, closed Jestha 13)
and educatenepal.com; the seven provincial figures printed beside the total (132, 149, 130, 109, 197, 117, 123) add up to 957, not 1,065, while the 16
programme rows do add up to 1,065. Both are stated.
KU Laxmi Bank scholarship for women in STEM: ku.edu.np available endowment funds (item 33, NPR 10,000,000), newbusinessage.com (MoU of 2 January 2023,
50 percent of the yearly interest added back to the principal), gurubaa.com (says NPR 1 crore over five years), collegenp.com (KU School of Engineering call for
Nepali women in full time Master or PhD STEM studies) and the ku.edu.np scholarship notice list (6 August 2026 call, 15 September 2026 interview and result notices
for the Laxmi Sunrise Shikshit Laxmi scholarship for Woman in STEM).
Lok Sewa: unionnepal.com (13 November 2026) transcribing PSC notices 787, 788, 789, 580, 581 of 2083/84; loksewapathsala.com (notice 582/083-84, 89 health posts).
Medical entrance: Kathmandu Post, 26 October 2026 (9,691 seats, 77,359 applicants, 418 added, tuition Rs 4 to 4.4 million).
"""
CTEVT_TABLE = ('Agriculture (Animal Science) 186, Agriculture (Plant Science) 259, Architecture Engineering 30, Agricultural Engineering 4, Civil Engineering 640, '
               'Automobile Engineering 38, Civil (Hydropower) 20, Computer Engineering 187, Electrical and Electronics 30, Electrical Engineering 112, Electronics 2, '
               'Food and Dairy Technology 12, Forestry 60, Acupuncture 3, Diagnostic Radiography 100, General Ayurved Medicine 42, General Medicine 448, Geomatics 140, '
               'Information Technology 80, Mechanical 36, Mechatronics 2, Biomedical 8, Refrigeration and AC 6, Hotel Management 45, Medical Laboratory Technology 251, '
               'Nursing 189, Midwifery 6, Ophthalmic Science 27, Pharmacy 341, Dental Hygiene 30, Yog and Naturopathy 3, Physiotherapy 71, Beauty and Cosmetology 3, Fashion Designing 3')

SCHOLARSHIP_EXTRA = {
    's-ctevt': {
        'awards': 3417,
        'how': ('One programme in one province, filed on the ITMS online system (the 2083/84 form cost NPR 1,000 and closed on 2083/04/13, 11:59 pm, with printed acceptance card needed for admission). '
                'Seats per programme in the notice text (collegenp.com): ' + CTEVT_TABLE + '. These 34 rows add up to 3,414 against a printed grand total of 3,417, so one row may be misprinted. '
                'An older read of this page gave General Medicine 446, Agriculture Plant 261 and Medical Laboratory 250, which differ by one or two seats. '
                'Merit is the SEE GPA (with grade points from the percentage table) plus one extra mark for government, community or CTEVT constituent school applicants; ties go to Mathematics, Science and English grades in that order, then backward remote area, then the older candidate. '
                'Schools may not charge scholarship students tuition, practical, registration, exam, library or transport fees; recipients agree to serve where the government posts them, and nobody gets a second CTEVT scholarship.'),
    },
}

SCHOLARSHIPS_ADD = [
    {'id': 's-ctevt-prediploma', 'name': 'CTEVT classified (free) scholarship for pre-diploma programmes, 2083/84 (1,065 seats)', 'scope': 'nepal', 'levels': ['diploma'],
     'by': 'Council for Technical Education and Vocational Training (CTEVT), Office of the Controller of Examinations, Sanothimi',
     'covers': ('Free study in a pre-diploma (TSLC) programme. 1,065 seats in 16 programmes: Civil Engineering 267, Agriculture (Plant Science) 240, Livestock Production or Animal Health 165, '
                'Electrical 105, Computer 93, Survey (Amin) 78, Veterinary Science 60, Automobile 18, Mechanical 14, Hotel Management 5, Social Mobilization 6, Culinary Arts 2, Computer Application and Secretarial Management 3, '
                'Entrepreneurship Development 3, Electronics 3, Refrigeration and AC 3. Seats by province as printed: Lumbini 197, Madhesh 149, Koshi 132, Bagmati 130, Gandaki 109, Sudurpashchim 123, Karnali 117, '
                'but those seven add up to 957 while the 16 programme rows add up to 1,065, so read the Council notice for the real split (edusanjal.com, educatenepal.com).'),
     'who': 'Nepali citizens who passed SEE, or appeared in all SEE subjects (a Non-Graded result is accepted for pre-diploma), from government or community schools or CTEVT constituent institutions. One programme and one province only.',
     'how': 'Free choice of province and institutions on the ITMS online form at ctevtexam.org.np (the 2083/84 form cost NPR 500, opened 2083 Baisakh 28 or 29 and closed on 2083 Jestha 13 at 11:59 pm). The merit list and admission recommendations are made by each provincial CTEVT office and the printed acceptance card is mandatory for admission.',
     'link': 'https://ctevtexam.org.np', 'type': 'Government', 'open': [5, 5], 'awards': 1065},
    {'id': 's-ku-laxmi-stem', 'name': 'Laxmi Bank (Laxmi Sunrise) scholarship for Women in STEM at Kathmandu University', 'scope': 'nepal', 'levels': ['master', 'phd'],
     'by': 'Kathmandu University (KU) with Laxmi Sunrise Bank, through an endowment fund',
     'covers': ('Support for talented and economically disadvantaged women studying a Master or PhD in any STEM field at KU. The endowment is NPR 10,000,000 (KU available endowment funds list, item 33); '
                'Laxmi Bank said 50 percent of the yearly interest is added to the principal and 50 percent funds students, while another site says the bank pays NPR 1 crore over five years. '
                'The amount per student is not printed on the pages read.'),
     'who': 'Nepali women in full time Master or PhD STEM study at KU (the KU School of Engineering call also names economic need). KU runs the selection; the bank funds and promotes it.',
     'how': 'Watch the scholarship notices on ku.edu.np: the 2026 cycle had a call on 6 August 2026 with a form, then interview and result notices on 15 September 2026 under the name Laxmi Sunrise Shikshit Laxmi Scholarship for Woman in STEM (a collegenp.com summary gives a November deadline for the KU School of Engineering call, so the dates differ by school).',
     'link': 'https://ku.edu.np/available-endowment-funds', 'type': 'University', 'open': [8, 9]},
]

NOTE_ADD = {
    'p-sdcuhs': ('Edusanjal (8 April 2026) reported a proposal of MBBS 50, BSc Nursing 30, BSc MLT 20 and B Optometry 20 with NPR 2.58 billion secured, but the Medical Education Commission list used above gives BSc Nursing 20, BSc MLT 10 and B Optometry 10, so use the list. '
                 'The Kathmandu Post (26 October 2026) confirmed the first ever 50 MBBS seats and reported that campaigner Dr Govinda KC says the 300 bed teaching hospital the Medical Education Act needs is not ready; the Commission says seats follow expert inspection reports.'),
}

GOVT_NOTE_ADD = {
    'g-so': ('Notice 789/083-84 (on the PSC site 2083/07/25) lists 509 competitive seats, 504 open and inclusive plus 5 internal Health Service seats, for gazetted third class civil, federal parliament and national human rights service posts and Health Service 8th and 7th level posts (unionnepal.com, 13 November 2026). '
             'Apply online only at psconline1.psc.gov.np: regular deadline 2083/08/15, double fee until 2083/08/22, payment by 2083/08/23, fee NPR 1,200 per advertisement plus NPR 400 for each extra inclusive group. '
             'Age 21 to 35 (40 for women and persons with disabilities) for civil and human rights posts and 21 to 45 for Health Service. Written exams run in two phases at PSC offices (second phase at Dhankuta, Jaleshwar, Kathmandu, Pokhara, Butwal, Surkhet and Dipayal), with ICT, practical, group tests and interview where the syllabus says so. '
             'Promotion is separate: notices 787 (176 positions) and 788 (6) close on 2083/08/29 and notices 580 and 581 (182 positions in all) closed on 2083/08/01 with a fee of NPR 1,200 or 2,000; the note above gives Mangsir 25 for promotion, so read the PSC notice itself. '
             'Health Service Level 9 notice 582/083-84 had 89 specialist and consultant posts, fee NPR 2,000, age 21 to 45, applications 14 October to 3 November 2026 (loksewapathsala.com).'),
    'e-mecee': ('For 2083/84 the Medical Education Commission allocated 9,691 seats and 77,359 students applied for the integrated entrance examinations, against 9,273 seats and 8,548 enrolled last year; 418 seats were added, all in government institutions '
                '(110 MBBS, 120 BSc Nursing, 98 BMS, 30 each at BPKIHS and the Nepalese Army Institute) and seats were given to 84 of the 90 institutions that applied. Government colleges reserve 75 percent of seats for scholarship students while private colleges give 10 to 20 percent, '
                'and MBBS tuition is set between NPR 4 million and 4.4 million. The exams were held about a month late (31 October to 4 November 2026) because the commission posts were vacant (Kathmandu Post, 26 October 2026).'),
}

# IOE 2083 cycle: clamphook.com (application Ashadh 23 to Shrawan 1, exam Shrawan 11 to 18, result Shrawan 19 2083 = 4 August 2026, 13,000+ candidates),
# icenepal.com quoting the IOE B.E./B.Arch Booklet 2083 (published 7 August 2026; 7,179 names on the pass list; women 10 percent as seats, 20 percent of regular seats
# reserved for inclusive groups = 119 seats) and pcampus.edu.np admission notices (seventh list 5 October, remaining seats third and final phase 6 and 7 October 2026).
# TU bachelor 2083/84 annual calendar: collegenp.com and educatenepal.com (Rector's notice of 2083/02/19, posted 2 June 2026).
GOVT_NOTE_ADD.update({
    'e-ioe': ('The 2083/84 cycle ran like this (clamphook.com, icenepal.com quoting the IOE booklet and Pulchowk Campus notices): applications Ashadh 23 to Shrawan 1, exam Shrawan 11 to 18, result on Shrawan 19 2083 (4 August 2026) '
              'with 13,000 or more candidates and 7,179 names on the pass list (a rank each, no marks), the B.E./B.Arch booklet on 7 August 2026, then admission lists up to a seventh list on 5 October and a third and final phase for remaining seats on 6 and 7 October 2026. '
              'One calculator page prints a July exam instead, so trust the IOE portal entrance.ioe.edu.np. Women get 10 percent of seats as a printed count (56 Regular and 145 Full Fee seats across the five constituent campuses) and 20 percent of Regular seats go to inclusive groups, 119 seats in all (Pulchowk 55, Purwanchal 25, Paschimanchal 19, Thapathali 19, Chitwan 1).'),
    'e-tu-fom-bbs': ('The TU first year bachelor calendar for 2083/84 (Rector notice of 2083/02/19, collegenp.com): admission from the second week of Asar 2083 to the end of Bhadra, classes from the first week of Ashoj 2083, exam forms in Chaitra 2083, '
                     'exams in the last week of Jestha 2084 and results in Bhadra 2084. You file a separate form at each campus, faculty and subject you want.'),
    'e-tu-bachelor-sci': ('The TU first year bachelor calendar for 2083/84 (Rector notice of 2083/02/19, collegenp.com): admission from the second week of Asar 2083 to the end of Bhadra, classes from the first week of Ashoj 2083, exam forms in Chaitra 2083, '
                          'exams in the last week of Jestha 2084 and results in Bhadra 2084. Science entrance dates are set by IOST separately.'),
})
