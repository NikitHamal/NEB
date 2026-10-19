// A test-tube bench for wet tests: a rack of labelled tubes, rows of reagent bottles, a stand
// that holds the tube being worked on, drops that fall from a tilted bottle, a Bunsen flame to
// warm a tube in, and a tube whose look the chemistry decides: colour, cloudiness, a precipitate
// settling, a silver mirror, a separate layer, fizzing. The practical supplies the chemistry;
// the bench only shows it.
import { THREE } from '../engine.js';
import { reagentBottle } from '../bio-handson/props.js';
import { makeTube, makeRack } from '../bio-handson/glassware.js';
import { MAT, mesh } from '../bio-handson/kit.js';
import { sfx, tone } from '../bio-handson/sound.js';
import { screenDist } from './hud.js';
import { createDrops } from './glass.js';
import { makeWaterBath } from '../bio-handson/glassware.js';
import { bunsen } from './burner.js';

sfx.register('drip', () => { tone(1250 + Math.random() * 300, 0.07, { gain: 0.06, slide: 0.55 }); });

export function createTubeBench(ctx, { hud = null, reagents, order, tubes = 4, labels, burner = false, bath = false, cols = 4, bottleScale = 0.72, rackAt = [-1.5, -0.25], bottlesAt = [-0.15, -0.8], holdAt = [1.05, 0.35], burnerAt = [2.05, -0.2] }) {
  const { world, anim, fx } = ctx;
  const bench = mesh(new THREE.BoxGeometry(5.2, 0.02, 2.4), MAT.matte(0x2f3640), [0.2, 0.01, 0]); world.add(bench); ctx.surfaces.push(bench);
  const rack = makeRack(tubes); rack.group.position.set(rackAt[0], 0.02, rackAt[1]); world.add(rack.group);
  const T = []; for (let i = 0; i < tubes; i++) { const t = makeTube(labels ? labels[i] : String(i + 1)); t.group.position.copy(rack.slots[i]).add(rack.group.position); world.add(t.group); T.push(t); }
  const bottles = {}; const tags = [];
  order.forEach((k, i) => {
    const r = reagents[k]; const b = reagentBottle(r.short, r.color, r.sub || '', { amber: r.amber });
    b.scale.setScalar(bottleScale); b.position.set(bottlesAt[0] + (i % cols) * 0.42, 0, bottlesAt[1] + Math.floor(i / cols) * 0.42); world.add(b); bottles[k] = b;
    if (hud) { const c = hud.chip('ho-tag').set(r.tag || r.short).show(true); c.at.set(b.position.x, ctx.BENCH_Y + 0.62 * bottleScale, b.position.z); c.dx = -14; c.dy = -10; tags.push(c); }
  });
  const HOLD = new THREE.Vector3(holdAt[0], 0.1, holdAt[1]);
  const stand = new THREE.Group(); stand.position.set(HOLD.x, 0, HOLD.z - 0.16); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(0.5, 0.04, 0.4), MAT.matte(0x24323a), [0, 0.02, 0.1]));
  stand.add(mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.5, 12), MAT.steel(), [0, 0.75, 0]));
  stand.add(mesh(new THREE.BoxGeometry(0.06, 0.06, 0.2), MAT.matte(0x30363d), [0, 1.0, 0.08]));
  stand.add(mesh(new THREE.TorusGeometry(0.085, 0.012, 6, 20), MAT.steel(), [0, 1.0, 0.16]).rotateX(Math.PI / 2));
  let flame = null;
  if (burner) { flame = bunsen(ctx.quality); flame.group.position.set(burnerAt[0], 0, burnerAt[1]); flame.group.rotation.y = Math.PI / 2; world.add(flame.group); flame.setAir(0.9); }
  let wb = null;
  if (bath) { wb = makeWaterBath(); wb.position.set(burnerAt[0], 0, burnerAt[1]); world.add(wb); wb.userData.flame.visible = true; }
  const drops = createDrops(world, 8);
  const mirrorMat = new THREE.MeshStandardMaterial({ color: 0xd9dde2, metalness: 1, roughness: 0.12, transparent: true, opacity: 0 });
  const mirror = mesh(new THREE.CylinderGeometry(0.071, 0.071, 0.5, 20, 1, true), mirrorMat, null, { cast: false }); mirror.visible = false;
  const layer = mesh(new THREE.CylinderGeometry(0.066, 0.066, 0.12, 20), MAT.liquid(0xf3eee0, 0.75), null, { cast: false }); layer.visible = false;
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x5b3214, transparent: true, opacity: 0 });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.066, 0.012, 6, 24), ringMat); ring.rotation.x = Math.PI / 2; ring.visible = false;
  const st = { tube: null, idx: -1, busy: false, fizz: 0, fizzColor: 0xffffff, heating: false };
  const tmp = new THREE.Vector3();

  const api = {
    tags, showTags(on) { tags.forEach((c) => c.show(on)); },
    tubes: T, bottles, rack, HOLD, flame, stand, bath: wb,
    get tube() { return st.tube; },
    get busy() { return st.busy; },
    /** Brings tube i to the stand, empty and clean unless keep. */
    bring(i, keep = false) {
      const t = T[i]; st.tube = t; st.idx = i;
      if (!keep) { t.setFill(0); t.material.color.set(0xeef6ff); t.material.opacity = 0.55; }
      const from = t.group.position.clone();
      anim.add(0.8, (k) => { t.group.position.lerpVectors(from, HOLD, k); t.group.position.y += Math.sin(k * Math.PI) * 0.4; }, { done: () => sfx.play('glass') });
      t.group.add(mirror, layer, ring); mirror.visible = layer.visible = ring.visible = false; mirrorMat.opacity = 0; ringMat.opacity = 0;
      return t;
    },
    putBack() {
      const t = st.tube; if (!t) return; const to = rack.slots[st.idx].clone().add(rack.group.position);
      const from = t.group.position.clone(); anim.add(0.7, (k) => { t.group.position.lerpVectors(from, to, k); t.group.position.y += Math.sin(k * Math.PI) * 0.35; });
      st.tube = null; st.idx = -1;
    },
    /** Which bottle (of allowed) the pointer is on, if any. */
    bottleAt(p, allowed) {
      const list = allowed.map((k) => bottles[k]).filter(Boolean); const h = ctx.input.pick(list, true, false);
      if (h) { let o = h.object; while (o && !list.includes(o)) o = o.parent; if (o) return allowed.find((k) => bottles[k] === o); }
      let best = null; let bd = 46 * (p.touch ? 1.35 : 1);
      for (const k of allowed) { const b = bottles[k]; if (!b) continue; const d = screenDist(ctx, b, p, 0.3 * b.scale.y); if (d < bd) { bd = d; best = k; } }
      return best;
    },
    /** Tilts bottle k over the held tube and lets n drops fall; done() after they land. */
    pour(k, n, done, color) {
      if (st.busy || !st.tube) return false; st.busy = true;
      const b = bottles[k]; const home = b.position.clone(); const rz = b.rotation.z; const tag = hud ? tags[order.indexOf(k)] : null; if (tag) tag.show(false);
      const over = HOLD.clone().add(new THREE.Vector3(-0.32, 1.45, 0));
      anim.add(0.5, (e) => { b.position.lerpVectors(home, over, e); b.rotation.z = rz - 1.9 * e; }, { done: () => {
        let c = 0;
        const one = () => {
          b.localToWorld(tmp.set(0.06, 0.55, 0)); world.worldToLocal(tmp);
          drops.spawn(tmp, HOLD.y + 0.12 + st.tube.fill * 1.1, () => sfx.play('drip'), color ?? reagents[k].color);
          if (++c < n) anim.wait(0.14, one);
        };
        one();
        anim.wait(0.45 + n * 0.14, () => {
          anim.add(0.45, (e) => { b.position.lerpVectors(over, home, e); b.rotation.z = rz - 1.9 * (1 - e); }, { done: () => { st.busy = false; if (tag) tag.show(true); } });
          if (done) done();
        });
      } });
      return true;
    },
    /** Applies what the chemistry says the tube looks like now. */
    look(L) {
      const t = st.tube; if (!t || !L) return;
      t.to(anim, { fill: L.fill ?? Math.min(0.6, t.fill + 0.05), color: L.color ?? t.material.color.getHex(), dur: L.dur ?? 1.2, opacity: L.opacity ?? 0.5 });
      if (L.ppt) t.precipitate(anim, L.ppt.color, L.ppt.amount ?? 1);
      if (L.ppt === null) t.precipitate(anim, 0xffffff, 0.01);
      if (L.fizz) { st.fizz = L.fizz; st.fizzColor = L.fizzColor ?? 0xffffff; }
      if (L.mirror) { mirror.visible = true; mirror.position.y = 0.075 + 0.25; anim.add(3, (e) => { mirrorMat.opacity = 0.92 * e; }, { delay: 0.6 }); }
      if (L.layer) { layer.visible = true; layer.material = MAT.liquid(L.layer, 0.8); layer.position.y = 0.075 + 0.06; }
      if (L.ring) { ring.visible = true; ringMat.color.set(L.ring); ring.position.y = 0.075 + 0.13; anim.add(2.5, (e) => { ringMat.opacity = 0.9 * e; }, { delay: 0.6 }); }
    },
    /** Warms the held tube in the flame for `secs`, then brings it back. */
    heat(secs, done) {
      if ((!flame && !wb) || !st.tube || st.busy) return false; st.busy = true; const t = st.tube;
      if (flame && !wb && !flame.lit) { flame.setGas(1); flame.light(); sfx.play('whoosh'); }
      const from = t.group.position.clone(); const to = wb ? new THREE.Vector3(wb.position.x, 0.45, wb.position.z) : new THREE.Vector3(flame.group.position.x, flame.top + 0.3, flame.group.position.z);
      const tilt = wb ? 0 : -0.5; const lift = wb ? 0.9 : 0;
      anim.add(0.7, (k) => { t.group.position.lerpVectors(from, to, k); t.group.position.y += Math.sin(k * Math.PI) * lift; t.group.rotation.z = tilt * k; }, { done: () => {
        st.heating = true; anim.wait(secs, () => { st.heating = false; anim.add(0.7, (k) => { t.group.position.lerpVectors(to, from, k); t.group.position.y += Math.sin(k * Math.PI) * lift; t.group.rotation.z = tilt * (1 - k); }, { done: () => { st.busy = false; if (done) done(); } }); });
      } });
      return true;
    },
    update(dt, t) {
      drops.update(dt);
      if (flame) flame.update(dt, t);
      if (st.fizz > 0 && st.tube) {
        st.fizz -= dt; st.tube.top(tmp); tmp.y -= 0.12;
        if (Math.random() < dt * 30) fx.burst(tmp, st.fizzColor, 2, 0.12, tmp.y - 0.3);
      }
      if (st.heating && st.tube && Math.random() < dt * 12) { st.tube.top(tmp); fx.burst(tmp, 0xffffff, 1, 0.08, tmp.y - 0.2); }
    },
    dispose() { drops.dispose(); },
  };
  return api;
}
