/* NebPdf: a view-only PDF reader drawn with PDF.js, so a PDF reads the same on Android Chrome, iOS and desktop.
   Pages are placeholders until they scroll near the viewport, and are released when they leave it, so a 400 page
   book costs about as much as ten. window.NebPdf.mount(src, title) -> { node, ready } ; ready rejects when the
   file cannot be drawn and the caller falls back to the browser's own viewer. */
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

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  }
  function icon(name) { return '<span class="material-symbols-outlined" aria-hidden="true">' + name + '</span>'; }

  function mount(src, title) {
    var root = el('div', 'vw-pdf');
    var scroll = el('div', 'vw-pdf-scroll');
    scroll.tabIndex = 0;
    scroll.setAttribute('aria-label', title || 'Document');
    var dock = el('div', 'vw-pdf-dock');
    dock.innerHTML =
      '<button type="button" class="vw-pdf-btn" data-z="-1" aria-label="Zoom out">' + icon('remove') + '</button>' +
      '<span class="vw-pdf-count" aria-live="polite"><b>1</b> / <i>-</i></span>' +
      '<button type="button" class="vw-pdf-btn" data-z="1" aria-label="Zoom in">' + icon('add') + '</button>';
    root.appendChild(scroll);
    root.appendChild(dock);

    var state = { doc: null, pages: [], zoom: 1, ratio: 1.414, current: 1, io: null };
    var counter = dock.querySelector('b'), total = dock.querySelector('i');
    var dpr = Math.min(window.devicePixelRatio || 1, 2);

    function pageWidth() { return Math.max(200, (scroll.clientWidth - (scroll.clientWidth < 600 ? 20 : 40)) * state.zoom); }

    function layout() {
      var w = pageWidth();
      state.pages.forEach(function (p) {
        p.box.style.width = w + 'px';
        p.box.style.height = Math.round(w * (p.ratio || state.ratio)) + 'px';
        release(p);
      });
      observe();
    }

    function release(p) {
      p.token++;
      if (p.canvas) { p.canvas.width = 0; p.canvas.height = 0; p.canvas.remove(); p.canvas = null; }
      p.box.classList.remove('is-ready');
    }

    function draw(p) {
      if (p.canvas || p.busy) return;
      p.busy = true;
      var token = ++p.token;
      state.doc.getPage(p.n).then(function (page) {
        if (token !== p.token) { p.busy = false; return; }
        var base1 = page.getViewport({ scale: 1 });
        p.ratio = base1.height / base1.width;
        var w = pageWidth();
        p.box.style.height = Math.round(w * p.ratio) + 'px';
        var vp = page.getViewport({ scale: (w / base1.width) * dpr });
        var c = document.createElement('canvas');
        c.width = Math.floor(vp.width); c.height = Math.floor(vp.height);
        c.style.width = '100%'; c.style.height = '100%';
        return page.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise.then(function () {
          p.busy = false;
          if (token !== p.token) { c.width = 0; return; }
          p.canvas = c; p.box.appendChild(c); p.box.classList.add('is-ready');
        });
      }).catch(function () { p.busy = false; });
    }

    function observe() {
      if (state.io) state.io.disconnect();
      state.io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          var p = state.pages[+e.target.dataset.n - 1];
          if (e.isIntersecting) draw(p); else if (p.canvas) release(p);
        });
      }, { root: scroll, rootMargin: '900px 0px' });
      state.pages.forEach(function (p) { state.io.observe(p.box); });
    }

    var raf = 0;
    scroll.addEventListener('scroll', function () {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var mid = scroll.scrollTop + scroll.clientHeight * 0.4, best = 1;
        for (var i = 0; i < state.pages.length; i++) {
          var b = state.pages[i].box;
          if (b.offsetTop <= mid) best = i + 1; else break;
        }
        if (best !== state.current) { state.current = best; counter.textContent = best; }
      });
    }, { passive: true });

    dock.addEventListener('click', function (e) {
      var b = e.target.closest('[data-z]');
      if (!b) return;
      var before = scroll.scrollTop / Math.max(1, scroll.scrollHeight);
      state.zoom = Math.max(0.6, Math.min(3, state.zoom + (+b.dataset.z) * 0.25));
      layout();
      scroll.scrollTop = before * scroll.scrollHeight;
    });

    scroll.addEventListener('keydown', function (e) {
      var step = scroll.clientHeight * 0.9;
      if (e.key === 'PageDown' || e.key === ' ') { scroll.scrollBy({ top: step, behavior: 'smooth' }); e.preventDefault(); }
      if (e.key === 'PageUp') { scroll.scrollBy({ top: -step, behavior: 'smooth' }); e.preventDefault(); }
    });
    root.addEventListener('contextmenu', function (e) { e.preventDefault(); });

    var resizeT = 0, lastW = 0;
    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        if (!state.doc || !scroll.clientWidth || scroll.clientWidth === lastW) return;
        lastW = scroll.clientWidth;
        clearTimeout(resizeT);
        resizeT = setTimeout(layout, 150);
      }).observe(scroll);
    }

    var ready = load().then(function (m) {
      var task = m.getDocument({ url: src, withCredentials: false });
      return task.promise;
    }).then(function (doc) {
      state.doc = doc;
      total.textContent = doc.numPages;
      return doc.getPage(1).then(function (page) {
        var v = page.getViewport({ scale: 1 });
        state.ratio = v.height / v.width;
        for (var n = 1; n <= doc.numPages; n++) {
          var box = el('div', 'vw-pdf-page');
          box.dataset.n = n;
          box.setAttribute('role', 'img');
          box.setAttribute('aria-label', 'Page ' + n);
          scroll.appendChild(box);
          state.pages.push({ n: n, box: box, canvas: null, busy: false, token: 0, ratio: n === 1 ? state.ratio : 0 });
        }
        lastW = scroll.clientWidth;
        layout();
      });
    });

    return { node: root, ready: ready };
  }

  window.NebPdf = { mount: mount };
})();
