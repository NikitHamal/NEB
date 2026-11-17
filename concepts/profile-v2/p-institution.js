// Institution profile: a school page. Admissions, programs, people and the way to reach it are tabs, not About rows.
const iNotices = [
  { l: 'VB', tone: 5, sh: 'squircle', by: 'Vidya Bhawan', time: '1d ago', tag: '#Admission', h: 'Class 11 admissions open for 2083, Science and Management', b: 'Forms are available at the front desk and online until Baisakh 15. Entrance test on Baisakh 18. Scholarships for the top ten scorers in SEE.', up: 212, c: 40, pin: true },
  { l: 'VB', tone: 5, sh: 'squircle', by: 'Vidya Bhawan', time: '4d ago', tag: '#Notice', h: 'Pre-board exam routine published for Class 12', b: 'Exams begin on Falgun 24. Admit cards will be distributed from the class teachers on Falgun 20.', up: 88, c: 12 }
];
const iProg = [
  ['Science, +2', 'NEB', '64 seats', 'Physics, Chemistry, Maths or Biology, English, Nepali', 'Admissions open', 'g'],
  ['Management, +2', 'NEB', '48 seats', 'Accountancy, Economics, Business Studies, Marketing', 'Admissions open', 'g'],
  ['Secondary, 9 to 10', 'SEE', '96 seats', 'All compulsory and optional subjects', 'Waitlist', 'y'],
  ['Basic, 1 to 8', 'CDC', 'Full', 'Montessori style activity classes', 'Closed', 'r']
];
const iRes = [
  { t: 'PDF', n: 'Class 10 Science, school pre-board paper 2081', m: '1.8 MB · 1.9k reads', sub: 'Shared by the school' },
  { t: 'PDF', k: 'q', n: 'Class 12 Accountancy, unit tests with answer key', m: '2.2 MB · 740 reads', sub: 'Shared by the school' },
  { t: 'PDF', k: 'b', n: 'Annual academic calendar 2082', m: '0.6 MB · 3.4k reads', sub: 'Shared by the school' }
];
const gal = (n, c) => `<div class="${c}" style="--bg:var(--${['pc', 'tc', 'gc', 'yc', 'sc', 'pc'][n % 6]})">${ic('img')}<span>${['Science fair', 'Annual day', 'Library', 'Football', 'Assembly', 'Lab'][n % 6]}</span></div>`;
PROFILES.institution = {
  label: 'Institution', sh: 'squircle', tone: 3, cv: 'gc', letter: 'VB', name: 'Vidya Bhawan Secondary School', handle: '@vidyabhawan', v: true, big: true,
  role: ['School', 'school'], headline: 'Secondary and +2 in Science and Management. Learning with discipline since 2041 BS.',
  meta: [['pin', 'Baneshwor, Kathmandu'], ['shield', 'NEB affiliated'], ['globe', '<a>vidyabhawan.edu.np</a>']],
  nums: [['2.8k', 'Followers'], ['24', 'Teachers'], ['1,240', 'Students']],
  strip: ['Now', [['Admissions open', 'g', 'check'], ['Entrance test Baisakh 18', 'y', 'cal'], ['Scholarships', 'p', 'award']]],
  tabs: self => [['overview', 'Overview', 'grid'], ['notices', 'Notices', 'bell', 18], ['programs', 'Programs', 'cap', 4], ['teachers', 'Teachers', 'users', 24], ['gallery', 'Gallery', 'img', 32], ['resources', 'Resources', 'doc', 41], ['contact', 'Contact', 'pin'], ...(self ? [['admin', 'Manage', 'shield', 0, 1]] : [])],
  panes: {
    overview: self => [
      card(`<div class="row"><div class="tx"><b style="font-size:1rem">Admissions open for Class 11</b><small class="muted">Science and Management, 2083. Apply by Baisakh 15.</small></div></div><div style="margin-top:12px;display:flex;gap:8px"><button class="btn f" data-go="contact">${ic('phone', 's')}Enquire</button><button class="btn t" data-go="programs">See programs</button></div>`, 'tc'),
      stats([['1,240', 'Students'], ['24', 'Teachers'], ['36', 'Classrooms'], ['2041', 'Established BS']]),
      mod('About the school', 'school', 0, card(`<p>Vidya Bhawan is a co-educational school in Baneshwor with its own science wing, a 12,000 book library and a record of high board results. Our teachers publish free notes on NEBians every month.</p><div style="margin-top:8px"><button style="font-size:.76rem;font-weight:600;color:var(--p)">See more</button></div>`)),
      mod('Programs', 'cap', 'programs', `<div class="strip" style="margin:0 -16px;padding:0 16px">${iProg.slice(0, 3).map(p => chip(p[0], p[5], 'cap')).join('')}</div>`),
      mod('Latest notice', 'bell', 'notices', post(iNotices[1])),
      mod('Campus', 'img', 'gallery', `<div class="mos">${gal(0, 'a')}${gal(1, 'b')}${gal(2, 'c')}${gal(3, 'c')}${gal(4, 'c')}</div>`),
      mod('Teachers on NEBians', 'users', 'teachers', `<div class="hs">${[['R', 'Ramesh A.', 'Physics', 1, 'sunny'], ['S', 'Sarita P.', 'Maths', 2, 'cookie'], ['B', 'Bikash T.', 'Chemistry', 3, 'burst'], ['M', 'Mina G.', 'English', 4, 'clover']].map(t => `<div style="flex:none;width:92px;display:grid;justify-items:center;gap:6px;text-align:center">${avatar(t[0], t[3], 'lg', t[4])}<b style="font-size:.76rem">${t[1]}</b><small style="font-size:.68rem;color:var(--onv)">${t[2]}</small></div>`).join('')}</div>`),
      mod('Facilities', 'shield', 0, `<div class="strip" style="margin:0 -16px;padding:0 16px;flex-wrap:wrap">${['Science lab', 'Computer lab', 'Library', 'Playground', 'School bus', 'Canteen', 'Wi-Fi'].map(f => chip(f)).join('')}</div>`)
    ],
    notices: () => iNotices.map(post),
    programs: () => iProg.map(p => card(`<div class="row"><div class="tx"><b style="font-size:.95rem">${p[0]}</b><small>${p[1]} · ${p[2]}</small></div>${chip(p[4], p[5] + ' sm')}</div><p class="muted" style="margin-top:8px;font-size:.78rem">${p[3]}</p>${p[5] === 'g' ? `<div style="margin-top:12px"><button class="btn t" data-go="contact">Ask admissions</button></div>` : ''}`)),
    teachers: () => [`<div class="strip" style="margin:0">${[['All 24', 'p'], ['Science'], ['Maths'], ['Languages'], ['Management']].map(c => chip(c[0], c[1] || '')).join('')}</div>`, card(`<div class="list">${[['R', 'Ramesh Adhikari', 'Physics, Maths · Head of Science', 1, 'sunny', 1], ['S', 'Sarita Pandey', 'Mathematics · Class 10 lead', 2, 'cookie', 0], ['B', 'Bikash Thapa', 'Chemistry, Biology', 3, 'burst', 0], ['M', 'Mina Gurung', 'English · Literature', 4, 'clover', 0]].map(t => person({ l: t[0], n: t[1], s: t[2], tone: t[3], sh: t[4], v: t[5] })).join('')}</div>`)],
    gallery: () => [`<div class="strip" style="margin:0">${[['All 32', 'p'], ['Events'], ['Labs'], ['Sports']].map(c => chip(c[0], c[1] || '')).join('')}</div>`, `<div class="mos">${[0, 1, 2, 3, 4, 5].map((n, i) => gal(n, ['a', 'b', 'c', 'c', 'd', 'e'][i])).join('')}</div>`],
    resources: () => [...iRes.map(res), locked('Only members of the school can post here.')],
    contact: () => [
      `<div class="map"><i style="left:-10%;top:30%;width:130%;height:12px;transform:rotate(-8deg)"></i><i style="left:20%;top:-10%;width:12px;height:130%;transform:rotate(12deg)"></i><i style="left:62%;top:-10%;width:10px;height:130%;transform:rotate(-6deg)"></i><i style="left:-5%;top:72%;width:110%;height:10px;transform:rotate(4deg)"></i><b></b></div>`,
      card(`<div class="list">${[['pin', 'Baneshwor, Kathmandu', 'Open in Maps'], ['phone', '01-4781234', 'Call front desk'], ['mail', 'info@vidyabhawan.edu.np', 'Send email'], ['globe', 'vidyabhawan.edu.np', 'Website'], ['clock', 'Sun to Fri, 8:00 to 16:00', 'Admissions desk, until 15:00']].map(r => `<div class="row"><div class="ft b" style="width:38px;height:38px;border-radius:12px">${ic(r[0], 's')}</div><div class="tx"><b>${r[1]}</b><small>${r[2]}</small></div>${ic('chev', 's')}</div>`).join('')}</div>`),
      mod('Mentioned in', 'link', 0, card(`<small class="muted" style="font-size:.74rem">Facebook, YouTube and the NEB school directory.</small>`))
    ],
    admin: () => [locked('Only school admins see Manage.'), card(`<div class="row"><div class="tx"><b>Claimed and verified</b><small class="muted">Approved on 12 Magh by NEBians review. Manager: Sunita Basnet.</small></div>${ic('verified', 'fill')}</div>`, 'gc'), stats([['9.4k', 'Page views, 30 days', '+22%'], ['312', 'New followers'], ['86', 'Enquiries'], ['1.9k', 'Resource reads']]), card(`<div class="list">${[['edit', 'Edit page details'], ['users', 'Link teachers (3 requests)'], ['cap', 'Open or close admissions'], ['img', 'Manage gallery']].map(r => `<div class="row"><div class="ft b" style="width:38px;height:38px;border-radius:12px">${ic(r[0], 's')}</div><div class="tx"><b>${r[1]}</b></div>${ic('chev', 's')}</div>`).join('')}</div>`)
    ]
  }
};
