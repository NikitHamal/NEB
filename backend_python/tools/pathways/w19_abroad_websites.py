"""Wave 19 international scholarships (10 countries), abroad notes and 33 live-verified official college websites.

Sources (read 19 November 2026): University of Copenhagen ku.dk (Danish Government Scholarship 2026 level DKK 11,225/mo, DTU DKK 8,500/mo, older quotes DKK 6,090 to 6,397/mo);
OeAD grants.at and akbild.ac.at (Ernst Mach Grant Worldwide and FH EUR 1,300/mo + up to EUR 1,200 travel subsidy, deadline 1 Feb 2026);
BI Norwegian Business School bi.edu and leapscholar.com (BI Presidential Scholarship 100% MSc tuition + NOK 50,000/sem stipend, 20 international awards, deadline 1 Mar 2026);
Australian Dept of Education and University of Sydney sydney.edu.au (RTP 2026 national base AUD 36,061 to 37,010/yr, Melbourne/UQ AUD 32,192 to 39,220, ANU AUD 39,069, Sydney AUD 42,754);
Government of Canada vanier.gc.ca (Vanier CGS / Canada Graduate Research Scholarship Doctoral CAD 50,000/yr for 3 yrs, 166 awards);
TICA Thailand tica-thaigov.com (TIPP 2026 living THB 7,000/mo, housing THB 7,000 to 9,000/mo, settlement THB 6,000, books THB 10,000/yr, deadline 23 Feb 2026, plus AIT RTG scholarships);
Lithuania Education Exchanges Support Foundation studyin.lt (2026 State Master stipend 8 BSAs = EUR 592/mo, 70 grants, restricted to 17 countries excluding Nepal; KTU/VMU/VU waivers open);
Estonia Harno and howtoestonia.com (Tartu ended non-EU tuition waivers from 2026/27; Dora Plus ended 31 May 2023; Harno pays EUR 350/mo MA and EUR 660/mo PhD; TalTech waivers EUR 3,000 to 6,000/yr);
Spain study-abroad.org and opportunitiesjournal.com (UC3M, BSE, UB, Navarra 10% to 100% waivers, ICFO PhD EUR 2,100 to 2,200/mo; MAEC-AECID & Fundacion Carolina regional scope);
Portugal FCT and globalscholarships.com (FCT PhD EUR 1,144/mo, Aveiro EUR 1,000/yr Master fee reduction, Coimbra EUR 2,000 incentive, Porto 5x minimum wage merit award).
"""

SCHOLARSHIPS_ADD = [
    {'id': 's-danish-govt', 'name': 'Danish Government Scholarships for Non-EU/EEA Students (UCPH, DTU, Aarhus, ITU, CBS)', 'by': 'Ministry of Higher Education and Science of Denmark (via universities)',
     'country': 'dk', 'type': 'Government', 'open': [10, 3],
     'covers': 'Full or partial tuition waiver (worth DKK 70,000 to 120,000 or EUR 8,000 to 17,000 a year) plus, for top awardees, a monthly living grant (University of Copenhagen quotes DKK 11,225/month for 22 months in 2026; DTU quotes DKK 8,500/month; general listings quote DKK 6,090 to 6,397/month before tax)',
     'who': 'Non-EU/EEA citizens (including Nepal) admitted to an English-taught Master degree at a participating Danish public university (Copenhagen, DTU, Aarhus, CBS, ITU, SDU, Aalborg)',
     'how': 'No separate scholarship form at most universities: apply for Master admission by the non-EU deadline (typically 15 January at UCPH, DTU, Aarhus and ITU, or 1 February to 1 March at CBS, SDU and Aalborg) for automatic merit consideration.'},
    {'id': 's-ernst-mach-at', 'name': 'OeAD Ernst Mach Grant (Worldwide and Austrian Universities of Applied Sciences)', 'by': 'OeAD and Austrian Federal Ministry of Education, Science and Research',
     'country': 'at', 'type': 'Government', 'open': [10, 2],
     'covers': 'EUR 1,300 monthly stipend plus host tuition waiver and an international travel subsidy of up to EUR 1,200 (accommodation and health insurance are paid out of the monthly grant)',
     'who': 'Ernst Mach Worldwide funds 1 to 9 month research stays in Austria for PhD students, postgraduates and postdocs outside Austria aged 35 or under; the FH track funds 4 to 10 month exchange stays at Austrian Universities of Applied Sciences for non-European Bachelor (4+ semesters) or Master students. Neither track funds an entire degree',
     'how': 'Secure a host acceptance letter from an Austrian university professor or FH coordinator and submit online at scholarships.at / grants.at by 1 February. For full degrees in Austria, combine public university tuition (EUR 726.72/semester or LDC waiver) with university Leistungsstipendium merit grants (EUR 750 to 1,500/year).'},
    {'id': 's-bi-norway', 'name': 'BI Presidential Scholarship (BI Norwegian Business School)', 'by': 'BI Norwegian Business School, Oslo and Bergen',
     'country': 'no', 'type': 'University', 'open': [11, 3],
     'covers': '100% MSc tuition fee waiver for up to 2 years (worth about NOK 318,390 a year) plus a living stipend of NOK 50,000 per semester (NOK 100,000 a year) for international awardees',
     'who': 'International applicants from any country with a top undergraduate grade equivalent to an A on the ECTS scale admitted to a full-time Master of Science (Finance, Business Analytics, Applied Economics, Data Science, Strategic Marketing) at BI Oslo or Bergen (up to 20 international awards a year)',
     'how': 'Upload a one-page scholarship application letter and CV inside the BI MSc online admission portal by the 1 March priority deadline. Renewal each semester requires completing 30 ECTS with at least a B cumulative GPA.'},
    {'id': 's-rtp-au', 'name': 'Australian Government Research Training Program (RTP) International Scholarship', 'by': 'Australian Government Department of Education (via participating universities)',
     'country': 'au', 'type': 'Government', 'open': [4, 10],
     'covers': '100% tuition fee offset (up to 4 years for PhD, 2 years for Master by Research) plus a tax-free living stipend (2026 national base AUD 36,061 to 37,010/year; Melbourne/UQ quote AUD 32,192 to 39,220, ANU AUD 39,069, and University of Sydney AUD 42,754/year), single OSHC health cover, relocation allowance (about AUD 1,485 to 2,000) and thesis allowance (AUD 420 to 840)',
     'who': 'International students of any nationality with a first-class honours or research master equivalent applying for a Higher Degree by Research (MPhil / Master by Research or PhD) at an Australian university',
     'how': 'Apply directly to the target Australian university HDR admission portal (most assess RTP automatically with your PhD/MPhil application; key international deadlines fall between April and August/October such as ANU 15 April and 31 August).'},
    {'id': 's-vanier-ca', 'name': 'Vanier Canada Graduate Scholarships / Canada Graduate Research Scholarship (Doctoral)', 'by': 'Government of Canada (CIHR, NSERC and SSHRC)',
     'country': 'ca', 'type': 'Government', 'open': [7, 11],
     'covers': 'CAD 50,000 per year for up to 3 years toward doctoral tuition, research and living expenses (up to 166 awards annually across health, natural sciences/engineering and social sciences/humanities)',
     'who': 'International and Canadian PhD (or combined MA/PhD, MD/PhD) candidates with a first-class average in their last two years of study, strong research output and leadership, nominated by a Canadian university with a quota',
     'how': 'Secure PhD admission/supervision support and apply for your Canadian university internal nomination (deadlines usually August to October) before the federal ResearchNet submission in late October/November. Note that Canada is transitioning Vanier CGS into the harmonized Canada Graduate Research Scholarship - Doctoral framework.'},
    {'id': 's-tipp-th', 'name': 'Thailand International Postgraduate Programme (TIPP) and Royal Thai Government AIT Scholarships', 'by': 'Thailand International Cooperation Agency (TICA), Ministry of Foreign Affairs of Thailand',
     'country': 'th', 'type': 'Government', 'open': [11, 2],
     'covers': 'Full tuition, monthly living allowance of THB 7,000, accommodation allowance of THB 7,000 to 9,000/month, one-time settlement allowance of THB 6,000, books allowance of THB 10,000/year, thesis fieldwork up to THB 20,000 and printing THB 8,000 to 12,000, round-trip economy flights, visa fee and medical insurance',
     'who': 'Graduates from eligible developing countries including Nepal, aged under 45 with a bachelor degree, English proficiency and work experience (often nominated through government or development agencies) for Master degrees in public health, climate change, agriculture and sufficiency economy',
     'how': 'Complete the online TICA form and submit hard copies through the Royal Thai Embassy in Kathmandu and Nepal government nodal channel by the February deadline (23 February 2026 for the 2026 intake). Separate non-bonded Royal Thai Government (King and Queen) scholarships are also awarded directly through AIT near Bangkok.'},
    {'id': 's-ktu-vmu-lt', 'name': 'Lithuanian University Merit Waivers (KTU, VMU, Vilnius University) and State Scholarship Rule', 'by': 'Kaunas University of Technology, Vytautas Magnus University, Vilnius University and Study in Lithuania',
     'country': 'lt', 'type': 'University', 'open': [1, 6],
     'covers': '25% to 100% tuition fee waivers at KTU, VMU and Vilnius University (plus EUR 250/month talent stipends for top students). Note: the government Lithuanian State Scholarship for Full-Time Master Studies (8 BSAs = EUR 592/month in 2026, 70 grants) is restricted to 17 listed countries (such as Ukraine, Georgia, Uzbekistan, Kazakhstan, China, Japan, USA) and Nepal is NOT on the eligible country list',
     'who': 'International Bachelor and Master applicants from any country (including Nepal) with a strong GPA (typically 80% / CGPA 3.2+ for KTU and VMU tuition waivers)',
     'how': 'Apply for university tuition waivers inside your KTU, VMU or Vilnius University admission portal between January and May/June; do not rely on the Lithuanian State Master call on studyin.lt unless Nepal is added to the country list.'},
    {'id': 's-taltech-harno-ee', 'name': 'Estonia Harno Degree Scholarship and TalTech International Tuition Waivers (2026/27 Rules)', 'by': 'Education and Youth Board of Estonia (Harno) and Tallinn University of Technology (TalTech)',
     'country': 'ee', 'type': 'Government', 'open': [1, 4],
     'covers': 'Harno degree and exchange scholarship pays EUR 350/month for Master and EUR 660/month for PhD; TalTech International Degree Scholarships waive tuition worth EUR 3,000 to 6,000/year for top non-EU engineering/IT/cybersecurity admits plus optional EUR 100/month performance stipends',
     'who': 'Non-EU international students admitted to TalTech or Estonian Master/PhD programmes. Important 2026/27 update: the University of Tartu ended tuition waivers for newly admitted non-EU students from the 2026/27 intake (announced March 2026), and the older Dora Plus scheme ended on 31 May 2023',
     'how': 'Apply to TalTech before the non-EU deadline (around 1 February to 1 March) for automatic tuition waiver and TalTech Development Fund consideration, and check harno.ee for the spring Harno scholarship window.'},
    {'id': 's-spain-uc3m-bse', 'name': 'Spanish University International Merit Scholarships (UC3M, BSE, UB, Navarra, ICFO)', 'by': 'Spanish Public and Research Universities (UC3M, Barcelona School of Economics, ICFO, Navarra)',
     'country': 'es', 'type': 'University', 'open': [11, 4],
     'covers': '25% to 100% Master tuition waivers at Barcelona School of Economics (BSE), 10% to 50% tuition reductions at UC3M (Madrid), University of Barcelona and University of Navarra (plus up to EUR 400/month), and 100% funded PhD contracts (EUR 2,100 to 2,200/month) at ICFO Institute of Photonic Sciences',
     'who': 'International Master and PhD applicants of all nationalities including Nepal. Note that Spain national Fundación Carolina awards target Latin America and MAEC-AECID bilateral calls primarily cover Latin America, Africa, the Middle East and the Philippines, so Nepali students should target university merit awards, La Caixa/ICFO fellowships or Erasmus Mundus',
     'how': 'Submit your Master or PhD application by the university priority scholarship deadline (mid-January for BSE, January to April for UC3M, UB and Navarra).'},
    {'id': 's-fct-aveiro-pt', 'name': 'Portugal FCT Doctoral Studentships and Aveiro / Coimbra / Porto Merit Scholarships', 'by': 'Fundacao para a Ciencia e a Tecnologia (FCT) and Portuguese Public Universities',
     'country': 'pt', 'type': 'Government', 'open': [1, 6],
     'covers': 'FCT PhD studentships pay EUR 1,144 to 1,259/month plus full tuition and research/travel allowances; for 2026/27 Master students, University of Aveiro reduces international tuition to EUR 1,000/year, University of Coimbra awards a EUR 2,000 Master incentive reduction, and University of Porto awards merit grants equal to 5x the national minimum monthly wage',
     'who': 'International PhD candidates (any nationality) for FCT doctoral calls, and high-achieving non-EU Bachelor/Master students at Aveiro, Coimbra, Porto, Lisbon (IST) and NOVA (note: SASUP social grants are closed to non-EU international student status)',
     'how': 'Apply to the annual FCT doctoral call in March/April on myfct.fct.pt with a Portuguese host research centre, or apply directly during Master admission at Aveiro, Coimbra or Porto between January and June.'},
]

ABROAD_NOTE_ADD = {
    'ee': 'March 2026 update: the University of Tartu ended tuition waivers for newly admitted non-EU students starting from the 2026/27 intake (English fees EUR 3,800 to 13,200/year), and Dora Plus ended in May 2023. Non-EU students can still win TalTech tuition waivers (worth EUR 3,000 to 6,000/year) and Harno stipends (EUR 350/month Master, EUR 660/month PhD).',
    'lt': 'The Lithuanian State Scholarship for Full-Time Master Studies (EUR 592/month in 2026 plus tuition up to the national standard cost) is open only to 17 listed countries and does not include Nepal; Nepali students apply instead for KTU, VMU or Vilnius University tuition waivers (25% to 100%) or Erasmus Mundus.',
    'pt': 'For 2026/27, University of Porto international bachelor/integrated master fees are EUR 3,500 to 16,500/year, while University of Aveiro reduces qualifying international Master tuition to EUR 1,000/year and University of Coimbra grants a EUR 2,000 Master incentive reduction. FCT PhD studentships pay about EUR 1,144/month.',
}

PROVIDER_WEBSITES = {
    'p-peoples-dental': 'https://pdch.com.np',
    'p-bc-med': 'https://bncmedicalcollege.edu.np',
    'p-yeti-health': 'https://yhsa.edu.np',
    'p-little-buddha': 'https://littlebuddhacollege.edu.np',
    'p-kantipur-academy': 'https://www.kahs.edu.np',
    'p-nagarik-health': 'https://nagarikhealthsciences.edu.np',
    'p-cite': 'https://cit.edu.np',
    'p-kantipur-intl': 'https://kantipurinternational.edu.np',
    'p-niet': 'https://niet.edu.np',
    'p-vishwa-adarsha': 'https://vac.edu.np',
    'p-itahari-namuna': 'https://namunacollege.edu.np',
    'p-hetauda-sms': 'https://hsm.edu.np',
    'p-arunima': 'https://arunima.edu.np',
    'p-caribbean': 'https://caribbean.edu.np',
    'p-dav': 'https://davcollege.edu.np',
    'p-goldengate': 'https://goldengate.edu.np',
    'p-kcmit': 'https://kcmit.edu.np',
    'p-ktm-business': 'https://kbcampus.edu.np',
    'p-nims': 'https://nimscollege.edu.np',
    'p-padmashree': 'https://www.padmashreecollege.edu.np',
    'p-pascal': 'https://pascalcollege.edu.np',
    'p-times': 'https://timescollege.edu.np',
    'p-thames': 'https://thamescollege.edu.np',
    'p-united-college': 'https://united.edu.np',
    'p-universal': 'https://uc.edu.np',
    'p-kmc-model': 'https://kmcen.edu.np',
    'p-daffodil': 'https://daffodil.edu.np',
    'p-xavier-intl': 'https://xavier.edu.np',
    'p-kist': 'https://kist.edu.np',
    'p-degree-biratnagar': 'https://pgc.tu.edu.np',
    'p-national-law': 'https://nalc.edu.np',
    'p-w12-ce-lumbini-engineering-college': 'https://lumbini.edu.np',
    'p-malpi': 'https://malpi.edu.np',
}
