/* NebPdfKit: everything the two PDF readers (pdf-book.js, pdf-reader.js) share, so neither carries its own copy.
   - sfx      synthesized page sounds (WebAudio, no files): paper turn, flurry, thud, cover, ticks, chimes
   - speech   read aloud (speechSynthesis), sentence by sentence
   - store    resume point, furthest page, reading time, bookmarks (localStorage, one key per file)
   - ink      pen / highlighter strokes per page, stored as 0..1 coordinates, painted on a canvas overlay
   - text     lazy text index of the document: search, highlight rectangles (only a few pages keep full geometry)
   - thumbs   small page images, one render queue (newest request first), small LRU
   - panels   Pages / Contents / Search / Bookmarks side panel;   scrubber, settings sheet, ink bar, help, toast
   All UI is flat (no shadows), tonal M3 role pairs. ES5 on purpose: the static bundle is minified without transpiling. */
(function () {
  'use strict';
  var D = document, W = window;
  var K = {};

  /* ------------------------------------------------------------------ small helpers */
  K.reduced = !!(W.matchMedia && W.matchMedia('(prefers-reduced-motion: reduce)').matches);
  K.el = function (tag, cls, html) {
    var n = D.createElement(tag);
    if (cls) n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  };
  K.icon = function (name) { return '<span class="material-symbols-outlined" aria-hidden="true">' + name + '</span>'; };
  K.clamp = function (v, a, b) { return v < a ? a : (v > b ? b : v); };
  K.jget = function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } };
  K.jset = function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode or full */ } };
  K.ease = {
    inOut: function (k) { return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; },
    out: function (k) { return 1 - Math.pow(1 - k, 3); },
    outBack: function (k) { var c = 1.4; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); }
  };
  K.btn = function (cls, ic, label, extra) {
    return '<button type="button" class="' + cls + '" aria-label="' + label + '" title="' + label + '"' + (extra || '') + '>' + K.icon(ic) + '</button>';
  };
  K.setLabel = function (b, t) { b.title = t; b.setAttribute('aria-label', t); };
  K.restart = function (n, cls) { n.classList.remove(cls); void n.offsetWidth; n.classList.add(cls); };
  /* Pixels we allow all page canvases together: scaled to the device so a phone does not run out. */
  K.budget = function () {
    var gb = navigator.deviceMemory || 4;
    return Math.max(56, Math.min(190, gb * 28)) * 1048576;
  };
  K.toneFilter = function (p) {
    var f = p.tone === 'night' ? 'invert(.9) hue-rotate(180deg) contrast(.92)' : (p.tone === 'sepia' ? 'sepia(.4) saturate(1.05) contrast(.95)' : '');
    if (p.warm > 0) f += ' sepia(' + (p.warm / 100).toFixed(2) + ')';
    f += ' brightness(' + (p.bright / 100).toFixed(2) + ')';
    return f.trim() || 'none';
  };

  /* ------------------------------------------------------------------ sound */
  K.sfx = (function () {
    var KEY = 'neb.pdf.sfx';
    var st = Object.assign({ on: true, vol: 0.7 }, K.jget(KEY) || {});
    var ctx = null, master = null, noiseBuf = null, lastTick = 0;

    function ac() {
      if (!st.on || st.vol <= 0) return null;
      try {
        if (!ctx) {
          var C = W.AudioContext || W.webkitAudioContext;
          if (!C) return null;
          ctx = new C();
          master = ctx.createGain();
          var comp = ctx.createDynamicsCompressor();
          comp.threshold.value = -16; comp.ratio.value = 4;
          master.connect(comp); comp.connect(ctx.destination);
        }
        if (ctx.state === 'suspended') ctx.resume();
        master.gain.value = Math.pow(st.vol, 1.7) * 1.4;
        return ctx;
      } catch (e) { return null; }
    }
    function noise(c) {
      if (noiseBuf) return noiseBuf;
      var len = Math.floor(c.sampleRate * 1.6), b = c.createBuffer(1, len, c.sampleRate), d = b.getChannelData(0);
      var b0 = 0, b1 = 0, b2 = 0, i, w;
      for (i = 0; i < len; i++) { w = Math.random() * 2 - 1; b0 = 0.99765 * b0 + w * 0.099046; b1 = 0.963 * b1 + w * 0.2965164; b2 = 0.57 * b2 + w * 1.0526913; d[i] = (b0 + b1 + b2 + w * 0.1848) * 0.28; }
      noiseBuf = b;
      return b;
    }
    function route(c, node, pan) {
      if (pan && c.createStereoPanner) { var p = c.createStereoPanner(); p.pan.value = K.clamp(pan, -1, 1); node.connect(p); p.connect(master); } else node.connect(master);
    }
    /* A burst of filtered noise: the building block of every paper sound. */
    function nz(c, t, dur, o) {
      var s = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain(), at = o.at || 0.15;
      s.buffer = noise(c);
      f.type = o.type || 'bandpass'; f.Q.value = o.q || 0.8;
      f.frequency.setValueAtTime(o.f0, t);
      f.frequency.exponentialRampToValueAtTime(Math.max(40, o.f1 || o.f0), t + dur);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(Math.max(0.0002, o.gain), t + Math.max(0.004, dur * at));
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      s.connect(f); f.connect(g); route(c, g, o.pan);
      s.start(t, Math.random() * 0.5, dur + 0.05);
    }
    function tone(c, t, f0, f1, dur, gain, type, pan) {
      var o = c.createOscillator(), g = c.createGain();
      o.type = type || 'sine';
      o.frequency.setValueAtTime(f0, t);
      o.frequency.exponentialRampToValueAtTime(Math.max(30, f1), t + dur);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(gain, t + Math.min(0.012, dur / 3));
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g); route(c, g, pan);
      o.start(t); o.stop(t + dur + 0.03);
    }
    function paper(c, t, dur, gain, dir) {
      var pan = (dir || 0) * 0.35, i, n = 4 + Math.floor(Math.random() * 5), tc;
      nz(c, t, dur, { f0: 1100, f1: 3900, q: 0.55, gain: 0.17 * gain, at: 0.4, pan: pan });
      nz(c, t + dur * 0.08, dur * 0.8, { type: 'highpass', f0: 4800, f1: 2400, q: 0.5, gain: 0.05 * gain, at: 0.5, pan: pan });
      nz(c, t, dur * 0.7, { type: 'lowpass', f0: 700, f1: 260, q: 0.5, gain: 0.07 * gain, at: 0.3, pan: pan });
      for (i = 0; i < n; i++) {
        tc = t + dur * (0.04 + Math.random() * 0.8);
        nz(c, tc, 0.01 + Math.random() * 0.025, { f0: 2400 + Math.random() * 3600, q: 1.4, gain: (0.08 + Math.random() * 0.1) * gain, at: 0.1, pan: pan });
      }
    }
    var api = {
      state: st,
      set: function (k, v) { st[k] = v; K.jset(KEY, st); },
      /* speed 1 = normal turn (~0.8 s); dir +1 forward, -1 back */
      turn: function (speed, dir, gain) {
        var c = ac(); if (!c) return;
        paper(c, c.currentTime + 0.005, K.clamp(0.62 / (speed || 1), 0.26, 1.2), gain || 1, dir);
      },
      land: function (dir, gain) {
        var c = ac(); if (!c) return; var t = c.currentTime + 0.005, g = gain || 1;
        nz(c, t, 0.12, { type: 'lowpass', f0: 420, f1: 110, q: 0.7, gain: 0.26 * g, at: 0.08, pan: (dir || 0) * 0.3 });
        nz(c, t, 0.05, { f0: 1700, f1: 900, q: 0.9, gain: 0.07 * g, at: 0.1, pan: (dir || 0) * 0.3 });
        tone(c, t, 120, 52, 0.1, 0.1 * g, 'sine');
      },
      flurry: function (n, dir) {
        var c = ac(); if (!c) return; var i, t = c.currentTime + 0.005;
        for (i = 0; i < Math.min(n, 9); i++) paper(c, t + i * 0.075, 0.2 + Math.random() * 0.06, 0.8 - i * 0.04, dir);
      },
      cover: function (open) {
        var c = ac(); if (!c) return; var t = c.currentTime + 0.005, o = c.createOscillator(), f = c.createBiquadFilter(), g = c.createGain(), lfo = c.createOscillator(), lg = c.createGain();
        o.type = 'sawtooth'; o.frequency.setValueAtTime(open ? 72 : 118, t); o.frequency.exponentialRampToValueAtTime(open ? 124 : 66, t + 0.5);
        f.type = 'bandpass'; f.Q.value = 3; f.frequency.setValueAtTime(open ? 240 : 420, t); f.frequency.exponentialRampToValueAtTime(open ? 520 : 200, t + 0.5);
        lfo.frequency.value = 38; lg.gain.value = 0.02; lfo.connect(lg); lg.connect(g.gain);
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.05, t + 0.12); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.52);
        o.connect(f); f.connect(g); g.connect(master);
        o.start(t); lfo.start(t); o.stop(t + 0.56); lfo.stop(t + 0.56);
        paper(c, t + (open ? 0.06 : 0.22), 0.4, 1.1, open ? 1 : -1);
        nz(c, t + (open ? 0.5 : 0.46), 0.2, { type: 'lowpass', f0: 380, f1: 70, q: 0.7, gain: 0.45, at: 0.05 });
        tone(c, t + (open ? 0.5 : 0.46), 95, 38, 0.2, 0.2, 'sine');
      },
      bump: function (dir) {
        var c = ac(); if (!c) return; var t = c.currentTime + 0.005;
        tone(c, t, 96, 54, 0.14, 0.2, 'sine', (dir || 0) * 0.4);
        nz(c, t, 0.08, { type: 'lowpass', f0: 300, f1: 100, gain: 0.16, at: 0.05 });
      },
      tick: function () {
        var now = Date.now(); if (now - lastTick < 30) return; lastTick = now;
        var c = ac(); if (!c) return; tone(c, c.currentTime + 0.002, 1500, 880, 0.04, 0.05, 'triangle');
      },
      pop: function (on) {
        var c = ac(); if (!c) return; var t = c.currentTime + 0.002;
        if (on) { tone(c, t, 560, 840, 0.09, 0.06, 'sine'); tone(c, t + 0.06, 840, 1120, 0.1, 0.05, 'sine'); } else { tone(c, t, 840, 520, 0.1, 0.05, 'sine'); }
      },
      chime: function (add) {
        var c = ac(); if (!c) return; var t = c.currentTime + 0.002;
        if (add) { tone(c, t, 988, 988, 0.7, 0.07, 'sine'); tone(c, t + 0.06, 1480, 1480, 0.6, 0.05, 'sine'); tone(c, t + 0.12, 1976, 1976, 0.5, 0.03, 'sine'); } else { tone(c, t, 740, 494, 0.2, 0.06, 'sine'); }
      },
      zoom: function (up) {
        var c = ac(); if (!c) return; tone(c, c.currentTime + 0.002, up ? 520 : 760, up ? 760 : 520, 0.08, 0.045, 'sine');
      },
      pen: function () {
        var c = ac(); if (!c) return; nz(c, c.currentTime + 0.002, 0.07, { f0: 3200, f1: 2200, q: 1.2, gain: 0.05, at: 0.2 });
      },
      erase: function () {
        var c = ac(); if (!c) return; nz(c, c.currentTime + 0.002, 0.12, { f0: 900, f1: 1800, q: 0.9, gain: 0.06, at: 0.3 });
      },
      close: function () { if (ctx) { try { ctx.close(); } catch (e) { /* closed */ } ctx = null; master = null; noiseBuf = null; } }
    };
    return api;
  })();

  /* ------------------------------------------------------------------ read aloud */
  K.speech = (function () {
    var ok = !!(W.speechSynthesis && W.SpeechSynthesisUtterance), token = 0, on = false;
    function chunks(text) {
      var parts = (text || '').replace(/\s+/g, ' ').match(/[^.!?\u0964]+[.!?\u0964]*\s*/g) || [], out = [], cur = '';
      parts.forEach(function (p) {
        if ((cur + p).length > 170 && cur) { out.push(cur); cur = p; } else cur += p;
      });
      if (cur.trim()) out.push(cur);
      return out;
    }
    return {
      ok: ok,
      active: function () { return on; },
      speak: function (text, rate, done) {
        if (!ok) { if (done) done(); return; }
        var my = ++token, list = chunks(text), i = 0;
        speechSynthesis.cancel(); on = true;
        (function next() {
          if (my !== token) return;
          if (i >= list.length) { if (done) done(); return; }
          var u = new SpeechSynthesisUtterance(list[i++]);
          u.rate = rate || 1; u.onend = next; u.onerror = function () { if (my === token && done) done(); };
          speechSynthesis.speak(u);
        })();
      },
      stop: function () { token++; on = false; if (ok) speechSynthesis.cancel(); }
    };
  })();

  /* ------------------------------------------------------------------ reading state */
  K.store = function (src) {
    var key = 'neb.book.doc:' + src, d = Object.assign({ last: 1, max: 1, time: 0, marks: [] }, K.jget(key) || {}), dirty = false, t = 0;
    var api = {
      d: d,
      save: function () { clearTimeout(t); t = 0; if (dirty) { K.jset(key, d); dirty = false; } },
      soon: function () { dirty = true; if (!t) t = setTimeout(api.save, 1500); },
      isMarked: function (n) { return d.marks.some(function (m) { return m.p === n; }); },
      /* bookmark every page of the current view, or clear them when any is set */
      toggle: function (pages, first) {
        var on = pages.filter(api.isMarked);
        if (on.length) d.marks = d.marks.filter(function (m) { return on.indexOf(m.p) === -1; });
        else d.marks.push({ p: first, note: '', at: Date.now() });
        dirty = true; api.save();
        return on.length ? 'removed' : 'added';
      }
    };
    return api;
  };
  /* Counts reading seconds while the reader is on screen and was used in the last 90 s. */
  K.session = function (store, root, every) {
    var idle = Date.now(), timer = setInterval(function () {
      if (!D.hidden && root.isConnected && Date.now() - idle < 90000) { store.d.time++; store.soon(); }
      if (every) every(store.d.time);
    }, 1000);
    function hide() { store.save(); }
    W.addEventListener('pagehide', hide);
    return {
      touch: function () { idle = Date.now(); },
      stop: function () { clearInterval(timer); W.removeEventListener('pagehide', hide); store.save(); }
    };
  };

  /* ------------------------------------------------------------------ ink (pen and highlighter) */
  K.INK = {
    pen: { colors: ['#202124', '#d93025', '#1a73e8', '#188038', '#e8710a', '#c2185b'], widths: { s: 1.6, m: 3.2, l: 6.5 } },
    hl: { colors: ['#ffd23f', '#7be495', '#ff9ec4', '#ffb257', '#6fd9e8'], widths: { s: 9, m: 15, l: 26 } }
  };
  K.drawStrokes = function (ctx, strokes, w, h) {
    var i, j, s, p;
    for (i = 0; i < strokes.length; i++) {
      s = strokes[i]; p = s.p;
      if (!p || p.length < 2) continue;
      ctx.save();
      ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.strokeStyle = s.c; ctx.globalAlpha = s.t === 'hl' ? 0.4 : 1;
      ctx.lineWidth = Math.max(1, s.w * w / 1000);
      ctx.beginPath();
      ctx.moveTo(p[0] * w, p[1] * h);
      if (p.length === 2) ctx.lineTo(p[0] * w + 0.1, p[1] * h);
      for (j = 2; j < p.length - 2; j += 2) ctx.quadraticCurveTo(p[j] * w, p[j + 1] * h, (p[j] + p[j + 2]) / 2 * w, (p[j + 1] + p[j + 3]) / 2 * h);
      if (p.length > 3) ctx.lineTo(p[p.length - 2] * w, p[p.length - 1] * h);
      ctx.stroke();
      ctx.restore();
    }
  };
  K.paintInk = function (cv, strokes) {
    var ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    if (strokes.length) K.drawStrokes(ctx, strokes, cv.width, cv.height);
  };
  K.ink = function (src) {
    var key = 'neb.pdf.ink:' + src, all = K.jget(key) || {}, t = 0, subs = [];
    function save() { clearTimeout(t); t = 0; K.jset(key, all); }
    function soon() { if (!t) t = setTimeout(save, 700); }
    function fire(n) { subs.forEach(function (f) { f(n); }); }
    return {
      get: function (n) { return all[n] || []; },
      has: function (n) { return !!(all[n] && all[n].length); },
      pages: function () { return Object.keys(all).filter(function (n) { return all[n].length; }).length; },
      add: function (n, s) { (all[n] = all[n] || []).push(s); soon(); fire(n); },
      undo: function (n) { if (all[n] && all[n].length) { all[n].pop(); soon(); fire(n); return true; } return false; },
      clear: function (n) { if (all[n] && all[n].length) { delete all[n]; soon(); fire(n); return true; } return false; },
      /* removes strokes that pass within r of (x, y); ar = page height / width keeps the eraser round */
      erase: function (n, x, y, r, ar) {
        var list = all[n]; if (!list) return false;
        var keep = list.filter(function (s) {
          for (var i = 0; i < s.p.length; i += 2) { var dx = s.p[i] - x, dy = (s.p[i + 1] - y) * ar; if (dx * dx + dy * dy < r * r) return false; }
          return true;
        });
        if (keep.length === list.length) return false;
        if (keep.length) all[n] = keep; else delete all[n];
        soon(); fire(n); return true;
      },
      on: function (f) { subs.push(f); },
      flush: save
    };
  };
  /* Makes a canvas overlay take strokes. o: { n(): page, ink, tool(): {t, c, w}, active(): bool, ratio(): h/w } */
  K.inkBind = function (cv, o) {
    var cur = null, raf = 0, id = -1;
    function pt(e) { var r = cv.getBoundingClientRect(); return [K.clamp((e.clientX - r.left) / r.width, 0, 1), K.clamp((e.clientY - r.top) / r.height, 0, 1)]; }
    function repaint() { raf = 0; K.paintInk(cv, o.ink.get(o.n()).concat(cur && cur.t !== 'eraser' ? [cur] : [])); }
    function later() { if (!raf) raf = requestAnimationFrame(repaint); }
    cv.addEventListener('pointerdown', function (e) {
      if (!o.active() || e.button > 0) return;
      e.preventDefault(); e.stopPropagation();
      var tool = o.tool(), p = pt(e);
      id = e.pointerId;
      try { cv.setPointerCapture(id); } catch (x) { /* fine */ }
      if (tool.t === 'eraser') { cur = { t: 'eraser' }; if (o.ink.erase(o.n(), p[0], p[1], 0.022, o.ratio())) K.sfx.erase(); return; }
      cur = { t: tool.t, c: tool.c, w: tool.w, p: [+p[0].toFixed(4), +p[1].toFixed(4)] };
      K.sfx.pen(); later();
    });
    cv.addEventListener('pointermove', function (e) {
      if (!cur || e.pointerId !== id) return;
      e.stopPropagation();
      var p = pt(e);
      if (cur.t === 'eraser') { if (o.ink.erase(o.n(), p[0], p[1], 0.022, o.ratio())) K.sfx.erase(); return; }
      var l = cur.p, dx = p[0] - l[l.length - 2], dy = (p[1] - l[l.length - 1]) * o.ratio();
      if (dx * dx + dy * dy < 0.000004) return;
      l.push(+p[0].toFixed(4), +p[1].toFixed(4));
      later();
    });
    function end(e) {
      if (!cur || e.pointerId !== id) return;
      e.stopPropagation();
      var s = cur; cur = null; id = -1;
      if (s.t !== 'eraser' && s.p.length >= 2) o.ink.add(o.n(), s); else later();
    }
    cv.addEventListener('pointerup', end);
    cv.addEventListener('pointercancel', end);
  };
  /* Pen / highlighter / eraser, colours, size, undo, clear, done. Returns { el, tool(), sync(), show(b) }. */
  K.inkBar = function (o) {
    var st = { t: 'pen', pc: K.INK.pen.colors[1], hc: K.INK.hl.colors[0], s: 'm' };
    var bar = K.el('div', 'nx-inkbar nx-ui');
    bar.hidden = true;
    bar.setAttribute('role', 'toolbar'); bar.setAttribute('aria-label', 'Annotate');
    function html() {
      var hl = st.t === 'hl', er = st.t === 'eraser', pal = hl ? K.INK.hl.colors : K.INK.pen.colors, cur = hl ? st.hc : st.pc;
      return '<div class="nx-grp">' +
        K.btn('nx-ib' + (st.t === 'pen' ? ' is-on' : ''), 'draw', 'Pen', ' data-ink="pen"') +
        K.btn('nx-ib' + (hl ? ' is-on' : ''), 'highlight', 'Highlighter', ' data-ink="hl"') +
        K.btn('nx-ib' + (er ? ' is-on' : ''), 'ink_eraser', 'Eraser', ' data-ink="eraser"') + '</div>' +
        (er ? '' : '<div class="nx-grp nx-pal">' + pal.map(function (c) { return '<button type="button" class="nx-dot' + (c === cur ? ' is-on' : '') + '" style="--c:' + c + '" data-c="' + c + '" aria-label="Colour ' + c + '"></button>'; }).join('') + '</div>' +
          '<div class="nx-grp nx-sz">' + ['s', 'm', 'l'].map(function (z) { return '<button type="button" class="nx-sz-b' + (z === st.s ? ' is-on' : '') + '" data-s="' + z + '" aria-label="Size ' + z + '"><i style="--d:' + (z === 's' ? 5 : (z === 'm' ? 9 : 14)) + 'px"></i></button>'; }).join('') + '</div>') +
        '<div class="nx-grp">' + K.btn('nx-ib', 'undo', 'Undo stroke', ' data-ink-act="undo"') + K.btn('nx-ib', 'delete_sweep', 'Clear this page', ' data-ink-act="clear"') +
        K.btn('nx-ib nx-done', 'check', 'Finish annotating', ' data-ink-act="done"') + '</div>';
    }
    function paint() { bar.innerHTML = html(); }
    bar.addEventListener('click', function (e) {
      var t = e.target.closest('button'); if (!t) return;
      if (t.dataset.ink) { st.t = t.dataset.ink; paint(); K.sfx.tick(); if (o.onTool) o.onTool(); }
      else if (t.dataset.c) { if (st.t === 'hl') st.hc = t.dataset.c; else st.pc = t.dataset.c; paint(); K.sfx.tick(); }
      else if (t.dataset.s) { st.s = t.dataset.s; paint(); K.sfx.tick(); }
      else if (t.dataset.inkAct) o.onAct(t.dataset.inkAct);
    });
    paint();
    return {
      el: bar,
      tool: function () {
        if (st.t === 'eraser') return { t: 'eraser' };
        return { t: st.t, c: st.t === 'hl' ? st.hc : st.pc, w: K.INK[st.t].widths[st.s] };
      },
      show: function (on) { bar.hidden = !on; if (on) { paint(); K.restart(bar, 'is-in'); } }
    };
  };

  /* ------------------------------------------------------------------ text index, search, highlights */
  K.text = function (doc) {
    var lite = {}, full = {}, fullOrder = [], running = false, done = 0, alive = true;
    var mctx = D.createElement('canvas').getContext('2d');
    function load(n) {
      return doc.getPage(n).then(function (page) {
        var vp = page.getViewport({ scale: 1 });
        return page.getTextContent().then(function (tc) {
          var items = [], offs = [], str = '', i, it;
          for (i = 0; i < tc.items.length; i++) {
            it = tc.items[i];
            if (typeof it.str !== 'string') continue;
            offs.push(str.length); items.push(it);
            str += it.str + ' ';
          }
          return { vp: vp, items: items, offs: offs, str: str, low: str.toLowerCase(), styles: tc.styles || {} };
        });
      }).catch(function () { return { vp: null, items: [], offs: [], str: '', low: '', styles: {} }; });
    }
    function info(n) {
      if (full[n]) return full[n];
      var p = load(n).then(function (inf) { lite[n] = { str: inf.str, low: inf.low }; return inf; });
      full[n] = p; fullOrder.push(n);
      if (fullOrder.length > 20) delete full[fullOrder.shift()];
      return p;
    }
    /* normalized rectangles (0..1 of the page) for every match of q on a page */
    function rects(inf, q) {
      var out = [], low = q.toLowerCase(), from = 0, idx, k, it, s0, e0, vp = inf.vp;
      if (!vp) return out;
      while ((idx = inf.low.indexOf(low, from)) !== -1 && out.length < 90) {
        from = idx + low.length;
        for (k = 0; k < inf.items.length; k++) {
          it = inf.items[k]; s0 = inf.offs[k]; e0 = s0 + it.str.length;
          if (!it.str.length || e0 <= idx || s0 >= from) continue;
          var ia = Math.max(idx, s0) - s0, ib = Math.min(from, e0) - s0, f0 = ia / it.str.length, f1 = ib / it.str.length;
          mctx.font = Math.abs(it.transform[3] || it.height || 10) + 'px ' + ((inf.styles[it.fontName] || {}).fontFamily || 'sans-serif');
          var wd = mctx.measureText(it.str).width;
          if (wd > 0) { f0 = mctx.measureText(it.str.slice(0, ia)).width / wd; f1 = mctx.measureText(it.str.slice(0, ib)).width / wd; }
          var h = it.height || Math.hypot(it.transform[2], it.transform[3]) || 10;
          var p1 = vp.convertToViewportPoint(it.transform[4] + f0 * it.width, it.transform[5] - 0.2 * h);
          var p2 = vp.convertToViewportPoint(it.transform[4] + f1 * it.width, it.transform[5] + 0.85 * h);
          out.push({ x: Math.min(p1[0], p2[0]) / vp.width, y: Math.min(p1[1], p2[1]) / vp.height, w: Math.abs(p2[0] - p1[0]) / vp.width, h: Math.abs(p2[1] - p1[1]) / vp.height });
        }
      }
      return out;
    }
    /* Fills a .nx-hls box with the matches of q */
    function paintHits(box, n, q, still) {
      box.innerHTML = '';
      if (!q || q.length < 2) return;
      info(n).then(function (inf) {
        if (!alive || (still && !still()) || !inf.vp) return;
        box.innerHTML = '';
        rects(inf, q).forEach(function (r) {
          var m = K.el('i', 'nx-hl');
          m.style.left = (r.x * 100) + '%'; m.style.top = (r.y * 100) + '%'; m.style.width = (r.w * 100) + '%'; m.style.height = (r.h * 100) + '%';
          box.appendChild(m);
        });
      });
    }
    function indexAll(step) {
      if (running || done >= doc.numPages) return;
      running = true;
      (function next() {
        if (!alive || done >= doc.numPages) { running = false; if (step) step(done); return; }
        var n = ++done;
        info(n).then(function () {
          if (step && (n % 20 === 0 || n === doc.numPages)) step(done);
          if (n % 4 === 0) setTimeout(next, 0); else next();
        });
      })();
    }
    function search(q) {
      q = q.toLowerCase();
      var res = [], n, from, idx, count;
      for (n = 1; n <= done; n++) {
        var l = lite[n]; if (!l) continue;
        from = 0; count = 0;
        while ((idx = l.low.indexOf(q, from)) !== -1 && count < 3 && res.length < 400) { res.push({ p: n, idx: idx, str: l.str }); from = idx + q.length; count++; }
      }
      return res;
    }
    return {
      info: info, rects: rects, paintHits: paintHits, indexAll: indexAll, search: search,
      progress: function () { return done; },
      /* the plain text of a page, for reading aloud */
      plain: function (n) { return info(n).then(function (inf) { return inf.str; }); },
      stop: function () { alive = false; }
    };
  };

  /* ------------------------------------------------------------------ thumbnails */
  K.thumbs = function (doc, width) {
    var cache = new Map(), jobs = {}, queue = [], busy = false, alive = true;
    function pump() {
      if (busy || !queue.length || !alive) return;
      var job = queue.pop();
      delete jobs[job.n];
      if (!job.live()) { pump(); return; }
      busy = true;
      doc.getPage(job.n).then(function (page) {
        var v1 = page.getViewport({ scale: 1 }), w = width * Math.min(W.devicePixelRatio || 1, 2), vp = page.getViewport({ scale: w / v1.width });
        var c = D.createElement('canvas');
        c.width = Math.floor(vp.width); c.height = Math.floor(vp.height);
        var ctx = c.getContext('2d');
        ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height);
        return page.render({ canvasContext: ctx, viewport: vp }).promise.then(function () {
          cache.set(job.n, c);
          if (cache.size > 90) { var first = cache.keys().next().value; cache.get(first).width = 0; cache.delete(first); }
          job.cbs.forEach(function (cb) { cb(c); });
          try { page.cleanup(); } catch (e) { /* page already released */ }
        });
      }).catch(function () { /* the thumbnail stays blank */ }).then(function () { busy = false; setTimeout(pump, 8); });
    }
    function copy(src) {
      var c = D.createElement('canvas');
      c.width = src.width; c.height = src.height;
      c.getContext('2d').drawImage(src, 0, 0);
      return c;
    }
    function get(n, cb, live) {
      var hit = cache.get(n);
      if (hit) { cb(copy(hit)); return; }
      var job = jobs[n];
      if (job) { job.cbs.push(function (c) { cb(copy(c)); }); job.live = live || job.live; queue.splice(queue.indexOf(job), 1); queue.push(job); }
      else { job = { n: n, cbs: [function (c) { cb(copy(c)); }], live: live || function () { return true; } }; jobs[n] = job; queue.push(job); }
      pump();
    }
    return {
      get: get,
      /* a copy of the thumbnail when it is already drawn (a blurry stand-in while the real page renders), else null */
      peek: function (n) { var hit = cache.get(n); return hit ? copy(hit) : null; },
      destroy: function () { alive = false; cache.forEach(function (c) { c.width = 0; }); cache.clear(); queue = []; jobs = {}; }
    };
  };

  /* ------------------------------------------------------------------ outline */
  K.outline = function (doc) {
    return doc.getOutline().then(function (o) { return o || []; }).catch(function () { return []; });
  };
  K.destPage = function (doc, dest) {
    if (!dest) return Promise.resolve(0);
    var get = typeof dest === 'string' ? doc.getDestination(dest) : Promise.resolve(dest);
    return get.then(function (d) {
      if (!d) return 0;
      var ref = d[0];
      if (typeof ref === 'number') return ref + 1;
      return doc.getPageIndex(ref).then(function (i) { return i + 1; });
    }).catch(function () { return 0; });
  };

  /* ------------------------------------------------------------------ toast */
  K.toast = function (host) {
    var el = K.el('div', 'nx-toast'), t = 0;
    el.hidden = true; el.setAttribute('role', 'status');
    host.appendChild(el);
    return function (msg, action, fn) {
      el.innerHTML = '';
      var sp = K.el('span'); sp.textContent = msg; el.appendChild(sp);
      if (action) {
        var b = K.el('button'); b.type = 'button'; b.textContent = action;
        b.addEventListener('click', function () { fn(); el.hidden = true; });
        el.appendChild(b);
      }
      el.hidden = false; K.restart(el, 'is-in');
      clearTimeout(t);
      t = setTimeout(function () { el.hidden = true; }, action ? 6500 : 2600);
    };
  };

  /* ------------------------------------------------------------------ scrubber with page preview */
  K.SCRUB = '<div class="nx-scrub"><div class="nx-track"><i class="nx-fill"></i><span class="nx-ticks"></span></div>' +
    '<input type="range" class="nx-range" min="1" max="1" value="1" aria-label="Go to page"><div class="nx-tip" hidden><span class="nx-tipc"></span><b></b></div></div>';
  /* o: { N(): pages, go(n), thumbs, marks(): [pages], ratio(): h/w, focus() } */
  K.scrubber = function (scrub, o) {
    var range = scrub.querySelector('.nx-range'), tip = scrub.querySelector('.nx-tip'), tc = scrub.querySelector('.nx-tipc'), tn = tip.querySelector('b'), ticks = scrub.querySelector('.nx-ticks');
    var shown = 0, dragging = false;
    function pct(v) { var N = o.N(); return N > 1 ? (v - 1) / (N - 1) * 100 : 0; }
    function show(v, p) {
      tip.hidden = false; tn.textContent = v;
      tip.style.left = 'calc(' + p + '% + ' + (10 - p * 0.2) + 'px)';
      if (shown === v) return;
      shown = v;
      if (o.thumbs) o.thumbs.get(v, function (c) { if (shown === v) { tc.innerHTML = ''; c.style.aspectRatio = '1 / ' + o.ratio().toFixed(3); tc.appendChild(c); } }, function () { return shown === v; });
    }
    range.addEventListener('input', function () {
      var v = +range.value, p = pct(v);
      scrub.style.setProperty('--p', p.toFixed(2) + '%');
      dragging = true; show(v, p);
    });
    range.addEventListener('change', function () { dragging = false; tip.hidden = true; shown = 0; o.go(+range.value); if (o.focus) o.focus(); });
    range.addEventListener('keydown', function (e) { e.stopPropagation(); });
    range.addEventListener('blur', function () { dragging = false; tip.hidden = true; shown = 0; });
    scrub.addEventListener('pointermove', function (e) {
      if (dragging || e.pointerType !== 'mouse') return;
      var r = scrub.getBoundingClientRect(), f = K.clamp((e.clientX - r.left - 10) / Math.max(1, r.width - 20), 0, 1), N = o.N(), v = Math.round(1 + f * (N - 1));
      show(v, pct(v));
    });
    scrub.addEventListener('pointerleave', function () { if (!dragging) { tip.hidden = true; shown = 0; } });
    return {
      set: function (c) {
        var N = o.N();
        range.max = N; range.value = c;
        scrub.style.setProperty('--p', pct(c).toFixed(2) + '%');
        ticks.innerHTML = '';
        if (N < 2) return;
        o.marks().forEach(function (p) { var t = K.el('i', 'nx-tick'); t.style.left = ((p - 1) / (N - 1) * 100) + '%'; ticks.appendChild(t); });
      }
    };
  };

  /* ------------------------------------------------------------------ settings sheet and help */
  /* schema items: {t:'seg',k,h,o:[[value,label,icon]]} {t:'range',k,h,min,max} {t:'sw',k,label,icon} {t:'btn',act,label,icon} */
  K.settingsHTML = function (schema, prefs) {
    return schema.map(function (it) {
      if (it.t === 'seg') {
        return '<div class="nx-ps"><h4>' + it.h + '</h4><div class="nx-seg" role="radiogroup" data-k="' + it.k + '">' + it.o.map(function (o) {
          return '<button type="button" role="radio" data-v="' + o[0] + '" aria-checked="' + (String(prefs[it.k]) === String(o[0])) + '">' + (o[2] ? K.icon(o[2]) : '') + '<span>' + o[1] + '</span></button>';
        }).join('') + '</div></div>';
      }
      if (it.t === 'range') return '<div class="nx-ps"><h4>' + it.h + '</h4><input type="range" class="nx-slide" data-k="' + it.k + '" min="' + it.min + '" max="' + it.max + '" value="' + prefs[it.k] + '" aria-label="' + it.h + '"></div>';
      if (it.t === 'sw') return '<button type="button" class="nx-sw" role="switch" data-k="' + it.k + '" aria-checked="' + !!prefs[it.k] + '">' + K.icon(it.icon) + '<span>' + it.label + '</span><i class="nx-knob"></i></button>';
      return '<button type="button" class="x-btn x-btn-tonal nx-wide" data-act="' + it.act + '">' + K.icon(it.icon) + it.label + '</button>';
    }).join('');
  };
  /* onChange(key, value) for prefs, onChange('@act') for buttons */
  K.bindSettings = function (pop, prefs, onChange) {
    pop.addEventListener('click', function (e) {
      var s = e.target.closest('.nx-seg button'), w = e.target.closest('.nx-sw'), b = e.target.closest('[data-act]');
      if (s) {
        var k = s.parentNode.dataset.k, v = s.dataset.v;
        if (/^-?\d+(\.\d+)?$/.test(v)) v = +v;
        s.parentNode.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-checked', x === s ? 'true' : 'false'); });
        K.sfx.tick();
        onChange(k, v);
      } else if (w) {
        var kk = w.dataset.k, nv = !prefs[kk];
        w.setAttribute('aria-checked', String(nv));
        onChange(kk, nv);
        K.sfx.pop(nv);
      } else if (b) onChange('@' + b.dataset.act);
    });
    pop.addEventListener('input', function (e) {
      var r = e.target.closest('.nx-slide');
      if (r) onChange(r.dataset.k, +r.value);
    });
  };
  K.helpHTML = function (rows) {
    return '<div class="nx-hc"><div class="nx-hh"><b>Keyboard</b>' + K.btn('nx-ib', 'close', 'Close', ' data-act="closehelp"') + '</div>' +
      rows.map(function (r) { return '<div class="nx-hr"><span>' + r[0] + '</span><kbd>' + r[1] + '</kbd></div>'; }).join('') + '</div>';
  };

  /* ------------------------------------------------------------------ side panels */
  /* o: { host, root, doc, N(), ratio(), text, thumbs, store, ink, visible(): [pages], cur(), go(n), query: {get(), set(q)},
          relayout(), phone(): bool, mark(), toast } */
  K.panels = function (o) {
    var host = o.host, name = '', P = { grid: null, sInput: null, sList: null, sStat: null, mStats: null, mList: null, mAdd: null, outline: null };
    var TITLES = { pages: 'Pages', toc: 'Contents', search: 'Search', marks: 'Bookmarks' };
    var timers = [];

    function open(n) {
      if (name === n) { close(); return; }
      name = n;
      host.hidden = false;
      host.innerHTML = '<div class="nx-ph"><b></b>' + K.btn('nx-ib', 'close', 'Close panel', ' data-act="closepanel"') + '</div><div class="nx-pb"></div>';
      host.firstChild.firstChild.textContent = TITLES[n];
      K.restart(host, 'is-in');
      o.root.dataset.open = n;
      o.root.querySelectorAll('[data-panel]').forEach(function (b) { b.classList.toggle('is-on', b.dataset.panel === n); });
      var body = host.lastChild;
      if (n === 'pages') buildThumbs(body); else if (n === 'toc') buildToc(body); else if (n === 'search') buildSearch(body); else buildMarks(body);
      o.relayout();
    }
    function close() {
      if (!name) return;
      name = '';
      host.hidden = true; host.innerHTML = '';
      P.grid = null; P.sList = null; P.mList = null;
      o.root.dataset.open = '';
      o.root.querySelectorAll('[data-panel]').forEach(function (b) { b.classList.remove('is-on'); });
      o.relayout();
    }
    function leave() { if (o.phone()) close(); }

    function buildThumbs(body) {
      var grid = K.el('div', 'nx-thumbs'), io = null, n, b;
      P.grid = grid;
      function fill(btn) {
        var n2 = +btn.dataset.n;
        o.thumbs.get(n2, function (c) { var slot = btn.firstChild; if (slot) { slot.appendChild(c); slot.classList.add('is-ready'); } }, function () { return btn.isConnected; });
      }
      if ('IntersectionObserver' in W) {
        io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); fill(e.target); } }); }, { root: body, rootMargin: '300px 0px' });
      }
      for (n = 1; n <= o.N(); n++) {
        b = K.el('button', 'nx-th');
        b.type = 'button'; b.dataset.n = n;
        b.setAttribute('aria-label', 'Page ' + n);
        b.innerHTML = '<span class="nx-thp" style="aspect-ratio: 1 / ' + o.ratio().toFixed(3) + '"></span><span class="nx-thn">' + n + '</span>';
        grid.appendChild(b);
        if (io) io.observe(b); else fill(b);
      }
      grid.addEventListener('click', function (e) {
        var t = e.target.closest('.nx-th');
        if (t) { o.go(+t.dataset.n); leave(); }
      });
      body.appendChild(grid);
      marks(true);
    }
    function marks(scroll) {
      if (!P.grid) return;
      var vis = o.visible(), first = null;
      P.grid.querySelectorAll('.nx-th').forEach(function (b) {
        var n = +b.dataset.n, on = vis.indexOf(n) !== -1;
        b.classList.toggle('is-cur', on);
        b.classList.toggle('is-marked', o.store.isMarked(n));
        b.classList.toggle('is-inked', o.ink.has(n));
        if (on && !first) first = b;
      });
      if (first && scroll) first.scrollIntoView({ block: 'center' });
    }

    function buildToc(body) {
      body.innerHTML = '<div class="nx-empty"><span>Reading the contents</span></div>';
      var load = P.outline ? Promise.resolve(P.outline) : K.outline(o.doc).then(function (list) { P.outline = list; return list; });
      load.then(function (items) {
        if (name !== 'toc') return;
        body.innerHTML = '';
        if (!items.length) { body.appendChild(K.el('div', 'nx-empty', K.icon('menu_book') + '<span>No contents in this file</span>')); return; }
        body.appendChild(tocList(items, 0));
      });
    }
    function tocList(items, depth) {
      var ul = K.el('ul', 'nx-toc');
      items.forEach(function (it) {
        var li = K.el('li'), row = K.el('div', 'nx-tr'), kids = it.items && it.items.length;
        row.style.paddingLeft = (4 + depth * 14) + 'px';
        var tg = K.el('button', 'nx-tt' + (kids ? '' : ' is-leaf'), kids ? K.icon('chevron_right') : '');
        tg.type = 'button'; tg.setAttribute('aria-label', 'Expand');
        var go = K.el('button', 'nx-tl'); go.type = 'button'; go.textContent = it.title || 'Untitled';
        row.appendChild(tg); row.appendChild(go); li.appendChild(row);
        if (kids) {
          var sub = tocList(it.items, depth + 1); sub.hidden = true; li.appendChild(sub);
          tg.addEventListener('click', function () { sub.hidden = !sub.hidden; tg.classList.toggle('is-open', !sub.hidden); });
        }
        go.addEventListener('click', function () { K.destPage(o.doc, it.dest).then(function (n) { if (n) { o.go(n); leave(); } }); });
        ul.appendChild(li);
      });
      return ul;
    }

    function buildSearch(body) {
      var box = K.el('div', 'nx-sbox', K.icon('search')), input = K.el('input', 'nx-sin');
      input.type = 'search'; input.placeholder = 'Search the book'; input.value = o.query.get(); input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Search the book');
      box.appendChild(input);
      var stat = K.el('div', 'nx-sstat'), list = K.el('div', 'nx-sres');
      body.appendChild(box); body.appendChild(stat); body.appendChild(list);
      P.sInput = input; P.sList = list; P.sStat = stat;
      var t = 0;
      input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { o.query.set(input.value.trim()); runSearch(); }, 220); });
      input.addEventListener('keydown', function (e) {
        e.stopPropagation();
        if (e.key === 'Escape') { if (input.value) { input.value = ''; o.query.set(''); runSearch(); } else { close(); o.root.focus(); } }
        if (e.key === 'Enter' && P.first) { o.go(P.first.p); leave(); }
      });
      o.text.indexAll(function () { if (name === 'search') runSearch(); });
      runSearch();
      timers.push(setTimeout(function () { input.focus(); }, 80));
    }
    function runSearch() {
      if (!P.sList || name !== 'search') return;
      var q = o.query.get().toLowerCase(), N = o.N(), done = o.text.progress() >= N;
      if (q.length < 2) { P.first = null; P.sList.innerHTML = ''; P.sStat.textContent = ''; return; }
      var res = o.text.search(q);
      P.first = res[0] || null;
      P.sList.innerHTML = '';
      res.forEach(function (r) {
        var b = K.el('button', 'nx-sri'); b.type = 'button';
        var chip = K.el('span', 'nx-chip'); chip.textContent = 'p. ' + r.p;
        var txt = K.el('span', 'nx-snip');
        var a = Math.max(0, r.idx - 34), z = Math.min(r.str.length, r.idx + q.length + 70);
        txt.appendChild(D.createTextNode((a > 0 ? '\u2026' : '') + r.str.slice(a, r.idx)));
        var mk = K.el('mark'); mk.textContent = r.str.slice(r.idx, r.idx + q.length); txt.appendChild(mk);
        txt.appendChild(D.createTextNode(r.str.slice(r.idx + q.length, z) + (z < r.str.length ? '\u2026' : '')));
        b.appendChild(chip); b.appendChild(txt);
        b.addEventListener('click', function () { o.go(r.p); leave(); });
        P.sList.appendChild(b);
      });
      var pct = Math.round(o.text.progress() / N * 100);
      P.sStat.textContent = (res.length ? res.length + (res.length >= 400 ? '+ matches' : (res.length === 1 ? ' match' : ' matches')) : (done ? 'No matches' : 'Searching')) + (done ? '' : ' \u00b7 ' + pct + '%');
    }

    function buildMarks(body) {
      var stats = K.el('div', 'nx-stats'), add = K.el('button', 'x-btn x-btn-tonal nx-wide');
      add.type = 'button';
      add.innerHTML = K.icon('bookmark_add') + '<span>Bookmark this page</span>';
      add.addEventListener('click', function () { o.mark(); });
      var list = K.el('div', 'nx-marks');
      body.appendChild(stats); body.appendChild(add); body.appendChild(list);
      P.mStats = stats; P.mList = list; P.mAdd = add;
      renderMarks();
    }
    function renderMarks() {
      if (!P.mList || name !== 'marks') return;
      var d = o.store.d, N = o.N(), pct = Math.round((d.max || 1) / N * 100), mins = Math.floor(d.time / 60), left = Math.max(0, N - (d.max || 1));
      var inked = o.ink.pages();
      P.mStats.innerHTML = '<div class="nx-bar"><i style="width:' + pct + '%"></i></div>' +
        '<div class="nx-srow"><span><b>' + pct + '%</b> read</span><span><b>' + left + '</b> pages left</span><span><b>' + (mins < 1 ? '<1' : mins) + '</b> min</span>' + (inked ? '<span><b>' + inked + '</b> marked up</span>' : '') + '</div>';
      P.mAdd.lastChild.textContent = o.visible().some(o.store.isMarked) ? 'Remove bookmark here' : 'Bookmark this page';
      P.mList.innerHTML = '';
      if (!d.marks.length) { P.mList.appendChild(K.el('div', 'nx-empty', K.icon('bookmarks') + '<span>No bookmarks yet</span>')); return; }
      d.marks.slice().sort(function (a, b) { return a.p - b.p; }).forEach(function (m) {
        var row = K.el('div', 'nx-mark'), g = K.el('button', 'nx-chip nx-chip-go'); g.type = 'button'; g.textContent = 'p. ' + m.p;
        g.addEventListener('click', function () { o.go(m.p); leave(); });
        var inp = K.el('input', 'nx-note'); inp.type = 'text'; inp.placeholder = 'Add a note'; inp.value = m.note || ''; inp.maxLength = 160;
        inp.setAttribute('aria-label', 'Note for page ' + m.p);
        inp.addEventListener('keydown', function (e) { e.stopPropagation(); });
        inp.addEventListener('input', function () { m.note = inp.value; o.store.soon(); });
        var del = K.el('button', 'nx-ib nx-del', K.icon('delete')); del.type = 'button'; del.setAttribute('aria-label', 'Delete bookmark');
        del.addEventListener('click', function () { d.marks = d.marks.filter(function (x) { return x !== m; }); o.store.save(); o.store.soon(); o.changed(); });
        row.appendChild(g); row.appendChild(inp); row.appendChild(del);
        P.mList.appendChild(row);
      });
    }
    return {
      open: open, close: close,
      current: function () { return name; },
      sync: function () { if (name === 'pages') marks(); else if (name === 'marks') renderMarks(); },
      renderMarks: renderMarks,
      focusSearch: function () { if (name !== 'search') open('search'); else if (P.sInput) P.sInput.focus(); },
      destroy: function () { timers.forEach(clearTimeout); }
    };
  };

  W.NebPdfKit = K;
})();
