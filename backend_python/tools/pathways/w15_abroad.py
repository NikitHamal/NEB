"""Wave 15: four more destinations (Romania, Estonia, Switzerland, Cyprus) and the Romanian government scholarship. Plain sentences, no dashes.

Rates used for NPR figures (late 2026, rough): EUR 1 = NPR 175, CHF 1 = NPR 175, USD 1 = NPR 145. The note says so, figures move.
Sources (read November 2026, agency or secondary unless named): sanmarina.edu.np, truescho.com, stinwo.ro and bluehawksedu.com (Romania fees, work 4 hours a day);
globaladmissions.com, eduatlashub.com and scholarshipsjet.com (Romanian MFA scholarship, call 16 February to 31 March 2026, stipend EUR 65 / 75 / 85);
study-abroad.org (Estonia costs and permit fees), karangupta.com and sugimotovisa.com (Estonia funds and work); college-council.com, falconnovaconsultants.com and study-abroad.org
(ETH and EPFL fees, CHF 21,000 funds, 15 hours); bajwamigration.com and studyu.org (Cyprus fees).
"""

FX = ' NPR figures are rough, at EUR 1 about NPR 175 and CHF 1 about NPR 175.'

ABROAD_ADD = [
    {'id': 'ro', 'country': 'Romania', 'tuition': [297500, 1575000], 'living': [840000, 1470000], 'code': 'RO',
     'exams': ['IELTS, TOEFL or a university English test for English taught programmes', 'Romanian language preparatory year for Romanian taught programmes'],
     'intakes': 'October (the academic year starts then); apply from spring', 'fields': ['Medicine', 'Dentistry', 'Engineering', 'Computer science', 'Business'],
     'work': 'Agency pages agree that a student residence permit lets you work up to 4 hours a day (about 20 hours a week) in term without a separate work permit, and generally full time in official holidays. Confirm with the General Inspectorate for Immigration and your university.',
     'work_hours': 20,
     'note': 'The cheapest tuition in the European Union. Public universities charge non EU students EUR 1,700 to 4,500 a year for most degrees (one list starts at EUR 660, another quotes up to EUR 9,000), English taught medicine EUR 5,000 to 8,500 and sometimes up to 12,000 a year over six years, living EUR 400 to 700 a month (Bucharest and Cluj cost more than smaller cities). '
             'The long stay study visa is applied for after your acceptance letter; agencies say Nepali students use the honorary consulate in Kathmandu or the embassy in New Delhi and quote about EUR 3,000 as the funds to show plus a residence permit fee near EUR 120, so ask the Romanian foreign ministry or your university before you pay anyone. '
             'Several agencies advertise MBBS as NMC approved, which means India. For Nepal, check that the Nepal Medical Council recognises the college first.' + FX},
    {'id': 'ee', 'country': 'Estonia', 'tuition': [262500, 1312500], 'living': [1155000, 2100000], 'code': 'EE',
     'exams': ['IELTS, TOEFL or an equal English test', 'Entrance test or portfolio for some programmes'],
     'intakes': 'September, and February for some programmes', 'fields': ['IT and computer science', 'Engineering', 'Business', 'Digital society', 'Natural sciences'],
     'work': 'Agency and guide pages say a student residence permit holder can work with no weekly hour cap as long as the job does not harm the studies, so part time work is practical mostly in IT and hospitality. Confirm with the Police and Border Guard Board before counting on income.',
     'stay_back': '9 months to look for work after graduating',
     'note': 'English taught programmes at public universities cost EUR 1,500 to 7,500 a year (Tartu bachelor about EUR 2,500 to 4,000, TalTech bachelor about EUR 3,200 to 7,500, private universities EUR 7,000 to 12,000, medicine about EUR 12,000); one source says doctoral studies carry no tuition at public universities. '
             'Living is about EUR 550 to 850 a month in Tartu and EUR 700 to 1,000 in Tallinn. Funds for the permit are quoted at EUR 350 a month on one page and EUR 438 on another, so the figure moves: ask the Police and Border Guard Board. The state fee for a study residence permit is quoted at EUR 96, and you first need a D visa from an Estonian embassy or VFS centre.' + FX,
     'scholarships': ['s-erasmus']},
    {'id': 'ch', 'country': 'Switzerland', 'tuition': [766500, 766500], 'living': [3675000, 4200000], 'code': 'CH',
     'exams': ['German or French proof for most bachelor programmes', 'IELTS or TOEFL for English taught master programmes at ETH and EPFL'],
     'intakes': 'September (autumn semester); ETH and EPFL deadlines are months earlier', 'fields': ['Engineering', 'Computer science', 'Natural sciences', 'Architecture', 'Hospitality'],
     'work': 'Agency pages say 15 hours a week in term. Swiss rules normally allow student work only after the first six months of study and with the canton\'s approval, so confirm with your canton\'s migration office. Pay is high but so are costs.',
     'work_hours': 15, 'stay_back': '6 months to look for work after graduating',
     'note': 'No student visa as such: non EU students apply for a residence permit for education through the canton. Since autumn 2025 most international students at ETH Zurich and EPFL pay CHF 2,190 a semester (about CHF 4,380 a year), against CHF 730 for Swiss residents. ETH asks for proof of CHF 21,000 a year (CHF 24,000 in Basel), in your own name at a Swiss regulated bank, and compulsory Swiss health insurance of about CHF 300 to 400 a month adds to that. '
             'The tuition figure here is the two federal institutes only; cantonal universities set their own fees. Admission is strict. The Swiss Government Excellence Scholarship is for researchers and artists at master and doctoral level.' + FX,
     'scholarships': ['s-swiss']},
    {'id': 'cy', 'country': 'Cyprus', 'tuition': [612500, 1925000], 'living': [1575000, 2100000], 'code': 'CY',
     'exams': ['IELTS or an equal English test, or the university\'s own test'],
     'intakes': 'September and February', 'fields': ['Business', 'Medicine', 'Computer science', 'Engineering', 'Hospitality'],
     'work': 'Not checked on an official page. Agencies describe tight limits for non EU students and several say work is allowed only after the first months with the university\'s support. Ask the university and the Civil Registry and Migration Department before you count on any income.',
     'note': 'Mostly private universities. Agencies quote bachelor tuition at EUR 3,500 to 7,000 in public and EUR 5,500 to 9,500 in private universities; one 2026/27 table lists European University Cyprus at EUR 9,240 to 10,980 for a bachelor, EUR 8,910 for a master and EUR 23,000 for medicine. Living is quoted at EUR 9,000 to 12,000 a year. '
             'The education system is EU recognised, but the recognition of a degree by Nepal for later study or a licence is separate: ask for the Tribhuvan University equivalence rules and, for medicine, the Nepal Medical Council. Choose your university yourself and keep the fee letter in writing.' + FX},
]

ABROAD_UPDATE = {}

SCHOLARSHIPS_ADD = [
    {'id': 's-romania-govt', 'name': 'Romanian Government Scholarship (Ministry of Foreign Affairs)', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'], 'by': 'Romanian Ministry of Foreign Affairs with the Ministry of Education',
     'covers': 'Exemption from registration and tuition fees, a free Romanian language preparatory year if needed, a dormitory place subject to availability and a small monthly stipend (listings quote EUR 65 bachelor, EUR 75 master, EUR 85 doctoral)',
     'who': 'Non EU citizens, for bachelor, master and doctoral study in Romanian universities in all fields except medicine, dental medicine and pharmacy. The call is annual and lists some categories that cannot apply, so read the current call.',
     'how': 'Apply online at scholarships.studyinromania.gov.ro. The 2026/27 call ran from 16 February to 31 March 2026 with results about 15 July, so the next call is expected in the same months of 2027. Documents must be apostilled or attested, scanned as PDFs and translated into English, French, Spanish or Romanian.',
     'link': 'https://scholarships.studyinromania.gov.ro', 'country': 'ro', 'type': 'Government', 'open': [2, 3]},
]

SCHOLARSHIP_EXTRA = {
    's-swiss': {'country': 'ch'},
}
