/* NebBook: the page-turning PDF reader. A PDF becomes a hardcover book: a closed cover that opens, two-page spreads
   on wide screens and single pages on phones, leaves that bend and turn in 3D (drag a corner, swipe, click an edge,
   use the keys), page stacks that grow and shrink as you read, and a reading desk around it: thumbnails, contents,
   full-text search with highlights, bookmarks with notes, a resume point, paper / sepia / night tones, zoom, auto-turn
   and an optional page sound.  Pages are drawn by PDF.js (shared with the classic reader through NebPdf.open) and only
   the few pages around the spread live in memory.

   window.NebBook.mount(src, title, { page, onClassic }) -> { node, ready, goto(n), page(), destroy() }
   `ready` rejects when the file cannot be drawn so the caller can fall back to the classic reader.
   Everything is flat: no shadows, shading is a neutral overlay that follows the leaf angle. */
(function () {
  'use strict';

  var D = document;
  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var PREFS_KEY = 'neb.book.prefs';
  var DEFAULTS = { tone: 'paper', bright: 100, layout: 'auto', speed: 'normal', curl: true, sound: false, interval: 8 };
  var SPEED = { slow: 1250, normal: 820, fast: 520 };
  var STRIPS = 14, CURL = 34, PEEK = 13, CACHE = 14;

  function el(tag, cls, html) {
    var n = D.createElement(tag);
    if (cls) n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  }
  function icon(name) { return '<span class="material-symbols-outlined" aria-hidden="true">' + name + '</span>'; }
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function jget(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function jset(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  function easeInOut(k) { return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }
  function easeOut(k) { return 1 - Math.pow(1 - k, 3); }
  function btn(cls, ic, label, extra) {
    return '<button type="button" class="' + cls + '" aria-label="' + label + '" title="' + label + '"' + (extra || '') + '>' + icon(ic) + '</button>';
  }
  function setLabel(b, t) { b.title = t; b.setAttribute('aria-label', t); }

  function mount(src, title, opts) {
    opts = opts || {};
    var alive = true;
    var prefs = Object.assign({}, DEFAULTS, jget(PREFS_KEY) || {});
    var docKey = 'neb.book.doc:' + src;
    var store = Object.assign({ last: 1, max: 1, time: 0, marks: [] }, jget(docKey) || {});
    var S = {
      doc: null, N: 0, ratio: 1.414, W: 0, H: 0, spread: true, pos: 0, zoom: 1, F: null, busy: false, queue: [], tok: 0,
      hlq: '', panel: '', drag: null, peek: 0, auto: 0, idle: Date.now(), dirty: false, bare: false
    };
    var cache = new Map();
    var texts = {};
    var timers = [];

    /* ---------------------------------------------------------------- DOM */
    var root = el('div', 'bk');
    root.tabIndex = 0;
    root.setAttribute('role', 'application');
    root.setAttribute('aria-label', (title || 'Book') + ', page turning reader');
    root.innerHTML =
      '<div class="bk-desk"><div class="bk-zoom"><div class="bk-book">' +
        '<div class="bk-board bk-bl"></div><div class="bk-board bk-br"></div>' +
        '<div class="bk-stack bk-sl"></div><div class="bk-stack bk-sr"></div>' +
        '<div class="bk-cell bk-l is-empty"><div class="bk-pg"><div class="bk-hls"></div></div></div>' +
        '<div class="bk-cell bk-r is-empty"><div class="bk-pg"><div class="bk-hls"></div></div></div>' +
        '<div class="bk-castw"><div class="bk-cast"></div></div>' +
      '</div></div></div>' +
      '<div class="bk-top bk-ui" role="toolbar" aria-label="Reader tools">' +
        '<div class="bk-grp">' +
          btn('bk-ib', 'grid_view', 'Pages', ' data-panel="pages"') + btn('bk-ib', 'toc', 'Contents', ' data-panel="toc"') +
          btn('bk-ib', 'search', 'Search', ' data-panel="search"') + btn('bk-ib', 'bookmarks', 'Bookmarks', ' data-panel="marks"') +
        '</div>' +
        '<div class="bk-grp">' +
          btn('bk-ib', 'bookmark_add', 'Bookmark this page', ' data-act="mark"') + btn('bk-ib', 'tune', 'Reading settings', ' data-act="settings"') +
          btn('bk-ib bk-hide-s', 'keyboard', 'Keyboard shortcuts', ' data-act="help"') +
        '</div>' +
      '</div>' +
      '<div class="bk-dock bk-ui">' +
        '<div class="bk-grp bk-nav">' + btn('bk-ib bk-hide-s', 'first_page', 'First page', ' data-act="first"') + btn('bk-ib', 'chevron_left', 'Previous page', ' data-act="prev"') + '</div>' +
        '<div class="bk-scrub"><div class="bk-track"><i class="bk-fill"></i><span class="bk-ticks"></span></div><input type="range" class="bk-range" min="1" max="1" value="1" aria-label="Go to page"><span class="bk-tip" hidden></span></div>' +
        '<button type="button" class="bk-pill" data-act="goto" aria-label="Go to page"><b>1</b><i>/ 1</i></button>' +
        '<div class="bk-grp bk-nav">' + btn('bk-ib', 'chevron_right', 'Next page', ' data-act="next"') + btn('bk-ib bk-hide-s bk-mirror', 'first_page', 'Last page', ' data-act="last"') + '</div>' +
        '<div class="bk-sep bk-hide-s"></div>' +
        '<div class="bk-grp bk-hide-s">' + btn('bk-ib', 'remove', 'Zoom out', ' data-act="zout"') + '<button type="button" class="bk-zl" data-act="zreset" aria-label="Reset zoom">100%</button>' + btn('bk-ib', 'add', 'Zoom in', ' data-act="zin"') + btn('bk-ib', 'play_arrow', 'Turn pages automatically', ' data-auto="1"') + '</div>' +
      '</div>' +
      '<aside class="bk-panel bk-ui" hidden aria-label="Book panel"></aside>' +
      '<div class="bk-pop bk-ui" hidden role="dialog" aria-label="Reading settings"></div>' +
      '<div class="bk-help bk-ui" hidden role="dialog" aria-label="Keyboard shortcuts"></div>' +
      '<div class="bk-toast" hidden role="status"></div>' +
      '<div class="bk-load"><span class="bk-spin"></span></div>';

    function $(s) { return root.querySelector(s); }
    var desk = $('.bk-desk'), zoomBox = $('.bk-zoom'), book = $('.bk-book');
    var boardL = $('.bk-bl'), boardR = $('.bk-br'), stackL = $('.bk-sl'), stackR = $('.bk-sr');
    var cells = { l: { el: $('.bk-l'), n: 0 }, r: { el: $('.bk-r'), n: 0 } };
    var cast = $('.bk-cast');
    var panel = $('.bk-panel'), pop = $('.bk-pop'), help = $('.bk-help'), toastEl = $('.bk-toast'), loadEl = $('.bk-load');
    var range = $('.bk-range'), track = $('.bk-ticks'), scrub = $('.bk-scrub'), tip = $('.bk-tip');
    var pill = $('.bk-pill'), markBtn = $('[data-act="mark"]'), autoBtn = $('[data-auto]'), zl = $('.bk-zl');
    var settingsBtn = $('[data-act="settings"]');

    /* ---------------------------------------------------------------- small model helpers */
    function pg(n) { return n >= 1 && n <= S.N ? n : 0; }
    function maxPos() { return S.spread ? Math.floor(S.N / 2) : S.N - 1; }
    function pagesAt(pos) { return S.spread ? { l: pg(2 * pos), r: pg(2 * pos + 1) } : { l: 0, r: pg(pos + 1) }; }
    function posOf(n) { n = clamp(n, 1, S.N); return S.spread ? Math.floor(n / 2) : n - 1; }
    function cur() { var p = pagesAt(S.pos); return p.l || p.r || 1; }
    function visible() { var p = pagesAt(S.pos); return [p.l, p.r].filter(Boolean); }
    function leafPages(s) { return S.spread ? { f: pg(2 * s + 1), b: pg(2 * s + 2) } : { f: pg(s + 1), b: 0 }; }
    function canTurn(dir) { return dir > 0 ? S.pos < maxPos() : S.pos > 0; }
    function shiftFor(t) {
      if (!S.spread) return 0;
      if (t <= 0) return -S.W / 2;
      if (S.N % 2 === 0 && t >= maxPos()) return S.W / 2;
      return 0;
    }
    function shiftAt(tf) {
      var a = Math.floor(tf + 1e-9), f = tf - a;
      return shiftFor(a) * (1 - f) + shiftFor(Math.min(a + 1, maxPos())) * f;
    }

    /* ---------------------------------------------------------------- rendering */
    function dims() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var k = Math.min(dpr, 2800 / Math.max(S.W, 1));
      return { pw: Math.max(2, Math.round(S.W * k)), ph: Math.max(2, Math.round(S.H * k)) };
    }
    function keyOf(n, d) { return n + '@' + d.pw; }
    function cachedCanvas(n) { var e = cache.get(keyOf(n, dims())); return e && e.c || null; }
    function near(n) { var c = cur(); return n >= c - 6 && n <= c + 8; }
    function trim() {
      if (cache.size <= CACHE) return;
      var d = dims();
      cache.forEach(function (e, k) {
        if (cache.size <= CACHE || !e.c || e.c.isConnected) return;
        if (e.pw !== d.pw || !near(e.n)) { e.c.width = 0; cache.delete(k); }
      });
    }
    function renderPage(n) {
      var d = dims(), key = keyOf(n, d), hit = cache.get(key);
      if (hit) { cache.delete(key); cache.set(key, hit); return hit.p; }
      var entry = { n: n, pw: d.pw, c: null, p: null };
      entry.p = S.doc.getPage(n).then(function (page) {
        var v1 = page.getViewport({ scale: 1 });
        var vp = page.getViewport({ scale: Math.min(d.pw / v1.width, d.ph / v1.height) });
        var c = D.createElement('canvas');
        c.width = d.pw; c.height = d.ph;
        var ctx = c.getContext('2d');
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, d.pw, d.ph);
        return page.render({ canvasContext: ctx, viewport: vp, transform: [1, 0, 0, 1, (d.pw - vp.width) / 2, (d.ph - vp.height) / 2] }).promise.then(function () {
          entry.c = c;
          trim();
          return c;
        });
      });
      entry.p.catch(function () { cache.delete(key); });
      cache.set(key, entry);
      return entry.p;
    }

    function fillCell(cell, n) {
      cell.n = n;
      var box = cell.el, page = box.firstChild, old = page.querySelector('canvas');
      box.classList.toggle('is-empty', !n);
      if (!n) { if (old) old.remove(); clearHL(page); box.classList.remove('is-wait'); return; }
      var c = cachedCanvas(n);
      if (c) { attach(cell, c, n); return; }
      box.classList.add('is-wait');
      renderPage(n).then(function (cv) { if (alive && cell.n === n) attach(cell, cv, n); }, function () { box.classList.remove('is-wait'); });
    }
    function attach(cell, c, n) {
      var page = cell.el.firstChild, old = page.querySelector('canvas');
      if (old && old !== c) old.remove();
      if (c.parentNode !== page) page.insertBefore(c, page.firstChild);
      cell.el.classList.remove('is-wait');
      drawHL(cell, n);
    }
    function refreshCells() {
      var p = pagesAt(S.pos);
      fillCell(cells.l, p.l);
      fillCell(cells.r, p.r);
    }

    var preToken = 0;
    function prefetch() {
      var tok = ++preToken, c = cur(), list = [];
      var span = S.spread ? [1, 2, 3, 4, 5, 6] : [1, 2, 3];
      span.forEach(function (i) { list.push(c + i); });
      [1, 2, 3].forEach(function (i) { list.push(c - i); });
      list = list.filter(pg).filter(function (n) { return !cachedCanvas(n); });
      (function next() {
        if (!list.length || tok !== preToken || !alive) return;
        renderPage(list.shift()).then(function () { timers.push(setTimeout(next, 30)); }, next);
      })();
    }

    /* ---------------------------------------------------------------- layout */
    function leftPad() { return S.panel && root.clientWidth >= 720 ? 344 : 0; }
    function measure() {
      var dw = desk.clientWidth, dh = desk.clientHeight, lay = prefs.layout, pad = leftPad();
      var spread = S.N > 1 && (lay === 'two' || (lay === 'auto' && dw - pad >= 700));
      var narrow = dw < 640;
      var availH = Math.max(220, dh - (narrow ? 64 : 70) - (narrow ? 84 : 90));
      var availW = dw - pad - (narrow ? 20 : 64);
      var w = spread ? Math.min(availW / 2, availH / S.ratio) : Math.min(availW, availH / S.ratio);
      w = Math.floor(Math.max(110, w) * S.zoom);
      return { spread: spread, W: w, H: Math.round(w * S.ratio), pad: pad };
    }
    function applyLayout() {
      var m = measure();
      var page = cur();
      var changed = m.spread !== S.spread;
      if (S.F) discardFlip();
      S.spread = m.spread; S.W = m.W; S.H = m.H;
      if (changed) S.pos = posOf(page);
      S.pos = clamp(S.pos, 0, maxPos());
      book.style.width = (S.spread ? S.W * 2 : S.W) + 'px';
      book.style.height = S.H + 'px';
      zoomBox.style.paddingLeft = (m.pad + (S.zoom > 1 ? S.W / 2 : 0)) + 'px';
      zoomBox.style.paddingRight = (S.zoom > 1 ? S.W / 2 : 0) + 'px';
      [cells.l, cells.r].forEach(function (c) { c.el.style.width = S.W + 'px'; c.el.style.height = S.H + 'px'; });
      cells.l.el.style.left = '0px';
      cells.r.el.style.left = (S.spread ? S.W : 0) + 'px';
      cells.l.el.style.display = S.spread ? '' : 'none';
      root.dataset.spread = S.spread ? '1' : '0';
      if (changed || S.W !== applyLayout.lastW) { applyLayout.lastW = S.W; refreshCells(); }
      visuals(S.pos);
      syncUI();
    }

    /* Stacks, boards, shift and the shade cast on the page below: all a function of "tf", how many leaves are over. */
    function visuals(tf, theta, leaf) {
      var Lc = S.spread ? Math.ceil(S.N / 2) : S.N;
      var unit = Math.min(0.9, S.W * 0.0028), cap = Math.min(18, S.W * 0.05);
      var tl = clamp(tf * unit, 0, cap), tr = clamp((Lc - tf) * unit, 0, cap);
      var bw = S.spread ? S.W * 2 : S.W;
      stackL.style.width = tl + 'px'; stackL.style.left = (-tl) + 'px'; stackL.style.height = (S.H - 4) + 'px';
      stackR.style.width = tr + 'px'; stackR.style.left = bw + 'px'; stackR.style.height = (S.H - 4) + 'px';
      stackL.hidden = tl < 0.6 || !S.spread && tf < 0.5;
      stackR.hidden = tr < 0.6;
      var bl = S.spread ? clamp(tf, 0, 1) : 0;
      var br = S.spread && S.N % 2 === 0 ? clamp(maxPos() - tf, 0, 1) : 1;
      boardL.style.width = (S.W + 16) + 'px'; boardL.style.height = (S.H + 16) + 'px'; boardL.style.left = '-8px';
      boardL.style.transform = 'scaleX(' + Math.max(bl, 0.001) + ')'; boardL.style.opacity = bl > 0.01 ? 1 : 0;
      boardR.style.width = (S.W + 16) + 'px'; boardR.style.height = (S.H + 16) + 'px'; boardR.style.left = ((S.spread ? S.W : 0) - 8) + 'px';
      boardR.style.transform = 'scaleX(' + Math.max(br, 0.001) + ')'; boardR.style.opacity = br > 0.01 ? 1 : 0;
      boardR.style.transformOrigin = S.spread ? '0 50%' : '50% 50%';
      book.style.transform = 'translateX(' + shiftAt(tf).toFixed(2) + 'px)';
      if (theta == null) { cast.style.opacity = 0; return; }
      var rad = theta * Math.PI / 180, spine = S.spread ? S.W : 0, reach = S.W * 0.34;
      var tipX = spine + S.W * Math.cos(rad);
      cast.style.width = reach + 'px';
      if (theta < 90) { cast.style.left = tipX + 'px'; cast.dataset.side = 'r'; }
      else { cast.style.left = (tipX - reach) + 'px'; cast.dataset.side = 'l'; }
      cast.style.height = S.H + 'px';
      // A shade only falls on a page that is there: not on the empty side of a closed cover.
      var under = theta < 90 ? !!pg(S.spread ? 2 * leaf + 3 : leaf + 2) : (S.spread && leaf > 0);
      cast.style.opacity = under ? (0.55 * Math.sin(rad)).toFixed(3) : 0;
    }

    /* ---------------------------------------------------------------- the turning leaf */
    function slice(src, x0, w) {
      var k = src.width / S.W, c = D.createElement('canvas');
      c.width = Math.max(1, Math.ceil(w * k)); c.height = src.height;
      c.style.width = w + 'px'; c.style.height = S.H + 'px';
      c.getContext('2d').drawImage(src, x0 * k, 0, w * k, src.height, 0, 0, c.width, c.height);
      return c;
    }
    function makeFlip(dir, cb) {
      var s = dir > 0 ? S.pos : S.pos - 1, lp = leafPages(s), tok = ++S.tok;
      Promise.all([renderPage(lp.f), lp.b ? renderPage(lp.b) : null]).then(function (cv) {
        if (!alive || tok !== S.tok) return;
        var n = prefs.curl ? STRIPS : 1, sw = S.W / n, ov = n > 1 ? 1 : 0;
        var holder = el('div', 'bk-flip');
        holder.style.left = (S.spread ? S.W : 0) + 'px';
        holder.style.width = S.W + 'px';
        holder.style.height = S.H + 'px';
        var strips = [], parent = holder;
        for (var i = 0; i < n; i++) {
          var st = el('div', 'bk-s');
          st.style.width = (sw + ov) + 'px';
          st.style.height = S.H + 'px';
          if (i > 0) st.style.left = sw + 'px';
          var f = el('div', 'bk-sf'), b = el('div', 'bk-sb');
          f.appendChild(slice(cv[0], sw * i, sw + ov));
          if (cv[1]) b.appendChild(slice(cv[1], S.W - (i + 1) * sw - ov, sw + ov));
          var fs = el('i', 'bk-sh'), bs = el('i', 'bk-sh');
          f.appendChild(fs); b.appendChild(bs);
          if (i === 0) { f.classList.add('is-gut'); b.classList.add('is-gut'); }
          st.appendChild(f); st.appendChild(b);
          parent.appendChild(st);
          strips.push({ st: st, fs: fs, bs: bs });
          parent = st;
        }
        book.appendChild(holder);
        var F = { s: s, dir: dir, theta: dir > 0 ? 0 : 180, el: holder, strips: strips, raf: 0, mode: 'drag' };
        S.F = F;
        // The page the leaf uncovers is put in place straight away.
        if (dir > 0) fillCell(cells.r, S.spread ? pg(2 * S.pos + 3) : pg(S.pos + 2));
        else if (S.spread) fillCell(cells.l, pg(2 * S.pos - 2));
        setTheta(F, F.theta);
        cb(F);
      }, function () { /* a page that cannot be drawn: the turn is skipped */ });
    }
    function shade(a, front) {
      var r = (front ? clamp(a, 0, 90) : clamp(180 - a, 0, 90)) * Math.PI / 180;
      return (0.36 * Math.pow(Math.sin(r), 1.45)).toFixed(3);
    }
    function setTheta(F, theta) {
      F.theta = theta;
      var n = F.strips.length, rad = theta * Math.PI / 180;
      var local = n > 1 ? (CURL * Math.sin(rad)) / n : 0;
      for (var i = 0; i < n; i++) {
        var deg = i === 0 ? -theta : local;
        F.strips[i].st.style.transform = 'rotateY(' + deg.toFixed(3) + 'deg)';
        var a = theta - i * local;
        F.strips[i].fs.style.opacity = shade(a, true);
        F.strips[i].bs.style.opacity = shade(a, false);
      }
      F.el.style.opacity = !S.spread && theta > 140 ? clamp(1 - (theta - 140) / 40, 0, 1) : 1;
      visuals(F.s + theta / 180, theta, F.s);
    }
    function tween(F, to, ms, ease, done) {
      cancelAnimationFrame(F.raf);
      var from = F.theta, t0 = performance.now();
      ms = reduced ? 1 : Math.max(120, ms * Math.abs(to - from) / 180);
      (function step(now) {
        var k = clamp((now - t0) / ms, 0, 1);
        setTheta(F, from + (to - from) * ease(k));
        if (k < 1) F.raf = requestAnimationFrame(step); else { F.raf = 0; if (done) done(); }
      })(t0);
    }
    function discardFlip() {
      var F = S.F;
      S.tok++;
      if (!F) return;
      cancelAnimationFrame(F.raf);
      F.el.remove();
      S.F = null;
      refreshCells();
      visuals(S.pos);
    }
    function getFlip(dir, cb) {
      if (S.F && S.F.dir === dir) { cb(S.F); return; }
      if (S.F) discardFlip();
      makeFlip(dir, cb);
    }
    function land(F, completed) {
      cancelAnimationFrame(F.raf);
      if (completed) S.pos = clamp(S.pos + F.dir, 0, maxPos());
      S.tok++;
      refreshCells();
      F.el.remove();
      S.F = null;
      S.busy = false;
      visuals(S.pos);
      onMoved();
      if (S.queue.length) runQueue();
    }
    function finish(F, completed, ms, ease) {
      S.busy = true;
      F.mode = 'go';
      var to = completed ? (F.dir > 0 ? 180 : 0) : (F.dir > 0 ? 0 : 180);
      if (completed) chirp();
      tween(F, to, ms || SPEED[prefs.speed], ease || easeInOut, function () { land(F, completed); });
    }
    function turn(dir, fast) {
      if (S.busy) { S.queue.push(dir); return; }
      if (!canTurn(dir)) { nudge(dir); return; }
      var ms = fast ? 300 : SPEED[prefs.speed];
      getFlip(dir, function (F) { finish(F, true, ms); });
    }
    function runQueue() {
      if (S.busy || !S.queue.length) return;
      var d = S.queue.shift();
      turn(d, S.queue.length > 0);
    }
    function nudge(dir) {
      if (!book.animate || reduced) return;
      book.animate([{ translate: '0 0' }, { translate: (dir > 0 ? '-10px' : '10px') + ' 0' }, { translate: '0 0' }], { duration: 300, easing: 'cubic-bezier(.2,1.2,.3,1)' });
    }
    function jump(t) {
      if (S.F) discardFlip();
      S.queue = [];
      S.pos = clamp(t, 0, maxPos());
      book.style.transition = reduced ? '' : 'transform .5s cubic-bezier(.2,1,.3,1)';
      refreshCells();
      visuals(S.pos);
      timers.push(setTimeout(function () { book.style.transition = ''; }, 560));
      if (book.animate && !reduced) book.animate([{ opacity: 0.2, scale: '.97' }, { opacity: 1, scale: '1' }], { duration: 380, easing: 'cubic-bezier(.2,1,.3,1)' });
      onMoved();
    }
    function goPos(t) {
      t = clamp(t, 0, maxPos());
      if (S.busy) { S.queue = []; return; }
      if (S.F) discardFlip();
      var d = t - S.pos, n = Math.abs(d);
      if (!n) return;
      if (n <= 6 && !reduced) {
        S.queue = [];
        for (var i = 1; i < n; i++) S.queue.push(d > 0 ? 1 : -1);
        turn(d > 0 ? 1 : -1, n > 1);
      } else jump(t);
    }
    function goto(page) { goPos(posOf(clamp(Math.round(page) || 1, 1, S.N))); }

    /* ---------------------------------------------------------------- page sound */
    var actx = null, noise = null;
    function chirp() {
      if (!prefs.sound) return;
      try {
        actx = actx || new (window.AudioContext || window.webkitAudioContext)();
        if (actx.state === 'suspended') actx.resume();
        if (!noise) {
          var len = Math.floor(actx.sampleRate * 0.32), buf = actx.createBuffer(1, len, actx.sampleRate), d = buf.getChannelData(0);
          for (var i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.2);
          noise = buf;
        }
        var src2 = actx.createBufferSource(), flt = actx.createBiquadFilter(), g = actx.createGain(), t = actx.currentTime;
        src2.buffer = noise;
        flt.type = 'bandpass'; flt.Q.value = 0.7;
        flt.frequency.setValueAtTime(2600, t); flt.frequency.exponentialRampToValueAtTime(700, t + 0.3);
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.22, t + 0.04); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.32);
        src2.connect(flt); flt.connect(g); g.connect(actx.destination);
        src2.start(t);
      } catch (e) { /* audio is optional */ }
    }

    /* ---------------------------------------------------------------- pointer: peek, drag, tap */
    function bookRect() { return book.getBoundingClientRect(); }
    function zoneAt(e) {
      var r = bookRect();
      if (e.clientY < r.top || e.clientY > r.bottom || e.clientX < r.left - 30 || e.clientX > r.right + 30) return 0;
      var edge = S.W * (S.spread ? 0.16 : 0.22), x = e.clientX - r.left, p = pagesAt(S.pos);
      if (S.spread) {
        if (p.r && x > S.W * 2 - edge) return 1;
        if (p.l && x < edge) return -1;
        return 0;
      }
      if (x > S.W - edge) return 1;
      if (x < edge) return -1;
      return 0;
    }
    function peekTo(dir) {
      if (S.peek === dir) return;
      S.peek = dir;
      if (!dir) {
        var F = S.F;
        if (F && F.mode === 'peek') tween(F, F.dir > 0 ? 0 : 180, 420, easeOut, function () { if (S.F === F && F.mode === 'peek') discardFlip(); });
        else S.tok++;
        desk.style.cursor = '';
        return;
      }
      if (!canTurn(dir) || S.busy || S.drag || S.zoom > 1) { S.peek = 0; return; }
      desk.style.cursor = 'pointer';
      getFlip(dir, function (F2) {
        if (S.peek !== dir) { if (F2.mode !== 'go') discardFlip(); return; }
        F2.mode = 'peek';
        tween(F2, dir > 0 ? PEEK : 180 - PEEK, 520, easeOut);
      });
    }
    desk.addEventListener('pointerdown', function (e) {
      if (e.button > 0 || S.busy) return;
      stopAuto();
      root.focus({ preventScroll: true });
      S.drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, x: e.clientX, mode: null, pts: [{ x: e.clientX, t: performance.now() }], sl: desk.scrollLeft, st: desk.scrollTop, touch: e.pointerType !== 'mouse' };
      try { desk.setPointerCapture(e.pointerId); } catch (x) { /* ok */ }
    });
    desk.addEventListener('pointermove', function (e) {
      var d = S.drag;
      if (!d) {
        if (e.pointerType === 'mouse' && S.zoom === 1 && !S.busy) peekTo(zoneAt(e));
        return;
      }
      if (e.pointerId !== d.id) return;
      var dx = e.clientX - d.x0, dy = e.clientY - d.y0;
      d.x = e.clientX;
      d.pts.push({ x: e.clientX, t: performance.now() });
      if (d.pts.length > 5) d.pts.shift();
      if (!d.mode && (Math.abs(dx) > 8 || Math.abs(dy) > 8)) {
        if (S.zoom > 1) { d.mode = 'pan'; desk.classList.add('is-pan'); }
        else if (Math.abs(dx) > Math.abs(dy) * 0.7) {
          var dir = dx < 0 ? 1 : -1;
          if (!canTurn(dir)) d.mode = 'none';
          else {
            d.mode = 'wait'; d.dir = dir;
            if (S.F && S.F.dir !== dir) discardFlip();
            S.peek = 0;
            getFlip(dir, function (F) {
              if (S.drag !== d) { if (F.mode !== 'go') discardFlip(); return; }
              cancelAnimationFrame(F.raf); F.raf = 0;
              F.mode = 'drag'; d.F = F; d.xs = d.x; d.th0 = F.theta; d.mode = 'flip';
              root.classList.add('is-turning');
            });
          }
        } else d.mode = 'none';
      }
      if (d.mode === 'pan') { desk.scrollLeft = d.sl - dx; desk.scrollTop = d.st - dy; }
      if (d.mode === 'flip') setTheta(d.F, clamp(d.th0 - ((e.clientX - d.xs) / (S.W * 1.1)) * 180, 0, 180));
    });
    function release(e) {
      var d = S.drag;
      if (!d || e.pointerId !== d.id) return;
      S.drag = null;
      root.classList.remove('is-turning');
      desk.classList.remove('is-pan');
      if (d.mode === 'flip') {
        var F = d.F, p = d.pts, v = 0;
        if (p.length > 1) v = (p[p.length - 1].x - p[0].x) / Math.max(1, p[p.length - 1].t - p[0].t);
        var fwd = F.dir > 0, ok;
        if (Math.abs(v) > 0.55) ok = fwd ? v < 0 : v > 0;
        else ok = fwd ? F.theta > 75 : F.theta < 105;
        finish(F, ok, Math.abs(v) > 0.9 ? 520 : null);
      } else if (d.mode === 'wait') {
        discardFlip();
      } else if (!d.mode && e.type === 'pointerup') {
        tap(e, d);
      }
    }
    desk.addEventListener('pointerup', release);
    desk.addEventListener('pointercancel', release);
    desk.addEventListener('pointerleave', function (e) { if (!S.drag && e.pointerType === 'mouse') peekTo(0); });
    function tap(e, d) {
      var r = bookRect(), x = e.clientX - r.left, bw = r.width, dir = 0;
      if (S.spread) { if (x >= 0 && x <= bw) dir = x < bw / 2 ? -1 : 1; }
      else dir = x < bw * 0.33 ? -1 : (x > bw * 0.67 ? 1 : 0);
      if (dir && S.zoom === 1) {
        if (S.F && S.F.mode === 'peek' && S.F.dir === dir) { S.peek = 0; finish(S.F, true); }
        else { S.peek = 0; if (S.F) discardFlip(); turn(dir); }
        return;
      }
      if (!dir && d.touch) toggleBare();
    }
    function toggleBare() { S.bare = !S.bare; root.classList.toggle('is-bare', S.bare); }
    desk.addEventListener('dblclick', function (e) {
      if (!e.target.closest || !e.target.closest('.bk-cell')) return;
      setZoom(S.zoom > 1 ? 1 : 2);
      e.preventDefault();
    });
    var wheelAcc = 0, wheelT = 0;
    desk.addEventListener('wheel', function (e) {
      if (e.ctrlKey) { e.preventDefault(); setZoom(S.zoom + (e.deltaY < 0 ? 0.25 : -0.25)); return; }
      if (S.zoom > 1 || Math.abs(e.deltaX) < Math.abs(e.deltaY) * 1.2) return;
      e.preventDefault();
      wheelAcc += e.deltaX;
      clearTimeout(wheelT);
      wheelT = setTimeout(function () { wheelAcc = 0; }, 160);
      if (Math.abs(wheelAcc) > 70 && !S.busy) { var dir = wheelAcc > 0 ? 1 : -1; wheelAcc = 0; turn(dir); }
    }, { passive: false });
    root.addEventListener('contextmenu', function (e) { e.preventDefault(); });

    /* ---------------------------------------------------------------- zoom, tones, preferences */
    function setZoom(z) {
      z = clamp(Math.round(z * 4) / 4, 1, 3);
      if (z === S.zoom) return;
      S.zoom = z;
      root.classList.toggle('is-zoomed', z > 1);
      applyLayout();
      zl.textContent = Math.round(z * 100) + '%';
      desk.scrollLeft = (desk.scrollWidth - desk.clientWidth) / 2;
      desk.scrollTop = (desk.scrollHeight - desk.clientHeight) / 2;
    }
    function applyPrefs() {
      root.dataset.tone = prefs.tone;
      root.style.setProperty('--bk-bright', (prefs.bright / 100).toFixed(2));
      jset(PREFS_KEY, prefs);
    }
    function toast(msg, action, fn) {
      toastEl.innerHTML = '';
      var sp = el('span');
      sp.textContent = msg;
      toastEl.appendChild(sp);
      if (action) {
        var b = el('button');
        b.type = 'button'; b.textContent = action;
        b.addEventListener('click', function () { fn(); toastEl.hidden = true; });
        toastEl.appendChild(b);
      }
      toastEl.hidden = false;
      toastEl.classList.remove('is-in'); void toastEl.offsetWidth; toastEl.classList.add('is-in');
      clearTimeout(toast.t);
      toast.t = setTimeout(function () { toastEl.hidden = true; }, action ? 6500 : 2600);
    }

    /* ---------------------------------------------------------------- reading state and chrome */
    function label() {
      var p = pagesAt(S.pos);
      if (p.l && p.r) return p.l + '\u2013' + p.r;
      return String(p.l || p.r || 1);
    }
    function isMarked(n) { return store.marks.some(function (m) { return m.p === n; }); }
    function syncUI() {
      if (!S.N) return;
      var c = cur(), marked = visible().some(isMarked);
      pill.firstChild.textContent = label();
      pill.lastChild.textContent = '/ ' + S.N;
      range.max = S.N; range.value = c;
      scrub.style.setProperty('--p', S.N > 1 ? ((c - 1) / (S.N - 1) * 100).toFixed(2) + '%' : '0%');
      markBtn.classList.toggle('is-on', marked);
      markBtn.firstChild.textContent = marked ? 'bookmark_check' : 'bookmark_add';
      setLabel(markBtn, marked ? 'Remove bookmark' : 'Bookmark this page');
      $('[data-act="prev"]').disabled = S.pos <= 0;
      $('[data-act="first"]').disabled = S.pos <= 0;
      $('[data-act="next"]').disabled = S.pos >= maxPos();
      $('[data-act="last"]').disabled = S.pos >= maxPos();
      zl.textContent = Math.round(S.zoom * 100) + '%';
      drawTicks();
      if (S.panel === 'pages') markThumbs();
      if (S.panel === 'marks') renderMarks();
    }
    function drawTicks() {
      track.innerHTML = '';
      if (S.N < 2) return;
      store.marks.forEach(function (m) {
        var t = el('i', 'bk-tick');
        t.style.left = ((m.p - 1) / (S.N - 1) * 100) + '%';
        track.appendChild(t);
      });
    }
    function onMoved() {
      S.idle = Date.now();
      var c = cur(), hi = Math.max.apply(null, visible());
      store.last = c; store.max = Math.max(store.max || 1, hi); S.dirty = true;
      syncUI();
      refreshHL();
      prefetch();
      saveSoon();
    }
    var saveT = 0;
    function saveSoon() { if (!saveT) saveT = setTimeout(save, 1500); }
    function save() { clearTimeout(saveT); saveT = 0; if (S.dirty) { jset(docKey, store); S.dirty = false; } }
    timers.push(setInterval(function () {
      if (!alive) return;
      if (!D.hidden && root.isConnected && Date.now() - S.idle < 90000) { store.time++; S.dirty = true; }
      if (S.panel === 'marks' && store.time % 30 === 0) renderMarks();
      save();
    }, 1000));
    function onHide() { save(); }
    window.addEventListener('pagehide', onHide);

    function startAuto() {
      stopAuto();
      S.auto = setInterval(function () {
        if (S.busy || S.drag) return;
        if (!canTurn(1)) { stopAuto(); toast('End of the book'); return; }
        turn(1);
      }, Math.max(3, prefs.interval) * 1000);
      autoBtn.classList.add('is-on'); autoBtn.firstChild.textContent = 'pause';
      setLabel(autoBtn, 'Stop turning automatically');
    }
    function stopAuto() {
      if (S.auto) clearInterval(S.auto);
      S.auto = 0;
      autoBtn.classList.remove('is-on'); autoBtn.firstChild.textContent = 'play_arrow';
      setLabel(autoBtn, 'Turn pages automatically');
    }
    function toggleAuto() { if (S.auto) stopAuto(); else { startAuto(); turn(1); } }

    /* ---------------------------------------------------------------- text, search, highlights */
    function textInfo(n) {
      if (!texts[n]) {
        texts[n] = S.doc.getPage(n).then(function (page) {
          var vp = page.getViewport({ scale: 1 });
          return page.getTextContent().then(function (tc) {
            var items = [], offs = [], str = '', i, it;
            for (i = 0; i < tc.items.length; i++) {
              it = tc.items[i];
              if (typeof it.str !== 'string') continue;
              offs.push(str.length); items.push(it);
              str += it.str + ' ';
            }
            return { vp: vp, items: items, offs: offs, str: str, low: str.toLowerCase(), styles: tc.styles || {} };
          });
        }).catch(function () { return { vp: null, items: [], offs: [], str: '', low: '', styles: {} }; });
      }
      return texts[n];
    }
    var mctx = D.createElement('canvas').getContext('2d');
    function clearHL(page) { var h = page.querySelector('.bk-hls'); if (h) h.innerHTML = ''; }
    function drawHL(cell, n) {
      var box = cell.el.firstChild.querySelector('.bk-hls'), q = S.hlq;
      if (!box) return;
      box.innerHTML = '';
      if (!q || q.length < 2) return;
      textInfo(n).then(function (info) {
        if (!alive || cell.n !== n || S.hlq !== q || !info.vp) return;
        box.innerHTML = '';
        var from = 0, idx, ql = q.toLowerCase(), vp = info.vp, k, it, s0, e0, f0, f1, p1, p2, h, m;
        while ((idx = info.low.indexOf(ql, from)) !== -1 && box.childNodes.length < 80) {
          from = idx + ql.length;
          for (k = 0; k < info.items.length; k++) {
            it = info.items[k]; s0 = info.offs[k]; e0 = s0 + it.str.length;
            if (!it.str.length || e0 <= idx || s0 >= from) continue;
            var ia = Math.max(idx, s0) - s0, ib = Math.min(from, e0) - s0;
            f0 = ia / it.str.length; f1 = ib / it.str.length;
            // The line is one text item; measure with its own font so a match in the middle lands on the right letters.
            mctx.font = Math.abs(it.transform[3] || it.height || 10) + 'px ' + ((info.styles[it.fontName] || {}).fontFamily || 'sans-serif');
            var full = mctx.measureText(it.str).width;
            if (full > 0) { f0 = mctx.measureText(it.str.slice(0, ia)).width / full; f1 = mctx.measureText(it.str.slice(0, ib)).width / full; }
            h = it.height || Math.hypot(it.transform[2], it.transform[3]) || 10;
            p1 = vp.convertToViewportPoint(it.transform[4] + f0 * it.width, it.transform[5] - 0.2 * h);
            p2 = vp.convertToViewportPoint(it.transform[4] + f1 * it.width, it.transform[5] + 0.85 * h);
            m = el('i', 'bk-hl');
            m.style.left = (Math.min(p1[0], p2[0]) / vp.width * 100) + '%';
            m.style.top = (Math.min(p1[1], p2[1]) / vp.height * 100) + '%';
            m.style.width = (Math.abs(p2[0] - p1[0]) / vp.width * 100) + '%';
            m.style.height = (Math.abs(p2[1] - p1[1]) / vp.height * 100) + '%';
            box.appendChild(m);
          }
        }
      });
    }
    function refreshHL() { if (S.hlq) { drawHL(cells.l, cells.l.n); drawHL(cells.r, cells.r.n); } }

    /* ---------------------------------------------------------------- panels */
    var P = { thumbs: null, thQ: [], thBusy: false, outline: null, sIndexed: 0, sRunning: false, sResults: [], sInput: null, sList: null, sStat: null, mStats: null, mList: null, mAdd: null };
    var TITLES = { pages: 'Pages', toc: 'Contents', search: 'Search', marks: 'Bookmarks' };

    function openPanel(name) {
      togglePop(false);
      if (S.panel === name) { closePanel(); return; }
      S.panel = name;
      panel.hidden = false;
      panel.innerHTML = '<div class="bk-ph"><b></b>' + btn('bk-ib', 'close', 'Close panel', ' data-act="closepanel"') + '</div><div class="bk-pb"></div>';
      panel.firstChild.firstChild.textContent = TITLES[name];
      panel.classList.remove('is-in'); void panel.offsetWidth; panel.classList.add('is-in');
      root.dataset.open = name;
      root.querySelectorAll('[data-panel]').forEach(function (b) { b.classList.toggle('is-on', b.dataset.panel === name); });
      var body = panel.lastChild;
      if (name === 'pages') buildThumbs(body);
      else if (name === 'toc') buildToc(body);
      else if (name === 'search') buildSearch(body);
      else buildMarks(body);
      relayoutSoon();
    }
    function closePanel() {
      S.panel = '';
      panel.hidden = true;
      panel.innerHTML = '';
      P.thumbs = null; P.thQ = []; P.sList = null; P.mList = null;
      root.dataset.open = '';
      root.querySelectorAll('[data-panel]').forEach(function (b) { b.classList.remove('is-on'); });
      relayoutSoon();
    }
    var relT = 0;
    function relayoutSoon() { clearTimeout(relT); relT = setTimeout(function () { if (alive) applyLayout(); }, 40); }
    function leavePanelOnPhone() { if (root.clientWidth < 720) closePanel(); }

    function buildThumbs(body) {
      var grid = el('div', 'bk-thumbs'), io = null, n, b;
      P.thumbs = grid;
      if ('IntersectionObserver' in window) {
        io = new IntersectionObserver(function (es) {
          es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); queueThumb(e.target); } });
        }, { root: body, rootMargin: '300px 0px' });
      }
      for (n = 1; n <= S.N; n++) {
        b = el('button', 'bk-th');
        b.type = 'button'; b.dataset.n = n;
        b.setAttribute('aria-label', 'Page ' + n);
        b.innerHTML = '<span class="bk-thp" style="aspect-ratio: 1 / ' + S.ratio.toFixed(3) + '"></span><span class="bk-thn">' + n + '</span>';
        grid.appendChild(b);
        if (io) io.observe(b); else queueThumb(b);
      }
      grid.addEventListener('click', function (e) {
        var t = e.target.closest('.bk-th');
        if (t) { goto(+t.dataset.n); leavePanelOnPhone(); }
      });
      body.appendChild(grid);
      markThumbs(true);
    }
    function markThumbs(scroll) {
      if (!P.thumbs) return;
      var vis = visible(), first = null;
      P.thumbs.querySelectorAll('.bk-th').forEach(function (b) {
        var n = +b.dataset.n, on = vis.indexOf(n) !== -1;
        b.classList.toggle('is-cur', on);
        b.classList.toggle('is-marked', isMarked(n));
        if (on && !first) first = b;
      });
      if (first && scroll) first.scrollIntoView({ block: 'center' });
    }
    function queueThumb(b) { P.thQ.push(b); pumpThumbs(); }
    function pumpThumbs() {
      if (P.thBusy || !P.thQ.length || !P.thumbs) return;
      var b = P.thQ.shift();
      if (!b.isConnected) { pumpThumbs(); return; }
      P.thBusy = true;
      S.doc.getPage(+b.dataset.n).then(function (page) {
        var v1 = page.getViewport({ scale: 1 }), w = 150 * Math.min(window.devicePixelRatio || 1, 2);
        var vp = page.getViewport({ scale: w / v1.width });
        var c = D.createElement('canvas');
        c.width = Math.floor(vp.width); c.height = Math.floor(vp.height);
        return page.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise.then(function () {
          var slot = b.firstChild;
          if (slot) { slot.appendChild(c); slot.classList.add('is-ready'); }
        });
      }).catch(function () { /* thumbnail stays blank */ }).then(function () { P.thBusy = false; timers.push(setTimeout(pumpThumbs, 10)); });
    }

    function buildToc(body) {
      body.innerHTML = '<div class="bk-empty"><span>Reading the contents</span></div>';
      var load = P.outline ? Promise.resolve(P.outline) : S.doc.getOutline().then(function (o) { P.outline = o || []; return P.outline; }).catch(function () { P.outline = []; return P.outline; });
      load.then(function (items) {
        if (S.panel !== 'toc') return;
        body.innerHTML = '';
        if (!items.length) { body.appendChild(el('div', 'bk-empty', icon('menu_book') + '<span>No contents in this file</span>')); return; }
        body.appendChild(tocList(items, 0));
      });
    }
    function tocList(items, depth) {
      var ul = el('ul', 'bk-toc');
      items.forEach(function (it) {
        var li = el('li'), row = el('div', 'bk-tr'), kids = it.items && it.items.length;
        row.style.paddingLeft = (4 + depth * 14) + 'px';
        var tg = el('button', 'bk-tt' + (kids ? '' : ' is-leaf'), kids ? icon('chevron_right') : '');
        tg.type = 'button'; tg.setAttribute('aria-label', 'Expand');
        var go = el('button', 'bk-tl'); go.type = 'button'; go.textContent = it.title || 'Untitled';
        row.appendChild(tg); row.appendChild(go); li.appendChild(row);
        if (kids) {
          var sub = tocList(it.items, depth + 1); sub.hidden = true; li.appendChild(sub);
          tg.addEventListener('click', function () { sub.hidden = !sub.hidden; tg.classList.toggle('is-open', !sub.hidden); });
        }
        go.addEventListener('click', function () { destPage(it.dest).then(function (n) { if (n) { goto(n); leavePanelOnPhone(); } }); });
        ul.appendChild(li);
      });
      return ul;
    }
    function destPage(dest) {
      if (!dest) return Promise.resolve(0);
      var get = typeof dest === 'string' ? S.doc.getDestination(dest) : Promise.resolve(dest);
      return get.then(function (d) {
        if (!d) return 0;
        var ref = d[0];
        if (typeof ref === 'number') return ref + 1;
        return S.doc.getPageIndex(ref).then(function (i) { return i + 1; });
      }).catch(function () { return 0; });
    }

    function buildSearch(body) {
      var box = el('div', 'bk-sbox', icon('search')), input = el('input', 'bk-sin');
      input.type = 'search'; input.placeholder = 'Search the book'; input.value = S.hlq; input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Search the book');
      box.appendChild(input);
      var stat = el('div', 'bk-sstat'), list = el('div', 'bk-sres');
      body.appendChild(box); body.appendChild(stat); body.appendChild(list);
      P.sInput = input; P.sList = list; P.sStat = stat;
      var t = 0;
      input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { setQuery(input.value); }, 220); });
      input.addEventListener('keydown', function (e) {
        e.stopPropagation();
        if (e.key === 'Escape') { if (input.value) { input.value = ''; setQuery(''); } else { closePanel(); root.focus(); } }
        if (e.key === 'Enter' && P.sResults.length) jumpResult(P.sResults[0]);
      });
      indexAll();
      runSearch();
      timers.push(setTimeout(function () { input.focus(); }, 80));
    }
    function setQuery(v) {
      S.hlq = (v || '').trim();
      runSearch();
      refreshHL();
    }
    function indexAll() {
      if (P.sRunning || P.sIndexed >= S.N) return;
      P.sRunning = true;
      (function next() {
        if (!alive || P.sIndexed >= S.N) { P.sRunning = false; runSearch(); return; }
        var n = ++P.sIndexed;
        textInfo(n).then(function () {
          if (n % 25 === 0 || n === S.N) runSearch();
          if (n % 4 === 0) timers.push(setTimeout(next, 0)); else next();
        });
      })();
    }
    function runSearch() {
      if (!P.sList || S.panel !== 'search') return;
      var q = S.hlq.toLowerCase(), n, jobs = [];
      var done = P.sIndexed >= S.N;
      if (q.length < 2) { P.sResults = []; P.sList.innerHTML = ''; P.sStat.textContent = ''; return; }
      for (n = 1; n <= P.sIndexed; n++) jobs.push(n);
      Promise.all(jobs.map(textInfo)).then(function (infos) {
        if (S.hlq.toLowerCase() !== q || !P.sList) return;
        var res = [];
        infos.forEach(function (info, i) {
          var from = 0, idx, count = 0;
          while ((idx = info.low.indexOf(q, from)) !== -1 && count < 3 && res.length < 400) {
            res.push({ p: jobs[i], idx: idx, str: info.str });
            from = idx + q.length; count++;
          }
        });
        P.sResults = res;
        P.sList.innerHTML = '';
        res.forEach(function (r) {
          var b = el('button', 'bk-sri'); b.type = 'button';
          var chip = el('span', 'bk-chip'); chip.textContent = 'p. ' + r.p;
          var txt = el('span', 'bk-snip');
          var a = Math.max(0, r.idx - 34), z = Math.min(r.str.length, r.idx + q.length + 70);
          txt.appendChild(D.createTextNode((a > 0 ? '\u2026' : '') + r.str.slice(a, r.idx)));
          var mk = el('mark'); mk.textContent = r.str.slice(r.idx, r.idx + q.length); txt.appendChild(mk);
          txt.appendChild(D.createTextNode(r.str.slice(r.idx + q.length, z) + (z < r.str.length ? '\u2026' : '')));
          b.appendChild(chip); b.appendChild(txt);
          b.addEventListener('click', function () { jumpResult(r); });
          P.sList.appendChild(b);
        });
        var pct = Math.round(P.sIndexed / S.N * 100);
        P.sStat.textContent = (res.length ? res.length + (res.length >= 400 ? '+ matches' : (res.length === 1 ? ' match' : ' matches')) : (done ? 'No matches' : 'Searching')) + (done ? '' : ' \u00b7 ' + pct + '%');
      });
    }
    function jumpResult(r) { goto(r.p); leavePanelOnPhone(); }

    function buildMarks(body) {
      var stats = el('div', 'bk-stats'), add = el('button', 'x-btn x-btn-tonal bk-addmark');
      add.type = 'button'; add.setAttribute('data-act', 'mark');
      add.innerHTML = icon('bookmark_add') + '<span>Bookmark this page</span>';
      var list = el('div', 'bk-marks');
      body.appendChild(stats); body.appendChild(add); body.appendChild(list);
      P.mStats = stats; P.mList = list; P.mAdd = add;
      renderMarks();
    }
    function renderMarks() {
      if (!P.mList || S.panel !== 'marks') return;
      var pct = Math.round((store.max || 1) / S.N * 100), mins = Math.floor(store.time / 60);
      var left = Math.max(0, S.N - (store.max || 1));
      P.mStats.innerHTML = '<div class="bk-bar"><i style="width:' + pct + '%"></i></div>' +
        '<div class="bk-srow"><span><b>' + pct + '%</b> read</span><span><b>' + left + '</b> pages left</span><span><b>' + (mins < 1 ? '<1' : mins) + '</b> min</span></div>';
      P.mAdd.lastChild.textContent = visible().some(isMarked) ? 'Remove bookmark here' : 'Bookmark this page';
      P.mList.innerHTML = '';
      if (!store.marks.length) { P.mList.appendChild(el('div', 'bk-empty', icon('bookmarks') + '<span>No bookmarks yet</span>')); return; }
      store.marks.slice().sort(function (a, b) { return a.p - b.p; }).forEach(function (m) {
        var row = el('div', 'bk-mark'), g = el('button', 'bk-chip bk-chip-go'); g.type = 'button'; g.textContent = 'p. ' + m.p;
        g.addEventListener('click', function () { goto(m.p); leavePanelOnPhone(); });
        var inp = el('input', 'bk-note'); inp.type = 'text'; inp.placeholder = 'Add a note'; inp.value = m.note || ''; inp.maxLength = 160;
        inp.setAttribute('aria-label', 'Note for page ' + m.p);
        inp.addEventListener('keydown', function (e) { e.stopPropagation(); });
        inp.addEventListener('input', function () { m.note = inp.value; S.dirty = true; saveSoon(); });
        var del = el('button', 'bk-ib bk-del', icon('delete')); del.type = 'button'; del.setAttribute('aria-label', 'Delete bookmark');
        del.addEventListener('click', function () { store.marks = store.marks.filter(function (x) { return x !== m; }); S.dirty = true; save(); syncUI(); });
        row.appendChild(g); row.appendChild(inp); row.appendChild(del);
        P.mList.appendChild(row);
      });
    }
    function toggleMark() {
      var on = visible().filter(isMarked);
      if (on.length) {
        store.marks = store.marks.filter(function (m) { return on.indexOf(m.p) === -1; });
        toast('Bookmark removed');
      } else {
        store.marks.push({ p: cur(), note: '', at: Date.now() });
        toast('Bookmarked page ' + cur());
      }
      S.dirty = true; save(); syncUI();
    }

    /* settings */
    function buildPop() {
      function seg(k, list) {
        return '<div class="bk-seg" role="radiogroup" data-k="' + k + '">' + list.map(function (o) {
          return '<button type="button" role="radio" data-v="' + o[0] + '" aria-checked="' + (String(prefs[k]) === String(o[0])) + '">' + (o[2] ? icon(o[2]) : '') + '<span>' + o[1] + '</span></button>';
        }).join('') + '</div>';
      }
      function sw(k, text, ic) {
        return '<button type="button" class="bk-sw" role="switch" data-k="' + k + '" aria-checked="' + !!prefs[k] + '">' + icon(ic) + '<span>' + text + '</span><i class="bk-knob"></i></button>';
      }
      pop.innerHTML =
        '<div class="bk-ps"><h4>Page tone</h4>' + seg('tone', [['paper', 'Paper', 'light_mode'], ['sepia', 'Sepia', 'wb_twilight'], ['night', 'Night', 'dark_mode']]) + '</div>' +
        '<div class="bk-ps"><h4>Brightness</h4><input type="range" class="bk-bright" min="60" max="110" value="' + prefs.bright + '" aria-label="Brightness"></div>' +
        '<div class="bk-ps"><h4>Layout</h4>' + seg('layout', [['auto', 'Auto', 'devices'], ['one', 'One page', 'smartphone'], ['two', 'Two pages', 'auto_stories']]) + '</div>' +
        '<div class="bk-ps"><h4>Turn speed</h4>' + seg('speed', [['slow', 'Slow'], ['normal', 'Normal'], ['fast', 'Fast']]) + '</div>' +
        '<div class="bk-ps"><h4>Auto turn every</h4>' + seg('interval', [[5, '5 s'], [8, '8 s'], [15, '15 s'], [30, '30 s']]) + '</div>' +
        '<div class="bk-ps bk-sws">' + sw('curl', 'Page curl', 'swipe') + sw('sound', 'Page sound', 'volume_up') + '</div>' +
        '<button type="button" class="x-btn x-btn-tonal bk-classic" data-classic="1">' + icon('article') + 'Switch to classic reader</button>';
    }
    function togglePop(force) {
      var show = force == null ? pop.hidden : force;
      if (show) { buildPop(); pop.hidden = false; pop.classList.remove('is-in'); void pop.offsetWidth; pop.classList.add('is-in'); }
      else pop.hidden = true;
      settingsBtn.classList.toggle('is-on', show);
    }
    pop.addEventListener('click', function (e) {
      var s = e.target.closest('.bk-seg button'), w = e.target.closest('.bk-sw');
      if (s) {
        var k = s.parentNode.dataset.k, v = s.dataset.v;
        prefs[k] = (k === 'interval') ? +v : v;
        s.parentNode.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-checked', b === s ? 'true' : 'false'); });
        applyPrefs();
        if (k === 'layout') applyLayout();
        if (k === 'interval' && S.auto) startAuto();
      } else if (w) {
        var kk = w.dataset.k;
        prefs[kk] = !prefs[kk];
        w.setAttribute('aria-checked', String(!!prefs[kk]));
        applyPrefs();
        if (kk === 'sound' && prefs.sound) chirp();
      } else if (e.target.closest('[data-classic]')) {
        if (opts.onClassic) opts.onClassic();
      }
    });
    pop.addEventListener('input', function (e) {
      if (e.target.classList.contains('bk-bright')) { prefs.bright = +e.target.value; applyPrefs(); }
    });

    var HELP = [
      ['Turn the page', 'Left Right'], ['Turn by dragging', 'Pull a corner'], ['First or last page', 'Home End'],
      ['Go to page', 'G'], ['Search', 'S'], ['Pages / contents', 'T  C'], ['Bookmark', 'B'],
      ['Zoom', '+  \u2212  0'], ['Auto turn', 'P'], ['Full screen', 'F'], ['Close', 'Esc']
    ];
    function toggleHelp(force) {
      var show = force == null ? help.hidden : force;
      if (show) {
        help.innerHTML = '<div class="bk-hc"><div class="bk-hh"><b>Keyboard</b>' + btn('bk-ib', 'close', 'Close', ' data-act="closehelp"') + '</div>' +
          HELP.map(function (r) { return '<div class="bk-hr"><span>' + r[0] + '</span><kbd>' + r[1] + '</kbd></div>'; }).join('') + '</div>';
        help.hidden = false;
      } else help.hidden = true;
    }

    /* ---------------------------------------------------------------- commands */
    function gotoPrompt() {
      var inp = el('input', 'bk-gin');
      inp.type = 'number'; inp.min = 1; inp.max = S.N; inp.value = cur();
      inp.setAttribute('aria-label', 'Page number');
      pill.hidden = true;
      pill.parentNode.insertBefore(inp, pill);
      inp.focus(); inp.select();
      function end(go) {
        if (!inp.parentNode) return;
        var v = +inp.value;
        inp.remove(); pill.hidden = false;
        if (go && v) goto(v);
        root.focus({ preventScroll: true });
      }
      inp.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter') end(true); if (e.key === 'Escape') end(false); });
      inp.addEventListener('blur', function () { end(false); });
    }
    function act(a) {
      stopAuto();
      switch (a) {
        case 'prev': turn(-1); break;
        case 'next': turn(1); break;
        case 'first': goPos(0); break;
        case 'last': goPos(maxPos()); break;
        case 'goto': gotoPrompt(); break;
        case 'zin': setZoom(S.zoom + 0.25); break;
        case 'zout': setZoom(S.zoom - 0.25); break;
        case 'zreset': setZoom(1); break;
        case 'mark': toggleMark(); break;
        case 'settings': togglePop(); break;
        case 'help': toggleHelp(true); break;
        case 'closehelp': toggleHelp(false); break;
        case 'closepanel': closePanel(); break;
        default: break;
      }
    }
    root.addEventListener('click', function (e) {
      var pb = e.target.closest('[data-panel]');
      if (pb) { openPanel(pb.dataset.panel); return; }
      if (e.target.closest('[data-auto]')) { toggleAuto(); return; }
      var a = e.target.closest('[data-act]');
      if (a) act(a.dataset.act);
      if (!pop.hidden && !e.target.closest('.bk-pop') && !e.target.closest('[data-act="settings"]')) togglePop(false);
      if (e.target === help) toggleHelp(false);
    });
    range.addEventListener('input', function () {
      var v = +range.value, pct = S.N > 1 ? (v - 1) / (S.N - 1) * 100 : 0;
      scrub.style.setProperty('--p', pct.toFixed(2) + '%');
      tip.hidden = false; tip.textContent = v;
      tip.style.left = 'calc(' + pct + '% + ' + (10 - pct * 0.2) + 'px)';
    });
    range.addEventListener('change', function () { tip.hidden = true; stopAuto(); goto(+range.value); root.focus({ preventScroll: true }); });
    range.addEventListener('keydown', function (e) { e.stopPropagation(); });
    range.addEventListener('blur', function () { tip.hidden = true; });

    root.addEventListener('keydown', function (e) {
      if (e.target.matches && e.target.matches('input, textarea')) return;
      if (e.altKey || e.metaKey || e.key === 'Tab' || e.key === 'Shift' || e.key === 'Control') return;
      var k = e.key, handled = true;
      if (e.ctrlKey) {
        if (k === 'f' || k === 'F') { e.preventDefault(); if (S.panel !== 'search') openPanel('search'); else if (P.sInput) P.sInput.focus(); }
        return;
      }
      if (k !== 'p' && k !== 'P') stopAuto();
      if (k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) turn(1);
      else if (k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey)) turn(-1);
      else if (k === 'Home') goPos(0);
      else if (k === 'End') goPos(maxPos());
      else if (k === '+' || k === '=') setZoom(S.zoom + 0.25);
      else if (k === '-' || k === '_') setZoom(S.zoom - 0.25);
      else if (k === '0') setZoom(1);
      else if (k === 'b' || k === 'B') toggleMark();
      else if (k === 's' || k === 'S' || k === '/') openPanel('search');
      else if (k === 't' || k === 'T') openPanel('pages');
      else if (k === 'c' || k === 'C') openPanel('toc');
      else if (k === 'g' || k === 'G') gotoPrompt();
      else if (k === 'p' || k === 'P') toggleAuto();
      else if (k === 'f' || k === 'F') { var fs = D.getElementById('vw-fs'); if (fs) fs.click(); }
      else if (k === '?') toggleHelp();
      else if (k === 'Escape') {
        if (!help.hidden) toggleHelp(false); else if (!pop.hidden) togglePop(false); else if (S.panel) closePanel(); else handled = false;
      } else if (k === 'ArrowDown' || k === 'ArrowUp') { handled = S.zoom === 1; if (handled) turn(k === 'ArrowDown' ? 1 : -1); }
      else handled = false;
      if (handled) e.preventDefault();
    });

    var resizeT = 0, lastDW = 0, lastDH = 0;
    var ro = window.ResizeObserver ? new ResizeObserver(function () {
      if (!S.N || !desk.clientWidth || (desk.clientWidth === lastDW && desk.clientHeight === lastDH)) return;
      lastDW = desk.clientWidth; lastDH = desk.clientHeight;
      clearTimeout(resizeT);
      resizeT = setTimeout(function () { if (alive) applyLayout(); }, 120);
    }) : null;
    if (ro) ro.observe(desk);

    /* ---------------------------------------------------------------- start */
    applyPrefs();
    var ready = openDoc(src).then(function (doc) {
      S.doc = doc; S.N = doc.numPages;
      return doc.getPage(1).then(function (page) {
        var v = page.getViewport({ scale: 1 });
        S.ratio = clamp(v.height / v.width, 0.6, 2.2);
        lastDW = desk.clientWidth; lastDH = desk.clientHeight;
        S.spread = measure().spread;
        var start = opts.page || (store.last > 1 && store.last < S.N ? store.last : 1);
        S.pos = clamp(posOf(start), 0, maxPos());
        applyLayout();
        return Promise.all(visible().map(renderPage)).then(function () {
          loadEl.classList.add('is-done');
          onMoved();
          if (start > 1 && !opts.page) toast('Continued on page ' + start, 'From the start', function () { goPos(0); });
          if (!reduced && book.animate) book.animate([{ opacity: 0, scale: '.94', translate: '0 14px' }, { opacity: 1, scale: '1', translate: '0 0' }], { duration: 650, easing: 'cubic-bezier(.2,1,.3,1)' });
        });
      });
    });

    function destroy() {
      alive = false;
      save();
      stopAuto();
      timers.forEach(function (t) { clearTimeout(t); clearInterval(t); });
      if (ro) ro.disconnect();
      window.removeEventListener('pagehide', onHide);
      cache.forEach(function (e) { if (e.c) e.c.width = 0; });
      cache.clear();
      if (actx) { try { actx.close(); } catch (e) { /* already closed */ } }
      root.remove();
    }
    return { node: root, ready: ready, goto: goto, page: function () { return S.N ? cur() : (opts.page || 1); }, destroy: destroy };
  }

  function openDoc(src) {
    if (window.NebPdf && window.NebPdf.open) return window.NebPdf.open(src);
    return Promise.reject(new Error('pdf engine missing'));
  }

  window.NebBook = { mount: mount };
})();
