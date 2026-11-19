"""Wave 33: four destinations (Pakistan, Egypt, Serbia, Qatar) and two government scholarships with a Nepal route. Read on 2026-11-21.
Pakistan PTAP: Edusanjal "Scholarships Under Pakistan Technical Assistance Program" (the notice text, deadline Asar 26 2083 = 10 July 2026),
Nepal Diplomat (9 July 2026), nepalontheweb.com and Danfe TV English quoting the Ministry of Education notice (moest.gov.np content 13636, whose page
exists but its text is an attached notice). NUST: pakera.pk, blog.maqsad.io and feestructure.pk (USD 5,400 a year, USD 600 processing fee, USD 250 deposit,
USD 120 health; feestructure.pk also prints USD 3,500 to 4,000 a semester). Pakistan living: campusaxis.pk (hostel student PKR 18,000 to 31,000 a month),
gyandhan.com (Islamabad PKR 64,640 a month). Pakistan student visa: fpcci.org.pk (NOC from the ministry and security clearance, one year extensions)
and desinri.com (public material does not clearly grant work rights).
Egypt: study-abroad.org (public university EGP 5,000 to 15,000 a year, AUC USD 25,000 to 40,000, Cairo EGP 8,000 to 15,000 a month, Al-Azhar free for many Muslim
students), Edusanjal on the MEC MD/MS scholarship (Ministry letter ref 145 of 2082/01/26, 27 to 30 May 2025).
Serbia: studyu.org (University of Belgrade 2026/27 call, Medicine in English EUR 8,000, Novi Sad EUR 7,000, Nis and Kragujevac EUR 6,000, bachelor EUR 900 to 3,600),
studyinserbia.rs (monthly EUR 750 to 1,450, Belgrade EUR 850 to 2,000), studyinternational.com (University of Belgrade estimate EUR 600 to 800), expatsi.com
(residence permit fee RSD 23,880, work needs a National Employment Service permit), standyou.com (Type D visa, 20 hours).
Qatar: qu.edu.qa international students page (QAR 1,700 a credit hour, minimum 11 credit hours, 1 USD about 3.65 QAR, residence permit under university sponsorship
within one month), brightkey.co (Doha QAR 5,000 to 9,000 a month), excelsiorscholarships.com (undergraduate deadlines March to June 2026).
Rates: USD 1 = NPR 145, QAR 1 = NPR 39.7, EGP 1 = NPR 3, EUR 1 = NPR 175. Where sources disagree the text says so.
"""
FX = ' NPR figures are rough.'
NMC = ('A foreign medical degree counts for a licence in Nepal only if the Nepal Medical Council recognises that exact university, and you must pass the NMC '
       'licensing examination after returning, so ask the council before you pay a deposit.')

ABROAD_ADD = [
    {'id': 'pk', 'country': 'Pakistan', 'tuition': [0, 783000], 'living': [112000, 400000], 'code': 'PK',
     'exams': ['Grade 12 (or equivalent) with at least 60 percent and the right subjects: English, Physics, Chemistry and Mathematics for BSc Engineering, English, Physics, Chemistry and Biology for D Pharmacy (PTAP notice)',
               'Equivalence certificate from the Inter Board Committee of Chairmen (IBCC) in Islamabad', 'Each university sets its own admission test or merit rule'],
     'intakes': 'Autumn session; the 2026/27 PTAP call closed on 10 July 2026 (Asar 26 2083)',
     'fields': ['Engineering (civil, computer, electrical)', 'D Pharmacy', 'Computing and IT', 'Business', 'Medicine (separate PTAP and MBBS routes)'],
     'work': 'Not clearly allowed: the public student visa material read does not grant general work rights, so assume none unless an official says otherwise.',
     'stay_back': 'No post study stay route found. Foreign students on a proper student visa get a visa or extension for one year with one re-entry (fpcci.org.pk).',
     'note': 'The practical route for a Nepali student is the Pakistan Technical Assistance Programme (PTAP): for 2026/27 the Ministry of Economic Affairs gave Nepal 14 seats, which Nepal fills from its own merit list. Without a PTAP seat, NUST charges international undergraduates USD 5,400 a year plus a USD 600 non refundable processing fee, a USD 250 refundable deposit and USD 120 for health (pakera.pk, maqsad.io, feestructure.pk; one guide prints USD 3,500 to 4,000 a semester, so read nust.edu.pk). The tuition range here starts at 0 because PTAP exemption from tuition and other dues follows each institution\'s policy.'
             ' Living is cheap: a hostel student budgets PKR 18,000 to 31,000 a month at Lahore (campusaxis.pk) while a Numbeo style estimate for Islamabad is about PKR 64,640 (gyandhan.com); the range here is PKR 216,000 to about PKR 775,000 a year at PKR 1 about NPR 0.52. The student visa needs a no objection certificate from the education ministry and security clearance, and Pakistan Missions issue it only after the Ministry of Economic Affairs confirms admission (fpcci.org.pk, PTAP notice).'
             ' Travel, boarding and lodging are paid by the student.' + FX,
     'scholarships': ['s-ptap-pk']},
    {'id': 'eg', 'country': 'Egypt', 'tuition': [15000, 5800000], 'living': [288000, 540000], 'code': 'EG',
     'exams': ['School certificate recognised by the Supreme Council of Universities', 'English proof for English medium private universities', 'Arabic for Arabic medium public faculties'],
     'intakes': 'Usually one intake in September or October (study-abroad.org)',
     'fields': ['Medicine (Arabic and English faculties)', 'Dentistry and pharmacy', 'Engineering', 'Islamic studies and Arabic (Al-Azhar)', 'Business and humanities'],
     'work': 'Not checked yet: no Egyptian official page on student work rights was read.',
     'stay_back': 'Not checked yet.',
     'note': 'Egypt has three very different price levels (study-abroad.org, 2026): public universities such as Cairo, Ain Shams, Alexandria, Mansoura and Assiut charge international students roughly EGP 5,000 to 15,000 a year (about NPR 15,000 to 45,000, medicine and dentistry often EGP 20,000 to 40,000 or more), English medium private universities (GUC, BUE, MUST, MIU) about USD 5,000 to 15,000, and the American University in Cairo about USD 25,000 to 40,000 (about NPR 36 to 58 lakh, the top of the range here). Al-Azhar is free for many Muslim international students and is run separately from the secular system.'
             ' Cairo living is quoted at EGP 8,000 to 15,000 a month (about USD 165 to 310) but the pound has been volatile since the 2024 float. The route Nepal itself runs is postgraduate: the Medical Education Commission offers Government of Egypt scholarship seats for MD or MS (see the scholarship). ' + NMC + FX,
     'scholarships': ['s-mec-egypt-pg']},
    {'id': 'rs', 'country': 'Serbia', 'tuition': [157500, 1400000], 'living': [1260000, 4200000], 'code': 'RS',
     'exams': ['School certificate recognised by the Qualifications Agency (the ENIC/NARIC centre in Belgrade, up to 60 days)', 'Faculty entrance exam; medicine tests biology and chemistry, Belgrade and Kragujevac add an interview',
               'English (Kragujevac asks B2) for English taught programmes; a Serbian certificate for Serbian taught ones'],
     'intakes': 'October (academic year start); 2026/27 calls were published in spring 2026',
     'fields': ['Medicine (English, 6 years)', 'Dental medicine', 'Pharmacy', 'Engineering and IT', 'Economics', 'Veterinary medicine'],
     'work': 'Students need a National Employment Service work permit as well as temporary residence (expatsi.com); one agency page says up to 20 hours a week, which is the permit rule not a free right, so ask the university.',
     'stay_back': 'Not an automatic route: after a degree you apply for work or another residence ground; study time counts at half towards three years needed for permanent residence (expatsi.com).',
     'note': 'The University of Belgrade 2026/27 call lists Medicine in English at EUR 8,000 a year (EUR 48,000 over six years), Novi Sad medicine or dentistry in English EUR 7,000, Nis and Kragujevac medicine EUR 6,000, while most bachelor programmes cost a foreign student EUR 900 to 3,600 a year (studyu.org); another guide prints EUR 5,000 to 7,000 for medicine. Foreign students pay for the whole course and state funded places generally are not open to them.'
             ' Monthly living is EUR 850 to 2,000 in Belgrade and EUR 750 to 1,450 in Novi Sad, Nis or Kragujevac (studyinserbia.rs) while the University of Belgrade itself estimates EUR 600 to 800; the range here runs EUR 600 to 2,000. Nepali students normally need a Type D visa for stays over 90 days, then temporary residence (government fee RSD 23,880, expatsi.com), health insurance and proof of funds. ' + NMC + FX,
     'scholarships': []},
    {'id': 'qa', 'country': 'Qatar', 'tuition': [1620000, 2020000], 'living': [2380000, 4290000], 'code': 'QA',
     'exams': ['Qatar University undergraduate admission: school certificate, English proof, and college requirements', 'Branch campuses in Education City (Carnegie Mellon, Northwestern, Texas A&M, UCL) set their own entry rules'],
     'intakes': 'September; international undergraduate applications run about mid March to April (excelsiorscholarships.com)',
     'fields': ['Engineering', 'Business and economics', 'Health sciences', 'Computing', 'Arts and sciences'],
     'work': 'Not checked yet: no Qatari official page on student work was read.',
     'stay_back': 'Not checked yet. The residence permit is issued under university sponsorship within one month of arrival (qu.edu.qa).',
     'note': 'Qatar University is the public flagship and the Nepali student pays international fees: QAR 1,700 a credit hour on its own international students page, with at least 11 credit hours a term, so a year of 24 to 30 credits is about QAR 40,800 to 51,000 (the range here, QAR 1 about NPR 39.7). Other guides print QAR 800 to 1,500 a credit hour, so confirm the table for your college. Education City branch campuses are far higher, QAR 100,000 to 250,000 a year in one guide.'
             ' Doha living is about QAR 5,000 to 9,000 a month (brightkey.co); university dorm places are limited. No Nepal government scholarship for Qatar was found on the pages read. ' + FX,
     'scholarships': []},
]

SCHOLARSHIPS_ADD = [
    {'id': 's-ptap-pk', 'name': 'Pakistan Technical Assistance Programme (PTAP) scholarship, BSc Engineering and D Pharmacy', 'scope': 'abroad', 'levels': ['bachelor'],
     'by': 'Ministry of Economic Affairs, Government of Pakistan, nominated through MoEST and the Medical Education Commission, Nepal',
     'covers': 'A seat in a Pakistani institution for 2026/27 with exemption from tuition and other dues as per each institution\'s policy; travel, boarding and lodging are paid by the student (PTAP notice). Programme running since 1976.',
     'who': 'Nepali citizens who passed Grade 12 or equivalent with at least 60 percent (English, Physics, Chemistry and Mathematics for engineering; English, Physics, Chemistry and Biology for D Pharmacy) and hold an IBCC equivalence certificate. 2026/27 seats for Nepal: Civil Engineering 2, Computer Engineering 2, Electrical Engineering 2, D Pharmacy 8 (14 in all). The Ministry of Education notice ties selection to the IOE Pulchowk entrance merit list.',
     'how': 'The Ministry of Education notice (July 2026) said to apply on its Google Form with transcript, citizenship and IOE score card, while Edusanjal quoting the PTAP notice says to apply on entrance.mec.gov.np under MECEE-BL 2026; the deadline was Asar 26 2083 (10 July 2026). Placement is by the Ministry of Economic Affairs, and the student visa is issued only after it confirms admission. Read the next call on moest.gov.np before applying.',
     'link': 'https://moest.gov.np/content/13636/information-regarding-scholarship/', 'country': 'pk', 'type': 'Government', 'open': [6, 7], 'awards': 14},
    {'id': 's-mec-egypt-pg', 'name': 'Government of Egypt scholarship for MD or MS (Radiology and Internal Medicine)', 'scope': 'abroad', 'levels': ['master'],
     'by': 'Government of Egypt, offered through the Scholarship Section of the Ministry of Education, Science and Technology and the Medical Education Commission (MEC), Nepal',
     'covers': 'Postgraduate medical seats in Egypt for 2025/26. The pages read do not list the stipend, so check the Egyptian embassy or the ministry letter.',
     'who': 'Candidates on the MECEE-PG 2025 merit list. Egypt gave one seat each for MD or MS in Radiology and in Internal Medicine (Ministry letter ref 145 of 2082/01/26, Edusanjal).',
     'how': 'Apply online through your MEC profile (the 2025 window ran 27 to 30 May 2025); the final candidate is chosen in an Open House Matching Process where you must be present (31 May 2025). Calls repeat each year, so watch mec.gov.np.',
     'link': 'https://mec.gov.np', 'country': 'eg', 'type': 'Government', 'open': [5, 5], 'awards': 2},
]
