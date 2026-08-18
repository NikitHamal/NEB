/*!
 * blobatar.js — deterministic geometric blobatars from any string.
 * Vanilla-JS port of the blobatar library (github.com/Alain00/blobatar, gen 1),
 * vendored so the NEBians avatar page can render realtime previews client-side.
 * The same name always renders the same SVG, in every runtime.
 */
(function () {
  "use strict";

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
    var state = seedState(seed, normalize);
    var t = function (key) {
      var o = overrides && overrides[key];
      return o === undefined ? stream(state, key) : o > 0 ? (o < 1 ? o : 0.999999) : 0;
    };
    t.num = function (key, min, max) { return min + t(key) * (max - min); };
    t.int = function (key, min, max) { return min + Math.floor(t(key) * (max - min + 1)); };
    t.pick = function (key, options) { return options[Math.floor(t(key) * options.length)]; };
    t.bool = function (key, p) { return t(key) < (p === undefined ? 0.5 : p); };
    t.jitter = function (key, amount) { return (t(key) * 2 - 1) * amount; };
    return t;
  }

  function toLinear(l, c, h) {
    var r = (h * Math.PI) / 180;
    var a = c * Math.cos(r);
    var b = c * Math.sin(r);

    var l_ = l + 0.3963377774 * a + 0.2158037573 * b;
    var m_ = l - 0.1055613458 * a - 0.0638541728 * b;
    var s_ = l - 0.0894841775 * a - 1.291485548 * b;

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

  function resolve(color) {
    var rgb = toLinear(color[0], color[1], color[2]);
    if (!inGamut(rgb)) {
      var lo = 0, hi = color[1];
      for (var i = 0; i < 12; i++) {
        var mid = (lo + hi) / 2;
        if (inGamut(toLinear(color[0], mid, color[2]))) lo = mid;
        else hi = mid;
      }
      rgb = toLinear(color[0], lo, color[2]);
    }
    return rgb.map(function (v) { return Math.min(1, Math.max(0, v)); });
  }

  function luminance(color) {
    var rgb = resolve(color);
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
  }

  function contrast(a, b) {
    var x = luminance(a), y = luminance(b);
    return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
  }

  function ensureContrast(fg, bg, min) {
    if (contrast(fg, bg) >= min) return fg;
    var lean = fg[0] >= bg[0] ? 1 : -1;
    for (var d = 0; d < 2; d++) {
      var dir = d === 0 ? lean : -lean;
      var probe = fg.slice();
      for (var i = 0; i < 60; i++) {
        probe[0] = Math.min(1, Math.max(0, probe[0] + dir * 0.02));
        if (contrast(probe, bg) >= min) return probe;
        if (probe[0] === 0 || probe[0] === 1) break;
      }
    }
    var black = [0, 0, fg[2]];
    var white = [1, 0, fg[2]];
    return contrast(black, bg) >= contrast(white, bg) ? black : white;
  }

  function toHex(color) {
    return (
      "#" +
      resolve(color)
        .map(function (v) {
          var s = v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055;
          return Math.round(s * 255)
            .toString(16)
            .padStart(2, "0");
        })
        .join("")
    );
  }

  var TONES = [
    [0.2, [0.86, 0.085]],
    [0.36, [0.9, 0.028]],
    [0.62, [0.73, 0.135]],
    [0.8, [0.62, 0.165]],
    [0.93, [0.87, 0.16]],
    [1.0, [0.34, 0.035]],
  ];

  function toneAt(v) {
    for (var i = 0; i < TONES.length; i++) {
      if (v < TONES[i][0]) return TONES[i][1];
    }
    return TONES[0][1];
  }

  var DARK_SURFACE = [0.145, 0, 0];
  var SURFACE_FLOOR = 1.5;

  var FLOORS = [
    ["head", "bg", 1.25],
    ["eye", "head", 4.5],
  ];

  function ramp(hue, enforce, tone) {
    var t = toneAt(tone);
    var head = ensureContrast([t[0], t[1], hue], DARK_SURFACE, SURFACE_FLOOR);
    var r = {
      bg: [0.965, 0.01, hue],
      head: head,
      eye: head[0] >= 0.5 ? [0.17, 0.02, hue] : [0.97, 0.012, hue],
    };
    if (enforce !== false) {
      for (var i = 0; i < FLOORS.length; i++) {
        r[FLOORS[i][0]] = ensureContrast(r[FLOORS[i][0]], r[FLOORS[i][1]], FLOORS[i][2]);
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

  function r2(v) {
    var s = Math.round(v * 100) / 100;
    return Object.is(s, -0) ? "0" : String(s);
  }

  function superellipse(cx, cy, rx, ry, n, rot) {
    n = n === undefined ? 4 : n;
    rot = rot === undefined ? 0 : rot;
    var k = Math.min(1, (8 * Math.pow(2, -1 / n) - 4) / 3);
    var a = rx, b = ry, ak = a * k, bk = b * k;

    var pts = [
      [a, 0],
      [a, bk], [ak, b], [0, b],
      [-ak, b], [-a, bk], [-a, 0],
      [-a, -bk], [-ak, -b], [0, -b],
      [ak, -b], [a, -bk], [a, 0],
    ];

    var t = (rot * Math.PI) / 180;
    var cos = Math.cos(t), sin = Math.sin(t);
    var at = function (i) {
      var x = pts[i][0], y = pts[i][1];
      return r2(cx + x * cos - y * sin) + " " + r2(cy + x * sin + y * cos);
    };

    var d = "M" + at(0);
    for (var i = 1; i < 13; i += 3) d += "C" + at(i) + " " + at(i + 1) + " " + at(i + 2);
    return d + "Z";
  }

  function blobPath(cx, cy, rx, ry, radii, rot) {
    rot = rot === undefined ? 0 : rot;
    var n = radii.length;
    var t0 = (rot * Math.PI) / 180;
    var p = radii.map(function (m, i) {
      var a = t0 + (2 * Math.PI * i) / n;
      return [cx + rx * m * Math.cos(a), cy + ry * m * Math.sin(a)];
    });

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

  function shapeOf(v) {
    return v < 0.28
      ? "round"
      : v < 0.58
        ? "organic"
        : v < 0.72
          ? "boxy"
          : v < 0.84
            ? "nub"
            : v < 0.93
              ? "cloud"
              : "sun";
  }

  var CORE = {
    round: 1,
    boxy: 0.86,
    organic: 0.98,
    cloud: 0.78,
    sun: 0.7,
    nub: 0.88,
  };

  function layout(t) {
    var shape = shapeOf(t("shape"));
    var r = t.num("body.r", 31, 38) * CORE[shape];
    var rx = r;
    var ry = r * t.num("body.ratio", 0.92, 1.08);

    var body = {
      cx: 50 + t.jitter("body.x", 1.5),
      cy: 50 + t.jitter("body.y", 1.5),
      rx: rx,
      ry: ry,
      n: shape === "boxy" ? t.num("body.n", 3.4, 6) : t.num("body.n", 1.9, 2.5),
      rot: shape === "boxy" ? t.num("body.rot", -20, 20) : 0,
      radii: Array.from(
        { length: t.int("body.pts", 6, 8) },
        function (_, i) { return 1 + t.jitter("body.r" + i, 0.16); },
      ),
    };

    var gx = t.jitter("gaze.x", 0.09) * rx;
    var gy = t.num("gaze.y", -0.2, 0.08) * ry;

    var er0 = t.num("eye.rx", 0.075, 0.105) * rx;
    var ratio = t.num("eye.ratio", 1.9, 3.2);
    var scale = t.num("eye.scale", 0.78, 1.24);
    var stretch = t.num("eye.stretch", 0.85, 1.18);

    var clearance = t.num("eye.gap", 0.1, 0.24) * rx;
    var wide = er0 * Math.max(1, scale);
    var tall = er0 * ratio * Math.max(1, scale * stretch);
    var gap0 = wide + rx * 0.03 + clearance;

    var tight = shape === "organic" || shape === "cloud"
      ? Math.min.apply(null, body.radii) * 0.95
      : 1;
    var need = (Math.abs(gx) + gap0 + Math.hypot(wide, tall)) / rx;
    var fit = need > tight * 0.9 ? (tight * 0.9) / need : 1;

    var er = er0 * fit;
    var gap = gap0 * fit;
    var eyeRy = er * ratio;

    var MAX_LEAN = 12;
    var room = Math.max(0, Math.min(1, (clearance * fit) / (tall * fit)));
    var bound = Math.min(MAX_LEAN, (Math.asin(room) * 180) / Math.PI);
    var lean = t.num("eye.lean", -1, 1) * bound;
    var lean2 = Math.max(
      -MAX_LEAN,
      Math.min(MAX_LEAN, lean + t.jitter("eye.lean2", 3.5)),
    );

    var petals = [];

    if (shape === "sun") {
      var count = t.int("sun.n", 6, 9);
      var dist = r * t.num("sun.dist", 1.0, 1.08);
      var pr = r * t.num("sun.r", 0.2, 0.26);
      var off = t.num("sun.rot", 0, 2 * Math.PI);
      for (var i = 0; i < count; i++) {
        var a = off + (2 * Math.PI * i) / count;
        petals.push({
          cx: body.cx + Math.cos(a) * dist,
          cy: body.cy + Math.sin(a) * dist,
          r: pr,
        });
      }
    } else if (shape === "cloud") {
      var ccount = t.int("cloud.n", 4, 6);
      for (var ci = 0; ci < ccount; ci++) {
        var ca = Math.PI + (Math.PI * (ci + 0.5)) / ccount;
        petals.push({
          cx: body.cx + Math.cos(ca) * r * 0.8,
          cy: body.cy + Math.sin(ca) * r * 0.5,
          r: r * t.num("cloud.r" + ci, 0.44, 0.62),
        });
      }
    } else if (shape === "nub") {
      var ncount = t.int("nub.n", 1, 2);
      for (var ni = 0; ni < ncount; ni++) {
        var na = t.num("nub.a" + ni, 0, 2 * Math.PI);
        petals.push({
          cx: body.cx + Math.cos(na) * r * 0.88,
          cy: body.cy + Math.sin(na) * r * 0.88,
          r: r * t.num("nub.r" + ni, 0.24, 0.4),
        });
      }
    }

    return {
      shape: shape,
      body: body,
      petals: petals,
      eyes: [
        {
          cx: body.cx + gx - gap,
          cy: body.cy + gy,
          rx: er,
          ry: eyeRy,
          n: t.num("eye.n", 3.5, 6),
          rot: lean,
        },
        {
          cx: body.cx + gx + gap,
          cy: body.cy + gy + t.jitter("eye.dy", 0.04) * ry,
          rx: er * scale,
          ry: eyeRy * scale * stretch,
          n: t.num("eye.n", 3.5, 6),
          rot: lean2,
        },
      ],
    };
  }

  var rr2 = function (v) { return Math.round(v * 100) / 100; };

  function render(l, p) {
    var b = l.body;
    var core =
      l.shape === "organic" || l.shape === "cloud"
        ? blobPath(
            b.cx,
            b.cy,
            b.rx,
            b.ry,
            b.radii,
            l.shape === "cloud" ? 0 : b.rot,
          )
        : superellipse(b.cx, b.cy, b.rx, b.ry, b.n, b.rot);

    var eye = function (e) {
      return '<path d="' + superellipse(e.cx, e.cy, e.rx, e.ry, e.n, e.rot) + '"/>';
    };

    var body =
      '<g fill="' + p.head + '">' +
      l.petals
        .map(function (d) {
          return '<circle cx="' + rr2(d.cx) + '" cy="' + rr2(d.cy) + '" r="' + rr2(d.r) + '"/>';
        })
        .join("") +
      '<path d="' + core + '"/>' +
      "</g>" +
      '<g fill="' + p.eye + '">' +
      l.eyes.map(eye).join("") +
      "</g>";

    return body;
  }

  var escapeHtml = function (s) {
    return s.replace(/[&<>]/g, function (c) {
      return c === "&" ? "&amp;" : c === "<" ? "&lt;" : "&gt;";
    });
  };

  function backdrop(opts, p) {
    var bg = opts.background === undefined ? false : opts.background;
    if (bg === false) return null;
    return {
      d:
        bg === "square"
          ? "M0 0H100V100H0Z"
          : superellipse(50, 50, 50, 50, bg === "circle" ? 2 : 6),
      fill: p.bg,
    };
  }

  function blobatar(name, opts) {
    opts = opts || {};
    var t = traits(name, opts.normalize, opts.traits);
    var p = palette(
      opts.hue === undefined ? t.num("hue", 0, 360) : opts.hue,
      opts.contrast === undefined ? true : opts.contrast,
      opts.tone === undefined ? t("tone") : opts.tone,
    );
    for (var k in (opts.palette || {})) p[k] = opts.palette[k];

    var dim = opts.size ? ' width="' + opts.size + '" height="' + opts.size + '"' : "";
    var title = opts.title ? "<title>" + escapeHtml(opts.title) + "</title>" : "";
    var plate = backdrop(opts, p);
    var plateSvg = plate
      ? '<path d="' + plate.d + '" fill="' + plate.fill + '"/>'
      : "";
    var body = title + plateSvg + render(layout(t), p);
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"' + dim + ">" + body + "</svg>";
  }

  function uri(name, opts) {
    return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(blobatar(name, opts));
  }

  window.Blobatar = { blobatar: blobatar, uri: uri, palette: palette };
})();