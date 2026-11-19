"""Wave 36 Nepal data, read on 2026-11-19.
Gandaki notice 169/2083-84 (2083/07/11): sarkarijagir.com transcription with the post table, madanibeat.com 28 Oct 2026 (single fee to Mangsir 1, double fee to Mangsir 8).
Lumbini notice 84/083-084: educatenepal.com vacancy page, loksewas.com list (published 2083 Asoj 30, last date Kartik 19).
Karnali notice 14/2083-84 (2083/06/27): unionnepal.com, 24 Oct 2026, loksewas.com list (Asoj 27 to Kartik 16).
Madhesh notice 107/2083-84 (9th level): educatenepal.com. Sudurpashchim 103/082-083 (assistant 4th level, 44 posts): educatenepal.com.
Federal promotion notices 787, 788, 580 and 581 of 2083/84: unionnepal.com, 13 Nov 2026.
Websites: each domain answered HTTP 200 over valid HTTPS and the page title or text named the college (read 2026-11-19).
"""
PSC_COMMON_PREP = [
    'Get the syllabus from the commission of your province, not from a federal PSC page',
    'Open, inclusive and inter level groups are separate advertisements, and each extra group costs extra, so list your groups before you pay',
    'Qualification, age and council registration must be complete on the regular deadline; the double fee date does not extend them',
]

GOVT_ADD = [
    {'id': 'g-gandaki-psc-l7', 'track': 'psc',
     'name': 'Gandaki Province Level 7 officer posts (Notice 169/2083-84): 75 seats',
     'level': 'Seventh level (officer) technical and non technical posts of the Gandaki provincial civil service and local service, run by the Gandaki Province Public Service Commission in Pokhara',
     'need': 'Bachelor level qualification in the subject each post names, with council registration where the post is an engineering or health post; read the exact degree in the advertisement for your post',
     'age': '21 to 35 years, up to 40 for women and persons with disabilities, 21 to 45 for health service posts; no limit for permanent federal, provincial or local service employees',
     'body': 'Province Public Service Commission, Gandaki Province, Pokhara (onlineppsc.gandaki.gov.np)',
     'stages': [
         ['Written examination', 'Two papers for most posts, three for Education posts, held in Pokhara from 2083/09/04 to 2083/09/30 (Engineer 04 and 05, Agriculture 09 and 10, Veterinarian 15 and 16, Computer Engineer 29 and 30). Administrative, Accounts, Revenue and Internal Audit Officers sit a first phase on 2083/09/18 and a second phase announced with the first result.', ''],
         ['Practical test and interview', 'Dates are announced after the written result.', '']],
     'subjects': ['General knowledge, province and local government law', 'Post specific technical paper', 'Computer skill test where the syllabus says so'],
     'prep': PSC_COMMON_PREP,
     'note': ('Notice 169/2083-84 published 2083/07/11 lists 75 competitive seats: 48 technical (Engineer 12, Agriculture Officer 9, Education and Section Officer Education 8, Livestock Development Officer 6, Veterinarian 4, Medical Record Officer 2, Radiography Technologist 2, Survey Officer 1, Nursing Officer 1, Medical Lab Technologist 1, Physiotherapist 1, Public Health Officer 1) '
              'and 27 non technical (Administrative Officer 15, Accounts Officer 6, Revenue Officer 2, Internal Audit Officer 2, Computer Engineer 2). Fee NPR 1,200 plus NPR 400 for each extra inter level or inclusive group; regular deadline 2083/08/01, double fee to 2083/08/08, fee payment by 2083/08/09. '
              'Total counted from the notice table (sarkarijagir.com, 28 October 2026); the notice does not print a salary.'),
     'prep_hours': 400, 'fee': 1200, 'apply': [10, 11], 'exam_month': 12},
    {'id': 'g-lumbini-psc-l9', 'track': 'psc',
     'name': 'Lumbini Province Level 9 officer posts (Notice 84/083-084): 25 seats',
     'level': 'Ninth level (senior officer) technical and non technical posts in Local Administration, Health, Engineering and Education, and Province Health, Engineering, Agriculture, Education and Forest groups, run by the Lumbini Province Public Service Commission in Butwal',
     'need': 'Set by each advertisement: the degree, the years of service or experience and the council registration for the post; read the notice text for your group',
     'age': '21 to 45 years for civil service posts and up to 45 for health service; no limit for permanent federal, provincial or local service employees',
     'body': 'Province Public Service Commission, Lumbini Province, Butwal (ppsconline.lumbini.gov.np)',
     'stages': [
         ['Written examination', 'Held in Butwal. Dates, time and venue come later on ppsc.lumbini.gov.np. Province services also test case study, analysis and a presentation.', ''],
         ['Interview', 'After the written result.', '']],
     'subjects': ['Management, public administration and law', 'Post specific technical paper', 'Case study and presentation for province services'],
     'prep': PSC_COMMON_PREP,
     'note': ('Notice 84/083-084 (published 2083 Asoj 30) is for 25 posts through inter level, open and inclusive competition. Fee NPR 1,200 plus NPR 500 for each extra group or post; regular deadline 2083/07/19 (5 November 2026), double fee to 2083/07/26 (12 November 2026). '
              'The posted age line says 2087-07-19, a typing slip for 2083-07-19. The commission also had a notice for 8th and 11th level posts closing the same day, and the annual 2083/84 calendar is on ppsc.lumbini.gov.np.'),
     'prep_hours': 450, 'fee': 1200, 'apply': [10, 11]},
    {'id': 'g-karnali-psc-l5', 'track': 'psc',
     'name': 'Karnali Province Level 5 assistant posts (Notice 14/2083-84): 64 seats',
     'level': 'Fifth level (assistant) technical and non technical posts of the local service in Karnali, run by the Karnali Province Public Service Commission in Birendranagar, Surkhet',
     'need': 'Set by each advertisement (technical posts name a certificate or diploma in agriculture, veterinary, education or health); read the notice text for your post',
     'age': 'Upper limit 35 years, 40 for women and persons with disabilities and 45 for health service applicants (unionnepal.com reading of the notice)',
     'body': 'Province Public Service Commission, Karnali Province, Birendranagar (ppsc.karnali.gov.np)',
     'stages': [
         ['Written examination', 'Held at Birendranagar, Surkhet in earlier Karnali calls; the centre and dates of this call are announced later.', ''],
         ['Computer skill test and interview', 'Where the syllabus says so, after the written result.', '']],
     'subjects': ['General knowledge, province and local government law', 'Post specific paper', 'Computer skill test'],
     'prep': PSC_COMMON_PREP,
     'note': ('Notice 14/2083-84 (published 2083/06/27) lists 64 local service posts, 32 non technical and 32 technical (Health Assistant 12, Technical Assistant Education Administration 9, Public Health Nurse 5, Animal Service Technician 1 and more), online only. Fee NPR 500 per advertisement, NPR 250 for each extra inclusive group and NPR 200 for each extra examination type; '
              'regular deadline 2083/07/16 and double fee to 2083/07/23 (unionnepal.com, 24 October 2026).'),
     'prep_hours': 300, 'fee': 500, 'apply': [10, 11]},
]

GOVT_NOTE_ADD = {
    'g-nea': ('Open notice of 2083/07/20 (6 November 2026): 408 posts, 84 officer level and 324 assistant level across the provinces, apply at career.nea.org.np by 2083/08/10 midnight (26 November 2026), double fee to 2083/08/17. '
              'Officer posts include Engineer Electrical 42, Administrative Officer 7, Accounts Officer 6, Engineer Civil 5, Engineer Mechanical 4, Engineer Computer 4, Engineer Electronics 3, Assistant Manager Electrical 3 and Chartered Accountant 2; assistant posts are Supervisor Electrical 246, Accountant 36, Meter Reading Supervisor 31, Supervisor Mechanical 8 and Supervisor Civil 3. '
              'Base fee NPR 500 (Level 5), 1,200 (Level 7), 1,400 (Level 8) and 2,000 (Level 10). Ages 21 to 40 for Level 7 and above and 18 to 35 for assistant Level 5, 40 for women and persons with disabilities, no limit for serving NEA staff. '
              'A separate notice has 337 internal competitive promotion posts (HRIS, closing 2083/08/10) and seniority or competency promotion closing 2083/08/19; those are for serving employees only (unionnepal.com, 6 November 2026).'),
    'g-army': ('Latest notices seen: Sainya and trade follower notice published 2083/01/18 with fee payment to 2083/02/16 (30 May 2026) and late fee to 2083/02/23, ages 18 to 22 for open Sainya (born 2061/02/16 to 2065/02/16), up to 26 for serving soldiers and 18 to 26 for trade followers, minimum Class 8 pass (sarkarijagir.com and loksewatayariapp.com). '
               'The 2082/83 technical Subedar, Jamdar and Amaldar notice needed +2 for Prad Jamdar, age 18 to 25 and a last date of 2083/01/26 (collegenp.com). On 16 Kartik 2083 (2 November 2026) the army also posted contract service notices and a notice inviting applications for MBBS at the Armed Forces Medical College, Pune; read the notice for who may apply.'),
    'g-police': ('Technical Police Constable (Jawan) notice of 2083: applications 2082/12/26 to 2083/01/31 at NPR 300, Inspector through the online ORMS from 2082/12/25 to 2083/01/24, hospital constable needs SEE plus 3 months of health training; the notice also fills inclusive seats lost in 2079/80 under a Supreme Court order of 2079/10/24 (unionnepal.com).'),
    'g-provincial-psc': ('Other provinces, 2083/84 notices seen on 19 November 2026: Gandaki 169/2083-84 with 75 Level 7 seats (apply by 2083/08/01), Lumbini 84/083-084 with 25 Level 9 seats (closed 2083/07/19), Karnali 14/2083-84 with 64 Level 5 posts (closed 2083/07/16), '
                         'Madhesh 107/2083-84 for Level 9 officers (regular deadline 2083/06/14, double fee 2083/06/21; the seat count was not read) and Sudurpashchim 103/082-083 with 44 non technical Level 4 assistant posts (closed 2083/01/17 and 2083/01/24). Bagmati published its 2083/84 yearly calendar (1 Shrawan 2083 to 32 Ashad 2084). '
                         'Fees differ: Gandaki NPR 1,200 plus 400 per group, Lumbini NPR 1,200 plus 500, Karnali NPR 500 plus 250. Each has its own entry in this list.'),
    'g-so': ('Promotion notices of 2083/84 are not open vacancies: federal Notice 787 has 176 positions (173 civil service, 3 human rights service) and 788 has 6 health service posts, both closing 2083/08/29 with fee NPR 1,200; '
             'Notices 580 (62 positions) and 581 (120 positions) closed 2083/08/01 with fee NPR 2,000 (unionnepal.com, 13 November 2026).'),
}

PROVIDER_UPDATE = {
    'p-w28-pu-asian-college-of-management-and-technology-kathmandu': {'website': 'https://acmt.edu.np'},
    'p-jf-health': {'website': 'https://www.lajf.edu.np'},
    'p-w28-pu-kathmandu-academy-of-tourism-and-hospitality-kathmandu': {'website': 'https://kathtourism.edu.np'},
    'p-w28-pu-zenith-international-college-morang': {'website': 'https://zic.edu.np'},
    'p-w28-pu-himalayan-whitehouse-college-of-law-kathmandu': {'website': 'https://whitehousecollegeoflaw.edu.np'},
}
