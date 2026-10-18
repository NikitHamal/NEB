/* Pixel Neby on the web. Replaces the 3D avatar (neby-avatar.js, kept in the
   repo for later) everywhere Neby the mascot appears: any [data-neby-avatar]
   element becomes a pixel Neby playing its data-animation state.

   - The hero (data-hero="true") is interactive: a tap plays the next
     reaction, the profile's mood pills ([data-neby-react]) play a named one,
     and an idle hero comes alive now and then (looks around, waves, hops).
   - Old 3D animation names map onto the pixel states, so no template changes.
   - window.NebyAvatar keeps its old shape (initAll, init, mount) for htmx
     swaps and the canvas. */
(function (window, document) {
  'use strict';

  var STATES = ['idle', 'still', 'blink', 'hop', 'think', 'sleep', 'wink', 'talk', 'love', 'surprised', 'sad',
    'laugh', 'dizzy', 'wave', 'success', 'oops', 'read', 'listen', 'celebrate', 'cool', 'kiss', 'look-around'];
  var ALIASES = {
    happy: 'hop', joy: 'hop', jump: 'hop', delight: 'hop', agree: 'success', proud: 'cool', thinking: 'think',
    typing: 'think', loading: 'think', puzzled: 'think', focus: 'think', sleepy: 'sleep', speaking: 'talk',
    responding: 'talk', heart: 'love', gasp: 'surprised', wow: 'surprised', notification: 'surprised',
    disagree: 'sad', concern: 'sad', 'sad-deep': 'sad', laughing: 'laugh', lol: 'laugh', smug: 'laugh',
    confused: 'dizzy', error: 'oops', panic: 'oops', shy: 'kiss', hello: 'wave', hi: 'wave', greet: 'wave',
    'intro-pop': 'wave', done: 'success', reading: 'read', study: 'read', listening: 'listen', dance: 'celebrate',
    party: 'celebrate', confetti: 'celebrate', sunglasses: 'cool', look: 'look-around', 'side-eye': 'look-around',
    'idle-front': 'idle', 'static': 'still', none: 'still'
  };
  var TAP_REACTIONS = ['hop', 'wink', 'love', 'laugh', 'surprised', 'cool', 'kiss', 'celebrate'];
  var AMBIENT = ['look-around', 'wave', 'blink', 'hop'];
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resolve(name) {
    var s = String(name || 'idle').toLowerCase().replace(/_/g, '-');
    if (STATES.indexOf(s) >= 0) return s;
    if (ALIASES[s]) return ALIASES[s];
    if (s.indexOf('talk') === 0) return 'talk';
    if (s.indexOf('idle') === 0) return 'idle';
    return 'idle';
  }

  function mount(el, opts) {
    if (el.__nebyInstance) return el.__nebyInstance;
    opts = opts || {};
    var base = resolve(opts.animation || el.getAttribute('data-animation'));
    var hero = opts.hero != null ? opts.hero : (el.getAttribute('data-hero') === 'true' || el.classList.contains('neby-avatar-hero'));
    var timer = 0, ambientTimer = 0, taps = 0;

    el.classList.add('neby-px');
    el.textContent = '';
    el.appendChild(document.createElement('i'));
    el.setAttribute('data-neby-initialized', 'true');
    if (!el.hasAttribute('role')) el.setAttribute('role', 'img');
    if (!el.hasAttribute('aria-label')) el.setAttribute('aria-label', 'Neby');
    if (el.title && /3D/.test(el.title)) el.title = 'Neby — tap to play';

    function show(state) { el.setAttribute('data-state', state); }

    // a reaction plays about twice through, then Neby settles back
    function react(name) {
      var s = resolve(name);
      clearTimeout(timer);
      show(s);
      timer = setTimeout(function () { show(base); scheduleAmbient(); }, 1900);
      return s;
    }

    function scheduleAmbient() {
      clearTimeout(ambientTimer);
      if (!hero || reduced || base !== 'idle') return;
      ambientTimer = setTimeout(function () {
        if (!el.isConnected) return;
        if (el.getAttribute('data-state') === 'idle' && !document.hidden) {
          show(AMBIENT[Math.floor(Math.random() * AMBIENT.length)]);
          timer = setTimeout(function () { show(base); scheduleAmbient(); }, 1400);
        } else scheduleAmbient();
      }, 7000 + Math.random() * 7000);
    }

    if (hero) {
      el.setAttribute('data-interactive', '');
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      var tap = function () { react(TAP_REACTIONS[taps++ % TAP_REACTIONS.length]); };
      el.addEventListener('click', tap);
      el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tap(); } });
      // say hello the first time the hero appears
      if (!reduced && base === 'idle') react('wave'); else show(base);
    } else {
      show(base);
    }
    scheduleAmbient();

    var instance = {
      el: el,
      react: react,
      setAnimation: function (name) { base = resolve(name); show(base); scheduleAmbient(); },
      play: function (name) { return react(name); },
      destroy: function () { clearTimeout(timer); clearTimeout(ambientTimer); }
    };
    el.__nebyInstance = instance;
    return instance;
  }

  function initAll(root) {
    (root || document).querySelectorAll('[data-neby-avatar]:not([data-neby-initialized])').forEach(function (el) { mount(el); });
  }

  // the profile's mood pills
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-neby-react]');
    if (!btn) return;
    var id = btn.getAttribute('data-neby-target') || 'profilePageNebyAvatar';
    var target = document.getElementById(id) || document.querySelector('[data-neby-avatar][data-hero="true"]') || document.querySelector('[data-neby-avatar]');
    if (target) mount(target).react(btn.getAttribute('data-neby-react'));
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();

  window.NebyAvatar = { mount: mount, init: initAll, initAll: initAll, states: STATES.slice(), resolve: resolve };
})(window, document);
