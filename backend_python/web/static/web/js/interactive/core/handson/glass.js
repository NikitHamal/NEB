// Volumetric glassware for the hands-on chemistry practicals, at true size (1 unit = 10 cm), with
// liquids whose level follows the real volume: a conical flask whose liquid is re-turned from the
// flask's own inner profile, a 50 mL burette with a printed 0.1 mL scale read from the top down
// and a concave meniscus, a 25 mL bulb pipette with its etched mark, and a pool of falling drops.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';

const V2 = (r, y) => new THREE.Vector2(r, y);
const ML_PER_UNIT3 = 1000;

/** Lathe-turned vessel with a wall: the outer skin, the inner skin and a rolled rim. */
function vessel(outer, wall, seg) {
  const g = new THREE.Group();
  const inner = outer.map((p) => V2(Math.max(0.0005, p.x - wall), p.y + (p.y < wall ? wall : 0)));
  const o = mesh(new THREE.LatheGeometry(outer, seg), MAT.glass(), null, { cast: false, receive: false });
  const i = mesh(new THREE.LatheGeometry(inner, seg), MAT.glass(), null, { cast: false, receive: false });
  o.renderOrder = 5; i.renderOrder = 4;
  const top = outer[outer.length - 1];
  const rim = mesh(new THREE.TorusGeometry(top.x - wall / 2, wall * 0.75, 8, seg), MAT.glassEdge(), [0, top.y, 0], { cast: false });
  rim.rotation.x = Math.PI / 2; rim.renderOrder = 5;
  g.add(o, i, rim);
  return { group: g, inner };
}

/** Volume table for an inner profile: height -> mL, and the inverse. */
function volumeTable(inner, steps = 240) {
  const top = inner[inner.length - 1].y; const ys = new Float32Array(steps + 1); const vs = new Float32Array(steps + 1);
  const rAt = (y) => { for (let k = 1; k < inner.length; k++) { const a = inner[k - 1]; const b = inner[k]; if (y <= b.y) { const t = (y - a.y) / Math.max(1e-6, b.y - a.y); return a.x + (b.x - a.x) * t; } } return inner[inner.length - 1].x; };
  let v = 0; const base = inner[0].y;
  for (let i = 0; i <= steps; i++) {
    const y = base + (top - base) * (i / steps); ys[i] = y;
    if (i > 0) { const y0 = ys[i - 1]; const r0 = rAt(y0); const r1 = rAt(y); v += Math.PI * (r0 * r0 + r0 * r1 + r1 * r1) / 3 * (y - y0) * ML_PER_UNIT3; }
    vs[i] = v;
  }
  return {
    rAt, total: v,
    heightOf(ml) { if (ml <= 0) return base; for (let i = 1; i <= steps; i++) if (vs[i] >= ml) { const t = (ml - vs[i - 1]) / Math.max(1e-6, vs[i] - vs[i - 1]); return ys[i - 1] + (ys[i] - ys[i - 1]) * t; } return top; },
  };
}

/** Liquid material whose colour can be driven per frame. */
export function liquidMaterial(color = 0xf3f8ff, opacity = 0.42) {
  return new THREE.MeshPhysicalMaterial({ color, roughness: 0.05, transparent: true, opacity, clearcoat: 1, clearcoatRoughness: 0.04, depthWrite: false, side: THREE.DoubleSide });
}

/** A 250 mL conical (Erlenmeyer) flask. setVolume(ml) re-turns the liquid; swirl tilts it. */
export function conicalFlask({ color = 0xf3f8ff, opacity = 0.42 } = {}) {
  const outer = [V2(0.001, 0), V2(0.36, 0), V2(0.415, 0.02), V2(0.43, 0.07), V2(0.4, 0.2), V2(0.18, 1.0), V2(0.165, 1.08), V2(0.165, 1.38), V2(0.19, 1.42)];
  const { group, inner } = vessel(outer, 0.016, 48);
  const table = volumeTable(inner.slice(0, 7));
  const mat = liquidMaterial(color, opacity);
  const liquid = new THREE.Mesh(new THREE.BufferGeometry(), mat); liquid.renderOrder = 3; liquid.receiveShadow = false; group.add(liquid);
  const surfMat = new THREE.MeshPhysicalMaterial({ color, roughness: 0.02, transparent: true, opacity: Math.min(1, opacity + 0.15), clearcoat: 1, depthWrite: false });
  const surface = mesh(new THREE.CircleGeometry(1, 40), surfMat, null, { cast: false }); surface.rotation.x = -Math.PI / 2; surface.renderOrder = 3;
  group.add(surface);
  const scaleTex = canvasTexture('ho-flask-grad', 256, 256, (g, w, h) => {
    g.clearRect(0, 0, w, h); g.strokeStyle = 'rgba(255,255,255,.9)'; g.fillStyle = 'rgba(255,255,255,.95)'; g.lineWidth = 3; g.font = '700 22px system-ui, sans-serif';
    [50, 100, 150, 200].forEach((ml, i) => { const y = h - 30 - i * 50; g.beginPath(); g.moveTo(80, y); g.lineTo(150, y); g.stroke(); g.fillText(String(ml), 160, y + 8); });
  });
  scaleTex.userData.sharedFx = true;
  let ml = 0; let built = -1;
  function rebuild() {
    const h = table.heightOf(ml);
    const pts = []; const n = 14; const y0 = inner[0].y;
    pts.push(V2(0.0005, y0));
    for (let k = 0; k <= n; k++) { const y = y0 + (h - y0) * (k / n); pts.push(V2(Math.max(0.001, table.rAt(y) - 0.002), y)); }
    liquid.geometry.dispose(); liquid.geometry = new THREE.LatheGeometry(pts, 40);
    const r = table.rAt(h) - 0.002; surface.scale.set(r, r, 1); surface.position.y = h;
    liquid.visible = surface.visible = ml > 0.05; built = ml;
  }
  return {
    group, material: mat, surface, surfMat,
    get volume() { return ml; },
    setVolume(v) { ml = Math.max(0, Math.min(table.total * 0.98, v)); if (Math.abs(ml - built) > 0.15 || ml === 0) rebuild(); },
    surfaceY() { return table.heightOf(ml); },
    radiusAt(y) { return table.rAt(y); },
    setColor(c, o) { mat.color.copy(c); surfMat.color.copy(c); if (o !== undefined) { mat.opacity = o; surfMat.opacity = Math.min(1, o + 0.15); } },
    dispose() { liquid.geometry.dispose(); mat.dispose(); surfMat.dispose(); },
  };
}

// ---- burette ----------------------------------------------------------------------------------
export const BURETTE = { r: 0.0564, zeroY: 6.1, len: 5.0, bottomY: 0.95, tipY: 0 };

function buretteScale() {
  return canvasTexture('ho-burette-scale', 256, 4096, (g, w, h) => {
    g.clearRect(0, 0, w, h);
    const pad = 96; const span = h - pad * 2;
    g.fillStyle = 'rgba(17,24,39,.95)'; g.strokeStyle = 'rgba(17,24,39,.95)';
    for (let i = 0; i <= 500; i++) {
      const y = pad + span * (i / 500);
      const major = i % 10 === 0; const half = i % 5 === 0;
      g.lineWidth = major ? 3.2 : 2;
      const len = major ? 110 : half ? 72 : 44;
      g.beginPath(); g.moveTo(14, y); g.lineTo(14 + len, y); g.stroke();
      if (major) { g.font = '700 34px system-ui, sans-serif'; g.textBaseline = 'middle'; g.fillText(String(i / 10), 136, y); }
    }
    g.font = '700 26px system-ui, sans-serif'; g.textBaseline = 'top'; g.fillText('mL  20°C', 18, 18); g.fillText('±0.05', 18, 50);
  }, { anisotropy: 8 });
}

/** A 50 mL burette, graduated 0 at the top to 50 below, with a PTFE stopcock and a drawn tip. */
export function burette() {
  const B = BURETTE; const g = new THREE.Group();
  const top = B.zeroY + 0.55;
  const tube = mesh(new THREE.CylinderGeometry(B.r + 0.01, B.r + 0.01, top - B.bottomY, 28, 1, true), MAT.glass(), [0, (top + B.bottomY) / 2, 0], { cast: false });
  tube.renderOrder = 5; g.add(tube);
  const rim = mesh(new THREE.TorusGeometry(B.r + 0.012, 0.008, 6, 24), MAT.glassEdge(), [0, top, 0], { cast: false }); rim.rotation.x = Math.PI / 2; g.add(rim);
  const taper = mesh(new THREE.CylinderGeometry(B.r + 0.01, 0.022, 0.22, 24, 1, true), MAT.glass(), [0, B.bottomY - 0.11, 0], { cast: false }); g.add(taper);
  const barrel = mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.2, 20), MAT.glassEdge(), [0, 0.68, 0], { cast: false }); barrel.rotation.z = Math.PI / 2; g.add(barrel);
  const key = new THREE.Group(); key.position.set(0, 0.68, 0);
  const plug = mesh(new THREE.CylinderGeometry(0.036, 0.03, 0.3, 16), MAT.plastic(0xf4f4f5)); plug.rotation.z = Math.PI / 2; key.add(plug);
  const handle = mesh(new THREE.BoxGeometry(0.035, 0.2, 0.06), MAT.plastic(0xf4f4f5), [0.17, 0, 0]); key.add(handle);
  const nut = mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.04, 6), MAT.plastic(0x1f2937), [-0.17, 0, 0]); nut.rotation.z = Math.PI / 2; key.add(nut);
  g.add(key);
  g.add(mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.2, 14), MAT.glass(), [0, 0.53, 0], { cast: false }));
  const tip = mesh(new THREE.CylinderGeometry(0.02, 0.006, 0.43, 14, 1, true), MAT.glass(), [0, 0.215, 0], { cast: false }); g.add(tip);
  // printed scale on a quarter of the circumference, facing +z
  const sMat = new THREE.MeshBasicMaterial({ map: buretteScale(), transparent: true, depthWrite: false });
  const pad = 96 / 4096; const tot = B.len / (1 - pad * 2);
  const scale = new THREE.Mesh(new THREE.CylinderGeometry(B.r + 0.0115, B.r + 0.0115, tot, 24, 1, true, -0.62, 1.24), sMat);
  scale.position.y = B.zeroY - B.len / 2; scale.renderOrder = 6; scale.userData.noPick = true; g.add(scale);
  // the acid column and its meniscus
  const lMat = liquidMaterial(0xe6f0ff, 0.3);
  const col = mesh(new THREE.CylinderGeometry(B.r, B.r, 1, 24, 1, true), lMat, null, { cast: false }); col.renderOrder = 3; g.add(col);
  const menPts = []; for (let i = 0; i <= 10; i++) { const t = i / 10; menPts.push(V2(Math.max(0.0005, B.r * t), 0.014 * Math.pow(t, 2.6))); }
  const men = mesh(new THREE.LatheGeometry(menPts, 24), new THREE.MeshBasicMaterial({ color: 0x3b4a5c, transparent: true, opacity: 0.78, depthWrite: false, side: THREE.DoubleSide }), null, { cast: false });
  men.renderOrder = 4; g.add(men);
  const band = mesh(new THREE.CylinderGeometry(B.r + 0.0005, B.r + 0.0005, 0.012, 24, 1, true), new THREE.MeshBasicMaterial({ color: 0x1e293b, transparent: true, opacity: 0.35, depthWrite: false }), null, { cast: false });
  band.renderOrder = 4; g.add(band);
  const stem = mesh(new THREE.CylinderGeometry(0.013, 0.005, 1, 10), lMat, null, { cast: false }); stem.renderOrder = 3; g.add(stem);
  let reading = 50; let jetFull = false;
  const yOf = (r) => B.zeroY - (r / 50) * B.len;
  function set(r) {
    reading = Math.max(-6, Math.min(50.5, r));
    const y = yOf(reading); const h = Math.max(0.001, y - B.bottomY);
    col.visible = men.visible = band.visible = reading < 50.4;
    col.scale.y = h; col.position.y = B.bottomY + h / 2;
    men.position.y = y; band.position.y = y + 0.006;
  }
  set(50.5); stem.scale.y = 0.48; stem.position.y = 0.24 + 0.47; stem.visible = false;
  return {
    group: g, key, handle, tube, scale, material: lMat,
    get reading() { return reading; },
    set,
    yOf,
    readingAtY(y) { return (B.zeroY - y) / B.len * 50; },
    setJet(full) { jetFull = full; stem.visible = full; },
    get jetFull() { return jetFull; },
    tipWorld(out) { return out.set(0, B.tipY, 0).applyMatrix4(g.matrixWorld); },
  };
}

// ---- pipette ----------------------------------------------------------------------------------
/** A 25 mL bulb pipette: set(ml) is the volume held; exactly 25 mL puts the meniscus on the mark. */
export function bulbPipette() {
  const g = new THREE.Group();
  const prof = [V2(0.0035, 0), V2(0.012, 0.04), V2(0.016, 0.55), V2(0.02, 0.62), V2(0.13, 0.95), V2(0.13, 1.45), V2(0.02, 1.78), V2(0.016, 1.85), V2(0.016, 3.4)];
  const body = mesh(new THREE.LatheGeometry(prof, 28), MAT.glass(), null, { cast: false }); body.renderOrder = 5; g.add(body);
  const MARK = 2.75; const STEM_R = 0.0125; const mlPerUnit = Math.PI * STEM_R * STEM_R * ML_PER_UNIT3;
  const ring = mesh(new THREE.TorusGeometry(0.0172, 0.0016, 4, 28), MAT.ink(0x111827), [0, MARK, 0]); ring.rotation.x = Math.PI / 2; g.add(ring);
  const label = mesh(new THREE.PlaneGeometry(0.2, 0.2), new THREE.MeshBasicMaterial({ map: canvasTexture('ho-pip-label', 128, 128, (c, w, h) => { c.clearRect(0, 0, w, h); c.fillStyle = 'rgba(17,24,39,.9)'; c.font = '800 34px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText('25 mL', w / 2, 52); c.font = '600 20px system-ui, sans-serif'; c.fillText('AS ±0.03', w / 2, 84); }), transparent: true, depthWrite: false }), [0, 1.2, 0.132]);
  g.add(label);
  const lMat = liquidMaterial(0xf8fafc, 0.5);
  const fill = mesh(new THREE.LatheGeometry(prof.map((p) => V2(Math.max(0.0005, p.x - 0.004), p.y)).slice(0, 8), 20), lMat, null, { cast: false }); fill.renderOrder = 3; g.add(fill);
  const stem = mesh(new THREE.CylinderGeometry(STEM_R, STEM_R, 1, 12), lMat, null, { cast: false }); stem.renderOrder = 3; g.add(stem);
  const men = mesh(new THREE.CylinderGeometry(STEM_R + 0.0008, STEM_R + 0.0008, 0.006, 12, 1, true), new THREE.MeshBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.6, depthWrite: false }), null, { cast: false }); g.add(men);
  const filler = new THREE.Group(); filler.position.y = 3.4;
  const bulb = mesh(new THREE.SphereGeometry(0.17, 24, 16), MAT.gloss(0xb91c1c), [0, 0.24, 0]); bulb.scale.set(1, 1.15, 1); filler.add(bulb);
  filler.add(mesh(new THREE.CylinderGeometry(0.035, 0.03, 0.12, 14), MAT.gloss(0x991b1b), [0, 0.04, 0]));
  g.add(filler);
  let vol = 0;
  function set(ml) {
    vol = Math.max(0, ml);
    fill.visible = vol > 0.05;
    fill.scale.y = Math.min(1, Math.max(0.02, vol / 24));
    const y = MARK + (vol - 25) / mlPerUnit;
    const up = vol > 24 && y > 1.79;
    stem.visible = men.visible = up;
    if (up) { const yTop = Math.min(3.38, y); stem.scale.y = Math.max(0.001, yTop - 1.78); stem.position.y = 1.78 + stem.scale.y / 2; men.position.y = yTop; }
  }
  set(0);
  return {
    group: g, bulb, filler, material: lMat, MARK, mlPerUnit,
    get volume() { return vol; },
    levelY() { return MARK + (vol - 25) / mlPerUnit; },
    set,
    tipWorld(out) { return out.set(0, 0, 0).applyMatrix4(g.matrixWorld); },
  };
}

// ---- drops ------------------------------------------------------------------------------------
/** A small pool of falling drops. spawn(at, color) and each drop calls onLand(drop) when it reaches floorY(). */
export function createDrops(parent, n = 6) {
  const geo = new THREE.SphereGeometry(0.022, 12, 8);
  const pool = [];
  for (let i = 0; i < n; i++) {
    const m = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: 0xeef6ff, roughness: 0.02, transparent: true, opacity: 0.65, clearcoat: 1, depthWrite: false }));
    m.visible = false; m.renderOrder = 6; m.scale.set(1, 1.25, 1); parent.add(m);
    pool.push({ m, vy: 0, alive: false, floor: 0, onLand: null });
  }
  return {
    spawn(at, floorY, onLand, color) {
      const d = pool.find((p) => !p.alive); if (!d) return false;
      d.alive = true; d.m.visible = true; d.m.position.copy(at); d.vy = 0; d.floor = floorY; d.onLand = onLand;
      if (color !== undefined) d.m.material.color.set(color);
      return true;
    },
    update(dt) {
      for (const d of pool) {
        if (!d.alive) continue;
        d.vy -= 9.8 * 10 * dt * 0.5; d.m.position.y += d.vy * dt;
        if (d.m.position.y <= d.floor) { d.alive = false; d.m.visible = false; if (d.onLand) d.onLand(d.m.position); }
      }
    },
    clear() { pool.forEach((d) => { d.alive = false; d.m.visible = false; }); },
    dispose() { geo.dispose(); pool.forEach((d) => { parent.remove(d.m); d.m.material.dispose(); }); },
  };
}

/** A white glazed tile to stand the flask on, so a faint colour shows. */
export function whiteTile() {
  return mesh(new THREE.BoxGeometry(1.2, 0.04, 1.2), MAT.gloss(0xfcfcfa), [0, 0.02, 0]);
}

/** A small glass funnel. */
export function funnel() {
  const prof = [V2(0.012, 0), V2(0.012, 0.3), V2(0.022, 0.34), V2(0.22, 0.6), V2(0.23, 0.62)];
  const m = mesh(new THREE.LatheGeometry(prof, 32), MAT.glass(), null, { cast: false }); m.renderOrder = 5;
  const g = new THREE.Group(); g.add(m); return g;
}

/** A 100 mL beaker with a spout, for waste or reagent. */
export function beaker(fillMl = 0, color = 0xeef6ff) {
  const outer = [V2(0.001, 0), V2(0.24, 0), V2(0.255, 0.015), V2(0.26, 0.05), V2(0.26, 0.86), V2(0.275, 0.9)];
  const { group, inner } = vessel(outer, 0.012, 40);
  const table = volumeTable(inner.slice(0, 5));
  const mat = liquidMaterial(color, 0.45);
  const liq = mesh(new THREE.CylinderGeometry(0.244, 0.244, 1, 32), mat, null, { cast: false }); liq.renderOrder = 3; group.add(liq);
  let v = 0;
  const api = { group, material: mat, get volume() { return v; }, setVolume(x) { v = Math.max(0, x); const h = table.heightOf(v) - 0.012; liq.visible = v > 0.2; liq.scale.y = Math.max(0.001, h); liq.position.y = 0.012 + h / 2; } };
  api.setVolume(fillMl);
  return api;
}
