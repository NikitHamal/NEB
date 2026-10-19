import { THREE, getSoftDotTexture } from '../../core/engine.js';
import { catmull } from '../anatomy/sdf.js';
import { PATHS } from './heart-model.js';
import { AIRWAY } from './lung-model.js';

const RA = [-3.0, 1.4, 0.0];
const TRI = [-1.6, 0.2, 0.9];
const RVB = [-0.4, -2.2, 1.9];
const RVO = [0.4, 0.0, 2.2];
const LA = [0.6, 2.3, -2.4];
const MIT = [1.0, 0.5, -0.6];
const LVB = [2.2, -2.8, 0.9];
const LVO = [0.9, -0.2, 0.3];

function lungLoop(side, from, to) {
  const s = side === 'left' ? 1 : -1;
  return catmull([from, [s * 6.8, 4.0, -1.6], [s * 8.2, 0.2, -0.4], [s * 7.6, -3.6, 0.6], [s * 6.2, -1.0, -2.6], [s * 6.0, 2.2, -3.6], to], 6);
}

function route(parts) {
  const pts = []; const kinds = [];
  parts.forEach(([kind, poly]) => {
    poly.forEach((p, i) => { if (i === 0 && pts.length) return; pts.push(new THREE.Vector3(...p)); kinds.push(kind); });
  });
  const cum = [0];
  for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + pts[i].distanceTo(pts[i - 1]));
  return { pts, kinds, cum, len: cum[cum.length - 1] };
}

function circuits() {
  const venous = { svc: PATHS.svc.slice().reverse().concat([RA]), ivc: PATHS.ivc.slice().reverse().concat([RA]) };
  const right = [RA, TRI, RVB, RVO, ...PATHS.trunk.slice(1)];
  const lungR = (pv) => [['lung', lungLoop('right', PATHS.rpa[PATHS.rpa.length - 1], pv[pv.length - 1])], ['pv', pv.slice().reverse().concat([LA])]];
  const lungL = (pv) => [['lung', lungLoop('left', PATHS.lpa[PATHS.lpa.length - 1], pv[pv.length - 1])], ['pv', pv.slice().reverse().concat([LA])]];
  const left = [LA, MIT, LVB, LVO, ...PATHS.aorta.slice(0, 18)];
  const exits = {
    brachio: PATHS.brachio, carotid: PATHS.carotid, subclavian: PATHS.subclavian, down: PATHS.aorta.slice(17),
  };
  const out = [];
  for (const v of ['svc', 'ivc']) {
    for (const lung of ['r1', 'r2', 'l1', 'l2']) {
      for (const ex of Object.keys(exits)) {
        const pa = lung[0] === 'r' ? PATHS.rpa : PATHS.lpa;
        const pv = { r1: PATHS.rspv, r2: PATHS.ripv, l1: PATHS.lspv, l2: PATHS.lipv }[lung];
        const lungParts = lung[0] === 'r' ? lungR(pv) : lungL(pv);
        out.push(route([
          ['vein', venous[v]], ['heartR', right], ['pa', pa], ...lungParts, ['heartL', left],
          ['artery', ex === 'down' ? exits.down : [PATHS.aorta[17], ...exits[ex]]],
        ]));
      }
    }
  }
  return out;
}

function rbcGeometry() {
  const prof = [];
  for (let i = 0; i <= 12; i++) {
    const r = i / 12;
    const th = 0.18 + 0.32 * Math.pow(r, 2) - 0.25 * Math.pow(r, 6);
    prof.push(new THREE.Vector2(r * 0.24, th * 0.24));
  }
  for (let i = 12; i >= 0; i--) {
    const r = i / 12;
    const th = 0.18 + 0.32 * Math.pow(r, 2) - 0.25 * Math.pow(r, 6);
    prof.push(new THREE.Vector2(r * 0.24, -th * 0.24));
  }
  const g = new THREE.LatheGeometry(prof, 18);
  g.computeVertexNormals();
  return g;
}

export function createBloodFlow(quality) {
  const routes = circuits();
  const n = quality.tier === 'low' ? 140 : quality.tier === 'medium' ? 240 : 360;
  const mat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.35, clearcoat: 0.6, sheen: 0.5, sheenColor: new THREE.Color(0xff9a8a) });
  const mesh = new THREE.InstancedMesh(rbcGeometry(), mat, n);
  mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  mesh.frustumCulled = false;
  const cells = [];
  for (let i = 0; i < n; i++) {
    const r = routes[Math.floor(Math.random() * routes.length)];
    cells.push({ r, s: Math.random() * r.len, seg: 0, rot: new THREE.Euler(Math.random() * 6, Math.random() * 6, 0), spin: (Math.random() - 0.5) * 3, jit: new THREE.Vector3((Math.random() - 0.5) * 0.5, (Math.random() - 0.5) * 0.5, (Math.random() - 0.5) * 0.5) });
  }
  const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const pos = new THREE.Vector3(); const sc = new THREE.Vector3(1, 1, 1);
  const deox = new THREE.Color(); const ox = new THREE.Color(); const col = new THREE.Color();
  const speedOf = { vein: 2.6, heartR: 3.4, pa: 5.0, lung: 1.4, pv: 3.0, heartL: 3.8, artery: 6.5 };
  return {
    mesh,
    update(dt, flowK, textbook) {
      deox.set(textbook ? 0x2f4fd8 : 0x5a0f1e);
      ox.set(textbook ? 0xe02020 : 0xd2140f);
      for (let i = 0; i < n; i++) {
        const c = cells[i];
        const R = c.r;
        while (c.seg < R.cum.length - 2 && R.cum[c.seg + 1] < c.s) c.seg++;
        const kind = R.kinds[c.seg + 1] || 'vein';
        const pulsed = kind === 'artery' || kind === 'pa' || kind === 'heartL' || kind === 'heartR';
        c.s += dt * speedOf[kind] * (pulsed ? flowK.pulse : flowK.steady);
        if (c.s >= R.len) {
          c.r = routes[Math.floor(Math.random() * routes.length)];
          c.s = Math.random() * 2; c.seg = 0;
          continue;
        }
        const a = R.pts[c.seg]; const b = R.pts[c.seg + 1];
        const t = (c.s - R.cum[c.seg]) / Math.max(1e-6, R.cum[c.seg + 1] - R.cum[c.seg]);
        pos.copy(a).lerp(b, Math.min(1, Math.max(0, t))).add(c.jit);
        c.rot.x += c.spin * dt; c.rot.y += c.spin * 0.7 * dt;
        q.setFromEuler(c.rot);
        m4.compose(pos, q, sc);
        mesh.setMatrixAt(i, m4);
        let o = 0;
        const firstLung = R.kinds.indexOf('lung');
        const lastLung = R.kinds.lastIndexOf('lung');
        if (c.seg >= lastLung) o = 1;
        else if (c.seg >= firstLung) o = (c.seg - firstLung) / Math.max(1, lastLung - firstLung);
        col.copy(deox).lerp(ox, o);
        mesh.setColorAt(i, col);
      }
      mesh.instanceMatrix.needsUpdate = true;
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
    },
    dispose() { mesh.geometry.dispose(); mat.dispose(); mesh.dispose(); },
  };
}

export function createAirFlow(branches, quality) {
  const leaves = branches.filter((b) => b.gen >= 6);
  const byEnd = new Map();
  branches.forEach((b) => byEnd.set(b.b.join(','), b));
  const chains = leaves.map((leaf) => {
    const pts = [leaf.b, leaf.a];
    let cur = leaf;
    for (let i = 0; i < 12; i++) {
      const parent = byEnd.get(cur.a.join(','));
      if (!parent) break;
      pts.push(parent.a);
      cur = parent;
    }
    const side = leaf.a[0] < 0 ? AIRWAY.right : AIRWAY.left;
    const all = [...AIRWAY.trachea, ...side.slice(1), ...pts.reverse().slice(1)];
    const v = all.map((p) => new THREE.Vector3(...p));
    const cum = [0];
    for (let i = 1; i < v.length; i++) cum.push(cum[i - 1] + v[i].distanceTo(v[i - 1]));
    return { v, cum, len: cum[cum.length - 1] };
  });
  const n = quality.tier === 'low' ? 260 : 520;
  const position = new Float32Array(n * 3);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(position, 3));
  const mat = new THREE.PointsMaterial({ size: 0.045, map: getSoftDotTexture(), color: 0xaee8ff, transparent: true, opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
  const pts = new THREE.Points(geo, mat);
  pts.frustumCulled = false;
  const parts = [];
  for (let i = 0; i < n; i++) parts.push({ c: chains[i % chains.length], off: Math.random(), j: [(Math.random() - 0.5) * 0.4, (Math.random() - 0.5) * 0.4, (Math.random() - 0.5) * 0.4] });
  const tmp = new THREE.Vector3();
  return {
    points: pts,
    update(vol) {
      for (let i = 0; i < n; i++) {
        const p = parts[i];
        const s = Math.min(0.999, Math.max(0, vol * 0.9 + p.off * 0.35 - 0.12)) * p.c.len;
        let k = 1;
        while (k < p.c.cum.length - 1 && p.c.cum[k] < s) k++;
        const a = p.c.v[k - 1]; const b = p.c.v[k];
        const t = (s - p.c.cum[k - 1]) / Math.max(1e-6, p.c.cum[k] - p.c.cum[k - 1]);
        tmp.copy(a).lerp(b, t);
        position[i * 3] = tmp.x + p.j[0] * (1 - s / p.c.len); position[i * 3 + 1] = tmp.y + p.j[1] * (1 - s / p.c.len); position[i * 3 + 2] = tmp.z + p.j[2] * (1 - s / p.c.len);
      }
      geo.attributes.position.needsUpdate = true;
    },
    dispose() { geo.dispose(); mat.dispose(); },
  };
}
