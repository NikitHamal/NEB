/* Pathways: the real map of Nepal (the "chuche" boundary, 77 districts, 7 provinces) for the Colleges tab.
   Same data as Android (res/raw/nepal_map.json). Geometry is built once, five fill layers instead of 77 elements,
   labels are drawn in screen space with a collision pass and stay thin and small so they fit inside their district.
   PWMAP.mount(el, {counts: {District: n}, selected: 'Kathmandu', onPick(name)}) returns {update(counts, selected)}. */
(function (g) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg', KMAX = 16, PROV = ['Koshi', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim'];
  var GEO = null, pending = null;

  function decode(rings) {
    return rings.map(function (r) {
      var x = 0, y = 0, o = [];
      for (var k = 0; k < r.length; k += 2) { if (k === 0) { x = r[0]; y = r[1]; } else { x += r[k]; y += r[k + 1]; } o.push(x, y); }
      return o;
    });
  }
  function pathOf(rings) {
    var s = '';
    rings.forEach(function (r) { s += 'M' + r[0] + ' ' + r[1]; for (var i = 2; i < r.length; i += 2) s += 'L' + r[i] + ' ' + r[i + 1]; s += 'Z'; });
    return s;
  }
  function build(j) {
    var sx = [0, 0, 0, 0, 0, 0, 0], sy = [0, 0, 0, 0, 0, 0, 0], n = [0, 0, 0, 0, 0, 0, 0], all = '';
    var ds = j.d.map(function (o) {
      var rings = decode(o.r), x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      rings.forEach(function (r) { for (var k = 0; k < r.length; k += 2) { if (r[k] < x0) x0 = r[k]; if (r[k] > x1) x1 = r[k]; if (r[k + 1] < y0) y0 = r[k + 1]; if (r[k + 1] > y1) y1 = r[k + 1]; } });
      sx[o.p] += o.c[0]; sy[o.p] += o.c[1]; n[o.p]++;
      var d = pathOf(rings); all += d;
      return { n: o.n, p: o.p, hq: o.hq || '', cx: o.c[0], cy: o.c[1], rings: rings, d: d, x0: x0, y0: y0, x1: x1, y1: y1, w: x1 - x0 };
    });
    var pv = ''; j.pv.forEach(function (r) { pv += pathOf(decode(r)); });
    return {
      w: j.w, h: j.h, ds: ds, by: ds.reduce(function (m, d) { m[d.n] = d; return m; }, {}), borders: all, prov: pv, outline: pathOf(decode(j.o)),
      centres: sx.map(function (v, i) { return [v / Math.max(1, n[i]), sy[i] / Math.max(1, n[i])]; }),
      area: ds.slice().sort(function (a, b) { return b.w * (b.y1 - b.y0) - a.w * (a.y1 - a.y0); })
    };
  }
  function inside(d, x, y) {
    if (x < d.x0 || x > d.x1 || y < d.y0 || y > d.y1) return false;
    var c = false;
    d.rings.forEach(function (r) {
      for (var i = 0, j = r.length - 2; i < r.length; j = i, i += 2) {
        var xi = r[i], yi = r[i + 1], xj = r[j], yj = r[j + 1];
        if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c;
      }
    });
    return c;
  }
  var bin = function (n) { return n <= 0 ? 0 : n === 1 ? 1 : n < 4 ? 2 : n < 7 ? 3 : 4; };

  function get(cb) {
    if (GEO) return cb(GEO);
    if (pending) return pending.push(cb);
    pending = [cb];
    var done = function (j) { GEO = build(j); var q = pending; pending = null; q.forEach(function (f) { f(GEO); }); };
    if (g.NM_DATA) return done(g.NM_DATA);
    fetch(g.NM_SRC || '/static/web/data/nepal_map.json').then(function (r) { return r.json(); }).then(done).catch(function () { pending = null; });
  }

  function mount(el, o) {
    var counts = o.counts || {}, sel = o.selected || '', geo = null, k = 1, tx = 0, ty = 0, W = 0, H = 0, raf = 0, moved = false;
    el.classList.add('nm');
    el.innerHTML = '<svg class="nmw" aria-hidden="true"></svg><svg class="nml" aria-hidden="true"></svg><div class="nmi" hidden></div>' +
      '<div class="nmc"><button type="button" class="ib" data-z="in" aria-label="Zoom in"><svg class="i" width="20" height="20" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></button>' +
      '<button type="button" class="ib" data-z="out" aria-label="Zoom out"><svg class="i" width="20" height="20" viewBox="0 0 24 24"><path d="M5 12h14"/></svg></button></div>';
    var wsvg = el.querySelector('.nmw'), lsvg = el.querySelector('.nml'), info = el.querySelector('.nmi');

    function paint() {
      var bins = ['', '', '', '', ''];
      geo.ds.forEach(function (d) { bins[bin(counts[d.n] || 0)] += d.d; });
      var s = geo.by[sel];
      wsvg.setAttribute('viewBox', '0 0 ' + geo.w + ' ' + geo.h);
      wsvg.innerHTML = '<g class="nmg">' + bins.map(function (d, i) { return '<path class="nb' + i + '" fill-rule="evenodd" d="' + d + '"/>'; }).join('') +
        (s ? '<path class="nsel" fill-rule="evenodd" d="' + s.d + '"/>' : '') +
        '<path class="nbd" fill-rule="evenodd" d="' + geo.borders + '"/><path class="npv" fill-rule="evenodd" d="' + geo.prov + '"/><path class="nol" fill-rule="evenodd" d="' + geo.outline + '"/>' +
        (s ? '<path class="nso" fill-rule="evenodd" d="' + s.d + '"/>' : '') + '</g>';
      if (s) { info.hidden = false; var c = counts[s.n] || 0; info.innerHTML = '<b>' + s.n + '</b><span>' + (s.hq ? s.hq + ' · ' : '') + c + (c === 1 ? ' college' : ' colleges') + '</span>'; } else info.hidden = true;
      view();
    }
    // zoom k, shift (tx, ty) in map units; screen = ox + base * (t + k * p)
    var base = function () { return Math.min(W / geo.w, H / geo.h) || 1; };
    var ox = function () { return (W - geo.w * base()) / 2; }, oy = function () { return (H - geo.h * base()) / 2; };
    function clamp() {
      k = Math.max(1, Math.min(KMAX, k)); var px = geo.w * .25, py = geo.h * .25;
      tx = Math.max(geo.w - geo.w * k - px, Math.min(px, tx)); ty = Math.max(geo.h - geo.h * k - py, Math.min(py, ty));
    }
    function view() {
      if (!geo || !W) return;
      var gEl = wsvg.firstChild;
      // the svg viewBox is fitted and centred by the browser, so the group only needs the pan and zoom
      if (gEl) gEl.setAttribute('transform', 'translate(' + tx + ' ' + ty + ') scale(' + k + ')');
      labels();
    }
    function labels() {
      var b = base(), s = b * k, out = '', taken = [];
      var X = function (x) { return ox() + b * (tx + k * x); }, Y = function (y) { return oy() + b * (ty + k * y); };
      var free = function (r) { for (var i = 0; i < taken.length; i++) { var t = taken[i]; if (r[0] < t[2] && r[2] > t[0] && r[1] < t[3] && r[3] > t[1]) return false; } return true; };
      if (k < 1.6) geo.centres.forEach(function (c, i) {
        var t = PROV[i].toUpperCase(), fs = 8.5, w = t.length * fs * .72, x = X(c[0]), y = Y(c[1]);
        out += '<text class="lp" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" font-size="' + fs + '">' + t + '</text>';
        taken.push([x - w / 2 - 2, y - fs, x + w / 2 + 2, y + fs]);
      });
      var fs = k < 1.6 ? 6.5 : k < 2.6 ? 7.5 : k < 4.2 ? 8.5 : k < 7 ? 9.5 : 10.5, cw = fs * .5;
      var order = sel && geo.by[sel] ? [geo.by[sel]].concat(geo.area) : geo.area;
      for (var i = 0; i < order.length; i++) {
        var d = order[i], on = d.n === sel, x = X(d.cx), y = Y(d.cy), w = d.n.length * cw;
        if (!on && d.w * s < 18) continue;
        if (x < -60 || y < -30 || x > W + 60 || y > H + 30) continue;
        if (!on && d.w * s < w * 1.12) continue;
        var box = [x - w / 2 - 2, y - fs * .7 - 1, x + w / 2 + 2, y + fs * .7 + 1];
        if (!on && !free(box)) continue;
        taken.push(box);
        out += '<text class="ld' + (on ? ' on' : '') + '" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" font-size="' + (on ? Math.max(fs, 8.5) : fs) + '">' + d.n + '</text>';
      }
      lsvg.innerHTML = out;
    }
    function size() {
      var r = el.getBoundingClientRect(); W = r.width; H = r.height;
      lsvg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); view();
    }
    function fly(k2, x2, y2) {
      cancelAnimationFrame(raf);
      var k0 = k, x0 = tx, y0 = ty, t0 = performance.now(), D = 380;
      if (matchMedia('(prefers-reduced-motion: reduce)').matches) { k = k2; tx = x2; ty = y2; clamp(); view(); return; }
      (function step(t) {
        var p = Math.min(1, (t - t0) / D), e = 1 - Math.pow(1 - p, 3);
        k = k0 + (k2 - k0) * e; tx = x0 + (x2 - x0) * e; ty = y0 + (y2 - y0) * e; clamp(); view();
        if (p < 1) raf = requestAnimationFrame(step);
      })(t0);
    }
    function zoomAt(px, py, f) { // px, py in map units under the finger
      var k2 = Math.max(1, Math.min(KMAX, k * f)), r = k2 / k;
      k = k2; tx = px - (px - tx) * r; ty = py - (py - ty) * r; clamp(); view();
    }
    function toMap(cx, cy) { var r = el.getBoundingClientRect(), b = base(); return [(cx - r.left - ox()) / b, (cy - r.top - oy()) / b]; }
    function fit(d) {
      if (!geo) return;
      if (!d) return fly(1, 0, 0);
      var k2 = Math.max(1.5, Math.min(7, Math.min(geo.w / (d.x1 - d.x0 + 260), geo.h / (d.y1 - d.y0 + 260)) * .8));
      fly(k2, geo.w / 2 - k2 * d.cx, geo.h / 2 - k2 * d.cy);
    }
    function pick(cx, cy) {
      var m = toMap(cx, cy), x = (m[0] - tx) / k, y = (m[1] - ty) / k;
      for (var i = 0; i < geo.ds.length; i++) if (inside(geo.ds[i], x, y)) return geo.ds[i].n;
      return '';
    }
    // one pointer pans (only when zoomed), two pointers pinch, a tap picks
    var ptrs = new Map(), pinch = 0, down = null;
    el.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.nmc')) return;
      ptrs.set(e.pointerId, [e.clientX, e.clientY]); moved = false; down = [e.clientX, e.clientY];
      if (ptrs.size === 2) { var a = Array.from(ptrs.values()); pinch = Math.hypot(a[0][0] - a[1][0], a[0][1] - a[1][1]); }
    });
    el.addEventListener('pointermove', function (e) {
      var p = ptrs.get(e.pointerId); if (!p || !geo) return;
      var dx = e.clientX - p[0], dy = e.clientY - p[1];
      if (!moved && Math.hypot(e.clientX - down[0], e.clientY - down[1]) < 6) return;
      moved = true; cancelAnimationFrame(raf);
      if (ptrs.size === 2) {
        ptrs.set(e.pointerId, [e.clientX, e.clientY]);
        var a = Array.from(ptrs.values()), dist = Math.hypot(a[0][0] - a[1][0], a[0][1] - a[1][1]);
        var c = toMap((a[0][0] + a[1][0]) / 2, (a[0][1] + a[1][1]) / 2); if (pinch) zoomAt(c[0], c[1], dist / pinch); pinch = dist;
      } else if (k > 1.02) { var b = base(); tx += dx / b; ty += dy / b; clamp(); view(); ptrs.set(e.pointerId, [e.clientX, e.clientY]); try { el.setPointerCapture(e.pointerId); } catch (_) {} }
    });
    var end = function (e) {
      if (!ptrs.has(e.pointerId)) return;
      var tap = !moved && ptrs.size === 1 && geo; ptrs.delete(e.pointerId); pinch = 0;
      if (tap && e.type === 'pointerup') { var n = pick(e.clientX, e.clientY); if (o.onPick) o.onPick(n === sel ? '' : n); }
    };
    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);
    el.addEventListener('wheel', function (e) {
      if (!geo || !(e.ctrlKey || e.metaKey)) return;
      e.preventDefault(); var m = toMap(e.clientX, e.clientY); zoomAt(m[0], m[1], e.deltaY < 0 ? 1.25 : .8);
    }, { passive: false });
    el.addEventListener('click', function (e) {
      var z = e.target.closest('[data-z]'); if (!z || !geo) return;
      var c = [(W / 2 - ox()) / base(), (H / 2 - oy()) / base()], f = z.dataset.z === 'in' ? 1.8 : 1 / 1.8, k2 = Math.max(1, Math.min(KMAX, k * f)), r = k2 / k;
      fly(k2, c[0] - (c[0] - tx) * r, c[1] - (c[1] - ty) * r);
    });
    var ro = g.ResizeObserver ? new ResizeObserver(function () { if (el.isConnected && geo) size(); }) : null;
    if (ro) ro.observe(el);
    get(function (G) { geo = G; if (!el.isConnected) return; size(); paint(); if (sel) fit(geo.by[sel]); });
    return {
      update: function (c, s) {
        counts = c; var changed = s !== sel; sel = s;
        if (geo) { paint(); if (changed) fit(geo.by[sel]); }
      }
    };
  }
  g.PWMAP = { mount: mount, get: get, PROV: PROV };
})(window);
