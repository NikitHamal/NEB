/* NEBians landing. Small on purpose: everything visual lives in landing.css; this file only
   flips classes. Nothing here is needed to read the page (no-js shows every section).
   - .ready      fonts are in (or 900 ms passed): the hero entrance plays
   - .in         a [data-reveal] element has scrolled into view: its spring plays once
   - .is-live    a [data-live] section is on screen: its looping motion runs, otherwise it pauses
   - nav         menu sheet, scrolled state, and a pill that follows the current section
   - [data-type] the hero search types through a few subjects */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;

  function ready() { requestAnimationFrame(function () { doc.classList.add('ready'); }); }
  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise(function (r) { setTimeout(r, 900); })]).then(ready);
  } else { ready(); }

  var all = function (sel) { return [].slice.call(document.querySelectorAll(sel)); };

  /* ---- reveal once ---- */
  var reveal = all('[data-reveal], .foot-word');
  if (canObserve && !still) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveal.forEach(function (el) { io.observe(el); });
  } else {
    reveal.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- looping motion only while on screen ---- */
  var live = all('[data-live]');
  if (canObserve) {
    var lio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle('is-live', en.isIntersecting); });
    }, { rootMargin: '10% 0px' });
    live.forEach(function (el) { lio.observe(el); });
  } else {
    live.forEach(function (el) { el.classList.add('is-live'); });
  }

  /* ---- navigation ---- */
  var nav = document.querySelector('[data-nav]');
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  function setMenu(open) {
    doc.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    menu.setAttribute('aria-hidden', open ? 'false' : 'true');
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!doc.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    matchMedia('(min-width: 921px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', scrollY > 24); };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var links = all('.nav-links a');
  var ind = document.querySelector('.nav-ind');
  var current = null;
  function place(link) {
    if (!ind) return;
    if (!link) { ind.classList.remove('on'); return; }
    ind.style.setProperty('--x', link.offsetLeft + 'px');
    ind.style.setProperty('--w', link.offsetWidth + 'px');
    ind.classList.add('on');
  }
  function setCurrent(link) {
    current = link;
    links.forEach(function (a) { if (a === link) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    place(link);
  }
  links.forEach(function (a) {
    a.addEventListener('mouseenter', function () { place(a); });
    a.addEventListener('focus', function () { place(a); });
    a.addEventListener('mouseleave', function () { place(current); });
    a.addEventListener('blur', function () { place(current); });
  });
  addEventListener('resize', function () { place(current); });
  if (canObserve && links.length) {
    var seen = {};
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { seen[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
      var best = null, top = 0;
      links.forEach(function (a) {
        var id = a.getAttribute('href').slice(1);
        if ((seen[id] || 0) > top) { top = seen[id]; best = a; }
      });
      setCurrent(best);
    }, { rootMargin: '-30% 0px -40% 0px', threshold: [0, 0.1, 0.3, 0.6, 1] });
    links.forEach(function (a) {
      var t = document.getElementById(a.getAttribute('href').slice(1));
      if (t) sio.observe(t);
    });
  }

  /* ---- hero: the search types through a few subjects ---- */
  var typed = document.querySelector('[data-type]');
  var rows = document.querySelector('[data-rows]');
  var words = ['Physics Class 12', 'Mathematics Class 10', 'Accountancy Class 11', 'Biology Class 12', 'Science Class 8'];
  if (typed && !still) {
    var wi = 0, ci = typed.textContent.length, dir = -1, timer = null, running = false;
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
        if (rows) {
          rows.classList.remove('swap');
          void rows.offsetWidth; // restart the pop
          rows.classList.add('swap');
        }
        return later(260);
      }
      later(26);
    };
    var later = function (ms) { timer = setTimeout(step, ms); };
    var stage = document.querySelector('.stage');
    var tio = new IntersectionObserver(function (en) {
      var on = en[0].isIntersecting;
      if (on && !running) { running = true; later(1600); }
      if (!on && running) { running = false; clearTimeout(timer); }
    });
    if (stage) tio.observe(stage);

    /* pointer parallax on the floating shapes (fine pointers only) */
    if (stage && matchMedia('(hover: hover) and (pointer: fine)').matches) {
      var raf = 0;
      addEventListener('pointermove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          stage.style.setProperty('--mx', (e.clientX / innerWidth * 2 - 1).toFixed(3));
          stage.style.setProperty('--my', (e.clientY / innerHeight * 2 - 1).toFixed(3));
        });
      }, { passive: true });
    }
  }
})();
