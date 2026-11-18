"""Wave 22 route exam links (closing all academic/vocational routes), career licence links and 6 step-by-step guides.

Sources (read 19 November 2026): NSTB CTEVT skill testing portal (nstb.org.np); CFA Institute registration and Access Scholarship
(cfainstitute.org); British Council Nepal Cambridge A Level private candidate & CDC Sanothimi equivalence (britishcouncil.org.np);
Sainik Awasiya Mahavidyalaya & Budhanilkantha SEBS portals (bsamv.edu.np, bnks.edu.np); NEA & Nepal Telecom Lok Sewa portals
(nea.org.np, ntc.net.np); Lok Sewa Aayog Foreign Service & Revenue Service (psconline1.psc.gov.np).
"""

ROUTE_EXAM = {
    'see-general': 'e-see',
    'tvet-school': 'e-see',
    'open-school-see': 'e-see',
    'plus2-science': 'e-neb-plus2',
    'plus2-management': 'e-neb-plus2',
    'plus2-humanities': 'e-neb-plus2',
    'plus2-education': 'e-neb-plus2',
    'plus2-law': 'e-neb-plus2',
    'sanskrit-gurukul': 'e-neb-plus2',
    'a-levels': 'e-cambridge-ib',
    'bbs': 'e-tu-fom-bbs',
    'ba': 'e-fohss-bachelor',
    'bed': 'e-tu-foe-bed',
    'skill-training': 'e-nstb-skill',
    'sports-cadet-school': 'e-sainik-police-school',
    'aviation-cabin-crew': 'g-nac',
    'ingo-fellowship-route': 'e-fohss-master',
}

CAREER_LICENCE = {
    'electrician': {'name': 'NSTB / NVQS National Skill Certificate (Level 1 to 3)', 'exam': 'e-nstb-skill'},
    'bank-officer': {'name': 'NRB / Public Bank Officer Exam or CFA Charter', 'exam': 'l-cfa'},
}

GUIDES_ADD = [
    {'id': 'nstb-skill-test', 'name': 'Take the NSTB / CTEVT National Skill Test (Level 1, 2 or 3)', 'cat': 'Study',
     'steps': [
         ['Complete a 390 hour Level 1 or 1,692 hour Level 2 vocational course (or gather 1 to 2 years of documented trade work experience) and download the NOSS standard for your occupation from nstb.org.np', 1, 0, 'online'],
         ['Submit the skill test application form at an NSTB accredited testing center or CTEVT provincial office with citizenship, photos and training/experience letters', 2, 0, 'in person'],
         ['Pay the NSTB assessment fee of NPR 500 to 2,200 (waived for CTEVT/ENSSURE/municipal free quota trainees)', 1, 1000, 'in person'],
         ['Pass the 20 mark safety/theory check and 80 mark hands-on practical trade demonstration to receive your NVQS / NSTB National Skill Certificate', 14, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate and 3 passport size photos', '390 hour / 1,692 hour training certificate or employer experience verification letter', 'Fee receipt (unless covered by free government/project quota)'],
     'link': 'exam:e-nstb-skill'},
    {'id': 'cfa-nepal-register', 'name': 'Register for the CFA Level I Exam and Access Scholarship in Nepal', 'cat': 'Study',
     'steps': [
         ['Ensure you hold an international passport and either a Bachelor degree or are within 23 months of completing your 4 year Bachelor degree', 1, 0, 'in person'],
         ['Create a CFA Institute account at cfainstitute.org and apply for the CFA Access Scholarship during the scholarship window to reduce the exam fee to USD 400', 14, 0, 'online'],
         ['Register for your chosen exam window (February, May, August or November) before the Early Bird deadline (USD 990 regular or USD 400 with Access Scholarship) using an international USD card or bank swift transfer', 2, 143550, 'online'],
         ['Schedule your Prometric computer-based test appointment in Kathmandu and complete the mandatory Practical Skills Module (Python or Financial Modeling) before results release', 30, 0, 'in person'],
     ],
     'docs': ['Valid international passport (name must match CFA profile character for character)', 'University enrollment verification or Bachelor transcript', 'International USD payment card or bank draft'],
     'link': 'exam:l-cfa'},
    {'id': 'camb-alevel-nepal', 'name': 'Register for Cambridge A Levels and Obtain CDC / TU +2 Equivalence', 'cat': 'Study',
     'steps': [
         ['Select at least 3 full A Level subjects plus AS Level English General Paper (8021) so your subject combination meets the 3.5 credit CDC / Tribhuvan University equivalence rule', 1, 0, 'in person'],
         ['Enroll at an approved Cambridge A Level school or register as a Private Candidate on britishcouncil.org.np for the May/June or October/November exam series', 3, 75000, 'online'],
         ['Sit your written and practical lab papers at the British Council Kathmandu examination venue and collect your official Statement of Results and Cambridge certificate', 60, 0, 'in person'],
         ['Submit your SEE and Cambridge A Level certificates at the Curriculum Development Centre (CDC, Sanothimi, Bhaktapur) to receive your Class 12 (+2) equivalence letter', 3, 1000, 'in person'],
     ],
     'docs': ['Valid passport or citizenship certificate', 'SEE gradesheet and character certificate', 'Official Cambridge Statement of Results and A Level certificate'],
     'link': 'exam:e-cambridge-ib'},
    {'id': 'sainik-school-apply', 'name': 'Apply for Sainik Awasiya Mahavidyalaya, Police School or Budhanilkantha Scholarship', 'cat': 'Applications',
     'steps': [
         ['Watch for the annual Chaitra/Baisakh notice (Class 5/6 entry) or Ashadh post-SEE notice (Class 11 +2 Science/Management entry) on bsamv.edu.np, nps.edu.np and bnks.edu.np', 1, 0, 'online'],
         ['For the 100 percent free Budhanilkantha SEBS Ministry scholarship, submit the community school verification and parental income/remote-district form at your District EDCU', 3, 0, 'in person'],
         ['Fill the online entrance form and pay the NPR 500 to 1,000 entrance fee via ConnectIPS, eSewa or bank voucher', 1, 1000, 'online'],
         ['Sit the 100 mark written test (English, Nepali, Maths, Science, IQ) followed by medical fitness screening and interview', 14, 0, 'in person'],
     ],
     'docs': ['Birth registration certificate and parents citizenship certificates', 'Previous class gradesheet / SEE gradesheet and school character certificate', 'Service verification letter (for Army/Police personnel quota) or community school verification (for SEBS scholarship)'],
     'link': 'exam:e-sainik-police-school'},
    {'id': 'nea-ntc-apply', 'name': 'Apply for NEA (Electricity Authority) and Nepal Telecom Lok Sewa Exams', 'cat': 'Applications',
     'steps': [
         ['Check the annual Bhadra/Ashwin (NEA) and Kartik (Nepal Telecom) vacancy notices on career.nea.org.np and recruit.ntc.net.np for your qualification (Level 3/4/5 Assistant/Technician or Level 6/7 Officer/Engineer)', 1, 0, 'online'],
         ['For Level 7 Engineering posts, ensure your NEC Engineering Registration Certificate (e-nec) is issued before the application closing date', 1, 0, 'online'],
         ['Complete your online recruitment profile, upload citizenship, transcripts and inclusive quota certificates, and pay the NPR 700 to 1,200 exam fee via ConnectIPS, eSewa or Khalti', 1, 1000, 'online'],
         ['Download your admit card when Lok Sewa Aayog publishes the exam schedule and sit Paper 1 and Paper 2 followed by the interview', 45, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate and digital photo/signature', 'Academic transcripts, character certificates and NEC registration certificate (for Engineers)', 'Inclusive group certificate if applying under Samabesi quotas'],
     'link': 'exam:g-nea'},
    {'id': 'foreign-revenue-psc', 'name': 'Apply for Lok Sewa Foreign Affairs (Pararastra) and Revenue Service (Rajaswa)', 'cat': 'Applications',
     'steps': [
         ['Log in to psconline1.psc.gov.np on the last Wednesday of Mangsir (Section Officer) or Poush (Nayab Subba) when the unified Lok Sewa notice opens', 1, 0, 'online'],
         ['Tick Foreign Affairs Service (open to any Bachelor) and/or Revenue Service (open to Management, Economics, Law, Statistics or CA graduates) alongside General Administration', 1, 0, 'online'],
         ['Pay NPR 1,000 for the base Section Officer group plus NPR 400 for each additional service or inclusive cluster via ConnectIPS or eSewa', 1, 1400, 'online'],
         ['Pass the 100 mark Stage I MCQ Prelim, then sit the two common 100 mark papers plus the 100 mark specialized Foreign Service (in English) or Revenue Service paper', 60, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate', 'Bachelor (or +2 for Nayab Subba) transcript and character certificate', 'Inclusive quota certificate if claiming reserved seats'],
     'link': 'exam:g-foreign-service'},
]
