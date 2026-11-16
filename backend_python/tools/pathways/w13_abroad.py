"""Wave 13: study abroad money and visa rules (2026), scholarship windows and eligibility. Plain sentences, no dashes.

Sources: Home Affairs fee notice of 1 July 2026 (via This is Australia and RACC), GOV.UK student visa pages (via UKCISA and
lender guides), IRCC announcements (via ircc.com and umberapp.com), study.eu on the German blocked account, US Embassy fee
pages and F-1 guides (usvisa.com, edwisefoundation.com), Clickmandu on the NRB notice of June 2026, scholars4dev (Manaaki),
YTB call for Turkiye Burslari 2026, USEF-Nepal (Humphrey), edunepal (Rhodes), SAU admission pages.
"""

ABROAD_EXTRA = {
    'us': {
        'note': 'Government costs for an F-1 visa: SEVIS fee USD 350 and visa fee USD 185, plus a USD 250 visa integrity fee created by the 2025 law and '
                'collected when the visa is issued. The DS-160 asks for the social media handles you used in the last five years. The DHS rule that would '
                'replace duration of status with a fixed admission period of up to 4 years (due on 15 September 2026) was blocked by a federal court on '
                '14 September 2026 and is under appeal, so confirm the current position before you plan. OPT (1 year, 3 for STEM) still applies. '
                'Assistantships can cover tuition for master and PhD students in science and engineering.',
    },
    'uk': {
        'note': 'The Student visa fee is GBP 558 and the health surcharge GBP 776 a year. Maintenance funds are GBP 1,529 a month for London and GBP 1,171 a month '
                'outside London, for up to 9 months, and must sit in your account for 28 days; a Statement of Changes of September 2026 raises them to GBP 1,570 '
                'and GBP 1,203 from 30 November 2026. The Graduate Route falls from 2 years to 18 months for applications from 1 January 2027 (PhD graduates keep 3 years). '
                'One year master degrees save time and money.',
    },
    'de': {
        'note': 'Proof of funds in 2026 is a blocked account holding EUR 11,904 for a year, released at EUR 992 a month. Public universities charge little '
                'or no tuition, so the blocked account and health insurance are the main upfront costs.',
    },
    'jp': {
        'note': 'National universities are low cost. MEXT covers everything for winners. For a language school or diploma route the school applies for your Certificate of Eligibility '
                'and guides say immigration looks for sponsor funds of about JPY 1.5 to 2 million for the first year. Part time work needs a permission stamp and is capped at 28 hours a week in term.',
    },
    'th': {
        'work': 'A student visa holder cannot simply take a job: any work needs a Thai work permit from the Department of Employment, and the '
                'Non Immigrant ED visa is applied for at the Royal Thai Embassy in Kathmandu. Plan your budget without part time income.',
    },
}

SCHOLARSHIP_EXTRA = {
    's-manaaki': {
        'who': 'Nepal is on the Asian eligible country list for the 2026-27 round, so Nepali citizens can apply for study at a New Zealand university or '
               'institute of technology. You must be a citizen and resident of an eligible country and return home after study.',
        'how': 'Apply on the official New Zealand scholarships portal. The tertiary round for 2026-27 ran from 1 to 31 March 2026 (midday New Zealand time). '
               'The next round is expected in March 2027.',
        'open': [3, 3],
    },
    's-turkiye': {
        'who': 'Any non Turkish citizen. Age limits are under 21 for a bachelor, under 30 for a master and under 35 for a PhD. The call asks for at least '
               '70 percent in school, 75 in the bachelor for a master and 80 in the master for a PhD, and medicine or dentistry want higher marks.',
        'how': 'Apply online on the Turkiye Burslari portal. The 2026 call ran from 10 January to 20 February 2026 and the next call is expected in the same '
               'months of 2027. Results come in July or August, then a one year Turkish course and placement.',
        'open': [1, 2],
    },
    's-rhodes': {
        'how': 'Nepali students apply through the Global constituency when it is open. One Nepali listing says it was paused for the 2026 to 2027 cycle, '
               'so read the Rhodes House site before you prepare an application.',
    },
}

SCHOLARSHIPS_ADD = [
    {
        'id': 's-humphrey', 'name': 'Hubert H. Humphrey Fellowship (USA)', 'scope': 'abroad', 'levels': ['master'],
        'by': 'US Department of State via USEF-Nepal',
        'covers': 'A 10 to 12 month non degree programme at a US university with tuition, stipend, health cover and airfare',
        'who': 'Nepali citizens in a mid career policy level job in government, an NGO or the private sector, with at least 5 years of progressively '
               'responsible work in Nepal. Volunteering, internships and degree placements do not count. Not open to people who studied a year or more '
               'in a US graduate school in the last 7 years or joined a US government exchange in the last 3 years.',
        'how': 'Apply online through USEF-Nepal. The 2027-28 call opened on 5 June 2026 and closed on 31 July 2026; the 2026-27 call is closed. '
               'Interviews and nominations follow in August and September, with the final selection in April.',
        'link': 'https://usefnepal.org', 'country': 'us', 'type': 'Government', 'open': [6, 7],
    },
    {
        'id': 's-ugc-higher-ed', 'name': 'UGC Nepal Higher Education Scholarship (six target groups)', 'scope': 'nepal', 'levels': ['bachelor', 'master'],
        'by': 'University Grants Commission Nepal',
        'covers': 'NPR 24,000 a year for a bachelor student for up to four years (five for technical subjects); the master amount is set in the same directive',
        'who': 'First year bachelor or master students at a recognised institution in Nepal who belong to one of six groups: children of martyrs and conflict victims, '
               'people with disabilities, economically disadvantaged students, Dalit students, Mukta Kamlari and Muslim women. Age limits are 25 for a bachelor and 30 for a master, with some exceptions.',
        'how': 'Apply online on the UGC scholarship portal (ugc.pathway.com.np) inside the window in the yearly notice, with the certificate for your group. '
               'The 2082/83 cycle closed around April 2026 and the results for the economically disadvantaged, disabled and Dalit groups came out on 14 Asoj 2083.',
        'link': 'https://ugcnepal.edu.np', 'type': 'Government', 'open': [3, 4],
    },
    {
        'id': 's-sau', 'name': 'South Asian University scholarships (Delhi)', 'scope': 'abroad', 'levels': ['bachelor', 'master', 'phd'],
        'by': 'South Asian University, set up by the SAARC countries',
        'covers': 'Fee waiver and a living allowance in steps from 25 percent to a full scholarship that includes the hostel',
        'who': 'Students from the SAARC countries, including Nepal, with a +2 for the bachelor, a bachelor for the master and a master for the PhD. '
               'SAARC citizens pay a small part of what other students pay, in US dollars, and the top scorers in the entrance test win the President scholarship.',
        'how': 'Apply on the university site before the entrance test. The 2026 entrance test was held on 25 and 26 April after an online application that closed '
               'in the spring, with a fee of USD 20. Earlier years had centres in Biratnagar, Kathmandu and Pokhara; the latest test ran online.',
        'link': 'https://sau.int', 'country': 'in', 'type': 'University', 'open': [2, 4],
    },
]

ABROAD_SCHOLARSHIPS_ADD = {}
