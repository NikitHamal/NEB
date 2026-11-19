"""Wave 35 exams. Read on 2026-11-19.
NEET UG: NTA bulletin figures as printed by collegedekho.com, indianexpress.com, msmunify.com, indiatvnews.com (fee Rs 9,500 for centres outside India, 2026 cycle), centre list of 14 cities
with Kathmandu code 9907 (careers360.com, collegedunia.com, unacademy.com), re-exam of 21 June 2026 (indianexpress.com, aakash.ac.in, notice of 7 June 2026).
JEE Main 2027 and DASA: JEE Main 2027 bulletin fees (myndaq.com, careerlauncheruae.com, ozitutors.com: Session 1 on 22 to 30 January 2027, registration to 22 November 2026, Kathmandu centre ZZ05);
DASA UG 2026 (bodmaseducation.com, shiksha.com, jeecounselling.in quoting the brochure version 1.5: JEE Main rank only, USD 300 plus tuition, SAARC half tuition waiver); official dasanit.org home page read.
CUET UG 2026: NTA notification text mirrored on clsite-file1.s3.amazonaws.com (fee outside India Rs 4,500 plus Rs 1,800 a subject, Kathmandu ZZ05), prepp.in, getmyuni.com, lptedtech.com, testbook.com.
Provincial PSC: Koshi Provincial Public Service Commission notices 104, 105 and 106 of 2083/84 (published 2083/06/26) as transcribed on unionnepal.com, 29 October 2026.
Rupee to NPR uses the fixed peg of NPR 1.6 per INR, rounded.
"""
GOVT_ADD = [
    {'id': 'e-neet-ug-india', 'track': 'ent_med', 'name': 'NEET UG (India) for MBBS, BDS, BAMS and nursing seats in India',
     'level': 'The single national medical entrance test of India, run by the National Testing Agency (NTA). Nepali students take it at the Kathmandu centre',
     'need': '+2 Science with Physics, Chemistry, Biology or Biotechnology and English; age 17 by 31 December of the admission year, no upper age limit',
     'age': '17 years or more by 31 December of the admission year',
     'body': 'National Testing Agency (NTA), India, neet.nta.nic.in',
     'stages': [['NEET UG written test', 'Pen and paper test of 3 hours (180 minutes) on Physics, Chemistry, Botany and Zoology, +4 for a right answer and -1 for a wrong one, 720 marks, offered in 13 languages. The qualifying cut off is the 50th percentile for the general category.', '720'],
                ['Counselling for a seat', 'Seat choice happens in the counselling of the Indian state or the Medical Counselling Committee, or directly in a private or deemed university. Foreign nationals mostly enter through the foreign national or management quota of a private or deemed college (hubintlglobal.com, studyinindiahub.com), so confirm the seat route per college.', '']],
     'subjects': ['Physics, Chemistry, Botany and Zoology from the NCERT Class 11 and 12 books', 'English plus the language of your choice for the paper'],
     'prep': ['Read the NCERT Biology books line by line; most Biology questions come straight from them',
              'Fix a college list only from the National Medical Commission (NMC) recognised list, because the Nepal Medical Council licensing exam (NMCLE) needs a recognised degree',
              'Get the Nepal no objection certificate for foreign study before you pay a seat fee (see the NOC guide)'],
     'note': ('2026 cycle: registration 8 February to 11 March 2026 (extended from 8 March), correction 12 to 14 March, fee Rs 9,500 (about NPR 15,200) for centres outside India against Rs 1,700 for a general candidate at an Indian centre, '
              'one of 14 foreign cities, with Kathmandu as city code 9907. The test planned for 3 May 2026 was held again on 21 June 2026 (Indian Express, Aakash notice of 7 June). NTA data for 2026 counted 927 foreign national registrants (msmunify.com). '
              'Nepali citizens need no visa to study in India (1950 Treaty), but the Indian degree only counts in Nepal after the NMCLE. The 2027 bulletin and dates are not out yet, so watch neet.nta.nic.in from about February.'),
     'prep_hours': 900, 'fee': 15200, 'apply': [2, 3], 'exam_month': 5},
    {'id': 'e-jee-main-dasa', 'track': 'ent_sci', 'name': 'JEE Main and DASA (BTech and BArch seats at NITs and IIITs for foreign nationals)',
     'level': 'JEE Main is the entrance test for NITs, IIITs and other centrally funded institutes; DASA (Direct Admission of Students Abroad) is the Government of India scheme that gives foreign nationals extra seats there',
     'need': '+2 or equivalent with Physics, Mathematics and one of Chemistry, Biotechnology, Computer Science or Biology; 75 percent (or 7.5 CGPA) in the best five subjects for DASA 2026',
     'age': 'Born on or after 1 October 2001 for DASA UG 2026 (check the new brochure each year)',
     'body': 'National Testing Agency for JEE Main (jeemain.nta.nic.in); DASA coordinated by IIEST Shibpur with NIC for the Ministry of Education (dasanit.org, csab.nic.in)',
     'stages': [['JEE Main Paper 1 (BE/BTech) or Paper 2A (BArch) or 2B (BPlanning)', 'Computer based test. Paper 1 has 75 questions for 300 marks with minus one for a wrong answer. Taken at the Kathmandu centre (city code ZZ05); the paper outside India is in English only.', '300'],
                ['DASA registration and choice filling', 'Online on the DASA and CSAB portal. The DASA enrolment fee for the SAARC category is USD 2,300 (USD 300 non refundable registration plus USD 2,000 first semester tuition) and USD 4,300 for non SAARC applicants.', ''],
                ['Seat allotment', 'Two rounds on the JEE Main common rank list, in up to 15 percent supernumerary seats per programme at 31 NITs, IIEST Shibpur, 18 IIITs and other centrally funded institutes (2026 brochure).', '']],
     'subjects': ['Physics, Chemistry and Mathematics (Class 11 and 12 NCERT level)', 'For BArch: Mathematics, aptitude and drawing'],
     'prep': ['Sit Session 1 in January and keep Session 2 in April as a second chance; the better rank counts',
              'Ignore old pages that say DASA uses the SAT: the 2026 brochure (version 1.5) allots seats on the JEE Main rank only',
              'DASA is not the same as JoSAA: JoSAA is the Indian citizen counselling, DASA is the separate foreign national pool'],
     'note': ('JEE Main 2027: Session 1 on 22, 23, 24, 28, 29 and 30 January 2027 with 31 January as a buffer day; registration closes on 22 November 2026 at 11:50 pm IST (one site lists a late window to 26 November with Rs 500 extra, so read the NTA notice); '
              'Session 2 in April 2027 (applications expected 5 January to 3 February 2027, to be confirmed). Fee at a centre outside India: Rs 5,000 for a general male and Rs 4,000 for a general female per paper per session (about NPR 8,000 and 6,400); '
              'Rs 2,500 for SC, ST and PwD. DASA UG 2026 registration closed on 3 August 2026. SAARC applicants get half the tuition waived when the qualifying exam was passed in a SAARC country, which covers the NEB +2 (bodmaseducation.com). '
              'The seat tuition then follows the institute: about Rs 125,000 a year is the domestic level used for the Gulf quota (brilliantqatar.com).'),
     'prep_hours': 700, 'fee': 8000, 'apply': [10, 11], 'exam_month': 1},
    {'id': 'e-cuet-ug', 'track': 'ent_biz', 'name': 'CUET UG (India central and state universities, BA, BSc, BCom and integrated courses)',
     'level': 'The Common University Entrance Test (Undergraduate) of the National Testing Agency, used by 280 plus universities in India; held at a Kathmandu centre',
     'need': 'Class 12 or equivalent (the NTA list accepts Cambridge A Level, IB and other boards; the NEB +2 is normally taken as equivalent but each university decides)',
     'age': 'No upper age limit at the NTA level; some university courses set one',
     'body': 'National Testing Agency (NTA), cuet.nta.nic.in',
     'stages': [['CUET UG computer based test', 'Up to 5 subjects chosen from 13 languages, 23 domain subjects and the General Test; +5 for a right answer and -1 for a wrong one. Offered in 13 mediums.', ''],
                ['University admission round', 'Each participating university publishes its own CUET subject combination and cut off. Foreign national seats are limited and run by the university or ICCR, so write to the international office before you pay.', '']],
     'subjects': ['Language paper (English, Hindi and others)', 'Domain subjects such as Physics, Chemistry, Mathematics, Biology, Economics, Accountancy, Business Studies, Political Science and History', 'General Test'],
     'prep': ['Pick the subjects your target university lists for your course; a wrong subject mix makes the score useless there',
              'Read NCERT Class 12 books, since the domain papers follow that syllabus',
              'Ask the university international office whether it admits foreign nationals on CUET or on another route'],
     'note': ('2026 cycle: notification 3 January 2026, registration to 30 January then extended to 4 February and reopened 23 to 26 February; the exam ran in mid May to early June (sources print 11 to 31 May and 13 May to 3 June). '
              'Fee: Rs 1,000 for a general candidate for up to 3 subjects in India, but Rs 4,500 for up to 3 subjects at a centre outside India plus Rs 1,800 for each extra subject (about NPR 7,200 and 2,900). Kathmandu is one of the foreign centres (ZZ05). '
              'The foreign centre list in 2026 had 14 to 15 cities. Treat the score as one of several routes: the ICCR and Embassy scholarships (see the ICCR entry) and private university direct admission stay open without it.'),
     'prep_hours': 300, 'fee': 7200, 'apply': [1, 2], 'exam_month': 5},
    {'id': 'g-provincial-psc', 'track': 'psc', 'name': 'Provincial Public Service Commissions (Koshi, Madhesh, Bagmati, Gandaki, Lumbini, Karnali, Sudurpashchim) and local government service',
     'level': 'Level 7 and 8 officer posts, plus lower levels, for provincial and local government service, set by the commission of each of the 7 provinces',
     'need': 'Bachelor for Level 7 (the post lists the exact degree, such as civil engineering, BSc Agriculture, BVSc, law or any bachelor for Section Officer); MBBS plus council registration for Level 8 Medical Officer',
     'age': '21 to 35 years, up to 40 for women and persons with disabilities, and 21 to 45 for health service posts (Koshi notice 106/2083-84)',
     'body': 'Provincial Public Service Commission of each province, for example psc.koshi.gov.np in Biratnagar',
     'stages': [['Written examination (post wise papers)', 'Two papers for most technical posts (Medical Officer, Engineer, Veterinary, Livestock, Public Health, Lab) and three for Education Officer; four papers for Section Officer and Accounts Officer. Centre announced by the commission.', ''],
                ['Computer skill, group assessment and interview', 'Held where the syllabus says so, after the written result. Open and inclusive candidates sit the first paper together.', '']],
     'subjects': ['General knowledge, province and local government law', 'Post specific technical paper', 'Computer skills test for non technical posts'],
     'prep': ['Get the syllabus from the commission of your province, not from a federal PSC page',
              'You can apply to more than one inclusive group, and you pay NPR 400 for each extra group in the Koshi notice',
              'Qualification, age and council registration must be complete on the regular deadline; the double fee date does not extend them'],
     'note': ('Koshi 2083/84 (notices 104, 105 and 106 published 2083/06/26): 69 competitive seats (49 technical and 20 non technical, 6 of them Level 8 Medical Officer) and 29 promotion posts for serving staff. Fee NPR 1,200 for Level 7 or 8 plus NPR 400 per extra group, '
              'regular deadline 2083/07/15, double fee deadline 2083/07/22, payment by 2083/07/23, online at the Koshi portal with PDF documents and both sides of the citizenship in JPG. Post wise written papers ran 2083/09/04 to 2083/10/25. '
              'Promotion forms (NPR 1,200 for Level 7, 2,000 for Level 9) are paper forms at the Biratnagar office and are not open competition. The other six provinces run their own calls, so fees and dates differ; the notice does not print a salary. '
              'An older blog prints NPR 300 and 400 for assistant level forms, so read each vacancy notice for the fee.'),
     'prep_hours': 400, 'fee': 1200, 'apply': [10, 10], 'exam_month': 12},
]

GOVT_NOTE_ADD = {
    'e-mecee': ('Indian students apply to Nepal in the reverse way: for 2026/27 the MEC opened foreign applications on 10 August 2026, with the MECEE-BL track closing on 31 August (late until 7 September) '
                'and a NEET based sub category closing on 2 October 2026 with a fee of INR 5,000 (alladmission.co.in, bodmaseducation.com). A Nepali student who wants a seat in India sits NEET UG instead and still needs the Nepal NOC.'),
}
