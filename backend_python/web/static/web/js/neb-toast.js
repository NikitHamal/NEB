/* Toasts. One stack for every message the app shows: window.showSnackbar(msg[, ms | opts]) keeps working for the
   250 existing call sites, NebToast adds tone, an action and dismissal.

     NebToast.show('Reply posted', { tone: 'success', duration: 3600, action: { label: 'View', onClick: fn } })

   The tone is read from the words when it is not given, so "Failed to delete." is an error without a call site
   changing. A repeat of a message already on screen pulses it instead of stacking a copy. At most three show at
   once; the oldest leaves first. Hover or focus pauses the countdown, a sideways swipe or the close button dismisses. */
(function () {
  'use strict';

  var MAX = 3;
  var ICONS = { success: 'check_circle', error: 'error', warn: 'warning', info: 'info' };
  var live = [];

  function toneOf(msg) {
    var m = String(msg).toLowerCase();
    if (/\b(fail|failed|error|could not|couldn't|cannot|can't|unable|invalid|denied|went wrong|not allowed|not available)\b/.test(m)) return 'error';
    if (/\b(maximum|required|too (large|long|big|many)|at least|only)\b/.test(m)) return 'warn';
    if (/\b(deleted|removed|copied|saved|posted|marked|submitted|updated|sent|archived|following|followed|published|added|created|reported|thank|done)\b/.test(m)) return 'success';
    return 'info';
  }

  function root() {
    var c = document.getElementById('snackbar-container');
    if (!c) {
      c = document.createElement('div');
      c.id = 'snackbar-container';
      c.setAttribute('role', 'status');
      c.setAttribute('aria-live', 'polite');
      document.body.appendChild(c);
    }
    return c;
  }

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }

  function dismiss(t) {
    if (t.gone) return;
    t.gone = true;
    clearTimeout(t.timer);
    live = live.filter(function (x) { return x !== t; });
    t.slot.classList.add('is-leaving');
    var done = function () { if (t.slot.parentNode) t.slot.remove(); };
    t.slot.addEventListener('transitionend', function (e) { if (e.target === t.slot) done(); });
    setTimeout(done, 700);
  }

  function arm(t, ms) {
    clearTimeout(t.timer);
    t.left = ms;
    t.started = Date.now();
    t.timer = setTimeout(function () { dismiss(t); }, ms);
  }

  function pause(t) {
    if (t.gone || t.paused) return;
    t.paused = true;
    clearTimeout(t.timer);
    t.left = Math.max(800, t.left - (Date.now() - t.started));
  }

  function resume(t) {
    if (t.gone || !t.paused) return;
    t.paused = false;
    t.started = Date.now();
    t.timer = setTimeout(function () { dismiss(t); }, t.left);
  }

  function swipe(t) {
    var x0 = null, dx = 0;
    t.toast.addEventListener('pointerdown', function (e) {
      if (e.target.closest('button')) return;
      x0 = e.clientX; dx = 0;
      t.toast.setPointerCapture(e.pointerId);
      t.toast.classList.add('is-dragging');
    });
    t.toast.addEventListener('pointermove', function (e) {
      if (x0 == null) return;
      dx = e.clientX - x0;
      t.toast.style.transform = 'translateX(' + dx + 'px)';
      t.toast.style.opacity = String(Math.max(.2, 1 - Math.abs(dx) / 260));
    });
    function end() {
      if (x0 == null) return;
      x0 = null;
      t.toast.classList.remove('is-dragging');
      if (Math.abs(dx) > 80) {
        t.toast.style.transform = 'translateX(' + (dx > 0 ? 120 : -120) + '%)';
        t.toast.style.opacity = '0';
        dismiss(t);
      } else {
        t.toast.style.transform = '';
        t.toast.style.opacity = '';
      }
    }
    t.toast.addEventListener('pointerup', end);
    t.toast.addEventListener('pointercancel', end);
  }

  function show(msg, opts) {
    if (msg == null || msg === '') return null;
    if (typeof opts === 'number') opts = { duration: opts };
    opts = opts || {};
    msg = String(msg);
    var ms = opts.duration || (opts.action ? 6000 : Math.min(7000, 3200 + msg.length * 28));

    for (var i = 0; i < live.length; i++) {
      if (live[i].msg === msg) {
        var again = live[i];
        again.toast.classList.remove('is-bump');
        void again.toast.offsetWidth;
        again.toast.classList.add('is-bump');
        arm(again, ms);
        return again;
      }
    }
    while (live.length >= MAX) dismiss(live[0]);

    var tone = opts.tone || toneOf(msg);
    var t = { msg: msg, tone: tone };
    t.slot = el('div', 'neb-toast-slot');
    var fit = el('div', 'neb-toast-fit');
    t.toast = el('div', 'neb-toast');
    t.toast.setAttribute('data-tone', tone);
    t.toast.setAttribute('role', tone === 'error' ? 'alert' : 'status');
    t.toast.innerHTML =
      '<span class="neb-toast-icon" aria-hidden="true"><span class="material-symbols-outlined">' + (opts.icon || ICONS[tone]) + '</span></span>' +
      '<span class="neb-toast-msg">' + esc(msg) + '</span>';
    if (opts.action && opts.action.label) {
      var a = el('button', 'neb-toast-action');
      a.type = 'button';
      a.textContent = opts.action.label;
      a.addEventListener('click', function () {
        try { if (opts.action.onClick) opts.action.onClick(); } finally { dismiss(t); }
      });
      t.toast.appendChild(a);
    }
    var x = el('button', 'neb-toast-x', '<span class="material-symbols-outlined" aria-hidden="true">close</span>');
    x.type = 'button';
    x.setAttribute('aria-label', 'Dismiss');
    x.addEventListener('click', function () { dismiss(t); });
    t.toast.appendChild(x);
    fit.appendChild(t.toast);
    t.slot.appendChild(fit);
    root().appendChild(t.slot);
    live.push(t);

    t.toast.addEventListener('pointerenter', function () { pause(t); });
    t.toast.addEventListener('pointerleave', function () { resume(t); });
    t.toast.addEventListener('focusin', function () { pause(t); });
    t.toast.addEventListener('focusout', function () { resume(t); });
    swipe(t);
    arm(t, ms);
    return t;
  }

  window.NebToast = {
    show: show,
    success: function (m, o) { return show(m, Object.assign({ tone: 'success' }, o)); },
    error: function (m, o) { return show(m, Object.assign({ tone: 'error' }, o)); },
    info: function (m, o) { return show(m, Object.assign({ tone: 'info' }, o)); },
    clear: function () { live.slice().forEach(dismiss); }
  };
  window.showSnackbar = function (msg, opts) { return show(msg, opts); };
})();

/* One place that flips a Follow button, so the class, the label and the tone never disagree. */
window.nebFollowSet = function (btn, on) {
  if (!btn) return;
  btn.classList.remove('following', 'not-following');
  btn.classList.add(on ? 'following' : 'not-following');
  btn.textContent = on ? 'Following' : 'Follow';
  btn.setAttribute('aria-pressed', on ? 'true' : 'false');
};
