"""Wave 21 exams (part 2): TU IOST BSc/BTech Food & MSc entrances, TU FoHSS Bachelor & Master entrances, Purbanchal University
central entrance, and ACCA professional qualification exams.

Sources (read 19 November 2026): TU IOST BSc, BTech Food and MSc entrance notices (iost.tu.edu.np, edusanjal.com);
TU FoHSS Bachelor and Master entrance notices (fohss.tu.edu.np, cdpa.edu.np); Purbanchal University entrance notices (puexam.edu.np,
pufost.edu.np); ACCA 2026/27 global fee schedule (accaglobal.com, accountingstack.co.uk, nifmacademy.com).
"""
from w21_exams import GOVT_ADD_A

GOVT_ADD_B = [
    {'id': 'e-tu-bachelor-sci', 'track': 'ent_sci', 'name': 'TU IOST BSc and BTech Food Technology Entrance Exam',
     'level': 'Bachelor in Science (Physics, Chemistry, Biology, Microbiology, Geology, Environment) and BTech Food Technology',
     'need': '+2 Science (or ISc / A Level with Physics, Chemistry and Mathematics or Biology) with at least Second Division or C grade in each subject (minimum CGPA 1.8 to 2.0)',
     'age': 'No upper age limit', 'body': 'Tribhuvan University, Institute of Science and Technology (IOST)',
     'stages': [
         ['Computer / OMR Objective Entrance Test (2 hours)', '100 multiple choice questions (100 marks) covering Physics, Chemistry and either Mathematics (Physical group) or Biology (Biological group / BTech Food); minimum 35 marks required to pass (no negative marking).', '100'],
         ['Campus merit list and admission', 'Constituent and affiliated campuses publish merit lists combining the IOST entrance score (80 percent weight) and +2 marks (20 percent weight).', '0'],
     ],
     'subjects': ['Grade 11 and 12 Physics and Chemistry fundamentals', 'Grade 11 and 12 Mathematics (for Physical group, Geology, Statistics and Computer/Physics combinations)', 'Grade 11 and 12 Botany and Zoology (for Biological group, Microbiology, Environmental Science and BTech Food Technology)'],
     'prep': ['Practise 2 hour 100 question IOST past papers for your chosen stream (Physical or Biological) as there is no negative marking', 'Apply early to constituent campuses (Tri-Chandra, ASCOL, Patan, Prithvi Narayan, Central Campus of Technology Dharan) where fees are lowest', 'Submit your online entrance form at iost.tu.edu.np before the single fee deadline'],
     'note': 'Conducted annually by TU IOST across constituent and affiliated science and food technology campuses; entrance fee is NPR 1,650 to 2,200.',
     'prep_hours': 120, 'fee': 1650, 'apply': [8, 9], 'exam_month': 9},
    {'id': 'e-tu-msc-iost', 'track': 'ent_sci', 'name': 'TU IOST MSc (Physics, Chemistry, Maths, Microbiology, Environment, Geology, Biotech) Entrance Exam',
     'level': 'Master of Science across Tribhuvan University Central Departments and constituent campuses',
     'need': 'BSc in the relevant discipline from Tribhuvan University or a recognized university with minimum pass division / CGPA',
     'age': 'No upper age limit', 'body': 'Tribhuvan University, Institute of Science and Technology (IOST)',
     'stages': [
         ['Objective Written / CBT Entrance Test (2 hours)', '100 multiple choice questions (100 marks) on core four year undergraduate BSc topics; minimum 35 marks required to pass.', '100'],
         ['Central Department and campus merit admission', 'Admission to Kirtipur Central Departments and constituent campuses on entrance merit (80 percent entrance + 20 percent BSc aggregate).', '0'],
     ],
     'subjects': ['Four year TU BSc core syllabus of the respective science subject (Physics, Chemistry, Mathematics, Statistics, Microbiology, Environmental Science, Geology or Biotechnology)', 'Analytical problem solving and subject specific conceptual MCQs', 'Research methodology and laboratory instrumentation basics'],
     'prep': ['Revise all four years of the TU BSc curriculum of your major subject, as all 100 MCQs come directly from the undergraduate syllabus', 'Apply early for Central Department seats at Kirtipur where 80 percent open merit and 20 percent inclusive scholarship seats are offered', 'File your online entrance form at iost.tu.edu.np'],
     'note': 'Entrance fee is NPR 1,500 to 2,200 depending on the department; Kirtipur Central Departments allocate 80 percent open merit and 20 percent free scholarship seats.',
     'prep_hours': 140, 'fee': 2000, 'apply': [11, 12], 'exam_month': 1},
    {'id': 'e-fohss-bachelor', 'track': 'ent_biz', 'name': 'TU FoHSS and CDPA Bachelor Entrance Exam (BSW, BJMC, BFA, BPA, Psychology, Economics)',
     'level': 'Four year Bachelor in Humanities and Social Sciences (BSW, BJMC, BFA, BPA, BA Economics/BDevS, Psychology)',
     'need': '+2 or equivalent in any stream with at least D+ grade in each subject (minimum CGPA 1.8 or Second Division)',
     'age': 'No upper age limit', 'body': 'Tribhuvan University, Faculty of Humanities and Social Sciences (FoHSS) and Central Department of Public Administration (CDPA)',
     'stages': [
         ['Written Entrance Test (Objective + Short Answer / Studio Practical)', '100 mark entrance test covering English, Nepali, General Awareness and subject aptitude (plus drawing/practical audition for BFA Fine Arts and Music).', '100'],
         ['Personal interview and campus admission', 'Shortlisted candidates attend an interview at the constituent campus (Ratna Rajya, Padma Kanya, Tri-Chandra, Lalitkala, Public Administration Campus Balkhu) or affiliated college.', '20'],
     ],
     'subjects': ['English reading comprehension, grammar, vocabulary and analytical paragraph writing', 'General knowledge of Nepal history, geography, constitution, social issues, media and economy', 'Practical drawing, sculpture or music performance test for Bachelor of Fine Arts (BFA) at Lalitkala and Sirjana College of Fine Arts'],
     'prep': ['Prepare current social, economic and constitutional affairs of Nepal for BSW, BJMC, BPA and Economics entrance questions', 'BFA applicants should build a sketching/still life portfolio and practise timed studio drawing', 'Check entrance notices at fohss.tu.edu.np and cdpa.edu.np after NEB Grade 12 results'],
     'note': 'Required for specialized 4 year TU bachelor programmes (BPA at Balkhu, BFA at Lalitkala/Sirjana, and BSW/BJMC/Psychology at selective campuses); entrance fee is about NPR 1,500.',
     'prep_hours': 80, 'fee': 1500, 'apply': [8, 9], 'exam_month': 9},
    {'id': 'e-fohss-master', 'track': 'ent_biz', 'name': 'TU Master and Postgraduate Entrance Exam (MBS, MA, MSW, MPA, MEd, LLM, MPhil, PhD)',
     'level': 'Master (MBS, MA, MSW, MPA, MEd, LLM) and MPhil / PhD at Tribhuvan University',
     'need': 'Bachelor degree in the relevant or eligible discipline (BBS/BBA/any Bachelor for MBS; LL.B/BA LL.B for LLM; BEd for MEd; any Bachelor for MA/MSW/MPA; Master with CGPA 3.0 or Second Division for MPhil/PhD)',
     'age': 'No upper age limit', 'body': 'Tribhuvan University Faculties of Management (FOM), Humanities (FoHSS), Law (FoL) and Education (FoE)',
     'stages': [
         ['Faculty Central Entrance Examination (100 marks)', 'MBS uses the 100 mark FOM CMAT (Verbal, Quantitative, Logical, General Awareness); LLM uses the 100 mark Faculty of Law entrance; MA/MSW/MPA/MEd use faculty written tests.', '100'],
         ['Research proposal defense and interview (MPhil / PhD and selective Masters)', 'Statement of purpose, research synopsis assessment and oral interview at the Central Department.', '30'],
     ],
     'subjects': ['Verbal ability, quantitative aptitude, logical reasoning and business/general awareness (for MBS CMAT and MPA)', 'Constitutional law, jurisprudence, criminal law, commercial law and international law (for LLM 70 MCQ + 30 subjective entrance)', 'Discipline theory, research methodology and academic writing (for MA, MSW, MEd, MPhil and PhD)'],
     'prep': ['For MBS, practise 100 question FOM CMAT papers; for LLM at Nepal Law Campus, revise the 70 mark MCQ + 30 mark subjective law syllabus thoroughly', 'For MPhil and PhD, prepare a 2,500 word research concept note aligned with your Central Department supervisor areas', 'Apply online via fomcd.tu.edu.np, fohss.tu.edu.np, fol.edu.np or tufoe.edu.np during the Mangsir/Poush admission call'],
     'note': 'Entrance fees range from NPR 1,500 (MA, MBS, MEd, MPA, MSW) to NPR 2,000 to 3,500 (LLM, MPhil and PhD).',
     'prep_hours': 120, 'fee': 1500, 'apply': [11, 1], 'exam_month': 1},
    {'id': 'e-purbanchal', 'track': 'ent_sci', 'name': 'Purbanchal University Central Bachelor and Master Entrance Exam (PUFOST / PUFOM / PUFHS)',
     'level': 'BE (Civil, Computer, Biomedical, Geomatics), BTech Food, BFDM Fashion, BCA/BIT and MCA / MPharm / MPH / LLM',
     'need': '+2 Science with 45 percent or C grade in Physics, Chemistry and Mathematics (or Biology for Biomedical/BTech Food) for BE/BTech; +2 in any stream for BFDM Fashion Design, BBA and BHM; relevant Bachelor for MCA, MPharm, MPH and LLM',
     'age': 'No upper age limit', 'body': 'Purbanchal University Examination Management Office and Faculty Deans (Biratnagar / Gothgaun, Morang)',
     'stages': [
         ['Written Entrance Test (2 hours, 100 marks)', '100 objective MCQs (English, Mathematics, Physics and Chemistry for Engineering/IT; Aptitude, English and GK for Management/Fashion; Undergraduate core for Masters); pass mark 40.', '100'],
         ['University scholarship and college merit admission', 'Central merit list allocates the 10 percent Purbanchal University scholarship quota (5 percent open merit + 5 percent reserved/community school) and 90 percent paying seats.', '0'],
     ],
     'subjects': ['Grade 11 and 12 Mathematics, Physics, Chemistry and English (for BE Civil, Computer, Electronics, Geomatics, Biomedical and BTech Food)', 'Creative design aptitude, drawing, general awareness and English (for Bachelor of Fashion Design and Management BFDM)', 'Programming, mathematics and logical reasoning (for BCA, BIT and MCA)'],
     'prep': ['Apply for the central Purbanchal University scholarship quota alongside the regular entrance form to compete for the 10 percent tuition waiver seats', 'BE Biomedical Engineering (College of Biomedical Engineering and Applied Sciences) accepts both Mathematics and Biology group +2 Science students', 'Submit the online entrance form at puexam.edu.np or pufost.edu.np'],
     'note': 'Covers 21 engineering colleges (2,938 seats), College of Biomedical Engineering, CAFODAT (BTech Food), Namuna College of Fashion Technology (BFDM) and PU master programmes; entrance fee is NPR 1,500 to 2,000.',
     'prep_hours': 110, 'fee': 1500, 'apply': [8, 9], 'exam_month': 9},
    {'id': 'e-acca', 'track': 'lic', 'name': 'ACCA (Association of Chartered Certified Accountants) Qualification Exams',
     'level': 'Global Chartered Certified Accountant qualification (13 exams + Ethics Module + 36 months PER)',
     'need': '+2 with at least 65 percent in two subjects and 50 percent in three others (including English and Mathematics/Accounts) for direct ACCA Qualification entry; or Foundations in Accountancy (FIA) route after SEE/+2; BBS/BBA/MBS and CA students receive up to 4 to 9 paper exemptions',
     'age': '16+ years', 'body': 'ACCA Global (UK) and British Council / Approved Learning Partner CBE Centers in Kathmandu, Lalitpur and Pokhara',
     'stages': [
         ['Applied Knowledge (3 on-demand CBE papers: BT, MA, FA)', '2 hour computer based exams (100 marks, 50 percent pass mark) available any month at British Council and Gold/Platinum ALP centers in Nepal (about GBP 89 to 98 per paper).', '300'],
         ['Applied Skills (6 session CBE papers: LW, PM, TX, FR, AA, FM)', '3 hour session computer based exams held in March, June, September and December (100 marks, 50 percent pass mark; standard fee GBP 160 to 173 per paper in 2026).', '600'],
         ['Strategic Professional (SBL, SBR + 2 options from AFM, APM, ATX, AAA) and PER', 'Four strategic case/professional exams (GBP 208 to 295 per paper), the online Ethics and Professional Skills Module (EPSM, GBP 83) and 36 months signed Practical Experience Requirement (PER).', '400'],
     ],
     'subjects': ['Business and Technology (BT), Management Accounting (MA), Financial Accounting (FA) and Corporate and Business Law (LW)', 'Performance Management (PM), Taxation (TX), Financial Reporting (FR), Audit and Assurance (AA) and Financial Management (FM)', 'Strategic Business Leader (SBL), Strategic Business Reporting (SBR), Advanced Financial Management (AFM) and Advanced Audit (AAA)'],
     'prep': ['Check the official ACCA Exemption Calculator before registering: TU BBS/BBA/MBS graduates and ICAN CAP-II/CA qualifiers can claim 4 to 9 exemptions', 'Sit Applied Knowledge (BT, MA, FA) and Corporate Law (LW) as on-demand CBEs at your own pace before booking quarterly Applied Skills sessions', 'Pair ACCA study with a BBS or BSc (Hons) Applied Accounting degree if you later plan to sit Nepal Lok Sewa or TU equivalence'],
     'note': 'Per the 2026 ACCA fee schedule: initial registration is GBP 89, annual student subscription is GBP 140, EPSM is GBP 83, Applied Knowledge papers cost about GBP 89 to 98, Applied Skills GBP 160 to 173, and Strategic Professional GBP 208 to 295 (total UK fees about GBP 2,750 / NPR 475,000 for all 13 papers before tuition).',
     'prep_hours': 900, 'fee': 15500, 'apply': [1, 12], 'career': 'chartered-accountant'},
]

GOVT_ADD = GOVT_ADD_A + GOVT_ADD_B
