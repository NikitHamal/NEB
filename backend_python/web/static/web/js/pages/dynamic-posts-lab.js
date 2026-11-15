/* Dynamic posts lab: looks, covers and decorations on three sample posts, as a card, a reading page and a mixed feed.
   Flat colour only. Data in dynamic-posts-data.js mirrors the Android lab (ui/screens/lab). */
(function () {
  'use strict';
  var D = window.NebDP, $ = function (id) { return document.getElementById(id); };
  var FONTS = { serif: 'Georgia, "Times New Roman", serif', sans: 'inherit', mono: 'ui-monospace, "SFMono-Regular", Menlo, monospace' };
  var uid = 0, view = 'card', si = 0, base = D.LOOKS[0], cur = Object.assign({}, base), open = false;

  function h(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; }
  function btn(label, on, fn, dot) {
    var b = h('button', 'dp-chip'); b.type = 'button'; b.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (dot) { var d = h('i', 'dp-dot'); d.style.background = dot; b.appendChild(d); }
    if (label) b.appendChild(document.createTextNode(label));
    b.addEventListener('click', fn); return b;
  }
  function mix(a, b) {
    function p(x) { return [1, 3, 5].map(function (i) { return parseInt(x.substr(i, 2), 16); }); }
    var x = p(a), y = p(b); return '#' + x.map(function (v, i) { return ('0' + Math.round(v * .16 + y[i] * .84).toString(16)).slice(-2); }).join('');
  }
  function art(p) {
    if (p === 'none') return null;
    var id = 'dp-p' + (++uid), tile = {
      lines: [80, 16, '<path d="M0 12H80" stroke="currentColor" stroke-width="2" fill="none"/>'],
      dots: [26, 26, '<circle cx="13" cy="13" r="3.2" fill="currentColor"/>'],
      grid: [28, 28, '<path d="M0 .75H28M.75 0V28" stroke="currentColor" stroke-width="1.5" fill="none"/>'],
      waves: [60, 24, '<path d="M0 12Q15 0 30 12T60 12" stroke="currentColor" stroke-width="2.5" fill="none"/>'],
      stripes: [30, 30, '<rect width="9" height="30" fill="currentColor"/>', ' patternTransform="rotate(45)"'],
      confetti: [52, 52, '<rect x="6" y="8" width="14" height="5" rx="2.5" fill="currentColor" transform="rotate(30 13 10)"/><rect x="32" y="34" width="14" height="5" rx="2.5" fill="currentColor" transform="rotate(-40 39 36)"/>']
    }[p], inner;
    if (tile) inner = '<defs><pattern id="' + id + '" width="' + tile[0] + '" height="' + tile[1] + '" patternUnits="userSpaceOnUse"' + (tile[3] || '') + '>' + tile[2] + '</pattern></defs><rect width="100%" height="100%" fill="url(#' + id + ')"/>';
    else if (p === 'rings') inner = [1, 2, 3, 4, 5, 6].map(function (i) { return '<circle cx="86%" cy="20%" r="' + i * 26 + '" fill="none" stroke="currentColor" stroke-width="2.5"/>'; }).join('');
    else inner = '<circle cx="84%" cy="18%" r="70" fill="currentColor"/><circle cx="10%" cy="92%" r="42" fill="currentColor"/><rect x="42%" y="58%" width="60" height="60" rx="24" fill="currentColor"/>';
    var s = h('div', 'dp-art'); s.setAttribute('aria-hidden', 'true');
    s.innerHTML = '<svg width="100%" height="100%">' + inner + '</svg>'; return s;
  }
  function divider(l) {
    var d = h('div', 'dp-div'); d.dataset.d = l.divider;
    if (l.divider === 'dots') { d.appendChild(h('i')); d.appendChild(h('i')); d.appendChild(h('i')); }
    if (l.divider === 'wave') d.innerHTML = '<svg width="240" height="18" viewBox="0 0 240 18"><path d="M0 9' + 'q15 -9 30 0t30 0t30 0t30 0t30 0t30 0t30 0t30 0" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>';
    return d;
  }
  function lead(l, s, read) {
    var p = h('p', 'dp-text dp-lead'), i = s.lead.indexOf(s.mark);
    if (read && l.mark && i >= 0) {
      p.appendChild(document.createTextNode(s.lead.slice(0, i))); p.appendChild(h('mark', 'dp-mark', s.mark)); p.appendChild(document.createTextNode(s.lead.slice(i + s.mark.length)));
    } else p.textContent = s.lead;
    return p;
  }
  function card(l, s, read) {
    var c = h('article', 'dp-card dp-card--' + (read ? 'read' : 'feed')), st = c.style;
    if (l.id !== 'default') { st.setProperty('--dp-bg', l.bg); st.setProperty('--dp-ink', l.ink); st.setProperty('--dp-accent', l.accent); st.setProperty('--dp-soft', l.soft); }
    st.setProperty('--dp-font', FONTS[l.font]); st.setProperty('--dp-r', l.r + 'px');
    c.dataset.cap = l.cap ? '1' : '0'; c.dataset.bar = l.bar ? '1' : '0'; c.dataset.center = l.center ? '1' : '0'; c.dataset.tall = l.tall ? '1' : '0';
    var a = art(l.pattern), tag = h('span', 'dp-tag', s.tag);
    if (a) { var cv = h('div', 'dp-cover'); cv.appendChild(a); cv.appendChild(tag); c.appendChild(cv); } else tag.classList.add('dp-tag--soft');
    var b = h('div', 'dp-body'); if (!a) b.appendChild(tag);
    var by = h('div', 'dp-by'); by.appendChild(h('span', 'dp-av', s.author.charAt(0))); by.appendChild(h('span', 'dp-name', s.author)); by.appendChild(h('span', 'dp-time', read ? s.min + ' min read' : '2h'));
    b.appendChild(by); b.appendChild(h('h2', 'dp-title', s.title)); b.appendChild(lead(l, s, read));
    if (read) {
      var co = h('div', 'dp-callout'); co.appendChild(h('span', 'material-symbols-outlined', 'lightbulb')); co.appendChild(h('span', '', s.callout)); b.appendChild(co);
      var q = h('blockquote', 'dp-quote'); q.appendChild(h('span', 'material-symbols-outlined dp-qg', 'format_quote')); q.appendChild(h('p', '', s.quote)); b.appendChild(q);
      var ol = h('ol', 'dp-steps dp-list--' + s.kind);
      s.items.forEach(function (t, i) {
        var li = h('li'); if (s.kind === 'checks') { var k = h('button', 'dp-check'); k.type = 'button'; k.setAttribute('aria-pressed', 'false'); k.appendChild(h('i', 'material-symbols-outlined', 'check')); k.appendChild(h('span', '', t)); k.addEventListener('click', function () { k.setAttribute('aria-pressed', k.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); }); li.appendChild(k); } else { li.appendChild(h('b', '', String(i + 1))); li.appendChild(h('span', '', t)); }
        ol.appendChild(li);
      }); b.appendChild(ol); b.appendChild(divider(l)); b.appendChild(h('p', 'dp-text', s.outro));
    }
    var f = h('div', 'dp-foot'); [['favorite', '128'], ['chat_bubble', '24'], ['bookmark', 'Save']].forEach(function (x) {
      var sp = h('span', 'dp-act'); sp.appendChild(h('span', 'material-symbols-outlined', x[0])); sp.appendChild(document.createTextNode(x[1])); f.appendChild(sp);
    });
    b.appendChild(f); c.appendChild(b); return c;
  }
  function paint() {
    var host = $('dp-preview'); host.textContent = ''; host.className = view === 'mix' ? 'dp-mix' : '';
    if (view === 'mix') D.MIX.forEach(function (m) { host.appendChild(card(D.LOOKS.filter(function (l) { return l.id === m[1]; })[0], D.SAMPLES[m[0]], false)); });
    else host.appendChild(card(cur, D.SAMPLES[si], view === 'read'));
    var c = host.firstChild; if (c && c.animate) c.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: 'cubic-bezier(.2,1,.3,1)' });
  }
  function row(box, label, items) { var r = h('div', 'dp-row'); r.appendChild(h('span', 'dp-lab', label)); var w = h('div', 'dp-chips'); items.forEach(function (i) { w.appendChild(i); }); r.appendChild(w); box.appendChild(r); }
  function set(k, v) { cur[k] = v; controls(); paint(); }
  function controls() {
    var a = $('dp-looks'); a.textContent = ''; a.hidden = view === 'mix';
    D.LOOKS.forEach(function (l) { a.appendChild(btn(l.name, base === l, function () { base = l; cur = Object.assign({}, l); controls(); paint(); }, l.accent || null)); });
    var v = $('dp-view'); v.textContent = '';
    [['card', 'Card'], ['read', 'Reading'], ['mix', 'Mixed feed']].forEach(function (x) { v.appendChild(btn(x[1], view === x[0], function () { view = x[0]; controls(); paint(); })); });
    var sm = $('dp-sample'); sm.textContent = ''; sm.hidden = view === 'mix';
    D.SAMPLES.forEach(function (s, i) { sm.appendChild(btn(s.label, si === i, function () { si = i; controls(); paint(); })); });
    var tg = $('dp-toggle'); tg.textContent = ''; tg.hidden = view === 'mix';
    tg.appendChild(btn('Customise', open, function () { open = !open; controls(); }));
    tg.appendChild(btn('Reset', false, function () { cur = Object.assign({}, base); controls(); paint(); }));
    var c = $('dp-custom'); c.textContent = ''; c.hidden = view === 'mix' || !open;
    if (c.hidden) return;
    row(c, 'Cover', D.PATTERNS.map(function (p) { return btn(p, cur.pattern === p, function () { set('pattern', p); }); }));
    row(c, 'Type', ['serif', 'sans', 'mono'].map(function (f) { return btn(f, cur.font === f, function () { set('font', f); }); }));
    row(c, 'Corners', [12, 20, 28, 36].map(function (r) { return btn(String(r), cur.r === r, function () { set('r', r); }); }));
    row(c, 'Layout', [btn('Tall cover', cur.tall, function () { set('tall', !cur.tall); }), btn('Centred title', cur.center, function () { set('center', !cur.center); })]);
    row(c, 'Divider', ['line', 'dots', 'wave'].map(function (d) { return btn(d, cur.divider === d, function () { set('divider', d); }); }));
    row(c, 'Extras', [btn('Drop cap', cur.cap, function () { set('cap', !cur.cap); }), btn('Quote bar', cur.bar, function () { set('bar', !cur.bar); }), btn('Highlight', cur.mark, function () { set('mark', !cur.mark); })]);
    if (cur.id !== 'default') row(c, 'Accent', D.SWATCHES.map(function (s) { return btn('', cur.accent.toLowerCase() === s.toLowerCase(), function () { cur.accent = s; cur.soft = mix(s, cur.bg); controls(); paint(); }, s); }));
  }
  controls(); paint();
})();
