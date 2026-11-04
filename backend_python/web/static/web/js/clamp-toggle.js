/* Comments taller than their cap fold to the cap and get a "Show more" button;
   the fold is decided by measurement, not by markup, so a comment that fits
   never grows a button. Pages that render comments after load call
   NebClamp.refresh(root) over the new nodes. */
(function () {
  'use strict';

  var DEFAULT_MAX = 132;

  function toggleFor(el) {
    var next = el.nextElementSibling;
    return next && next.classList.contains('neb-clamp-toggle') ? next : null;
  }

  function label(el, btn) {
    var open = el.classList.contains('is-open');
    btn.textContent = open ? 'Show less' : 'Show more';
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  function apply(el) {
    var max = parseInt(el.getAttribute('data-clamp'), 10) || DEFAULT_MAX;
    var btn = toggleFor(el);
    if (el.scrollHeight <= max + 12) {
      el.classList.remove('is-clamped', 'is-open');
      if (btn) btn.remove();
      return;
    }
    el.style.setProperty('--clamp-height', max + 'px');
    if (!btn) {
      btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'neb-clamp-toggle';
      btn.addEventListener('click', function () {
        var stillClamped = el.classList.toggle('is-clamped');
        el.classList.toggle('is-open', !stillClamped);
        label(el, btn);
      });
      el.after(btn);
    }
    el.classList.toggle('is-clamped', !el.classList.contains('is-open'));
    label(el, btn);
  }

  function refresh(root) {
    (root || document).querySelectorAll('[data-clamp]').forEach(apply);
  }

  document.addEventListener('DOMContentLoaded', function () {
    refresh(document);
    var timer;
    window.addEventListener('resize', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { refresh(document); }, 180);
    });
  });

  /* "+N" on a tag row reveals the tags that did not fit the first three */
  document.addEventListener('click', function (e) {
    var more = e.target.closest && e.target.closest('[data-tags-more]');
    if (!more) return;
    var row = more.parentElement;
    row.querySelectorAll('.is-extra').forEach(function (t) { t.hidden = false; });
    more.remove();
  });

  window.NebClamp = { refresh: refresh };
})();
