/* A model paper (a chapter exported with "exam", see notes/tools/export_study.py) taken as a
 * timed test: the key and the explanations stay hidden, one answer per question can be changed
 * until Submit, the clock runs on an absolute deadline (no pause; it keeps running through a
 * reload or a closed tab) and the paper's own marking is applied: +1 right, -negative wrong,
 * 0 blank. Needs window.NebReader from js/study-reader.js.
 *
 * Saved on this device, localStorage "neb.exam.v1":
 *   { "<doc key>": { s: started ms, e: deadline ms, n: questions, a: { "<question index>": "b" },
 *                    f: submitted ms (0 while running), o: 1 when the time ran out } }
 * The last result is also kept with the chapter's progress: NebStudy doc.x = { s, n, c, w, b, at }. */
(function () {
  'use strict';
  var R = window.NebReader;
  if (!R || !R.mcqs.length) return;
  var root = R.root, body = R.body, key = R.key, mcqs = R.mcqs;
  var minutes = parseFloat(root.getAttribute('data-rd-exam-min'));
  if (!(minutes > 0)) return;
  var negative = Math.max(0, parseFloat(root.getAttribute('data-rd-exam-neg')) || 0);
  var STORE = 'neb.exam.v1';
  var MARKS = [60, 30, 15, 5, 1];
  var startBtn = root.querySelector('[data-rd-exam-start]');
  var head = root.querySelector('.rd-head');
  var mode = '', st = null, timer = null, bar = null, result = null, live = null, openDlg = null, said = {};

  /* ---------- the paper: numbers, sections, the answer key ---------- */
  var heads = Array.prototype.slice.call(body.querySelectorAll('h2'));
  var sections = [], info = [];
  function sectionHead(el) {
    var h = null;
    heads.forEach(function (x) { if (x.compareDocumentPosition(el) & 4) h = x; });
    return h;
  }
  function shortTitle(t) { return t.replace(/\s*\(\s*questions?\b[^)]*\)\s*$/i, '').trim() || t; }
  mcqs.forEach(function (el, i) {
    var no = i + 1;
    if (el.tagName === 'LI') {
      no = (parseInt(el.parentNode.getAttribute('start'), 10) || 1) + Array.prototype.indexOf.call(el.parentNode.children, el);
    } else {
      var s = el.querySelector('strong');
      var n = s ? parseInt(s.textContent.replace(/[०-९]/g, function (d) { return '०१२३४५६७८९'.indexOf(d); }), 10) : NaN;
      if (n > 0) no = n;
    }
    var h = sectionHead(el), sec = sections[sections.length - 1];
    if (!sec || sec.h !== h) {
      sec = { h: h, title: h ? shortTitle(h.textContent.replace(/\s+/g, ' ').trim()) : 'Questions', items: [] };
      sections.push(sec);
    }
    sec.items.push(i);
    info.push({ no: no, sec: sections.length - 1, key: el.getAttribute('data-key') });
  });

  /* an explanation line per question number, when the numbers run straight through */
  var lines = {}, seen = {}, unique = true;
  info.forEach(function (q) { if (seen[q.no]) unique = false; seen[q.no] = 1; });
  if (unique) body.querySelectorAll('details.ans .ansline').forEach(function (p) {
    var s = p.querySelector('strong'), n = s ? parseInt(s.textContent, 10) : NaN;
    if (n > 0 && seen[n] && !lines[n]) lines[n] = p;
  });

  /* sections that hold only answers (the key at the end of a paper) disappear during the test */
  heads.forEach(function (h) {
    if (h.parentNode !== body) return;
    var run = [], ans = false, qs = false;
    for (var n = h.nextElementSibling; n && n.tagName !== 'H2'; n = n.nextElementSibling) {
      run.push(n);
      if (n.matches('details.ans') || n.querySelector('details.ans')) ans = true;
      if (n.matches('[data-key]') || n.querySelector('[data-key]')) qs = true;
    }
    if (!ans || qs) return;
    [h].concat(run).forEach(function (x) { x.classList.add('rd-x-key'); });
    var link = h.id && root.querySelector('[data-rd-toc="' + h.id + '"]');
    if (link && link.parentNode) link.parentNode.classList.add('rd-x-key');
  });

  /* ---------- storage and formatting ---------- */
  function all() { try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; } }
  function save() {
    var a = all();
    if (st) a[key] = st; else delete a[key];
    try { localStorage.setItem(STORE, JSON.stringify(a)); } catch (e) { /* private mode: the test runs, it just does not survive a reload */ }
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function two(n) { return (n < 10 ? '0' : '') + n; }
  function clock(ms, up) {
    var s = Math.max(0, up ? Math.ceil(ms / 1000) : Math.floor(ms / 1000));
    var h = Math.floor(s / 3600), m = Math.floor(s / 60) % 60;
    return (h || minutes >= 60 ? h + ':' + two(m) : String(m)) + ':' + two(s % 60);
  }
  function num(x) { var v = Math.round(x * 100) / 100; return (v < 0 ? '−' : '') + Math.abs(v); }
  function span(m) {
    if (m >= 60 && m % 60 === 0) return m / 60 + (m === 60 ? ' hour' : ' hours');
    if (m > 60) return Math.floor(m / 60) + ' h ' + Math.round(m % 60) + ' min';
    return Math.round(m) + ' minutes';
  }
  function icon(name) { return '<span class="material-symbols-outlined" aria-hidden="true">' + name + '</span>'; }
  function answered() { return Object.keys(st.a).length; }

  /* ---------- a modal: a centred card, a bottom sheet on a phone ---------- */
  function dialog(o) {
    var opener = document.activeElement, done = false, focus = null;
    var d = document.createElement('dialog');
    d.className = 'rd-xdlg' + (o.cls ? ' ' + o.cls : '');
    d.setAttribute('aria-labelledby', 'rd-xdlg-t');
    d.innerHTML = '<div class="rd-xdlg-head"><div><h2 class="rd-xdlg-t" id="rd-xdlg-t"></h2>' + (o.sub ? '<p class="rd-xdlg-sub"></p>' : '') + '</div>' +
      (o.x ? '<button type="button" class="rd-xdlg-x" aria-label="Close">' + icon('close') + '</button>' : '') +
      '</div><div class="rd-xdlg-body"></div><div class="rd-xdlg-act"></div>';
    d.querySelector('.rd-xdlg-t').textContent = o.title;
    if (o.sub) d.querySelector('.rd-xdlg-sub').textContent = o.sub;
    var bodyEl = d.querySelector('.rd-xdlg-body'), act = d.querySelector('.rd-xdlg-act');
    if (o.node) bodyEl.appendChild(o.node); else bodyEl.innerHTML = o.html || '';
    function close(v, keepFocus) {
      if (done) return;
      done = true;
      if (openDlg && openDlg.el === d) openDlg = null;
      try { if (d.open && d.close) d.close(); } catch (e) { /* closed already */ }
      d.remove();
      if (!keepFocus && opener && opener.isConnected && opener.focus) opener.focus({ preventScroll: true });
      if (o.done) o.done(v);
    }
    (o.actions || []).forEach(function (a) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'rd-xbtn' + (a.primary ? ' is-primary' : '');
      b.innerHTML = (a.icon ? icon(a.icon) : '') + esc(a.label);
      b.addEventListener('click', function () { close(a.value); });
      act.appendChild(b);
      if (a.focus) focus = b;
    });
    if (!act.children.length) act.remove();
    var x = d.querySelector('.rd-xdlg-x');
    if (x) x.addEventListener('click', function () { close(o.cancel); });
    d.addEventListener('cancel', function (e) { e.preventDefault(); close(o.cancel); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { e.preventDefault(); close(o.cancel); } });
    d.addEventListener('click', function (e) { if (e.target === d) close(o.cancel); });
    if (openDlg) openDlg.close(null, true);
    root.appendChild(d);
    if (typeof d.showModal === 'function') d.showModal(); else { d.setAttribute('open', ''); d.classList.add('is-fallback'); }
    openDlg = { el: d, close: close };
    (focus || x || act.lastChild || d).focus();
    return openDlg;
  }

  /* ---------- before: what the test is ---------- */
  function fact(name, html) { return '<li>' + icon(name) + '<span>' + html + '</span></li>'; }
  function intro() {
    dialog({
      title: 'Take this paper as a timed test',
      html: '<ul class="rd-xdlg-facts">' +
        fact('quiz', '<b>' + mcqs.length + ' questions</b>, one answer each. You can change an answer until you submit.') +
        fact('timer', '<b>' + span(minutes) + '</b> on a clock that cannot be paused. It keeps running if you leave this page, and the test submits itself when the time is up.') +
        fact('rule', '<b>+1</b> for a right answer, ' + (negative ? '<b>−' + num(negative) + '</b> for a wrong one' : 'nothing taken off for a wrong one') + ', 0 for a blank.') +
        fact('visibility_off', 'The key and the explanations stay hidden until you submit.') + '</ul>',
      actions: [{ label: 'Cancel', value: false }, { label: 'Start the test', icon: 'timer', value: true, primary: true, focus: true }],
      cancel: false,
      done: function (go) { if (go) begin(); }
    });
  }
  function begin() {
    var now = Date.now();
    st = { s: now, e: now + Math.round(minutes * 60000), n: mcqs.length, a: {}, f: 0, o: 0 };
    save();
    enterTest();
    var h = sections[0] && sections[0].h;
    reach(h || mcqs[0], 'start');
  }

  /* ---------- during ---------- */
  function tools(el) {
    var t = el.querySelector(':scope > .rd-x-tools');
    if (!t) { t = document.createElement('div'); t.className = 'rd-x-tools'; el.appendChild(t); }
    t.innerHTML = '';
    return t;
  }
  function reset() {
    clearInterval(timer);
    timer = null;
    if (openDlg) openDlg.close(null, true);
    mcqs.forEach(function (el) {
      R.unmark(el);
      el.classList.remove('has-pick', 'is-blank', 'is-flash');
      el.querySelectorAll('.opt').forEach(function (o) { o.classList.remove('is-picked'); o.removeAttribute('aria-pressed'); });
      var t = el.querySelector(':scope > .rd-x-tools');
      if (t) t.remove();
    });
    root.classList.remove('rd-exam-on', 'rd-exam-review');
    if (bar) { bar.remove(); bar = null; }
    if (result) { result.remove(); result = null; }
  }
  function paint(i) {
    var el = mcqs[i], p = st.a[i] || '';
    el.classList.toggle('has-pick', !!p);
    el.querySelectorAll('.opt').forEach(function (o) {
      var on = o.getAttribute('data-opt') === p;
      o.classList.toggle('is-picked', on);
      o.setAttribute('aria-pressed', String(on));
    });
  }
  function choose(i, letter) {
    if (mode !== 'test') return;
    if (Date.now() >= st.e) { tick(); return; }
    if (letter) st.a[i] = letter; else delete st.a[i];
    save();
    paint(i);
    counts();
  }
  function enterTest() {
    reset();
    mode = 'test';
    root.classList.add('rd-exam-on');
    if (startBtn) startBtn.hidden = true;
    mcqs.forEach(function (el, i) {
      var c = document.createElement('button');
      c.type = 'button';
      c.className = 'rd-x-clear';
      c.innerHTML = icon('close') + 'Clear';
      c.setAttribute('aria-label', 'Clear the answer to question ' + info[i].no);
      c.addEventListener('click', function () { choose(i, null); });
      tools(el).appendChild(c);
      paint(i);
    });
    makeBar();
    var left = st.e - Date.now();
    said = {};
    MARKS.forEach(function (m) { if (left <= m * 60000) said[m] = 1; });
    tick();
    timer = setInterval(tick, 1000);
  }
  function counts() {
    if (!bar || mode !== 'test') return;
    bar.querySelector('[data-x-done]').textContent = answered();
    bar.querySelector('[data-x-left]').textContent = mcqs.length - answered();
  }
  function tick() {
    if (mode !== 'test') return;
    var left = st.e - Date.now();
    if (left <= 0) { submit(true); return; }
    bar.querySelector('[data-x-clock]').textContent = clock(left, true);
    bar.classList.toggle('is-low', left <= 5 * 60000);
    MARKS.forEach(function (m) {
      if (left <= m * 60000 && !said[m]) { said[m] = 1; live.textContent = m === 1 ? 'One minute left' : m + ' minutes left'; }
    });
  }
  function makeBar() {
    bar = document.createElement('div');
    bar.className = 'rd-xbar';
    bar.setAttribute('role', 'region');
    if (mode === 'test') {
      bar.setAttribute('aria-label', 'Timed test');
      bar.innerHTML =
        '<div class="rd-xbar-clock">' + icon('timer') + '<b data-x-clock role="timer" aria-label="Time left"></b></div>' +
        '<div class="rd-xbar-count"><span><b data-x-done>0</b>/' + mcqs.length + '<span class="rd-xbar-w"> answered</span></span>' +
          '<small><span data-x-left></span><span class="rd-xbar-w"> unanswered</span><span class="rd-xbar-m"> left</span></small></div>' +
        '<button type="button" class="rd-xbar-btn rd-xbar-pal" data-x-pal aria-haspopup="dialog" aria-label="Questions">' + icon('grid_view') + '<span class="rd-xbar-l">Questions</span></button>' +
        '<button type="button" class="rd-xbar-btn is-primary" data-x-submit>' + icon('send') + 'Submit</button>';
      bar.querySelector('[data-x-submit]').addEventListener('click', confirmSubmit);
    } else {
      bar.setAttribute('aria-label', 'Test result');
      bar.innerHTML =
        '<button type="button" class="rd-xbar-score" data-x-res>' + icon('emoji_events') + '<span><span class="rd-xbar-w">Score </span><b data-x-score></b><small> / ' + mcqs.length + '</small></span></button>' +
        '<button type="button" class="rd-xbar-btn rd-xbar-pal" data-x-pal aria-haspopup="dialog" aria-label="Questions">' + icon('grid_view') + '<span class="rd-xbar-l">Questions</span></button>';
      bar.querySelector('[data-x-res]').addEventListener('click', function () {
        if (!result) return;
        reach(result, 'start');
        result.focus({ preventScroll: true });
      });
    }
    live = document.createElement('span');
    live.className = 'rd-x-live';
    live.setAttribute('aria-live', 'polite');
    bar.appendChild(live);
    bar.querySelector('[data-x-pal]').addEventListener('click', palette);
    root.appendChild(bar);
    counts();
  }

  /* ---------- the question palette ---------- */
  /* the site scrolls smoothly; across a 200-question paper that takes seconds, so a far target is reached at once */
  function reach(el, block) {
    var html = document.documentElement, was = html.style.scrollBehavior;
    if (Math.abs(el.getBoundingClientRect().top - window.innerHeight / 2) > window.innerHeight * 3) {
      html.style.scrollBehavior = 'auto';
      el.scrollIntoView({ block: block });
      html.style.scrollBehavior = was;
    } else el.scrollIntoView({ block: block, behavior: 'smooth' });
  }
  function jump(el) {
    reach(el, 'center');
    el.classList.remove('is-flash');
    void el.offsetWidth;
    el.classList.add('is-flash');
    setTimeout(function () { el.classList.remove('is-flash'); }, 1700);
  }
  function goTo(i) {
    var el = mcqs[i];
    if (!el) return;
    jump(el);
    var o = el.querySelector('.opt.is-picked') || el.querySelector('.opt');
    if (o) { try { o.focus({ preventScroll: true }); } catch (e) { /* old browsers */ } }
  }
  function state(i) {
    var p = st.a[i];
    if (mode === 'test') return p ? 'done' : '';
    return !p ? 'blank' : p === info[i].key ? 'right' : 'wrong';
  }
  function palette() {
    var test = mode === 'test', wrap = document.createElement('div'), html = '';
    var words = { done: 'answered', '': 'not answered', blank: 'not answered', right: 'right', wrong: 'wrong' };
    sections.forEach(function (sec) {
      var a = info[sec.items[0]].no, b = info[sec.items[sec.items.length - 1]].no;
      html += '<p class="rd-xpal-sec">' + esc(sec.title) + ' <small>' + (a === b ? a : a + '–' + b) + '</small></p><div class="rd-xpal-grid">';
      sec.items.forEach(function (i) {
        var s = state(i);
        html += '<button type="button" class="rd-xq' + (s ? ' is-' + s : '') + '" data-x-go="' + i + '" aria-label="Question ' + info[i].no + ', ' + words[s] + '">' + info[i].no + '</button>';
      });
      html += '</div>';
    });
    wrap.innerHTML = html;
    var t = tally().t, firstOpen = -1;
    for (var i = 0; i < mcqs.length && firstOpen < 0; i++) if (test ? !st.a[i] : st.a[i] !== info[i].key) firstOpen = i;
    var dlg = dialog({
      title: 'Questions',
      sub: test ? answered() + ' answered · ' + (mcqs.length - answered()) + ' unanswered' : t.c + ' right · ' + t.w + ' wrong · ' + t.b + ' blank',
      node: wrap,
      cls: 'rd-xpal',
      x: true,
      cancel: null,
      actions: firstOpen < 0 ? [] : [{ label: test ? 'First unanswered question' : 'First question you missed', icon: 'arrow_downward', value: 'next' }],
      done: function (v) { if (v === 'next') goTo(firstOpen); }
    });
    wrap.addEventListener('click', function (e) {
      var b = e.target.closest('[data-x-go]');
      if (!b) return;
      dlg.close(null, true);
      goTo(+b.getAttribute('data-x-go'));
    });
    var here = wrap.querySelector('[data-x-go="' + (firstOpen < 0 ? 0 : firstOpen) + '"]');
    if (here) here.focus();
  }

  /* ---------- after: the paper's marking, then the key ---------- */
  function confirmSubmit() {
    var done = answered(), blank = mcqs.length - done;
    dialog({
      title: 'Submit the test?',
      html: '<p>' + (blank
        ? 'You have answered <b>' + done + '</b> of ' + mcqs.length + ' questions; <b>' + blank + '</b> ' + (blank === 1 ? 'is' : 'are') + ' blank and score 0.'
        : 'All ' + mcqs.length + ' questions are answered.') + ' You cannot change an answer after you submit.</p>',
      actions: [{ label: 'Keep going', value: false, focus: true }, { label: 'Submit now', icon: 'send', value: true, primary: true }],
      cancel: false,
      done: function (go) { if (go) submit(false); }
    });
  }
  function submit(out) {
    if (mode !== 'test') return;
    st.f = Math.min(Date.now(), st.e);
    st.o = out ? 1 : 0;
    save();
    enterReview(true);
  }
  function tally() {
    var t = { n: 0, c: 0, w: 0, b: 0 };
    var per = sections.map(function (s) { return { title: s.title, n: 0, c: 0, w: 0, b: 0 }; });
    info.forEach(function (q, i) {
      var p = st.a[i], k = !p ? 'b' : p === q.key ? 'c' : 'w';
      t.n++; t[k]++;
      per[q.sec].n++; per[q.sec][k]++;
    });
    return { t: t, per: per };
  }
  function score(x) { return x.c - negative * x.w; }
  function showLine(line) {
    var d = line.closest('details');
    if (d) d.open = true;
    jump(line);
  }
  function enterReview(fresh) {
    reset();
    mode = 'review';
    root.classList.add('rd-exam-review');
    if (startBtn) startBtn.hidden = true;
    var r = tally();
    mcqs.forEach(function (el, i) {
      var k = info[i].key, p = st.a[i];
      el.classList.add('is-answered');
      el.classList.toggle('got-it', p === k);
      el.classList.toggle('is-blank', !p);
      el.querySelectorAll('.opt').forEach(function (o) {
        var l = o.getAttribute('data-opt');
        o.classList.toggle('is-right', l === k);
        o.classList.toggle('is-wrong', !!p && l === p && p !== k);
        o.setAttribute('aria-disabled', 'true');
      });
      var t = tools(el), v = document.createElement('span');
      v.className = 'rd-x-verdict is-' + (!p ? 'blank' : p === k ? 'right' : 'wrong');
      v.innerHTML = !p ? icon('flag') + 'Not answered · 0'
        : p === k ? icon('check_circle') + 'Right · +1'
        : icon('cancel') + 'Wrong · ' + (negative ? '−' + num(negative) : '0');
      t.appendChild(v);
      var line = lines[info[i].no];
      if (line) {
        var w = document.createElement('button');
        w.type = 'button';
        w.className = 'rd-x-why';
        w.textContent = 'Explanation';
        w.setAttribute('aria-label', 'Explanation of question ' + info[i].no);
        w.addEventListener('click', function () { showLine(line); });
        t.appendChild(w);
      }
    });
    if (R.answers) R.answers.forEach(function (d) { d.open = true; });
    makeBar();
    bar.querySelector('[data-x-score]').textContent = num(score(r.t));
    renderResult(r);
    if (fresh) {
      try { window.NebStudy.put(key, { x: { s: Math.round(score(r.t) * 100) / 100, n: r.t.n, c: r.t.c, w: r.t.w, b: r.t.b, at: st.f } }); } catch (e) { /* storage full */ }
      reach(result, 'start');
      result.focus({ preventScroll: true });
    }
  }
  function stat(label, value) { return '<div><dt>' + label + '</dt><dd>' + value + '</dd></div>'; }
  function renderResult(r) {
    var t = r.t, tried = t.c + t.w, used = Math.max(0, Math.min(st.f, st.e) - st.s);
    var cells = function (x) { return '<td>' + x.n + '</td><td>' + x.c + '</td><td>' + x.w + '</td><td>' + x.b + '</td><td><b>' + num(score(x)) + '</b></td>'; };
    result = document.createElement('section');
    result.className = 'rd-xres';
    result.tabIndex = -1;
    result.setAttribute('aria-labelledby', 'rd-xres-h');
    result.innerHTML =
      '<p class="rd-xres-kick">' + icon(st.o ? 'alarm' : 'task_alt') + (st.o ? 'Time is up: the test was submitted with the answers you had chosen' : 'Test submitted') + '</p>' +
      '<h2 class="rd-xres-score" id="rd-xres-h"><b>' + num(score(t)) + '</b> <span>out of ' + t.n + '</span></h2>' +
      '<p class="rd-xres-sum">' + t.c + ' right × 1' + (negative ? ' − ' + t.w + ' wrong × ' + num(negative) : '') + ' = ' + num(score(t)) +
        (t.b ? ' · ' + t.b + ' blank, 0 each' : '') + '</p>' +
      '<dl class="rd-xres-stats">' + stat('Right', t.c) + stat('Wrong', t.w) + stat('Blank', t.b) +
        stat('Accuracy', tried ? Math.round(100 * t.c / tried) + '%' : '—') +
        stat('Time used', clock(used) + '<small> of ' + clock(minutes * 60000) + '</small>') + '</dl>' +
      (r.per.length > 1
        ? '<div class="rd-xres-scroll"><table class="rd-xres-table"><thead><tr><th scope="col">Section</th><th scope="col"><abbr title="Questions">Qs</abbr></th><th scope="col">Right</th><th scope="col">Wrong</th><th scope="col">Blank</th><th scope="col">Score</th></tr></thead><tbody>' +
          r.per.map(function (p) { return '<tr><th scope="row">' + esc(p.title) + '</th>' + cells(p) + '</tr>'; }).join('') +
          '</tbody><tfoot><tr><th scope="row">Total</th>' + cells(t) + '</tr></tfoot></table></div>'
        : '') +
      '<p class="rd-xres-note">Every question now shows the right option in green and a wrong choice in red; the explanations are open in the answer key' +
        (Object.keys(lines).length ? ' (Explanation under a question jumps to its line)' : '') + '.</p>' +
      '<div class="rd-xres-act"><button type="button" class="rd-xbtn is-primary" data-x-retake>' + icon('restart_alt') + 'Retake the test</button>' +
        '<button type="button" class="rd-xbtn" data-x-practice>' + icon('menu_book') + 'Back to practice</button></div>';
    head.parentNode.insertBefore(result, head.nextSibling);
    result.querySelector('[data-x-retake]').addEventListener('click', function () { toPractice(); intro(); });
    result.querySelector('[data-x-practice]').addEventListener('click', function () {
      toPractice();
      if (startBtn) startBtn.focus({ preventScroll: true });
    });
  }
  function toPractice() {
    st = null;
    save();
    reset();
    mode = '';
    if (R.foldAnswers) R.foldAnswers();
    if (R.paintPractice) R.paintPractice();
    if (startBtn) startBtn.hidden = false;
  }

  R.exam = {
    take: function (el, o) {
      if (mode === 'test') { choose(+el.getAttribute('data-q'), o.getAttribute('data-opt')); return true; }
      return mode === 'review';
    }
  };
  if (startBtn) startBtn.addEventListener('click', intro);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) tick(); });

  st = all()[key] || null;
  if (st && (st.n !== mcqs.length || !(st.e > st.s) || typeof st.a !== 'object' || !st.a)) { st = null; save(); }
  if (st) {
    if (!st.f && Date.now() >= st.e) { st.f = st.e; st.o = 1; save(); enterReview(true); }
    else if (st.f) enterReview(false);
    else enterTest();
  }
})();
