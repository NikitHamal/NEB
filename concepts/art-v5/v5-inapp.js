/* v5 in-app preview: profiles for four roles, resources, empty states, badges, picture shapes, books, pathways, heroes, stories. */
(function () {
  'use strict';
  var A = NebArtV5, G = window.G5, host = document.getElementById('inapp'), cache = {};
  function by(k) { return cache[k] || (cache[k] = G.byKind(k)); }
  function r(k, i) { var l = by(k); return G.html(l[i % l.length]); }
  function item(k, i) { var l = by(k); return l[i % l.length]; }
  function prof(role, cover, pp, name, line) { return '<div class="prof"><div class="cv">' + r('cover', cover) + '</div><div class="pp">' + r('avatar', pp) + '</div><div class="pb"><b>' + name + '</b><div class="sub">' + role + ' / ' + line + '</div></div></div>'; }
  function res(i, t, m) { return '<div class="card" style="cursor:default"><span class="art">' + r('thumb', i) + '</span><span class="meta"><b>' + t + '</b><span class="s">' + m + '</span></span></div>'; }
  function build() {
    var h = '', i, R = [['Class 12 Physics Notes', 'Grade 12 / 4.2 MB'], ['Accountancy Model Paper', 'Grade 11 / 1.8 MB'], ['Chemistry Chapter 3', 'Grade 12 / 3.1 MB'], ['English Grammar Guide', 'Grade 10 / 2.4 MB'], ['Economics Solutions', 'Grade 12 / 5.0 MB'], ['Computer Science Lab Book', 'Grade 11 / 6.2 MB']];
    h += '<h2>Profiles</h2><div class="st" style="--m:340px">' + prof('Student', 3, 4, 'Anisha Rai', 'Grade 12 Science') + prof('Teacher', 9, 15, 'Hari Sharma', 'Physics, 12 years') + prof('School', 3 + 30, 12 + 20, 'Sunrise Secondary', 'Kathmandu') + prof('Parent', 21, 33, 'Laxmi Gurung', 'Follows 3 schools') + '</div>';
    h += '<h2>Resource cards</h2><div class="st" style="--m:260px">' + R.map(function (x, i) { return res(i * 7, x[0], x[1]); }).join('') + '</div>';
    h += '<h2>Empty states</h2><div class="st" style="--m:230px">' + [0, 4, 8, 12, 16, 20, 24, 40, 44, 52, 60, 64].map(function (i) { var it = item('spot', i * 1); return '<div><div class="a">' + G.html(it) + '</div><div class="cap">' + it.name + '</div></div>'; }).join('') + '</div>';
    h += '<h2>Achievements</h2><div class="st" style="--m:130px">' + [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75].map(function (i) { var it = item('sticker', i); return '<div><div class="a">' + G.html(it) + '</div><div class="cap">' + it.name.split(' / ')[0] + '</div></div>'; }).join('') + '</div>';
    h += '<h2>Picture shapes</h2><div class="panel"><div class="shapes">' + ['50%', '30%', '50% 50% 14% 14%', '50% 0 50% 0', '22% 50% 22% 50%', '16%'].map(function (s, i) { return '<div style="border-radius:' + s + '">' + r('avatar', 40 + i * 31) + '</div>'; }).join('') + '</div></div>';
    h += '<h2>Books</h2><div class="st" style="--m:140px">' + [0, 2, 5, 8, 11, 14].map(function (i) { return '<div class="a">' + r('book', i) + '</div>'; }).join('') + '</div>';
    h += '<h2>Pathways and labs</h2><div class="st" style="--m:340px">' + [0, 6, 12].map(function (i) { return '<div class="a">' + r('pathway', i) + '</div>'; }).join('') + [0, 5, 9].map(function (i) { return '<div class="a">' + r('lab', i) + '</div>'; }).join('') + '</div>';
    h += '<h2>Hero banners and posts</h2><div class="st" style="--m:480px">' + [0, 3].map(function (i) { return '<div class="a">' + r('wide', i) + '</div>'; }).join('') + [0, 1].map(function (i) { return '<div class="a">' + r('post', i) + '</div>'; }).join('') + '</div>';
    h += '<h2>Onboarding stories</h2><div class="st" style="--m:150px">' + [0, 1, 2, 3, 4, 5].map(function (i) { return '<div class="a">' + r('story', i) + '</div>'; }).join('') + '</div>';
    host.innerHTML = h;
  }
  G.listeners.push(function () { if (!host.hidden) build(); });
  window.G5.buildInapp = build;
})();
