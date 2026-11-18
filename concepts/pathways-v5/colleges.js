/* Pathways v5 colleges: directory with map of all 77 districts, filters, compare and show more. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW, mapH = null;
  var S = V.st.colleges = V.st.colleges || { q: '', district: '', sector: '', kind: '', route: '', web: false, sort: 'name', map: window.innerWidth > 700, n: 24 };
  var KINDS = ['College', 'Campus', 'Institute', 'School', 'University', 'Medical college'];
  function match(p, skipDistrict) {
    if (!skipDistrict && S.district && p.district !== S.district) return false;
    if (S.sector && p.sector.toLowerCase() !== S.sector) return false; if (S.kind && p.kind !== S.kind) return false;
    if (S.route && !p._r[S.route]) return false; if (S.web && !p.website) return false;
    return !S.q || (p.name + ' ' + p.place + ' ' + p.district).toLowerCase().indexOf(S.q.toLowerCase()) >= 0;
  }
  var SORT = { name: function (a, b) { return a.name.localeCompare(b.name); }, seats: function (a, b) { return (b.seats || 0) - (a.seats || 0); }, courses: function (a, b) { return b._n - a._n; } };
  function counts() { var c = {}; PW.providers.forEach(function (p) { if (match(p, true)) c[p.district] = (c[p.district] || 0) + 1; }); return c; }
  function list() {
    var rs = PW.providers.filter(function (p) { return match(p); }).sort(SORT[S.sort]);
    return '<div class="cnt">' + rs.length.toLocaleString('en-US') + ' result' + (rs.length === 1 ? '' : 's') + (S.district ? ' in ' + E(S.district) : ' across Nepal') + '</div>' +
      (rs.length ? '<div class="grid g3 stag">' + rs.slice(0, S.n).map(function (p, i) { return ui.college(p, i % 12); }).join('') + '</div>' + (rs.length > S.n ? '<div class="row" style="justify-content:center;margin-top:16px"><button class="btn t" data-act="more24">Show ' + Math.min(24, rs.length - S.n) + ' more</button></div>' : '') : ui.empty('No college matches. Try another district or clear a filter.', 'apartment'));
  }
  function refresh() { V.$('#res').innerHTML = list(); if (mapH) mapH.update(counts(), S.district); var c = V.$('#dsel'); if (c) c.value = S.district; }
  V.acts.more24 = function () { S.n += 24; V.$('#res').innerHTML = list(); };
  V.chipH.k = function (el, k) { var p = k.split('-'); S[p[0]] = p[1] === 'x' ? '' : p.slice(1).join('-'); S.n = 24; V.$$('[data-k^="k-' + p[0] + '-"]').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); refresh(); };
  V.ins.kq = function (el) { S.q = el.value; S.n = 24; refresh(); };
  V.ins.kd = function (el) { S.district = el.value; S.n = 24; refresh(); };
  V.ins.kr = function (el) { S.route = el.value; S.n = 24; refresh(); };
  V.ins.ks = function (el) { S.sort = el.value; refresh(); };
  V.acts.kweb = function (el) { S.web = !S.web; el.setAttribute('aria-pressed', S.web); S.n = 24; refresh(); };
  V.acts.kmap = function (el) { S.map = !S.map; el.setAttribute('aria-pressed', S.map); drawMap(); };
  V.acts.kclear = function () { Object.assign(S, { q: '', district: '', sector: '', kind: '', route: '', web: false, n: 24 }); V.render(); };
  function drawMap() {
    var box = V.$('#kmap'); mapH = null; box.innerHTML = ''; box.hidden = !S.map; V.$('#kleg').hidden = !S.map; if (!S.map) return;
    mapH = window.PWMAP.mount(box, { counts: counts(), selected: S.district, onPick: function (n) { S.district = n; S.n = 24; refresh(); } });
  }
  function chips(prefix, items, cur) { return '<div class="chips">' + items.map(function (x) { return '<button class="chip" data-act="chip" data-k="k-' + prefix + '-' + (x[0] || 'x') + '" aria-pressed="' + (cur === x[0]) + '">' + x[1] + '</button>'; }).join('') + '</div>'; }
  V.views.colleges = function () {
    var ds = Object.keys(PW.providers.reduce(function (m, p) { m[p.district] = 1; return m; }, {})).sort();
    var rs = PW.routes.filter(function (r) { return r._pro.length; }).sort(function (a, b) { return a.name.localeCompare(b.name); });
    return { title: 'Colleges', html: ui.head('Colleges and schools', PW.stats.providers + ' places across all ' + PW.stats.districts + ' districts. Pick one on the map or search.') +
      '<div class="fb"><div class="rowf"><label class="fld grow" style="min-width:220px">' + M('search') + '<input type="search" data-in="kq" placeholder="Search by name or place" value="' + E(S.q) + '"></label>' +
      '<label class="fld">' + M('location_on') + '<select id="dsel" data-in="kd"><option value="">All districts</option>' + ds.map(function (d) { return '<option' + (S.district === d ? ' selected' : '') + '>' + E(d) + '</option>'; }).join('') + '</select></label>' +
      '<label class="fld">' + M('school') + '<select data-in="kr"><option value="">Any course</option>' + rs.map(function (r) { return '<option value="' + r.id + '"' + (S.route === r.id ? ' selected' : '') + '>' + E(r.name) + '</option>'; }).join('') + '</select></label></div>' +
      chips('sector', [['', 'Any sector'], ['public', 'Public'], ['private', 'Private'], ['community', 'Community']], S.sector) + chips('kind', [['', 'All types']].concat(KINDS.map(function (k) { return [k, k]; })), S.kind) +
      '<div class="rowf"><button class="chip" data-act="locate">' + M('my_location') + 'Near me</button><button class="chip" data-act="kweb" aria-pressed="' + S.web + '">' + M('language') + 'Has website</button><button class="chip" data-act="kmap" aria-pressed="' + S.map + '">' + M('map') + 'Map</button><button class="chip" data-act="kclear">' + M('filter_alt_off') + 'Clear</button>' +
      '<label class="fld" style="margin-left:auto">' + M('sort') + '<select data-in="ks">' + [['name', 'A to Z'], ['seats', 'Most seats'], ['courses', 'Most courses']].map(function (o) { return '<option value="' + o[0] + '"' + (S.sort === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label></div></div>' +
      '<div id="kmap"></div><div class="legend" id="kleg"><i style="background:var(--s4)"></i>none<i style="background:color-mix(in srgb,var(--p) 40%,var(--s4))"></i>a few<i style="background:var(--p)"></i>many</div><div id="res" style="margin-top:14px">' + list() + '</div>', after: drawMap };
  };
})();
