// Flames and light for the hands-on practicals. A Bunsen flame is two shaded cones whose opacity
// follows how much flame a ray passes through (dense at the core, fading at the silhouette and
// toward the tip) and that flicker with layered sine noise in the vertex shader. Flame-test
// colours are not picked from a table: each metal's visible emission lines (nm, relative
// intensity) are converted to RGB and summed, so a cobalt-blue glass can filter them line by
// line, and the same lines draw the spectrum in a hand spectroscope.
import { THREE } from '../engine.js';

export const LINES = {
  Na: { name: 'Sodium', ion: 'Na⁺', lines: [[589.0, 1], [589.6, 0.5]], colour: 'golden yellow, persistent' },
  K: { name: 'Potassium', ion: 'K⁺', lines: [[766.5, 0.9], [769.9, 0.45], [404.4, 0.35], [404.7, 0.2]], colour: 'lilac (crimson through cobalt glass)' },
  Li: { name: 'Lithium', ion: 'Li⁺', lines: [[670.8, 1], [610.4, 0.08]], colour: 'crimson red' },
  Ca: { name: 'Calcium', ion: 'Ca²⁺', lines: [[622, 1], [618, 0.6], [554, 0.45], [602, 0.3]], colour: 'brick red' },
  Sr: { name: 'Strontium', ion: 'Sr²⁺', lines: [[606, 0.45], [636, 0.7], [662, 0.9], [674, 0.7], [460.7, 0.25]], colour: 'crimson' },
  Ba: { name: 'Barium', ion: 'Ba²⁺', lines: [[513.7, 0.8], [524.3, 1], [553.5, 0.5], [487, 0.2]], colour: 'apple green' },
  Cu: { name: 'Copper', ion: 'Cu²⁺', lines: [[427, 0.5], [435, 0.6], [452, 0.45], [479, 0.5], [488, 0.35], [510.5, 0.6], [515.3, 0.45], [521.8, 0.55]], colour: 'blue-green' },
};

/** Approximate linear RGB of monochromatic light (Bruton), with the eye's falloff at the ends. */
export function wavelengthRGB(nm, out = [0, 0, 0]) {
  let r = 0, g = 0, b = 0;
  if (nm >= 380 && nm < 440) { r = -(nm - 440) / 60; b = 1; }
  else if (nm < 490) { g = (nm - 440) / 50; b = 1; }
  else if (nm < 510) { g = 1; b = -(nm - 510) / 20; }
  else if (nm < 580) { r = (nm - 510) / 70; g = 1; }
  else if (nm < 645) { r = 1; g = -(nm - 645) / 65; }
  else if (nm <= 780) { r = 1; }
  let f = 0;
  if (nm >= 380 && nm < 420) f = 0.3 + 0.7 * (nm - 380) / 40;
  else if (nm < 701) f = 1;
  else if (nm <= 780) f = 0.3 + 0.7 * (780 - nm) / 80;
  out[0] = r * f; out[1] = g * f; out[2] = b * f;
  return out;
}

/** Transmission of a cobalt-blue glass: passes violet-blue and deep red, absorbs yellow. */
export function cobaltT(nm) {
  if (nm < 500) return 0.85; if (nm < 560) return 0.12; if (nm < 640) return 0.02; if (nm < 700) return 0.3; return 0.75;
}

const tmpRGB = [0, 0, 0];
/** Colour of a mix of emitters { Na: amount, ... }; returns brightness 0..1 and sets out. */
export function emissionColour(mix, out, { cobalt = false } = {}) {
  let r = 0, g = 0, b = 0; let total = 0;
  for (const k in mix) {
    const a = mix[k]; if (!(a > 0) || !LINES[k]) continue;
    for (const [nm, w] of LINES[k].lines) {
      const t = cobalt ? cobaltT(nm) : 1;
      wavelengthRGB(nm, tmpRGB);
      r += tmpRGB[0] * w * a * t; g += tmpRGB[1] * w * a * t; b += tmpRGB[2] * w * a * t; total += w * a * t;
    }
  }
  const m = Math.max(r, g, b);
  if (m <= 1e-6) { out.setRGB(0, 0, 0); return 0; }
  out.setRGB(r / m, g / m, b / m);
  return Math.min(1, total);
}

/** Approximate colour of a glowing wire at T (deg C): dull red near 550, orange 900, yellow-white 1200. */
export function glowColour(tC, out) {
  if (tC < 480) return out.setRGB(0, 0, 0);
  const k = Math.min(1, (tC - 480) / 800);
  return out.setRGB(0.55 + 0.45 * Math.min(1, k * 2), 0.04 + 0.6 * k * k, 0.02 + 0.25 * k * k * k).multiplyScalar(0.4 + 1.6 * k);
}

const VERT = `
uniform float uTime; uniform float uWobble; uniform float uSeed;
varying vec3 vN; varying vec3 vV; varying float vH;
void main() {
  vec3 p = position;
  float h = clamp(p.y / uHeight, 0.0, 1.0);
  float n = sin(uTime * 11.0 + p.y * 18.0 + uSeed) * 0.6 + sin(uTime * 23.0 - p.y * 31.0 + uSeed * 2.0) * 0.4;
  p.x += n * uWobble * h * h;
  p.z += cos(uTime * 13.0 + p.y * 21.0 + uSeed) * uWobble * 0.7 * h * h;
  p.xz *= 1.0 + 0.06 * sin(uTime * 17.0 + uSeed) * h;
  vH = h;
  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz);
  gl_Position = projectionMatrix * mv;
}`;
const FRAG = `
uniform vec3 uColor; uniform vec3 uTip; uniform float uAlpha;
varying vec3 vN; varying vec3 vV; varying float vH;
void main() {
  float f = abs(dot(normalize(vN), normalize(vV)));
  float body = pow(f, 1.6) * smoothstep(1.0, 0.55, vH) * smoothstep(0.0, 0.06, vH);
  vec3 c = mix(uColor, uTip, smoothstep(0.35, 1.0, vH));
  gl_FragColor = vec4(c, uAlpha * body);
}`;

export function flameMaterial({ color = 0x3b82f6, tip = color, alpha = 0.6, height = 1, wobble = 0.02, seed = 0 } = {}) {
  return new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uColor: { value: new THREE.Color(color) }, uTip: { value: new THREE.Color(tip) }, uAlpha: { value: alpha }, uWobble: { value: wobble }, uSeed: { value: seed }, uHeight: { value: height } },
    vertexShader: `uniform float uHeight;\n${VERT}`, fragmentShader: FRAG, transparent: true, depthWrite: false, side: THREE.DoubleSide,
  });
}

/** A rounded flame body (a lathe), base at y = 0, tip at y = h. */
export function flameGeometry(r, h, seg = 24) {
  const pts = [];
  for (let i = 0; i <= 14; i++) { const t = i / 14; const y = t * h; const rr = r * Math.sin(Math.min(1, t * 3.2) * Math.PI / 2) * Math.pow(1 - t, 0.85); pts.push(new THREE.Vector2(Math.max(0.0005, rr), y)); }
  return new THREE.LatheGeometry(pts, seg);
}

/** Draws the spectrum of a mix as a hand spectroscope shows it, 400-700 nm. */
export function drawSpectrum(canvas, mix, glow = 0) {
  const g = canvas.getContext('2d'); const W = canvas.width; const H = canvas.height;
  g.fillStyle = '#05060a'; g.fillRect(0, 0, W, H);
  const x = (nm) => 16 + (W - 32) * (nm - 400) / 300;
  const top = 10; const bh = H - 40;
  if (glow > 0) {
    for (let nm = 400; nm <= 700; nm += 2) { wavelengthRGB(nm, tmpRGB); const w = Math.min(1, glow * Math.pow((nm - 380) / 320, 3)); g.fillStyle = `rgba(${tmpRGB[0] * 255 | 0},${tmpRGB[1] * 255 | 0},${tmpRGB[2] * 255 | 0},${w * 0.5})`; g.fillRect(x(nm), top, x(nm + 2) - x(nm) + 0.5, bh); }
  }
  g.globalCompositeOperation = 'lighter';
  for (const k in mix) {
    const a = mix[k]; if (!(a > 0.01) || !LINES[k]) continue;
    for (const [nm, w] of LINES[k].lines) {
      if (nm < 400 || nm > 700) continue;
      wavelengthRGB(nm, tmpRGB); const I = Math.min(1, w * a * 1.4);
      const cx = x(nm);
      const grd = g.createLinearGradient(cx - 4, 0, cx + 4, 0);
      const col = `${tmpRGB[0] * 255 | 0},${tmpRGB[1] * 255 | 0},${tmpRGB[2] * 255 | 0}`;
      grd.addColorStop(0, `rgba(${col},0)`); grd.addColorStop(0.5, `rgba(${col},${I})`); grd.addColorStop(1, `rgba(${col},0)`);
      g.fillStyle = grd; g.fillRect(cx - 4, top, 8, bh);
      g.fillStyle = `rgba(255,255,255,${I * 0.35})`; g.fillRect(cx - 0.6, top, 1.2, bh);
    }
  }
  g.globalCompositeOperation = 'source-over';
  g.fillStyle = '#94a3b8'; g.font = '600 11px system-ui, sans-serif'; g.textAlign = 'center';
  for (let nm = 400; nm <= 700; nm += 50) { g.fillRect(x(nm) - 0.5, H - 28, 1, 8); g.fillText(String(nm), x(nm), H - 8); }
  for (let nm = 410; nm < 700; nm += 10) g.fillRect(x(nm) - 0.5, H - 28, 1, 4);
}
