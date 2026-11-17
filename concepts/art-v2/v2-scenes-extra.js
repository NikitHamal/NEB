/* NEBians M3X Art Library v2 — Domain Scene Engine C: Advanced Science, AI/Robotics, Nepali Pagoda & Finance (10 scenes).
   Brings total bespoke domain scenes to 30 (50 total composition engines). */
(function (g) {
  'use strict';
  var V = g.NebArtV2, S = V.scenes, f1 = V.f1, sh = V.shape, ci = V.circle, rc = V.rect, ln = V.line, pl = V.poly, rg = V.ring;

  /* 21. Quantum Wave: Bohr orbital shells, electron transition nodes & wave-packet envelope */
  S.quantumWave = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.32, cy = H * 0.5, o = '', i;
    for (i = 3; i >= 1; i--) o += rg(cx, cy, u * (0.11 * i), i === 2 ? u * 0.022 : u * 0.014, T[i + 1]);
    o += sh('sunny', cx, cy, u * 0.09, 0, T[6]) + ci(cx, cy, u * 0.04, T[5]);
    o += ci(cx + u * 0.22, cy, u * 0.032, T[5]) + ci(cx - u * 0.16, cy - u * 0.28, u * 0.032, T[6]);
    var d = '';
    for (i = 0; i <= 64; i++) {
      var t = i / 64, env = Math.sin(t * Math.PI), x = W * 0.52 + t * W * 0.42, y = cy + Math.sin(t * 38) * env * H * 0.32;
      d += (i ? 'L' : 'M') + f1(x) + ' ' + f1(y);
    }
    o += rc(W * 0.50, H * 0.14, W * 0.46, H * 0.72, u * 0.06, T[1]);
    o += '<path d="' + d + '" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.026) + '" stroke-linecap="round"/>';
    return o;
  };

  /* 22. Organic Synthesis: Round-bottom boiling flask, condenser bridge, receiver & crystallization stars */
  S.organicSynthesis = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, x1 = W * 0.26, y1 = H * 0.64, x2 = W * 0.74, y2 = H * 0.68, o = '';
    o += sh('cookie', x1, y1, u * 0.28, 0, T[1]) + sh('clover', x2, y2, u * 0.24, 0, T[1]);
    /* Condenser tube connecting flask 1 to flask 2 */
    o += ln(x1, y1 - u * 0.28, W * 0.46, H * 0.24, u * 0.055, T[3]) + ln(W * 0.46, H * 0.24, x2, y2 - u * 0.2, u * 0.055, T[3]);
    o += ln(x1, y1 - u * 0.28, W * 0.46, H * 0.24, u * 0.022, T[7]) + ln(W * 0.46, H * 0.24, x2, y2 - u * 0.2, u * 0.022, T[7]);
    o += rc(x1 - u * 0.05, y1 - u * 0.32, u * 0.1, u * 0.18, u * 0.02, T[5]) + ci(x1, y1, u * 0.2, T[7]) + V.quarter(x1 - u * 0.2, y1, u * 0.2, 2, T[4]) + V.quarter(x1, y1, u * 0.2, 3, T[4]);
    o += rg(x1, y1, u * 0.2, u * 0.026, T[5]);
    o += ci(x2, y2, u * 0.16, T[7]) + rg(x2, y2, u * 0.16, u * 0.024, T[5]) + ci(x2, y2 + u * 0.04, u * 0.1, T[6]);
    o += sh('starburst', W * 0.5, H * 0.56, u * 0.09, 0.2, T[6]);
    return o;
  };

  /* 23. Botany Cell: Hexagonal plant cell wall, chloroplast stacks & lotus flower emblem */
  S.botanyCell = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.36, cy = H * 0.5, r = u * 0.36, pts = [], pts2 = [], i, a, o = '';
    for (i = 0; i < 6; i++) {
      a = i * Math.PI / 3;
      pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
      pts2.push([cx + Math.cos(a) * r * 0.82, cy + Math.sin(a) * r * 0.82]);
    }
    o += pl(pts, T[4]) + pl(pts2, T[1]) + sh('pebble', cx - u * 0.06, cy, u * 0.15, 0.3, T[3]) + ci(cx + u * 0.09, cy - u * 0.06, u * 0.08, T[5]);
    o += sh('lotus', W * 0.76, H * 0.48, u * 0.28, 0, T[2]) + sh('flower', W * 0.76, H * 0.48, u * 0.18, 0.4, T[6]) + ci(W * 0.76, H * 0.48, u * 0.06, T[5]);
    return o;
  };

  /* 24. Calculus Surface: Isometric 3D surface grid, tangent vector & definite integral shaded curve */
  S.calculusSurface = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', d = 'M' + f1(W * 0.08) + ' ' + f1(H * 0.82), i;
    for (i = 0; i <= 40; i++) {
      var t = i / 40, x = W * (0.08 + t * 0.48), y = H * (0.64 - 0.36 * Math.sin(t * Math.PI * 1.4) - 0.12 * t);
      d += 'L' + f1(x) + ' ' + f1(y);
    }
    o += '<path d="' + d + 'L' + f1(W * 0.56) + ' ' + f1(H * 0.82) + 'Z" fill="' + T[2] + '"/>';
    o += '<path d="' + d.replace(/^M[^L]+L/, 'M') + '" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.03) + '" stroke-linecap="round"/>';
    o += V.isoBox(W * 0.76, H * 0.22, u * 0.28, u * 0.28, u * 0.34, T[7], T[3], T[5], T[0]);
    o += ci(W * 0.32, H * 0.26, u * 0.05, T[6]) + ln(W * 0.18, H * 0.38, W * 0.46, H * 0.14, u * 0.022, T[6]);
    return o;
  };

  /* 25. Neural Network: Multi-layer perceptron with synaptic weights & isometric tensor block */
  S.neuralNetwork = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cols = [W * 0.16, W * 0.44, W * 0.72], counts = [3, 4, 2], layers = [], o = '', i, j, k;
    for (i = 0; i < 3; i++) {
      layers[i] = [];
      for (j = 0; j < counts[i]; j++) layers[i].push([cols[i], H * (0.5 + (j - (counts[i] - 1) / 2) * 0.22)]);
    }
    for (i = 0; i < 2; i++) for (j = 0; j < layers[i].length; j++) for (k = 0; k < layers[i + 1].length; k++) {
      o += ln(layers[i][j][0], layers[i][j][1], layers[i + 1][k][0], layers[i + 1][k][1], u * 0.015, (j + k) % 3 === 0 ? T[4] : T[2]);
    }
    for (i = 0; i < 3; i++) for (j = 0; j < layers[i].length; j++) {
      var p = layers[i][j];
      o += sh(i === 1 ? 'cookie' : 'squircle', p[0], p[1], u * 0.075, 0, i === 2 ? T[6] : T[i === 1 ? 4 : 5]) + ci(p[0], p[1], u * 0.028, T[7]);
    }
    o += V.isoBox(W * 0.88, H * 0.38, u * 0.16, u * 0.16, u * 0.22, T[7], T[3], T[5], T[0]);
    return o;
  };

  /* 26. Himalayan Pagoda: Traditional Nepali 3-tiered pagoda temple with upturned eaves & mountain peak */
  S.himalayanPagoda = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.5, o = '', i;
    o += pl([[W * 0.16, H * 0.88], [W * 0.36, H * 0.24], [W * 0.56, H * 0.88]], T[1]);
    o += pl([[W * 0.48, H * 0.88], [W * 0.74, H * 0.2], [W * 0.94, H * 0.88]], T[2]);
    o += sh('sunny', W * 0.24, H * 0.26, u * 0.14, 0, T[6]);
    /* Spire pinnacle */
    o += pl([[cx, H * 0.08], [cx - u * 0.05, H * 0.22], [cx + u * 0.05, H * 0.22]], T[6]);
    for (i = 0; i < 3; i++) {
      var rw = W * (0.24 + i * 0.12), ry = H * (0.22 + i * 0.19), rh = H * 0.09;
      o += rc(cx - rw * 0.34, ry + rh, rw * 0.68, H * 0.11, 4, T[3]);
      o += pl([[cx - rw * 0.38, ry], [cx + rw * 0.38, ry], [cx + rw * 0.56, ry + rh], [cx - rw * 0.56, ry + rh]], T[5]);
      o += ln(cx - rw * 0.56, ry + rh, cx + rw * 0.56, ry + rh, u * 0.02, T[6]);
    }
    o += V.arch(cx - u * 0.09, H * 0.72, u * 0.18, H * 0.18, T[6]);
    return o;
  };

  /* 27. Kathmandu Valley: Stupa dome, harmika eyes block, 13-tier spire & prayer flags */
  S.kathmanduValley = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.5, by = H * 0.82, dr = u * 0.34, o = '';
    o += ln(cx, H * 0.16, W * 0.1, H * 0.52, u * 0.016, T[3]) + ln(cx, H * 0.16, W * 0.9, H * 0.52, u * 0.016, T[3]);
    o += V.arch(cx - dr, by - dr * 1.05, dr * 2, dr * 1.05, T[7]);
    o += '<path d="M' + f1(cx - dr) + ' ' + f1(by) + 'V' + f1(by - dr * 0.05) + 'A' + f1(dr) + ' ' + f1(dr) + ' 0 0 1 ' + f1(cx + dr) + ' ' + f1(by - dr * 0.05) + 'V' + f1(by) + 'Z" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.024) + '"/>';
    o += rc(cx - u * 0.12, by - dr * 1.05 - u * 0.14, u * 0.24, u * 0.14, u * 0.02, T[6]);
    o += ci(cx - u * 0.045, by - dr * 1.05 - u * 0.07, u * 0.022, T[5]) + ci(cx + u * 0.045, by - dr * 1.05 - u * 0.07, u * 0.022, T[5]);
    o += pl([[cx, H * 0.12], [cx - u * 0.09, by - dr * 1.05 - u * 0.14], [cx + u * 0.09, by - dr * 1.05 - u * 0.14]], T[5]);
    o += rc(cx - dr * 1.25, by, dr * 2.5, H * 0.1, u * 0.02, T[4]);
    return o;
  };

  /* 28. Macro Finance: Allocation donut ring, yield curve & reserve pillars */
  S.macroFinance = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, dx = W * 0.28, dy = H * 0.5, dr = u * 0.3, o = '', i;
    o += ci(dx, dy, dr, T[2]) + V.quarter(dx, dy - dr, dr, 1, T[4]) + V.quarter(dx, dy, dr, 2, T[5]) + V.quarter(dx - dr, dy, dr, 3, T[6]) + ci(dx, dy, dr * 0.52, T[0]);
    for (i = 0; i < 5; i++) {
      var bh = H * (0.24 + i * 0.11);
      o += rc(W * (0.54 + i * 0.08), H * 0.84 - bh, W * 0.055, bh, u * 0.02, i === 4 ? T[6] : T[2 + (i % 3)]);
    }
    return o;
  };

  /* 29. Hospitality Culinary: Serving cloche dome, botanical garnish & geometric table setting */
  S.hospitalityCulinary = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.5, by = H * 0.72, dr = u * 0.36, o = '';
    o += sh('lotus', W * 0.2, H * 0.36, u * 0.18, 0.2, T[2]) + sh('flower', W * 0.8, H * 0.36, u * 0.18, 0.5, T[6]);
    o += ci(cx, by - dr * 0.92, u * 0.055, T[6]);
    o += V.arch(cx - dr, by - dr * 0.92, dr * 2, dr * 0.92, T[4]);
    o += rc(cx - dr * 1.2, by, dr * 2.4, u * 0.07, u * 0.035, T[5]);
    return o;
  };

  /* 30. Robotics Mechatronics: Articulated servo arm, joint medallions & PWM signal trace */
  S.roboticsMechatronics = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, j1 = [W * 0.24, H * 0.76], j2 = [W * 0.44, H * 0.32], j3 = [W * 0.72, H * 0.44], o = '';
    o += rc(j1[0] - u * 0.16, j1[1], u * 0.32, H * 0.14, u * 0.03, T[5]);
    o += ln(j1[0], j1[1], j2[0], j2[1], u * 0.08, T[3]) + ln(j2[0], j2[1], j3[0], j3[1], u * 0.065, T[4]);
    [j1, j2, j3].forEach(function (p, i) { o += ci(p[0], p[1], u * (0.09 - i * 0.012), T[5]) + ci(p[0], p[1], u * 0.04, i === 1 ? T[6] : T[7]); });
    o += V.isoBox(W * 0.82, H * 0.56, u * 0.16, u * 0.16, u * 0.18, T[6], T[4], T[5], T[0]);
    return o;
  };
})(typeof window !== 'undefined' ? window : globalThis);
