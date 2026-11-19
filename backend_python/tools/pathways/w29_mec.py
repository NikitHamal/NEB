"""Wave 29: Medical Education Commission tuition ceilings (notice dated 2081/03/13, published 30 June 2024, still the current
notice on mec.gov.np/en/feeStructure as of Sept 2026), transcribed in full by smartacademyhq.com ("MEC Fees 2083 in Nepal", Sept 2026)
and matching Edusanjal's "updated list of fees, Medical Education Commission" (Aug 2026).

CEILING (NPR, tuition only, whole programme): MBBS 41,68,090 inside Kathmandu Valley and 45,95,720 outside, BDS 20,92,290,
B.Sc. Nursing 10,36,000, BNS/PBN 5,18,000, BPT, B.Sc. MIT, B.Sc. MLT, B.Pharm, BPH and B.Optom 7,77,000, BAMS 11,31,930.
Cross check: the earlier 2023 schedule (MBBS 40,23,250 valley, 44,36,025 outside) raised by 3.6 percent gives 41,68,090 and 45,95,720,
so the three Kathmandu Valley MBBS rows that still carried 40,23,250 are corrected here.
The ceiling is applied only to private colleges that already have a MEC seat count for that programme and no fee yet. It is the
upper limit for a paying seat, not the college's own price, and the note on each row says so.
"""
VALLEY = {'Kathmandu', 'Lalitpur', 'Bhaktapur'}
CEILING = {'bsc-nursing': 1036000, 'bns': 518000, 'bpharm': 777000, 'bmlt': 777000, 'bpt': 777000, 'bsc-mit': 777000, 'bph': 777000,
           'boptom': 777000, 'bds': 2092290, 'bams': 1131930}
MBBS_VALLEY, MBBS_OUTSIDE = 4168090, 4595720
OLD_VALLEY = 4023250
NOTE = ('Fee shown is the Medical Education Commission tuition ceiling for a paying seat (notice 2081/03/13, mec.gov.np, tuition only, '
        'checked 19 Nov 2026), not this college\'s own price; ask for its written fee sheet.')
NAMES = {'bsc-nursing': 'B.Sc. Nursing', 'bns': 'BNS', 'bpharm': 'B.Pharm', 'bmlt': 'B.Sc. MLT', 'bpt': 'BPT', 'bsc-mit': 'B.Sc. MIT',
         'bph': 'BPH', 'boptom': 'B.Optom', 'bds': 'BDS', 'bams': 'BAMS'}
MEC_FAQ_NOTE = 'MEC notice 2081/03/13'
