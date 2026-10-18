// Bench apparatus for the biology practicals, at true size (1 unit = 10 cm): a wax dissecting
// tray, glass slides and coverslips, watch glasses, reagent bottles with printed labels, a
// spirit lamp, filter paper and a wash bottle.
import { THREE } from '../engine.js';
import { MAT, mesh, roundedSlab, canvasTexture, wet } from './kit.js';

export function dissectingTray(w = 3.2, d = 2.0) {
  const g = new THREE.Group();
  const wall = 0.035; const h = 0.14;
  const tin = new THREE.MeshStandardMaterial({ color: 0xc7ced6, metalness: 0.85, roughness: 0.35 });
  g.add(mesh(roundedSlab(w, d, 0.012, 0.08), tin));
  g.add(mesh(new THREE.BoxGeometry(w, h, wall), tin, [0, h / 2, d / 2 - wall / 2]));
  g.add(mesh(new THREE.BoxGeometry(w, h, wall), tin, [0, h / 2, -d / 2 + wall / 2]));
  g.add(mesh(new THREE.BoxGeometry(wall, h, d), tin, [w / 2 - wall / 2, h / 2, 0]));
  g.add(mesh(new THREE.BoxGeometry(wall, h, d), tin, [-w / 2 + wall / 2, h / 2, 0]));
  const waxTex = canvasTexture('bh-wax', 512, 512, (c, W, H) => {
    c.fillStyle = '#2a221d'; c.fillRect(0, 0, W, H);
    for (let i = 0; i < 260; i++) { // old pin holes and knife scores
      c.fillStyle = `rgba(0,0,0,${0.25 + Math.random() * 0.3})`; c.beginPath(); c.arc(Math.random() * W, Math.random() * H, 1 + Math.random() * 1.6, 0, Math.PI * 2); c.fill();
    }
    c.strokeStyle = 'rgba(90,70,60,0.22)';
    for (let i = 0; i < 40; i++) { c.lineWidth = 1; c.beginPath(); const x = Math.random() * W; const y = Math.random() * H; c.moveTo(x, y); c.lineTo(x + (Math.random() - 0.5) * 120, y + (Math.random() - 0.5) * 40); c.stroke(); }
  });
  const wax = mesh(new THREE.BoxGeometry(w - wall * 2, 0.06, d - wall * 2), new THREE.MeshPhysicalMaterial({ map: waxTex, roughness: 0.6, clearcoat: 0.3, clearcoatRoughness: 0.5 }), [0, 0.042, 0], { name: 'wax' });
  g.add(wax);
  g.userData.wax = wax; g.userData.waxY = 0.072;
  return g;
}

export function slide(opts = {}) {
  const g = new THREE.Group();
  const s = mesh(new THREE.BoxGeometry(0.76, 0.012, 0.26), MAT.glassEdge(), [0, 0.006, 0], { cast: false });
  s.renderOrder = 3; g.add(s);
  if (opts.frosted !== false) {
    const f = mesh(new THREE.BoxGeometry(0.17, 0.0125, 0.255), new THREE.MeshStandardMaterial({ color: 0xf5f5f0, roughness: 0.9, transparent: true, opacity: 0.92 }), [-0.29, 0.0062, 0]);
    g.add(f);
  }
  g.userData.top = 0.012;
  return g;
}
export function coverslip() {
  const m = mesh(new THREE.BoxGeometry(0.22, 0.0018, 0.22), MAT.glass(), null, { cast: false });
  m.renderOrder = 4;
  return m;
}
/** A flat lens of liquid on a surface (a drop of stain or water). */
export function drop(color, opacity = 0.75) {
  const geo = new THREE.SphereGeometry(1, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2);
  const m = mesh(geo, MAT.liquid(color, opacity), null, { cast: false });
  m.scale.set(0.001, 0.001, 0.001); m.renderOrder = 4;
  return m;
}
export function watchGlass(color = null, opacity = 0.7) {
  const g = new THREE.Group();
  const pts = []; for (let i = 0; i <= 12; i++) { const a = (i / 12) * 0.9; pts.push(new THREE.Vector2(Math.sin(a) * 0.4, (1 - Math.cos(a)) * 0.4)); }
  g.add(mesh(new THREE.LatheGeometry(pts, 40), MAT.glass(), null, { cast: false }));
  if (color !== null) {
    const liq = mesh(new THREE.CircleGeometry(0.24, 32), MAT.liquid(color, opacity), [0, 0.07, 0], { cast: false });
    liq.rotation.x = -Math.PI / 2; g.add(liq); g.userData.liquid = liq;
  }
  return g;
}
export function labelTexture(text, sub = '', color = '#1e3a8a') {
  return canvasTexture(`lbl:${text}:${sub}`, 256, 128, (c, W, H) => {
    c.fillStyle = '#fbfaf3'; c.fillRect(0, 0, W, H);
    c.fillStyle = color; c.fillRect(0, 0, W, 16); c.fillRect(0, H - 8, W, 8);
    c.fillStyle = '#111827'; c.font = '700 34px system-ui, sans-serif'; c.textAlign = 'center';
    c.fillText(text, W / 2, 66);
    if (sub) { c.font = '500 22px system-ui, sans-serif'; c.fillStyle = '#374151'; c.fillText(sub, W / 2, 100); }
  });
}
export function reagentBottle(text, liquid = 0x7c3aed, sub = '', opts = {}) {
  const g = new THREE.Group();
  const brown = opts.amber;
  const glass = new THREE.MeshPhysicalMaterial({ color: brown ? 0x8a4b16 : 0xe8f4f8, roughness: 0.06, transparent: true, opacity: brown ? 0.75 : 0.3, clearcoat: 1, depthWrite: false });
  const prof = [[0.001, 0], [0.13, 0.0], [0.15, 0.02], [0.15, 0.36], [0.12, 0.42], [0.06, 0.46], [0.06, 0.52]];
  g.add(mesh(new THREE.LatheGeometry(prof.map(([r, y]) => new THREE.Vector2(r, y)), 32), glass, null, { cast: false }));
  g.add(mesh(new THREE.CylinderGeometry(0.135, 0.135, 0.28, 32), MAT.liquid(liquid, 0.8), [0, 0.16, 0], { cast: false }));
  g.add(mesh(new THREE.CylinderGeometry(0.068, 0.068, 0.07, 20), MAT.gloss(0x1f2937), [0, 0.53, 0]));
  const lbl = mesh(new THREE.CylinderGeometry(0.152, 0.152, 0.16, 32, 1, true, -0.9, 1.8), new THREE.MeshStandardMaterial({ map: labelTexture(text, sub), roughness: 0.8 }), [0, 0.2, 0]);
  g.add(lbl);
  return g;
}
export function spiritLamp() {
  const g = new THREE.Group();
  const prof = [[0.001, 0], [0.22, 0], [0.24, 0.03], [0.24, 0.16], [0.16, 0.26], [0.06, 0.3], [0.06, 0.33]];
  g.add(mesh(new THREE.LatheGeometry(prof.map(([r, y]) => new THREE.Vector2(r, y)), 32), MAT.glass(), null, { cast: false }));
  g.add(mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.1, 28), MAT.liquid(0x93c5fd, 0.5), [0, 0.07, 0], { cast: false }));
  g.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.05, 16), MAT.brushed(), [0, 0.34, 0]));
  g.add(mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.05, 8), MAT.matte(0xf5f5f4), [0, 0.38, 0]));
  const flame = new THREE.Group(); flame.position.y = 0.4;
  const outer = mesh(new THREE.SphereGeometry(0.04, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffb547, transparent: true, opacity: 0.7, depthWrite: false }), null, { cast: false });
  outer.scale.set(1, 2.6, 1); outer.position.y = 0.08;
  const inner = mesh(new THREE.SphereGeometry(0.022, 12, 10), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.7, depthWrite: false }), null, { cast: false });
  inner.scale.set(1, 1.8, 1); inner.position.y = 0.035;
  flame.add(outer, inner); flame.visible = false; g.add(flame);
  g.userData.flame = flame;
  return g;
}
export function filterPaper(w = 0.5, d = 0.3) {
  return mesh(new THREE.BoxGeometry(w, 0.003, d), MAT.paper(), [0, 0.0015, 0]);
}
export function washBottle() {
  const g = new THREE.Group();
  const body = new THREE.MeshPhysicalMaterial({ color: 0xf1f5f9, roughness: 0.35, transparent: true, opacity: 0.85, clearcoat: 0.4 });
  const prof = [[0.001, 0], [0.24, 0], [0.26, 0.04], [0.26, 0.62], [0.2, 0.74], [0.07, 0.8]];
  g.add(mesh(new THREE.LatheGeometry(prof.map(([r, y]) => new THREE.Vector2(r, y)), 28), body));
  g.add(mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.08, 20), MAT.plastic(0x0ea5e9), [0, 0.83, 0]));
  const tube = mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.45, 8), MAT.plastic(0xe2e8f0), [0.16, 0.98, 0]);
  tube.rotation.z = -1.0; g.add(tube);
  return g;
}
export function petriDish(color = 0xf5f5f4) {
  const g = new THREE.Group();
  const prof = [[0.001, 0], [0.45, 0], [0.46, 0.01], [0.46, 0.07], [0.455, 0.075]];
  g.add(mesh(new THREE.LatheGeometry(prof.map(([r, y]) => new THREE.Vector2(r, y)), 40), MAT.glass(), null, { cast: false }));
  const m = mesh(new THREE.CircleGeometry(0.44, 40), new THREE.MeshStandardMaterial({ color, roughness: 0.6 }), [0, 0.012, 0]);
  m.rotation.x = -Math.PI / 2; g.add(m);
  return g;
}
export function tissueMat(color) { return wet(color, { roughness: 0.45 }); }
