/* Syllabus hub, subject pages and the study progress they share with the reader.
 *
 * Progress lives on this device (localStorage "neb.study.v1"):
 *   docs[key] = { p: furthest point read 0-100, d: 1 when marked done, q: { mcqIndex: 1|0 },
 *                 t: last opened (ms), n: title, u: url }
 *   last      = key of the chapter opened most recently
 * key is "<grade>/<subject>/unit<N>", ".../bank<N>" or ".../guide".
 */
(function () {
  'use strict';

  var KEY = 'neb.study.v1';
  var GRADE = 'neb.syllabus.grade';

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || { docs: {} }; } catch (e) { return { docs: {} }; }
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* private mode */ } }
  var Study = {
    get: function (key) { return load().docs[key] || null; },
    put: function (key, patch) {
      var s = load(); s.docs = s.docs || {};
      var cur = s.docs[key] || {};
      Object.keys(patch).forEach(function (k) { cur[k] = patch[k]; });
      s.docs[key] = cur;
      if (patch.t) s.last = key;
      save(s);
      return cur;
    },
    all: function () { return load().docs || {}; },
    last: function () { var s = load(); return s.last ? { key: s.last, doc: (s.docs || {})[s.last] } : null; },
    /* a chapter counts as done when marked, or read to the end */
    isDone: function (d) { return !!(d && (d.d || d.p >= 96)); },
    score: function (d) {
      if (!d || !d.q) return null;
      var k = Object.keys(d.q); if (!k.length) return null;
      var right = k.filter(function (i) { return d.q[i]; }).length;
      return { right: right, total: k.length };
    }
  };
  window.NebStudy = Study;

  function read(key, fallback) { try { var v = JSON.parse(localStorage.getItem(key)); return v == null ? fallback : v; } catch (e) { return fallback; } }
  function write(key, v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fold(s) { return String(s || '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, ''); }
  function highlight(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
    });
    return out;
  }
  function slashFocus(input) {
    document.addEventListener('keydown', function (e) {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      var a = document.activeElement;
      if (a && (/INPUT|TEXTAREA|SELECT/.test(a.tagName) || a.isContentEditable)) return;
      e.preventDefault(); input.focus();
    });
  }
  function subjectStats(prefix, units) {
    var docs = Study.all(), done = 0, started = 0;
    Object.keys(docs).forEach(function (k) {
      if (k.indexOf(prefix + '/unit') !== 0) return;
      if (Study.isDone(docs[k])) done++; else if (docs[k].p > 3) started++;
    });
    return { done: Math.min(done, units), started: started, pct: units ? Math.round(100 * Math.min(done, units) / units) : 0 };
  }
  function ago(ms) {
    var m = Math.round((Date.now() - ms) / 60000);
    if (m < 2) return 'just now';
    if (m < 60) return m + ' min ago';
    var h = Math.round(m / 60); if (h < 24) return h + ' h ago';
    var d = Math.round(h / 24); return d === 1 ? 'yesterday' : d + ' days ago';
  }

  /* ------------------------------------------------------------ hub */
  function initHub(hub) {
    var buttons = hub.querySelectorAll('[data-syl-grade]');
    var panels = hub.querySelectorAll('[data-syl-panel]');
    var base = hub.getAttribute('data-base-url');

    function selectGrade(grade, push) {
      buttons.forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-syl-grade') === grade)); });
      panels.forEach(function (p) { p.hidden = p.getAttribute('data-syl-panel') !== grade; });
      write(GRADE, grade);
      if (push && history.replaceState) {
        var url = new URL(window.location.href);
        if (url.pathname.indexOf('/app/syllabus') === 0) url.pathname = base + grade + '/';
        else url.searchParams.set('grade', grade);
        history.replaceState(null, '', url.toString());
      }
    }
    buttons.forEach(function (b, i) {
      b.addEventListener('click', function () { selectGrade(b.getAttribute('data-syl-grade'), true); });
      b.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : null;
        if (n === null) return;
        var t = buttons[(n + buttons.length) % buttons.length]; t.focus(); t.click();
      });
    });
    var url = new URL(window.location.href);
    var explicit = url.searchParams.get('grade') || /\/app\/syllabus\/\d+\/?$/.test(url.pathname);
    var remembered = read(GRADE, null);
    if (!explicit && remembered && hub.querySelector('[data-syl-panel="' + remembered + '"]')) selectGrade(remembered, false);

    hub.querySelectorAll('[data-syl-card]').forEach(function (card) {
      var st = subjectStats(card.getAttribute('data-syl-card'), parseInt(card.getAttribute('data-units'), 10) || 0);
      var bar = card.querySelector('[data-syl-bar]');
      if (bar) bar.style.width = st.pct + '%';
      var lab = card.querySelector('[data-syl-pct]');
      if (lab) lab.textContent = st.done ? st.done + ' done' : (st.started ? st.started + ' started' : '');
      card.classList.toggle('is-started', !!(st.done || st.started));
    });

    var last = Study.last();
    var cont = hub.querySelector('[data-syl-continue]');
    if (last && last.doc && last.doc.u && cont) {
      cont.href = last.doc.u;
      cont.querySelector('[data-syl-continue-title]').textContent = last.doc.n || 'Your last chapter';
      cont.querySelector('[data-syl-continue-meta]').textContent = (last.doc.s ? last.doc.s + ' · ' : '') + Math.round(last.doc.p || 0) + '% read · ' + ago(last.doc.t || Date.now());
      cont.querySelector('[data-syl-continue-bar]').style.width = Math.round(last.doc.p || 0) + '%';
      cont.hidden = false;
    }
    initSearch(hub);
  }

  function initSearch(hub) {
    var input = hub.querySelector('[data-syl-search]');
    var box = hub.querySelector('[data-syl-results]');
    if (!input || !box) return;
    var active = -1, seq = 0, timer;
    var src = hub.getAttribute('data-search-url');
    var base = hub.getAttribute('data-base-url');
    function currentGrade() {
      var sel = hub.querySelector('[data-syl-grade][aria-selected="true"]');
      return sel ? sel.getAttribute('data-syl-grade') : '';
    }
    function render(q, data) {
      var terms = fold(q).split(/\s+/).filter(Boolean);
      active = -1;
      box.innerHTML = !data.results.length
        ? '<div class="syl-results-empty">Nothing found for “' + esc(q) + '”. Try another word.</div>'
        : data.results.map(function (r, i) {
          return '<a class="syl-result" role="option" id="syl-r' + i + '" href="' + base + r.grade + '/' + r.subject + '/unit-' + r.unit + '/">' +
            '<span class="syl-result-badge">Class ' + r.grade + '</span>' +
            '<span class="syl-result-title">' + highlight(r.name + ' · Unit ' + r.unit + ': ' + r.title, terms) + '</span>' +
            '<span class="syl-result-sub">' + highlight(r.match, terms) + '</span></a>';
        }).join('') + (data.total > data.results.length ? '<div class="syl-results-empty">The best ' + data.results.length + ' of ' + data.total + ' matches. Add a word to narrow down.</div>' : '');
      box.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    }
    input.addEventListener('input', function () {
      clearTimeout(timer);
      var q = input.value.trim();
      if (q.length < 2) { box.hidden = true; box.innerHTML = ''; input.setAttribute('aria-expanded', 'false'); return; }
      timer = setTimeout(function () {
        var mine = ++seq;
        fetch(src + '?q=' + encodeURIComponent(q) + '&grade=' + encodeURIComponent(currentGrade()), { credentials: 'same-origin' })
          .then(function (r) { return r.json(); })
          .then(function (data) { if (mine === seq) render(q, data); })
          .catch(function () { /* offline: keep the last results */ });
      }, 140);
    });
    input.addEventListener('keydown', function (e) {
      var items = box.querySelectorAll('.syl-result');
      if (e.key === 'Escape') { box.hidden = true; input.blur(); return; }
      if (!items.length || (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Enter')) return;
      if (e.key === 'Enter') { if (active >= 0) { e.preventDefault(); items[active].click(); } return; }
      e.preventDefault();
      active = (active + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
      items.forEach(function (el, i) { el.setAttribute('aria-selected', String(i === active)); });
      input.setAttribute('aria-activedescendant', 'syl-r' + active);
      items[active].scrollIntoView({ block: 'nearest' });
    });
    input.addEventListener('focus', function () { if (box.innerHTML && input.value.trim().length > 1) box.hidden = false; });
    document.addEventListener('click', function (e) { if (!input.parentNode.contains(e.target)) box.hidden = true; });
    slashFocus(input);
  }

  /* ------------------------------------------------------------ subject */
  function initSubject(root) {
    var prefix = root.getAttribute('data-st-subject');
    var units = Array.prototype.slice.call(root.querySelectorAll('[data-st-unit]'));
    var total = parseInt(root.getAttribute('data-st-units'), 10) || units.length;
    var state = { q: '', show: 'all', area: '' };

    function stateOf(no) { return Study.get(prefix + '/unit' + no); }

    function paint() {
      var done = 0;
      units.forEach(function (u) {
        var d = stateOf(u.getAttribute('data-st-unit'));
        var isDone = Study.isDone(d), p = d ? Math.round(d.p || 0) : 0, sc = Study.score(d);
        if (isDone) done++;
        u.classList.toggle('is-done', isDone);
        u.classList.toggle('is-started', !isDone && p > 3);
        u.querySelector('[data-st-unit-bar]').style.width = (isDone ? 100 : p) + '%';
        var label = isDone ? 'Done' : (p > 3 ? p + '%' : '');
        if (sc) label += (label ? ' · ' : '') + sc.right + '/' + sc.total;
        var s = u.querySelector('[data-st-state]');
        s.textContent = label;
        s.className = 'st-unit-state' + (isDone ? ' is-done' : '') + (sc && sc.right / sc.total < 0.6 ? ' is-weak' : '');
      });
      root.querySelectorAll('[data-st-doc]').forEach(function (b) {
        var d = Study.get(b.getAttribute('data-st-doc')), bar = b.querySelector('[data-st-unit-bar]');
        if (bar) bar.style.width = (Study.isDone(d) ? 100 : Math.round((d && d.p) || 0)) + '%';
      });
      root.querySelector('[data-st-done]').textContent = done;
      root.querySelector('[data-st-bar]').style.width = (total ? Math.round(100 * done / total) : 0) + '%';
      suggest();
    }

    /* the next thing to do: carry on with what is open, else the first chapter not done; and
       separately the chapter whose self-check went worst, if any went badly */
    function suggest() {
      var box = root.querySelector('[data-st-next]');
      var readable = units.filter(function (u) { return u.getAttribute('data-st-href'); });
      if (!readable.length) { box.hidden = true; return; }
      var open = null, first = null, weak = null, weakRatio = 1;
      readable.forEach(function (u) {
        var d = stateOf(u.getAttribute('data-st-unit'));
        if (!Study.isDone(d)) {
          if (d && d.p > 3 && (!open || (d.t || 0) > (open.d.t || 0))) open = { u: u, d: d };
          if (!first) first = u;
        }
        var sc = Study.score(d);
        if (sc && sc.total >= 2 && sc.right / sc.total < 0.6 && sc.right / sc.total < weakRatio) { weak = { u: u, sc: sc }; weakRatio = sc.right / sc.total; }
      });
      var main = open ? open.u : first;
      var kicker = root.querySelector('[data-st-next-kicker]');
      var a = root.querySelector('[data-st-next-main]');
      if (main) {
        var started = Object.keys(Study.all()).some(function (k) { return k.indexOf(prefix + '/') === 0; });
        kicker.textContent = open ? 'Continue' : (started ? 'Up next' : 'Start here');
        a.href = main.getAttribute('data-st-href');
        root.querySelector('[data-st-next-title]').textContent = 'Unit ' + main.getAttribute('data-st-unit') + ': ' + main.getAttribute('data-st-title');
        root.querySelector('[data-st-next-meta]').textContent = open
          ? Math.round(open.d.p) + '% read · about ' + Math.max(1, Math.round(main.getAttribute('data-st-min') * (1 - open.d.p / 100))) + ' min left'
          : main.getAttribute('data-st-min') + ' min read';
        a.hidden = false;
      } else {
        kicker.textContent = 'All chapters done';
        a.href = '#bank';
        root.querySelector('[data-st-next-title]').textContent = 'Test yourself with the question bank';
        root.querySelector('[data-st-next-meta]').textContent = 'Model sets in the board’s pattern, with keys';
      }
      var r = root.querySelector('[data-st-review]');
      if (weak && weak.u !== main) {
        r.href = weak.u.getAttribute('data-st-href') + '#questions';
        root.querySelector('[data-st-review-title]').textContent = 'Unit ' + weak.u.getAttribute('data-st-unit') + ': ' + weak.u.getAttribute('data-st-title');
        root.querySelector('[data-st-review-meta]').textContent = 'You got ' + weak.sc.right + ' of ' + weak.sc.total + ' self-check questions right';
        r.hidden = false;
      } else r.hidden = true;
      box.hidden = false;
    }

    function applyFilters() {
      var terms = fold(state.q).split(/\s+/).filter(Boolean), shown = 0;
      units.forEach(function (u) {
        var d = stateOf(u.getAttribute('data-st-unit')), isDone = Study.isDone(d);
        var ok = (!state.area || u.getAttribute('data-st-area') === state.area) &&
          (state.show === 'all' || (state.show === 'done') === isDone) &&
          terms.every(function (t) { return fold(u.getAttribute('data-st-text')).indexOf(t) !== -1; });
        u.hidden = !ok;
        if (ok) shown++;
      });
      root.querySelectorAll('[data-st-head]').forEach(function (h) {
        var any = false;
        for (var n = h.nextElementSibling; n && !n.hasAttribute('data-st-head'); n = n.nextElementSibling) if (!n.hidden) { any = true; break; }
        h.hidden = !any;
      });
      root.querySelector('[data-st-empty]').hidden = shown > 0;
    }
    var filter = root.querySelector('[data-st-filter]');
    if (filter) {
      var ft;
      filter.addEventListener('input', function () { clearTimeout(ft); ft = setTimeout(function () { state.q = filter.value.trim(); applyFilters(); }, 80); });
      slashFocus(filter);
    }
    root.querySelectorAll('[data-st-show]').forEach(function (chip, _, all) {
      chip.addEventListener('click', function () {
        all.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        state.show = chip.getAttribute('data-st-show'); applyFilters();
      });
    });
    var area = root.querySelector('[data-st-area]');
    if (area && area.tagName === 'SELECT') area.addEventListener('change', function () { state.area = area.value; applyFilters(); });

    units.forEach(function (u) {
      var btn = u.querySelector('[data-st-more]'), det = u.querySelector('.st-unit-detail');
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open)); det.hidden = !open; u.classList.toggle('is-open', open);
      });
    });

    /* tabs, deep-linkable as #chapters / #bank / #exam */
    var tabs = root.querySelectorAll('[data-st-tab]');
    function showTab(name, focus) {
      var hit = false;
      tabs.forEach(function (t) { var on = t.getAttribute('data-st-tab') === name; hit = hit || on; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; if (on && focus) t.focus(); });
      if (!hit) return;
      root.querySelectorAll('[data-st-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-st-panel') !== name; });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { var n = t.getAttribute('data-st-tab'); showTab(n); history.replaceState(null, '', n === 'chapters' ? location.pathname : '#' + n); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : null;
        if (n !== null) { var x = tabs[(n + tabs.length) % tabs.length]; x.click(); x.focus(); }
      });
    });
    function fromHash() {
      var h = location.hash.replace('#', '');
      var m = /^unit-(\d+)$/.exec(h);
      if (m) {
        showTab('chapters');
        var u = root.querySelector('[data-st-unit="' + m[1] + '"]');
        if (u) { u.querySelector('[data-st-more]').click(); u.scrollIntoView({ block: 'center' }); }
      } else if (h) showTab(h);
    }
    window.addEventListener('hashchange', fromHash);
    fromHash();
    paint();
    applyFilters();
    window.addEventListener('pageshow', paint);   // back from the reader: show the new progress
  }

  function boot() {
    document.querySelectorAll('[data-syl-hub]').forEach(initHub);
    document.querySelectorAll('[data-st-subject]').forEach(initSubject);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
