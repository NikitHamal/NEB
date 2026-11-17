/* Every tab, for every profile type. A tab is a function of the profile; Overview only summarises and links. */
(function () {
  var U = window.U, N = window.NebArt, T = window.TABS = {};
  var who = function (P) { return { name: P.name, letter: P.letter, shape: P.shape, tone: P.tone, verified: P.verified }; };
  var posts = function (P) { return [P.pinned].concat(P.posts).map(function (p) { return U.post(p, who(P)); }).join(''); };
  var rail = function (P, n) { return '<div class="hs">' + P.resources.slice(0, n || 4).map(U.resource).join('') + '</div>'; };
  var sec = function (h, b) { return '<section>' + h + b + '</section>'; };
  var pinned = function (P) { return '<section>' + U.head('Pinned', null, 'posts') + U.post(P.pinned, who(P)) + '</section>'; };
  var lockTag = '<div class="lock">' + U.ms('lock', 'xs') + 'Only you can see this</div>';

  function strength(P) {
    if (!S.self) return '';
    var miss = P.id === 'student' ? ['Add a project to your portfolio', 'portfolio', 'work'] : P.id === 'teacher' ? ['Add a contact number', 'overview', 'call'] : P.id === 'institution' ? ['Upload 4 more campus photos', 'gallery', 'photo_library'] : ['Pin a collection', 'collections', 'collections_bookmark'];
    return '<section class="card str"><div class="srow"><b style="font-size:.94rem">Profile strength</b><b style="color:var(--p)">82%</b></div><div class="bar2"><i style="width:82%"></i></div>' +
      '<button class="link" data-act="tab" data-tab="' + miss[1] + '">' + U.ms(miss[2]) + '<div class="grow" style="flex:1"><b>' + miss[0] + '</b><small>Gets you to 90%</small></div>' + U.ms('chevron_right') + '</button></section>';
  }
  function stickers(P, rows) {
    return '<div class="stickers">' + P.achievements.slice(0, rows || 6).map(function (a, i) { return '<div class="stk">' + U.art('sticker', 300 + i * 13 + P.name.length, { glyph: a[0], palette: N.palettes[(i * 3 + P.name.length) % 12] }) + a[1] + '</div>'; }).join('') + '</div>';
  }
  function rows(list, fn) { return '<div class="list">' + list.map(fn).join('') + '</div>'; }

  T.overview = function (P) {
    var o = strength(P) + U.glance(P.glance), call = P.contact ? U.call(P.contact, P) : '';
    if (P.id === 'student') return o + U.studying(P.studying) + U.openTo(P.openTo) + pinned(P) +
      sec(U.head('Resources', P.resources.length, 'resources'), rail(P)) + sec(U.head('Achievements', P.achievements.length), stickers(P)) +
      sec(U.head('Portfolio', P.portfolio.length, 'portfolio'), rows(P.portfolio, function (r) { return U.row(r[0], r[3], r[1], r[2]); })) +
      sec(U.head('Skills'), '<div style="display:flex;gap:6px;flex-wrap:wrap">' + P.skills.map(function (s) { return U.chip(s); }).join('') + '</div>');
    if (P.id === 'teacher') return o + call + sec(U.head('Teaches', P.teaches.length, 'teaches'), rows(P.teaches.slice(0, 3), function (r) { return U.row(r[0], r[3], r[1], r[2], U.ms('chevron_right')); })) + U.openTo(P.openTo) + pinned(P) +
      sec(U.head('Most read', P.resources.length, 'resources'), rail(P)) + sec(U.head('Top answer', null, 'answers'), '<div class="card"><div style="display:flex;justify-content:space-between;gap:8px;margin-bottom:8px"><b style="font-size:.88rem">' + P.answers[0][0] + '</b>' + U.chip('Accepted', 'g', 'check') + '</div><div class="pb">' + P.answers[0][1] + '</div></div>') +
      sec(U.head('Current school', null, 'schools'), rows(P.schools.slice(0, 1), function (r) { return U.row(r[2], r[3], r[0], r[1]); })) + sec(U.head('Achievements'), stickers(P));
    if (P.id === 'institution') return '<div class="card" style="background:var(--gc);color:var(--ongc);border-color:transparent;display:flex;gap:12px;align-items:center">' + U.glyph('how_to_reg', 'c2') + '<div style="flex:1"><b style="font-size:.9rem">Admissions 2083 are open</b><div style="font-size:.74rem;opacity:.85">Closes on 15 Baisakh</div></div><button class="btn sm f" data-act="open" data-what="Admission form">Apply</button></div>' +
      o + call + U.openTo(P.openTo) + pinned(P) + sec(U.head('Programs', P.programs.length, 'programs'), T.programs(P, 2)) + sec(U.head('Notices', P.notices.length, 'notices'), T.notices(P, 2)) +
      sec(U.head('Teachers', P.teachers.length, 'teachers'), '<div class="hs">' + P.teachers.map(function (t) { return '<div class="tile" style="width:128px;text-align:center">' + U.av(t[2], t[3], t[4], 'lg') + '<b style="display:block;font-size:.78rem;margin-top:8px">' + t[0] + '</b><small style="font-size:.68rem;color:var(--onv)">' + t[1] + '</small></div>'; }).join('') + '</div>') +
      sec(U.head('Campus', 48, 'gallery'), T.gallery(P, 3)) + sec(U.head('Facilities'), '<div style="display:flex;gap:6px;flex-wrap:wrap">' + P.facilities.map(function (f) { return U.chip(f[1], '', f[0]); }).join('') + '</div>') + sec(U.head('Resources', P.resources.length, 'resources'), rail(P));
    return o + U.openTo(P.openTo) + pinned(P) + sec(U.head('Book shelf', P.books.length, 'books'), T.books(P, 3)) + sec(U.head('Latest resources', P.resources.length, 'resources'), rail(P)) +
      sec(U.head('Collections', P.collections.length, 'collections'), T.collections(P, 2)) + sec(U.head('Reads, last 12 weeks', null, 'impact'), T.chart(P));
  };
  T.posts = posts;
  T.resources = function (P) { return '<div class="rgrid">' + P.resources.concat(P.resources.slice(0, 2).map(function (r, i) { var c = Object.assign({}, r); c.seed += 100; c.title = c.title + ', part 2'; return c; })).map(U.resource).join('') + '</div>'; };
  T.replies = function (P) { return rows(P.replies, function (r) { return '<div class="card" style="display:grid;gap:8px"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:.86rem;line-height:1.35">' + r[0] + '</b>' + U.chip(r[2], 'g', 'check') + '</div><div class="pb">' + r[1] + '</div></div>'; }); };
  T.answers = function (P) { return rows(P.answers, function (r) { return '<div class="card" style="display:grid;gap:8px"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:.86rem;line-height:1.35">' + r[0] + '</b>' + U.chip(r[2], 'g', 'check') + '</div><div class="pb">' + r[1] + '</div></div>'; }); };
  T.portfolio = function (P) { return rows(P.portfolio, function (r) { return U.row(r[0], r[3], r[1], r[2], U.ms('open_in_new', 's')); }); };
  T.progress = function (P) { return U.studying(P.studying) + sec(U.head('Subjects'), rows([['Physics', 'bolt', 'c1', 'Chapter 7 of 12'], ['Chemistry', 'science', 'c2', 'Chapter 5 of 14'], ['Mathematics', 'functions', 'c3', 'Chapter 9 of 11']], function (r) { return U.row(r[1], r[2], r[0], r[3], U.ms('chevron_right')); })); };
  T.saved = function (P) { return lockTag + '<div class="rgrid">' + P.resources.slice(0, 4).map(U.resource).join('') + '</div>'; };
  T.teaches = function (P) { return rows(P.teaches, function (r) { return U.row(r[0], r[3], r[1], r[2], U.ms('chevron_right')); }); };
  T.schools = function (P) { return rows(P.schools, function (r) { return U.row(r[2], r[3], r[0], r[1]); }); };
  T.earnings = function (P) { return lockTag + U.glance([{ i: 'payments', n: 'Rs 18k', l: 'This month', c: 2 }, { i: 'shopping_bag', n: '64', l: 'Sales', c: 1 }, { i: 'star', n: '4.9', l: 'Rating', c: 3 }]); };
  T.studio = function (P) { return lockTag + rows([['Drafts', 'draft', 'c6', '3 unfinished'], ['Scheduled', 'schedule_send', 'c1', '1 for Sunday'], ['Insights', 'insights', 'c3', 'Reads up 18 percent']], function (r) { return U.row(r[1], r[2], r[0], r[3], U.ms('chevron_right')); }); };
  T.notices = function (P, n) { return rows(P.notices.slice(0, n || 9), function (r) { return U.row(r[0], 'c' + (r[4] === 'g' ? 2 : r[4] === 'y' ? 3 : 4), r[1], r[2], U.chip(r[3], r[4])); }); };
  T.programs = function (P, n) { return rows(P.programs.slice(0, n || 9), function (r) { return U.row(r[3], r[4], r[0], r[1] + '. ' + r[2], U.ms('chevron_right')); }); };
  T.teachers = function (P) { return rows(P.teachers, function (t) { return '<div class="row">' + U.av(t[2], t[3], t[4], 'md') + '<div class="grow"><b>' + t[0] + '</b><small>' + t[1] + ' teacher</small></div><div class="end">' + U.ms('chevron_right') + '</div></div>'; }); };
  T.gallery = function (P, n) { var a = [], i; for (i = 0; i < (n || 7); i++) a.push('<div>' + U.art(i % 2 ? 'post' : 'school', 60 + i * 11, { palette: ['azure', 'teal', 'amber', 'sky', 'mint', 'coral', 'moss'][i % 7] }) + '</div>'); return '<div class="mosaic">' + a.join('') + '</div>'; };
  T.books = function (P, n) { return '<div class="books">' + P.books.slice(0, n || 9).map(function (b, i) { return '<div class="bk">' + U.art('book', 900 + i * 5, { subject: b[1], motif: 'book' }) + '<b>' + b[0] + '</b><small>' + b[2] + '</small></div>'; }).join('') + '</div>'; };
  T.collections = function (P, n) { return '<div class="cols">' + P.collections.slice(0, n || 9).map(function (c, i) { return '<div class="col"><div class="ca">' + U.art('tile', 2100 + i * 9, { subject: c[1], motif: 'none' }) + '</div><div><b>' + c[0] + '</b><small>' + c[2] + ' resources</small></div></div>'; }).join('') + '</div>'; };
  T.chart = function (P) { var m = Math.max.apply(null, P.impact); return '<div class="card"><div class="chart">' + P.impact.map(function (v) { return '<i style="height:' + Math.round(v / m * 100) + '%"></i>'; }).join('') + '</div></div>'; };
  T.impact = function (P) { return U.glance(P.glance) + sec(U.head('Reads, last 12 weeks'), T.chart(P)) + sec(U.head('Top resource'), '<div class="rgrid">' + U.resource(P.resources[0]) + '</div>'); };
})();
