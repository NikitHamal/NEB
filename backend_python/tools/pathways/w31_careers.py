"""Wave 31: seven careers that had no entry yet, with monthly NPR salary bands from 2026 Nepal salary guides (read 20 Nov 2026).
Ratings (demand, competition 1 to 5) are the editors' reading of the same guides and of the job pages named.

- chef: necojobs.com.np (Jan 2026: entry 12,000 to 20,000, commis 15,000 to 25,000, sous 35,000 to 60,000, head 70,000 to 120,000+), hwc.edu.np (commis 18,000 to 30,000,
  sous 70,000 to 150,000, executive 200,000+), jwalajobs.com (commis 22,000 to 35,000, executive 150,000 to 250,000 at five star hotels). Band: entry 18,000 to 30,000, senior 70,000 to 150,000.
- QA engineer: skillshikshya.com (June 2026, Glassdoor Nepal April 2026: junior 25,000 to 50,000, senior 120,069 to 221,683).
- HR manager: kumarijob.com (Nov 2025: entry 18,000 to 30,000, manager 60,000 to 120,000), upskillsnepal.com (HR manager 60,000 to 120,000).
- Hydropower engineer: necojobs.com.np (Jan 2026: fresh engineers 25,000 to 45,000, experienced 60,000 to 120,000).
- Cabin crew: globalwings.com.np (May 2026: entry total pay 40,000 to 70,000, Buddha Air and Yeti senior 95,000 to 130,000), kumarijob.com (30,000 to 60,000 on domestic airlines).
- Network engineer: texascollege.edu.np (Aug 2026: entry 30,000 to 50,000, senior 75,000 to 140,000), kumarijob.com (entry 20,000 to 40,000, senior 80,000 to 120,000+).
- NGO programme officer: kumarijob.com (Dec 2025: entry 30,000 to 60,000, senior 150,000 to 300,000+), ejobsnp.com and pawanjoshi.com.np (programme officer 80,000 to 180,000).
"""

CAREERS_NEW = [
    {'id': 'chef', 'name': 'Chef', 'about': 'Plans, cooks and runs kitchens in hotels, restaurants, resorts, airlines and ships, moving from commis to sous chef to executive chef. Many Nepali chefs also work in the Gulf, Europe and cruise lines.',
     'demand': 4, 'competition': 3, 'trend': 'steady', 'abroad': 5, 'salary': {'entry': [18000, 30000], 'senior': [70000, 150000]},
     'skills': ['Food safety', 'Menu costing', 'Continental and Nepali cuisine', 'Team leadership'], 'ladder': ['Commis', 'Chef de partie', 'Sous chef', 'Executive chef'],
     'employers': ['Star hotels and resorts', 'Restaurant chains', 'Airline catering', 'Overseas hotels and cruise lines'], 'hours': 48},
    {'id': 'qa-engineer', 'name': 'QA engineer (software tester)', 'about': 'Tests apps and websites before release, writes test cases and automation scripts, and reports bugs to developers.',
     'demand': 4, 'competition': 3, 'trend': 'rising', 'abroad': 4, 'salary': {'entry': [25000, 50000], 'senior': [120000, 221000]},
     'skills': ['Test cases', 'Selenium and Postman', 'SQL', 'CI/CD basics'], 'ladder': ['Junior QA', 'QA engineer', 'Senior or automation QA', 'QA lead'],
     'employers': ['Software companies', 'Fintech such as eSewa, Khalti and F1Soft', 'Banks', 'Overseas clients'], 'hours': 40},
    {'id': 'hr-manager', 'name': 'HR officer and manager', 'about': 'Hires, trains and looks after staff, runs payroll and labour law paperwork, and builds the culture of a company, bank, hotel or INGO.',
     'demand': 3, 'competition': 4, 'trend': 'steady', 'abroad': 3, 'salary': {'entry': [18000, 30000], 'senior': [60000, 120000]},
     'skills': ['Recruitment', 'Labour law', 'Payroll and HRMS tools', 'Communication'], 'ladder': ['HR assistant', 'HR officer', 'HR manager', 'HR director'],
     'employers': ['Banks and finance', 'Hotels', 'INGOs', 'Large private companies'], 'hours': 40},
    {'id': 'hydropower-engineer', 'name': 'Hydropower engineer', 'about': 'Designs, builds and runs hydropower plants and transmission lines, working on site in the hills with civil, electrical and mechanical teams.',
     'demand': 4, 'competition': 3, 'trend': 'steady', 'abroad': 3, 'salary': {'entry': [25000, 45000], 'senior': [60000, 120000]},
     'skills': ['Hydrology', 'Structural design', 'Turbines and generators', 'Project management'], 'ladder': ['Site engineer', 'Design or plant engineer', 'Senior engineer', 'Project manager'],
     'employers': ['Nepal Electricity Authority', 'Private hydropower companies', 'Consulting firms', 'Contractors'], 'hours': 48},
    {'id': 'cabin-crew', 'name': 'Cabin crew', 'about': 'Looks after passenger safety and service on board, trains on emergency procedures for each aircraft type and works rotating shifts on domestic and international routes.',
     'demand': 3, 'competition': 4, 'trend': 'steady', 'abroad': 5, 'salary': {'entry': [35000, 60000], 'senior': [95000, 130000]},
     'skills': ['Safety and first aid', 'Customer service', 'English and another language', 'Grooming and fitness'], 'ladder': ['Trainee crew', 'Cabin crew', 'Senior crew', 'Purser'],
     'employers': ['Buddha Air', 'Yeti Airlines', 'Nepal Airlines', 'Gulf and Asian airlines'], 'hours': 40},
    {'id': 'network-engineer', 'name': 'Network engineer', 'about': 'Plans and runs the wired, wireless and cloud networks of banks, telecoms, ISPs and companies, and keeps them fast and secure.',
     'demand': 4, 'competition': 3, 'trend': 'steady', 'abroad': 4, 'salary': {'entry': [25000, 50000], 'senior': [75000, 140000]},
     'skills': ['Cisco and routing', 'Linux and servers', 'Network security', 'Cloud networking'], 'ladder': ['Network support', 'Network engineer', 'Senior engineer', 'Network architect'],
     'employers': ['Banks', 'Telecoms such as Ncell and Nepal Telecom', 'ISPs', 'Data centres'], 'hours': 40},
    {'id': 'ngo-program-officer', 'name': 'NGO and INGO programme officer', 'about': 'Designs, runs and reports on development projects in health, education, livelihoods or governance for NGOs, UN agencies and donors.',
     'demand': 3, 'competition': 5, 'trend': 'steady', 'abroad': 4, 'salary': {'entry': [30000, 60000], 'senior': [150000, 300000]},
     'skills': ['Project cycle management', 'Report and proposal writing', 'Monitoring and evaluation', 'English'], 'ladder': ['Program assistant', 'Program officer', 'Program manager', 'Country or technical lead'],
     'employers': ['INGOs', 'UN agencies', 'National NGOs', 'Donor funded projects'], 'hours': 40},
]

CAREER_LINKS = {
    'bhm': ['chef'], 'dip-hospitality': ['chef'],
    'bsc-csit': ['qa-engineer', 'network-engineer'], 'bca': ['qa-engineer'], 'bit': ['qa-engineer', 'network-engineer'], 'mca': ['qa-engineer'], 'be-computer': ['qa-engineer', 'network-engineer'],
    'bbs': ['hr-manager'], 'bba': ['hr-manager'], 'bbm': ['hr-manager'], 'mba': ['hr-manager'], 'mbs': ['hr-manager'], 'bim': ['hr-manager'],
    'be-civil': ['hydropower-engineer'], 'be-electrical': ['hydropower-engineer'], 'be-mechanical': ['hydropower-engineer'], 'be-chemical-hydro': ['hydropower-engineer'],
    'aviation-cabin-crew': ['cabin-crew'],
    'dip-computer-eng': ['network-engineer'], 'dip-it-computer': ['network-engineer'], 'be-electronics': ['network-engineer'], 'bicte': ['network-engineer'],
    'bsw': ['ngo-program-officer'], 'msw': ['ngo-program-officer'], 'ba': ['ngo-program-officer'], 'mpa': ['ngo-program-officer'], 'mph': ['ngo-program-officer'],
    'ingo-fellowship-route': ['ngo-program-officer'], 'bph': ['ngo-program-officer'],
}
