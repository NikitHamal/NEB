/* NEBians M3X Art Library v2 — Domain Scene Engine B: Nepal Heritage, Campus, Commerce, Humanities.
   Handcrafted procedural flat-tonal vector illustrations. */
(function (g) {
  'use strict';
  var V = g.NebArtV2, S = V.scenes, f1 = V.f1, sh = V.shape, ci = V.circle, rc = V.rect, ln = V.line, pl = V.poly, rg = V.ring;

  /* 11. Nepal Himalaya: Layered Machhapuchhre / Everest ridgelines, terraced foothills, stupa spire & sun burst */
  S.nepalHimalaya = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, sx = W * c.rr(0.68, 0.8), sy = H * 0.28, o = '';
    o += sh('sunny', sx, sy, u * 0.26, 0.2, T[1]) + ci(sx, sy, u * 0.14, T[6]);
    /* High Himalayan peaks with crisp snow facet + shadow facet */
    var pks = [[0.18, 0.26], [0.42, 0.14], [0.64, 0.24], [0.86, 0.3]];
    pks.forEach(function (pk, i) {
      var px = pk[0] * W, py = pk[1] * H, pw = W * 0.28;
      o += pl([[px, py], [px - pw, H * 0.78], [px + pw * 0.12, H * 0.78]], i % 2 ? T[7] : T[3]);
      o += pl([[px, py], [px + pw * 0.12, H * 0.78], [px + pw, H * 0.78]], i % 2 ? T[4] : T[5]);
    });
    /* Terraced valley bands */
    o += '<path d="M0 ' + f1(H * 0.68) + 'Q' + f1(W * 0.35) + ' ' + f1(H * 0.54) + ' ' + f1(W) + ' ' + f1(H * 0.66) + 'V' + H + 'H0Z" fill="' + T[2] + '"/>';
    o += '<path d="M0 ' + f1(H * 0.82) + 'Q' + f1(W * 0.6) + ' ' + f1(H * 0.68) + ' ' + f1(W) + ' ' + f1(H * 0.8) + 'V' + H + 'H0Z" fill="' + T[4] + '"/>';
    return o;
  };

  /* 12. Campus Courtyard: Classical & modern school colonnade arches, pediment gable, expressive clover trees */
  S.campusCourtyard = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, bx = W * 0.22, bw = W * 0.56, by = H * 0.34, bh = H * 0.54, o = '';
    o += rc(0, H * 0.84, W, H * 0.16, 0, T[2]);
    o += pl([[bx - u * 0.04, by], [bx + bw / 2, H * 0.12], [bx + bw + u * 0.04, by]], T[4]);
    o += rc(bx, by, bw, bh, u * 0.02, T[1]) + ci(bx + bw / 2, H * 0.24, u * 0.06, T[7]);
    var cols = 5, cw = bw / cols, i;
    for (i = 0; i < cols; i++) {
      o += V.arch(bx + i * cw + cw * 0.18, by + bh * 0.24, cw * 0.64, bh * 0.76, i === 2 ? T[5] : T[3]);
    }
    o += rc(W * 0.1, H * 0.56, u * 0.04, H * 0.3, 0, T[5]) + sh('clover', W * 0.12, H * 0.48, u * 0.18, 0.2, T[4]);
    o += rc(W * 0.86, H * 0.56, u * 0.04, H * 0.3, 0, T[5]) + sh('flower', W * 0.88, H * 0.48, u * 0.18, 0.5, T[6]);
    return o;
  };

  /* 13. Economics Ledger: Ascending growth columns, supply-demand equilibrium curve & coin medallions */
  S.economicsLedger = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, n = 7, bw = (W * 0.72) / n, o = '', i;
    for (i = 0; i < n; i++) {
      var bh = H * (0.2 + (i / (n - 1)) * 0.54 * c.rr(0.88, 1.08)), x = W * 0.14 + i * bw;
      o += rc(x, H * 0.86 - bh, bw * 0.72, bh, u * 0.03, i === n - 1 ? T[4] : T[1 + (i % 3)]);
    }
    o += '<path d="M' + f1(W * 0.12) + ' ' + f1(H * 0.76) + 'Q' + f1(W * 0.48) + ' ' + f1(H * 0.62) + ' ' + f1(W * 0.86) + ' ' + f1(H * 0.18) + '" fill="none" stroke="' + T[5] + '" stroke-width="' + f1(u * 0.032) + '" stroke-linecap="round"/>';
    o += ci(W * 0.86, H * 0.18, u * 0.055, T[6]) + sh('cookie', W * 0.24, H * 0.28, u * 0.16, 0, T[6]) + ci(W * 0.24, H * 0.28, u * 0.07, T[7]);
    return o;
  };

  /* 14. Accountancy Balance: Structured double-entry ledger cards, balance bars & verification seal */
  S.accountancyBalance = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', i;
    o += rc(W * 0.08, H * 0.14, W * 0.38, H * 0.72, u * 0.06, T[1]) + rc(W * 0.54, H * 0.14, W * 0.38, H * 0.72, u * 0.06, T[2]);
    for (i = 0; i < 4; i++) {
      var y = H * (0.26 + i * 0.14);
      o += rc(W * 0.13, y, W * c.rr(0.16, 0.28), u * 0.055, u * 0.025, T[4]);
      o += rc(W * 0.59, y, W * c.rr(0.16, 0.28), u * 0.055, u * 0.025, i === 3 ? T[6] : T[5]);
    }
    o += sh('sunny', W * 0.5, H * 0.5, u * 0.18, 0.2, T[5]) + ci(W * 0.5, H * 0.5, u * 0.08, T[6]);
    return o;
  };

  /* 15. Literature Editorial: Open book spread with rising expressive motifs & manuscript lines */
  S.literatureEditorial = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.5, by = H * 0.42, bw = W * 0.34, bh = H * 0.44, o = '', i;
    o += sh('flower', cx - u * 0.28, H * 0.26, u * 0.18, 0.3, T[2]) + sh('sunny', cx + u * 0.26, H * 0.22, u * 0.15, 0.5, T[6]) + sh('cookie', cx, H * 0.18, u * 0.12, 0.1, T[3]);
    o += pl([[cx, by + u * 0.04], [cx - bw, by - u * 0.04], [cx - bw, by + bh - u * 0.04], [cx, by + bh + u * 0.04]], T[7], ' stroke="' + T[5] + '" stroke-width="' + f1(u * 0.024) + '" stroke-linejoin="round"');
    o += pl([[cx, by + u * 0.04], [cx + bw, by - u * 0.04], [cx + bw, by + bh - u * 0.04], [cx, by + bh + u * 0.04]], T[1], ' stroke="' + T[5] + '" stroke-width="' + f1(u * 0.024) + '" stroke-linejoin="round"');
    for (i = 0; i < 4; i++) {
      var ly = by + u * (0.12 + i * 0.08);
      o += ln(cx - bw * 0.82, ly - u * 0.02, cx - bw * 0.18, ly + u * 0.02, u * 0.022, T[3]);
      o += ln(cx + bw * 0.18, ly + u * 0.02, cx + bw * 0.82, ly - u * 0.02, u * 0.022, T[4]);
    }
    return o;
  };

  /* 16. History Monument: Tiered pagoda/heritage arches, chronicle timeline & rosette seal */
  S.historyMonument = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.5, o = '', i;
    o += sh('lotus', cx, H * 0.42, u * 0.46, 0, T[1]);
    for (i = 0; i < 3; i++) {
      var tw = W * (0.54 - i * 0.13), ty = H * (0.64 - i * 0.18), th = H * 0.15;
      o += rc(cx - tw / 2, ty, tw, th, u * 0.02, T[3 + (i % 3)]);
      o += pl([[cx - tw * 0.58, ty], [cx + tw * 0.58, ty], [cx + tw * 0.46, ty - u * 0.05], [cx - tw * 0.46, ty - u * 0.05]], T[5]);
    }
    o += V.arch(cx - u * 0.12, H * 0.62, u * 0.24, H * 0.26, T[6]);
    return o;
  };

  /* 17. Law Civic: Classical pillars, balanced beam scales geometry & civic arch */
  S.lawCivic = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, cx = W * 0.5, o = '';
    o += V.arch(cx - u * 0.42, H * 0.12, u * 0.84, H * 0.78, T[1]);
    o += rc(cx - u * 0.03, H * 0.22, u * 0.06, H * 0.58, u * 0.02, T[5]) + rc(cx - u * 0.24, H * 0.78, u * 0.48, u * 0.06, u * 0.02, T[5]);
    o += ln(cx - u * 0.34, H * 0.34, cx + u * 0.34, H * 0.34, u * 0.03, T[5]) + ci(cx, H * 0.22, u * 0.055, T[6]);
    o += V.quarter(cx - u * 0.46, H * 0.46, u * 0.24, 0, T[4]) + V.quarter(cx + u * 0.22, H * 0.46, u * 0.24, 1, T[4]);
    return o;
  };

  /* 18. Geography Atlas: Topographic rings, globe meridian grid & compass star */
  S.geographyAtlas = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, gx = W * 0.38, gy = H * 0.5, gr = u * 0.34, o = '';
    o += ci(gx, gy, gr, T[1]) + rg(gx, gy, gr, u * 0.024, T[4]);
    o += '<ellipse cx="' + f1(gx) + '" cy="' + f1(gy) + '" rx="' + f1(gr * 0.48) + '" ry="' + f1(gr) + '" fill="none" stroke="' + T[3] + '" stroke-width="' + f1(u * 0.018) + '"/>';
    o += ln(gx - gr, gy, gx + gr, gy, u * 0.018, T[3]) + ln(gx, gy - gr, gx, gy + gr, u * 0.018, T[3]);
    o += sh('starburst', W * 0.76, H * 0.36, u * 0.2, 0.2, T[6]) + ci(W * 0.76, H * 0.36, u * 0.06, T[5]);
    return o;
  };

  /* 19. Music Acoustics: Harmonic equalizer columns, resonator discs & stave lines */
  S.musicAcoustics = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, o = '', i, n = 12, bw = (W * 0.54) / n;
    for (i = 0; i < 5; i++) o += ln(0, H * (0.28 + i * 0.1), W, H * (0.28 + i * 0.1), 1.4, T[1]);
    o += ci(W * 0.26, H * 0.5, u * 0.32, T[5]) + ci(W * 0.26, H * 0.5, u * 0.14, T[6]) + ci(W * 0.26, H * 0.5, u * 0.04, T[0]);
    for (i = 0; i < n; i++) {
      var bh = H * (0.16 + 0.52 * Math.abs(Math.sin(i * 0.65 + c.r())));
      o += rc(W * 0.42 + i * bw, (H - bh) / 2, bw * 0.68, bh, bw * 0.34, T[2 + (i % 4)]);
    }
    return o;
  };

  /* 20. Agriculture Botany: Botanical stem with expressive leaves, terraced rows & sun disc */
  S.agricultureBotany = function (c) {
    var T = c.T, W = c.W, H = c.H, u = c.u, sx = W * 0.32, o = '', i;
    o += sh('sunny', W * 0.74, H * 0.28, u * 0.2, 0.2, T[6]);
    for (i = 0; i < 3; i++) o += rc(W * 0.48, H * (0.54 + i * 0.13), W * 0.44, H * 0.09, u * 0.04, T[2 + i]);
    o += ln(sx, H * 0.86, sx, H * 0.18, u * 0.032, T[5]);
    for (i = 0; i < 3; i++) {
      var ly = H * (0.3 + i * 0.18);
      o += sh('pebble', sx - u * 0.14, ly, u * 0.11, -0.5, T[4]) + sh('pebble', sx + u * 0.14, ly + u * 0.06, u * 0.11, 0.5, T[3]);
    }
    return o;
  };
})(typeof window !== 'undefined' ? window : globalThis);
