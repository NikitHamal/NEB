"""Wave 18 abroad side: seven scholarships for destinations that had none, 2026 funds and work rules for 15 destinations. Plain sentences, no dashes.

Sources (read 18 November 2026): VIAA Latvia (viaa.gov.lv, globaladmissions.com, titansabroad.org, studycountry.com); MEC and DGME Bangladesh SAARC quota 2025/26
(edusanjal.com, smartacademyhq.com); OSCE Academy Bishkek 2027-2029 call (greatyop.com, scholarships.af); Ilia State University and University of Georgia (iliauni.edu.ge,
edu-mentor.com, leapscholar.com); ADB-JSP and SEARCA Philippines (searca.org, wemakescholars.com); University of Nicosia and Gov.cy Cyprus (gov.cy, uni2study.com,
afterschoolafrica.com); University of Malta and Get Qualified (leapscholar.com, aaraconsultancy.com, timeshighereducation.com); France VLS-TS (ccfs-sorbonne.fr,
study-abroad.org, thehonestjourney.com); Austria OeAD 2026 (college-council.com, degreestep.com, akbild.ac.at); Belgium 2026/27 (cekrel.com, thechopras.com,
study-abroad.org, studyineurope.eu); Spain IPREM 2026 (eecglobal.com, vamospanish.com); Italy 2026/27 (gostudyin.com); Poland (leverageedu.com, wise.com, upgrad.com);
Singapore MOE Tuition Grant (thehonestjourney.com); Taiwan NIA and WDA (spainexchange.com, admission.taiwan-world.net); Malaysia EMGS 2026 (globaladmissions.com, studyu.org).
"""

SCHOLARSHIPS_ADD = [
    {'id': 's-latvia-state', 'name': 'Latvian State Scholarships for Studies (VIAA)', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'],
     'by': 'State Education Development Agency (VIAA), Ministry of Education and Science of Latvia',
     'covers': 'A monthly living stipend for up to 10 months (11 months for PhD): Study in Latvia lists EUR 500 a month for bachelor and master students and EUR 700 for PhD candidates, while several scholarship guides list EUR 500 for bachelor, EUR 600 for master and EUR 700 for PhD. Tuition, travel and insurance are not covered unless waived by the host university.',
     'who': 'Citizens of the 39 countries that hold a bilateral education agreement with Latvia or offer reciprocal grants to Latvian citizens. Bachelor applicants must have already completed at least one academic year of higher education. Check that Nepal is on the active VIAA country list before you apply.',
     'how': 'Apply online at scholarships.viaa.gov.lv with a confirmation letter from a Latvian university, transcripts, CV and motivation letter. The annual call runs from 1 February to 1 April.',
     'link': 'https://www.viaa.gov.lv/en/latvian-state-scholarships', 'country': 'lv', 'type': 'Government', 'open': [2, 4]},
    {'id': 's-bangladesh-saarc', 'name': 'Bangladesh Government SAARC Quota (MBBS and BDS)', 'scope': 'abroad', 'levels': ['bachelor'],
     'by': 'Directorate General of Medical Education (DGME), Bangladesh, nominated through MEC and MOEST Nepal',
     'covers': 'A government medical or dental college seat where SAARC students pay tuition at the domestic Bangladeshi government rate instead of the private foreign package, with subsidised hostel access.',
     'who': 'Nepali citizens on the latest MECEE-BL merit list with a combined SEE and Class 12 GPA of at least 8.0 on the 10 point Bangladesh scale. In the 2025/26 MEC notice Nepal had 19 MBBS seats (9 Open, 2 Woman, 1 Dalit Woman, 1 Dalit, 1 Aadibasi Janajati, 2 Khas Arya, 1 Madhesi, 1 Tharu, 1 Underprivileged) and 3 BDS seats (2 Open, 1 Madhesi) out of 224 foreign seats.',
     'how': 'Apply first on the DGME Bangladesh portal and then submit the MEC Nepal online application when the Examination Directorate opens the window (the 2082 call ran from 11 to 13 December 2025).',
     'link': 'https://mec.gov.np', 'country': 'bd', 'type': 'Government', 'open': [11, 12]},
    {'id': 's-osce-bishkek', 'name': 'OSCE Academy in Bishkek Master Scholarship (Kyrgyzstan)', 'scope': 'abroad', 'levels': ['master'],
     'by': 'OSCE Academy in Bishkek, Kyrgyz Government and OSCE',
     'covers': 'Full tuition waiver for the 18 month MA (Politics and Security, Economic Governance and Development, or Human Rights and Sustainability), a monthly stipend of EUR 450, economy return airfare to Bishkek, basic medical insurance and competitive funded internships in Europe or Central Asia.',
     'who': 'Graduates with a four year bachelor degree (or 240 ECTS) and strong English (IELTS 6.5 or TOEFL iBT 90 are quoted). Open to citizens of Central Asia, Afghanistan, Mongolia and OSCE participating or partner states; check that your nationality is eligible on the specific programme call before applying.',
     'how': 'Register and submit the online form on the OSCE Academy admissions portal. For the 2027 to 2029 cohort the deadline is 31 January 2027 at 11 pm Bishkek time.',
     'link': 'https://osce-academy.net', 'country': 'kg', 'type': 'University', 'open': [10, 1]},
    {'id': 's-ilia-georgia', 'name': 'Ilia State University and Georgian University Merit Waivers', 'scope': 'abroad', 'levels': ['bachelor', 'master'],
     'by': 'Ilia State University, Tbilisi State University and the University of Georgia',
     'covers': 'Partial tuition fee waivers on a competitive basis: Ilia State University publishes up to 50 percent tuition reduction for selected international programmes (medicine MD is not guaranteed), and the University of Georgia Tbilisi lists up to 20 to 30 percent merit discounts.',
     'who': 'International applicants with strong Class 12 marks or high semester GPAs after enrolment. Medicine applicants should budget for the full fee and treat any waiver as a bonus.',
     'how': 'Tick the scholarship or waiver request inside the university admission application and ask for written confirmation of the net tuition fee before paying.',
     'link': 'https://iliauni.edu.ge/en/international-students', 'country': 'ge', 'type': 'University', 'open': [3, 7]},
    {'id': 's-adb-uplb-ph', 'name': 'ADB-JSP at UP Los Banos, IRRI and AIM (Philippines)', 'scope': 'abroad', 'levels': ['master'],
     'by': 'Asian Development Bank and the Government of Japan at designated Philippine institutions',
     'covers': 'Full tuition, a monthly subsistence and housing allowance, medical insurance, books and thesis grant, and economy return airfare.',
     'who': 'Citizens of ADB developing member countries, including Nepal, aged 35 or under with a bachelor degree and at least two years of full time work experience, admitted to an approved master programme at the University of the Philippines Los Banos (with IRRI) or the Asian Institute of Management. Note that SEARCA own scholarships at UPLB are restricted to the 11 SEAMEO Southeast Asian countries and do not cover Nepal.',
     'how': 'Apply for admission to UPLB or AIM and submit the ADB-JSP sheet at least six months before the intake.',
     'link': 'https://www.adb.org/work-with-us/careers/japan-scholarship-program', 'country': 'ph', 'type': 'Government', 'open': [5, 9]},
    {'id': 's-unic-cyprus', 'name': 'University of Nicosia and Open University of Cyprus Waivers', 'scope': 'abroad', 'levels': ['bachelor', 'master'],
     'by': 'University of Nicosia (UNIC) and Open University of Cyprus',
     'covers': 'Partial tuition reductions of 10 to 50 percent on bachelor marks at UNIC, or 20 to 30 percent on selected master degrees such as the Master of Public Health (cutting EUR 13,950 to EUR 11,160). Living costs are not covered.',
     'who': 'International applicants meeting the grade bar or financial need rules. Note that the full CyprusAid scholarship at UNIC is restricted to 10 African nations and Cyprus EU Presidency scholarships are for Cypriot and European citizens, so Nepali students only qualify for university fee reductions.',
     'how': 'Apply with your admission file (EUR 60 application fee at UNIC). Open University of Cyprus closed its 2026/27 scholarship call on 3 June 2026.',
     'link': 'https://www.unic.ac.cy', 'country': 'cy', 'type': 'University', 'open': [3, 7]},
    {'id': 's-um-malta', 'name': 'University of Malta Tuition Waivers and Get Qualified Rebate', 'scope': 'abroad', 'levels': ['bachelor', 'master'],
     'by': 'University of Malta, MCAST and the Government of Malta',
     'covers': 'University of Malta waives 40 to 100 percent of non EU tuition for top applicants on academic merit and interview. Separately, Malta Get Qualified scheme refunds up to 70 percent of tuition (capped at EUR 12,500) only as a future income tax credit if you stay, work and pay tax in Malta after graduation.',
     'who': 'Non EU applicants with strong Class 12 or bachelor marks. Never let an agent count the Get Qualified tax credit as a discount on your first year tuition.',
     'how': 'Apply in one of the three University of Malta scholarship rounds (deadlines quoted on 31 January, 31 May and 31 October) alongside admission.',
     'link': 'https://www.um.edu.mt', 'country': 'mt', 'type': 'University', 'open': [1, 10]},
]

ABROAD_UPDATE = {
    'es': {'work_hours': 30, 'work': 'Since the Spanish immigration reform (RD 1155/2024 Article 190), higher education students on a Type D study permit can work up to 30 hours a week without a separate work permit, provided the hours do not clash with classes, and full time during academic holidays.'},
    'tw': {'work_hours': 20, 'work': 'International degree students who obtain a work permit from the Workforce Development Agency (fee NTD 100) may work up to 20 hours a week during the semester and without an weekly hour cap during winter and summer vacations.'},
}

ABROAD_NOTE_ADD = {
    'fr': 'For a 2026 long stay student visa (VLS-TS, fee EUR 50 to 99 plus EUR 50 to 75 OFII validation and EUR 103 to 105 CVEC fee) you must prove at least EUR 615 a month in living funds (EUR 6,150 for 10 months or EUR 7,380 for 12 months), though Paris living costs are closer to EUR 1,000 to 1,400 a month. The visa includes the right to work up to 964 hours a year (about 20 hours a week at the EUR 11.88 gross minimum wage), and master graduates can apply for a two year post study job search permit (RECE / APS).',
    'at': 'Non EU students at public universities pay EUR 726.72 a semester in tuition plus the OH union fee of EUR 25.20 to 26.20, while citizens of countries on Austria Least Developed Countries list have tuition waived at public universities such as the University of Vienna and TU Wien and pay only the union fee. For the 2026 Residence Permit Student (fee EUR 218) OeAD requires 12 months of funds in advance: EUR 722.58 a month if under 24 (EUR 8,670.96 a year) or EUR 1,308.39 a month from age 24 (EUR 15,700.68 a year), plus any rent above EUR 386.43 a month, OeGK student insurance (EUR 78.84 a month) and at least 16 ECTS a year to renew.',
    'be': 'For the 2026/27 intake the published minimum financial proof for a Belgian Type D student visa is EUR 1,062 net a month (about EUR 12,744 a year, often placed in a university blocked account or guaranteed on an Annex 32 sponsor form; one older guide still quotes EUR 759 a month), and the long stay visa fee rose to EUR 250 in July 2026. Priority English master deadlines fall on 1 March at KU Leuven and Ghent University, and graduates can apply for a 12 month search year permit.',
    'es': 'For a 2026 Spanish Type D student visa you must prove 100 percent of IPREM for each month of stay, which is EUR 600 a month (EUR 7,200 for a 12 month year), plus private health insurance with zero co payments and repatriation, and a police clearance and medical certificate for stays over 180 days.',
    'it': 'Before applying for the visa you must complete pre enrolment on the Universitaly portal. Guides for the 2026/27 cycle report that the required student visa proof of funds has risen to EUR 10,179.85 a year (older pages still quote about EUR 6,079), and students may work up to 20 hours a week (capped at 1,040 hours a year). Regional DSU scholarships waive tuition and pay a stipend based on family income documents (ISEE Parificato).',
    'pl': 'For a Polish D type student visa (fee EUR 60 to 80) authorities require living funds for the stay (older rules cite PLN 701 a month while newer 2025/26 guides cite PLN 1,086 a month or about EUR 6,400 for a year) plus PLN 2,500 for a return ticket to a non EU country and EUR 30,000 health insurance. The Polish minimum wage in 2025/26 is PLN 4,666 a month (PLN 30.50 an hour gross).',
    'sg': 'At Singapore six publicly funded universities the Ministry of Education Tuition Grant cuts international tuition sharply, but requires you to sign a legally binding three year service bond to work for a Singapore registered employer after graduation. Only full time students at approved public institutions may work up to 16 hours a week in term; private institute students cannot work.',
    'tw': 'Degree students get an Alien Resident Certificate (ARC, NTD 500 a year) after arrival and medical check, can work up to 20 hours a week in term with a WDA permit (NTD 100), and since 2024 can extend the ARC for up to two years after graduation to look for work.',
    'my': 'All applications go through Education Malaysia Global Services (EMGS) for an electronic Visa Approval Letter (eVAL, about 14 working days); first year mandatory EMGS, eVAL, medical screening, insurance and pass charges total about USD 680 to 740 (RM 2,770 to 3,020). Student Pass holders may work up to 20 hours a week ONLY during semester breaks or holidays longer than seven days, never during term, and only in restaurants, hotels, petrol stations and mini markets.',
    'cn': 'International bachelor applicants to Chinese universities now sit the China Scholastic Competency Assessment (CSCA) alongside university screening, and apply for an X1 visa (for study over 180 days, converted to a residence permit within 30 days of arrival) using the JW201 or JW202 form.',
    'in': 'Nepali citizens do not need a passport visa to enter India, but medical and dental candidates must pass Nepal MECEE-BL for foreign study eligibility and Indian universities require AIU equivalence when your board is not already on their list.',
    'tr': 'Public university tuition in Turkiye is far lower than private foundation universities, and all international students must register for a student residence permit (ikamet) with provincial migration authorities after arrival.',
    'ru': 'Russian government quota applications go through education-in-russia.com and Russian House in Kathmandu; medical students must verify that the university and language track meet both Russian Roszdravnadzor and Nepal Medical Council rules.',
    'th': 'Holders of a Thai Non Immigrant ED student visa must file 90 day address reports with Thai Immigration and renew their extension of stay before expiry; off campus work is prohibited without a work permit.',
    'ae': 'Student visas in Dubai and Abu Dhabi are sponsored by the university (usually renewed yearly for AED 2,500 to 4,000 including Emirates ID and medical test) or granted as a 5 year Green / Golden student residence visa for high GPA graduates.',
}
