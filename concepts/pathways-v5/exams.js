/* Pathways v5 exams: government, entrance, language and licence exams with a live eligibility check. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, ch = V.ch, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.exams = V.st.exams || { grp: 'gov', track: '', q: '', lvl: 0, age: '' };
  var LV = [['SEE', 1], ['+2', 2], ['Bachelor', 3], ['Master', 4]];
  function need(g) {
    var t = g.need.toLowerCase(), l = [];
    if (/master/.test(t)) l.push(4); if (/bachelor|degree|graduat/.test(t)) l.push(3); if (/\+2|plus two|10\+2|intermediate|class 12|grade 12|proficiency certificate/.test(t)) l.push(2); if (/\bsee\b|slc|class 10|grade 10/.test(t)) l.push(1);
    return l.length ? Math.min.apply(null, l) : 0;
  }
  function ageOk(g, a) {
    var m = g.age.match(/(\d{2})\s*(?:to|-)\s*(\d{2})/); if (!m || !a) return null;
    return a >= +m[1] && a <= +m[2] ? true : /women|disab|candidate/i.test(g.age) && a <= +m[2] + 5 && a >= +m[1] ? 'extra' : false;
  }
  function fit(g) {
    if (!S.lvl && !S.age) return ''; var n = need(g), a = ageOk(g, +S.age);
    if (S.lvl && n && S.lvl < n) return '<span class="tag t-rc">' + M('block') + 'Needs ' + LV[n - 1][0] + '</span>';
    if (a === false) return '<span class="tag t-rc">' + M('block') + 'Age outside ' + E(g.age.split(',')[0]) + '</span>';
    if (S.lvl && n) return '<span class="tag t-gc">' + M('check_circle') + (a === 'extra' ? 'Eligible with age relaxation' : 'You can apply') + '</span>';
    return '<span class="tag">' + M('help') + 'Check the notice</span>';
  }
  function list() {
    var gs = PW.govt.filter(function (g) { var t = ui.TRACK[g.track]; return t && t.group === S.grp && (!S.track || g.track === S.track) && (!S.q || (g.name + ' ' + g.body).toLowerCase().indexOf(S.q.toLowerCase()) >= 0); });
    gs.sort(function (a, b) { return (S.lvl ? (need(b) <= S.lvl ? 1 : 0) - (need(a) <= S.lvl ? 1 : 0) : 0) || (ch.inWindow(b.apply) ? 1 : 0) - (ch.inWindow(a.apply) ? 1 : 0); });
    return '<div class="cnt">' + gs.length + ' exams</div><div class="grid g3 stag">' + gs.map(function (g, i) { return ui.exam(g, i).replace('</article>', (fit(g) ? '<div class="row wrap">' + fit(g) + '</div>' : '') + '</article>'); }).join('') + '</div>';
  }
  function tracks() { return ui.chipRow('x-track', [['', 'All']].concat(PW.govt_tracks.filter(function (t) { return t.group === S.grp; }).map(function (t) { return [t.id, t.label]; })), S.track); }
  V.chipH.x = function (el, k) { S.track = el.dataset.v; V.$$('#x-track .chip').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); V.$('#res').innerHTML = list(); };
  V.acts.xgrp = function (el) { S.grp = el.dataset.v; S.track = ''; V.$$('#xgrp button').forEach(function (b) { b.setAttribute('aria-pressed', b === el); }); V.$('#x-track').outerHTML = tracks(); V.$('#res').innerHTML = list(); };
  V.ins.xq = function (el) { S.q = el.value; V.$('#res').innerHTML = list(); };
  V.ins.xl = function (el) { S.lvl = +el.value; V.$('#res').innerHTML = list(); };
  V.ins.xa = function (el) { S.age = el.value; V.$('#res').innerHTML = list(); };
  V.views.exams = function () {
    var gl = { gov: 'Government', ent: 'Entrance and licence', lang: 'Language' };
    return { title: 'Exams', html: ui.head('Exams', 'Lok Sewa, entrances, licences and language tests: stages, dates, eligibility.') +
      '<div class="card flat row wrap" style="margin-bottom:14px"><div class="grow"><h3>Can I apply?</h3><div class="xs mut">Tell us your level and age. Every card shows the answer.</div></div><label class="fld">' + M('school') + '<select data-in="xl"><option value="0">My level</option>' + LV.map(function (l) { return '<option value="' + l[1] + '"' + (S.lvl === l[1] ? ' selected' : '') + '>' + l[0] + '</option>'; }).join('') + '</select></label><label class="fld" style="width:130px">' + M('cake') + '<input data-in="xa" type="number" min="14" max="60" placeholder="Age" value="' + E(S.age) + '"></label></div>' +
      '<div class="fb"><div class="rowf"><div class="seg" id="xgrp">' + PW.govt_groups.map(function (g) { return '<button data-act="xgrp" data-v="' + g.id + '" aria-pressed="' + (S.grp === g.id) + '">' + (gl[g.id] || g.label) + '</button>'; }).join('') + '</div><label class="fld grow" style="min-width:200px">' + M('search') + '<input type="search" data-in="xq" placeholder="Search exams" value="' + E(S.q) + '"></label></div>' + tracks() + '</div><div id="res">' + list() + '</div>' };
  };
  V.views.exam = function (id) {
    var g = V.G[id]; if (!g) return ui.empty('Exam not found.'); var t = ui.TRACK[g.track], c = g.career && V.C[g.career], rs = PW.routes.filter(function (r) { return r.exam_id === g.id; });
    var kp = [['Level', g.level], ['Age', g.age.split(',')[0]], g.fee && ['Fee', typeof g.fee === 'number' ? V.npr(g.fee) : g.fee], g.seats && ['Seats', g.seats], g.prep_hours && ['Prep time', g.prep_hours + ' hours'], g.pay && ['Pay', typeof g.pay === 'number' ? V.npr(g.pay) : g.pay]].filter(Boolean).slice(0, 4);
    return { title: g.name, html: '<div class="crumbs">' + ui.crumb('Exams', 'exams') + '<span class="tag">' + E(t ? t.label : '') + '</span>' + ui.open(g.apply) + '</div>' +
      '<section class="dh card tone t-sc"><div class="row" style="align-items:flex-start"><div class="grow"><h1>' + E(g.name) + '</h1><div style="margin-top:6px">' + E(g.body) + '</div></div>' + V.saveBtn('exam', g.id) + '</div><div class="kpis">' + kp.map(function (k) { return '<div class="kpi"><b>' + E(k[1]) + '</b><span>' + k[0] + '</span></div>'; }).join('') + '</div></section>' +
      '<div class="cols sec"><div class="col" style="gap:16px"><div class="card"><h3>Who can apply</h3><div class="kv"><span>Education</span><b>' + E(g.need) + '</b></div><div class="kv"><span>Age</span><b>' + E(g.age) + '</b></div>' + (fit(g) ? '<div style="margin-top:10px">' + fit(g) + '</div>' : '<div class="xs mut" style="margin-top:8px">Set your level on the Exams page to see if you qualify.</div>') + '</div>' +
      (g.apply ? '<div class="card"><h3>Apply window</h3><div class="xs mut" style="margin:4px 0 10px">Usually ' + V.MONTHS[g.apply[0] - 1] + ' to ' + V.MONTHS[g.apply[1] - 1] + (g.exam_month ? ', exam in ' + V.MONTHS[g.exam_month - 1] : '') + '</div>' + ch.months(g.apply[0], g.apply[1], 'var(--good)') + '</div>' : '') +
      '<div class="card"><h3>Stages</h3><ol class="tl" style="margin-top:14px">' + g.stages.map(function (s, i) { return '<li style="--i:' + i + '"><span class="dot">' + (i + 1) + '</span><div><b>' + E(s[0]) + '</b><div class="sm mut">' + E(s[1]) + '</div></div></li>'; }).join('') + '</ol></div>' +
      (g.syllabus ? '<div class="card"><h3>Syllabus weight</h3><div class="col" style="margin-top:12px">' + g.syllabus.map(function (s) { return ch.meter(E(s[0]).slice(0, 14), s[1], 'var(--p)', s[1] + '%'); }).join('') + '</div></div>' : '<div class="card"><h3>Subjects</h3><div class="row wrap" style="gap:8px;margin-top:10px">' + g.subjects.map(function (s) { return '<span class="tag t-pc">' + E(s) + '</span>'; }).join('') + '</div></div>') +
      (g.quota ? '<div class="card"><h3>Seat quota</h3><div style="margin-top:12px">' + ch.stack(g.quota.map(function (q, i) { return [q[0], q[1], ['var(--p)', 'var(--good)', 'var(--warn)', 'var(--bad)', 'var(--onv)'][i % 5]]; })).replace(/NPR /g, '') + '</div></div>' : '') +
      (g.note ? '<div class="card flat"><h3>Good to know</h3><p class="sm mut" style="margin-top:8px">' + E(g.note) + '</p></div>' : '') + '</div>' +
      '<aside class="side col"><div class="card"><h3>How to prepare</h3><ol class="tl" style="margin-top:12px">' + g.prep.map(function (p, i) { return '<li style="--i:' + i + '"><span class="dot">' + (i + 1) + '</span><div class="sm">' + E(p) + '</div></li>'; }).join('') + '</ol></div>' +
      (c ? '<button class="card click row" data-go="career/' + c.id + '"><span class="ic t-tc">' + M('work') + '</span><div class="grow" style="text-align:left"><b>' + E(c.name) + '</b><div class="xs mut">Career this opens</div></div>' + M('chevron_right') + '</button>' : '') +
      rs.slice(0, 4).map(function (r) { return '<button class="card click row" data-go="course/' + r.id + '"><span class="ic t-pc">' + M('school') + '</span><div class="grow" style="text-align:left"><b>' + E(r.name) + '</b><div class="xs mut">Course that uses this exam</div></div>' + M('chevron_right') + '</button>'; }).join('') + '</aside></div>' };
  };
})();
