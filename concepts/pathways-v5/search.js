/* Pathways v5 search: one box for courses, colleges, careers, exams, countries, grants, guides and answers. Ctrl K or /. */
(function () {
  'use strict';
  var V = window.V, PW = V.PW, M = V.ms, E = V.esc, IDX = null, cur = 0;
  var GROUPS = [['course', 'Courses', 'school'], ['college', 'Colleges', 'apartment'], ['career', 'Careers', 'work'], ['exam', 'Exams', 'quiz'], ['country', 'Countries', 'public'], ['schol', 'Scholarships', 'workspace_premium'], ['guide', 'Guides', 'checklist'], ['faq', 'Answers', 'help']];
  function build() {
    IDX = [];
    PW.routes.forEach(function (r) { IDX.push({ k: 'course', t: r.name, s: r.kind + ', ' + r.years, x: (r.skills || []).join(' '), go: 'course/' + r.id }); });
    PW.providers.forEach(function (p) { IDX.push({ k: 'college', t: p.name, s: p.place + ', ' + p.district, x: p.kind, go: 'college/' + p.id }); });
    PW.careers.forEach(function (c) { IDX.push({ k: 'career', t: c.name, s: 'Starts ' + V.range(c.salary.entry), x: (c.skills || []).join(' '), go: 'career/' + c.id }); });
    PW.govt.forEach(function (g) { IDX.push({ k: 'exam', t: g.name, s: g.body, x: g.level, go: 'exam/' + g.id }); });
    PW.abroad.forEach(function (a) { IDX.push({ k: 'country', t: a.country, s: a.intakes, x: a.fields.join(' '), go: 'country/' + a.id }); });
    PW.scholarships.forEach(function (s) { IDX.push({ k: 'schol', t: s.name, s: s.by, x: s.covers, act: s.id }); });
    PW.guides.forEach(function (g) { IDX.push({ k: 'guide', t: g.name, s: g.cat, x: '', go: 'guide/' + g.id }); });
    PW.faq.forEach(function (f) { IDX.push({ k: 'faq', t: f.q, s: '', x: f.a, go: 'help' }); });
    IDX.forEach(function (i) { i.l = (i.t + ' ' + i.s).toLowerCase(); i.lx = (i.x || '').toLowerCase(); });
  }
  function hl(t, q) { var i = t.toLowerCase().indexOf(q); return i < 0 || !q ? E(t) : E(t.slice(0, i)) + '<mark class="mk-hl">' + E(t.slice(i, i + q.length)) + '</mark>' + E(t.slice(i + q.length)); }
  function find(q) {
    q = q.trim().toLowerCase(); var by = {}; if (!q) return null; var words = q.split(/\s+/);
    IDX.forEach(function (i) {
      var s = 0; words.forEach(function (w) { var p = i.l.indexOf(w); if (p < 0) { if (i.lx.indexOf(w) >= 0) s += 1; else s = -99; } else s += p === 0 ? 8 : i.l.charAt(p - 1) === ' ' ? 5 : 3; });
      if (s > 0) (by[i.k] = by[i.k] || []).push([s, i]);
    });
    return by;
  }
  function render(q) {
    var by = find(q), box = V.$('#sres'), h = '', n = 0;
    if (!by) { h = '<div class="gh">Try</div>' + [['Nursing', 'course'], ['Kathmandu', 'college'], ['Software developer', 'career'], ['Lok Sewa', 'exam'], ['Australia', 'country'], ['Passport', 'guide']].map(function (s) { return '<button class="hit" data-act="sfill" data-q="' + s[0] + '">' + M('north_west', 'sm') + '<span>' + s[0] + '</span></button>'; }).join(''); }
    else {
      GROUPS.forEach(function (g) {
        var a = (by[g[0]] || []).sort(function (x, y) { return y[0] - x[0]; }).slice(0, g[0] === 'faq' ? 3 : 4); if (!a.length) return;
        h += '<div class="gh">' + g[1] + '</div>' + a.map(function (x) { var i = x[1]; n++; return '<button class="hit" data-sgo="' + (i.go || '') + '" data-sact="' + (i.act || '') + '"><span class="ic sm">' + M(g[2], 'sm') + '</span><span class="grow"><b class="sm">' + hl(i.t.length > 90 ? i.t.slice(0, 90) + '...' : i.t, q.trim().toLowerCase()) + '</b>' + (i.s ? '<span class="xs mut" style="display:block">' + E(i.s) + '</span>' : '') + '</span>' + M('chevron_right', 'sm') + '</button>'; }).join('');
      });
      if (!n) h = '<div class="empty">' + M('search_off') + '<p>No match for "' + E(q) + '". Try a course, a district or a country.</p></div>';
    }
    box.innerHTML = h; cur = 0; sel();
  }
  function sel() { V.$$('#sres .hit').forEach(function (b, i) { b.classList.toggle('sel', i === cur && !!b.dataset.sgo + !!b.dataset.sact > 0); }); }
  V.acts.sfill = function (el) { var i = V.$('#sq'); i.value = el.dataset.q; render(i.value); i.focus(); };
  V.acts.search = function () {
    if (!IDX) build();
    var s = V.sheet('<div class="srch"><label class="fld"><span class="ms">search</span><input id="sq" type="search" placeholder="Search everything" autocomplete="off"><button class="ib" data-act="sclose" aria-label="Close" style="width:32px;height:32px"><span class="ms sm">close</span></button></label><div id="sres" style="margin-top:6px"></div></div>');
    s.style.alignItems = 'flex-start'; s.firstChild.style.marginTop = '8vh'; s.firstChild.style.borderRadius = 'var(--r4)';
    var i = V.$('#sq'); i.focus(); render('');
    i.addEventListener('input', function () { render(i.value); });
    i.addEventListener('keydown', function (e) {
      var hits = V.$$('#sres .hit[data-sgo]'); if (!hits.length) return;
      if (e.key === 'ArrowDown') { cur = Math.min(hits.length - 1, cur + 1); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { cur = Math.max(0, cur - 1); e.preventDefault(); }
      else if (e.key === 'Enter') { hits[cur].click(); return; } else return;
      V.$$('#sres .hit').forEach(function (b) { b.classList.remove('sel'); }); hits[cur].classList.add('sel'); hits[cur].scrollIntoView({ block: 'nearest' });
    });
  };
  V.acts.sclose = function () { V.closeSheet(); };
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-sgo]'); if (!b) return; e.stopPropagation(); V.closeSheet();
    if (b.dataset.sact) V.acts.schol({ dataset: { id: b.dataset.sact } }); else V.go(b.dataset.sgo);
  }, true);
})();
