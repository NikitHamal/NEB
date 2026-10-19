/* Pixel Neby on the web. Replaces the 3D avatar (neby-avatar.js, kept in the
   repo for later) everywhere Neby the mascot appears: any [data-neby-avatar]
   element becomes a pixel Neby playing its data-animation state.

   - Looks: Neby wears what the server says (<html data-neby-look>, an admin's
     pick or the festival's dress); an element can ask for its own with
     data-look. Strips live in img/neby/<look>/<state>.png, exported from the
     Android app's drawing code, so both apps show the same Neby.
   - Avatars (.neby-avatar-mini, or data-crop) show a centred head-and-
     shoulders crop in a circle; looks with hats get a taller window.
   - The hero (data-hero="true") is interactive: a tap plays the next
     reaction, [data-neby-react] buttons play a named one, and an idle hero
     comes alive now and then. It greets with the season's animation.
   - Old 3D animation names map onto the pixel states, so no template changes.
   - window.NebyAvatar keeps its old shape (initAll, init, mount) for htmx
     swaps and the canvas. */
(function (window, document) {
  'use strict';

  // state -> [frames, ms per frame]; keep in step with web/neby_looks.py
  var META = {
    'idle': [16, 115], 'still': [1, 1000], 'blink': [6, 110], 'look-around': [12, 130], 'think': [8, 160],
    'talk': [8, 95], 'listen': [8, 140], 'read': [14, 140], 'sleep': [12, 140], 'wave': [10, 110],
    'hop': [12, 72], 'wink': [10, 110], 'love': [12, 110], 'kiss': [12, 110], 'laugh': [10, 80],
    'cool': [10, 120], 'surprised': [10, 80], 'sad': [12, 130], 'dizzy': [12, 100], 'oops': [10, 100],
    'success': [12, 80], 'celebrate': [14, 85], 'tika': [24, 110], 'kite': [16, 130], 'swing': [16, 90],
    'diyo': [12, 110], 'deusi': [12, 95], 'splash': [16, 90], 'fireworks': [16, 100], 'namaste': [12, 120]
  };
  var LOOKS = ['classic', 'dashain', 'tihar', 'holi', 'teej', 'losar', 'new-year', 'christmas', 'monsoon', 'winter',
    'topi', 'graduate', 'astronaut', 'wizard', 'headphones', 'scientist', 'ninja', 'night', 'crown'];
  var HATS = { 'dashain': 1, 'losar': 1, 'new-year': 1, 'christmas': 1, 'monsoon': 1, 'winter': 1, 'topi': 1,
    'graduate': 1, 'astronaut': 1, 'wizard': 1, 'headphones': 1, 'night': 1, 'crown': 1 };
  var ALIASES = {
    happy: 'hop', joy: 'hop', jump: 'hop', delight: 'hop', agree: 'success', proud: 'cool', thinking: 'think',
    typing: 'think', loading: 'think', puzzled: 'think', focus: 'think', sleepy: 'sleep', speaking: 'talk',
    responding: 'talk', heart: 'love', gasp: 'surprised', wow: 'surprised', notification: 'surprised',
    disagree: 'sad', concern: 'sad', 'sad-deep': 'sad', laughing: 'laugh', lol: 'laugh', smug: 'laugh',
    confused: 'dizzy', error: 'oops', panic: 'oops', shy: 'kiss', hello: 'wave', hi: 'wave', greet: 'wave',
    'intro-pop': 'wave', done: 'success', reading: 'read', study: 'read', listening: 'listen', dance: 'deusi',
    party: 'celebrate', confetti: 'celebrate', sunglasses: 'cool', look: 'look-around', 'side-eye': 'look-around',
    'idle-front': 'idle', 'static': 'still', none: 'still', changa: 'kite', ping: 'swing', gulal: 'splash',
    diwali: 'diyo', deepawali: 'diyo', bhailo: 'deusi', blessing: 'tika', bow: 'namaste'
  };
  var TAP_REACTIONS = ['hop', 'wink', 'love', 'laugh', 'surprised', 'cool', 'kiss', 'celebrate'];
  var AMBIENT = ['look-around', 'wave', 'blink', 'hop'];
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;

  // img/neby/ sits next to js/, wherever static files are served from
  var BASE = (function () {
    var s = document.currentScript && document.currentScript.src;
    return s ? s.replace(/js\/neby-pixel\.js.*$/, 'img/neby/') : '/static/web/img/neby/';
  })();

  function resolve(name) {
    var s = String(name || 'idle').toLowerCase().replace(/_/g, '-');
    if (META[s]) return s;
    if (ALIASES[s]) return ALIASES[s];
    if (s.indexOf('talk') === 0) return 'talk';
    return 'idle';
  }
  function siteLook() { var l = root.getAttribute('data-neby-look'); return LOOKS.indexOf(l) >= 0 ? l : 'classic'; }
  function flag(name) { return root.getAttribute(name) !== 'false'; }

  function mount(el, opts) {
    if (el.__nebyInstance) return el.__nebyInstance;
    opts = opts || {};
    var base = resolve(opts.animation || el.getAttribute('data-animation'));
    var hero = opts.hero != null ? opts.hero : (el.getAttribute('data-hero') === 'true' || el.classList.contains('neby-avatar-hero'));
    var crop = el.hasAttribute('data-crop') ? el.getAttribute('data-crop') !== 'false' : el.classList.contains('neby-avatar-mini');
    var interactive = (hero || el.hasAttribute('data-interactive')) && flag('data-neby-reactions');
    var timer = 0, ambientTimer = 0, taps = 0;
    var sprite = document.createElement('i');

    el.classList.add('neby-px');
    if (crop) el.classList.add('neby-px--avatar');
    el.textContent = '';
    el.appendChild(sprite);
    el.setAttribute('data-neby-initialized', 'true');
    if (!el.hasAttribute('role')) el.setAttribute('role', 'img');
    if (!el.hasAttribute('aria-label')) el.setAttribute('aria-label', 'Neby');
    if (el.title && /3D/.test(el.title)) el.title = 'Neby — tap to play';

    function look() { var l = el.getAttribute('data-look'); return LOOKS.indexOf(l) >= 0 ? l : siteLook(); }

    function frame() {
      // the avatar window: 36 px around the body, or 42 px when a hat needs the headroom
      if (!crop) { sprite.style.cssText = sprite.style.cssText.replace(/(width|height|left|top):[^;]*;?/g, ''); return; }
      var hat = HATS[look()], w = hat ? 42 : 36, x = hat ? 3 : 6, y = hat ? 2 : 10;
      sprite.style.width = sprite.style.height = (4800 / w).toFixed(3) + '%';
      sprite.style.left = (-100 * x / w).toFixed(3) + '%';
      sprite.style.top = (-100 * y / w).toFixed(3) + '%';
    }

    function show(state) {
      var m = META[state] || META.idle;
      el.setAttribute('data-state', state);
      sprite.style.backgroundImage = 'url(' + BASE + look() + '/' + state + '.png)';
      sprite.style.setProperty('--n', m[0]);
      sprite.style.setProperty('--d', (m[0] * m[1]) + 'ms');
      // restart the strip from its first frame, so a reaction always plays from the top
      sprite.style.animation = 'none'; void sprite.offsetWidth; sprite.style.animation = '';
    }

    // a reaction plays through (twice for short ones), then Neby settles back
    function react(name) {
      var s = resolve(name), m = META[s];
      clearTimeout(timer);
      show(s);
      var len = m[0] * m[1];
      timer = setTimeout(function () { show(base); scheduleAmbient(); }, Math.max(1200, Math.min(len * 2, 2800)));
      return s;
    }

    function scheduleAmbient() {
      clearTimeout(ambientTimer);
      if (!hero || reduced || base !== 'idle' || !flag('data-neby-ambient')) return;
      ambientTimer = setTimeout(function () {
        if (!el.isConnected) return;
        if (el.getAttribute('data-state') === 'idle' && !document.hidden) {
          show(AMBIENT[Math.floor(Math.random() * AMBIENT.length)]);
          timer = setTimeout(function () { show(base); scheduleAmbient(); }, 1500);
        } else scheduleAmbient();
      }, 7000 + Math.random() * 7000);
    }

    frame();
    if (interactive) {
      el.setAttribute('data-interactive', '');
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      var tap = function () { react(TAP_REACTIONS[taps++ % TAP_REACTIONS.length]); };
      el.addEventListener('click', tap);
      el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tap(); } });
    }
    // the hero says hello: the season's own animation when there is one, else a wave
    if (hero && !reduced && base === 'idle') react(root.getAttribute('data-neby-greet') || 'wave');
    else show(base);
    scheduleAmbient();

    var instance = {
      el: el,
      react: react,
      play: react,
      setAnimation: function (name) { base = resolve(name); clearTimeout(timer); show(base); scheduleAmbient(); },
      setLook: function (l) { if (l) el.setAttribute('data-look', l); else el.removeAttribute('data-look'); frame(); show(el.getAttribute('data-state') || base); },
      destroy: function () { clearTimeout(timer); clearTimeout(ambientTimer); }
    };
    el.__nebyInstance = instance;
    return instance;
  }

  function initAll(scope) {
    (scope || document).querySelectorAll('[data-neby-avatar]:not([data-neby-initialized])').forEach(function (el) { mount(el); });
  }

  // mood buttons: the profile's pills, the admin studio's state chips
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-neby-react]');
    if (!btn) return;
    var id = btn.getAttribute('data-neby-target') || 'profilePageNebyAvatar';
    var target = document.getElementById(id) || document.querySelector('[data-neby-avatar][data-hero="true"]') || document.querySelector('[data-neby-avatar]');
    if (target) mount(target).react(btn.getAttribute('data-neby-react'));
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();

  window.NebyAvatar = { mount: mount, init: initAll, initAll: initAll, states: Object.keys(META), looks: LOOKS.slice(), resolve: resolve, base: BASE };
})(window, document);
