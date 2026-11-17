/* NEBians M3X Art Library v2 — Gallery Controller, Custom Studio & High-Res PNG/SVG Exporter. */
(function () {
  'use strict';
  var V = window.NebArtV2, cat = V.catalog();
  var view = 'gallery', kind = 'cover', tag = '', q = '', mode = 'light', salt = 0, cur = null;
  var $ = function (s) { return document.querySelector(s); };
  var MIN = { cover: 330, school: 330, thumb: 280, book: 175, lab: 310, pathway: 310, post: 310, bg: 320, tile: 195, spot: 240, sticker: 140, glyph: 140 };
  var kinds = Object.keys(V.kinds), rail = $('#rail'), stage = $('#stage'), fbar = $('#fbar');

  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { paint(e.target); io.unobserve(e.target); } });
  }, { rootMargin: '420px' });

  function entry(o) {
    var c = {}; for (var k in o) c[k] = o[k];
    if (salt) c.seed = o.seed + salt * 977;
    c.mode = mode;
    return c;
  }
  function paint(el) { el.innerHTML = V.make(entry(cat[el.dataset.i])); }

  function filtered() {
    return cat.map(function (o, i) { return [o, i]; }).filter(function (p) {
      var o = p[0];
      if (o.kind !== kind) return false;
      if (tag && o.tag !== tag) return false;
      if (!q) return true;
      var hay = (o.id + ' ' + (o.title || '') + ' ' + o.tag + ' ' + (o.subject || '') + ' ' + (o.palette || '') + ' ' + (o.layout || '')).toLowerCase();
      return hay.indexOf(q) > -1;
    });
  }

  function drawKpis() {
    var items = [[cat.length, 'Deterministic pieces'], [V.allCompositions.length, 'Scene & M3X engines'], [V.palettes.length, '8-tone palettes'], [V.subjectNames.length, 'Subjects covered'], [kinds.length, 'UI art categories'], ['2x', 'Light & graphite dark']];
    $('#kpis').innerHTML = items.map(function (x) { return '<div class="kpi"><b>' + x[0] + '</b><span>' + x[1] + '</span></div>'; }).join('');
  }

  function drawRail() {
    rail.innerHTML = kinds.map(function (k) {
      var n = cat.filter(function (o) { return o.kind === k; }).length;
      return '<button role="tab" data-k="' + k + '" aria-selected="' + (k === kind) + '">' + V.kinds[k].label + '<i>' + n + '</i></button>';
    }).join('');
  }

  function drawFilters() {
    if (view !== 'gallery') { fbar.innerHTML = ''; return; }
    var tags = [];
    cat.forEach(function (o) { if (o.kind === kind && tags.indexOf(o.tag) < 0) tags.push(o.tag); });
    fbar.innerHTML = tags.length < 2 ? '' : '<button class="chip" data-t="" aria-pressed="' + !tag + '">All (' + cat.filter(function (o) { return o.kind === kind; }).length + ')</button>' +
      tags.map(function (t) { return '<button class="chip" data-t="' + t + '" aria-pressed="' + (t === tag) + '">' + t + '</button>'; }).join('');
  }

  function renderStudio() {
    var st = window._st || (window._st = { kind: 'thumb', subject: 'Physics', layout: 'physicsOptics', palette: 'brand', seed: 'neb-v2-physics' });
    var svgL = V.make({ kind: st.kind, subject: st.subject, layout: st.layout, palette: st.palette, seed: st.seed + (salt || ''), mode: 'light' });
    var svgD = V.make({ kind: st.kind, subject: st.subject, layout: st.layout, palette: st.palette, seed: st.seed + (salt || ''), mode: 'dark' });
    var T = V.palette(st.palette, mode);
    var sw = T.map(function (c, i) { return '<div class="sw" style="background:' + c + ';color:' + (i > 3 && i < 7 ? '#fff' : '#0b1530') + '">T' + i + '</div>'; }).join('');
    stage.innerHTML = '<div class="studio"><div class="panel">' +
      '<div class="field"><label>Category</label><select id="st-k" class="md-in">' + kinds.map(function (k) { return '<option value="' + k + '"' + (k === st.kind ? ' selected' : '') + '>' + V.kinds[k].label + '</option>'; }).join('') + '</select></div>' +
      '<div class="field"><label>Subject</label><select id="st-s" class="md-in">' + V.subjectNames.map(function (s) { return '<option value="' + s + '"' + (s === st.subject ? ' selected' : '') + '>' + s + '</option>'; }).join('') + '</select></div>' +
      '<div class="field"><label>Scene / Composition Engine</label><select id="st-l" class="md-in">' + V.allCompositions.map(function (l) { return '<option value="' + l + '"' + (l === st.layout ? ' selected' : '') + '>' + l + '</option>'; }).join('') + '</select></div>' +
      '<div class="field"><label>M3X 8-Tone Palette</label><select id="st-p" class="md-in">' + V.palettes.map(function (p) { return '<option value="' + p + '"' + (p === st.palette ? ' selected' : '') + '>' + p + '</option>'; }).join('') + '</select></div>' +
      '<div class="field"><label>Deterministic Seed</label><input id="st-seed" class="md-in" value="' + st.seed + '"></div>' +
      '<div><label style="display:block;font-size:.76rem;font-weight:600;color:var(--md-on-surface-variant);margin-bottom:6px">8-Tone Flat Harmonic Ramp</label><div class="swatches">' + sw + '</div></div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn f" id="st-dl"><span class="ms">download</span>Download SVG</button><button class="btn t" id="st-cp"><span class="ms">content_copy</span>Copy SVG</button></div>' +
      '</div><div style="display:grid;gap:16px">' +
      '<div class="pcard" style="padding:18px"><div style="display:flex;justify-content:space-between;margin-bottom:10px"><b>Light Theme Surface (#f6f8ff)</b><span class="pill">' + st.layout + ' · ' + st.palette + '</span></div><div style="border-radius:20px;overflow:hidden;border:1px solid var(--md-outline-variant)">' + svgL + '</div></div>' +
      '<div class="pcard" style="padding:18px"><div style="display:flex;justify-content:space-between;margin-bottom:10px"><b>Dark Neutral Graphite (#121318)</b><span class="pill">Dark mode pair</span></div><div style="border-radius:20px;overflow:hidden;border:1px solid var(--md-outline-variant)">' + svgD + '</div></div>' +
      '</div></div>';
    ['st-k', 'st-s', 'st-l', 'st-p', 'st-seed'].forEach(function (id) {
      $('#' + id).onchange = $('#' + id).oninput = function () {
        st.kind = $('#st-k').value; st.subject = $('#st-s').value; st.layout = $('#st-l').value; st.palette = $('#st-p').value; st.seed = $('#st-seed').value;
        if (this.id === 'st-s' && V.subjects[st.subject]) { st.palette = V.subjects[st.subject][1]; st.layout = V.subjects[st.subject][2]; }
        renderStudio();
      };
    });
    $('#st-dl').onclick = function () { dlSvg(mode === 'dark' ? svgD : svgL, 'neb-v2-' + st.kind + '-' + st.layout + '.svg'); };
    $('#st-cp').onclick = function () { navigator.clipboard && navigator.clipboard.writeText(mode === 'dark' ? svgD : svgL); };
  }

  function draw() {
    rail.hidden = view !== 'gallery';
    drawFilters();
    if (view === 'inapp') { stage.innerHTML = V.renderInApp(mode, salt); $('#subcount').textContent = 'Live NEBians UI mockups powered by M3X Art Library v2'; return; }
    if (view === 'studio') { renderStudio(); $('#subcount').textContent = 'Interactive M3X procedural scene & palette studio'; return; }
    if (view === 'compare') { stage.innerHTML = V.renderCompare(mode, salt); $('#subcount').textContent = 'Side-by-side comparison: V1 abstract shapes vs V2 bespoke scenes'; return; }
    var K = V.kinds[kind], items = filtered();
    stage.innerHTML = '<div class="grid" id="grid" style="--min:' + MIN[kind] + 'px;--ar:' + K.w + '/' + K.h + '">' +
      (items.length ? items.map(function (p) {
        return '<button class="card" data-i="' + p[1] + '"><span class="art" data-i="' + p[1] + '"></span><span class="cap"><b>' + (p[0].title || p[0].tag) + '</b><small>' + p[0].id + '</small></span></button>';
      }).join('') : '<div style="grid-column:1/-1;padding:64px 0;text-align:center;color:var(--md-on-surface-variant)">No matching pieces found.</div>') + '</div>';
    stage.querySelectorAll('.art').forEach(function (a) { io.observe(a); });
    $('#subcount').textContent = items.length + ' of ' + cat.length + ' pieces · ' + K.desc;
  }

  function dlSvg(svg, name) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
    a.download = name; a.click();
  }

  function dlPng(svg, w, h, name) {
    var img = new Image(), c = document.createElement('canvas');
    c.width = w * 2; c.height = h * 2;
    img.onload = function () {
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      c.toBlob(function (b) { var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = name; a.click(); });
    };
    img.src = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
  }

  function openModal(i) {
    cur = entry(cat[i]);
    var svg = V.make(cur), K = V.kinds[cur.kind], T = V.palette(cur.resolved.palette, mode);
    $('#dart').innerHTML = svg;
    $('#dtitle').textContent = (cur.title || cur.tag) + ' (' + cat[i].id + ')';
    $('#dmeta').textContent = [cur.resolved.engine, cur.resolved.layout, cur.resolved.palette + ' palette', K.w + '×' + K.h].join(' · ');
    $('#dsw').innerHTML = T.map(function (c) { return '<span style="width:18px;height:18px;border-radius:6px;background:' + c + ';border:1px solid var(--md-outline-variant)"></span>'; }).join('');
    $('#dlg').hidden = false; cur.svg = svg; cur.w = K.w; cur.h = K.h;
  }

  $('#views').onclick = function (e) {
    var b = e.target.closest('button'); if (!b) return;
    view = b.dataset.v;
    $('#views').querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
    draw();
  };
  rail.onclick = function (e) { var b = e.target.closest('button'); if (!b) return; kind = b.dataset.k; tag = ''; drawRail(); draw(); };
  fbar.onclick = function (e) { var b = e.target.closest('button'); if (!b) return; tag = b.dataset.t; draw(); };
  stage.onclick = function (e) { var c = e.target.closest('.card'); if (c && c.dataset.i !== undefined) openModal(+c.dataset.i); };
  $('#q').oninput = function () { q = this.value.trim().toLowerCase(); if (view !== 'gallery') { view = 'gallery'; $('#views button').click(); } else draw(); };
  $('#mode').onclick = function () {
    mode = mode === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = mode;
    this.querySelector('.ms').textContent = mode === 'light' ? 'dark_mode' : 'light_mode';
    draw();
  };
  $('#shuf').onclick = function () { salt++; draw(); };
  $('#dx').onclick = function () { $('#dlg').hidden = true; };
  $('#dlg').onclick = function (e) { if (e.target === this) this.hidden = true; };
  document.onkeydown = function (e) { if (e.key === 'Escape') $('#dlg').hidden = true; };
  $('#dcopy').onclick = function () { navigator.clipboard && navigator.clipboard.writeText(cur.svg); };
  $('#ddl').onclick = function () { dlSvg(cur.svg, cur.id + '-' + mode + '.svg'); };
  $('#dpng').onclick = function () { dlPng(cur.svg, cur.w, cur.h, cur.id + '-' + mode + '@2x.png'); };

  drawKpis(); drawRail(); draw();
})();
