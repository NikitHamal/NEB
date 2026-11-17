/* v3 in-app preview (profiles, resource cards, school page, posts, empty states, achievements, stories, collections, books) and V2 vs V3 compare. */
(function () {
  'use strict';
  var G = window.V3G, A = G.A, $ = function (s) { return document.querySelector(s); }, h = G.html;
  var PEOPLE = [
    ['Aarav Sharma', 'Student', 'Grade 12, Science', 'Physics', [['148', 'Notes'], ['32', 'Answers'], ['12', 'Day streak']]],
    ['Sita Rai', 'Teacher', 'Physics and Maths, 9 years', 'Mathematics', [['86', 'Resources'], ['410', 'Followers'], ['4.9', 'Rating']]],
    ['Himalayan Valley School', 'Institution', 'Lalitpur, Bagmati', 'Education', [['42', 'Teachers'], ['1.2k', 'Students'], ['18', 'Programs']]],
    ['Prabin Thapa', 'Contributor', 'Notes and solutions', 'Computer Science', [['230', 'Uploads'], ['9.4k', 'Downloads'], ['61', 'Helpful']]]
  ];
  function sec(icon, title, body) { return '<section class="panel"><h2><span class="ms">' + icon + '</span>' + title + '</h2>' + body + '</section>'; }
  function profile(p, i, n) {
    var inst = p[1] === 'Institution', cv = inst ? G.pick('school', null, n * 3 + i) : G.pick('cover', p[3], n + (i > 1 ? 4 : 0)), av = inst ? G.pick('avatar', null, 181 + n) : G.pick('avatar', null, i * 60 + n * 7 + 5);
    if (inst) av = G.pick('avatar', null, 181 + n);
    return '<div class="phone"><div class="pf-cover">' + G.svg(cv, G.st.salt) + '</div><div class="pf-body"><div class="pf-av">' + G.svg(av, G.st.salt) + '</div><h3>' + h(p[0]) + ' <span class="ms vf" style="font-size:18px;font-variation-settings:\'FILL\' 1">' + (i === 1 || inst ? 'verified' : 'new_releases') + '</span></h3><p>' + p[1] + ' - ' + h(p[2]) + '</p><div class="stats">' + p[4].map(function (s) { return '<div class="stat"><b>' + s[0] + '</b>' + s[1] + '</div>'; }).join('') + '</div><div class="tabs"><span>Overview</span><span>Resources</span><span>Posts</span><span>Gallery</span></div></div></div>';
  }
  function cards(kind, n, count, mark) {
    var o = '', i, it;
    for (i = 0; i < count; i++) { it = G.pick(kind, null, n * 5 + i * 9); o += '<div class="card"><span class="art">' + G.svg(it, G.st.salt) + '</span><span class="meta"><b>' + h(it.name.split(' / ')[1] || it.name) + '</b><small>' + h(it.subj) + (mark || ' - Grade 11 - 2.4 MB') + '</small></span></div>'; }
    return o;
  }
  function row(kind, n, count, cls, label) {
    var o = '', i, it; for (i = 0; i < count; i++) { it = G.pick(kind, null, n * 3 + i * (kind === 'sticker' ? 4 : 7)); o += cls === 'spot' ? '<div class="spot">' + G.svg(it, G.st.salt) + '<b>' + h(it.name.replace(/ \d$/, '')) + '</b><small>Nothing here yet</small></div>' : cls === 'medal' ? '<div class="medal">' + G.svg(it, G.st.salt) + h(it.name.replace(/ \d$/, '')) + '</div>' : '<div class="story">' + G.svg(it, G.st.salt) + '</div>'; }
    return '<div class="rowx">' + o + '</div>';
  }
  G.views.inapp = function () {
    var n = G.st.salt % 11, o = sec('person', 'Profiles: student, teacher, institution, contributor (frameless pictures, art-led covers)', '<div class="phones">' + PEOPLE.map(function (p, i) { return profile(p, i, n); }).join('') + '</div>');
    o += sec('description', 'Resource cards (thumbnail art per subject)', '<div class="grid" style="--min:260px">' + cards('thumb', n, 8) + '</div>');
    o += sec('edit_note', 'Post and share headers', '<div class="grid" style="--min:340px">' + cards('post', n, 3, ' - 5 min read') + '</div>');
    o += sec('collections_bookmark', 'Collection tiles and book covers', '<div class="rowx">' + [0, 1, 2, 3, 4, 5].map(function (i) { var it = G.pick('tile', null, n * 7 + i * 11); return '<div class="card" style="width:190px"><span class="art">' + G.svg(it, G.st.salt) + '</span><span class="meta"><b>' + h(it.subj) + '</b><small>12 resources</small></span></div>'; }).join('') + [0, 1, 2, 3, 4].map(function (i) { var it = G.pick('book', null, n * 5 + i * 13); return '<div class="card" style="width:150px"><span class="art">' + G.svg(it, G.st.salt) + '</span><span class="meta"><b>' + h(it.subj) + '</b><small>Textbook</small></span></div>'; }).join('') + '</div>');
    o += sec('inbox', 'Empty states', row('spot', n, 7, 'spot'));
    o += sec('workspace_premium', 'Achievements', row('sticker', n, 12, 'medal'));
    o += sec('smartphone', 'Onboarding stories (9:16)', row('story', n, 8, 'story'));
    o += sec('route', 'Pathways and labs', '<div class="grid" style="--min:340px">' + cards('pathway', n, 3, ' - 4 years') + cards('lab', n, 3, ' - Interactive') + '</div>');
    $('#stage').innerHTML = o;
  };
  G.views.compare = function () {
    var V = window.NebArtV2, subj = G.cmpSubj || 'Physics', subs = A.subjectNames;
    function v2(kind, s) { try { return V.make({ kind: kind, subject: s, seed: s + kind, mode: G.theme() }); } catch (e) { return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200"></svg>'; } }
    var rows = [['cover', 'Profile cover', 100], ['thumb', 'Resource thumbnail', 100], ['tile', 'Collection tile', 46], ['book', 'Book cover', 40], ['spot', 'Empty state', 70], ['sticker', 'Achievement', 40]];
    var o = '<div class="fbar"><select class="sel" id="cs" aria-label="Subject">' + subs.map(function (s) { return '<option' + (s === subj ? ' selected' : '') + '>' + h(s) + '</option>'; }).join('') + '</select><span class="count">Left: v2 (49 engines, 1,108 pieces). Right: v3 (' + Object.keys(A.engines).length + ' engines, ' + G.cat.length.toLocaleString() + ' pieces).</span></div>';
    o += rows.map(function (r) { var it3 = G.pick(r[0], r[0] === 'spot' || r[0] === 'sticker' ? null : subj, 0); return '<div style="max-width:' + (r[2] < 100 ? 520 : 1300) + 'px"><div class="cmp"><div><h4>v2 <span class="tag">' + r[1] + '</span></h4>' + v2(r[0], subj) + '</div><div><h4>v3 <span class="tag">' + r[1] + '</span></h4>' + G.svg(it3, G.st.salt) + '</div></div></div>'; }).join('');
    o += sec('verified', 'What v3 changes', '<div class="rowx" style="flex-wrap:wrap;gap:8px">' + ['OKLCH tonal ramps (perceptual, no purple)', 'Depth ramp: atmospheric perspective in every landscape', 'Nepal-grounded: Himalaya, terraces, valley, pagoda, stupa, flags', '36 hand-built study objects', '15 pattern engines (Dhaka, lattice, truchet)', 'Frameless people, buddy and critter avatars', 'Light and Dark parity on every piece', '14 kinds incl. 9:16 stories and patterns'].map(function (t) { return '<span class="chip">' + t + '</span>'; }).join('') + '</div>');
    $('#stage').innerHTML = o; $('#cs').onchange = function (e) { G.cmpSubj = e.target.value; G.views.compare(); };
  };
})();
