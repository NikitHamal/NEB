/* The chapter reader: KaTeX for the maths, tappable multiple-choice questions checked against
 * the book's key, folded answers, a contents rail that follows the reading, and progress
 * (how far read, done, self-check score) saved through window.NebStudy (syllabus.js). */
(function () {
  'use strict';
  var root = document.querySelector('[data-rd-key]');
  if (!root || !window.NebStudy) return;
  var Study = window.NebStudy;
  var key = root.getAttribute('data-rd-key');
  var body = root.querySelector('[data-rd-body]');
  var bar = document.querySelector('[data-rd-bar]');
  var SIZE = 'neb.study.size';

  Study.put(key, { t: Date.now(), n: root.getAttribute('data-rd-title'), u: location.pathname, s: root.getAttribute('data-rd-label') });

  /* ---------- maths: typeset as it comes into view, a screenful at a time ---------- */
  function typeset(el) {
    if (el.getAttribute('data-done')) return;
    el.setAttribute('data-done', '1');
    try {
      window.katex.render(el.textContent, el, { throwOnError: false, displayMode: el.classList.contains('d'), strict: 'ignore', trust: false, output: 'html' });
    } catch (e) { el.classList.add('m-raw'); }
  }
  var maths = body.querySelectorAll('.m');
  if (window.katex) {
    if ('IntersectionObserver' in window && maths.length > 60) {
      var mio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { typeset(en.target); mio.unobserve(en.target); } });
      }, { rootMargin: '600px 0px' });
      maths.forEach(function (m) { mio.observe(m); });
    } else maths.forEach(typeset);
  } else maths.forEach(function (m) { m.classList.add('m-raw'); });

  /* ---------- multiple choice ---------- */
  var mcqs = Array.prototype.slice.call(body.querySelectorAll('ol.mcq > li[data-key], .mcq-p[data-key]'));
  var saved = (Study.get(key) || {}).q || {};
  function scoreText() {
    var box = root.querySelector('[data-rd-score]');
    var k = Object.keys((Study.get(key) || {}).q || {});
    if (!mcqs.length || !k.length) { box.hidden = true; return; }
    var right = k.filter(function (i) { return Study.get(key).q[i]; }).length;
    box.hidden = false;
    root.querySelector('[data-rd-score-text]').textContent = right + ' of ' + k.length + ' right';
    root.querySelector('[data-rd-score-note]').textContent = k.length < mcqs.length
      ? ' · ' + (mcqs.length - k.length) + ' multiple-choice questions still to try'
      : (right / k.length >= 0.8 ? ' · well done' : ' · read the sections you missed again');
  }
  function mark(li, choice, store) {
    var keyLetter = li.getAttribute('data-key');
    li.classList.add('is-answered');
    li.querySelectorAll('.opt').forEach(function (o) {
      var l = o.getAttribute('data-opt');
      o.classList.toggle('is-right', l === keyLetter);
      o.classList.toggle('is-wrong', l === choice && choice !== keyLetter);
      o.setAttribute('aria-disabled', 'true');
    });
    li.classList.toggle('got-it', choice === keyLetter);
    if (store) {
      var q = (Study.get(key) || {}).q || {};
      q[li.getAttribute('data-q')] = choice === keyLetter ? 1 : 0;
      Study.put(key, { q: q });
      scoreText();
    }
  }
  mcqs.forEach(function (li, i) {
    li.setAttribute('data-q', i);
    li.querySelectorAll('.opt').forEach(function (o) {
      var letter = (o.querySelector('i') || {}).textContent;
      if (!o.getAttribute('data-opt')) o.setAttribute('data-opt', (letter || '').trim());
      o.setAttribute('role', 'button');
      o.tabIndex = 0;
      function pick() { if (!li.classList.contains('is-answered')) mark(li, o.getAttribute('data-opt'), true); }
      o.addEventListener('click', pick);
      o.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
    });
    if (saved[i] !== undefined) mark(li, saved[i] ? li.getAttribute('data-key') : '', false);
  });
  if (mcqs.length) {
    var tip = document.createElement('p');
    tip.className = 'rd-tip';
    tip.textContent = 'Tap an option to check it. Worked answers stay folded until you open them; your score is kept on this device.';
    var first = mcqs[0].tagName === 'LI' ? mcqs[0].parentNode : mcqs[0];
    first.parentNode.insertBefore(tip, first);
    var redo = document.createElement('button');
    redo.type = 'button'; redo.className = 'rd-link'; redo.textContent = 'Try the questions again';
    redo.addEventListener('click', function () {
      Study.put(key, { q: {} });
      mcqs.forEach(function (li) { li.classList.remove('is-answered', 'got-it'); li.querySelectorAll('.opt').forEach(function (o) { o.className = 'opt'; o.removeAttribute('aria-disabled'); }); });
      scoreText();
    });
    root.querySelector('[data-rd-score]').appendChild(redo);
  }
  scoreText();

  /* ---------- answers ---------- */
  var answers = body.querySelectorAll('details.ans');
  var allBtn = root.querySelector('[data-rd-answers]');
  if (!answers.length) allBtn.hidden = true;
  var allLabel = allBtn.querySelector('[data-rd-answers-label]');
  allBtn.addEventListener('click', function () {
    var open = allBtn.getAttribute('aria-pressed') !== 'true';
    allBtn.setAttribute('aria-pressed', String(open));
    if (allLabel) allLabel.textContent = open ? 'Hide answers' : 'Show answers';
    answers.forEach(function (d) { d.open = open; });
  });
  window.addEventListener('beforeprint', function () { answers.forEach(function (d) { d.open = true; }); });
  var firstQs = body.querySelector('h2.qs');
  if (firstQs && !document.getElementById('questions')) {
    var anchor = document.createElement('span'); anchor.id = 'questions'; firstQs.parentNode.insertBefore(anchor, firstQs);
  }

  /* ---------- figures open full screen: pinch, wheel or double-tap to zoom, drag to pan ---------- */
  var view = null, vimg = null, zs = 1, zx = 0, zy = 0, W = 0, H = 0, bw = 0, bh = 0, gest = null, lastTap = 0, moved = false, opener = null;
  function zApply() { vimg.style.transform = 'translate(' + zx + 'px,' + zy + 'px) scale(' + zs + ')'; }
  function zClamp() { var mx = Math.max(0, (bw * zs - W) / 2), my = Math.max(0, (bh * zs - H) / 2); zx = Math.max(-mx, Math.min(mx, zx)); zy = Math.max(-my, Math.min(my, zy)); }
  function zMeasure() { var st = view.firstChild; W = st.clientWidth; H = st.clientHeight; var t = vimg.style.transform; vimg.style.transform = 'none'; bw = vimg.offsetWidth; bh = vimg.offsetHeight; vimg.style.transform = t; }
  function zoomAt(ns, px, py) {
    var r = view.firstChild.getBoundingClientRect(), cx = r.left + W / 2, cy = r.top + H / 2;
    var ux = (px - cx - zx) / zs, uy = (py - cy - zy) / zs;
    zs = Math.max(1, Math.min(6, ns)); zx = px - cx - ux * zs; zy = py - cy - uy * zs;
    if (zs === 1) { zx = 0; zy = 0; }
    zClamp(); zApply();
  }
  function zClose() {
    if (!view) return;
    view.remove(); view = null; vimg = null; document.body.style.overflow = '';
    if (opener) opener.focus();
  }
  function zOpen(src, alt, cap, from) {
    opener = from;
    view = document.createElement('div'); view.className = 'rd-zoom'; view.setAttribute('role', 'dialog'); view.setAttribute('aria-modal', 'true'); view.setAttribute('aria-label', alt || 'Figure');
    var st = document.createElement('div'); st.className = 'rd-zoom-stage';
    vimg = document.createElement('img'); vimg.src = src; vimg.alt = alt || ''; st.appendChild(vimg); view.appendChild(st);
    var x = document.createElement('button'); x.type = 'button'; x.className = 'rd-zoom-x'; x.setAttribute('aria-label', 'Close');
    x.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">close</span>'; x.addEventListener('click', zClose); view.appendChild(x);
    if (cap) { var c = document.createElement('p'); c.className = 'rd-zoom-cap'; c.textContent = cap; view.appendChild(c); }
    var hint = document.createElement('span'); hint.className = 'rd-zoom-hint'; hint.textContent = 'Scroll, pinch or double-click to zoom · Esc to close'; view.appendChild(hint);
    setTimeout(function () { hint.classList.add('is-gone'); }, 2200);
    document.body.appendChild(view); document.body.style.overflow = 'hidden';
    zs = 1; zx = 0; zy = 0; vimg.onload = zMeasure; if (vimg.complete) zMeasure();
    x.focus();
    st.addEventListener('wheel', function (e) { e.preventDefault(); zoomAt(zs * Math.exp(-e.deltaY * 0.0022), e.clientX, e.clientY); }, { passive: false });
    st.addEventListener('dblclick', function (e) { zoomAt(zs > 1 ? 1 : 2.5, e.clientX, e.clientY); });
    st.addEventListener('mousedown', function (e) { if (zs <= 1) return; e.preventDefault(); var sx = e.clientX, sy = e.clientY, ox = zx, oy = zy;
      function mv(ev) { zx = ox + ev.clientX - sx; zy = oy + ev.clientY - sy; zClamp(); zApply(); }
      function up() { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); }
      window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up); });
    st.addEventListener('click', function (e) { if (e.target === st && zs === 1 && e.detail === 1 && e.pointerType !== 'touch') zClose(); });
    st.addEventListener('touchstart', function (e) { moved = false; var t = e.touches;
      if (t.length === 2) gest = { d: Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY), s: zs, mx: (t[0].clientX + t[1].clientX) / 2, my: (t[0].clientY + t[1].clientY) / 2, x0: zx, y0: zy };
      else if (t.length === 1) gest = { x: t[0].clientX, y: t[0].clientY, x0: zx, y0: zy }; }, { passive: true });
    st.addEventListener('touchmove', function (e) { if (!gest) return; e.preventDefault(); moved = true; var t = e.touches;
      if (t.length === 2 && gest.d) {
        var r = st.getBoundingClientRect(), cx = r.left + W / 2, cy = r.top + H / 2;
        var ux = (gest.mx - cx - gest.x0) / gest.s, uy = (gest.my - cy - gest.y0) / gest.s;
        zs = Math.max(1, Math.min(6, gest.s * Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY) / gest.d));
        zx = (t[0].clientX + t[1].clientX) / 2 - cx - ux * zs; zy = (t[0].clientY + t[1].clientY) / 2 - cy - uy * zs;
        zClamp(); zApply();
      }
      else if (t.length === 1 && gest.x !== undefined && zs > 1) { zx = gest.x0 + t[0].clientX - gest.x; zy = gest.y0 + t[0].clientY - gest.y; zClamp(); zApply(); } }, { passive: false });
    st.addEventListener('touchend', function (e) { var t = e.changedTouches[0];
      if (e.touches.length === 0) {
        if (!moved && t) { var now = Date.now(); if (now - lastTap < 300) { zoomAt(zs > 1 ? 1 : 2.5, t.clientX, t.clientY); lastTap = 0; } else { lastTap = now; if (zs === 1 && e.target === st) setTimeout(function () { if (lastTap && Date.now() - lastTap >= 290) zClose(); }, 310); } }
        gest = null;
      } else if (e.touches.length === 1) gest = { x: e.touches[0].clientX, y: e.touches[0].clientY, x0: zx, y0: zy }; });
  }
  body.querySelectorAll('figure img').forEach(function (im) {
    var w = document.createElement('button'); w.type = 'button'; w.className = 'rd-zf'; w.setAttribute('aria-label', 'Open the figure full screen');
    im.parentNode.insertBefore(w, im); w.appendChild(im);
    var b = document.createElement('span'); b.className = 'rd-zb material-symbols-outlined'; b.setAttribute('aria-hidden', 'true'); b.textContent = 'open_in_full'; w.appendChild(b);
    w.addEventListener('click', function () {
      var f = im.closest('figure'), cap = f && f.querySelector('figcaption');
      zOpen(im.currentSrc || im.src, im.alt, cap ? cap.textContent.replace(/\s+/g, ' ').trim() : '', w);
    });
  });
  document.addEventListener('keydown', function (e) { if (view && e.key === 'Escape') zClose(); });
  window.addEventListener('resize', function () { if (view) { zMeasure(); zClamp(); zApply(); } });

  /* ---------- text size ---------- */
  var size = parseFloat(localStorage.getItem(SIZE)) || 1;
  function applySize() { root.style.setProperty('--rd-scale', size); }
  applySize();
  root.querySelectorAll('[data-rd-size]').forEach(function (b) {
    b.addEventListener('click', function () {
      size = Math.min(1.3, Math.max(0.85, size + parseFloat(b.getAttribute('data-rd-size')) * 0.075));
      try { localStorage.setItem(SIZE, size); } catch (e) { /* private mode */ }
      applySize();
    });
  });

  /* ---------- done ---------- */
  var doneBtn = root.querySelector('[data-rd-done]');
  function paintDone() {
    var d = Study.get(key), on = !!(d && d.d);
    doneBtn.setAttribute('aria-pressed', String(on));
    root.querySelector('[data-rd-done-label]').textContent = on ? 'Done' : 'Mark as done';
  }
  doneBtn.addEventListener('click', function () { Study.put(key, { d: doneBtn.getAttribute('aria-pressed') === 'true' ? 0 : 1 }); paintDone(); });
  paintDone();

  /* ---------- progress, resume and the contents rail ---------- */
  var heads = Array.prototype.slice.call(body.querySelectorAll('h2[id]'));
  var links = root.querySelectorAll('[data-rd-toc]');
  /* Reading credit grows with time on the page, never faster than a quick reader could manage
     (a quarter of the estimated reading time for the whole chapter): jumping to the end saves
     the place but does not count the chapter as read. */
  var minutes = Math.max(1, parseFloat(root.getAttribute('data-rd-min')) || 5);
  var rate = 100 / (minutes * 60 * 0.25);
  var credit = (Study.get(key) || {}).p || 0, here = 0, ticking = false, lastSave = 0, lastTick = Date.now();
  function position() {
    var top = body.getBoundingClientRect().top + window.scrollY;
    var span = Math.max(1, body.offsetHeight - window.innerHeight * 0.6);
    return Math.max(0, Math.min(100, 100 * (window.scrollY - top + window.innerHeight * 0.4) / span));
  }
  function persist(force) {
    if (!force && Date.now() - lastSave < 2000) return;
    lastSave = Date.now();
    Study.put(key, { p: Math.round(credit), y: Math.round(here) });
  }
  function onScroll() {
    ticking = false;
    here = position();
    if (bar) bar.style.width = here + '%';
    var cur = null;
    heads.forEach(function (h) { if (h.getBoundingClientRect().top < 140) cur = h.id; });
    links.forEach(function (l) { l.classList.toggle('is-current', l.getAttribute('data-rd-toc') === cur); });
    persist(false);
  }
  setInterval(function () {
    var now = Date.now(), dt = Math.min(5, (now - lastTick) / 1000);
    lastTick = now;
    if (document.hidden || here <= credit) return;
    credit = Math.min(here, credit + rate * dt);
    persist(false);
  }, 1000);
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('pagehide', function () { persist(true); });
  document.addEventListener('visibilitychange', function () { lastTick = Date.now(); if (document.hidden) persist(true); });
  onScroll();

  var resumeAt = (Study.get(key) || {}).y;
  if (!location.hash && resumeAt > 4 && resumeAt < 95) {
    var chip = document.createElement('button');
    chip.type = 'button'; chip.className = 'rd-resume';
    chip.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">bookmark</span>Resume where you stopped (' + resumeAt + '%)';
    chip.addEventListener('click', function () {
      var top = body.getBoundingClientRect().top + window.scrollY;
      var span = Math.max(1, body.offsetHeight - window.innerHeight * 0.6);
      window.scrollTo({ top: top + span * resumeAt / 100 - window.innerHeight * 0.4, behavior: 'smooth' });
      chip.remove();
    });
    root.querySelector('.rd-head').appendChild(chip);
    setTimeout(function () { if (chip.isConnected) chip.classList.add('is-quiet'); }, 9000);
  }

  /* contents as a sheet on small screens */
  var side = root.querySelector('.rd-side');
  var fab = root.querySelector('[data-rd-toc-open]');
  fab.addEventListener('click', function () { side.classList.toggle('is-open'); fab.setAttribute('aria-expanded', String(side.classList.contains('is-open'))); });
  side.addEventListener('click', function (e) { if (e.target === side || e.target.closest('a')) side.classList.remove('is-open'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') side.classList.remove('is-open'); });
})();
