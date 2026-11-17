(function () {
  var N = window.NebArt, cat = N.catalog(), kind = 'cover', tag = '', q = '', mode = 'light', salt = 0, view = 'lib', uid = 0;
  var $ = function (s) { return document.querySelector(s); };
  var MIN = { cover: 330, school: 330, thumb: 280, book: 170, note: 300, empty: 260, avatar: 130, post: 300, bg: 320, wall: 150, story: 170, strip: 380, tile: 190, icon: 130, sticker: 130 };
  var kinds = Object.keys(N.kinds), tabs = $('#tabs'), grid = $('#grid'), filters = $('#filters'), inapp = $('#inapp');
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { paint(e.target); io.unobserve(e.target); } }); }, { rootMargin: '400px' });
  var CLIPS = ['cookie', 'sunny', 'flower', 'clover', 'burst', 'squircle', 'pebble', 'circle'];

  function entry(o) { var c = {}; for (var k in o) c[k] = o[k]; if (salt) c.seed = o.seed + salt * 977; return c; }
  function paint(el) { el.innerHTML = N.render(entry(cat[el.dataset.i]), mode); }
  function list() {
    return cat.map(function (o, i) { return [o, i]; }).filter(function (p) {
      var o = p[0]; if (o.kind !== kind) return false; if (tag && o.tag !== tag) return false;
      return !q || (o.id + ' ' + o.tag + ' ' + (o.subject || '') + ' ' + (o.palette || '') + ' ' + (o.layout || '') + ' ' + (o.glyph || '')).toLowerCase().indexOf(q) > -1;
    });
  }
  function drawTabs() {
    tabs.innerHTML = kinds.map(function (k) {
      var n = cat.filter(function (o) { return o.kind === k; }).length;
      return '<button role="tab" data-k="' + k + '" aria-selected="' + (view === 'lib' && k === kind) + '">' + N.kinds[k].label + '<i>' + n + '</i></button>';
    }).join('');
  }
  function drawFilters() {
    var tags = []; cat.forEach(function (o) { if (o.kind === kind && tags.indexOf(o.tag) < 0) tags.push(o.tag); });
    filters.innerHTML = tags.length < 2 || tags.length > 70 ? '' : '<button class="chip" data-t="" aria-pressed="' + !tag + '">All</button>' + tags.map(function (t) { return '<button class="chip" data-t="' + t + '" aria-pressed="' + (t === tag) + '">' + t + '</button>'; }).join('');
  }
  function draw() {
    var K = N.kinds[kind], items = list();
    grid.style.setProperty('--min', MIN[kind] + 'px'); grid.style.setProperty('--ar', K.w + '/' + K.h);
    grid.innerHTML = items.length ? items.map(function (p) {
      return '<button class="card" data-i="' + p[1] + '"><span class="art" data-i="' + p[1] + '"></span><span class="cap"><b>' + p[0].tag + '</b><span>' + p[0].id + '</span></span></button>';
    }).join('') : '<div class="empty">Nothing matches that search.</div>';
    grid.querySelectorAll('.art').forEach(function (a) { io.observe(a); });
    $('#count').textContent = items.length + ' of ' + cat.length + ' pieces, ' + kinds.length + ' types';
  }
  function facts() {
    $('#facts').innerHTML = [[cat.length, 'pieces'], [cat.length * 2, 'Light and Dark files'], [kinds.length, 'art types'], [N.layoutNames.length, 'compositions'], [N.palettes.length, 'colour families'], [N.emptyStates.length, 'empty states']]
      .map(function (f) { return '<div><b>' + f[0].toLocaleString() + '</b><span>' + f[1] + '</span></div>'; }).join('');
  }
  var cur;
  function open(i) {
    cur = entry(cat[i]); var svg = N.render(cur, mode);
    $('#dart').innerHTML = svg; $('#dart').dataset.k = cur.kind; $('#dtitle').textContent = cat[i].id;
    $('#dmeta').textContent = [cur.resolved && cur.resolved.layout, cur.resolved && cur.resolved.palette, N.kinds[cur.kind].w + ' x ' + N.kinds[cur.kind].h].filter(Boolean).join(', ');
    $('#dclips').innerHTML = cur.kind === 'avatar' ? CLIPS.map(function (c) { return '<span class="clipv">' + clipped(cur, c) + '</span>'; }).join('') : '';
    $('#dlg').hidden = false; cur.svg = svg;
  }
  function clipped(o, shape) {
    var id = 'c' + (++uid), svg = N.render(o, mode);
    return '<svg viewBox="0 0 512 512"><defs><clipPath id="' + id + '"><path d="' + N.clipShape(shape, 512) + '"/></clipPath></defs><g clip-path="url(#' + id + ')">' + svg + '</g></svg>';
  }
  function pngOf(svg, w, h, name) {
    var im = new Image(); im.onload = function () {
      var cv = document.createElement('canvas'); cv.width = w * 2; cv.height = h * 2; cv.getContext('2d').drawImage(im, 0, 0, w * 2, h * 2);
      var a = document.createElement('a'); a.href = cv.toDataURL('image/png'); a.download = name; a.click();
    }; im.src = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
  }
  /* In-app preview: the pieces where the app would put them. */
  function by(kind, n, step, start) { var l = cat.filter(function (o) { return o.kind === kind; }), r = [], i; for (i = start || 0; r.length < n; i += step) r.push(l[i % l.length]); return r; }
  function img(o) { return N.render(entry(o), mode); }
  function drawInapp() {
    var h = '', av = by('avatar', 4, 41, 3), K = N.kinds;
    h += '<h3>Profile</h3><div class="mockrow">' + [0, 1, 2].map(function (i) {
      var cv = by('cover', 3, 97, 5)[i], a = av[i], s = ['cookie', 'sunny', 'flower'][i];
      return '<div class="mock prof"><div class="pc">' + img(cv) + '</div><div class="pa">' + clipped(a, s) + '</div><b>' + ['Aarav Sharma', 'Sita Rai', 'Kathmandu Model School'][i] + '</b><small>' + ['Student', 'Teacher', 'School'][i] + '</small></div>';
    }).join('') + '</div>';
    h += '<h3>Resources</h3><div class="mockrow">' + by('thumb', 4, 29).map(function (o) { return '<div class="mock res"><div style="aspect-ratio:640/256">' + img(o) + '</div><b>' + o.subject + ' notes</b><small>Grade 12</small></div>'; }).join('') + '</div>';
    h += '<h3>Books</h3><div class="mockrow shelf">' + by('book', 7, 17).map(function (o) { return '<div class="bk">' + img(o) + '</div>'; }).join('') + '</div>';
    h += '<h3>Notes (Android covers)</h3><div class="mockrow">' + by('note', 6, 23).map(function (o, i) { return '<div class="mock res"><div style="aspect-ratio:720/320">' + img(o) + '</div><b>' + ['Chapter summary', 'Lab report', 'Reading list', 'Exam plan', 'Formulas', 'Essay draft'][i] + '</b><small>Edited today</small></div>'; }).join('') + '</div>';
    h += '<h3>Empty states</h3><div class="mockrow">' + by('empty', 4, 13, 2).map(function (o) { return '<div class="mock emp"><div style="aspect-ratio:480/360">' + img(o) + '</div><b>' + o.title + '</b></div>'; }).join('') + '</div>';
    h += '<h3>Achievements and subject icons</h3><div class="mockrow mini">' + by('sticker', 8, 19).map(function (o) { return '<div>' + img(o) + '</div>'; }).join('') + by('icon', 6, 11).map(function (o) { return '<div>' + img(o) + '</div>'; }).join('') + '</div>';
    h += '<h3>Wallpapers and stories</h3><div class="mockrow phones">' + by('wall', 3, 17).map(function (o) { return '<div class="ph" style="aspect-ratio:540/1170">' + img(o) + '</div>'; }).join('') + by('story', 2, 7).map(function (o) { return '<div class="ph" style="aspect-ratio:540/960">' + img(o) + '</div>'; }).join('') + '</div>';
    h += '<h3>Dividers</h3><div class="mockcol">' + by('strip', 3, 19).map(function (o) { return '<div class="strip">' + img(o) + '</div>'; }).join('') + '</div>';
    inapp.innerHTML = h;
  }
  function show() {
    var lib = view === 'lib'; grid.hidden = !lib; filters.hidden = !lib; inapp.hidden = lib; $('#intro').hidden = !lib;
    document.querySelectorAll('#views button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.v === view); });
    drawTabs(); if (lib) { drawFilters(); draw(); } else drawInapp();
  }
  tabs.onclick = function (e) { var b = e.target.closest('button'); if (!b) return; view = 'lib'; kind = b.dataset.k; tag = ''; show(); };
  $('#views').onclick = function (e) { var b = e.target.closest('button'); if (!b) return; view = b.dataset.v; show(); };
  filters.onclick = function (e) { var b = e.target.closest('button'); if (!b) return; tag = b.dataset.t; drawFilters(); draw(); };
  grid.onclick = function (e) { var c = e.target.closest('.card'); if (c) open(+c.dataset.i); };
  $('#q').oninput = function () { q = this.value.trim().toLowerCase(); view = 'lib'; show(); };
  $('#mode').onclick = function () {
    mode = mode === 'light' ? 'dark' : 'light'; document.documentElement.dataset.theme = mode;
    this.firstChild.textContent = mode === 'light' ? 'dark_mode' : 'light_mode'; show();
  };
  $('#shuf').onclick = function () { salt++; show(); };
  $('#dx').onclick = function () { $('#dlg').hidden = true; };
  $('#dlg').onclick = function (e) { if (e.target === this) this.hidden = true; };
  document.onkeydown = function (e) { if (e.key === 'Escape') $('#dlg').hidden = true; };
  $('#dcopy').onclick = function () { var b = this; navigator.clipboard && navigator.clipboard.writeText(cur.svg).then(function () { b.lastChild.textContent = 'Copied'; setTimeout(function () { b.lastChild.textContent = 'Copy SVG'; }, 1400); }); };
  $('#ddl').onclick = function () { var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([cur.svg], { type: 'image/svg+xml' })); a.download = cur.id + '-' + mode + '.svg'; a.click(); };
  $('#dpng').onclick = function () { pngOf(cur.svg, N.kinds[cur.kind].w, N.kinds[cur.kind].h, cur.id + '-' + mode + '@2x.png'); };
  var k0 = (location.hash || '').slice(1); if (kinds.indexOf(k0) > -1) kind = k0;
  facts(); show();
})();
