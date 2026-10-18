// A micrometer screw gauge at true size (1 unit = 10 cm): a lacquered U-frame with a heat
// insulating grip, the anvil, the spindle, a sleeve printed with a millimetre scale above the
// datum line and half millimetres below it, and a thimble of 50 divisions that turns 360 degrees
// per 0.5 mm pitch (least count 0.01 mm), with the ratchet at its end. The spindle face sits at
// the gap; the thimble reads gap + zero error, as a gauge that does not read zero when closed does.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';

const MM = 0.01;
export const PITCH = 0.5;
export const DIVS = 50;
const R_SLEEVE = 0.032; const R_THIMBLE = 0.042;
const S0 = 0.14;

function sleeveTex() {
  return canvasTexture('ho-mic-sleeve', 2048, 256, (g, w, h) => {
    g.fillStyle = '#e9edf1'; g.fillRect(0, 0, w, h);
    const px = w / 28; const x = (mm) => 40 + mm * px; const mid = h / 2;
    g.fillStyle = '#0b0f14'; g.fillRect(0, mid - 2, w, 4);
    for (let i = 0; i <= 26; i++) {
      const big = i % 5 === 0;
      g.fillRect(Math.round(x(i) - 2), mid - (big ? 70 : 52), 4, big ? 70 : 52);
      if (big) { g.font = '700 54px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(String(i), x(i), mid - 84); }
      if (i < 26) g.fillRect(Math.round(x(i + 0.5) - 2), mid, 4, 46);
    }
    g.font = '600 30px system-ui, sans-serif'; g.textAlign = 'left'; g.fillStyle = '#334155'; g.fillText('0–25 mm   0.01 mm', x(14), h - 30);
  }, { anisotropy: 16 });
}
function thimbleTex() {
  // one canvas pixel is 0.065 mm round the thimble but 0.625 mm along it, so marks are a few
  // pixels long and the numbers are drawn squeezed ten times along the axis to come out square
  return canvasTexture('ho-mic-thimble', 4096, 256, (g, w, h) => {
    g.fillStyle = '#d7dde3'; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 3) { g.fillStyle = `rgba(255,255,255,${0.04 + (y % 9 === 0 ? 0.05 : 0)})`; g.fillRect(0, y, w, 1); }
    g.fillStyle = '#0b0f14';
    for (let d = 0; d < DIVS; d++) {
      const xx = (((DIVS - d) % DIVS) / DIVS) * w; const big = d % 5 === 0;
      g.fillRect(Math.round(xx - 3), 0, 6, big ? 9 : 6);
      if (big) { g.save(); g.translate(xx, 15); g.scale(1, 0.16); g.rotate(Math.PI / 2); g.font = '700 58px system-ui, sans-serif'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText(String(d), 0, 0); g.restore(); }
    }
    g.fillRect(0, 0, 4, 9); g.fillRect(w - 4, 0, 4, 9);
  }, { anisotropy: 16 });
}

export function micrometer({ zeroErrMm = 0 } = {}) {
  const g = new THREE.Group();
  const lacquer = new THREE.MeshPhysicalMaterial({ color: 0x7c8a99, roughness: 0.32, metalness: 0.5, clearcoat: 0.6 });
  const insulator = MAT.gloss(0x8a1c1c);
  // the C-frame: a half ring under the gauge from the anvil boss to the sleeve boss
  const arc = mesh(new THREE.TorusGeometry(0.125, 0.024, 14, 48, Math.PI), lacquer, [-0.015, 0, 0]); arc.rotation.z = Math.PI; arc.scale.set(1, 1.1, 0.8); g.add(arc);
  const grip = mesh(new THREE.TorusGeometry(0.125, 0.029, 14, 28, Math.PI * 0.5), insulator, [-0.015, 0, 0]); grip.rotation.z = Math.PI * 1.25; grip.scale.set(1, 1.1, 1.0); g.add(grip);
  const anvilBoss = mesh(new THREE.CylinderGeometry(0.034, 0.034, 0.06, 24), lacquer, [-0.14, 0, 0]); anvilBoss.rotation.z = Math.PI / 2; g.add(anvilBoss);
  const anvil = mesh(new THREE.CylinderGeometry(0.0125, 0.0125, 0.06, 20), MAT.steel(), [-0.08, 0, 0]); anvil.rotation.z = Math.PI / 2; g.add(anvil);
  const boss = mesh(new THREE.CylinderGeometry(0.036, 0.036, 0.05, 24), lacquer, [0.11, 0, 0]); boss.rotation.z = Math.PI / 2; g.add(boss);
  const lock = mesh(new THREE.CylinderGeometry(0.012, 0.014, 0.03, 12), MAT.steel(), [0.11, 0.045, 0]); g.add(lock);
  const sleeve = mesh(new THREE.CylinderGeometry(R_SLEEVE, R_SLEEVE, 0.3, 32), MAT.brushed(), [S0 + 0.12, 0, 0]); sleeve.rotation.z = Math.PI / 2; g.add(sleeve);
  const strip = new THREE.Mesh(new THREE.PlaneGeometry(28 * MM, 0.026), new THREE.MeshStandardMaterial({ map: sleeveTex(), metalness: 0.3, roughness: 0.4 }));
  // the strip is 28 mm long: 40 px of margin then 1 mm per w/28 px, so its 0 mark sits at S0
  strip.position.set(S0 - (40 / 2048) * 28 * MM + 14 * MM, 0, R_SLEEVE + 0.0006); g.add(strip);
  const spindle = mesh(new THREE.CylinderGeometry(0.0125, 0.0125, 0.3, 20), MAT.steel(), [0, 0, 0]); spindle.rotation.z = Math.PI / 2; g.add(spindle);
  const thimble = new THREE.Group(); g.add(thimble);
  const tMat = new THREE.MeshStandardMaterial({ map: thimbleTex(), metalness: 0.55, roughness: 0.35 });
  const shell = new THREE.Mesh(new THREE.CylinderGeometry(R_THIMBLE, R_THIMBLE, 0.16, 64, 1, true), tMat); shell.rotation.z = Math.PI / 2; shell.position.x = 0.092;
  thimble.add(shell);
  const bevel = mesh(new THREE.CylinderGeometry(R_THIMBLE, R_SLEEVE + 0.001, 0.012, 64, 1, true), MAT.brushed(), [0.006, 0, 0]); bevel.rotation.z = Math.PI / 2; thimble.add(bevel);
  const knurl = mesh(new THREE.CylinderGeometry(R_THIMBLE + 0.003, R_THIMBLE + 0.003, 0.07, 40), MAT.matte(0x4b5563), [0.21, 0, 0]); knurl.rotation.z = -Math.PI / 2; thimble.add(knurl);
  const ratchet = new THREE.Group(); ratchet.position.x = 0.27; thimble.add(ratchet);
  const rr = mesh(new THREE.CylinderGeometry(0.026, 0.026, 0.06, 24), MAT.matte(0x374151)); rr.rotation.z = -Math.PI / 2; ratchet.add(rr);
  const cap = mesh(new THREE.CylinderGeometry(0.02, 0.026, 0.012, 24), MAT.steel(), [0.036, 0, 0]); cap.rotation.z = -Math.PI / 2; ratchet.add(cap);
  let gap = 0;
  const api = {
    group: g, thimble, shell, ratchet: rr, strip, zeroErrMm, S0,
    get gap() { return gap; },
    get reading() { return gap + zeroErrMm; },
    setGap(mm) {
      gap = Math.max(0, Math.min(25, mm));
      const r = gap + zeroErrMm;
      spindle.position.x = (-0.05 + gap * MM) + 0.15;
      thimble.position.x = S0 + r * MM;
      thimble.rotation.x = -(r / PITCH) * Math.PI * 2;
    },
    /** Spindle face x for the jaw gap: the anvil face is at x = -0.05. */
    faceX() { return -0.05 + gap * MM; },
    /** The thimble division (0..49) on a hit's uv. */
    divisionAt(uv) { return ((Math.round((1 - uv.x) * DIVS) % DIVS) + DIVS) % DIVS; },
    MM,
  };
  api.setGap(0);
  return api;
}
