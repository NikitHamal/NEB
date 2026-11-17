/* NEBians M3X art v7, core. Built on the v1 engine (concepts/art/art-core.js): same seeded random, same
   expressive shapes, same flat fills. v7 widens the palette (18 families, 8 tones, tuned for Light and Dark)
   and adds small drawing helpers. No gradients, no shadows, no purple, no emoji, no pixels. */
(function (g) {
  'use strict';
  var N = g.NebArt, f1 = N.f1;
  /* name, hue, accent hue, saturation scale. Tone order: 0 page, 1 soft, 2 mid, 3 strong, 4 ink, 5 accent, 6 mist, 7 deep. */
  var FAM = [
    ['azure', 218, 44, 1], ['sky', 200, 18, 1], ['aqua', 180, 8, 1], ['teal', 164, 36, 1], ['mint', 142, 340, 1], ['moss', 98, 210, 1],
    ['amber', 42, 215, 1], ['orange', 22, 205, 1], ['coral', 6, 190, 1], ['rose', 346, 160, 1], ['periwinkle', 230, 48, 1], ['slate', 214, 38, 0.35],
    ['sage', 128, 22, 0.55], ['clay', 14, 196, 0.6], ['ocean', 205, 28, 1], ['citrine', 56, 214, 0.9], ['cherry', 352, 172, 0.95], ['lagoon', 188, 14, 0.9]
  ];
  function hsl(h, s, l) { return 'hsl(' + Math.round(h) + ',' + Math.round(s) + '%,' + Math.round(l) + '%)'; }
  N.palettes = FAM.map(function (f) { return f[0]; });
  N.palette = function (name, mode) {
    var f = FAM.filter(function (x) { return x[0] === name; })[0] || FAM[0], h = f[1], ha = f[2], k = f[3];
    if (mode === 'dark') return [hsl(h, 46 * k, 9), hsl(h, 50 * k, 17), hsl(h, 56 * k, 30), hsl(h, 70 * k, 62), hsl(h, 74 * k, 85), hsl(ha, 80, 62), hsl(h, 44 * k, 13), hsl(h, 56 * k, 42)];
    return [hsl(h, 82 * k, 92), hsl(h, 76 * k, 82), hsl(h, 72 * k, 66), hsl(h, 88 * k, 40), hsl(h, 92 * k, 15), hsl(ha, 86, 62), hsl(h, 80 * k, 96), hsl(h, 78 * k, 52)];
  };
  /* Warm-or-cool partner for a family, used by two-family pieces. */
  N.partner = function (name) { var i = N.palettes.indexOf(name); return N.palettes[(i + 6 + (i % 3)) % N.palettes.length]; };

  N.rot = function (inner, deg, cx, cy) { return '<g transform="rotate(' + f1(deg) + ' ' + f1(cx) + ' ' + f1(cy) + ')">' + inner + '</g>'; };
  N.pill = function (cx, cy, w, h, fill, extra) { return N.rect(cx - w / 2, cy - h / 2, w, h, Math.min(w, h) / 2, fill, extra); };
  N.ring = function (cx, cy, r, sw, stroke, extra) { return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="' + f1(r) + '" fill="none" stroke="' + stroke + '" stroke-width="' + f1(sw) + '"' + (extra || '') + '/>'; };
  N.arc = function (cx, cy, r, a0, a1, sw, stroke) {
    var x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0), x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
    return '<path d="M' + f1(x0) + ' ' + f1(y0) + 'A' + f1(r) + ' ' + f1(r) + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + f1(x1) + ' ' + f1(y1) + '" fill="none" stroke="' + stroke + '" stroke-width="' + f1(sw) + '" stroke-linecap="round"/>';
  };
  N.curve = function (pts, sw, stroke) {
    var d = 'M' + f1(pts[0][0]) + ' ' + f1(pts[0][1]), i;
    for (i = 1; i < pts.length - 1; i++) d += 'Q' + f1(pts[i][0]) + ' ' + f1(pts[i][1]) + ' ' + f1((pts[i][0] + pts[i + 1][0]) / 2) + ' ' + f1((pts[i][1] + pts[i + 1][1]) / 2);
    d += 'L' + f1(pts[pts.length - 1][0]) + ' ' + f1(pts[pts.length - 1][1]);
    return '<path d="' + d + '" fill="none" stroke="' + stroke + '" stroke-width="' + f1(sw) + '" stroke-linecap="round" stroke-linejoin="round"/>';
  };
  /* A clip so a piece can be shown inside any expressive silhouette (profile pictures). */
  N.clipShape = function (kind, size) { return N.shapeD(kind, size / 2, size / 2, size / 2 * (kind === 'flower' ? 1.33 : kind === 'clover' ? 1.2 : 0.98), 0); };
})(typeof window !== 'undefined' ? window : globalThis);
