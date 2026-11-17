/* v5 studio: avatar builder (every face parameter) and banner builder (scene, hero object, palette, size). */
(function () {
  'use strict';
  var A = NebArtV5, P5 = A.people, G = window.G5, host = document.getElementById('studio');
  var S = { skin: 2, hair: 'sweep', hc: 0, outfit: 'tee', acc: 'none', expr: 'smile', bg: 'disc', fem: true, beard: false, palette: 'blue', oc: 'm', flip: false }, B = { engine: 'ribbons', palette: 'teal', obj: 'book', plate: 'tile', size: '1200x400', hero: true, soft: true, alt: false };
  function sel(id, label, opts, val) { return '<label>' + label + '<select id="' + id + '">' + opts.map(function (o) { return '<option' + (String(o) === String(val) ? ' selected' : '') + '>' + o + '</option>'; }).join('') + '</select></label>'; }
  function build() {
    var av = A.make({ id: 'studio', engine: 'person', w: 256, h: 256, palette: S.palette, mode: G.mode, seed: 1, o: { skin: S.skin, hair: S.hair, hc: S.hc, outfit: S.outfit, acc: S.acc, expr: S.expr, bg: S.bg, fem: S.fem, beard: S.beard, jaw: S.fem ? 0.9 : 1.1, oc: S.oc, flip: S.flip } });
    var wh = B.size.split('x'), bw = +wh[0], bh = +wh[1], bo = B.hero ? { obj: B.obj, plate: B.plate, scene: B.engine, soft: B.soft, alt: B.alt, side: 'right', scale: bh > 500 ? 0.5 : 0.42 } : { soft: B.soft, alt: B.alt, bias: 0.7 };
    var bn = A.make({ id: 'studio-b', engine: B.hero ? 'stage' : B.engine, w: bw, h: bh, palette: B.palette, mode: G.mode, seed: 2, o: bo });
    G.stAv = av; G.stBn = bn;
    var sw = P5.SKIN.map(function (c, i) { return '<button data-skin="' + i + '" style="background:' + c + '" aria-label="Skin ' + (i + 1) + '" aria-pressed="' + (i === S.skin) + '"></button>'; }).join('');
    var hc = P5.HAIRCOL.map(function (c, i) { return '<button data-hc="' + i + '" style="background:' + c[0] + '" aria-label="Hair ' + (i + 1) + '" aria-pressed="' + (i === S.hc) + '"></button>'; }).join('');
    host.innerHTML = '<h2>Avatar studio</h2><div class="studio"><div class="panel"><div style="border-radius:32px;overflow:hidden">' + av + '</div><div class="row" style="margin-top:12px"><button class="btn" id="avsv"><span class="ms">download</span>SVG</button><button class="btn t" id="avpn"><span class="ms">image</span>PNG</button><button class="btn t" id="avrn"><span class="ms">shuffle</span>Random</button></div></div><div class="panel"><div class="ctl">' +
      sel('s-hair', 'Hair', P5.HAIR_F.concat(P5.HAIR_M.filter(function (x) { return P5.HAIR_F.indexOf(x) < 0; })), S.hair) + sel('s-outfit', 'Outfit', P5.OUTFITS, S.outfit) + sel('s-acc', 'Accessory', ['none', 'round', 'rect', 'headphones', 'topi', 'grad', 'bindi', 'earring'], S.acc) + sel('s-expr', 'Expression', ['smile', 'grin', 'calm', 'joy'], S.expr) + sel('s-bg', 'Backdrop', P5.BGS, S.bg) + sel('s-pal', 'Palette', A.palettes.filter(function (p) { return p !== 'ink'; }), S.palette) + sel('s-oc', 'Outfit tone', ['m', 'alt'], S.oc) + sel('s-fem', 'Face', ['soft', 'strong'], S.fem ? 'soft' : 'strong') + sel('s-beard', 'Beard', ['no', 'yes'], S.beard ? 'yes' : 'no') +
      '</div><h2>Skin</h2><div class="sw" id="sw-skin">' + sw + '</div><h2>Hair colour</h2><div class="sw" id="sw-hc">' + hc + '</div></div></div>' +
      '<h2>Banner studio</h2><div class="panel"><div class="ctl">' + sel('b-eng', 'Scene', A.SCENES, B.engine) + sel('b-pal', 'Palette', A.palettes.filter(function (p) { return p !== 'ink'; }), B.palette) + sel('b-obj', 'Hero object', Object.keys(A.objects), B.obj) + sel('b-plate', 'Plate', ['disc', 'arch', 'tile', 'cookie', 'bloom'], B.plate) + sel('b-size', 'Size', ['1200x400', '1600x560', '1200x630', '640x256', '800x320', '512x512', '400x560', '1600x900'], B.size) + sel('b-hero', 'Hero', ['yes', 'no'], B.hero ? 'yes' : 'no') + sel('b-soft', 'Tone', ['soft', 'bold'], B.soft ? 'soft' : 'bold') + sel('b-alt', 'Second hue', ['no', 'yes'], B.alt ? 'yes' : 'no') + '</div><div style="margin-top:14px;border-radius:24px;overflow:hidden">' + bn + '</div><div class="row" style="margin-top:12px"><button class="btn" id="bnsv"><span class="ms">download</span>SVG</button><button class="btn t" id="bnpn"><span class="ms">image</span>PNG</button></div></div>';
    wire(bw, bh);
  }
  function wire(bw, bh) {
    var $ = function (s) { return host.querySelector(s); };
    [['s-hair', 'hair'], ['s-outfit', 'outfit'], ['s-acc', 'acc'], ['s-expr', 'expr'], ['s-bg', 'bg'], ['s-pal', 'palette'], ['s-oc', 'oc']].forEach(function (p) { $('#' + p[0]).onchange = function () { S[p[1]] = this.value; build(); }; });
    $('#s-fem').onchange = function () { S.fem = this.value === 'soft'; build(); }; $('#s-beard').onchange = function () { S.beard = this.value === 'yes'; build(); };
    $('#sw-skin').onclick = function (e) { var b = e.target.closest('button'); if (b) { S.skin = +b.dataset.skin; build(); } }; $('#sw-hc').onclick = function (e) { var b = e.target.closest('button'); if (b) { S.hc = +b.dataset.hc; build(); } };
    $('#avsv').onclick = function () { G.fileSvg(G.stAv, 'avatar-studio'); }; $('#avpn').onclick = function () { G.filePng(G.stAv, 256, 256, 'avatar-studio', 3); };
    $('#avrn').onclick = function () { var q = function (a) { return a[Math.floor(Math.random() * a.length)]; }; S.fem = Math.random() < 0.5; S.skin = Math.floor(Math.random() * 8); S.hair = q(S.fem ? P5.HAIR_F : P5.HAIR_M); S.hc = Math.floor(Math.random() * 8); S.outfit = q(P5.OUTFITS); S.acc = q(['none', 'round', 'rect', 'headphones']); S.expr = q(['smile', 'grin', 'calm', 'joy']); S.bg = q(P5.BGS); S.palette = q(A.palettes.filter(function (p) { return p !== 'ink'; })); S.beard = !S.fem && Math.random() < 0.3; build(); };
    [['b-eng', 'engine'], ['b-pal', 'palette'], ['b-obj', 'obj'], ['b-plate', 'plate'], ['b-size', 'size']].forEach(function (p) { $('#' + p[0]).onchange = function () { B[p[1]] = this.value; build(); }; });
    $('#b-hero').onchange = function () { B.hero = this.value === 'yes'; build(); }; $('#b-soft').onchange = function () { B.soft = this.value === 'soft'; build(); }; $('#b-alt').onchange = function () { B.alt = this.value === 'yes'; build(); };
    $('#bnsv').onclick = function () { G.fileSvg(G.stBn, 'banner-studio'); }; $('#bnpn').onclick = function () { G.filePng(G.stBn, bw, bh, 'banner-studio', 2); };
  }
  G.listeners.push(function () { if (!host.hidden) build(); });
})();
