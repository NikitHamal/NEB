"""Wave 39 overseas armed service pathways, read on 2026-11-19. Nothing like them existed in the dataset (zero Gurkha rows before this wave).

British Army: gurkhabde.com news (Intake 26 attestation, 6 Feb 2026: 323 recruits, more than 14,000 applicants, 39 week course at Catterick, Brigade of Gurkhas Association),
army.mod.uk news (26 Nov 2025: all 274 recruits of the previous intake passed, about 16,000 applicants, final selection in Pokhara in January), Lord Ashcroft in the Express
(reprinted on gurkhabde.com, March 2026: 571 reached the final phase, 414 left on results day, applications from 74 of 77 districts, first year pay above GBP 26,000),
gurkhaaction.com.np and gurkhavictorytrainingcentre.com.np (pre-army trainers that copy the BGN notice: age 18 to 21 on 1 December, SEE 5 C grades with C in English and
Maths, 158 cm, BMI 18 to 28 in phase 2, no glasses or laser surgery, CTEVT certificates not accepted). Registration windows seen: 1 to 30 April 2023 and 1 to 29 March 2024
on gurkha.defencegateway.mod.uk. The official BGN pages (army.mod.uk) block this server (HTTP 403), so every rule is copied from the pages above and must be re-read there.
Singapore: the same BGN selection also fills the Gurkha Contingent of the Singapore Police Force; trainers print a C in English and a D in Maths (Gurkha Victory TC) or a C in both.
Indian Army: Times of India 18 Aug 2026, ThePrint 17 Aug 2026, News18 19 Aug 2026 (no Nepal domiciled Gorkha recruited since Nepal paused it in 2022; Agnipath is 4 years with up to
25 percent kept), Al Jazeera 30 Dec 2024 (1,300 to 1,500 recruits a year before the pause).
"""
GOVT_ADD = [
    {'id': 'g-british-gurkha', 'track': 'sec', 'name': 'British Army Gurkha (Brigade of Gurkhas)', 'level': 'Trainee rifleman, selected in Nepal and trained in the UK',
     'need': 'SEE with a C in English and a C in Maths (5 C grades in all for SEE from 2016); CTEVT certificates are not accepted. Nepali man with a Nepalese birth certificate',
     'age': '18 to 21 years on 1 December before the intake (the 2026 intake took people born between 1 Dec 2004 and 1 Dec 2007)', 'body': 'British Gurkhas Nepal (British Army), Pokhara and Dharan camps',
     'seats': 323,
     'stages': [['Online registration', 'Free online form on gurkha.defencegateway.mod.uk for district, citizenship number and passport name. Past windows were 1 to 30 April 2023 and 1 to 29 March 2024. A late or wrong form is not called forward.', ''],
                ['Phase 1 registration', 'Documents, a chin up test and a leg test at Pokhara, Dharan or the Surkhet welfare centre, by district date from the call forward list on the BGN site.', ''],
                ['Phase 2 initial selection', 'Written English and Maths of about Entry Level 2 standard, medical check, 800 metre run, overarm heaves, lift and carry. BMI must be 18 to 28.', ''],
                ['Phase 3 final selection', 'Four days at British Gurkhas Pokhara in January: medical, English test, the doko race (a basket carry run) and a 20 minute interview. Places go by points. In 2026 only 414 of 571 were left on results day and 323 were taken.', ''],
                ['Training in the UK', 'Attestation parade in Pokhara in early February, then 39 weeks of infantry training at Catterick before joining one of the cap badges, including the new King\'s Gurkha Artillery.', '']],
     'subjects': ['English and basic Maths at SEE level', 'Fitness: running, heaves, carrying a loaded doko', 'Interview: why you want to serve, teamwork and honesty'],
     'prep': ['Start fitness a year ahead; run 800 metres and 2 km for time and practise overarm heaves', 'Revise SEE English and Maths until a C is safe',
              'Never pay an agent for a seat: selection is free and the only entry is the online form', 'Read the BGN notice every year; windows and numbers change'],
     'note': 'Intake 26 (selected January 2026): more than 14,000 applicants for 323 places (the Express reports more than 10,000 first applications, the Brigade page more than 14,000; both are stated). First year pay is reported as above GBP 26,000 a year. About 16,000 applied for the intake before it, and all 274 of its recruits passed out of Catterick in November 2025 (army.mod.uk). The 2027 registration window was not found on 19 November 2026; past windows ran in March and April. Pre army coaching classes are optional, and none is connected with BGN.',
     'career': 'security-officer', 'fee': 0, 'apply': [3, 4], 'exam_month': 1},
    {'id': 'g-singapore-gurkha', 'track': 'sec', 'name': 'Singapore Police Force Gurkha Contingent', 'level': 'Trainee policeman in the Gurkha Contingent, selected by the same British Gurkhas Nepal process',
     'need': 'SEE with a C in English; Maths grade shown as D by one trainer and C by another, so read the BGN notice. 5 C grades for SEE from 2016. Nepali man',
     'age': '18 to 21 years on 1 December before the intake (some pages show 17 years 6 months as the lower limit)', 'body': 'British Gurkhas Nepal for the Singapore Police Force',
     'stages': [['Online registration', 'Same free form as the British Army; you tick Singapore Police or British Army and the choice must match the paper form.', ''],
                ['Phase 1 and 2', 'Registration day, then initial selection at Pokhara with the written English and Maths test, medical and fitness tests.', ''],
                ['Phase 3 final selection', 'A separate final selection window in late November and early December (28 November to 10 December 2025 for the 2026 intake), then a Singapore police training course.', '']],
     'subjects': ['English and Maths', 'Fitness and interview'],
     'prep': ['Prepare exactly as for the British Army', 'Take the form for one force only, because the paper form must match the online choice', 'Pay nothing to anyone for selection'],
     'note': 'A pre army academy page lists 204 British Army and 144 Singapore Police places for one cycle and does not give the year, so it is not used as a seat count. The Gurkha Contingent hires on contracts, and contract length and pay are not printed on any page checked, so ask at the selection camp.',
     'career': 'security-officer', 'fee': 0, 'apply': [3, 4], 'exam_month': 11},
    {'id': 'g-indian-gorkha', 'track': 'sec', 'name': 'Indian Army Gorkha Rifles (paused for Nepali youth)', 'level': 'Agniveer soldier, 4 year tenure. Recruitment of Nepal domiciled Gorkhas is on hold',
     'need': 'SEE pass with a minimum of D plus on older rallies; Nepali citizen. Not open: no rally has run since Nepal paused it in August 2022', 'age': '17.5 to 21 years under Agnipath',
     'body': 'Indian Army through the Gorkha Recruiting Depot, Kunraghat. Nepal government must agree under the 1947 tripartite agreement',
     'stages': [['Status in November 2026', 'No Nepal domiciled Gorkha has been recruited since 2022. India says Agnipath is its only route and that the call is Nepal\'s. Veterans asked Prime Minister Balen Shah to restart it in August 2026 and the Indian Army chief visited Pokhara, but no restart was reported.', ''],
                ['Agnipath terms in force', 'Four years of service, then up to 25 percent of a batch kept in the regular army and the rest leave with the Seva Nidhi payment and no pension.', '']],
     'subjects': ['Nothing to prepare for until a rally is announced'],
     'prep': ['Treat every offer of an Indian Army seat as a scam until the Nepal government and the Indian Embassy announce a rally', 'Do not pay agents, trainers or brokers for a promised seat',
              'Meanwhile use the same fitness for the British Army, Nepal Army, Nepal Police or Armed Police routes'],
     'note': 'Before the pause the Indian Army took about 1,300 to 1,500 Nepali Gorkha recruits a year (Al Jazeera, December 2024). Nepal blocked the first Agnipath round in July 2022 and later rounds. Check Nepal Ministry of Defence and the Indian Embassy in Kathmandu for any change.',
     'career': 'security-officer', 'fee': 0},
]
GUIDES_ADD = [
    {'id': 'dofe-labour-permit', 'name': 'Labour permit (Shram Swikriti) for work abroad', 'cat': 'Documents',
     'steps': [['Check that the agency is licensed and the demand letter is real on dofe.gov.np before you pay anyone', 1, 0, 'online'],
               ['Create your FEIMS account at feims.dofe.gov.np with your passport number and mobile number', 1, 0, 'online'],
               ['First time workers sit the 2 day pre departure orientation at an approved centre (one page prints NPR 700, another NPR 500 to 1,000)', 2, 700, 'in person'],
               ['Take the medical at a government approved centre (pages print NPR 1,500 to 3,000 and NPR 5,000 to 8,000 by country)', 1, 3000, 'in person'],
               ['Buy the term life insurance for the contract period (about NPR 1,886 and up, the amount shown in FEIMS)', 1, 1886, 'online'],
               ['Pay the Welfare Fund contribution (NPR 1,500 on most pages) and the Social Security Fund share (NPR 2,595 on one page, 2,500 to 3,000 on another)', 1, 4095, 'online'],
               ['Upload the contract, passport and photos and wait for the approval; check the result by passport number on foreignjob.dofe.gov.np', 5, 0, 'online']],
     'docs': ['Passport', 'Citizenship certificate', 'Signed employment contract', 'Employer demand letter', 'Passport size photos', 'Orientation certificate', 'Medical report', 'Insurance receipt'],
     'link': 'route:foreign-lang-work'},
]
ROUTE_NOTE_ADD = {
    'police-army': 'Gurkha routes (checked 19 November 2026): the British Army and the Singapore Police take Nepali men aged 18 to 21 with a C in SEE English and Maths through one free selection at Pokhara and Dharan (323 places for more than 14,000 applicants in 2026). Indian Army Gorkha recruitment from Nepal has been paused since 2022, so any seat offered by an agent is a scam.',
    'foreign-lang-work': 'Every Nepali worker going abroad except to India needs a labour permit (Shram Swikriti) from the Department of Foreign Employment, applied for online in FEIMS. See the guide for the steps and the fees.',
}
