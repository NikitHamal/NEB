// A vernier caliper at true size (1 unit = 10 cm), lying face up: a stainless beam with a main
// scale in millimetres, a fixed jaw, and a slider carrying the moving jaw, a thumb wheel and a
// vernier plate of 10 divisions over 9 mm (least count 0.1 mm). The slider sits at the jaw gap
// plus the instrument's zero error, so a caliper that does not read zero when closed reads every
// object wrong by the same amount, as a real worn one does.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';

const MM = 0.01;
const PX = 32;
const SPAN0 = -2; const SPAN1 = 158;
const TOP = 0.035;

function mainScaleTex() {
  const w = (SPAN1 - SPAN0) * PX; const h = 360;
  return canvasTexture('ho-cal-main', w, h, (g) => {
    g.fillStyle = '#e7ebef'; g.fillRect(0, 0, w, h);
    const grd = g.createLinearGradient(0, 0, 0, h); grd.addColorStop(0, 'rgba(255,255,255,.25)'); grd.addColorStop(1, 'rgba(120,130,140,.18)'); g.fillStyle = grd; g.fillRect(0, 0, w, h);
    g.fillStyle = '#0b0f14';
    for (let mm = 0; mm <= 150; mm++) {
      const x = (mm - SPAN0) * PX; const cm = mm % 10 === 0; const half = mm % 5 === 0;
      const len = cm ? 150 : half ? 110 : 78;
      g.fillRect(Math.round(x - (cm ? 2.5 : 1.6)), h - len, cm ? 5 : 3.2, len);
      if (cm) { g.font = '700 70px system-ui, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'alphabetic'; g.fillText(String(mm / 10), x, h - 172); }
    }
    g.font = '700 46px system-ui, sans-serif'; g.textAlign = 'left'; g.fillText('cm', (151 - SPAN0) * PX, h - 172);
    g.font = '600 34px system-ui, sans-serif'; g.fillStyle = '#334155'; g.fillText('0.1 mm  · STAINLESS HARDENED', (20 - SPAN0) * PX, 60);
  }, { anisotropy: 16 });
}
function vernierTex() {
  const w = 14 * 64; const h = 220;
  return canvasTexture('ho-cal-vernier', w, h, (g) => {
    g.fillStyle = '#d9dee3'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#0b0f14';
    for (let i = 0; i <= 10; i++) {
      const x = (1 + i * 0.9) * 64; const big = i % 5 === 0;
      const len = big ? 110 : 76;
      g.fillRect(Math.round(x - 1.6), 0, 3.2, len);
      if (i % 2 === 0) { g.font = '700 46px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(i), x, 168); }
    }
    g.font = '600 26px system-ui, sans-serif'; g.textAlign = 'left'; g.fillStyle = '#475569'; g.fillText('1/10 mm', 11.2 * 64, 200);
  }, { anisotropy: 16 });
}

export function caliper({ zeroErrMm = 0 } = {}) {
  const g = new THREE.Group();
  const steel = MAT.steel(); const satin = MAT.brushed();
  // beam
  g.add(mesh(new THREE.BoxGeometry(1.86, TOP, 0.16), satin, [0.68, TOP / 2, 0]));
  const face = new THREE.Mesh(new THREE.PlaneGeometry((SPAN1 - SPAN0) * MM, 0.115), new THREE.MeshStandardMaterial({ map: mainScaleTex(), metalness: 0.35, roughness: 0.38 }));
  face.rotation.x = -Math.PI / 2; face.position.set((SPAN0 + SPAN1) / 2 * MM, TOP + 0.0006, -0.0225); g.add(face);
  // fixed jaw (outside, measuring along +z) and the small inside jaw (-z)
  const jawShape = (len) => { const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(0, len); s.lineTo(-0.025, len - 0.012); s.lineTo(-0.06, 0.12); s.lineTo(-0.075, 0); s.lineTo(0, 0); return s; };
  const jawGeo = new THREE.ExtrudeGeometry(jawShape(0.42), { depth: TOP, bevelEnabled: false }); jawGeo.rotateX(Math.PI / 2); jawGeo.translate(0, TOP, 0);
  const fixed = mesh(jawGeo, satin); fixed.position.set(0, 0, 0.07); g.add(fixed);
  const inGeo = new THREE.ExtrudeGeometry(jawShape(0.14), { depth: TOP * 0.8, bevelEnabled: false }); inGeo.rotateX(-Math.PI / 2); inGeo.translate(0, 0, 0);
  const fixedIn = mesh(inGeo, satin); fixedIn.position.set(0, 0.004, -0.07); g.add(fixedIn);
  // slider
  const slider = new THREE.Group(); g.add(slider);
  slider.add(mesh(new THREE.BoxGeometry(0.46, 0.012, 0.03), steel, [0.23, TOP + 0.006, -0.085]));
  slider.add(mesh(new THREE.BoxGeometry(0.46, 0.022, 0.05), steel, [0.23, TOP + 0.011, 0.077]));
  slider.add(mesh(new THREE.BoxGeometry(0.46, 0.05, 0.02), steel, [0.23, TOP / 2, 0.092]));
  slider.add(mesh(new THREE.BoxGeometry(0.46, 0.05, 0.02), steel, [0.23, TOP / 2, -0.092]));
  const vPlate = new THREE.Mesh(new THREE.PlaneGeometry(14 * MM, 0.047), new THREE.MeshStandardMaterial({ map: vernierTex(), metalness: 0.3, roughness: 0.35 }));
  vPlate.rotation.x = -Math.PI / 2; vPlate.position.set(6 * MM, TOP + 0.0225, 0.0585); slider.add(vPlate);
  const bevel = mesh(new THREE.BoxGeometry(0.14, 0.006, 0.006), steel, [0.06, TOP + 0.02, 0.035]); slider.add(bevel);
  const moving = mesh(jawGeo, satin); moving.scale.x = -1; moving.position.set(0, 0, 0.07); slider.add(moving);
  const movingIn = mesh(inGeo, satin); movingIn.scale.x = -1; movingIn.position.set(0, 0.004, -0.07); slider.add(movingIn);
  const wheel = mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.022, 24), MAT.matte(0x52606d), [0.33, TOP / 2, 0.118]); wheel.rotation.x = Math.PI / 2; slider.add(wheel);
  for (let i = 0; i < 16; i++) { const k = mesh(new THREE.BoxGeometry(0.004, 0.005, 0.024), MAT.matte(0x3b4650)); const a = i / 16 * Math.PI * 2; k.position.set(Math.cos(a) * 0.031, Math.sin(a) * 0.031, 0); k.rotation.z = a; wheel.add(k); }
  const screw = mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.03, 16), MAT.matte(0x52606d), [0.4, TOP + 0.035, 0.005]); slider.add(screw);
  const depth = mesh(new THREE.BoxGeometry(1, 0.008, 0.012), steel, [0, TOP / 2, 0]); g.add(depth);
  let gapMm = 0;
  const api = {
    group: g, slider, wheel, face, vPlate, zeroErrMm,
    get gap() { return gapMm; },
    /** Jaw gap in mm; the slider (and its vernier zero) sits at gap + zero error. */
    setGap(mm) {
      gapMm = Math.max(0, Math.min(140, mm));
      const x = (gapMm + zeroErrMm) * MM;
      slider.position.x = x; moving.position.x = -zeroErrMm * MM; movingIn.position.x = -zeroErrMm * MM;
      wheel.rotation.y = -gapMm * 0.6;
      depth.scale.x = Math.max(0.001, gapMm * MM); depth.position.x = 1.6 - 0.02 + depth.scale.x / 2 - 0.02;
    },
    /** The reading the scales show (mm), i.e. the position of the vernier zero. */
    get reading() { return gapMm + zeroErrMm; },
    vernierZeroX() { return slider.position.x; },
    mmAtX(x) { return x / MM; },
    TOP, MM,
  };
  api.setGap(0);
  return api;
}
