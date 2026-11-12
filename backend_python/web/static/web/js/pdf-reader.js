/* NebPdf: PDF.js loader shared by both readers, and the classic reader: a continuous, scrolling, view-only PDF drawn with PDF.js so a
   PDF reads the same on Android Chrome, iOS and desktop.  The classic reader is a full reading desk too: zoom presets, fit width / fit
   page, pinch and Ctrl+wheel zoom, rotate, continuous / two-up / one-page views, drag to pan, auto-scroll, paper / sepia / night tones,
   thumbnails, contents, search with highlights, bookmarks, pen and highlighter, page sounds, resume.  Pages are placeholders until
   they scroll near the viewport and are released when they leave it (a 400 page book costs about as much as ten); a zoom re-renders
   in place, so pages never flash blank.  Shared parts live in pdf-core.js.
   window.NebPdf.mount(src, title, { page, onBook }) -> { node, ready, goto(n), page(), destroy() } ; ready rejects when the file
   cannot be drawn and the caller falls back to the browser's own viewer. */
(function () {
  'use strict';
  var base = (document.currentScript && document.currentScript.src || '').replace(/pdf-reader\.js.*$/, 'vendor/pdfjs/');
  var lib = null;

  function load() {
    if (!lib) {
      lib = import(base + 'pdf.min.mjs').then(function (m) {
        m.GlobalWorkerOptions.workerSrc = base + 'pdf.worker.min.mjs';
        return m;
      });
    }
    return lib;
  }

  /* One document per file, shared by the classic reader and the book reader, so switching modes never downloads twice. */
  var docs = {};
  function open(src) {
    if (!docs[src]) {
      docs[src] = load().then(function (m) { return m.getDocument({ url: src, withCredentials: false }).promise; });
      docs[src].catch(function () { delete docs[src]; });
    }
    return docs[src];
  }

  var K = window.NebPdfKit;
  var PREFS_KEY = 'neb.classic.prefs';
  var DEFAULTS = { tone: 'paper', bright: 100, warm: 0, view: 'scroll', scroll: 2 };
  var ZOOMS = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 3, 4];
  var GAP = 12, SCROLL_PX = { 1: 34, 2: 70, 3: 130 };

  function mount(src, title, opts) {
    opts = opts || {};
    if (!K) return plain(src, title);
    var D = document, el = K.el, clamp = K.clamp, btn = K.btn, setLabel = K.setLabel, sfx = K.sfx;
    var alive = true, timers = [];
    var prefs = Object.assign({}, DEFAULTS, K.jget(PREFS_KEY) || {});
    prefs.sound = sfx.state.on; prefs.vol = Math.round(sfx.state.vol * 100);
    var store = K.store(src), ink = K.ink(src);
    var st = { doc: null, N: 0, pages: [], mode: prefs.view === 'single' ? 'fitp' : 'fitw', pct: 1, rot: 0, cur: 1, nw: 595, nh: 842, hlq: '', inking: false, io: null, auto: 0, pts: {}, pinch: null, pan: null, bare: false };
    var panels = null, text = null, thumbs = null, session = null, scr = null;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);

    /* ---------------------------------------------------------------- DOM */
    var root = el('div', 'vw-pdf cl');
    root.tabIndex = -1;
    root.setAttribute('role', 'application');
    root.setAttribute('aria-label', (title || 'Document') + ', reader');
    root.innerHTML =
      '<div class="cl-prog"><i></i></div>' +
      '<div class="vw-pdf-scroll cl-scroll" tabindex="0"></div>' +
      '<div class="cl-top nx-ui" role="toolbar" aria-label="Reader tools">' +
        '<div class="nx-grp">' + btn('nx-ib', 'grid_view', 'Pages', ' data-panel="pages"') + btn('nx-ib', 'toc', 'Contents', ' data-panel="toc"') +
          btn('nx-ib', 'search', 'Search', ' data-panel="search"') + btn('nx-ib', 'bookmarks', 'Bookmarks', ' data-panel="marks"') + '</div>' +
        '<div class="nx-grp">' + btn('nx-ib', 'bookmark_add', 'Bookmark this page', ' data-act="mark"') + btn('nx-ib', 'draw', 'Annotate', ' data-act="ink"') +
          btn('nx-ib', 'rotate_right', 'Rotate pages', ' data-act="rotate"') + btn('nx-ib nx-hide-s', 'volume_up', 'Page sound', ' data-act="sound"') +
          btn('nx-ib', 'tune', 'Reading settings', ' data-act="settings"') + btn('nx-ib nx-hide-s', 'keyboard', 'Keyboard shortcuts', ' data-act="help"') + '</div>' +
      '</div>' +
      '<div class="cl-dock nx-ui">' +
        '<div class="nx-grp">' + btn('nx-ib', 'chevron_left', 'Previous page', ' data-act="prev"') + '</div>' + K.SCRUB +
        '<button type="button" class="nx-pill" data-act="goto" aria-label="Go to page"><b>1</b><i>/ 1</i></button>' +
        '<div class="nx-grp">' + btn('nx-ib', 'chevron_right', 'Next page', ' data-act="next"') + '</div>' +
        '<div class="nx-sep nx-hide-s"></div>' +
        '<div class="nx-grp nx-hide-s">' + btn('nx-ib', 'remove', 'Zoom out', ' data-act="zout"') +
          '<button type="button" class="nx-zl" data-act="zmenu" aria-haspopup="true" aria-label="Zoom options"><span>100%</span>' + K.icon('expand_more') + '</button>' +
          btn('nx-ib', 'add', 'Zoom in', ' data-act="zin"') + btn('nx-ib', 'fit_screen', 'Fit page', ' data-act="fitp"') + btn('nx-ib', 'play_arrow', 'Scroll automatically', ' data-act="auto"') + '</div>' +
      '</div>' +
      '<div class="nx-menu nx-ui" hidden role="menu" aria-label="Zoom"></div>' +
      '<aside class="nx-panel nx-ui cl-panel" hidden aria-label="Document panel"></aside>' +
      '<div class="nx-pop nx-ui" hidden role="dialog" aria-label="Reading settings"></div>' +
      '<div class="nx-help nx-ui" hidden role="dialog" aria-label="Keyboard shortcuts"></div>';

    function $(s) { return root.querySelector(s); }
    var scroll = $('.cl-scroll'), prog = $('.cl-prog i'), panelEl = $('.nx-panel'), pop = $('.nx-pop'), help = $('.nx-help'), menu = $('.nx-menu');
    var pill = $('.nx-pill'), markBtn = $('[data-act="mark"]'), zl = $('.nx-zl span'), soundBtn = $('[data-act="sound"]'), inkBtn = $('[data-act="ink"]');
    var autoBtn = $('[data-act="auto"]'), settingsBtn = $('[data-act="settings"]');
    scroll.setAttribute('aria-label', title || 'Document');
    var toast = K.toast(root);
    var inkBar = K.inkBar({
      onTool: function () { },
      onAct: function (a) {
        var p = st.pages[st.cur - 1];
        if (a === 'done') toggleInk(false);
        else if (a === 'undo') { if (!ink.undo(st.cur)) toast('Nothing to undo'); }
        else if (a === 'clear' && p) { if (ink.clear(st.cur)) sfx.erase(); }
      }
    });
    root.appendChild(inkBar.el);
    ink.on(function (n) { var p = st.pages[n - 1]; if (p) paintInk(p); if (panels) panels.sync(); });

    /* ---------------------------------------------------------------- geometry */
    function effSwap() { return st.rot % 180 !== 0; }
    function natural(p) { var w = p.nw || st.nw, h = p.nh || st.nh; return effSwap() ? { w: h, h: w } : { w: w, h: h }; }
    function ratioOf(p) { var n = natural(p); return n.h / n.w; }
    function geometry() {
      var cw = scroll.clientWidth, ch = scroll.clientHeight, padX = cw < 600 ? 10 : 24, cols = prefs.view === 'two' && cw >= 560 ? 2 : 1;
      return { cw: cw, ch: ch, cols: cols, avail: Math.max(120, (cw - padX * 2 - GAP * (cols - 1)) / cols) };
    }
    function widthFor(p, g) {
      var n = natural(p);
      if (st.mode === 'pct') return Math.max(80, Math.floor(n.w * 4 / 3 * st.pct));
      if (st.mode === 'fitp') return Math.max(120, Math.floor(Math.min(g.avail, (g.ch - 132) / (n.h / n.w))));
      return Math.floor(g.avail);
    }
    function pctOf(p) { var n = natural(p); return p.w / (n.w * 4 / 3); }
    function anchor() {
      var mid = scroll.scrollTop + scroll.clientHeight / 2, best = null;
      for (var i = 0; i < st.pages.length; i++) {
        var b = st.pages[i].box;
        if (b.offsetTop <= mid) best = i; else break;
      }
      if (best == null) return null;
      var bx = st.pages[best].box;
      return { i: best, fy: clamp((mid - bx.offsetTop) / Math.max(1, bx.offsetHeight), 0, 1), fx: (scroll.scrollLeft + scroll.clientWidth / 2) / Math.max(1, scroll.scrollWidth) };
    }
    function restore(a) {
      if (!a) return;
      var bx = st.pages[a.i].box;
      scroll.scrollTop = bx.offsetTop + a.fy * bx.offsetHeight - scroll.clientHeight / 2;
      scroll.scrollLeft = a.fx * scroll.scrollWidth - scroll.clientWidth / 2;
    }
    var redrawT = 0;
    function layout(keep) {
      if (!st.pages.length) return;
      var a = keep === false ? null : anchor(), g = geometry();
      root.dataset.view = prefs.view;
      st.pages.forEach(function (p) {
        p.w = widthFor(p, g);
        p.box.style.width = p.w + 'px';
        p.box.style.height = Math.round(p.w * ratioOf(p)) + 'px';
        p.box.style.minHeight = prefs.view === 'single' ? '' : '';
        if (p.canvas && (p.rw !== p.w || p.rrot !== st.rot)) p.box.classList.add('is-stale');
      });
      st.br.hidden = !(prefs.view === 'two' && g.cols === 2);
      restore(a);
      clearTimeout(redrawT);
      redrawT = setTimeout(function () { st.pages.forEach(function (p) { if (p.vis) draw(p); }); }, 140);
      syncUI();
    }

    /* ---------------------------------------------------------------- rendering (in place, released off screen) */
    function sizeInk(p) {
      var ik = Math.min(dpr, 1.5), w = Math.round(p.w * ik), h = Math.round(p.w * ratioOf(p) * ik);
      if (p.inkc.width !== w || p.inkc.height !== h) { p.inkc.width = w; p.inkc.height = h; }
    }
    function paintInk(p) { if (p.inkc.width > 0 && p.canvas) K.paintInk(p.inkc, ink.get(p.n)); }
    function paintHits(p) { if (text) text.paintHits(p.hls, p.n, st.hlq, function () { return p.canvas && st.hlq; }); }
    function release(p) {
      p.token++;
      if (p.canvas) { p.canvas.width = 0; p.canvas.height = 0; p.canvas.remove(); p.canvas = null; }
      p.inkc.width = 0; p.hls.innerHTML = '';
      p.box.classList.remove('is-ready', 'is-stale');
    }
    function draw(p) {
      if (p.busy || !st.doc) return;
      if (p.canvas && p.rw === p.w && p.rrot === st.rot) { p.box.classList.remove('is-stale'); return; }
      p.busy = true;
      var token = ++p.token, w = p.w, rot = st.rot;
      st.doc.getPage(p.n).then(function (page) {
        if (token !== p.token) { p.busy = false; return; }
        var r0 = page.getViewport({ scale: 1, rotation: page.rotate });
        p.nw = r0.width; p.nh = r0.height;
        var rotation = (page.rotate + rot) % 360, b = page.getViewport({ scale: 1, rotation: rotation }), ratio = b.height / b.width;
        p.box.style.height = Math.round(w * ratio) + 'px';
        var k = Math.min(dpr, Math.sqrt(12e6 / Math.max(1, w * w * ratio)));
        var vp = page.getViewport({ scale: (w / b.width) * k, rotation: rotation });
        var c = D.createElement('canvas');
        c.width = Math.floor(vp.width); c.height = Math.floor(vp.height);
        var ctx = c.getContext('2d', { alpha: false });
        ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height);
        return page.render({ canvasContext: ctx, viewport: vp }).promise.then(function () {
          p.busy = false;
          try { page.cleanup(); } catch (e) { /* released */ }
          if (token !== p.token || !alive) { c.width = 0; return; }
          if (p.canvas) { p.canvas.width = 0; p.canvas.remove(); }
          p.canvas = c; p.rw = w; p.rrot = rot;
          p.box.insertBefore(c, p.box.firstChild);
          p.box.classList.add('is-ready'); p.box.classList.remove('is-stale');
          sizeInk(p); paintInk(p); paintHits(p);
          if (p.w !== w || st.rot !== rot) { layout(); }
        });
      }).catch(function () { p.busy = false; });
    }
    function observe() {
      if (st.io) st.io.disconnect();
      st.io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          var p = st.pages[+e.target.dataset.n - 1];
          p.vis = e.isIntersecting;
          if (e.isIntersecting) draw(p); else if (p.canvas) release(p);
        });
      }, { root: scroll, rootMargin: '900px 0px' });
      st.pages.forEach(function (p) { st.io.observe(p.box); });
    }

    /* ---------------------------------------------------------------- reading state */
    function visibleNums() { var p = st.pages[st.cur - 1]; return p ? [p.n] : []; }
    function syncUI() {
      if (!st.N) return;
      var p = st.pages[st.cur - 1], marked = store.isMarked(st.cur);
      pill.firstChild.textContent = st.cur; pill.lastChild.textContent = '/ ' + st.N;
      if (scr) scr.set(st.cur);
      markBtn.classList.toggle('is-on', marked);
      markBtn.firstChild.textContent = marked ? 'bookmark_check' : 'bookmark_add';
      setLabel(markBtn, marked ? 'Remove bookmark' : 'Bookmark this page');
      $('[data-act="prev"]').disabled = st.cur <= 1;
      $('[data-act="next"]').disabled = st.cur >= st.N;
      if (p && p.w) zl.textContent = Math.round(pctOf(p) * 100) + '%';
      soundBtn.classList.toggle('is-on', sfx.state.on);
      inkBtn.classList.toggle('is-on', st.inking);
      $('[data-act="fitp"]').classList.toggle('is-on', st.mode === 'fitp');
      if (panels) panels.sync();
    }
    var raf = 0;
    function onScroll() {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var mid = scroll.scrollTop + scroll.clientHeight * 0.4, best = 1;
        for (var i = 0; i < st.pages.length; i++) {
          if (st.pages[i].box.offsetTop <= mid) best = i + 1; else break;
        }
        var max = scroll.scrollHeight - scroll.clientHeight;
        prog.style.transform = 'scaleX(' + (max > 0 ? clamp(scroll.scrollTop / max, 0, 1) : 0).toFixed(4) + ')';
        if (best !== st.cur) {
          st.cur = best;
          store.d.last = best; store.d.max = Math.max(store.d.max || 1, best); store.soon();
          syncUI();
          if (st.hlq === '' && text) { /* highlights are per page; nothing to refresh */ }
        }
      });
    }
    scroll.addEventListener('scroll', onScroll, { passive: true });

    function goto(n, quiet) {
      var p = st.pages[clamp(Math.round(n) || 1, 1, st.N) - 1];
      if (!p) return;
      var far = Math.abs(p.n - st.cur) > 3, from = st.cur;
      scroll.scrollTo({ top: p.box.offsetTop - 12, behavior: far || K.reduced ? 'auto' : 'smooth' });
      if (p.n !== from) sfx.turn(far ? 2 : 1.5, p.n > from ? 1 : -1, 0.6);
      if (!quiet && far) toast('Page ' + p.n, 'Back', function () { goto(from, true); });
    }
    function step(dir) {
      var span = prefs.view === 'two' && geometry().cols === 2 ? 2 : 1;
      var target = clamp(st.cur + dir * span, 1, st.N);
      if (target === st.cur) { sfx.bump(dir); return; }
      goto(target, true);
    }

    /* ---------------------------------------------------------------- zoom, rotate, view */
    function curPage() { return st.pages[st.cur - 1] || st.pages[0]; }
    function setMode(mode, pct, quiet) {
      var before = curPage() ? pctOf(curPage()) : 1;
      st.mode = mode; if (pct) st.pct = clamp(pct, 0.25, 4);
      layout();
      var after = curPage() ? curPage().w / (natural(curPage()).w * 4 / 3) : 1;
      if (!quiet) sfx.zoom(after > before);
      closeMenu();
    }
    function stepZoom(dir) {
      var p = curPage(); if (!p) return;
      var c = pctOf(p), z;
      if (dir > 0) { z = ZOOMS.filter(function (v) { return v > c * 1.02; })[0] || ZOOMS[ZOOMS.length - 1]; }
      else { var lo = ZOOMS.filter(function (v) { return v < c * 0.98; }); z = lo.length ? lo[lo.length - 1] : ZOOMS[0]; }
      setMode('pct', z);
    }
    function rotate() {
      var a = anchor();
      st.rot = (st.rot + 90) % 360;
      layout(false); restore(a);
      sfx.turn(1.6, 1, 0.5);
    }
    function setView(v) {
      prefs.view = v;
      if (v === 'single' && st.mode === 'fitw') st.mode = 'fitp';
      if (v === 'scroll' && st.mode === 'fitp') st.mode = 'fitw';
      var a = anchor(), n = st.cur;
      layout(false);
      scroll.classList.toggle('is-snap', v === 'single');
      goto(n, true);
      if (!a) return;
    }
    function buildMenu() {
      var cur = curPage() ? Math.round(pctOf(curPage()) * 100) : 100;
      var items = [['fitw', 'Fit width', 'fit_screen'], ['fitp', 'Fit page', 'pageview']];
      menu.innerHTML = items.map(function (it) {
        return '<button type="button" role="menuitemradio" class="nx-mi' + (st.mode === it[0] ? ' is-on' : '') + '" data-z="' + it[0] + '">' + K.icon(it[2]) + '<span>' + it[1] + '</span></button>';
      }).join('') + '<div class="nx-mis">' + ZOOMS.map(function (z) {
        return '<button type="button" role="menuitemradio" class="nx-mi nx-mn' + (st.mode === 'pct' && Math.abs(st.pct - z) < 0.01 ? ' is-on' : '') + '" data-z="' + z + '">' + Math.round(z * 100) + '%</button>';
      }).join('') + '</div><div class="nx-mc">' + cur + '%</div>';
    }
    function toggleMenu(force) {
      var show = force == null ? menu.hidden : force;
      if (show) { buildMenu(); menu.hidden = false; K.restart(menu, 'is-in'); } else menu.hidden = true;
    }
    function closeMenu() { menu.hidden = true; }
    menu.addEventListener('click', function (e) {
      var b = e.target.closest('[data-z]'); if (!b) return;
      var z = b.dataset.z;
      if (z === 'fitw' || z === 'fitp') setMode(z); else setMode('pct', +z);
    });

    /* pinch zoom, Ctrl + wheel, drag to pan */
    function pDist() { var k = Object.keys(st.pts), a = st.pts[k[0]], b = st.pts[k[1]]; return Math.hypot(a.x - b.x, a.y - b.y) || 1; }
    scroll.addEventListener('pointerdown', function (e) {
      if (st.inking) return;
      st.pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      stopAuto();
      if (Object.keys(st.pts).length === 2) { var p = curPage(); st.pinch = { d0: pDist(), z0: p ? pctOf(p) : 1 }; st.pan = null; return; }
      if (e.pointerType === 'mouse' && e.button === 0 && !e.target.closest('input')) {
        st.pan = { id: e.pointerId, x: e.clientX, y: e.clientY, sl: scroll.scrollLeft, stp: scroll.scrollTop, on: false };
      }
    });
    scroll.addEventListener('pointermove', function (e) {
      if (st.pts[e.pointerId]) { st.pts[e.pointerId].x = e.clientX; st.pts[e.pointerId].y = e.clientY; }
      if (st.pinch && Object.keys(st.pts).length === 2) {
        var z = clamp(st.pinch.z0 * pDist() / st.pinch.d0, 0.25, 4);
        st.mode = 'pct'; st.pct = Math.round(z * 100) / 100;
        if (!pinchRaf) pinchRaf = requestAnimationFrame(function () { pinchRaf = 0; layout(); });
        return;
      }
      var s = st.pan;
      if (!s || s.id !== e.pointerId) return;
      var dx = e.clientX - s.x, dy = e.clientY - s.y;
      if (!s.on && Math.abs(dx) + Math.abs(dy) > 4) { s.on = true; scroll.classList.add('is-grab'); try { scroll.setPointerCapture(e.pointerId); } catch (x) { /* fine */ } }
      if (s.on) { scroll.scrollLeft = s.sl - dx; scroll.scrollTop = s.stp - dy; }
    });
    var pinchRaf = 0;
    function endPtr(e) {
      delete st.pts[e.pointerId];
      if (Object.keys(st.pts).length < 2) st.pinch = null;
      if (st.pan && st.pan.id === e.pointerId) { st.pan = null; scroll.classList.remove('is-grab'); }
    }
    scroll.addEventListener('pointerup', endPtr);
    scroll.addEventListener('pointercancel', endPtr);
    scroll.addEventListener('wheel', function (e) {
      stopAuto();
      if (!e.ctrlKey) return;
      e.preventDefault();
      var p = curPage(); if (!p) return;
      st.mode = 'pct'; st.pct = clamp(pctOf(p) * (e.deltaY < 0 ? 1.1 : 0.9), 0.25, 4);
      if (!pinchRaf) pinchRaf = requestAnimationFrame(function () { pinchRaf = 0; layout(); });
    }, { passive: false });
    scroll.addEventListener('dblclick', function (e) {
      if (st.inking || !e.target.closest('.vw-pdf-page')) return;
      var p = curPage();
      if (st.mode === 'fitw' || st.mode === 'fitp') setMode('pct', 2); else setMode('fitw');
      void p;
    });
    root.addEventListener('contextmenu', function (e) { e.preventDefault(); });

    /* ---------------------------------------------------------------- auto scroll */
    function stopAuto() {
      if (!st.auto) return;
      cancelAnimationFrame(st.auto); st.auto = 0;
      autoBtn.classList.remove('is-on'); autoBtn.firstChild.textContent = 'play_arrow';
      setLabel(autoBtn, 'Scroll automatically');
    }
    function startAuto() {
      stopAuto();
      var last = performance.now(), carry = 0;
      autoBtn.classList.add('is-on'); autoBtn.firstChild.textContent = 'pause';
      setLabel(autoBtn, 'Stop scrolling');
      (function tick(now) {
        if (!alive) return;
        carry += (now - last) / 1000 * (SCROLL_PX[prefs.scroll] || 70); last = now;
        if (carry >= 1) { var d = Math.floor(carry); carry -= d; scroll.scrollTop += d; }
        if (scroll.scrollTop + scroll.clientHeight >= scroll.scrollHeight - 2) { stopAuto(); toast('End of the document'); return; }
        st.auto = requestAnimationFrame(tick);
      })(last);
      st.auto = st.auto || 1;
    }

    /* ---------------------------------------------------------------- annotate, bookmarks, search highlights */
    function toggleInk(on) {
      st.inking = on == null ? !st.inking : on;
      root.classList.toggle('is-inking', st.inking);
      inkBar.show(st.inking);
      if (st.inking) stopAuto();
      sfx.pop(st.inking);
      syncUI();
    }
    function toggleMark() {
      var r = store.toggle([st.cur], st.cur);
      toast(r === 'added' ? 'Bookmarked page ' + st.cur : 'Bookmark removed');
      sfx.chime(r === 'added');
      syncUI();
    }
    function refreshHL() { st.pages.forEach(function (p) { if (p.canvas) paintHits(p); }); }

    /* ---------------------------------------------------------------- settings and help */
    function applyPrefs() {
      root.dataset.tone = prefs.tone;
      root.style.setProperty('--nx-filter', K.toneFilter(prefs));
      var save = Object.assign({}, prefs); delete save.sound; delete save.vol;
      K.jset(PREFS_KEY, save);
    }
    function schema() {
      var s = [
        { t: 'seg', k: 'tone', h: 'Page tone', o: [['paper', 'Paper', 'light_mode'], ['sepia', 'Sepia', 'wb_twilight'], ['night', 'Night', 'dark_mode']] },
        { t: 'range', k: 'bright', h: 'Brightness', min: 60, max: 110 },
        { t: 'range', k: 'warm', h: 'Warmth', min: 0, max: 60 },
        { t: 'seg', k: 'view', h: 'View', o: [['scroll', 'Scroll', 'table_rows'], ['two', 'Two pages', 'auto_stories'], ['single', 'One page', 'smartphone']] },
        { t: 'seg', k: 'scroll', h: 'Auto-scroll speed', o: [[1, 'Slow'], [2, 'Medium'], [3, 'Fast']] },
        { t: 'range', k: 'vol', h: 'Volume', min: 0, max: 100 },
        { t: 'sw', k: 'sound', label: 'Page sound', icon: 'volume_up' }
      ];
      if (opts.onBook) s.push({ t: 'btn', act: 'book', label: 'Switch to book reader', icon: 'auto_stories' });
      return s;
    }
    function togglePop(force) {
      var show = force == null ? pop.hidden : force;
      if (show) { closeMenu(); pop.innerHTML = K.settingsHTML(schema(), prefs); pop.hidden = false; K.restart(pop, 'is-in'); } else pop.hidden = true;
      settingsBtn.classList.toggle('is-on', show);
    }
    K.bindSettings(pop, prefs, function (k, v) {
      if (k === '@book') { if (opts.onBook) opts.onBook(); return; }
      if (k === 'sound') { sfx.set('on', v); prefs.sound = v; syncUI(); return; }
      if (k === 'vol') { sfx.set('vol', v / 100); prefs.vol = v; return; }
      prefs[k] = v; applyPrefs();
      if (k === 'view') setView(v);
    });
    var HELP = [
      ['Next / previous page', 'Right Left  PgDn PgUp'], ['First or last page', 'Home End'], ['Go to page', 'G'], ['Zoom', '+  \u2212  0'], ['Fit width / page', '1  2'],
      ['Rotate', 'R'], ['View', 'V'], ['Search', 'S'], ['Pages / contents', 'T  C'], ['Bookmark', 'B'], ['Annotate', 'A'], ['Scroll automatically', 'P'],
      ['Sound', 'M'], ['Hide controls', 'H'], ['Full screen', 'F'], ['Close', 'Esc']
    ];
    function toggleHelp(force) {
      var show = force == null ? help.hidden : force;
      if (show) { help.innerHTML = K.helpHTML(HELP); help.hidden = false; } else help.hidden = true;
    }

    /* ---------------------------------------------------------------- commands */
    function gotoPrompt() {
      var done = false, inp = el('input', 'nx-pill bk-gin');
      inp.type = 'number'; inp.min = 1; inp.max = st.N; inp.value = st.cur;
      inp.setAttribute('aria-label', 'Page number');
      pill.hidden = true; pill.parentNode.insertBefore(inp, pill);
      inp.focus(); inp.select();
      function end(go) {
        if (done) return; done = true;
        var v = +inp.value; pill.hidden = false;
        if (inp.parentNode) inp.parentNode.removeChild(inp);
        if (go && v) goto(v);
        scroll.focus({ preventScroll: true });
      }
      inp.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter') end(true); if (e.key === 'Escape') end(false); });
      inp.addEventListener('blur', function () { end(false); });
    }
    function act(a) {
      if (a !== 'auto' && a !== 'zmenu') stopAuto();
      switch (a) {
        case 'prev': step(-1); break;
        case 'next': step(1); break;
        case 'goto': gotoPrompt(); break;
        case 'zin': stepZoom(1); break;
        case 'zout': stepZoom(-1); break;
        case 'zmenu': togglePop(false); toggleMenu(); break;
        case 'fitp': setMode(st.mode === 'fitp' ? 'fitw' : 'fitp'); break;
        case 'rotate': rotate(); break;
        case 'mark': toggleMark(); break;
        case 'ink': toggleInk(); break;
        case 'auto': if (st.auto) stopAuto(); else startAuto(); sfx.tick(); break;
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
      if (pb) { togglePop(false); closeMenu(); panels.open(pb.dataset.panel); sfx.tick(); return; }
      var a = e.target.closest('[data-act]');
      if (a && !a.closest('.nx-pop')) act(a.dataset.act);
      if (!pop.hidden && !e.target.closest('.nx-pop') && !e.target.closest('[data-act="settings"]')) togglePop(false);
      if (!menu.hidden && !e.target.closest('.nx-menu') && !e.target.closest('[data-act="zmenu"]')) closeMenu();
      if (e.target === help) toggleHelp(false);
    });
    var VIEWS = ['scroll', 'two', 'single'];
    root.addEventListener('keydown', function (e) {
      if (e.target.matches && e.target.matches('input, textarea')) return;
      if (e.altKey || e.metaKey || e.key === 'Tab' || e.key === 'Shift' || e.key === 'Control') return;
      var k = e.key, handled = true, fit = st.mode !== 'pct' || scroll.scrollWidth <= scroll.clientWidth + 2;
      if (e.ctrlKey) {
        if (k === 'f' || k === 'F') { e.preventDefault(); panels.focusSearch(); }
        else if (k === 'z' || k === 'Z') { if (st.inking) { e.preventDefault(); ink.undo(st.cur); } }
        return;
      }
      if (k !== 'p' && k !== 'P') stopAuto();
      if (k === 'PageDown' || (k === ' ' && !e.shiftKey)) step(1);
      else if (k === 'PageUp' || (k === ' ' && e.shiftKey)) step(-1);
      else if ((k === 'ArrowRight' || k === 'ArrowLeft') && fit) step(k === 'ArrowRight' ? 1 : -1);
      else if (k === 'Home') goto(1);
      else if (k === 'End') goto(st.N);
      else if (k === '+' || k === '=') stepZoom(1);
      else if (k === '-' || k === '_') stepZoom(-1);
      else if (k === '0') setMode('pct', 1);
      else if (k === '1') setMode('fitw');
      else if (k === '2') setMode('fitp');
      else if (k === 'r' || k === 'R') rotate();
      else if (k === 'v' || k === 'V') { var nv = VIEWS[(VIEWS.indexOf(prefs.view) + 1) % 3]; prefs.view = nv; applyPrefs(); setView(nv); toast(nv === 'scroll' ? 'Scrolling view' : (nv === 'two' ? 'Two pages' : 'One page')); }
      else if (k === 'b' || k === 'B') toggleMark();
      else if (k === 'a' || k === 'A') toggleInk();
      else if (k === 'm' || k === 'M') act('sound');
      else if (k === 'h' || k === 'H') { st.bare = !st.bare; root.classList.toggle('is-bare', st.bare); }
      else if (k === 's' || k === 'S' || k === '/') panels.open('search');
      else if (k === 't' || k === 'T') panels.open('pages');
      else if (k === 'c' || k === 'C') panels.open('toc');
      else if (k === 'g' || k === 'G') gotoPrompt();
      else if (k === 'p' || k === 'P') { if (st.auto) stopAuto(); else startAuto(); }
      else if (k === 'f' || k === 'F') { var fs = D.getElementById('vw-fs'); if (fs) fs.click(); }
      else if (k === '?') toggleHelp();
      else if (k === 'Escape') {
        if (!help.hidden) toggleHelp(false); else if (!menu.hidden) closeMenu(); else if (!pop.hidden) togglePop(false); else if (st.inking) toggleInk(false); else if (panels.current()) panels.close(); else handled = false;
      } else handled = false;
      if (handled) e.preventDefault();
    });

    var resizeT = 0, lastW = 0, lastH = 0;
    var ro = window.ResizeObserver ? new ResizeObserver(function () {
      if (!st.doc || !scroll.clientWidth || (scroll.clientWidth === lastW && scroll.clientHeight === lastH)) return;
      lastW = scroll.clientWidth; lastH = scroll.clientHeight;
      clearTimeout(resizeT);
      resizeT = setTimeout(function () { if (alive) layout(); }, 120);
    }) : null;
    if (ro) ro.observe(scroll);

    /* ---------------------------------------------------------------- start */
    applyPrefs();
    var ready = open(src).then(function (doc) {
      st.doc = doc; st.N = doc.numPages;
      text = K.text(doc);
      thumbs = K.thumbs(doc, 140);
      var sthumbs = K.thumbs(doc, 96);
      st.sthumbs = sthumbs;
      panels = K.panels({
        host: panelEl, root: root, doc: doc, N: function () { return st.N; }, ratio: function () { var p = st.pages[0]; return p ? p.nh / p.nw || st.nh / st.nw : st.nh / st.nw; }, text: text, thumbs: thumbs,
        store: store, ink: ink, visible: visibleNums, cur: function () { return st.cur; }, go: function (n) { goto(n); },
        query: { get: function () { return st.hlq; }, set: function (q) { st.hlq = q; refreshHL(); } },
        relayout: function () { setTimeout(function () { if (alive) layout(); }, 40); }, phone: function () { return root.clientWidth < 720; },
        mark: toggleMark, toast: toast, changed: syncUI
      });
      scr = K.scrubber($('.nx-scrub'), { N: function () { return st.N; }, go: function (n) { stopAuto(); goto(n, true); }, thumbs: sthumbs, marks: function () { return store.d.marks.map(function (m) { return m.p; }); }, ratio: function () { return st.nh / st.nw; }, focus: function () { scroll.focus({ preventScroll: true }); } });
      session = K.session(store, root, function (t) { if (panels.current() === 'marks' && t % 30 === 0) panels.renderMarks(); });
      return doc.getPage(1).then(function (page) {
        var v = page.getViewport({ scale: 1, rotation: page.rotate });
        st.nw = v.width; st.nh = v.height;
        st.br = el('div', 'cl-br'); st.br.hidden = true;
        for (var n = 1; n <= doc.numPages; n++) {
          var box = el('div', 'vw-pdf-page');
          box.dataset.n = n;
          box.setAttribute('role', 'img');
          box.setAttribute('aria-label', 'Page ' + n);
          var hls = el('div', 'nx-hls'), inkc = el('canvas', 'nx-ink');
          box.appendChild(hls); box.appendChild(inkc);
          scroll.appendChild(box);
          if (n === 1) scroll.appendChild(st.br);
          var p = { n: n, box: box, hls: hls, inkc: inkc, canvas: null, busy: false, token: 0, vis: false, w: 0, nw: n === 1 ? v.width : 0, nh: n === 1 ? v.height : 0 };
          st.pages.push(p);
          (function (pp) {
            K.inkBind(inkc, { n: function () { return pp.n; }, ink: ink, tool: inkBar.tool, active: function () { return st.inking; }, ratio: function () { return ratioOf(pp); } });
          })(p);
        }
        lastW = scroll.clientWidth; lastH = scroll.clientHeight;
        scroll.classList.toggle('is-snap', prefs.view === 'single');
        layout(false);
        observe();
        var start = opts.page || (store.d.last > 1 && store.d.last < st.N ? store.d.last : 1);
        if (start > 1) { setTimeout(function () { var p2 = st.pages[start - 1]; if (p2) scroll.scrollTop = p2.box.offsetTop - 12; if (!opts.page) toast('Continued on page ' + start, 'From the start', function () { goto(1, true); }); }, 60); }
        onScroll();
      });
    });

    function destroy() {
      alive = false;
      stopAuto();
      if (session) session.stop(); else store.save();
      ink.flush();
      timers.forEach(clearTimeout);
      clearTimeout(redrawT); clearTimeout(resizeT);
      cancelAnimationFrame(raf); cancelAnimationFrame(pinchRaf);
      if (ro) ro.disconnect();
      if (st.io) st.io.disconnect();
      if (text) text.stop();
      if (thumbs) thumbs.destroy();
      if (st.sthumbs) st.sthumbs.destroy();
      if (panels) panels.destroy();
      st.pages.forEach(function (p) { if (p.canvas) { p.canvas.width = 0; } });
      sfx.close();
      root.remove();
    }
    return { node: root, ready: ready, goto: function (n) { goto(n, true); }, page: function () { return st.cur; }, destroy: destroy };
  }

  /* Without the kit (a script failed to load) the reader is just a stack of pages. */
  function plain(src, title) {
    var root = document.createElement('div');
    root.className = 'vw-pdf';
    var scroll = document.createElement('div');
    scroll.className = 'vw-pdf-scroll';
    root.appendChild(scroll);
    var ready = open(src).then(function (doc) {
      var chain = Promise.resolve();
      for (var n = 1; n <= Math.min(doc.numPages, 60); n++) {
        (function (k) {
          chain = chain.then(function () {
            return doc.getPage(k).then(function (page) {
              var w = Math.max(240, scroll.clientWidth - 24), v = page.getViewport({ scale: 1 }), vp = page.getViewport({ scale: w / v.width });
              var c = document.createElement('canvas');
              c.width = vp.width; c.height = vp.height; c.className = 'vw-pdf-page'; c.style.width = w + 'px';
              scroll.appendChild(c);
              return page.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise;
            });
          });
        })(n);
      }
      return chain;
    });
    return { node: root, ready: ready, goto: function () { }, page: function () { return 1; }, destroy: function () { root.remove(); } };
  }

  window.NebPdf = { mount: mount, open: open };
})();
