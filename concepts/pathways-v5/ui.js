/* Pathways v5 shared cards and small building blocks. */
(function () {
  'use strict';
  var V = window.V, ch = V.ch, ui = V.ui = {}, E = V.esc, M = V.ms;
  ui.TRACK = V.by(V.PW.govt_tracks);
  ui.head = function (title, sub, right) {
    return '<header class="ph"><div class="grow"><h1>' + title + '</h1>' + (sub ? '<p class="mut" style="margin-top:6px;max-width:640px">' + sub + '</p>' : '') + '</div>' + (right || '') + '</header>';
  };
  ui.sec = function (title, body, more) {
    return '<section class="sec"><div class="hd"><h2>' + title + '</h2>' + (more ? '<button class="more" data-go="' + more[0] + '">' + more[1] + M('chevron_right', 'sm') + '</button>' : '') + '</div>' + body + '</section>';
  };
  ui.crumb = function (label, to) { return '<button class="btn g sm back" data-act="back" data-to="' + to + '">' + M('arrow_back', 'sm') + label + '</button>'; };
  V.acts.back = function (el) { V.go(el.dataset.to); };
  ui.chipRow = function (id, items, cur, multi) {
    return '<div class="chips ' + (multi ? 'wrap' : '') + '" id="' + id + '">' + items.map(function (x) { return '<button class="chip" data-act="chip" data-k="' + id + '" data-v="' + E(x[0]) + '" aria-pressed="' + (cur === x[0]) + '">' + (x[2] ? M(x[2]) : '') + E(x[1]) + '</button>'; }).join('') + '</div>';
  };
  ui.course = function (r, i, note) {
    var g = V.grp(r.group), pro = r._pro.length, has = r._c.length, fee = V.range(r.fee).replace(/NPR /g, '');
    return '<article class="card click cc cv2" style="--i:' + (i || 0) + '" data-go="course/' + r.id + '" tabindex="0"><div class="row" style="align-items:flex-start"><span class="ic ' + g[2] + '">' + M(g[1]) + '</span><div class="grow"><h3>' + E(r.name) + '</h3><div class="xs mut">' + E(r.kind) + ' &middot; ' + E(r.years) + '</div></div>' + V.saveBtn('course', r.id) + '</div>' +
      (note ? '<span class="tag note">' + M('auto_awesome') + E(note) + '</span>' : '') +
      '<p class="sm mut cl2">' + E(r.about) + '</p>' +
      '<div class="cstat"><div><b>' + E(fee) + '</b><span>Fee, NPR</span></div><div><b>' + (pro || '-') + '</b><span>Colleges</span></div><div><b>' + (has ? V.npr(r._pay).replace('NPR ', '') : '-') + '</b><span>Pay a month</span></div></div>' +
      (has ? '<div class="olk"><span class="xs mut">Demand</span><div class="mt" style="--v:' + Math.round(r._dem * 20) + ';--c:var(--good)"><i></i></div><b class="xs">' + ch.level(r._dem) + '</b></div>' : '') + '</article>';
  };
  ui.college = function (p, i) {
    var rs = Object.keys(p._r).filter(function (x) { return V.R[x]; }).slice(0, 3).map(function (x) { return '<span class="tag">' + E(V.R[x].name) + '</span>'; }).join('');
    return '<article class="card click" style="--i:' + (i || 0) + '" data-go="college/' + p.id + '" tabindex="0"><div class="row"><span class="ic t-sc">' + M(p.kind === 'School' ? 'backpack' : p.kind === 'University' ? 'account_balance' : /medical|dental/i.test(p.kind) ? 'local_hospital' : 'apartment') + '</span><div class="grow"><h3>' + E(p.name) + '</h3><div class="xs mut row" style="gap:4px">' + M('location_on', 'xs') + E(p.place) + ', ' + E(p.district) + '</div></div>' + V.saveBtn('college', p.id) + '</div>' +
      '<div class="row wrap" style="gap:6px"><span class="tag">' + E(p.kind) + '</span><span class="tag ' + (/pub/i.test(p.sector) ? 't-gc' : /comm/i.test(p.sector) ? 't-yc' : 't-sc') + '">' + E(V.cap(p.sector)) + '</span>' + (p.seats ? '<span class="tag">' + M('event_seat') + p.seats + ' seats</span>' : '') + (p.website ? '<span class="tag t-pc">' + M('language') + 'Website</span>' : '') + '</div>' +
      (rs ? '<div class="row wrap" style="gap:6px">' + rs + (p._n > 3 ? '<span class="tag">+' + (p._n - 3) + ' more</span>' : '') + '</div>' : '') + '<div class="row" style="justify-content:flex-end">' + V.cmpBtn('college', p.id) + '</div></article>';
  };
  ui.career = function (c, i) {
    var o = V.opp(c);
    return '<article class="card click" style="--i:' + (i || 0) + '" data-go="career/' + c.id + '" tabindex="0"><div class="row"><span class="ic t-tc" style="color:var(--tf)">' + ch.ring(o, 44, 'Opportunity') + '</span><div class="grow"><h3>' + E(c.name) + '</h3><div class="xs mut">Starts ' + V.range(c.salary.entry) + ' a month</div></div>' + V.saveBtn('career', c.id) + '</div>' +
      '<p class="sm mut cl2">' + E(c.about) + '</p><div class="row wrap" style="gap:6px">' + ch.trendTag(c.trend) + '<span class="tag">Demand ' + ch.level(c.demand) + '</span><span class="tag">Competition ' + ch.level(c.competition) + '</span></div></article>';
  };
  ui.open = function (w) { return ch.inWindow(w) ? '<span class="tag t-gc">' + M('radio_button_checked') + 'Open now</span>' : ''; };
  ui.exam = function (g, i) {
    var t = ui.TRACK[g.track];
    return '<article class="card click" style="--i:' + (i || 0) + '" data-go="exam/' + g.id + '" tabindex="0"><div class="row"><span class="ic ' + (t && t.group === 'gov' ? 't-sc' : t && t.group === 'lang' ? 't-yc' : 't-pc') + '">' + M(t && t.group === 'lang' ? 'translate' : t && t.group === 'gov' ? 'account_balance' : 'edit_note') + '</span><div class="grow"><h3>' + E(g.name) + '</h3><div class="xs mut">' + E(g.body) + '</div></div>' + V.saveBtn('exam', g.id) + '</div>' +
      '<div class="row wrap" style="gap:6px"><span class="tag">' + E(t ? t.label : g.track) + '</span><span class="tag">' + M('school') + E(g.need.split(',')[0].slice(0, 34)) + '</span>' + ui.open(g.apply) + '</div></article>';
  };
  ui.country = function (a, i) {
    var cost = V.mid(a.tuition) + V.mid(a.living);
    return '<article class="card click" style="--i:' + (i || 0) + '" data-go="country/' + a.id + '" tabindex="0"><div class="row"><span class="ic t-pc" style="font-weight:600;font-size:14px">' + E(a.code || a.id.toUpperCase()) + '</span><div class="grow"><h3>' + E(a.country) + '</h3><div class="xs mut">' + E(a.intakes) + '</div></div>' + V.saveBtn('country', a.id) + '</div>' +
      '<div class="kv"><span>Tuition a year</span><b>' + V.range(a.tuition) + '</b></div><div class="kv"><span>Living a year</span><b>' + V.range(a.living) + '</b></div><div class="row wrap" style="gap:6px">' + (a.work_hours ? '<span class="tag">' + M('schedule') + a.work_hours + ' h work a week</span>' : '') + '<span class="tag t-gc">' + M('workspace_premium') + a.scholarships.length + ' grants</span>' + '</div><div class="row" style="justify-content:space-between"><span class="xs mut">About ' + V.npr(cost) + ' a year</span>' + V.cmpBtn('country', a.id) + '</div></article>';
  };
  ui.schol = function (s, i) {
    return '<article class="card click" style="--i:' + (i || 0) + '" data-act="schol" data-id="' + s.id + '" tabindex="0"><div class="row"><span class="ic t-gc">' + M(s.scope === 'abroad' ? 'flight_takeoff' : 'workspace_premium') + '</span><div class="grow"><h3>' + E(s.name) + '</h3><div class="xs mut">' + E(s.by) + '</div></div>' + V.saveBtn('schol', s.id) + '</div>' +
      '<p class="sm mut cl2">' + E(s.covers) + '</p><div class="row wrap" style="gap:6px"><span class="tag">' + E(s.type) + '</span>' + (s.levels || []).map(function (l) { return '<span class="tag">' + E(V.cap(l)) + '</span>'; }).join('') + ui.open(s.open) + '</div>' + (s.open ? ch.months(s.open[0], s.open[1], 'var(--good)') : '') + '</article>';
  };
  V.acts.schol = function (el) {
    var s = V.S[el.dataset.id]; if (!s) return; var a = s.country && V.A[s.country];
    V.sheet('<div class="row" style="align-items:flex-start"><span class="ic t-gc">' + M('workspace_premium') + '</span><div class="grow"><h2>' + E(s.name) + '</h2><div class="sm mut">' + E(s.by) + '</div></div>' + V.saveBtn('schol', s.id) + '</div>' +
      '<div class="row wrap" style="gap:6px;margin:14px 0"><span class="tag">' + E(s.type) + '</span><span class="tag">' + (s.scope === 'abroad' ? 'Study abroad' : 'In Nepal') + '</span>' + (s.levels || []).map(function (l) { return '<span class="tag">' + E(V.cap(l)) + '</span>'; }).join('') + ui.open(s.open) + '</div>' + (s.open ? '<div class="sm mut" style="margin-bottom:6px">Applications usually open ' + V.MONTHS[s.open[0] - 1] + ' to ' + V.MONTHS[s.open[1] - 1] + '</div>' + ch.months(s.open[0], s.open[1], 'var(--good)') : '') +
      '<div class="kv"><span>Covers</span><b>' + E(s.covers) + '</b></div><div class="kv"><span>Who can apply</span><b>' + E(s.who) + '</b></div><div class="kv"><span>How to apply</span><b>' + E(s.how) + '</b></div>' +
      '<div class="row wrap" style="margin-top:16px">' + (s.link ? '<a class="btn" target="_blank" rel="noopener" href="' + E(s.link) + '">' + M('open_in_new', 'sm') + 'Official page</a>' : '') + (a ? '<button class="btn t" data-go="country/' + a.id + '">' + M('public', 'sm') + E(a.country) + '</button>' : '') + '</div>');
  };
  ui.empty = function (t, ic) { return '<div class="empty">' + M(ic || 'search_off') + '<p>' + t + '</p></div>'; };
})();
