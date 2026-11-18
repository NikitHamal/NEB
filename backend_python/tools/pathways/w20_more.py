"""Wave 20 part 2 (w20_more.py): HICAST, Kathmandu Forestry College (KAFCOL), Namuna College of Fashion Technology (NCFT) and IEC College of Art and Fashion;
BVSc & AH, BSc Ag, BFDM and TU School of Mathematical Sciences (SMSTU) BMathSc Actuarial / Data Science seat quotas and fees; ADBL, Nepal Bank Limited and
SMSTU entrance exams; s-quota open window; and 7 FAQs (fw20-19 to fw20-25).

Sources (read 19 November 2026): BVSc & AH and BSc Ag seat and fee tables for HICAST and NPI (helpforentrance.com, helpforag.app, imnepal.com, hicast.edu.np);
Kathmandu Forestry College (kafcol.edu.np); Namuna College of Fashion Technology BFDM 96 seats and NPR 9,53,500 fee (studyinfocentre.com, ktmpadai.com,
tipsnepal.com); IEC College of Art and Fashion (ieccollege.com.np, tipsnepal.com); TU School of Mathematical Sciences BMathSc Actuarial Science and Bachelor of
Data Science 40 seats and NPR 5,30,000 fee (collegenp.com, sms.tu.edu.np); ADBL and Nepal Bank Limited Lok Sewa syllabi and fee notices (loksewatayariapp.com,
adbl.gov.np, nepalbank.com.np).
"""

PROVIDERS_MORE = [
    {'id': 'p-hicast', 'name': 'Himalayan College of Agricultural Sciences and Technology (HICAST)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Kirtipur / Kalanki, Kathmandu', 'website': 'https://hicast.edu.np', 'seats': 136,
     'route_seats': {'bvsc': 40, 'bsc-agri': 96},
     'fees': {'bvsc': [1900000, 2200000], 'bsc-agri': [1000000, 1000000]},
     'note': 'Established in 2000 under Purbanchal University affiliation in Kathmandu; offers 5 year BVSc and AH (40 seats; paying fee NPR 19 to 22 lakh, MOE scholarship seat NPR 3 to 4 lakh), 4 year BSc (Hons) Agriculture (96 seats; fee about NPR 10 lakh) and MSc in Dairy Technology, Meat Technology and Agri-Business Management.'},
    {'id': 'p-kafcol', 'name': 'Kathmandu Forestry College (KAFCOL)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Koteshwor, Kathmandu', 'website': 'https://www.kafcol.edu.np', 'seats': 50,
     'route_seats': {'bsc-forestry': 50},
     'fees': {'bsc-forestry': [900000, 950000]},
     'note': 'Tribhuvan University affiliated forestry college in Koteshwor, Kathmandu offering 4 year BSc in Forestry (around 50 seats; TU private forestry fee about NPR 9 lakh) and MSc in Forestry and GIS.'},
    {'id': 'p-ncft', 'name': 'Namuna College of Fashion Technology (NCFT)', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Bansbari, Kathmandu', 'seats': 96,
     'route_seats': {'bfd-design': 96},
     'fees': {'bfd-design': [953500, 953500]},
     'note': 'Founded in 2002 by Gyani Shova Tuladhar in Bansbari, Kathmandu as Nepal first fashion college under Purbanchal University; offers the 4 year (8 semester) Bachelor of Fashion Design and Management (BFDM, 96 seats, total fee NPR 9,53,500, entrance form NPR 1,200).'},
    {'id': 'p-iec-art', 'name': 'IEC College of Art and Fashion', 'kind': 'private', 'sector': 'private',
     'district': 'Kathmandu', 'place': 'Mandikhatar, Kathmandu', 'website': 'https://ieccollege.com.np',
     'note': 'Art, fashion and interior design college in Mandikhatar, Kathmandu offering international BA (Hons) programmes in Fashion and Retailing and Interior Architecture.'},
]

WHERE_MORE = {
    'bvsc': ['p-hicast', 'p-nepal-polytechnic'],
    'bsc-agri': ['p-hicast', 'p-nepal-polytechnic'],
    'msc-agri': ['p-hicast'],
    'bsc-forestry': ['p-kafcol'],
    'bfd-design': ['p-ncft', 'p-iec-art'],
}

ROUTE_SEATS_MORE = {
    'p-nepal-polytechnic': {'bvsc': 40},
    'p-sms-tu': {'bmath-actuarial': 40, 'mds-data-science': 40},
}

FEES_MORE = {
    'p-nepal-polytechnic': {'bvsc': [1900000, 2200000]},
    'p-sms-tu': {'bmath-actuarial': [530000, 530000]},
}

PROVIDER_NOTE_MORE = {
    'p-nepal-polytechnic': 'Also runs Purbanchal University 5 year BVSc and AH (40 seats, paying fee NPR 19 to 22 lakh) and BSc Agriculture in Bharatpur, Chitwan.',
    'p-sms-tu': 'Offers 4 year Bachelor in Mathematical Sciences (BMathSc) with Major in Actuarial Science (40 seats on course tables, 36 on older notices; 4 year fee NPR 5,30,000), 4 year Bachelor in Data Science (BDS, launched 2024, 40 seats, fee NPR 5,30,000) and 2 year Master in Data Science (MDS, 40 seats).',
}

GOVT_MORE = [
    {'id': 'g-adbl', 'track': 'fin', 'name': 'Agricultural Development Bank (ADBL) Level 4 Accountant and Level 6 Officer Exam', 'level': 'Level 4 Lekhapal (Accountant) and Level 6 Business Officer',
     'need': '+2 in Management/Commerce/Economics for Level 4 Lekhapal; Master degree in Management, Economics or Commerce (or CA) for Level 6 Business Officer; BE/BCA/BIT for MIS/IT Officer',
     'age': '18 to 35 years for Level 4; 21 to 35 years for Level 6 (up to 40 for women and persons with disabilities)', 'body': 'Agricultural Development Bank Limited (written exam by Lok Sewa Aayog)',
     'stages': [
         ['First Phase: Pre-test (Level 4)', '100 mark objective MCQ preliminary test covering Management, Accounting, Economics, Banking, Mathematics, Computer and GK.', '100'],
         ['Second Phase: Written Examination (2 papers)', 'Paper 1 (100 marks: Management 50, Accounting 20, Mathematics 20, Computer 10 for Level 4; Management, Banking, ADBL and Laws for Level 6) and Paper 2 (100 marks: Economics 20, Banking 45, ADBL and Banking Laws 35).', '200'],
         ['Interview', 'Oral interview for shortlisted candidates.', '30']
     ],
     'subjects': ['Accounting principles, ratio analysis, auditing, internal control and banking operations', 'Micro and macroeconomics, Nepalese agricultural and rural economy, monetary and fiscal policy', 'BAFIA 2073, NRB Act 2058, ADBL Bylaws, AML/CFT, business mathematics and computer applications'],
     'prep': ['Give special attention to rural banking, agricultural credit and ADBL institutional bylaws along with standard NRB directives', 'Practise time management on Paper 1 where Management (5x10 = 50 marks) and Accounting/Maths calculations appear together', 'Apply online at adbl.gov.np when the annual vacancy notice opens'],
     'note': 'Application fee is NPR 800 for Level 3 and 4 (+ NPR 200 per inclusive group) and NPR 1,000 for Level 6 and above (+ NPR 400 per inclusive group).',
     'prep_hours': 280, 'fee': 800, 'career': 'bank-officer'},
    {'id': 'g-nbl', 'track': 'fin', 'name': 'Nepal Bank Limited (NBL) Level 3, 4 Assistant and Level 6 Assistant Manager Exam', 'level': 'Level 3 Junior Assistant (Gold Tester), Level 4 Assistant and Level 6 Assistant Manager',
     'need': '+2 or equivalent for Level 3; Bachelor degree in Management/Economics for Level 4 Assistant; Master degree in Management/Economics (or CA) for Level 6 Assistant Manager',
     'age': '18 to 35 years for Level 3/4; 21 to 35 years for Level 6 (up to 40 for women and persons with disabilities)', 'body': 'Nepal Bank Limited (written exam conducted by Lok Sewa Aayog)',
     'stages': [
         ['First Phase: Pre-test (Level 3 and 4)', '45 minute, 100 mark objective MCQ screening test (pass mark 40).', '100'],
         ['Second Phase: Written Examination (2 papers)', 'Paper 1 (100 marks: Banking, Management, Accounting and Customer Handling) and Paper 2 (100 marks: Economics, Banking Laws, NRB Directives, Mathematics and IT).', '200'],
         ['Practical computer test and interview', 'Computer test and 30 mark interview.', '30']
     ],
     'subjects': ['Banking concepts, Nepal Bank Limited history (established 1994 BS), accounting, financial statements and auditing', 'Macroeconomics, monetary policy, capital and money markets, BAFIA 2073 and NRB Unified Directives', 'General management, customer service, business mathematics and office IT'],
     'prep': ['Note that unlike RBB and ADBL where Level 4 requires +2, Nepal Bank Limited Level 4 Assistant requires a Bachelor degree in Management or Economics', 'Prepare provincially as NBL Level 3 and Level 4 vacancies are announced by province', 'Apply online at nepalbank.com.np'],
     'note': 'Conducted by Lok Sewa Aayog; application fee is NPR 800 for Level 3/4 and NPR 1,000 for Level 6 (+ NPR 200 to 300 per inclusive group).',
     'prep_hours': 280, 'fee': 800, 'career': 'bank-officer'},
    {'id': 'e-smstu', 'track': 'ent_sci', 'name': 'SMSTU Entrance (TU Actuarial Science and Data Science)', 'level': 'Entrance exam for BMathSc (Actuarial Science), Bachelor in Data Science (BDS) and Master in Data Science (MDS)',
     'need': 'Passed +2 or equivalent in any stream (Science, Management, Humanities or Education) with 100 mark Mathematics or Business Mathematics in Class 11 or 12 and minimum CGPA 1.8 / second division',
     'age': '', 'body': 'School of Mathematical Sciences, Tribhuvan University (SMSTU, Balkhu/Kirtipur)',
     'stages': [
         ['Written objective examination', '2 hour written test in Mathematics, English and Quantitative/Analytical Reasoning.', '100'],
         ['Personal interview', 'Campus interview and document verification at SMSTU Balkhu (10 percent of seats carry TU merit/need scholarships).', '20']
     ],
     'subjects': ['Class 11 and 12 Mathematics / Business Mathematics (algebra, calculus, probability, statistics and matrices)', 'English reading comprehension, grammar and technical vocabulary', 'Logical, analytical and quantitative reasoning'],
     'prep': ['Revise +2 probability, statistics, calculus and algebra thoroughly as they form the core of the paper', 'Check sms.tu.edu.np for separate admission calls for BMathSc (Actuarial Science, 40 seats) and Bachelor in Data Science (BDS, 40 seats)'],
     'note': 'Application fee is NPR 2,000 on sms.tu.edu.np. Both the 4 year BMathSc (Actuarial Science) and the 4 year Bachelor in Data Science (BDS) have 40 seats each and a total 8 semester tuition fee of NPR 5,30,000.',
     'prep_hours': 140, 'fee': 2000, 'seats': 80},
]

ROUTE_EXAM_MORE = {
    'bmath-actuarial': 'e-smstu',
    'mds-data-science': 'e-smstu',
}

SCHOLARSHIP_EXTRA_MORE = {
    's-quota': {'open': [8, 10]},
}

FAQ_MORE = [
    {'id': 'fw20-19', 'topic': 'after12', 'q': 'Which colleges in Nepal offer BVSc and AH (Veterinary Science) and what are the seats and fees?',
     'a': 'Four institutions offer the 5 year BVSc and AH degree in Nepal: Agriculture and Forestry University (AFU Rampur, 50 seats), TU IAAS Paklihawa Campus (50 seats), and two Purbanchal University private colleges with 40 seats each, HICAST (Kathmandu) and Nepal Polytechnic Institute (NPI, Bharatpur). Full paying fees at HICAST and NPI are about NPR 19 to 22 lakh (around NPR 3 to 4 lakh on MOE scholarship seats).',
     'go': ['bvsc', 'bsc-agri']},
    {'id': 'fw20-20', 'topic': 'after12', 'q': 'Where can I study Bachelor of Fashion Design and Management (BFDM) in Nepal and what does it cost?',
     'a': 'Namuna College of Fashion Technology (NCFT) in Bansbari, Kathmandu (founded in 2002 under Purbanchal University) offers the 4 year, 8 semester BFDM degree with 96 seats and a total tuition fee of NPR 9,53,500 (entrance form NPR 1,200). IEC College of Art and Fashion in Mandikhatar also offers international bachelor degrees in Fashion and Retailing and Interior Architecture.',
     'go': ['bfd-design']},
    {'id': 'fw20-21', 'topic': 'after12', 'q': 'How many seats and what fee does TU School of Mathematical Sciences charge for Actuarial Science and Data Science?',
     'a': 'Tribhuvan University School of Mathematical Sciences (SMSTU, Balkhu, sms.tu.edu.np) offers both the 4 year Bachelor in Mathematical Sciences (BMathSc in Actuarial Science, 40 seats on course tables / 36 on older notices) and the 4 year Bachelor in Data Science (BDS, 40 seats). Each programme charges NPR 5,30,000 for 8 semesters (entrance fee NPR 2,000) and is open to students from any +2 stream who took 100 mark Mathematics or Business Mathematics.',
     'go': ['bmath-actuarial', 'mds-data-science']},
    {'id': 'fw20-22', 'topic': 'after12', 'q': 'Can I study BSc Forestry at a private college in Kathmandu?',
     'a': 'Yes. In addition to the government campuses of TU Institute of Forestry (Pokhara and Hetauda) and AFU Faculty of Forestry (Hetauda), Kathmandu Forestry College (KAFCOL) in Koteshwor, Kathmandu offers the TU affiliated 4 year BSc Forestry (about 50 seats, total fee around NPR 9 to 9.5 lakh) and MSc in Forestry and GIS.',
     'go': ['bsc-forestry']},
    {'id': 'fw20-23', 'topic': 'after12', 'q': 'What is the difference between Level 4 eligibility at RBB, ADBL and Nepal Bank Limited?',
     'a': 'Rastriya Banijya Bank (RBB) Level 4 Assistant and Agricultural Development Bank (ADBL) Level 4 Lekhapal accept +2 graduates, whereas Nepal Bank Limited (NBL) Level 4 Assistant requires a Bachelor degree in Management or Economics (+2 is eligible for NBL Level 3 Junior Assistant). All three exams are conducted by Lok Sewa Aayog with an application fee of NPR 800 for Level 3/4 and NPR 1,000 for Level 6.',
     'go': ['banking-route', 'public-enterprise-route']},
    {'id': 'fw20-24', 'topic': 'after12', 'q': 'What is the exam pattern for Agricultural Development Bank (ADBL) Level 4 Lekhapal?',
     'a': 'ADBL Level 4 has a 100 mark objective MCQ pre-test followed by two 100 mark subjective papers (Paper 1: Management 50, Accounting 20, Mathematics 20, Computer 10; Paper 2: Economics 20, Banking 45, ADBL and Banking Laws 35) and a 30 mark interview.',
     'go': ['banking-route', 'bbs', 'bba']},
    {'id': 'fw20-25', 'topic': 'after12', 'q': 'Can Management or Humanities students apply for TU Actuarial Science or Bachelor in Data Science?',
     'a': 'Yes. Any student who passed +2 in Science, Management, Humanities or Education with 100 mark Mathematics or Business Mathematics in Class 11 or 12 and at least CGPA 1.8 (or second division) is eligible to sit the SMSTU entrance exam at Balkhu.',
     'go': ['bmath-actuarial', 'plus2-management']},
]
