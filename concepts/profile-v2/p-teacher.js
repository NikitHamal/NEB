// Teacher profile: credibility first (what, where, how long), then proof (resources, answers).
const tRes = [
  { t: 'PDF', n: 'Physics Class 11 Mechanics: complete chapter notes', m: '4.8 MB · 1.2k reads', sub: 'Physics · Class 11' },
  { t: 'PDF', k: 'q', n: 'Mathematics Class 10 Question Bank with step solutions', m: '6.1 MB · 2.4k reads', sub: 'Mathematics · Class 10' },
  { t: 'PDF', k: 'b', n: 'Optional Maths SEE model papers 2081', m: '2.7 MB · 890 reads', sub: 'Optional Maths · Class 10' },
  { t: 'NOTE', k: 'n', n: 'Electrostatics: derivations in one page', m: 'Note · 640 reads', sub: 'Physics · Class 12' }
];
const tPosts = [
  { l: 'R', tone: 1, by: 'Ramesh Adhikari', time: '3d ago', tag: '#Teaching', h: 'Five ways to make numericals less scary', b: 'Start from units, draw the situation, write what is given and wanted, then pick the formula. Students who skip the sketch lose half the marks.', up: 142, c: 31, pin: true },
  { l: 'R', tone: 1, by: 'Ramesh Adhikari', time: '1w ago', tag: '#Exam', h: 'SEE 2082 Science: chapters that repeat every year', b: 'From the last ten papers, these seven chapters carry more than 60 percent of the marks.', up: 98, c: 22 }
];
const tAns = [
  { in: 'Why is the net force zero at terminal velocity?', q: 'If it is still moving, shouldn\u2019t a force act on it?', b: 'Motion does not need a net force, only a change in motion does. Drag grows with speed until it cancels weight, then acceleration is zero and the speed stays constant.', up: 74, tag: 'Answer', time: '2d ago' },
  { in: 'Quadratic formula derivation', q: 'Where does the discriminant come from?', b: 'Complete the square on ax\u00B2 + bx + c = 0. The leftover term under the root is b\u00B2 \u2212 4ac, and its sign tells you how many real roots exist.', up: 51, tag: 'Answer', time: '6d ago' }
];
const cell = (v) => `<span class="c ${v === 2 ? 'b' : v === 1 ? 'a' : ''}"></span>`;
PROFILES.teacher = {
  label: 'Teacher', sh: 'sunny', tone: 2, cv: 'pc', letter: 'R', name: 'Ramesh Adhikari', handle: '@ramesh.sir', v: true,
  role: ['Teacher', 'school'], headline: 'Physics and Mathematics teacher. Nine years of turning formulas into stories.',
  meta: [['school', '<a>Vidya Bhawan Secondary School</a>'], ['pin', 'Kathmandu'], ['clock', 'Teaching since 2074']],
  nums: [['4.2k', 'Followers'], ['64', 'Following'], ['214', 'Answers']],
  strip: ['Teaches', [['Physics', 'p'], ['Mathematics', 'p'], ['Optional Maths', 'p'], ['Secondary 9 to 10', ''], ['+2', '']]],
  tabs: self => [['overview', 'Overview', 'grid'], ['teaches', 'Teaches', 'book', 4], ['resources', 'Resources', 'doc', 36], ['posts', 'Posts', 'post', 21], ['answers', 'Answers', 'reply', 214], ['schools', 'Schools', 'school', 3], ...(self ? [['insights', 'Insights', 'trend', 0, 1]] : [])],
  panes: {
    overview: self => [
      self && card(`<div class="row"><div class="tx"><b>Your profile reached 1,240 people this week</b><small class="muted">Up 18 percent. Open Insights to see which resources brought them.</small></div></div><div style="margin-top:12px"><button class="btn f" data-go="insights">See insights</button></div>`, 'pc'),
      stats([['9', 'Years teaching'], ['214', 'Answers', '87 accepted'], ['36', 'Resources', '12k reads'], ['3', 'Schools']]),
      mod('Teaches', 'book', 'teaches', card(`<div class="strip" style="margin:0;flex-wrap:wrap">${['Physics', 'Mathematics', 'Optional Maths', 'Computer Science'].map(s => chip(s, 'p')).join('')}</div><div class="strip" style="margin:8px 0 0;flex-wrap:wrap">${['Basic 6 to 8', 'Secondary 9 to 10', '+2', 'Entrance coaching'].map(s => chip(s)).join('')}</div>`)),
      mod('Current school', 'school', 'schools', card(`<div class="row">${avatar('VB', 5, 'lg', 'squircle')}<div class="tx"><b>Vidya Bhawan Secondary School ${verified()}</b><small>Head of Science, since 2078. Kathmandu</small></div>${ic('chev', 's')}</div>`)),
      mod('Most read resources', 'doc', 'resources', `<div class="hs">${tRes.slice(0, 3).map(resCard).join('')}</div>`),
      mod('Top answers', 'reply', 'answers', reply(tAns[0])),
      mod('Pinned post', 'post', 'posts', post(tPosts[0])),
      mod('Open to', 'users', 0, `<div class="strip" style="margin:0 -16px;padding:0 16px">${[['Tutoring', 'g', 'check'], ['Mentoring juniors', 'p', 'users'], ['Project collab', '', 'bulb']].map(c => chip(c[0], c[1], c[2])).join('')}</div>`)
    ],
    teaches: () => [
      card(`<div class="mx"><div class="r"><span></span>${['Basic', 'Sec.', '+2', 'Entrance'].map(h => `<span class="h">${h}</span>`).join('')}</div>${[['Physics', [0, 2, 2, 1]], ['Mathematics', [1, 2, 2, 0]], ['Optional Maths', [0, 2, 1, 0]], ['Computer', [0, 1, 2, 0]]].map(([s, a]) => `<div class="r"><span>${s}</span>${a.map(cell).join('')}</div>`).join('')}</div><div class="row" style="margin-top:12px;font-size:.7rem"><span class="chip sm p">Teaches</span><span class="chip sm">Occasionally</span></div>`),
      mod('Coverage on NEBians', 'trend', 0, card(`<div class="list">${[['Physics', 86, '11 of 13 chapters · 14 resources'], ['Mathematics', 72, '9 of 12 chapters · 12 resources'], ['Optional Maths', 55, '6 of 11 chapters · 7 resources']].map(([s, p, c]) => `<div class="row"><div class="tx"><b>${s}</b><small>${c}</small><div style="margin-top:8px">${bar(p)}</div></div><b>${p}%</b></div>`).join('')}</div>`)),
      card(`<div class="row"><div class="tx"><b>Tutoring, evenings and weekends</b><small class="muted">Small groups for SEE and +2 Physics. Message to ask about seats.</small></div></div><div style="margin-top:12px;display:flex;gap:8px"><button class="btn f">${ic('chat', 's')}Message</button><button class="btn t">Share</button></div>`, 'gc')
    ],
    resources: () => [`<div class="strip" style="margin:0">${[['All 36', 'p'], ['Physics'], ['Mathematics'], ['Optional Maths']].map(c => chip(c[0], c[1] || '')).join('')}</div>`, ...tRes.map(res)],
    posts: () => tPosts.map(post),
    answers: () => [stats([['214', 'Answers'], ['87', 'Accepted'], ['1.2k', 'Helpful votes'], ['94%', 'Replied in 1 day']]), ...tAns.map(reply)],
    schools: () => [mod('Current', 'school', 0, card(tl([{ y: '2078 to present', t: 'Head of Science', s: 'Vidya Bhawan Secondary School, Kathmandu', now: 1 }]))), mod('Past schools', 'cap', 0, card(tl([{ y: '2074 to 2078', t: 'Physics teacher', s: 'Shree Mahendra Secondary School, Lalitpur' }, { y: '2072 to 2074', t: 'Teaching assistant', s: 'Kantipur Academy, Kathmandu' }])))],
    insights: () => [locked('Only you can see Insights.'), card(`<b style="font-size:.9rem">Profile views, last 8 weeks</b>${bars([34, 40, 38, 52, 61, 58, 80, 96], 7)}<div class="bl">${['1', '2', '3', '4', '5', '6', '7', '8'].map(w => `<span>${w}</span>`).join('')}</div>`), stats([['1,240', 'Views this week', '+18%'], ['86', 'New followers'], ['3.1k', 'Resource reads'], ['41', 'Messages']])]
  }
};
