"""Wave 14: document guides (consular attestation, TU equivalence, foreign MBBS and Nepal licence) and 14 FAQs. Plain sentences, no dashes.

Sources: attorneynepal.com and digitalsolutionnepal.com (MoFA attestation, NPR 500 per document, Nepal E-Attestation System announced 6 August 2026;
the fee is quoted by law firm guides and was not confirmed on an official page); acadbuddy.com, thenext.edu.np and collegedarpan.com (TU Curriculum Development Centre
equivalence, NPR 1,000 or 4,000, HSEB +2 equivalence NPR 500); studyabroadfromnepal.com (foreign MBBS, NMCLE, minimum marks); gyanaedutech.com (NMCLE format).
"""

GUIDES_ADD = [
    {'id': 'mofa-attestation', 'name': 'Get a certificate attested for study abroad (MoFA consular stamp)', 'cat': 'Documents',
     'steps': [
         ['Get the SEE, +2 or university certificate and transcript verified first by the issuing board, university or the Ministry of Education (about 3 to 7 working days)', 5, 0, 'in person'],
         ['Apply on the Nepal E-Attestation System or book a slot at demand.nepalconsular.gov.np and wait for online approval', 2, 0, 'online'],
         ['Pay the Department fee, quoted at NPR 500 per document by law firm guides (check the portal)', 1, 500, 'online'],
         ['Take the originals, a copy and your citizenship copy to the Department of Consular Services at Tripureshwor (1 to 3 working days for the stamp)', 3, 0, 'in person'],
         ['If the country asks, legalise the stamped paper at its embassy in Kathmandu (embassy fees start near NPR 2,000)', 14, 2000, 'in person'],
     ],
     'docs': ['Original certificate and transcript', 'Photocopy of each document', 'Citizenship certificate copy', 'Passport copy if you hold one', 'Authorisation letter if someone submits for you'],
     'link': 'guide:noc-study-abroad'},
    {'id': 'tu-equivalence', 'name': 'Equivalence certificate for a foreign or non TU qualification', 'cat': 'Documents',
     'steps': [
         ['Ask at the TU Curriculum Development Centre (Kirtipur) whether your degree already has an equivalence; show the originals at the window', 1, 0, 'in person'],
         ['For a foreign +2 or A level, first get the HSEB equivalence at Sanothimi (about NPR 500 for HSEB board papers, NPR 1,000 for A level)', 7, 500, 'in person'],
         ['Fill the equivalence form and pay NPR 1,000 at Nepal Bank when the university is already recognised by TU, or NPR 4,000 when it is not', 1, 1000, 'in person'],
         ['If the university is not recognised, add the syllabus, thesis or project report and a translation when the paper is not in English', 2, 0, 'in person'],
         ['Collect the certificate when the Centre calls you; an online registration route exists on tucdc.edu.np', 14, 0, 'online'],
     ],
     'docs': ['Degree certificate and transcript', 'Character certificate', 'SEE mark sheet and certificate', 'Migration certificate where it applies', 'Passport and visa copy (not needed for India)', 'Syllabus and thesis for a non recognised university'],
     'link': 'guide:mofa-attestation'},
    {'id': 'foreign-mbbs-nepal', 'name': 'Study MBBS abroad and practise in Nepal', 'cat': 'Applications',
     'steps': [
         ['Before you pay anything, confirm that the college and the course are recognised by the Nepal Medical Council and listed in the World Directory of Medical Schools', 7, 0, 'online'],
         ['Check the minimum: NEB +2 Science with Physics, Chemistry and Biology, around 50 percent or GPA 2.4, and age 17 in the year of admission', 1, 0, 'online'],
         ['Get the NOC from the Ministry of Education, then the attested documents, before the visa', 14, 2000, 'in person'],
         ['Finish the course and the internship the college requires', 2190, 0, 'in person'],
         ['Return and pass the Nepal Medical Council licensing exam (NMCLE) to register; it is computer based', 120, 0, 'in person'],
     ],
     'docs': ['NEB +2 Science certificate', 'SEE certificate', 'Passport', 'NOC from the Ministry of Education', 'Attested documents', 'Written fee letter from the college'],
     'link': 'route:council-license'},
]

FAQ_ADD = [
    {'id': 'fw14-1', 'topic': 'abroad', 'q': 'Is a foreign MBBS valid in Nepal?', 'go': ['mbbs', 'council-license'],
     'a': 'Only if the Nepal Medical Council recognises the college and the course, and you then pass the NMCLE licensing exam and register after your internship. Check recognition before you pay a deposit, and keep the college fee letter and the recognition proof together.'},
    {'id': 'fw14-2', 'topic': 'abroad', 'q': 'An agency says its MBBS college is NMC approved. Does that count for Nepal?', 'go': ['mbbs'],
     'a': 'Not necessarily. Most agency pages mean the National Medical Commission of India, which is a different body. For a Nepali graduate the Nepal Medical Council recognition is the one that matters. Ask the Council, not the agency, and read the college entry on the World Directory of Medical Schools.'},
    {'id': 'fw14-3', 'topic': 'abroad', 'q': 'What does MBBS in Uzbekistan cost?', 'go': ['mbbs'],
     'a': 'Two agency lists quote tuition of USD 2,500 to 4,000 a year and up to USD 7,500, with living near USD 500 to 650 a month, over six years including the internship. That is roughly NPR 3.6 to 10.9 lakh a year for tuition alone at USD 1 about NPR 145. The work rule is not checked, so assume no income. Ask for a written fee letter and confirm Nepal Medical Council recognition first.'},
    {'id': 'fw14-4', 'topic': 'abroad', 'q': 'Can I work while studying in Bangladesh, the Philippines, Georgia or Czechia?', 'go': ['mbbs'],
     'a': 'Bangladesh: no, the student visa prohibits employment. Philippines: not on the student visa alone, a Special Work Permit is needed. Georgia: unclear, guides say 20 hours but others say jobs are informal. Czechia: yes without a separate work permit, but sources disagree on a 20 hour cap. Always confirm with the immigration office and your university.'},
    {'id': 'fw14-5', 'topic': 'abroad', 'q': 'Can I really work 40 hours a week as a student in Lithuania?', 'go': ['mba'],
     'a': 'The European Commission country page says non EU students can work up to 40 hours a week once they hold the temporary residence permit. Several agencies say 20 hours in term. Because sources disagree, ask the Lithuanian Migration Department and your university before you plan your budget around wages.'},
    {'id': 'fw14-6', 'topic': 'abroad', 'q': 'How much does it cost to study in Portugal?', 'go': ['mba'],
     'a': 'Public universities charge non EU students EUR 1,500 to 7,000 a year, with most programmes at EUR 3,500 to 7,000 and medicine at EUR 16,500 to 18,000 in 2026/27. Living is EUR 700 to 1,100 a month. For the visa, show about EUR 760 a month (EUR 9,120 a year); the figure follows the minimum wage and changes. Bachelor degrees are mostly in Portuguese.'},
    {'id': 'fw14-7', 'topic': 'abroad', 'q': 'Can I work while studying in Hong Kong and stay after?', 'go': ['abroad-ms'],
     'a': 'Full time degree students may work on campus up to 20 hours a week and take summer jobs and internships; since November 2024 a temporary exemption has lifted the hour limits for local degree programmes, and your No Objection Letter shows what applies. After graduating you can apply within six months for 24 months under IANG without a job offer.'},
    {'id': 'fw14-8', 'topic': 'abroad', 'q': 'Is there a fully funded PhD in Hong Kong open to Nepalis?', 'go': ['phd-route'],
     'a': 'Yes, the Hong Kong PhD Fellowship Scheme. It pays HKD 344,400 a year plus HKD 14,400 for travel for up to three years and is open to every nationality. For 2027/28 you register for a reference number by 1 December 2026 at noon Hong Kong time, and you still need admission from a participating university.'},
    {'id': 'fw14-9', 'topic': 'general', 'q': 'How do I get my certificates attested for a visa or a university abroad?', 'go': ['abroad-ms'],
     'a': 'Nepal does not use the apostille. Get the paper verified by the issuing board or university, apply to the Department of Consular Services (Tripureshwor) through the Nepal E-Attestation System or its appointment portal, pay the fee (law firm guides quote NPR 500 a document), collect the stamp and, if the country asks, legalise it at its embassy in Kathmandu. See the guide for the steps.'},
    {'id': 'fw14-10', 'topic': 'general', 'q': 'What is a TU equivalence certificate and who needs one?', 'go': ['abroad-ms'],
     'a': 'It states that a foreign or non TU qualification matches a TU one. You need it when a Nepali university, office or employer asks for that proof. The Curriculum Development Centre charges NPR 1,000 when the university is already recognised by TU and NPR 4,000 when it is not; a foreign +2 first needs HSEB equivalence. Check the fee at the window before you pay.'},
    {'id': 'fw14-11', 'topic': 'after12', 'q': 'When did the Indian Embassy scholarship (MGSS and GJSS) close this year?', 'go': ['bbs', 'be-civil'],
     'a': 'The 2026-27 window on goischolarship.com.np ran from 23 October to 15 November 2026 for MGSS (Class 11) and GJSS (first year bachelor). Both need an application made directly, not through an agent, and awardees send mark sheets by 31 December each year. The next call is expected in the same autumn months.'},
    {'id': 'fw14-12', 'topic': 'after12', 'q': 'How do Pokhara University scholarship seats work?', 'go': ['bba', 'be-computer'],
     'a': 'The university runs central scholarship entrance rounds and publishes calls for vacant seats during the year, the latest on 4 November 2026. Seats are split between open merit and reserved groups (disabled, martyr and conflict families, remote, Dalit, Janajati, Madhesi), with half of each for women. Read the notice for the deadline.'},
    {'id': 'fw14-13', 'topic': 'after12', 'q': 'Can I get a scholarship for a bachelor degree abroad?', 'go': ['abroad-ms'],
     'a': 'A few exist. The Lester B. Pearson scholarship at the University of Toronto needs school nomination and ran to 6 November 2026 for September 2027 entry. Turkiye Burslari, Stipendium Hungaricum and some university awards also take bachelor students. Start the application a full year ahead.'},
    {'id': 'fw14-14', 'topic': 'abroad', 'q': 'When does the Stipendium Hungaricum 2027/28 call open?', 'go': ['abroad-ms'],
     'a': 'The last call was published on 28 October 2025 and closed on 15 January 2026. For 2027/28 the call was not out in early November 2026, but expect the portal in mid November and a deadline about 15 January 2027. Watch stipendiumhungaricum.hu and prepare marks, a motivation letter and the national partner step.'},
]
