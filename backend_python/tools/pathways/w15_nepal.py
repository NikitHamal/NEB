"""Wave 15 Nepal side: two Health Service exams, 2083/84 Lok Sewa dates, NEB and SEE calendar, FAQs. Plain sentences, no dashes.

Sources (read November 2026): Public Service Commission notices 101 and 102 of 2083/84 as reproduced by educatenepal.com (22 July 2026);
loksewaai.com (2083/84 calendar summary); loksewatayariapp.com (Staff Nurse and Health Service pages); edusanjal.com and nepalipoint.com (NEB Grade 12
routine 2083, notice of 17 February 2026); edusanjal.com (SEE 2083 registration notice); nebresult.com and nebeducation.com (SEE 2082 dates, re-exam routine).
Only secondary copies of the notices were readable, so each answer says to confirm on the official site (psc.gov.np, neb.gov.np, see.gov.np).
"""

GOVT_ADD = [
    {'id': 'g-staff-nurse', 'track': 'psc', 'name': 'Staff Nurse (Health Service)', 'level': 'Assistant fifth level, nursing group',
     'need': 'PCL in Nursing and Nepal Nursing Council registration', 'age': '18 to 45 years as quoted by prep guides; read the notice',
     'body': 'Public Service Commission (health service posts in ministry, hospital and provincial offices)',
     'stages': [['First paper', 'Objective test of 100 marks, pass mark 45. It is a screening paper and the marks do not add to the final merit.', '100'],
                ['Second paper', 'Subjective paper of 100 marks: 12 short answers (60 marks) and 4 long answers (40 marks), 2 hours 15 minutes, pass mark 40.', '100'],
                ['Interview', 'Oral interview of 30 marks. Final merit adds the written and interview marks.', '30']],
     'subjects': ['Fundamentals of nursing', 'Medical and surgical nursing', 'Community health and public health', 'Maternal and child health', 'Health policy and management'],
     'prep': ['Keep the Nepal Nursing Council licence valid before the notice closes', 'Practise past papers from the commission site', 'Read the current syllabus on psc.gov.np, which was revised in 2080'],
     'note': 'Notices appear on psc.gov.np and the commission calendar for the year; health posts follow their own dates. Fees, ages and the quota for women, Madhesi, Dalit, Janajati and disabled candidates are listed in each notice. The age and mark pattern here comes from prep guides, so check the notice before you apply.',
     'career': 'nurse'},
    {'id': 'g-health-assistant', 'track': 'psc', 'name': 'Health Assistant (Health Service)', 'level': 'Assistant fifth level, general medicine group',
     'need': 'PCL in General Medicine (Health Assistant) and Nepal Health Professional Council registration', 'age': '18 to 45 years as quoted by prep guides; read the notice',
     'body': 'Public Service Commission (health posts, hospitals and provincial offices)',
     'stages': [['Written examination', 'Objective and subjective papers on general medicine, public health and emergency care, with a first stage screening pass. The exact marks and times are in each notice.'],
                ['Interview', 'Oral interview, then the merit list.']],
     'subjects': ['General medicine', 'Public health and community health', 'Emergency care and first aid', 'Maternal and child health', 'Health policy and management'],
     'prep': ['Renew the Health Professional Council registration', 'Study the syllabus for the group on psc.gov.np', 'Practise past papers and follow notices through the year'],
     'note': 'Same Health Service route as the Staff Nurse. Health Assistants run health posts and primary care, so rural postings are common in the first years. Only the qualification, registration and the broad stages are given here; the commission notice has the dates, fee and marks.',
     'career': 'health-assistant'},
]

GOVT_NOTE_ADD = {
    'g-kharidar': 'Dates seen for 2083/84: the commission ran an open pre qualifying test for organised institutions (Sangathit Sanstha), notice 102/083-84 for Assistant second class (Kharidar level), on 4 Ashoj 2083 at 2 pm (about 21 September 2026), with applications to 26 Shrawan 2083 (11 August 2026) and a double fee window to 2 Bhadra 2083 (18 August). Age is counted on the deadline: 18 to 35, up to 40 for women and candidates with disability, and a SEE grade point of at least 2.0. A pass in this test is the entry ticket for the later main written exam of the organised institution. A calendar summary says the civil service Kharidar and Nayab Subba notices come in the first week of Shrawan and again in Baisakh, with the exams in Ashoj and Asar, so the next round is expected around Baisakh 2084. The notice has the fee.',
    'g-nayab': 'Dates seen for 2083/84: notice 101/083-84 for Assistant first class (Nayab Subba level, fifth level) in organised institutions held its open pre qualifying test on 3 Ashoj 2083 at 2 pm (about 20 September 2026); applications closed on 26 Shrawan 2083 (11 August 2026), double fee to 2 Bhadra 2083 (18 August). Age 18 to 35, up to 40 for women and candidates with disability, counted on the deadline; +2 with a grade point of at least 2.0. The calendar summary puts the next civil service round in Baisakh 2084 with exams in Asar.',
}

FAQ_ADD = [
    {'id': 'fw15-1', 'topic': 'after12', 'q': 'When were the NEB Grade 12 exams of 2083 held?', 'go': ['plus2-science', 'plus2-management'],
     'a': 'The National Examination Board published the Grade 12 routine on 17 February 2026: exams for regular and partial students in the general, technical and traditional streams ran from 14 Baisakh 2083 to 27 Baisakh 2083 (about 27 April to 10 May 2026), starting with Compulsory English and then Compulsory Nepali. Results and the improvement or partial exam dates are posted on neb.gov.np, so read the official notice before you plan your bachelor entrance forms.'},
    {'id': 'fw15-2', 'topic': 'after10', 'q': 'What are the SEE exam, result and re-exam dates?', 'go': ['see-general', 'open-school-see'],
     'a': 'The SEE of the 2082 session was held from 2 to 12 April 2026 and the result came out on 28 Baisakh 2083 (11 May 2026). The supplementary exam ran from 1 to 9 Asar 2083 (about 15 to 23 June 2026) and the grade improvement exam was set for Bhadra 2083. The next SEE is called SEE 2083: Class 9 students of the 2082 session filled the registration form from 19 Kartik to 24 Mangsir 2082, and a student must complete 14 years by the end of Chaitra 2083. Dates move, so check see.gov.np or neb.gov.np.'},
    {'id': 'fw15-3', 'topic': 'afterbach', 'q': 'What is the Lok Sewa pre qualifying test for organised institutions?', 'go': ['lok-sewa'],
     'a': 'Government owned organisations (Sangathit Sanstha) hold an open pre qualifying test before their main exam. For 2083/84, notice 101 (Nayab Subba level) was held on 3 Ashoj 2083 and notice 102 (Kharidar level) on 4 Ashoj 2083, both at 2 pm; the age bar is 18 to 35 (40 for women and candidates with disability) counted on the application deadline of 26 Shrawan 2083. Passing it lets you apply to the later main exam of the organisation. The next round is expected after Baisakh 2084 and the dates are on psc.gov.np.'},
    {'id': 'fw15-4', 'topic': 'afterbach', 'q': 'How do I become a government Staff Nurse or Health Assistant?', 'go': ['pcl-nursing', 'pcl-general-medicine', 'bsc-nursing'],
     'a': 'Both are Health Service posts at the assistant fifth level in the Lok Sewa Aayog. A Staff Nurse needs a PCL in Nursing and a Nepal Nursing Council registration; a Health Assistant needs a PCL in General Medicine and the council registration. Prep guides describe a 100 mark screening paper (pass 45), a 100 mark subjective paper (pass 40) and a 30 mark interview, with an age bar of 18 to 45; read the notice because the age and fee can change. A bachelor in nursing also opens higher posts and strong demand abroad.'},
    {'id': 'fw15-5', 'topic': 'abroad', 'q': 'How much does it cost to study in Romania?', 'go': ['abroad-ms'],
     'a': 'Agency pages quote EUR 1,700 to 4,500 a year for most degrees at public universities, EUR 5,000 to 8,500 and sometimes up to 12,000 for English taught medicine, and EUR 400 to 700 a month for living, with a student permit that lets you work about 4 hours a day. Funds of about EUR 3,000 and a residence permit fee near EUR 120 are quoted, but these are agency figures. Confirm fees in a written letter from the university and check Nepal Medical Council recognition before paying for medicine.'},
    {'id': 'fw15-6', 'topic': 'abroad', 'q': 'Can I get a Romanian government scholarship?', 'go': ['abroad-ms'],
     'a': 'Yes for bachelor, master and doctoral study in every field except medicine, dental medicine and pharmacy. It exempts tuition and registration, gives a free Romanian language year if needed, a dormitory place subject to availability and a small stipend (listings quote EUR 65, 75 and 85). The 2026/27 call ran from 16 February to 31 March 2026, so expect the next one at the same time in 2027 on scholarships.studyinromania.gov.ro.'},
    {'id': 'fw15-7', 'topic': 'abroad', 'q': 'Is Estonia a cheap option for IT?', 'go': ['abroad-ms', 'bsc-csit'],
     'a': 'It is cheaper than the UK or Australia: English taught programmes cost EUR 1,500 to 7,500 a year and living is about EUR 550 to 1,000 a month. There is no weekly work cap for students with a study permit, and graduates get 9 months to look for work, but funds for the permit are quoted at EUR 350 to 438 a month, so ask the Police and Border Guard Board. The strongest English choices are in computing and engineering at Tartu and TalTech.'},
    {'id': 'fw15-8', 'topic': 'abroad', 'q': 'What does ETH Zurich cost an international student?', 'go': ['abroad-ms', 'be-computer'],
     'a': 'Since autumn 2025 most international students at ETH and EPFL pay CHF 2,190 a semester (about CHF 4,380 a year, roughly NPR 7.7 lakh), against CHF 730 for Swiss residents. The real cost is living and the funds proof: ETH asks for CHF 21,000 a year (CHF 24,000 in Basel) in your own account, plus Swiss health insurance. Fees and the permit are set by the school and the canton, so read the ETH page before applying.'},
    {'id': 'fw15-9', 'topic': 'abroad', 'q': 'Is Cyprus worth it for a bachelor?', 'go': ['abroad-ms', 'bba'],
     'a': 'It is mostly private universities with bachelor fees of about EUR 5,500 to 11,000 a year and living of EUR 9,000 to 12,000, and agencies describe tight work limits for non EU students. It is not cheap and the degree recognition for later study or a licence in Nepal is a separate step, so ask for the written fee letter, check Tribhuvan University equivalence and compare it with Romania, Portugal or Lithuania.'},
    {'id': 'fw15-10', 'topic': 'abroad', 'q': 'Which European countries are the cheapest for Nepali students?', 'go': ['abroad-ms'],
     'a': 'On tuition plus living, agency lists put Romania, Hungary (with the Stipendium Hungaricum), Lithuania, Estonia, Czechia and Portugal ahead of the UK, Netherlands or Switzerland. Compare the whole year: tuition, living, funds proof, work rules and what happens after you graduate. Germany has low tuition but a blocked account of about EUR 11,904. Use this app to open each country and compare the notes.'},
]
