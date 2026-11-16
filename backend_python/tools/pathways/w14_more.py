"""Wave 14b: official KUSOM fees (som.ku.edu.np) and the Nepal Rastra Bank vacancy notice of 2083 Kartik 27. Plain sentences, no dashes.

Sources: Kathmandu University School of Management site (BBA Emphasis admission page and MBA page, read November 2026);
Nepal Rastra Bank notice of 2083/07/27 as reproduced by collegenp.com and educatenepal.com.
"""

PROVIDER_UPDATE = {
    'p-ku-school': {'website': 'https://som.ku.edu.np', 'seats': 120},
}

FEES = {
    'p-ku-school': {'bba': [960000, 960000], 'mba': [656000, 656000]},
}

NOTE_ADD = {
    'p-ku-school': 'Official fees (school website, Fall 2026 intake): the whole BBA (Emphasis) programme is NPR 9,60,000 plus a refundable caution deposit of NPR 10,000, and Honours students pay extra for the Honours courses; the whole MBA package is NPR 6,56,000 (deposit included), payable in 12 instalments, books and accommodation extra. '
                   'The application fee is NPR 1,500. SAARC students pay 1.5 times and other international students 2 times the MBA fee. BBA entry needs +2 with at least 40 percent or CGPA 1.6 and a D+ in each subject, then the entrance test, statement of objectives and interview; needy and deserving students can apply for a tuition waiver after admission. Figures can change without notice.',
}

GOVT_NOTE_ADD = {
    'g-so': 'A Public Service Commission notice reported on 14 November 2026 invites applications for gazetted third class posts (Section Officer or equal) in the civil, federal parliament and national human rights services and for Health Service 7th and 8th level posts; promotion applicants must submit by 2083 Mangsir 25 and the technical written exams start on 2083 Chaitra 14. Read the notice on psc.gov.np for the open competition groups, fee and dates.',
    'g-nrb': 'Current call (notice of 2083 Kartik 27): 61 vacancies, all online at jobs.nrb.org.np. Assistant Director (Administration) 26 seats, Accounts and Audit 3, Commercial Law 2, Information Technology 4, and Assistant (Second Class) 26. Applications close on 2083 Mangsir 17 (about 2 December 2026) and the double fee window ends on Mangsir 24 (about 9 December); age and certificates are counted on Mangsir 17. '
                   'Fees are NPR 1,000 for one group and NPR 400 for each more for Assistant Director, NPR 800 and NPR 300 for Assistant. Assistant applicants must hold a valid Public Service Commission preliminary qualification certificate (Kharidar, Level 4 or Level 5 equivalent) issued within one year. '
                   'Age at the deadline: Assistant Director 21 to 35 years for men and up to 40 for women; Assistant 18 to 35 and up to 40 for women. The IT group adds a practical test run by the bank. Probation is 1 year for men and 6 months for women, with a contribution based pension.',
}

FAQ_ADD = [
    {'id': 'fw14-15', 'topic': 'afterbach', 'q': 'What is open now at Nepal Rastra Bank?', 'go': ['banking-route', 'acca-route'],
     'a': 'A call of 2083 Kartik 27 lists 61 posts: 26 Assistant Director (Administration), 3 Accounts and Audit (CA, ACCA or CPA), 2 Commercial Law, 4 Information Technology and 26 Assistant (+2 with a valid PSC preliminary certificate). Apply online by 2083 Mangsir 17 (about 2 December 2026); a double fee window runs to Mangsir 24 (about 9 December). Read the notice for age and group fees.'},
    {'id': 'fw14-16', 'topic': 'after12', 'q': 'What does the BBA and MBA at Kathmandu University School of Management cost?', 'go': ['bba', 'mba'],
     'a': 'The school lists the whole BBA (Emphasis) at NPR 9,60,000 plus a NPR 10,000 refundable deposit, with Honours courses costing extra, and the whole MBA package at NPR 6,56,000 in 12 instalments. The application fee is NPR 1,500 and a tuition waiver is possible for needy students after admission. Confirm on the school site because the figures can change.'},
]


ABROAD_NOTE_ADD = {
    'kr': 'Proof of funds for the D-2 degree visa is quoted differently: one 2026 guide says a statement of at least KRW 9,000,000 (about USD 6,800) from three months of bank statements; two Nepali consultancies say about USD 20,000 including tuition, with sponsor statements. Universities and the Embassy of Korea in Kathmandu set the rule, so ask them. The visa fee is quoted at KRW 60,000 and the MoEST NOC is part of the file.',
    'jp': 'Language schools ask for JLPT N5 or an equal test (NAT-TEST 5Q, J-CERT) or about 150 hours of study; most degree programmes in Japanese want N2. The school applies for the Certificate of Eligibility (about 2 to 3 months), then you apply at the Embassy of Japan in Kathmandu (2 to 4 weeks, visa fee quoted at NPR 3,000 to 5,000). Sponsor fund figures vary from JPY 1.5 million to 3 million between guides, so use the figure your school gives in writing.',
}

FAQ_ADD = FAQ_ADD + [
    {'id': 'fw14-17', 'topic': 'abroad', 'q': 'How much money must I show for a South Korea student visa?', 'go': ['abroad-ms'],
     'a': 'Guides disagree. One says KRW 9,000,000 (about USD 6,800) from three months of statements; others say about USD 20,000 including tuition, with the sponsor six month statements. The university and the Korean Embassy in Kathmandu set the rule, so get the figure from them in writing and also prepare the MoEST NOC.'},
    {'id': 'fw14-18', 'topic': 'abroad', 'q': 'Do I need a Japanese language test before I apply to a school in Japan?', 'go': ['abroad-ms'],
     'a': 'For a language school, yes: JLPT N5 or an equal test (NAT-TEST 5Q or J-CERT) or about 150 hours of study is the usual proof. Degree programmes taught in Japanese ask for N2 or higher. Your school applies for the Certificate of Eligibility, which takes about 2 to 3 months, before you apply at the Embassy of Japan in Kathmandu.'},
]
