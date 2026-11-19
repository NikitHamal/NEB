"""Wave 34: three careers with monthly NPR bands from 2026 Nepal salary guides (read 19 Nov 2026).
Ratings (demand, competition 1 to 5) are the editors' reading of the same pages.

- Video editor: kumarijob.com (3 Sept 2026: fresher 15,000 to 30,000, mid 30,000 to 60,000, experienced 60,000 to 120,000+), necojobs.com.np (3 June 2026: 15,000 to 30,000,
  30,000 to 60,000, 60,000 to 120,000 or more; freelancers 30,000 to 200,000). Disagreeing pages: kumarijob.com (14 Jan 2026) prints entry 30,000 to 60,000 and senior 100,000+,
  worldsalaries.com prints an average of NPR 54,733 a month (lowest 26,708, highest 85,250). Band used: entry 15,000 to 30,000, senior 60,000 to 120,000.
- Nutritionist and dietitian: kumarijob.com (30 July 2026: entry 25,000 to 40,000, overall 30,000 to 70,000, government hospitals 35,000 to 70,000, private hospitals 30,000 to 80,000+).
  An older undated listing on collegesnepal.com prints 16,000 to 27,000, which is below the 2026 guide and was not used. Band: entry 25,000 to 40,000, senior 60,000 to 80,000.
- Game developer: kumarijob.com (26 May 2026: entry 20,000 to 40,000, senior and lead from 80,000 and above 120,000, remote foreign studio work pays more).
  Glassdoor shows only three 3D animator submissions for Nepal (NPR 10,000 to 15,000 a month base), too few to use.
"""
CAREERS_NEW = [
    {'id': 'video-editor', 'name': 'Video editor and videographer', 'about': 'Cuts, colours and sounds video for YouTube channels, TV and news, ads, weddings, NGOs and brands, and often shoots it too. Many work as freelancers for clients abroad.',
     'demand': 4, 'competition': 4, 'trend': 'rising', 'abroad': 4, 'salary': {'entry': [15000, 30000], 'senior': [60000, 120000]},
     'skills': ['Premiere Pro or DaVinci Resolve', 'Motion graphics and colour', 'Storytelling and scripting', 'Camera and audio basics'], 'ladder': ['Intern or junior editor', 'Video editor', 'Senior editor or motion designer', 'Creative or video lead'],
     'employers': ['Production houses and media', 'Marketing and advertising agencies', 'YouTube and brand teams', 'Overseas freelance clients'], 'hours': 45},
    {'id': 'nutritionist', 'name': 'Nutritionist and dietitian', 'about': 'Plans diets for patients and communities in hospitals, clinics, NGOs, schools and fitness centres, from diabetes and kidney care to child nutrition programmes.',
     'demand': 3, 'competition': 2, 'trend': 'rising', 'abroad': 3, 'salary': {'entry': [25000, 40000], 'senior': [60000, 80000]},
     'skills': ['Medical nutrition therapy', 'Diet and growth assessment', 'Counselling', 'Community programme design'], 'ladder': ['Nutrition assistant', 'Nutritionist or dietitian', 'Senior or clinical dietitian', 'Nutrition programme manager'],
     'employers': ['Government and private hospitals', 'NGOs and INGOs', 'Wellness centres', 'Food and health companies'], 'hours': 40},
    {'id': 'game-developer', 'name': 'Game developer', 'about': 'Builds mobile, PC and web games with engines such as Unity, covering gameplay code, art pipelines and testing, often for outsourcing studios or foreign remote clients.',
     'demand': 3, 'competition': 3, 'trend': 'rising', 'abroad': 4, 'salary': {'entry': [20000, 40000], 'senior': [80000, 120000]},
     'skills': ['C# and Unity or Unreal', 'Game design basics', '2D and 3D asset pipelines', 'Version control and testing'], 'ladder': ['Junior game developer', 'Game developer', 'Senior or lead developer', 'Technical director or studio founder'],
     'employers': ['Local game and animation studios', 'Software outsourcing companies', 'Remote foreign studios', 'Own indie games'], 'hours': 42},
]
CAREER_LINKS = {
    'bjmc': ['video-editor'], 'bfd-design': ['video-editor'], 'freelance-digital': ['video-editor', 'game-developer'],
    'bph': ['nutritionist'], 'btech-food': ['nutritionist'],
    'bicte': ['game-developer'], 'bsc-csit': ['game-developer'], 'bca': ['game-developer'], 'bit': ['game-developer'],
}
