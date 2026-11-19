"""Wave 29: Sweden's June 2026 student work cap and the first post-study notes for the six destinations that had none
(all read on 2026-11-19; each text names its source and where sources disagree it says so).

- Sweden: KPMG Global Mobility flash alert 2026-162 and thescholarsdream.com (Migrationsverket notice of May 2026): from 11 June 2026
  higher education students on new permits may work at most 15 hours a week in term, unlimited in June, July and August; permits
  granted before that date keep the old rules until their next extension. Job search permit 12 months, 12 to 18 after doctoral studies.
- Uzbekistan: StandYou, GoHijrat and Visit World (2026): a student visa carries no work right, any paid work needs a work permit,
  no automatic post-study permit, an employer sponsored work permit is the route.
- Georgia: StandYou and Leverage Edu say no formal post-study visa, a work residence permit needs an employer offer; LeapScholar says
  a 1 year temporary residence permit to seek work. Marked as disagreeing.
- Kyrgyzstan: studycountry.com (Oct 2026, citing KSMA and the e-visa portal): student visa holders may not work, no post-study work visa,
  work needs a Unified Permit (work visa plus work permit). StandYou agrees on the permit.
- Kazakhstan: StandYou (2026) says no formal post-study work visa, a job offer and employer sponsored work permit are needed; egov.kz
  describes the work permit route. Agency pages disagree on student work hours, so the existing work text stays.
- Philippines: studiesmultiverse.com (checked 4 Oct 2026, citing the Bureau of Immigration and DOLE) and studycountry.com (18 Oct 2026):
  no post-study work visa, an employer must sponsor an Alien Employment Permit and a work visa.
"""
ABROAD_UPDATE = {
    'se': {
        'work_hours': 15,
        'work': 'Since 11 June 2026 a higher education student on a new or extended permit may work at most 15 hours a week during term, with no cap in June, July and August (Migrationsverket rule as reported by KPMG and The Scholars Dream). Permits granted before that date keep the old rules until the next extension. Exceeding the cap can lead to the permit being revoked or not extended, and an extension also asks for at least 37.5 credits in the first year and 45 a year after.',
        'stay_back': 'Up to 12 months on a residence permit to look for work or start a business after a completed bachelor or master programme (12 to 18 months after doctoral studies); it cannot be extended. You need at least two semesters of study in Sweden and SEK 10,656 a month in funds for the whole period for 2026 applications (Migrationsverket rule as quoted by EnglishJobsSweden, September 2026).',
    },
    'uz': {
        'work': 'The student visa carries no work right: three 2026 guides (StandYou, GoHijrat, Visit World) say any paid work needs a work permit, and some universities allow on campus jobs or internships. Do not budget for wages; confirm with your university and the migration office.',
        'stay_back': 'No automatic post-study job search permit found (StandYou, 2026). To stay after graduating an employer has to sponsor a work permit and you change from the student visa; the guides do not name an official page, so confirm with the migration service.',
    },
    'ge': {
        'stay_back': 'Sources disagree. StandYou and Leverage Edu say Georgia has no formal post-study work visa and a work residence permit needs an employer offer; LeapScholar describes a 1 year temporary residence permit to seek employment. No official page was read, so ask the Public Service Hall before you count on a job search period.',
    },
    'kg': {
        'work': 'Student visa holders may not work, full time or part time, according to KSMA as quoted by studycountry.com (October 2026); StandYou also says a separate work permit is needed and part time jobs are mostly informal. Older agency pages claiming part time work is allowed are not backed by an official page. Plan to pay for your studies without wages.',
        'stay_back': 'No post-study work visa: official sources checked by studycountry.com (October 2026) name none. A graduate who wants to work needs an employer to arrange a work visa and work permit, issued together as a Unified Permit on the e-visa portal.',
    },
    'kz': {
        'stay_back': 'No formal post-study work visa found (StandYou, 2026). To stay and work after graduating you need a job offer and an employer sponsored work permit, applied for through the Citizen Service Centre (egov.kz describes the work permit steps). Confirm the current rule with the Migration Service.',
    },
    'ph': {
        'stay_back': 'No post-study work visa or job seeking stay: the 9(f) student visa is tied to enrolment and the Bureau of Immigration visa list has none (studiesmultiverse.com, checked 4 Oct 2026; studycountry.com, 18 Oct 2026). To remain and work an employer must sponsor an Alien Employment Permit and the matching work visa (for example the 9(g) pre-arranged employment visa).',
    },
}
