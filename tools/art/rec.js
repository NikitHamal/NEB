// Records the call stream of one art, so it can be diffed against the Kotlin's.
global.Path2D = function () { this.ops = []; };
Path2D.prototype.moveTo = function (x, y) { this.ops.push(['M', x, y]); };
Path2D.prototype.lineTo = function (x, y) { this.ops.push(['L', x, y]); };
Path2D.prototype.bezierCurveTo = function (a,b,c,d,e,f) { this.ops.push(['C',a,b,c,d,e,f]); };
Path2D.prototype.closePath = function () { this.ops.push(['Z']); };
Path2D.prototype.rect = function () {}; Path2D.prototype.arc = function () {};
Path2D.prototype.ellipse = function () {};
global.window = global; global.document = {
  readyState: 'complete', querySelectorAll: function () { return []; },
  addEventListener: function () {}, documentElement: { getAttribute: function(){return null;} }
};
global.ResizeObserver = null; global.matchMedia = null;
require(require('path').join(__dirname, '../../backend_python/web/static/web/js/neb-art.js'));

function n(v) { return Math.round(v * 1e6) / 1e6; }
function col(c) { return [n(c.r), n(c.g), n(c.b), n(c.a)]; }
function Rec(w, h) { this.w = w; this.h = h; this.log = []; }
Rec.prototype._st = function (s) { return s ? [n(s.width), s.cap] : null; };
Rec.prototype.drawRect = function (o) {
  this.log.push(['rect', o.brush ? ['brush', o.brush.kind, o.brush.o.colors.map(col)] : col(o.color),
    o.topLeft ? [n(o.topLeft.x), n(o.topLeft.y)] : null,
    o.size ? [n(o.size.w), n(o.size.h)] : null, this._st(o.style)]);
};
Rec.prototype.drawCircle = function (o) {
  this.log.push(['circle', col(o.color), n(o.radius), n(o.center.x), n(o.center.y), this._st(o.style)]);
};
Rec.prototype.drawLine = function (o) {
  this.log.push(['line', col(o.color), n(o.start.x), n(o.start.y), n(o.end.x), n(o.end.y),
    n(o.strokeWidth === undefined ? 1 : o.strokeWidth), o.cap || null]);
};
Rec.prototype.drawPath = function (o) {
  this.log.push(['path', col(o.color), o.path.p.ops.map(function (q) {
    return [q[0]].concat(q.slice(1).map(n)); }), this._st(o.style)]);
};
Rec.prototype.drawArc = function (o) {
  this.log.push(['arc', col(o.color), n(o.startAngle), n(o.sweepAngle), !!o.useCenter,
    n(o.topLeft.x), n(o.topLeft.y), n(o.size.w), n(o.size.h), this._st(o.style)]);
};
Rec.prototype.rotate = function (deg, pivot, body) {
  this.log.push(['rotate>', n(deg), n(pivot.x), n(pivot.y)]); body(); this.log.push(['<rotate']);
};
Rec.prototype.translate = function (x, y, body) {
  this.log.push(['translate>', n(x), n(y)]); body(); this.log.push(['<translate']);
};

var A = NebArt.__arts, out = {};
// MEMBER is the `else` branch of drawCoverMotif, so it has no MOTIF entry.
var coverFallback = A.fallback;
var W = 320, H = 120;

// every banner art, on every family that offers it, with a fixed seed
Object.keys(A.FAMILY).forEach(function (fam) {
  A.FAMILY[fam].forEach(function (fn, i) {
    var key = fam + '#' + i + '#' + fn.name;
    var p = NebArt.bannerPalette('Physics', false);
    var d = new Rec(W, H);
    fn(d, p, new NebArt.Rng(NebArt.stableSeed(key)));
    out[key] = d.log;
  });
});

// every cover motif, plus ground and finish
Object.keys(A.COVER_PALETTES).forEach(function (role) {
  var p = A.COVER_PALETTES[role];
  ['ground', 'motif', 'finish'].forEach(function (stage) {
    var d = new Rec(640, 260);
    var r = new NebArt.Rng(NebArt.stableSeed('cover|nikit|' + role));
    var fn = stage === 'ground' ? A.ground : stage === 'finish' ? A.finish : (A.MOTIF[role] || coverFallback);
    if (!fn) return;
    fn(d, p, r);
    out['COVER#' + role + '#' + stage] = d.log;
  });
});

// and the seed/family/selection contract itself
var probes = ['Physics', 'Health and Physical Education', 'Computer Science',
              'सामाजिक अध्ययन', 'Compulsory English', 'Moral Education', '', 'Model Set 2081'];
out['__contract'] = probes.map(function (s) {
  var h = NebArt.stableSeed(s + '|pdf');
  var fam = NebArt.subjectFamily(s);
  return [s, fam, h, ((h >>> 3) & 0x7FFFFFFF) % A.FAMILY[fam].length,
          A.FAMILY[fam][((h >>> 3) & 0x7FFFFFFF) % A.FAMILY[fam].length].name];
});
process.stdout.write(JSON.stringify(out));
