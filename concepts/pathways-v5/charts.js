/* Pathways v5 charts: small, flat SVG and HTML pieces. No gradients, no shadows. */
(function () {
  'use strict';
  var V = window.V, ch = V.ch = {};
  var clamp = function (x, a, b) { return Math.max(a, Math.min(b, x)); };
  // score ring, v 0..100
  ch.ring = function (v, size, label, color) {
    var r = 26, c = 2 * Math.PI * r, d = c * clamp(v, 0, 100) / 100;
    return '<svg class="ring" width="' + size + '" height="' + size + '" viewBox="0 0 64 64" role="img" aria-label="' + (label || '') + ' ' + Math.round(v) + '"><circle cx="32" cy="32" r="' + r + '" fill="none" stroke="var(--s4)" stroke-width="6"/>' +
      '<circle cx="32" cy="32" r="' + r + '" fill="none" stroke="' + (color || 'var(--p)') + '" stroke-width="6" stroke-linecap="round" stroke-dasharray="' + d.toFixed(1) + ' ' + c.toFixed(1) + '" transform="rotate(-90 32 32)" style="--c:' + c.toFixed(1) + '"/>' +
      '<text x="32" y="33" text-anchor="middle" dominant-baseline="central" font-size="17" font-weight="600" fill="currentColor">' + Math.round(v) + '</text></svg>';
  };
  // labelled meter, v 0..100
  ch.meter = function (label, v, color, shown) {
    return '<div class="met"><span class="mut">' + label + '</span><div class="mt"><i style="--v:' + clamp(v, 0, 100) + (color ? ';--c:' + color : '') + '"></i></div><b>' + (shown == null ? Math.round(v) : shown) + '</b></div>';
  };
  ch.dots = function (n, color) { var h = ''; for (var i = 1; i <= 5; i++) h += '<i class="' + (i <= Math.round(n) ? 'on' : '') + '"></i>'; return '<span class="dots" style="--c:' + (color || 'var(--p)') + '" aria-label="' + n.toFixed(1) + ' of 5">' + h + '</span>'; };
  // a range inside a shared scale, used for pay ladders
  ch.range = function (lo, hi, max, color, label) {
    var a = lo / max * 100, b = hi / max * 100;
    return '<div class="rb" title="' + label + '"><i style="left:' + a.toFixed(1) + '%;width:' + Math.max(2, b - a).toFixed(1) + '%;--c:' + (color || 'var(--p)') + '"></i></div>';
  };
  // five-axis radar, axes [[label, 0..100]]
  ch.radar = function (axes) {
    var n = axes.length, cx = 110, cy = 100, R = 70, pt = function (i, k) { var a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + Math.cos(a) * R * k, cy + Math.sin(a) * R * k]; };
    var ring = function (k) { return axes.map(function (_, i) { return pt(i, k).map(function (v) { return v.toFixed(1); }).join(','); }).join(' '); };
    var poly = axes.map(function (a, i) { return pt(i, clamp(a[1], 6, 100) / 100).map(function (v) { return v.toFixed(1); }).join(','); }).join(' ');
    var spokes = axes.map(function (_, i) { var p = pt(i, 1); return '<line x1="' + cx + '" y1="' + cy + '" x2="' + p[0].toFixed(1) + '" y2="' + p[1].toFixed(1) + '"/>'; }).join('');
    var labs = axes.map(function (a, i) { var p = pt(i, 1.2); return '<text x="' + p[0].toFixed(1) + '" y="' + p[1].toFixed(1) + '" text-anchor="middle" dominant-baseline="central">' + a[0] + '</text>'; }).join('');
    return '<svg class="radar" viewBox="0 0 220 200" role="img" aria-label="Career profile"><g class="rg"><polygon points="' + ring(1) + '"/><polygon points="' + ring(.66) + '"/><polygon points="' + ring(.33) + '"/>' + spokes + '</g><polygon class="rp" points="' + poly + '"/>' + labs + '</svg>';
  };
  // 12 month strip; from..to inclusive and may wrap the year
  ch.months = function (from, to, color) {
    var h = '<div class="mo" style="--c:' + (color || 'var(--p)') + '">';
    for (var m = 1; m <= 12; m++) {
      var on = from <= to ? (m >= from && m <= to) : (m >= from || m <= to);
      h += '<i class="' + (on ? 'on ' : '') + (m === V.now ? 'now' : '') + '" title="' + V.MONTHS[m - 1] + '">' + V.MONTHS[m - 1].charAt(0) + '</i>';
    }
    return h + '</div>';
  };
  ch.monthSet = function (set, color) {
    var h = '<div class="mo" style="--c:' + (color || 'var(--p)') + '">';
    for (var m = 1; m <= 12; m++) h += '<i class="' + (set.indexOf(m) >= 0 ? 'on ' : '') + (m === V.now ? 'now' : '') + '" title="' + V.MONTHS[m - 1] + '">' + V.MONTHS[m - 1].charAt(0) + '</i>';
    return h + '</div>';
  };
  ch.inWindow = function (w) { if (!w) return false; var m = V.now; return w[0] <= w[1] ? (m >= w[0] && m <= w[1]) : (m >= w[0] || m <= w[1]); };
  // stacked bar, parts [[label, value, cssVar]]
  ch.stack = function (parts) {
    var tot = parts.reduce(function (s, p) { return s + p[1]; }, 0) || 1;
    return '<div class="stk">' + parts.map(function (p) { return '<i style="flex:' + (p[1] / tot).toFixed(3) + ';background:' + p[2] + '" title="' + p[0] + '"></i>'; }).join('') + '</div><div class="row wrap sm mut" style="gap:14px;margin-top:8px">' +
      parts.map(function (p) { return '<span class="row" style="gap:6px"><i class="sw" style="background:' + p[2] + '"></i>' + p[0] + ' ' + V.npr(p[1]) + '</span>'; }).join('') + '</div>';
  };
  ch.trend = function (t) { return { rising: ['trending_up', 'Rising', 't-gc'], steady: ['trending_flat', 'Steady', 't-sc'], falling: ['trending_down', 'Falling', 't-rc'] }[t] || ['trending_flat', V.cap(t || 'Steady'), 't-sc']; };
  ch.trendTag = function (t) { var x = ch.trend(t); return '<span class="tag ' + x[2] + '">' + V.ms(x[0]) + x[1] + '</span>'; };
  ch.level = function (v) { return v >= 4.2 ? 'Very high' : v >= 3.4 ? 'High' : v >= 2.6 ? 'Medium' : v >= 1.8 ? 'Low' : 'Very low'; };
})();
