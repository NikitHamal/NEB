/* v5 gallery: Library (lazy grid), detail dialog (copy, SVG, 2x PNG, avatar in clip shapes), view + theme switching. */
(function () {
  'use strict';
  var A = NebArtV5, $ = function (s) { return document.querySelector(s); }, cat = A.catalog(), G = window.G5 = { mode: 'light', kind: 'avatar', subj: '', q: '', shown: 0, list: [], listeners: [] };
  var el = { kinds: $('#kinds'), subs: $('#subs'), grid: $('#grid'), dlg: $('#dlg') }, PAGE = 48;
  G.byKind = function (k) { return cat.filter(function (i) { return i.kind === k; }); };
  G.html = function (it, mode) { return A.render(it, mode || G.mode); };
  G.card = function (it) { var b = document.createElement('button'); b.className = 'card'; b.innerHTML = '<span class="art">' + G.html(it) + '</span><span class="meta"><b>' + it.name + '</b><span class="s">' + it.id + ' / ' + it.subject + '</span></span>'; b.firstChild.style.aspectRatio = it.w + '/' + it.h; b.onclick = function () { G.open(it); }; return b; };
  function filter() { var q = G.q.toLowerCase(); G.list = cat.filter(function (i) { return i.kind === G.kind && (!G.subj || i.subj === G.subj) && (!q || (i.name + ' ' + i.subj + ' ' + i.palette + ' ' + i.id).toLowerCase().indexOf(q) > -1); }); }
  function more(reset) { if (reset) { el.grid.innerHTML = ''; G.shown = 0; filter(); var k = A.kinds[G.kind]; el.grid.style.setProperty('--min', (k.w / k.h > 2.2 ? 340 : k.w / k.h > 1.2 ? 280 : k.w === k.h ? (G.kind === 'avatar' ? 150 : 200) : 190) + 'px'); } var e = Math.min(G.list.length, G.shown + PAGE), i; for (i = G.shown; i < e; i++) el.grid.appendChild(G.card(G.list[i])); G.shown = e; $('#more').style.display = e < G.list.length ? '' : 'none'; $('#subcount').textContent = cat.length.toLocaleString() + ' pieces, ' + (cat.length * 2).toLocaleString() + ' Light and Dark SVGs. Showing ' + G.list.length + ' of ' + A.kinds[G.kind].label; }
  function chips(host, items, cur, fn) { host.innerHTML = ''; items.forEach(function (it) { var b = document.createElement('button'); b.className = 'chip'; b.textContent = it[1]; b.setAttribute('aria-pressed', it[0] === cur); b.onclick = function () { fn(it[0]); }; host.appendChild(b); }); }
  function rail() {
    chips(el.kinds, Object.keys(A.kinds).map(function (k) { return [k, A.kinds[k].label + ' ' + G.byKind(k).length]; }), G.kind, function (k) { G.kind = k; G.subj = ''; rail(); more(true); });
    var ss = {}; G.byKind(G.kind).forEach(function (i) { ss[i.subj] = 1; }); var names = Object.keys(ss);
    chips(el.subs, [['', 'All']].concat(names.map(function (n) { return [n, n]; })), G.subj, function (s) { G.subj = s; rail(); more(true); }); el.subs.style.display = names.length > 1 ? '' : 'none';
  }
  G.fileSvg = function (svg, name) { var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' })); a.download = name + '.svg'; a.click(); };
  G.filePng = function (svg, w, h, name, sc) { var im = new Image(); im.onload = function () { var c = document.createElement('canvas'); c.width = w * (sc || 2); c.height = h * (sc || 2); c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); c.toBlob(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = name + '.png'; a.click(); }); }; im.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg); };
  G.open = function (it) {
    var svg = G.html(it), other = G.html(it, G.mode === 'light' ? 'dark' : 'light'), shapes = '';
    if (it.kind === 'avatar') shapes = '<div class="shapes">' + ['50%', '30%', '50% 50% 14% 14%', '50% 0 50% 0', '22% 50% 22% 50%', '16%'].map(function (r) { return '<div style="border-radius:' + r + '">' + svg + '</div>'; }).join('') + '</div>';
    el.dlg.innerHTML = '<div class="dl"><div class="row"><div><b>' + it.name + '</b><div class="sub">' + it.id + ' / ' + it.subject + ' / ' + it.palette + ' / ' + it.w + 'x' + it.h + '</div></div><span class="grow"></span><button class="ib" id="x" aria-label="Close"><span class="ms">close</span></button></div><div class="big">' + svg + '</div>' + shapes + '<div class="row"><button class="btn" id="cp"><span class="ms">content_copy</span>Copy SVG</button><button class="btn t" id="sv"><span class="ms">download</span>SVG</button><button class="btn t" id="pn"><span class="ms">image</span>PNG 2x</button><button class="btn t" id="oth"><span class="ms">contrast</span>Show ' + (G.mode === 'light' ? 'Dark' : 'Light') + '</button></div></div>';
    $('#x').onclick = function () { el.dlg.close(); }; $('#cp').onclick = function () { navigator.clipboard.writeText(svg); this.lastChild.textContent = 'Copied'; };
    $('#sv').onclick = function () { G.fileSvg(svg, it.id + '-' + G.mode); }; $('#pn').onclick = function () { G.filePng(svg, it.w, it.h, it.id + '-' + G.mode, 2); };
    $('#oth').onclick = function () { el.dlg.querySelector('.big').innerHTML = el.dlg.querySelector('.big').innerHTML === svg ? other : svg; };
    el.dlg.showModal();
  };
  el.dlg.addEventListener('click', function (e) { if (e.target === el.dlg) el.dlg.close(); });
  $('#more').onclick = function () { more(false); };
  var t; $('#q').oninput = function () { clearTimeout(t); var v = this.value; t = setTimeout(function () { G.q = v; more(true); }, 160); };
  $('#shuf').onclick = function () { var l = G.byKind(G.kind).slice(), i, j, x; for (i = l.length - 1; i > 0; i--) { j = Math.floor(Math.random() * (i + 1)); x = l[i]; l[i] = l[j]; l[j] = x; } el.grid.innerHTML = ''; G.list = l.slice(0, 120); G.shown = 0; more(false); };
  $('#theme').onclick = function () { G.mode = G.mode === 'light' ? 'dark' : 'light'; document.documentElement.dataset.theme = G.mode; this.firstChild.textContent = G.mode === 'light' ? 'dark_mode' : 'light_mode'; more(true); G.listeners.forEach(function (f) { f(); }); };
  $('#views').onclick = function (e) { var b = e.target.closest('button'); if (!b) return; [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', x === b); }); ['library', 'inapp', 'studio'].forEach(function (v) { $('#' + v).hidden = v !== b.dataset.v; }); $('#q').parentNode.style.display = b.dataset.v === 'library' ? '' : 'none'; $('#shuf').style.display = b.dataset.v === 'library' ? '' : 'none'; G.listeners.forEach(function (f) { f(); }); };
  rail(); more(true);
})();
