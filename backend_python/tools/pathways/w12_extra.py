"""Wave 12, part 5: three IT careers with 2026 salary bands, an English test guide, and FAQs on test fees and education loans.

Keys owned in wave12.json: careers_new, career_links, guides_more, faq_extra.
Sources: Nepali salary surveys read in 2026 (necojobs.com.np, skillshikshya.com, thelondoncollege.edu.np, texasintl.edu.np: ranges agree within
about 20 percent, the mid point is used), IELTS fee pages read October 2026 (NPR 36,000 computer delivered at British Council and IDP; paper test phased out
from mid 2026), TOEFL and PTE fee guides (USD 195 to 205 and about USD 220), NRB Unified Directives 2081 education loan summary (collegenp.com, edunepal.com).
Run: python3 backend_python/tools/pathways/w12_extra.py
"""
import json
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave12.json'
w = json.loads(FILE.read_text('utf-8')) if FILE.exists() else {}

w['careers_new'] = [
    {'id': 'ui-ux-designer', 'name': 'UI and UX designer',
     'about': 'Designs how apps and websites look and feel, from research and wireframes to the final Figma screens that developers build.',
     'demand': 4, 'competition': 4, 'trend': 'rising', 'abroad': 4, 'salary': {'entry': [25000, 40000], 'senior': [90000, 150000]},
     'skills': ['Figma', 'User research', 'Design systems', 'Prototyping'], 'ladder': ['Intern', 'Junior designer', 'Product designer', 'Design lead'],
     'employers': ['Product companies', 'Software agencies', 'Banks and fintech', 'Overseas clients'], 'hours': 40},
    {'id': 'data-scientist', 'name': 'Data scientist',
     'about': 'Builds models and analyses from large data sets to predict and decide: forecasts, recommendations and language or vision systems.',
     'demand': 4, 'competition': 3, 'trend': 'rising', 'abroad': 5, 'salary': {'entry': [25000, 60000], 'senior': [120000, 250000]},
     'skills': ['Python', 'Statistics', 'SQL', 'Machine learning'], 'ladder': ['Analyst', 'Data scientist', 'Senior scientist', 'Head of data'],
     'employers': ['Fusemachines', 'Leapfrog', 'F1Soft', 'Deerwalk', 'Verisk', 'Overseas clients'], 'hours': 40},
    {'id': 'cloud-devops-engineer', 'name': 'Cloud and DevOps engineer',
     'about': 'Runs the servers, pipelines and cloud accounts that keep software online, secure and fast.',
     'demand': 4, 'competition': 3, 'trend': 'rising', 'abroad': 5, 'salary': {'entry': [35000, 65000], 'senior': [100000, 160000]},
     'skills': ['Linux', 'AWS or Azure', 'Docker and Kubernetes', 'CI/CD'], 'ladder': ['Junior engineer', 'DevOps engineer', 'Senior engineer', 'Platform lead'],
     'employers': ['Software companies', 'Banks and telecom', 'Data centres', 'Overseas clients'], 'hours': 40},
]
w['career_links'] = {'be-computer': ['cloud-devops-engineer', 'data-scientist'], 'bsc-csit': ['data-scientist', 'cloud-devops-engineer'],
                     'bca': ['ui-ux-designer'], 'bit': ['cloud-devops-engineer'], 'mds-data-science': ['data-scientist'],
                     'bfd-design': ['ui-ux-designer'], 'dip-computer-eng': ['cloud-devops-engineer']}

w['guides_more'] = [
    {'id': 'english-test', 'name': 'English test for study abroad (IELTS, PTE, TOEFL)', 'cat': 'Abroad',
     'steps': [['Ask your university which test and score it accepts (many take Duolingo, some need UKVI IELTS)', 0, 0, 'online'],
               ['Book IELTS at British Council or IDP with your original passport, the only accepted ID', 1, 36000, 'online'],
               ['Sit the computer delivered test', 14, 0, 'in person'],
               ['Send the score to universities; the report is valid for 2 years', 3, 0, 'online']],
     'docs': ['Original passport', 'Passport photo', 'University score requirement'], 'link': 'guide:noc-study-abroad'},
]

F = [
    ('abroad', 'How much do IELTS, PTE and TOEFL cost in Nepal in 2026?', ['abroad-ms'],
     'IELTS on computer is NPR 36,000 at both British Council and IDP in October 2026 (UKVI IELTS NPR 36,400, Life Skills NPR 29,000). Earlier in 2026 some pages listed NPR 33,000, so confirm on the booking page. The paper test was being phased out from mid 2026. TOEFL iBT is about USD 195 to 205 (NPR 27,000 to 30,000) and PTE Academic about USD 220, while the Duolingo English Test is about USD 70 and accepted by many universities. You need your original passport as ID, and scores stay valid for 2 years.'),
    ('abroad', 'How does an education loan for study abroad work in Nepal?', ['abroad-ms'],
     'Under Nepal Rastra Bank rules a bank can finance 80 to 100 percent of fees, hostel and other needed costs, depending on how it values your collateral (it often lends up to about 80 percent of a distress value, not the market price). The family income test is that the instalment must fit within 50 percent of verified monthly income, and a PAN is needed above NPR 50 lakh. Rates are the bank base rate plus a 2 to 5 percent premium, which came to roughly 10 to 14 percent fixed in 2025; floating offers were lower. Ceilings quoted by banks range from NPR 40 to 80 lakh. Loans above about NPR 7.5 lakh normally need collateral such as land or a fixed deposit, so ask each bank for its current sheet.'),
    ('after12', 'What does a UI and UX designer earn in Nepal?', [],
     'Surveys read in 2026 agree closely: interns NPR 8,000 to 15,000, juniors NPR 25,000 to 40,000, mid level (2 to 4 years) NPR 50,000 to 85,000 and seniors NPR 90,000 to 150,000 a month, with leads on overseas projects above NPR 150,000. A Figma portfolio matters more than the degree; BCA, BIT, BSc CSIT and design diplomas all lead here.'),
    ('after12', 'What do software, data and cloud jobs pay in Nepal in 2026?', ['bsc-csit', 'be-computer'],
     'Software developers start at about NPR 25,000 to 50,000, reach NPR 50,000 to 100,000 with 2 to 5 years and NPR 90,000 to 250,000 or more at senior level or on overseas projects. Data scientists are listed at NPR 25,000 to 60,000 as juniors and NPR 120,000 to 250,000 as seniors, and cloud and DevOps engineers at about NPR 65,000 to 160,000 once experienced. Figures vary by company and survey; read them as bands, not offers.'),
    ('after10', 'How did SEE 2082 go, and what can a student with NG do?', ['open-school-see', 'pre-diploma', 'plus2-science'],
     'NEB published SEE 2082 on 28 Baishakh 2083 (11 May 2026): 512,421 registered, 430,667 regular students sat, 284,160 passed with a grade (65.98 percent) and 146,507 got Non-Graded (NG). Grades were spread as GPA 3.6 to 4.0: 48,392; 3.2 to 3.6: 80,372; 2.8 to 3.2: 94,222; 2.4 to 2.8: 55,977; 2.0 to 2.4: 5,190; 1.6 to 2.0: 7. A GPA above 1.6 opens higher study. With NG you can sit the grade increment or supplementary exam, and CTEVT pre-diploma programmes also accept students who sat every SEE subject and received NG.'),
]
w['faq_extra'] = [{'id': f'fw12-x{i}', 'topic': t, 'q': q, 'go': g, 'a': a} for i, (t, q, g, a) in enumerate(F, 1)]

FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(len(w['careers_new']), len(w['faq_extra']))
