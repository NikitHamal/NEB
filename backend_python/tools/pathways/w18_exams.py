"""Wave 18 exams and guides side: six statutory professional council licensing exams in Nepal, 20 career licence links and four step by step guides.

Sources (read 18 November 2026): Nepal Engineering Council AMIS portal (register.nec.gov.np, neccomputerprep.site, veedhyapeeth.com, loksewatayariapp.com);
Nepal Medical Council NMCLE (nmc.org.np, open-exam-prep.com, richglobaledu.com, journals.sagepub.com); Nepal Nursing Council NLEN/NLEM/NSREN 2025/2082 guidelines
(nnc.org.np, educatenepal.com, collegenp.com); Nepal Pharmacy Council 30th notice (nepalpharmacycouncil.org.np, edusanjal.com, pharmainfonepal.com);
Nepal Bar Council 35th Advocate exam notice 2083 (nepalbarcouncil.org.np, edusanjal.com, legalalphabet.com); Nepal Health Professional Council (nhpc.gov.np,
therapyroute.com, smartacademyhq.com).
"""

GOVT_TRACKS_ADD = [
    {'id': 'lic', 'label': 'Council licence', 'group': 'ent'},
]

GOVT_ADD = [
    {'id': 'e-nec', 'track': 'lic', 'name': 'NEC Engineering Registration Exam', 'level': 'Mandatory licensing exam for BE and B.Arch graduates',
     'need': 'Bachelor degree in Engineering or Architecture (BE, BTech, B.Arch) from a university recognised by the Nepal Engineering Council',
     'age': '', 'body': 'Nepal Engineering Council (NEC)',
     'stages': [
         ['Computer based test', '2 hour computer based test worth 100 marks across 10 syllabus chapters (10 marks per chapter; guides describe 100 one mark MCQs or 60 one mark and 20 two mark MCQs). Minimum 50 marks (50 percent) to pass, no negative marking.', '100'],
         ['Council registration and ID card', 'After passing, pay NPR 5,000 registration fee and NPR 200 ID card charge (total NPR 5,200) on the AMIS portal to receive your NEC certificate.', '0']
     ],
     'subjects': ['Core fundamentals of your engineering discipline (chapters 1 to 4)', 'Applied engineering and design (chapters 5 to 9)', 'Project planning, professional ethics and NEC regulations (chapter 10)'],
     'prep': ['Download the exact 10 chapter syllabus for your discipline from nec.gov.np', 'Give equal study time to all 10 chapters because each chapter carries 10 marks', 'Practise 2 hour CBT mock tests and attempt every question since there is no negative marking'],
     'note': 'Mandatory since the 2023 amendment to the Nepal Engineering Council Act. The NEC AMIS portal (register.nec.gov.np) lists an examination fee of NPR 2,500 (one older guide quotes NPR 3,400 for Nepali degrees and NPR 4,400 for foreign degrees at Rastriya Banijya Bank), plus NPR 5,200 for registration and ID card after passing.',
     'prep_hours': 240, 'fee': 2500},
    {'id': 'e-nmcle', 'track': 'lic', 'name': 'NMCLE (MBBS and BDS medical licensing exam)', 'level': 'National medical and dental registration exam',
     'need': 'MBBS or BDS degree from an NMC recognised institution plus at least 6 months of compulsory rotatory internship to sit (full 1 year internship required before the certificate is issued)',
     'age': '', 'body': 'Nepal Medical Council (NMC)',
     'stages': [
         ['Computer based test', '3 hour CBT with 140 questions (130 one mark MCQs and 10 five mark Clinical Scenario Questions) for 180 total marks. Minimum 90 out of 180 (50 percent) to pass, no negative marking.', '180'],
         ['Council registration', 'Submit the completed 1 year rotatory internship certificate and original credentials to receive permanent NMC registration.', '0']
     ],
     'subjects': ['Medicine, surgery, paediatrics, obstetrics and gynaecology', 'Basic medical sciences (anatomy, physiology, pathology, pharmacology, microbiology)', 'Community medicine, medical ethics and clinical vignettes (for BDS: prosthodontics, oral surgery, conservative dentistry, orthodontics and community dentistry)'],
     'prep': ['Focus on clinical vignettes and diseases common in Nepal', 'Attempt all 130 MCQs and 10 five mark CSQs because there is no negative marking', 'Practise timed 3 hour CBT blocks as MCQs and CSQs appear in mixed order'],
     'note': 'Conducted three times a year (every four months) by the Nepal Medical Council. NMC notices list NPR 3,500 for the undergraduate NMCLE and NPR 7,000 for the postgraduate Special Examination (MD, MS, MDS). Check nmc.org.np for the current notice.',
     'prep_hours': 400, 'fee': 3500},
    {'id': 'e-nlen', 'track': 'lic', 'name': 'NLEN and NLEM (Nursing and Midwifery licence exam)', 'level': 'National licensure exam for PCL Nursing, BSc Nursing, BMS and MN/MSc',
     'need': 'Passed PCL Nursing, BSc Nursing, BNS, Bachelor in Midwifery Sciences (BMS) or Master in Nursing from a recognised institution',
     'age': '', 'body': 'Nepal Nursing Council (NNC)',
     'stages': [
         ['Written MCQ exam (CBT / paper)', '2 hours 30 minutes, 150 multiple choice questions (150 marks), no negative marking. Pass mark is 50 percent aggregate for PCL and BSc NLEN and 60 percent for Specialist Nursing NSREN (results are issued as pass or fail).', '150'],
         ['OSPE / viva (Midwifery NLEM only)', 'Midwifery (BMS) candidates also complete a practical OSPE / viva requiring at least 80 percent.', '100']
     ],
     'subjects': ['Integrated health sciences, anatomy and physiology', 'Medical surgical nursing and fundamentals of nursing', 'Community health, child health, mental health and midwifery'],
     'prep': ['Cover all nursing specialties according to the NNC test guideline weightings', 'Leave no question blank because there is no minus marking', 'Keep all original transcripts and citizenship ready for verification when collecting the certificate'],
     'note': 'Held three times a year via application.nnc.org.np. The 2025/2082 NNC guidelines list exam fees of NPR 3,500 for PCL and BSc Nursing NLEN, NPR 4,100 for BMS Midwifery NLEM and NPR 5,100 for Specialist Nursing NSREN (double in the late window), plus NPR 2,000 registration certificate fee after passing (an older 2021 page quotes NPR 1,600 and NPR 800). From Magh 1, 2082 license renewal requires 60 CPD credit hours over six years.',
     'prep_hours': 220, 'fee': 3500},
    {'id': 'e-npc', 'track': 'lic', 'name': 'NPC Pharmacy Licensure Exam (BPharm and Diploma)', 'level': 'Pharmacist and Pharmacy Assistant registration exam',
     'need': 'Diploma in Pharmacy (for Pharmacy Assistant) or Bachelor in Pharmacy (BPharm, for Pharmacist) from an NPC recognised institution with curriculum internship completed',
     'age': '', 'body': 'Nepal Pharmacy Council (NPC)',
     'stages': [
         ['Licensure examination', '100 multiple choice questions (100 marks). Minimum 50 marks (50 percent) required to pass.', '100'],
         ['Name registration certificate', 'Pay the NPR 3,000 registration certificate fee after passing and verify certified documents.', '0']
     ],
     'subjects': ['Pharmaceutics, pharmacology and clinical pharmacy', 'Pharmaceutical chemistry, pharmacognosy and quality analysis', 'Forensic pharmacy, drug act, hospital pharmacy and dispensing ethics'],
     'prep': ['Study the Nepal Drug Act, hospital pharmacy standards and dosage calculations carefully', 'Practise 100 question MCQ sets from past NPC exam cycles', 'Prepare certified copies of all academic, internship and equivalence certificates before the portal opens'],
     'note': 'Held three times a year via onlinenameregistration.nepalpharmacycouncil.org.np. The 30th NPC notice lists an exam fee of NPR 3,000 (deposited at Nabil Bank) and NPR 3,000 for the registration certificate after passing.',
     'prep_hours': 200, 'fee': 3000},
    {'id': 'e-bar', 'track': 'lic', 'name': 'Nepal Bar Council Advocate (Adhibakta) License Exam', 'level': 'National legal practice licensing exam',
     'need': 'Bachelor degree in Law (BA LLB, BBA LLB or 3 year LLB) from a recognised university, or 7 years continuous practice as a Pleader (Abhibakta)',
     'age': '', 'body': 'Nepal Bar Council',
     'stages': [
         ['Paper 1: Constitution and Law (MCQs)', '100 marks, 1 hour 30 minutes. Pass mark is 50 out of 100.', '100'],
         ['Paper 2: Legal Translation and Drafting (Masyouda)', 'Part A Legal Translation (English and Nepali, 10 marks, 30 minutes) and Part B Legal Drafting of civil, criminal and writ petitions (90 marks, 3 hours 30 minutes). Combined pass mark is 50 out of 100.', '100'],
         ['Oral interview and Bar Oath', 'Candidates who pass both written papers attend the viva and take the Bar Oath to receive the Advocate licence.', '0']
     ],
     'subjects': ['Constitution of Nepal, Muluki Civil and Criminal Codes and Evidence Act', 'Procedural law, court rules, corporate law and professional ethics', 'Bilingual legal translation and drafting of plaints, written statements, appeals and writ petitions'],
     'prep': ['Practise handwriting complete civil, criminal and writ drafts (Masyouda) within the 3.5 hour time limit', 'Read the Muluki Codes, Evidence Act and landmark Supreme Court precedents for Paper 1 MCQs', 'Keep your email and password on exam.nepalbarcouncil.com safe as the same account is used across cycles'],
     'note': 'The 35th Advocate Level Exam notice (Shrawan to Bhadra 2083 / August to September 2026) lists a total form and exam fee of NPR 4,500 at Siddhartha Bank (double fee in the 7 day late window). Apply at exam.nepalbarcouncil.com.',
     'prep_hours': 300, 'fee': 4500, 'apply': [8, 9]},
    {'id': 'e-nhpc', 'track': 'lic', 'name': 'NHPC Health Professional Licensing Exam', 'level': 'Certificate, bachelor and master health professional registration exam',
     'need': 'Approved PCL (HA, CMLT, Radiography, Ophthalmic, Dental, Physio), Bachelor (BPH, BMLT, BPT, BSc MIT, BOptom, BASLP, Perfusion) or Master / MPhil Clinical Psychology qualification',
     'age': '', 'body': 'Nepal Health Professional Council (NHPC)',
     'stages': [
         ['Computer based test', '2 hour CBT tailored to your specific health qualification level and faculty syllabus. Minimum 50 percent required to pass.', '100'],
         ['Council registration', 'Pay the level registration fee (higher for foreign qualifications) and submit verified credentials.', '0']
     ],
     'subjects': ['Qualification specific clinical and diagnostic subjects from the NHPC syllabus', 'Primary health care, community health and infection control', 'NHPC Act, code of ethics and patient safety'],
     'prep': ['Download the exact PCL, bachelor or master syllabus for your subject from nhpc.gov.np', 'Practise 2 hour computer based mock tests in your discipline', 'Foreign graduates must obtain TU equivalence and submit their course curriculum with the form'],
     'note': 'NHPC notices list a standard examination fee of NPR 3,000 across certificate, bachelor and master levels (doubled to NPR 6,000 in the late registration window).',
     'prep_hours': 180, 'fee': 3000},
]

CAREER_LICENCE = {
    'civil-engineer': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'architect': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'electrical-engineer': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'mechanical-engineer': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'geomatics-engineer': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'electronics-engineer': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'biomedical-engineer': {'name': 'Nepal Engineering Council registration', 'exam': 'e-nec'},
    'doctor': {'name': 'Nepal Medical Council registration', 'exam': 'e-nmcle'},
    'dentist': {'name': 'Nepal Medical Council registration', 'exam': 'e-nmcle'},
    'nurse': {'name': 'Nepal Nursing Council licence', 'exam': 'e-nlen'},
    'midwife-specialist': {'name': 'Nepal Nursing Council licence', 'exam': 'e-nlen'},
    'pharmacist': {'name': 'Nepal Pharmacy Council registration', 'exam': 'e-npc'},
    'lawyer': {'name': 'Nepal Bar Council licence', 'exam': 'e-bar'},
    'lab-tech': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
    'health-assistant': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
    'physiotherapist': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
    'optometrist': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
    'radiographer': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
    'speech-audiologist': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
    'perfusionist-anesthesia': {'name': 'Nepal Health Professional Council registration', 'exam': 'e-nhpc'},
}

ROUTE_EXAM = {
    'council-license': 'e-nec',
    'llb': 'e-bar',
    'ba-llb': 'e-bar',
}

GUIDES_ADD = [
    {'id': 'nec-licence', 'name': 'NEC engineering licence exam and registration', 'cat': 'Study',
     'steps': [
         ['Check that your university and BE or B.Arch course are on the NEC recognised list at nec.gov.np (get TU equivalence first if you studied abroad)', 2, 0, 'online'],
         ['Create an account on register.nec.gov.np, upload notarised transcripts, citizenship and photos, and pay the NPR 2,500 exam fee via Khalti or ConnectIPS', 1, 2500, 'online'],
         ['Download your admit card and sit the 2 hour 100 mark computer based test (pass mark 50)', 1, 0, 'in person'],
         ['After passing, pay NPR 5,000 registration and NPR 200 ID card fee on the portal and collect your NEC certificate', 7, 5200, 'in person'],
     ],
     'docs': ['Citizenship certificate (notarised)', 'SEE and +2 transcripts and character certificates', 'Bachelor transcript, provisional or degree certificate and character certificate', 'TU equivalence certificate (if foreign degree)', 'Passport size photos'],
     'link': 'exam:e-nec'},
    {'id': 'nmcle-licence', 'name': 'Nepal Medical Council (NMCLE) licence application', 'cat': 'Study',
     'steps': [
         ['Complete your MBBS or BDS degree and at least 6 months of compulsory rotatory internship', 1, 0, 'in person'],
         ['Apply online at nmc.org.np when the NMCLE window opens (held every 4 months) and pay the NPR 3,500 exam fee', 1, 3500, 'online'],
         ['Sit the 3 hour 180 mark CBT (130 MCQs and 10 Clinical Scenario Questions; pass mark 90)', 1, 0, 'in person'],
         ['Submit your full 1 year internship completion certificate and original documents at NMC Bansbari for registration', 7, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate', 'SEE, +2 and MBBS or BDS transcripts and certificates', 'Internship completion certificate (minimum 6 months to sit, 12 months to register)', 'MEC eligibility / equivalence letter (for foreign graduates)'],
     'link': 'exam:e-nmcle'},
    {'id': 'nnc-licence', 'name': 'Nepal Nursing Council (NLEN) licence registration', 'cat': 'Study',
     'steps': [
         ['Open an applicant profile at application.nnc.org.np and upload white background photo, citizenship and nursing transcripts', 1, 0, 'online'],
         ['Pay the exam fee online (NPR 3,500 for PCL or BSc Nursing NLEN, NPR 4,100 for BMS NLEM, NPR 5,100 for Specialist NSREN)', 1, 3500, 'online'],
         ['Sit the 2.5 hour 150 MCQ examination (pass mark 50 percent aggregate; BMS also has OSPE / viva)', 1, 0, 'in person'],
         ['Pay the NPR 2,000 registration fee online and bring original certificates and admit card to NNC Bansbari to collect your licence', 5, 2000, 'in person'],
     ],
     'docs': ['Citizenship certificate (original and copy)', 'SLC / SEE and nursing transcripts and character certificates', 'Equivalence certificate (for foreign nursing degrees)', 'Admit card and white background passport photos'],
     'link': 'exam:e-nlen'},
    {'id': 'bar-licence', 'name': 'Nepal Bar Council Advocate licence application', 'cat': 'Study',
     'steps': [
         ['Deposit the NPR 4,500 form and exam fee at Siddhartha Bank (Nepal Bar Council Aamdani Khata) with your full name and mobile number on the voucher', 1, 4500, 'in person'],
         ['Log in at exam.nepalbarcouncil.com, upload your law transcripts, citizenship and bank voucher within the regular window', 1, 0, 'online'],
         ['Download the admit card a week before the test and sit Paper 1 (100 mark MCQs) and Paper 2 (10 mark translation + 90 mark Masyouda drafting)', 2, 0, 'in person'],
         ['Pass the oral viva and take the Bar Oath to receive your Advocate certificate', 14, 0, 'in person'],
     ],
     'docs': ['Nepali citizenship certificate', 'BA LLB or LLB transcript and character certificate', 'TU equivalence certificate (if studied abroad)', 'Siddhartha Bank fee voucher'],
     'link': 'exam:e-bar'},
]
