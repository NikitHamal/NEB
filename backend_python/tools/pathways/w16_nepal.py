"""Wave 16 Nepal side: A Level and IB schools, ICAN official fees, MEC fee text fix, A Level route text. Plain sentences, no dashes.

Sources (read 16 November 2026): ICAN official page en.ican.org.np/site/show/about-ca-education (CAP I NPR 34,500, CAP II NPR 40,500, CAP III NPR 50,000, eligibility);
kshitijpari.com, primeca.edu.np and kmcen.edu.np (lower or older ICAN and coaching fee quotes); the Medical Education Commission fee list for academic year 2083 as reproduced by edusanjal.com
(19 August 2026) and blog.educatenepal.com (an earlier copy dated 2023 gives the same MBBS figures); tipsnepal.com (2022 and 2024 lists of A Level and IB schools, fee guesses);
kharchapatra.com (May 2026, A Level fee ranges and Rato Bangala about NPR 40,000 a month); ischooladvisor.com (October 2026, The British School Kathmandu and Lincoln School);
ratobangala.edu.np and ullens.edu.np (both fetched; Ullens alumni notes name IBDP cohorts).
"""

PROVIDERS_ADD = [
    {'id': 'p-rbs', 'name': 'Rato Bangala School', 'kind': 'School', 'sector': 'Private', 'district': 'Lalitpur', 'place': 'Patandhoka', 'website': 'https://www.ratobangala.edu.np',
     'note': 'Co educational day school founded in 1992 with a post SEE programme that guides list for Cambridge A Levels; one 2026 guide says IBDP, so ask which diploma the next intake takes. A May 2026 guide quotes about NPR 40,000 a month for the A Level years including lunch, transport and lab; a 2022 list put the two years at NPR 11 to 12 lakh. Entry uses a public entrance test and is competitive.'},
    {'id': 'p-ullens', 'name': 'Ullens School', 'kind': 'School', 'sector': 'Private', 'district': 'Lalitpur', 'place': 'Khumaltar', 'website': 'https://www.ullens.edu.np',
     'note': 'Nepal school from Grade 1 to 12 that runs the IB Diploma Programme for Grades 11 and 12 (its alumni page names IBDP cohorts of 2017, 2020 and 2024). A 2024 guide quoted about NPR 75,000 a month for Grades 10 to 12; confirm the current fee in writing.'},
    {'id': 'p-tbs', 'name': 'The British School Kathmandu', 'kind': 'School', 'sector': 'Private', 'district': 'Lalitpur', 'place': 'Sanepa',
     'note': 'English National Curriculum school that reaches IGCSE and A Level with Cambridge International and Edexcel syllabi (October 2026 guide). A 2022 list expected NPR 20 to 25 lakh over two years and said it takes few outside A Level entrants. Ask the school for the written fee.'},
    {'id': 'p-malpi', 'name': 'Malpi International College', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Baluwatar',
     'note': 'Listed by a 2022 guide for A Levels at about NPR 6 to 7 lakh for two years with merit based scholarships. The guide is old, so confirm that the A Level intake and the fee still stand.'},
    {'id': 'p-chelsea', 'name': 'Chelsea International Academy', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'New Baneshwor',
     'note': 'Listed by a 2022 guide for A Levels at about NPR 6 to 7 lakh for two years, with need and merit scholarships for students who keep a top rank. Confirm the current intake and fee.'},
]

WHERE_ADD = {'a-levels': ['p-rbs', 'p-ullens', 'p-tbs', 'p-malpi', 'p-chelsea', 'p-trinity']}

FEES = {
    'p-sxc': {'a-levels': [500000, 500000]},
    'p-rbs': {'a-levels': [960000, 1200000]},
    'p-tbs': {'a-levels': [2000000, 2500000]},
    'p-malpi': {'a-levels': [600000, 700000]},
    'p-chelsea': {'a-levels': [600000, 700000]},
}

PROVIDER_NOTE_ADD = {
    'p-trinity': 'A 2022 list of Cambridge A Level schools also shows it offering A Level subjects from Grade 11. Ask for the current subject list, exam centre and total fee.',
    'p-sxc': 'A 2022 list quoted about NPR 5 lakh for the two A Level years, the lowest of the Cambridge schools, with no scholarships; confirm the current fee.',
    'p-ican': 'ICAN lists its own registration fees: CAP I NPR 34,500 (NPR 20,000 at registration, the rest within 3 months), CAP II NPR 40,500 (NPR 22,500 then NPR 18,000 within 6 months) and CAP III NPR 50,000 (NPR 25,000 then NPR 25,000 within a year). '
              'CAP I is open after +2 in any stream (a +2 pass with grade C or CGPA 2.0, with provisional registration while results wait), CAP II after CAP I or after a degree (50 percent with accounts, audit and tax as a major, 55 percent in other commerce or management degrees, 60 percent in any other degree), '
              'and each exam needs an online ICAN pre test passed months ahead. Coaching pages quote lower registration fees (NPR 27,500 to 30,100 for CAP I) and add NPR 3,200 for the exam and NPR 35,000 to 50,000 for classes, so use the ICAN figure and ask for the current exam fee.',
}

ROUTE_ABOUT_ADD = {
    'a-levels': 'Schools that guides list for A Levels in Kathmandu and Lalitpur include Rato Bangala, The British School, St. Xavier\'s College, Malpi, Chelsea and Trinity. Ullens School teaches the IB Diploma. Lincoln School Kathmandu follows an American diploma with Advanced Placement subjects instead, which is a separate route that US and Canadian universities read directly. '
                 'Two year totals quoted by guides range from about NPR 5 lakh to 25 lakh, and most guides are from 2022, so ask each school for a written fee and ask whether Tribhuvan University or the Medical Education Commission will accept your result before you enrol.',
    'ca-route': 'ICAN fees on its own page: CAP I NPR 34,500, CAP II NPR 40,500 and CAP III NPR 50,000 at registration, plus exam fees and coaching. No entrance test; each level needs an online pre test.',
}

TEXT_SWAP = {
    'route': {'mbbs': [['MEC fixes paying tuition at NPR 40.23 lakh inside Kathmandu Valley', 'MEC fixes paying tuition at NPR 41.68 lakh inside Kathmandu Valley (an older list had NPR 40.23 lakh)']]},
    'faq': {
        'f12-8': [['MBBS NPR 40.23 lakh inside Kathmandu Valley', 'MBBS NPR 41.68 lakh inside Kathmandu Valley (older lists show 40.23 lakh)']],
        'f7-1': [['MBBS is NPR 40,23,250 inside the Kathmandu Valley', 'MBBS is NPR 41,68,090 inside the Kathmandu Valley (an older list showed NPR 40,23,250)']],
    },
}
