(function () {
  var N = window.NebArt, cat = N.catalog(), kind = 'cover', tag = '', q = '', mode = 'light', salt = 0;
  var $ = function (s) { return document.querySelector(s); };
  var MIN = { cover: 330, school: 330, thumb: 280, book: 170, post: 300, bg: 320, tile: 190, sticker: 130 };
  var kinds = Object.keys(N.kinds), tabs = $('#tabs'), grid = $('#grid'), filters = $('#filters');
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { paint(e.target); io.unobserve(e.target); } }); }, { rootMargin: '400px' });

  function entry(o) { var c = {}; for (var k in o) c[k] = o[k]; if (salt) c.seed = o.seed + salt * 977; return c; }
  function paint(el) { el.innerHTML = N.render(entry(cat[el.dataset.i]), mode); }
  function list() {
    return cat.map(function (o, i) { return [o, i]; }).filter(function (p) {
      var o = p[0]; if (o.kind !== kind) return false; if (tag && o.tag !== tag) return false;
      return !q || (o.id + ' ' + o.tag + ' ' + (o.subject || '') + ' ' + (o.palette || '') + ' ' + (o.layout || '')).toLowerCase().indexOf(q) > -1;
    });
  }
  function drawTabs() {
    tabs.innerHTML = kinds.map(function (k) {
      var n = cat.filter(function (o) { return o.kind === k; }).length;
      return '<button role="tab" data-k="' + k + '" aria-selected="' + (k === kind) + '">' + N.kinds[k].label + '<i>' + n + '</i></button>';
    }).join('');
  }
  function drawFilters() {
    var tags = []; cat.forEach(function (o) { if (o.kind === kind && tags.indexOf(o.tag) < 0) tags.push(o.tag); });
    filters.innerHTML = tags.length < 2 ? '' : '<button class="chip" data-t="" aria-pressed="' + !tag + '">All</button>' + tags.map(function (t) { return '<button class="chip" data-t="' + t + '" aria-pressed="' + (t === tag) + '">' + t + '</button>'; }).join('');
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
    var by = {}; cat.forEach(function (o) { by[o.kind] = (by[o.kind] || 0) + 1; });
    $('#facts').innerHTML = [[cat.length, 'pieces'], [N.layoutNames.length, 'compositions'], [N.palettes.length, 'colour families'], [N.subjectNames.length, 'subjects'], [Object.keys(window.NebGlyphs).length, 'icon stickers'], [2, 'themes']]
      .map(function (f) { return '<div><b>' + f[0] + '</b><span>' + f[1] + '</span></div>'; }).join('');
  }
  var cur;
  function open(i) {
    cur = entry(cat[i]); var svg = N.render(cur, mode);
    $('#dart').innerHTML = svg; $('#dtitle').textContent = cat[i].id;
    $('#dmeta').textContent = [cur.resolved && cur.resolved.layout, cur.resolved && cur.resolved.palette, N.kinds[cur.kind].w + ' x ' + N.kinds[cur.kind].h].filter(Boolean).join(', ');
    $('#dlg').hidden = false; cur.svg = svg;
  }
  tabs.onclick = function (e) { var b = e.target.closest('button'); if (!b) return; kind = b.dataset.k; tag = ''; drawTabs(); drawFilters(); draw(); };
  filters.onclick = function (e) { var b = e.target.closest('button'); if (!b) return; tag = b.dataset.t; drawFilters(); draw(); };
  grid.onclick = function (e) { var c = e.target.closest('.card'); if (c) open(+c.dataset.i); };
  $('#q').oninput = function () { q = this.value.trim().toLowerCase(); draw(); };
  $('#mode').onclick = function () {
    mode = mode === 'light' ? 'dark' : 'light'; document.documentElement.dataset.theme = mode;
    this.firstChild.textContent = mode === 'light' ? 'dark_mode' : 'light_mode'; draw();
  };
  $('#shuf').onclick = function () { salt++; draw(); };
  $('#dx').onclick = function () { $('#dlg').hidden = true; };
  $('#dlg').onclick = function (e) { if (e.target === this) this.hidden = true; };
  document.onkeydown = function (e) { if (e.key === 'Escape') $('#dlg').hidden = true; };
  $('#dcopy').onclick = function () { var b = this; navigator.clipboard && navigator.clipboard.writeText(cur.svg).then(function () { b.lastChild.textContent = 'Copied'; setTimeout(function () { b.lastChild.textContent = 'Copy SVG'; }, 1400); }); };
  $('#ddl').onclick = function () { var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([cur.svg], { type: 'image/svg+xml' })); a.download = cur.id + '-' + mode + '.svg'; a.click(); };
  var k0 = (location.hash || '').slice(1); if (kinds.indexOf(k0) > -1) kind = k0;
  facts(); drawTabs(); drawFilters(); draw();
})();
