(function () {
  'use strict';

  var STORE = 'neb.syllabus.v1';
  var LAST = 'neb.syllabus.last';
  var GRADE = 'neb.syllabus.grade';
  var RING = 2 * Math.PI * 15.5;

  function read(key, fallback) {
    try { var v = JSON.parse(localStorage.getItem(key)); return v == null ? fallback : v; } catch (e) { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ }
  }
  function doneFor(id) {
    var all = read(STORE, {});
    return (all[id] && all[id].t) || [];
  }
  function saveDone(id, list) {
    var all = read(STORE, {});
    all[id] = { t: list, ts: Date.now() };
    write(STORE, all);
  }
  function setRing(el, pct) {
    if (!el) return;
    el.style.strokeDasharray = (RING * pct / 100).toFixed(2) + ' ' + RING.toFixed(2);
    el.classList.toggle('is-empty', !pct);
  }
  function pct(done, total) {
    return total ? Math.min(100, Math.round(100 * done / total)) : 0;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function fold(s) {
    return String(s || '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '');
  }
  function highlight(text, terms) {
    var out = escapeHtml(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }
  function slashFocus(input) {
    document.addEventListener('keydown', function (e) {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      var tag = (document.activeElement && document.activeElement.tagName) || '';
      if (/INPUT|TEXTAREA|SELECT/.test(tag) || document.activeElement.isContentEditable) return;
      e.preventDefault();
      input.focus();
    });
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
      if (push && window.history && history.replaceState) {
        var url = new URL(window.location.href);
        if (url.pathname.indexOf('/app/syllabus') === 0) url.pathname = base + grade + '/';
        else url.searchParams.set('grade', grade);
        history.replaceState(null, '', url.toString());
      }
    }
    buttons.forEach(function (b, i) {
      b.addEventListener('click', function () { selectGrade(b.getAttribute('data-syl-grade'), true); });
      b.addEventListener('keydown', function (e) {
        var next = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : null;
        if (next === null) return;
        var target = buttons[(next + buttons.length) % buttons.length];
        target.focus();
        target.click();
      });
    });
    var url = new URL(window.location.href);
    var explicit = url.searchParams.get('grade') || /\/app\/syllabus\/\d+\/?$/.test(url.pathname);
    var remembered = read(GRADE, null);
    if (!explicit && remembered && hub.querySelector('[data-syl-panel="' + remembered + '"]')) selectGrade(remembered, false);

    var progress = read(STORE, {});
    hub.querySelectorAll('[data-syl-card]').forEach(function (card) {
      var id = card.getAttribute('data-syl-card');
      var total = parseInt(card.getAttribute('data-topics'), 10) || 0;
      var p = pct(((progress[id] && progress[id].t) || []).length, total);
      setRing(card.querySelector('[data-syl-ring]'), p);
      var label = card.querySelector('[data-syl-pct]');
      if (label) label.textContent = p + '%';
      card.setAttribute('aria-label', card.querySelector('.syl-card-name').textContent + ', ' + p + '% done');
    });

    var last = read(LAST, null);
    var cont = hub.querySelector('[data-syl-continue]');
    if (last && last.url && cont) {
      var link = cont.querySelector('[data-syl-continue-link]');
      link.href = last.url;
      link.textContent = last.name;
      var lp = pct(((progress[last.id] && progress[last.id].t) || []).length, last.total || 0);
      cont.querySelector('[data-syl-continue-bar]').style.width = lp + '%';
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
      if (!data.results.length) {
        box.innerHTML = '<div class="syl-results-empty">Nothing found for “' + escapeHtml(q) + '”. Try another word.</div>';
      } else {
        box.innerHTML = data.results.map(function (r, i) {
          return '<a class="syl-result" role="option" id="syl-r' + i + '" href="' + base + r.grade + '/' + r.subject + '/#unit-' + r.unit + '">' +
            '<span class="syl-result-badge">Class ' + r.grade + '</span>' +
            '<span class="syl-result-title">' + highlight(r.name + ' · Unit ' + r.unit + ': ' + r.title, terms) + '</span>' +
            '<span class="syl-result-sub">' + highlight(r.match, terms) + '</span></a>';
        }).join('') + (data.total > data.results.length ? '<div class="syl-results-empty">Showing the best ' + data.results.length + ' of ' + data.total + ' matches — add a word to narrow down.</div>' : '');
      }
      box.hidden = false;
    }
    input.addEventListener('input', function () {
      clearTimeout(timer);
      var q = input.value.trim();
      if (q.length < 2) { box.hidden = true; return; }
      timer = setTimeout(function () {
        var mine = ++seq;
        fetch(src + '?q=' + encodeURIComponent(q) + '&grade=' + encodeURIComponent(currentGrade()), { credentials: 'same-origin' })
          .then(function (r) { return r.json(); })
          .then(function (data) { if (mine === seq) render(q, data); })
          .catch(function () { /* offline: keep the last results */ });
      }, 160);
    });
    input.addEventListener('keydown', function (e) {
      var items = box.querySelectorAll('.syl-result');
      if (e.key === 'Escape') { box.hidden = true; input.blur(); return; }
      if (!items.length || box.hidden) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        active = (active + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
        items.forEach(function (el, i) { el.setAttribute('aria-selected', String(i === active)); });
        input.setAttribute('aria-activedescendant', items[active].id);
        items[active].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        (items[active] || items[0]).click();
      }
    });
    input.addEventListener('focus', function () { if (box.innerHTML && input.value.trim().length > 1) box.hidden = false; });
    document.addEventListener('click', function (e) { if (!hub.querySelector('.syl-search').contains(e.target)) box.hidden = true; });
    slashFocus(input);
  }

  /* -------------------------------------------------------- subject */
  function initSubject(root) {
    var id = root.getAttribute('data-syl-subject');
    var total = parseInt(root.getAttribute('data-syl-topics'), 10) || 0;
    var checks = root.querySelectorAll('[data-syl-check]');
    var units = root.querySelectorAll('[data-syl-unit]');
    var toast = root.querySelector('[data-syl-toast]');
    var toastTimer;
    var state = { show: 'all', area: '', q: '' };

    write(LAST, { id: id, url: window.location.pathname, name: root.getAttribute('data-syl-name'), total: total });

    var done = doneFor(id);
    checks.forEach(function (c) { c.checked = done.indexOf(c.getAttribute('data-syl-check')) !== -1; });

    function say(msg) {
      if (!toast) return;
      toast.textContent = msg;
      toast.hidden = false;
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { toast.hidden = true; }, 2200);
    }
    function persist() {
      var list = [];
      checks.forEach(function (c) { if (c.checked) list.push(c.getAttribute('data-syl-check')); });
      saveDone(id, list);
      return list.length;
    }
    function refresh() {
      var n = 0;
      checks.forEach(function (c) { if (c.checked) n++; });
      var p = pct(n, total);
      root.querySelector('[data-syl-done-pct]').textContent = p + '%';
      var bar = root.querySelector('[data-syl-progress]');
      bar.setAttribute('aria-valuenow', String(p));
      bar.querySelector('span').style.width = p + '%';
      units.forEach(function (u) {
        var no = u.getAttribute('data-syl-unit');
        var boxes = u.querySelectorAll('[data-syl-check]');
        var k = 0;
        boxes.forEach(function (c) { if (c.checked) k++; });
        var up = pct(k, boxes.length);
        u.querySelector('[data-syl-unit-count]').textContent = k + '/' + boxes.length;
        setRing(u.querySelector('[data-syl-ring]'), up);
        var full = boxes.length > 0 && k === boxes.length;
        u.classList.toggle('is-done', full);
        var allBtn = u.querySelector('[data-syl-unit-all]');
        if (allBtn) allBtn.textContent = full ? 'Clear unit' : 'Mark all done';
        var toc = root.querySelector('[data-syl-toc="' + no + '"]');
        if (toc) { toc.classList.toggle('is-done', full); toc.classList.toggle('is-part', k > 0 && !full); }
        var seg = root.querySelector('[data-syl-seg="' + no + '"]');
        if (seg) seg.classList.toggle('is-done', full);
      });
      applyFilters();
    }
    checks.forEach(function (c) {
      c.addEventListener('change', function () {
        var before = root.querySelectorAll('.syl-unit.is-done').length;
        persist();
        refresh();
        var after = root.querySelectorAll('.syl-unit.is-done').length;
        if (after > before) say('Unit complete — well done!');
      });
    });
    root.querySelectorAll('[data-syl-unit-all]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var unit = btn.closest('[data-syl-unit]');
        var boxes = unit.querySelectorAll('[data-syl-check]');
        var all = Array.prototype.every.call(boxes, function (c) { return c.checked; });
        boxes.forEach(function (c) { c.checked = !all; });
        persist();
        refresh();
        say(all ? 'Unit cleared' : 'Unit marked as done');
      });
    });

    function applyFilters() {
      var terms = fold(state.q).split(/\s+/).filter(Boolean);
      var visibleUnits = 0;
      units.forEach(function (u) {
        var areaOk = !state.area || u.getAttribute('data-area') === state.area;
        var title = fold(u.querySelector('.syl-unit-title').textContent);
        var titleHit = terms.length && terms.every(function (t) { return title.indexOf(t) !== -1; });
        var shown = 0;
        u.querySelectorAll('[data-syl-topic]').forEach(function (li) {
          var text = li.querySelector('.syl-topic-text');
          if (!text.dataset.raw) text.dataset.raw = text.textContent;
          var raw = text.dataset.raw;
          var checked = li.querySelector('input').checked;
          var showOk = state.show === 'all' || (state.show === 'done' ? checked : !checked);
          var qOk = !terms.length || titleHit || terms.every(function (t) { return fold(raw).indexOf(t) !== -1; });
          var visible = showOk && qOk;
          li.classList.toggle('is-hidden', !visible);
          text.innerHTML = terms.length && visible ? highlight(raw, terms) : escapeHtml(raw);
          if (visible) shown++;
        });
        var visibleUnit = areaOk && (shown > 0 || (!terms.length && state.show === 'all'));
        u.classList.toggle('is-hidden', !visibleUnit);
        if (visibleUnit) visibleUnits++;
        if (terms.length && visibleUnit) u.querySelector('details').open = true;
      });
      var empty = root.querySelector('[data-syl-empty]');
      if (empty) empty.hidden = visibleUnits > 0;
    }

    var filter = root.querySelector('[data-syl-filter]');
    if (filter) {
      var t;
      filter.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () { state.q = filter.value.trim(); applyFilters(); }, 80);
      });
      filter.addEventListener('keydown', function (e) { if (e.key === 'Escape') { filter.value = ''; state.q = ''; applyFilters(); } });
      slashFocus(filter);
    }
    function chipGroup(attr, key) {
      var chips = root.querySelectorAll('[' + attr + ']');
      chips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
          state[key] = chip.getAttribute(attr);
          applyFilters();
        });
      });
    }
    chipGroup('data-syl-show', 'show');
    chipGroup('data-syl-area', 'area');

    function setAll(open) { root.querySelectorAll('.syl-unit details').forEach(function (d) { d.open = open; }); }
    var ex = root.querySelector('[data-syl-expand]');
    if (ex) ex.addEventListener('click', function () { setAll(true); });
    var co = root.querySelector('[data-syl-collapse]');
    if (co) co.addEventListener('click', function () { setAll(false); });
    var pr = root.querySelector('[data-syl-print]');
    if (pr) pr.addEventListener('click', function () { setAll(true); window.print(); });
    window.addEventListener('beforeprint', function () { setAll(true); });
    var rs = root.querySelector('[data-syl-reset]');
    if (rs) rs.addEventListener('click', function () {
      if (!window.confirm('Clear every tick for this subject?')) return;
      checks.forEach(function (c) { c.checked = false; });
      persist();
      refresh();
      say('Progress cleared');
    });

    function openHash() {
      var m = /^#unit-(\d+)$/.exec(window.location.hash);
      if (!m) return;
      var u = root.querySelector('[data-syl-unit="' + m[1] + '"]');
      if (u) { u.querySelector('details').open = true; u.scrollIntoView({ block: 'start' }); }
    }
    window.addEventListener('hashchange', openHash);
    root.querySelectorAll('a[href^="#unit-"]').forEach(function (a) {
      a.addEventListener('click', function () {
        var u = root.querySelector(a.getAttribute('href'));
        if (u) u.querySelector('details').open = true;
      });
    });

    var top = root.querySelector('[data-syl-top]');
    if (top) {
      var segs = Array.prototype.slice.call(root.querySelectorAll('[data-syl-seg]'));
      segs.sort(function (a, b) { return parseFloat(b.style.flexGrow) - parseFloat(a.style.flexGrow); });
      top.innerHTML = segs.slice(0, 3).map(function (s) {
        var parts = s.getAttribute('title').split(' · ');
        return '<li><span>Heaviest: <strong>' + escapeHtml(parts[0] + ' · ' + parts[1]) + '</strong></span><span>' + escapeHtml(parts[2]) + '</span></li>';
      }).join('');
    }

    if ('IntersectionObserver' in window) {
      var tocLinks = root.querySelectorAll('[data-syl-toc]');
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var no = en.target.getAttribute('data-syl-unit');
          tocLinks.forEach(function (l) { l.classList.toggle('is-current', l.getAttribute('data-syl-toc') === no); });
        });
      }, { rootMargin: '-140px 0px -60% 0px' });
      units.forEach(function (u) { io.observe(u); });
    }

    refresh();
    openHash();
  }

  function boot() {
    document.querySelectorAll('[data-syl-hub]').forEach(initHub);
    document.querySelectorAll('[data-syl-subject]').forEach(initSubject);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
