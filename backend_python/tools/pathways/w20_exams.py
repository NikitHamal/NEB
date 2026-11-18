"""Wave 20 exams and guides: NEA, Nepal Telecom and Rastriya Banijya Bank Lok Sewa exams, EPS-TOPIK Korea and JFT-Basic / Japan SSW skill tests,
plus route exam links and four step by step guides.

Sources (read 19 November 2026): Nepal Electricity Authority Lok Sewa syllabus (nea.org.np, loksewatayariapp.com); Nepal Telecom Kartik 13, 2083 vacancy notice
(ntc.net.np, berojgarengineer.com); Rastriya Banijya Bank Lok Sewa syllabus (rbb.com.np); EPS Korea Branch Gwarko 2026 notice (eoers.epsnepal.gov.np,
blog.educatenepal.com, collegenp.com); Prometric Japan SSW & JFT-Basic Nepal fee schedule (prometric-jp.com, digitalsolutionnepal.com, examsanjal.com).
"""

GOVT_ADD = [
    {'id': 'g-nea', 'track': 'psc', 'name': 'Nepal Electricity Authority (NEA) Officer and Supervisor Exam', 'level': 'Level 3, 4, 5 Assistant/Supervisor and Level 7 Engineer/Officer',
     'need': '+2 or Diploma in Engineering for Level 4/5 Supervisor; Bachelor degree (BE for Engineer, BBS/BBA/MBS for Account/Admin Officer) plus NEC licence for engineers at Level 7',
     'age': '18 to 35 years (up to 40 for women and persons with disabilities)', 'body': 'Nepal Electricity Authority (written exam conducted by Lok Sewa Aayog)',
     'stages': [
         ['First Paper: General Knowledge, Institutional and Technical/Service Basics', '100 marks written paper combining objective MCQs and structured questions on the Constitution, Electricity Act 2049, NEA regulations and core subject.', '100'],
         ['Second Paper: Service or Engineering Discipline Subject', '100 marks descriptive written paper on electrical/civil/mechanical/computer engineering or accounting/administration.', '100'],
         ['Computer skill test and interview', 'Practical skill test (where applicable) and 30 mark oral interview.', '30']
     ],
     'subjects': ['Electricity Act 2049, Electricity Regulation 2050, Electricity Regulatory Commission Act 2074 and NEA Financial/Staff Bylaws', 'Power sector development in Nepal, hydropower generation, transmission, distribution and tariff structure', 'Discipline specific engineering (electrical, civil, mechanical, computer) or financial administration and public procurement'],
     'prep': ['Memorise key sections of the Electricity Act 2049, Public Procurement Act 2063 and NEA Employee Service Regulations 2075', 'Combine Lok Sewa technical MCQ practice with long answer diagrams for Paper 2', 'Apply online via career.nea.org.np when the annual vacancy notice opens'],
     'note': 'Written exams are conducted by the Public Service Commission (Lok Sewa Aayog). Application fees start at NPR 800 for assistant level and NPR 1,200 for Level 7 officer roles.',
     'prep_hours': 320, 'fee': 1200, 'career': 'electrical-engineer'},
    {'id': 'g-ntc', 'track': 'psc', 'name': 'Nepal Telecom (NTC) Engineer, Officer and Technician Exam', 'level': 'Level 3/4 Technician and Assistant, Level 7 Engineer and Officer',
     'need': 'SLC/SEE + training or CTEVT Diploma for Level 3/4 Technician; BE in Electronics and Communication, Computer or Electrical (with NEC licence) for Level 7 Engineer; Bachelor/Master for Admin/Account Officer',
     'age': '18 to 35 years (up to 40 for women and persons with disabilities; up to 40 for permanent NTC staff)', 'body': 'Nepal Doorsanchar Company Limited (written exam by Lok Sewa Aayog)',
     'stages': [
         ['First Paper: General Knowledge, Telecom Act and Core Fundamentals', '100 marks written examination covering GK, institutional bylaws, Telecommunications Act 2053 and core discipline.', '100'],
         ['Second Paper: Specialized Technical or Administrative Paper', '100 marks descriptive subjective paper on telecommunications, networking, software/IT or management.', '100'],
         ['Interview', 'Oral interview for candidates who pass both written papers.', '30']
     ],
     'subjects': ['Telecommunications Act 2053, Nepal Telecom Employee Bylaws and ICT Policy of Nepal', 'Digital communication, mobile networks (4G/5G), optical fibre, IP networking and database/operating systems', 'Public enterprise management, financial rules and customer service delivery'],
     'prep': ['Download the exact level syllabus PDF from ntc.net.np and cover every unit equally as NTC gives no fixed chapter weightage', 'Engineering graduates in Computer Engineering can also check eligibility for Electronics and Communication vacancies if prepared for telecom subjects', 'Submit your online application at recruitment.ntc.net.np before the single fee deadline'],
     'note': 'Per the Kartik 13, 2083 (October 30, 2026) Nepal Telecom vacancy notice, the examination fee for Level 6 and Level 7 is NPR 700 (plus NPR 200 for each additional inclusive quota group).',
     'prep_hours': 300, 'fee': 700, 'apply': [10, 11], 'career': 'electronics-engineer'},
    {'id': 'g-rbb', 'track': 'fin', 'name': 'Rastriya Banijya Bank (RBB) Level 4 Assistant and Level 6 Officer Exam', 'level': 'Level 4 Assistant (Administration/Cash) and Level 6 Assistant Manager',
     'need': '+2 in any stream (or Management for Cash) for Level 4 Assistant; Master degree in Economics/Management (or Bachelor with 50% in Management/Economics under updated notices) for Level 6 Officer; BE/BCA/BIT/BCIS for IT roles',
     'age': '18 to 35 years for Level 4; 21 to 35 years for Level 6 (up to 40 for women and persons with disabilities)', 'body': 'Rastriya Banijya Bank Limited (written exam conducted by Lok Sewa Aayog)',
     'stages': [
         ['First Phase: Pre-test (Level 4 only)', '45 minute, 100 mark objective MCQ screening test (50 questions x 2 marks; Banking, Accounting, Mathematics, Computer and GK; pass mark 40, no marks carried forward).', '100'],
         ['Second Phase: Written Examination (2 papers)', 'Paper 1 (100 marks: Banking, Management, Accounting and Customer Service) and Paper 2 (100 marks: Economics, Banking Laws, NRB Directives, Mathematics and IT).', '200'],
         ['Practical computer test and interview', 'Final interview (30 marks) plus computer skill check.', '30']
     ],
     'subjects': ['Nepal Rastra Bank Act 2058, BAFIA 2073, Banking Offence and Punishment Act 2064, AML/CFT and NRB Unified Directives', 'Financial accounting, ratio analysis, auditing, internal control and banking operations', 'Macroeconomics, monetary and fiscal policy, business mathematics and office IT'],
     'prep': ['Clear the Level 4 MCQ pre-test by focusing on NRB Unified Directives, BAFIA 2073 and basic accounting ratios', 'Practise structured 10 mark descriptive answers citing specific BAFIA sections and latest Monetary Policy figures', 'Apply online at career.rbb.com.np when the annual vacancy opens'],
     'note': 'Conducted by Lok Sewa Aayog across provincial clusters; application fee is NPR 800 for Level 4/5 and NPR 1,000 for Level 6 (+ NPR 200 to 300 per inclusive group).',
     'prep_hours': 280, 'fee': 800, 'career': 'bank-officer'},
    {'id': 'l-eps', 'track': 'lang_oth', 'name': 'EPS-TOPIK (Korean Employment Permit System Test)', 'level': 'Government to government Korean language and skill test for work in South Korea',
     'need': 'Nepali citizen aged 18 to 39 years with no criminal record, no history of illegal stay in Korea, and no colour blindness',
     'age': '18 to 39 years (strictly enforced by birth date window in each notice)', 'body': 'HRD Korea and Department of Foreign Employment, EPS Korea Branch (Gwarko, Lalitpur)',
     'stages': [
         ['Computer / UBT Korean Language Test (Reading and Listening)', '50 minutes continuous test without a break at the UBT Building, Bhaisepati: 20 Reading questions + 20 Listening questions (40 questions total, scored out of 200 points; some notices list 100 marks per section or 100 total).', '200'],
         ['Skill, physical and competency test', 'Candidates who pass the language cutoff take a sector skill test (manufacturing, agriculture and livestock, or shipbuilding) and colour vision / physical check.', '100']
     ],
     'subjects': ['Korean workplace reading comprehension, safety signs and basic grammar (20 questions)', 'Korean listening comprehension of dialogues, numbers, instructions and workplace announcements (20 questions)', 'Basic physical measurement, colour vision check and sector tool/skill test'],
     'prep': ['Study the official HRD Korea EPS-TOPIK Standard Textbook Volumes 1 and 2 thoroughly', 'Practise 40 question 50 minute continuous UBT mock tests on a tablet', 'Attend biometric verification at EPS Office Gwarko one day before your scheduled exam date'],
     'note': 'Applications are filed online at eoers.epsnepal.gov.np with an exam fee of USD 28 (about NPR 3,850 converted at the previous day Nepal Rastra Bank rate). Recent annual quotas included 3,500 for manufacturing and 1,800 for agriculture and livestock; results remain valid for 2 years.',
     'prep_hours': 260, 'fee': 3850, 'apply': [7, 8]},
    {'id': 'l-ssw', 'track': 'lang_oth', 'name': 'JFT-Basic and Japan SSW (Specified Skilled Worker) Test', 'level': 'Japanese language (A2) and sector skill tests for Japan SSW (i) work visa',
     'need': 'At least 17 years old on the exam date (18+ for the SSW visa) with a valid passport; passing both JFT-Basic (or JLPT N4; N3 for taxi/bus driver) and one sector skill test is required',
     'age': '17+ to sit the exam, 18+ for visa', 'body': 'Japan Foundation and Prometric (test centers in Kathmandu, Lalitpur and Pokhara)',
     'stages': [
         ['JFT-Basic (Japan Foundation Test for Basic Japanese)', '60 minute computer based test (about 50 questions across Script/Vocabulary, Conversation/Expression, Listening and Reading) scored out of 250 points. Minimum 200 out of 250 (CEFR A2 / JLPT N4 equivalent) required to pass; fee in Nepal is USD 36.', '250'],
         ['SSW (i) Sector Skill Evaluation Test', 'Computer based technical skill exam in your chosen field (Nursing Care USD 8 to 15, Construction USD 8, Auto Repair USD 31, Agriculture USD 33, Food Service USD 33, Accommodation USD 55).', '100']
     ],
     'subjects': ['Practical daily and workplace Japanese communication at A2 level (Script, Conversation, Listening, Reading)', 'Sector specific technical skills and safety procedures (Nursing Care also requires the 15 question Nursing Care Japanese test)', 'Japanese traffic/driving knowledge and JLPT N3 for the Automobile Transportation (bus/taxi) track'],
     'prep': ['Study the free Japan Foundation Irodori: Japanese for Life in Japan (Starter A1 and Elementary A2) textbooks', 'Create a Prometric ID at prometric-jp.com and book seats early at Kathmandu (Dillibazar, New Baneshwor), Lalitpur (Kumaripati) or Pokhara (Ranipauwa)', 'After receiving your Certificate of Eligibility and visa, apply for your Nepal labour permit online via FEIMS (feims.dofe.gov.np)'],
     'note': 'Per the official Prometric Nepal fee schedule (October to November 2026), JFT-Basic costs USD 36 (about NPR 5,000), Nursing Care costs USD 8 to 15, Construction USD 8, Auto Repair USD 31, Agriculture USD 33 and Accommodation USD 55. SSW (i) allows up to 5 years stay in Japan.',
     'prep_hours': 240, 'fee': 5000},
]

ROUTE_EXAM = {
    'foreign-lang-work': 'l-eps',
    'abroad-ms': 'l-gre',
    'msc-cs': 'e-ioe-msc',
}

GUIDES_ADD = [
    {'id': 'eps-korea-apply', 'name': 'Apply for EPS-TOPIK South Korea from Nepal', 'cat': 'Abroad',
     'steps': [
         ['Obtain a machine readable or e-passport and verify that your age is between 18 and 39 years on the notice cutoff date', 3, 5000, 'in person'],
         ['Register at eoers.epsnepal.gov.np when the EPS Korea Branch Gwarko opens the sector window and pay USD 28 online in NPR', 1, 3850, 'online'],
         ['Attend biometric registration at EPS Office Gwarko one day before your exam and sit the 50 minute 40 question UBT test at Bhaisepati', 2, 0, 'in person'],
         ['Pass the skill/competency test, complete the medical check and wait for employer roster selection via HRD Korea', 30, 0, 'in person'],
     ],
     'docs': ['Valid passport', 'Citizenship certificate', 'Digital passport photo with white background'],
     'link': 'exam:l-eps'},
    {'id': 'ssw-japan-apply', 'name': 'Apply for JFT-Basic and Japan SSW visa from Nepal', 'cat': 'Abroad',
     'steps': [
         ['Create a Prometric ID at prometric-jp.com and book the JFT-Basic exam (USD 36) and your SSW sector skill test (USD 8 to 55) at Kathmandu, Lalitpur or Pokhara', 2, 5000, 'online'],
         ['Score at least 200 out of 250 on the 60 minute JFT-Basic CBT (or pass JLPT N4) and pass your sector skill test', 1, 2000, 'in person'],
         ['Interview with a Japanese accepting organization / registered support organization to receive a job contract and Certificate of Eligibility (CoE)', 45, 0, 'online'],
         ['Apply for your SSW (i) visa at VFS Japan Kathmandu and obtain your Foreign Employment labour permit on feims.dofe.gov.np', 10, 0, 'in person'],
     ],
     'docs': ['Valid passport and citizenship certificate', 'JFT-Basic (or JLPT N4/N3) pass report and SSW sector skill test pass certificate', 'Signed employment contract and Certificate of Eligibility (CoE)'],
     'link': 'exam:l-ssw'},
    {'id': 'somat-mba-apply', 'name': 'Apply for TU MBA and MBS through SOMAT or CDMAT', 'cat': 'Applications',
     'steps': [
         ['Verify that you hold a bachelor degree in any discipline with at least CGPA 2.0 or 45 percent aggregate', 1, 0, 'online'],
         ['Submit your online application at somtu.edu.np or cdmtu.edu.np and pay the NPR 2,000 SOMAT entrance fee', 1, 2000, 'online'],
         ['Sit the written GMAT style SOMAT/CDMAT test (verbal, quantitative, issue essay and case analysis)', 1, 0, 'in person'],
         ['Attend the group discussion, presentation and personal interview to secure admission on the merit list', 5, 0, 'in person'],
     ],
     'docs': ['SEE, +2 and Bachelor transcripts and character certificates', 'Citizenship certificate', 'Passport size photos'],
     'link': 'exam:e-somat'},
    {'id': 'caan-cpl-licence', 'name': 'Obtain a CAAN Commercial Pilot License (CPL) in Nepal', 'cat': 'Study',
     'steps': [
         ['Pass +2 Science (Physics and Mathematics), complete a CAAN Class 1 Medical exam and secure an offer from a CAAN approved Flying Training Organization (ATO)', 7, 10000, 'in person'],
         ['Apply to CAAN Flight Safety Standards Department for a No Objection Letter (NOL) before starting flight training abroad', 10, 5000, 'in person'],
         ['Complete at least 200 flight hours (100 PIC, 20 cross country PIC, 10 instrument, 5 night) or 150 hours in an approved integrated course', 365, 0, 'in person'],
         ['Return to Nepal and pass the CAAN CPL written conversion exams across 9 aviation subjects (75 percent pass mark)', 14, 150000, 'in person'],
     ],
     'docs': ['+2 Science transcript with Physics and Mathematics', 'Valid CAAN Class 1 Medical Certificate and CAAN No Objection Letter', 'Certified pilot logbook (200 modular / 150 integrated hours) and foreign ICAO CPL'],
     'link': 'exam:e-caan-cpl'},
]
