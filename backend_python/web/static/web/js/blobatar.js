/*!
 * blobatar.js - deterministic geometric blobatars from any string.
 * Vanilla-JS port of the blobatar library (github.com/Alain00/blobatar, v2.0.0),
 * vendored so the NEBians avatar page can render realtime previews client-side.
 * The same name always renders the same SVG, in every runtime, as the server.
 * Exposes window.Blobatar.blobatar(name, opts) - plus an `anim` extension
 * (SMIL) so previews match the server-rendered <img> avatars.
 */
(function (global) {
  "use strict";

  // ------------------------------------------------------------------ hash
  var SEP = 0xff;

  function feed(h, bytes) {
    for (var i = 0; i < bytes.length; i++) {
      h = Math.imul(h ^ bytes[i], 3432918353);
      h = (h << 13) | (h >>> 19);
    }
    return h;
  }

  function finalize(h) {
    h = Math.imul(h ^ (h >>> 16), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return (h ^ (h >>> 16)) >>> 0;
  }

  var utf8 = new TextEncoder();

  function normalizeSeed(seed) {
    return seed.normalize("NFC").trim().toLowerCase();
  }

  function seedState(seed, normalize) {
    var s = normalize === false ? seed : normalizeSeed(seed);
    return feed(1779033703 ^ s.length, utf8.encode(s));
  }

  function stream(state, key) {
    return finalize(feed(feed(state, Uint8Array.of(SEP)), utf8.encode(key))) / 4294967296;
  }

  function traits(seed, normalize, overrides) {
    var _state = seedState(seed, normalize);
    var _overrides = overrides || {};
    function call(key) {
      var v = _overrides[key];
      var o = Array.isArray(v) ? v[Math.floor(stream(_state, key) * v.length)] : v;
      return o === undefined ? stream(_state, key) : o > 0 ? (o < 1 ? o : 0.999999) : 0;
    }
    call.num = function (key, min, max) { return min + call(key) * (max - min); };
    call.int = function (key, min, max) { return min + Math.floor(call(key) * (max - min + 1)); };
    call.pick = function (key, options) { return options[Math.floor(call(key) * options.length)]; };
    call.bool = function (key, p) { return call(key) < (p === undefined ? 0.5 : p); };
    call.jitter = function (key, amount) { return (call(key) * 2 - 1) * amount; };
    return call;
  }

  // ----------------------------------------------------------------- color
  function toLinear(o) {
    var r = (o.h * Math.PI) / 180;
    var a = o.c * Math.cos(r);
    var b = o.c * Math.sin(r);

    var l_ = o.l + 0.3963377774 * a + 0.2158037573 * b;
    var m_ = o.l - 0.1055613458 * a - 0.0638541728 * b;
    var s_ = o.l - 0.0894841775 * a - 1.291485548 * b;

    var L = l_ * l_ * l_;
    var M = m_ * m_ * m_;
    var S = s_ * s_ * s_;

    return [
      4.0767416621 * L - 3.3077115913 * M + 0.2309699292 * S,
      -1.2684380046 * L + 2.6097574011 * M - 0.3413193965 * S,
      -0.0041960863 * L - 0.7034186147 * M + 1.707614701 * S,
    ];
  }

  function inGamut(rgb) {
    return rgb.every(function (v) { return v >= -1e-4 && v <= 1 + 1e-4; });
  }

  function resolveColor(color) {
    var rgb = toLinear(color);
    if (!inGamut(rgb)) {
      var lo = 0;
      var hi = color.c;
      for (var i = 0; i < 12; i++) {
        var mid = (lo + hi) / 2;
        if (inGamut(toLinear({ l: color.l, c: mid, h: color.h }))) lo = mid;
        else hi = mid;
      }
      rgb = toLinear({ l: color.l, c: lo, h: color.h });
    }
    return rgb.map(function (v) { return Math.min(1, Math.max(0, v)); });
  }

  function luminance(color) {
    var rgb = resolveColor(color);
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
  }

  function contrast(a, b) {
    var x = luminance(a);
    var y = luminance(b);
    return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
  }

  function ensureContrast(fg, bg, min) {
    if (contrast(fg, bg) >= min) return fg;

    var lean = fg.l >= bg.l ? 1 : -1;
    var dirs = [lean, -lean];
    for (var d = 0; d < dirs.length; d++) {
      var dir = dirs[d];
      var probe = { l: fg.l, c: fg.c, h: fg.h };
      for (var i = 0; i < 60; i++) {
        probe.l = Math.min(1, Math.max(0, probe.l + dir * 0.02));
        if (contrast(probe, bg) >= min) return probe;
        if (probe.l === 0 || probe.l === 1) break;
      }
    }

    var black = { l: 0, c: 0, h: fg.h };
    var white = { l: 1, c: 0, h: fg.h };
    return contrast(black, bg) >= contrast(white, bg) ? black : white;
  }

  function toHex(color) {
    return (
      "#" +
      resolveColor(color)
        .map(function (v) {
          var s = v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055;
          return Math.round(s * 255)
            .toString(16)
            .padStart(2, "0");
        })
        .join("")
    );
  }

  function fromHex(hex) {
    var n = parseInt(hex.slice(1), 16);
    var ch = [0, 0, 0];
    ch[0] = (n >> 16) & 255;
    ch[1] = (n >> 8) & 255;
    ch[2] = n & 255;
    var rgb = ch.map(function (v) {
      var s = v / 255;
      return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });

    var l = Math.cbrt(0.4122214708 * rgb[0] + 0.5363325363 * rgb[1] + 0.0514459929 * rgb[2]);
    var m = Math.cbrt(0.2119034982 * rgb[0] + 0.6806995451 * rgb[1] + 0.1073969566 * rgb[2]);
    var s = Math.cbrt(0.0883024619 * rgb[0] + 0.2817188376 * rgb[1] + 0.6299787005 * rgb[2]);

    var A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
    var B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;

    return {
      l: 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
      c: Math.hypot(A, B),
      h: (Math.atan2(B, A) * 180) / Math.PI,
    };
  }

  function mix(a, b, t) {
    var rad = function (v) { return (v * Math.PI) / 180; };
    var ax = a.c * Math.cos(rad(a.h));
    var ay = a.c * Math.sin(rad(a.h));
    var bx = b.c * Math.cos(rad(b.h));
    var by = b.c * Math.sin(rad(b.h));
    var x = ax + (bx - ax) * t;
    var y = ay + (by - ay) * t;
    return {
      l: a.l + (b.l - a.l) * t,
      c: Math.hypot(x, y),
      h: (Math.atan2(y, x) * 180) / Math.PI,
    };
  }

  function mixHex(a, b, t) {
    return toHex(mix(fromHex(a), fromHex(b), t));
  }

  var TINT_FLOOR = 4.55;
  var HOT = { h: 27, l: 0.58, pull: 0.6, c: 0.18 };
  var ROSE = { h: 358, l: 0.72, pull: 0.55, c: 0.16 };
  var BLUSH = { h: 12, l: 0.84, pull: 0.4, c: 0.1 };
  var BILE = { h: 142, l: 0.66, pull: 0.6, c: 0.13 };

  function tinted(head, eye, t) {
    var base = fromHex(head);
    var baseEye = fromHex(eye);

    var hotHead = {
      l: base.l + (t.l - base.l) * t.pull,
      c: Math.max(base.c, t.c),
      h: t.h,
    };
    hotHead = ensureContrast(hotHead, { l: 0.145, c: 0, h: 0 }, 1.5);

    var hotEye = ensureContrast(baseEye, hotHead, TINT_FLOOR);

    var dir = hotEye.l >= hotHead.l ? 1 : -1;
    var headHex = toHex(hotHead);
    for (var pass = 0; pass < 40; pass++) {
      var eyeHex = toHex(hotEye);
      var worst = Infinity;
      for (var i = 0; i <= 10; i++) {
        var tt = i / 10;
        worst = Math.min(
          worst,
          contrast(
            fromHex(mixHex(eye, eyeHex, tt)),
            fromHex(mixHex(head, headHex, tt)),
          ),
        );
      }
      if (worst >= TINT_FLOOR) return [headHex, eyeHex];
      var l = Math.min(1, Math.max(0, hotEye.l + dir * 0.02));
      if (l === hotEye.l) return [headHex, eyeHex];
      hotEye = { l: l, c: hotEye.c, h: hotEye.h };
    }
    return [headHex, toHex(hotEye)];
  }

  var TONES = [
    [0.14, { l: 0.82, c: 0.17 }],
    [0.3, { l: 0.73, c: 0.2 }],
    [0.5, { l: 0.64, c: 0.22 }],
    [0.7, { l: 0.55, c: 0.21 }],
    [0.87, { l: 0.46, c: 0.18 }],
    [1.0, { l: 0.36, c: 0.14 }],
  ];

  function toneAt(v) {
    for (var i = 0; i < TONES.length; i++) {
      if (v < TONES[i][0]) return TONES[i][1];
    }
    return TONES[0][1];
  }

  function ramp(hue, enforce, tone) {
    var t = toneAt(tone);
    var head = ensureContrast({ l: t.l, c: t.c, h: hue }, { l: 0.145, c: 0, h: 0 }, 1.5);
    var r = {
      bg: { l: 0.965, c: 0.01, h: hue },
      head: head,
      eye: head.l >= 0.5 ? { l: 0.17, c: 0.02, h: hue } : { l: 0.97, c: 0.012, h: hue },
    };
    if (enforce) {
      var floors = [["head", "bg", 1.25], ["eye", "head", 4.5]];
      for (var i = 0; i < floors.length; i++) {
        var fg = floors[i][0];
        var bg = floors[i][1];
        var min = floors[i][2];
        r[fg] = ensureContrast(r[fg], r[bg], min);
      }
    }
    return r;
  }

  function palette(hue, enforce, tone) {
    var r = ramp(hue, enforce, tone);
    var out = {};
    for (var k in r) out[k] = toHex(r[k]);
    return out;
  }

  // ----------------------------------------------------------------- shape
  function r2(v) {
    var s = Math.round(v * 100) / 100;
    return Object.is(s, -0) ? "0" : String(s);
  }

  function superellipse(o) {
    var k = Math.min(1, (8 * Math.pow(2, -1 / o.n) - 4) / 3);
    var a = o.rx;
    var b = o.ry;
    var ak = a * k;
    var bk = b * k;

    var pts = [
      [a, 0],
      [a, bk], [ak, b], [0, b],
      [-ak, b], [-a, bk], [-a, 0],
      [-a, -bk], [-ak, -b], [0, -b],
      [ak, -b], [a, -bk], [a, 0],
    ];

    var t = (o.rot * Math.PI) / 180;
    var cos = Math.cos(t);
    var sin = Math.sin(t);
    var at = function (i) {
      var x = pts[i][0];
      var y = pts[i][1];
      return r2(o.cx + x * cos - y * sin) + " " + r2(o.cy + x * sin + y * cos);
    };

    var d = "M" + at(0);
    for (var i = 1; i < 13; i += 3) d += "C" + at(i) + " " + at(i + 1) + " " + at(i + 2);
    return d + "Z";
  }

  function arc(cx, cy, w, depth) {
    return "M" + r2(cx - w) + " " + r2(cy) + "Q" + r2(cx) + " " + r2(cy + depth) + " " + r2(cx + w) + " " + r2(cy);
  }

  function blobPath(cx, cy, rx, ry, radii, rot) {
    var n = radii.length;
    var t0 = (rot * Math.PI) / 180;
    var p = [];
    for (var i = 0; i < n; i++) {
      var a = t0 + (2 * Math.PI * i) / n;
      p.push([cx + rx * radii[i] * Math.cos(a), cy + ry * radii[i] * Math.sin(a)]);
    }

    var at = function (i) { return p[((i % n) + n) % n]; };
    var d = "M" + r2(at(0)[0]) + " " + r2(at(0)[1]);

    for (var i = 0; i < n; i++) {
      var x0 = at(i - 1)[0], y0 = at(i - 1)[1];
      var x1 = at(i)[0], y1 = at(i)[1];
      var x2 = at(i + 1)[0], y2 = at(i + 1)[1];
      var x3 = at(i + 2)[0], y3 = at(i + 2)[1];
      d +=
        "C" + r2(x1 + (x2 - x0) / 6) + " " + r2(y1 + (y2 - y0) / 6) +
        " " + r2(x2 - (x3 - x1) / 6) + " " + r2(y2 - (y3 - y1) / 6) +
        " " + r2(x2) + " " + r2(y2);
    }

    return d + "Z";
  }

  function polygon(o) {
    var k = o.round > 0 ? (o.round < 1 ? o.round / 2 : 0.5) : 0;
    var t0 = (o.rot * Math.PI) / 180 - Math.PI / 2;
    var v = [];
    for (var i = 0; i < o.sides; i++) {
      var a = t0 + (2 * Math.PI * i) / o.sides;
      v.push([o.cx + o.rx * Math.cos(a), o.cy + o.ry * Math.sin(a)]);
    }

    var at = function (i) { return v[((i % o.sides) + o.sides) % o.sides]; };
    var cut = function (i, j) {
      var x0 = at(i)[0], y0 = at(i)[1];
      var x1 = at(j)[0], y1 = at(j)[1];
      return r2(x0 + (x1 - x0) * k) + " " + r2(y0 + (y1 - y0) * k);
    };

    var d = "M" + cut(0, -1);
    for (var i = 0; i < o.sides; i++) {
      var x = at(i)[0], y = at(i)[1];
      d += "Q" + r2(x) + " " + r2(y) + " " + cut(i, i + 1);
      if (k < 0.5) d += "L" + cut(i + 1, i);
    }
    return d + "Z";
  }

  function box(cx, cy, rx, ry) {
    var l = r2(cx - rx);
    var r = r2(cx + rx);
    return "M" + l + " " + r2(cy - ry) + "H" + r + "V" + r2(cy + ry) + "H" + l + "Z";
  }

  function taper(cx, cy, rx, ry, tip) {
    var t = Math.max(1.05, tip);
    var tx = rx * Math.sqrt(1 - 1 / (t * t));
    var ty = cy - ry / t;
    var apex = cy - t * ry;
    var px = tx * 0.14;
    var py = ty + 0.86 * (apex - ty);
    return (
      "M" + r2(cx - tx) + " " + r2(ty) +
      "L" + r2(cx - px) + " " + r2(py) +
      "Q" + r2(cx) + " " + r2(apex) + " " + r2(cx + px) + " " + r2(py) +
      "L" + r2(cx + tx) + " " + r2(ty) + "Z"
    );
  }

  // ---------------------------------------------------------------- styles
  function poly(b) { return polygon(b); }

  function spline(b) { return blobPath(b.cx, b.cy, b.rx, b.ry, b.radii, b.rot); }

  function shrunk(k) {
    return function (b) { return { cx: b.cx, cy: b.cy, rx: b.rx * k, ry: b.ry * k }; };
  }

  function splineFace(b) { return shrunk(Math.min.apply(null, b.radii) * 0.95)(b); }

  function polyFace(b) { return shrunk(0.84)(b); }

  var ROUND = { name: "round", core: 1 };

  var ORGANIC = { name: "organic", core: 0.98, path: spline, face: splineFace };

  var BOXY = {
    name: "boxy", core: 0.86,
    body: function (t, b) {
      b.n = t.num("body.n", 3.4, 6);
      b.rot = t.num("body.rot", -20, 20);
    },
  };

  var CAPSULE = {
    name: "capsule", core: 1.02,
    body: function (t, b) { b.ry *= t.num("capsule.squat", 0.55, 0.68); },
    face: shrunk(0.94),
    decorate: function (_t, b, out) {
      for (var s = -1; s <= 1; s += 2) {
        out.petals.push({ cx: b.cx + s * (b.rx - b.ry), cy: b.cy, r: b.ry });
      }
    },
    path: function (b) { return box(b.cx, b.cy, b.rx - b.ry, b.ry); },
  };

  var NUB = {
    name: "nub", core: 0.88,
    decorate: function (t, b, out) {
      var count = t.int("nub.n", 1, 2);
      for (var i = 0; i < count; i++) {
        var a = t.num("nub.a" + i, 0, 2 * Math.PI);
        out.petals.push({
          cx: b.cx + Math.cos(a) * b.rx * 0.88,
          cy: b.cy + Math.sin(a) * b.rx * 0.88,
          r: b.rx * t.num("nub.r" + i, 0.24, 0.4),
        });
      }
    },
  };

  var CLOUD = {
    name: "cloud", core: 0.78, face: splineFace, path: spline,
    decorate: function (t, b, out) {
      var count = t.int("cloud.n", 4, 6);
      for (var i = 0; i < count; i++) {
        var a = Math.PI + (Math.PI * (i + 0.5)) / count;
        out.petals.push({
          cx: b.cx + Math.cos(a) * b.rx * 0.8,
          cy: b.cy + Math.sin(a) * b.rx * 0.5,
          r: b.rx * t.num("cloud.r" + i, 0.44, 0.62),
        });
      }
    },
  };

  var DROPLET = {
    name: "droplet", core: 0.78,
    body: function (_t, b) { b.cy += 0.22 * b.ry; b.n = 2; },
    face: function (b) { return { cx: b.cx, cy: b.cy + b.ry * 0.05, rx: b.rx * 0.88, ry: b.ry * 0.88 }; },
    decorate: function (t, b, out) {
      out.extra.push(taper(b.cx, b.cy, b.rx, b.ry, t.num("droplet.tip", 1.4, 1.65)));
    },
  };

  var HEXAGON = {
    name: "hexagon", core: 1.05, path: poly, face: polyFace,
    body: function (t, b) {
      b.sides = 6;
      b.rot = t.num("body.rot", -12, 12);
      b.round = t.num("poly.round", 0.24, 0.5);
    },
  };

  var SUN = {
    name: "sun", core: 0.7,
    decorate: function (t, b, out) {
      var count = t.int("sun.n", 6, 9);
      var dist = b.rx * t.num("sun.dist", 1.0, 1.08);
      var pr = b.rx * t.num("sun.r", 0.2, 0.26);
      var off = t.num("sun.rot", 0, 2 * Math.PI);
      for (var i = 0; i < count; i++) {
        var a = off + (2 * Math.PI * i) / count;
        out.petals.push({ cx: b.cx + Math.cos(a) * dist, cy: b.cy + Math.sin(a) * dist, r: pr });
      }
    },
  };

  var TRIANGLE = {
    name: "triangle", core: 1.15, path: poly,
    body: function (t, b) {
      b.sides = 3;
      b.rot = t.num("body.rot", -5, 5);
      b.round = t.num("poly.round", 0.24, 0.5);
    },
    face: function (b) { return { cx: b.cx, cy: b.cy + b.ry * 0.1, rx: b.rx * 0.54, ry: b.ry * 0.36 }; },
  };

  var BANDS = [
    [ROUND, 0.22], [ORGANIC, 0.48], [BOXY, 0.6], [CAPSULE, 0.7], [NUB, 0.79],
    [CLOUD, 0.86], [DROPLET, 0.915], [HEXAGON, 0.95], [SUN, 0.98], [TRIANGLE, 1],
  ];

  function pick(v) {
    for (var i = 0; i < BANDS.length; i++) {
      if (v < BANDS[i][1]) return BANDS[i][0];
    }
    return BANDS[BANDS.length - 1][0];
  }

  function faceFit(t, b, face) {
    var rx = b.rx;
    var er0 = t.num("eye.rx", 0.075, 0.105) * rx;
    var ratio = t.num("eye.ratio", 1.9, 3.2);
    var scale = t.num("eye.scale", 0.78, 1.24);
    var stretch = t.num("eye.stretch", 0.85, 1.18);
    var clearance = t.num("eye.gap", 0.1, 0.24) * rx;
    var wide = er0 * Math.max(1, scale);
    var tall = er0 * ratio * Math.max(1, scale * stretch);
    var gap0 = wide + rx * 0.03 + clearance;

    var gx = t.jitter("gaze.x", 0.09) * face.rx;
    var gy = t.num("gaze.y", -0.2, 0.08) * face.ry;
    var dy = t.jitter("eye.dy", 0.04) * face.ry;
    var reach = Math.hypot(wide, tall);
    var need = Math.hypot(
      (Math.abs(gx) + gap0 + reach) / face.rx,
      (Math.abs(gy) + Math.abs(dy) + reach) / face.ry,
    );
    var fit = need > 0.9 ? 0.9 / need : 1;

    var er = er0 * fit;
    var eyeRy = er * ratio;
    var gap = gap0 * fit;
    var room = Math.max(0, Math.min(1, clearance / tall));
    var bound = Math.min(12, (Math.asin(room) * 180) / Math.PI);
    var lean = t.num("eye.lean", -1, 1) * bound;
    var lean2 = Math.max(-12, Math.min(12, lean + t.jitter("eye.lean2", 3.5)));

    var cx = face.cx + gx * fit;
    var cy = face.cy + gy * fit;
    return [
      { cx: cx - gap, cy: cy, rx: er, ry: eyeRy, n: t.num("eye.n", 3.5, 6), rot: lean },
      {
        cx: cx + gap, cy: cy + dy * fit,
        rx: er * scale, ry: eyeRy * scale * stretch,
        n: t.num("eye.n", 3.5, 6), rot: lean2,
      },
    ];
  }

  function layout(t) {
    var shape = pick(t("shape"));
    var r = t.num("body.r", 31, 38) * shape.core;
    var body = {
      cx: 50 + t.jitter("body.x", 1.5),
      cy: 50 + t.jitter("body.y", 1.5),
      rx: r,
      ry: r * t.num("body.ratio", 0.92, 1.08),
      n: t.num("body.n", 1.9, 2.5),
      rot: 0,
      radii: [],
    };
    var pts = t.int("body.pts", 6, 8);
    for (var i = 0; i < pts; i++) body.radii.push(1 + t.jitter("body.r" + i, 0.16));
    if (shape.body) shape.body(t, body);

    var face = shape.face ? shape.face(body) : body;
    var deco = { petals: [], extra: [] };
    if (shape.decorate) shape.decorate(t, body, deco);

    return {
      shape: shape.name,
      draw: shape.path,
      body: body,
      face: face,
      petals: deco.petals,
      extra: deco.extra,
      eyes: faceFit(t, body, face),
    };
  }

  function renderStyle(l, p, mo) {
    var eye = function (e, i) {
      var path = '<path d="' + superellipse(e) + '"/>';
      if (mo) {
        return '<g class="mo-eye" style="--mo-wrap:' + (i ? 1 : -1) + ";--mo-lean:" +
          r2(e.rot) + ';transform-origin:' + r2(e.cx) + "px " + r2(e.cy) + 'px">' + path + "</g>";
      }
      return path;
    };
    var body =
      '<g fill="' + p.head + '">' +
      l.petals.map(function (d) {
        return '<circle cx="' + r2(d.cx) + '" cy="' + r2(d.cy) + '" r="' + r2(d.r) + '"/>';
      }).join("") +
      l.extra.map(function (d) { return '<path d="' + d + '"/>'; }).join("") +
      '<path d="' + (l.draw ? l.draw(l.body) : superellipse(l.body)) + '"/>' +
      "</g>" +
      '<g fill="' + p.eye + '"' + (mo ? ' class="mo-eyes"' : "") + ">" +
      l.eyes.map(eye).join("") +
      "</g>";
    return mo ? '<g class="mo-breathe"><g class="mo-bob">' + body + "</g></g>" : body;
  }

  // ------------------------------------------------------------- expression
  var IDENT = {
    esx: 1, esy: 1, tilt: 0, edy: 0, edx: 0,
    esx2: 0, esy2: 0, tilt2: 0, edy2: 0,
    lock: 0, heat: 0, shake: 0, rock: 0, bdy: 0,
  };

  function r3(v) {
    var s = Math.round(v * 1000) / 1000;
    return Object.is(s, -0) ? "0" : String(s);
  }

  function bakePose(l, p) {
    var eyes = l.eyes.map(function (e, i) {
      return {
        cx: e.cx + p.edx * (i ? 1 : -1),
        cy: e.cy + p.edy + (i ? p.edy2 : 0),
        rx: e.rx * (p.esx + (i ? p.esx2 : 0)),
        ry: e.ry * (p.esy + (i ? p.esy2 : 0)),
        n: e.n,
        rot: e.rot * (1 - p.lock) + (p.tilt + (i ? p.tilt2 : 0)) * (i ? 1 : -1),
      };
    });
    return {
      l: { shape: l.shape, draw: l.draw, body: l.body, face: l.face, petals: l.petals, extra: l.extra, eyes: eyes },
      wrap: p.bdy !== 0 ? "translate(0 " + r3(p.bdy) + ")" : "",
    };
  }

  function tintWith(pal, p, t) {
    var pair = tinted(pal.head, pal.eye, t);
    return {
      head: mixHex(pal.head, pair[0], p.heat),
      eye: mixHex(pal.eye, pair[1], p.heat),
    };
  }

  function mk(p, tint) {
    return tint ? { p: p, bake: bakePose, tint: tint } : { p: p, bake: bakePose };
  }

  var EXPRESSIONS = {
    idle: mk(IDENT),
    happy: mk({
      esx: 1.72, esy: 0.3, tilt: 8, edy: -1.5, edx: 1.5,
      esx2: 0.08, esy2: 0.05, tilt2: -16, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: -2.2,
    }),
    sad: mk({
      esx: 0.6, esy: 0.56, tilt: 26, edy: 3.6, edx: 1.9,
      esx2: -0.05, esy2: -0.07, tilt2: -7, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: 2.6,
    }),
    mad: mk({
      esx: 1.85, esy: 0.26, tilt: -33, edy: 0.4, edx: 0.6,
      esx2: 0, esy2: -0.03, tilt2: 5, edy2: 0,
      lock: 1, heat: 0.62, shake: 0.55, rock: 0, bdy: 0.8,
    }, function (pal, p) { return tintWith(pal, p, HOT); }),
    surprised: mk({
      esx: 1.34, esy: 1.2, tilt: -6, edy: -1.05, edx: 0.5,
      esx2: 0.05, esy2: 0.07, tilt2: 3, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: -1.4,
    }),
    wink: mk({
      esx: 1.32, esy: 0.76, tilt: 5, edy: -0.6, edx: 0.8,
      esx2: 0.26, esy2: -0.56, tilt2: -11, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: -1.1,
    }),
    sleepy: mk({
      esx: 1.14, esy: 0.22, tilt: 0, edy: 2.4, edx: 0.3,
      esx2: -0.04, esy2: 0.03, tilt2: 4, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: 1.2,
    }),
    smug: mk({
      esx: 1.3, esy: 0.42, tilt: 18, edy: -0.5, edx: 0.5,
      esx2: 0.06, esy2: -0.06, tilt2: -36, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: -1,
    }),
    unsure: mk({
      esx: 0.95, esy: 1.02, tilt: 4, edy: -0.2, edx: 0.3,
      esx2: 0.24, esy2: -0.44, tilt2: -18, edy2: 0,
      lock: 1, heat: 0, shake: 0, rock: 0, bdy: 0,
    }),
    scared: mk({
      esx: 0.78, esy: 0.96, tilt: -12, edy: -1.5, edx: -0.8,
      esx2: -0.04, esy2: 0.05, tilt2: 4, edy2: 0,
      lock: 1, heat: 0, shake: 0.35, rock: 0, bdy: -0.6,
    }),
    love: mk({
      esx: 0.86, esy: 1.28, tilt: -14, edy: -0.5, edx: -0.35,
      esx2: 0.05, esy2: 0.06, tilt2: 6, edy2: 0,
      lock: 1, heat: 0.6, shake: 0, rock: 0, bdy: -1.6,
    }, function (pal, p) { return tintWith(pal, p, ROSE); }),
    shy: mk({
      esx: 0.62, esy: 0.5, tilt: 10, edy: 1.4, edx: -0.2,
      esx2: -0.05, esy2: -0.04, tilt2: -8, edy2: 0,
      lock: 1, heat: 0.55, shake: 0, rock: 0, bdy: 0.9,
    }, function (pal, p) { return tintWith(pal, p, BLUSH); }),
    sick: mk({
      esx: 1.25, esy: 0.34, tilt: 20, edy: 1.8, edx: 0.8,
      esx2: 0.05, esy2: -0.05, tilt2: -6, edy2: 0,
      lock: 1, heat: 0.6, shake: 0.18, rock: 0, bdy: 1.4,
    }, function (pal, p) { return tintWith(pal, p, BILE); }),
    thinking: mk({
      esx: 1.15, esy: 0.62, tilt: 0, edy: 4.2, edx: 0.4,
      esx2: 0.02, esy2: 0.06, tilt2: 0, edy2: -8.4,
      lock: 1, heat: 0, shake: 0, rock: 0.8, bdy: -0.4,
    }),
  };

  // ------------------------------------------------------------------ render
  function escape(s) {
    return String(s).replace(/[&<>]/g, function (c) {
      return c === "&" ? "&amp;" : c === "<" ? "&lt;" : "&gt;";
    });
  }

  function resolveOpts(seed, opts) {
    var t = traits(seed, opts.normalize !== false, opts.traits);
    var overrides = opts.palette || {};
    var merged = Object.assign(
      palette(
        opts.hue !== undefined ? opts.hue : t.num("hue", 0, 360),
        opts.contrast !== false,
        opts.tone !== undefined ? opts.tone : t("tone"),
      ),
      overrides,
    );
    if (Object.keys(overrides).length) {
      var floors = [["head", "bg", 1.25], ["eye", "head", 4.5]];
      for (var i = 0; i < floors.length; i++) {
        var fg = floors[i][0];
        var bg = floors[i][1];
        var min = floors[i][2];
        merged[fg] = toHex(ensureContrast(fromHex(merged[fg]), fromHex(merged[bg]), min));
      }
    }
    return { t: t, palette: merged };
  }

  function backdrop(opts, p) {
    var bg = opts.background !== undefined ? opts.background : false;
    if (bg === false) return undefined;
    return {
      d: bg === "square"
        ? "M0 0H100V100H0Z"
        : superellipse({ cx: 50, cy: 50, rx: 50, ry: 50, n: bg === "circle" ? 2 : 6, rot: 0 }),
      fill: p.bg,
    };
  }

  function posed(l, opts, mo) {
    var e = opts.expression && EXPRESSIONS[opts.expression];
    if (mo || !e) return { l: l, wrap: "" };
    return e.bake(l, e.p);
  }

  function tintedPalette(p, opts) {
    var e = opts.expression && EXPRESSIONS[opts.expression];
    return e && e.tint ? Object.assign({}, p, e.tint(p, e.p)) : p;
  }

  function animElement(anim) {
    if (anim === "bob") {
      return '<animateTransform attributeName="transform" type="translate" ' +
        'values="0 0; 0 -7; 0 0" keyTimes="0; 0.5; 1" ' +
        'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" ' +
        'dur="3s" repeatCount="indefinite"/>';
    }
    if (anim === "wave") {
      return '<animateTransform attributeName="transform" type="rotate" ' +
        'values="0 50 50; 5 50 50; 0 50 50; -5 50 50; 0 50 50" ' +
        'keyTimes="0; 0.25; 0.5; 0.75; 1" ' +
        'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1" ' +
        'dur="4s" repeatCount="indefinite"/>';
    }
    if (anim === "spin") {
      return '<animateTransform attributeName="transform" type="rotate" ' +
        'from="0 50 50" to="360 50 50" dur="6s" repeatCount="indefinite"/>';
    }
    if (anim === "pulse") {
      return '<animateTransform attributeName="transform" ' +
        'values="translate(50 50) scale(1) translate(-50 -50); ' +
        'translate(50 50) scale(1.06) translate(-50 -50); ' +
        'translate(50 50) scale(1) translate(-50 -50)" ' +
        'keyTimes="0; 0.5; 1" calcMode="spline" ' +
        'keySplines="0.45 0 0.55 1;0.45 0 0.55 1" ' +
        'dur="3s" repeatCount="indefinite"/>';
    }
    return null;
  }

  function blobatar(name, opts) {
    opts = opts || {};
    var resolved = resolveOpts(name, opts);
    var p = tintedPalette(resolved.palette, opts);
    var dim = opts.size ? ' width="' + opts.size + '" height="' + opts.size + '"' : "";
    var label = opts.title ? "<title>" + escape(opts.title) + "</title>" : "";
    var plate = backdrop(opts, p);
    var pose = posed(layout(resolved.t), opts, null);
    var body =
      label +
      (plate ? '<path d="' + plate.d + '" fill="' + plate.fill + '"/>' : "") +
      (pose.wrap ? '<g transform="' + pose.wrap + '">' + renderStyle(pose.l, p) + "</g>" : renderStyle(pose.l, p));
    var anim = animElement(opts.anim);
    if (anim) body = label + (plate ? '<path d="' + plate.d + '" fill="' + plate.fill + '"/>' : "") +
      "<g>" + anim + (pose.wrap ? '<g transform="' + pose.wrap + '">' + renderStyle(pose.l, p) + "</g>" : renderStyle(pose.l, p)) + "</g>";
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"' + dim + ">" + body + "</svg>";
  }

  var SHAPE_TRAITS = {
    round: 0.11, organic: 0.35, boxy: 0.54, capsule: 0.65, nub: 0.745,
    cloud: 0.825, droplet: 0.8875, hexagon: 0.9325, sun: 0.965, triangle: 0.99,
  };

  function paletteFor(name, opts) {
    opts = opts || {};
    var resolved = resolveOpts(name, opts);
    return tintedPalette(resolved.palette, opts);
  }

  function colorFor(name, opts) {
    return paletteFor(name, opts).head;
  }

  global.Blobatar = {
    blobatar: blobatar,
    _layout: layout,
    _traits: traits,
    shapeTraits: SHAPE_TRAITS,
    paletteFor: paletteFor,
    colorFor: colorFor,
  };
})(typeof window !== "undefined" ? window : globalThis);