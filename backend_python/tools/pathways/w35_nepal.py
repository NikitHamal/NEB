"""Wave 35 Nepal and India side. Read on 2026-11-19.
MGSS and GJSS 2026-27: the official Embassy of India portal goischolarship.com.np carried the banner "The last date for online application has been extended till 29 November 2026 (23.59 hrs)"
when read on 2026-11-19 (it replaces the 15 November date of the first Embassy notice quoted by educatenepal.com, Edusanjal and the earlier wave); smartacademyhq.com (16 November 2026) printed the same 29 November date.
The amounts come from the Embassy notice text on Edusanjal: MGSS NPR 24,000 a year for 2 years for Class 11 students with 60 percent in Class 10 (SEE) and family income below NPR 2,00,000;
GJSS NPR 48,000 a year for MBBS, BDS, BE, BTech, BArch and BAMS (5 years for MBBS and BDS, 4 for the others) and NPR 36,000 a year for 3 years for other courses, age 17 to 22 on 1 July 2027.
India study route: NEET UG, JEE Main, DASA and CUET figures are in w35_exams.py. Kathmandu centre codes: NEET 9907, JEE Main and CUET ZZ05.
"""
SCHOLARSHIP_EXTRA = {
    's-mgss': {
        'covers': ('NPR 24,000 per year (NPR 2,000 a month) for two years across Class 11 and 12, so NPR 48,000 at most, paid into a bank account the Embassy opens in your name. '
                   'Applicants who get another scholarship are not eligible.'),
        'how': ('The 2026-27 window on goischolarship.com.np opened on 23 October 2026. The first Embassy notice closed it on 15 November 2026 (portal shut at 00.00 on 16 November), '
                'but the portal now says the last date was extended to 29 November 2026 at 23.59 hrs (checked on 19 November 2026), so you still have days left. '
                'You need a regular Class 11 place (not a diploma), at least 60 percent in SEE, and family income below NPR 200,000 a year; upload the SEE mark sheet and an income proof. '
                'Apply directly; the Embassy does not take applications through consultants or agents. Awardees send the Class 11 mark sheet and a promotion certificate by 31 December to continue in Class 12.'),
        'open': [10, 11],
    },
    's-gjss': {
        'covers': ('NPR 48,000 a year for MBBS and BDS (5 years) and for BE, BTech, BArch and BAMS (4 years), and NPR 36,000 a year for 3 years for other bachelor courses, '
                   'paid into a bank account the Embassy opens in your name. Continuation each year needs the mark sheet and a promotion certificate.'),
        'how': ('The 2026-27 window on goischolarship.com.np opened on 23 October 2026. The first Embassy notice closed it on 15 November 2026, but the portal banner now reads that the last date was extended to '
                '29 November 2026 at 23.59 hrs (checked on 19 November 2026). You must be a regular first year bachelor student (not diploma) in a recognised Nepali institution, aged 17 to 22 on 1 July 2027, '
                'with a Class 12 mark sheet, family income below NPR 200,000 a year, and no other scholarship. Send the mark sheet and promotion certificate by 31 December each year to continue. '
                'Apply directly, not through agents.'),
        'open': [10, 11],
    },
}

ABROAD_UPDATE = {
    'in': {
        'exams': ['NEET UG for MBBS, BDS, BAMS and nursing (held at Kathmandu, fee Rs 9,500)',
                  'JEE Main for BTech and BArch at NITs and IIITs through DASA (Kathmandu centre, fee Rs 5,000 a paper, Session 1 on 22 to 30 January 2027)',
                  'CUET UG for central and state university BA, BSc and BCom seats (Kathmandu centre, fee Rs 4,500 for 3 subjects)',
                  'Private universities and deemed universities set their own tests or accept these scores'],
    },
}

ABROAD_NOTE_ADD = {
    'in': ('Entrance routes for a Nepali student (2026 cycle, see the exam entries for details): NEET UG for medicine, JEE Main then DASA for NIT and IIIT engineering (SAARC applicants pay USD 300 plus half the tuition, '
           'USD 2,300 first semester enrolment fee), CUET UG for central university arts, science and commerce. All three run a Kathmandu centre, so you sit the test at home; the foreign centre fee is much higher than the Indian fee '
           '(Rs 9,500 against Rs 1,700 for NEET). Medical and dental students also need the Nepal NOC and must pass the Nepal Medical Council licensing exam to practise in Nepal.'),
}

GUIDES_ADD = [
    {'id': 'india-entrance-nepali', 'name': 'Study in India as a Nepali student: NEET, JEE Main or CUET', 'cat': 'Applications',
     'steps': [['Pick the course and the matching test: NEET UG for medicine, JEE Main for engineering and architecture, CUET UG for BA, BSc and BCom at central universities', 1, 0, 'online'],
               ['Read the new NTA bulletin on neet.nta.nic.in, jeemain.nta.nic.in or cuet.nta.nic.in and register in the window, choosing Kathmandu as the exam city (JEE Main Session 1 closes on 22 November 2026)', 14, 8000, 'online'],
               ['Sit the test at the Kathmandu centre with your admit card and a valid ID', 1, 0, 'in person'],
               ['Apply for a seat: DASA on the DASA and CSAB portal for NIT and IIIT engineering, the Medical Counselling Committee or a private college for medicine, or the university itself for CUET courses', 30, 20000, 'online'],
               ['For medical study, get the NOC from the Ministry of Education before you pay the seat fee (noc.moest.gov.np)', 5, 2000, 'online'],
               ['Travel with your citizenship or passport; no student visa is needed under the 1950 Treaty', 1, 0, 'in person']],
     'docs': ['NEB +2 mark sheet and certificate', 'SEE certificate', 'Citizenship certificate or passport', 'Admit card and score card', 'NOC (medical and dental)', 'Passport photos'],
     'link': 'exam:e-neet-ug-india'},
]
