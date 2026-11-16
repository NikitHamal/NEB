/* Pathways: real map of Nepal (official 2020 boundary, 77 districts, 7 provinces).
   Data: static/web/data/nepal_map.json (see backend_python/tools/pathways/build_nepal_map.js), same file as Android.
   PW.mapCore({counts, selected, full, onPick}) returns {el, update(counts, selected), reset(), destroy()}.
   One SVG, one transformed group: pan and zoom only change one transform attribute. */
(function () {
  'use strict';
  var PW = window.PW, h = PW.h, icon = PW.icon;
  var NS = 'http://www.w3.org/2000/svg', KMAX = 16;
  var PROV = ['Koshi', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim'];
  var tag = document.querySelector('script[data-geo]'), geo = null, pending = null;
  function s(t, a) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); return e; }

  function dpath(rs, box) {
    return rs.map(function (r) {
      var x = r[0], y = r[1], p = ['M' + x + ' ' + y];
      for (var i = 2; i < r.length; i += 2) {
        x += r[i]; y += r[i + 1]; p.push(x + ' ' + y);
        if (box) { box[0] = Math.min(box[0], x); box[1] = Math.min(box[1], y); box[2] = Math.max(box[2], x); box[3] = Math.max(box[3], y); }
      }
      return p[0] + 'L' + p.slice(1).join('L') + 'Z';
    }).join('');
  }
  function load() {
    if (geo) return Promise.resolve(geo);
    if (!pending) pending = fetch(tag ? tag.getAttribute('data-geo') : '/static/web/data/nepal_map.json').then(function (r) { return r.json(); }).then(function (j) {
      var pc = PROV.map(function () { return [0, 0, 0]; });
      j.d.forEach(function (d) {
        d.box = [1e9, 1e9, -1e9, -1e9]; d.path = dpath(d.r, d.box); d.bw = d.box[2] - d.box[0];
        pc[d.p][0] += d.c[0]; pc[d.p][1] += d.c[1]; pc[d.p][2]++;
      });
      j.pc = pc.map(function (a) { return [a[0] / a[2], a[1] / a[2]]; });
      j.pvPath = j.pv.map(function (r) { return dpath(r); }); j.oPath = dpath(j.o);
      return (geo = j);
    });
    return pending;
  }
  function bin(n) { return n <= 0 ? 0 : n === 1 ? 1 : n < 4 ? 2 : n < 7 ? 3 : 4; }

  PW.mapCore = function (o) {
    var full = !!o.full, counts = o.counts || {}, sel = o.selected || '', G, st = { k: 1, x: 0, y: 0 };
    var paths = {}, labels = [], pvLabels = [], raf = 0, anim = 0, moved = false, ptrs = {}, last = null, hover = '';
    var svg = s('svg', { class: 'pw-map', preserveAspectRatio: 'xMidYMid meet', 'aria-label': 'Map of Nepal by district' });
    var vp = s('g'), info = h('div', { class: 'pw-geo-info', hidden: true });
    var el = h('div', { class: 'pw-geo' + (full ? ' full' : ' skel') }, [svg, info]);
    var selPath = s('path', { class: 'pw-sel' }), size = null;

    function dims() { var r = svg.getBoundingClientRect(); var sc = Math.min(r.width / G.w, r.height / G.h) || 1; return { r: r, sc: sc, ox: (r.width - G.w * sc) / 2, oy: (r.height - G.h * sc) / 2 }; }
    function clamp() {
      st.k = Math.max(1, Math.min(KMAX, st.k));
      var px = G.w * 0.25, py = G.h * 0.25;
      st.x = Math.max(G.w - G.w * st.k - px, Math.min(px, st.x)); st.y = Math.max(G.h - G.h * st.k - py, Math.min(py, st.y));
    }
    function paint() {
      raf = 0; clamp(); var d = size || (size = dims());
      vp.setAttribute('transform', 'translate(' + st.x.toFixed(1) + ' ' + st.y.toFixed(1) + ') scale(' + st.k.toFixed(3) + ')');
      svg.style.setProperty('--u', (1 / (d.sc * st.k)).toFixed(4));
      labels.forEach(function (l) { var on = l.d.bw * st.k * d.sc > l.w * 6.2 || l.d.n === sel; if (on !== l.on) { l.on = on; l.t.style.display = on ? '' : 'none'; } });
      var pOn = st.k < 2.6; pvLabels.forEach(function (t) { t.style.display = pOn ? '' : 'none'; });
      el.classList.toggle('zoomed', st.k > 1.02);
    }
    function draw() { if (!raf) raf = requestAnimationFrame(paint); }
    function toSvg(cx, cy) { var d = size || (size = dims()); return [(cx - d.r.left - d.ox) / d.sc, (cy - d.r.top - d.oy) / d.sc]; }
    function zoomAt(px, py, f) { var k2 = Math.max(1, Math.min(KMAX, st.k * f)), r = k2 / st.k; st.x = px - (px - st.x) * r; st.y = py - (py - st.y) * r; st.k = k2; draw(); }
    function fly(k, x, y) {
      cancelAnimationFrame(anim); var a = { k: st.k, x: st.x, y: st.y }, t0 = performance.now();
      if (matchMedia('(prefers-reduced-motion: reduce)').matches) { st.k = k; st.x = x; st.y = y; draw(); return; }
      (function step(t) {
        var p = Math.min(1, (t - t0) / 380), e = 1 - Math.pow(1 - p, 3);
        st.k = a.k + (k - a.k) * e; st.x = a.x + (x - a.x) * e; st.y = a.y + (y - a.y) * e; paint();
        if (p < 1) anim = requestAnimationFrame(step);
      })(t0);
    }
    function reset() { fly(1, 0, 0); }
    function fit(d) {
      var bw = d.box[2] - d.box[0], bh = d.box[3] - d.box[1], k = Math.max(1.6, Math.min(7, 0.55 * Math.min(G.w / bw, G.h / bh)));
      fly(k, G.w / 2 - k * (d.box[0] + bw / 2), G.h / 2 - k * (d.box[1] + bh / 2));
    }
    function shape() {
      G.d.forEach(function (d) { var n = counts[d.n] || 0; paths[d.n].setAttribute('class', 'pw-dist pwl' + bin(n)); });
      var d = sel && G.d.filter(function (x) { return x.n === sel; })[0];
      selPath.setAttribute('d', d ? d.path : ''); selPath.style.display = d ? '' : 'none';
      var who = d || (hover && G.d.filter(function (x) { return x.n === hover; })[0]);
      info.hidden = !who;
      if (who) {
        var n = counts[who.n] || 0; info.textContent = '';
        info.appendChild(h('b', { text: who.n })); info.appendChild(h('small', { text: PROV[who.p] + (who.hq ? ' · ' + who.hq : '') }));
        info.appendChild(h('span', { class: 'pw-geo-n', text: n + (n === 1 ? ' college' : ' colleges') }));
      }
    }
    function pick(n) { if (o.onPick) o.onPick(n === sel ? '' : n); }
    function build() {
      svg.setAttribute('viewBox', '0 0 ' + G.w + ' ' + G.h); el.classList.remove('skel'); el.style.aspectRatio = full ? '' : G.w + ' / ' + G.h;
      var dg = s('g'); G.d.forEach(function (d) { var p = s('path', { d: d.path, class: 'pw-dist' }); p.dataset.n = d.n; paths[d.n] = p; dg.appendChild(p); });
      vp.appendChild(dg);
      G.pvPath.forEach(function (d) { vp.appendChild(s('path', { d: d, class: 'pw-prov' })); });
      vp.appendChild(s('path', { d: G.oPath, class: 'pw-out' })); vp.appendChild(selPath);
      var lg = s('g', { class: 'pw-lbls' });
      G.d.forEach(function (d) { var t = s('text', { x: d.c[0], y: d.c[1], class: 'pw-lbl' }); t.textContent = d.n; t.style.display = 'none'; lg.appendChild(t); labels.push({ d: d, t: t, w: d.n.length, on: false }); });
      PROV.forEach(function (n, i) { var t = s('text', { x: G.pc[i][0], y: G.pc[i][1], class: 'pw-plbl' }); t.textContent = n; lg.appendChild(t); pvLabels.push(t); });
      vp.appendChild(lg); svg.appendChild(vp);
      var ctl = h('div', { class: 'pw-geo-ctl' }, [
        ctrl('add', 'Zoom in', function () { var c = toSvg(size.r.left + size.r.width / 2, size.r.top + size.r.height / 2); zoomAt(c[0], c[1], 1.7); }),
        ctrl('remove', 'Zoom out', function () { var c = toSvg(size.r.left + size.r.width / 2, size.r.top + size.r.height / 2); zoomAt(c[0], c[1], 1 / 1.7); }),
        ctrl('center_focus_strong', 'Reset view', reset),
      ]);
      el.appendChild(ctl); if (o.extra) ctl.appendChild(o.extra);
      shape(); paint(); if (sel) fit(G.d.filter(function (x) { return x.n === sel; })[0]);
    }
    function ctrl(g, label, fn) { size = size || dims(); var b = h('button', { class: 'pw-round sm', type: 'button', 'aria-label': label }, [icon(g)]); b.addEventListener('click', function () { size = dims(); fn(); }); return b; }

    /* pointer: one finger or mouse pans, two fingers pinch, tap picks. Inline on touch, the page keeps its scroll. */
    function touchOk(e) { return full || e.pointerType !== 'touch'; }
    svg.addEventListener('pointerdown', function (e) {
      if (!G || !touchOk(e)) return; size = dims(); ptrs[e.pointerId] = [e.clientX, e.clientY]; moved = false; last = null; cancelAnimationFrame(anim);
    });
    svg.addEventListener('pointermove', function (e) {
      if (!G) return; var q = ptrs[e.pointerId];
      if (!q) { if (e.pointerType === 'mouse') { var t = e.target.dataset && e.target.dataset.n || ''; if (t !== hover) { hover = t; shape(); } } return; }
      var ids = Object.keys(ptrs), d = size || (size = dims());
      if (ids.length >= 2) {
        var o2 = ptrs[ids[0] === String(e.pointerId) ? ids[1] : ids[0]], a = Math.hypot(q[0] - o2[0], q[1] - o2[1]);
        ptrs[e.pointerId] = [e.clientX, e.clientY];
        var b = Math.hypot(e.clientX - o2[0], e.clientY - o2[1]), c = toSvg((e.clientX + o2[0]) / 2, (e.clientY + o2[1]) / 2);
        if (a > 8) zoomAt(c[0], c[1], b / a); moved = true; return;
      }
      var dx = e.clientX - q[0], dy = e.clientY - q[1];
      if (!moved && Math.hypot(dx, dy) < 5) return;
      if (!moved) { moved = true; try { svg.setPointerCapture(e.pointerId); } catch (x) {} el.classList.add('drag'); }
      ptrs[e.pointerId] = [e.clientX, e.clientY]; st.x += dx / d.sc; st.y += dy / d.sc; draw();
    });
    function up(e) { delete ptrs[e.pointerId]; if (!Object.keys(ptrs).length) { el.classList.remove('drag'); setTimeout(function () { moved = false; }, 0); } }
    svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && hover) { hover = ''; if (G) shape(); } });
    svg.addEventListener('click', function (e) { if (moved) return; var n = e.target.dataset && e.target.dataset.n; if (n) pick(n); else if (sel && o.onPick) o.onPick(''); });
    svg.addEventListener('dblclick', function (e) { if (!G) return; size = dims(); var c = toSvg(e.clientX, e.clientY); zoomAt(c[0], c[1], 2); });
    svg.addEventListener('wheel', function (e) {
      if (!G || !(full || e.ctrlKey || e.metaKey)) return; e.preventDefault(); size = dims();
      var c = toSvg(e.clientX, e.clientY); zoomAt(c[0], c[1], Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0022)));
    }, { passive: false });
    window.addEventListener('resize', onResize); function onResize() { size = null; if (G) draw(); }

    load().then(function (j) { G = j; build(); }).catch(function () { el.classList.remove('skel'); el.appendChild(PW.empty('The map could not load.')); });
    return {
      el: el,
      update: function (c, d) { counts = c || {}; var ch = d !== sel; sel = d || ''; if (!G) return; shape(); if (ch) { if (sel) fit(G.d.filter(function (x) { return x.n === sel; })[0]); else reset(); } },
      reset: reset,
      destroy: function () { window.removeEventListener('resize', onResize); cancelAnimationFrame(anim); cancelAnimationFrame(raf); },
    };
  };
})();
