/* Reading mode page. Loads chapters of the book's own HTML (c/<n>.html) and its pictures (r/<file>), lays
   them out with book.css + reader.css and talks to the app through `NebAndroid` (see ReadingBook.kt).
   Everything here is for reading: scroll position and page, jump, text size (pinch), settings, search,
   speech text, folded answers, and a pinch / pan viewer for figures, equations and tables. */
(function () {
  'use strict';
  var root = document.documentElement, doc = document.getElementById('doc'), ov = document.getElementById('ov');
  var A = window.NebAndroid || {};
  function call(n) {
    try { var f = A[n]; if (f) f.apply(A, Array.prototype.slice.call(arguments, 1)); } catch (e) { }
  }
  var meta = null, first = 0, last = -1, chapEls = {}, blocks = [], blocksDirty = true;
  var pageNow = 0, busy = false, S = { scale: 1, hide: false, top: 76 }, viewerOpen = false;

  function $(s, r) { return (r || doc).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  /* ---------------------------------------------------------------- spoken maths */
  var GREEK = { alpha: 'alpha', beta: 'beta', gamma: 'gamma', delta: 'delta', epsilon: 'epsilon', varepsilon: 'epsilon', theta: 'theta',
    lambda: 'lambda', mu: 'mu', nu: 'nu', pi: 'pi', rho: 'rho', sigma: 'sigma', tau: 'tau', phi: 'phi', varphi: 'phi', omega: 'omega',
    Delta: 'delta', Omega: 'omega', Sigma: 'sigma', Phi: 'phi', Gamma: 'gamma', Lambda: 'lambda', eta: 'eta', kappa: 'kappa', psi: 'psi', chi: 'chi', zeta: 'zeta' };
  function speakMath(t) {
    if (!t) return 'formula';
    var s = ' ' + t + ' ', n = 0, g;
    s = s.replace(/\\(?:left|right|,|;|!|quad|qquad|displaystyle|mathrm|mathbf|text|operatorname)\b\s*/g, ' ');
    s = s.replace(/\\\\/g, ' , ');
    for (g = 0; g < 4; g++) {
      s = s.replace(/\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g, ' $1 over $2 ');
      s = s.replace(/\\sqrt\s*\[([^\]]*)\]\s*\{([^{}]*)\}/g, ' root $1 of $2 ');
      s = s.replace(/\\sqrt\s*\{([^{}]*)\}/g, ' square root of $1 ');
      s = s.replace(/\^\s*\{\s*2\s*\}|\^2/g, ' squared ').replace(/\^\s*\{\s*3\s*\}|\^3/g, ' cubed ');
      s = s.replace(/\^\s*\{([^{}]*)\}/g, ' to the power $1 ').replace(/\^\s*(\S)/g, ' to the power $1 ');
      s = s.replace(/_\s*\{([^{}]*)\}/g, ' sub $1 ').replace(/_\s*(\S)/g, ' sub $1 ');
      s = s.replace(/\\(?:bar|vec|hat|overline)\s*\{([^{}]*)\}/g, ' $1 ');
    }
    s = s.replace(/\\(int)\b/g, ' integral ').replace(/\\sum\b/g, ' sum ').replace(/\\lim\b/g, ' limit ').replace(/\\infty/g, ' infinity ')
      .replace(/\\times|\\cdot/g, ' times ').replace(/\\div/g, ' divided by ').replace(/\\pm/g, ' plus or minus ')
      .replace(/\\approx/g, ' approximately ').replace(/\\propto/g, ' proportional to ').replace(/\\neq|\\ne\b/g, ' not equal to ')
      .replace(/\\leq?\b/g, ' less than or equal to ').replace(/\\geq?\b/g, ' greater than or equal to ')
      .replace(/\\rightarrow|\\to\b/g, ' goes to ').replace(/\\circ/g, ' degrees ').replace(/\\partial/g, ' partial ')
      .replace(/\\nabla/g, ' del ').replace(/\\ln\b/g, ' natural log ').replace(/\\log\b/g, ' log ')
      .replace(/\\(sin|cos|tan|cot|sec|csc)\b/g, ' $1 ');
    s = s.replace(/\\([A-Za-z]+)/g, function (m, w) { return GREEK[w] ? ' ' + GREEK[w] + ' ' : ' ' + w + ' '; });
    s = s.replace(/=/g, ' equals ').replace(/\+/g, ' plus ').replace(/-|\u2212/g, ' minus ').replace(/</g, ' less than ').replace(/>/g, ' greater than ')
      .replace(/[{}$]/g, ' ').replace(/\//g, ' over ').replace(/\s+/g, ' ');
    return s.trim();
  }

  /* ---------------------------------------------------------------- chapters */
  function chapterOfPage(p) {
    var i = 0, k;
    for (k = 0; k < meta.chapters.length; k++) if (meta.chapters[k].page <= p) i = k;
    return i;
  }
  function fetchChapter(i) {
    return fetch('c/' + i + '.html').then(function (r) { return r.text(); });
  }
  function build(i, html) {
    var s = document.createElement('section');
    s.className = 'chap'; s.setAttribute('data-c', i);
    s.innerHTML = html;
    post(s);
    return s;
  }
  function loadChapter(i, where) {
    if (i < 0 || i >= meta.chapters.length || chapEls[i]) return Promise.resolve();
    return fetchChapter(i).then(function (html) {
      if (chapEls[i]) return;
      var el = build(i, html);
      chapEls[i] = el;
      if (where === 'before') {
        var anchor = doc.firstElementChild, off = anchor ? anchor.getBoundingClientRect().top : 0;
        doc.insertBefore(el, anchor);
        window.scrollBy(0, anchor.getBoundingClientRect().top - off);
        first = i;
      } else {
        var end = $('.end'); if (end) end.remove();
        doc.appendChild(el); last = Math.max(last, i);
        if (i === meta.chapters.length - 1) {
          var e = document.createElement('div'); e.className = 'end'; e.textContent = 'End of the book'; doc.appendChild(e);
        }
      }
      blocksDirty = true; measureTables();
    });
  }
  function reset(i) {
    doc.innerHTML = ''; chapEls = {}; first = i; last = i - 1; blocksDirty = true;
    return loadChapter(i, 'after').then(function () { first = i; });
  }
  function loadAll() {
    var p = Promise.resolve(), i;
    function one(k) { return function () { return loadChapter(k, k < first ? 'before' : 'after'); }; }
    for (i = 0; i < meta.chapters.length; i++) if (!chapEls[i]) p = p.then(one(i));
    return p;
  }
  function more() {
    if (busy || !meta) return;
    var y = window.scrollY, h = window.innerHeight, H = document.documentElement.scrollHeight;
    if (last < meta.chapters.length - 1 && y + h * 2.2 > H) { busy = true; loadChapter(last + 1, 'after').then(function () { busy = false; }); }
    else if (first > 0 && y < h * 1.2) { busy = true; loadChapter(first - 1, 'before').then(function () { busy = false; }); }
  }

  /* ---------------------------------------------------------------- post processing */
  function post(el) {
    // tables: scroll box + Expand
    $$('table', el).forEach(function (t) {
      if (t.classList.contains('pgrid') || t.closest('.tw')) return;
      var w = document.createElement('div'); w.className = 'tw';
      var sc = document.createElement('div'); sc.className = 'sc';
      var b = document.createElement('button'); b.className = 'more'; b.type = 'button'; b.setAttribute('data-act', 'table');
      b.textContent = 'Expand table';
      t.parentNode.insertBefore(w, t); sc.appendChild(t); w.appendChild(sc); w.appendChild(b);
    });
    // maths: spoken alt text, so TalkBack reads a formula
    $$('img[alt]', el).forEach(function (im) {
      var a = im.getAttribute('alt');
      if (a && a !== 'figure' && a !== 'diagram' && a !== 'photograph' && a !== 'formula' && im.style.width) {
        im.setAttribute('data-tex', a); im.setAttribute('alt', speakMath(a)); im.setAttribute('role', 'img');
      }
    });
    $$('figure > img, .dm img, .dv img, .fxs img', el).forEach(function (im) { im.classList.add('zoomable'); });
    $$('img', el).forEach(function (im) { im.decoding = 'async'; if (!im.loading) im.loading = 'lazy'; });
    foldAnswers(el);
  }
  function fold(first, items, title) {
    var f = document.createElement('div'); f.className = 'fold';
    var bar = document.createElement('button'); bar.type = 'button'; bar.className = 'fold-bar'; bar.setAttribute('data-act', 'fold');
    bar.setAttribute('aria-expanded', 'false');
    bar.innerHTML = '<span></span><i class="chev"></i>'; bar.firstChild.textContent = title;
    var body = document.createElement('div'); body.className = 'fold-body';
    first.parentNode.insertBefore(f, first); f.appendChild(bar); f.appendChild(body);
    items.forEach(function (n) { body.appendChild(n); });
  }
  function foldAnswers(el) {
    // worked examples: everything from "Solution." (or Answer / Proof) to the end of the card
    $$('.box', el).forEach(function (b) {
      var kids = Array.prototype.slice.call(b.children), i, k;
      for (i = 0; i < kids.length; i++) {
        k = kids[i];
        var st = k.firstElementChild;
        if (k.tagName === 'P' && st && st.tagName === 'STRONG' && /^(solution|answer|ans|proof|hint)\b/i.test(st.textContent.trim())) {
          fold(k, kids.slice(i), st.textContent.replace(/[.:]\s*$/, '').trim());
          return;
        }
      }
    });
    // answer keys: a run of answer lines
    $$('.ansline', el).forEach(function (a) {
      if (a.closest('.fold') || a.previousElementSibling && a.previousElementSibling.classList.contains('ansline')) return;
      var run = [a], n = a.nextElementSibling;
      while (n && n.classList.contains('ansline')) { run.push(n); n = n.nextElementSibling; }
      fold(a, run, 'Answers');
    });
  }

  /* ---------------------------------------------------------------- position */
  function indexBlocks() {
    if (!blocksDirty) return;
    blocks = $$('[data-pg]');
    blocksDirty = false;
  }
  function topBlock() {
    indexBlocks();
    var line = S.top + window.innerHeight * 0.08, lo = 0, hi = blocks.length - 1, ans = -1, m, r;
    while (lo <= hi) {
      m = (lo + hi) >> 1; r = blocks[m].getBoundingClientRect();
      if (r.bottom > line && r.height > 0) { ans = m; hi = m - 1; } else if (r.height === 0 || r.bottom <= line) { lo = m + 1; }
    }
    return ans < 0 ? null : blocks[ans];
  }
  function report() {
    var b = topBlock(); if (!b) return;
    var p = parseInt(b.getAttribute('data-pg'), 10) || 0;
    if (p && p !== pageNow) { pageNow = p; call('onPage', p); }
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return; ticking = true;
    setTimeout(function () { ticking = false; report(); more(); }, 90);
  }, { passive: true });

  function goPage(p, smooth) {
    p = clamp(p, 1, meta.pages);
    var ci = chapterOfPage(p);
    var ready = chapEls[ci] ? Promise.resolve() : reset(ci);
    return ready.then(function () {
      indexBlocks();
      var target = null, i;
      for (i = 0; i < blocks.length; i++) {
        var v = parseInt(blocks[i].getAttribute('data-pg'), 10) || 0;
        if (v >= p && blocks[i].closest('.chap').getAttribute('data-c') >= String(ci)) { target = blocks[i]; break; }
      }
      if (!target) target = chapEls[ci];
      // a page may start in the middle of a chapter that has not got blocks on it: nearest block after
      window.scrollTo(0, target.getBoundingClientRect().top + window.scrollY - S.top - 6);
      setTimeout(function () { report(); more(); }, 120);
    });
  }

  /* ---------------------------------------------------------------- settings, text size */
  function keepAnchor(fn) {
    var b = topBlock(), off = b ? b.getBoundingClientRect().top : 0;
    fn();
    if (b) window.scrollBy(0, b.getBoundingClientRect().top - off);
    measureTables();
  }
  function setScale(s) {
    S.scale = s;
    root.style.setProperty('--fs', (18 * s).toFixed(2));
    root.setAttribute('data-wide', s >= 1.7 ? '2' : s >= 1.25 ? '1' : '0');
  }
  function apply(o) {
    keepAnchor(function () {
      if (o.theme) root.setAttribute('data-theme', o.theme);
      if (o.font) root.setAttribute('data-font', o.font);
      if (o.lang) root.setAttribute('lang', o.lang);
      if (o.accent) root.style.setProperty('--ba', o.accent);
      if (o.margin != null) root.setAttribute('data-margin', String(o.margin));
      if (o.justify != null) root.setAttribute('data-justify', o.justify ? '1' : '0');
      if (o.line != null) root.style.setProperty('--lh', (1.62 * o.line).toFixed(3));
      if (o.top != null) { S.top = o.top; root.style.setProperty('--top', (o.top + 10) + 'px'); root.style.setProperty('--inset-top', Math.max(0, o.top - 56) + 'px'); }
      if (o.bottom != null) root.style.setProperty('--bottom', o.bottom + 'px');
      if (o.hide != null) { S.hide = !!o.hide; root.setAttribute('data-hide', o.hide ? '1' : '0'); }
      if (o.scale != null) setScale(o.scale);
    });
  }

  var badge = document.createElement('div');
  badge.style.cssText = 'position:fixed;left:50%;top:45%;transform:translateX(-50%);background:var(--ink);color:var(--bg);font:600 15px Poppins,sans-serif;padding:8px 16px;border-radius:24px;z-index:60;display:none';
  document.body.appendChild(badge);
  var pinch = null, badgeT = 0;
  function dist(t) { var dx = t[0].clientX - t[1].clientX, dy = t[0].clientY - t[1].clientY; return Math.sqrt(dx * dx + dy * dy); }
  document.addEventListener('touchstart', function (e) {
    if (viewerOpen || e.touches.length !== 2) return;
    pinch = { d: dist(e.touches), s: S.scale, last: S.scale };
  }, { passive: true });
  document.addEventListener('touchmove', function (e) {
    if (!pinch || e.touches.length !== 2) return;
    e.preventDefault();
    var s = clamp(Math.round(pinch.s * dist(e.touches) / pinch.d * 20) / 20, 0.7, 3);
    if (s !== pinch.last) { pinch.last = s; keepAnchor(function () { setScale(s); }); }
    badge.textContent = Math.round(s * 100) + '%'; badge.style.display = 'block'; clearTimeout(badgeT);
  }, { passive: false });
  function endPinch() {
    if (!pinch) return;
    var s = pinch.last; pinch = null; call('onFontScale', s);
    badgeT = setTimeout(function () { badge.style.display = 'none'; }, 700);
  }
  document.addEventListener('touchend', function (e) { if (pinch && e.touches.length < 2) endPinch(); }, { passive: true });
  document.addEventListener('touchcancel', endPinch, { passive: true });

  /* ---------------------------------------------------------------- tables */
  function measureTables() {
    requestAnimationFrame(function () {
      $$('.tw').forEach(function (w) {
        var sc = w.firstElementChild; w.classList.toggle('wide', sc.scrollWidth > sc.clientWidth + 3 || (w.querySelectorAll('tr:first-child > *').length >= 4));
      });
    });
  }
  window.addEventListener('resize', measureTables);

  /* ---------------------------------------------------------------- viewer (figure, equation, table) */
  function openViewer(node, title, page) {
    ov.innerHTML = '';
    var bar = document.createElement('div'); bar.className = 'bar';
    bar.innerHTML = '<button class="x" type="button" aria-label="Close" data-act="close">\u2715</button><b></b>' +
      '<button type="button" data-act="orig">Original page</button><button type="button" data-act="fit">Fit</button>';
    bar.querySelector('b').textContent = title;
    if (!page) bar.querySelector('[data-act=orig]').style.display = 'none';
    var stage = document.createElement('div'); stage.className = 'stage';
    stage.appendChild(node);
    ov.appendChild(stage); ov.appendChild(bar);
    ov.hidden = false; viewerOpen = true; call('onViewer', true);
    ov._page = page;
    var st = { x: 0, y: 0, k: 1 }, vw = window.innerWidth, vh = window.innerHeight, top = 64 + (parseFloat(getComputedStyle(root).getPropertyValue('--inset-top')) || 0);
    function put() { stage.style.transform = 'translate(' + st.x + 'px,' + st.y + 'px) scale(' + st.k + ')'; }
    function size() { return { w: stage.offsetWidth, h: stage.offsetHeight }; }
    function fit() {
      var z = size(), k = Math.min((vw - 24) / z.w, (vh - top - 24) / z.h);
      if (node.tagName !== 'IMG') k = Math.min(1, (vw - 24) / z.w);
      st.k = clamp(k, 0.1, 2.4); st.x = (vw - z.w * st.k) / 2; st.y = node.tagName === 'IMG' ? top + Math.max(12, (vh - top - z.h * st.k) / 2) : top + 12; put();
    }
    function bounds() {
      var z = size(), w = z.w * st.k, h = z.h * st.k;
      st.x = w <= vw ? (vw - w) / 2 : clamp(st.x, vw - w - 12, 12);
      st.y = h <= vh - top ? Math.max(top + 8, (vh - h + top) / 2) : clamp(st.y, vh - h - 12, top + 8);
    }
    ov._fit = function () { fit(); };
    if (node.tagName === 'IMG' && !node.complete) node.onload = fit;
    fit(); setTimeout(fit, 60);
    var ptrs = {}, g = null, lastTap = 0;
    function pts() { return Object.keys(ptrs).map(function (k) { return ptrs[k]; }); }
    stage.parentNode.onpointerdown = function (e) {
      if (e.target.closest('.bar')) return;
      ov.setPointerCapture && ov.setPointerCapture(e.pointerId);
      ptrs[e.pointerId] = { x: e.clientX, y: e.clientY };
      var p = pts();
      if (p.length === 1) {
        g = { mode: 'pan', x: p[0].x, y: p[0].y, sx: st.x, sy: st.y, moved: false };
        var now = Date.now();
        if (now - lastTap < 280) {
          var k2 = st.k > Math.max(1.2, fitK()) * 1.05 ? fitK() : Math.min(4, Math.max(2.5, fitK() * 2.5));
          zoomAt(p[0].x, p[0].y, k2); lastTap = 0;
        } else lastTap = now;
      } else if (p.length === 2) {
        g = { mode: 'pinch', d: Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y), k: st.k, mx: (p[0].x + p[1].x) / 2, my: (p[0].y + p[1].y) / 2, sx: st.x, sy: st.y };
      }
    };
    function fitK() { var z = size(); return Math.min((vw - 24) / z.w, (vh - top - 24) / z.h, 2.4); }
    function zoomAt(cx, cy, k) {
      k = clamp(k, Math.min(0.1, fitK()), 8);
      st.x = cx - (cx - st.x) * (k / st.k); st.y = cy - (cy - st.y) * (k / st.k); st.k = k; bounds(); put();
    }
    ov.onpointermove = function (e) {
      if (!ptrs[e.pointerId]) return;
      ptrs[e.pointerId] = { x: e.clientX, y: e.clientY };
      var p = pts();
      if (g && g.mode === 'pan' && p.length === 1) { st.x = g.sx + (p[0].x - g.x); st.y = g.sy + (p[0].y - g.y); bounds(); put(); }
      else if (g && g.mode === 'pinch' && p.length === 2) {
        var d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y), k = clamp(g.k * d / g.d, 0.1, 8);
        var cx = (p[0].x + p[1].x) / 2, cy = (p[0].y + p[1].y) / 2;
        st.x = cx - (g.mx - g.sx) * (k / g.k); st.y = cy - (g.my - g.sy) * (k / g.k); st.k = k; bounds(); put();
      }
    };
    ov.onpointerup = ov.onpointercancel = function (e) {
      delete ptrs[e.pointerId];
      var p = pts();
      if (p.length === 1) g = { mode: 'pan', x: p[0].x, y: p[0].y, sx: st.x, sy: st.y };
      else if (!p.length) g = null;
    };
  }
  function closeViewer() {
    if (!viewerOpen) return false;
    ov.hidden = true; ov.innerHTML = ''; viewerOpen = false; call('onViewer', false); return true;
  }
  function pageOf(el) { var b = el.closest('[data-pg]'); return b ? parseInt(b.getAttribute('data-pg'), 10) || 0 : 0; }

  /* ---------------------------------------------------------------- taps */
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (viewerOpen) {
      var act = t.closest('[data-act]'); if (!act) return;
      var a = act.getAttribute('data-act');
      if (a === 'close') closeViewer(); else if (a === 'fit' && ov._fit) ov._fit(); else if (a === 'orig') { var p = ov._page; closeViewer(); call('onOriginal', p); }
      return;
    }
    var sel = window.getSelection && String(window.getSelection());
    if (sel && sel.length > 0) return;
    var act2 = t.closest('[data-act]');
    if (act2) {
      var kind = act2.getAttribute('data-act');
      if (kind === 'fold') { var f = act2.parentNode; f.classList.toggle('open'); act2.setAttribute('aria-expanded', f.classList.contains('open') ? 'true' : 'false'); return; }
      if (kind === 'table') {
        var tw = act2.closest('.tw'), clone = tw.cloneNode(true);
        openViewer(clone, 'Table', pageOf(tw)); return;
      }
    }
    var a2 = t.closest('a[href]');
    if (a2) { e.preventDefault(); var h = a2.getAttribute('href'); if (/^(https?:|mailto:)/i.test(h)) call('onLink', h); return; }
    var im = t.closest('img.zoomable');
    if (im) {
      var c = im.cloneNode(false); c.classList.remove('zoomable'); c.removeAttribute('loading');
      var isFig = !!im.closest('figure'), cap = isFig ? (im.closest('figure').querySelector('figcaption') || {}).textContent : '';
      var big = im.cloneNode(false); big.style.width = Math.max(im.naturalWidth || 0, im.clientWidth * 1.6) + 'px'; big.style.maxWidth = 'none'; big.style.height = 'auto'; big.classList.remove('zoomable');
      openViewer(big, isFig ? (cap ? cap.slice(0, 60) : 'Figure') : 'Equation', pageOf(im)); return;
    }
    if (t.closest('.fold-bar')) return;
    call('onTap', e.clientY / window.innerHeight);
  });

  /* ---------------------------------------------------------------- search */
  var hits = [], cur = -1;
  function clearMarks() {
    $$('mark.hit').forEach(function (m) { var p = m.parentNode; p.replaceChild(document.createTextNode(m.textContent), m); p.normalize(); });
    hits = []; cur = -1;
  }
  function markAll(q) {
    var walker = document.createTreeWalker(doc, NodeFilter.SHOW_TEXT, null), nodes = [], n, lq = q.toLowerCase();
    while ((n = walker.nextNode())) { if (n.nodeValue.length >= q.length && n.parentNode.tagName !== 'SCRIPT') nodes.push(n); }
    nodes.forEach(function (tn) {
      var text = tn.nodeValue, low = text.toLowerCase(), idx = low.indexOf(lq), pos = 0;
      if (idx < 0) return;
      var frag = document.createDocumentFragment();
      while (idx >= 0) {
        if (idx > pos) frag.appendChild(document.createTextNode(text.slice(pos, idx)));
        var m = document.createElement('mark'); m.className = 'hit'; m.textContent = text.slice(idx, idx + q.length); frag.appendChild(m);
        pos = idx + q.length; idx = low.indexOf(lq, pos);
      }
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      tn.parentNode.replaceChild(frag, tn);
    });
    hits = $$('mark.hit');
  }
  function showHit(i) {
    if (!hits.length) { call('onSearch', 0, -1); return; }
    cur = (i + hits.length) % hits.length;
    $$('mark.hit.on').forEach(function (m) { m.classList.remove('on'); });
    var m = hits[cur]; m.classList.add('on');
    var f = m.closest('.fold'); if (f) f.classList.add('open');
    var r = m.getBoundingClientRect();
    window.scrollBy(0, r.top - window.innerHeight * 0.3);
    call('onSearch', hits.length, cur);
    setTimeout(report, 120);
  }
  function search(q) {
    clearMarks();
    if (!q || q.trim().length < 2) { call('onSearch', 0, -1); return; }
    loadAll().then(function () { markAll(q.trim()); showHit(0); });
  }

  /* ---------------------------------------------------------------- speech */
  var speechList = [], speechAt = 0, speakingEl = null;
  var SPEAK = 'h1,h2,h3,h4,p,li,figcaption,.stp,.part,.opt,.ansline,.bt,th,td';
  function leafBlocks() {
    return $$(SPEAK).filter(function (e) { return !e.querySelector(SPEAK) && e.offsetParent !== null && !e.closest('.fold-body') || (e.closest('.fold.open')); });
  }
  function textOf(el) {
    var out = '', w = document.createTreeWalker(el, NodeFilter.SHOW_ALL, null), n;
    while ((n = w.nextNode())) {
      if (n.nodeType === 3) out += n.nodeValue;
      else if (n.tagName === 'IMG' && n.getAttribute('data-tex')) out += ' ' + n.getAttribute('alt') + ' ';
    }
    return out.replace(/\s+/g, ' ').trim();
  }
  function speechBegin() {
    speechList = leafBlocks(); var b = topBlock(), i = 0;
    if (b) for (i = 0; i < speechList.length; i++) { if (speechList[i] === b || b.contains(speechList[i]) || (speechList[i].compareDocumentPosition(b) & 2)) break; }
    speechAt = i;
  }
  function speechNext() {
    if (speakingEl) speakingEl.classList.remove('speaking');
    while (speechAt < speechList.length) {
      var el = speechList[speechAt++], t = textOf(el);
      if (t.length < 2) continue;
      speakingEl = el; el.classList.add('speaking');
      var r = el.getBoundingClientRect();
      if (r.top < S.top || r.bottom > window.innerHeight - 140) window.scrollBy(0, r.top - window.innerHeight * 0.28);
      return t;
    }
    speakingEl = null;
    return '';
  }
  function speechStop() { if (speakingEl) speakingEl.classList.remove('speaking'); speakingEl = null; }

  /* ---------------------------------------------------------------- start */
  function words() {
    var n = 0; $$('p,li', doc).slice(0, 400).forEach(function (e) { n += e.textContent.split(/\s+/).length; }); return n;
  }
  window.NebReader = {
    apply: apply, goPage: goPage, search: search, step: function (d) { showHit(cur + d); }, clear: clearMarks,
    closeViewer: closeViewer, scrollPage: function (d) { window.scrollBy(0, d * window.innerHeight * 0.85); }, speechBegin: speechBegin, speechNext: speechNext, speechStop: speechStop,
    pageNow: function () { return pageNow; }, words: words,
    start: function (page, settings) {
      apply(settings || {});
      return fetch('meta.json').then(function (r) { return r.json(); }).then(function (m) {
        meta = m;
        call('onMeta', JSON.stringify({ title: m.title, pages: m.pages, chapters: m.chapters }));
        return goPage(page || 1);
      }).then(function () { call('onReady'); });
    }
  };
  if (!window.NebAndroid) { // plain browser: the test harness starts it
    window.__standalone = true;
  }
})();
