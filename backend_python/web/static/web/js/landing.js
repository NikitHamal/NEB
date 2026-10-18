/* NEBians landing page. No dependencies. Every effect is optional: without JS the page is
   complete; with reduced motion it is still; off-screen layers are paused. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.remove('no-js');
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;

  /* Reveal on scroll, once. */
  var revealed = function (el) { el.classList.add('is-in'); };
  var items = d.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window) || still) {
    items.forEach(revealed);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { revealed(e.target); io.unobserve(e.target); if (e.target.querySelector('[data-count]')) count(e.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* Count-up for the numbers strip. */
  function count(scope) {
    scope.querySelectorAll('[data-count]').forEach(function (b) {
      var to = +b.getAttribute('data-count'), t0 = null, dur = 1400;
      if (!to || still || d.visibilityState !== 'visible') return;
      var fmt = new Intl.NumberFormat('en-IN');
      function step(t) {
        if (!t0) t0 = t;
        var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        b.textContent = fmt.format(Math.round(to * e));
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
  d.querySelectorAll('[data-count]').forEach(function (b) {
    b.textContent = new Intl.NumberFormat('en-IN').format(+b.getAttribute('data-count'));
  });

  /* Nav: solid once the page moves. */
  var nav = d.querySelector('.lp-nav'), ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { nav.classList.toggle('is-stuck', scrollY > 8); ticking = false; });
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Mobile menu. */
  var menu = d.querySelector('.lp-menu'), sheet = d.getElementById('lp-sheet');
  if (menu) menu.addEventListener('click', function () {
    var open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', open); sheet.hidden = !open;
  });
  if (sheet) sheet.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') { menu.setAttribute('aria-expanded', 'false'); sheet.hidden = true; }
  });

  /* Class tabs: roving tabindex, arrow keys, sliding indicator. */
  var tabs = d.querySelector('.lp-tabs');
  if (tabs) {
    var btns = [].slice.call(tabs.querySelectorAll('[role=tab]')), ink = tabs.querySelector('.lp-tab-ink');
    var place = function (b) { ink.style.setProperty('--x', b.offsetLeft + 'px'); ink.style.setProperty('--w', b.offsetWidth + 'px'); };
    var select = function (b, focus) {
      btns.forEach(function (x) {
        var on = x === b;
        x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        d.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      });
      place(b); if (focus) b.focus();
      if (b.scrollIntoView && tabs.scrollWidth > tabs.clientWidth) b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: still ? 'auto' : 'smooth' });
    };
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { select(b); });
      b.addEventListener('keydown', function (e) {
        var j = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? btns.length - 1 : null;
        if (j === null) return; e.preventDefault(); select(btns[(j + btns.length) % btns.length], true);
      });
    });
    var cur = function () { return tabs.querySelector('[aria-selected=true]') || btns[0]; };
    (d.fonts && d.fonts.ready ? d.fonts.ready : Promise.resolve()).then(function () { place(cur()); });
    addEventListener('resize', function () { place(cur()); }, { passive: true });
  }

  /* Pause decor and the hero stage when they are off-screen. */
  var hero = d.querySelector('.lp-hero');
  if ('IntersectionObserver' in window) {
    var pio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('is-paused', !e.isIntersecting); });
    });
    d.querySelectorAll('.lp-hero,.lp-final').forEach(function (s) { pio.observe(s); });
  }

  /* Pointer parallax on the hero cards: desktop pointers only, one rAF per frame. */
  if (fine && !still && hero) {
    var floats = [].slice.call(hero.querySelectorAll('[data-depth]')), mx = 0, my = 0, raf = 0;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      mx = (e.clientX - r.left) / r.width - 0.5; my = (e.clientY - r.top) / r.height - 0.5;
      if (!raf) raf = requestAnimationFrame(function () {
        raf = 0;
        floats.forEach(function (f) {
          var k = +f.getAttribute('data-depth');
          f.style.setProperty('--px', (mx * k).toFixed(1) + 'px'); f.style.setProperty('--py', (my * k).toFixed(1) + 'px');
        });
      });
    }, { passive: true });
  }

  /* The real Neby, loaded only when the hero is on screen and the browser is idle. */
  var slot = d.querySelector('[data-lazy-neby]');
  var conn = navigator.connection || {};
  if (slot && !conn.saveData && !/(^|-)2g$/.test(conn.effectiveType || '')) {
    var load = function () {
      var l = d.createElement('link'); l.rel = 'stylesheet'; l.href = slot.getAttribute('data-css'); d.head.appendChild(l);
      var host = d.createElement('div');
      host.setAttribute('data-neby-avatar', ''); host.setAttribute('data-animation', 'intro-neby');
      host.className = 'lp-neby-live';
      var s = d.createElement('script'); s.src = slot.getAttribute('data-src'); s.async = true;
      s.onload = function () {
        slot.appendChild(host);
        if (window.NebyAvatar) window.NebyAvatar.initAll();
        requestAnimationFrame(function () { slot.classList.add('is-live'); });
      };
      d.body.appendChild(s);
    };
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 300); };
    if ('IntersectionObserver' in window) {
      var nio = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { nio.disconnect(); idle(load, { timeout: 2000 }); }
      });
      nio.observe(slot);
    } else { idle(load); }
  }
})();
