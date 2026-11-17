/* v3 gallery: Library (lazy batches), detail dialog (copy, SVG, 2x PNG) and Studio. In-app and compare live in v3-previews.js. */
(function () {
  'use strict';
  var A = window.NebArtV3, cat = A.catalog(), $ = function (s) { return document.querySelector(s); };
  var st = { view: 'library', kind: 'all', q: '', subj: 'all', salt: 0 };
  var G = window.V3G = { st: st, A: A, cat: cat, views: {} };
  var MIN = { cover: 360, school: 360, post: 360, bg: 360, lab: 340, pathway: 340, thumb: 300, book: 190, tile: 220, spot: 260, sticker: 150, avatar: 130, story: 170, pattern: 200, all: 300 };
  G.theme = function () { return document.documentElement.dataset.theme; };
  G.svg = function (it, salt) { var c = {}, k; for (k in it) c[k] = it[k]; if (salt) c.id = it.id + '~' + salt; return A.render(c, G.theme()); };
  G.pick = function (kind, subj, n) { var l = cat.filter(function (i) { return i.kind === kind && (!subj || i.subj === subj); }); return l[(n || 0) % Math.max(1, l.length)]; };
  G.html = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  function dl(name, blob) { var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000); }
  var cur = null;
  G.open = function (it) {
    cur = it; var svg = G.svg(it, st.salt); $('#dart').innerHTML = svg; $('#dtitle').textContent = it.name;
    $('#dmeta').textContent = it.id + '  |  ' + it.engine + '  |  ' + it.palette + '  |  ' + it.w + ' x ' + it.h + '  |  ' + G.theme(); $('#dlg').hidden = false;
  };
  G.exporters = function (svgFn, nameFn) {
    $('#dcopy').onclick = function () { navigator.clipboard.writeText(svgFn()); };
    $('#ddl').onclick = function () { dl(nameFn() + '.svg', new Blob([svgFn()], { type: 'image/svg+xml' })); };
    $('#dpng').onclick = function () { var s = svgFn(), m = s.match(/width="(\d+)" height="(\d+)"/), w = +m[1] * 2, h = +m[2] * 2, im = new Image(); im.onload = function () { var cv = document.createElement('canvas'); cv.width = w; cv.height = h; cv.getContext('2d').drawImage(im, 0, 0, w, h); cv.toBlob(function (b) { dl(nameFn() + '@2x.png', b); }); }; im.src = URL.createObjectURL(new Blob([s], { type: 'image/svg+xml' })); };
  };
  G.exporters(function () { return G.svg(cur, st.salt); }, function () { return cur.id + '-' + G.theme(); });
  $('#dx').onclick = function () { $('#dlg').hidden = true; };
  $('#dlg').onclick = function (e) { if (e.target.id === 'dlg') $('#dlg').hidden = true; };
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') $('#dlg').hidden = true; });

  function rail() {
    var n = {}; cat.forEach(function (i) { n[i.kind] = (n[i.kind] || 0) + 1; });
    var h = '<button class="chip" data-k="all" aria-pressed="' + (st.kind === 'all') + '">All <small>' + cat.length + '</small></button>';
    Object.keys(A.kinds).forEach(function (k) { h += '<button class="chip" data-k="' + k + '" aria-pressed="' + (st.kind === k) + '">' + A.kinds[k].label + ' <small>' + n[k] + '</small></button>'; });
    $('#rail').innerHTML = h;
  }
  function kpis() {
    var eng = Object.keys(A.engines).length, k = [[cat.length, 'named pieces'], [cat.length * 2, 'Light and Dark SVGs'], [Object.keys(A.kinds).length, 'art kinds'], [A.subjectNames.length, 'subjects'], [eng, 'engines'], [A.palettes.length, 'OKLCH palettes']];
    $('#kpis').innerHTML = k.map(function (x) { return '<div class="kpi"><b>' + x[0].toLocaleString() + '</b><span>' + x[1] + '</span></div>'; }).join('');
    $('#subcount').textContent = cat.length.toLocaleString() + ' pieces, ' + (cat.length * 2).toLocaleString() + ' SVGs, flat tonal fills only';
  }
  function library() {
    var q = st.q.toLowerCase().trim(), list = cat.filter(function (i) { return (st.kind === 'all' || i.kind === st.kind) && (st.subj === 'all' || i.subj === st.subj) && (!q || (i.name + ' ' + i.subj + ' ' + i.engine + ' ' + i.palette + ' ' + i.kind).toLowerCase().indexOf(q) > -1); });
    var subs = {}; cat.forEach(function (i) { subs[i.subj] = 1; });
    $('#stage').innerHTML = '<div class="fbar"><select class="sel" id="fs" aria-label="Subject"><option value="all">All subjects</option>' + Object.keys(subs).map(function (s) { return '<option' + (s === st.subj ? ' selected' : '') + '>' + G.html(s) + '</option>'; }).join('') + '</select><span class="count">' + list.length + ' pieces' + (st.kind !== 'all' ? ' - ' + A.kinds[st.kind].desc : '') + '</span></div><div class="grid" id="grid" style="--min:' + MIN[st.kind] + 'px"></div><div class="sent" id="sent"></div>';
    $('#fs').onchange = function (e) { st.subj = e.target.value; library(); };
    var grid = $('#grid'), at = 0, io;
    function more() { var end = Math.min(list.length, at + 36), h = ''; for (; at < end; at++) { var it = list[at]; h += '<button class="card" data-i="' + cat.indexOf(it) + '"><span class="art">' + G.svg(it, st.salt) + '</span><span class="meta"><b>' + G.html(it.name) + '</b><small>' + it.kind + ' - ' + it.palette + '</small></span></button>'; } grid.insertAdjacentHTML('beforeend', h); if (at >= list.length && io) io.disconnect(); }
    grid.onclick = function (e) { var c = e.target.closest('.card'); if (c) G.open(cat[+c.dataset.i]); };
    io = new IntersectionObserver(function (e) { if (e[0].isIntersecting) more(); }, { rootMargin: '900px' }); io.observe($('#sent')); more();
  }
  G.views.library = library;
  G.views.studio = function () {
    var S = { engine: 'himal', palette: 'brand', seed: 7, kind: 'cover', obj: 'books', style: 'plate' }, E = Object.keys(A.engines);
    function opt(l, v) { return l.map(function (x) { return '<option' + (x === v ? ' selected' : '') + '>' + x + '</option>'; }).join(''); }
    $('#stage').innerHTML = '<div class="studio"><div class="panel ctl"><h2><span class="ms">tune</span>Custom studio</h2><label>Engine<select class="sel" id="s-e">' + opt(E, S.engine) + '</select></label><label>Palette<select class="sel" id="s-p">' + opt(A.palettes, S.palette) + '</select></label><label>Size<select class="sel" id="s-k">' + opt(Object.keys(A.kinds), S.kind) + '</select></label><label>Object (still engine)<select class="sel" id="s-o">' + opt(A.objectNames(), S.obj) + '</select></label><label>Backdrop (still engine)<select class="sel" id="s-s">' + opt(['disc', 'arch', 'plate', 'ground', 'pattern'], S.style) + '</select></label><label>Seed<input id="s-d" type="number" value="7"></label><button class="btn" id="s-r"><span class="ms">casino</span>Random seed</button><button class="btn f" id="s-x"><span class="ms">open_in_full</span>Open and export</button></div><div class="out" id="s-out"></div></div>';
    var item = function () { var K = A.kinds[S.kind]; return { id: 'studio-' + S.engine + '-' + S.palette + '-' + S.seed, kind: S.kind, name: 'Studio ' + S.engine, engine: S.engine, palette: S.palette, seed: S.seed, subj: 'Studio', w: K.w, h: K.h, o: { objs: [S.obj, 'books', 'bulb'], style: S.style } }; };
    var paint = function () { $('#s-out').innerHTML = G.svg(item(), 0); };
    [['e', 'engine'], ['p', 'palette'], ['k', 'kind'], ['o', 'obj'], ['s', 'style']].forEach(function (p) { $('#s-' + p[0]).onchange = function (e) { S[p[1]] = e.target.value; paint(); }; });
    $('#s-d').oninput = function (e) { S.seed = +e.target.value || 0; paint(); };
    $('#s-r').onclick = function () { S.seed = Math.floor(Math.random() * 9999); $('#s-d').value = S.seed; paint(); };
    $('#s-x').onclick = function () { var it = item(); G.open(it); G.exporters(function () { return G.svg(it, 0); }, function () { return it.id + '-' + G.theme(); }); };
    paint();
  };
  function go(v) {
    st.view = v; document.querySelectorAll('#views button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.v === v); });
    $('#rail').style.display = v === 'library' ? '' : 'none'; $('#kpis').style.display = v === 'library' ? '' : 'none'; G.views[v](); window.scrollTo(0, 0);
  }
  G.go = go; G.refresh = function () { go(st.view); };
  $('#views').onclick = function (e) { var b = e.target.closest('button'); if (b) go(b.dataset.v); };
  $('#rail').onclick = function (e) { var b = e.target.closest('.chip'); if (b) { st.kind = b.dataset.k; rail(); library(); } };
  $('#q').oninput = function (e) { st.q = e.target.value; if (st.view !== 'library') go('library'); else library(); };
  $('#shuf').onclick = function () { st.salt = Math.floor(Math.random() * 9999); G.refresh(); };
  $('#mode').onclick = function () { var d = G.theme() === 'dark'; document.documentElement.dataset.theme = d ? 'light' : 'dark'; $('#mode .ms').textContent = d ? 'dark_mode' : 'light_mode'; G.refresh(); };
  rail(); kpis(); window.addEventListener('load', function () { var h = location.hash.slice(1); if (G.views[h]) go(h); else go('library'); });
})();
