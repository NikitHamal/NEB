"""Wave 21 route exam links, career licence links and six step by step guides.

Sources (read 19 November 2026): ADBL/NBL/RBB Lok Sewa application portals (career.adbl.gov.np, nepalbank.com.np); PSC Judicial Service
online portal (psconline1.psc.gov.np); ACCA Global registration and Nepal CBE centers (accaglobal.com); NHPC online licensing portal
(nhpc.gov.np); Nepal Pharmacy Council licensing portal (nepalpharmacycouncil.org.np); Nepal Veterinary Council NLEV notice (vcn.gov.np).
"""

ROUTE_EXAM = {
    'btech-food': 'e-tu-bachelor-sci',
    'bsc-science': 'e-tu-bachelor-sci',
    'bsc-environment': 'e-tu-bachelor-sci',
    'bsc-microbiology': 'e-tu-bachelor-sci',
    'bsc-geology': 'e-tu-bachelor-sci',
    'be-biomedical': 'e-purbanchal',
    'bfd-design': 'e-purbanchal',
    'mca': 'e-purbanchal',
    'acca-route': 'e-acca',
    'bsw': 'e-fohss-bachelor',
    'bjmc': 'e-fohss-bachelor',
    'bfa': 'e-fohss-bachelor',
    'ba-psychology': 'e-fohss-bachelor',
    'ba-economics': 'e-fohss-bachelor',
    'mbs': 'e-fohss-master',
    'ma': 'e-fohss-master',
    'msw': 'e-fohss-master',
    'mpa': 'e-fohss-master',
    'med': 'e-fohss-master',
    'llm': 'e-fohss-master',
    'mphil': 'e-fohss-master',
    'phd-route': 'e-fohss-master',
    'msc-agri': 'e-afu',
    'bicte': 'e-bit',
}

CAREER_LICENCE = {
    'actuary-risk-analyst': {'name': 'IFoA / SOA Actuarial or ACCA Financial Certification', 'exam': 'e-acca'},
}

GUIDES_ADD = [
    {'id': 'adbl-nbl-bank-apply', 'name': 'Apply for ADBL, Nepal Bank and RBB Government Bank Exams', 'cat': 'Applications',
     'steps': [
         ['Check your level eligibility: +2 qualifies for RBB Level 4 and ADBL Level 4 Lekhapal, while Nepal Bank Level 4 Assistant requires a Bachelor degree and Level 6 Officer requires a Master degree or CA', 1, 0, 'online'],
         ['Create your candidate profile on career.adbl.gov.np, nepalbank.com.np or career.rbb.com.np when the annual vacancy notice is published', 1, 0, 'online'],
         ['Upload your citizenship, transcripts, character certificates, equivalence (if foreign board) and inclusive group documents and pay the NPR 800 (Level 4) or NPR 1,000 (Level 6) exam fee via ConnectIPS, eSewa or Khalti', 1, 800, 'online'],
         ['Download your admit card once Lok Sewa Aayog publishes the exam center notice and sit the 100 mark Pre-test (Level 4) followed by Paper 1 and Paper 2', 30, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate and digital photo/signature', 'SEE, +2, Bachelor or Master transcripts and character certificates', 'Inclusive group certificate (Adivasi Janajati, Madhesi, Dalit, Backward Area or Disability) if claiming quota'],
     'link': 'exam:g-adbl'},
    {'id': 'judicial-service-apply', 'name': 'Apply for Lok Sewa Judicial Service Officer (Nyaya Sewa)', 'cat': 'Applications',
     'steps': [
         ['Complete your 3 year LL.B or 5 year BA LL.B degree and obtain your transcript and character certificate (Advocate licence is recommended though not mandatory for Section Officer entry)', 1, 0, 'in person'],
         ['Log in to psconline1.psc.gov.np when the Public Service Commission publishes the annual Mangsir Gazetted Third Class (Technical/Non-Technical/Judicial) notice', 1, 0, 'online'],
         ['Select Judicial Service (Justice, Law and Government Attorney groups) and pay the NPR 1,000 fee (+ NPR 400 per additional group)', 1, 1000, 'online'],
         ['Sit the four 100 mark descriptive law papers directly (no Stage I administrative MCQ prelim is required for Judicial Service) followed by computer test and interview', 45, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate', 'LL.B or BA LL.B transcript and character certificate', 'Equivalence certificate from TU Curriculum Development Centre if law degree is from abroad'],
     'link': 'exam:g-judicial'},
    {'id': 'acca-nepal-register', 'name': 'Register and Sit for ACCA Exams in Nepal', 'cat': 'Study',
     'steps': [
         ['Verify +2 grades (65 percent in two subjects including English or Maths/Accounts and 50 percent in others) or use the Foundations in Accountancy (FIA) entry route', 1, 0, 'online'],
         ['Create a MyACCA account at accaglobal.com, upload transcripts and citizenship/passport, claim any BBS/BBA/MBS/CA exemptions and pay the GBP 89 initial registration fee', 5, 15500, 'online'],
         ['Book on-demand Computer Based Exams (BT, MA, FA, LW) at an ACCA Approved Learning Partner CBE center in Kathmandu, Lalitpur or Pokhara', 7, 17000, 'in person'],
         ['Enter quarterly session CBEs (March, June, September, December) for Applied Skills and Strategic Professional papers, complete EPSM (GBP 83) and log 36 months of PER', 365, 28000, 'online'],
     ],
     'docs': ['Passport or English translated citizenship certificate', 'SEE and +2 (and Bachelor/Master/CA if claiming exemptions) transcripts', 'International dollar card or bank draft for GBP fee payment'],
     'link': 'exam:e-acca'},
    {'id': 'nhpc-licence-apply', 'name': 'Register for the NHPC Health Professional Licensing Exam', 'cat': 'Study',
     'steps': [
         ['Complete your PCL (HA, CMLT, Radiography, Dental, Physiotherapy, Ophthalmic) or Bachelor/Master (BPH, BSc MLT, BSc MIT, BPT, BOptom, BASLP) from an NHPC recognized institution', 1, 0, 'in person'],
         ['Create an online profile at nhpc.gov.np, select your level (Second Class for PCL, First Class for Bachelor, Specialist for Master) and upload notarized transcripts and internship completion letters', 2, 0, 'online'],
         ['Pay the NPR 3,000 NHPC licensing exam fee online before the quarterly deadline', 1, 3000, 'online'],
         ['Sit the 2 hour computer based licensing exam (50 percent pass mark) at Bansbari, Kathmandu to receive your NHPC registration certificate', 14, 0, 'in person'],
     ],
     'docs': ['Citizenship certificate', 'SEE, PCL/Bachelor transcripts, character certificates and compulsory internship letter', 'TU or CTEVT equivalence certificate for foreign health degrees'],
     'link': 'exam:e-nhpc'},
    {'id': 'npc-pharmacy-licence', 'name': 'Register for the Nepal Pharmacy Council (NPC) Licensure Exam', 'cat': 'Study',
     'steps': [
         ['Complete a 3 year Diploma in Pharmacy (DPharm) or 4 year Bachelor of Pharmacy (BPharm) from an NPC approved institution', 1, 0, 'in person'],
         ['Submit your online application at nepalpharmacycouncil.org.np during the thrice yearly NPC exam window and upload all academic and citizenship documents', 2, 0, 'online'],
         ['Pay the NPR 3,000 exam fee online and download your admit card once verified by the council', 1, 3000, 'online'],
         ['Pass the 100 question MCQ licensure exam (minimum 50 percent required) and pay the NPR 3,000 registration certificate fee', 10, 3000, 'in person'],
     ],
     'docs': ['Citizenship certificate', 'SEE and DPharm or BPharm transcripts, provisional and character certificates', 'Equivalence certificate and NOC for foreign BPharm graduates'],
     'link': 'exam:e-npc'},
    {'id': 'nvc-vet-licence', 'name': 'Register for the Nepal Veterinary Council (NLEV) Licensure Exam', 'cat': 'Study',
     'steps': [
         ['Complete your 5 year BVSc and AH degree (including compulsory rotating internship) from AFU, TU IAAS, HICAST, NPI or an approved foreign university', 1, 0, 'in person'],
         ['Register on the Nepal Veterinary Council portal (vcn.gov.np) when the annual NLEV call opens and upload your degree and internship documents', 2, 0, 'online'],
         ['Pay the NPR 3,000 NLEV examination fee and collect your admit card from the Tripureshwor, Kathmandu office', 1, 3000, 'online'],
         ['Pass the 90 minute, 100 question MCQ exam (40 percent pass mark) to register as a licensed Veterinarian under the Nepal Veterinary Council Act 2055', 7, 2500, 'in person'],
     ],
     'docs': ['Citizenship certificate', 'SEE, +2 and BVSc and AH transcripts, internship completion and character certificates', 'TU equivalence certificate and Ministry NOC if graduated abroad'],
     'link': 'exam:e-nvc'},
]
