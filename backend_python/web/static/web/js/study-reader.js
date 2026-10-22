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
    tip.textContent = 'Tap an option to check it. Your score is kept on this device.';
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
  allBtn.addEventListener('click', function () {
    var open = allBtn.getAttribute('aria-pressed') !== 'true';
    allBtn.setAttribute('aria-pressed', String(open));
    answers.forEach(function (d) { d.open = open; });
  });
  window.addEventListener('beforeprint', function () { answers.forEach(function (d) { d.open = true; }); });
  var firstQs = body.querySelector('h2.qs');
  if (firstQs && !document.getElementById('questions')) {
    var anchor = document.createElement('span'); anchor.id = 'questions'; firstQs.parentNode.insertBefore(anchor, firstQs);
  }

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
