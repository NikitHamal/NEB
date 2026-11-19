"""Wave 27: post-study stay rules for the destinations that had none (all read on 2026-11-19; wording keeps the source named).

- Singapore: Long-Term Visit Pass for graduates of ICA's list of institutes of higher learning (ICA rule as quoted by ApplyBoard,
  "Study in Singapore", Sep 2026 and StudyU "Singapore Student's Pass 2026"); private institutions are not covered.
- Taiwan: National Immigration Agency rule as published by NTUNHS ("Employment in Taiwan"): ARC extended 6 months from the month the
  diploma is issued, one more extension, 1 year in total, no work while job seeking. The Ministry of Education Taiwan office page says
  "from 6 months to one year".
- Malaysia: Education Malaysia Global Services FAQ (educationmalaysia.gov.my): Graduate Pass, a Long-Term Visit Pass for up to 1 year for
  bachelor and higher graduates of a Malaysian HEI. A StudyU guide (Nov 2026) adds that it is open by nationality, so Nepal must be checked.
- Turkiye: Law No. 6458 Article 31(1)(i) and 31(4) (Presidency of Migration Management), as summarised by SP Law Istanbul (Nov 2026) and
  Delil Avukatlik (Nov 2026); METU International Students Office confirms the six month window. study-abroad.org says there is no
  automatic post-study visa, which refers to a work visa. One law firm reports a second year from August 2026; not read on an official page.
- Thailand: ED Plus visa (Cabinet resolution of 28 May 2024) as described by Thai Law Online (Nov 2026) and Bachelorsportal (Aug 2026).
- UAE: no stay-back on the student visa; 60, 90 or 120 day job seeker visa, Green Visa, Golden Visa for top graduates (Craydel and
  Study-abroad.org guides, 2026); the 15 hours in term and 40 in breaks is from Craydel and the existing text stays at 15 to 20.
- China: no national post-study work rule; Hainan guidance (TropicalHainan, May 2026) allows a 2 year private-affairs residence permit.
- Russia: a Saint Petersburg university's guide says full time students with an education temporary residence permit can work without
  a work permit; TopEdu Academy says there is no job search period after graduation.
"""
ABROAD_UPDATE = {
    'sg': {'stay_back': 'Up to 1 year on a Long-Term Visit Pass to look for work, for graduates of institutes of higher learning on the ICA list (the six autonomous universities, the polytechnics and listed overseas campuses). Private institutions are not covered. After that your employer applies for a work pass (ICA rule as quoted by ApplyBoard and StudyU, 2026).'},
    'tw': {'stay_back': 'Your Alien Resident Certificate is extended 6 months from the month the diploma is issued, and once more if needed, 1 year in all, to look for a job. Work is not allowed during it; a work permit for a full time job must be issued first (National Immigration Agency rule as published by NTUNHS; the Ministry of Education Taiwan office says 6 months to one year).'},
    'my': {'stay_back': 'Graduate Pass: a Long-Term Visit Pass of up to 1 year for bachelor and higher graduates of a Malaysian institution, with permission for part time work in approved sectors (Education Malaysia Global Services FAQ). It is open by nationality, so check on EMGS that Nepal is covered before you count on it.'},
    'tr': {'stay_back': 'One short-term residence permit of up to 1 year to look for work, if you apply within 6 months of graduating (Law No. 6458 Article 31(1)(i) and 31(4), Presidency of Migration Management, as summarised by SP Law Istanbul and METU). It does not authorise work: your employer must apply for a work permit. One law firm reports a second year from August 2026; not confirmed on an official page. study-abroad.org says Turkiye has no automatic post-study work visa, which is true for work, not for the stay.'},
    'th': {'stay_back': 'Only for degree students (bachelor or above at a Thai university) on the ED Plus visa: the university can file a 1 year extension after graduation to look for work or travel, and you change visa type inside Thailand if hired (Cabinet resolution of 28 May 2024, as described by Thai Law Online and Bachelorsportal). Language school and non-degree students are not covered.'},
    'ae': {'stay_back': 'No stay-back on the student visa. After graduating you move to a 60, 90 or 120 day job seeker visa, an employer sponsored visa, the 5 year Green Visa (AED 15,000 a month) or, for top graduates, a Golden Visa (Craydel and Study-abroad.org guides, 2026). The UAE does not grant permanent residence.'},
    'cn': {'stay_back': 'No national post-study stay or job search permit. Hainan guidance (as reported by TropicalHainan, May 2026) lets graduates of Chinese universities apply for a 2 year private-affairs residence permit for innovation or entrepreneurship, and a work type permit once an employer hires you. Bachelor graduates otherwise need an employer, and a work visa asks for a degree and experience.'},
    'ru': {'work': 'Rules differ by university. A Saint Petersburg university guide says full time students with a temporary residence permit linked to study can work without a work permit, but not in public service or security posts or as accountants; ask your university before taking a job.',
           'stay_back': 'No job search period found: after graduation you need a work visa or work permit arranged by an employer (TopEdu Academy guide; the Russian Ministry of Internal Affairs migration page is the place to confirm).'},
}
