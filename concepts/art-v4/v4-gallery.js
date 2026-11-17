/* v4 gallery: Library (lazy, filters, detail), In-app (v4-previews.js), Studio. Everything renders live from the deterministic engines. */
(function (g) {
  'use strict';
  var A = g.NebArtV4, cat = A.catalog(), $ = function (id) { return document.getElementById(id); }, st = { mode: 'light', view: 'library', kind: 'cover', subj: 'all', q: '', n: 60 };
  var SHAPES = ['circle', 'squircle', 'cookie', 'flower', 'clover', 'burst', 'pebble', 'sunny'], stage = $('stage'), io, cur = null;
  A.esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  /* shape clips for profile pictures: clip only, never a ring */
  var clips = SHAPES.map(function (k) { return '<clipPath id="cp-' + k + '" clipPathUnits="objectBoundingBox"><path transform="scale(.00390625)" d="' + A.shapeD(k, 128, 128, k === 'circle' ? 126 : 112, 0) + '"/></clipPath>'; }).join('');
  document.body.insertAdjacentHTML('beforeend', '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + clips + '</defs></svg>');
  A.pp = function (it, shape, size) { return '<span class="pp" style="width:' + size + 'px;height:' + size + 'px;clip-path:url(#cp-' + shape + ')">' + A.render(it, st.mode) + '</span>'; };
  A.of = function (kind, i) { var l = cat.filter(function (x) { return x.kind === kind; }); return l[((i % l.length) + l.length) % l.length]; };
  A.mode = function () { return st.mode; };

  function card(it) {
    var b = document.createElement('button'); b.className = 'card'; b.type = 'button'; b.dataset.id = it.id;
    b.innerHTML = '<span class="art" style="aspect-ratio:' + it.w + '/' + it.h + '"></span><span class="meta"><b>' + A.esc(it.name) + '</b><small>' + it.id + ' - ' + it.palette + '</small></span>';
    io.observe(b); return b;
  }
  function filtered() {
    var q = st.q.toLowerCase();
    return cat.filter(function (x) { return (st.kind === 'all' || x.kind === st.kind) && (st.subj === 'all' || x.subject === st.subj || x.subj === st.subj) && (!q || (x.name + ' ' + x.engine + ' ' + x.palette + ' ' + x.id).toLowerCase().indexOf(q) > -1); });
  }
  function library() {
    var list = filtered(), K = A.kinds[st.kind], min = st.kind === 'all' ? 260 : K.w / K.h > 2.2 ? 340 : K.w / K.h > 1.4 ? 280 : K.h > K.w ? 170 : 190, subs = ['all'].concat(A.subjectNames.concat(['People', 'Buddies', 'Critters', 'Empty states', 'Achievements', 'Backgrounds', 'Patterns', 'Schools']));
    stage.innerHTML = '<div class="fbar"><select class="sel" id="subj">' + subs.map(function (s) { return '<option' + (s === st.subj ? ' selected' : '') + '>' + s + '</option>'; }).join('') + '</select><span class="count">' + list.length + ' pieces</span><span class="grow"></span><span class="count">' + (K ? K.desc : 'All kinds') + '</span></div><div class="grid" id="grid" style="--min:' + min + 'px"></div><div class="sent" id="sent"></div>';
    $('subj').onchange = function (e) { st.subj = e.target.value; st.n = 60; library(); };
    var grid = $('grid'), shown = 0;
    function more() { list.slice(shown, shown + st.n).forEach(function (it) { grid.appendChild(card(it)); }); shown += st.n; }
    more(); var so = new IntersectionObserver(function (e) { if (e[0].isIntersecting && shown < list.length) more(); }, { rootMargin: '900px' }); so.observe($('sent'));
    grid.onclick = function (e) { var c = e.target.closest('.card'); if (c) open(cat.filter(function (x) { return x.id === c.dataset.id; })[0]); };
  }
  io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (!e.isIntersecting) return; var c = e.target, it = cat.filter(function (x) { return x.id === c.dataset.id; })[0]; c.firstChild.innerHTML = A.render(it, st.mode); io.unobserve(c); }); }, { rootMargin: '600px' });

  function open(it) {
    cur = it; var d = $('dlg'), extra = '';
    if (it.kind === 'avatar') extra = '<div class="shapes">' + SHAPES.map(function (s) { return A.pp(it, s, 72); }).join('') + '</div>';
    $('dart').innerHTML = A.render(it, st.mode) + extra; $('dtitle').textContent = it.name; $('dmeta').textContent = it.id + ' - ' + it.engine + ' - ' + it.palette + ' - ' + it.w + 'x' + it.h; d.hidden = false;
  }
  function dl(name, blob) { var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000); }
  $('dx').onclick = function () { $('dlg').hidden = true; }; $('dlg').onclick = function (e) { if (e.target === $('dlg')) $('dlg').hidden = true; };
  $('dcopy').onclick = function () { navigator.clipboard && navigator.clipboard.writeText(A.render(cur, st.mode)); };
  $('ddl').onclick = function () { dl(cur.id + '-' + st.mode + '.svg', new Blob([A.render(cur, st.mode)], { type: 'image/svg+xml' })); };
  $('dpng').onclick = function () { var im = new Image(), u = URL.createObjectURL(new Blob([A.render(cur, st.mode)], { type: 'image/svg+xml' })); im.onload = function () { var cv = document.createElement('canvas'); cv.width = cur.w * 2; cv.height = cur.h * 2; cv.getContext('2d').drawImage(im, 0, 0, cv.width, cv.height); cv.toBlob(function (b) { dl(cur.id + '-' + st.mode + '@2x.png', b); }); URL.revokeObjectURL(u); }; im.src = u; };

  function studio() {
    var E = Object.keys(A.engines).filter(function (k) { return ['person', 'buddy', 'critter', 'glyphTile', 'stage'].concat(Object.keys(A.engines)).indexOf(k) > -1; }), O = Object.keys(A.objects), S = { engine: 'stage', palette: 'brand', seed: 7, w: 1200, h: 400, obj: 'rocket', style: 'disc', side: 'right', bg: 'tessera' };
    function opt(l, v) { return l.map(function (x) { return '<option' + (x === v ? ' selected' : '') + '>' + x + '</option>'; }).join(''); }
    stage.innerHTML = '<div class="studio"><div class="panel ctl"><h2><span class="ms">tune</span>Studio</h2>' + [['engine', E], ['palette', A.palettes], ['obj', O], ['style', ['disc', 'arch', 'plate', 'ground', 'burst', 'pattern']], ['side', ['left', 'center', 'right']], ['bg', A.PATTERN_BG], ['size', ['1200x400', '1600x560', '640x256', '480x360', '512x512', '256x256', '400x560', '540x960']]].map(function (c) { return '<label>' + c[0] + '<select class="sel" data-k="' + c[0] + '">' + opt(c[1], c[0] === 'size' ? '1200x400' : S[c[0]]) + '</select></label>'; }).join('') + '<label>seed<input type="number" data-k="seed" value="7"></label><button class="btn f" id="rnd"><span class="ms">casino</span>Random seed</button></div><div class="out" id="out"></div></div>';
    function draw() { var o = $('out'); try { o.innerHTML = A.make({ engine: S.engine, palette: S.palette, seed: S.seed, w: S.w, h: S.h, mode: st.mode, id: 'studio', o: { objs: [S.obj], style: S.style, side: S.side, bg: S.bg, glyph: 'science' } }); } catch (e) { o.textContent = e.message; } }
    stage.querySelector('.panel').oninput = function (e) { var k = e.target.dataset.k; if (!k) return; if (k === 'size') { var p = e.target.value.split('x'); S.w = +p[0]; S.h = +p[1]; } else S[k] = k === 'seed' ? +e.target.value : e.target.value; draw(); };
    $('rnd').onclick = function () { S.seed = Math.floor(Math.random() * 99999); stage.querySelector('[data-k=seed]').value = S.seed; draw(); }; draw();
  }
  function render() {
    document.documentElement.dataset.theme = st.mode; $('rail').style.display = st.view === 'library' ? '' : 'none';
    [].forEach.call($('views').children, function (b) { b.setAttribute('aria-pressed', b.dataset.v === st.view); });
    if (st.view === 'library') library(); else if (st.view === 'studio') studio(); else A.inapp(stage, st);
  }
  function rail() {
    var ks = Object.keys(A.kinds), cnt = {}; cat.forEach(function (x) { cnt[x.kind] = (cnt[x.kind] || 0) + 1; });
    $('rail').innerHTML = [['all', 'All', cat.length]].concat(ks.map(function (k) { return [k, A.kinds[k].label, cnt[k]]; })).map(function (k) { return '<button class="chip" data-k="' + k[0] + '" aria-pressed="' + (k[0] === st.kind) + '">' + k[1] + ' <small>' + k[2] + '</small></button>'; }).join('');
  }
  $('rail').onclick = function (e) { var b = e.target.closest('.chip'); if (!b) return; st.kind = b.dataset.k; st.n = 60; rail(); library(); };
  $('views').onclick = function (e) { var b = e.target.closest('button'); if (b) { st.view = b.dataset.v; render(); } };
  $('q').oninput = function (e) { st.q = e.target.value; if (st.view !== 'library') st.view = 'library'; render(); };
  $('mode').onclick = function () { st.mode = st.mode === 'light' ? 'dark' : 'light'; render(); };
  $('shuf').onclick = function () { cat.sort(function () { return Math.random() - 0.5; }); render(); };
  $('subcount').textContent = cat.length + ' pieces - ' + cat.length * 2 + ' Light and Dark SVGs - ' + Object.keys(A.engines).length + ' engines - ' + Object.keys(A.objects).length + ' objects';
  rail(); render();
})(window);
