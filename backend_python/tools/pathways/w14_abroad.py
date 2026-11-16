"""Wave 14: four new destinations, work rules for the six wave 12 destinations, scholarship windows. Plain sentences, no dashes.

Rates used for NPR figures (late 2026, rough): EUR 1 = NPR 175, USD 1 = NPR 145. Say so in the note, figures move.
Sources: Study in Portugal and studyu.org (fees, 2026/27), studyineurope.eu (funds); EC country profile for Lithuania, edunepal, upgrad, moksh16 (work and funds);
Hong Kong Immigration Department FAQ on study and studyu.org (work, IANG, fees), unipage (tuition 2027/28); bukharasmi.com, neet.futeducation.com
(Uzbekistan fees); trw.co and jarniascyril.com (Bangladesh S visa); goingto.university and sulekha (Georgia); standyou, europestudy.eu and globaladmissions (Czechia);
studyinkz.kz and goingto.university (Kazakhstan); 3d-universal.com (Philippines SWP); isageorgia.com (Kyrgyzstan); HKPFS call 2027/28; Embassy of India Kathmandu (MGSS, GJSS, HJBSS).
"""

FX = ' NPR figures are rough, at EUR 1 about NPR 175 and USD 1 about NPR 145.'

ABROAD_ADD = [
    {'id': 'uz', 'country': 'Uzbekistan', 'tuition': [360000, 1090000], 'living': [870000, 1130000], 'code': 'UZ',
     'exams': ['NEB +2 Science with Physics, Chemistry and Biology (50 percent) for medicine', 'English test only if the university asks'],
     'intakes': 'February and September', 'fields': ['Medicine', 'Dentistry', 'Pharmacy'],
     'work': 'Not checked yet. Treat part time work as unavailable and budget your whole stay.',
     'note': 'Mostly a medicine destination. State medical institutes in Tashkent, Samarkand, Bukhara, Andijan and Fergana teach in English; quoted tuition is USD 2,500 to 4,000 a year on one list and up to USD 7,500 on another, living about USD 500 to 650 a month, and the course is six years with the internship. One university asks for a bank statement of USD 5,000 to 6,000. '
             'Many agency pages say NMC approved, which usually means the National Medical Commission of India. For Nepal what counts is Nepal Medical Council recognition of the college and course before you pay, then the NMCLE after you return. Ask for a written fee letter.' + FX},
    {'id': 'pt', 'country': 'Portugal', 'tuition': [260000, 1230000], 'living': [1470000, 2310000], 'code': 'PT',
     'exams': ['IELTS or TOEFL for English taught programmes', 'CAPLE Portuguese test for Portuguese taught programmes'],
     'intakes': 'September; applications usually March to July', 'fields': ['Engineering', 'Economics and management', 'Computer science', 'Medicine'],
     'work': 'Not checked on an official page. Agency guides say up to 20 hours a week in term and full time in holidays; one guide says there is no weekly cap. Confirm with AIMA and your university.',
     'note': 'Public universities charge non EU students EUR 1,500 to 7,000 a year (most EUR 3,500 to 7,000; medicine EUR 16,500 to 18,000 at Lisbon and Porto in 2026/27). Bachelor degrees are mostly in Portuguese (B1 at Lisbon, B2 at Coimbra); English is realistic at master level and at economics and management schools such as Nova SBE, ISEG and Catolica. '
             'Funds are pegged to the minimum wage: about EUR 760 a month, EUR 9,120 for a year, and the figure changes every year. Apply for the D4 study visa, then the residence permit through AIMA. Living is EUR 700 to 1,100 a month.' + FX,
     'scholarships': ['s-erasmus']},
    {'id': 'lt', 'country': 'Lithuania', 'tuition': [230000, 1490000], 'living': [1050000, 1680000], 'code': 'LT',
     'exams': ['IELTS or equal English test', 'University admission test for some programmes'],
     'intakes': 'September (applications from about November)', 'fields': ['Engineering', 'Computer science', 'Business', 'Medicine', 'Life sciences'],
     'work': 'Sources disagree. The European Commission country page says non EU students can work up to 40 hours a week once they hold the temporary residence permit; several agencies say 20 hours in term and full time in holidays. Ask the Migration Department and your university before you plan around work.',
     'note': 'More than 500 English taught programmes. The European Commission lists bachelor tuition from EUR 1,300 and master from EUR 2,300 a year; agencies quote EUR 3,950 to 8,500 for non EU students and EUR 12,800 to 14,100 for medicine at Vilnius and Kaunas (LSMU). Living EUR 500 to 800 a month. '
             'Proof of funds is quoted from EUR 500 to about EUR 1,200 a month depending on the source, health insurance is compulsory, and one guide says Nepali applicants use the Lithuanian Embassy in New Delhi. Check the current figures with the Migration Department.' + FX,
     'stay_back': '12 months to look for work after graduating', 'scholarships': ['s-erasmus']},
    {'id': 'hk', 'country': 'Hong Kong', 'tuition': [930000, 5240000], 'living': [1260000, 2080000], 'code': 'HK', 'work_hours': 20,
     'exams': ['IELTS 6.5 at most universities (HKU asks 6.0 in writing and speaking)', 'TOEFL iBT accepted'],
     'intakes': 'September; applications open from September of the year before', 'fields': ['Business', 'Engineering', 'Computer science', 'Medicine', 'Research PhD'],
     'work': 'The default rule for full time degree students is on campus work up to 20 hours a week, summer work from 1 June to 31 August with no limit, and study related internships. Since November 2024 degree students on local programmes have been temporarily exempt from the hour limits, but the Immigration Department still calls the exemption temporary. Permission arrives as a No Objection Letter with your visa.',
     'note': 'Non local bachelor tuition for 2027/28 is about USD 27,000 to 36,000 a year; research postgraduate places at the eight public universities cost about USD 6,400. No tuition free route, so scholarships matter (HKPFS for PhD). The university sponsors your student visa (government fee HKD 330, about six weeks). Living including a hall place is about USD 8,700 to 14,300 a year.' + FX,
     'stay_back': '24 months under IANG with no job offer if you apply within 6 months of graduating'},
]

ABROAD_UPDATE = {
    'cz': {'work': 'A long term study permit carries the right to work without a separate work permit and the employer must report the job to the labour office. Agencies say a 20 hour weekly cap applies; a 2026 guide says there is no weekly cap. Read the Ministry of the Interior (MV CR) rules for your permit.'},
    'ge': {'work': 'Not clear in law. Two agency guides say a student with a residence permit can work up to 20 hours a week; another says no law covers student work so part time jobs are informal. Do not count on income; ask the Public Service Hall and your university.'},
    'bd': {'work': 'Not allowed. The S student visa carries the endorsement employment in Bangladesh prohibited (Visa Policy 2026) and a breach can lead to cancellation. There is no student work allowance and no post study work period.'},
    'kg': {'work': 'Agencies disagree. Some say part time work is allowed after you convert to a multiple entry status with a valid permit and the approval of the migration service; others say a student visa does not encourage jobs for medical students. Plan to pay for your studies without wages.'},
    'kz': {'work': 'Agencies say students may work part time, usually up to 20 hours a week in term and full time in holidays, only with the university authorisation and within limits set by the labour ministry. No official page was read, so confirm with your university before you accept a job.'},
    'ph': {'work': 'A 9(f) student visa does not allow work. Limited short jobs or internships need a Special Work Permit from the Bureau of Immigration (agencies quote 3 to 6 months) with a school endorsement; working without one risks fines, visa cancellation or deportation.'},
}

SCHOLARSHIP_EXTRA = {
    's-mgss': {
        'how': 'The 2026-27 window on goischolarship.com.np ran from 23 October to 15 November 2026 (the portal closed at 00.00 on 16 November). Apply directly; the Embassy does not accept applications through consultants or agents. Awardees send the Class 11 mark sheet and a promotion certificate by 31 December to continue in Class 12.',
        'open': [10, 11],
    },
    's-gjss': {
        'how': 'The 2026-27 window on goischolarship.com.np ran from 23 October to 15 November 2026. You must be a regular first year bachelor student (not diploma) aged 17 to 22 on 1 July 2027 with a Class 12 mark sheet, and not receiving any other scholarship. Continuation each year needs the mark sheet and a promotion certificate by 31 December. Apply directly, not through agents.',
        'open': [10, 11],
    },
    's-homi-bhabha': {
        'how': 'The 2026-27 notice closed on 4 June 2026: age 25 or less on 1 July 2026, at least 60 percent aggregate in BE and at least 50 percent in English in Class 12, an application fee of NPR 400 paid at Nepal SBI Bank, and the form sent by post or handed in at the Embassy. Only completed bachelor degrees count.',
        'open': [5, 6],
    },
    's-sh': {
        'how': 'Apply on the Tempus Public Foundation portal (apply.stipendiumhungaricum.hu). The 2026-27 call came out on 28 October 2025 and closed on 15 January 2026 at 2 pm Central European Time. For 2027-28 expect the same pattern (portal in mid November, deadline about 15 January 2027) but the call was not published when this was checked in early November 2026. Nepali applicants also complete the national partner step, then sit the university exam or interview from March to May.',
    },
    's-pu-scholarship': {
        'how': 'Pokhara University runs several calls a year. The master scholarship entrance for Fall 2026 took applications from 26 August to 21 September 2026 (60 percent open, 40 percent reserved for disabled, martyr and conflict families, remote, Dalit, Janajati and Madhesi students, half of each for women, bachelor completed within three years). A call for vacant undergraduate scholarship seats was published on 4 November 2026; read the notice for its deadline. One summary lists 1,328 bachelor scholarship seats for 2083 (Science and Technology 501, Management 788, Humanities 39).',
    },
}

SCHOLARSHIPS_ADD = [
    {'id': 's-hkpfs', 'name': 'Hong Kong PhD Fellowship Scheme (HKPFS)', 'scope': 'abroad', 'levels': ['phd'], 'by': 'Research Grants Council, Hong Kong',
     'covers': 'Annual stipend of HKD 344,400 (HKD 28,700 a month) and HKD 14,400 a year for conference and research travel, for up to three years; 400 fellowships for 2027/28',
     'who': 'Open to every nationality. New full time PhD students at the eight participating Hong Kong universities, judged on academic record, research ability, communication and leadership. You must also meet the admission rules of your university and programme and show English proof (IELTS or a degree taught in English).',
     'how': 'Register on the HKPFS electronic system for a reference number before you apply to a university. The 2027/28 deadline is 1 December 2026 at 12:00 noon Hong Kong time, so for a later start the next call opens in the autumn of 2027.',
     'link': 'https://cerg1.ugc.edu.hk/hkpfs/', 'country': 'hk', 'type': 'Government', 'open': [9, 12]},
    {'id': 's-pearson', 'name': 'Lester B. Pearson International Scholarship (University of Toronto)', 'scope': 'abroad', 'levels': ['bachelor'], 'by': 'University of Toronto',
     'covers': 'Tuition, books, incidental fees and residence for four years',
     'who': 'Outstanding international students about to start their first university degree at Toronto. Your school must take part in the programme and nominate you (one student per school each year). You also apply for admission to at least one undergraduate programme.',
     'how': 'For September 2027 entry the school nomination closed on 9 October 2026, the admission application on 16 October 2026 and the scholarship form on 6 November 2026, so all three are shut. Expect the same months in 2027; ask your counsellor to register the school in July.',
     'link': 'https://future.utoronto.ca/pearson-scholarships', 'country': 'ca', 'type': 'University', 'open': [10, 11]},
]
