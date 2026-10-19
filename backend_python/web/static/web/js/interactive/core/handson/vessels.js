// More glassware at true size (1 unit = 10 cm) and the act of pouring: a 100 mL measuring
// cylinder whose printed scale is read by tapping at the bottom of the meniscus, and a pour that
// carries a vessel over another, tilts it and runs a stream for as long as the student holds on.
import { THREE } from '../engine.js';
import { MAT, mesh, canvasTexture } from '../bio-handson/kit.js';
import { liquidMaterial } from './glass.js';

/** A 100 mL measuring cylinder (1 mL divisions). set(ml); reader.tap() gives the value at a tap. */
export function measuringCylinder({ cap = 100, color = 0xe8f2fb } = {}) {
  const g = new THREE.Group(); const R = 0.135; const H = cap / (Math.PI * R * R * 1000); const y0 = 0.12;
  const foot = new THREE.Shape(); for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2; const fn = i ? 'lineTo' : 'moveTo'; foot[fn](Math.cos(a) * 0.3, Math.sin(a) * 0.3); }
  const fg = new THREE.ExtrudeGeometry(foot, { depth: 0.06, bevelEnabled: false }); fg.rotateX(-Math.PI / 2);
  g.add(mesh(fg, MAT.glassEdge(), null, { cast: false }));
  const tube = mesh(new THREE.CylinderGeometry(R + 0.012, R + 0.012, H + 0.35, 28, 1, true), MAT.glass(), [0, y0 + (H + 0.35) / 2 - 0.06, 0], { cast: false }); tube.renderOrder = 5; g.add(tube);
  g.add(mesh(new THREE.CircleGeometry(R + 0.012, 28), MAT.glass(), [0, y0 - 0.06, 0], { cast: false }).rotateX(-Math.PI / 2));
  const lip = mesh(new THREE.TorusGeometry(R + 0.016, 0.01, 6, 28), MAT.glassEdge(), [0, y0 + H + 0.29, 0], { cast: false }); lip.rotation.x = Math.PI / 2; g.add(lip);
  const TH = 2048; const pad = 40;
  const tex = canvasTexture(`ho-mcyl:${cap}`, 192, TH, (c, w, h) => {
    c.clearRect(0, 0, w, h); c.fillStyle = 'rgba(15,23,42,.95)';
    for (let ml = 0; ml <= cap; ml++) { const y = h - pad - (h - 2 * pad) * ml / cap; const big = ml % 10 === 0; const mid = ml % 5 === 0; c.fillRect(0, Math.round(y - 2), big ? 96 : mid ? 66 : 40, 4); if (big && ml) { c.font = '800 46px system-ui, sans-serif'; c.textBaseline = 'middle'; c.fillText(String(ml), 104, y); } }
    c.font = '700 26px system-ui, sans-serif'; c.fillText('mL', 104, pad + 70); c.fillText('20°C', 104, pad + 104);
  }, { anisotropy: 16 });
  const sh = H * TH / (TH - 2 * pad);
  const scale = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.0135, R + 0.0135, sh, 24, 1, true, -0.5, 1.0), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
  scale.position.y = y0 + H / 2; scale.renderOrder = 6; g.add(scale);
  const mat = liquidMaterial(color, 0.45);
  const liq = mesh(new THREE.CylinderGeometry(R, R, 1, 24), mat, null, { cast: false }); liq.renderOrder = 3; g.add(liq);
  const men = mesh(new THREE.CylinderGeometry(R + 0.001, R + 0.001, 0.012, 24, 1, true), new THREE.MeshBasicMaterial({ color: 0x1e293b, transparent: true, opacity: 0.45, depthWrite: false }), null, { cast: false }); men.renderOrder = 4; g.add(men);
  let vol = 0;
  const yOf = (ml) => y0 + H * ml / cap;
  function set(ml) { vol = Math.max(0, Math.min(cap * 1.12, ml)); const h = Math.max(0.001, yOf(vol) - y0 + 0.06); liq.visible = men.visible = vol > 0.2; liq.scale.y = h; liq.position.y = y0 - 0.06 + h / 2; men.position.y = yOf(vol) - 0.004; }
  set(0);
  const plane = new THREE.Plane(); const hit = new THREE.Vector3(); const p = new THREE.Vector3(); const nrm = new THREE.Vector3();
  const mark = mesh(new THREE.BoxGeometry(0.06, 0.003, 0.003), new THREE.MeshBasicMaterial({ color: 0xdc2626, depthTest: false }), null, { cast: false }); mark.renderOrder = 20; mark.visible = false; g.add(mark);
  return {
    group: g, material: mat, liquid: liq, cap, R,
    get volume() { return vol; }, set, yOf, topY: y0 + H + 0.29, levelY: () => yOf(vol),
    reader(ctx) {
      return {
        tap() {
          g.getWorldPosition(p); ctx.camera.getWorldDirection(nrm); nrm.y = 0; nrm.normalize().negate(); p.addScaledVector(nrm, R);
          plane.setFromNormalAndCoplanarPoint(nrm, p);
          if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return null; g.worldToLocal(hit);
          if (Math.hypot(hit.x, hit.z) > R * 2.5) return null;
          const ml = Math.round(((hit.y - y0) / H * cap) * 2) / 2; if (ml < 0 || ml > cap) return null;
          mark.visible = true; mark.position.set(hit.x, yOf(ml), hit.z);
          return ml;
        },
        hide() { mark.visible = false; },
      };
    },
  };
}

/**
 * Pouring: the vessel flies to `over` (or to where its lip lands on lipAt()) and tilts; while held, `flow(dt)` is called and a stream runs
 * from its lip down to targetY(). stop() returns it home.
 */
export function createPour(ctx, { vessel, over = new THREE.Vector3(), lipAt = null, tilt = 1.9, lip = new THREE.Vector3(0.3, 0.9, 0), color = 0xe8f2fb, flow, targetY, id = 'pour' }) {
  const stream = mesh(new THREE.CylinderGeometry(0.014, 0.01, 1, 8), MAT.liquid(color, 0.65), null, { cast: false }); stream.visible = false; stream.renderOrder = 6; ctx.world.add(stream);
  const home = vessel.position.clone(); const homeRot = vessel.rotation.z;
  let on = false; let ready = false; const lp = new THREE.Vector3();
  const api = {
    get on() { return on; },
    stream,
    setHome(v) { home.copy(v); },
    start() {
      if (on) return; on = true; ready = false; const from = vessel.position.clone(); const r0 = vessel.rotation.z;
      if (lipAt) { const sc = vessel.scale.x; const c = Math.cos(tilt); const s = Math.sin(tilt); const L = lipAt(); over.set(L.x - sc * (lip.x * c - lip.y * s), L.y - sc * (lip.x * s + lip.y * c), L.z - sc * lip.z); }
      ctx.anim.add(0.55, (k) => { vessel.position.lerpVectors(from, over, k); vessel.rotation.z = r0 + (tilt - r0) * k; }, { id, done: () => { ready = true; } });
    },
    stop(done) {
      if (!on) { if (done) done(); return; } on = false; ready = false; stream.visible = false; const from = vessel.position.clone(); const r0 = vessel.rotation.z;
      ctx.anim.add(0.55, (k) => { vessel.position.lerpVectors(from, home, k); vessel.rotation.z = r0 + (homeRot - r0) * k; }, { id, done });
    },
    update(dt) {
      if (!on || !ready) return;
      const more = flow(dt);
      if (more === false) { api.stop(); return; }
      lp.copy(lip); vessel.localToWorld(lp); ctx.world.worldToLocal(lp);
      const ty = targetY(); stream.visible = true; stream.scale.y = Math.max(0.01, lp.y - ty); stream.position.set(lp.x, (lp.y + ty) / 2, lp.z);
    },
    dispose() { ctx.world.remove(stream); stream.geometry.dispose(); },
  };
  return api;
}
