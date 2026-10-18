// An onion bulb grown over water for a few days, lifted out and laid on its side on a tile with
// its fresh white adventitious roots fanned out (about 1 mm thick, 3-4 cm long, creamy at the
// tip where the meristem is). Each root is two pieces either side of a cut line 1.2 cm from
// its tip, so a stroke of the blade can cut the tip free. 1 unit = 10 cm.
import { THREE } from '../../engine.js';
import { wet, mesh, canvasTexture, rng } from '../kit.js';

function skinTexture() {
  return canvasTexture('onion-skin', 512, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, 0);
    gr.addColorStop(0, '#8a4a22'); gr.addColorStop(0.5, '#b06a35'); gr.addColorStop(1, '#7a3c1b');
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    const R = rng(5);
    for (let i = 0; i < 160; i++) { g.strokeStyle = `rgba(${60 + R() * 60 | 0},${25 + R() * 30 | 0},10,${0.25 + R() * 0.3})`; g.lineWidth = 0.6 + R() * 1.4; const y = R() * h; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + (R() - 0.5) * 12, w * 0.6, y + (R() - 0.5) * 12, w, y + (R() - 0.5) * 8); g.stroke(); }
    for (let i = 0; i < 30; i++) { g.fillStyle = `rgba(230,190,140,${0.12 + R() * 0.15})`; g.fillRect(R() * w, R() * h, 20 + R() * 60, 2 + R() * 4); }
  }, { wrapS: true });
}

export function buildOnion(quality) {
  const root = new THREE.Group(); root.name = 'onion';
  const seg = quality.tier === 'low' ? 24 : 40;
  // bulb profile, base (basal plate) at y=0 up to the neck
  const prof = [[0.0, 0], [0.08, 0.005], [0.17, 0.04], [0.25, 0.12], [0.285, 0.22], [0.27, 0.32], [0.21, 0.42], [0.12, 0.5], [0.05, 0.56], [0.03, 0.62], [0.015, 0.68], [0, 0.69]];
  const bulb = mesh(new THREE.LatheGeometry(prof.map(([r, y]) => new THREE.Vector2(r, y)), seg), new THREE.MeshPhysicalMaterial({ map: skinTexture(), roughness: 0.55, clearcoat: 0.4, clearcoatRoughness: 0.4, sheen: 0.5, sheenColor: new THREE.Color(0xffd6a0) }));
  const plate = mesh(new THREE.CylinderGeometry(0.075, 0.09, 0.03, 24), new THREE.MeshStandardMaterial({ color: 0xcdb48a, roughness: 0.9 }), [0, 0.0, 0]);
  const body = new THREE.Group(); body.add(bulb, plate);
  // lying on its side: the bulb's axis along -x, basal plate toward +x
  body.rotation.z = Math.PI / 2; body.position.set(0, 0.285, 0);
  root.add(body);

  const R = rng(9);
  const rootMat = wet(0xf3efe4, { roughness: 0.35, clearcoat: 0.8, sheen: 0.4, sheenColor: 0xffffff });
  const tipMat = wet(0xeedfae, { roughness: 0.32, clearcoat: 0.8 });
  const roots = [];
  const N = 9; const rr = 0.0055; const CUT = 0.12;
  for (let i = 0; i < N; i++) {
    const a = (i / (N - 1) - 0.5) * 1.15 + (R() - 0.5) * 0.1;
    const len = 0.3 + R() * 0.1;
    const y0 = 0.285 + (R() - 0.5) * 0.06; const z0 = (R() - 0.5) * 0.06;
    const pts = [];
    for (let k = 0; k <= 14; k++) {
      const f = k / 14; const d = f * len;
      const drop = Math.min(1, f * 3.2);
      pts.push(new THREE.Vector3(0.02 + Math.cos(a) * d + Math.sin(f * 7 + i) * 0.006, y0 * (1 - drop) + rr * drop, z0 + Math.sin(a) * d * 1.05));
    }
    const curve = new THREE.CatmullRomCurve3(pts);
    const L = curve.getLength(); const cutT = 1 - CUT / L;
    const basePts = []; const tipPts = [];
    for (let k = 0; k <= 24; k++) basePts.push(curve.getPointAt((k / 24) * cutT));
    for (let k = 0; k <= 10; k++) tipPts.push(curve.getPointAt(cutT + (k / 10) * (1 - cutT)));
    const base = mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(basePts), 40, rr, 8), rootMat);
    const tipGroup = new THREE.Group();
    const tipCenter = tipPts[5].clone();
    tipPts.forEach((p) => p.sub(tipCenter));
    const tipTube = mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(tipPts), 16, rr, 8), tipMat.clone());
    const cap = mesh(new THREE.SphereGeometry(rr, 10, 8), tipTube.material, tipPts[10]);
    tipGroup.add(tipTube, cap); tipGroup.position.copy(tipCenter);
    root.add(base, tipGroup);
    roots.push({ base, tip: tipGroup, tipMat: tipTube.material, curve, cutT, cutPoint: curve.getPointAt(cutT), tipEnd: curve.getPointAt(1), cut: false, len: L });
  }
  return { root, roots, rootRadius: rr, cutLength: CUT };
}
