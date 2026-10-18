/* NEBians landing. One passive scroll listener and one rAF write per frame: each on-screen
   [data-track] element gets --p (progress through its pinned stretch) and --e (how far it has
   entered). CSS turns those into motion. Off-screen elements are skipped entirely. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ready() { requestAnimationFrame(function () { doc.classList.add('ready'); }); }
  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise(function (r) { setTimeout(r, 900); })]).then(ready);
  } else { ready(); }

  /* ---- scroll-linked progress ---- */
  var tracks = [].slice.call(document.querySelectorAll('[data-track]'));
  var live = new Set();
  var vh = innerHeight;
  var queued = false;

  function measure() {
    queued = false;
    // read every rect first, then write: interleaving would force a layout per element
    var reads = [];
    live.forEach(function (el) { reads.push([el, el.getBoundingClientRect()]); });
    reads.forEach(function (pair) {
      var el = pair[0], r = pair[1];
      var span = r.height - vh;
      var p = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
      var e = Math.min(1, Math.max(0, (vh - r.top) / vh));
      el.style.setProperty('--p', p.toFixed(4));
      el.style.setProperty('--e', e.toFixed(4));
    });
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(measure); } }

  if (!still && 'IntersectionObserver' in window) {
    var watch = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) live.add(en.target); else live.delete(en.target);
        en.target.classList.toggle('is-live', en.isIntersecting);
      });
      queue();
    }, { rootMargin: '10% 0px' });
    tracks.forEach(function (el) { watch.observe(el); });
    addEventListener('scroll', queue, { passive: true });
    addEventListener('resize', function () { vh = innerHeight; queue(); });
  }
  /* the flag only waves while the hero is on screen */
  var hero = document.querySelector('.lp-hero-track');
  if (hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { doc.classList.toggle('is-live', en[0].isIntersecting); }).observe(hero);
  }

  /* ---- reveal once ---- */
  var reveal = [].slice.call(document.querySelectorAll('[data-reveal], .lp-phone'));
  if ('IntersectionObserver' in window && !still) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    reveal.forEach(function (el) { io.observe(el); });
  } else {
    reveal.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- nav: solid once off the top, hides going down, returns going up ---- */
  var nav = document.querySelector('[data-nav]');
  var lastY = scrollY;
  var navQueued = false;
  function navFrame() {
    navQueued = false;
    var y = scrollY;
    nav.classList.toggle('is-solid', y > 40);
    if (!menuOpen) nav.classList.toggle('is-hidden', y > 300 && y > lastY + 4);
    if (Math.abs(y - lastY) > 4) lastY = y;
  }
  addEventListener('scroll', function () { if (!navQueued) { navQueued = true; requestAnimationFrame(navFrame); } }, { passive: true });

  /* ---- mobile menu ---- */
  var burger = document.querySelector('.lp-burger');
  var menu = document.getElementById('lp-menu');
  var menuOpen = false;
  function setMenu(open) {
    menuOpen = open;
    burger.setAttribute('aria-expanded', String(open));
    if (open) { menu.hidden = false; requestAnimationFrame(function () { menu.classList.add('is-open'); }); }
    else { menu.classList.remove('is-open'); setTimeout(function () { if (!menuOpen) menu.hidden = true; }, 700); }
    nav.classList.remove('is-hidden');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!menuOpen); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && menuOpen) { setMenu(false); burger.focus(); } });
  }

  measure();
  live = new Set(tracks.filter(function (el) { var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < vh; }));
  queue();
})();
