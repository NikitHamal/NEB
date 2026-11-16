"""Wave 16 abroad side: Malta and Latvia, six scholarships for countries that had none, the COMPEX 2026 window. Plain sentences, no dashes.

Rates (late 2026, rough): EUR 1 = NPR 175. The notes say so, figures move.
Sources (read 16 November 2026, secondary unless named): studyu.org (University of Malta fees 2026/27 and visa costs), aspireglobalpathways.com and eecglobal.com (Malta work rule and
cost ranges, which disagree with studyu and the note says so); jarniascyril.com, meridean.org, leapscholar.com and visahowtoapply.com (Latvia fees, work 20 hours, visa EUR 60, RTU);
Aalto University and scholarshipclaude.com, globaladmissions.com (Aalto Excellence Scholarship, 7 December 2026 to 5 January 2027); scholars4dev.com (University of Helsinki waivers, 5 to 19 January 2027);
MOHE guidance as reproduced by findmymoney.app and scholarshipsfuture.com (Malaysia International Scholarship, 4 March to 3 April 2026, RM 1,500 a month);
greatyop.com, scholarships.af and scholarshipsedge.com (Kazakhstan, 550 awards, studyin.kz, 30 March to 31 May 2026); scholarshipscentral.com, propakistani.pk and masirborsia.com (MBZUAI);
zamin.uz and daryo.uz (New Uzbekistan Scholarship, April 2026); Embassy of India Kathmandu COMPEX 2026 notice (educatenepal copy, 27 August 2026).
"""

FX = ' NPR figures are rough, at EUR 1 about NPR 175.'

ABROAD_ADD = [
    {'id': 'mt', 'country': 'Malta', 'tuition': [1155000, 4550000], 'living': [1470000, 3423000], 'code': 'MT',
     'exams': ['IELTS 6.0 for most bachelor programmes and 6.5 for master programmes at the University of Malta (foundation year 5.5)'],
     'intakes': 'October at the University of Malta; visa applicants applied by 1 July in the 2026 round', 'fields': ['IT and AI', 'Business and commerce', 'Law', 'Health sciences', 'Psychology'],
     'work': 'Agency pages say a student can work up to 20 hours a week in term and full time in holidays, with the work permit arranged through the employer and Jobsplus. The rule was not read on a government page, so confirm it with your institution and Identita before you plan around income.',
     'work_hours': 20,
     'note': 'English is an official language and the only teaching language, in the European Union. For 2026/27 the University of Malta lists non EU fees of EUR 8,500 or EUR 10,800 a year for most bachelor degrees, EUR 6,600 for a foundation year, '
             'about EUR 10,800 to 13,400 for a whole full time master, and EUR 26,000 a year for medicine and dental surgery (one study site page, studyu.org). Other guides quote EUR 2,160 to 8,000 a year or EUR 5,000 to 12,000, so the sources disagree: ask the university for the written fee. '
             'Private institutions charge EUR 5,500 to 16,000 a year. Living is quoted at EUR 700 to 1,050 a month in some guides and EUR 1,360 to 1,630 by the university for shared accommodation. '
             'The study route is a long stay D visa through the Central Visa Unit (about EUR 100 to 150), insurance of at least EUR 30,000 and then a residence permit after arrival (about EUR 50).' + FX},
    {'id': 'lv', 'country': 'Latvia', 'tuition': [420000, 2625000], 'living': [945000, 1680000], 'code': 'LV',
     'exams': ['IELTS 5.5 or TOEFL iBT 72 at Riga Technical University', 'Interview or entrance test for some programmes'],
     'intakes': 'September; Riga Technical University closed its 2026 call on 15 July', 'fields': ['Engineering', 'Computer systems and IT', 'Architecture', 'Business', 'Medicine'],
     'work': 'Guides agree that a residence permit for study lets you work up to 20 hours a week in term and up to 40 hours in breaks, and say full time master and doctoral students face no hour cap. Confirm with the Office of Citizenship and Migration Affairs before you count on this.',
     'work_hours': 20,
     'note': 'A low cost European Union country with English taught degrees. Guides quote bachelor tuition at EUR 2,400 to 7,100 a year and master tuition at EUR 2,700 to 6,000, medicine and dentistry at EUR 8,000 to 15,000, and Riga Technical University at EUR 3,220 to 7,550 a year with a EUR 150 registration fee. '
             'Living is quoted at EUR 450 to 800 a month (Riga EUR 600 to 1,000, dormitory beds from about EUR 70 to 180). The student visa is quoted at EUR 60 and you then apply for a residence permit after arrival. Check the university is accredited in Latvia and, for medicine, ask the Nepal Medical Council before paying.' + FX},
]

ABROAD_UPDATE = {}

SCHOLARSHIPS_ADD = [
    {'id': 's-aalto', 'name': 'Aalto University Excellence Scholarship (Finland)', 'scope': 'abroad', 'levels': ['bachelor', 'master'], 'by': 'Aalto University',
     'covers': 'A waiver of the full tuition fee for the standard length of the degree (two years for a master, three for a bachelor). Living costs are not covered; Aalto advises at least EUR 800 a month.',
     'who': 'Non EU and non EEA applicants who must pay tuition and apply to an English taught Aalto bachelor or master programme. It is decided together with admission on academic merit and not every programme awards one.',
     'how': 'Answer yes to the scholarship question in the admission form. For autumn 2027 master programmes the window runs from 7 December 2026 to 5 January 2027, the application fee is EUR 100 and English test results must arrive by 12 January 2027. Dates are from secondary pages that copy the Aalto notice, so read admissions.aalto.fi before you apply.',
     'link': 'https://www.aalto.fi/en/admissions', 'country': 'fi', 'type': 'University', 'open': [12, 1]},
    {'id': 's-helsinki', 'name': 'University of Helsinki tuition fee waivers (Finland)', 'scope': 'abroad', 'levels': ['master'], 'by': 'University of Helsinki',
     'covers': '50 percent or 100 percent of the tuition fee for an English taught master programme (fees are EUR 13,000 to 18,000 a year; most waivers are 50 percent). Living costs are not covered.',
     'who': 'Citizens of countries outside the EU, EEA and Switzerland who pay tuition. Each master programme chooses its own recipients on grades, motivation letter and the scholarship answers. Waivers are given at admission only.',
     'how': 'Tick the waiver in the same Studyinfo.fi application as the programme. The autumn 2027 round runs from 5 to 19 January 2027 (closing times differ by programme) and applicants from outside the EU pay a EUR 100 application fee. The second year depends on study progress.',
     'link': 'https://www.helsinki.fi/en/admissions-and-education/tuition-fees-and-scholarships', 'country': 'fi', 'type': 'University', 'open': [1, 1]},
    {'id': 's-mis-my', 'name': 'Malaysia International Scholarship (MIS)', 'scope': 'abroad', 'levels': ['master', 'phd'], 'by': 'Ministry of Higher Education Malaysia',
     'covers': 'Tuition for the whole sponsored period paid to the university and a living allowance of RM 1,500 a month, paid every four months after a progress report. Paid work is not allowed without permission.',
     'who': 'Graduates from eligible countries for full time master or PhD study at one of 20 listed public and 4 private universities. Age up to 40 for a master and 45 for a PhD; CGPA 3.00 or Second Class Upper; a research proposal of at least 1,000 words for research degrees; IELTS 6.0 or TOEFL 550, or proof that the previous degree was taught in English. Check that Nepal is on the eligible country list in the current guidelines.',
     'how': 'Apply online at the MOHE portal (biasiswa.mohe.gov.my). The 2026/27 window ran from 4 March to 3 April 2026, so expect the next call about the same months of 2027. There is no application fee.',
     'link': 'https://biasiswa.mohe.gov.my/INTER/index.php', 'country': 'my', 'type': 'Government', 'open': [3, 4]},
    {'id': 's-kz-govt', 'name': 'Kazakhstan Government Scholarship for international students', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'], 'by': 'Ministry of Science and Higher Education of Kazakhstan, run by the Center for International Programs',
     'covers': 'Reports say the grant covers tuition, a monthly stipend and a hostel place, but one listing calls it partly funded, so read the call. The 2026 call had 550 awards: 490 bachelor, 50 master and 10 PhD.',
     'who': 'Foreign citizens (and ethnic Kazakhs who are not citizens) for full time study at Kazakh universities. Applications may be written in Kazakh, Russian or English.',
     'how': 'Apply at studyin.kz. The 2026 window ran from 30 March to 31 May 2026, so expect a similar call in spring 2027. Use only the official portal.',
     'link': 'https://studyin.kz', 'country': 'kz', 'type': 'Government', 'open': [3, 5]},
    {'id': 's-mbzuai', 'name': 'MBZUAI graduate funding (UAE, artificial intelligence)', 'scope': 'abroad', 'levels': ['master', 'phd'], 'by': 'Mohamed bin Zayed University of Artificial Intelligence, Abu Dhabi',
     'covers': 'Funded students get free tuition, health insurance, a return flight each year and a university sponsored residence visa. Published stipends for international students are AED 15,500 a month for the MSc and AED 17,500 for the PhD, and the newer notes say the stipend includes housing support. Older posts quoted far higher figures and free housing.',
     'who': 'Applicants with a relevant STEM degree, English test (IELTS 6.5, TOEFL iBT 90, PTE 60 or Duolingo 120 are quoted) and the programme screening. PhD students are funded centrally in year one while they match an advisor. MSc funding is not automatic with admission.',
     'how': 'Apply on the MBZUAI admissions site. For the autumn 2027 intake the main deadline is 15 December 2026 (5 pm Gulf time), the fee is AED 200, decisions are expected by 31 March 2027 and offers must be answered by 15 April 2027. The Master in Applied AI has its own deadline of 28 February 2027.',
     'link': 'https://mbzuai.ac.ae/admissions', 'country': 'ae', 'type': 'University', 'open': [9, 12]},
    {'id': 's-new-uz', 'name': 'New Uzbekistan Scholarship', 'scope': 'abroad', 'levels': ['bachelor'], 'by': 'Ministry of Higher Education, Science and Innovation of Uzbekistan',
     'covers': 'A state grant place at an Uzbek public university. Up to 500 foreign students a year can be funded from unused state grant quotas. The detailed benefits were not published in the sources read.',
     'who': 'Foreign bachelor applicants. A presidential decree reported in April 2026 introduced it from the 2026/27 academic year and moves foreign admissions to the Study in Uzbekistan platform. Students who finished a foreign language programme no longer need a language certificate for the next stage.',
     'how': 'Not announced for Nepal in the sources read. Watch the Study in Uzbekistan platform and the Uzbek embassy before you pay anyone, and note that Uzbek state scholarship quotas for local students are a separate scheme. Do not rely on agents.',
     'link': 'https://studyinuzbekistan.uz', 'country': 'uz', 'type': 'Government'},
]

SCHOLARSHIP_EXTRA = {
    's-turkiye': {'covers': 'Tuition, housing, health insurance, a return flight, a free one year Turkish language course and a monthly stipend. Published figures in 2026 are TRY 6,500 for a bachelor, TRY 9,500 for a master and TRY 13,000 for a PhD (older pages show lower figures). The minimum marks are 70 percent for associate and bachelor, 75 percent for graduate study and 90 percent for medicine, dentistry and pharmacy.'},
    's-csc': {'how': 'Apply online at campuschina.org with a pre-admission document from the university, then through the Chinese embassy for the bilateral route (Type A). Embassy deadlines fall between mid February and March. Bachelor applicants must also hold a CSCA score report from the new national test. '
                     'The embassy has also posted a Youth of Excellence Scheme for master applicants with at least three years of work experience, whose main instructions give 29 March 2027, 23:59 Beijing time, while a timetable lower on the same page still shows older dates (a secondary review of 31 October 2026), so read the embassy page. There is no single deadline for all applicants.'},
    's-sh': {'covers': 'Tuition, stipend, housing support and insurance. Secondary pages quote the stipend at HUF 43,700 a month for bachelor and master and HUF 140,000 to 180,000 for a PhD, and the 2026/27 timeline put university exams and interviews between mid March and the end of May, results from late June and acceptance by 1 August 2026 (scoring minimum 56 out of 100). All scholars take a Hungarian language course in year one.'},
    's-compex': {'open': [8, 9], 'how': 'The 2026/27 round ran online at indembkathmandu.gov.in from 27 August to 10 September 2026 (fee paid at Nepal SBI by 14 September, full application by 16 September), followed by a computer based test in Kathmandu in the fourth week of September 2026. '
                 'Expect the next call about August 2027. Candidates need at least 60 percent aggregate and 50 percent in English in Class 12 and 60 percent in each of Physics, Chemistry and Mathematics for BE or BTech (55 percent in Physics, Chemistry and Biology for BPharm, BSc Agriculture, BSc Food Technology and BSc Nursing). An embassy nomination does not guarantee a seat; the Indian university confirms it.'},
}
