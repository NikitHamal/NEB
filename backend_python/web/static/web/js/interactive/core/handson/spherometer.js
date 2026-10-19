// A spherometer at true size (1 unit = 10 cm): a three-armed frame on three pointed legs at the
// corners of an equilateral triangle, a central screw of pitch 1 mm through the hub, a disc of
// 100 divisions on top of the screw (least count 0.01 mm), and a vertical pitch scale beside the
// disc rim whose edge is the index for the disc. The screw's reading r (mm) is the height of the
// disc's upper face on the pitch scale; the tip stands r - r0 mm above the plane of the legs.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';

export const MM = 0.01;
const DISC_R = 0.24; const HUB_Y = 0.2; const Z0 = 0.26; const SCALE_X = DISC_R + 0.002;

function discTex() {
  return canvasTexture('ho-sph-disc', 512, 512, (g, w, h) => {
    const c = w / 2; const R = w / 2 - 2;
    const grd = g.createRadialGradient(c, c, R * 0.2, c, c, R); grd.addColorStop(0, '#e3e8ec'); grd.addColorStop(1, '#bcc5cd');
    g.fillStyle = grd; g.beginPath(); g.arc(c, c, R, 0, Math.PI * 2); g.fill();
    g.strokeStyle = 'rgba(255,255,255,.22)'; for (let r = 20; r < R; r += 3) { g.beginPath(); g.arc(c, c, r, 0, Math.PI * 2); g.stroke(); }
    g.fillStyle = '#334155'; g.font = '700 22px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText('PITCH 1 mm   L.C. 0.01 mm', c, c + 120);
  });
}

function rimTex() {
  // graduations on the bevelled rim: division d sits at u = 1 - d/100, so it faces the front when
  // the disc has turned 2πd/100 anticlockwise (seen from above), i.e. the screw has risen d/100 mm
  return canvasTexture('ho-sph-rim', 8192, 192, (g, w, h) => {
    g.fillStyle = '#d5dbe1'; g.fillRect(0, 0, w, h); g.fillStyle = '#0b0f14';
    for (let d = 0; d < 100; d++) {
      const x = ((100 - d) % 100) / 100 * w; const big = d % 10 === 0; const mid = d % 5 === 0;
      const len = big ? 96 : mid ? 70 : 46;
      g.fillRect(Math.round(x - 4), 0, 8, len);
      if (big) { g.font = '800 72px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(d), x, 172); if (d === 0) g.fillText('0', x + w, 172); }
    }
    g.fillRect(w - 4, 0, 4, 96);
  }, { anisotropy: 16 });
}

function pitchTex() {
  return canvasTexture('ho-sph-pitch', 128, 1024, (g, w, h) => {
    g.fillStyle = '#eef1f4'; g.fillRect(0, 0, w, h);
    const y = (mm) => h - 40 - (h - 80) * mm / 12;
    g.fillStyle = '#0b0f14';
    for (let mm = 0; mm <= 12; mm++) {
      const big = mm % 5 === 0;
      g.fillRect(0, Math.round(y(mm) - 2), big ? 70 : 48, 4);
      g.font = '800 30px system-ui, sans-serif'; g.textBaseline = 'middle'; g.fillText(String(mm), big ? 76 : 56, y(mm));
    }
    g.fillRect(0, 0, 5, h);
  }, { anisotropy: 16 });
}

/** The instrument. r0: the reading at which the tip is level with the legs (mm). */
export function spherometer({ l = 0.45, r0 = 4.5 } = {}) {
  const g = new THREE.Group();
  const rho = l / Math.sqrt(3);
  const steel = MAT.steel(); const dark = MAT.gloss(0x2b2f36);
  const legs = [];
  for (let i = 0; i < 3; i++) {
    const a = -Math.PI / 2 + i * Math.PI * 2 / 3;
    const x = Math.cos(a) * rho; const z = Math.sin(a) * rho;
    const arm = mesh(new THREE.BoxGeometry(rho, 0.018, 0.028), dark, [x / 2, HUB_Y, z / 2]); arm.rotation.y = -a; g.add(arm);
    const leg = new THREE.Group(); leg.position.set(x, 0, z);
    leg.add(mesh(new THREE.CylinderGeometry(0.008, 0.008, HUB_Y - 0.02, 12), steel, [0, HUB_Y / 2 + 0.01, 0]));
    leg.add(mesh(new THREE.ConeGeometry(0.008, 0.02, 12), steel, [0, 0.01, 0]).rotateX(Math.PI));
    g.add(leg); legs.push(leg);
  }
  g.add(mesh(new THREE.CylinderGeometry(0.045, 0.05, 0.05, 24), dark, [0, HUB_Y, 0]));
  const HS = 0.12 * 1024 / 944;
  const yc = Z0 - HS * 40 / 1024 + HS / 2;
  const scale = mesh(new THREE.PlaneGeometry(0.026, HS), new THREE.MeshStandardMaterial({ map: pitchTex(), roughness: 0.5, metalness: 0.2 }), [-0.0031, yc, SCALE_X + 0.011]);
  scale.rotation.y = -Math.PI / 2; g.add(scale);
  g.add(mesh(new THREE.BoxGeometry(0.004, HS, 0.028), dark, [0, yc, SCALE_X + 0.011]));
  g.add(mesh(new THREE.BoxGeometry(0.02, Z0 - HUB_Y, 0.02), dark, [0.008, (HUB_Y + Z0) / 2 - 0.02, SCALE_X + 0.014]));
  g.add(mesh(new THREE.BoxGeometry(0.02, 0.016, SCALE_X), dark, [0.008, HUB_Y, SCALE_X / 2 + 0.01]));
  const screw = new THREE.Group(); g.add(screw);
  const LEN = Z0 + r0 * MM;
  const thread = canvasTexture('ho-sph-thread', 64, 512, (c, w, h) => { c.fillStyle = '#9aa4ae'; c.fillRect(0, 0, w, h); c.fillStyle = '#e8edf1'; for (let y = 0; y < h; y += 8) c.fillRect(0, y, w, 3); });
  screw.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, LEN - 0.03, 16), new THREE.MeshStandardMaterial({ map: thread, metalness: 0.85, roughness: 0.3 }), [0, (LEN - 0.03) / 2 + 0.03, 0]));
  const tip = mesh(new THREE.ConeGeometry(0.012, 0.03, 16), steel, [0, 0.015, 0]); tip.rotation.x = Math.PI; screw.add(tip);
  const disc = mesh(new THREE.CylinderGeometry(DISC_R, DISC_R, 0.03, 96), [new THREE.MeshStandardMaterial({ map: rimTex(), metalness: 0.3, roughness: 0.45 }), new THREE.MeshStandardMaterial({ map: discTex(), metalness: 0.5, roughness: 0.35 }), new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.9, roughness: 0.4 })], [0, LEN - 0.015, 0]);
  disc.castShadow = true; screw.add(disc);
  const knob = mesh(new THREE.CylinderGeometry(0.03, 0.035, 0.05, 20), MAT.gloss(0x111827), [0, LEN + 0.025, 0]); screw.add(knob);
  const refl = mesh(new THREE.ConeGeometry(0.012, 0.03, 16), new THREE.MeshStandardMaterial({ color: 0xb8c2cc, metalness: 1, roughness: 0.15, transparent: true, opacity: 0.55 }), [0, -0.015, 0]);
  refl.userData.noPick = true; g.add(refl);
  let r = r0;
  return {
    group: g, screw, disc, scale, tip, refl, legs, rho, r0, DISC_R, Z0, SCALE_X,
    get reading() { return r; },
    /** Sets the screw reading in mm; the disc turns one full revolution per millimetre. */
    set(v) {
      r = Math.max(0.2, Math.min(11.8, v));
      screw.position.y = (r - r0) * MM;
      disc.rotation.y = 2 * Math.PI * (r - Math.floor(r));
    },
    /** Tip height above the plane of the leg points, in mm. */
    tipMm() { return r - r0; },
    /** Mirror image of the tip in a surface `s` mm above the leg plane (at the centre). */
    setReflection(s) { refl.visible = s !== null; if (s !== null) refl.position.y = (2 * s - (r - r0)) * MM - 0.015; },
    /** Disc division at a local hit point on the disc. */
    divisionAt(local) { const u = Math.atan2(local.x, local.z) / (Math.PI * 2); return ((Math.round((1 - u) * 100) % 100) + 100) % 100; },
  };
}

/** A watch glass of radius of curvature R (units), convex side up, resting on its rim. */
export function watchGlassCap(R, aperture = 0.42) {
  const a = Math.asin(aperture / R); const pts = [];
  for (let i = 0; i <= 24; i++) { const t = a * i / 24; pts.push(new THREE.Vector2(Math.sin(t) * R, Math.cos(t) * R - Math.cos(a) * R)); }
  const geo = new THREE.LatheGeometry(pts.reverse(), 64);
  const m = mesh(geo, new THREE.MeshPhysicalMaterial({ color: 0xd8f1ff, roughness: 0.02, transparent: true, opacity: 0.38, clearcoat: 1, envMapIntensity: 2, depthWrite: false, side: THREE.DoubleSide }), null, { cast: false });
  m.renderOrder = 5;
  const top = R - Math.cos(a) * R;
  return { mesh: m, top, heightAt: (rr) => Math.sqrt(R * R - rr * rr) - Math.cos(a) * R };
}
