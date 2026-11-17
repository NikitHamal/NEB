/* NEBians M3X Art Library v2 — Domain Scene Engine A: Science, Math, CS, Space, Engineering, Medicine.
   Handcrafted procedural flat-tonal vector illustrations with authentic domain geometry. */
(function (g) {
  'use strict';
  var V = g.NebArtV2, S = V.scenes, f1 = V.f1, sh = V.shape, ci = V.circle, rc = V.rect, ln = V.line, pl = V.poly, rg = V.ring;

  /* 1. Physics Optics: Equilateral prism dispersing 4 flat-tonal spectrum beams + harmonic wave + lens */
  S.physicsOptics = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * c.rr(0.42, 0.56), cy = H * 0.54, s = u * 0.42, o = '';
    o += sh('sunny', cx, cy, s * 1.15, c.r() * 3, T[1]);
    var pTop = [cx, cy - s * 0.65], pL = [cx - s * 0.62, cy + s * 0.48], pR = [cx + s * 0.62, cy + s * 0.48];
    var cols = [T[6], T[4], T[3], T[2]], i;
    for (i = 0; i < 4; i++) {
      var y1 = cy - s * 0.18 + i * s * 0.12, y2 = cy - s * 0.45 + i * s * 0.34;
      o += pl([[cx + s * 0.15, y1], [W, y2], [W, y2 + s * 0.22], [cx + s * 0.25, y1 + s * 0.1]], cols[i]);
    }
    o += ln(0, cy + s * 0.15, cx - s * 0.26, cy - s * 0.06, u * 0.038, T[5]);
    o += pl([pTop, pR, pL], T[5]) + pl([[cx, cy - s * 0.48], [cx + s * 0.44, cy + s * 0.36], [cx - s * 0.44, cy + s * 0.36]], T[7]);
    o += pl([[cx - s * 0.26, cy - s * 0.06], [cx + s * 0.22, cy - s * 0.16], [cx + s * 0.3, cy + s * 0.08]], T[3]);
    o += ci(W * 0.18, H * 0.28, u * 0.08, T[6]) + rg(W * 0.18, H * 0.28, u * 0.15, u * 0.018, T[3]);
    return o;
  };

  /* 2. Physics Electromagnetism: Solenoid field loops, harmonic oscilloscope wave & dipole nodes */
  S.physicsFields = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.52, cy = H * 0.5, o = '', i, sw = f1(u * 0.016);
    for (i = 1; i <= 4; i++) {
      var rx = u * (0.22 + i * 0.16), ry = u * (0.12 + i * 0.09);
      o += '<ellipse cx="' + f1(cx) + '" cy="' + f1(cy) + '" rx="' + f1(rx) + '" ry="' + f1(ry) + '" fill="none" stroke="' + T[i % 2 ? 2 : 3] + '" stroke-width="' + sw + '"/>';
    }
    for (i = -2; i <= 2; i++) o += rc(cx + i * u * 0.14 - u * 0.04, cy - u * 0.18, u * 0.08, u * 0.36, u * 0.04, T[i % 2 ? 4 : 5]);
    var d = '', ph = c.r() * 4;
    for (i = 0; i <= 60; i++) d += (i ? 'L' : 'M') + f1(i / 60 * W) + ' ' + f1(H * 0.22 + Math.sin(i / 60 * 18.8 + ph) * u * 0.09);
    o += '<path d="' + d + '" fill="none" stroke="' + T[6] + '" stroke-width="' + f1(u * 0.028) + '" stroke-linecap="round"/>';
    o += sh('burst', cx - u * 0.52, cy, u * 0.12, 0, T[6]) + sh('cookie', cx + u * 0.52, cy, u * 0.12, 0, T[4]);
    return o;
  };

  /* 3. Chemistry Lab: Erlenmeyer flask, volumetric round flask, flat meniscus layers, benzene hexagon lattice */
  S.chemistryLab = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, fx = W * 0.34, fy = H * 0.84, fw = u * 0.44, fh = u * 0.62, o = '';
    o += sh('clover', fx, fy - fh * 0.45, u * 0.46, 0.3, T[1]);
    /* Hexagonal benzene lattice on the right */
    var hx = W * 0.68, hy = H * 0.42, hr = u * 0.16, pts = [], i, a;
    for (i = 0; i < 6; i++) { a = i * Math.PI / 3 - Math.PI / 6; pts.push([hx + Math.cos(a) * hr, hy + Math.sin(a) * hr]); }
    o += pl(pts, T[2], ' stroke="' + T[5] + '" stroke-width="' + f1(u * 0.025) + '" stroke-linejoin="round"') + rg(hx, hy, hr * 0.56, u * 0.02, T[5]);
    for (i = 0; i < 6; i++) o += ci(pts[i][0], pts[i][1], u * 0.036, i % 2 ? T[6] : T[4]);
    /* Erlenmeyer flask silhouette & liquid fill */
    o += pl([[fx - fw * 0.14, fy - fh], [fx + fw * 0.14, fy - fh], [fx + fw * 0.14, fy - fh * 0.62], [fx + fw * 0.52, fy], [fx - fw * 0.52, fy], [fx - fw * 0.14, fy - fh * 0.62]], T[7], ' stroke="' + T[5] + '" stroke-width="' + f1(u * 0.026) + '" stroke-linejoin="round"');
    o += pl([[fx - fw * 0.27, fy - fh * 0.38], [fx + fw * 0.27, fy - fh * 0.38], [fx + fw * 0.47, fy - fh * 0.05], [fx - fw * 0.47, fy - fh * 0.05]], T[4]);
    o += rc(fx - fw * 0.22, fy - fh - u * 0.04, fw * 0.44, u * 0.05, u * 0.025, T[5]);
    o += ci(fx - fw * 0.08, fy - fh * 0.22, u * 0.035, T[7]) + ci(fx + fw * 0.1, fy - fh * 0.5, u * 0.028, T[6]) + ci(fx, fy - fh * 0.75, u * 0.022, T[6]);
    return o;
  };

  /* 4. Biology Helix: Twisted DNA base-pair ladder + cellular organelle cross-section */
  S.biologyHelix = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', n = 14, i, x, y1, y2, amp = H * 0.26, cy = H * 0.52;
    o += sh('pebble', W * 0.26, H * 0.48, u * 0.42, 0.4, T[1]) + sh('flower', W * 0.26, H * 0.48, u * 0.22, 0.8, T[2]) + ci(W * 0.26, H * 0.48, u * 0.09, T[6]);
    var d1 = '', d2 = '';
    for (i = 0; i <= n; i++) {
      x = W * 0.08 + (i / n) * W * 0.84;
      var s = Math.sin(i * 0.58 + c.r() * 0.2);
      y1 = cy + s * amp; y2 = cy - s * amp;
      d1 += (i ? 'L' : 'M') + f1(x) + ' ' + f1(y1);
      d2 += (i ? 'L' : 'M') + f1(x) + ' ' + f1(y2);
      o += ln(x, y1, x, y2, u * 0.018, T[i % 2 ? 3 : 2]);
      o += ci(x, y1, u * 0.034, T[4]) + ci(x, y2, u * 0.034, i % 3 === 0 ? T[6] : T[5]);
    }
    o += '<path d="' + d1 + '" fill="none" stroke="' + T[4] + '" stroke-width="' + f1(u * 0.028) + '" stroke-linecap="round"/>';
    o += '<path d="' + d2 + '" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.028) + '" stroke-linecap="round"/>';
    return o;
  };

  /* 5. Math Fibonacci: Golden ratio subdivision + Riemann integral step columns + isometric solid */
  S.mathFibonacci = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', i, n = 10, bw = (W * 0.52) / n;
    for (i = 0; i < n; i++) {
      var t = i / (n - 1), bh = H * (0.18 + 0.58 * Math.sin(t * 2.6 + 0.3));
      o += rc(W * 0.06 + i * bw, H * 0.86 - bh, bw * 0.84, bh, u * 0.02, T[1 + (i % 4)]);
    }
    var gx = W * 0.62, gy = H * 0.14, gs = u * 0.68;
    o += rc(gx, gy, gs, gs, u * 0.04, T[1]) + V.quarter(gx, gy, gs, 0, T[2]) + V.quarter(gx + gs * 0.38, gy + gs * 0.38, gs * 0.62, 1, T[3]) + V.quarter(gx + gs * 0.38, gy + gs * 0.62, gs * 0.38, 2, T[4]);
    o += V.isoBox(W * 0.76, H * 0.36, u * 0.2, u * 0.2, u * 0.22, T[7], T[4], T[5], T[0]);
    o += ci(gx + gs * 0.52, gy + gs * 0.52, u * 0.055, T[6]);
    return o;
  };

  /* 6. Math Harmonic: Polar rose curves, coordinate grid & secant geometry */
  S.mathHarmonic = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.56, cy = H * 0.5, R = u * 0.42, o = '', s = u / 5, x, y, i;
    for (x = s; x < W; x += s) o += ln(x, 0, x, H, 1.2, T[1]);
    for (y = s; y < H; y += s) o += ln(0, y, W, y, 1.2, T[1]);
    o += rg(cx, cy, R, u * 0.015, T[2]) + rg(cx, cy, R * 0.55, u * 0.012, T[2]);
    var d = '', k = c.pick([3, 4, 5]);
    for (i = 0; i <= 120; i++) {
      var a = (i / 120) * Math.PI * 2, r = R * Math.cos(k * a);
      d += (i ? 'L' : 'M') + f1(cx + r * Math.cos(a)) + ' ' + f1(cy + r * Math.sin(a));
    }
    o += '<path d="' + d + 'Z" fill="' + T[2] + '" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.024) + '"/>';
    o += ci(cx, cy, u * 0.05, T[6]) + sh('squircle', W * 0.2, H * 0.5, u * 0.22, 0.3, T[3]);
    return o;
  };

  /* 7. CS Architecture: Framed terminal code window with syntax pills + binary tree graph */
  S.csArchitecture = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, wx = W * 0.07, wy = H * 0.14, ww = W * 0.48, wh = H * 0.72, o = '';
    o += rc(wx, wy, ww, wh, u * 0.06, T[5]) + rc(wx + u * 0.025, wy + u * 0.11, ww - u * 0.05, wh - u * 0.135, u * 0.04, T[1]);
    o += ci(wx + u * 0.07, wy + u * 0.055, u * 0.02, T[6]) + ci(wx + u * 0.13, wy + u * 0.055, u * 0.02, T[3]) + ci(wx + u * 0.19, wy + u * 0.055, u * 0.02, T[2]);
    for (var i = 0; i < 5; i++) {
      var ly = wy + u * (0.17 + i * 0.1), indent = (i === 1 || i === 2 || i === 4) ? u * 0.08 : 0;
      o += rc(wx + u * 0.07 + indent, ly, u * c.rr(0.18, 0.34), u * 0.045, u * 0.022, i % 2 ? T[4] : T[5]);
      o += rc(wx + u * 0.46 + indent, ly, u * c.rr(0.14, 0.28), u * 0.045, u * 0.022, i === 2 ? T[6] : T[3]);
    }
    var nx = W * 0.75, ny = H * 0.24, dx = u * 0.22, dy = H * 0.26;
    var nodes = [[nx, ny], [nx - dx, ny + dy], [nx + dx, ny + dy], [nx - dx * 1.45, ny + dy * 2], [nx - dx * 0.45, ny + dy * 2], [nx + dx * 0.55, ny + dy * 2]];
    var edges = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]];
    edges.forEach(function (e) { o += ln(nodes[e[0]][0], nodes[e[0]][1], nodes[e[1]][0], nodes[e[1]][1], u * 0.022, T[3]); });
    nodes.forEach(function (p, j) { o += sh(j === 0 ? 'squircle' : 'cookie', p[0], p[1], u * (j === 0 ? 0.085 : 0.065), 0, j === 0 ? T[6] : T[j % 2 ? 4 : 5]); });
    return o;
  };

  /* 8. Astronomy Cosmos: Ringed Saturnian planet, tilted orbital rings, constellation mesh */
  S.astronomyCosmos = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, px = W * 0.58, py = H * 0.5, pr = u * 0.24, o = '', i;
    var stars = [[0.14, 0.24], [0.26, 0.18], [0.34, 0.36], [0.18, 0.64], [0.32, 0.74], [0.84, 0.22]];
    for (i = 0; i < 4; i++) o += ln(stars[i][0] * W, stars[i][1] * H, stars[i + 1][0] * W, stars[i + 1][1] * H, u * 0.012, T[2]);
    stars.forEach(function (s, j) { o += sh('starburst', s[0] * W, s[1] * H, u * (j % 2 ? 0.03 : 0.048), j, j === 0 ? T[6] : T[4]); });
    o += sh('sunny', px, py, pr * 1.45, 0.2, T[1]) + ci(px, py, pr, T[4]) + V.quarter(px - pr, py - pr, pr, 0, T[3]);
    o += '<g transform="translate(' + f1(px) + ' ' + f1(py) + ') rotate(-22)"><ellipse cx="0" cy="0" rx="' + f1(pr * 2.05) + '" ry="' + f1(pr * 0.52) + '" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.036) + '"/><ellipse cx="0" cy="0" rx="' + f1(pr * 1.65) + '" ry="' + f1(pr * 0.38) + '" fill="none" stroke="' + T[6] + '" stroke-width="' + f1(u * 0.018) + '"/></g>';
    return o;
  };

  /* 9. Engineering Isometric: 30-deg isometric architectural monument blocks & precision gear rosette */
  S.engineeringIso = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '';
    o += sh('burst', W * 0.26, H * 0.48, u * 0.34, 0.2, T[2]) + sh('burst', W * 0.26, H * 0.48, u * 0.22, 0.5, T[4]) + ci(W * 0.26, H * 0.48, u * 0.09, T[0]);
    o += V.isoBox(W * 0.64, H * 0.16, u * 0.32, u * 0.32, u * 0.38, T[7], T[3], T[5], T[0]);
    o += V.isoBox(W * 0.52, H * 0.38, u * 0.24, u * 0.24, u * 0.28, T[6], T[4], T[5], T[0]);
    o += V.isoBox(W * 0.76, H * 0.42, u * 0.22, u * 0.22, u * 0.24, T[2], T[3], T[4], T[0]);
    return o;
  };

  /* 10. Medicine Vital: ECG PQRST waveform trace, diagnostic pulse rings & cross medallion */
  S.medicineVital = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, mx = W * 0.26, my = H * 0.48, o = '';
    o += sh('clover', mx, my, u * 0.34, 0, T[1]) + sh('squircle', mx, my, u * 0.22, 0, T[4]);
    o += rc(mx - u * 0.035, my - u * 0.11, u * 0.07, u * 0.22, u * 0.02, T[7]) + rc(mx - u * 0.11, my - u * 0.035, u * 0.22, u * 0.07, u * 0.02, T[7]);
    var y = H * 0.56, d = 'M' + f1(W * 0.44) + ' ' + f1(y) + 'L' + f1(W * 0.54) + ' ' + f1(y) + 'L' + f1(W * 0.57) + ' ' + f1(y - u * 0.08) + 'L' + f1(W * 0.60) + ' ' + f1(y + u * 0.06) + 'L' + f1(W * 0.64) + ' ' + f1(y - u * 0.34) + 'L' + f1(W * 0.68) + ' ' + f1(y + u * 0.22) + 'L' + f1(W * 0.72) + ' ' + f1(y - u * 0.12) + 'L' + f1(W * 0.76) + ' ' + f1(y) + 'L' + f1(W * 0.94) + ' ' + f1(y);
    o += '<path d="' + d + '" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.032) + '" stroke-linecap="round" stroke-linejoin="round"/>';
    o += ci(W * 0.64, y - u * 0.34, u * 0.04, T[6]);
    return o;
  };
})(typeof window !== 'undefined' ? window : globalThis);
