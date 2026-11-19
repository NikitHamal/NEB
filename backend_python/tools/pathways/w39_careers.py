"""Wave 39: three careers with monthly NPR bands from 2026 Nepal salary guides (read 19 Nov 2026). Ratings (demand, competition 1 to 5) are the editors' reading of the same pages.

- Mobile app developer: kumarijob.com guide (2026: entry 25,000 to 40,000, mid 40,000 to 70,000, senior 70,000 to 150,000 and above; table fresher 25,000 to 35,000, senior 80,000 to 150,000+),
  necojobs.com.np (15 April 2026: entry 20,000 to 40,000, senior 100,000 to 200,000 and above), kumarijob .NET page (25 May 2026: entry mobile 25,000 to 45,000, experienced 80,000 to 180,000,
  remote or international senior above 250,000). Band used: entry 25,000 to 40,000 (the overlap), senior 80,000 to 150,000 (the lower of the two senior ranges against the higher one).
- Customer support and BPO: kumarijob.com BPO guide (12 Aug 2026: entry 15,000 to 25,000, customer service representative 18,000 to 30,000, experienced 30,000 to 50,000 and more) and two kumarijob
  vacancy pages (Classic Tech: 15,000 to 20,000 with +2 and 6 months; GPG Services: 20,000 to 25,000 negotiable, 5 am shift for Australia, USA, Canada and UK campaigns). Band: entry 15,000 to 25,000,
  senior 30,000 to 50,000. Night shift allowances and incentives are extra and not counted.
- Insurance officer and agent: kumarijob.com Nepal life insurance guide (19 Feb 2026: management trainee 40,000 to 45,000, entry 25,000 to 35,000, mid level 60,000 to 95,000, senior up to 250,000+),
  necojobs.com.np (22 June 2026: starting 15,000 to 30,000, agents earn commission only, 20,000 to 40,000 at first and 100,000 or more with strong sales), worldsalaries.com (agent average 48,208, lowest
  25,741, highest 73,308). Band: entry 25,000 to 40,000, senior 95,000 to 250,000 for salaried staff. Agent pay is commission and swings widely.
"""
CAREERS_NEW = [
    {'id': 'mobile-app-developer', 'name': 'Mobile app developer', 'about': 'Builds Android, iOS and cross platform apps for fintech, e-commerce, ride and delivery, education and startups, and often takes remote contracts from foreign clients.',
     'demand': 4, 'competition': 4, 'trend': 'rising', 'abroad': 5, 'salary': {'entry': [25000, 40000], 'senior': [80000, 150000]},
     'skills': ['Flutter or React Native', 'Kotlin or Swift', 'REST APIs and Firebase', 'App store release and testing'], 'ladder': ['Junior or intern developer', 'Mobile developer', 'Senior mobile engineer', 'Tech lead or architect'],
     'employers': ['Software companies in Kathmandu and Lalitpur', 'Banks, wallets and fintech', 'Product startups', 'Overseas remote clients'], 'hours': 45},
    {'id': 'customer-support-bpo', 'name': 'Customer support and BPO agent', 'about': 'Answers calls, chats and emails for telecom, banks, e-commerce and overseas companies, many of them on night or early shifts for Australia, the UK and the US. A common first job for +2 and bachelor students.',
     'demand': 4, 'competition': 3, 'trend': 'steady', 'abroad': 2, 'salary': {'entry': [15000, 25000], 'senior': [30000, 50000]},
     'skills': ['Spoken and written English', 'Typing and MS Office', 'Patience and problem solving', 'Sales conversion and call quality targets'], 'ladder': ['Customer service representative', 'Senior agent', 'Team leader or quality analyst', 'Operations manager'],
     'employers': ['BPO and call centres in Kathmandu', 'Telecom and internet providers', 'Banks and wallets', 'E-commerce and delivery apps'], 'hours': 45},
    {'id': 'insurance-officer', 'name': 'Insurance officer and agent', 'about': 'Sells and services life and non life insurance, handles claims, underwriting and branch work. Agents earn commission, while officers and management trainees are paid a salary with incentives.',
     'demand': 3, 'competition': 3, 'trend': 'steady', 'abroad': 1, 'salary': {'entry': [25000, 40000], 'senior': [95000, 250000]},
     'skills': ['Sales and relationship building', 'Product and policy knowledge', 'Claims and risk assessment', 'Insurance Authority agent licence'], 'ladder': ['Agent or trainee officer', 'Officer', 'Senior officer or assistant manager', 'Branch or department manager'],
     'employers': ['Life insurance companies', 'Non life insurance companies', 'Banks with bancassurance desks', 'Insurance brokers'], 'hours': 45},
]
CAREER_LINKS = {
    'be-computer': ['mobile-app-developer'], 'bsc-csit': ['mobile-app-developer'], 'bca': ['mobile-app-developer'], 'bit': ['mobile-app-developer'], 'bicte': ['mobile-app-developer'],
    'bbs': ['customer-support-bpo', 'insurance-officer'], 'bba': ['customer-support-bpo', 'insurance-officer'], 'bbm': ['insurance-officer'], 'bim': ['insurance-officer'],
    'ba': ['customer-support-bpo'], 'plus2-management': ['customer-support-bpo'], 'plus2-humanities': ['customer-support-bpo'], 'mbs': ['insurance-officer'],
}
