/* The plus tool of the comment composer (partials/_comment_composer.html): a small popup of what can be added.
   An entry that picks a file sets the accepted types on the page's own hidden file input and presses the
   composer's own (hidden) attach button, so the page's upload code runs exactly as before. The poll entry
   carries its own data-action and is handled by poll-card.js. */
(function () {
  if (window.NebComposerPlus) return;
  window.NebComposerPlus = true;

  function setOpen(wrap, on) {
    wrap.classList.toggle('is-open', on);
    var btn = wrap.querySelector('[data-plus-toggle]');
    if (btn) btn.setAttribute('aria-expanded', on ? 'true' : 'false');
  }

  function closeAll(except) {
    document.querySelectorAll('[data-neb-plus].is-open').forEach(function (w) {
      if (w !== except) setOpen(w, false);
    });
  }

  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('[data-plus-toggle]');
    if (toggle) {
      var wrap = toggle.closest('[data-neb-plus]');
      var on = !wrap.classList.contains('is-open');
      closeAll(wrap);
      setOpen(wrap, on);
      return;
    }
    var pick = e.target.closest('[data-plus-pick]');
    if (pick) {
      var w = pick.closest('[data-neb-plus]');
      setOpen(w, false);
      var input = document.getElementById(w.dataset.plusInput || 'replyMediaInput');
      var proxy = w.querySelector('[data-plus-proxy]');
      if (input) input.accept = pick.dataset.plusPick;
      if (proxy) proxy.click();
      return;
    }
    var item = e.target.closest('.neb-plus-item');
    if (item) { setOpen(item.closest('[data-neb-plus]'), false); return; }
    closeAll(null);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll(null);
  });
})();
