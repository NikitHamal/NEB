/* NEBians landing: what is specific to this page. Shared behaviour (reveal, looping-motion
   pause, the sliding pill nav) lives in m3x.js. Nothing here is needed to read the page.
   - .ready      fonts are in (or 900 ms passed): the hero entrance plays
   - nav         scrolled state, and the full-screen menu sheet on small screens
   - [data-type] the hero search types through a few subjects
   - pointer     the floating shapes drift toward the pointer, eased, fine pointers only */
(function () {
  var doc = document.documentElement;
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var all = function (sel) { return [].slice.call(document.querySelectorAll(sel)); };

  function ready() { requestAnimationFrame(function () { doc.classList.add('ready'); }); }
  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise(function (r) { setTimeout(r, 900); })]).then(ready);
  } else { ready(); }

  /* ---- navigation bar: solid once scrolled ---- */
  var nav = document.querySelector('[data-nav]');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', scrollY > 24); };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- menu sheet (small screens) ----
     Closed: inert, so its links are out of the tab order and the reader. Open: the page
     behind is inert too, focus moves into the sheet, Escape closes and focus goes back. */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  var main = document.getElementById('main');
  var lastFocus = null;
  function setMenu(open) {
    if (!burger || !menu) return;
    if (open === doc.classList.contains('menu-open')) return;
    doc.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    menu.setAttribute('aria-hidden', open ? 'false' : 'true');
    if ('inert' in menu) { menu.inert = !open; if (main) main.inert = open; }
    if (open) {
      lastFocus = document.activeElement;
      var first = menu.querySelector('a');
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 60);
    } else if (lastFocus && lastFocus.focus) { lastFocus.focus({ preventScroll: true }); lastFocus = null; }
  }
  if (burger && menu) {
    if ('inert' in menu) menu.inert = true;
    burger.addEventListener('click', function () { setMenu(!doc.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) { lastFocus = null; setMenu(false); } });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
      if (e.key === 'Tab' && doc.classList.contains('menu-open')) {
        var items = [burger].concat([].slice.call(menu.querySelectorAll('a')));
        var i = items.indexOf(document.activeElement);
        var next = e.shiftKey ? (i <= 0 ? items.length - 1 : i - 1) : (i === items.length - 1 ? 0 : i + 1);
        e.preventDefault(); items[next].focus();
      }
    });
    matchMedia('(min-width: 921px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  /* ---- hero: the search types through a few subjects ---- */
  var typed = document.querySelector('[data-type]');
  var rows = document.querySelector('[data-rows]');
  var stage = document.querySelector('.stage');
  var words = ['Physics Class 12', 'Mathematics Class 10', 'Accountancy Class 11', 'Biology Class 12', 'Science Class 8'];
  if (typed && !still) {
    var wi = 0, ci = typed.textContent.length, dir = -1, timer = 0, running = false;
    var later = function (ms) { timer = setTimeout(step, ms); };
    var step = function () {
      var w = words[wi];
      if (dir > 0) {
        ci++;
        typed.textContent = w.slice(0, ci);
        if (ci >= w.length) { dir = -1; return later(1900); }
        return later(55 + Math.random() * 45);
      }
      ci--;
      typed.textContent = w.slice(0, Math.max(ci, 0));
      if (ci <= 0) {
        dir = 1; wi = (wi + 1) % words.length;
        if (rows) { rows.classList.remove('swap'); void rows.offsetWidth; rows.classList.add('swap'); }
        return later(260);
      }
      later(26);
    };
    if (stage && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        var on = en[0].isIntersecting;
        if (on && !running) { running = true; later(1600); }
        if (!on && running) { running = false; clearTimeout(timer); }
      }).observe(stage);
    }
  }

  /* ---- pointer: eased drift of the floating shapes, only while the hero is on screen ---- */
  if (stage && !still && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, visible = true;
    var tick = function () {
      cx += (tx - cx) * 0.12; cy += (ty - cy) * 0.12;
      stage.style.setProperty('--mx', cx.toFixed(3));
      stage.style.setProperty('--my', cy.toFixed(3));
      raf = (Math.abs(tx - cx) > 0.002 || Math.abs(ty - cy) > 0.002) ? requestAnimationFrame(tick) : 0;
    };
    var kick = function () { if (!raf && visible) raf = requestAnimationFrame(tick); };
    addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX / innerWidth * 2 - 1; ty = e.clientY / innerHeight * 2 - 1; kick();
    }, { passive: true });
    document.addEventListener('pointerleave', function () { tx = 0; ty = 0; kick(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (!visible) { tx = ty = 0; } kick(); }).observe(stage);
    }
  }
})();
