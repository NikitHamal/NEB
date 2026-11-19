"""Wave 32 abroad: four scholarships for the wave 31 destinations, a Vietnam correction, Iceland and Armenia notes.
Read on 2026-11-20. Sources: darmasiswa.kemendikdasmen.go.id (official Darmasiswa site: 111 countries since 1976, Ministry of Primary and Secondary
Education), io.uny.ac.id (UNY Darmasiswa page: aged 18 to 32, unmarried, high school diploma, programme returned in 2026 after a pause since 2024),
scholyhub.com (IDR 4,700,000 monthly allowance and book allowance, third party), pakadmissions.com (2026/27 window 15 May to 15 June, third party);
studyinvietnam.edu.vn (official Vietnam Government Scholarship application portal, its country list includes Nepal), globaladmissions.com and
titansabroad.org (VIED runs it under bilateral agreements); admissions.aua.am (AUA tuition table, AMD 4,250,000 BA in Business and 3,700,000 other
programmes for international students, merit scholarships up to 50 percent, separate international scholarship application, need based aid for
Armenian citizens only), studyu.org (AUA 2026/27 USD 11,700 to 13,080); globaladmissions.com, truescho.com and careershelpdesk.com (KAUST Fellowship:
every admitted MS and PhD student funded, stipend USD 20,000 MS and 25,000 to 30,000 PhD, deadline 3 January 2027 in one guide and 17 January or
11 April 2026 in older listings); the-updates.com and european-funding-guide.eu (Icelandic Government scholarship country list, Nepal not listed).
"""

SCHOLARSHIPS_ADD = [
    {'id': 's-darmasiswa-id', 'name': 'Darmasiswa Indonesian Scholarship (Bahasa Indonesia, arts and culture, one year, non-degree)', 'scope': 'abroad', 'levels': ['diploma'],
     'by': 'Ministry of Primary and Secondary Education of Indonesia with the Ministry of Foreign Affairs',
     'covers': 'Tuition at the host university, a monthly living allowance (IDR 4,700,000 in one third party listing; the host university UNY said the 2026 amounts were still to be announced) and a book allowance. Airfare and the visa fee are paid by you. It is a one year course, not a degree.',
     'who': 'Young people from countries that have diplomatic relations with Indonesia (the official site says more than 111 countries have taken part since 1976): unmarried, aged 18 to 32 and holding a high school diploma or equivalent (UNY page), who choose Bahasa Indonesia or an arts, music, dance or craft subject at one of about 60 host universities. No earlier Indonesian is needed.',
     'how': 'Register online on the official Darmasiswa site (darmasiswa.kemendikdasmen.go.id) and pick host universities. The programme paused after 2024 and returned for 2026; one third party page reports a 15 May to 15 June 2026 window, so expect a similar window in 2027 and read the dates on the official site.',
     'link': 'https://darmasiswa.kemendikdasmen.go.id', 'country': 'id', 'type': 'Government', 'open': [5, 6]},
    {'id': 's-vn-govt', 'name': 'Vietnam Government Scholarship (VIED, Ministry of Education and Training)', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'],
     'by': 'Vietnam International Education Development (VIED), Ministry of Education and Training of Vietnam',
     'covers': 'Tuition and a monthly living allowance; the exact amounts and subjects follow the bilateral agreement and level (guides print USD 700 to 800 a month, which no official page confirms). Many places are for programmes in Vietnamese with a language year first.',
     'who': 'Nationals of countries with an education agreement with Vietnam. The official application portal (studyinvietnam.edu.vn) lists Nepal in its country menu, so a Nepali applicant can open an application; other pages say some countries are nominated by their own ministry first and quotas are yearly, so no fixed Nepal quota is confirmed here.',
     'how': 'Create an account on studyinvietnam.edu.vn, choose level, university and subject and upload your documents. Guides place the nomination window in the first half of the year for a September or October start; the dates change every year, so check the portal.',
     'link': 'https://studyinvietnam.edu.vn', 'country': 'vn', 'type': 'Government'},
    {'id': 's-aua-merit', 'name': 'American University of Armenia merit scholarship for international students', 'scope': 'abroad', 'levels': ['bachelor', 'master'],
     'by': 'American University of Armenia (AUA), Yerevan',
     'covers': 'A merit based reduction of up to 50 percent of tuition for international students. The AUA tuition table for international students shows AMD 4,250,000 a year for the BA in Business and AMD 3,700,000 for other undergraduate programmes (about NPR 14 to 16 lakh at AMD 1 about NPR 0.38); a 2026/27 guide prints USD 11,700 to 13,080, so read the current table before you plan.',
     'who': 'International applicants (not citizens of Armenia, ethnic Armenians or Armenian special passport holders, who get an automatic AMD 2,000,000 subsidy and need based aid up to 90 percent) who apply to an AUA bachelor or master programme taught in English.',
     'how': 'Apply for admission and send the separate Application for International Scholarship to the AUA Office of Financial Aid by its deadline; AUA asks you to send it as early as possible, alongside the admission application.',
     'link': 'https://admissions.aua.am', 'country': 'am', 'type': 'University'},
    {'id': 's-kaust', 'name': 'KAUST Fellowship (King Abdullah University of Science and Technology)', 'scope': 'abroad', 'levels': ['master', 'phd'],
     'by': 'King Abdullah University of Science and Technology (KAUST), Thuwal, Saudi Arabia',
     'covers': 'Admission and funding come together: tuition and bench fees, a stipend of about USD 20,000 a year for MS and USD 25,000 to 30,000 for PhD, on campus housing, health and dental insurance and relocation (guides value the package at USD 70,000 to 80,000 a year).',
     'who': 'Applicants of any nationality with a relevant STEM bachelor (MS) or master (PhD), a GPA of about 3.0 of 4 or better (listings say 3.5 is competitive) and English proof such as TOEFL iBT 81 or IELTS 6.5. There is no application fee and GRE is optional (listings).',
     'how': 'Apply online on the KAUST admissions portal for the August intake. One guide (November 2026) prints a 3 January 2027 deadline for Fall 2027 while older listings show 17 January and 11 April for 2026, so read the portal for the exact date.',
     'link': 'https://www.kaust.edu.sa/en/study', 'country': 'sa', 'type': 'University', 'open': [11, 1]},
]

ABROAD_TEXT_SWAP = {
    'vn': [('note', 'so no Nepal specific call was confirmed',
            'and the official application portal (studyinvietnam.edu.vn) lists Nepal in its country menu, but no Nepal specific call or quota was confirmed')],
}

ABROAD_NOTE_ADD = {
    'is': 'The Icelandic Government scholarship for the BA in Icelandic as a Second Language lists the citizens it is open to (Austria, Canada, China, Germany, Norway, Poland, Slovakia, the United Kingdom, the United States through Fulbright and others) and Nepal is not among them in the 2026 call text, so it is not a route for Nepali students (the-updates.com, european-funding-guide.eu).',
    'am': 'The American University of Armenia teaches in English and lists international undergraduate tuition of AMD 3,700,000 (most programmes) to 4,250,000 (BA in Business) a year on its own tuition page, with merit scholarships of up to 50 percent (admissions.aua.am).',
}

# Work rule corrections read on 2026-11-20 (the older text said "not clear in law" for Georgia and quoted agencies for Kazakhstan).
# Georgia: inc.ge (20 Feb 2026), jam-news.net (1 Apr 2026), albatoulgroup.net (13 Aug 2026), lawverse.ge (21 Apr 2026), studyu.org (30 Sep 2026).
# Kazakhstan: iec.edu.kz (3 Jun 2026), almau.edu.kz and kaznpu.kz international student pages.
ABROAD_UPDATE = {
    'ge': {'work': 'Not as a student without a separate permit. Since 1 March 2026 any foreign national who is not a permanent resident needs a "right to work" from the Georgian authorities before any paid or self employed work, including remote work for a Georgian employer, and international students are not on the exemption list (inc.ge, jam-news.net and studyu.org, 2026). One legal commentary says a student who already holds a valid residence card does not need a separate work visa but still needs the right to work, and the employer files the application. Earlier agency claims of 20 hours a week are out of date; do not budget for income.'},
    'kz': {'work': 'Not allowed on the student visa. Three university pages say it: the International Educational Corporation (foreign students are not allowed to work), Almaty Management University (not eligible to work) and Abai Kazakh National Pedagogical University (carrying out labor activities with a student visa is an administrative offence). Older agency pages that say 20 hours a week are not backed by a university or official page, so plan to pay for your studies without wages.'},
}

ABROAD_NOTE_ADD.update({
    'ge': 'Government Resolution No. 437 of 8 September 2026 sets how state universities admit international students (the rector consents within the places the government approves for each programme and year), and a university must suspend a foreign student who earns no more than one third of the year\'s credits; if 90 days pass after the suspension the Public Service Development Agency may end the study residence permit (studyu.org, 30 September 2026).',
})

FAQ_ADD = [
    {'id': 'fw32-11', 'topic': 'abroad', 'q': 'Can a Nepali student work part time in Georgia or Kazakhstan?',
     'a': ('Georgia changed its rules on 1 March 2026: a foreign national who is not a permanent resident now needs a separate "right to work" before any paid or self employed work, and international students are not on the exemption list (inc.ge, jam-news.net, studyu.org). '
           'The employer applies for it, so a cafe job is no longer informal. Kazakhstan is stricter: the International Educational Corporation, Almaty Management University and Abai Kazakh National Pedagogical University all say a student visa holder may not work, and the Abai page calls it an administrative offence. '
           'Older agency pages that promise 20 hours a week in either country are not backed by these sources, so budget your whole fee and living cost without wages. Ask your university in writing before you accept any job.'),
     'go': ['abroad-ms']},
]

FAQ_TEXT_SWAP = {
    'fw14-4': [('Georgia: unclear, guides say 20 hours but others say jobs are informal.',
                'Georgia: not without a separate right to work since 1 March 2026 (inc.ge, jam-news.net).')],
}
