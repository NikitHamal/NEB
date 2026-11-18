"""Wave 19 part 4 (w19_more.py): SOMTU MBA, NATHM BHM/BTTM seats and fee, TU/PU BBA seats and fees, SOMAT / CAAN CPL / GMAT Focus exams,
19 more directory-verified .edu.np college websites, and 5 FAQs (fw19-21 to fw19-25).

Sources (read 19 November 2026): NATHM 2082/83 admission notice on collegenp.com and edusanjal.com (BHM 264 seats = 198 open + 66 inclusive, BTTM 176 = 132 + 44,
8-semester BHM fee NPR 575,000, older tables show 240 and 160); SOMTU Kirtipur on edusanjal.com and collegenp.com (SOMAT 100 marks, 2h, 0.25 negative marking,
fee NPR 2,000; MBA 35 to 40 seats NPR 465,850, MFC 40 seats NPR 465,850, MBA-GLM 25 seats NPR 563,900, MBA-IT 30 seats NPR 556,600);
Shanker Dev, Nepal Commerce Campus, Thames and Tilottama BBA pages on shikshasanjal.com, gyanstation.com and collegenp.com;
CAAN CPL pilot guide on ktmalliance.com and sudishaviation.com.np (200h total, 100h PIC, Class 1 Medical, 9 subjects 75% pass);
GMAT Focus Edition 2026 on evec.com.np, aeccglobal.com.np and propelld.com (64 questions, 2h 15m, 205 to 805 scale, USD 275 / NPR 39,875).
"""

PROVIDERS_MORE = [
    {'id': 'p-somtu', 'name': 'School of Management, Tribhuvan University (SOMTU)', 'kind': 'Campus', 'sector': 'Public',
     'district': 'Kathmandu', 'place': 'Kirtipur', 'website': 'https://somtu.edu.np',
     'note': 'Autonomous management school of Tribhuvan University at Kirtipur (founded 2012). Admits through SOMAT (written test, group discussion, presentation and interview): MBA (35 to 40 seats, fee NPR 465,850; older 2018 notice NPR 385,000), MBA Finance and Control (40 seats, NPR 465,850), MBA-IT (30 seats, NPR 556,600) and MBA Global Leadership and Management (25 seats, NPR 563,900).',
     'seats': 135, 'fees': {'mba': [465850, 563900]}},
]

ROUTE_SEATS_MORE = {
    'p-somtu': {'mba': 135},
    'p-nathm': {'bhm': 264},
    'p-shankerdev': {'bba': 99, 'bim': 66},
    'p-ncc-minbhawan': {'bba': 99, 'bim': 66},
    'p-thames': {'bba': 66},
    'p-tilottama-campus': {'bba': 96},
}

FEES_MORE = {
    'p-nathm': {'bhm': [575000, 575000]},
    'p-shankerdev': {'bba': [350000, 400000]},
    'p-ncc-minbhawan': {'bba': [350000, 440000]},
}

PROVIDER_NOTE_MORE = {
    'p-nathm': 'NATHM 2082/83 admission notice seats: BHM 264 (75% open = 198, 25% inclusive = 66) and BTTM 176 (132 open, 44 inclusive); older course tables quote 240 BHM and 160 BTTM seats. Total 8-semester BHM fee is NPR 575,000. Selection weights CMAT (50%), +2 marks (30%) and GD/interview (20%).',
    'p-shankerdev': 'TU constituent campus at Putalisadak running BBA (99 seats), BITM/BIM (66 seats), BBM (66 seats), BBA-Finance, BBS and MBS; public 4-year BBA fee is roughly NPR 3.5 to 4 lakh.',
    'p-ncc-minbhawan': 'TU constituent campus at Minbhawan running BBA (99 seats), BITM/BIM (66 seats), BBM (88 seats), BBS, MBS and MBM; public 4-year BBA fee is roughly NPR 3.5 to 4.4 lakh.',
    'p-tilottama-campus': 'Also runs Pokhara University 4-year BBA (96 seats, 120 credits) in Yogikuti, Butwal.',
    'p-indreni': 'Also known after its IT-focused rebrand as Chitwan College of Technology (CCT) at Aastha Chowk, Bharatpur-12, running TU BSc CSIT, BCA and BITM.',
}

GOVT_MORE = [
    {'id': 'e-somat', 'track': 'ent_biz', 'name': 'SOMAT (TU School of Management MBA Entrance)', 'level': 'Postgraduate MBA admission (MBA, MFC, MBA-IT, MBA-GLM at SOMTU Kirtipur)',
     'need': 'Minimum 15 years of formal education (12 + 3-year Bachelor) with CGPA 2.0 or 45% (some tracks ask GPA 2.5 and 2 years work experience)',
     'age': 'No upper age bar', 'body': 'School of Management, Tribhuvan University (SOMTU), Kirtipur',
     'stages': [['SOMAT written exam', '2-hour 100-mark paper covering Verbal Ability, Quantitative Ability, Issue-based Essay Writing and Case Analysis (0.25 negative marking on objective questions).', '100'],
                ['GD, presentation and interview', 'Shortlisted candidates complete Group Discussion, Individual Presentation and Personal Interview.', '50']],
     'subjects': ['Verbal ability and reading comprehension', 'Quantitative and data analysis', 'Issue-based essay and business case analysis', 'Group discussion and individual presentation'],
     'prep': ['Practise GMAT-style verbal, quantitative and business case writing', 'Prepare a crisp 5-minute individual presentation and follow current Nepal economic issues for GD'],
     'fee': 2000, 'apply': [2, 8], 'exam_month': 3, 'seats': 135,
     'note': 'Held twice a year (Spring intake around Feb/March and Fall intake around June/July) for SOMTU Kirtipur programmes: MBA (35 to 40 seats, NPR 465,850), MBA Finance and Control (40 seats, NPR 465,850), MBA-IT (30 seats, NPR 556,600) and MBA Global Leadership and Management (25 seats, NPR 563,900).'},
    {'id': 'e-caan-cpl', 'track': 'lic', 'name': 'CAAN Commercial Pilot Licence (CPL) and Conversion Exam', 'level': 'National commercial flight crew licensing and foreign ICAO CPL conversion',
     'need': '+2 Science with Physics and Mathematics, minimum age 18, CAAN Class 1 Medical Certificate, and 200 total flight hours (including 100 hours PIC, 20h cross-country, 10h instrument, 5h night) with IR and Multi-Engine Rating from a CAAN/ICAO-approved flying school',
     'age': 'Minimum 18 years (17 years for PPL)', 'body': 'Civil Aviation Authority of Nepal (CAAN), Personnel Licensing Division, Babarmahal',
     'stages': [['Class 1 Medical and Ground School', 'Pass the annual CAAN Class 1 Medical assessment and complete 3 to 6 months of CPL/frozen-ATPL ground school.', '0'],
                ['CAAN Written Exams (9 subjects)', 'Multiple-choice written exams across 9 aviation subjects administered by CAAN; minimum passing score is 75% in each paper.', '100'],
                ['Flight Skill Test / Foreign CPL Conversion', 'Complete 200 flight hours and skill checks abroad (Philippines, South Africa, USA or India) and pass the CAAN licence conversion and aircraft type-rating check in Nepal.', '100']],
     'subjects': ['Air Law and CAAN Civil Aviation Requirements', 'Meteorology and Air Navigation', 'Aircraft General Knowledge, Principles of Flight and Flight Performance/Planning', 'Human Performance and Limitations, Operational Procedures and Radio Telephony'],
     'prep': ['Complete your CAAN Class 1 Medical in Kathmandu BEFORE paying tuition to any flying school abroad', 'Verify that your foreign flight academy is on the CAAN-recognised ICAO list before enrolling', 'Budget NPR 50 to 66.5 lakh for full SPL-to-CPL training with Instrument and Multi-Engine ratings plus 2 to 6 months for CAAN conversion'],
     'fee': 150000, 'apply': [1, 12], 'exam_month': 6, 'career': 'pilot',
     'note': 'Fixed-wing CPL flight training is completed at CAAN-approved schools abroad (such as in the Philippines, South Africa or the USA) followed by mandatory CAAN written conversion exams and type-rating endorsement in Nepal.'},
    {'id': 'l-gmat', 'track': 'lang_eng', 'name': 'GMAT Focus Edition (GMAC)', 'level': 'Global graduate business school admission test (MBA, Master in Finance/Analytics)',
     'need': 'Valid international passport (no minimum degree required to sit the test)', 'age': '18 years or older (13 to 17 with parental consent)',
     'body': 'Graduate Management Admission Council (GMAC, delivered via Pearson VUE)',
     'stages': [['Computer-adaptive test (3 sections)', '2 hours 15 minutes total (64 questions across three 45-minute sections: Quantitative Reasoning 21 questions, Verbal Reasoning 23 questions, Data Insights 20 questions). Scored 205 to 805.', '805']],
     'subjects': ['Quantitative Reasoning (21 questions, 45m: algebra and arithmetic problem solving, no geometry)', 'Verbal Reasoning (23 questions, 45m: critical reasoning and reading comprehension, no sentence correction)', 'Data Insights (20 questions, 45m: data sufficiency, multi-source reasoning, table/graphics analysis and two-part analysis)'],
     'prep': ['Use the official GMAT Focus Edition Starter Kit on mba.com and practise the new Data Insights section', 'Use the bookmark and review feature wisely (you can change up to 3 answers per section)'],
     'fee': 39875, 'apply': [1, 12], 'exam_month': 6,
     'note': 'The GMAT Focus Edition (205 to 805 scale) completely replaced the retired 200 to 800 GMAT Classic. Standard registration fee is USD 275 (about NPR 39,875 at USD 1 = NPR 145; some pages quote USD 250 test-centre and USD 275 to 300 online). Scores are valid for 5 years.'},
]

ROUTE_EXAM_MORE = {'pilot-route': 'e-caan-cpl'}
CAREER_LICENCE_MORE = {'pilot': {'name': 'CAAN Commercial Pilot Licence (CPL)', 'exam': 'e-caan-cpl'}}

WEBSITES_MORE = {
    'p-united-academy': 'https://academy.united.edu.np',
    'p-saptagandaki': 'https://smc.edu.np',
    'p-ace-mgt': 'https://www.ace.edu.np',
    'p-lalitpur-eng': 'https://lec.edu.np',
    'p-butwal-kalika': 'https://btlkalikacampus.edu.np',
    'p-whitefield': 'https://ref.edu.np',
    'p-morgan': 'https://morgancollege.edu.np',
    'p-sahid-smarak-kirtipur': 'https://sscollegekirtipur.edu.np',
    'p-himalaya-darshan': 'https://himalayacollege.edu.np',
    'p-aims-biratnagar': 'https://aimsbrt.edu.np',
    'p-sagarmatha-hs': 'https://smcollege.edu.np',
    'p-tilottama-campus': 'https://tilottama.edu.np',
    'p-janajyoti-kanchanpur': 'https://janjyotieducation.edu.np',
    'p-jaya-multiple': 'https://jmcampus.edu.np',
    'p-birat-multiple': 'https://bmc.arnikofoundation.edu.np',
    'p-everest-innovative': 'https://eiccollege.edu.np',
    'p-reliance': 'https://riacollege.edu.np',
    'p-saheed-smarak-bharatpur': 'https://sscbakhanpur.edu.np',
    'p-nesfield': 'https://nesfield.edu.np',
}

FAQ_MORE = [
    {'id': 'fw19-21', 'topic': 'after12', 'q': 'How many BHM and BTTM seats and what fee does NATHM charge?', 'go': ['bhm', 'mhm-mttm'],
     'a': 'In its 2082/83 admission notice, the government Nepal Academy of Tourism and Hotel Management (NATHM) at Rabi Bhawan, Kalimati lists 264 BHM seats (198 open competition, 66 inclusive) and 176 BTTM seats (132 open, 44 inclusive); older course tables quote 240 BHM and 160 BTTM seats. The published 8-semester BHM fee total is NPR 575,000. Applicants must score at least 40 percent in TU CMAT, and final merit weights CMAT (50 percent), +2 marks (30 percent) and Group Discussion/Personal Interview (20 percent).'},
    {'id': 'fw19-22', 'topic': 'afterbach', 'q': 'How does the SOMAT entrance for TU MBA at SOMTU Kirtipur work?', 'go': ['mba', 'mbs'],
     'a': 'The School of Management at Tribhuvan University (SOMTU) in Kirtipur runs its own School of Management Admission Test (SOMAT, fee NPR 2,000) twice a year in Spring and Fall rather than the central FoM CMAT. SOMAT is a 2-hour 100-mark written test (Verbal, Quantitative, Issue-based Essay and Case Analysis, with 0.25 negative marking on objective items) followed by Group Discussion, Individual Presentation and Personal Interview. SOMTU offers MBA (35 to 40 seats, fee NPR 465,850), MBA Finance and Control (40 seats, NPR 465,850), MBA-IT (30 seats, NPR 556,600) and MBA Global Leadership and Management (25 seats, NPR 563,900).'},
    {'id': 'fw19-23', 'topic': 'after12', 'q': 'What are the BBA seats and fees at Shanker Dev, Nepal Commerce Campus, Thames and Tilottama?', 'go': ['bba', 'bim'],
     'a': 'Under Tribhuvan University, Shanker Dev Campus (Putalisadak) and Nepal Commerce Campus (Minbhawan) each offer 99 BBA seats and 66 BITM (formerly BIM) seats with 4-year public BBA fees of roughly NPR 3.5 to 4.4 lakh, while private TU colleges such as Thames International College (66 BBA seats) charge around NPR 5 to 8 lakh. Under Pokhara University, Tilottama Campus in Butwal offers 96 BBA seats (120 credits) with 10 percent central scholarship seats.'},
    {'id': 'fw19-24', 'topic': 'after12', 'q': 'How do I get a CAAN Commercial Pilot Licence (CPL) in Nepal after training abroad?', 'go': ['pilot-route'],
     'a': 'To qualify for a Civil Aviation Authority of Nepal (CAAN) Commercial Pilot Licence, you need +2 Science with Physics and Mathematics, minimum age 18, a CAAN Class 1 Medical Certificate obtained before flying, and at least 200 flight hours (including 100 hours Pilot-in-Command, 20 hours cross-country, 10 hours instrument and 5 hours night) with Instrument and Multi-Engine ratings from a CAAN-recognised ICAO flight school abroad. Upon returning to Nepal, you must pass CAAN written conversion exams across 9 aviation subjects (75 percent pass mark) and aircraft type-rating checks.'},
    {'id': 'fw19-25', 'topic': 'afterbach', 'q': 'What is the GMAT Focus Edition format, score scale and fee in Nepal for 2026?', 'go': ['mba', 'abroad-ms'],
     'a': 'The GMAT Focus Edition (which completely replaced the old 200 to 800 GMAT Classic) is a 2 hour 15 minute computer-adaptive exam of 64 questions across three equally weighted 45-minute sections: Quantitative Reasoning (21 questions), Verbal Reasoning (23 questions) and Data Insights (20 questions), scored on a 205 to 805 scale. You can bookmark and change up to 3 answers per section. In Nepal the registration fee is USD 275 (about NPR 39,875; some listings quote USD 250 test-centre and USD 275 to 300 online) at Pearson VUE in Kathmandu or online.'},
]
