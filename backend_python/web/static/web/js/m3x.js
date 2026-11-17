/* m3x.js: behaviour shared by the landing page and the app. No dependencies, ~4 KB.

   - [data-reveal]   springs in once when scrolled into view (siblings in [data-stagger] get --i)
   - [data-live]     .is-live while on screen, so looping animations pause off screen
   - [data-m3-nav]   pill nav with one sliding indicator (.m3-ind)
        data-spy     the current link follows the section being read (links are #hash anchors)

   Pill nav rules, each one a bug the first version had:
   1. First placement never slides in from x=0: position, show, then enable the transition.
   2. Re-measured on resize, on web-font load and on layout change, with the transition off.
   3. Hover only counts for a real mouse; touch and pen never leave a sticky hover.
   4. Leaving the bar waits 140 ms, so crossing the gap between two links does not bounce the pill home.
   5. Keyboard focus moves the pill (and tab order is untouched); blur returns it.
   6. Clicking an anchor locks the spy until the scroll settles, so the pill does not flicker through
      every section on the way.
   7. At the very top of the page nothing is current; at the very bottom the last section is. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;
  var all = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };

  /* ---- reveal once ---- */
  all('[data-stagger]').forEach(function (group) {
    [].slice.call(group.children).forEach(function (kid, i) {
      if (!kid.style.getPropertyValue('--i')) kid.style.setProperty('--i', Math.min(i, 8));
      if (!kid.hasAttribute('data-reveal')) kid.setAttribute('data-reveal', '');
    });
  });
  var reveal = all('[data-reveal], .foot-word');
  if (canObserve && !still) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
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

  /* ---- pill nav ---- */
  function pill(bar) {
    var links = [].slice.call(bar.children).filter(function (n) { return n.tagName === 'A'; });
    if (!links.length) return;
    var ind = bar.querySelector('.m3-ind');
    if (!ind) { ind = document.createElement('span'); ind.className = 'm3-ind'; ind.setAttribute('aria-hidden', 'true'); bar.insertBefore(ind, bar.firstChild); }
    var spy = bar.hasAttribute('data-spy');
    var current = links.filter(function (a) { return a.hasAttribute('aria-current') || a.classList.contains('md-nav-active'); })[0] || null;
    var target = null, leaveTimer = 0, hovering = false;

    function put(link) {
      ind.style.setProperty('--x', link.offsetLeft + 'px');
      ind.style.setProperty('--w', link.offsetWidth + 'px');
    }
    function mark(link) {
      target = link;
      links.forEach(function (a) { a.classList.toggle('is-target', a === link); });
    }
    function go(link) {
      mark(link);
      if (!link) { ind.classList.remove('on'); return; }
      if (!ind.classList.contains('on')) {          // appearing: do not slide in from elsewhere
        ind.classList.remove('anim');
        put(link);
        ind.classList.add('on');
        void ind.offsetWidth;
        if (!still) ind.classList.add('anim');
      } else { put(link); }
    }
    function remeasure() {                           // layout moved under us: snap, do not glide
      if (!target) return;
      var had = ind.classList.contains('anim');
      ind.classList.remove('anim');
      put(target);
      void ind.offsetWidth;
      if (had && !still) ind.classList.add('anim');
    }
    function setCurrent(link) {
      if (link === current) return;
      current = link;
      links.forEach(function (a) { if (a === link) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      if (!hovering) go(current);
    }
    function home() { hovering = false; go(current); }

    links.forEach(function (a) {
      a.addEventListener('pointerenter', function (e) {
        if (e.pointerType !== 'mouse') return;
        clearTimeout(leaveTimer); hovering = true; go(a);
      });
      a.addEventListener('focus', function () {
        if (!a.matches(':focus-visible')) return;
        clearTimeout(leaveTimer); hovering = true; go(a);
      });
      a.addEventListener('blur', function () { leaveTimer = setTimeout(home, 140); });
    });
    bar.addEventListener('pointerleave', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse') return;
      clearTimeout(leaveTimer); leaveTimer = setTimeout(home, 140);
    });
    bar.addEventListener('pointerenter', function () { clearTimeout(leaveTimer); });

    go(current);
    if ('ResizeObserver' in window) {
      var ro = new ResizeObserver(remeasure);
      ro.observe(bar);
      links.forEach(function (a) { ro.observe(a); });
    } else { addEventListener('resize', remeasure); }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);
    addEventListener('load', remeasure);

    if (!spy) return;
    var sections = links.map(function (a) { return document.getElementById((a.getAttribute('href') || '').slice(1)); });
    var locked = false, lockTimer = 0, ticking = false;
    function unlock() { locked = false; clearTimeout(lockTimer); onScroll(); }
    function onScroll() {
      if (locked || ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        var line = innerHeight * 0.4, best = null;
        var atEnd = innerHeight + scrollY >= doc.scrollHeight - 6;
        sections.forEach(function (s, i) {
          if (s && s.getBoundingClientRect().top <= line) best = links[i];
        });
        if (atEnd) { for (var i = sections.length - 1; i >= 0; i--) { if (sections[i]) { best = links[i]; break; } } }
        setCurrent(best);                            // null above the first section: nothing is current
      });
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function () {
        if (!sections[i]) return;
        locked = true; setCurrent(a); go(a);
        clearTimeout(lockTimer); lockTimer = setTimeout(unlock, 1400);
      });
    });
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('scrollend', function () { if (locked) unlock(); });
    addEventListener('wheel', function () { if (locked) unlock(); }, { passive: true });
    addEventListener('touchstart', function () { if (locked) unlock(); }, { passive: true });
    onScroll();
  }
  all('[data-m3-nav]').forEach(pill);

  /* ---- theme: one controller for the landing page and the app ----
     [data-theme-toggle] buttons call NebTheme.toggle. The change is a circular reveal from the
     button (View Transitions); without them, or with reduced motion, it just swaps. The choice
     is stored under localStorage "theme", the same key the head script reads, and posted to
     /ajax/theme/ when the app is around (CSRF_TOKEN exists), so it follows the reader everywhere. */
  var themeBtns = all('[data-theme-toggle]');
  function paintTheme(t) {
    doc.setAttribute('data-theme', t);
    themeBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
      b.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    });
    var m = document.querySelector('meta[name=theme-color]');
    if (m) m.content = t === 'dark' ? '#121318' : '#f6f8ff';
    document.dispatchEvent(new CustomEvent('neb:theme-change'));
  }
  function setTheme(next, origin) {
    try { localStorage.setItem('theme', next); } catch (e) {}
    if (typeof CSRF_TOKEN !== 'undefined') {
      try {
        fetch('/ajax/theme/', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }, body: JSON.stringify({ theme: next }) });
      } catch (e) {}
    }
    if (!document.startViewTransition || still || !origin) { paintTheme(next); return; }
    var r = origin.getBoundingClientRect();
    var x = r.left + r.width / 2, y = r.top + r.height / 2;
    var end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    doc.classList.add('theming');
    var vt = document.startViewTransition(function () { paintTheme(next); });
    vt.ready.then(function () {
      doc.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + end + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 750, easing: 'cubic-bezier(.2,.8,.2,1)', pseudoElement: '::view-transition-new(root)' });
    }).catch(function () {});
    vt.finished.then(function () { doc.classList.remove('theming'); }, function () { doc.classList.remove('theming'); });
  }
  window.NebTheme = {
    get: function () { return doc.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; },
    set: setTheme,
    toggle: function (origin) { setTheme(window.NebTheme.get() === 'dark' ? 'light' : 'dark', origin); }
  };
  paintTheme(window.NebTheme.get());
  themeBtns.forEach(function (b) { b.addEventListener('click', function () { window.NebTheme.toggle(b); }); });

  doc.classList.add('m3-ready');
})();
