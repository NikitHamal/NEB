"""Wave 20 scholarships side: verified 2026/27 open windows, award counts and stipend rules for 16 national and international scholarships.

Sources (read 19 November 2026): SINGA Singapore (a-star.edu.sg/SINGA, opportunitiesnexus.com, worldwidestudies.info); Swedish Institute SISGP (si.se,
studyabroad.pk); VLIR-UOS ICP Connect Belgium (vliruos.be, tuniversite.com); JDS Japan Nepal (jds-scholarship.org, collegenp.com, collegesinnepal.com);
UGC Nepal (ugcnepal.edu.np, collegesinnepal.com); ICCR A2A portal (a2ascholarships.iccr.gov.in); MAECI Italy (studyinitaly.esteri.it); Oxford Clarendon Fund
(ox.ac.uk/clarendon); Rhodes Global (rhodeshouse.ox.ac.uk); ADB-JSP (adb.org); KOICA CIAT (koica.go.kr); IOE, Pokhara University and Kathmandu University
scholarship notices (edusanjal.com).
"""

SCHOLARSHIP_EXTRA = {
    's-singa': {
        'open': [6, 12],
        'covers': 'Full PhD tuition for up to 4 years, monthly stipend of SGD 2,700 rising to SGD 3,200 after passing the qualifying examination, one time airfare grant up to SGD 1,500 and settling in allowance of SGD 1,000 (bond free)',
        'how': 'Apply online at sms-applicant-app.a-star.edu.sg by 1 December 2026 (23:59 GMT+8) for the August 2027 intake across A*STAR, NUS, NTU, SUTD, SMU and SIT, or by 1 June 2027 for the January 2028 intake (A*STAR and NTU only).',
    },
    's-sisgp': {
        'open': [1, 2],
        'how': 'First apply to up to four eligible Swedish master programmes on universityadmissions.se by mid January, then submit the Swedish Institute Scholarship for Global Professionals (SISGP) application on si.se during the February portal window.',
    },
    's-vliruos': {
        'open': [10, 2],
        'awards': 150,
        'how': 'Apply directly through the participating Flemish university website (KU Leuven, Ghent University, University of Antwerp, VUB or Hasselt University) for an eligible ICP Connect master programme between October and the 1 February / 1 March scholarship deadline.',
    },
    's-jds-japan': {
        'open': [9, 11],
        'awards': 22,
        'who': 'Permanent gazetted Nepal Government civil servants (Level 7 and above under the Civil Service Act) aged 25 to 40 with at least 3 years of civil service experience (20 Master seats and 2 PhD seats per year)',
        'how': 'Submit applications through the JDS Project Office in Kathmandu (jds-scholarship.org) between September and November (10 November deadline for the 2026/27 cycle).',
    },
    's-ugc': {
        'open': [2, 3],
        'how': 'Apply online at ugcnepal.edu.np when the University Grants Commission publishes its annual Falgun/Chaitra call for Higher Education National Scholarships and MPhil/PhD Research Fellowships.',
    },
    's-ugc-qaa-need': {
        'open': [3, 5],
    },
    's-iccr': {
        'open': [2, 4],
        'how': 'Apply on the ICCR A2A portal (a2ascholarships.iccr.gov.in) between February and April for undergraduate, postgraduate and PhD seats at Indian public universities.',
    },
    's-italy': {
        'open': [4, 6],
        'covers': 'Tuition waiver at Italian public universities, health insurance and a EUR 9,000 annual grant paid in three instalments (EUR 1,000 a month for 9 months)',
        'how': 'Submit your online application on the Study in Italy portal (studyinitaly.esteri.it) when the annual MAECI call opens between April and June.',
    },
    's-rhodes': {
        'open': [6, 8],
        'awards': 2,
        'how': 'Apply for the Rhodes Global Scholarship (2 seats worldwide per year) between June and early August at rhodeshouse.ox.ac.uk after obtaining a nomination through your university.',
    },
    's-clarendon': {
        'open': [9, 1],
        'awards': 200,
        'how': 'No separate scholarship form is required: apply for any full time or part time master or DPhil course at the University of Oxford by the December or January course deadline to be automatically considered for roughly 200 annual Clarendon awards.',
    },
    's-adb-jsp': {
        'open': [7, 12],
        'awards': 135,
    },
    's-koica': {
        'open': [2, 4],
    },
    's-ioe-regular': {
        'open': [8, 9],
    },
    's-pu-scholarship': {
        'open': [6, 7],
        'how': 'Apply online at scholarship.pu.edu.np during Ashadh (June to July) and sit the 3 hour 150 mark central scholarship exam (80 percent of seats reserved for community school SEE graduates and 20 percent for private school graduates).',
    },
    's-ku-scholarship': {
        'open': [6, 8],
    },
    's-new-uz': {
        'open': [5, 7],
    },
}
