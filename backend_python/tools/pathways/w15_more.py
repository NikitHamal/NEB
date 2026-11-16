"""Wave 15b: ACCA learning partners, three flying schools, MEXT window, four FAQs. Plain sentences, no dashes.

Sources (read November 2026): nishantgupta.com.np (September 2026), edusanjal.com (June 2026) and sterlingwells.edu.np (ACCA colleges in Kathmandu); the college sites
cca.edu.np, nca.edu.np, seedfinancial.edu.np and thebritishcollege.edu.np (each page names its Kathmandu locality); buddhaair.com (2024 list of pilot schools),
educatenepal.com (pilot entry rules, medical by CAAN); Embassy of Japan press release for the 2027 MEXT call and fundeddegree.com (Nepal research deadline 31 May 2026, a repost).
"""

ACCA_NOTE = ' Listed as an ACCA Approved Learning Partner by several college guides; the partner tier (Platinum, Gold) differs between sources, so check the ACCA site before you pay.'

PROVIDERS_ADD = [
    {'id': 'p-cca', 'name': 'Certified College of Accountancy (CCA)', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Thapagaun', 'website': 'https://cca.edu.np',
     'note': 'ACCA preparation college in Thapagaun, New Baneshwor, running since 2006 with a computer based exam facility.' + ACCA_NOTE},
    {'id': 'p-nca', 'name': 'NCA College of Management', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Min Bhawan', 'website': 'https://nca.edu.np',
     'note': 'Describes itself as the first ACCA college in Nepal (2004), at Min Bhawan, Battisputali. ACCA can be combined with a BBS.' + ACCA_NOTE},
    {'id': 'p-seed', 'name': 'Seed Financial Academy', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Dillibazar', 'website': 'https://seedfinancial.edu.np',
     'note': 'ACCA classes in classroom and online form at Dillibazar, with a computer based exam centre.' + ACCA_NOTE},
    {'id': 'p-tbc', 'name': 'The British College', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Thapathali', 'website': 'https://thebritishcollege.edu.np',
     'note': 'Private college at Thapathali whose British Professional College unit teaches ACCA; it also runs UK partnered business and IT degrees. Ask for the written fee and the awarding university for each degree.' + ACCA_NOTE},
    {'id': 'p-naa', 'name': 'Nepal Aviation Academy', 'kind': 'Institute', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Sinamangal',
     'note': 'Flying school near Sinamangal airport offering Private, Commercial and Airline Transport pilot licence courses, from a 2024 list of Nepal flying schools. Confirm the current CAAN approval, aircraft and total cost in writing.'},
    {'id': 'p-haa', 'name': 'Himalayan Aviation Academy', 'kind': 'Institute', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Sinamangal',
     'note': 'Flying school near Sinamangal airport with courses from Private to Airline Transport licence, plus upset recovery and mountain flying training, from a 2024 list. Confirm the current CAAN approval and total cost in writing.'},
    {'id': 'p-ofsn', 'name': 'Orient Flight School Nepal', 'kind': 'Institute', 'sector': 'Private', 'district': 'Morang', 'place': 'Biratnagar',
     'note': 'Biratnagar flying school listed for Private and Commercial licences, multi engine and instrument ratings, type rating and instructor courses. Confirm the current CAAN approval and total cost in writing.'},
]

WHERE_ADD = {
    'acca-route': ['p-cca', 'p-nca', 'p-seed', 'p-tbc'],
    'pilot-route': ['p-naa', 'p-haa', 'p-ofsn'],
}

NOTE_ROUTE = {
    'pilot-route': 'A CAAN medical, an age of at least 18 and +2 Science (physics and mathematics) are the usual entry rules quoted by guides; total training costs are high anywhere and are not listed here because published figures differ widely. Ask for a written fee that includes flying hours, exams and licence fees.',
}

SCHOLARSHIP_EXTRA = {
    's-mext': {'how': 'Apply via the Embassy of Japan in Kathmandu (written exam and interview, no application fee) or the university track. A repost of the Nepal embassy notice puts the 2027 research student deadline at 31 May 2026, so expect the next yearly call from about April 2027 and read the embassy page for the exact date and the undergraduate track.'},
}

FAQ_ADD = [
    {'id': 'fw15-11', 'topic': 'afterbach', 'q': 'Where can I study ACCA in Kathmandu?', 'go': ['acca-route', 'ca-route'],
     'a': 'College guides list Certified College of Accountancy (Thapagaun), NCA College of Management (Min Bhawan), Seed Financial Academy (Dillibazar), The British College (Thapathali), Seekshya Academy and Bright Academy (New Baneshwor) among the ACCA Approved Learning Partners. The partner tier differs between lists, so check the ACCA site, then compare the fee per paper and the exam dates. ACCA can also be studied beside a BBS.'},
    {'id': 'fw15-12', 'topic': 'after12', 'q': 'How do I become a pilot from Nepal?', 'go': ['pilot-route'],
     'a': 'Guides say you need to be at least 18, hold +2 Science with physics and mathematics, pass the CAAN medical, and then train for a Private and then Commercial licence at a flying school; a Commercial course takes about 12 months. Several schools sit near Sinamangal in Kathmandu and one in Biratnagar. Training is expensive and published costs vary a lot, so ask each school for a written total and confirm its CAAN approval first.'},
    {'id': 'fw15-13', 'topic': 'abroad', 'q': 'When does the MEXT Japan scholarship open for Nepal?', 'go': ['abroad-ms'],
     'a': 'The Embassy of Japan in Kathmandu runs it once a year. A repost of the embassy notice gives 31 May 2026 as the deadline for research students (master and above) for the 2027 intake, followed by a written exam and interview, and selection results between January and March of the next year. Expect the next call from about April 2027 and read the embassy page for the exact date.'},
    {'id': 'fw15-14', 'topic': 'general', 'q': 'How do I know a college website is the real one?', 'go': [],
     'a': 'Check three things: the page names the college and its town, the address ends in edu.np or is the one printed on the university affiliation list, and the fee, seat and affiliation numbers match the university notice. Many look alike sites belong to consultancies. When the college site and a consultancy differ, believe the university or board notice, and pay only through the college bank account.'},
    {'id': 'fw15-15', 'topic': 'after10', 'q': 'What is the Class 11 subject registration rule and fee for 2083/84?', 'go': ['plus2-science', 'plus2-management', 'open-school-see'],
     'a': 'The National Examination Board notice of 17 Bhadra 2083 says only students with at least GPA 1.6 in SEE can fill the Class 11 subject registration form, with the principal verified SEE grade sheet attached. The regular fee is NPR 400, due by 30 Ashoj 2083; the late fee is quoted as NPR 500 in total on one page and NPR 800 on another, and the school online entry window ends between 7 Kartik and 6 Mangsir 2083 depending on the copy. The dates have passed, so ask your school at once and read neb.gov.np. An NEB calendar plans the next Grade 12 exams in Baisakh 2084 with the routine out by 15 Falgun 2083.'},
    {'id': 'fw15-16', 'topic': 'afterbach', 'q': 'When do Lok Sewa notices come out in 2083/84?', 'go': ['lok-sewa'],
     'a': 'A calendar summary of the 2083/84 plan says Kharidar and Nayab Subba notices are published in the first week of Shrawan and again in Baisakh with exams in Ashoj and Asar; gazetted second class (Section Officer) notices come in the last week of Ashoj with written exams in Mangsir and Poush; gazetted first class notices come in the last week of Bhadra with exams in Kartik and Mangsir. For the Armed Police Inspector the notice is due in the first week of Poush with exams in Magh and Falgun. It is a plan and dates slip, so confirm on psc.gov.np.'},
    {'id': 'fw15-17', 'topic': 'abroad', 'q': 'How much do IELTS, PTE and Duolingo cost in Nepal?', 'go': ['abroad-ms'],
     'a': 'IELTS Academic or General Training on computer is NPR 36,000 at both the British Council and IDP according to centre pages quoted in October 2026; IELTS for UKVI is NPR 36,400 and IELTS Life Skills NPR 29,000. Guides quote PTE Academic at about USD 220 and the Duolingo English Test at about USD 70. Fees change without notice, so read the live price at booking, and ask your university which test it accepts before you pay.'},
]
