"""Wave 10 hand written parts: +2 colleges, health colleges the MEC notice left without a town, scholarship and work rule fixes, FAQs.

No em or en dashes anywhere (a test fails on them). Every figure here has a named source in ANDROID_STATUS.md session 31.
"""
S, M, H, L = 'plus2-science', 'plus2-management', 'plus2-humanities', 'plus2-law'
# key or existing id, name, district, place, sector, streams (routes), source note
PLUS2 = [
    ('united-academy', 'United Academy', 'Lalitpur', 'Kumaripati', 'Private', [S, M, H, L]),
    ('prasadi', 'Prasadi Academy', 'Lalitpur', 'Manbhawan', 'Private', [S, M]),
    ('kmc-model', 'Kathmandu Model College', 'Kathmandu', 'Bagbazar', 'Private', [S, M, H, L]),
    ('trinity', None, None, None, 'Private', [S, M, H]),
    ('xavier-intl', 'Xavier International College', 'Kathmandu', 'Kalopul', 'Private', [S, M, H]),
    ('xavier-academy', 'Xavier Academy', 'Kathmandu', 'Lazimpat', 'Private', [S, M]),
    ('kist', 'KIST College and Secondary School', 'Kathmandu', 'Kamalpokhari', 'Private', [S, M]),
    ('gcm', 'Global College of Management', 'Kathmandu', 'Mid Baneshwor', 'Private', [M]),
    ('st-lawrence', None, None, None, 'Private', [S, M]),
    ('texas', None, None, None, 'Private', [S, M, H, L]),
    ('ccrc', 'Capital College and Research Center', 'Kathmandu', 'Koteshwor', 'Private', [S, M, L]),
    ('kbc', None, None, None, 'Private', [M]),
    ('orchid', None, None, None, 'Private', [S, M]),
    ('goldengate', None, None, None, 'Private', [S, M, H]),
    ('triton', None, None, None, 'Private', [S, M, L]),
    ('uniglobe', 'Uniglobe Secondary School and College', 'Kathmandu', 'Kamaladi', 'Private', [S, M, L]),
    ('tilottama-campus', 'Tilottama Campus', 'Rupandehi', 'Yogikuti', 'Private', [M]),
    ('new-horizon-butwal', 'New Horizon College', 'Rupandehi', 'Devinagar', 'Private', [M]),
]
# key, name, district, place, MEC notice names (all rows are summed per program)
HEALTH = [
    ('p-hamro-nursing', 'Hamro School of Nursing', 'Morang', 'Biratnagar',
     'Purbanchal University. Private nursing college at Kanchanbari, recognised by the Nepal Nursing Council.', ['Hamro School of Nursing']),
    ('p-jf-health', 'JF Institute of Health Sciences', 'Lalitpur', 'Hattiban',
     'Janamaitri Foundation institute (the hospital is at Balaju). Classes run on the Little Angels College campus at Hattiban.', ['JF Institute of Health Science']),
    ('p-suvekchya', 'Suvekchya School of Health Sciences', 'Kathmandu', 'Sitapaila',
     'Runs with Suvekchya International Hospital at Sitapaila.', ['Suvekchya School of Health Sciences', 'Suvekchya International Hospital Pvt. Ltd.']),
]
PROGRAM_ROUTE = {'BSc Nursing': 'bsc-nursing', 'BNS': 'bns', 'BPharm': 'bpharm', 'BPH': 'bph', 'BSc MLT': 'bmlt', 'BPT': 'bpt',
                 'BSc MIT': 'bsc-mit', 'BOptom': 'boptom', 'BAMS': 'bams'}
SCHOLARSHIP_EXTRA = {
    's-commonwealth': {
        'who': 'Citizens of listed Commonwealth countries. Nepal is not a Commonwealth member and is not on the eligible country list for the Master and PhD rounds, so Nepali citizens cannot apply.',
        'how': 'Nothing to apply for as a Nepali citizen. Look at Chevening, a university scholarship or another route listed for the UK.',
    },
    's-holland': {
        'name': 'NL Scholarship (formerly Holland Scholarship)',
        'covers': 'EUR 5,000 one time grant paid in the first year of study. It is not a full tuition award',
        'who': 'Non-EEA students (Nepal qualifies) starting a full time bachelor or master programme at a participating Dutch university, who do not already hold a Dutch degree',
        'how': 'Apply through the university, not a central office. There is no single national deadline: each institution sets its own, usually 1 February or 1 May, and applications open about 1 November. Check that your programme is on the university list.',
        'open': [11, 5],
    },
}
SCHOLARSHIP_DROP = {'s-commonwealth': ['open']}
ABROAD_EXTRA = {
    'hu': {'work_hours': 24, 'work': 'A student residence permit lets you work up to 24 hours a week in term and full time in official breaks (up to 90 days or 66 working days a year), with no separate work permit. You need a Hungarian tax number and your employer must register the job. Pay covers daily costs, not tuition.'},
    'cn': {'work_hours': 8, 'work': 'A study residence permit is not a work permit. Off campus work study or an internship needs your university approval and the employer and period written on your residence permit before you start. In term work study is generally limited to 8 hours a week and 40 hours a month, and in vacations to 16 hours a week and 80 hours a month. Ordinary jobs, freelancing and business are not allowed on a student permit.'},
}
ROUTE_UPDATE = {
    'bim': {'name': 'BITM (formerly BIM, Bachelor of Information Technology Management)',
            'about_add': 'TU renamed BIM to BITM from the 2082/83 session. A section takes 33 students (30 regular and 3 scholarship seats). Shanker Dev Campus has 66 seats.'},
    'bsc-csit': {'about_add': 'For 2083 TU allotted 3,108 seats in 61 colleges, 80 percent open and 20 percent Samabesi (inclusive).'},
    'bca': {'about_add': 'More than 125 colleges run TU BCA and every one admits through the same FoHSS entrance exam.'},
}
