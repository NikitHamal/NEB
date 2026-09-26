/*
 * NEBians generative art -- the web half.
 *
 * GENERATED FILE. Do not hand-edit.
 *   source:  app/src/main/java/com/neb/ians/ui/components/ResourceBannerArt.kt
 *            app/src/main/java/com/neb/ians/ui/components/ProfileCoverArt.kt
 *            app/src/main/java/com/neb/ians/ui/theme/Color.kt
 *   emitter: tools/art/genjs.py
 *
 * The app draws 67 subject banner arts and 7 profile cover motifs procedurally
 * in Compose. The website used to draw flat gradients, so the same resource
 * looked like two different products depending on where you opened it. Rather
 * than transcribe four thousand lines of drawing code into JavaScript by hand
 * -- which would be wrong within a week -- this file is emitted from the Kotlin
 * itself. Same hash, same PRNG, same arithmetic, same picture: a resource whose
 * banner is a titration burette in the app is a titration burette here, down to
 * the position of the meniscus.
 *
 * Canvas rather than SVG because the arts are written against a Compose
 * DrawScope, and Canvas2D is the same shape of API: immediate mode, one
 * transform stack, fill and stroke. The mapping is mechanical, which is exactly
 * what makes it safe to generate.
 */
(function (global) {
  'use strict';

  // ------------------------------------------------------------- colour ----
  function Color(r, g, b, a) { this.r = r; this.g = g; this.b = b; this.a = a === undefined ? 1 : a; }
  Color.hex = function (v) {
    return new Color(((v >> 16) & 255) / 255, ((v >> 8) & 255) / 255, (v & 255) / 255,
                     v > 0xFFFFFF ? ((v >>> 24) & 255) / 255 : 1);
  };
  Color.prototype.copy = function (alpha) {
    return new Color(this.r, this.g, this.b, alpha === undefined ? this.a : alpha);
  };
  Color.prototype.css = function () {
    return 'rgba(' + Math.round(this.r * 255) + ',' + Math.round(this.g * 255) + ','
         + Math.round(this.b * 255) + ',' + this.a + ')';
  };
  function lerp(a, b, t) {
    return new Color(a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t,
                     a.b + (b.b - a.b) * t, a.a + (b.a - a.a) * t);
  }
  var WHITE = new Color(1, 1, 1);
  var BLACK = new Color(0, 0, 0);

  // ---------------------------------------------------------------- rng ----
  // FNV-1a and xorshift32, both in signed 32-bit to match Kotlin's Int exactly.
  // Math.imul is the only way to get a wrapping 32-bit multiply in JS.
  function stableSeed(key) {
    var h = -2128831035;
    for (var i = 0; i < key.length; i++) {
      h = (h ^ key.charCodeAt(i)) | 0;
      h = Math.imul(h, 16777619);
    }
    return h | 0;
  }
  function Rng(seed) { this.s = (seed | 0) === 0 ? 1 : (seed | 0); }
  Rng.prototype.next = function () {
    var s = this.s;
    s = (s ^ (s << 13)) | 0;
    s = (s ^ (s >>> 17)) | 0;
    s = (s ^ (s << 5)) | 0;
    this.s = s;
    return ((s >>> 8) & 0xFFFFFF) / 16777216;
  };
  Rng.prototype.range = function (a, b) { return a + (b - a) * this.next(); };
  Rng.prototype.int = function (n) {
    var v = Math.trunc(this.next() * n);
    return v >= n ? n - 1 : v;
  };

  // ----------------------------------------------------------- geometry ----
  function Off(x, y) { this.x = x; this.y = y; }
  function Sz(w, h) { this.w = w; this.h = h; }
  function Stroke(o) { return { width: o.width, cap: o.cap || 'butt' }; }

  function P() { this.p = new Path2D(); this.x = 0; this.y = 0; }
  P.prototype.moveTo = function (x, y) { this.p.moveTo(x, y); this.x = x; this.y = y; };
  P.prototype.lineTo = function (x, y) { this.p.lineTo(x, y); this.x = x; this.y = y; };
  P.prototype.cubicTo = function (a, b, c, d, e, f) {
    this.p.bezierCurveTo(a, b, c, d, e, f); this.x = e; this.y = f;
  };
  P.prototype.close = function () { this.p.closePath(); };

  // --------------------------------------------------------- gradients ----
  function grad(kind, o) { return { kind: kind, o: o }; }
  var Brush = {
    verticalGradient: function (a) {
      var o = Array.isArray(a) ? { colors: a } : a;
      return grad('v', o);
    },
    linearGradient: function (a) { return grad('l', a); },
    radialGradient: function (a) { return grad('r', a); }
  };

  // --------------------------------------------------------- draw scope ----
  // A Compose DrawScope over Canvas2D. Every method takes the same named
  // arguments the Kotlin does, as one object, because that is what the emitter
  // produces from Kotlin's named-argument call sites.
  function D(ctx, w, h) { this.c = ctx; this.w = w; this.h = h; }

  D.prototype._grad = function (g) {
    var c = this.c, o = g.o, cs = o.colors, out;
    if (g.kind === 'v') {
      var y0 = o.startY === undefined ? 0 : o.startY;
      var y1 = (o.endY === undefined || !isFinite(o.endY)) ? this.h : o.endY;
      out = c.createLinearGradient(0, y0, 0, y1);
    } else if (g.kind === 'l') {
      out = c.createLinearGradient(o.start.x, o.start.y, o.end.x, o.end.y);
    } else {
      out = c.createRadialGradient(o.center.x, o.center.y, 0, o.center.x, o.center.y, o.radius);
    }
    for (var i = 0; i < cs.length; i++) {
      out.addColorStop(cs.length === 1 ? 0 : i / (cs.length - 1), cs[i].css());
    }
    return out;
  };

  D.prototype._paint = function (o, path, closed) {
    var c = this.c;
    if (o.style) {
      c.lineWidth = o.style.width;
      c.lineCap = o.style.cap === 'round' ? 'round' : 'butt';
      c.lineJoin = o.style.cap === 'round' ? 'round' : 'miter';
      c.strokeStyle = o.color.css();
      c.stroke(path);
    } else {
      c.fillStyle = o.color.css();
      c.fill(path);
    }
  };

  D.prototype.drawRect = function (o) {
    var c = this.c;
    if (o.brush) {                       // always the full field, as in Compose
      c.fillStyle = this._grad(o.brush);
      c.fillRect(0, 0, this.w, this.h);
      return;
    }
    var tl = o.topLeft || new Off(0, 0);
    var sz = o.size || new Sz(this.w, this.h);
    var p = new Path2D();
    p.rect(tl.x, tl.y, sz.w, sz.h);
    this._paint(o, p);
  };

  D.prototype.drawCircle = function (o) {
    var p = new Path2D();
    p.arc(o.center.x, o.center.y, Math.max(0, o.radius), 0, Math.PI * 2);
    this._paint(o, p);
  };

  D.prototype.drawLine = function (o) {
    var c = this.c;
    c.lineWidth = o.strokeWidth === undefined ? 1 : o.strokeWidth;
    c.lineCap = o.cap === 'round' ? 'round' : 'butt';
    c.strokeStyle = o.color.css();
    c.beginPath();
    c.moveTo(o.start.x, o.start.y);
    c.lineTo(o.end.x, o.end.y);
    c.stroke();
  };

  D.prototype.drawPath = function (o) { this._paint(o, o.path.p); };

  D.prototype.drawArc = function (o) {
    var rx = o.size.w / 2, ry = o.size.h / 2;
    var cx = o.topLeft.x + rx, cy = o.topLeft.y + ry;
    var a0 = o.startAngle * Math.PI / 180;
    var a1 = (o.startAngle + o.sweepAngle) * Math.PI / 180;
    var p = new Path2D();
    if (o.useCenter) { p.moveTo(cx, cy); }
    p.ellipse(cx, cy, Math.max(0, rx), Math.max(0, ry), 0, a0, a1, o.sweepAngle < 0);
    if (o.useCenter) { p.closePath(); }
    this._paint(o, p);
  };

  D.prototype.rotate = function (deg, pivot, body) {
    var c = this.c;
    c.save();
    c.translate(pivot.x, pivot.y);
    c.rotate(deg * Math.PI / 180);
    c.translate(-pivot.x, -pivot.y);
    body();
    c.restore();
  };
  D.prototype.translate = function (x, y, body) {
    this.c.save(); this.c.translate(x, y); body(); this.c.restore();
  };
  D.prototype.scale = function (sx, sy, body) {
    this.c.save(); this.c.scale(sx, sy); body(); this.c.restore();
  };

  // ------------------------------------------------------- subject hues ----
  var HUES = {
    "Physics": [0xFF1D4ED8, 0xFFDBE7FE, 0xFF1B3FA8, 0xFF9DBBFF, 0xFF1B2A4D, 0xFFD6E3FF],
    "Chemistry": [0xFF15803D, 0xFFDCFCE7, 0xFF14602F, 0xFF7CD9A0, 0xFF14301F, 0xFFD3F5DF],
    "Mathematics": [0xFFB91C1C, 0xFFFEE2E2, 0xFF8F1717, 0xFFFF9C93, 0xFF3A1A18, 0xFFFFDAD6],
    "Biology": [0xFF0F766E, 0xFFCCFBF1, 0xFF0C5B55, 0xFF5FD3C4, 0xFF10302D, 0xFFCDF3ED],
    "English": [0xFF7E22CE, 0xFFF3E8FF, 0xFF631AA3, 0xFFD3B4FE, 0xFF2C1A44, 0xFFEDE0FF],
    "Nepali": [0xFF9A6206, 0xFFFEF3C7, 0xFF7A4E05, 0xFFE8B457, 0xFF32260E, 0xFFF7E6C2],
    "Computer Science": [0xFF0E7490, 0xFFCFFAFE, 0xFF0B5A70, 0xFF5CC8E0, 0xFF0E2C36, 0xFFC9EFF8],
    "Economics": [0xFFC2410C, 0xFFFFEDD5, 0xFF9A330A, 0xFFFFA76B, 0xFF3A2013, 0xFFFFE0CB],
    "Accountancy": [0xFF9D174D, 0xFFFCE7F3, 0xFF7D1240, 0xFFF79CC0, 0xFF3A1428, 0xFFFBDCE9],
    "Exam Tips": [0xFF6D28D9, 0xFFEDE9FE, 0xFF56209F, 0xFFC4B5FD, 0xFF261C46, 0xFFE6E0FF]
  };
  var FAM_HUES = {
    PHYSICS: [0xFF1D4ED8, 0xFFDBE7FE, 0xFF1B3FA8, 0xFF9DBBFF, 0xFF1B2A4D, 0xFFD6E3FF],
    CHEMISTRY: [0xFF15803D, 0xFFDCFCE7, 0xFF14602F, 0xFF7CD9A0, 0xFF14301F, 0xFFD3F5DF],
    MATH: [0xFFB91C1C, 0xFFFEE2E2, 0xFF8F1717, 0xFFFF9C93, 0xFF3A1A18, 0xFFFFDAD6],
    BIOLOGY: [0xFF0F766E, 0xFFCCFBF1, 0xFF0C5B55, 0xFF5FD3C4, 0xFF10302D, 0xFFCDF3ED],
    LANGUAGE: [0xFF7E22CE, 0xFFF3E8FF, 0xFF631AA3, 0xFFD3B4FE, 0xFF2C1A44, 0xFFEDE0FF],
    COMPUTING: [0xFF0E7490, 0xFFCFFAFE, 0xFF0B5A70, 0xFF5CC8E0, 0xFF0E2C36, 0xFFC9EFF8],
    COMMERCE: [0xFFC2410C, 0xFFFFEDD5, 0xFF9A330A, 0xFFFFA76B, 0xFF3A2013, 0xFFFFE0CB],
    EXAM: [0xFF6D28D9, 0xFFEDE9FE, 0xFF56209F, 0xFFC4B5FD, 0xFF261C46, 0xFFE6E0FF],
    SCIENCE: [0xFF047857, 0xFFD1FAE5, 0xFF04604A, 0xFF6EDCB4, 0xFF0D2E25, 0xFFCFF5E6],
    SOCIAL: [0xFF3F5A8A, 0xFFDDE6F6, 0xFF2C4066, 0xFF9CB7E8, 0xFF1B2638, 0xFFD9E4F7],
    HEALTH: [0xFFBE123C, 0xFFFFE4E9, 0xFF8F0E2E, 0xFFFF9BB0, 0xFF3D1520, 0xFFFFD9E1],
    GENERAL: [0xFF004AC6, 0xFFDBE1FF, 0xFF00174B, 0xFFB4C5FF, 0xFF22324C, 0xFFDBE1FF]
  };
  var FAM_KEYWORDS = [
    ["HEALTH", ["health", "physical education", "phy. edu", "hpe", "sport", "fitness", "nutrition", "yoga", "स्वास्थ्य"]],
    ["EXAM", ["exam tip", "exam prep", "entrance", "model paper", "model set", "past paper", "question bank", "mock test", "revision"]],
    ["COMPUTING", ["computer", "software", "programming", "informatics", "information tech", "digital", "coding", "algorithm", "database", "web dev"]],
    ["PHYSICS", ["physics", "भौतिक"]],
    ["CHEMISTRY", ["chemistry", "chemical", "रसायन"]],
    ["MATH", ["math", "algebra", "geometry", "trigonometry", "calculus", "statistic", "गणित"]],
    ["BIOLOGY", ["biology", "botany", "zoology", "microbio", "anatomy", "genetic", "जीव"]],
    ["SOCIAL", ["social", "history", "geography", "civic", "population", "culture", "सामाजिक", "अध्ययन"]],
    ["COMMERCE", ["economic", "account", "business", "finance", "commerce", "marketing", "banking", "book keeping", "bookkeeping", "अर्थ"]],
    ["LANGUAGE", ["english", "nepali", "literature", "grammar", "language", "sanskrit", "hindi", "maithili", "newari", "writing", "नेपाली", "अंग्रेजी", "साहित्य"]],
    ["SCIENCE", ["science", "environment", "astronomy", "geology", "laboratory", "विज्ञान"]]
  ];

  function subjectFamily(subject) {
    var s = (subject || '').trim().toLowerCase();
    if (!s) return 'GENERAL';
    for (var i = 0; i < FAM_KEYWORDS.length; i++) {
      var kws = FAM_KEYWORDS[i][1];
      for (var k = 0; k < kws.length; k++) {
        if (s.indexOf(kws[k]) >= 0) return FAM_KEYWORDS[i][0];
      }
    }
    return 'GENERAL';
  }

  function subjectHue(subject) {
    if (HUES[subject]) return HUES[subject];
    var lower = (subject || '').trim().toLowerCase();
    for (var k in HUES) { if (k.toLowerCase() === lower) return HUES[k]; }
    return FAM_HUES[subjectFamily(subject)] || FAM_HUES.GENERAL;
  }

  function bannerPalette(subject, dark) {
    var hx = subjectHue(subject).map(Color.hex);
    var t = dark ? { color: hx[3], container: hx[4] } : { color: hx[0], container: hx[1] };
    var surface = dark ? SURFACE_DARK : SURFACE_LIGHT;
    return dark ? { top: lerp(t.container, surface, 0.58), bottom: lerp(t.container, surface, 0.12), ink: t.color, paper: lerp(t.color, WHITE, 0.34), field: lerp(lerp(t.container, surface, 0.58), lerp(t.container, surface, 0.12), 0.55) } : { top: lerp(t.container, WHITE, 0.62), bottom: lerp(t.container, WHITE, 0.14), ink: t.color, paper: WHITE, field: lerp(lerp(t.container, WHITE, 0.62), lerp(t.container, WHITE, 0.14), 0.55) };
  }

  // ------------------------------------------------------ cover palettes ----
  var COVER_PALETTES = {
    ADMIN: { deep: Color.hex(0xFF060608), mid: Color.hex(0xFF131318), rise: Color.hex(0xFF24242C), glow: Color.hex(0xFF4A4A5A), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFFCFCFDC) },
    MODERATOR: { deep: Color.hex(0xFF05101C), mid: Color.hex(0xFF102338), rise: Color.hex(0xFF1B3A5A), glow: Color.hex(0xFF2E5C8C), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFF9FC4EC) },
    VERIFIED: { deep: Color.hex(0xFF03122A), mid: Color.hex(0xFF0A2A5E), rise: Color.hex(0xFF12459B), glow: Color.hex(0xFF2C6BE0), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFFAEC9FF) },
    TUTOR: { deep: Color.hex(0xFF120B26), mid: Color.hex(0xFF241544), rise: Color.hex(0xFF3C2470), glow: Color.hex(0xFF6A43B8), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFFCDB6F5) },
    INSTITUTION: { deep: Color.hex(0xFF03140F), mid: Color.hex(0xFF0B2A20), rise: Color.hex(0xFF134737), glow: Color.hex(0xFF1F6E55), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFFA4DCC4) },
    BOT: { deep: Color.hex(0xFF021118), mid: Color.hex(0xFF05283A), rise: Color.hex(0xFF0A4358), glow: Color.hex(0xFF13738F), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFF8FE2F7) },
    MEMBER: { deep: Color.hex(0xFF070A11), mid: Color.hex(0xFF141A27), rise: Color.hex(0xFF232E44), glow: Color.hex(0xFF3A4C6E), ink: Color.hex(0xFFFFFFFF), accent: Color.hex(0xFFB3C2DB) },
  };

  // --------------------------------------------------------- banner arts ----
  function artApple(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const extras = Math.min(Math.max(Math.trunc(((w / h) * 1.1)), 0), 3);
    for (let k = Math.trunc(0); k < Math.trunc(extras + 1); k++) {
      const lead = k == 0;
      const sc = ((lead) ? (1) : (0.46 + r.range(0, 0.12)));
      const side = ((k % 2 == 1) ? (-1) : (1));
      const tier = (k + 1) / 2;
      const rad = unit * 0.32 * sc;
      const cx = ((lead) ? (w * 0.50) : (w * 0.50 + side * unit * (0.62 + tier * 0.40)));
      const cy = ((lead) ? (h * 0.60) : (h * 0.66));
      const al = ((lead) ? (0.86) : (0.34));
      if (cx > rad && cx < w - rad) {
        const body = new P();
        body.moveTo(cx, cy - rad * 0.72);
        body.cubicTo(cx - rad * 0.50, cy - rad * 1.24, cx - rad * 1.36, cy - rad * 0.50, cx - rad * 1.00, cy + rad * 0.44);
        body.cubicTo(cx - rad * 0.78, cy + rad * 1.20, cx - rad * 0.18, cy + rad * 1.28, cx, cy + rad * 0.96);
        body.cubicTo(cx + rad * 0.18, cy + rad * 1.28, cx + rad * 0.78, cy + rad * 1.20, cx + rad * 1.00, cy + rad * 0.44);
        body.cubicTo(cx + rad * 1.36, cy - rad * 0.50, cx + rad * 0.50, cy - rad * 1.24, cx, cy - rad * 0.72);
        body.close();
        d.drawPath({path: body, color: p.ink.copy(al * 0.22)});
        d.drawPath({path: body, color: p.ink.copy(al), style: Stroke({width: unit * 0.024 * (0.62 + sc * 0.38), cap: 'round'})});
        d.drawLine({color: p.ink.copy(al), start: new Off(cx, cy - rad * 0.72), end: new Off(cx + rad * 0.10, cy - rad * 1.34), strokeWidth: unit * 0.024 * (0.62 + sc * 0.38), cap: 'round'});
        if (lead) {
          const leaf = new P();
          leaf.moveTo(cx + rad * 0.08, cy - rad * 1.16);
          leaf.cubicTo(cx + rad * 0.62, cy - rad * 1.52, cx + rad * 0.92, cy - rad * 1.16, cx + rad * 0.86, cy - rad * 0.86);
          leaf.cubicTo(cx + rad * 0.56, cy - rad * 0.80, cx + rad * 0.20, cy - rad * 0.96, cx + rad * 0.08, cy - rad * 1.16);
          leaf.close();
          d.drawPath({path: leaf, color: p.ink.copy(0.60)});
          d.drawArc({color: p.paper.copy(0.34), startAngle: 185, sweepAngle: 62, useCenter: false, topLeft: new Off(cx - rad * 0.74, cy - rad * 0.50), size: new Sz(rad * 1.0, rad * 1.2), style: Stroke({width: unit * 0.030, cap: 'round'})});
        }
      }
    }
  }
  function artArcs(d, p, r) {
    const w = d.w;
    const h = d.h;
    const ox = w * 0.05;
    const oy = h * 1.00;
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      const rad = h * (0.24 + i * 0.33);
      d.drawArc({color: p.ink.copy(0.42 - i * 0.055), startAngle: -92, sweepAngle: 94, useCenter: false, topLeft: new Off(ox - rad, oy - rad), size: new Sz(rad * 2, rad * 2), style: Stroke({width: h * 0.028, cap: 'round'})});
    }
    d.drawCircle({color: p.ink, radius: h * 0.055, center: new Off(ox, oy)});
    d.drawCircle({color: p.ink.copy(0.55), radius: h * 0.048, center: new Off(w * r.range(0.62, 0.82), h * 0.26)});
  }
  function artAtom(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cx = w * 0.50;
    const cy = h * 0.54;
    const rx = h * 0.44;
    const ry = h * 0.17;
    const spin = r.range(0, 60);
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      d.rotate(spin + i * 60, new Off(cx, cy), () => {
        d.drawArc({color: p.ink.copy(0.58 - i * 0.09), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rx, cy - ry), size: new Sz(rx * 2, ry * 2), style: Stroke({width: h * 0.024})});
      });
    }
    d.rotate(spin, new Off(cx, cy), () => {
      d.drawCircle({color: p.ink, radius: h * 0.052, center: new Off(cx + rx, cy)});
    });
    d.drawCircle({color: p.ink, radius: h * 0.090, center: new Off(cx, cy)});
    d.drawCircle({color: p.paper.copy(0.70), radius: h * 0.034, center: new Off(cx, cy)});
  }
  function artBars(d, p, r) {
    const w = d.w;
    const h = d.h;
    const n = 7;
    const baseY = h * 0.86;
    const bw = w / (n * 2.0);
    const gap = w / n;
    const trend = new P();
    for (let i = Math.trunc(0); i < Math.trunc(n); i++) {
      const f = i / (n - 1);
      const bh = h * (0.14 + f * 0.46 + r.range(0, 0.12));
      const x = gap * i + (gap - bw) * 0.5;
      const topY = baseY - bh;
      d.drawRect({color: p.ink.copy(0.28 + f * 0.34), topLeft: new Off(x, topY), size: new Sz(bw, bh)});
      d.drawCircle({color: p.ink.copy(0.28 + f * 0.34), radius: bw * 0.5, center: new Off(x + bw * 0.5, topY)});
      if (i == 0) {
        trend.moveTo(x + bw * 0.5, topY - h * 0.10);
      } else {
        trend.lineTo(x + bw * 0.5, topY - h * 0.10);
      }
    }
    d.drawPath({path: trend, color: p.ink, style: Stroke({width: h * 0.026, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.30), start: new Off(0, baseY), end: new Off(w, baseY), strokeWidth: h * 0.014});
  }
  function artBeaker(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const half = unit * 0.36;
    const top = h * 0.14;
    const bot = h * 0.88;
    const liq = top + (bot - top) * 0.40;
    d.drawRect({color: p.ink.copy(0.22), topLeft: new Off(cx - half, liq), size: new Sz(half * 2, bot - liq)});
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx - half, top), end: new Off(cx - half, bot), strokeWidth: unit * 0.022, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx + half, top), end: new Off(cx + half, bot), strokeWidth: unit * 0.022, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx - half, bot), end: new Off(cx + half, bot), strokeWidth: unit * 0.022, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx - half - unit * 0.07, top - unit * 0.03), end: new Off(cx - half, top + unit * 0.02), strokeWidth: unit * 0.022, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.72), start: new Off(cx - half, liq), end: new Off(cx + half, liq), strokeWidth: unit * 0.018, cap: 'round'});
    const ticks = Math.min(Math.max(Math.trunc(((bot - top) / (unit * 0.13))), 3), 9);
    for (let i = Math.trunc(0); i < Math.trunc(ticks); i++) {
      const ty = top + (bot - top) * (i + 1) / (ticks + 1);
      d.drawLine({color: p.ink.copy(0.40), start: new Off(cx + half, ty), end: new Off(cx + half - unit * (((i % 2 == 0) ? (0.13) : (0.07))), ty), strokeWidth: unit * 0.012, cap: 'round'});
    }
    for (let i = Math.trunc(0); i < Math.trunc(9); i++) {
      const f = i / 8;
      const bxx = cx + r.range(-0.55, 0.55) * half;
      const byy = bot - f * (bot - liq) * 0.95 - unit * 0.03;
      d.drawCircle({color: p.ink.copy(0.22 + f * 0.34), radius: unit * (0.016 + f * 0.026), center: new Off(bxx, byy), style: Stroke({width: unit * 0.010})});
    }
  }
  function artBenzene(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const spin = r.range(0, 0.5);
    const rings = Math.min(Math.max(Math.trunc(((w / h) * 1.05)), 1), 4);
    for (let k = Math.trunc(0); k < Math.trunc(rings); k++) {
      const lead = k == 0;
      const rad = ((lead) ? (unit * 0.36) : (unit * 0.20));
      const cx = ((lead) ? (w * 0.50) : (w * (0.16 + k * 0.24)));
      const cy = ((lead) ? (h * 0.50) : (h * (0.26 + (k % 2) * 0.48)));
      const al = ((lead) ? (0.86) : (0.30));
      const ring = new P();
      for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
        const a = spin + i * (Math.PI / 3);
        const x = cx + Math.cos(a) * rad;
        const y = cy + Math.sin(a) * rad;
        if (i == 0) {
          ring.moveTo(x, y);
        } else {
          ring.lineTo(x, y);
        }
      }
      ring.close();
      d.drawPath({path: ring, color: p.ink.copy(al), style: Stroke({width: unit * 0.022, cap: 'round'})});
      d.drawCircle({color: p.ink.copy(al * 0.62), radius: rad * 0.56, center: new Off(cx, cy), style: Stroke({width: unit * 0.018})});
      if (lead) {
        for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
          const a = spin + i * (Math.PI / 3);
          d.drawCircle({color: p.ink.copy(0.55), radius: unit * 0.040, center: new Off(cx + Math.cos(a) * rad, cy + Math.sin(a) * rad)});
        }
      }
    }
  }
  function artBinary(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const step = unit * 0.20;
    const cols = Math.min(Math.max(Math.trunc((w / step)), 4), 40);
    const rows = Math.min(Math.max(Math.trunc((h / step)), 2), 9);
    const ox = (w - (cols - 1) * step) * 0.5;
    const oy = (h - (rows - 1) * step) * 0.5;
    for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
      const fade = 1 - Math.abs(c / (cols - 1) - 0.42) * 0.9;
      for (let rw = Math.trunc(0); rw < Math.trunc(rows); rw++) {
        const cxx = ox + c * step;
        const cyy = oy + rw * step;
        const al = (0.14 + 0.46 * fade) * (0.55 + r.range(0, 0.65));
        if (r.int(2) == 0) {
          d.drawLine({color: p.ink.copy(al), start: new Off(cxx, cyy - step * 0.28), end: new Off(cxx, cyy + step * 0.28), strokeWidth: unit * 0.026, cap: 'round'});
        } else {
          d.drawCircle({color: p.ink.copy(al), radius: step * 0.25, center: new Off(cxx, cyy), style: Stroke({width: unit * 0.024})});
        }
      }
    }
  }
  function artBloom(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cx = w * 0.50;
    const cy = h * 0.56;
    const len = h * 0.42;
    const spin = r.range(0, 60);
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      d.rotate(spin + i * 60, new Off(cx, cy), () => {
        const petal = new P();
        petal.moveTo(cx + len * 0.16, cy);
        petal.cubicTo(cx + len * 0.46, cy - len * 0.30, cx + len * 0.88, cy - len * 0.18, cx + len, cy);
        petal.cubicTo(cx + len * 0.88, cy + len * 0.18, cx + len * 0.46, cy + len * 0.30, cx + len * 0.16, cy);
        petal.close();
        d.drawPath({path: petal, color: p.ink.copy(0.20 + (i % 2) * 0.12)});
        d.drawPath({path: petal, color: p.ink.copy(0.52), style: Stroke({width: h * 0.016})});
      });
    }
    d.drawCircle({color: p.ink, radius: h * 0.072, center: new Off(cx, cy)});
    d.drawCircle({color: p.paper.copy(0.70), radius: h * 0.026, center: new Off(cx, cy)});
  }
  function artBraces(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const top = h * 0.12;
    const bot = h * 0.88;
    const mid = (top + bot) * 0.5;
    const bw = unit * 0.16;
    for (let k = Math.trunc(0); k < Math.trunc(2); k++) {
      const s = ((k == 0) ? (1) : (-1));
      const bx = ((k == 0) ? (w * 0.11) : (w * 0.89));
      const br = new P();
      br.moveTo(bx + s * bw * 0.75, top);
      br.cubicTo( bx - s * bw * 0.10, top, bx + s * bw * 0.05, top + (mid - top) * 0.40, bx - s * bw * 0.55, mid );
      br.cubicTo( bx + s * bw * 0.05, mid + (bot - mid) * 0.60, bx - s * bw * 0.10, bot, bx + s * bw * 0.75, bot );
      d.drawPath({path: br, color: p.ink.copy(0.82), style: Stroke({width: unit * 0.030, cap: 'round'})});
    }
    const rule = unit * 0.155;
    const lines = Math.min(Math.max(Math.trunc(((bot - top) / rule)), 2), 6);
    const innerL = w * 0.11 + bw * 1.2;
    const innerR = w * 0.89 - bw * 1.2;
    for (let i = Math.trunc(0); i < Math.trunc(lines); i++) {
      const ly = top + rule * (i + 0.70);
      if (ly < bot - rule * 0.2) {
        const ind = (((i == 0) ? (0) : (1))) * unit * 0.14 + (((i == lines - 1) ? (-unit * 0.14) : (0)));
        const sx = innerL + ind + unit * 0.06;
        const frac = 0.40 + r.range(0, 0.50);
        d.drawLine({color: p.ink.copy(0.26 + (((i == 0) ? (0.26) : (0)))), start: new Off(sx, ly), end: new Off(sx + (innerR - sx) * frac, ly), strokeWidth: unit * 0.034, cap: 'round'});
      }
    }
  }
  function artBurette(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const top = h * 0.04;
    const tapY = h * 0.44;
    const tipY = h * 0.54;
    const half = unit * 0.070;
    d.drawRect({color: p.ink.copy(0.20), topLeft: new Off(cx - half, top + (tapY - top) * 0.34), size: new Sz(half * 2, (tapY - top) * 0.66)});
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx - half, top), end: new Off(cx - half, tapY), strokeWidth: unit * 0.020, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx + half, top), end: new Off(cx + half, tapY), strokeWidth: unit * 0.020, cap: 'round'});
    const ticks = Math.min(Math.max(Math.trunc(((tapY - top) / (unit * 0.095))), 4), 12);
    for (let i = Math.trunc(0); i < Math.trunc(ticks); i++) {
      const ty = top + (tapY - top) * (i + 1) / (ticks + 1);
      const long = i % 3 == 0;
      d.drawLine({color: p.ink.copy(((long) ? (0.62) : (0.32))), start: new Off(cx - half, ty), end: new Off(cx - half + (((long) ? (unit * 0.080) : (unit * 0.044))), ty), strokeWidth: unit * 0.012, cap: 'round'});
    }
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx - unit * 0.105, tapY), end: new Off(cx + unit * 0.105, tapY), strokeWidth: unit * 0.026, cap: 'round'});
    d.drawCircle({color: p.ink.copy(0.90), radius: unit * 0.050, center: new Off(cx, tapY)});
    d.drawLine({color: p.ink.copy(0.80), start: new Off(cx, tapY), end: new Off(cx, tipY), strokeWidth: unit * 0.016, cap: 'round'});
    const neck = unit * 0.055;
    const fTop = h * 0.66;
    const fBot = h * 0.94;
    const fBase = unit * 0.25;
    for (let i = Math.trunc(0); i < Math.trunc(2); i++) {
      d.drawCircle({color: p.ink.copy(0.70 - i * 0.28), radius: unit * (0.034 - i * 0.009), center: new Off(cx, tipY + unit * (0.07 + i * 0.11))});
    }
    const liq = fBot - (fBot - fTop) * 0.34;
    const lw = neck + (fBase - neck) * (liq - fTop) / (fBot - fTop);
    const pool = new P();
    pool.moveTo(cx - lw, liq);
    pool.lineTo(cx + lw, liq);
    pool.lineTo(cx + fBase, fBot);
    pool.lineTo(cx - fBase, fBot);
    pool.close();
    d.drawPath({path: pool, color: p.ink.copy(0.26)});
    const flask = new P();
    flask.moveTo(cx - neck, fTop);
    flask.lineTo(cx - fBase, fBot);
    flask.lineTo(cx + fBase, fBot);
    flask.lineTo(cx + neck, fTop);
    d.drawPath({path: flask, color: p.ink.copy(0.82), style: Stroke({width: unit * 0.022, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.72), start: new Off(cx - lw, liq), end: new Off(cx + lw, liq), strokeWidth: unit * 0.018, cap: 'round'});
    const stands = Math.min(Math.max(Math.trunc(((w / h) * 1.2)), 0), 2);
    for (let i = Math.trunc(0); i < Math.trunc(stands); i++) {
      const sx = ((i == 0) ? (cx - unit * 0.52) : (cx + unit * 0.52));
      d.drawLine({color: p.ink.copy(0.22), start: new Off(sx, h * 0.10), end: new Off(sx, h * 0.94), strokeWidth: unit * 0.022, cap: 'round'});
      d.drawLine({color: p.ink.copy(0.22), start: new Off(sx, h * 0.26), end: new Off(cx - half - unit * 0.01, h * 0.26), strokeWidth: unit * 0.016, cap: 'round'});
    }
  }
  function artCalendar(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cw = unit * 0.80;
    const ch = unit * 0.76;
    const ox = w * 0.5 - cw * 0.5;
    const oy = h * 0.5 - ch * 0.5 + unit * 0.03;
    const head = ch * 0.24;
    d.drawRect({color: p.ink.copy(0.08), topLeft: new Off(ox, oy), size: new Sz(cw, ch)});
    d.drawRect({color: p.ink.copy(0.72), topLeft: new Off(ox, oy), size: new Sz(cw, head)});
    d.drawRect({color: p.ink.copy(0.82), topLeft: new Off(ox, oy), size: new Sz(cw, ch), style: Stroke({width: unit * 0.020})});
    for (let i = Math.trunc(0); i < Math.trunc(2); i++) {
      const rx = ox + cw * (0.26 + i * 0.48);
      d.drawLine({color: p.ink.copy(0.85), start: new Off(rx, oy - unit * 0.07), end: new Off(rx, oy + head * 0.40), strokeWidth: unit * 0.024, cap: 'round'});
    }
    const cols = 5;
    const rows = 3;
    const gx = cw / (cols + 1);
    const gy = (ch - head) / (rows + 1);
    const mark = 1 + r.int(cols * rows - 2);
    for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
      for (let rw = Math.trunc(0); rw < Math.trunc(rows); rw++) {
        const dx = ox + gx * (c + 1);
        const dy = oy + head + gy * (rw + 1);
        const idx = rw * cols + c;
        if (idx == mark) {
          d.drawCircle({color: p.ink.copy(0.88), radius: unit * 0.055, center: new Off(dx, dy)});
          d.drawCircle({color: p.ink.copy(0.50), radius: unit * 0.090, center: new Off(dx, dy), style: Stroke({width: unit * 0.014})});
        } else {
          d.drawCircle({color: p.ink.copy(((idx < mark) ? (0.20) : (0.40))), radius: unit * 0.032, center: new Off(dx, dy)});
        }
      }
    }
  }
  function artCell(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const cy = h * 0.52;
    const rad = unit * 0.42;
    d.drawCircle({color: p.ink.copy(0.10), radius: rad, center: new Off(cx, cy)});
    d.drawCircle({color: p.ink.copy(0.80), radius: rad, center: new Off(cx, cy), style: Stroke({width: unit * 0.024})});
    d.drawCircle({color: p.ink.copy(0.34), radius: rad * 0.88, center: new Off(cx, cy), style: Stroke({width: unit * 0.013})});
    const nx = cx - rad * 0.16;
    const ny = cy - rad * 0.08;
    d.drawCircle({color: p.ink.copy(0.30), radius: rad * 0.40, center: new Off(nx, ny)});
    d.drawCircle({color: p.ink.copy(0.85), radius: rad * 0.40, center: new Off(nx, ny), style: Stroke({width: unit * 0.018})});
    d.drawCircle({color: p.ink.copy(0.90), radius: rad * 0.15, center: new Off(nx + rad * 0.08, ny - rad * 0.06)});
    for (let i = Math.trunc(0); i < Math.trunc(5); i++) {
      const a = r.range(0, 6.2832);
      const dist = rad * r.range(0.52, 0.82);
      const ex = cx + Math.cos(a) * dist;
      const ey = cy + Math.sin(a) * dist * 0.94;
      d.drawArc({color: p.ink.copy(0.52), startAngle: r.range(0, 360), sweepAngle: 180 + r.range(0, 120), useCenter: false, topLeft: new Off(ex - rad * 0.16, ey - rad * 0.10), size: new Sz(rad * 0.32, rad * 0.20), style: Stroke({width: unit * 0.016, cap: 'round'})});
    }
    for (let i = Math.trunc(0); i < Math.trunc(7); i++) {
      const a = r.range(0, 6.2832);
      const dist = rad * r.range(0.30, 0.90);
      d.drawCircle({color: p.ink.copy(0.34), radius: unit * r.range(0.014, 0.026), center: new Off(cx + Math.cos(a) * dist, cy + Math.sin(a) * dist * 0.94)});
    }
  }
  function artChecklist(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const box = unit * 0.17;
    const rule = box * 1.55;
    const rows = Math.min(Math.max(Math.trunc((h * 0.84 / rule)), 2), 5);
    const ox = w * 0.12;
    const oy = h * 0.5 - (rows - 1) * rule * 0.5;
    for (let i = Math.trunc(0); i < Math.trunc(rows); i++) {
      const cy = oy + i * rule;
      const done = i < rows - 1;
      d.drawRect({color: p.ink.copy(((done) ? (0.80) : (0.16))), topLeft: new Off(ox, cy - box * 0.5), size: new Sz(box, box)});
      d.drawRect({color: p.ink.copy(((done) ? (0.88) : (0.55))), topLeft: new Off(ox, cy - box * 0.5), size: new Sz(box, box), style: Stroke({width: unit * 0.018})});
      if (done) {
        const tick = new P();
        tick.moveTo(ox + box * 0.22, cy + box * 0.02);
        tick.lineTo(ox + box * 0.44, cy + box * 0.24);
        tick.lineTo(ox + box * 0.80, cy - box * 0.26);
        d.drawPath({path: tick, color: p.paper.copy(0.92), style: Stroke({width: unit * 0.026, cap: 'round'})});
      }
      const sx = ox + box * 1.55;
      const frac = ((i == rows - 1) ? (0.52) : (0.72 + r.range(0, 0.24)));
      d.drawLine({color: p.ink.copy(((done) ? (0.30) : (0.50))), start: new Off(sx, cy), end: new Off(sx + (w * 0.92 - sx) * frac, cy), strokeWidth: unit * 0.032, cap: 'round'});
      if (done) {
        d.drawLine({color: p.ink.copy(0.55), start: new Off(sx, cy), end: new Off(sx + (w * 0.92 - sx) * frac, cy), strokeWidth: unit * 0.010});
      }
    }
  }
  function artChevrons(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cy = h * 0.52;
    const x0 = w * r.range(0.06, 0.16);
    const step = w * 0.13;
    const arm = h * 0.34;
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      const x = x0 + i * step;
      const chev = new P();
      chev.moveTo(x, cy - arm);
      chev.lineTo(x + h * 0.26, cy);
      chev.lineTo(x, cy + arm);
      d.drawPath({path: chev, color: p.ink.copy(0.16 + i * 0.115), style: Stroke({width: h * 0.034, cap: 'round'})});
    }
  }
  function artChip(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const half = unit * 0.30;
    const cx = w * 0.50;
    const cy = h * 0.52;
    const pins = 4;
    const leg = unit * 0.13;
    for (let side = Math.trunc(0); side < Math.trunc(4); side++) {
      for (let i = Math.trunc(0); i < Math.trunc(pins); i++) {
        const t = (i + 0.5) / pins;
        const px0 = cx - half + half * 2 * t;
        const py0 = cy - half + half * 2 * t;
        if (side == 0) {
          d.drawLine({color: p.ink.copy(0.55), start: new Off(px0, cy - half), end: new Off(px0, cy - half - leg), strokeWidth: unit * 0.024, cap: 'round'});
        } else if (side == 1) {
          d.drawLine({color: p.ink.copy(0.55), start: new Off(px0, cy + half), end: new Off(px0, cy + half + leg), strokeWidth: unit * 0.024, cap: 'round'});
        } else if (side == 2) {
          d.drawLine({color: p.ink.copy(0.55), start: new Off(cx - half, py0), end: new Off(cx - half - leg, py0), strokeWidth: unit * 0.024, cap: 'round'});
        } else {
          d.drawLine({color: p.ink.copy(0.55), start: new Off(cx + half, py0), end: new Off(cx + half + leg, py0), strokeWidth: unit * 0.024, cap: 'round'});
        }
      }
    }
    d.drawRect({color: p.ink.copy(0.16), topLeft: new Off(cx - half, cy - half), size: new Sz(half * 2, half * 2)});
    d.drawRect({color: p.ink.copy(0.85), topLeft: new Off(cx - half, cy - half), size: new Sz(half * 2, half * 2), style: Stroke({width: unit * 0.024})});
    d.drawRect({color: p.ink.copy(0.34), topLeft: new Off(cx - half * 0.56, cy - half * 0.56), size: new Sz(half * 1.12, half * 1.12), style: Stroke({width: unit * 0.014})});
    d.drawCircle({color: p.ink.copy(0.70), radius: unit * 0.034, center: new Off(cx - half * 0.74, cy - half * 0.74)});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const ty = cy - half * 0.30 + i * half * 0.30;
      d.drawLine({color: p.ink.copy(0.34), start: new Off(cx - half * 0.40, ty), end: new Off(cx + half * 0.40, ty), strokeWidth: unit * 0.013});
    }
    const trace = Math.min(Math.max(Math.trunc(((w / h) * 1.6)), 1), 5);
    for (let i = Math.trunc(0); i < Math.trunc(trace); i++) {
      const ty = h * (0.16 + i * 0.18);
      d.drawLine({color: p.ink.copy(0.14), start: new Off(0, ty), end: new Off(w, ty), strokeWidth: unit * 0.011});
    }
  }
  function artCircuit(d, p, r) {
    const w = d.w;
    const h = d.h;
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const y = h * (0.26 + i * 0.24);
      const turn = w * r.range(0.30, 0.62);
      const y2 = y + h * (r.range(0.10, 0.22));
      const trace = new P();
      trace.moveTo(0, y);
      trace.lineTo(turn, y);
      trace.lineTo(turn + h * 0.16, y2);
      trace.lineTo(w, y2);
      d.drawPath({path: trace, color: p.ink.copy(0.55 - i * 0.08), style: Stroke({width: h * 0.022, cap: 'round'})});
      d.drawCircle({color: p.ink.copy(0.80), radius: h * 0.042, center: new Off(turn, y)});
      d.drawCircle({color: p.paper.copy(0.75), radius: h * 0.016, center: new Off(turn, y)});
    }
    const bx = w * 0.72;
    const by = h * 0.62;
    d.drawRect({color: p.ink.copy(0.24), topLeft: new Off(bx, by), size: new Sz(h * 0.34, h * 0.30)});
    d.drawRect({color: p.ink.copy(0.75), topLeft: new Off(bx, by), size: new Sz(h * 0.34, h * 0.30), style: Stroke({width: h * 0.020})});
  }
  function artClock(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const cy = h * 0.52;
    const rad = unit * 0.40;
    d.drawCircle({color: p.ink.copy(0.09), radius: rad, center: new Off(cx, cy)});
    const spent = 120 + r.range(0, 160);
    d.drawArc({color: p.ink.copy(0.26), startAngle: -90, sweepAngle: spent, useCenter: true, topLeft: new Off(cx - rad * 0.94, cy - rad * 0.94), size: new Sz(rad * 1.88, rad * 1.88)});
    d.drawCircle({color: p.ink.copy(0.84), radius: rad, center: new Off(cx, cy), style: Stroke({width: unit * 0.024})});
    for (let i = Math.trunc(0); i < Math.trunc(12); i++) {
      const a = i * (Math.PI / 6);
      const major = i % 3 == 0;
      d.drawLine({color: p.ink.copy(((major) ? (0.66) : (0.30))), start: new Off(cx + Math.cos(a) * rad * (((major) ? (0.76) : (0.84))), cy + Math.sin(a) * rad * (((major) ? (0.76) : (0.84)))), end: new Off(cx + Math.cos(a) * rad * 0.92, cy + Math.sin(a) * rad * 0.92), strokeWidth: unit * (((major) ? (0.020) : (0.012))), cap: 'round'});
    }
    const ha = (-90 + spent * 0.34) * Math.PI / 180;
    const ma = (-90 + spent) * Math.PI / 180;
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx, cy), end: new Off(cx + Math.cos(ha) * rad * 0.48, cy + Math.sin(ha) * rad * 0.48), strokeWidth: unit * 0.030, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx, cy), end: new Off(cx + Math.cos(ma) * rad * 0.72, cy + Math.sin(ma) * rad * 0.72), strokeWidth: unit * 0.022, cap: 'round'});
    d.drawCircle({color: p.ink, radius: unit * 0.040, center: new Off(cx, cy)});
    d.drawCircle({color: p.paper.copy(0.80), radius: unit * 0.014, center: new Off(cx, cy)});
  }
  function artCoins(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const rx = unit * 0.22;
    const ry = rx * 0.34;
    const thick = ry * 0.85;
    const stacks = Math.min(Math.max(Math.trunc((w / (rx * 2.6))), 2), 6);
    const gap = w / (stacks + 0.6);
    const ground = h * 0.88;
    for (let s = Math.trunc(0); s < Math.trunc(stacks); s++) {
      const cx = gap * (s + 0.8);
      const n = 2 + r.int(4);
      for (let i = Math.trunc(0); i < Math.trunc(n); i++) {
        const cy = ground - ry - i * thick;
        d.drawArc({color: p.ink.copy(0.20), startAngle: 0, sweepAngle: 180, useCenter: true, topLeft: new Off(cx - rx, cy - ry), size: new Sz(rx * 2, ry * 2)});
        d.drawLine({color: p.ink.copy(0.70), start: new Off(cx - rx, cy), end: new Off(cx - rx, cy - thick * 0.02), strokeWidth: unit * 0.016});
        d.drawArc({color: p.ink.copy(0.78), startAngle: 0, sweepAngle: 180, useCenter: false, topLeft: new Off(cx - rx, cy - ry), size: new Sz(rx * 2, ry * 2), style: Stroke({width: unit * 0.018, cap: 'round'})});
        if (i == n - 1) {
          d.drawArc({color: p.ink.copy(0.14), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rx, cy - ry - thick), size: new Sz(rx * 2, ry * 2)});
          d.drawArc({color: p.ink.copy(0.85), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rx, cy - ry - thick), size: new Sz(rx * 2, ry * 2), style: Stroke({width: unit * 0.020})});
          d.drawArc({color: p.ink.copy(0.40), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rx * 0.52, cy - ry * 0.52 - thick), size: new Sz(rx * 1.04, ry * 1.04), style: Stroke({width: unit * 0.013})});
        }
      }
    }
    d.drawLine({color: p.ink.copy(0.30), start: new Off(w * 0.02, ground + ry * 0.3), end: new Off(w * 0.98, ground + ry * 0.3), strokeWidth: unit * 0.012});
  }
  function artComet(d, p, r) {
    const w = d.w;
    const h = d.h;
    const x0 = w * 0.02;
    const y0 = h * 0.92;
    const x1 = w * 0.40;
    const y1 = h * 0.88;
    const x2 = w * (0.72 + r.range(-0.05, 0.05));
    const y2 = h * 0.30;
    const tail = new P();
    for (let i = Math.trunc(0); i < Math.trunc(26); i++) {
      const f = i / 25;
      const u = 1 - f;
      const cxp = u * u * x0 + 2 * u * f * x1 + f * f * x2;
      const cyp = u * u * y0 + 2 * u * f * y1 + f * f * y2;
      const dx = 2 * (u * (x1 - x0) + f * (x2 - x1));
      const dy = 2 * (u * (y1 - y0) + f * (y2 - y1));
      const len = Math.sqrt(dx * dx + dy * dy);
      const hw = h * 0.155 * f * f;
      if (i == 0) {
        tail.moveTo(cxp - dy / len * hw, cyp + dx / len * hw);
      } else {
        tail.lineTo(cxp - dy / len * hw, cyp + dx / len * hw);
      }
    }
    for (let i = Math.trunc(0); i < Math.trunc(26); i++) {
      const f = (25 - i) / 25;
      const u = 1 - f;
      const cxp = u * u * x0 + 2 * u * f * x1 + f * f * x2;
      const cyp = u * u * y0 + 2 * u * f * y1 + f * f * y2;
      const dx = 2 * (u * (x1 - x0) + f * (x2 - x1));
      const dy = 2 * (u * (y1 - y0) + f * (y2 - y1));
      const len = Math.sqrt(dx * dx + dy * dy);
      const hw = h * 0.155 * f * f;
      tail.lineTo(cxp + dy / len * hw, cyp - dx / len * hw);
    }
    tail.close();
    d.drawPath({path: tail, color: p.ink.copy(0.52)});
    d.drawCircle({color: p.ink, radius: h * 0.105, center: new Off(x2, y2)});
    d.drawCircle({color: p.ink.copy(0.42), radius: h * 0.200, center: new Off(x2, y2), style: Stroke({width: h * 0.016})});
    for (let i = Math.trunc(0); i < Math.trunc(5); i++) {
      d.drawCircle({color: p.ink.copy(0.16 + r.range(0, 0.20)), radius: h * 0.018, center: new Off(w * r.range(0.04, 0.96), h * r.range(0.06, 0.92))});
    }
  }
  function artCompass(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const cy = h * 0.52;
    const rad = unit * 0.42;
    d.drawCircle({color: p.ink.copy(0.09), radius: rad, center: new Off(cx, cy)});
    d.drawCircle({color: p.ink.copy(0.80), radius: rad, center: new Off(cx, cy), style: Stroke({width: unit * 0.022})});
    d.drawCircle({color: p.ink.copy(0.26), radius: rad * 0.86, center: new Off(cx, cy), style: Stroke({width: unit * 0.011})});
    const ticks = 16;
    for (let i = Math.trunc(0); i < Math.trunc(ticks); i++) {
      const a = i * (Math.PI * 2 / ticks);
      const major = i % 4 == 0;
      const r0 = rad * (((major) ? (0.70) : (0.80)));
      d.drawLine({color: p.ink.copy(((major) ? (0.62) : (0.30))), start: new Off(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0), end: new Off(cx + Math.cos(a) * rad * 0.92, cy + Math.sin(a) * rad * 0.92), strokeWidth: unit * (((major) ? (0.018) : (0.011))), cap: 'round'});
    }
    const spin = r.range(-0.5, 0.5) - Math.PI / 2;
    const nx = Math.cos(spin);
    const ny = Math.sin(spin);
    const wing = rad * 0.20;
    const nd = new P();
    nd.moveTo(cx + nx * rad * 0.80, cy + ny * rad * 0.80);
    nd.lineTo(cx - ny * wing, cy + nx * wing);
    nd.lineTo(cx + ny * wing, cy - nx * wing);
    nd.close();
    d.drawPath({path: nd, color: p.ink.copy(0.88)});
    const sd = new P();
    sd.moveTo(cx - nx * rad * 0.80, cy - ny * rad * 0.80);
    sd.lineTo(cx - ny * wing, cy + nx * wing);
    sd.lineTo(cx + ny * wing, cy - nx * wing);
    sd.close();
    d.drawPath({path: sd, color: p.ink.copy(0.30)});
    d.drawCircle({color: p.field, radius: unit * 0.060, center: new Off(cx, cy)});
    d.drawCircle({color: p.ink.copy(0.85), radius: unit * 0.052, center: new Off(cx, cy), style: Stroke({width: unit * 0.018})});
  }
  function artConstellation(d, p, r) {
    const w = d.w;
    const h = d.h;
    const link = new P();
    let bx = 0;
    let by = 0;
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      const f = (i + 0.5) / 6;
      const x = w * (0.10 + f * 0.80) + w * r.range(-0.035, 0.035);
      const y = h * (0.34 + Math.sin(f * 5.4) * 0.22) + h * r.range(-0.06, 0.06);
      if (i == 0) {
        link.moveTo(x, y);
      } else {
        link.lineTo(x, y);
      }
      d.drawCircle({color: p.ink.copy(0.90), radius: h * (0.030 + r.range(0, 0.026)), center: new Off(x, y)});
      if (i == 3) {
        bx = x;
        by = y;
      }
    }
    d.drawPath({path: link, color: p.ink.copy(0.44), style: Stroke({width: h * 0.016})});
    d.drawCircle({color: p.ink, radius: h * 0.062, center: new Off(bx, by)});
    d.drawCircle({color: p.ink.copy(0.35), radius: h * 0.135, center: new Off(bx, by), style: Stroke({width: h * 0.014})});
    for (let i = Math.trunc(0); i < Math.trunc(9); i++) {
      d.drawCircle({color: p.ink.copy(0.16 + r.range(0, 0.14)), radius: h * 0.013, center: new Off(w * r.range(0.02, 0.98), h * r.range(0.06, 0.94))});
    }
  }
  function artContours(d, p, r) {
    const w = d.w;
    const h = d.h;
    const k = 0.5523;
    const cx = w * r.range(0.46, 0.62);
    const cy = h * 0.54;
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      const s = 0.13 + i * 0.155;
      const rx = w * 0.52 * s + w * 0.02;
      const ry = h * 1.05 * s + h * 0.04;
      const ox = cx + w * 0.02 * i * r.range(-1, 1);
      const oy = cy + h * 0.03 * i * r.range(-1, 1);
      const path = new P();
      path.moveTo(ox, oy - ry);
      path.cubicTo(ox + rx * k, oy - ry, ox + rx, oy - ry * k, ox + rx, oy);
      path.cubicTo(ox + rx, oy + ry * k, ox + rx * k, oy + ry, ox, oy + ry);
      path.cubicTo(ox - rx * k, oy + ry, ox - rx, oy + ry * k, ox - rx, oy);
      path.cubicTo(ox - rx, oy - ry * k, ox - rx * k, oy - ry, ox, oy - ry);
      path.close();
      d.drawPath({path: path, color: p.ink.copy(0.54 - i * 0.070), style: Stroke({width: h * 0.022})});
    }
    d.drawCircle({color: p.ink, radius: h * 0.045, center: new Off(cx, cy)});
  }
  function artDotMatrix(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cols = 12;
    const rows = 4;
    for (let yi = Math.trunc(0); yi < Math.trunc(rows); yi++) {
      for (let xi = Math.trunc(0); xi < Math.trunc(cols); xi++) {
        const fx = (xi + 0.5) / cols;
        const fy = (yi + 0.5) / rows;
        const rad = h * 0.034 * (0.50 + fy * 0.95) * (1.22 - fx * 0.62);
        d.drawCircle({color: p.ink.copy(0.14 + fy * 0.34), radius: rad, center: new Off(w * fx, h * (0.16 + fy * 0.74))});
      }
    }
    const ai = r.int(cols - 4) + 2;
    const ax = w * ((ai + 0.5) / cols);
    d.drawCircle({color: p.ink, radius: h * 0.088, center: new Off(ax, h * 0.53)});
    d.drawCircle({color: p.ink.copy(0.55), radius: h * 0.052, center: new Off(ax, h * 0.16)});
  }
  function artDrop(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const drops = Math.min(Math.max(Math.trunc(((w / h) * 1.6)), 1), 5);
    for (let k = Math.trunc(0); k < Math.trunc(drops); k++) {
      const lead = k == 0;
      const sc = ((lead) ? (1) : (0.42 + r.range(0, 0.22)));
      const cx = ((lead) ? (w * 0.46) : (w * (0.10 + k * 0.21)));
      const cy = ((lead) ? (h * 0.56) : (h * (0.24 + (k % 2) * 0.50)));
      const rad = unit * 0.28 * sc;
      const al = ((lead) ? (0.86) : (0.30));
      const shape = new P();
      shape.moveTo(cx, cy - rad * 1.70);
      shape.cubicTo(cx + rad * 0.52, cy - rad * 0.86, cx + rad, cy - rad * 0.30, cx + rad, cy + rad * 0.18);
      shape.cubicTo(cx + rad, cy + rad * 1.02, cx - rad, cy + rad * 1.02, cx - rad, cy + rad * 0.18);
      shape.cubicTo(cx - rad, cy - rad * 0.30, cx - rad * 0.52, cy - rad * 0.86, cx, cy - rad * 1.70);
      shape.close();
      d.drawPath({path: shape, color: p.ink.copy(al * 0.22)});
      d.drawPath({path: shape, color: p.ink.copy(al), style: Stroke({width: unit * 0.022 * (0.6 + sc * 0.4), cap: 'round'})});
      if (lead) {
        d.drawArc({color: p.paper.copy(0.42), startAngle: 130, sweepAngle: 80, useCenter: false, topLeft: new Off(cx - rad * 0.58, cy - rad * 0.50), size: new Sz(rad * 1.16, rad * 1.16), style: Stroke({width: unit * 0.028, cap: 'round'})});
        for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
          d.drawArc({color: p.ink.copy(0.22 - i * 0.05), startAngle: 200, sweepAngle: 140, useCenter: false, topLeft: new Off(cx - rad * (1.5 + i * 0.5), cy + rad * (0.80 - (0.24 + i * 0.10))), size: new Sz(rad * (3.0 + i * 1.0), rad * (0.48 + i * 0.20)), style: Stroke({width: unit * 0.013, cap: 'round'})});
        }
      }
    }
  }
  function artEclipse(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cx = w * r.range(0.42, 0.58);
    const cy = h * 0.52;
    const rad = h * 0.34;
    d.drawCircle({color: p.ink.copy(0.88), radius: rad, center: new Off(cx, cy)});
    d.drawCircle({color: p.field, radius: rad * 0.88, center: new Off(cx + rad * 0.52, cy - rad * 0.30)});
    d.drawCircle({color: p.ink.copy(0.42), radius: rad * 1.42, center: new Off(cx, cy), style: Stroke({width: h * 0.018})});
    d.drawCircle({color: p.ink.copy(0.24), radius: rad * 1.86, center: new Off(cx, cy), style: Stroke({width: h * 0.014})});
  }
  function artFieldLines(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cy = h * 0.52;
    const half = w * 0.13;
    const bar = h * 0.11;
    const loops = Math.min(Math.max(Math.trunc(((w / h) * 1.4)), 2), 6);
    for (let i = Math.trunc(0); i < Math.trunc(loops); i++) {
      const f = (i + 1) / loops;
      const rx = half + w * 0.10 + f * w * 0.30;
      const ry = bar * 1.6 + f * h * 0.42;
      d.drawArc({color: p.ink.copy(0.34 - f * 0.16), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(w * 0.5 - rx, cy - ry), size: new Sz(rx * 2, ry * 2), style: Stroke({width: unit * 0.015})});
    }
    d.drawRect({color: p.ink.copy(0.30), topLeft: new Off(w * 0.5 - half, cy - bar), size: new Sz(half, bar * 2)});
    d.drawRect({color: p.ink.copy(0.88), topLeft: new Off(w * 0.5, cy - bar), size: new Sz(half, bar * 2)});
    d.drawRect({color: p.ink.copy(0.72), topLeft: new Off(w * 0.5 - half, cy - bar), size: new Sz(half * 2, bar * 2), style: Stroke({width: unit * 0.018})});
    const tick = unit * 0.055;
    d.drawLine({color: p.paper.copy(0.85), start: new Off(w * 0.5 + half * 0.5 - tick, cy), end: new Off(w * 0.5 + half * 0.5 + tick, cy), strokeWidth: unit * 0.020, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.80), start: new Off(w * 0.5 - half * 0.5, cy - tick), end: new Off(w * 0.5 - half * 0.5, cy + tick), strokeWidth: unit * 0.020, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.80), start: new Off(w * 0.5 - half * 0.5 - tick, cy), end: new Off(w * 0.5 - half * 0.5 + tick, cy), strokeWidth: unit * 0.020, cap: 'round'});
  }
  function artFlask(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const top = h * 0.12;
    const bot = h * 0.84;
    const neck = unit * 0.11;
    const base = unit * 0.40;
    const liq = bot - (bot - top) * 0.34;
    const body = new P();
    body.moveTo(cx - neck, top);
    body.lineTo(cx - neck, top + (bot - top) * 0.28);
    body.lineTo(cx - base, bot - unit * 0.07);
    body.cubicTo(cx - base, bot, cx - base, bot, cx - base + unit * 0.08, bot);
    body.lineTo(cx + base - unit * 0.08, bot);
    body.cubicTo(cx + base, bot, cx + base, bot, cx + base, bot - unit * 0.07);
    body.lineTo(cx + neck, top + (bot - top) * 0.28);
    body.lineTo(cx + neck, top);
    d.drawPath({path: body, color: p.ink.copy(0.82), style: Stroke({width: unit * 0.022, cap: 'round'})});
    const shoulder = top + (bot - top) * 0.28;
    const lw = neck + (base - neck) * (liq - shoulder) / (bot - shoulder);
    const fill = new P();
    fill.moveTo(cx - lw, liq);
    fill.lineTo(cx + lw, liq);
    fill.lineTo(cx + base, bot);
    fill.lineTo(cx - base, bot);
    fill.close();
    d.drawPath({path: fill, color: p.ink.copy(0.24)});
    d.drawLine({color: p.ink.copy(0.70), start: new Off(cx - lw, liq), end: new Off(cx + lw, liq), strokeWidth: unit * 0.018, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.78), start: new Off(cx - neck - unit * 0.05, top), end: new Off(cx + neck + unit * 0.05, top), strokeWidth: unit * 0.024, cap: 'round'});
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      const bx = cx + r.range(-0.60, 0.60) * base;
      const by = liq + r.range(0.08, 0.82) * (bot - liq);
      d.drawCircle({color: p.ink.copy(0.40), radius: unit * r.range(0.016, 0.036), center: new Off(bx, by), style: Stroke({width: unit * 0.010})});
    }
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      d.drawCircle({color: p.ink.copy(0.30 - i * 0.08), radius: unit * (0.024 + i * 0.012), center: new Off(cx + unit * (0.05 - i * 0.06), top - unit * (0.06 + i * 0.14))});
    }
  }
  function artGeometry(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const ax = w * 0.50 + r.range(-0.06, 0.10) * w;
    const ay = h * 0.12;
    const bx = w * 0.22;
    const by = h * 0.86;
    const cx = w * 0.78;
    const cy = h * 0.86;
    const tri = new P();
    tri.moveTo(ax, ay);
    tri.lineTo(cx, cy);
    tri.lineTo(bx, by);
    tri.close();
    d.drawPath({path: tri, color: p.ink.copy(0.14)});
    d.drawPath({path: tri, color: p.ink.copy(0.86), style: Stroke({width: unit * 0.022, cap: 'round'})});
    const ix = (ax + bx + cx) / 3;
    const iy = (ay + by + cy) / 3;
    const inr = (by - ay) * 0.26;
    d.drawCircle({color: p.ink.copy(0.50), radius: inr, center: new Off(ix, iy), style: Stroke({width: unit * 0.016})});
    d.drawLine({color: p.ink.copy(0.34), start: new Off(ax, ay), end: new Off((bx + cx) * 0.5, by), strokeWidth: unit * 0.013});
    d.drawLine({color: p.ink.copy(0.34), start: new Off(ax, ay), end: new Off(ax, by), strokeWidth: unit * 0.013});
    const sq = unit * 0.085;
    d.drawLine({color: p.ink.copy(0.60), start: new Off(ax, by - sq), end: new Off(ax + sq, by - sq), strokeWidth: unit * 0.014});
    d.drawLine({color: p.ink.copy(0.60), start: new Off(ax + sq, by - sq), end: new Off(ax + sq, by), strokeWidth: unit * 0.014});
    d.drawCircle({color: p.ink, radius: unit * 0.046, center: new Off(ax, ay)});
    d.drawCircle({color: p.ink, radius: unit * 0.046, center: new Off(bx, by)});
    d.drawCircle({color: p.ink, radius: unit * 0.046, center: new Off(cx, cy)});
  }
  function artGlobe(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const cy = h * 0.52;
    const rad = unit * 0.42;
    d.drawCircle({color: p.ink.copy(0.10), radius: rad, center: new Off(cx, cy)});
    d.drawCircle({color: p.ink.copy(0.84), radius: rad, center: new Off(cx, cy), style: Stroke({width: unit * 0.024})});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const f = (i + 1) / 4;
      const yy = cy - rad * 0.66 + rad * 1.32 * f;
      const rr = Math.sqrt(rad * rad - (yy - cy) * (yy - cy));
      d.drawLine({color: p.ink.copy(0.40), start: new Off(cx - rr, yy), end: new Off(cx + rr, yy), strokeWidth: unit * 0.014, cap: 'round'});
    }
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const f = (i + 0.5) / 3;
      const rx = rad * Math.abs(Math.cos(f * Math.PI));
      d.drawArc({color: p.ink.copy(0.40), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rx, cy - rad), size: new Sz(rx * 2, rad * 2), style: Stroke({width: unit * 0.014})});
    }
    d.drawLine({color: p.ink.copy(0.55), start: new Off(cx, cy - rad), end: new Off(cx, cy + rad), strokeWidth: unit * 0.014});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const a = r.range(0, 6.2832);
      const dist = rad * r.range(0.20, 0.74);
      d.drawCircle({color: p.ink.copy(0.66), radius: unit * 0.036, center: new Off(cx + Math.cos(a) * dist, cy + Math.sin(a) * dist)});
    }
  }
  function artGraph(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cols = Math.min(Math.max(Math.trunc(((w / h) * 1.5)), 2), 6);
    const step = w * 0.86 / (cols - 1 + 0.001);
    const ox = w * 0.07;
    for (let c = Math.trunc(0); c < Math.trunc(cols - 1); c++) {
      const n0 = 1 + ((c + r.int(2)) % 2);
      const n1 = 1 + ((c + 1 + r.int(2)) % 2);
      for (let a = Math.trunc(0); a < Math.trunc(n0); a++) {
        for (let b = Math.trunc(0); b < Math.trunc(n1); b++) {
          const y0 = h * (0.5 + (a - (n0 - 1) * 0.5) * 0.40);
          const y1 = h * (0.5 + (b - (n1 - 1) * 0.5) * 0.40);
          d.drawLine({color: p.ink.copy(0.32), start: new Off(ox + c * step, y0), end: new Off(ox + (c + 1) * step, y1), strokeWidth: unit * 0.014, cap: 'round'});
        }
      }
    }
    for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
      const n = 1 + ((c + r.int(2)) % 2);
      for (let a = Math.trunc(0); a < Math.trunc(n); a++) {
        const y = h * (0.5 + (a - (n - 1) * 0.5) * 0.40);
        const cxx = ox + c * step;
        d.drawCircle({color: p.field, radius: unit * 0.088, center: new Off(cxx, y)});
        d.drawCircle({color: p.ink.copy(0.85), radius: unit * 0.082, center: new Off(cxx, y)});
        d.drawCircle({color: p.paper.copy(0.55), radius: unit * 0.030, center: new Off(cxx - unit * 0.022, y - unit * 0.024)});
      }
    }
  }
  function artHatch(d, p, r) {
    const w = d.w;
    const h = d.h;
    const span = w + h;
    const n = Math.min(Math.max(Math.trunc((span / (h * 0.20))), 8), 34);
    const off = r.range(0, 1);
    for (let i = Math.trunc(0); i < Math.trunc(n); i++) {
      const f = (i + off) / n;
      const x = f * span - h;
      d.drawLine({color: p.ink.copy(0.09 + 0.19 * (1 - f)), start: new Off(x, 0), end: new Off(x + h, h), strokeWidth: h * 0.022});
    }
    const bx = w * 0.56;
    const by = h * 0.24;
    const bw = w * 0.34;
    const bh = h * 0.52;
    d.drawRect({color: p.field.copy(0.94), topLeft: new Off(bx, by), size: new Sz(bw, bh)});
    d.drawRect({color: p.ink.copy(0.70), topLeft: new Off(bx, by), size: new Sz(bw, bh), style: Stroke({width: h * 0.020})});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      d.drawLine({color: p.ink.copy(0.52), start: new Off(bx + bw * 0.14, by + bh * (0.28 + i * 0.22)), end: new Off(bx + bw * (0.86 - i * 0.18), by + bh * (0.28 + i * 0.22)), strokeWidth: h * 0.017, cap: 'round'});
    }
  }
  function artHelix(d, p, r) {
    const w = d.w;
    const h = d.h;
    const mid = h * 0.52;
    const amp = h * 0.28;
    const phase = r.range(0, 3.1);
    const turns = 2.4;
    const a = new P();
    const b = new P();
    for (let i = Math.trunc(0); i < Math.trunc(41); i++) {
      const f = i / 40;
      const t = phase + f * turns * Math.PI * 2;
      const x = w * f;
      if (i == 0) {
        a.moveTo(x, mid + Math.sin(t) * amp);
        b.moveTo(x, mid - Math.sin(t) * amp);
      } else {
        a.lineTo(x, mid + Math.sin(t) * amp);
        b.lineTo(x, mid - Math.sin(t) * amp);
      }
    }
    d.drawPath({path: a, color: p.ink.copy(0.72), style: Stroke({width: h * 0.026, cap: 'round'})});
    d.drawPath({path: b, color: p.ink.copy(0.38), style: Stroke({width: h * 0.026, cap: 'round'})});
    for (let i = Math.trunc(0); i < Math.trunc(11); i++) {
      const f = (i + 0.5) / 11;
      const t = phase + f * turns * Math.PI * 2;
      const x = w * f;
      d.drawLine({color: p.ink.copy(0.30), start: new Off(x, mid + Math.sin(t) * amp), end: new Off(x, mid - Math.sin(t) * amp), strokeWidth: h * 0.016, cap: 'round'});
    }
  }
  function artHorizon(d, p, r) {
    const w = d.w;
    const h = d.h;
    const sunX = w * r.range(0.60, 0.80);
    d.drawCircle({color: p.ink.copy(0.80), radius: h * 0.165, center: new Off(sunX, h * 0.34)});
    const back = new P();
    back.moveTo(0, h);
    back.lineTo(0, h * 0.66);
    back.cubicTo(w * 0.22, h * 0.46, w * 0.38, h * 0.74, w * 0.58, h * 0.60);
    back.cubicTo(w * 0.76, h * 0.48, w * 0.88, h * 0.66, w, h * 0.56);
    back.lineTo(w, h);
    back.close();
    d.drawPath({path: back, color: p.ink.copy(0.26)});
    const front = new P();
    front.moveTo(0, h);
    front.lineTo(0, h * 0.86);
    front.cubicTo(w * 0.24, h * 0.70, w * 0.44, h * 0.94, w * 0.66, h * 0.80);
    front.cubicTo(w * 0.82, h * 0.70, w * 0.92, h * 0.82, w, h * 0.76);
    front.lineTo(w, h);
    front.close();
    d.drawPath({path: front, color: p.ink.copy(0.54)});
    for (let i = Math.trunc(0); i < Math.trunc(2); i++) {
      d.drawLine({color: p.paper.copy(0.55 - i * 0.18), start: new Off(w * (0.07 + i * 0.05), h * (0.22 + i * 0.11)), end: new Off(w * (0.24 - i * 0.04), h * (0.22 + i * 0.11)), strokeWidth: h * 0.030, cap: 'round'});
    }
  }
  function artLattice(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const step = unit * 0.36;
    const skewX = step * 0.42;
    const skewY = step * 0.25;
    const cols = Math.min(Math.max(Math.trunc(((w - step * 1.4) / step)), 2), 7);
    const rows = ((h > unit * 0.9) ? (3) : (2));
    const ox = w * 0.5 - (cols - 1) * step * 0.5 - skewX * 0.5;
    const oy = h * 0.5 - (rows - 1) * step * 0.5 + skewY * 0.5;
    for (let dep = Math.trunc(0); dep < Math.trunc(2); dep++) {
      const dx = ox + dep * skewX;
      const dy = oy - dep * skewY;
      const al = ((dep == 0) ? (0.26) : (0.80));
      for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
        d.drawLine({color: p.ink.copy(al * 0.40), start: new Off(dx + c * step, dy), end: new Off(dx + c * step, dy + (rows - 1) * step), strokeWidth: unit * 0.013});
      }
      for (let rw = Math.trunc(0); rw < Math.trunc(rows); rw++) {
        d.drawLine({color: p.ink.copy(al * 0.40), start: new Off(dx, dy + rw * step), end: new Off(dx + (cols - 1) * step, dy + rw * step), strokeWidth: unit * 0.013});
      }
      for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
        for (let rw = Math.trunc(0); rw < Math.trunc(rows); rw++) {
          const big = (c + rw) % 2 == 0;
          d.drawCircle({color: p.ink.copy(al), radius: ((big) ? (unit * 0.068) : (unit * 0.040)), center: new Off(dx + c * step, dy + rw * step)});
        }
      }
    }
    for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
      for (let rw = Math.trunc(0); rw < Math.trunc(rows); rw++) {
        d.drawLine({color: p.ink.copy(0.24), start: new Off(ox + c * step, oy + rw * step), end: new Off(ox + skewX + c * step, oy - skewY + rw * step), strokeWidth: unit * 0.012});
      }
    }
  }
  function artLeaf(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const tipx = w * 0.78;
    const tipy = h * 0.16;
    const basex = w * 0.24;
    const basey = h * 0.86;
    const bow = unit * 0.40;
    const dx = tipx - basex;
    const dy = tipy - basey;
    const len = Math.sqrt(dx * dx + dy * dy);
    const nx = -dy / len;
    const ny = dx / len;
    const leaf = new P();
    leaf.moveTo(basex, basey);
    leaf.cubicTo( basex + dx * 0.20 + nx * bow, basey + dy * 0.20 + ny * bow, basex + dx * 0.72 + nx * bow * 0.82, basey + dy * 0.72 + ny * bow * 0.82, tipx, tipy );
    leaf.cubicTo( basex + dx * 0.72 - nx * bow * 0.82, basey + dy * 0.72 - ny * bow * 0.82, basex + dx * 0.20 - nx * bow, basey + dy * 0.20 - ny * bow, basex, basey );
    leaf.close();
    d.drawPath({path: leaf, color: p.ink.copy(0.16)});
    d.drawPath({path: leaf, color: p.ink.copy(0.84), style: Stroke({width: unit * 0.024, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.72), start: new Off(basex, basey), end: new Off(tipx, tipy), strokeWidth: unit * 0.020, cap: 'round'});
    const veins = Math.min(Math.max(Math.trunc((len / (unit * 0.20))), 3), 9);
    for (let i = Math.trunc(0); i < Math.trunc(veins); i++) {
      const t = (i + 0.8) / (veins + 1);
      const mx = basex + dx * t;
      const my = basey + dy * t;
      const reach = bow * (1 - t) * 0.86;
      d.drawLine({color: p.ink.copy(0.44), start: new Off(mx, my), end: new Off(mx + nx * reach + dx * 0.10, my + ny * reach + dy * 0.10), strokeWidth: unit * 0.013, cap: 'round'});
      d.drawLine({color: p.ink.copy(0.44), start: new Off(mx, my), end: new Off(mx - nx * reach + dx * 0.10, my - ny * reach + dy * 0.10), strokeWidth: unit * 0.013, cap: 'round'});
    }
    d.drawLine({color: p.ink.copy(0.66), start: new Off(basex, basey), end: new Off(basex - dx * 0.16, basey - dy * 0.16), strokeWidth: unit * 0.022, cap: 'round'});
  }
  function artLedger(d, p, r) {
    const w = d.w;
    const h = d.h;
    const left = w * 0.13;
    const right = w * 0.90;
    const rule = left - w * 0.045;
    d.drawLine({color: p.ink.copy(0.30), start: new Off(rule, h * 0.12), end: new Off(rule, h * 0.90), strokeWidth: h * 0.016});
    const hot = r.int(4) + 1;
    for (let i = Math.trunc(0); i < Math.trunc(6); i++) {
      const y = h * (0.19 + i * 0.126);
      const end = left + (right - left) * r.range(0.42, 1.0);
      if (i == hot) {
        d.drawRect({color: p.ink.copy(0.18), topLeft: new Off(left - w * 0.014, y - h * 0.055), size: new Sz(end - left + w * 0.028, h * 0.110)});
      }
      d.drawLine({color: p.ink.copy(((i == hot) ? (0.88) : (0.36))), start: new Off(left, y), end: new Off(end, y), strokeWidth: h * 0.036, cap: 'round'});
    }
    d.drawCircle({color: p.ink, radius: h * 0.034, center: new Off(rule, h * (0.19 + hot * 0.126))});
  }
  function artLensRays(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const lx = w * 0.42;
    const cy = h * 0.52;
    const lh = h * 0.36;
    const bulge = w * 0.045;
    const fx = lx + w * 0.36;
    const rays = Math.min(Math.max(Math.trunc(((h / unit) * 5)), 4), 7);
    for (let i = Math.trunc(0); i < Math.trunc(rays); i++) {
      const t = (i + 0.5) / rays;
      const y = cy - lh + lh * 2 * t;
      d.drawLine({color: p.ink.copy(0.44), start: new Off(w * 0.03, y), end: new Off(lx, y), strokeWidth: unit * 0.015, cap: 'round'});
      d.drawLine({color: p.ink.copy(0.62), start: new Off(lx, y), end: new Off(fx, cy), strokeWidth: unit * 0.015, cap: 'round'});
      d.drawLine({color: p.ink.copy(0.18), start: new Off(fx, cy), end: new Off(fx + (fx - lx) * 0.55, cy + (cy - y) * 0.55), strokeWidth: unit * 0.013, cap: 'round'});
    }
    const lens = new P();
    lens.moveTo(lx, cy - lh);
    lens.cubicTo(lx + bulge, cy - lh * 0.4, lx + bulge, cy + lh * 0.4, lx, cy + lh);
    lens.cubicTo(lx - bulge, cy + lh * 0.4, lx - bulge, cy - lh * 0.4, lx, cy - lh);
    lens.close();
    d.drawPath({path: lens, color: p.ink.copy(0.20)});
    d.drawPath({path: lens, color: p.ink.copy(0.85), style: Stroke({width: unit * 0.020})});
    d.drawCircle({color: p.ink, radius: unit * 0.045, center: new Off(fx, cy)});
    d.drawLine({color: p.ink.copy(0.22), start: new Off(w * 0.02, cy), end: new Off(w * 0.98, cy), strokeWidth: unit * 0.010});
  }
  function artLetterform(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const capTop = h * 0.16;
    const baseline = h * 0.82;
    const xh = capTop + (baseline - capTop) * 0.38;
    d.drawLine({color: p.ink.copy(0.20), start: new Off(0, baseline), end: new Off(w, baseline), strokeWidth: unit * 0.012});
    d.drawLine({color: p.ink.copy(0.13), start: new Off(0, xh), end: new Off(w, xh), strokeWidth: unit * 0.010});
    d.drawLine({color: p.ink.copy(0.13), start: new Off(0, capTop), end: new Off(w, capTop), strokeWidth: unit * 0.010});
    const cx = w * 0.50;
    const spread = unit * 0.30;
    const stem = unit * 0.075;
    const glyph = new P();
    glyph.moveTo(cx - spread, baseline);
    glyph.lineTo(cx - stem * 0.45, capTop);
    glyph.lineTo(cx + stem * 0.45, capTop);
    glyph.lineTo(cx + spread, baseline);
    glyph.lineTo(cx + spread - stem * 1.25, baseline);
    glyph.lineTo(cx + spread * 0.58, baseline - (baseline - capTop) * 0.30);
    glyph.lineTo(cx - spread * 0.58, baseline - (baseline - capTop) * 0.30);
    glyph.lineTo(cx - spread + stem * 1.25, baseline);
    glyph.close();
    d.drawPath({path: glyph, color: p.ink.copy(0.86)});
    const bar = new P();
    bar.moveTo(cx - spread * 0.40, baseline - (baseline - capTop) * 0.46);
    bar.lineTo(cx + spread * 0.40, baseline - (baseline - capTop) * 0.46);
    bar.lineTo(cx + spread * 0.40, baseline - (baseline - capTop) * 0.46 + stem * 0.9);
    bar.lineTo(cx - spread * 0.40, baseline - (baseline - capTop) * 0.46 + stem * 0.9);
    bar.close();
    d.drawPath({path: bar, color: p.ink.copy(0.86)});
    const ghosts = Math.min(Math.max(Math.trunc(((w / h) * 1.3)), 1), 4);
    for (let k = Math.trunc(0); k < Math.trunc(ghosts); k++) {
      const gx = ((k % 2 == 0) ? (cx - spread * (2.4 + k * 1.5)) : (cx + spread * (2.4 + (k - 1) * 1.5)));
      if (gx > -spread && gx < w + spread) {
        const g = new P();
        g.moveTo(gx - spread * 0.72, baseline);
        g.lineTo(gx, capTop + (baseline - capTop) * 0.10);
        g.lineTo(gx + spread * 0.72, baseline);
        d.drawPath({path: g, color: p.ink.copy(0.16), style: Stroke({width: unit * 0.026, cap: 'round'})});
      }
    }
  }
  function artManuscript(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const m = unit * 0.13;
    d.drawRect({color: p.ink.copy(0.07), topLeft: new Off(w * 0.06, h * 0.08), size: new Sz(w * 0.88, h * 0.84)});
    d.drawRect({color: p.ink.copy(0.60), topLeft: new Off(w * 0.06, h * 0.08), size: new Sz(w * 0.88, h * 0.84), style: Stroke({width: unit * 0.018})});
    d.drawRect({color: p.ink.copy(0.22), topLeft: new Off(w * 0.06 + m, h * 0.08 + m), size: new Sz(w * 0.88 - m * 2, h * 0.84 - m * 2), style: Stroke({width: unit * 0.010})});
    const ix = w * 0.06 + m + unit * 0.02;
    const iy = h * 0.08 + m + unit * 0.02;
    const iw = unit * 0.30;
    d.drawRect({color: p.ink.copy(0.80), topLeft: new Off(ix, iy), size: new Sz(iw, iw)});
    d.drawRect({color: p.paper.copy(0.72), topLeft: new Off(ix + iw * 0.22, iy + iw * 0.20), size: new Sz(iw * 0.16, iw * 0.60)});
    d.drawRect({color: p.paper.copy(0.72), topLeft: new Off(ix + iw * 0.60, iy + iw * 0.20), size: new Sz(iw * 0.16, iw * 0.60)});
    d.drawRect({color: p.paper.copy(0.72), topLeft: new Off(ix + iw * 0.22, iy + iw * 0.42), size: new Sz(iw * 0.54, iw * 0.15)});
    const rule = unit * 0.125;
    const lines = Math.min(Math.max(Math.trunc(((h * 0.84 - m * 2) / rule)), 3), 8);
    for (let i = Math.trunc(0); i < Math.trunc(lines); i++) {
      const ly = iy + rule * (i + 0.7);
      if (ly < h * 0.92 - m) {
        const startx = ((ly < iy + iw + unit * 0.02) ? (ix + iw + unit * 0.09) : (ix));
        const frac = ((i == lines - 1) ? (0.52) : (0.92 + r.range(-0.10, 0.06)));
        d.drawLine({color: p.ink.copy(0.40), start: new Off(startx, ly), end: new Off(startx + (w * 0.88 - m * 2 - (startx - ix)) * frac, ly), strokeWidth: unit * 0.026, cap: 'round'});
      }
    }
  }
  function artMatrix(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const rows = 3;
    const step = unit * 0.24;
    const cols = Math.min(Math.max(Math.trunc(((w * 0.74) / step)), 3), 10);
    const gw = (cols - 1) * step;
    const gh = (rows - 1) * step;
    const ox = w * 0.5 - gw * 0.5;
    const oy = h * 0.5 - gh * 0.5;
    const pad = unit * 0.15;
    const arm = unit * 0.12;
    const lb = new P();
    lb.moveTo(ox - pad + arm, oy - pad);
    lb.lineTo(ox - pad, oy - pad);
    lb.lineTo(ox - pad, oy + gh + pad);
    lb.lineTo(ox - pad + arm, oy + gh + pad);
    d.drawPath({path: lb, color: p.ink.copy(0.85), style: Stroke({width: unit * 0.026, cap: 'round'})});
    const rb = new P();
    rb.moveTo(ox + gw + pad - arm, oy - pad);
    rb.lineTo(ox + gw + pad, oy - pad);
    rb.lineTo(ox + gw + pad, oy + gh + pad);
    rb.lineTo(ox + gw + pad - arm, oy + gh + pad);
    d.drawPath({path: rb, color: p.ink.copy(0.85), style: Stroke({width: unit * 0.026, cap: 'round'})});
    const diag = r.int(2) == 0;
    for (let c = Math.trunc(0); c < Math.trunc(cols); c++) {
      for (let rw = Math.trunc(0); rw < Math.trunc(rows); rw++) {
        const on = ((diag) ? (c % rows == rw) : (r.int(2) == 0));
        const cxx = ox + c * step;
        const cyy = oy + rw * step;
        if (on) {
          d.drawCircle({color: p.ink.copy(0.88), radius: unit * 0.056, center: new Off(cxx, cyy)});
        } else {
          d.drawCircle({color: p.ink.copy(0.34), radius: unit * 0.044, center: new Off(cxx, cyy), style: Stroke({width: unit * 0.014})});
        }
      }
    }
  }
  function artMolecule(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cx = w * 0.52;
    const cy = h * 0.54;
    const rad = h * 0.33;
    const spin = r.range(0, 1.2);
    for (let i = Math.trunc(0); i < Math.trunc(5); i++) {
      const a = spin + i * (Math.PI * 2 / 5);
      const nx = cx + Math.cos(a) * rad * (w / h) * 0.42;
      const ny = cy + Math.sin(a) * rad;
      d.drawLine({color: p.ink.copy(0.48), start: new Off(cx, cy), end: new Off(nx, ny), strokeWidth: h * 0.020, cap: 'round'});
      d.drawCircle({color: p.ink.copy(0.85), radius: h * 0.072, center: new Off(nx, ny)});
      d.drawCircle({color: p.paper.copy(0.60), radius: h * 0.026, center: new Off(nx, ny)});
    }
    d.drawCircle({color: p.ink, radius: h * 0.105, center: new Off(cx, cy)});
    d.drawCircle({color: p.paper.copy(0.72), radius: h * 0.038, center: new Off(cx, cy)});
  }
  function artMonument(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const ground = h * 0.90;
    const domeR = unit * 0.30;
    const domeY = ground - unit * 0.34;
    const steps = 3;
    for (let i = Math.trunc(0); i < Math.trunc(steps); i++) {
      const sw = domeR * (1.85 - i * 0.28);
      const sy = ground - i * unit * 0.075;
      d.drawRect({color: p.ink.copy(0.22 + i * 0.10), topLeft: new Off(cx - sw, sy - unit * 0.075), size: new Sz(sw * 2, unit * 0.075)});
      d.drawRect({color: p.ink.copy(0.70), topLeft: new Off(cx - sw, sy - unit * 0.075), size: new Sz(sw * 2, unit * 0.075), style: Stroke({width: unit * 0.014})});
    }
    d.drawArc({color: p.ink.copy(0.22), startAngle: 180, sweepAngle: 180, useCenter: true, topLeft: new Off(cx - domeR, domeY - domeR), size: new Sz(domeR * 2, domeR * 2)});
    d.drawArc({color: p.ink.copy(0.85), startAngle: 180, sweepAngle: 180, useCenter: false, topLeft: new Off(cx - domeR, domeY - domeR), size: new Sz(domeR * 2, domeR * 2), style: Stroke({width: unit * 0.022, cap: 'round'})});
    d.drawRect({color: p.ink.copy(0.80), topLeft: new Off(cx - domeR * 0.40, domeY - domeR - unit * 0.14), size: new Sz(domeR * 0.80, unit * 0.14)});
    const spireBase = domeY - domeR - unit * 0.14;
    const tiers = 4;
    for (let i = Math.trunc(0); i < Math.trunc(tiers); i++) {
      const tw = domeR * (0.34 - i * 0.055);
      d.drawLine({color: p.ink.copy(0.78), start: new Off(cx - tw, spireBase - i * unit * 0.055), end: new Off(cx + tw, spireBase - i * unit * 0.055), strokeWidth: unit * 0.026, cap: 'round'});
    }
    d.drawLine({color: p.ink.copy(0.85), start: new Off(cx, spireBase - tiers * unit * 0.055), end: new Off(cx, spireBase - tiers * unit * 0.055 - unit * 0.12), strokeWidth: unit * 0.020, cap: 'round'});
    d.drawCircle({color: p.ink, radius: unit * 0.038, center: new Off(cx, spireBase - tiers * unit * 0.055 - unit * 0.15)});
    const flags = Math.min(Math.max(Math.trunc(((w / h) * 0.9)), 0), 2);
    for (let i = Math.trunc(0); i < Math.trunc(flags); i++) {
      const s = ((i == 0) ? (-1) : (1));
      const ex = cx + s * (domeR * 2.6);
      if (ex > unit * 0.10 && ex < w - unit * 0.10) {
        d.drawLine({color: p.ink.copy(0.20), start: new Off(cx + s * domeR * 0.20, spireBase - unit * 0.02), end: new Off(ex, domeY - domeR * 0.30), strokeWidth: unit * 0.010});
        for (let j = Math.trunc(0); j < Math.trunc(4); j++) {
          const t = (j + 1) / 5;
          const fx = cx + s * domeR * 0.20 + (ex - cx - s * domeR * 0.20) * t;
          const fy = spireBase - unit * 0.02 + (domeY - domeR * 0.30 - spireBase + unit * 0.02) * t;
          d.drawRect({color: p.ink.copy(0.26), topLeft: new Off(fx - unit * 0.020, fy), size: new Sz(unit * 0.040, unit * 0.055)});
        }
      }
    }
    d.drawLine({color: p.ink.copy(0.30), start: new Off(0, ground), end: new Off(w, ground), strokeWidth: unit * 0.012});
  }
  function artPages(d, p, r) {
    const w = d.w;
    const h = d.h;
    const pw = h * 0.46;
    const ph = h * 0.60;
    const cx = w * r.range(0.44, 0.58);
    const cy = h * 0.54;
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const inset = (2 - i) * h * 0.075;
      const x = cx - pw * 0.5 - inset;
      const y = cy - ph * 0.5 - inset * 0.6;
      d.drawRect({color: ((i == 2) ? (p.paper.copy(0.92)) : (p.ink.copy(0.16 + i * 0.08))), topLeft: new Off(x, y), size: new Sz(pw, ph)});
      d.drawRect({color: p.ink.copy(0.55), topLeft: new Off(x, y), size: new Sz(pw, ph), style: Stroke({width: h * 0.018})});
    }
    const fx = cx - pw * 0.5 + pw;
    const fy = cy - ph * 0.5;
    const fold = new P();
    fold.moveTo(fx - pw * 0.30, fy);
    fold.lineTo(fx, fy + ph * 0.30);
    fold.lineTo(fx - pw * 0.30, fy + ph * 0.30);
    fold.close();
    d.drawPath({path: fold, color: p.ink.copy(0.46)});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const ly = fy + ph * (0.50 + i * 0.15);
      d.drawLine({color: p.ink.copy(0.50), start: new Off(fx - pw * 0.78, ly), end: new Off(fx - pw * (0.22 + i * 0.14), ly), strokeWidth: h * 0.017, cap: 'round'});
    }
  }
  function artParabola(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const ox = w * 0.20;
    const oy = h * 0.78;
    const gw = w * 0.70;
    const gh = h * 0.60;
    const grid = Math.min(Math.max(Math.trunc((gw / (unit * 0.26))), 3), 16);
    for (let i = Math.trunc(0); i < Math.trunc(grid + 1); i++) {
      const gx = ox + gw * i / grid;
      d.drawLine({color: p.ink.copy(0.10), start: new Off(gx, oy - gh), end: new Off(gx, oy), strokeWidth: unit * 0.008});
    }
    for (let i = Math.trunc(0); i < Math.trunc(4); i++) {
      const gy = oy - gh * (i + 1) / 4;
      d.drawLine({color: p.ink.copy(0.10), start: new Off(ox, gy), end: new Off(ox + gw, gy), strokeWidth: unit * 0.008});
    }
    d.drawLine({color: p.ink.copy(0.60), start: new Off(ox, oy), end: new Off(ox + gw + unit * 0.08, oy), strokeWidth: unit * 0.017, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.60), start: new Off(ox, oy), end: new Off(ox, oy - gh - unit * 0.08), strokeWidth: unit * 0.017, cap: 'round'});
    const vx = ox + gw * r.range(0.24, 0.40);
    const steps = Math.min(Math.max(Math.trunc((gw / (unit * 0.10))), 16), 90);
    const curve = new P();
    for (let i = Math.trunc(0); i < Math.trunc(steps + 1); i++) {
      const x = ox + gw * i / steps;
      const t = (x - vx) / (gw * 0.52);
      const y = oy - gh * 0.08 - gh * 0.84 * t * t;
      if (y < oy - gh - unit * 0.02) {
        curve.moveTo(x, oy - gh);
      } else {
        if (i == 0) {
          curve.moveTo(x, y);
        } else {
          curve.lineTo(x, y);
        }
      }
    }
    d.drawPath({path: curve, color: p.ink.copy(0.82), style: Stroke({width: unit * 0.022, cap: 'round'})});
    d.drawCircle({color: p.ink, radius: unit * 0.050, center: new Off(vx, oy - gh * 0.08)});
    const tx = ox + gw * 0.72;
    const tt = (tx - vx) / (gw * 0.52);
    const ty = oy - gh * 0.08 - gh * 0.84 * tt * tt;
    const slope = -gh * 0.84 * 2 * tt / (gw * 0.52);
    d.drawLine({color: p.ink.copy(0.40), start: new Off(tx - gw * 0.22, ty - slope * gw * 0.22), end: new Off(tx + gw * 0.18, ty + slope * gw * 0.18), strokeWidth: unit * 0.014, cap: 'round'});
    d.drawCircle({color: p.ink.copy(0.85), radius: unit * 0.042, center: new Off(tx, ty)});
  }
  function artPeaks(d, p, r) {
    const w = d.w;
    const h = d.h;
    const baseY = h * 0.94;
    const back = new P();
    back.moveTo(0, baseY);
    for (let i = Math.trunc(0); i < Math.trunc(5); i++) {
      const f = i / 4;
      back.lineTo(w * (f + 0.06), baseY - h * (0.30 + r.range(0, 0.26)));
      back.lineTo(w * (f + 0.14), baseY - h * 0.10);
    }
    back.lineTo(w, baseY);
    back.close();
    d.drawPath({path: back, color: p.ink.copy(0.28)});
    const px = w * r.range(0.36, 0.56);
    const peakY = baseY - h * 0.66;
    const front = new P();
    front.moveTo(w * 0.04, baseY);
    front.lineTo(px, peakY);
    front.lineTo(w * 0.82, baseY);
    front.close();
    d.drawPath({path: front, color: p.ink.copy(0.58)});
    const drop = h * 0.24;
    const t = drop / (h * 0.66);
    const lx = px - (px - w * 0.04) * t;
    const rx = px + (w * 0.82 - px) * t;
    const span = rx - lx;
    const cap = new P();
    cap.moveTo(px, peakY);
    cap.lineTo(rx, peakY + drop);
    cap.lineTo(rx - span * 0.20, peakY + drop * 0.62);
    cap.lineTo(rx - span * 0.42, peakY + drop * 1.00);
    cap.lineTo(rx - span * 0.68, peakY + drop * 0.58);
    cap.lineTo(lx, peakY + drop * 0.90);
    cap.close();
    d.drawPath({path: cap, color: p.paper.copy(0.85)});
    d.drawCircle({color: p.ink.copy(0.55), radius: h * 0.075, center: new Off(w * 0.86, h * 0.28)});
  }
  function artPendulum(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const px = w * 0.52;
    const py = h * 0.07;
    const len = h * 0.66;
    const swing = 0.46 + r.range(0, 0.22);
    d.drawLine({color: p.ink.copy(0.50), start: new Off(w * 0.5 - len * 0.85, py), end: new Off(w * 0.5 + len * 0.85, py), strokeWidth: unit * 0.026, cap: 'round'});
    d.drawArc({color: p.ink.copy(0.18), startAngle: 90 - swing * 57.2958, sweepAngle: swing * 114.5916, useCenter: false, topLeft: new Off(px - len, py - len), size: new Sz(len * 2, len * 2), style: Stroke({width: unit * 0.016, cap: 'round'})});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const a = -swing + swing * i;
      const bx = px + Math.sin(a) * len;
      const by = py + Math.cos(a) * len;
      const lead = i == 2;
      const al = ((lead) ? (0.88) : (0.20 + i * 0.09));
      d.drawLine({color: p.ink.copy(al * 0.62), start: new Off(px, py), end: new Off(bx, by), strokeWidth: unit * 0.018, cap: 'round'});
      d.drawCircle({color: p.ink.copy(al), radius: unit * 0.088, center: new Off(bx, by)});
      if (lead) {
        d.drawCircle({color: p.paper.copy(0.50), radius: unit * 0.030, center: new Off(bx - unit * 0.026, by - unit * 0.028)});
      }
    }
    d.drawCircle({color: p.ink, radius: unit * 0.032, center: new Off(px, py)});
  }
  function artPetri(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const cy = h * 0.52;
    const rad = unit * 0.43;
    d.drawCircle({color: p.ink.copy(0.09), radius: rad, center: new Off(cx, cy)});
    d.drawCircle({color: p.ink.copy(0.80), radius: rad, center: new Off(cx, cy), style: Stroke({width: unit * 0.024})});
    d.drawCircle({color: p.ink.copy(0.30), radius: rad * 0.90, center: new Off(cx, cy), style: Stroke({width: unit * 0.012})});
    const colonies = Math.min(Math.max(Math.trunc(((w / h) * 5)), 6), 22);
    for (let i = Math.trunc(0); i < Math.trunc(colonies); i++) {
      const a = r.range(0, 6.2832);
      const dist = rad * 0.82 * Math.sqrt(r.range(0.02, 1));
      const ccx = cx + Math.cos(a) * dist;
      const ccy = cy + Math.sin(a) * dist;
      const cr = unit * r.range(0.022, 0.070);
      d.drawCircle({color: p.ink.copy(0.26 + r.range(0, 0.40)), radius: cr, center: new Off(ccx, ccy)});
      if (cr > unit * 0.050) {
        d.drawCircle({color: p.ink.copy(0.30), radius: cr * 1.9, center: new Off(ccx, ccy), style: Stroke({width: unit * 0.010})});
      }
    }
    d.drawArc({color: p.paper.copy(0.30), startAngle: 200, sweepAngle: 70, useCenter: false, topLeft: new Off(cx - rad * 0.76, cy - rad * 0.76), size: new Sz(rad * 1.52, rad * 1.52), style: Stroke({width: unit * 0.034, cap: 'round'})});
  }
  function artPie(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const rad = unit * 0.40;
    const cx = w * 0.42;
    const cy = h * 0.52;
    const start = r.range(-120, -40);
    const a0 = 96 + r.range(0, 40);
    const a1 = 78 + r.range(0, 40);
    const a2 = 360 - a0 - a1;
    d.drawArc({color: p.ink.copy(0.16), startAngle: start + a0, sweepAngle: a1, useCenter: true, topLeft: new Off(cx - rad, cy - rad), size: new Sz(rad * 2, rad * 2)});
    d.drawArc({color: p.ink.copy(0.40), startAngle: start + a0 + a1, sweepAngle: a2, useCenter: true, topLeft: new Off(cx - rad, cy - rad), size: new Sz(rad * 2, rad * 2)});
    d.drawArc({color: p.ink.copy(0.78), startAngle: start, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rad, cy - rad), size: new Sz(rad * 2, rad * 2), style: Stroke({width: unit * 0.020})});
    const mid = (start + a0 * 0.5) * Math.PI / 180;
    const push = rad * 0.16;
    const px0 = cx + Math.cos(mid) * push;
    const py0 = cy + Math.sin(mid) * push;
    d.drawArc({color: p.ink.copy(0.86), startAngle: start, sweepAngle: a0, useCenter: true, topLeft: new Off(px0 - rad, py0 - rad), size: new Sz(rad * 2, rad * 2)});
    d.drawArc({color: p.paper.copy(0.40), startAngle: start, sweepAngle: a0, useCenter: true, topLeft: new Off(px0 - rad * 0.30, py0 - rad * 0.30), size: new Sz(rad * 0.60, rad * 0.60)});
    const keys = Math.min(Math.max(Math.trunc(((w - cx - rad) / (unit * 0.22))), 0), 3);
    for (let i = Math.trunc(0); i < Math.trunc(keys); i++) {
      const ky = cy - unit * 0.22 + i * unit * 0.22;
      const kx = cx + rad + unit * 0.22;
      d.drawCircle({color: p.ink.copy(0.85 - i * 0.26), radius: unit * 0.045, center: new Off(kx, ky)});
      d.drawLine({color: p.ink.copy(0.28), start: new Off(kx + unit * 0.10, ky), end: new Off(kx + unit * 0.10 + (w * 0.96 - kx - unit * 0.10) * (0.55 + r.range(0, 0.40)), ky), strokeWidth: unit * 0.026, cap: 'round'});
    }
  }
  function artPrism(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cx = w * 0.42;
    const cy = h * 0.52;
    const s = h * 0.34;
    const tri = new P();
    tri.moveTo(cx, cy - s);
    tri.lineTo(cx + s * 0.92, cy + s * 0.70);
    tri.lineTo(cx - s * 0.92, cy + s * 0.70);
    tri.close();
    d.drawPath({path: tri, color: p.ink.copy(0.20)});
    d.drawPath({path: tri, color: p.ink.copy(0.80), style: Stroke({width: h * 0.026})});
    d.drawLine({color: p.ink.copy(0.68), start: new Off(0, cy - h * 0.20), end: new Off(cx - s * 0.30, cy - h * 0.02), strokeWidth: h * 0.024, cap: 'round'});
    for (let i = Math.trunc(0); i < Math.trunc(4); i++) {
      const spread = (i - 1.5) * h * 0.17 + r.range(-0.02, 0.02) * h;
      d.drawLine({color: p.ink.copy(0.62 - i * 0.10), start: new Off(cx + s * 0.30, cy + h * 0.02), end: new Off(w, cy + spread), strokeWidth: h * 0.022, cap: 'round'});
    }
  }
  function artProjectile(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const gy = h * 0.86;
    const x0 = w * 0.10;
    const x1 = w * 0.90;
    const peak = h * 0.16;
    const steps = Math.min(Math.max(Math.trunc((w / (unit * 0.16))), 12), 64);
    d.drawLine({color: p.ink.copy(0.55), start: new Off(w * 0.02, gy), end: new Off(w * 0.98, gy), strokeWidth: unit * 0.018, cap: 'round'});
    const hatches = Math.min(Math.max(Math.trunc((w / (unit * 0.34))), 4), 22);
    for (let i = Math.trunc(0); i < Math.trunc(hatches); i++) {
      const hx = w * 0.03 + (w * 0.94) * (i + 0.5) / hatches;
      d.drawLine({color: p.ink.copy(0.16), start: new Off(hx, gy), end: new Off(hx - unit * 0.07, gy + unit * 0.09), strokeWidth: unit * 0.011, cap: 'round'});
    }
    const arc = new P();
    for (let i = Math.trunc(0); i < Math.trunc(steps + 1); i++) {
      const t = i / steps;
      const x = x0 + (x1 - x0) * t;
      const y = gy - (gy - peak) * 4 * t * (1 - t);
      if (i == 0) {
        arc.moveTo(x, y);
      } else {
        arc.lineTo(x, y);
      }
    }
    d.drawPath({path: arc, color: p.ink.copy(0.78), style: Stroke({width: unit * 0.020, cap: 'round'})});
    const marks = 5;
    for (let i = Math.trunc(0); i < Math.trunc(marks); i++) {
      const t = (i + 1) / (marks + 1);
      const x = x0 + (x1 - x0) * t;
      const y = gy - (gy - peak) * 4 * t * (1 - t);
      d.drawCircle({color: p.ink.copy(0.34), radius: unit * 0.030, center: new Off(x, y)});
    }
    const vx = x0 + (x1 - x0) * 0.22;
    const vy = gy - (gy - peak) * 4 * 0.22 * 0.78;
    d.drawLine({color: p.ink.copy(0.60), start: new Off(x0, gy), end: new Off(vx, vy), strokeWidth: unit * 0.016, cap: 'round'});
    d.drawCircle({color: p.ink, radius: unit * 0.062, center: new Off(x0, gy)});
    const apex = (x0 + x1) * 0.5;
    d.drawCircle({color: p.ink, radius: unit * 0.075, center: new Off(apex, peak)});
    d.drawCircle({color: p.paper.copy(0.55), radius: unit * 0.026, center: new Off(apex - unit * 0.022, peak - unit * 0.024)});
  }
  function artPulse(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const base = h * 0.56;
    const amp = h * 0.34;
    const beats = Math.min(Math.max(Math.trunc((w / (unit * 1.05))), 1), 6);
    const span = w / beats;
    d.drawLine({color: p.ink.copy(0.14), start: new Off(0, base), end: new Off(w, base), strokeWidth: unit * 0.010});
    const grid = Math.min(Math.max(Math.trunc((w / (unit * 0.22))), 4), 40);
    for (let i = Math.trunc(0); i < Math.trunc(grid); i++) {
      const gx = w * (i + 0.5) / grid;
      d.drawLine({color: p.ink.copy(0.07), start: new Off(gx, h * 0.10), end: new Off(gx, h * 0.92), strokeWidth: unit * 0.007});
    }
    const trace = new P();
    trace.moveTo(0, base);
    for (let b = Math.trunc(0); b < Math.trunc(beats); b++) {
      const o = b * span;
      trace.lineTo(o + span * 0.14, base);
      trace.lineTo(o + span * 0.22, base - amp * 0.22);
      trace.lineTo(o + span * 0.30, base);
      trace.lineTo(o + span * 0.38, base + amp * 0.18);
      trace.lineTo(o + span * 0.44, base - amp);
      trace.lineTo(o + span * 0.50, base + amp * 0.46);
      trace.lineTo(o + span * 0.58, base);
      trace.lineTo(o + span * 0.74, base - amp * 0.30);
      trace.lineTo(o + span * 0.86, base);
    }
    trace.lineTo(w, base);
    d.drawPath({path: trace, color: p.ink.copy(0.86), style: Stroke({width: unit * 0.026, cap: 'round'})});
    for (let b = Math.trunc(0); b < Math.trunc(beats); b++) {
      d.drawCircle({color: p.ink, radius: unit * 0.044, center: new Off(b * span + span * 0.44, base - amp)});
    }
  }
  function artQuill(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const tipx = w * 0.30;
    const tipy = h * 0.74;
    const topx = tipx + unit * 0.62;
    const topy = h * 0.10;
    const dx = topx - tipx;
    const dy = topy - tipy;
    const len = Math.sqrt(dx * dx + dy * dy);
    const nx = -dy / len;
    const ny = dx / len;
    const bow = unit * 0.20;
    const feather = new P();
    feather.moveTo(tipx, tipy);
    feather.cubicTo( tipx + dx * 0.34 + nx * bow, tipy + dy * 0.34 + ny * bow, tipx + dx * 0.78 + nx * bow * 1.10, tipy + dy * 0.78 + ny * bow * 1.10, topx, topy );
    feather.cubicTo( tipx + dx * 0.70 - nx * bow * 0.34, tipy + dy * 0.70 - ny * bow * 0.34, tipx + dx * 0.30 - nx * bow * 0.22, tipy + dy * 0.30 - ny * bow * 0.22, tipx, tipy );
    feather.close();
    d.drawPath({path: feather, color: p.ink.copy(0.18)});
    d.drawPath({path: feather, color: p.ink.copy(0.86), style: Stroke({width: unit * 0.022, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.72), start: new Off(tipx, tipy), end: new Off(topx, topy), strokeWidth: unit * 0.016, cap: 'round'});
    const barbs = Math.min(Math.max(Math.trunc((len / (unit * 0.13))), 4), 12);
    for (let i = Math.trunc(0); i < Math.trunc(barbs); i++) {
      const t = (i + 1.2) / (barbs + 2);
      const mx = tipx + dx * t;
      const my = tipy + dy * t;
      d.drawLine({color: p.ink.copy(0.40), start: new Off(mx, my), end: new Off(mx + nx * bow * (1 - t * 0.5) * 0.82 + dx * 0.07, my + ny * bow * (1 - t * 0.5) * 0.82 + dy * 0.07), strokeWidth: unit * 0.011, cap: 'round'});
    }
    d.drawCircle({color: p.ink, radius: unit * 0.034, center: new Off(tipx, tipy)});
    const ink = new P();
    ink.moveTo(tipx - unit * 0.04, tipy + unit * 0.06);
    ink.cubicTo( w * 0.10, h * 0.90, w * 0.44, h * 0.99, w * 0.94, h * 0.84 );
    d.drawPath({path: ink, color: p.ink.copy(0.56), style: Stroke({width: unit * 0.026, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.20), start: new Off(w * 0.06, h * 0.94), end: new Off(w * 0.94, h * 0.94), strokeWidth: unit * 0.010});
  }
  function artQuotes(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const qx = w * 0.14;
    const qy = h * 0.34;
    const qr = unit * 0.15;
    for (let k = Math.trunc(0); k < Math.trunc(2); k++) {
      const ox = qx + k * qr * 2.15;
      const hook = new P();
      hook.moveTo(ox + qr * 0.95, qy - qr * 0.95);
      hook.cubicTo( ox - qr * 0.55, qy - qr * 0.95, ox - qr * 0.95, qy + qr * 0.30, ox + qr * 0.10, qy + qr * 0.95 );
      hook.cubicTo( ox + qr * 0.95, qy + qr * 0.55, ox + qr * 0.55, qy - qr * 0.20, ox + qr * 0.95, qy - qr * 0.95 );
      hook.close();
      d.drawPath({path: hook, color: p.ink.copy(0.80 - k * 0.16)});
    }
    const lines = Math.min(Math.max(Math.trunc(((h * 0.44) / (unit * 0.16))), 2), 5);
    for (let i = Math.trunc(0); i < Math.trunc(lines); i++) {
      const ly = h * 0.58 + i * unit * 0.165;
      if (ly < h * 0.95) {
        const frac = ((i == lines - 1) ? (0.46) : (0.78 + r.range(0, 0.16)));
        d.drawLine({color: p.ink.copy(0.34 + (((i == 0) ? (0.22) : (0)))), start: new Off(w * 0.12, ly), end: new Off(w * 0.12 + (w * 0.80) * frac, ly), strokeWidth: unit * 0.034, cap: 'round'});
      }
    }
    const cq = w * 0.90;
    const cy = h * 0.80;
    d.drawCircle({color: p.ink.copy(0.26), radius: unit * 0.055, center: new Off(cq, cy)});
    d.drawCircle({color: p.ink.copy(0.26), radius: unit * 0.038, center: new Off(cq - unit * 0.13, cy + unit * 0.03)});
  }
  function artReceipt(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const half = unit * 0.34;
    const top = h * 0.08;
    const bot = h * 0.86;
    const teeth = 7;
    const tz = unit * 0.07;
    d.drawRect({color: p.ink.copy(0.10), topLeft: new Off(cx - half, top), size: new Sz(half * 2, bot - top)});
    const edge = new P();
    edge.moveTo(cx - half, bot);
    for (let i = Math.trunc(0); i < Math.trunc(teeth); i++) {
      edge.lineTo(cx - half + half * 2 * (i + 0.5) / teeth, bot + (((i % 2 == 0) ? (tz) : (-tz * 0.2))));
    }
    edge.lineTo(cx + half, bot);
    edge.lineTo(cx + half, top);
    edge.lineTo(cx - half, top);
    edge.close();
    d.drawPath({path: edge, color: p.ink.copy(0.80), style: Stroke({width: unit * 0.020, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.70), start: new Off(cx - half * 0.54, top + unit * 0.13), end: new Off(cx + half * 0.54, top + unit * 0.13), strokeWidth: unit * 0.036, cap: 'round'});
    const rule = unit * 0.115;
    const rows = Math.min(Math.max(Math.trunc(((bot - top - unit * 0.42) / rule)), 2), 6);
    for (let i = Math.trunc(0); i < Math.trunc(rows); i++) {
      const ly = top + unit * 0.30 + rule * (i + 0.6);
      if (ly < bot - unit * 0.14) {
        d.drawLine({color: p.ink.copy(0.32), start: new Off(cx - half * 0.76, ly), end: new Off(cx - half * 0.76 + half * 0.86 * (0.5 + r.range(0, 0.5)), ly), strokeWidth: unit * 0.024, cap: 'round'});
        d.drawLine({color: p.ink.copy(0.46), start: new Off(cx + half * 0.30, ly), end: new Off(cx + half * 0.76, ly), strokeWidth: unit * 0.024, cap: 'round'});
      }
    }
    const sumy = top + unit * 0.30 + rule * (rows + 0.35);
    if (sumy < bot - unit * 0.06) {
      d.drawLine({color: p.ink.copy(0.40), start: new Off(cx - half * 0.76, sumy - rule * 0.45), end: new Off(cx + half * 0.76, sumy - rule * 0.45), strokeWidth: unit * 0.011});
      d.drawLine({color: p.ink.copy(0.85), start: new Off(cx + half * 0.16, sumy), end: new Off(cx + half * 0.76, sumy), strokeWidth: unit * 0.030, cap: 'round'});
    }
  }
  function artRings(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const cy = h * 0.52;
    const outer = unit * 0.42;
    const band = unit * 0.075;
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const rad = outer - i * (band * 1.55);
      d.drawCircle({color: p.ink.copy(0.14), radius: rad, center: new Off(cx, cy), style: Stroke({width: band})});
      const sweep = 200 + r.range(0, 150);
      d.drawArc({color: p.ink.copy(0.86 - i * 0.20), startAngle: -90, sweepAngle: sweep, useCenter: false, topLeft: new Off(cx - rad, cy - rad), size: new Sz(rad * 2, rad * 2), style: Stroke({width: band, cap: 'round'})});
      const ea = (-90 + sweep) * Math.PI / 180;
      d.drawCircle({color: p.paper.copy(0.40), radius: band * 0.22, center: new Off(cx + Math.cos(ea) * rad, cy + Math.sin(ea) * rad)});
    }
    const pips = Math.min(Math.max(Math.trunc(((w / h) * 2.2)), 0), 6);
    for (let i = Math.trunc(0); i < Math.trunc(pips); i++) {
      const s = ((i % 2 == 0) ? (-1) : (1));
      const k = i / 2;
      d.drawCircle({color: p.ink.copy(0.22), radius: unit * (0.030 - k * 0.006), center: new Off(cx + s * (outer + unit * (0.20 + k * 0.18)), cy + (((k % 2 == 0) ? (-unit * 0.14) : (unit * 0.16))))});
    }
  }
  function artRipple(d, p, r) {
    const w = d.w;
    const h = d.h;
    const cx = w * r.range(0.74, 0.90);
    const cy = h * 0.52;
    for (let i = Math.trunc(0); i < Math.trunc(7); i++) {
      const rad = h * (0.10 + i * 0.20);
      d.drawCircle({color: p.ink.copy(0.52 - i * 0.062), radius: rad, center: new Off(cx, cy), style: Stroke({width: h * 0.024})});
    }
    d.drawCircle({color: p.ink, radius: h * 0.062, center: new Off(cx, cy)});
    d.drawCircle({color: p.ink.copy(0.30), radius: h * 0.030, center: new Off(w * 0.12, h * 0.30)});
    d.drawCircle({color: p.ink.copy(0.22), radius: h * 0.020, center: new Off(w * 0.20, h * 0.72)});
  }
  function artRunner(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.52;
    const hipY = h * 0.56;
    const s = unit * 0.20;
    const stroke = unit * 0.034;
    d.drawCircle({color: p.ink.copy(0.88), radius: s * 0.40, center: new Off(cx + s * 0.55, hipY - s * 1.70)});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx + s * 0.35, hipY - s * 1.25), end: new Off(cx - s * 0.10, hipY), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx + s * 0.22, hipY - s * 1.00), end: new Off(cx + s * 1.05, hipY - s * 1.30), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx + s * 1.05, hipY - s * 1.30), end: new Off(cx + s * 1.30, hipY - s * 0.66), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx + s * 0.22, hipY - s * 1.00), end: new Off(cx - s * 0.80, hipY - s * 1.10), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx - s * 0.80, hipY - s * 1.10), end: new Off(cx - s * 1.00, hipY - s * 0.46), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx - s * 0.10, hipY), end: new Off(cx + s * 0.60, hipY + s * 0.66), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx + s * 0.60, hipY + s * 0.66), end: new Off(cx + s * 0.44, hipY + s * 1.60), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx - s * 0.10, hipY), end: new Off(cx - s * 1.10, hipY + s * 0.30), strokeWidth: stroke, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.88), start: new Off(cx - s * 1.10, hipY + s * 0.30), end: new Off(cx - s * 1.34, hipY + s * 1.30), strokeWidth: stroke, cap: 'round'});
    const trails = Math.min(Math.max(Math.trunc(((w / h) * 2)), 2), 6);
    for (let i = Math.trunc(0); i < Math.trunc(trails); i++) {
      const ty = hipY - s * (1.30 - i * 0.62);
      d.drawLine({color: p.ink.copy(0.22), start: new Off(cx - s * (2.0 + i * 0.5), ty), end: new Off(cx - s * (3.4 + i * 0.9), ty), strokeWidth: unit * 0.020, cap: 'round'});
    }
    d.drawLine({color: p.ink.copy(0.30), start: new Off(0, hipY + s * 1.72), end: new Off(w, hipY + s * 1.72), strokeWidth: unit * 0.012});
  }
  function artShelf(d, p, r) {
    const w = d.w;
    const h = d.h;
    const baseY = h * 0.88;
    const n = 11;
    let x = w * 0.07;
    for (let i = Math.trunc(0); i < Math.trunc(n); i++) {
      const bw = w * r.range(0.028, 0.055);
      const bh = h * r.range(0.30, 0.58);
      const lean = ((i == n - 4) ? (14) : (0));
      d.rotate(lean, new Off(x + bw, baseY), () => {
        d.drawRect({color: ((i % 4 == 1) ? (p.paper.copy(0.85)) : (p.ink.copy(0.34 + r.range(0, 0.42)))), topLeft: new Off(x, baseY - bh), size: new Sz(bw, bh)});
        d.drawLine({color: p.ink.copy(0.48), start: new Off(x + bw * 0.5, baseY - bh * 0.78), end: new Off(x + bw * 0.5, baseY - bh * 0.30), strokeWidth: bw * 0.22, cap: 'round'});
      });
      x = x + bw + w * 0.016;
    }
    d.drawLine({color: p.ink.copy(0.65), start: new Off(w * 0.04, baseY), end: new Off(w * 0.78, baseY), strokeWidth: h * 0.024, cap: 'round'});
  }
  function artSigma(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const left = w * 0.14;
    const right = left + unit * 0.52;
    const top = h * 0.16;
    const bot = h * 0.84;
    const mid = (top + bot) * 0.5;
    const sig = new P();
    sig.moveTo(right, top);
    sig.lineTo(left, top);
    sig.lineTo(left + unit * 0.30, mid);
    sig.lineTo(left, bot);
    sig.lineTo(right, bot);
    d.drawPath({path: sig, color: p.ink.copy(0.88), style: Stroke({width: unit * 0.060, cap: 'round'})});
    d.drawCircle({color: p.ink.copy(0.50), radius: unit * 0.038, center: new Off(right + unit * 0.09, top - unit * 0.02)});
    d.drawCircle({color: p.ink.copy(0.50), radius: unit * 0.038, center: new Off(right + unit * 0.09, bot + unit * 0.02)});
    const bars = Math.min(Math.max(Math.trunc(((w - right) / (unit * 0.20))), 2), 10);
    for (let i = Math.trunc(0); i < Math.trunc(bars); i++) {
      const bxx = right + unit * 0.24 + i * unit * 0.185;
      if (bxx < w * 0.96) {
        const fh = (bot - top) * (0.24 + r.range(0, 0.68));
        d.drawLine({color: p.ink.copy(0.26 + r.range(0, 0.34)), start: new Off(bxx, bot), end: new Off(bxx, bot - fh), strokeWidth: unit * 0.075, cap: 'round'});
      }
    }
    d.drawLine({color: p.ink.copy(0.30), start: new Off(right + unit * 0.14, bot + unit * 0.09), end: new Off(w * 0.96, bot + unit * 0.09), strokeWidth: unit * 0.012, cap: 'round'});
  }
  function artSineField(d, p, r) {
    const w = d.w;
    const h = d.h;
    const phase = r.range(0, 6.2);
    for (let k = Math.trunc(0); k < Math.trunc(5); k++) {
      const line = new P();
      const amp = h * (0.10 + k * 0.030);
      const mid = h * (0.22 + k * 0.15);
      for (let i = Math.trunc(0); i < Math.trunc(33); i++) {
        const f = i / 32;
        const y = mid + Math.sin(f * Math.PI * 2.6 + phase + k * 0.55) * amp;
        if (i == 0) {
          line.moveTo(w * f, y);
        } else {
          line.lineTo(w * f, y);
        }
      }
      d.drawPath({path: line, color: p.ink.copy(0.22 + k * 0.13), style: Stroke({width: h * 0.022, cap: 'round'})});
    }
  }
  function artSteps(d, p, r) {
    const w = d.w;
    const h = d.h;
    const bw = w * 0.15;
    const rise = h * 0.15;
    const skew = h * 0.16;
    const baseY = h * 0.92;
    const x0 = w * r.range(0.10, 0.20);
    for (let i = Math.trunc(0); i < Math.trunc(4); i++) {
      const x = x0 + i * bw * 0.82;
      const y = baseY - i * rise;
      const top = new P();
      top.moveTo(x, y);
      top.lineTo(x + bw * 0.62, y - skew);
      top.lineTo(x + bw, y);
      top.lineTo(x + bw * 0.38, y + skew);
      top.close();
      d.drawPath({path: top, color: p.ink.copy(0.66 - i * 0.06)});
      const face = new P();
      face.moveTo(x, y);
      face.lineTo(x + bw * 0.38, y + skew);
      face.lineTo(x + bw * 0.38, y + skew + rise);
      face.lineTo(x, y + rise);
      face.close();
      d.drawPath({path: face, color: p.ink.copy(0.36)});
      const side = new P();
      side.moveTo(x + bw * 0.38, y + skew);
      side.lineTo(x + bw, y);
      side.lineTo(x + bw, y + rise);
      side.lineTo(x + bw * 0.38, y + skew + rise);
      side.close();
      d.drawPath({path: side, color: p.ink.copy(0.18)});
    }
  }
  function artSupplyDemand(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const ox = w * 0.16;
    const oy = h * 0.84;
    const gw = w * 0.74;
    const gh = h * 0.68;
    const grid = Math.min(Math.max(Math.trunc((gw / (unit * 0.26))), 3), 14);
    for (let i = Math.trunc(0); i < Math.trunc(grid + 1); i++) {
      d.drawLine({color: p.ink.copy(0.08), start: new Off(ox + gw * i / grid, oy - gh), end: new Off(ox + gw * i / grid, oy), strokeWidth: unit * 0.008});
    }
    d.drawLine({color: p.ink.copy(0.60), start: new Off(ox, oy), end: new Off(ox + gw + unit * 0.07, oy), strokeWidth: unit * 0.017, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.60), start: new Off(ox, oy), end: new Off(ox, oy - gh - unit * 0.07), strokeWidth: unit * 0.017, cap: 'round'});
    const ex = ox + gw * (0.46 + r.range(0, 0.12));
    const ey = oy - gh * (0.46 + r.range(0, 0.12));
    d.drawLine({color: p.ink.copy(0.80), start: new Off(ox + gw * 0.06, oy - gh * 0.12), end: new Off(ox + gw * 0.94, oy - gh * 0.92), strokeWidth: unit * 0.024, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.52), start: new Off(ox + gw * 0.06, oy - gh * 0.92), end: new Off(ox + gw * 0.94, oy - gh * 0.12), strokeWidth: unit * 0.024, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.26), start: new Off(ox, ey), end: new Off(ex, ey), strokeWidth: unit * 0.012});
    d.drawLine({color: p.ink.copy(0.26), start: new Off(ex, oy), end: new Off(ex, ey), strokeWidth: unit * 0.012});
    d.drawCircle({color: p.field, radius: unit * 0.082, center: new Off(ex, ey)});
    d.drawCircle({color: p.ink, radius: unit * 0.060, center: new Off(ex, ey)});
    d.drawCircle({color: p.paper.copy(0.70), radius: unit * 0.022, center: new Off(ex, ey)});
  }
  function artTarget(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.52;
    const cy = h * 0.50;
    const outer = unit * 0.42;
    for (let i = Math.trunc(0); i < Math.trunc(4); i++) {
      const rad = outer * (1 - i * 0.235);
      if (i % 2 == 0) {
        d.drawCircle({color: p.ink.copy(0.13), radius: rad, center: new Off(cx, cy)});
      }
      d.drawCircle({color: p.ink.copy(0.34 + i * 0.14), radius: rad, center: new Off(cx, cy), style: Stroke({width: unit * 0.018})});
    }
    d.drawCircle({color: p.ink, radius: outer * 0.10, center: new Off(cx, cy)});
    const a = r.range(2.5, 3.6);
    const ax = cx + Math.cos(a) * outer * 2.1;
    const ay = cy + Math.sin(a) * outer * 2.1;
    d.drawLine({color: p.ink.copy(0.85), start: new Off(ax, ay), end: new Off(cx - Math.cos(a) * outer * 0.04, cy - Math.sin(a) * outer * 0.04), strokeWidth: unit * 0.024, cap: 'round'});
    for (let i = Math.trunc(0); i < Math.trunc(2); i++) {
      const s = ((i == 0) ? (1) : (-1));
      d.drawLine({color: p.ink.copy(0.70), start: new Off(ax, ay), end: new Off(ax - Math.cos(a) * outer * 0.40 - s * Math.sin(a) * outer * 0.22, ay - Math.sin(a) * outer * 0.40 + s * Math.cos(a) * outer * 0.22), strokeWidth: unit * 0.020, cap: 'round'});
    }
    d.drawArc({color: p.ink.copy(0.22), startAngle: (a * 180 / Math.PI) - 40, sweepAngle: 80, useCenter: false, topLeft: new Off(cx - outer * 1.70, cy - outer * 1.70), size: new Sz(outer * 3.40, outer * 3.40), style: Stroke({width: unit * 0.011})});
  }
  function artTerminal(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const x0 = w * 0.08;
    const y0 = h * 0.12;
    const ww = w * 0.84;
    const wh = h * 0.76;
    const chrome = unit * 0.16;
    d.drawRect({color: p.ink.copy(0.10), topLeft: new Off(x0, y0), size: new Sz(ww, wh)});
    d.drawRect({color: p.ink.copy(0.26), topLeft: new Off(x0, y0), size: new Sz(ww, chrome)});
    d.drawRect({color: p.ink.copy(0.72), topLeft: new Off(x0, y0), size: new Sz(ww, wh), style: Stroke({width: unit * 0.020})});
    d.drawLine({color: p.ink.copy(0.50), start: new Off(x0, y0 + chrome), end: new Off(x0 + ww, y0 + chrome), strokeWidth: unit * 0.014});
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      d.drawCircle({color: p.ink.copy(0.60 - i * 0.12), radius: chrome * 0.22, center: new Off(x0 + chrome * (0.42 + i * 0.60), y0 + chrome * 0.50)});
    }
    const rule = unit * 0.135;
    const lines = Math.min(Math.max(Math.trunc(((wh - chrome) / rule)), 2), 7);
    for (let i = Math.trunc(0); i < Math.trunc(lines); i++) {
      const ly = y0 + chrome + rule * (i + 0.72);
      if (ly < y0 + wh - rule * 0.30) {
        const ind = ((i == 0) ? (0) : ((i % 3) * unit * 0.11));
        if (i == 0) {
          d.drawLine({color: p.ink.copy(0.85), start: new Off(x0 + unit * 0.09, ly), end: new Off(x0 + unit * 0.17, ly), strokeWidth: unit * 0.026, cap: 'round'});
        }
        const sx = x0 + unit * (((i == 0) ? (0.24) : (0.11))) + ind;
        const frac = 0.34 + r.range(0, 0.52);
        d.drawLine({color: p.ink.copy(((i == 0) ? (0.62) : (0.34))), start: new Off(sx, ly), end: new Off(sx + (x0 + ww - unit * 0.10 - sx) * frac, ly), strokeWidth: unit * 0.028, cap: 'round'});
      }
    }
    const cy = y0 + chrome + rule * (lines - 0.28);
    if (cy < y0 + wh - unit * 0.05) {
      d.drawRect({color: p.ink.copy(0.80), topLeft: new Off(x0 + unit * 0.11, cy - rule * 0.34), size: new Sz(unit * 0.045, rule * 0.62)});
    }
  }
  function artTrophy(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * 0.50;
    const top = h * 0.20;
    const cupH = unit * 0.36;
    const half = unit * 0.24;
    const cup = new P();
    cup.moveTo(cx - half, top);
    cup.cubicTo(cx - half, top + cupH * 0.70, cx - half * 0.52, top + cupH, cx, top + cupH);
    cup.cubicTo(cx + half * 0.52, top + cupH, cx + half, top + cupH * 0.70, cx + half, top);
    cup.close();
    d.drawPath({path: cup, color: p.ink.copy(0.20)});
    d.drawPath({path: cup, color: p.ink.copy(0.86), style: Stroke({width: unit * 0.024, cap: 'round'})});
    d.drawLine({color: p.ink.copy(0.86), start: new Off(cx - half - unit * 0.04, top), end: new Off(cx + half + unit * 0.04, top), strokeWidth: unit * 0.026, cap: 'round'});
    for (let i = Math.trunc(0); i < Math.trunc(2); i++) {
      const s = ((i == 0) ? (-1) : (1));
      d.drawArc({color: p.ink.copy(0.66), startAngle: ((i == 0) ? (90) : (-90)), sweepAngle: ((i == 0) ? (180) : (180)), useCenter: false, topLeft: new Off(cx + s * half - (((i == 0) ? (half * 0.52) : (0))), top + unit * 0.02), size: new Sz(half * 0.52, cupH * 0.52), style: Stroke({width: unit * 0.020, cap: 'round'})});
    }
    d.drawLine({color: p.ink.copy(0.86), start: new Off(cx, top + cupH), end: new Off(cx, top + cupH + unit * 0.14), strokeWidth: unit * 0.036, cap: 'round'});
    d.drawRect({color: p.ink.copy(0.70), topLeft: new Off(cx - half * 0.72, top + cupH + unit * 0.14), size: new Sz(half * 1.44, unit * 0.070)});
    d.drawRect({color: p.ink.copy(0.34), topLeft: new Off(cx - half * 1.00, top + cupH + unit * 0.21), size: new Sz(half * 2.00, unit * 0.060)});
    const stars = Math.min(Math.max(Math.trunc(((w / h) * 1.8)), 2), 8);
    for (let i = Math.trunc(0); i < Math.trunc(stars); i++) {
      const s = ((i % 2 == 0) ? (-1) : (1));
      const k = i / 2;
      const sx = cx + s * (half * 1.7 + k * unit * 0.30);
      const sy = h * (0.22 + (i % 3) * 0.22);
      if (sx > unit * 0.05 && sx < w - unit * 0.05) {
        const sr = unit * (0.055 - k * 0.008);
        for (let j = Math.trunc(0); j < Math.trunc(2); j++) {
          const a = j * (Math.PI / 2);
          d.drawLine({color: p.ink.copy(0.30), start: new Off(sx - Math.cos(a) * sr, sy - Math.sin(a) * sr), end: new Off(sx + Math.cos(a) * sr, sy + Math.sin(a) * sr), strokeWidth: unit * 0.014, cap: 'round'});
        }
      }
    }
    d.drawArc({color: p.paper.copy(0.36), startAngle: 120, sweepAngle: 70, useCenter: false, topLeft: new Off(cx - half * 0.60, top + cupH * 0.10), size: new Sz(half * 0.70, cupH * 0.80), style: Stroke({width: unit * 0.026, cap: 'round'})});
  }
  function artVenn(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const rad = unit * 0.34;
    const cx = w * 0.50;
    const cy = h * 0.52;
    const off = rad * 0.62;
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const a = -Math.PI / 2 + i * (Math.PI * 2 / 3) + r.range(0, 0.3);
      d.drawCircle({color: p.ink.copy(0.17), radius: rad, center: new Off(cx + Math.cos(a) * off, cy + Math.sin(a) * off * 0.92)});
    }
    for (let i = Math.trunc(0); i < Math.trunc(3); i++) {
      const a = -Math.PI / 2 + i * (Math.PI * 2 / 3);
      d.drawCircle({color: p.ink.copy(0.72), radius: rad, center: new Off(cx + Math.cos(a) * off, cy + Math.sin(a) * off * 0.92), style: Stroke({width: unit * 0.020})});
    }
    d.drawCircle({color: p.ink.copy(0.55), radius: unit * 0.048, center: new Off(cx, cy)});
    const dots = Math.min(Math.max(Math.trunc(((w / h) * 2)), 2), 8);
    for (let i = Math.trunc(0); i < Math.trunc(dots); i++) {
      d.drawCircle({color: p.ink.copy(0.18 + r.range(0, 0.16)), radius: unit * r.range(0.016, 0.030), center: new Off(w * r.range(0.03, 0.97), h * r.range(0.06, 0.94))});
    }
  }
  function artWaveform(d, p, r) {
    const w = d.w;
    const h = d.h;
    const n = 20;
    const mid = h * 0.54;
    const phase = r.range(0, 6.2);
    for (let i = Math.trunc(0); i < Math.trunc(n); i++) {
      const f = (i + 0.5) / n;
      const env = Math.abs(Math.sin(f * Math.PI * 2.3 + phase));
      const amp = h * (0.07 + 0.32 * env) + h * r.range(0, 0.05);
      const x = w * f;
      d.drawLine({color: p.ink.copy(0.30 + 0.50 * env), start: new Off(x, mid - amp), end: new Off(x, mid + amp), strokeWidth: w / (n * 3.4), cap: 'round'});
    }
    d.drawLine({color: p.paper.copy(0.45), start: new Off(0, mid), end: new Off(w, mid), strokeWidth: h * 0.010});
  }

  var FAMILY = {
    PHYSICS: [artAtom, artPrism, artPendulum, artFieldLines, artLensRays, artProjectile],
    CHEMISTRY: [artMolecule, artFlask, artBenzene, artBurette, artLattice, artBeaker],
    MATH: [artParabola, artGeometry, artSigma, artMatrix, artVenn, artSteps],
    BIOLOGY: [artHelix, artBloom, artCell, artLeaf, artPulse, artPetri],
    SCIENCE: [artFlask, artAtom, artLeaf, artFieldLines, artPetri],
    LANGUAGE: [artPages, artShelf, artQuill, artQuotes, artManuscript, artLetterform],
    COMPUTING: [artCircuit, artTerminal, artBinary, artGraph, artBraces, artChip],
    COMMERCE: [artBars, artLedger, artCoins, artSupplyDemand, artPie, artReceipt],
    SOCIAL: [artPeaks, artContours, artGlobe, artMonument, artCompass],
    HEALTH: [artPulse, artRunner, artApple, artRings, artDrop],
    EXAM: [artChecklist, artClock, artTarget, artCalendar, artTrophy],
    GENERAL: [artArcs, artHorizon, artDotMatrix, artWaveform, artRipple, artHatch, artConstellation, artSineField, artChevrons, artEclipse, artComet, artSteps]
  };

  // ---------------------------------------------------------- cover arts ----
  function coverColonnade(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const baseY = h * r.range(0.80, 0.90);
    const capY = h * r.range(0.26, 0.36);
    const pitch = unit * r.range(0.26, 0.34);
    const cols = Math.min(Math.max(Math.trunc((w / pitch)), 3), 16);
    const x0 = (w - (cols - 1) * pitch) * 0.5;
    const shaft = pitch * 0.30;
    const markCol = r.int(cols);
    d.drawLine({color: p.ink.copy(0.34), start: new Off(x0 - pitch * 0.6, capY), end: new Off(x0 + (cols - 1) * pitch + pitch * 0.6, capY), strokeWidth: unit * 0.016});
    d.drawLine({color: p.ink.copy(0.18), start: new Off(x0 - pitch * 0.45, capY - unit * 0.06), end: new Off(x0 + (cols - 1) * pitch + pitch * 0.45, capY - unit * 0.06), strokeWidth: unit * 0.010});
    const apex = capY - unit * r.range(0.16, 0.26);
    const mid = x0 + (cols - 1) * pitch * 0.5;
    d.drawLine({color: p.ink.copy(0.26), start: new Off(x0 - pitch * 0.45, capY - unit * 0.06), end: new Off(mid, apex), strokeWidth: unit * 0.012, cap: 'round'});
    d.drawLine({color: p.ink.copy(0.26), start: new Off(mid, apex), end: new Off(x0 + (cols - 1) * pitch + pitch * 0.45, capY - unit * 0.06), strokeWidth: unit * 0.012, cap: 'round'});
    for (let i = Math.trunc(0); i < Math.trunc(cols); i++) {
      const cx = x0 + i * pitch;
      const lit = i == markCol;
      const alpha = ((lit) ? (0.62) : (0.14 + 0.10 * Math.sin(i * 1.7) * Math.sin(i * 1.7)));
      const ink = ((lit) ? (p.accent.copy(alpha)) : (p.ink.copy(alpha)));
      d.drawLine({color: ink, start: new Off(cx - shaft * 0.5, capY), end: new Off(cx - shaft * 0.5, baseY), strokeWidth: unit * 0.012});
      d.drawLine({color: ink, start: new Off(cx + shaft * 0.5, capY), end: new Off(cx + shaft * 0.5, baseY), strokeWidth: unit * 0.012});
      d.drawLine({color: ink.copy(alpha * 0.5), start: new Off(cx, capY + unit * 0.04), end: new Off(cx, baseY - unit * 0.04), strokeWidth: unit * 0.008});
    }
    for (let i = Math.trunc(0); i < Math.trunc(2); i++) {
      const over = pitch * (0.6 + i * 0.35);
      d.drawLine({color: p.ink.copy(0.30 - i * 0.10), start: new Off(x0 - over, baseY + i * unit * 0.055), end: new Off(x0 + (cols - 1) * pitch + over, baseY + i * unit * 0.055), strokeWidth: unit * 0.014});
    }
  }
  function coverGuard(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const left = r.next() < 0.5;
    const ox = ((left) ? (w * r.range(0.04, 0.20)) : (w * r.range(0.80, 0.96)));
    const oy = h * r.range(0.92, 1.10);
    const gap = unit * r.range(0.20, 0.28);
    const rings = Math.min(Math.max(Math.trunc(((((w > h) ? (w) : (h))) / gap)), 4), 12);
    for (let i = Math.trunc(0); i < Math.trunc(rings); i++) {
      const rad = gap * (i + 1);
      d.drawArc({color: p.ink.copy(0.26 - 0.015 * i), startAngle: 180, sweepAngle: 180, useCenter: false, topLeft: new Off(ox - rad, oy - rad), size: new Sz(rad * 2, rad * 2), style: Stroke({width: unit * 0.014, cap: 'round'})});
    }
    const ry = h * r.range(0.24, 0.40);
    d.drawLine({color: p.ink.copy(0.22), start: new Off(0, ry), end: new Off(w, ry), strokeWidth: unit * 0.010});
    const tick = unit * 0.14;
    const ticks = Math.min(Math.max(Math.trunc((w / tick)), 6), 40);
    for (let i = Math.trunc(0); i < Math.trunc(ticks); i++) {
      const tx = tick * (i + 0.5);
      const tall = i % 4 == 0;
      d.drawLine({color: p.ink.copy(((tall) ? (0.34) : (0.16))), start: new Off(tx, ry), end: new Off(tx, ry + ((tall) ? (unit * 0.12) : (unit * 0.06))), strokeWidth: unit * 0.009});
    }
    d.drawCircle({color: p.accent.copy(0.85), radius: unit * 0.026, center: new Off(ox, ry)});
  }
  function coverKeystone(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const step = unit * r.range(0.30, 0.40);
    const cols = Math.min(Math.max(Math.trunc(((w + step) / step)), 3), 14);
    const rows = Math.min(Math.max(Math.trunc(((h + step) / step)), 2), 8);
    const x0 = (w - (cols - 1) * step) * 0.5;
    const y0 = (h - (rows - 1) * step) * 0.5;
    const half = step * 0.48;
    const markCol = r.int(cols);
    const markRow = r.int(rows);
    for (let row = Math.trunc(0); row < Math.trunc(rows); row++) {
      for (let col = Math.trunc(0); col < Math.trunc(cols); col++) {
        const cx = x0 + col * step + (row % 2) * step * 0.5;
        const cy = y0 + row * step;
        const path = new P();
        path.moveTo(cx, cy - half);
        path.lineTo(cx + half, cy);
        path.lineTo(cx, cy + half);
        path.lineTo(cx - half, cy);
        path.close();
        const fall = 0.10 + 0.24 * (cx / w);
        if (col == markCol && row == markRow) {
          d.drawPath({path: path, color: p.accent.copy(0.16)});
          d.drawPath({path: path, color: p.accent.copy(0.70), style: Stroke({width: unit * 0.016})});
        } else {
          d.drawPath({path: path, color: p.ink.copy(fall), style: Stroke({width: unit * 0.010})});
        }
      }
    }
  }
  function coverOrbits(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * r.range(0.24, 0.44);
    const cy = h * r.range(0.44, 0.62);
    const rings = 3 + r.int(2);
    const base = unit * r.range(0.32, 0.44);
    for (let i = Math.trunc(0); i < Math.trunc(rings); i++) {
      const grow = 1 + i * 0.34;
      const rx = base * grow;
      const ry = base * grow * r.range(0.26, 0.44);
      const spin = r.range(-40, 40);
      d.rotate(spin, new Off(cx, cy), () => {
        d.drawArc({color: p.ink.copy(0.30 - 0.05 * i), startAngle: 0, sweepAngle: 360, useCenter: false, topLeft: new Off(cx - rx, cy - ry), size: new Sz(rx * 2, ry * 2), style: Stroke({width: unit * 0.012})});
        const at = r.range(0, 6.2831855);
        d.drawCircle({color: ((i == 0) ? (p.accent.copy(0.95)) : (p.ink.copy(0.70))), radius: unit * (0.030 - 0.005 * i), center: new Off(cx + Math.cos(at) * rx, cy + Math.sin(at) * ry)});
      });
    }
    d.drawCircle({color: p.accent.copy(0.22), radius: unit * 0.14, center: new Off(cx, cy)});
    d.drawCircle({color: p.accent.copy(0.90), radius: unit * 0.070, center: new Off(cx, cy)});
    const rays = 4 + r.int(4);
    for (let i = Math.trunc(0); i < Math.trunc(rays); i++) {
      const ang = r.range(-0.9, 0.9);
      const len = unit * r.range(0.55, 1.15);
      d.drawLine({color: p.ink.copy(r.range(0.07, 0.17)), start: new Off(cx + Math.cos(ang) * unit * 0.20, cy + Math.sin(ang) * unit * 0.20), end: new Off(cx + Math.cos(ang) * len, cy + Math.sin(ang) * len), strokeWidth: unit * 0.010, cap: 'round'});
    }
  }
  function coverRidgeline(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const sx = w * r.range(0.14, 0.86);
    const sy = h * r.range(0.16, 0.34);
    d.drawRect({brush: Brush.radialGradient({colors: [p.accent.copy(0.22), p.accent.copy(0)], center: new Off(sx, sy), radius: unit * 0.34})});
    d.drawCircle({color: p.accent.copy(0.72), radius: unit * 0.075, center: new Off(sx, sy)});
    const stars = 8 + r.int(9);
    for (let i = Math.trunc(0); i < Math.trunc(stars); i++) {
      d.drawCircle({color: p.ink.copy(r.range(0.10, 0.34)), radius: unit * r.range(0.004, 0.012), center: new Off(w * r.next(), h * r.range(0.04, 0.55))});
    }
    const ranges = 4 + r.int(2);
    for (let k = Math.trunc(0); k < Math.trunc(ranges); k++) {
      const depth = k / (ranges - 0.999);
      const baseY = h * (0.62 + 0.34 * depth);
      const amp = unit * (0.50 - 0.085 * k) * r.range(0.80, 1.10);
      const freq = r.range(0.8, 1.5) + k * 0.55;
      const phase = r.range(0, 6.2831855);
      const steps = Math.min(Math.max(Math.trunc((w / (unit * 0.045))), 24), 220);
      const body = new P();
      const crest = new P();
      body.moveTo(0, h * 1.2);
      for (let i = Math.trunc(0); i < Math.trunc(steps + 1); i++) {
        const t = i / steps;
        const ridge = (Math.sin(t * freq * 6.2831855 + phase) * 0.62 + Math.sin(t * freq * 2.3 * 6.2831855 + phase * 1.7) * 0.20 + Math.sin(t * freq * 0.5 * 6.2831855 + phase * 0.6) * 0.18);
        const py = baseY - amp * ridge;
        body.lineTo(w * t, py);
        if (i == 0) {
          crest.moveTo(0, py);
        } else {
          crest.lineTo(w * t, py);
        }
      }
      body.lineTo(w, h * 1.2);
      body.close();
      d.drawPath({path: body, color: p.deep.copy(0.52 + 0.13 * k)});
      d.drawPath({path: crest, color: p.ink.copy(0.34 - 0.055 * k), style: Stroke({width: unit * 0.013})});
    }
  }
  function coverSeal(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const cx = w * r.range(0.56, 0.80);
    const cy = h * r.range(0.40, 0.58);
    const rad = unit * r.range(0.30, 0.40);
    const lobes = 12 + r.int(7);
    const path = new P();
    const steps = lobes * 12;
    for (let i = Math.trunc(0); i < Math.trunc(steps + 1); i++) {
      const ang = i / steps * 6.2831855;
      const wob = rad * (1 + 0.075 * Math.cos(ang * lobes));
      const px = cx + Math.cos(ang) * wob;
      const py = cy + Math.sin(ang) * wob;
      if (i == 0) {
        path.moveTo(px, py);
      } else {
        path.lineTo(px, py);
      }
    }
    path.close();
    d.drawPath({path: path, color: p.ink.copy(0.30), style: Stroke({width: unit * 0.013})});
    d.drawCircle({color: p.ink.copy(0.22), radius: rad * 0.80, center: new Off(cx, cy), style: Stroke({width: unit * 0.010})});
    d.drawCircle({color: p.accent.copy(0.55), radius: rad * 0.52, center: new Off(cx, cy), style: Stroke({width: unit * 0.016})});
    const spokes = 24;
    for (let i = Math.trunc(0); i < Math.trunc(spokes); i++) {
      const ang = i / spokes * 6.2831855;
      const long = i % 3 == 0;
      const inner = rad * ((long) ? (0.58) : (0.66));
      const outer = rad * 0.74;
      d.drawLine({color: p.ink.copy(((long) ? (0.34) : (0.16))), start: new Off(cx + Math.cos(ang) * inner, cy + Math.sin(ang) * inner), end: new Off(cx + Math.cos(ang) * outer, cy + Math.sin(ang) * outer), strokeWidth: unit * 0.010, cap: 'round'});
    }
    const arm = rad * 0.30;
    d.drawLine({color: p.accent.copy(0.95), start: new Off(cx - arm, cy + arm * 0.10), end: new Off(cx - arm * 0.22, cy + arm * 0.72), strokeWidth: unit * 0.026, cap: 'round'});
    d.drawLine({color: p.accent.copy(0.95), start: new Off(cx - arm * 0.22, cy + arm * 0.72), end: new Off(cx + arm * 0.96, cy - arm * 0.74), strokeWidth: unit * 0.026, cap: 'round'});
    const sparks = 5 + r.int(5);
    for (let i = Math.trunc(0); i < Math.trunc(sparks); i++) {
      d.drawCircle({color: p.ink.copy(r.range(0.10, 0.30)), radius: unit * r.range(0.008, 0.022), center: new Off(w * r.next(), h * r.next())});
    }
  }
  function coverSignal(d, p, r) {
    const w = d.w;
    const h = d.h;
    const unit = ((h < w) ? (h) : (w));
    const lane = unit * r.range(0.16, 0.22);
    const lanes = Math.min(Math.max(Math.trunc((h / lane)), 3), 12);
    const y0 = (h - (lanes - 1) * lane) * 0.5;
    for (let i = Math.trunc(0); i < Math.trunc(lanes); i++) {
      const ly = y0 + i * lane;
      const runs = 1 + r.int(3);
      let x = w * r.range(-0.05, 0.18);
      for (let k = Math.trunc(0); k < Math.trunc(runs); k++) {
        const len = w * r.range(0.16, 0.42);
        const alpha = r.range(0.10, 0.26);
        d.drawLine({color: p.ink.copy(alpha), start: new Off(x, ly), end: new Off(x + len, ly), strokeWidth: unit * 0.011});
        if (r.next() < 0.55) {
          const drop = lane * (((r.next() < 0.5) ? (1) : (-1)));
          d.drawLine({color: p.ink.copy(alpha), start: new Off(x + len, ly), end: new Off(x + len + lane * 0.7, ly + drop), strokeWidth: unit * 0.011, cap: 'round'});
        }
        d.drawCircle({color: p.ink.copy(alpha + 0.16), radius: unit * 0.020, center: new Off(x + len, ly)});
        x = x + len + w * r.range(0.06, 0.16);
      }
    }
    const wy = h * r.range(0.38, 0.66);
    const amp = unit * r.range(0.10, 0.18);
    const cycles = r.range(1.6, 3.4);
    const steps = Math.min(Math.max(Math.trunc((w / (unit * 0.05))), 24), 220);
    const path = new P();
    for (let i = Math.trunc(0); i < Math.trunc(steps + 1); i++) {
      const t = i / steps;
      const px = w * t;
      const py = wy + Math.sin(t * cycles * 6.2831855) * amp * (0.35 + 0.65 * Math.sin(t * 3.1415927));
      if (i == 0) {
        path.moveTo(px, py);
      } else {
        path.lineTo(px, py);
      }
    }
    d.drawPath({path: path, color: p.accent.copy(0.80), style: Stroke({width: unit * 0.018, cap: 'round'})});
  }
  function drawCoverFinish(d, p, r) {
    const w = d.w;
    const h = d.h;
    const span = ((w > h) ? (w) : (h));
    d.drawRect({brush: Brush.radialGradient({colors: [p.deep.copy(0), p.deep.copy(0.55)], center: new Off(w * 0.5, h * 0.42), radius: span * 0.72})});
    d.drawRect({brush: Brush.verticalGradient({colors: [p.deep.copy(0), p.deep.copy(0.42)], startY: h * 0.52, endY: h})});
    const specks = Math.min(Math.max(Math.trunc(((w * h) / 2600)), 14), 54);
    for (let i = Math.trunc(0); i < Math.trunc(specks); i++) {
      d.drawCircle({color: p.ink.copy(r.range(0.02, 0.07)), radius: r.range(0.5, 1.4), center: new Off(w * r.next(), h * r.next())});
    }
  }
  function drawCoverGround(d, p, r) {
    const w = d.w;
    const h = d.h;
    const tilt = r.range(0.55, 1.0);
    d.drawRect({brush: Brush.linearGradient({colors: [p.deep, p.mid, p.rise], start: new Off(w * (1 - tilt), h), end: new Off(w * tilt, 0)})});
    const bx = w * r.range(0.16, 0.86);
    const by = h * r.range(0.02, 0.46);
    const span = ((w > h) ? (w) : (h));
    d.drawRect({brush: Brush.radialGradient({colors: [p.glow.copy(0.50), p.glow.copy(0)], center: new Off(bx, by), radius: span * r.range(0.50, 0.85)})});
  }

  var MOTIF = {
    ADMIN: coverKeystone,
    MODERATOR: coverGuard,
    VERIFIED: coverSeal,
    TUTOR: coverOrbits,
    INSTITUTION: coverColonnade,
    BOT: coverSignal
  };

  // ------------------------------------------------------------- public ----
  var SURFACE_LIGHT = Color.hex(0xFFF5F6F8);
  var SURFACE_DARK = Color.hex(0xFF0B1C30);

  function isDarkNow() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t === 'dark') return true;
    if (t === 'light') return false;
    return !!(global.matchMedia && global.matchMedia('(prefers-color-scheme: dark)').matches);
  }

  function prepare(canvas, cssW, cssH) {
    var dpr = Math.min(global.devicePixelRatio || 1, 2.5);
    canvas.width = Math.max(1, Math.round(cssW * dpr));
    canvas.height = Math.max(1, Math.round(cssH * dpr));
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, cssW, cssH);
    return new D(ctx, cssW, cssH);
  }

  function drawBanner(canvas, opts) {
    var w = canvas.clientWidth || opts.width || 320;
    var h = canvas.clientHeight || opts.height || 120;
    if (w < 2 || h < 2) return;
    var subject = opts.subject || '';
    var dark = opts.dark === undefined ? isDarkNow() : opts.dark;
    var p = bannerPalette(subject, dark);
    var hash = stableSeed(opts.seed || subject);
    var fam = subjectFamily(subject);
    var names = FAMILY[fam];
    var i = ((hash >>> 3) & 0x7FFFFFFF) % names.length;
    var d = prepare(canvas, w, h);
    d.drawRect({ brush: Brush.verticalGradient([p.top, p.bottom]) });
    names[i](d, p, new Rng(hash));
  }

  function drawCover(canvas, opts) {
    var w = canvas.clientWidth || opts.width || 640;
    var h = canvas.clientHeight || opts.height || 220;
    if (w < 2 || h < 2) return;
    var role = (opts.role || 'MEMBER').toUpperCase();
    if (!COVER_PALETTES[role]) role = 'MEMBER';
    var p = COVER_PALETTES[role];
    var r = new Rng(stableSeed('cover|' + (opts.seed || '') + '|' + role));
    var d = prepare(canvas, w, h);
    drawCoverGround(d, p, r);
    (MOTIF[role] || coverRidgeline)(d, p, r);
    drawCoverFinish(d, p, r);
    return p;
  }

  // --------------------------------------------------------------- init ----
  // Any element carrying data-neb-art paints itself and repaints on resize and
  // on a theme flip. Nothing else on the page has to know this file exists.
  var observed = [];

  function paint(el) {
    var canvas = el.tagName === 'CANVAS' ? el : el.querySelector('canvas.neb-art-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'neb-art-canvas';
      el.insertBefore(canvas, el.firstChild);
    }
    var kind = el.getAttribute('data-neb-art');
    try {
      if (kind === 'cover') {
        var cp = drawCover(canvas, { role: el.getAttribute('data-neb-role'),
                                     seed: el.getAttribute('data-neb-seed') || '' });
        // Anything layered over the cover in CSS — a deco word, a rule, a
        // scrim — needs the palette the art actually chose, not a guess.
        if (cp) {
          el.style.setProperty('--neb-cover-ink', cp.ink.css());
          el.style.setProperty('--neb-cover-accent', cp.accent.css());
          el.style.setProperty('--neb-cover-deep', cp.deep.css());
        }
      } else {
        drawBanner(canvas, { subject: el.getAttribute('data-neb-subject') || '',
                             seed: el.getAttribute('data-neb-seed') || '' });
      }
    } catch (e) { /* a broken art must never take the page down with it */ }
  }

  var ro = global.ResizeObserver ? new ResizeObserver(function (entries) {
    for (var i = 0; i < entries.length; i++) paint(entries[i].target);
  }) : null;

  function scan(root) {
    var els = (root || document).querySelectorAll('[data-neb-art]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.__nebArt) continue;
      el.__nebArt = true;
      observed.push(el);
      paint(el);
      if (ro) ro.observe(el);
    }
  }

  function repaintAll() { for (var i = 0; i < observed.length; i++) paint(observed[i]); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { scan(); });
  } else { scan(); }
  // htmx swaps in card grids constantly; pick up whatever arrives.
  document.addEventListener('htmx:afterSwap', function (e) { scan(e.target); });
  document.addEventListener('neb:theme-change', repaintAll);
  if (global.matchMedia) {
    var mq = global.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', repaintAll);
  }

  global.NebArt = {
    banner: drawBanner, cover: drawCover, scan: scan, repaint: repaintAll,
    subjectFamily: subjectFamily, subjectHue: subjectHue,
    bannerPalette: bannerPalette, stableSeed: stableSeed, Rng: Rng,
    Color: Color, roles: Object.keys(COVER_PALETTES),
    // The art tables, so a test harness can call one drawing directly and diff
    // its call stream against the Kotlin's. This file is generated from that
    // Kotlin, and the only thing that proves the emitter is honest is running
    // both and comparing numbers.
    __arts: { FAMILY: FAMILY, MOTIF: MOTIF, COVER_PALETTES: COVER_PALETTES,
              ground: drawCoverGround, finish: drawCoverFinish,
              fallback: coverRidgeline }
  };
})(window);
