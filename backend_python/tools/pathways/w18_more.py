"""Wave 18 part 2: KUUMAT, TU BA LL.B entrance, AFU bachelor entrance, Digital SAT and GRE General Test, plus five FAQs. Plain sentences, no dashes.

Sources (read 18 November 2026): KUSOM KUUMAT 2026/27 (collegesinnepal.com, shikshasanjal.com, merouni.com, collegedarpan.com); TU Faculty of Law BA LL.B 2083/84
notice (collegenp.com, educatenepal.com); AFU Dean Office Rampur 2083/84 bachelor entrance notice (collegenp.com, educatenepal.com, smartacademyhq.com);
College Board Digital SAT 2026 Nepal fee (consultancyhunt.com, edwisefoundation.com, searcheducation.com.np); ETS GRE General Test 2026 Nepal fee (edwisefoundation.com,
consultancyhunt.com).
"""

GOVT_MORE = [
    {'id': 'e-kuumat', 'track': 'ent_biz', 'name': 'KUUMAT (Kathmandu University BBA and BBIS entrance)', 'level': 'Undergraduate management admission test, paper based',
     'need': '+2 or equivalent in any stream with at least 40 percent aggregate or CGPA 1.6 on a 4.0 scale (or 3 A Level subjects plus AS General Paper)',
     'age': '', 'body': 'Kathmandu University School of Management (KUSOM)',
     'stages': [
         ['Paper based test', '100 multiple choice questions, 100 marks, 1 hour 55 minutes (Verbal Ability 25, Quantitative Ability 25, Data Interpretation 25, English Proficiency 25). Wrong answers lose 0.25 marks; candidates must reach the 50th percentile overall and in the analytical section.', '100'],
         ['Personal interview', 'Shortlisted candidates attend a personal interview at KUSOM or the affiliated college.', '0']
     ],
     'subjects': ['Verbal ability 25', 'Quantitative ability 25', 'Data interpretation 25', 'English proficiency 25'],
     'prep': ['Practise SAT style verbal, quantitative and data interpretation sets', 'Do not guess blindly because each wrong answer deducts 0.25 marks', 'Prepare current affairs and your motivation for management before the KUSOM interview'],
     'note': 'Apply online at apply.ku.edu.np. Guides for the 2025/26 and 2026/27 cycles list an application fee of NPR 1,500 and an exam window in July or August.',
     'syllabus': [['Verbal ability', 25], ['Quantitative ability', 25], ['Data interpretation', 25], ['English proficiency', 25]],
     'prep_hours': 200, 'fee': 1500, 'apply': [7, 8], 'exam_month': 8},
    {'id': 'e-ballb', 'track': 'ent_biz', 'name': 'TU BA LL.B entrance (5 year integrated law)', 'level': 'Bachelor of Arts Bachelor of Laws entrance, written',
     'need': '+2 or equivalent in any stream (Nepal Bar Council Legal Education Regulations Rule 4(3) requires at least 50 percent or C+ grade; TU also lets Grade 12 candidates apply provisionally)',
     'age': '', 'body': 'Faculty of Law, Tribhuvan University (fol.edu.np)',
     'stages': [
         ['Objective MCQs', '30 multiple choice questions, 30 marks, 30 minutes.', '30'],
         ['Subjective and creative writing', '2 hours 30 minutes: 1 long answer question (20 marks), 3 short answer questions (30 marks) and creative writing of about 300 words (20 marks). Total paper is 100 marks.', '70']
     ],
     'subjects': ['Introduction to law, kinds of law and sources of law', 'Role of law in society, rights and duties, legal and natural persons', 'Constitution of Nepal and fundamental rights', 'Creative legal writing (about 300 words)'],
     'prep': ['Practise writing structured long and short legal answers and a 300 word essay inside 2.5 hours', 'Study the Constitution of Nepal (Part 3 Fundamental Rights) and basic jurisprudence thoroughly', 'Remember that 70 of the 100 marks come from subjective writing, not MCQs'],
     'note': 'For the 2083/84 session (570 total seats across 6 colleges, with 10 percent freeship at each college), online forms at fol.edu.np ran from 5 Asar to 32 Asar 2083 (double fee till 7 Shrawan) with an exam fee of NPR 1,800 (paid via eSewa, Khalti or ConnectIPS) and the exam on 23 Shrawan 2083.',
     'syllabus': [['Objective MCQs', 30], ['Short answer questions', 30], ['Long answer question', 20], ['Creative writing', 20]],
     'prep_hours': 220, 'fee': 1800, 'seats': 570, 'apply': [6, 7], 'exam_month': 8},
    {'id': 'e-afu', 'track': 'ent_sci', 'name': 'AFU entrance (BSc Ag, BVSc and AH, Forestry, Fisheries)', 'level': 'Agriculture, veterinary, forestry and fisheries bachelor entrance',
     'need': 'SEE/SLC plus +2 Science or I.Sc. (Agriculture/Forestry) with 100 marks each in English, Chemistry and Biology and at least 50 marks each in Physics and Mathematics, minimum 50 percent or C grade in each and C+ overall',
     'age': '', 'body': 'Agriculture and Forestry University (AFU), Rampur (admission.afu.edu.np)',
     'stages': [
         ['Paper based MCQ test', '120 multiple choice questions, 120 marks, 1 hour 30 minutes. Pass mark is 60 out of 120 (50 percent), no negative marking.', '120'],
         ['Merit list and counselling', 'Ranked on entrance score (with +2 and SEE tie breakers) for constituent and affiliated campuses.', '0']
     ],
     'subjects': ['English 22', 'Chemistry 22', 'Botany 22', 'Zoology 22', 'Physics 12', 'Mathematics 12', 'General knowledge 8'],
     'prep': ['Botany, Zoology, Chemistry and English carry 88 of the 120 marks, so prioritise them', 'Practise finishing 120 questions in 90 minutes (45 seconds per question)', 'Answer every question because there is no negative marking'],
     'note': 'In the 2083/84 AFU notice, online applications at admission.afu.edu.np ran from 21 Shrawan to 17 Bhadra 2083 with an application fee of NPR 3,000 (an older 2081 notice listed NPR 4,000 and one guide quotes NPR 1,500) and the exam on 20 Bhadra 2083 across six centres (Rampur, Hetauda, Kathmandu, Janakpur, Itahari and Nepalgunj).',
     'syllabus': [['Botany', 22], ['Zoology', 22], ['Chemistry', 22], ['English', 22], ['Physics', 12], ['Mathematics', 12], ['General knowledge', 8]],
     'prep_hours': 260, 'fee': 3000, 'apply': [8, 9], 'exam_month': 9},
    {'id': 'l-sat', 'track': 'lang_eng', 'name': 'Digital SAT (College Board)', 'level': 'Undergraduate admission and scholarship test for US and global universities',
     'need': 'Open to high school (+2 or A Level) students and graduates; a valid unexpired passport is required on test day in Nepal',
     'age': '', 'body': 'College Board (satsuite.collegeboard.org)',
     'stages': [
         ['Reading and Writing (2 adaptive modules)', '64 minutes, 54 questions testing comprehension, craft, grammar and rhetoric (scored 200 to 800).', '800'],
         ['Math (2 adaptive modules, calculator built in)', '70 minutes, 44 questions testing algebra, advanced math, data analysis and geometry/trigonometry (scored 200 to 800). Total time is 2 hours 14 minutes.', '800']
     ],
     'subjects': ['Reading and Writing (64 minutes, 200 to 800)', 'Math with built in Desmos graphing calculator (70 minutes, 200 to 800)'],
     'prep': ['Practise full length adaptive tests inside the official College Board Bluebook app', 'Learn to use the built in Desmos graphing calculator fast on algebra and system questions', 'Book your Kathmandu test centre seat at least a month early for the August, October or December rounds'],
     'note': 'Held seven times a year in Nepal (March, May, June, August, October, November and December). The official 2026 fee for Nepal is USD 111 (USD 68 base fee plus USD 43 international fee, about NPR 14,800 to 15,500; late registration adds USD 34 to 38).',
     'prep_hours': 180, 'fee': 15200, 'apply': [1, 12]},
    {'id': 'l-gre', 'track': 'lang_eng', 'name': 'GRE General Test (ETS)', 'level': 'Graduate admission test for MS, MBA and PhD programmes abroad',
     'need': 'Bachelor students or graduates; a valid unexpired Nepali passport is the only accepted ID at test centres and for GRE at Home',
     'age': '', 'body': 'Educational Testing Service (ets.org/gre)',
     'stages': [
         ['Analytical Writing (1 essay)', '30 minutes: one Analyze an Issue task, scored 0 to 6 in half point steps.', '6'],
         ['Verbal Reasoning (2 section adaptive modules)', '41 minutes, 27 questions testing reading comprehension, text completion and sentence equivalence (scored 130 to 170).', '170'],
         ['Quantitative Reasoning (2 section adaptive modules)', '47 minutes, 27 questions testing arithmetic, algebra, geometry and data analysis (scored 130 to 170). Total test time is about 1 hour 58 minutes.', '170']
     ],
     'subjects': ['Analytical Writing (0 to 6)', 'Verbal Reasoning (130 to 170)', 'Quantitative Reasoning (130 to 170)'],
     'prep': ['Take the official ETS PowerPrep timed practice tests for the shorter 1 hour 58 minute format', 'Drill high frequency academic vocabulary in context rather than isolated word lists', 'Send your 4 free score reports on test day to save USD 30 per extra institution later'],
     'note': 'Offered year round at test centres in Kathmandu, Lalitpur and Chitwan and via GRE at Home. The 2026 registration fee in Nepal is USD 220 (about NPR 27,000 to 31,000 depending on the exchange rate) and includes 4 free official score reports.',
     'prep_hours': 200, 'fee': 30000, 'apply': [1, 12]},
]

ROUTE_EXAM_MORE = {
    'bsc-agri': 'e-afu',
    'bvsc': 'e-afu',
    'bsc-forestry': 'e-afu',
    'bsc-horticulture-fisheries': 'e-afu',
    'ba-llb': 'e-ballb',
}

FAQ_MORE = [
    {'id': 'fw18-21', 'topic': 'after12', 'q': 'How does KUUMAT differ from CMAT for BBA admission in Nepal?',
     'a': 'CMAT is run by Tribhuvan University for TU management colleges (100 MCQs, 100 marks, 90 minutes, no negative marking, pass mark 40 percent, fee about NPR 1,000), whereas KUUMAT is run by Kathmandu University School of Management (KUSOM) for KU BBA and BBIS programmes (100 MCQs across Verbal, Quantitative, Data Interpretation and English, 1 hour 55 minutes, fee NPR 1,500). Unlike CMAT, KUUMAT deducts 0.25 marks for every wrong answer and requires the 50th percentile overall and in the analytical section before the personal interview.',
     'go': ['bba', 'bbm', 'bim']},
    {'id': 'fw18-22', 'topic': 'after12', 'q': 'What is the question pattern, fee and 2083 schedule for the TU BA LL.B entrance exam?',
     'a': 'The Tribhuvan University 5 year BA LL.B entrance is a 3 hour, 100 mark written test: Part 1 has 30 objective MCQs (30 marks, 30 minutes) and Part 2 (2 hours 30 minutes) has one long answer question (20 marks), three short answer questions (30 marks) and a 300 word creative writing piece (20 marks). For the 2083/84 session (570 total seats across 6 colleges, with 10 percent freeship at each college), online forms at fol.edu.np ran from 5 Asar to 32 Asar 2083 with a fee of NPR 1,800 and the exam on 23 Shrawan 2083. Note that Nepal Bar Council Legal Education Rules require at least 50 percent or C+ in +2.',
     'go': ['ba-llb', 'llb']},
    {'id': 'fw18-23', 'topic': 'after12', 'q': 'What is the syllabus, fee and 2083 date for the AFU BSc Agriculture, BVSc and Forestry entrance?',
     'a': 'Agriculture and Forestry University (AFU) conducts a 1 hour 30 minute paper based test with 120 MCQs (120 marks, pass mark 60, no negative marking): English 22, Chemistry 22, Botany 22, Zoology 22, Physics 12, Mathematics 12 and General Knowledge 8. In the 2083/84 notice, online forms at admission.afu.edu.np ran from 21 Shrawan to 17 Bhadra 2083 with a fee of NPR 3,000 (an older 2081 notice listed NPR 4,000) and the exam took place on 20 Bhadra 2083 across six centres (Rampur, Hetauda, Kathmandu, Janakpur, Itahari and Nepalgunj).',
     'go': ['bsc-agri', 'bvsc', 'bsc-forestry', 'bsc-horticulture-fisheries']},
    {'id': 'fw18-24', 'topic': 'abroad', 'q': 'How much does the Digital SAT cost in Nepal in 2026 and how often is it held?',
     'a': 'The Digital SAT (2 hours 14 minutes, computer adaptive, scored 400 to 1600 across Reading and Writing and Math) is held seven times a year in Nepal (March, May, June, August, October, November and December). In 2026 the official College Board fee for Nepal is USD 111 (USD 68 base registration fee plus USD 43 international fee, about NPR 14,800 to 15,500 depending on the exchange rate), plus USD 34 to 38 if you register late.',
     'go': ['a-levels', 'plus2-science']},
    {'id': 'fw18-25', 'topic': 'abroad', 'q': 'What is the shorter GRE format and 2026 exam fee in Nepal?',
     'a': 'The GRE General Test takes about 1 hour 58 minutes and has one Analytical Writing Issue essay (30 minutes, scored 0 to 6), two Verbal Reasoning modules (27 questions, scored 130 to 170) and two Quantitative Reasoning modules (27 questions, scored 130 to 170). In 2026 the official ETS fee in Nepal is USD 220 (about NPR 27,000 to 31,000, including 4 free score reports), and you can sit it at test centres in Kathmandu, Lalitpur and Chitwan or via GRE at Home with a valid Nepali passport.',
     'go': ['msc-cs', 'mtech', 'mba']},
]
