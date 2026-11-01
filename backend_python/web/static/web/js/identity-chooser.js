/* The identity chooser: the avatar is the control, the menu picks between the
   account and its anonymous mask, and the checkbox inside is what the submit
   path already reads, so choosing an identity is only ever a write to that box.

   The menu opens below the field, unless the viewport has no room for it there
   -- a composer at the bottom of a page would otherwise drop its menu off the
   screen -- in which case it opens above. */
(function () {
  'use strict';

  function closeAll() {
    document.querySelectorAll('.fp-identity.is-open').forEach(function (open) {
      open.classList.remove('is-open', 'is-up');
      var t = open.querySelector('.fp-identity-trigger');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }

  function place(root) {
    var menu = root.querySelector('.fp-identity-menu');
    var field = root.closest('.neb-composer') || root;
    var rect = field.getBoundingClientRect();
    var needed = menu.offsetHeight + 16;
    var below = window.innerHeight - rect.bottom;
    root.classList.toggle('is-up', below < needed && rect.top > below);
  }

  function wire(root) {
    if (root.__wired) return;
    root.__wired = true;
    var trigger = root.querySelector('.fp-identity-trigger');
    var anonBox = root.querySelector('input[type="checkbox"]');
    if (!trigger || !anonBox) return;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var wasOpen = root.classList.contains('is-open');
      closeAll();
      if (!wasOpen) {
        root.classList.add('is-open');
        place(root);
        trigger.setAttribute('aria-expanded', 'true');
      }
    });
    root.querySelectorAll('.fp-identity-option').forEach(function (opt) {
      opt.addEventListener('click', function () {
        var anon = opt.getAttribute('data-identity') === '1';
        anonBox.checked = anon;
        root.classList.toggle('is-anon', anon);
        root.querySelectorAll('.fp-identity-option').forEach(function (other) {
          other.classList.toggle('is-active', other === opt);
        });
        closeAll();
        trigger.focus();
      });
    });
  }

  function boot() {
    document.querySelectorAll('.fp-identity').forEach(wire);
    document.addEventListener('click', function (e) {
      if (!e.target.closest || !e.target.closest('.fp-identity')) closeAll();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeAll();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
