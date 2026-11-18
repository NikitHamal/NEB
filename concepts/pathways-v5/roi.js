/* Pathways v5 "Is it worth it": cost against earnings, payback month and a cash line. */
(function () {
  'use strict';
  var V = window.V, ui = V.ui, M = V.ms, E = V.esc, PW = V.PW;
  var S = V.st.roi = V.st.roi || { route: '', career: '', fee: -1, sch: 0, live: 12000, save: 30, loan: 0, rate: 12 };
  var pool = PW.routes.filter(function (r) { return r._c.length && r.fee[1] > 0; }).sort(function (a, b) { return a.name.localeCompare(b.name); });
  var yrsOf = function (r) { var m = r.years.match(/\d+(\.\d+)?/); return m ? +m[0] : 3; };
  var payAt = function (c, y) { var a = V.mid(c.salary.entry), b = V.mid(c.salary.senior), t = Math.min(1, y / 15); return a + (b - a) * (1 - Math.pow(1 - t, 1.6)); };
  function calc() {
    var r = V.R[S.route] || pool[0]; if (!V.R[S.route]) S.route = r.id;
    var c = V.C[S.career] && r.careers.indexOf(S.career) >= 0 ? V.C[S.career] : r._c[0]; S.career = c.id;
    if (S.fee < 0 || S.fee < r.fee[0] * .5 || S.fee > r.fee[1] * 1.5) S.fee = Math.round(V.mid(r.fee) / 5000) * 5000;
    var y = yrsOf(r), fee = S.fee * (1 - S.sch / 100), live = S.live * 12 * y, loanCost = fee * (S.loan / 100) * (S.rate / 100) * 4, cost = fee + live + loanCost, pts = [], be = null, cum = 0, months = (y + 12) * 12;
    for (var m = 0; m <= months; m += 3) {
      var inc = 0; if (m <= y * 12) cum = -cost * (m / (y * 12)); else { var yy = (m - y * 12) / 12; inc = payAt(c, yy) * S.save / 100; cum = -cost + sumSave(c, y, m); }
      pts.push([m, cum]); if (be == null && cum >= 0 && m > y * 12) be = m;
    }
    return { r: r, c: c, y: y, fee: fee, live: live, loanCost: loanCost, cost: cost, pts: pts, be: be, months: months, start: V.mid(c.salary.entry), five: payAt(c, 5) };
  }
  function sumSave(c, y, m) { var s = 0, t0 = y * 12; for (var k = t0; k < m; k++) s += payAt(c, (k - t0) / 12) * S.save / 100; return s; }
  function chart(x) {
    var W = 600, H = 220, P = 28, lo = Math.min.apply(null, x.pts.map(function (p) { return p[1]; })), hi = Math.max(Math.max.apply(null, x.pts.map(function (p) { return p[1]; })), x.cost * .25), sx = function (m) { return P + (W - P * 2) * m / x.months; }, sy = function (v) { return H - P - (H - P * 2) * (v - lo) / (hi - lo || 1); };
    var d = x.pts.map(function (p, i) { return (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join(''), z = sy(0);
    return '<svg class="cash" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Cumulative savings against cost"><line class="ax" x1="' + P + '" x2="' + (W - P) + '" y1="' + z.toFixed(1) + '" y2="' + z.toFixed(1) + '"/>' +
      '<line class="ax" x1="' + sx(x.y * 12).toFixed(1) + '" x2="' + sx(x.y * 12).toFixed(1) + '" y1="' + P + '" y2="' + (H - P) + '"/><path class="ar" d="' + d + 'L' + sx(x.months).toFixed(1) + ' ' + z.toFixed(1) + 'L' + P + ' ' + z.toFixed(1) + 'Z"/>' +
      '<path class="ln" d="' + d + '" pathLength="1" style="--l:1" stroke-dasharray="1" stroke-dashoffset="1"/>' + (x.be ? '<circle class="be" cx="' + sx(x.be).toFixed(1) + '" cy="' + z.toFixed(1) + '" r="7"/>' : '') +
      '<text x="' + (sx(x.y * 12) + 6).toFixed(1) + '" y="' + (P + 6) + '">Graduate</text><text x="' + P + '" y="' + (H - 6) + '">Start</text><text x="' + (W - P) + '" y="' + (H - 6) + '" text-anchor="end">' + (x.y + 12) + ' years</text></svg>';
  }
  function out() {
    var x = calc(), yrs = x.be ? (x.be - x.y * 12) / 12 : null, tone = yrs == null ? 't-rc' : yrs <= 3 ? 't-gc' : yrs <= 7 ? 't-yc' : 't-rc';
    var msg = yrs == null ? 'Does not pay back within 12 years of graduating at this cost. Look for a scholarship, a cheaper college or a shorter route.' : yrs <= 3 ? 'Pays back quickly, about ' + yrs.toFixed(1) + ' years after you graduate.' : yrs <= 7 ? 'Pays back in about ' + yrs.toFixed(1) + ' years after you graduate.' : 'Slow payback, about ' + yrs.toFixed(1) + ' years. A scholarship or cheaper college would help.';
    return '<div class="verdict ' + tone + '" style="--tb:var(--' + (tone === 't-gc' ? 'gc' : tone === 't-yc' ? 'yc' : 'rc') + ');--tf:var(--' + (tone === 't-gc' ? 'ongc' : tone === 't-yc' ? 'onyc' : 'onrc') + ')">' + M(tone === 't-gc' ? 'trending_up' : tone === 't-yc' ? 'hourglass_top' : 'warning', 'lg') + '<div><b>' + msg + '</b></div></div>' +
      '<div class="grid g3" style="margin:14px 0"><div class="stat t-pc"><b>' + V.npr(x.cost) + '</b><span>Total cost over ' + x.y + ' years</span></div><div class="stat t-gc"><b>' + V.npr(x.start) + '</b><span>Starting pay a month</span></div><div class="stat t-yc"><b>' + V.npr(Math.round(x.five)) + '</b><span>Pay after 5 years, estimated</span></div></div>' +
      '<div class="card">' + chart(x) + '<div class="xs mut" style="margin-top:6px">Line: what you have kept after paying for the course. It crosses zero at the dot.</div></div>' +
      '<div class="card flat" style="margin-top:12px"><div class="kv"><span>Course fee after scholarship</span><b>' + V.npr(x.fee) + '</b></div><div class="kv"><span>Living during study</span><b>' + V.npr(x.live) + '</b></div>' + (x.loanCost ? '<div class="kv"><span>Loan interest, 4 years</span><b>' + V.npr(x.loanCost) + '</b></div>' : '') + '<div class="kv"><span>Saved from pay</span><b>' + S.save + '%</b></div></div>' +
      '<div class="row wrap" style="margin-top:12px"><button class="btn t" data-go="course/' + x.r.id + '">Open course</button><button class="btn t" data-go="career/' + x.c.id + '">Open career</button></div>';
  }
  function sl(id, label, v, min, max, step, fmt) { return '<div class="sl"><div class="row"><span class="sm mut">' + label + '</span><b id="' + id + 'v">' + fmt(v) + '</b></div><input class="rng" type="range" min="' + min + '" max="' + max + '" step="' + step + '" value="' + v + '" data-in="roi" data-f="' + id + '"></div>'; }
  V.ins.roi = function (el) {
    var f = el.dataset.f, v = +el.value; if (f === 'route') { S.route = el.value; S.career = ''; S.fee = -1; return V.render(); } if (f === 'career') S.career = el.value; else S[f] = v;
    var lab = V.$('#' + f + 'v'); if (lab) lab.textContent = f === 'fee' || f === 'live' ? V.npr(v) : v + '%'; V.$('#roiOut').innerHTML = out();
  };
  V.views.roi = function () {
    var x = calc(), r = x.r;
    return { title: 'Worth it', html: ui.head('Is it worth it?', 'Course cost against what you can earn, with the month you break even.') + '<div class="calc"><div class="card col" style="gap:14px"><label class="fld">' + M('school') + '<select data-in="roi" data-f="route">' + pool.map(function (p) { return '<option value="' + p.id + '"' + (p.id === r.id ? ' selected' : '') + '>' + E(p.name) + '</option>'; }).join('') + '</select></label>' +
      '<label class="fld">' + M('work') + '<select data-in="roi" data-f="career">' + r._c.map(function (c) { return '<option value="' + c.id + '"' + (c.id === x.c.id ? ' selected' : '') + '>' + E(c.name) + '</option>'; }).join('') + '</select></label>' +
      sl('fee', 'Course fee', S.fee, Math.round(r.fee[0] * .5), Math.round(r.fee[1] * 1.5), 5000, V.npr) + sl('sch', 'Scholarship on fee', S.sch, 0, 100, 5, function (v) { return v + '%'; }) + sl('live', 'Living cost a month', S.live, 0, 50000, 1000, V.npr) + sl('save', 'Share of pay you save', S.save, 10, 70, 5, function (v) { return v + '%'; }) + sl('loan', 'Paid by loan', S.loan, 0, 100, 10, function (v) { return v + '%'; }) + sl('rate', 'Loan interest a year', S.rate, 6, 16, 1, function (v) { return v + '%'; }) + '</div><div id="roiOut">' + out() + '</div></div>' };
  };
})();
