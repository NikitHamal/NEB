import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
#!/usr/bin/env python3
"""Emits backend_python/web/static/web/js/neb-art.js from the shipping Kotlin."""
import sys, re, json
sys.path.insert(0, _HERE)
import render as R
import tojs as J

OUT = os.path.join(_ROOT, "backend_python/web/static/web/js/neb-art.js")
BANNER = open(J.BANNER_KT).read()
COVER = open(J.COVER_KT).read()

def hexcolor(c):
    return "0x%02X%02X%02X%02X" % (int(c.a * 255 + .5), int(c.r * 255 + .5),
                                   int(c.g * 255 + .5), int(c.b * 255 + .5))

# ------------------------------------------------------------------ colour ---
hues_js = ",\n    ".join(
    '%s: [%s]' % (json.dumps(k), ", ".join(hexcolor(c) for c in v))
    for k, v in R.HUES.items())
famhues_js = ",\n    ".join(
    '%s: [%s]' % (k, ", ".join(hexcolor(c) for c in v)) for k, v in R.FAM_HUES.items())
famkw_js = ",\n    ".join(
    '["%s", %s]' % (f, json.dumps(kws, ensure_ascii=False)) for f, kws in R.FAM_KEYWORDS)

def pal_js(d):
    return ", ".join("%s: %s" % (k, J.jsexpr(d[k])) for k in
                     ("top", "bottom", "ink", "paper", "field"))

# ------------------------------------------------------------- cover palette -
def cover_palettes():
    body = COVER[COVER.index("fun coverPalette("):]
    body = body[:body.index("\n}")]
    out = []
    for m in re.finditer(r"CoverRole\.(\w+) -> CoverPalette\(([\s\S]*?)\n    \)", body):
        role, blk = m.group(1), re.sub(r"//[^\n]*", "", m.group(2))
        fields = dict(re.findall(r"(\w+)\s*=\s*Color\(0x([0-9A-Fa-f]{8})\)", blk))
        assert len(fields) == 6, (role, fields)
        out.append((role, fields))
    assert len(out) == 7, len(out)
    return out

def cover_dispatch():
    body = COVER[COVER.index("fun DrawScope.drawCoverMotif("):]
    body = body[:body.index("\n}")]
    pairs = re.findall(r"role == CoverRole\.(\w+)\) \{\s*(\w+)\(p, r\)", body)
    fallback = re.findall(r"\} else \{\s*(\w+)\(p, r\)", body)[0]
    return pairs, fallback

# ------------------------------------------------------------------- arts ----
SIG_B = r"(?:private )?fun DrawScope\.(\w+)\(p: BannerPalette, r: Rng\) \{"
SIG_C = r"(?:private )?fun DrawScope\.(\w+)\(p: CoverPalette, r: Rng\) \{"
banner_fns = J.transpile_js(BANNER, SIG_B)
cover_fns = J.transpile_js(COVER, SIG_C)
assert len(banner_fns) == 67, len(banner_fns)
assert len(cover_fns) == 9, sorted(cover_fns)      # ground + finish + 7 motifs

family_js = ",\n    ".join(
    "%s: [%s]" % (f, ", ".join(names)) for f, names in R.FAMILY.items())
cp, cfb = cover_dispatch()
motif_js = ",\n    ".join("%s: %s" % (role, fn) for role, fn in cp)

RUNTIME = r'''/*
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
'''

TAIL = r'''
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
    (MOTIF[role] || __FALLBACK_MOTIF__)(d, p, r);
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
              fallback: __FALLBACK_MOTIF__ }
  };
})(window);
'''

parts = [RUNTIME]
a = parts.append

a("\n  // ------------------------------------------------------- subject hues ----\n")
a("  var HUES = {\n    %s\n  };\n" % hues_js)
a("  var FAM_HUES = {\n    %s\n  };\n" % famhues_js)
a("  var FAM_KEYWORDS = [\n    %s\n  ];\n" % famkw_js)
a(r'''
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
    return dark ? { %s } : { %s };
  }
''' % (pal_js(R.PAL_DARK), pal_js(R.PAL_LIGHT)))

a("\n  // ------------------------------------------------------ cover palettes ----\n")
a("  var COVER_PALETTES = {\n")
for role, f in cover_palettes():
    a("    %s: { %s },\n" % (role, ", ".join(
        "%s: Color.hex(0x%s)" % (k, v.upper()) for k, v in f.items())))
a("  };\n")

a("\n  // --------------------------------------------------------- banner arts ----\n")
for name in sorted(banner_fns):
    a("  " + banner_fns[name].replace("\n", "\n  ") + "\n")
a("\n  var FAMILY = {\n    %s\n  };\n" % family_js)

a("\n  // ---------------------------------------------------------- cover arts ----\n")
for name in sorted(cover_fns):
    a("  " + cover_fns[name].replace("\n", "\n  ") + "\n")
a("\n  var MOTIF = {\n    %s\n  };\n" % motif_js)

a(TAIL.replace("__FALLBACK_MOTIF__", cfb))
src = "".join(parts)
open(OUT, "w").write(src)
print("wrote", OUT, len(src), "bytes,", len(banner_fns), "banner arts,", len(cover_fns), "cover fns")
