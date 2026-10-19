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
    nav.classList.remove('is-hidden'); nav.classList.toggle('is-menu', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!menuOpen); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && menuOpen) { setMenu(false); burger.focus(); } });
  }

  /* ---- nav: sliding pill under the hovered or current link, scroll progress ---- */
  var links = document.querySelector('.lp-links');
  var ind = links && links.querySelector('.lp-ind');
  var current = null;
  function pillTo(a) {
    if (!ind) return;
    if (!a) { ind.classList.remove('on'); return; }
    ind.style.width = a.offsetWidth + 'px';
    ind.style.transform = 'translateX(' + a.offsetLeft + 'px)';
    ind.classList.add('on');
  }
  if (links && ind) {
    links.addEventListener('pointerover', function (e) { var a = e.target.closest('a'); if (a) pillTo(a); });
    links.addEventListener('pointerleave', function () { pillTo(current); });
    links.addEventListener('focusin', function (e) { var a = e.target.closest('a'); if (a) pillTo(a); });
    var sections = [].slice.call(links.querySelectorAll('a[href^="#"]')).map(function (a) { return [a, document.querySelector(a.getAttribute('href'))]; }).filter(function (p) { return p[1]; });
    if ('IntersectionObserver' in window && sections.length) {
      var seen = new Map();
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { seen.set(en.target, en.isIntersecting); });
        var on = null;
        sections.forEach(function (p) { p[0].classList.remove('is-on'); if (!on && seen.get(p[1])) on = p[0]; });
        current = on; if (on) on.classList.add('is-on');
        if (!links.matches(':hover')) pillTo(current);
      }, { rootMargin: '-45% 0px -45% 0px' });
      sections.forEach(function (p) { spy.observe(p[1]); });
    }
  }
  var progQueued = false;
  function progress() {
    progQueued = false;
    var max = document.documentElement.scrollHeight - innerHeight;
    nav.style.setProperty('--sp', max > 0 ? Math.min(1, scrollY / max).toFixed(4) : 0);
  }
  addEventListener('scroll', function () { if (!progQueued) { progQueued = true; requestAnimationFrame(progress); } }, { passive: true });

  /* ---- menu: keep focus inside while open ---- */
  if (menu) {
    menu.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || !menuOpen) return;
      var f = [burger].concat([].slice.call(menu.querySelectorAll('a')));
      var i = f.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
    });
    burger && burger.addEventListener('keydown', function (e) {
      if (e.key === 'Tab' && menuOpen && !e.shiftKey) { var first = menu.querySelector('a'); if (first) { e.preventDefault(); first.focus(); } }
    });
  }

  /* ---- Neby on the wordmark: says hello, reacts, keeps out of the tab order ---- */
  var neby = document.querySelector('.lp-word .lp-neby');
  if (neby) {
    var say = document.createElement('span'); say.className = 'lp-neby-say';
    var lines = ['Namaste!', 'Need notes?', 'Ask me anything', 'Study mates!', 'Tap again'];
    var n = 0, sayT = 0;
    function speak(text, ms) { say.textContent = text; say.classList.add('on'); clearTimeout(sayT); sayT = setTimeout(function () { say.classList.remove('on'); }, ms || 1800); }
    neby.addEventListener('click', function () { speak(lines[n++ % lines.length]); });
    var settle = setInterval(function () {
      if (!neby.hasAttribute('data-neby-initialized')) return;
      clearInterval(settle);
      neby.setAttribute('tabindex', '-1'); neby.appendChild(say);
      if (!still) setTimeout(function () { speak('Namaste!', 2200); }, 1700);
    }, 120);
  }
  var peek = document.querySelector('.lp-peek');
  var openApp = document.querySelector('.lp-nav .lp-btn-sm');
  if (peek && openApp) openApp.addEventListener('pointerenter', function () { if (peek.__nebyInstance) peek.__nebyInstance.react('wave'); });

  /* festival decor pauses whenever it is off screen */
  if ('IntersectionObserver' in window) {
    var decorIo = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.parentElement.classList.toggle('is-paused', !e.isIntersecting); }); });
    document.querySelectorAll('.st-decor').forEach(function (d) { decorIo.observe(d); });
  }

  measure();
  live = new Set(tracks.filter(function (el) { var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < vh; }));
  queue();
})();
