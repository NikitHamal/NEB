/* One-shot like feedback, delegated so it works on every surface without each
   page handler knowing about it. At click time .liked still describes the old
   state, which is how an unlike is told apart and left uncelebrated. */
(function () {
  'use strict';

  var PARTICLE_COUNT = 7;
  var BURST_MS = 500;

  function spawnBurst(btn) {
    var icon = btn.querySelector('.material-symbols-outlined') || btn.querySelector('svg');
    var buttonRect = btn.getBoundingClientRect();
    var targetRect = icon ? icon.getBoundingClientRect() : buttonRect;

    var old = btn.querySelector('.neb-like-burst');
    if (old) old.remove();

    var layer = document.createElement('span');
    layer.className = 'neb-like-burst';
    layer.setAttribute('aria-hidden', 'true');
    layer.style.left = (targetRect.left - buttonRect.left + targetRect.width / 2) + 'px';
    layer.style.top = (targetRect.top - buttonRect.top + targetRect.height / 2) + 'px';

    var halo = document.createElement('i');
    halo.className = 'neb-like-halo';
    layer.appendChild(halo);

    var ring = document.createElement('i');
    ring.className = 'neb-like-ring';
    layer.appendChild(ring);

    var angleStep = 360 / PARTICLE_COUNT;
    for (var i = 0; i < PARTICLE_COUNT; i++) {
      var dot = document.createElement('i');
      var isSoft = i % 2 !== 0;
      dot.className = isSoft ? 'neb-like-dot neb-like-dot-soft' : 'neb-like-dot';

      var angle = angleStep * i + (isSoft ? 10 : -4);
      var dist = isSoft ? 15 : 21;
      var size = isSoft ? 2.5 : 3.5;
      var delay = Math.round(i * 14);

      dot.style.setProperty('--a', angle.toFixed(1) + 'deg');
      dot.style.setProperty('--d', dist.toFixed(1) + 'px');
      dot.style.setProperty('--s', size.toFixed(1) + 'px');
      dot.style.setProperty('--t', delay + 'ms');
      layer.appendChild(dot);
    }

    btn.appendChild(layer);
    window.setTimeout(function () {
      layer.remove();
    }, BURST_MS);
  }

  document.addEventListener('click', function (event) {
    var btn = event.target.closest('[data-action*="like"]');
    if (!btn || btn.disabled || btn.classList.contains('liked')) return;

    btn.classList.remove('is-like-pop');
    void btn.offsetWidth;
    btn.classList.add('is-like-pop');
    spawnBurst(btn);

    window.setTimeout(function () {
      btn.classList.remove('is-like-pop');
    }, 480);
  }, true);
})();
