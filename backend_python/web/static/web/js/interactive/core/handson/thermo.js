// Heat apparatus at true size (1 unit = 10 cm): a mercury-in-glass thermometer whose printed scale
// the student reads by tapping (the column follows set(T) with a little lag, as the bulb does), a
// copper calorimeter with stirrer in its insulating jacket, a polystyrene cup with a lid, and a
// top-pan electronic balance with a TARE key and a display that settles after each load.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';

/** A thermometer from min to max °C, `div` °C per division, scale length `len` units. */
export function thermometer({ min = -10, max = 110, div = 1, len = 2.4, label = '' } = {}) {
  const g = new THREE.Group();
  const span = max - min; const per = len / span; const y0 = 0.22;
  const stem = mesh(new THREE.CylinderGeometry(0.032, 0.032, len + 0.45, 16), MAT.glass(), [0, y0 + (len + 0.45) / 2 - 0.12, 0], { cast: false }); stem.renderOrder = 5; g.add(stem);
  g.add(mesh(new THREE.SphereGeometry(0.032, 14, 10), MAT.glass(), [0, y0 + len + 0.33, 0], { cast: false }));
  const bulb = mesh(new THREE.CylinderGeometry(0.026, 0.02, 0.18, 14), MAT.gloss(0xb8bfc8), [0, 0.11, 0]); g.add(bulb);
  g.add(mesh(new THREE.SphereGeometry(0.02, 12, 8), MAT.gloss(0xb8bfc8), [0, 0.02, 0]));
  const colMat = new THREE.MeshStandardMaterial({ color: 0xc0c7cf, metalness: 1, roughness: 0.2 });
  const col = mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 8), colMat, null, { cast: false }); g.add(col);
  const W = 256; const H = 4096; const pad = 60;
  const tex = canvasTexture(`ho-th:${min}:${max}:${div}`, W, H, (c, w, h) => {
    c.fillStyle = '#fbfaf3'; c.fillRect(0, 0, w, h); c.fillStyle = '#0b0f14';
    const n = Math.round(span / div);
    const every = div < 0.5 ? 5 : 10; const numEvery = div < 0.5 ? 1 : (span > 60 ? 10 : 5);
    for (let i = 0; i <= n; i++) {
      const t = min + i * div; const y = h - pad - (h - 2 * pad) * (i / n);
      const big = i % every === 0; const mid = i % (every / 2) === 0;
      c.fillRect(0, Math.round(y - (big ? 3 : 2)), big ? 120 : mid ? 84 : 52, big ? 6 : 4);
      if (big && Math.abs(Math.round(t / numEvery) * numEvery - t) < 1e-6) { c.font = '800 64px system-ui, sans-serif'; c.textBaseline = 'middle'; c.fillText(String(Math.round(t * 10) / 10), 132, y); }
    }
    c.font = '700 40px system-ui, sans-serif'; c.save(); c.translate(200, pad + 40); c.fillText('°C', 0, 0); c.restore();
  }, { anisotropy: 16 });
  const plate = mesh(new THREE.PlaneGeometry(0.05, len * H / (H - 2 * pad)), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6 }), [0.008, y0 + len / 2, 0.012]); g.add(plate);
  if (label) g.userData.label = label;
  let T = 20; let shown = 20;
  const yOf = (t) => y0 + (t - min) * per;
  function draw() { const h = Math.max(0.001, yOf(Math.max(min - 2, Math.min(max + 2, shown))) - 0.18); col.scale.y = h; col.position.set(0, 0.18 + h / 2, 0.022); }
  draw();
  return {
    group: g, plate, stem, min, max, div, yOf,
    get reading() { return shown; },
    set(t, snap = false) { T = t; if (snap) { shown = t; draw(); } },
    /** The bulb responds with a time constant of a few seconds. */
    update(dt, tau = 2.5) { shown += (T - shown) * (1 - Math.exp(-dt / tau)); draw(); },
    /** °C at a local height on the stem. */
    tempAt(y) { return min + (y - y0) / per; },
  };
}

/** Tap-to-read helper for a thermometer: returns the value nearest to the tap, to half a division. */
export function thermoReader(ctx, th) {
  const plane = new THREE.Plane(); const hit = new THREE.Vector3(); const n = new THREE.Vector3(); const p = new THREE.Vector3();
  const mark = mesh(new THREE.BoxGeometry(0.11, 0.004, 0.004), new THREE.MeshBasicMaterial({ color: 0x2563eb, depthTest: false }), null, { cast: false }); mark.renderOrder = 20; mark.visible = false; th.group.add(mark);
  return {
    mark,
    tap() {
      th.plate.getWorldPosition(p); n.set(0, 0, 1).applyQuaternion(th.plate.getWorldQuaternion(new THREE.Quaternion()));
      plane.setFromNormalAndCoplanarPoint(n, p);
      if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return null;
      th.group.worldToLocal(hit); if (Math.abs(hit.x) > 0.12) return null;
      const t = th.tempAt(hit.y); if (t < th.min - th.div || t > th.max + th.div) return null;
      const step = th.div / 2; const v = Math.round(t / step) * step;
      mark.visible = true; mark.position.set(0.02, th.yOf(v), 0.02);
      return Math.round(v * 100) / 100;
    },
    hide() { mark.visible = false; },
  };
}

/** A copper calorimeter with a copper stirrer, standing in a lagged wooden jacket with a lid. */
export function calorimeter() {
  const g = new THREE.Group();
  const copper = new THREE.MeshStandardMaterial({ color: 0xd08a5c, metalness: 1, roughness: 0.28, side: THREE.DoubleSide });
  const cup = new THREE.Group(); g.add(cup);
  cup.add(mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.95, 40, 1, true), copper, [0, 0.5, 0]));
  cup.add(mesh(new THREE.CircleGeometry(0.4, 40), copper, [0, 0.03, 0]).rotateX(-Math.PI / 2));
  cup.add(mesh(new THREE.TorusGeometry(0.4, 0.012, 6, 40), copper, [0, 0.975, 0]).rotateX(Math.PI / 2));
  const water = mesh(new THREE.CylinderGeometry(0.39, 0.39, 1, 36), MAT.liquid(0xcfe6f5, 0.5), null, { cast: false }); water.renderOrder = 3; water.visible = false; cup.add(water);
  const stirrer = new THREE.Group(); cup.add(stirrer);
  stirrer.add(mesh(new THREE.TorusGeometry(0.28, 0.012, 6, 32), copper, [0, 0.12, 0]).rotateX(Math.PI / 2));
  stirrer.add(mesh(new THREE.CylinderGeometry(0.01, 0.01, 1.2, 8), copper, [0.28, 0.7, 0]));
  stirrer.add(mesh(new THREE.SphereGeometry(0.03, 10, 8), MAT.gloss(0x111827), [0.28, 1.3, 0]));
  const jacket = new THREE.Group(); g.add(jacket);
  const wood = MAT.gloss(0x7a4a26);
  jacket.add(mesh(new THREE.CylinderGeometry(0.62, 0.62, 1.1, 40, 1, true), wood, [0, 0.55, 0]));
  jacket.add(mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.04, 40), wood, [0, 0.02, 0]));
  jacket.add(mesh(new THREE.RingGeometry(0.41, 0.62, 40), MAT.matte(0x4b3420), [0, 1.1, 0]).rotateX(-Math.PI / 2));
  const lid = new THREE.Group(); lid.position.y = 1.12;
  const lidShape = new THREE.Shape(); lidShape.absarc(0, 0, 0.64, 0, Math.PI * 2);
  [[-0.12, 0.05], [0.28, 0]].forEach(([x, z]) => { const h = new THREE.Path(); h.absarc(x, z, 0.05, 0, Math.PI * 2, true); lidShape.holes.push(h); });
  const lg = new THREE.ExtrudeGeometry(lidShape, { depth: 0.04, bevelEnabled: false }); lg.rotateX(-Math.PI / 2);
  lid.add(mesh(lg, wood)); g.add(lid);
  return {
    group: g, cup, water, stirrer, lid,
    setWater(ml) { const h = ml / 1000 / (Math.PI * 0.39 * 0.39); water.visible = ml > 1; water.scale.y = Math.max(0.001, h); water.position.y = 0.03 + h / 2; },
    waterTop(ml) { return 0.03 + ml / 1000 / (Math.PI * 0.39 * 0.39); },
  };
}

/** A polystyrene (thermocol) cup with a lid, for solution calorimetry. */
export function foamCup() {
  const g = new THREE.Group();
  const foam = new THREE.MeshStandardMaterial({ color: 0xf8f8f4, roughness: 0.95, side: THREE.DoubleSide });
  const pts = [new THREE.Vector2(0.001, 0), new THREE.Vector2(0.27, 0), new THREE.Vector2(0.4, 1.1), new THREE.Vector2(0.43, 1.13)];
  g.add(mesh(new THREE.LatheGeometry(pts, 40), foam));
  const liq = mesh(new THREE.CylinderGeometry(1, 1, 1, 32), MAT.liquid(0xe8f2fb, 0.55), null, { cast: false }); liq.visible = false; liq.renderOrder = 3; g.add(liq);
  const lid = new THREE.Group();
  const lidShape = new THREE.Shape(); lidShape.absarc(0, 0, 0.45, 0, Math.PI * 2); const hole = new THREE.Path(); hole.absarc(0, 0, 0.045, 0, Math.PI * 2, true); lidShape.holes.push(hole);
  const lg = new THREE.ExtrudeGeometry(lidShape, { depth: 0.04, bevelEnabled: false }); lg.rotateX(-Math.PI / 2);
  lid.add(mesh(lg, foam)); g.add(lid);
  const rAt = (y) => 0.27 + (0.13 * y / 1.1);
  let vol = 0;
  return {
    group: g, lid, liquid: liq,
    get volume() { return vol; },
    setVolume(ml) {
      vol = ml; let lo = 0; let hi = 1.1;
      for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; const r = rAt(m / 2); const v = Math.PI * r * r * m * 1000; if (v < ml) lo = m; else hi = m; }
      const h = (lo + hi) / 2; const r = rAt(h / 2) - 0.012; liq.visible = ml > 1; liq.scale.set(r, Math.max(0.001, h), r); liq.position.y = h / 2 + 0.01;
    },
    levelY() { let lo = 0; let hi = 1.1; for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; const r = rAt(m / 2); if (Math.PI * r * r * m * 1000 < vol) lo = m; else hi = m; } return lo; },
  };
}

/** A top-pan electronic balance reading to 0.01 g. set(grams on pan); tare(); the display settles. */
export function balance() {
  const g = new THREE.Group();
  g.add(mesh(new THREE.BoxGeometry(0.95, 0.2, 1.15), MAT.gloss(0xe5e7eb), [0, 0.1, 0]));
  g.add(mesh(new THREE.BoxGeometry(0.95, 0.12, 0.3), MAT.gloss(0xd1d5db), [0, 0.16, 0.45]).rotateX(-0.25));
  const pan = mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.02, 36), MAT.steel(), [0, 0.23, -0.08]); g.add(pan);
  const cv = document.createElement('canvas'); cv.width = 256; cv.height = 64; const c2 = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); if (tex.colorSpace !== undefined) tex.colorSpace = THREE.SRGBColorSpace;
  const disp = mesh(new THREE.PlaneGeometry(0.42, 0.105), new THREE.MeshBasicMaterial({ map: tex }), [-0.12, 0.225, 0.47]); disp.rotation.x = -Math.PI / 2 + 0.3; g.add(disp);
  const tareBtn = mesh(new THREE.BoxGeometry(0.14, 0.03, 0.08), MAT.gloss(0x2563eb), [0.3, 0.215, 0.47]); g.add(tareBtn);
  const lbl = mesh(new THREE.PlaneGeometry(0.14, 0.05), new THREE.MeshBasicMaterial({ map: canvasTexture('ho-bal-tare', 96, 32, (c, w, h) => { c.fillStyle = '#e5e7eb'; c.fillRect(0, 0, w, h); c.fillStyle = '#111827'; c.font = '800 20px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText('TARE', w / 2, 23); }) }), [0.3, 0.245, 0.56]); lbl.rotation.x = -Math.PI / 2 + 0.25; g.add(lbl);
  let load = 0; let zero = 0; let shown = 0; let txt = '';
  function paint() {
    const v = Math.round(shown * 100) / 100; const s = `${v.toFixed(2)} g`; if (s === txt) return; txt = s;
    c2.fillStyle = '#9fb59a'; c2.fillRect(0, 0, 256, 64); c2.fillStyle = '#0f1a0f'; c2.font = '700 44px ui-monospace, Menlo, monospace'; c2.textAlign = 'right'; c2.fillText(s, 246, 48); tex.needsUpdate = true;
  }
  paint();
  return {
    group: g, pan, tareBtn, panY: 0.24,
    set(grams) { load = grams; },
    tare() { zero = load; },
    get reading() { return Math.round((load - zero) * 100) / 100; },
    get shown() { return Math.round(shown * 100) / 100; },
    display: disp,
    get settled() { return Math.abs(shown - (load - zero)) < 0.006; },
    update(dt) { shown += ((load - zero) - shown) * (1 - Math.exp(-dt / 0.35)); paint(); },
  };
}

/** Rising, fading puffs of steam (or smoke). emit(at local to parent, rate per second) each frame. */
export function steamPuffs(parent, n = 24, color = 0xffffff) {
  const tex = canvasTexture('ho-puff', 64, 64, (c, w, h) => { const gr = c.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = gr; c.fillRect(0, 0, w, h); });
  const pool = [];
  for (let i = 0; i < n; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, color, transparent: true, opacity: 0, depthWrite: false })); s.visible = false; s.renderOrder = 15; parent.add(s); pool.push({ s, t: 0, life: 1, v: new THREE.Vector3() }); }
  let acc = 0;
  return {
    emit(at, rate, dt, spread = 0.05, rise = 0.5) {
      acc += rate * dt;
      while (acc >= 1) { acc -= 1; const p = pool.find((q) => !q.s.visible); if (!p) break; p.s.visible = true; p.t = 0; p.life = 1.2 + Math.random() * 0.8; p.s.position.copy(at).add(new THREE.Vector3((Math.random() - 0.5) * spread, 0, (Math.random() - 0.5) * spread)); p.v.set((Math.random() - 0.5) * 0.1, rise * (0.7 + Math.random() * 0.6), (Math.random() - 0.5) * 0.1); }
    },
    update(dt) {
      for (const p of pool) {
        if (!p.s.visible) continue; p.t += dt; const k = p.t / p.life;
        if (k >= 1) { p.s.visible = false; continue; }
        p.s.position.addScaledVector(p.v, dt); const sc = 0.08 + k * 0.35; p.s.scale.set(sc, sc, sc); p.s.material.opacity = 0.45 * Math.sin(Math.PI * Math.min(1, k * 1.3));
      }
    },
    dispose() { pool.forEach((p) => { parent.remove(p.s); p.s.material.dispose(); }); },
  };
}
