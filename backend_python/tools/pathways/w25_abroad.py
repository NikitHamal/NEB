"""Wave 25: student work and post-study stay rules for Spain, Portugal, Estonia, Hungary, Romania, Cyprus and Norway.

Sources, each page opened in this session:
- European Commission EU Immigration Portal student pages (home-affairs.ec.europa.eu/.../eu-immigration-portal/student-<country>_en)
  for Spain, Portugal, Estonia, Hungary, Romania and Cyprus.
- UDI (udi.no/en/want-to-apply/studies/studietillatelse/) for Norway.
- Study in Hungary FAQ (studyinhungary.hu, "Ask us" page) for the 24 hour figure.
Where two official pages disagree the note says so and keeps the lower figure as the headline number.
"""
EC = 'European Commission EU Immigration Portal'

ABROAD_UPDATE = {
    'es': {
        'stay_back': f'12 month job searching residence permit after you complete your studies ({EC}, Spain page); working after that needs a job offer and a work permit, or a highly qualified or start-up route',
    },
    'pt': {
        'work': f'The {EC} Portugal page says only secondary education students, unremunerated trainees and volunteers are not allowed to work on a student residence permit, so a higher education student may take a job. It gives no weekly hour cap, so confirm hours and registration with AIMA and your university.',
        'stay_back': f'You can work as an employee or self employed after your studies once you apply for and obtain the temporary residence permit for that purpose ({EC}, Portugal page); the page gives no job search period',
    },
    'ee': {
        'work': f'Students at Estonian higher education institutions may take a job without prior authorisation and without a limit on working hours, as long as the work does not interfere with studies ({EC}, Estonia page). Part time work is practical mostly in IT and hospitality.',
    },
    'hu': {
        'work': f'Two official pages differ. The {EC} Hungary page says up to 30 hours a week during the study period and full time for up to 90 days a year outside it; the Study in Hungary FAQ says 24 hours a week in term and up to 90 days or 66 working days outside term. Plan with 24 hours and ask your university career office. You need a Hungarian tax number and the employer must register the job.',
        'stay_back': f'After successfully completing studies you can apply for a residence permit to look for a job or start a business ({EC}, Hungary page); the page gives no duration',
    },
    'ro': {
        'stay_back': f'Residence for studies can be extended by 9 months after graduation to look for a job or open a business, and by up to 6 months to finalise the studies and authenticate documents ({EC}, Romania page)',
    },
    'cy': {
        'stay_back': f'One year after completing a master or PhD course to look for a job or start a business, by permit; bachelor graduates are not covered ({EC}, Cyprus page)',
    },
    'no': {
        'work': 'A study permit includes permission to work part time up to 20 hours a week, including remote work, and full time during holidays, with no separate work permit (UDI study permit page). You cannot start working before the permit is granted, and you cannot be self employed. PhD posts are salaried jobs with no tuition.',
    },
}
