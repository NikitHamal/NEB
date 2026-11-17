// Contributor / publisher profile (the NEBians official account, moderators, authors): output and impact first.
const cRes = [
  { t: 'PDF', n: 'Social Studies and Human Values Education Class 10 Notes', m: '27.5 MB · 12 reads', sub: 'Class 10 · Official' },
  { t: 'PDF', k: 'q', n: 'Science and Technology Class 10 Complete Notes', m: '31.2 MB · 3.1k reads', sub: 'Class 10 · Official' },
  { t: 'PDF', k: 'b', n: 'Accountancy Class 12 Model Questions 2082', m: '4.4 MB · 1.8k reads', sub: 'Class 12 · Official' },
  { t: 'PDF', k: 'n', n: 'English Class 11 Complete Guide', m: '9.0 MB · 2.2k reads', sub: 'Class 11 · Official' }
];
const cBooks = [['Physics 12', 'Official textbook', 'p'], ['Chemistry 12', 'Official textbook', 't'], ['Mathematics 11', 'Official textbook', 'y'], ['English 11', 'Reference guide', 'g']];
const cPosts = [
  { l: 'N', tone: 4, sh: 'burst', by: 'NEBians', time: '1d ago', tag: '#General', h: 'Welcome to NEBians', b: 'We are glad to have you here. Connect, share ideas, learn new things, explore opportunities and grow together.', up: 4, c: 1, pin: true },
  { l: 'N', tone: 4, sh: 'burst', by: 'NEBians', time: '1w ago', tag: '#Update', h: 'Class 10 notes are now chapter wise', b: 'Every subject has chapters, question banks and model papers in one place. Open any subject from the Library.', up: 211, c: 29 }
];
const col = [['SEE Class 10 Pack', '18 resources', 'pc'], ['Class 12 Science', '26 resources', 'tc'], ['Past papers 2078 to 2082', '41 resources', 'gc'], ['Entrance prep', '15 resources', 'yc']];
PROFILES.contributor = {
  label: 'Contributor', sh: 'burst', tone: 1, cv: 'yc', letter: 'N', name: 'NEBians', handle: '@nebians', v: true,
  role: ['Official', 'shield'], headline: 'Notes, books, question banks and model papers for every NEB subject. Free for every learner.',
  meta: [['globe', '<a>nebians.com</a>'], ['cal', 'Since Jan 2025'], ['pin', 'Nepal']],
  nums: [['18.4k', 'Followers'], ['148', 'Resources'], ['94k', 'Reads']],
  strip: ['Publishes', [['Class 9 to 12', 'p'], ['Notes', ''], ['Question banks', ''], ['Model papers', ''], ['Books', '']]],
  tabs: self => [['overview', 'Overview', 'grid'], ['resources', 'Resources', 'doc', 148], ['books', 'Books', 'book', 12], ['collections', 'Collections', 'route', 4], ['posts', 'Posts', 'post', 61], ['impact', 'Impact', 'trend'], ...(self ? [['drafts', 'Drafts', 'edit', 3, 1]] : [])],
  panes: {
    overview: self => [
      stats([['148', 'Resources'], ['94k', 'Total reads', '+8.2k this month'], ['12', 'Books'], ['61', 'Posts']]),
      mod('Collections', 'route', 'collections', `<div class="hs">${col.map(c => `<div class="card ${c[2]}" style="flex:none;width:158px;display:grid;gap:26px"><div>${ic('route')}</div><div><b style="font-size:.84rem;display:block">${c[0]}</b><small style="font-size:.7rem;opacity:.75">${c[1]}</small></div></div>`).join('')}</div>`),
      mod('Latest resources', 'doc', 'resources', cRes.slice(0, 3).map(res).join('')),
      mod('Book shelf', 'book', 'books', `<div class="hs">${cBooks.map(b => `<div style="flex:none;width:104px;display:grid;gap:8px"><div class="card ${{ p: 'pc', t: 'tc', y: 'yc', g: 'gc' }[b[2]]}" style="height:136px;border-radius:14px 22px 22px 14px;display:grid;align-content:space-between;padding:12px">${ic('book')}<b style="font-size:.8rem;line-height:1.25">${b[0]}</b></div><small style="font-size:.68rem;color:var(--onv)">${b[1]}</small></div>`).join('')}</div>`),
      mod('Pinned post', 'post', 'posts', post(cPosts[0])),
      mod('Reads, last 8 weeks', 'trend', 'impact', card(bars([40, 44, 52, 48, 66, 74, 70, 92], 7)))
    ],
    resources: () => [`<div class="strip" style="margin:0">${[['All 148', 'p'], ['Notes'], ['Past papers'], ['Question banks'], ['Model papers']].map(c => chip(c[0], c[1] || '')).join('')}</div>`, ...cRes.map(res)],
    books: () => [`<div class="grid4">${cBooks.concat([['Biology 12', 'Official textbook', 'g'], ['Computer 11', 'Official textbook', 'p']]).map(b => `<div style="display:grid;gap:8px"><div class="card ${{ p: 'pc', t: 'tc', y: 'yc', g: 'gc' }[b[2]]}" style="height:170px;border-radius:16px 26px 26px 16px;display:grid;align-content:space-between">${ic('book')}<b style="font-size:.88rem;line-height:1.25">${b[0]}</b></div><div class="row"><small class="tx">${b[1]}</small><button class="read t" style="height:28px;padding:0 10px">Read</button></div></div>`).join('')}</div>`],
    collections: () => col.map(c => card(`<div class="row"><div class="tx"><b style="font-size:.95rem">${c[0]}</b><small style="opacity:.75">${c[1]} · Updated this week</small></div>${ic('chev')}</div>`, c[2])),
    posts: () => cPosts.map(post),
    impact: () => [
      stats([['94k', 'Reads, all time'], ['8.2k', 'This month', '+14%'], ['3.4k', 'Saves'], ['612', 'Comments']]),
      mod('Reads by week', 'trend', 0, card(bars([40, 44, 52, 48, 66, 74, 70, 92], 7) + `<div class="bl">${['1', '2', '3', '4', '5', '6', '7', '8'].map(w => `<span>${w}</span>`).join('')}</div>`)),
      mod('Top resource', 'star', 0, res(cRes[1])),
      mod('Recognition', 'award', 0, `<div class="strip" style="margin:0 -16px;padding:0 16px">${[['Verified publisher', 'p', 'verified'], ['100 resources', 'y', 'doc'], ['Community pick', 'g', 'heart']].map(a => chip(a[0], a[1], a[2])).join('')}</div>`)
    ],
    drafts: () => [locked('Only you and moderators see Drafts.'), res({ t: 'PDF', n: 'Economics Class 12 revision notes (draft)', m: 'Draft · Edited 2h ago' }), res({ t: 'NOTE', k: 'n', n: 'Nepali Class 9 unit 5 summary (draft)', m: 'Draft · Edited yesterday' })]
  }
};
