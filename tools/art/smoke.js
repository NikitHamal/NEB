// Exercises the public path end to end: scan() -> paint() -> prepare() ->
// drawBanner/drawCover through a stubbed Canvas2D. Proves the file works as a
// browser module, not just that the arts arithmetic matches.
global.Path2D = function () {}; 
['moveTo','lineTo','bezierCurveTo','closePath','rect','arc','ellipse']
  .forEach(function (m) { Path2D.prototype[m] = function () {}; });

var calls = { fill: 0, stroke: 0, grad: 0, setTransform: 0, clear: 0 };
function Grad() { calls.grad++; }
Grad.prototype.addColorStop = function () {};
function Ctx() {}
Ctx.prototype.setTransform = function () { calls.setTransform++; };
Ctx.prototype.clearRect = function () { calls.clear++; };
Ctx.prototype.save = function () {}; Ctx.prototype.restore = function () {};
Ctx.prototype.translate = function () {}; Ctx.prototype.rotate = function () {};
Ctx.prototype.scale = function () {}; Ctx.prototype.beginPath = function () {};
Ctx.prototype.moveTo = function () {}; Ctx.prototype.lineTo = function () {};
Ctx.prototype.bezierCurveTo = function () {}; Ctx.prototype.closePath = function () {};
Ctx.prototype.rect = function () {}; Ctx.prototype.arc = function () {};
Ctx.prototype.ellipse = function () {}; Ctx.prototype.clip = function () {};
Ctx.prototype.fill = function () { calls.fill++; };
Ctx.prototype.stroke = function () { calls.stroke++; };
Ctx.prototype.fillRect = function () { calls.fill++; };
Ctx.prototype.strokeRect = function () { calls.stroke++; };
Ctx.prototype.createLinearGradient = function () { return new Grad(); };
Ctx.prototype.createRadialGradient = function () { return new Grad(); };

function Canvas() { this.className = ''; this.tagName = 'CANVAS';
  this.clientWidth = 0; this.clientHeight = 0; this._ctx = new Ctx(); }
Canvas.prototype.getContext = function () { return this._ctx; };

function El(attrs, w, h) {
  this.tagName = 'DIV'; this.attrs = attrs; this.children = [];
  this.clientWidth = w; this.clientHeight = h; this.style = { props: {},
    setProperty: function (k, v) { this.props[k] = v; } };
  this.firstChild = null;
}
El.prototype.getAttribute = function (k) {
  return k in this.attrs ? this.attrs[k] : null; };
El.prototype.querySelector = function () { return this.children[0] || null; };
El.prototype.insertBefore = function (c) {
  c.clientWidth = this.clientWidth; c.clientHeight = this.clientHeight;
  this.children.unshift(c); this.firstChild = c; };

var els = [
  new El({ 'data-neb-art': 'banner', 'data-neb-subject': 'Physics', 'data-neb-seed': '41|pdf' }, 300, 120),
  new El({ 'data-neb-art': 'banner', 'data-neb-subject': 'Moral Education', 'data-neb-seed': '9|note' }, 300, 120),
  new El({ 'data-neb-art': 'banner', 'data-neb-subject': '', 'data-neb-seed': '' }, 300, 120),
  new El({ 'data-neb-art': 'cover', 'data-neb-role': 'TUTOR', 'data-neb-seed': 'nikit' }, 320, 180),
  new El({ 'data-neb-art': 'cover', 'data-neb-role': 'MEMBER', 'data-neb-seed': 'asha' }, 320, 180),
  new El({ 'data-neb-art': 'cover', 'data-neb-role': 'nonsense', 'data-neb-seed': 'x' }, 320, 180),
];
var listeners = {};
global.window = global;
global.document = {
  readyState: 'complete',
  querySelectorAll: function () { return els; },
  addEventListener: function (n, f) { (listeners[n] = listeners[n] || []).push(f); },
  createElement: function () { return new Canvas(); },
  documentElement: { getAttribute: function () { return null; } }
};
global.ResizeObserver = null;
global.matchMedia = function () { return { matches: false }; };
global.devicePixelRatio = 2;

require(require('path').join(__dirname, '../../backend_python/web/static/web/js/neb-art.js'));

var painted = els.filter(function (e) { return e.children.length === 1; });
console.log('hosts painted: %d / %d', painted.length, els.length);
console.log('canvas class:', els[0].children[0].className);
console.log('backing store for a 300x120 host at dpr 2:',
            els[0].children[0].width + 'x' + els[0].children[0].height);
console.log('draw calls: fill=%d stroke=%d gradients=%d clears=%d',
            calls.fill, calls.stroke, calls.grad, calls.clear);
els.slice(3).forEach(function (e) {
  console.log('cover role %s vars: %j', e.getAttribute('data-neb-role'), e.style.props);
});
// A theme flip must repaint without throwing.
var before = calls.fill;
(listeners['neb:theme-change'] || []).forEach(function (f) { f(); });
console.log('repaint on theme change added %d fills', calls.fill - before);
// A zero-size host must not throw. It falls back to the API default size and
// paints an invisible canvas; the ResizeObserver repaints it once it has a box.
var zero = new El({ 'data-neb-art': 'banner', 'data-neb-subject': 'Physics' }, 0, 0);
NebArt.scan({ querySelectorAll: function () { return [zero]; } });
console.log('zero-size host survived:', zero.children.length === 1 ? 'yes' : 'no');
console.log('public API:', Object.keys(NebArt).join(' '));
