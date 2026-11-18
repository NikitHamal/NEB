"""Wave 21 part 2 (w21_more.py): National Investigation Department (NID), Mid-West / Far-Western University Central Entrance, and
DELF/DALF/TCF French exams at Alliance Francaise Kathmandu; 8 more country-specific scholarships (Hungary, Malaysia, Turkiye, Russia,
UAE, Czechia, Romania, Bangladesh); 25 more verified scholarship award counts; Nepal Mountain Academy (NMA) BMS seats and fee; and
8 FAQs (fw21-23 to fw21-30).

Sources (read 19 November 2026): National Investigation Department (nidept.gov.np, collegenp.com, loksewapost.com); Alliance Francaise
de Katmandou 2026 official DELF/DALF tariff (alliancefrancaise.org.np/official-diplomas/); Nepal Mountain Academy BMS 30 seats and
NPR 600,000 fee (nma.gov.np, english.nepalnews.com); CEU & Debrecen Hungary (ceu.edu, edu.unideb.hu); MTCP Malaysia (kln.gov.my);
Koc & Sabanci Turkiye (ku.edu.tr); Open Doors & Skoltech Russia (od.globaluni.ru, skoltech.ru); Khalifa University & NYUAD UAE (ku.ac.ae);
Masaryk & Charles University Czechia (muni.cz, cuni.cz); Transilvania University of Brasov Romania (unitbv.ro); Asian University for
Women Bangladesh (auw.edu.bd).
"""

GOVT_MORE = [
    {'id': 'g-nid', 'track': 'sec', 'name': 'National Investigation Department (Rastriya Anusandhan Bibhag, NID) Officer and Assistant Exam',
     'level': 'Investigation Officer (Anusandhan Adhikrit, Gazetted Third Class), Investigation Assistant (Anusandhan Sahayak, Non-Gazetted Second Class) and Sahayak Suchak',
     'need': 'Bachelor degree in any discipline for Investigation Officer; +2 (minimum CGPA 2.0) for Investigation Assistant; SEE/SLC (minimum GPA 2.0) for Sahayak Suchak',
     'age': 'Investigation Officer: 21 to 25 years for men, 21 to 30 years for women; Investigation Assistant: 18 to 25 years for men, 18 to 30 years for women; Sahayak Suchak: 18 to 25 years (up to 35 years for permanent NID staff)',
     'body': 'National Investigation Department (Office of the Prime Minister and Council of Ministers) and Lok Sewa Aayog',
     'stages': [
         ['First Phase: General Knowledge and General Ability (IQ) Preliminary Test', 'Objective MCQ screening test on General Knowledge and IQ conducted by Lok Sewa Aayog.', '100'],
         ['Second Phase: Written Examination', 'Descriptive written papers on national security, constitution, intelligence fundamentals, analytical writing and contemporary affairs.', '200'],
         ['Third Phase: Detailed Health Check, Psychological Test, Group Test, Presentation and Interview', 'Medical examination, psychological/aptitude evaluation, group discussion and presentation (for Officer) and final oral interview.', '60'],
     ],
     'subjects': ['Constitution of Nepal, Nepal Special Service Act 2042, national security policy, geopolitics and contemporary security challenges', 'General knowledge, analytical IQ, logical reasoning, drafting and report writing', 'Intelligence gathering, counter-intelligence, cyber and economic security basics'],
     'prep': ['Verify the strict age cutoff (21 to 25 for male Officer candidates and 18 to 25 for male Assistant candidates on Baishakh 1 of the vacancy year)', 'Practise timed IQ and GK preliminary papers before focusing on national security essays and report writing', 'Apply online via nidept.gov.np/career and pay the exam fee via ConnectIPS, eSewa or Rastriya Banijya Bank'],
     'note': 'Application fee is NPR 1,000 (+ NPR 200 per inclusive group) for Investigation Officer, NPR 300 (+ NPR 60 per inclusive group) for Investigation Assistant, and NPR 150 (+ NPR 30 per inclusive group) for Sahayak Suchak.',
     'prep_hours': 300, 'fee': 1000, 'career': 'security-officer'},
    {'id': 'e-mwu-fwu', 'track': 'ent_sci', 'name': 'Mid-West University (MWU) and Far-Western University (FWU) Central Entrance Exam',
     'level': 'Bachelor and Master entrance in Engineering (BE Civil, Computer, Hydropower), BSc CSIT, Agriculture, Law (BA LL.B), BBA and BHM',
     'need': '+2 Science with at least 45 percent or C grade in Physics, Chemistry and Mathematics (or Biology for BSc Ag / Health) for BE, BSc CSIT and BSc Ag; +2 in any stream with CGPA 1.8 / 45 percent for BBA, BHM and BA LL.B',
     'age': 'No upper age limit', 'body': 'Mid-West University (Birendranagar, Surkhet) and Far-Western University (Mahendranagar, Kanchanpur)',
     'stages': [
         ['Written Objective Entrance Examination (2 hours)', '100 multiple choice questions (100 marks) covering English, Mathematics, Physics/Chemistry (for Engineering/Science/Ag) or Verbal, Quantitative, Logical and Legal/General Aptitude (for BBA/BHM/BA LL.B); pass mark 40.', '100'],
         ['Central merit list, scholarship allocation and interview', 'Merit list allocates 10 to 20 percent university scholarship seats (jehendar and inclusive quotas across Karnali and Sudurpashchim provinces) and regular low-fee constituent seats.', '0'],
     ],
     'subjects': ['Grade 11 and 12 Physics, Chemistry, Mathematics and English (for BE Civil, Computer, Hydropower and BSc CSIT)', 'Botany, Zoology, Chemistry and Agriculture basics (for 4 year BSc Agriculture at Tikapur and constituent campuses)', 'English, Nepali, General Awareness, Quantitative Aptitude and Legal/Management Reasoning (for BA LL.B, BBA and BHM)'],
     'prep': ['Apply directly to constituent campuses in Surkhet (MWU) or Mahendranagar/Tikapur (FWU) where 4 year engineering and agriculture fees are among the lowest in Nepal', 'Prepare provincial and national GK alongside +2 core subjects', 'Submit your online entrance form at mwu.edu.np or fwu.edu.np during the Bhadra/Ashwin admission window'],
     'note': 'Entrance fee is NPR 1,000 to 1,500 across Mid-West University and Far-Western University faculties.',
     'prep_hours': 100, 'fee': 1200, 'apply': [8, 9], 'exam_month': 9},
    {'id': 'l-delf-tcf', 'track': 'lang_oth', 'name': 'DELF / DALF and TCF / TEF (French Language Proficiency Exams)',
     'level': 'Official French Ministry of Education diplomas (CEFR A1, A2, B1, B2, C1, C2) and TCF / TEF for France and Canada',
     'need': 'Open to all candidates with a valid passport or citizenship certificate',
     'age': 'No age limit (DELF Prim for ages 7 to 11, DELF Junior for ages 12 to 18, DELF/DALF Tout Public for adults)',
     'body': 'France Education International and Alliance Francaise de Katmandou (Pulchowk, Lalitpur)',
     'stages': [
         ['Written Comprehension, Listening Comprehension and Written Production', 'Group written examination testing listening (25 marks), reading comprehension (25 marks) and essay/letter writing (25 marks).', '75'],
         ['Individual Oral Production and Interaction', '15 to 30 minute one-on-one speaking examination with certified Alliance Francaise examiners (25 marks; minimum 50 out of 100 overall and at least 5 out of 25 in each skill required to pass).', '25'],
     ],
     'subjects': ['Listening comprehension of French dialogues, broadcasts and lectures (25 marks)', 'Reading comprehension of informational and argumentative French texts (25 marks)', 'Structured French written production (25 marks) and oral presentation/debate (25 marks)'],
     'prep': ['DELF B2 is the standard requirement for French taught programmes in France (Campus France) and waives language re-testing for life', 'For Canada Express Entry Francophone Mobility / French category draws, register for TEF Canada or TCF Canada and target NCLC 7 (CEFR B2)', 'Register at alliancefrancaise.org.np (Pulchowk, Lalitpur) during the quarterly session windows'],
     'note': 'Per the official 2026 Alliance Francaise de Katmandou fee schedule: DELF A1 costs NPR 5,775 (AFK student NPR 4,917), A2 NPR 6,490 (NPR 5,555), B1 NPR 7,315 (NPR 6,215), B2 NPR 8,085 (NPR 6,875), DALF C1 NPR 9,922 (NPR 7,700) and DALF C2 NPR 10,670 (NPR 9,075). DELF/DALF diplomas are valid for life.',
     'prep_hours': 220, 'fee': 8085},
]

SCHOLARSHIPS_MORE = [
    {'id': 's-ceu-debrecen-hu', 'name': 'Central European University (CEU) Master Excellence and University of Debrecen Merit Scholarships',
     'by': 'Central European University and University of Debrecen (Hungary)', 'type': 'University', 'country': 'hu',
     'open': [10, 2], 'awards': 200,
     'who': 'International students admitted to an English taught Master or PhD programme at CEU or Bachelor/Master/PhD at the University of Debrecen',
     'covers': 'Up to 100 percent tuition waiver, health insurance and monthly stipend of EUR 320 to EUR 1,000 plus housing at CEU; 30 percent to 90 percent tuition reduction under the University of Debrecen International Merit Scholarship',
     'how': 'Submit your online admission application with financial aid selected by 1 February (CEU scholarship deadline) or apply via edu.unideb.hu alongside Stipendium Hungaricum.'},
    {'id': 's-mtcp-taylors-my', 'name': 'Malaysian Technical Cooperation Programme (MTCP) Scholarship and University Merit Waivers',
     'by': 'Ministry of Foreign Affairs Malaysia (MTCP) and Malaysian Private Universities (Monash Malaysia, Taylor, APU)', 'type': 'Government', 'country': 'my',
     'open': [5, 7], 'awards': 100,
     'who': 'Citizens of MTCP partner developing countries (including Nepal) aged under 45 with at least CGPA 3.5 / Second Class Upper Bachelor degree and IELTS 6.0 / TOEFL iBT 60 applying for full time Master study in Malaysia',
     'covers': '100 percent tuition fee waiver at 24 public and private Malaysian universities, monthly living allowance of MYR 3,500, and return economy airfare under MTCP; 25 percent to 100 percent tuition waivers at Monash Malaysia, Taylor University and APU',
     'how': 'Secure an admission offer from an eligible Malaysian university and submit the online MTCP application through the Ministry of Foreign Affairs Malaysia portal between May and July.'},
    {'id': 's-koc-sabanci-tr', 'name': 'Koc University, Sabanci University and Bilkent University International Scholarships',
     'by': 'Koc University, Sabanci University and Bilkent University (Turkiye)', 'type': 'University', 'country': 'tr',
     'open': [12, 5], 'awards': 250,
     'who': 'International students applying to English taught Bachelor, Master or PhD programmes at leading Turkish foundation universities',
     'covers': '100 percent tuition waiver, free dormitory accommodation (or housing allowance), health insurance and monthly stipend (TRY 18,000 to TRY 35,000/month for MS and PhD fellows at Koc and Sabanci); 25 percent to 100 percent undergraduate merit tuition waivers at Bilkent',
     'how': 'No separate scholarship form is required at Koc or Sabanci: apply directly on the university online admission portal with SAT/ACT (undergraduate) or GRE/GPA (graduate) before the May deadline.'},
    {'id': 's-skoltech-hse-ru', 'name': 'Open Doors Russian Olympiad Scholarship and Skoltech / HSE University Fellowships',
     'by': 'Global Universities Association (Russia), Skolkovo Institute of Science and Technology (Skoltech) and HSE University', 'type': 'Government', 'country': 'ru',
     'open': [9, 12], 'awards': 500,
     'who': 'International Bachelor, Master and PhD applicants competing in the online Open Doors International Olympiad or applying to English taught STEM programmes at Skoltech and HSE Moscow',
     'covers': '100 percent state-funded tuition waiver across 24 leading Russian research universities (in English or Russian with a free 1 year prep year) via Open Doors; full tuition waiver, medical insurance and RUB 40,000/month MSc stipend (up to RUB 75,000/month PhD) at Skoltech',
     'how': 'Register online at od.globaluni.ru between September and December to complete the portfolio and online proctored Olympiad rounds, or apply directly at skoltech.ru by July.'},
    {'id': 's-khalifa-nyuad-ae', 'name': 'Khalifa University Graduate Fellowship and NYU Abu Dhabi Need-Blind Financial Aid',
     'by': 'Khalifa University and New York University Abu Dhabi (United Arab Emirates)', 'type': 'University', 'country': 'ae',
     'open': [10, 4], 'awards': 200,
     'who': 'International undergraduate applicants to NYU Abu Dhabi and Master/PhD/MD applicants to Khalifa University in Abu Dhabi',
     'covers': '100 percent tuition waiver, free university accommodation or housing support, UAE visa/medical insurance, return flights and monthly stipend of AED 4,000 to AED 8,000 (Master) or AED 10,000 to AED 12,000 (PhD) at Khalifa University; up to 100 percent demonstrated need aid (tuition, room, board, flights) at NYU Abu Dhabi',
     'how': 'Apply online at ku.ac.ae for Master/PhD admission (autumn deadline April) or submit the Common Application plus CSS Profile to NYU Abu Dhabi by the Early Decision (November) or Regular Decision (January) deadline.'},
    {'id': 's-charles-masaryk-cz', 'name': 'Masaryk University, Charles University and JCMM South Moravian International Scholarships',
     'by': 'Masaryk University (Brno), Charles University (Prague) and JCMM South Moravian Centre for International Mobility (Czechia)', 'type': 'University', 'country': 'cz',
     'open': [11, 4], 'awards': 120,
     'who': 'Non-EU international students enrolling in English taught or Czech taught degree programmes in Brno and Prague',
     'covers': 'CZK 50,000 to CZK 100,000 first year merit grants and dean tuition reductions at Masaryk University and Charles University, plus 100 percent free tuition across all Czech public universities for students who complete a 1 year Czech language preparatory course and study in Czech',
     'how': 'Apply for degree admission on muni.cz or cuni.cz between November and April and submit the faculty scholarship or JCMM Brno PhD Talent application.'},
    {'id': 's-transilvania-ro', 'name': 'Academica Transilvania Scholarship and Politehnica Bucharest International Waivers',
     'by': 'Transilvania University of Brasov and National University of Science and Technology Politehnica Bucharest (Romania)', 'type': 'University', 'country': 'ro',
     'open': [2, 4], 'awards': 35,
     'who': 'Non-EU international students applying for full Bachelor, Master or PhD degree programmes at Transilvania University of Brasov or Politehnica Bucharest',
     'covers': 'Full tuition fee waiver, free on-campus dormitory accommodation (including summer holidays), RON 800/month food allowance during the academic year, medical assistance and up to RON 4,000 annual return airfare grant at Transilvania University of Brasov',
     'how': 'Submit your online dossier (academic transcripts, CV, motivation letter and two recommendation letters) at unitbv.ro before the late April deadline.'},
    {'id': 's-auw-iut-bd', 'name': 'Asian University for Women (AUW Chittagong) and IUT OIC / SAARC Merit Scholarships',
     'by': 'Asian University for Women (Chittagong) and Islamic University of Technology / Bangladeshi Universities', 'type': 'University', 'country': 'bd',
     'open': [11, 3], 'awards': 100,
     'who': 'Nepali female +2 graduates with strong academic records and leadership potential applying to Asian University for Women (Chittagong), plus SAARC merit applicants to Bangladeshi engineering and medical universities',
     'covers': 'Up to 100 percent full ride coverage of tuition, residential accommodation, meals, textbooks, primary health care and return travel at Asian University for Women (Chittagong)',
     'how': 'Apply online at auw.edu.bd between November and March and sit the regional written entrance assessment and interview conducted for Nepal applicants.'},
]

SCHOLARSHIP_EXTRA_MORE = {
    's-chevening': {'awards': 1500},
    's-kgsp': {'awards': 2200},
    's-sh': {'awards': 4500},
    's-turkiye': {'awards': 5000},
    's-erasmus': {'awards': 2500},
    's-eiffel': {'awards': 350},
    's-sisgp': {'awards': 375},
    's-jjwbgsp': {'awards': 200},
    's-humphrey': {'awards': 150},
    's-nawa': {'awards': 400},
    's-romania-govt': {'awards': 85},
    's-vanier-ca': {'awards': 166},
    's-ernst-mach-at': {'awards': 100},
    's-osce-bishkek': {'awards': 60},
    's-latvia-state': {'awards': 100},
    's-czech': {'awards': 80},
    's-kz-govt': {'awards': 550},
    's-australia': {'awards': 1000},
    's-swiss': {'awards': 180},
    's-manaaki': {'awards': 650},
    's-taiwan': {'awards': 450},
    's-singa': {'awards': 240},
    's-koica': {'awards': 350},
    's-sau': {'awards': 150},
    's-mbzuai': {'awards': 150},
}

ROUTE_SEATS_MORE = {
    'p-nma': {'bms-mountaineering': 30},
}

FEES_MORE = {
    'p-nma': {'bms-mountaineering': [600000, 600000]},
}

PROVIDER_NOTE_MORE = {
    'p-nma': 'Government academy under the Ministry of Culture, Tourism and Civil Aviation (academic complex at Bijulibazar/Thapagaun, Kathmandu and 140 hectare field campus at Garma, Solukhumbu); TU affiliated 4 year Bachelor of Mountaineering Studies (BMS) has 30 seats per batch and an 8 semester fee of NPR 6,00,000 for Nepali students (NPR 8,00,000 SAARC, NPR 12,00,000 foreign).',
}

FAQ_MORE = [
    {'id': 'fw21-23', 'topic': 'after12', 'q': 'What are the age limits and exam fees for the National Investigation Department (Rastriya Anusandhan Bibhag)?',
     'a': 'For Investigation Officer (Anusandhan Adhikrit, Bachelor required, fee NPR 1,000), male candidates must be aged 21 to 25 and female candidates 21 to 30 on Baishakh 1. For Investigation Assistant (Anusandhan Sahayak, +2 with CGPA 2.0 required, fee NPR 300), male candidates must be 18 to 25 and female candidates 18 to 30. Selection includes a Lok Sewa GK/IQ prelim, written papers, health and psychological tests, group test (Officer) and interview via nidept.gov.np.',
     'go': ['police-army', 'lok-sewa']},
    {'id': 'fw21-24', 'topic': 'abroad', 'q': 'Where can I take the official French DELF, DALF, TCF and TEF exams in Nepal and what do they cost?',
     'a': 'Alliance Francaise de Katmandou (Pulchowk, Lalitpur, alliancefrancaise.org.np) is the sole accredited center in Nepal. Per the 2026 tariff, external candidate fees are NPR 5,775 (DELF A1), NPR 6,490 (DELF A2), NPR 7,315 (DELF B1), NPR 8,085 (DELF B2), NPR 9,922 (DALF C1) and NPR 10,670 (DALF C2), with a 15 percent discount for AFK students. TCF and TEF Canada are also administered for French university and Canadian Express Entry applicants.',
     'go': ['abroad-ms', 'foreign-lang-work']},
    {'id': 'fw21-25', 'topic': 'after12', 'q': 'How many seats and what tuition fee does Nepal Mountain Academy (NMA) charge for Bachelor of Mountaineering Studies (BMS)?',
     'a': 'Nepal Mountain Academy (nma.gov.np, Bijulibazar, Kathmandu with a 140 hectare field campus in Garma, Solukhumbu) allocates 30 seats per batch for its Tribhuvan University affiliated 4 year (8 semester) Bachelor of Mountaineering Studies (BMS). Total 8 semester tuition is NPR 6,00,000 for Nepali students (NPR 8,00,000 for SAARC and NPR 12,00,000 for other international students).',
     'go': ['bms-mountaineering']},
    {'id': 'fw21-26', 'topic': 'abroad', 'q': 'What scholarships are available in Hungary beyond Stipendium Hungaricum?',
     'a': 'Central European University (CEU) offers Master Excellence and Master Distinction Scholarships covering up to 100 percent tuition, health insurance and EUR 320 to EUR 1,000 a month plus dormitory housing (deadline 1 February), while the University of Debrecen International Merit Scholarship grants 30 percent to 90 percent tuition reductions.',
     'go': ['abroad-ms']},
    {'id': 'fw21-27', 'topic': 'abroad', 'q': 'How does the Malaysian Technical Cooperation Programme (MTCP) Scholarship work for Nepali graduates?',
     'a': 'Funded by the Ministry of Foreign Affairs Malaysia, the MTCP Scholarship covers 100 percent Master tuition at 24 Malaysian universities, a MYR 3,500 monthly living allowance and return flights for citizens of developing countries (including Nepal) aged under 45 with at least a CGPA 3.5 Bachelor degree and IELTS 6.0 / TOEFL iBT 60 (application window May to July).',
     'go': ['abroad-ms']},
    {'id': 'fw21-28', 'topic': 'abroad', 'q': 'Can Nepali students win full scholarships at Koc, Sabanci or Bilkent University in Turkiye?',
     'a': 'Yes. Leading Turkish foundation universities (Koc University, Sabanci University and Bilkent University) evaluate international English-track applicants automatically for 25 percent to 100 percent tuition waivers, free dormitory rooms and graduate stipends (TRY 18,000 to TRY 35,000 a month for MS/PhD fellows at Koc and Sabanci) alongside the government Turkiye Burslari scheme.',
     'go': ['abroad-ms']},
    {'id': 'fw21-29', 'topic': 'abroad', 'q': 'What is the Open Doors Russian Olympiad Scholarship and how does Skoltech funding work?',
     'a': 'The Open Doors International Olympiad (od.globaluni.ru, September to December) is a two-round online competition that awards 100 percent state-funded tuition waivers at 24 top Russian universities for Bachelor, Master and PhD tracks without a separate embassy interview. In parallel, Skoltech (Moscow) grants admitted English-track MSc and PhD students full tuition waivers plus RUB 40,000 to RUB 75,000 a month.',
     'go': ['abroad-ms']},
    {'id': 'fw21-30', 'topic': 'abroad', 'q': 'What full scholarships are available in the UAE besides MBZUAI?',
     'a': 'Khalifa University in Abu Dhabi offers graduate research/teaching fellowships covering 100 percent tuition, medical insurance, flights and a monthly stipend of AED 4,000 to AED 8,000 (Master) or AED 10,000 to AED 12,000 (PhD), while NYU Abu Dhabi meets up to 100 percent of demonstrated financial need (tuition, housing, meals and flights) for admitted undergraduate students.',
     'go': ['abroad-ms']},
]
