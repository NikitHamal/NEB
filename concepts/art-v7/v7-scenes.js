/* v7 empty states and profile pictures. Abstract on purpose: expressive shapes, one glyph, one accent. No faces, no ring, no clutter. */
(function (g) {
  var N = g.NebArt, sh = N.shape, ci = N.circle, rc = N.rect, f1 = N.f1, gl = function () { return N.glyph.apply(null, arguments); };
  var BIG = ['cookie', 'flower', 'sunny', 'burst', 'clover'], SOFT = ['squircle', 'pebble', 'cookie'];

  /* Empty state, 480 x 360. variant 0 plate, 1 stack, 2 duo, 3 orbit. */
  N.empty = function (o, c, T, glyph) {
    var W = c.W, H = c.H, v = (o.variant || 0) % 4, cx = W / 2, cy = H * 0.5, out = '', k = c.pick(BIG), k2 = c.pick(SOFT), i, r;
    if (v === 0) {
      out += sh(k, cx, cy, H * 0.46, c.r() * 6, T[1]) + sh(k2, cx - H * 0.4, cy + H * 0.2, H * 0.14, c.r() * 6, T[2]) + ci(cx + H * 0.38, cy - H * 0.26, H * 0.045, T[5]);
      r = H * 0.2; out += sh(c.pick(['squircle', 'cookie']), cx, cy, r * 1.45, c.r() * 6, T[4]) + gl(glyph, cx - r * 0.72, cy - r * 0.72, r * 1.44, T[0]);
    } else if (v === 1) {
      var w = H * 0.62, h = H * 0.5;
      out += N.rot(rc(cx - w / 2, cy - h / 2, w, h, h * 0.2, T[1]), -11, cx, cy) + N.rot(rc(cx - w / 2, cy - h / 2, w, h, h * 0.2, T[2]), 8, cx, cy) + rc(cx - w / 2, cy - h / 2, w, h, h * 0.2, T[6]);
      r = h * 0.32; out += sh(c.pick(['cookie', 'flower', 'squircle']), cx, cy, r * 1.4, c.r() * 6, T[4]) + gl(glyph, cx - r * 0.7, cy - r * 0.7, r * 1.4, T[0]) + ci(cx + w * 0.52, cy - h * 0.5, H * 0.05, T[5]);
    } else if (v === 2) {
      out += sh(k, cx - H * 0.2, cy + H * 0.04, H * 0.34, c.r() * 6, T[2]) + sh(k2, cx + H * 0.22, cy - H * 0.04, H * 0.3, c.r() * 6, T[1]);
      r = H * 0.17; out += N.pill(cx, cy + H * 0.02, r * 3.2, r * 2.2, T[4]) + gl(glyph, cx - r * 0.7, cy + H * 0.02 - r * 0.7, r * 1.4, T[0]) + ci(cx + H * 0.34, cy + H * 0.2, H * 0.05, T[5]);
    } else {
      for (i = 3; i >= 1; i--) out += N.ring(cx, cy, H * (0.16 + i * 0.1), H * 0.03, T[i === 3 ? 6 : 1 + (i % 2)]);
      out += N.arc(cx, cy, H * 0.46, c.r() * 6, c.r() * 6 + 2.4, H * 0.03, T[3]);
      r = H * 0.17; out += sh(k, cx, cy, r * 1.5, c.r() * 6, T[4]) + gl(glyph, cx - r * 0.72, cy - r * 0.72, r * 1.44, T[0]) + ci(cx + H * 0.41, cy - H * 0.2, H * 0.045, T[5]);
    }
    return out;
  };

  /* Profile picture, 512 x 512, frameless. The app clips it to a silhouette. variant 0 to 7. */
  N.avatar = function (o, c, T, glyph) {
    var S = c.W, v = (o.variant || 0) % 8, out = '', k = c.pick(BIG), k2 = c.pick(SOFT), q = c.r() * 6, i;
    if (v === 0) out = sh(k, S * 0.5, S * 0.56, S * 0.46, q, T[3]) + ci(S * 0.5, S * 0.56, S * 0.17, T[0]) + ci(S * 0.82, S * 0.2, S * 0.07, T[5]);
    else if (v === 1) out = rc(0, 0, S, S, 0, T[1]) + sh(k, S * 0.34, S * 0.62, S * 0.4, q, T[2]) + sh(k2, S * 0.7, S * 0.36, S * 0.3, c.r() * 6, T[3]) + ci(S * 0.78, S * 0.78, S * 0.06, T[5]);
    else if (v === 2) { out = rc(0, 0, S, S, 0, T[4]); out += N.quarter(0, 0, S / 2, 0, T[3]) + N.quarter(S / 2, S / 2, S / 2, 2, T[2]) + N.quarter(S / 2, 0, S / 2, 3, T[5]) + ci(S * 0.25, S * 0.75, S * 0.2, T[1]); }
    else if (v === 3) { out = rc(0, 0, S, S, 0, T[3]) + sh(k, S / 2, S / 2, S * 0.36, q, T[1]) + gl(glyph, S * 0.34, S * 0.34, S * 0.32, T[4]); }
    else if (v === 4) { out = rc(0, 0, S, S, 0, T[6]) + ci(S * 0.36, S * 0.5, S * 0.3, T[2]) + ci(S * 0.64, S * 0.5, S * 0.3, T[3], ' opacity="0.9"') + ci(S * 0.5, S * 0.5, S * 0.07, T[5]); }
    else if (v === 5) { out = rc(0, 0, S, S, 0, T[2]); for (i = 4; i >= 1; i--) out += ci(S * 0.5, S * 0.55, S * 0.1 * i + S * 0.04, T[i % 2 ? 1 : 3]); out += ci(S * 0.5, S * 0.55, S * 0.06, T[5]); }
    else if (v === 6) out = rc(0, 0, S, S, 0, T[1]) + sh(k, S * 0.5, S * 0.5, S * 0.52, q, T[2]) + sh(k2, S * 0.5, S * 0.5, S * 0.36, q + 1, T[3]) + sh(k, S * 0.5, S * 0.5, S * 0.18, q + 2, T[4]);
    else out = rc(0, 0, S, S, 0, T[7]) + sh(k, S * 0.5, S * 0.5, S * 0.4, q, T[0]) + gl(glyph, S * 0.33, S * 0.33, S * 0.34, T[7]) + ci(S * 0.8, S * 0.8, S * 0.06, T[5]);
    return out;
  };
})(typeof window !== 'undefined' ? window : globalThis);
