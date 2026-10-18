// The three flowers of the NEB family dissection, built from their real floral plans.
// Solanaceae, Datura: actinomorphic, bisexual; calyx a five-angled tube of five fused sepals,
// corolla a white funnel of five fused, pleated petals ending in five points, five stamens
// fused to the corolla tube (epipetalous), a bicarpellary superior ovary, falsely four-chambered,
// with swollen axile placentas. K(5) C(5) A5 G(2).
// Fabaceae, pea: zygomorphic; calyx of five fused sepals; a papilionaceous corolla of a large
// standard, two wings and a keel of two fused petals (vexillary aestivation); diadelphous stamens,
// nine fused into a sheath plus one free; a monocarpellary ovary with marginal placentation.
// K(5) C1+2+(2) A(9)+1 G1.
// Liliaceae, lily: actinomorphic, trimerous; six free tepals in two whorls of three, six stamens
// with versatile anthers, a tricarpellary syncarpous superior ovary, trilocular, axile. P3+3 A3+3 G(3).
import { THREE } from '../../engine.js';
import { wet, mesh } from '../kit.js';
import { petalTexture, sheetGeometry, petalMaterial, tubeGeometry, stamen, pistil } from './flower-parts.js';

function part(list, obj, id, name, whorl, extra = {}) { obj.name = id; list.push(Object.assign({ id, name, whorl, obj }, extra)); return obj; }

function datura() {
  const root = new THREE.Group(); const parts = [];
  const green = wet(0x6f9a3a, { roughness: 0.6, sheen: 0.2 });
  root.add(mesh(new THREE.CylinderGeometry(0.012, 0.014, 0.16, 10), green, [0, -0.08, 0]));
  const calyx = mesh(tubeGeometry({ len: 0.34, radius: (v) => 0.045 + 0.015 * Math.sin(v * Math.PI * 0.9), lobes: 5, lobeDepth: 0.0, lobeStart: 0.86, ridge: 0.18, nth: 50, nv: 16 }), new THREE.MeshPhysicalMaterial({ color: 0x7fae45, roughness: 0.55, side: THREE.DoubleSide, sheen: 0.3, sheenColor: new THREE.Color(0xe8ffd0) }));
  part(parts, calyx, 'calyx', 'Calyx (5 fused sepals)', 'calyx', { lay: { rx: -Math.PI / 2, s: 1 } });
  const corTex = petalTexture('datura', { base: '#f6f7ef', tip: '#ffffff', throat: '#e3efc8', vein: 'rgba(120,150,90,0.25)', veins: 14 });
  const corolla = new THREE.Group();
  const funnel = mesh(tubeGeometry({ len: 0.78, radius: (v) => (v < 0.45 ? 0.032 + v * 0.04 : 0.05 + Math.pow((v - 0.45) / 0.55, 2.2) * 0.25), lobes: 5, lobeDepth: 0.75, lobeStart: 0.82, ridge: 0.06, nth: 80, nv: 30, flare: 0.5 }), petalMaterial(corTex, { roughness: 0.5 }));
  corolla.add(funnel);
  // the five epipetalous stamens are fused to the inside of the corolla tube
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2 + Math.PI / 5;
    const s = stamen({ len: 0.36, anther: 0xf3e3a4, antherLen: 0.08, curve: 0.0 });
    s.position.set(Math.cos(a) * 0.03, 0.3, Math.sin(a) * 0.03); s.rotation.y = -a;
    corolla.add(s);
  }
  part(parts, corolla, 'corolla', 'Corolla with epipetalous stamens', 'corolla', { lay: { rx: -Math.PI / 2, s: 0.8 }, carries: 'androecium' });
  const pis = pistil({ ovaryR: 0.035, ovaryH: 0.075, styleLen: 0.62, stigma: 'lobed', lobes: 2, color: 0x93bf5a, spiny: true });
  part(parts, pis, 'pistil', 'Pistil (bicarpellary)', 'gynoecium', { lay: { rx: -Math.PI / 2, s: 1 }, gyno: true });
  [calyx, corolla, pis].forEach((o) => root.add(o));
  return {
    root, parts, gyno: pis, tsKind: 'axile2', placentation: 'axile', scale: 1,
    family: 'Solanaceae', example: 'Datura (dhaturo)', symmetry: 'actinomorphic',
    boxes: [['calyx', 'Calyx'], ['corolla', 'Corolla + stamens'], ['androecium', 'Androecium'], ['gynoecium', 'Gynoecium']],
    formula: { sym: '⊕', sex: '⚥', k: 'K(5)', c: 'C(5)', a: 'A5 (epipetalous)', g: 'G(2)' },
    tilt: 0.45,
  };
}

function pea() {
  const root = new THREE.Group(); const parts = [];
  const flower = new THREE.Group(); root.add(flower);
  const green = wet(0x6c9b3c, { roughness: 0.6 });
  flower.add(mesh(new THREE.CylinderGeometry(0.004, 0.005, 0.06, 8), green, [0, -0.03, 0]));
  const calyx = mesh(tubeGeometry({ len: 0.075, radius: (v) => 0.018 + v * 0.016, lobes: 5, lobeDepth: 1.1, lobeStart: 0.55, nth: 40, nv: 12 }), new THREE.MeshPhysicalMaterial({ color: 0x78a843, roughness: 0.55, side: THREE.DoubleSide }));
  part(parts, calyx, 'calyx', 'Calyx (5 fused sepals)', 'calyx', { lay: { rx: -Math.PI / 2, s: 1 } });
  const pink = petalTexture('pea-std', { base: '#f3c6dc', tip: '#d9468f', throat: '#f7e7ef', vein: 'rgba(140,20,80,0.35)', veins: 13 });
  const wingT = petalTexture('pea-wing', { base: '#e9a3c8', tip: '#b8236e', vein: 'rgba(120,20,70,0.3)', veins: 7 });
  const keelT = petalTexture('pea-keel', { base: '#f8eef3', tip: '#f0d4e2', vein: 'rgba(150,80,110,0.2)', veins: 5 });
  const stdP = { len: 0.17, width: (v) => (v < 0.15 ? 0.012 + v * 0.1 : 0.085 * Math.sin(Math.min(1, (v - 0.05) / 0.95) * Math.PI) * (1 - 0.18 * Math.exp(-Math.pow((v - 1) / 0.06, 2))) + 0.008), cup: 0.04, curl: -0.9, nu: 14, nv: 20 };
  const std = mesh(sheetGeometry(stdP), petalMaterial(pink));
  std.userData.flat = () => sheetGeometry(Object.assign({}, stdP, { curl: 0, cup: 0.01 }));
  std.position.set(0, 0.05, -0.022); std.rotation.x = -0.25;
  part(parts, std, 'standard', 'Standard (vexillum)', 'corolla', { lay: { rx: -Math.PI / 2, s: 1 } });
  const wings = [-1, 1].map((s) => {
    const w = mesh(sheetGeometry({ len: 0.13, width: (v) => (v < 0.18 ? 0.006 : 0.036 * Math.sin(Math.min(1, (v - 0.1) / 0.9) * Math.PI) + 0.006), cup: 0.12, curl: 0.25, nu: 8, nv: 14 }), petalMaterial(wingT));
    w.position.set(s * 0.016, 0.055, 0.0); w.rotation.set(0.35, s * 0.35, s * -0.25);
    return part(parts, w, s < 0 ? 'wingL' : 'wingR', 'Wing (ala)', 'corolla', { lay: { rx: -Math.PI / 2, s: 1 } });
  });
  const keel = mesh(sheetGeometry({ len: 0.11, width: (v) => (v < 0.2 ? 0.008 : 0.024 * Math.sin(Math.min(1, (v - 0.1) / 0.9) * Math.PI) + 0.006), cup: -0.0, keel: 0.9, curl: 0.9, nu: 10, nv: 14 }), petalMaterial(keelT));
  keel.position.set(0, 0.055, 0.008); keel.rotation.x = 0.55;
  part(parts, keel, 'keel', 'Keel (carina, 2 fused petals)', 'corolla', { lay: { rx: -Math.PI / 2, s: 1 } });
  // diadelphous stamens: nine filaments fused into a sheath around the ovary, one free
  const sheath = new THREE.Group();
  const tube = mesh(new THREE.CylinderGeometry(0.008, 0.009, 0.075, 12, 1, true, 0.4, Math.PI * 2 - 0.8), new THREE.MeshPhysicalMaterial({ color: 0xf2f0dc, roughness: 0.5, side: THREE.DoubleSide }), [0, 0.09, 0.016]);
  tube.rotation.x = 0.6; sheath.add(tube);
  for (let i = 0; i < 9; i++) { const a = (i / 9 - 0.5) * 2.4; const s = stamen({ len: 0.025, anther: 0xf2cf48, antherLen: 0.008 }); s.position.set(Math.sin(a) * 0.008, 0.115, 0.04 + Math.cos(a) * 0.004); s.rotation.x = 0.7; sheath.add(s); }
  part(parts, sheath, 'sheath', 'Stamens: sheath of 9 fused', 'androecium', { lay: { rx: -Math.PI / 2, s: 1 } });
  const free = stamen({ len: 0.09, anther: 0xf2cf48, antherLen: 0.008, curve: 0.01 }); free.position.set(0, 0.05, -0.004); free.rotation.x = 0.55;
  part(parts, free, 'free', 'Stamen: the 1 free one', 'androecium', { lay: { rx: -Math.PI / 2, s: 1 } });
  const pis = pistil({ ovaryR: 0.006, ovaryH: 0.07, styleLen: 0.03, stigma: 'capitate', color: 0x9ccc65, bend: -0.015 });
  pis.position.set(0, 0.05, 0.01); pis.rotation.x = 0.6;
  part(parts, pis, 'pistil', 'Pistil (monocarpellary)', 'gynoecium', { lay: { rx: -Math.PI / 2, s: 1 }, gyno: true });
  [calyx, std, ...wings, keel, sheath, free, pis].forEach((o) => flower.add(o));
  // the flower is held with its axis forward and the standard on top
  flower.rotation.x = -1.15;
  return {
    root, parts, gyno: pis, tsKind: 'marginal', placentation: 'marginal', scale: 0.42,
    family: 'Fabaceae', example: 'Pea (kerau)', symmetry: 'zygomorphic',
    boxes: [['calyx', 'Calyx'], ['corolla', 'Corolla'], ['androecium', 'Androecium'], ['gynoecium', 'Gynoecium']],
    formula: { sym: '%', sex: '⚥', k: 'K(5)', c: 'C1+2+(2)', a: 'A(9)+1', g: 'G1' },
    tilt: 0,
  };
}

function lily() {
  const root = new THREE.Group(); const parts = [];
  const green = wet(0x5f8f35, { roughness: 0.6 });
  root.add(mesh(new THREE.CylinderGeometry(0.014, 0.016, 0.2, 10), green, [0, -0.1, 0]));
  const tex = petalTexture('lily', { base: '#f7b26b', tip: '#f0793a', throat: '#f5d27a', vein: 'rgba(160,60,20,0.22)', spots: 'rgba(90,20,15,0.85)', veins: 7 });
  const texIn = petalTexture('lily-in', { base: '#f9be78', tip: '#f2853f', throat: '#f7da86', vein: 'rgba(160,60,20,0.22)', spots: 'rgba(90,20,15,0.85)', veins: 9 });
  for (let w = 0; w < 2; w++) {
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2 + (w ? Math.PI / 3 : 0);
      const holder = new THREE.Group(); holder.rotation.y = -a;
      const tp = { len: 0.46, width: (v) => (w ? 0.075 : 0.06) * Math.sin(Math.min(1, v * 1.05) * Math.PI) * (v < 0.1 ? 0.6 : 1) + 0.008, cup: 0.18, curl: 2.1, edgeWave: w ? 0.4 : 0.1, nu: 10, nv: 22 };
      const t = mesh(sheetGeometry(tp), petalMaterial(w ? texIn : tex));
      t.userData.flat = () => sheetGeometry(Object.assign({}, tp, { curl: 0.3, cup: 0.06 }));
      t.rotation.x = 0.42; t.position.set(0, 0.015, 0.012 * (w ? 0.6 : 1));
      holder.add(t); holder.position.y = 0.01;
      part(parts, holder, `tepal${w}${i}`, w ? 'Inner tepal' : 'Outer tepal', w ? 'inner' : 'outer', { lay: { rx: -Math.PI / 2, s: 0.75 } });
      root.add(holder);
    }
  }
  for (let i = 0; i < 6; i++) {
    const a = (i / 6) * Math.PI * 2 + Math.PI / 6;
    const holder = new THREE.Group(); holder.rotation.y = -a;
    const s = stamen({ len: 0.4, anther: 0x8a3d14, antherLen: 0.06, curve: 0.08, versatile: true, filament: 0xe8e3b0 });
    s.rotation.x = 0.28; holder.add(s); holder.position.y = 0.012;
    part(parts, holder, `stamen${i}`, 'Stamen', 'androecium', { lay: { rx: -Math.PI / 2, s: 0.9 } });
    root.add(holder);
  }
  const pis = pistil({ ovaryR: 0.032, ovaryH: 0.12, styleLen: 0.33, stigma: 'lobed', lobes: 3, color: 0x8fbf55, styleColor: 0xc9d98e });
  part(parts, pis, 'pistil', 'Pistil (tricarpellary)', 'gynoecium', { lay: { rx: -Math.PI / 2, s: 1 }, gyno: true });
  root.add(pis);
  return {
    root, parts, gyno: pis, tsKind: 'axile3', placentation: 'axile', scale: 1.15,
    family: 'Liliaceae', example: 'Lily', symmetry: 'actinomorphic',
    boxes: [['outer', 'Outer perianth'], ['inner', 'Inner perianth'], ['androecium', 'Androecium'], ['gynoecium', 'Gynoecium']],
    formula: { sym: '⊕', sex: '⚥', k: 'P3+3', c: '', a: 'A3+3', g: 'G(3)' },
    tilt: 0.25,
  };
}

export const FAMILIES = { Solanaceae: datura, Fabaceae: pea, Liliaceae: lily };
export const WHORL_ORDER = { calyx: 0, outer: 0, corolla: 1, inner: 1, androecium: 2, gynoecium: 3 };
