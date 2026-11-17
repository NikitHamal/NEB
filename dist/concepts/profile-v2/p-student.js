// Student profile: study identity first. Every module on Overview has its own tab behind "See all".
const sPosts = [
  { l: 'A', tone: 2, by: 'Anisha Karki', time: '2d ago', tag: '#Physics', h: 'Why does the induced EMF flip sign in Lenz law?', b: 'I get the magnitude from Faraday but the minus sign never clicks. Is it just conservation of energy, or is there a cleaner way to see it?', up: 24, c: 9, solved: true, pin: true },
  { l: 'A', tone: 2, by: 'Anisha Karki', time: '5d ago', tag: '#Study', h: 'My 6 week plan for the Class 12 board exams', b: 'Sharing the timetable that worked for me: two subjects a day, past papers on Saturday, one rest block. Happy to swap notes.', up: 61, c: 18 },
  { l: 'A', tone: 2, by: 'Anisha Karki', time: '2w ago', tag: '#Chemistry', h: 'Organic reactions cheat sheet request', b: 'Does anyone have a one page map of named reactions for Class 12? Willing to trade my Physics numericals.', up: 12, c: 7 }
];
const sRes = [
  { t: 'PDF', n: 'Physics Class 12 Numericals, Chapters 1 to 8', m: '2.1 MB · 340 reads · Approved', sub: 'Physics · Class 12' },
  { t: 'PDF', k: 'q', n: 'Chemistry Model Question 2081 with solutions', m: '1.4 MB · 212 reads · Approved', sub: 'Chemistry · Class 12' },
  { t: 'NOTE', k: 'n', n: 'Calculus quick revision: limits to integrals', m: 'Note · 96 reads · Approved', sub: 'Mathematics · Class 12' },
  { t: 'PDF', k: 'b', n: 'English Grammar workbook, unit tests', m: '3.0 MB · 58 reads · Pending', sub: 'English · Class 12' }
];
const sReplies = [
  { in: 'Integration by parts, when to pick u?', q: 'Is there any rule beyond LIATE? Sometimes it fails for me.', b: 'LIATE is a heuristic. Pick u as the part that gets simpler after differentiating, and check that dv integrates cleanly. If the integral loops, solve algebraically for it.', up: 38, tag: 'Answer', time: '1d ago' },
  { in: 'Heat and temperature difference', q: 'Can two bodies have the same heat but a different temperature?', b: 'Yes. Heat depends on mass and specific heat as well. Think of a bathtub and a cup of water at the same temperature.', up: 21, tag: 'Helpful', tc: 'p', time: '4d ago' }
];
PROFILES.student = {
  label: 'Student', sh: 'cookie', tone: 1, cv: 'tc', letter: 'A', name: 'Anisha Karki', handle: '@anisha.k', v: false,
  role: ['Student', 'cap'], headline: 'Class 12 Science. Physics numericals, calm study plans and past papers.',
  meta: [['school', '<a>Vidya Bhawan Secondary School</a>'], ['pin', 'Kathmandu'], ['cal', 'Joined Aug 2025']],
  nums: [['318', 'Followers', 'followers'], ['142', 'Following'], ['412', 'Helpful votes']],
  strip: ['Open to', [['Study partner', 'p', 'users'], ['Swapping notes', 'g', 'book'], ['Finding a mentor', '', 'bulb']]],
  tabs: self => [['overview', 'Overview', 'grid'], ['posts', 'Posts', 'post', 48], ['resources', 'Resources', 'doc', 12], ['replies', 'Replies', 'reply', 133], ['portfolio', 'Portfolio', 'brief', 9], ['progress', 'Progress', 'trend'], ...(self ? [['saved', 'Saved', 'bm', 31, 1]] : [])],
  panes: {
    overview: self => [
      self && strength(66, [['Profile photo', 1], ['Class and school', 1], ['Open to', 1], ['First resource', 1], ['Two portfolio entries', 0, 'portfolio'], ['Skills', 0, 'portfolio']]),
      stats([['48', 'Posts', '+3 this week'], ['133', 'Replies'], ['412', 'Helpful votes', '+36 this week'], ['12', 'Resources']]),
      mod('Studying now', 'trend', 'progress', card(`<div class="list">${[['Physics', 72, 'Ch 9 of 13'], ['Chemistry', 58, 'Ch 7 of 12'], ['Mathematics', 40, 'Ch 5 of 12']].map(([s, p, c]) => `<div class="row"><div class="tx"><b>${s}</b><small>${c}</small><div style="margin-top:8px">${bar(p)}</div></div><b>${p}%</b></div>`).join('')}</div>`)),
      mod('Pinned post', 'post', 'posts', post(sPosts[0])),
      mod('Latest resources', 'doc', 'resources', `<div class="hs">${sRes.slice(0, 3).map(resCard).join('')}</div>`),
      mod('Achievements', 'award', 'progress', `<div class="strip" style="margin:0 -16px;padding:0 16px">${[['Top replier', 'y', 'star'], ['30 day streak', 'p', 'flame'], ['First upload', 'g', 'doc'], ['Helpful x400', 't', 'heart']].map(a => chip(a[0], a[1], a[2])).join('')}</div>`),
      mod('Education', 'cap', 'portfolio', card(tl([{ y: '2024 to present', t: 'Class 12 Science', s: 'Vidya Bhawan Secondary School', now: 1 }, { y: '2022 to 2024', t: 'SEE, GPA 3.92', s: 'Shree Janata Secondary School' }]))),
      mod('Skills', 'bulb', 'portfolio', `<div class="strip" style="margin:0 -16px;padding:0 16px;flex-wrap:wrap">${['Problem solving', 'Python basics', 'Public speaking', 'Note taking'].map(s => chip(s)).join('')}</div>`)
    ],
    posts: () => [`<div class="strip" style="margin:0">${[['All', 'p'], ['Questions'], ['Discussions'], ['Polls']].map(c => chip(c[0], c[1] || '')).join('')}</div>`, ...sPosts.map(post)],
    resources: self => [`<div class="strip" style="margin:0">${[['All 12', 'p'], ['Notes'], ['Past papers'], ['Question banks']].map(c => chip(c[0], c[1] || '')).join('')}</div>`, ...sRes.map(res), self && locked('Pending items are only visible to you until approved.')],
    replies: () => [stats([['133', 'Replies'], ['37', 'Marked answer']], 3 - 1), ...sReplies.map(reply)],
    portfolio: self => [
      mod('Education', 'cap', 0, card(tl([{ y: '2024 to present', t: 'Class 12 Science', s: 'Vidya Bhawan Secondary School', now: 1 }, { y: '2022 to 2024', t: 'SEE, GPA 3.92', s: 'Shree Janata Secondary School' }]))),
      mod('Projects', 'bulb', 0, `<div class="grid4">${[['Pendulum timer', 'Arduino, Physics Fair 2081'], ['Study planner', 'Static site, 120 users']].map(p => card(`<b style="font-size:.84rem">${p[0]}</b><small class="muted" style="display:block;margin-top:4px;font-size:.72rem">${p[1]}</small>`)).join('')}</div>`),
      mod('Certificates', 'award', 0, card(`<div class="list">${[['Python for beginners', 'NEBians Pathways · 2081'], ['Regional Science Quiz', 'Second place · 2080']].map(c => `<div class="row"><div class="ft b">${ic('award', 's')}</div><div class="tx"><b>${c[0]}</b><small>${c[1]}</small></div></div>`).join('')}</div>`)),
      mod('Volunteering', 'heart', 0, card(`<div class="row"><div class="ft n">${ic('heart', 's')}</div><div class="tx"><b>Weekend tutor</b><small>Ward 10 learning centre · 2081 to present</small></div></div>`)),
      self && `<button class="btn t" style="justify-content:center;height:46px">${ic('plus', 's')}Add portfolio entry</button>`
    ],
    progress: () => [
      card(`<div class="row"><div class="tx"><b style="font-size:1rem">12 day streak</b><small>Longest 31 days. One lesson keeps it alive.</small></div>${ic('flame', 'fill')}</div><div class="row" style="margin-top:14px;justify-content:space-between">${'MTWTFSS'.split('').map((d, i) => `<div style="text-align:center;font-size:.66rem"><div style="width:30px;height:30px;margin-bottom:4px;display:grid;place-items:center;background:${i < 5 ? 'var(--onyc)' : 'transparent'};color:var(--yc);border:${i < 5 ? 0 : '2px solid currentColor'};border-radius:50%;opacity:${i < 5 ? 1 : .5}">${i < 5 ? ic('check', 'xs') : ''}</div>${d}</div>`).join('')}</div>`, 'yc'),
      mod('Lessons per week', 'trend', 0, card(bars([30, 45, 38, 60, 52, 78, 90, 70], 6) + `<div class="bl">${['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8'].map(w => `<span>${w}</span>`).join('')}</div>`)),
      mod('Level 7', 'star', 0, card(`<div class="row"><div class="tx"><b>1,240 of 1,500 points</b><small>Next level unlocks custom study themes.</small></div></div><div style="margin-top:10px">${bar(83)}</div>`))
    ],
    saved: () => [locked('Only you can see Saved.'), post(sPosts[1]), res(sRes[1])]
  }
};
