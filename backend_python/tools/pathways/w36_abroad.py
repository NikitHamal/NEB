"""Wave 36 abroad rules, read on 2026-11-19.
UK: Budget of 28 October 2026 as reported by studytravel.network (29 Oct 2026), shiksha.com, visavisuk.com, houseofadmissions.com, amberstudent.com (levy GBP 925 from 1 August 2028, 220 student allowance).
US: lawfirm4immigrants.com (11 Nov 2026), colorado.edu/isss (7 Oct 2026), ahluwalialaw.com (6 Nov 2026) on the H-1B payment and OPT proposals.
Germany Opportunity Card: germany-visa.org, forsawork.com, sprachschule.org, getwherenext.com, workbeyond.com (2026). Points for partial recognition are 4 on four pages and 2 on one page; 4 is used.
NRB foreign exchange: kharchapatra.com (9 June 2026, quoting the October 2024 circular reported by New Business Age), merokalam.com (13 Aug 2026); older pages quote USD 12,000 a year.
Hungary: stipendiumhungaricum.hu home page, read 2026-11-19.
"""
ABROAD_UPDATE = {
    'uk': {'stay_back': '2 years Graduate Route for applications up to 31 December 2026; 18 months from 1 January 2027, with a two year grant announced in the 28 October 2026 Budget for graduates of high compliance universities (list, tests and start date not yet published); PhD graduates 3 years'},
}

ABROAD_NOTE_ADD = {
    'uk': ('Budget of 28 October 2026: the government said the Graduate visa will be set at two years for graduates of "high compliance universities where there are strong labour market outcomes". It is a policy statement, not yet in the Immigration Rules: no university list, test or start date has been published, '
           'so the 18 month rule still applies to applications from 1 January 2027 until a Statement of Changes says otherwise. Plan with 18 months and treat two years as a possible bonus. The High Potential Individual route is to widen to graduates of the top 150 universities in the world. '
           'The international student levy of GBP 925 per student a year is confirmed for English providers from 1 August 2028 (first 220 students a year exempt); the university pays it, not the student, but fee rises are likely, and it does not apply in Scotland, Wales or Northern Ireland.'),
    'us': ('Status on 11 November 2026: the USD 100,000 H-1B payment (Proclamation 10973, extended to 21 September 2027) is blocked by court orders in Massachusetts (8 June 2026, appeal pending in the First Circuit) and California (30 September 2026) and is not collected; DHS has separately proposed a USD 103,265 fee for cap subject H-1B petitions (comment period closed 24 September 2026). '
           'DHS has also proposed OPT fees paid by the school (reported as USD 70,000 for first OPT and USD 30,000 for later or STEM OPT; an earlier report said USD 100,000); none of these is in force. OPT today costs the I-765 filing fee, about USD 470. Rules can change within weeks, so check uscis.gov and your school international office before you pay a deposit.'),
    'de': ('Opportunity Card (Chancenkarte, section 20a): up to 12 months in Germany to look for skilled work without a job offer, for a recognised degree or at least 2 years of vocational training plus 6 points or full recognition. '
           'Points: partial recognition 4, shortage occupation 1, 2 to 4 years of experience in the last 5 years 2 and 5 years 3, German A2 1, B1 2, B2 3, English C1 1, age up to 35 2 and 36 to 40 1, 6 months legal stay in Germany in the last 5 years 1, partner 1 (one page lists 2 points for partial recognition, four list 4). '
           'Entry minimum A1 German or B2 English; funds EUR 1,091 a month (EUR 13,092 for 12 months, higher than the EUR 992 a month for a student visa), shown by a blocked account, a declaration of commitment or a part time contract; application fee EUR 75; work up to 20 hours a week plus trial jobs of up to 2 weeks.'),
}

SCHOLARSHIP_NOTE_ADD = {
    's-sh': 'Status on 19 November 2026: the official stipendiumhungaricum.hu home page still said "Application is closed for the 2026/27 academic year" and its newest news item was dated 11 November 2026, so the 2027/28 call was not live yet; secondary sites expect it around 17 November with a 15 January 2027 deadline at 14:00 Central European Time, which is unconfirmed.',
}

GUIDES_ADD = [
    {'id': 'nrb-forex-study', 'name': 'Send tuition and living money abroad legally (NRB foreign exchange)', 'cat': 'Documents',
     'steps': [
         ['Get the Ministry of Education no objection certificate (NOC) and keep the admission letter, invoice or I-20 and visa', 7, 0, 'online'],
         ['Open or use a bank that offers the study foreign exchange facility and give it the NOC, admission letter, passport, citizenship and visa copy', 2, 0, 'in person'],
         ['Ask the bank for the tuition limit (reported USD 25,000 a year after the October 2024 NRB circular; older pages say USD 12,000) and the living expense limit for your country', 1, 0, 'in person'],
         ['Pay the 3 percent education service fee on the foreign currency released and send the money by SWIFT telegraphic transfer to the university account', 3, 0, 'in person']],
     'docs': ['NOC', 'Admission or offer letter and fee invoice', 'Visa copy and passport', 'Citizenship certificate and bank account details'],
     'link': 'guide:noc-study-abroad'},
]
