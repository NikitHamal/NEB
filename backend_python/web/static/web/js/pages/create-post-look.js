/* Dynamic posts, web composer: the page style picker (colour, cover pattern or photo, icon, paper, type).
   Same vocabulary as the app composer and post-look.js. The card itself becomes the page, so what you
   see here is what the feed card and the reading page draw. value() is sent as `look` with the post. */
(function () {
  'use strict';
  var host = document.getElementById('cpl');
  var card = document.querySelector('.cp-card');
  var PL = window.NebPostLook;
  if (!host || !card || !PL) return;

  var look = { tone: 0, cover: 0, photo: 0, icon: '', paper: 0, font: 0 };
  var photoUrl = '';
  var open = '';
  var PRESETS = [
    ['Study', { tone: 7, cover: 1, icon: 'book', paper: 1, font: 1 }],
    ['Garden', { tone: 8, cover: 2, icon: 'bio', paper: 0, font: 0 }],
    ['Sunrise', { tone: 10, cover: 3, icon: 'sun', paper: 3, font: 0 }],
    ['Ocean', { tone: 11, cover: 5, icon: 'world', paper: 0, font: 0 }],
    ['Rose', { tone: 18, cover: 9, icon: 'idea', paper: 3, font: 1 }],
    ['Blueprint', { tone: 14, cover: 13, icon: 'math', paper: 2, font: 2 }],
    ['Night', { tone: 16, cover: 7, icon: 'moon', paper: 0, font: 0 }],
    ['Chalk', { tone: 17, cover: 8, icon: 'task', paper: 2, font: 2 }]
  ];
  var PAPERS = [['None', 0], ['Lines', 1], ['Grid', 2], ['Dots', 3]];
  var FONTS = [['Default', 0], ['Serif', 1], ['Mono', 2]];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function icon(name) {
    var s = el('span', 'material-symbols-outlined', name);
    s.setAttribute('aria-hidden', 'true');
    return s;
  }
  function plain() {
    return !look.tone && !look.cover && !look.photo && !look.icon && !look.paper && !look.font;
  }
  function value() {
    if (plain()) return null;
    var o = {};
    ['tone', 'cover', 'photo', 'paper', 'font'].forEach(function (k) { if (look[k]) o[k] = look[k]; });
    if (look.icon) o.icon = look.icon;
    return o;
  }
  function paint() {
    if (plain()) { PL.clear(card); card.classList.remove('cpl-on'); return; }
    var l = {};
    for (var k in look) l[k] = look[k];
    card.classList.add('cpl-on');
    PL.render(card, l);
    // the picked photo may not be served yet by its id; show the local copy meanwhile
    var art = card.querySelector(':scope > .pl-cover > img.pl-art');
    if (art && photoUrl) art.src = photoUrl;
  }
  function set(patch) {
    for (var k in patch) look[k] = patch[k];
    if (patch.photo) look.cover = 0;
    if (patch.cover) { look.photo = 0; photoUrl = ''; }
    paint();
    draw();
  }

  var bar = el('div', 'cpl-bar');
  var panel = el('div', 'cpl-panel');
  panel.hidden = true;
  host.appendChild(bar);
  host.appendChild(panel);

  function chip(label, glyph, key, on) {
    var b = el('button', 'cpl-chip' + (on ? ' on' : ''));
    b.type = 'button';
    b.setAttribute('aria-pressed', open === key ? 'true' : 'false');
    b.appendChild(icon(glyph));
    b.appendChild(el('span', '', label));
    b.addEventListener('click', function () { open = open === key ? '' : key; draw(); });
    return b;
  }
  function section(title) {
    var s = el('div', 'cpl-sec');
    s.appendChild(el('div', 'cpl-sec-title', title));
    return s;
  }
  function seg(items, key) {
    var row = el('div', 'cpl-seg');
    items.forEach(function (it) {
      var b = el('button', 'cpl-pill' + (look[key] === it[1] ? ' on' : ''), it[0]);
      b.type = 'button';
      b.addEventListener('click', function () { var p = {}; p[key] = it[1]; set(p); });
      row.appendChild(b);
    });
    return row;
  }
  function removeBtn(label, fn) {
    var b = el('button', 'cpl-remove');
    b.type = 'button';
    b.appendChild(icon('close'));
    b.appendChild(el('span', '', label));
    b.addEventListener('click', fn);
    return b;
  }

  function coverPanel() {
    var wrap = el('div');
    var s = section('Cover pattern');
    var grid = el('div', 'cpl-grid');
    var dark = PL.isDark();
    for (var i = 1; i <= PL.covers.length; i++) {
      (function (n) {
        var p = PL.covers[n - 1];
        var b = el('button', 'cpl-sw' + (look.cover === n ? ' on' : ''));
        b.type = 'button';
        b.setAttribute('aria-label', 'Cover ' + n);
        b.style.background = '#' + (dark ? p[1] : p[0]);
        var dot = el('span', 'cpl-sw-dot');
        dot.style.background = '#' + p[4];
        b.appendChild(dot);
        b.addEventListener('click', function () { set({ cover: look.cover === n ? 0 : n }); });
        grid.appendChild(b);
      })(i);
    }
    s.appendChild(grid);
    wrap.appendChild(s);
    var s2 = section('Photo cover');
    var up = el('button', 'cpl-pill');
    up.type = 'button';
    up.appendChild(icon('add_photo_alternate'));
    up.appendChild(el('span', '', look.photo ? 'Change photo' : 'Choose a photo'));
    up.addEventListener('click', function () { document.getElementById('cpl-photo').click(); });
    s2.appendChild(up);
    wrap.appendChild(s2);
    if (look.cover || look.photo) wrap.appendChild(removeBtn('Remove cover', function () { photoUrl = ''; set({ cover: 0, photo: 0 }); }));
    return wrap;
  }
  function iconPanel() {
    var wrap = el('div');
    var s = section('Icon');
    var grid = el('div', 'cpl-grid icons');
    Object.keys(PL.icons).forEach(function (key) {
      var b = el('button', 'cpl-ic' + (look.icon === key ? ' on' : ''));
      b.type = 'button';
      b.setAttribute('aria-label', key);
      b.appendChild(icon(PL.icons[key]));
      b.addEventListener('click', function () { set({ icon: look.icon === key ? '' : key }); });
      grid.appendChild(b);
    });
    s.appendChild(grid);
    wrap.appendChild(s);
    if (look.icon) wrap.appendChild(removeBtn('Remove icon', function () { set({ icon: '' }); }));
    return wrap;
  }
  function stylePanel() {
    var wrap = el('div');
    var s0 = section('Themes');
    var row = el('div', 'cpl-seg');
    PRESETS.forEach(function (p) {
      var b = el('button', 'cpl-pill', p[0]);
      b.type = 'button';
      b.addEventListener('click', function () {
        photoUrl = '';
        look = { tone: 0, cover: 0, photo: 0, icon: '', paper: 0, font: 0 };
        for (var k in p[1]) look[k] = p[1][k];
        paint(); draw();
      });
      row.appendChild(b);
    });
    s0.appendChild(row);
    wrap.appendChild(s0);
    var s = section('Page colour');
    var grid = el('div', 'cpl-grid');
    var dark = PL.isDark();
    var none = el('button', 'cpl-sw plain' + (!look.tone ? ' on' : ''));
    none.type = 'button';
    none.setAttribute('aria-label', 'Default colour');
    none.addEventListener('click', function () { set({ tone: 0 }); });
    grid.appendChild(none);
    Object.keys(PL.tones).forEach(function (k) {
      var t = PL.tones[k];
      if (!t) return;
      var n = +k;
      var b = el('button', 'cpl-sw' + (look.tone === n ? ' on' : ''));
      b.type = 'button';
      b.setAttribute('aria-label', 'Colour ' + n);
      b.style.background = '#' + (dark ? t[2] : t[0]);
      b.addEventListener('click', function () { set({ tone: n }); });
      grid.appendChild(b);
    });
    s.appendChild(grid);
    wrap.appendChild(s);
    var s2 = section('Paper');
    s2.appendChild(seg(PAPERS, 'paper'));
    wrap.appendChild(s2);
    var s3 = section('Type');
    s3.appendChild(seg(FONTS, 'font'));
    wrap.appendChild(s3);
    if (!plain()) wrap.appendChild(removeBtn('Back to a plain post', function () {
      photoUrl = '';
      look = { tone: 0, cover: 0, photo: 0, icon: '', paper: 0, font: 0 };
      paint(); draw();
    }));
    return wrap;
  }

  function draw() {
    bar.textContent = '';
    bar.appendChild(chip(look.cover || look.photo ? 'Change cover' : 'Add cover', 'image', 'cover', !!(look.cover || look.photo)));
    bar.appendChild(chip(look.icon ? 'Change icon' : 'Add icon', 'add_reaction', 'icon', !!look.icon));
    bar.appendChild(chip('Style', 'palette', 'style', !!(look.tone || look.paper || look.font)));
    panel.textContent = '';
    panel.hidden = !open;
    if (open === 'cover') panel.appendChild(coverPanel());
    if (open === 'icon') panel.appendChild(iconPanel());
    if (open === 'style') panel.appendChild(stylePanel());
  }

  var input = document.getElementById('cpl-photo');
  input.addEventListener('change', function () {
    var f = input.files && input.files[0];
    input.value = '';
    if (!f) return;
    var fd = new FormData();
    fd.append('image', f);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/ajax/inline-image/upload/');
    xhr.setRequestHeader('X-CSRFToken', typeof CSRF_TOKEN === 'string' ? CSRF_TOKEN : '');
    host.classList.add('busy');
    xhr.onload = function () {
      host.classList.remove('busy');
      try {
        var d = JSON.parse(xhr.responseText);
        if (xhr.status === 200 && d.id) {
          photoUrl = URL.createObjectURL(f);
          set({ photo: d.id });
          return;
        }
        window.alert(d.error || 'Could not upload that photo');
      } catch (e) { window.alert('Could not upload that photo'); }
    };
    xhr.onerror = function () { host.classList.remove('busy'); window.alert('Network error. Please try again.'); };
    xhr.send(fd);
  });

  new MutationObserver(function () { if (open) draw(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  window.NebCpLook = { value: value };
  draw();
})();
