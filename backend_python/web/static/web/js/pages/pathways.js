/* Pathways (web). One dataset from /api/pathways/, hash routes, no framework.
   Files: pathways.js (core, search, saved), pathways-level.js (levels and course page),
   pathways-more.js (colleges, abroad, Lok Sewa, questions, saved), pathways-lab.js (Course Lab match).
   The matching and the numbers mirror the Android screens (PwMatch.kt, PwInsight.kt). */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var PW = window.PW = { $: $, views: {}, state: { district: '' }, D: null };
  try { PW.state.district = localStorage.getItem('pw-district') || ''; } catch (e) {}
  PW.districts = JSON.parse($('pw-districts').textContent);
  PW.GROUPS = { school: 'School', tech: 'Engineering and IT', sci: 'Science', health: 'Health sciences', biz: 'Business', arts: 'Arts and media', edu: 'Education', law: 'Law', ag: 'Agriculture', gov: 'Government', abroad: 'Abroad' };
  var view = PW.view = $('pw-view'), nav = $('pw-nav');

  PW.h = function (tag, attrs, kids) {
    var el = document.createElement(tag);
    for (var k in (attrs || {})) {
      var v = attrs[k];
      if (v == null || v === false) continue;
      if (k === 'text') el.textContent = v; else if (k === 'class') el.className = v;
      else if (k === 'w') el.style.setProperty('--w', v); else if (k === 'i') el.style.setProperty('--i', v);
      else el.setAttribute(k, v === true ? '' : v);
    }
    (kids || []).forEach(function (c) { if (c != null && c !== false) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  };
  var h = PW.h;
  PW.icon = function (n) { return h('span', { class: 'material-symbols-outlined', 'aria-hidden': 'true', text: n }); };
  function trim(x) { return (Math.round(x * 10) / 10).toString().replace(/\.0$/, ''); }
  PW.money = function (n) {
    if (n >= 10000000) return trim(n / 10000000) + ' crore';
    if (n >= 100000) return trim(n / 100000) + ' lakh';
    if (n >= 1000) return trim(n / 1000) + 'k';
    return String(n);
  };
  PW.npr = function (r) { return r[1] === 0 ? 'Free' : 'NPR ' + PW.money(r[0]) + ' to ' + PW.money(r[1]); };
  PW.tone = function (i) { return ['b', 'p', 'y', 'l'][i % 4]; };
  PW.by = function (list) { var m = {}; list.forEach(function (x) { m[x.id] = x; }); return m; };

  /* ---- numbers, all derived from the careers a route links to ---- */
  function avg(a) { return a.length ? a.reduce(function (s, x) { return s + x; }, 0) / a.length : 0; }
  PW.careersOf = function (r) { return r.careers.map(function (c) { return PW.careers[c]; }).filter(Boolean); };
  PW.demand = function (r) { return avg(PW.careersOf(r).map(function (c) { return c.demand; })); };
  PW.compet = function (r) { return avg(PW.careersOf(r).map(function (c) { return c.competition; })); };
  PW.word = function (v, low) { return v <= 0 ? 'Open' : v >= 3.7 ? 'High' : v >= 2.7 ? 'Medium' : low; };
  PW.pay = function (r) {
    var cs = PW.careersOf(r);
    if (!cs.length) return null;
    return [Math.round(avg(cs.map(function (c) { return c.salary.entry[0]; }))), Math.round(avg(cs.map(function (c) { return c.salary.entry[1]; })))];
  };
  PW.yearsNum = function (t) {
    var m = /\d+(\.\d+)?/.exec(t); if (!m) return 4;
    return /month/i.test(t) ? parseFloat(m[0]) / 12 : parseFloat(m[0]);
  };
  PW.code = function (name) {
    var m = /\(([A-Za-z.]{2,6})\)/.exec(name); if (m) return m[1].toUpperCase();
    var head = name.split('(')[0].trim(), first = head.split(/[ \/]/)[0];
    if (first.length >= 2 && first.length <= 5 && /[A-Z]/.test(first)) return first.toUpperCase();
    var caps = head.split(' ').filter(function (w) { return /^[A-Z]/.test(w); }).slice(0, 3).map(function (w) { return w[0]; }).join('');
    return caps || head.slice(0, 2).toUpperCase();
  };
  PW.stageWord = function (label) { return label.replace(/^After /, 'After ').replace('After Class 8', 'After 8').replace('After Bachelor', "Bachelor's"); };

  /* ---- saved (courses, countries, jobs), kept in this browser ---- */
  var saved = [];
  try { saved = JSON.parse(localStorage.getItem('pw-saved') || '[]'); } catch (e) {}
  PW.saved = {
    has: function (k) { return saved.indexOf(k) >= 0; },
    all: function () { return saved.slice(); },
    toggle: function (k) {
      var i = saved.indexOf(k);
      if (i >= 0) saved.splice(i, 1); else saved.push(k);
      try { localStorage.setItem('pw-saved', JSON.stringify(saved)); } catch (e) {}
      $('pw-saved').classList.toggle('on', saved.length > 0);
      return i < 0;
    }
  };
  PW.saveBtn = function (key, label) {
    var b = h('button', { class: 'pw-round sm', type: 'button', 'aria-label': 'Save ' + label, 'aria-pressed': PW.saved.has(key) }, [PW.icon(PW.saved.has(key) ? 'bookmark_added' : 'bookmark')]);
    b.addEventListener('click', function () {
      var on = PW.saved.toggle(key);
      b.setAttribute('aria-pressed', on); b.firstChild.textContent = on ? 'bookmark_added' : 'bookmark';
    });
    return b;
  };

  /* ---- shared small pieces ---- */
  PW.bar = function (v, max, tone) { return h('span', { class: 'pw-bar', 'data-t': tone || 'b' }, [h('i', { w: Math.max(4, Math.min(100, v / max * 100)) + '%' })]); };
  PW.chip = function (text, on, attrs) { var a = attrs || {}; a.class = 'pw-chip'; a.type = 'button'; a['aria-pressed'] = !!on; a.text = text; return h('button', a); };
  PW.sectionTitle = function (t, right) { return h('div', { class: 'pw-sh' }, [h('h2', { text: t })].concat(right ? [right] : [])); };
  PW.empty = function (t) { return h('p', { class: 'pw-empty', text: t }); };
  PW.head = function (title, sub, back) {
    var kids = [];
    if (back) kids.push(h('a', { class: 'pw-round sm', href: back, 'aria-label': 'Back' }, [PW.icon('arrow_back')]));
    kids.push(h('div', {}, [h('h2', { text: title })].concat(sub ? [h('p', { text: sub })] : [])));
    return h('div', { class: 'pw-head' }, kids);
  };

  /* ---- search: every word must appear in the name, prefix hits first, so nothing unrelated shows ---- */
  function pick(items, text, words, limit) {
    var out = [];
    items.forEach(function (x) {
      var t = text(x).toLowerCase();
      if (!words.every(function (w) { return t.indexOf(w) >= 0; })) return;
      out.push([x, t.indexOf(words[0]) === 0 ? 0 : t.indexOf(' ' + words[0]) >= 0 ? 1 : 2]);
    });
    return out.sort(function (a, b) { return a[1] - b[1]; }).slice(0, limit).map(function (p) { return p[0]; });
  }
  PW.search = function (q) {
    var words = q.toLowerCase().split(/[ ,]+/).filter(function (w) { return w.length >= 2; });
    if (!words.length || !PW.D) return [];
    var D = PW.D, out = [];
    pick(D.routes, function (r) { return r.name + ' ' + (PW.GROUPS[r.group] || ''); }, words, 7).forEach(function (r) { out.push({ t: 'Course', n: r.name, s: r.years + ', ' + r.kind, go: '#levels/' + r.stage + '/' + r.id, g: 'school' }); });
    pick(D.careers, function (c) { return c.name; }, words, 5).forEach(function (c) {
      var r = D.routes.filter(function (x) { return x.careers.indexOf(c.id) >= 0; })[0];
      if (r) out.push({ t: 'Career', n: c.name, s: 'Via ' + r.name, go: '#levels/' + r.stage + '/' + r.id, g: 'work' });
    });
    pick(D.providers, function (p) { return p.name + ' ' + p.district + ' ' + p.place; }, words, 6).forEach(function (p) { out.push({ t: 'College', n: p.name, s: p.place + ', ' + p.district, go: '#colleges', pv: p.district, g: 'apartment' }); });
    pick(D.govt || [], function (g) { return g.name + ' ' + g.body; }, words, 3).forEach(function (g) { out.push({ t: 'Lok Sewa', n: g.name, s: g.level, go: '#govt/' + g.id, g: 'account_balance' }); });
    return out;
  };
  var q = $('pw-q'), hits = $('pw-hits'), timer;
  function drawHits() {
    var list = PW.search(q.value);
    hits.textContent = '';
    if (!q.value.trim()) { hits.hidden = true; return; }
    if (!list.length) hits.appendChild(h('p', { class: 'pw-empty', text: 'Nothing matches that. Try one word, like nursing or law.' }));
    list.forEach(function (x) {
      var b = h('button', { class: 'pw-hit', type: 'button' }, [PW.icon(x.g), h('span', {}, [h('b', { text: x.n }), h('small', { text: x.t + ', ' + x.s })])]);
      b.addEventListener('click', function () {
        if (x.pv) { PW.state.district = x.pv; try { localStorage.setItem('pw-district', x.pv); } catch (e) {} }
        q.value = ''; hits.hidden = true; location.hash = x.go;
      });
      hits.appendChild(b);
    });
    hits.hidden = false;
  }
  q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(drawHits, 110); });
  q.addEventListener('keydown', function (e) { if (e.key === 'Escape') { q.value = ''; hits.hidden = true; } });
  document.addEventListener('click', function (e) { if (!e.target.closest('.pw-search')) hits.hidden = true; });
  $('pw-saved').addEventListener('click', function () { location.hash = '#saved'; });

  /* ---- sections and routing ---- */
  var SECTIONS = [['levels', 'Pathways', 'alt_route'], ['lab', 'Course Lab', 'science'], ['colleges', 'Colleges', 'apartment'], ['abroad', 'Abroad', 'public'], ['govt', 'Lok Sewa', 'account_balance'], ['faq', 'Questions', 'help']];
  PW.SECTIONS = SECTIONS;
  function drawNav(tab) {
    nav.textContent = '';
    SECTIONS.forEach(function (s) {
      var a = h('a', { class: 'pw-nav-i', href: '#' + s[0], 'aria-current': tab === s[0] ? 'page' : null }, [PW.icon(s[2]), h('span', { text: s[1] })]);
      nav.appendChild(a);
    });
  }
  PW.route = function () {
    var raw = location.hash.replace(/^#/, ''), parts;
    var legacy = /^route=(.+)$/.exec(raw);
    if (legacy) { var lr = PW.routes[legacy[1]]; parts = lr ? ['levels', lr.stage, lr.id] : ['levels']; }
    else if (/^(after8|after10|after12|afterbach)$/.test(raw)) parts = ['levels', raw];
    else parts = raw.split('/').filter(Boolean);
    var tab = parts[0] || 'levels';
    if (!PW.views[tab]) tab = 'levels';
    var prev = view.getAttribute('data-tab');
    view.setAttribute('data-tab', tab);
    drawNav(tab === 'saved' ? '' : tab);
    var keep = view.querySelector('.pw-list'); PW.keepScroll = keep ? keep.scrollTop : 0;
    view.textContent = '';
    view.classList.remove('in'); void view.offsetWidth; view.classList.add('in');
    PW.views[tab].apply(null, parts.slice(1));
    if (prev !== tab || parts.length < 3) window.scrollTo({ top: 0 });
  };
  window.addEventListener('hashchange', function () { if (PW.D) PW.route(); });
  PW.setDistrict = function (d) { PW.state.district = d; try { localStorage.setItem('pw-district', d); } catch (e) {} };
  $('pw-saved').classList.toggle('on', saved.length > 0);

  // runs once the data is here and the last view file (pathways-lab.js) has registered itself
  PW.tryStart = function () { if (PW.D && PW.ready) PW.route(); };
  fetch(view.dataset.src, { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (data) {
    var D = PW.D = data;
    PW.routes = PW.by(D.routes); PW.careers = PW.by(D.careers); PW.providers = PW.by(D.providers);
    PW.schol = PW.by(D.scholarships); PW.abroadBy = PW.by(D.abroad); PW.govtBy = PW.by(D.govt || []);
    PW.stages = D.stages;
    PW.tryStart();
  }).catch(function () {
    view.textContent = '';
    view.appendChild(PW.empty('Could not load Pathways. Check your connection and reload.'));
  });
})();
