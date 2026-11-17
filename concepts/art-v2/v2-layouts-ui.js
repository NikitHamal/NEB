/* NEBians M3X Art Library v2 — Purpose-Built UI & Identity Layouts:
   Role covers, Swiss/MIT-Press textbook covers, 3D lab heroes, pathways, empty states, medallions, glyph tiles. */
(function (g) {
  'use strict';
  var V = g.NebArtV2, L = V.layouts, f1 = V.f1, sh = V.shape, ci = V.circle, rc = V.rect, ln = V.line, pl = V.poly, rg = V.ring;

  /* Role-Tailored Profile Cover Compositions */
  L.roleStudent = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '';
    o += V.scenes.nepalHimalaya(c);
    o += sh('sunny', W * 0.82, H * 0.44, u * 0.28, 0.2, T[5]) + V.glyph('school', W * 0.82 - u * 0.14, H * 0.44 - u * 0.14, u * 0.28, T[7]);
    return o;
  };
  L.roleTeacher = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = L.bauhausChronicle(c);
    o += sh('cookie', W * 0.82, H * 0.48, u * 0.28, 0.1, T[5]) + V.glyph('auto_stories', W * 0.82 - u * 0.14, H * 0.48 - u * 0.14, u * 0.28, T[7]);
    return o;
  };
  L.roleInstitution = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = V.scenes.campusCourtyard(c);
    o += sh('shield', W * 0.5, H * 0.24, u * 0.14, 0, T[6]) + V.glyph('account_balance', W * 0.5 - u * 0.07, H * 0.24 - u * 0.07, u * 0.14, T[5]);
    return o;
  };
  L.roleContributor = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = L.isoMonolith(c);
    o += sh('clover', W * 0.84, H * 0.46, u * 0.26, 0.3, T[5]) + V.glyph('workspace_premium', W * 0.84 - u * 0.13, H * 0.46 - u * 0.13, u * 0.26, T[6]);
    return o;
  };
  L.roleAdmin = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = L.swissGrid(c);
    o += sh('squircle', W * 0.82, H * 0.48, u * 0.28, 0, T[5]) + V.glyph('verified', W * 0.82 - u * 0.14, H * 0.48 - u * 0.14, u * 0.28, T[6]);
    return o;
  };

  /* Swiss / MIT-Press Textbook Cover Generator (400 x 560) */
  V.makeBook = function (c, T, o) {
    var W = c.W, H = c.H, gl = o.glyph || V.glyphFor(o.subject), sc = V.sceneFor(o.subject), out = '';
    /* Spine & top editorial header band */
    out += rc(0, 0, W * 0.075, H, 0, T[5]) + rc(W * 0.075, 0, W * 0.925, H * 0.14, 0, T[1]);
    out += rc(W * 0.13, H * 0.045, W * 0.34, 14, 7, T[5]) + rc(W * 0.72, H * 0.042, W * 0.2, 20, 10, T[4]);
    /* Art plate window with bespoke domain scene clipped inside */
    var px = W * 0.13, py = H * 0.18, pw = W * 0.79, ph = H * 0.44, cid = 'bk-' + V.hash(o.id || o.seed);
    var subCtx = { W: pw, H: ph, u: Math.min(pw, ph), r: c.r, T: T, rr: c.rr, pick: c.pick };
    var art = (V.scenes[sc] || L[o.layout] || L.swissGrid)(subCtx);
    out += '<defs><clipPath id="' + cid + '">' + rc(px, py, pw, ph, 24, '#000') + '</clipPath></defs>';
    out += rc(px, py, pw, ph, 24, T[0]) + '<g clip-path="url(#' + cid + ')"><g transform="translate(' + f1(px) + ' ' + f1(py) + ')">' + art + '</g></g>';
    out += '<rect x="' + f1(px) + '" y="' + f1(py) + '" width="' + f1(pw) + '" height="' + f1(ph) + '" rx="24" fill="none" stroke="' + T[2] + '" stroke-width="2"/>';
    /* Subject glyph medallion straddling the lower right of the plate */
    out += sh('cookie', px + pw - 38, py + ph, 34, 0.2, T[5]) + V.glyph(gl, px + pw - 56, py + ph - 18, 36, T[7]);
    /* Typographic hierarchy bars at bottom */
    out += rc(px, H * 0.68, pw * 0.72, 20, 10, T[5]) + rc(px, H * 0.735, pw * 0.52, 16, 8, T[4]);
    out += rc(px, H * 0.80, pw * 0.36, 12, 6, T[3]) + rc(px, H * 0.88, pw * 0.26, 24, 12, T[2]) + ci(px + pw - 16, H * 0.90, 10, T[6]);
    return out;
  };

  /* Interactive 3D Lab Hero (800 x 360) */
  V.makeLab = function (c, T, o) {
    var W = c.W, H = c.H, u = c.u, gl = o.glyph || V.glyphFor(o.subject), sc = V.sceneFor(o.subject), out = '';
    /* Subtle 3D isometric floor grid */
    for (var i = 1; i < 8; i++) out += ln(W * (i / 8), 0, W * (i / 8), H, 1, T[1]);
    out += (V.scenes[sc] || L.isoMonolith)(c);
    /* 3D axis gizmo badge in corner + subject glyph tile */
    var gx = W * 0.11, gy = H * 0.76;
    out += sh('squircle', gx, gy, u * 0.16, 0, T[5]) + ln(gx, gy, gx, gy - u * 0.09, 3, T[6]) + ln(gx, gy, gx + u * 0.08, gy + u * 0.045, 3, T[7]) + ln(gx, gy, gx - u * 0.08, gy + u * 0.045, 3, T[3]);
    out += sh('clover', W * 0.88, H * 0.24, u * 0.15, 0.2, T[4]) + V.glyph(gl, W * 0.88 - u * 0.08, H * 0.24 - u * 0.08, u * 0.16, T[7]);
    return out;
  };

  /* Career & Course Pathway Banner (800 x 320) */
  V.makePathway = function (c, T, o) {
    var W = c.W, H = c.H, u = c.u, gl = o.glyph || V.glyphFor(o.subject), out = '';
    out += '<path d="M' + f1(W * 0.08) + ' ' + f1(H * 0.74) + 'C' + f1(W * 0.34) + ' ' + f1(H * 0.74) + ' ' + f1(W * 0.38) + ' ' + f1(H * 0.26) + ' ' + f1(W * 0.68) + ' ' + f1(H * 0.26) + 'L' + f1(W * 0.88) + ' ' + f1(H * 0.26) + '" fill="none" stroke="' + T[2] + '" stroke-width="' + f1(u * 0.14) + '" stroke-linecap="round"/>';
    out += '<path d="M' + f1(W * 0.08) + ' ' + f1(H * 0.74) + 'C' + f1(W * 0.34) + ' ' + f1(H * 0.74) + ' ' + f1(W * 0.38) + ' ' + f1(H * 0.26) + ' ' + f1(W * 0.68) + ' ' + f1(H * 0.26) + 'L' + f1(W * 0.88) + ' ' + f1(H * 0.26) + '" fill="none" stroke="' + T[4] + '" stroke-width="' + f1(u * 0.03) + '" stroke-linecap="round"/>';
    var steps = [[0.14, 0.74, 'cookie', 0.13, T[3]], [0.38, 0.52, 'flower', 0.15, T[4]], [0.62, 0.28, 'sunny', 0.17, T[6]], [0.84, 0.28, 'squircle', 0.24, T[5]]];
    steps.forEach(function (st, i) {
      out += sh(st[2], W * st[0], H * st[1], u * st[3], i * 0.4, st[4]);
      if (i < 3) out += ci(W * st[0], H * st[1], u * 0.045, T[7]);
    });
    out += V.glyph(gl, W * 0.84 - u * 0.12, H * 0.28 - u * 0.12, u * 0.24, T[7]);
    return out;
  };

  /* Calm M3X Empty-State Spot Illustration (480 x 360) */
  V.makeSpot = function (c, T, o) {
    var W = c.W, H = c.H, u = c.u, cx = W / 2, cy = H / 2, gl = o.glyph || 'auto_stories', out = '';
    out += sh('pebble', cx, cy, u * 0.42, c.r() * 4, T[1]);
    out += sh(c.pick(['cookie', 'flower', 'clover']), cx - u * 0.22, cy + u * 0.12, u * 0.18, 0.3, T[2]);
    out += sh(c.pick(['sunny', 'squircle']), cx + u * 0.24, cy - u * 0.14, u * 0.14, 0.6, T[3]);
    out += sh('squircle', cx, cy, u * 0.24, 0, T[5]) + V.glyph(gl, cx - u * 0.12, cy - u * 0.12, u * 0.24, T[7]);
    out += ci(cx + u * 0.28, cy + u * 0.18, u * 0.045, T[6]) + ci(cx - u * 0.26, cy - u * 0.2, u * 0.03, T[4]);
    return out;
  };

  /* Multi-layered M3X Achievement Medallion / Sticker (256 x 256) */
  V.makeSticker = function (c, T, o) {
    var k1 = c.pick(['burst', 'lotus', 'starburst', 'sunny', 'flower']), k2 = c.pick(['cookie', 'squircle', 'clover', 'shield']);
    var gl = o.glyph || V.glyphFor(o.subject), out = '';
    out += sh(k1, 128, 128, 118, c.r() * 6, T[1]) + sh(k1, 128, 128, 102, c.r() * 6 + 0.25, T[3]);
    out += sh(k2, 128, 128, 76, 0, T[5]) + rg(128, 128, 60, 2.5, T[2]);
    out += V.glyph(gl, 128 - 40, 128 - 40, 80, T[7]);
    out += sh('starburst', 206, 50, 16, 0.2, T[6]) + ci(48, 204, 9, T[4]) + ci(208, 198, 6, T[6]);
    return out;
  };

  /* Frameless M3X Expressive Glyph Tile / Avatar Silhouette (256 x 256) */
  V.makeGlyphTile = function (c, T, o) {
    var shName = o.shape || c.pick(V.shapeNames), gl = o.glyph || V.glyphFor(o.subject);
    return sh(shName, 128, 128, 114, 0, T[2]) + sh(shName, 128, 128, 88, 0.22, T[5]) + V.glyph(gl, 128 - 44, 128 - 44, 88, T[7]);
  };
})(typeof window !== 'undefined' ? window : globalThis);
