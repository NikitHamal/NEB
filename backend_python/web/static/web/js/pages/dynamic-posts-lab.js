/* Dynamic posts lab: looks, patterns and decorations on a sample post, as a feed card and as a reading view.
   Flat colour only. The Android lab uses the same six looks, so what you pick here is what the app shows. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var SERIF = 'Georgia, "Times New Roman", serif', SANS = 'inherit', MONO = 'ui-monospace, "SFMono-Regular", Menlo, monospace';
  var LOOKS = [
    { id: 'paper', name: 'Paper', bg: '#FBF8F1', ink: '#2B2620', accent: '#B4532A', soft: '#EFE7D6', font: 'serif', pattern: 'lines', cap: true, bar: true, r: 28 },
    { id: 'ink', name: 'Ink', bg: '#15171A', ink: '#EDEBE6', accent: '#E9B949', soft: '#24272C', font: 'serif', pattern: 'rings', cap: true, bar: true, r: 28 },
    { id: 'garden', name: 'Garden', bg: '#EAF3E4', ink: '#1F3322', accent: '#2F7D46', soft: '#D3E6C9', font: 'sans', pattern: 'waves', cap: false, bar: true, r: 32 },
    { id: 'sunrise', name: 'Sunrise', bg: '#FFF0E0', ink: '#3A2414', accent: '#E2622B', soft: '#FFDDBA', font: 'sans', pattern: 'dots', cap: false, bar: false, r: 36 },
    { id: 'blueprint', name: 'Blueprint', bg: '#E6EEF7', ink: '#14283D', accent: '#1E5F9E', soft: '#CADBEC', font: 'mono', pattern: 'grid', cap: false, bar: true, r: 16 },
    { id: 'rose', name: 'Rose', bg: '#FBEAEC', ink: '#3A1D22', accent: '#C03A52', soft: '#F5CFD5', font: 'serif', pattern: 'dots', cap: true, bar: false, r: 32 },
    { id: 'default', name: 'Default', bg: '', ink: '', accent: '', soft: '', font: 'sans', pattern: 'none', cap: false, bar: true, r: 24 }
  ];
  var FONTS = { serif: SERIF, sans: SANS, mono: MONO };
  var PATTERNS = ['none', 'lines', 'dots', 'grid', 'waves', 'rings'];
  var SWATCHES = ['#B4532A', '#E9B949', '#2F7D46', '#E2622B', '#1E5F9E', '#C03A52', '#6B4E9B', '#0F7B7B'];
  var TITLE = 'How I stopped dreading Maths in Class 10';
  var BODY = 'Last year I could not finish a paper in time. Then I changed three small things, and the marks followed. Here is the plan I wish someone had handed me.';
  var QUOTE = 'Do one chapter badly before you do one chapter perfectly.';
  var STEPS = ['Solve the last five years of papers', 'Keep a mistakes notebook', 'Teach one friend each Sunday'];
  var cur = null, view = 'feed';
  var stage = $('dp-stage'), look = LOOKS[0];

  function h(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; }
  function btn(label, on, fn, dot) {
    var b = h('button', 'dp-chip'); b.type = 'button'; b.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (dot) { var d = h('i', 'dp-dot'); d.style.background = dot; b.appendChild(d); }
    b.appendChild(document.createTextNode(label)); b.addEventListener('click', fn); return b;
  }
  function art(p) {
    if (p === 'none') return '';
    var body = {
      lines: '<path d="M0 14H80M0 34H80M0 54H80" stroke="currentColor" stroke-width="1.5" fill="none"/>',
      dots: '<circle cx="10" cy="10" r="3.2" fill="currentColor"/><circle cx="50" cy="40" r="3.2" fill="currentColor"/>',
      grid: '<path d="M0 0H40V40" stroke="currentColor" stroke-width="1" fill="none"/>',
      waves: '<path d="M0 20Q20 0 40 20T80 20" stroke="currentColor" stroke-width="2" fill="none"/>',
      rings: '<circle cx="40" cy="40" r="14" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="40" cy="40" r="30" stroke="currentColor" stroke-width="1.5" fill="none"/>'
    }[p];
    var size = p === 'grid' ? 40 : 80;
    return '<svg class="dp-art" aria-hidden="true" width="100%" height="100%"><defs><pattern id="dp-p-' + p + '" width="' + size + '" height="' + (p === 'dots' ? 60 : size) + '" patternUnits="userSpaceOnUse">' + body + '</pattern></defs><rect width="100%" height="100%" fill="url(#dp-p-' + p + ')"/></svg>';
  }
  function apply() {
    var s = stage.style, l = cur;
    ['bg', 'ink', 'accent', 'soft'].forEach(function (k) { if (l[k]) s.setProperty('--dp-' + k, l[k]); else s.removeProperty('--dp-' + k); });
    s.setProperty('--dp-font', FONTS[l.font]); s.setProperty('--dp-r', l.r + 'px');
    stage.dataset.cap = l.cap ? '1' : '0'; stage.dataset.bar = l.bar ? '1' : '0'; stage.dataset.default = l.id === 'default' ? '1' : '0';
    var card = h('article', 'dp-card dp-card--' + view);
    var cover = h('div', 'dp-cover'); cover.innerHTML = art(l.pattern);
    var chip = h('span', 'dp-tag', 'Study tips'); cover.appendChild(chip);
    var body = h('div', 'dp-body');
    var by = h('div', 'dp-by'); by.appendChild(h('span', 'dp-av', 'A')); by.appendChild(h('span', 'dp-name', 'Anita Gurung')); by.appendChild(h('span', 'dp-time', '2h'));
    body.appendChild(by);
    body.appendChild(h('h2', 'dp-title', TITLE));
    var p = h('p', 'dp-text', BODY); body.appendChild(p);
    if (view === 'read') {
      body.appendChild(h('blockquote', 'dp-quote', QUOTE));
      var ol = h('ol', 'dp-steps'); STEPS.forEach(function (t) { ol.appendChild(h('li', '', t)); }); body.appendChild(ol);
      body.appendChild(h('p', 'dp-text', 'None of this is clever. It is repetition with a little honesty, and it works because you can see progress every week.'));
    }
    var foot = h('div', 'dp-foot'); ['favorite 128', 'chat_bubble 24', 'bookmark Save'].forEach(function (x) {
      var parts = x.split(' '); var s2 = h('span', 'dp-act'); s2.appendChild(h('span', 'material-symbols-outlined', parts[0])); s2.appendChild(document.createTextNode(parts.slice(1).join(' '))); foot.appendChild(s2);
    });
    body.appendChild(foot); card.appendChild(cover); card.appendChild(body);
    var host = $('dp-preview'); host.textContent = ''; host.appendChild(card);
    card.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: 'cubic-bezier(.2,1,.3,1)' });
  }
  function controls() {
    var a = $('dp-looks'); a.textContent = '';
    LOOKS.forEach(function (l) { a.appendChild(btn(l.name, look === l, function () { look = l; cur = Object.assign({}, l); controls(); apply(); }, l.accent || null)); });
    var v = $('dp-view'); v.textContent = '';
    v.appendChild(btn('Feed card', view === 'feed', function () { view = 'feed'; controls(); apply(); }));
    v.appendChild(btn('Reading', view === 'read', function () { view = 'read'; controls(); apply(); }));
    var c = $('dp-custom'); c.textContent = '';
    var off = cur.id === 'default';
    function row(label, items) { var r = h('div', 'dp-row'); r.appendChild(h('span', 'dp-lab', label)); var w = h('div', 'dp-chips'); items.forEach(function (i) { w.appendChild(i); }); r.appendChild(w); c.appendChild(r); }
    row('Pattern', PATTERNS.map(function (p) { return btn(p, cur.pattern === p, function () { cur.pattern = p; controls(); apply(); }); }));
    row('Type', ['serif', 'sans', 'mono'].map(function (f) { return btn(f, cur.font === f, function () { cur.font = f; controls(); apply(); }); }));
    row('Corners', [12, 20, 28, 36].map(function (r) { return btn(String(r), cur.r === r, function () { cur.r = r; controls(); apply(); }); }));
    row('Extras', [btn('Drop cap', cur.cap, function () { cur.cap = !cur.cap; controls(); apply(); }), btn('Quote bar', cur.bar, function () { cur.bar = !cur.bar; controls(); apply(); })]);
    if (!off) row('Accent', SWATCHES.map(function (s) { return btn('', cur.accent.toLowerCase() === s.toLowerCase(), function () { cur.accent = s; cur.soft = mix(s, cur.bg); controls(); apply(); }, s); }));
  }
  function mix(a, b) {
    function p(x) { return [1, 3, 5].map(function (i) { return parseInt(x.substr(i, 2), 16); }); }
    var x = p(a), y = p(b); return '#' + x.map(function (v, i) { return ('0' + Math.round(v * .16 + y[i] * .84).toString(16)).slice(-2); }).join('');
  }
  cur = Object.assign({}, look); controls(); apply();
})();
