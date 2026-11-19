"""Wave 31: six new destinations (Slovakia, Indonesia, Saudi Arabia, Armenia, Vietnam, Iceland) and three government scholarships.
Read on 2026-11-20. Rates used for NPR figures (rough): EUR 1 = NPR 175, USD 1 = NPR 145, SAR 1 = NPR 38.
Sources: studyinslovakia.saia.sk (official SAIA page on work and the nine month job search), educations.com, atozserwisplus.com, helpstudyabroad.com
(Slovak costs); eduslovakia.sk, opportunitiesforyouth.org, daadscholarship.com (National Scholarship Programme); o4af.com, scholarwaka.com,
heysuccess.com, expat.com, acadfly.com, university.im (KNB and Indonesian costs, student work); truescho.com, titansabroad.org, study-abroad.org
(Saudi Government scholarship and costs); russianmbbs.com citing ysmu.am (Yerevan State Medical University AMD 2,600,000), iambbs.com,
universityinsights.in (Armenia costs); standyou.com, shiksha.com, thepienews.com (Oct 2025), veles-club.com (Vietnam); prospects.ac.uk, scholars4dev.com,
movingtoiceland.com, goingto.university, educations.com, expatfocus.com (Iceland). Where sources disagree, the text says so.
"""

FX = ' NPR figures are rough, at EUR 1 about NPR 175, USD 1 about NPR 145 and SAR 1 about NPR 38.'

ABROAD_ADD = [
    {'id': 'sk', 'country': 'Slovakia', 'tuition': [262500, 2100000], 'living': [1050000, 1680000], 'code': 'SK',
     'exams': ['Entrance exam or document review set by each university', 'English proof (IELTS, TOEFL or the university\'s own test) for English taught programmes'],
     'intakes': 'September (main) and February at a few universities', 'fields': ['Medicine and dentistry (English, 6 years)', 'Engineering', 'Computer science', 'Economics', 'Veterinary science'],
     'work': 'Official SAIA page (studyinslovakia.saia.sk): a third country national with a study residence permit may work up to 80 hours a month as a university student (a guide of Liberty School says 20 hours a week or 100 days a year, so the wording differs). A full time student does not need a separate work permit within this limit.',
     'work_hours': 20, 'stay_back': '9 months to look for a job or start a business after a bachelor, master or doctoral degree (SAIA). As a graduate you have free access to the labour market with a valid temporary residence; if you find a job you change the purpose of stay to employment at the Foreign Police.',
     'note': 'Programmes taught in Slovak at public universities are free, and English taught programmes cost EUR 1,500 to 6,000 a year at public universities and EUR 2,000 to 10,000 at private ones; medicine and dentistry in English cost more (one guide says up to EUR 12,000, the preparatory medicine course EUR 4,250). '
             'Living is quoted at EUR 500 to 800 a month in one guide and EUR 300 to 600 in two others, with the dormitory about EUR 100 a month and Bratislava 20 to 30 percent dearer than Kosice or Zilina. Proof of funds is quoted at EUR 5,000 on one page and about EUR 580 a month for a year on another, so ask the Slovak embassy in New Delhi, which handles Nepal, for the amount in writing. '
             'You get a D visa at the embassy, then apply for temporary residence for study at the Foreign Police after arrival. A Slovak degree is easier to use in Nepal than a private foreign MD, but a medical degree still needs the Nepal Medical Council to recognise that exact university.' + FX,
     'scholarships': ['s-sk-nsp']},
    {'id': 'id', 'country': 'Indonesia', 'tuition': [145000, 1160000], 'living': [522000, 1218000], 'code': 'ID',
     'exams': ['Bahasa Indonesia or English proof depending on the programme (KNB winners first take a year of Bahasa training, BIPA)', 'University admission test or document review'],
     'intakes': 'August or September (main) and February at some universities', 'fields': ['Engineering', 'Agriculture', 'Natural science', 'Business', 'Education and languages', 'Medicine (usually in Bahasa)'],
     'work': 'Student visa holders are not allowed to work unless a specific internship or programme is approved by the authorities (Expat.com, May 2026). Do not budget for wages.',
     'stay_back': 'No post study job search permit was found in the guides read. The university sponsors a limited stay visa (VITAS) that is converted to a student limited stay permit (ITAS) after arrival; staying to work means changing to a sponsored work permit.',
     'note': 'Public universities charge about USD 1,000 to 5,000 a year in one guide (IDR 5 to 20 million, USD 315 to 1,260, in another) and private universities USD 2,000 to 8,000; medicine and engineering cost more. Living is USD 300 to 700 a month (Jakarta IDR 8 to 18 million). '
             'Most teaching is in Bahasa Indonesia, with English taught programmes at a few universities. The Indonesian Government KNB scholarship lists Nepal among its eligible countries and is the realistic low cost route: it pays tuition and a living allowance. Choose the university from the KNB list, not from an agent.' + FX,
     'scholarships': ['s-knb-id']},
    {'id': 'sa', 'country': 'Saudi Arabia', 'tuition': [0, 3040000], 'living': [755000, 755000], 'code': 'SA',
     'exams': ['IELTS or TOEFL for English taught programmes, Arabic proof for Arabic taught ones', 'High school grade of 90 percent and above or postgraduate GPA 3.5 of 4 for the funded scholarship (one listing)'],
     'intakes': 'September (autumn semester); applications on the Study in Saudi portal open months earlier', 'fields': ['Islamic studies and Arabic', 'Engineering', 'Petroleum and energy', 'Computer science', 'Medicine and health sciences', 'Business'],
     'work': 'Not checked on an official page. A 2026 cost guide says work rules are restrictive and tied to your visa and university sponsorship, many scholarship students may not take outside jobs, and any work needs authorisation. Scholarship holders rarely need part time income because tuition, housing and a stipend are covered.',
     'stay_back': 'No post study job search permit found. Staying to work needs an employer sponsored residence.',
     'note': 'Funded places at public universities (King Saud University, King Abdulaziz University, King Fahd University of Petroleum and Minerals, Islamic University of Madinah, KAUST) carry full tuition waiver, a monthly stipend (SAR 900 to 1,200 for a bachelor, SAR 1,500 for a master and SAR 1,500 to 3,000 for a doctorate in one listing), housing, health insurance and a yearly flight, so the tuition range starts at zero. '
             'Private universities charge about SAR 40,000 to 80,000 a year. The living figure (SAR 20,400 a year for food, transport and personal costs, housing provided) is from one 2026 cost guide. Age limits quoted: bachelor 17 to 25, master up to 30, doctorate up to 35. The Islamic University of Madinah admits Muslim students only, and one listing says women need a male guardian living in or travelling to Saudi Arabia. Read the current call on the official Study in Saudi portal.' + FX,
     'scholarships': ['s-sa-govt']},
    {'id': 'am', 'country': 'Armenia', 'tuition': [435000, 1090000], 'living': [350000, 652500], 'code': 'AM',
     'exams': ['NEB +2 Science with Physics, Chemistry and Biology for medicine', 'English proof or an interview with the university', 'NEET qualification is an Indian rule and does not apply to Nepali applicants'],
     'intakes': 'September', 'fields': ['Medicine (MD, 6 years)', 'Dentistry', 'Pharmacy'],
     'work': 'Not checked on an official page. Guides read for Armenia do not state a student work rule; ask the university and the Migration and Citizenship Service before you count on any income.',
     'stay_back': 'Not checked. No post study permit was found in the pages read; ask the university and the Migration and Citizenship Service.',
     'note': 'Mostly chosen for English medium MD at Yerevan State Medical University, which publishes AMD 2,600,000 a year for foreign students on its 2026/27 admissions page (about USD 6,800 at AMD 380 to the dollar) and says the annual fee stays the same for the whole course. Guides quote USD 3,000 to 7,500 a year for tuition across the medical universities and USD 2,400 to 4,500 a year for living (hostel USD 100 to 300 a month). '
             'The total for six years is quoted at USD 40,000 to 60,000. A foreign MD counts for a licence in Nepal only if the Nepal Medical Council recognises that exact university, and you must pass the NMC licensing examination (NMCLE) after returning: ask for the recognition in writing before you pay any deposit.' + FX,
     'scholarships': []},
    {'id': 'vn', 'country': 'Vietnam', 'tuition': [145000, 1160000], 'living': [522000, 1044000], 'code': 'VN',
     'exams': ['IELTS or the university\'s English test for English taught programmes', 'Vietnamese language proof for programmes taught in Vietnamese'],
     'intakes': 'September (main) and a few February intakes', 'fields': ['Business', 'Engineering', 'Information technology', 'Hospitality', 'Medicine (mostly in Vietnamese)'],
     'work': 'No clear rule. The Vietnamese education ministry floated a 20 hours a week student work right in October 2025 (The PIE News) and said at that time there was no rule on student hours; another 2026 guide says a student residence card allows work only with approval for internships or part time jobs. Treat paid work as not allowed until a written rule exists.',
     'stay_back': 'No post study job search permit found. A work residence card is tied to a work permit with an employer.',
     'note': 'Public universities charge about USD 1,000 to 2,500 a year and private or international universities USD 2,500 to 8,000 (StandYou); Shiksha quotes USD 2,000 to 5,000 and living USD 300 to 600 a month, with a student dormitory USD 50 to 100. '
             'The Vietnam Government Scholarship for foreign students is nominated through governments and embassies and mostly for programmes in Vietnamese, so no Nepal specific call was confirmed. Student residence cards are tied to enrolment and are usually valid for one year.' + FX,
     'scholarships': []},
    {'id': 'is', 'country': 'Iceland', 'tuition': [76000, 102000], 'living': [2200000, 2200000], 'code': 'IS',
     'exams': ['IELTS or TOEFL for English taught master programmes', 'Bachelor degree for master entry', 'Many bachelor programmes are taught in Icelandic'],
     'intakes': 'September (autumn) and a few January starts; non EEA deadlines are early in the year', 'fields': ['Renewable energy', 'Environment and natural resources', 'Computer science', 'Fisheries and marine science', 'Medieval and Norse studies'],
     'work': 'Sources disagree. Two 2026 guides (educations.com and goingto.university) say a student permit allows 15 hours a week; Expat Focus (March 2026) says a 2023 law change raised it to 22.5 hours a week, 60 percent employment. Use 15 until the Directorate of Immigration confirms in writing.',
     'work_hours': 15, 'stay_back': 'Expat Focus (March 2026) says a graduate of a university in Iceland may renew the permit for up to three years from graduation to seek work in their field. No Directorate of Immigration page was read, so confirm before you plan on it.',
     'note': 'Public universities charge no tuition but a yearly registration fee (ISK 100,000 at the University of Iceland for 2026/27, ISK 75,000 at some others, about NPR 76,000 to 102,000) plus a one time ISK 20,000 handling fee for non EEA applicants; the University of Iceland says it has no funding for international applicants. '
             'Important: Icelandic law now lets public universities charge tuition to new students from outside the EEA, EFTA and Switzerland from autumn 2027, and the amounts were not set by October 2026, while the Iceland University of the Arts has confirmed tuition from autumn 2026, so check your university\'s page. '
             'The residence permit for study asks for proof of about ISK 180,840 a month (about ISK 2.17 million for a year, NPR 2.2 million); the permit fee is quoted at ISK 12,000 to 15,000. Living is among the dearest in Europe, so the figure here is that proof of funds amount, not a budget.' + ' ISK 100,000 is about NPR 102,000.' + FX,
     'scholarships': []},
]

SCHOLARSHIPS_ADD = [
    {'id': 's-sk-nsp', 'name': 'National Scholarship Programme of the Slovak Republic (SAIA)', 'scope': 'abroad', 'levels': ['master', 'phd'], 'by': 'Ministry of Education, Research, Development and Youth of Slovakia, run by SAIA',
     'covers': 'A monthly allowance (EUR 620 for a university student in the second level, EUR 1,025.50 for a doctoral student; another guide prints EUR 600 to 700) and, for students and doctoral students, a separate travel grant by distance. It funds a stay of 1 to 2 semesters (doctoral 1 to 10 months), not a full degree.',
     'who': 'Citizens of any country except Slovakia who are enrolled at a university outside Slovakia (master students, doctoral students, teachers, researchers and artists), with an acceptance or invitation letter from a Slovak university and a study or research plan. Not eligible: anyone who spent 15 months or more in Slovakia in the 36 months before the deadline.',
     'how': 'Apply online at scholarships.sk (the system opens at least six weeks before the deadline). Deadlines are 30 April 16:00 CET for the next academic year and 31 October 16:00 CET for the summer semester. The original acceptance letter must reach SAIA in Bratislava by 12 noon on the third working day after the deadline. Results come about eight weeks later.',
     'link': 'https://www.scholarships.sk', 'country': 'sk', 'type': 'Government', 'open': [3, 4]},
    {'id': 's-knb-id', 'name': 'Indonesian Government KNB Scholarship (Kemitraan Negara Berkembang)', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'], 'by': 'Ministry of Higher Education, Science and Technology of Indonesia',
     'covers': 'Tuition, a monthly living allowance, an arrival allowance, health insurance and airfare (listings), with a first year of Bahasa Indonesia training (BIPA) before the degree for most winners.',
     'who': 'Citizens of developing countries on the programme list, which names Nepal, with the academic record, age and language needed for the level. The 2026/27 call listed 30 bachelor, 162 master and 30 doctoral places (222), in 47 participating universities.',
     'how': 'Apply online at the KNB site. The 2026/27 call ran from 2 February to 31 March 2026, selection 4 to 22 May, results on 19 June 2026 and arrival in late August, so expect the next call in February and March 2027 and confirm on the official site. An embassy recommendation letter is part of the file.',
     'link': 'https://knb.kemdiktisaintek.go.id', 'country': 'id', 'type': 'Government', 'open': [2, 3], 'awards': 222},
    {'id': 's-sa-govt', 'name': 'Saudi Government Scholarship (Study in Saudi, Ministry of Education)', 'scope': 'abroad', 'levels': ['diploma', 'bachelor', 'master', 'phd'], 'by': 'Ministry of Education of Saudi Arabia',
     'covers': 'On fully funded places: tuition waiver, a monthly stipend (SAR 900 to 1,200 bachelor, SAR 1,500 master, SAR 1,500 to 3,000 doctoral), housing or a housing allowance, health insurance and a yearly flight. Partial and paid study places carry no stipend.',
     'who': 'Applicants from countries with diplomatic relations with Saudi Arabia, aged 17 to 25 (bachelor), up to 30 (master) or up to 35 (doctoral), with a high school grade of 90 percent or a postgraduate GPA of 3.5 of 4, a medical report, a police clearance and attested certificates, who hold no earlier Saudi scholarship.',
     'how': 'One free application on the Study in Saudi portal covers several universities. Listings quote a 21 May 2026 close for one round and 6 October 2026 for another (it varies by university), so read the portal for the current round. The Islamic University of Madinah accepts Muslim students only.',
     'link': 'https://studyinsaudi.moe.gov.sa', 'country': 'sa', 'type': 'Government', 'open': [4, 5]},
]

SCHOLARSHIP_EXTRA = {}
