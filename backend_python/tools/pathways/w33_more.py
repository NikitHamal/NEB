"""Wave 33 part 2: Morocco destination and four scholarships that the Ministry of Education sent for publication in 2026.
Sources (read 2026-11-21): Nepal Register and Collegenp copies of the Ministry notices (Morocco civil engineering, 5 June 2026; UII Future Global Leaders
Scholarship, 5 May 2026; United International University BSc Data Science, 2 May 2026; Tianjin University 2026/27, 1 January 2026), educatenepal.com and
Edusanjal for the Embassy of India Mahatma Gandhi notice (goischolarship.com.np, 23 October to 15 November 2026) and smartacademyhq.com (prints 29 November).
Morocco costs: university.im (public MAD 1,000 to 5,000 a year, private MAD 40,000 to 120,000, USD 400 to 700 a month), qogentglobal.com (USD 500 to 2,000 public,
USD 300 to 600 a month), edunepal.com (USD 200 to 500 public, engineering USD 1,000 to 4,000, Al Akhawayn USD 8,000 to 12,000, USD 300 to 500 a month). USD 1 = NPR 145.
"""
ABROAD_ADD = [
    {'id': 'ma', 'country': 'Morocco', 'tuition': [14500, 1740000], 'living': [522000, 1218000], 'code': 'MA',
     'exams': ['Arabic or French for most public programmes (English is growing; check the programme page)', 'School certificate recognised by the Moroccan ministry', 'Engineering schools and medicine run their own selection'],
     'intakes': 'September (the academic year runs September to June)',
     'fields': ['Civil and other engineering', 'Medicine and pharmacy', 'Business (Al Akhawayn, English)', 'Agriculture and sciences'],
     'work': 'Not checked yet: no Moroccan official page on student work was read.',
     'stay_back': 'Not checked yet.',
     'note': 'Public university tuition is the cheapest in this list but the three guides read disagree: MAD 1,000 to 5,000 a year (university.im), USD 500 to 2,000 (qogentglobal.com) and USD 200 to 500, with engineering schools at USD 1,000 to 4,000 (edunepal.com). Private universities are about MAD 40,000 to 120,000 and Al Akhawayn University about USD 8,000 to 12,000, the top of the range here. Monthly living is USD 300 to 700 depending on the guide and city (Rabat, Fez and Marrakech cheaper than Casablanca).'
             ' Nepal\'s own route is the Government of Morocco civil engineering scholarship that the Ministry of Education passes on through the Nepal Embassy in New Delhi (5 seats for 2026/27, see the scholarship). A foreign engineering degree needs recognition checks with the Nepal Engineering Council before you rely on a licence. NPR figures are rough.',
     'scholarships': ['s-morocco-civil']},
]

SCHOLARSHIPS_ADD = [
    {'id': 's-morocco-civil', 'name': 'Government of Morocco scholarship in Civil Engineering (AMCI, 2026/27)', 'scope': 'abroad', 'levels': ['bachelor', 'master'],
     'by': 'Moroccan Agency for International Cooperation (AMCI), nominated through the Ministry of Education, Science and Technology, Nepal',
     'covers': 'Study in public Moroccan higher, technical and professional institutions; a living allowance of MAD 750 a month, about USD 80 (Collegenp quoting AMCI guidelines).',
     'who': 'Five seats for 2026/27: bachelor 3 (2 open and 1 for women) and master 2 (1 open and 1 for women), Civil Engineering only. Bachelor applicants must have passed Grade 12; master applicants need a bachelor degree and an entrance result or score card from the TU Institute of Engineering, Pulchowk (Nepal Register).',
     'how': 'The notice of 5 June 2026 asked for an online Google Form between 5 and 11 June 2026 within office hours; selection follows Nepal\'s scholarship nomination rules. Questions go to the Scholarship Section of the Ministry at Sanothimi, Bhaktapur. A new call is likely each year, so watch moest.gov.np.',
     'link': 'https://www.amci.ma', 'country': 'ma', 'type': 'Government', 'open': [6, 6], 'awards': 5},
    {'id': 's-uii-fgls', 'name': 'Future Global Leaders Scholarship (FGLS), Universitas Islam Indonesia', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'],
     'by': 'Universitas Islam Indonesia (UII), forwarded to the Ministry of Education by the Ministry of Foreign Affairs after the Indonesian Embassy in Dhaka',
     'covers': 'Registration fee, tuition, Indonesian language and culture course, health insurance, living allowance, accommodation allowance, book allowance and thesis allowance (Ministry notice, 5 May 2026).',
     'who': 'Nepali citizens for undergraduate, master and doctoral programmes in many majors at UII. You need an Indonesian or English language certificate, and academic certificates and transcripts certified by the Ministry of Education and the Ministry of Foreign Affairs, in English. No Indonesian Embassy recommendation letter is needed.',
     'how': 'Apply on the UII admission portal. Academic year 2026: Intake 1 ran 1 February to 30 April 2026 (undergraduate and postgraduate; results 29 May), Intake 2 ran 1 October to 30 November 2026 for postgraduate only (interviews 7 to 11 December, results 18 December). Shortlisted candidates go through document selection and an interview. UII International Affairs: io@uii.ac.id.',
     'link': 'https://www.uii.ac.id', 'country': 'id', 'type': 'University', 'open': [2, 4]},
    {'id': 's-uiu-ds-bd', 'name': 'United International University (Dhaka) BSc Data Science tuition waiver, 2 seats', 'scope': 'abroad', 'levels': ['bachelor'],
     'by': 'United International University (UIU), Bangladesh, nominated through the Ministry of Education, Science and Technology, Nepal (Rule 10(a) of the Scholarship Rules, 2060)',
     'covers': '100 percent tuition fee waiver for the BSc in Data Science (Collegenp, 2 May 2026). Other costs are not listed.',
     'who': 'Two seats, distributed inclusively: one open and one for women. You must have passed Grade 12 and hold an entrance result or score card for the undergraduate Data Science programme run by the School of Mathematical Sciences, Institute of Science and Technology, Tribhuvan University. Documents: Grade 10 and Grade 12 certificates and marksheets, passport information page and a passport size photo.',
     'how': 'The 2083 call opened on Baisakh 17 and closed on Baisakh 25 2083 (8 May 2026) on a Google Form published by the Ministry. Contact the Scholarship Section at Sanothimi, Bhaktapur. Expect a similar call after the next TU Data Science entrance.',
     'link': 'https://www.uiu.ac.bd', 'country': 'bd', 'type': 'University', 'open': [4, 5], 'awards': 2},
    {'id': 's-tianjin-moest', 'name': 'Tianjin University scholarship for Master and PhD (2026/27, via MoEST)', 'scope': 'abroad', 'levels': ['master', 'phd'],
     'by': 'Tianjin University, China, nominated through the Ministry of Education, Science and Technology, Nepal',
     'covers': 'Not listed on the notice pages read; the full notice is the PDF on the Ministry page.',
     'who': 'Eligible Nepali students for postgraduate and doctoral study in the subjects listed on the Ministry notice (the listing is in the PDF, not in the pages read).',
     'how': 'By a decision of 2082/09/16 the Ministry asked for applications on paper at its Scholarship Section, Sanothimi, Bhaktapur, within office hours until Poush 29 2082 (mid January 2026). Watch the Ministry for the 2027/28 call.',
     'link': 'https://www.tju.edu.cn', 'country': 'cn', 'type': 'University', 'open': [1, 1]},
    {'id': 's-ku-geomatics', 'name': 'Government of Nepal scholarship for BE Geomatics Engineering at Kathmandu University (21 seats)', 'scope': 'nepal', 'levels': ['bachelor'],
     'by': 'Department of Civil and Geomatics Engineering, Kathmandu University, with the Land Management Training Centre (LMTC) of the Ministry of Agriculture, Land Management and Cooperatives',
     'covers': '33 percent of the total fee for twenty one candidates, three from each province (KU announcement on Collegenp). Awardees can also get other KU scholarships under the admission call.',
     'who': 'Candidates who take the KUCAT, choose Geomatics Engineering and rank among the top three in their province; the province is read from the citizenship certificate.',
     'how': 'No separate form was found: you apply for BE Geomatics Engineering through the normal KU admission call and the ranking by province decides the awards (collegesinnepal.com, 2026-27 cycle).',
     'link': 'https://ku.edu.np', 'type': 'University', 'awards': 21},
]

SCHOLARSHIP_NOTE_ADD = {
    's-mgss': 'One third party page (smartacademyhq.com) prints 29 November 2026 as the deadline, while the Embassy notice quoted by educatenepal.com and Edusanjal says the portal closed at 00.00 on 16 November 2026, so trust the Embassy dates.',
}
