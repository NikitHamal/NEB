(function () {
  'use strict';

  var root = document.documentElement;
  var body = document.body;
  var drawer = document.getElementById('adminDrawer');
  var hamburger = document.getElementById('hamburgerBtn');
  var mobileQuery = window.matchMedia('(max-width: 900px)');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var lastFocus = null;

  /* Drawer (modal below 900px, a fixed column above) */

  function setNav(open) {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    body.classList.toggle('admin-nav-open', open);
    if (hamburger) hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      lastFocus = document.activeElement;
      var current = drawer.querySelector('.admin-nav-item.active') || drawer.querySelector('a');
      if (current) current.focus({ preventScroll: true });
    } else if (lastFocus && lastFocus.focus) {
      lastFocus.focus({ preventScroll: true });
      lastFocus = null;
    }
  }

  function syncDrawerForViewport() {
    if (!drawer) return;
    if (mobileQuery.matches) {
      drawer.setAttribute('aria-modal', 'true');
      drawer.setAttribute('role', 'dialog');
      if (!drawer.classList.contains('open')) drawer.setAttribute('inert', '');
    } else {
      drawer.removeAttribute('aria-modal');
      drawer.removeAttribute('role');
      drawer.removeAttribute('inert');
      drawer.classList.remove('open');
      body.classList.remove('admin-nav-open');
    }
  }

  function openNav() {
    if (drawer) drawer.removeAttribute('inert');
    setNav(true);
  }

  function closeNav() {
    setNav(false);
    if (mobileQuery.matches && drawer) {
      window.setTimeout(function () {
        if (!drawer.classList.contains('open')) drawer.setAttribute('inert', '');
      }, 320);
    }
  }

  mobileQuery.addEventListener('change', syncDrawerForViewport);
  syncDrawerForViewport();

  if (drawer) {
    drawer.addEventListener('click', function (e) {
      if (mobileQuery.matches && e.target.closest('a')) closeNav();
    });
    var active = drawer.querySelector('.admin-nav-item.active');
    if (active && active.scrollIntoView) active.scrollIntoView({ block: 'center' });
  }

  /* Theme: a circular reveal from the button where View Transitions exist */

  function applyTheme(dark) {
    if (dark) root.setAttribute('data-theme', 'dark');
    else root.removeAttribute('data-theme');
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (err) { /* private mode */ }
    if (window.CSRF_TOKEN) {
      fetch('/ajax/theme/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': window.CSRF_TOKEN }
      }).catch(function () {});
    }
  }

  function toggleTheme(origin) {
    var dark = root.getAttribute('data-theme') !== 'dark';
    if (!document.startViewTransition || reduceMotion.matches) {
      body.classList.add('admin-theme-swap');
      applyTheme(dark);
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { body.classList.remove('admin-theme-swap'); });
      });
      return;
    }
    var rect = origin && origin.getBoundingClientRect();
    var x = rect ? rect.left + rect.width / 2 : window.innerWidth - 40;
    var y = rect ? rect.top + rect.height / 2 : 32;
    var r = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
    root.classList.add('admin-vt-theme');
    var t = document.startViewTransition(function () { applyTheme(dark); });
    t.ready.then(function () {
      root.animate(
        { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + r + 'px at ' + x + 'px ' + y + 'px)'] },
        { duration: 520, easing: 'cubic-bezier(0.2, 0, 0, 1)', pseudoElement: '::view-transition-new(root)' }
      );
    }).catch(function () {});
    t.finished.finally(function () { root.classList.remove('admin-vt-theme'); });
  }

  /* Snackbar */

  function showSnackbar(msg, duration) {
    var container = document.getElementById('snackbar-container') || body;
    var el = document.createElement('div');
    el.className = 'md-snackbar';
    el.textContent = msg;
    container.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('show'); });
    window.setTimeout(function () {
      el.classList.remove('show');
      window.setTimeout(function () { el.remove(); }, 260);
    }, duration || 3200);
  }

  /* Confirm dialog (replaces window.confirm) */

  var confirmDialog = document.getElementById('adminConfirm');
  var CONFIRM_ICONS = { danger: 'warning', primary: 'help' };

  function adminConfirm(opts) {
    opts = typeof opts === 'string' ? { message: opts } : (opts || {});
    if (!confirmDialog || !confirmDialog.showModal) {
      return Promise.resolve(window.confirm(opts.message || 'Are you sure?'));
    }
    var tone = opts.tone || 'primary';
    confirmDialog.dataset.tone = tone;
    document.getElementById('adminConfirmTitle').textContent = opts.title || 'Are you sure?';
    document.getElementById('adminConfirmText').textContent = opts.message || '';
    document.querySelector('#adminConfirmIcon .material-symbols-outlined').textContent = CONFIRM_ICONS[tone] || 'help';
    var ok = document.getElementById('adminConfirmOk');
    ok.textContent = opts.confirmLabel || 'Confirm';
    ok.className = 'md-btn ' + (tone === 'danger' ? 'md-btn-error' : 'md-btn-filled');
    return new Promise(function (resolve) {
      function done() {
        confirmDialog.removeEventListener('close', done);
        resolve(confirmDialog.returnValue === 'ok');
      }
      confirmDialog.returnValue = 'cancel';
      confirmDialog.addEventListener('close', done);
      confirmDialog.showModal();
      ok.focus();
    });
  }

  function confirmThen(el, run) {
    var danger = el.dataset.confirmTone !== 'primary';
    adminConfirm({
      title: el.dataset.confirmTitle || (danger ? 'Please confirm' : 'Are you sure?'),
      message: el.dataset.confirmMsg || 'Are you sure?',
      confirmLabel: el.dataset.confirmLabel || (danger ? 'Yes, continue' : 'Confirm'),
      tone: danger ? 'danger' : 'primary'
    }).then(function (yes) { if (yes) run(); });
  }

  /* Quick jump palette */

  var palette = document.getElementById('adminPalette');
  var paletteInput = document.getElementById('adminPaletteInput');
  var paletteList = document.getElementById('adminPaletteList');
  var paletteItems = [];
  var paletteIndex = 0;

  function collectPages() {
    if (!drawer) return [];
    return Array.prototype.map.call(drawer.querySelectorAll('.admin-nav a[data-nav]'), function (a) {
      var group = a.closest('.admin-nav-group');
      var label = group && group.querySelector('.admin-nav-group-label');
      return {
        href: a.getAttribute('href'),
        title: a.dataset.nav,
        group: label ? label.textContent : '',
        icon: a.querySelector('.material-symbols-outlined').textContent
      };
    });
  }

  function renderPalette() {
    var q = paletteInput.value.trim().toLowerCase();
    var pages = collectPages().filter(function (p) {
      return !q || (p.title + ' ' + p.group).toLowerCase().indexOf(q) !== -1;
    });
    paletteList.textContent = '';
    paletteItems = [];
    if (!pages.length) {
      var empty = document.createElement('div');
      empty.className = 'admin-palette-empty';
      empty.textContent = 'No matching page';
      paletteList.appendChild(empty);
      return;
    }
    pages.forEach(function (p, i) {
      var a = document.createElement('a');
      a.href = p.href;
      a.className = 'admin-palette-item';
      a.setAttribute('role', 'option');
      var icon = document.createElement('span');
      icon.className = 'material-symbols-outlined';
      icon.textContent = p.icon;
      var title = document.createElement('span');
      title.className = 'admin-palette-title';
      title.textContent = p.title;
      var group = document.createElement('span');
      group.className = 'admin-palette-group';
      group.textContent = p.group;
      a.appendChild(icon);
      a.appendChild(title);
      a.appendChild(group);
      a.addEventListener('mousemove', function () { setPaletteIndex(i); });
      paletteList.appendChild(a);
      paletteItems.push(a);
    });
    setPaletteIndex(0);
  }

  function setPaletteIndex(i) {
    if (!paletteItems.length) return;
    paletteIndex = (i + paletteItems.length) % paletteItems.length;
    paletteItems.forEach(function (el, n) {
      el.classList.toggle('is-active', n === paletteIndex);
      el.setAttribute('aria-selected', n === paletteIndex ? 'true' : 'false');
    });
    paletteItems[paletteIndex].scrollIntoView({ block: 'nearest' });
  }

  function openPalette() {
    if (!palette || !palette.showModal || palette.open) return;
    if (drawer && drawer.classList.contains('open')) closeNav();
    paletteInput.value = '';
    renderPalette();
    palette.showModal();
    paletteInput.focus();
  }

  if (palette) {
    paletteInput.addEventListener('input', renderPalette);
    paletteInput.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); setPaletteIndex(paletteIndex + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setPaletteIndex(paletteIndex - 1); }
      else if (e.key === 'Enter' && paletteItems[paletteIndex]) {
        e.preventDefault();
        window.location.href = paletteItems[paletteIndex].href;
      }
    });
    palette.addEventListener('click', function (e) {
      if (e.target === palette) palette.close();
    });
  }

  /* Wiring */

  window.CSRF_TOKEN = typeof CSRF_TOKEN !== 'undefined' ? CSRF_TOKEN : '';
  window.toggleTheme = toggleTheme;
  window.showSnackbar = showSnackbar;
  window.adminConfirm = adminConfirm;

  registerActions({
    'open-nav': function () { openNav(); },
    'close-nav': function () { closeNav(); },
    'toggle-theme': function (el) { toggleTheme(el); },
    'open-palette': function () { openPalette(); },
    'confirm-delete': function (form) {
      confirmThen(form, function () {
        form.removeAttribute('data-action');
        form.submit();
      });
    },
    'confirm-submit': function (el) {
      confirmThen(el, function () {
        var form = el.closest('form');
        if (!form) return;
        if (form.requestSubmit) form.requestSubmit(el);
        else form.submit();
      });
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) {
      closeNav();
      return;
    }
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || '')) || e.target.isContentEditable;
    if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      openPalette();
    } else if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      openPalette();
    }
  });

  var topbar = document.querySelector('.admin-topbar');
  if (topbar) {
    var stuck = function () { topbar.classList.toggle('is-stuck', window.scrollY > 4); };
    window.addEventListener('scroll', stuck, { passive: true });
    stuck();
  }
})();
