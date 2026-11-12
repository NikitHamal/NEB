/* NebBook: the page-turning PDF reader. A PDF becomes a hardcover book on a reading desk: a spine, boards and page stacks that
   grow and shrink as you read, leaves that bend and turn in 3D with a moving sheen and a cast shade (drag a corner, swipe,
   click an edge, keys), a book that tilts toward the pointer, pinch / wheel zoom to 400%, pen and highlighter on the pages,
   read aloud, paper sounds, search with highlights, contents, thumbnails, bookmarks with notes, resume point, paper / sepia /
   night tones and auto-turn.  Pages are drawn by PDF.js (shared through NebPdf.open); a byte budget decides how many canvases
   stay in memory, the turning leaf is one pooled DOM that is repainted, never rebuilt.
   Shared parts (sound, ink, search, panels, scrubber, settings) live in pdf-core.js.

   window.NebBook.mount(src, title, { page, onClassic }) -> { node, ready, goto(n), page(), destroy() }
   ready rejects when the file cannot be drawn so the caller can fall back to the classic reader.
   Everything is flat: no shadows, shading is a neutral overlay that follows the leaf angle. */
(function () {
  'use strict';
  var K = window.NebPdfKit;
  if (!K) return;
  var D = document, el = K.el, icon = K.icon, clamp = K.clamp, btn = K.btn, setLabel = K.setLabel, sfx = K.sfx;
  var reduced = K.reduced;
  var PREFS_KEY = 'neb.book.prefs';
  var DEFAULTS = { tone: 'paper', bright: 100, warm: 0, layout: 'auto', cover: 'subject', speed: 'normal', curl: 'rich', tilt: true, hide: true, interval: 8, rate: 1 };
  var SPEED = { slow: 1250, normal: 820, fast: 520 };
  var STRIPN = { off: 1, soft: 9, rich: 18 };
  var CURL = 34, PEEK = 13, ZMAX = 4;
  var CTXF = (function () { try { return 'filter' in CanvasRenderingContext2D.prototype; } catch (e) { return false; } })();
  var easeInOut = K.ease.inOut, easeOut = K.ease.out;

  function mount(src, title, opts) {
    opts = opts || {};
    var alive = true;
    var prefs = Object.assign({}, DEFAULTS, K.jget(PREFS_KEY) || {});
    if (prefs.curl === true) prefs.curl = 'rich'; else if (prefs.curl === false) prefs.curl = 'off';
    if (!STRIPN[prefs.curl]) prefs.curl = 'rich';
    prefs.sound = sfx.state.on; prefs.vol = Math.round(sfx.state.vol * 100);
    var store = K.store(src), ink = K.ink(src);
    var S = {
      doc: null, N: 0, ratio: 1.414, W: 0, H: 0, spread: true, pos: 0, zoom: 1, F: null, busy: false, queue: [], tok: 0, pending: null,
      hlq: '', drag: null, peek: 0, auto: 0, moved: Date.now(), bare: false, inking: false, reading: false, readPage: 0, overUi: false,
      tx: 0, ty: 0, gx: 0, gy: 0, shift: 0, pts: {}, pinch: null, rend: 0, lastTap: 0, text: null, thumbs: null
    };
    var cache = new Map(), bytes = 0, BUDGET = K.budget(), timers = [], leaf = null, text = null, thumbs = null, panels = null, session = null, scr = null;

    /* ---------------------------------------------------------------- DOM */
    var root = el('div', 'bk');
    root.tabIndex = 0;
    root.setAttribute('role', 'application');
    root.setAttribute('aria-label', (title || 'Book') + ', page turning reader');
    function page() { return '<div class="bk-pg"><div class="nx-hls"></div><canvas class="nx-ink"></canvas></div>'; }
    root.innerHTML =
      '<div class="bk-desk"><div class="bk-zoom"><div class="bk-book">' +
        '<div class="bk-ao"></div><div class="bk-board bk-bl"></div><div class="bk-board bk-br"></div><div class="bk-spine"></div>' +
        '<div class="bk-stack bk-sl"></div><div class="bk-stack bk-sr"></div>' +
        '<div class="bk-cell bk-l is-empty">' + page() + '</div><div class="bk-cell bk-r is-empty">' + page() + '</div>' +
        '<div class="bk-castw"><div class="bk-cast"></div></div>' +
      '</div></div></div>' +
      '<div class="bk-top nx-ui" role="toolbar" aria-label="Reader tools">' +
        '<div class="nx-grp">' + btn('nx-ib', 'grid_view', 'Pages', ' data-panel="pages"') + btn('nx-ib', 'toc', 'Contents', ' data-panel="toc"') +
          btn('nx-ib', 'search', 'Search', ' data-panel="search"') + btn('nx-ib', 'bookmarks', 'Bookmarks', ' data-panel="marks"') + '</div>' +
        '<div class="nx-grp">' + btn('nx-ib', 'bookmark_add', 'Bookmark this page', ' data-act="mark"') + btn('nx-ib', 'draw', 'Annotate', ' data-act="ink"') +
          (K.speech.ok ? btn('nx-ib nx-hide-s', 'record_voice_over', 'Read aloud', ' data-act="read"') : '') +
          btn('nx-ib nx-hide-s', 'volume_up', 'Page sound', ' data-act="sound"') + btn('nx-ib', 'tune', 'Reading settings', ' data-act="settings"') +
          btn('nx-ib nx-hide-s', 'keyboard', 'Keyboard shortcuts', ' data-act="help"') + '</div>' +
      '</div>' +
      '<div class="bk-dock nx-ui">' +
        '<div class="nx-grp">' + btn('nx-ib nx-hide-s', 'first_page', 'First page', ' data-act="first"') + btn('nx-ib', 'chevron_left', 'Previous page', ' data-act="prev"') + '</div>' + K.SCRUB +
        '<button type="button" class="nx-pill" data-act="goto" aria-label="Go to page"><b>1</b><i>/ 1</i></button>' +
        '<div class="nx-grp">' + btn('nx-ib', 'chevron_right', 'Next page', ' data-act="next"') + btn('nx-ib nx-hide-s nx-mirror', 'first_page', 'Last page', ' data-act="last"') + '</div>' +
        '<div class="nx-sep nx-hide-s"></div>' +
        '<div class="nx-grp nx-hide-s">' + btn('nx-ib', 'remove', 'Zoom out', ' data-act="zout"') + '<button type="button" class="nx-zl" data-act="zreset" aria-label="Reset zoom">100%</button>' +
          btn('nx-ib', 'add', 'Zoom in', ' data-act="zin"') + btn('nx-ib', 'play_arrow', 'Turn pages automatically', ' data-auto="1"') + '</div>' +
      '</div>' +
      '<aside class="nx-panel nx-ui bk-panel" hidden aria-label="Book panel"></aside>' +
      '<div class="nx-pop nx-ui" hidden role="dialog" aria-label="Reading settings"></div>' +
      '<div class="nx-help nx-ui" hidden role="dialog" aria-label="Keyboard shortcuts"></div>' +
      '<div class="nx-load"><span class="nx-spin"></span></div>';

    function $(s) { return root.querySelector(s); }
    var desk = $('.bk-desk'), zoomBox = $('.bk-zoom'), book = $('.bk-book');
    var boardL = $('.bk-bl'), boardR = $('.bk-br'), stackL = $('.bk-sl'), stackR = $('.bk-sr'), spine = $('.bk-spine');
    var cells = { l: { el: $('.bk-l'), n: 0 }, r: { el: $('.bk-r'), n: 0 } };
    [cells.l, cells.r].forEach(function (c) { c.ink = c.el.querySelector('.nx-ink'); c.hls = c.el.querySelector('.nx-hls'); });
    var ao = $('.bk-ao'), cast = $('.bk-cast'), panelEl = $('.nx-panel'), pop = $('.nx-pop'), help = $('.nx-help'), loadEl = $('.nx-load');
    var pill = $('.nx-pill'), markBtn = $('[data-act="mark"]'), autoBtn = $('[data-auto]'), zl = $('.nx-zl'), settingsBtn = $('[data-act="settings"]');
    var inkBtn = $('[data-act="ink"]'), readBtn = $('[data-act="read"]'), soundBtn = $('[data-act="sound"]');
    var toast = K.toast(root);
    var inkBar = K.inkBar({
      onTool: function () { },
      onAct: function (a) {
        var n = cur();
        if (a === 'done') toggleInk(false);
        else if (a === 'undo') { if (!(ink.undo(cells.r.n || n) || ink.undo(cells.l.n))) toast('Nothing to undo'); }
        else if (a === 'clear') { var any = ink.clear(cells.l.n) | ink.clear(cells.r.n); if (any) sfx.erase(); }
      }
    });
    root.appendChild(inkBar.el);
    [cells.l, cells.r].forEach(function (c) {
      K.inkBind(c.ink, { n: function () { return c.n; }, ink: ink, tool: inkBar.tool, active: function () { return S.inking && c.n; }, ratio: function () { return S.ratio; } });
    });
    ink.on(function (n) {
      [cells.l, cells.r].forEach(function (c) { if (c.n === n) paintInk(c); });
      if (panels) panels.sync();
    });

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

    /* ---------------------------------------------------------------- rendering: byte-budgeted canvas cache */
    function dims() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var k = Math.min(dpr, 2800 / Math.max(S.W, 1), Math.sqrt(9e6 / Math.max(1, S.W * S.H)));
      return { pw: Math.max(2, Math.round(S.W * k)), ph: Math.max(2, Math.round(S.H * k)) };
    }
    function keyOf(n, d) { return n + '@' + d.pw; }
    function cachedCanvas(n) { var e = cache.get(keyOf(n, dims())); return e && e.c || null; }
    function drop(k, e) { if (e.c) { bytes -= e.pw * e.ph * 4; e.c.width = 0; e.c = null; } cache.delete(k); }
    function trim() {
      var d = dims(), c = cur(), list = [];
      cache.forEach(function (e, k) {
        if (!e.c || e.c.isConnected) return;
        if (e.pw !== d.pw) { drop(k, e); return; }
        list.push({ k: k, e: e, far: Math.abs(e.n - c) });
      });
      if (bytes <= BUDGET) return;
      list.sort(function (a, b) { return b.far - a.far; });
      for (var i = 0; i < list.length && bytes > BUDGET; i++) drop(list[i].k, list[i].e);
    }
    var idleT = 0;
    function idleCleanup() {
      clearTimeout(idleT);
      idleT = setTimeout(function () { if (alive && !S.rend && S.doc) { try { S.doc.cleanup(true); } catch (e) { /* busy */ } } }, 6000);
    }
    function renderPage(n) {
      var d = dims(), key = keyOf(n, d), hit = cache.get(key);
      if (hit) return hit.p;
      var entry = { n: n, pw: d.pw, ph: d.ph, c: null, p: null };
      S.rend++;
      entry.p = S.doc.getPage(n).then(function (pgObj) {
        var v1 = pgObj.getViewport({ scale: 1 });
        var vp = pgObj.getViewport({ scale: Math.min(d.pw / v1.width, d.ph / v1.height) });
        var c = D.createElement('canvas');
        c.width = d.pw; c.height = d.ph;
        var ctx = c.getContext('2d', { alpha: false });
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, d.pw, d.ph);
        return pgObj.render({ canvasContext: ctx, viewport: vp, transform: [1, 0, 0, 1, (d.pw - vp.width) / 2, (d.ph - vp.height) / 2] }).promise.then(function () {
          try { pgObj.cleanup(); } catch (e) { /* released */ }
          if (!alive) { c.width = 0; return c; }
          entry.c = c; bytes += d.pw * d.ph * 4;
          trim();
          return c;
        });
      });
      entry.p.then(function () { S.rend--; idleCleanup(); }, function () { S.rend--; cache.delete(key); });
      cache.set(key, entry);
      return entry.p;
    }

    function paintInk(cell) {
      var cv = cell.ink;
      if (!cell.n) { K.paintInk(cv, []); return; }
      K.paintInk(cv, ink.get(cell.n));
    }
    function fillCell(cell, n) {
      cell.n = n;
      var box = cell.el, pgEl = box.firstChild, old = pgEl.querySelector('canvas:not(.nx-ink)');
      box.classList.toggle('is-empty', !n);
      paintInk(cell);
      if (!n) { if (old) old.remove(); cell.hls.innerHTML = ''; box.classList.remove('is-wait'); return; }
      var c = cachedCanvas(n);
      if (c) { attach(cell, c, n); return; }
      box.classList.add('is-wait');
      var lo = thumbs && thumbs.peek(n);
      if (lo) { lo.className = 'bk-lo'; if (old) old.remove(); pgEl.insertBefore(lo, pgEl.firstChild); }
      renderPage(n).then(function (cv) { if (alive && cell.n === n) attach(cell, cv, n); }, function () { box.classList.remove('is-wait'); });
    }
    function attach(cell, c, n) {
      var pgEl = cell.el.firstChild, old = pgEl.querySelector('canvas:not(.nx-ink)');
      if (old && old !== c) old.remove();
      if (c.parentNode !== pgEl) pgEl.insertBefore(c, pgEl.firstChild);
      cell.el.classList.remove('is-wait');
      drawHL(cell);
    }
    function refreshCells() {
      var p = pagesAt(S.pos);
      fillCell(cells.l, p.l);
      fillCell(cells.r, p.r);
    }

    var preToken = 0;
    function prefetch() {
      var tok = ++preToken, c = cur(), list = [], i;
      var ahead = S.zoom > 1.5 ? 1 : (S.spread ? 6 : 3), back = S.zoom > 1.5 ? 1 : 3;
      for (i = 1; i <= ahead; i++) list.push(c + i);
      for (i = 1; i <= back; i++) list.push(c - i);
      list = list.filter(pg).filter(function (n) { return !cachedCanvas(n); });
      (function next() {
        if (!list.length || tok !== preToken || !alive) return;
        renderPage(list.shift()).then(function () { timers.push(setTimeout(next, 30)); }, next);
      })();
    }

    /* ---------------------------------------------------------------- layout */
    function leftPad() { return panels && panels.current() && root.clientWidth >= 720 ? 344 : 0; }
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
      var m = measure(), pageNo = cur(), changed = m.spread !== S.spread, sized = m.W !== S.W || m.H !== S.H;
      if (S.F) discardFlip();
      if (sized || changed) destroyLeaf();
      S.spread = m.spread; S.W = m.W; S.H = m.H;
      if (changed) S.pos = posOf(pageNo);
      S.pos = clamp(S.pos, 0, maxPos());
      book.style.width = (S.spread ? S.W * 2 : S.W) + 'px';
      book.style.height = S.H + 'px';
      zoomBox.style.paddingLeft = (m.pad + (S.zoom > 1 ? S.W / 2 : 0)) + 'px';
      zoomBox.style.paddingRight = (S.zoom > 1 ? S.W / 2 : 0) + 'px';
      [cells.l, cells.r].forEach(function (c) {
        c.el.style.width = S.W + 'px'; c.el.style.height = S.H + 'px';
        var ik = Math.min(window.devicePixelRatio || 1, 1.5), iw = Math.round(S.W * ik), ih = Math.round(S.H * ik);
        if (c.ink.width !== iw || c.ink.height !== ih) { c.ink.width = iw; c.ink.height = ih; paintInk(c); }
      });
      cells.l.el.style.left = '0px';
      cells.r.el.style.left = (S.spread ? S.W : 0) + 'px';
      cells.l.el.style.display = S.spread ? '' : 'none';
      root.dataset.spread = S.spread ? '1' : '0';
      if (changed || sized) refreshCells();
      visuals(S.pos);
      syncUI();
    }

    /* The whole book follows "tf" (how many leaves are over): stacks, boards, spine, shift and the shade cast on the page below. */
    function applyBook() {
      var t = 'translateX(' + S.shift.toFixed(2) + 'px)';
      if (prefs.tilt && !reduced && S.zoom === 1 && (Math.abs(S.tx) > 0.02 || Math.abs(S.ty) > 0.02)) t += ' perspective(2600px) rotateX(' + S.ty.toFixed(2) + 'deg) rotateY(' + S.tx.toFixed(2) + 'deg)';
      book.style.transform = t;
    }
    function visuals(tf, theta, leafIx) {
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
      spine.style.left = (S.W - 9) + 'px'; spine.style.height = (S.H + 16) + 'px';
      // the contact shade only spans the pages that are showing
      var ax0 = S.spread ? S.W * (1 - bl) : 0, ax1 = bw - (S.spread && S.N % 2 === 0 ? S.W * (1 - br) : 0);
      ao.style.left = (ax0 - 8) + 'px'; ao.style.width = Math.max(0, ax1 - ax0 + 16) + 'px';
      S.shift = shiftAt(tf);
      applyBook();
      if (theta == null) { cast.style.opacity = 0; return; }
      var rad = theta * Math.PI / 180, sp = S.spread ? S.W : 0, reach = S.W * 0.34;
      var tipX = sp + S.W * Math.cos(rad);
      cast.style.width = reach + 'px';
      if (theta < 90) { cast.style.left = tipX + 'px'; cast.dataset.side = 'r'; }
      else { cast.style.left = (tipX - reach) + 'px'; cast.dataset.side = 'l'; }
      cast.style.height = S.H + 'px';
      // A shade only falls on a page that is there: not on the empty side of a closed cover.
      var under = theta < 90 ? !!pg(S.spread ? 2 * leafIx + 3 : leafIx + 2) : (S.spread && leafIx > 0);
      cast.style.opacity = under ? (0.55 * Math.sin(rad)).toFixed(3) : 0;
    }

    /* the book tilts a few degrees toward the pointer: depth without a shadow */
    var tiltRaf = 0;
    function tiltTo(px, py) {
      S.gx = (px - 0.5) * 2 * 3.2; S.gy = -(py - 0.5) * 2 * 2;
      if (!tiltRaf && prefs.tilt && !reduced) tiltRaf = requestAnimationFrame(tiltStep);
    }
    function tiltStep() {
      tiltRaf = 0;
      if (!alive) return;
      S.tx += (S.gx - S.tx) * 0.1; S.ty += (S.gy - S.ty) * 0.1;
      applyBook();
      if (Math.abs(S.gx - S.tx) > 0.02 || Math.abs(S.gy - S.ty) > 0.02) tiltRaf = requestAnimationFrame(tiltStep);
    }

    /* ---------------------------------------------------------------- the turning leaf (pooled, repainted per turn) */
    function toneF() { return K.toneFilter(prefs); }
    function destroyLeaf() {
      if (!leaf) return;
      leaf.holder.remove();
      leaf.strips.forEach(function (s) { s.fc.width = 0; s.bc.width = 0; });
      leaf = null;
    }
    function getLeaf() {
      var n = STRIPN[prefs.curl], key = n + '|' + S.W + '|' + S.H;
      if (leaf && leaf.key === key) return leaf;
      destroyLeaf();
      var lk = Math.min(Math.min(window.devicePixelRatio || 1, 2), 1100 / Math.max(S.W, 1));
      var sw = S.W / n, ov = n > 1 ? 1 : 0;
      var holder = el('div', 'bk-flip');
      holder.style.width = S.W + 'px'; holder.style.height = S.H + 'px'; holder.style.display = 'none';
      var strips = [], parent = holder, i;
      for (i = 0; i < n; i++) {
        var st = el('div', 'bk-s');
        st.style.width = (sw + ov) + 'px'; st.style.height = S.H + 'px';
        if (i > 0) st.style.left = sw + 'px';
        var f = el('div', 'bk-sf'), b = el('div', 'bk-sb'), fc = D.createElement('canvas'), bc = D.createElement('canvas');
        [fc, bc].forEach(function (c) {
          c.width = Math.max(1, Math.ceil((sw + ov) * lk)); c.height = Math.max(1, Math.ceil(S.H * lk));
          c.style.width = (sw + ov) + 'px'; c.style.height = S.H + 'px';
        });
        f.appendChild(fc); b.appendChild(bc);
        var fs = el('i', 'bk-sh'), bs = el('i', 'bk-sh'), fg = el('i', 'bk-gl'), bg = el('i', 'bk-gl');
        f.appendChild(fs); f.appendChild(fg); b.appendChild(bs); b.appendChild(bg);
        if (i === 0) { f.classList.add('is-gut'); b.classList.add('is-gut'); }
        st.appendChild(f); st.appendChild(b);
        parent.appendChild(st);
        strips.push({ st: st, fs: fs, bs: bs, fg: fg, bg: bg, fc: fc, bc: bc, fx: fc.getContext('2d'), bx: bc.getContext('2d') });
        parent = st;
      }
      book.appendChild(holder);
      leaf = { key: key, n: n, sw: sw, ov: ov, holder: holder, strips: strips };
      return leaf;
    }
    function withInk(c, n) {
      if (!n || !ink.has(n)) return { c: c, tmp: false };
      var t = D.createElement('canvas'); t.width = c.width; t.height = c.height;
      var x = t.getContext('2d'); x.drawImage(c, 0, 0);
      K.drawStrokes(x, ink.get(n), t.width, t.height);
      return { c: t, tmp: true };
    }
    function paintLeaf(L, fSrc, bSrc, fn, bn) {
      var fi = withInk(fSrc, fn), bi = bSrc ? withInk(bSrc, bn) : null, flt = toneF();
      L.strips.forEach(function (s, i) {
        var w = L.sw + L.ov, fk = fi.c.width / S.W, ctx = s.fx;
        ctx.clearRect(0, 0, s.fc.width, s.fc.height);
        if (CTXF) ctx.filter = flt;
        ctx.drawImage(fi.c, L.sw * i * fk, 0, w * fk, fi.c.height, 0, 0, s.fc.width, s.fc.height);
        if (CTXF) ctx.filter = 'none';
        ctx = s.bx;
        ctx.clearRect(0, 0, s.bc.width, s.bc.height);
        if (bi) {
          var bk = bi.c.width / S.W;
          if (CTXF) ctx.filter = flt;
          ctx.drawImage(bi.c, (S.W - (i + 1) * L.sw - L.ov) * bk, 0, w * bk, bi.c.height, 0, 0, s.bc.width, s.bc.height);
          if (CTXF) ctx.filter = 'none';
        }
      });
      if (fi.tmp) fi.c.width = 0;
      if (bi && bi.tmp) bi.c.width = 0;
      root.dataset.leaf = CTXF ? 'baked' : 'css';
    }
    function makeFlip(dir, cb) {
      var s = dir > 0 ? S.pos : S.pos - 1, lp = leafPages(s), tok = ++S.tok;
      Promise.all([renderPage(lp.f), lp.b ? renderPage(lp.b) : null]).then(function (cv) {
        if (!alive || tok !== S.tok) return;
        var L = getLeaf();
        paintLeaf(L, cv[0], cv[1], lp.f, lp.b);
        L.holder.style.left = (S.spread ? S.W : 0) + 'px';
        L.holder.style.display = '';
        var F = { s: s, dir: dir, theta: dir > 0 ? 0 : 180, el: L.holder, strips: L.strips, raf: 0, mode: 'drag' };
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
      return (0.38 * Math.pow(Math.sin(r), 1.45)).toFixed(3);
    }
    function gloss(a, front) {
      var r = front ? clamp(a, 0, 180) : clamp(180 - a, 0, 180), d = (r - 42) / 16;
      return (0.24 * Math.exp(-d * d)).toFixed(3);
    }
    function setTheta(F, theta) {
      F.theta = theta;
      var n = F.strips.length, rad = theta * Math.PI / 180;
      var local = n > 1 ? (CURL * Math.sin(rad)) / n : 0;
      for (var i = 0; i < n; i++) {
        var deg = i === 0 ? -theta : local, s = F.strips[i], a = theta - i * local;
        s.st.style.transform = 'rotateY(' + deg.toFixed(3) + 'deg)';
        s.fs.style.opacity = shade(a, true); s.bs.style.opacity = shade(a, false);
        s.fg.style.opacity = gloss(a, true); s.bg.style.opacity = gloss(a, false);
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
    function hideLeaf(F) { F.el.style.display = 'none'; F.el.style.opacity = 1; }
    function discardFlip() {
      var F = S.F;
      S.tok++;
      if (!F) return;
      cancelAnimationFrame(F.raf);
      hideLeaf(F);
      S.F = null;
      refreshCells();
      visuals(S.pos);
    }
    function getFlip(dir, cb) {
      if (S.F && S.F.dir === dir) { cb(S.F); return; }
      if (S.F) discardFlip();
      makeFlip(dir, cb);
    }
    function isCover(F) { return S.spread && ((F.dir > 0 && S.pos === 0) || (F.dir < 0 && S.pos === 1)); }
    function land(F, completed) {
      cancelAnimationFrame(F.raf);
      var cover = completed && isCover(F);
      if (completed) S.pos = clamp(S.pos + F.dir, 0, maxPos());
      S.tok++;
      refreshCells();
      hideLeaf(F);
      S.F = null;
      S.busy = false;
      visuals(S.pos);
      if (completed && !cover) sfx.land(F.dir);
      onMoved();
      if (S.pending != null) { var t = S.pending; S.pending = null; goPos(t); return; }
      if (S.queue.length) runQueue();
    }
    function finish(F, completed, ms, ease) {
      S.busy = true;
      F.mode = 'go';
      var to = completed ? (F.dir > 0 ? 180 : 0) : (F.dir > 0 ? 0 : 180), dur = ms || SPEED[prefs.speed];
      if (completed) { if (isCover(F)) sfx.cover(F.dir > 0); else sfx.turn(SPEED.normal / dur, F.dir); }
      tween(F, to, dur, ease || easeInOut, function () { land(F, completed); });
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
      sfx.bump(dir);
      if (!book.animate || reduced) return;
      book.animate([{ translate: '0 0' }, { translate: (dir > 0 ? '-12px' : '12px') + ' 0' }, { translate: '0 0' }], { duration: 320, easing: 'cubic-bezier(.2,1.2,.3,1)' });
    }
    function jump(t) {
      var d = t - S.pos;
      if (S.F) discardFlip();
      S.queue = [];
      S.pos = clamp(t, 0, maxPos());
      book.style.transition = reduced ? '' : 'transform .5s cubic-bezier(.2,1,.3,1)';
      refreshCells();
      visuals(S.pos);
      sfx.flurry(6, d > 0 ? 1 : -1);
      timers.push(setTimeout(function () { book.style.transition = ''; }, 560));
      if (book.animate && !reduced) book.animate([{ opacity: 0.2, scale: '.97' }, { opacity: 1, scale: '1' }], { duration: 380, easing: 'cubic-bezier(.2,1,.3,1)' });
      onMoved();
    }
    function goPos(t) {
      t = clamp(t, 0, maxPos());
      if (S.busy) { S.pending = t; S.queue = []; return; }
      if (S.F) discardFlip();
      var d = t - S.pos, n = Math.abs(d);
      if (!n) return;
      if (n <= 6 && !reduced) {
        S.queue = [];
        for (var i = 1; i < n; i++) S.queue.push(d > 0 ? 1 : -1);
        turn(d > 0 ? 1 : -1, n > 1);
      } else jump(t);
    }
    function goto(pageNo, quiet) {
      var from = S.N ? cur() : 1, to = clamp(Math.round(pageNo) || 1, 1, S.N);
      goPos(posOf(to));
      if (!quiet && Math.abs(to - from) > 4) toast('Page ' + to, 'Back', function () { goto(from, true); });
    }

    /* ---------------------------------------------------------------- pointer: peek, drag, tap, pinch */
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
      if (!canTurn(dir) || S.busy || S.drag || S.zoom > 1 || S.inking) { S.peek = 0; return; }
      desk.style.cursor = 'pointer';
      getFlip(dir, function (F2) {
        if (S.peek !== dir) { if (F2.mode !== 'go') discardFlip(); return; }
        F2.mode = 'peek';
        tween(F2, dir > 0 ? PEEK : 180 - PEEK, 520, easeOut);
      });
    }
    function ptCount() { return Object.keys(S.pts).length; }
    function pinchDist() { var k = Object.keys(S.pts), a = S.pts[k[0]], b = S.pts[k[1]]; return Math.hypot(a.x - b.x, a.y - b.y) || 1; }
    desk.addEventListener('pointerdown', function (e) {
      if (S.inking) return;
      S.pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      if (ptCount() === 2) {
        S.pinch = { d0: pinchDist(), z0: S.zoom };
        S.drag = null; S.peek = 0;
        if (S.F) discardFlip();
        return;
      }
      if (e.button > 0 || S.busy) return;
      stopAuto();
      root.focus({ preventScroll: true });
      S.drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, x: e.clientX, mode: null, pts: [{ x: e.clientX, t: performance.now() }], sl: desk.scrollLeft, st: desk.scrollTop, touch: e.pointerType !== 'mouse' };
      try { desk.setPointerCapture(e.pointerId); } catch (x) { /* ok */ }
    });
    desk.addEventListener('pointermove', function (e) {
      if (S.pts[e.pointerId]) { S.pts[e.pointerId].x = e.clientX; S.pts[e.pointerId].y = e.clientY; }
      if (S.pinch && ptCount() === 2) { setZoom(S.pinch.z0 * pinchDist() / S.pinch.d0, true); return; }
      var d = S.drag;
      if (!d) {
        if (e.pointerType === 'mouse' && !S.inking) {
          var r = desk.getBoundingClientRect();
          tiltTo((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height);
          if (S.zoom === 1 && !S.busy) peekTo(zoneAt(e));
        }
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
      delete S.pts[e.pointerId];
      if (ptCount() < 2) S.pinch = null;
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
    desk.addEventListener('pointerleave', function (e) {
      if (!S.drag && e.pointerType === 'mouse') { peekTo(0); S.gx = 0; S.gy = 0; if (!tiltRaf && prefs.tilt) tiltRaf = requestAnimationFrame(tiltStep); }
    });
    function tap(e, d) {
      var now = Date.now();
      if (d.touch && e.target.closest && e.target.closest('.bk-cell') && now - S.lastTap < 320) { S.lastTap = 0; setZoom(S.zoom > 1 ? 1 : 2); return; }
      S.lastTap = now;
      var r = bookRect(), x = e.clientX - r.left, bw = r.width, dir = 0;
      if (S.spread) { if (x >= 0 && x <= bw) dir = x < bw / 2 ? -1 : 1; }
      else dir = x < bw * 0.33 ? -1 : (x > bw * 0.67 ? 1 : 0);
      if (dir && S.zoom === 1) {
        if (S.F && S.F.mode === 'peek' && S.F.dir === dir) { S.peek = 0; finish(S.F, true); }
        else { S.peek = 0; if (S.F) discardFlip(); turn(dir); }
        return;
      }
      if (!dir && d.touch) setBare(!S.bare);
    }
    function setBare(v) { S.bare = v; root.classList.toggle('is-bare', v); }
    desk.addEventListener('dblclick', function (e) {
      if (S.inking || !e.target.closest || !e.target.closest('.bk-cell')) return;
      setZoom(S.zoom > 1 ? 1 : 2);
      e.preventDefault();
    });
    var wheelAcc = 0, wheelT = 0;
    desk.addEventListener('wheel', function (e) {
      if (e.ctrlKey) { e.preventDefault(); setZoom(S.zoom * (e.deltaY < 0 ? 1.12 : 0.89), true); return; }
      if (S.zoom > 1 || Math.abs(e.deltaX) < Math.abs(e.deltaY) * 1.2) return;
      e.preventDefault();
      wheelAcc += e.deltaX;
      clearTimeout(wheelT);
      wheelT = setTimeout(function () { wheelAcc = 0; }, 160);
      if (Math.abs(wheelAcc) > 70 && !S.busy) { var dir = wheelAcc > 0 ? 1 : -1; wheelAcc = 0; turn(dir); }
    }, { passive: false });
    root.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    root.addEventListener('pointermove', function (e) {
      S.moved = Date.now();
      S.overUi = !!(e.target.closest && e.target.closest('.nx-ui'));
      if (S.bare && e.pointerType === 'mouse') setBare(false);
      if (session) session.touch();
    });

    /* ---------------------------------------------------------------- zoom, tones, preferences */
    var zoomT = 0;
    function setZoom(z, quiet) {
      z = clamp(Math.round(z * 20) / 20, 1, ZMAX);
      if (z === S.zoom) return;
      var up = z > S.zoom, fx = (desk.scrollLeft + desk.clientWidth / 2) / Math.max(1, desk.scrollWidth), fy = (desk.scrollTop + desk.clientHeight / 2) / Math.max(1, desk.scrollHeight);
      S.zoom = z;
      root.classList.toggle('is-zoomed', z > 1);
      if (z > 1) { S.tx = 0; S.ty = 0; }
      applyLayout();
      zl.textContent = Math.round(z * 100) + '%';
      desk.scrollLeft = fx * desk.scrollWidth - desk.clientWidth / 2;
      desk.scrollTop = fy * desk.scrollHeight - desk.clientHeight / 2;
      if (!quiet) sfx.zoom(up);
      clearTimeout(zoomT);
      zoomT = setTimeout(function () { if (alive) { prefetch(); refreshCells(); } }, 160);
    }
    function applyPrefs() {
      root.dataset.tone = prefs.tone;
      root.dataset.cover = prefs.cover;
      root.style.setProperty('--nx-filter', K.toneFilter(prefs));
      var save = Object.assign({}, prefs); delete save.sound; delete save.vol;
      K.jset(PREFS_KEY, save);
    }

    /* ---------------------------------------------------------------- reading state and chrome */
    function label() {
      var p = pagesAt(S.pos);
      if (p.l && p.r) return p.l + '\u2013' + p.r;
      return String(p.l || p.r || 1);
    }
    function syncUI() {
      if (!S.N) return;
      var c = cur(), marked = visible().some(store.isMarked);
      pill.firstChild.textContent = label();
      pill.lastChild.textContent = '/ ' + S.N;
      if (scr) scr.set(c);
      markBtn.classList.toggle('is-on', marked);
      markBtn.firstChild.textContent = marked ? 'bookmark_check' : 'bookmark_add';
      setLabel(markBtn, marked ? 'Remove bookmark' : 'Bookmark this page');
      $('[data-act="prev"]').disabled = S.pos <= 0;
      $('[data-act="first"]').disabled = S.pos <= 0;
      $('[data-act="next"]').disabled = S.pos >= maxPos();
      $('[data-act="last"]').disabled = S.pos >= maxPos();
      zl.textContent = Math.round(S.zoom * 100) + '%';
      soundBtn.classList.toggle('is-on', sfx.state.on);
      inkBtn.classList.toggle('is-on', S.inking);
      if (panels) panels.sync();
    }
    function onMoved() {
      S.moved = Date.now();
      var c = cur(), hi = Math.max.apply(null, visible());
      store.d.last = c; store.d.max = Math.max(store.d.max || 1, hi); store.soon();
      if (session) session.touch();
      syncUI();
      refreshHL();
      prefetch();
      if (S.reading && S.readPage !== c) readStep();
    }

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
    function toggleAuto() { if (S.auto) stopAuto(); else { stopRead(); startAuto(); turn(1); } }

    /* ---------------------------------------------------------------- read aloud */
    function setReadUI(on) {
      if (!readBtn) return;
      readBtn.classList.toggle('is-on', on);
      readBtn.firstChild.textContent = on ? 'stop' : 'record_voice_over';
      setLabel(readBtn, on ? 'Stop reading aloud' : 'Read aloud');
    }
    function stopRead() {
      if (!S.reading) return;
      S.reading = false;
      K.speech.stop();
      setReadUI(false);
    }
    function readStep() {
      if (!S.reading || !alive) return;
      var pages = visible(), c = cur();
      S.readPage = c;
      Promise.all(pages.map(function (n) { return text.plain(n); })).then(function (parts) {
        if (!S.reading || S.readPage !== c) return;
        var t = parts.join(' ').trim();
        if (t.length < 3) {
          if (canTurn(1)) { turn(1); return; }
          stopRead(); toast('No text to read here'); return;
        }
        K.speech.speak(t, prefs.rate, function () {
          if (!S.reading || S.readPage !== c) return;
          if (!canTurn(1)) { stopRead(); toast('End of the book'); return; }
          turn(1);
        });
      });
    }
    function toggleRead() {
      if (S.reading) { stopRead(); return; }
      if (!K.speech.ok) { toast('This browser cannot read aloud'); return; }
      stopAuto();
      S.reading = true; setReadUI(true);
      readStep();
    }

    /* ---------------------------------------------------------------- annotate */
    function toggleInk(on) {
      S.inking = on == null ? !S.inking : on;
      root.classList.toggle('is-inking', S.inking);
      inkBar.show(S.inking);
      if (S.inking) { stopAuto(); peekTo(0); if (S.F) discardFlip(); }
      sfx.pop(S.inking);
      syncUI();
    }

    /* ---------------------------------------------------------------- search highlights on the page */
    function drawHL(cell) {
      var n = cell.n, q = S.hlq;
      if (!n || !text) return;
      text.paintHits(cell.hls, n, q, function () { return cell.n === n && S.hlq === q; });
    }
    function refreshHL() { drawHL(cells.l); drawHL(cells.r); }

    /* ---------------------------------------------------------------- bookmarks */
    function toggleMark() {
      var r = store.toggle(visible(), cur());
      toast(r === 'added' ? 'Bookmarked page ' + cur() : 'Bookmark removed');
      sfx.chime(r === 'added');
      syncUI();
    }

    /* ---------------------------------------------------------------- settings and help */
    function schema() {
      return [
        { t: 'seg', k: 'tone', h: 'Page tone', o: [['paper', 'Paper', 'light_mode'], ['sepia', 'Sepia', 'wb_twilight'], ['night', 'Night', 'dark_mode']] },
        { t: 'range', k: 'bright', h: 'Brightness', min: 60, max: 110 },
        { t: 'range', k: 'warm', h: 'Warmth', min: 0, max: 60 },
        { t: 'seg', k: 'layout', h: 'Layout', o: [['auto', 'Auto', 'devices'], ['one', 'One page', 'smartphone'], ['two', 'Two pages', 'auto_stories']] },
        { t: 'seg', k: 'cover', h: 'Cover', o: [['subject', 'Subject'], ['navy', 'Navy'], ['forest', 'Forest'], ['crimson', 'Crimson'], ['charcoal', 'Ink']] },
        { t: 'seg', k: 'speed', h: 'Turn speed', o: [['slow', 'Slow'], ['normal', 'Normal'], ['fast', 'Fast']] },
        { t: 'seg', k: 'curl', h: 'Page bend', o: [['off', 'Flat'], ['soft', 'Soft'], ['rich', 'Rich']] },
        { t: 'seg', k: 'interval', h: 'Auto turn every', o: [[5, '5 s'], [8, '8 s'], [15, '15 s'], [30, '30 s']] },
        { t: 'seg', k: 'rate', h: 'Reading voice speed', o: [[0.8, '0.8x'], [1, '1x'], [1.25, '1.25x'], [1.5, '1.5x']] },
        { t: 'range', k: 'vol', h: 'Volume', min: 0, max: 100 },
        { t: 'sw', k: 'sound', label: 'Page sound', icon: 'volume_up' },
        { t: 'sw', k: 'tilt', label: 'Book tilt', icon: 'flip' },
        { t: 'sw', k: 'hide', label: 'Hide controls while reading', icon: 'visibility_off' },
        { t: 'btn', act: 'classic', label: 'Switch to classic reader', icon: 'article' }
      ];
    }
    function togglePop(force) {
      var show = force == null ? pop.hidden : force;
      if (show) { pop.innerHTML = K.settingsHTML(schema(), prefs); pop.hidden = false; K.restart(pop, 'is-in'); }
      else pop.hidden = true;
      settingsBtn.classList.toggle('is-on', show);
    }
    K.bindSettings(pop, prefs, function (k, v) {
      if (k === '@classic') { if (opts.onClassic) opts.onClassic(); return; }
      if (k === 'sound') { sfx.set('on', v); prefs.sound = v; syncUI(); return; }
      if (k === 'vol') { sfx.set('vol', v / 100); prefs.vol = v; clearTimeout(onPrefVol.t); onPrefVol.t = setTimeout(function () { sfx.turn(1.4, 1); }, 200); return; }
      prefs[k] = v;
      applyPrefs();
      if (k === 'layout') applyLayout();
      if (k === 'interval' && S.auto) startAuto();
      if (k === 'curl' || k === 'tone' || k === 'bright' || k === 'warm') destroyLeaf();
      if (k === 'tilt') { S.gx = 0; S.gy = 0; S.tx = 0; S.ty = 0; applyBook(); }
      if (k === 'hide' && !v) setBare(false);
    });
    function onPrefVol() { }

    var HELP = [
      ['Turn the page', 'Left Right'], ['Jump ten pages', 'Shift + Left Right'], ['Turn by dragging', 'Pull a corner'], ['First or last page', 'Home End'],
      ['Go to page', 'G'], ['Search', 'S'], ['Pages / contents', 'T  C'], ['Bookmark', 'B'], ['Annotate', 'A'], ['Read aloud', 'R'],
      ['Zoom', '+  \u2212  0'], ['Auto turn', 'P'], ['Sound', 'M'], ['Hide controls', 'H'], ['Full screen', 'F'], ['Close', 'Esc']
    ];
    function toggleHelp(force) {
      var show = force == null ? help.hidden : force;
      if (show) { help.innerHTML = K.helpHTML(HELP); help.hidden = false; } else help.hidden = true;
    }

    /* ---------------------------------------------------------------- commands */
    function gotoPrompt() {
      var finished = false, inp = el('input', 'bk-gin nx-pill');
      inp.type = 'number'; inp.min = 1; inp.max = S.N; inp.value = cur();
      inp.setAttribute('aria-label', 'Page number');
      pill.hidden = true;
      pill.parentNode.insertBefore(inp, pill);
      inp.focus(); inp.select();
      function end(go) {
        if (finished) return;
        finished = true;
        var v = +inp.value;
        pill.hidden = false;
        if (inp.parentNode) inp.parentNode.removeChild(inp);
        if (go && v) goto(v);
        root.focus({ preventScroll: true });
      }
      inp.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter') end(true); if (e.key === 'Escape') end(false); });
      inp.addEventListener('blur', function () { end(false); });
    }
    function act(a) {
      if (a !== 'ink' && a !== 'sound') stopAuto();
      switch (a) {
        case 'prev': turn(-1); break;
        case 'next': turn(1); break;
        case 'first': goPos(0); break;
        case 'last': goPos(maxPos()); break;
        case 'goto': gotoPrompt(); break;
        case 'zin': setZoom(Math.round((S.zoom + 0.25) * 4) / 4); break;
        case 'zout': setZoom(Math.round((S.zoom - 0.25) * 4) / 4); break;
        case 'zreset': setZoom(1); break;
        case 'mark': toggleMark(); break;
        case 'ink': toggleInk(); break;
        case 'read': toggleRead(); break;
        case 'sound': sfx.set('on', !sfx.state.on); prefs.sound = sfx.state.on; if (sfx.state.on) sfx.pop(true); toast(sfx.state.on ? 'Page sound on' : 'Page sound off'); syncUI(); break;
        case 'settings': togglePop(); break;
        case 'help': toggleHelp(true); break;
        case 'closehelp': toggleHelp(false); break;
        case 'closepanel': panels.close(); break;
        default: break;
      }
    }
    root.addEventListener('click', function (e) {
      var pb = e.target.closest('[data-panel]');
      if (pb) { togglePop(false); panels.open(pb.dataset.panel); sfx.tick(); return; }
      if (e.target.closest('[data-auto]')) { toggleAuto(); return; }
      var a = e.target.closest('[data-act]');
      if (a && !a.closest('.nx-pop')) act(a.dataset.act);
      if (!pop.hidden && !e.target.closest('.nx-pop') && !e.target.closest('[data-act="settings"]')) togglePop(false);
      if (e.target === help) toggleHelp(false);
    });

    root.addEventListener('keydown', function (e) {
      if (e.target.matches && e.target.matches('input, textarea')) return;
      if (e.altKey || e.metaKey || e.key === 'Tab' || e.key === 'Shift' || e.key === 'Control') return;
      var k = e.key, handled = true;
      S.moved = Date.now();
      if (S.bare) setBare(false);
      if (e.ctrlKey) {
        if (k === 'f' || k === 'F') { e.preventDefault(); panels.focusSearch(); }
        else if (k === 'z' || k === 'Z') { if (S.inking) { e.preventDefault(); ink.undo(cells.r.n || cells.l.n); } }
        return;
      }
      if (k !== 'p' && k !== 'P') stopAuto();
      if (e.shiftKey && (k === 'ArrowRight' || k === 'ArrowLeft')) goto(cur() + (k === 'ArrowRight' ? 10 : -10));
      else if (k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) turn(1);
      else if (k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey)) turn(-1);
      else if (k === 'Home') goPos(0);
      else if (k === 'End') goPos(maxPos());
      else if (k === '+' || k === '=') setZoom(Math.round((S.zoom + 0.25) * 4) / 4);
      else if (k === '-' || k === '_') setZoom(Math.round((S.zoom - 0.25) * 4) / 4);
      else if (k === '0') setZoom(1);
      else if (k === 'b' || k === 'B') toggleMark();
      else if (k === 'a' || k === 'A') toggleInk();
      else if (k === 'r' || k === 'R') toggleRead();
      else if (k === 'm' || k === 'M') act('sound');
      else if (k === 'h' || k === 'H') setBare(!S.bare);
      else if (k === 's' || k === 'S' || k === '/') panels.open('search');
      else if (k === 't' || k === 'T') panels.open('pages');
      else if (k === 'c' || k === 'C') panels.open('toc');
      else if (k === 'g' || k === 'G') gotoPrompt();
      else if (k === 'p' || k === 'P') toggleAuto();
      else if (k === 'f' || k === 'F') { var fs = D.getElementById('vw-fs'); if (fs) fs.click(); }
      else if (k === '?') toggleHelp();
      else if (k === 'Escape') {
        if (!help.hidden) toggleHelp(false); else if (!pop.hidden) togglePop(false); else if (S.inking) toggleInk(false); else if (S.reading) stopRead(); else if (panels.current()) panels.close(); else handled = false;
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

    /* controls fade away while reading, and come back on any movement */
    timers.push(setInterval(function () {
      if (!alive || !prefs.hide || S.bare || S.panelBusy) return;
      var open = panels && panels.current(), idle = Date.now() - S.moved;
      if (idle > 4500 && !open && pop.hidden && help.hidden && !S.inking && !S.overUi && D.activeElement !== root.querySelector('input')) setBare(true);
    }, 800));

    /* ---------------------------------------------------------------- start */
    applyPrefs();
    var ready = openDoc(src).then(function (doc) {
      S.doc = doc; S.N = doc.numPages;
      text = K.text(doc);
      thumbs = K.thumbs(doc, 140);
      var hthumbs = K.thumbs(doc, 96);
      panels = K.panels({
        host: panelEl, root: root, doc: doc, N: function () { return S.N; }, ratio: function () { return S.ratio; }, text: text, thumbs: thumbs, store: store, ink: ink,
        visible: visible, cur: cur, go: function (n) { goto(n); }, query: { get: function () { return S.hlq; }, set: function (q) { S.hlq = q; refreshHL(); } },
        relayout: function () { clearTimeout(relT); relT = setTimeout(function () { if (alive) applyLayout(); }, 40); }, phone: function () { return root.clientWidth < 720; },
        mark: toggleMark, toast: toast, changed: syncUI
      });
      scr = K.scrubber($('.nx-scrub'), { N: function () { return S.N; }, go: function (n) { stopAuto(); goto(n, true); }, thumbs: hthumbs, marks: function () { return store.d.marks.map(function (m) { return m.p; }); }, ratio: function () { return S.ratio; }, focus: function () { root.focus({ preventScroll: true }); } });
      S.hthumbs = hthumbs;
      session = K.session(store, root, function (t) { if (panels.current() === 'marks' && t % 30 === 0) panels.renderMarks(); });
      return doc.getPage(1).then(function (p1) {
        var v = p1.getViewport({ scale: 1 });
        S.ratio = clamp(v.height / v.width, 0.6, 2.2);
        lastDW = desk.clientWidth; lastDH = desk.clientHeight;
        S.spread = measure().spread;
        var start = opts.page || (store.d.last > 1 && store.d.last < S.N ? store.d.last : 1);
        S.pos = clamp(posOf(start), 0, maxPos());
        applyLayout();
        return Promise.all(visible().map(renderPage)).then(function () {
          loadEl.classList.add('is-done');
          onMoved();
          if (start > 1 && !opts.page) toast('Continued on page ' + start, 'From the start', function () { goPos(0); });
          if (!reduced && book.animate) book.animate([{ opacity: 0, scale: '.92', translate: '0 22px' }, { opacity: 1, scale: '1', translate: '0 0' }], { duration: 760, easing: 'cubic-bezier(.2,1,.3,1)' });
          if (start === 1) sfx.cover(true);
          root.focus({ preventScroll: true });
        });
      });
    });
    var relT = 0;

    function destroy() {
      alive = false;
      stopAuto(); stopRead();
      if (session) session.stop(); else store.save();
      ink.flush();
      timers.forEach(function (t) { clearTimeout(t); clearInterval(t); });
      clearTimeout(idleT); clearTimeout(relT); clearTimeout(zoomT); clearTimeout(resizeT);
      cancelAnimationFrame(tiltRaf);
      if (ro) ro.disconnect();
      if (text) text.stop();
      if (thumbs) thumbs.destroy();
      if (S.hthumbs) S.hthumbs.destroy();
      if (panels) panels.destroy();
      destroyLeaf();
      cache.forEach(function (e) { if (e.c) e.c.width = 0; });
      cache.clear(); bytes = 0;
      sfx.close();
      root.remove();
    }
    return { node: root, ready: ready, goto: function (n) { goto(n, true); }, page: function () { return S.N ? cur() : (opts.page || 1); }, destroy: destroy };
  }

  function openDoc(src) {
    if (window.NebPdf && window.NebPdf.open) return window.NebPdf.open(src);
    return Promise.reject(new Error('pdf engine missing'));
  }

  window.NebBook = { mount: mount };
})();
