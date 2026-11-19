"""Wave 40 Nepal data, read on 2026-11-19.
Koshi notice 106/2083-84: unionnepal.com (29 Oct 2026, full ad table, fees, exam schedule) and merohealthline.com (12 Oct 2026, same dates and fee).
The commission site psc.koshi.gov.np answers HTTP 200 but its notice list is script built, so no figure here was read from it directly.
Driving licence: dotm.gov.np home page notice on EDLVRS going online (read 19 Nov 2026), province portal edlvrs.bagamati.gov.np (answers), careerkyt.com 14 Oct 2026
(DoTM question book ages and fees), wilson.com.np 24 Sep 2026 (FY 2083/84 provincial fees), drivequiznp.com (directive 2083 summary).
"""
PSC_COMMON_PREP = [
    'Get the syllabus from the commission of your province, not from a federal PSC page',
    'Open, inclusive and inter level groups are separate advertisements, and each extra group costs extra, so list your groups before you pay',
    'Qualification, age and council registration must be complete on the regular deadline; the double fee date does not extend them',
]

GOVT_ADD = [
    {'id': 'g-koshi-psc-l7', 'track': 'psc',
     'name': 'Koshi Province Level 7 and 8 officer posts (Notice 106/2083-84): 69 seats',
     'level': 'Seventh level officer and eighth level Medical Officer posts of the Koshi local service (engineering, agriculture, veterinary, livestock, fisheries, education, health and administration), run by the Koshi Province Public Service Commission in Biratnagar',
     'need': 'Bachelor level degree in the subject each post names (Civil Engineering, BSc Agriculture, BVSc and AH, Public Health, Medical Laboratory Technology, Law, Management or Commerce for Accounts, any bachelor degree for Section Officer); MBBS for Medical Officer. Health posts need valid council registration. Everything must be complete by the regular deadline',
     'age': '21 to 35 years, up to 40 for women and persons with disabilities, 21 to 45 for health service posts; permanent employees of the listed services are exempt from the upper limit',
     'body': 'Province Public Service Commission, Koshi Province, Biratnagar (psc.koshi.gov.np, applications at psconline.p1.gov.np)',
     'seats': 69,
     'stages': [
         ['Written examination', 'Post wise papers, centre announced later. Medical Officer 2083/09/04 and 05; Civil Engineer 09 and 10 (Building and Architecture group 04 and 05); Veterinary 11 and 12; Agriculture Extension, Horticulture and Crop 18 and 19; Livestock 25 and 26; Fisheries 27; Education 2083/10/01 to 03; Medical Lab 10/09 and 10; Public Health 10/16 and 17; Law 10/09 and 10; Section and Accounts Officer first paper 09/15 and later papers 10/23 to 25. Every date is Bikram Sambat.', ''],
         ['Computer skill test, group assessment and interview', 'Where the post syllabus says so, after the written result. A candidate who qualifies in more than one inclusive group attends these stages once.', '']],
     'subjects': ['General knowledge, province and local government law', 'Post specific technical or administrative paper', 'Computer skill test where the syllabus says so'],
     'prep': PSC_COMMON_PREP,
     'note': ('Notice 106/2083-84 (open and inclusive, published 2083/06/26) lists 69 seats: 49 technical (6 Medical Officer at level 8, Engineer 13, Agriculture, Horticulture and Crop officers 11, Veterinary 6, Education 6, Public Health 3, Livestock 2, Fisheries 1, Medical Lab 1) '
              'and 20 non technical (Section and Accounts Officer 18, Law Officer 2), counted from the advertisement table. Fee NPR 1,200 for level 7 or 8 plus NPR 400 for each extra group; regular deadline 2083/07/15 (about 1 November 2026) and double fee to 2083/07/22, fee payment by 2083/07/23, so the call is now closed. '
              'The same day the commission advertised 29 promotion posts (Notice 104 level 9 with 1 post and Notice 105 level 7 with 28 posts) for serving staff only, fee NPR 1,200 or 2,000, on paper at the Biratnagar office until 2083/07/24. '
              'The notice prints no salary. Read the post wise syllabus on psc.koshi.gov.np; the next Koshi call follows the annual 2083/84 calendar (1 Shrawan 2083 to 32 Ashad 2084).'),
     'prep_hours': 400, 'fee': 1200, 'apply': [10, 11], 'exam_month': 12},
]

GUIDES_ADD = [
    {'id': 'driving-licence-nepal', 'name': 'Driving licence (new, online system)', 'cat': 'Documents',
     'steps': [['Check the minimum age for your category: 16 years for motorcycle and scooter (A, K), 18 for car, jeep and van (B), 21 for heavy vehicles', 1, 0, 'online'],
               ['Open the portal of your province (Bagmati: edlvrs.bagamati.gov.np) and sign in; scanning the QR code on your National ID or the Nagarik App fills the form. Since 1 Shrawan 2083 the old national form has moved to the seven province portals', 1, 0, 'online'],
               ['Get the health check from an approved doctor (one guide prints NPR 200 to 300)', 1, 300, 'in person'],
               ['Pick the category and the transport office where you will sit the tests, then pay the application fee online (NPR 500 on the DoTM question books, up to 1,000 on another guide)', 1, 500, 'online'],
               ['Book and sit the 25 question written test on a computer at the transport office; pass marks are printed differently on different guides, so read the portal', 7, 0, 'in person'],
               ['Sit the practical trial on the trial track on your booked date; a retest costs about NPR 400 to 500', 10, 0, 'in person'],
               ['Pay the licence fee online after you pass: NPR 1,500 (motorcycle) and 2,000 (car) in the old DoTM books, NPR 3,000 (A, K) and 4,000 (B, 5,000 in Madhesh) in the 2083/84 province fee tables, so the portal shows the amount that applies to you', 1, 3000, 'online'],
               ['Collect the smart card from the office; the card normally takes a few working days to print', 10, 0, 'in person']],
     'docs': ['National ID or citizenship certificate', 'Nagarik App or National ID QR code', 'Health check certificate', 'Passport size photo', 'Online payment receipt'],
     'link': 'route:skill-training'},
]

ROUTE_NOTE_ADD = {
    'skill-training': 'Driving is a skill you can add at 16 (motorcycle) or 18 (car). Licences are applied for on the province portals since 1 Shrawan 2083; read the driving licence guide for the steps, ages and fees, and note that guides disagree on fees (NPR 1,500 to 4,000 for a first licence), so trust the amount your portal shows.',
}
