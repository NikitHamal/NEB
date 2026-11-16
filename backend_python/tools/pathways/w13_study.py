"""Wave 13: three step by step guides, two colleges, Kathmandu University fees, Pulchowk 2083/84 notice. No dashes.

Sources: IOE entrance notices and the Pulchowk Campus admission notice of 2083/04/27 (collegenp.com), MEC MECEE-BL 2027 notice
(prepolic.com, edusanjal.com), KU School of Engineering admission notice 2026/27 and KU fee structure 2082/83 (edusanjal.com,
edulibrary.icenepal.com), MoEST NOC portal guides, Ace and Apex college pages (collegenp.com, edusanjal.com, easyshiksha.com).
"""

GUIDES_ADD = [
    {'id': 'ioe-admission', 'name': 'Get a BE or B.Arch seat through IOE', 'cat': 'Applications',
     'steps': [['Fill the IOE entrance form on entrance.ioe.edu.np and pay the form fee', 14, 2500, 'online'],
               ['Sit the computer based test (100 objective questions, 2 hours)', 14, 0, 'in person'],
               ['Fill the campus priority form after the result, up to 16 choices at Pulchowk, NPR 500 per subject', 7, 500, 'online'],
               ['Take the architecture aptitude test if B.Arch is on your list (extra NPR 500)', 1, 500, 'in person'],
               ['Check the first, second and third lists and enrol with documents inside the dates', 21, 0, 'in person']],
     'docs': ['Entrance score card', 'SEE mark sheet and character certificate', '+2 transcript with 45 percent or a C grade in every subject',
              'Citizenship certificate with two certified copies', 'Two passport photos', 'Migration and equivalence certificates for other boards'],
     'link': 'route:be-computer'},
    {'id': 'mec-entrance', 'name': 'Apply for the MEC entrance (MBBS, BDS, nursing, pharmacy)', 'cat': 'Applications',
     'steps': [['Watch for the call on entrance.mec.gov.np, usually from Shrawan', 1, 0, 'online'],
               ['Fill the online form, upload photo, signature and citizenship, pay NPR 4,000 (double after the deadline)', 1, 4000, 'online'],
               ['Download the admit card and sit the 3 hour OMR paper of 200 marks (0.25 negative)', 30, 0, 'in person'],
               ['Check your percentile (50th percentile or above is ranked) and rank', 14, 0, 'online'],
               ['Apply for open or reserved seats in the college and scholarship rounds on the MEC portal', 21, 0, 'online']],
     'docs': ['+2 science or A Level transcript with 50 percent or GPA 2.4', 'Citizenship certificate', 'Passport size photo and signature',
              'Council registration for PCL and diploma holders'],
     'link': 'route:mbbs'},
    {'id': 'ku-engineering', 'name': 'Apply to Kathmandu University School of Engineering', 'cat': 'Applications',
     'steps': [['Register on the KU admission site (the 2026/27 window ran 19 June to 9 July) and pay NPR 2,000 by eSewa or Khalti', 1, 2000, 'online'],
               ['Choose a KUCAT centre: Dhulikhel, Lalitpur, Biratnagar or Butwal', 1, 0, 'online'],
               ['Sit the computer based KUCAT; B.Arch applicants also pass an aptitude test', 1, 0, 'in person'],
               ['Wait for the rank based list and the scholarship form for geomatics where offered', 14, 0, 'online'],
               ['Get documents verified and pay NPR 2,21,000 on admission day (NPR 2,23,000 for architecture)', 1, 221000, 'in person']],
     'docs': ['+2 with Physics, Chemistry, Maths or Computer Science, 50 percent or GPA 2.0', 'SEE and +2 certificates', 'Citizenship certificate',
              'Equivalence letter from KU for a foreign board', 'Passport size photos'],
     'link': 'route:be-computer'},
]

PROVIDERS_ADD = [
    {'id': 'p-ace-mgt', 'name': 'Ace Institute of Management', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'New Baneshwor',
     'website': '', 'note': 'Affiliated to Pokhara University. Runs BBA (four years, 10+2 in any stream with 45 percent) and MBA. Seat numbers differ between sources, so confirm the intake with the college.'},
    {'id': 'p-apex-college', 'name': 'Apex College', 'kind': 'College', 'sector': 'Private', 'district': 'Kathmandu', 'place': 'Mid Baneshwor',
     'website': '', 'note': 'Affiliated to Pokhara University since 2000. Runs BBA, BBA Banking and Insurance, BBA Travel and Tourism, BCIS and MBA (day and evening).'},
]

WHERE_ADD = {'bba': ['p-ace-mgt', 'p-apex-college'], 'mba': ['p-ace-mgt', 'p-apex-college'], 'bba-bi': ['p-apex-college']}

FEES = {'p-ku-eng': {'be-electronics': [960000, 960000], 'be-chemical-hydro': [960000, 960000]}}

NOTE_ADD = {
    'p-pulchowk': 'Admission notice 2083/84: per semester NPR 6,974 for a Regular seat and NPR 52,766 for a Full Fee seat; total payable on admission day NPR 19,269 Regular and NPR 218,070 Full Fee, '
                  'with refundable deposits of NPR 3,400 and NPR 40,000 inside those totals. Foreign students pay NPR 147,167 per semester.',
}

EXAM_SUB = [['KUEE (KU)', 'KUCAT, a computer based test (KU)']]
