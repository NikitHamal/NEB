/* Pathways v5 core: helpers, indexes, store, router, delegated events, sheets. Views register themselves on V.views. */
(function (g) {
  'use strict';
  var PW = g.PW, V = g.V = { PW: PW, views: {}, acts: {}, ins: {}, st: {}, hooks: [] };
  var D = document;
  V.$ = function (s, r) { return (r || D).querySelector(s); };
  V.$$ = function (s, r) { return Array.prototype.slice.call((r || D).querySelectorAll(s)); };
  V.esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  V.ms = function (n, c) { return '<span class="ms ' + (c || '') + '" aria-hidden="true">' + n + '</span>'; };
  V.MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  V.now = new Date().getMonth() + 1;
  V.npr = function (n) {
    if (n == null) return '';
    var a = Math.abs(n), f = function (x) { return String(+x.toFixed(x < 10 ? 2 : x < 100 ? 1 : 0)); };
    return 'NPR ' + (a >= 1e7 ? f(n / 1e7) + ' Cr' : a >= 1e5 ? f(n / 1e5) + ' L' : a >= 1e3 ? f(n / 1e3) + 'k' : Math.round(n));
  };
  V.range = function (a) { return !a ? '' : a[0] === a[1] ? V.npr(a[0]) : a[0] === 0 ? 'Up to ' + V.npr(a[1]) : V.npr(a[0]) + ' to ' + V.npr(a[1]).replace('NPR ', ''); };
  V.mid = function (a) { return a ? (a[0] + a[1]) / 2 : 0; };
  V.avg = function (a, f) { return a.length ? a.reduce(function (s, x) { return s + f(x); }, 0) / a.length : 0; };
  V.by = function (arr) { return arr.reduce(function (m, x) { m[x.id] = x; return m; }, {}); };
  V.cap = function (s) { return s.charAt(0).toUpperCase() + s.slice(1); };
  V.GROUPS = { tech: ['Tech and engineering', 'memory', 't-pc'], health: ['Health', 'medical_services', 't-rc'], biz: ['Business', 'business_center', 't-yc'], arts: ['Arts and media', 'palette', 't-tc'], sci: ['Science', 'science', 't-gc'], edu: ['Education', 'cast_for_education', 't-sc'], ag: ['Agriculture', 'agriculture', 't-gc'], gov: ['Government', 'account_balance', 't-sc'], law: ['Law', 'gavel', 't-tc'], school: ['School', 'backpack', 't-yc'], abroad: ['Abroad', 'flight_takeoff', 't-pc'] };
  V.STAGE_T = { after8: 't-yc', after10: 't-gc', after12: 't-pc', afterbach: 't-rc' };
  V.grp = function (k) { return V.GROUPS[k] || [V.cap(k || 'Other'), 'category', 't-sc']; };

  // indexes
  V.R = V.by(PW.routes); V.C = V.by(PW.careers); V.P = V.by(PW.providers); V.S = V.by(PW.scholarships); V.A = V.by(PW.abroad);
  V.G = V.by(PW.govt); V.GD = V.by(PW.guides); V.ST = V.by(PW.stages);
  PW.routes.forEach(function (r) {
    r._c = r.careers.map(function (i) { return V.C[i]; }).filter(Boolean);
    r._dem = V.avg(r._c, function (c) { return c.demand; }); r._comp = V.avg(r._c, function (c) { return c.competition; });
    r._pay = V.avg(r._c, function (c) { return V.mid(c.salary.entry); }); r._cost = V.mid(r.fee); r._pro = [];
  });
  PW.providers.forEach(function (p) {
    var ids = {}; Object.keys(p.fees || {}).concat(Object.keys(p.route_seats || {})).forEach(function (i) { ids[i] = 1; });
    p._r = ids;
  });
  PW.routes.forEach(function (r) { (r.where || []).forEach(function (id) { if (V.P[id]) V.P[id]._r[r.id] = 1; }); });
  PW.providers.forEach(function (p) { Object.keys(p._r).forEach(function (id) { if (V.R[id]) V.R[id]._pro.push(p); }); p._n = Object.keys(p._r).filter(function (i) { return V.R[i]; }).length; });
  PW.careers.forEach(function (c) { c._routes = PW.routes.filter(function (r) { return r.careers.indexOf(c.id) >= 0; }); c._lic = null; });
  V.opp = function (c) { return Math.round(Math.max(0, Math.min(100, (c.demand * 14 - c.competition * 4 + c.abroad * 4 + (c.trend === 'rising' ? 10 : c.trend === 'falling' ? -8 : 0)) + 8))); };

  // store
  var KEY = 'pwv5', S = { saved: {}, theme: '', ticks: {} };
  try { S = Object.assign(S, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}
  V.store = S;
  V.persist = function () { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };
  V.isSaved = function (k, id) { return (S.saved[k] || []).indexOf(id) >= 0; };
  V.savedCount = function () { return Object.keys(S.saved).reduce(function (n, k) { return n + S.saved[k].length; }, 0); };
  V.toggleSave = function (k, id) {
    var a = S.saved[k] = S.saved[k] || [], i = a.indexOf(id);
    if (i >= 0) a.splice(i, 1); else a.push(id);
    V.persist(); V.badge(); V.toast(i >= 0 ? 'Removed from My plan' : 'Saved to My plan', i >= 0 ? 'bookmark_remove' : 'bookmark_added'); return i < 0;
  };
  V.saveBtn = function (k, id, cls) { var on = V.isSaved(k, id); return '<button class="save ' + (cls || '') + '" data-save="' + k + ':' + id + '" aria-pressed="' + on + '" aria-label="Save">' + V.ms('bookmark') + '</button>'; };
  V.badge = function () { var b = V.$('#planBadge'), n = V.savedCount(); if (b) { b.hidden = !n; b.textContent = n; } };
  V.toast = function (t, ic) {
    var old = V.$('.toast'); if (old) old.remove();
    var el = D.createElement('div'); el.className = 'toast'; el.innerHTML = V.ms(ic || 'check_circle', 'sm') + V.esc(t); D.body.appendChild(el);
    setTimeout(function () { el.style.transition = 'opacity .3s'; el.style.opacity = 0; setTimeout(function () { el.remove(); }, 320); }, 1900);
  };
  V.sheet = function (html) {
    V.closeSheet(); var el = D.createElement('div'); el.className = 'scrim'; el.id = 'scrim';
    el.innerHTML = '<div class="sheet" role="dialog" aria-modal="true"><div class="grab"></div>' + html + '</div>'; D.body.appendChild(el);
    el.addEventListener('click', function (e) { if (e.target === el) V.closeSheet(); }); D.body.style.overflow = 'hidden'; return el;
  };
  V.closeSheet = function () { var s = V.$('#scrim'); if (s) s.remove(); D.body.style.overflow = ''; };

  // router
  V.NAV = [['home', 'Home', 'home'], ['roadmap', 'Roadmap', 'route'], ['courses', 'Courses', 'school'], ['colleges', 'Colleges', 'apartment'], ['careers', 'Careers', 'work'], ['exams', 'Exams', 'quiz'], ['abroad', 'Abroad', 'public'], ['schol', 'Grants', 'workspace_premium'], ['match', 'Match', 'auto_awesome'], ['roi', 'Worth it', 'savings'], ['plan', 'My plan', 'bookmark'], ['help', 'Guides', 'menu_book']];
  V.go = function (p) { location.hash = '#/' + p; };
  V.parse = function () { var h = location.hash.replace(/^#\/?/, '').split('/'); return { name: h[0] || 'home', arg: decodeURIComponent(h.slice(1).join('/')) }; };
  V.render = function () {
    var r = V.parse(), v = V.views[r.name] || V.views.home, root = V.$('#view');
    V.closeSheet(); var out = v(r.arg) || { html: '' }; if (typeof out === 'string') out = { html: out };
    root.className = 'view'; void root.offsetWidth; root.innerHTML = out.html; D.title = (out.title ? out.title + ' | ' : '') + 'NEBians Pathways';
    var key = r.name === 'course' ? 'courses' : r.name === 'college' ? 'colleges' : r.name === 'career' ? 'careers' : r.name === 'exam' ? 'exams' : r.name === 'country' ? 'abroad' : r.name === 'compare' ? 'colleges' : r.name;
    V.$$('[data-go][aria-current],[data-nav]').forEach(function (b) { if (b.dataset.nav) b.setAttribute('aria-current', b.dataset.nav === key ? 'page' : 'false'); });
    if (out.after) out.after(root); V.countUp(root); V.cmpTray(); g.scrollTo({ top: 0, behavior: 'instant' });
  };
  V.countUp = function (root) {
    V.$$('[data-count]', root).forEach(function (el) {
      var to = +el.dataset.count, t0 = performance.now(), D0 = 900;
      (function s(t) { var p = Math.min(1, (t - t0) / D0), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(to * e).toLocaleString('en-US'); if (p < 1) requestAnimationFrame(s); })(t0);
    });
  };
  // compare tray (colleges, courses, careers, countries)
  V.cmp = { kind: '', ids: [] };
  V.cmpTray = function () {
    var t = V.$('.tray'); if (t) t.remove();
    if (!V.cmp.ids.length || V.parse().name === 'compare') return;
    var c = V.cmp, el = D.createElement('div'); el.className = 'tray';
    el.innerHTML = V.ms('compare_arrows') + '<div class="grow"><b>' + c.ids.length + ' of 3</b> <span class="sm" style="opacity:.75">' + c.kind + ' to compare</span></div><button class="btn sm" data-go="compare/' + c.kind + '">Compare</button><button class="ib x" data-act="cmpclear" aria-label="Clear">' + V.ms('close', 'sm') + '</button>';
    D.body.appendChild(el);
  };
  V.toggleCmp = function (kind, id) {
    var c = V.cmp; if (c.kind !== kind) { c.kind = kind; c.ids = []; }
    var i = c.ids.indexOf(id); if (i >= 0) c.ids.splice(i, 1); else if (c.ids.length < 3) c.ids.push(id); else return V.toast('Compare up to 3 at a time', 'info');
    V.cmpTray(); V.$$('[data-cmp="' + kind + ':' + id + '"]').forEach(function (b) { b.setAttribute('aria-pressed', c.ids.indexOf(id) >= 0); });
  };
  V.cmpBtn = function (k, id) { return '<button class="chip" data-cmp="' + k + ':' + id + '" aria-pressed="' + (V.cmp.kind === k && V.cmp.ids.indexOf(id) >= 0) + '">' + V.ms('compare_arrows') + 'Compare</button>'; };

  D.addEventListener('click', function (e) {
    var t = e.target, el;
    if ((el = t.closest('[data-save]'))) { e.preventDefault(); e.stopPropagation(); var p = el.dataset.save.split(':'); el.setAttribute('aria-pressed', V.toggleSave(p[0], p[1])); return; }
    if ((el = t.closest('[data-cmp]'))) { e.preventDefault(); e.stopPropagation(); var q = el.dataset.cmp.split(':'); return V.toggleCmp(q[0], q[1]); }
    if ((el = t.closest('[data-act]'))) { var f = V.acts[el.dataset.act]; if (f) { e.preventDefault(); return f(el, e); } }
    if ((el = t.closest('[data-go]'))) { e.preventDefault(); if (el.dataset.go === location.hash.slice(2)) return V.render(); V.go(el.dataset.go); }
  });
  D.addEventListener('input', function (e) { var el = e.target.closest('[data-in]'); if (el && V.ins[el.dataset.in]) V.ins[el.dataset.in](el, e); });
  D.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') V.closeSheet();
    if ((e.key === 'k' && (e.ctrlKey || e.metaKey)) || (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(D.activeElement.tagName))) { e.preventDefault(); V.acts.search(); }
  });
  V.chipH = {};
  V.acts.chip = function (el) { var k = el.dataset.k, i = k.indexOf('-'), h = V.chipH[k.slice(0, i)]; if (h) h(el, k.slice(i + 1)); };
  V.acts.cmpclear = function () { V.cmp.ids = []; V.cmpTray(); V.$$('[data-cmp]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); }); };
  V.acts.theme = function () { var d = D.documentElement, n = d.dataset.theme === 'dark' ? 'light' : 'dark'; d.dataset.theme = n; S.theme = n; V.persist(); V.$('#themeIc').textContent = n === 'dark' ? 'light_mode' : 'dark_mode'; };
  V.acts.more = function () {
    V.sheet('<h2 style="margin-bottom:14px">All of Pathways</h2><div class="grid g3 stag">' + V.NAV.map(function (n, i) { return '<button class="card click row" style="--i:' + i + '" data-go="' + n[0] + '"><span class="ic sm">' + V.ms(n[2]) + '</span><b>' + n[1] + '</b></button>'; }).join('') + '</div>');
  };
  var lastY = 0;
  g.addEventListener('scroll', function () { var y = g.scrollY; D.body.classList.toggle('hide', y > lastY + 6 && y > 200); if (y < lastY - 6) D.body.classList.remove('hide'); lastY = y; }, { passive: true });
  g.addEventListener('hashchange', V.render);
})(window);
