import { THREE } from '../../core/engine.js';
import { clamp, smooth, lerp, easeInOut, makeCanvas, canvasTexture } from './kit.js';
import { leafHalfWidth, leafUvToCanvas } from './textures.js';
import { CAT_LENGTH } from './caterpillar.js';

const UP = new THREE.Vector3(0, 1, 0);
const BINS = 120;

function createBites(hero, tier) {
  const size = tier === 'high' ? 512 : 256;
  const canvas = makeCanvas(size); const g = canvas.getContext('2d');
  const tex = canvasTexture(canvas, { color: false, anisotropy: 1 });
  const mat = hero.material;
  mat.alphaMap = tex; mat.alphaTest = 0.5; mat.needsUpdate = true;
  const L = hero.leaf.len;
  const depth = new Float32Array(BINS);
  function reset() { g.fillStyle = '#fff'; g.fillRect(0, 0, size, size); depth.fill(0); tex.needsUpdate = true; }
  function bite(u, d, side, r) {
    const hw = leafHalfWidth(u) * L;
    const cx = side * (hw + r - d);
    const [px, py] = leafUvToCanvas(cx / L, u, size);
    g.fillStyle = '#000';
    g.beginPath(); g.ellipse(px, py, (r / L / 0.6) * size, (r / L) * size, 0, 0, Math.PI * 2); g.fill();
    for (let i = 0; i < BINS; i++) {
      const du = (i / (BINS - 1) - u) * L;
      if (Math.abs(du) < r) depth[i] = Math.max(depth[i], d - (r - Math.sqrt(r * r - du * du)));
    }
    tex.needsUpdate = true;
  }
  const depthAt = (u) => depth[Math.round(clamp(u) * (BINS - 1))];
  reset();
  return { reset, bite, depthAt, texture: tex };
}

export function createDirector(ctx) {
  const { plant, egg, cat, chry, adult, scene, tier, onStatus } = ctx;
  let rig = ctx.rig;
  const heroCat = plant.heroes.caterpillar; const heroEgg = plant.heroes.egg;
  const catSurf = heroCat.surface; const L = heroCat.leaf.len;
  const bites = createBites(heroCat, tier);
  const side = 1;

  const eggU = 0.42; const eggV = -0.28;
  const eP = heroEgg.surface.surf(eggU, eggV); const eN = heroEgg.surface.normal(eggU, eggV);
  egg.group.position.copy(eP).addScaledVector(eN, -0.004);
  egg.group.quaternion.setFromUnitVectors(UP, eN.clone().negate());
  heroEgg.holder.add(egg.group);
  heroCat.holder.add(cat.group);

  const anchor = new THREE.Group();
  anchor.position.copy(plant.chrysalisAnchor.position);
  const tan = plant.chrysalisAnchor.tangent.clone(); tan.y = 0; tan.normalize();
  anchor.quaternion.setFromUnitVectors(new THREE.Vector3(1, 0, 0), tan);
  plant.group.add(anchor);
  anchor.add(chry.group);

  const st = {
    mode: 'adult', day: 30, scale: 1, headU: 0.66, crawlBase: 0, chew: 0, nextCrawl: 3, develop: 0.15,
    mature: 0, empty: 0, cycle: null, seq: null, follow: null, flight: null, perchT: 0, wingT: 0,
  };

  const catPath = (d, swing, outP, outN) => {
    const Lb = CAT_LENGTH * st.scale * 0.95;
    const tailY = st.headU * L - Lb;
    const u = clamp((tailY + d) / L, 0.02, 0.96);
    const hw = leafHalfWidth(u) * L;
    const x0 = side * Math.max(0.2, hw - (0.42 + 0.6 * st.scale));
    const x = x0 + side * swing;
    const v = clamp(x / Math.max(0.01, hw), -0.97, 0.97);
    catSurf.surf(u, v, outP); catSurf.normal(u, v, outN);
  };
  const jPath = (d, swing, outP, outN) => {
    const Lb = CAT_LENGTH * st.scale;
    const straight = Lb * 0.55; const R = Lb * 0.2;
    if (d < straight) { outP.set(0, -d - 0.05, 0); outN.set(0, 0, 1); return; }
    const phi = (d - straight) / R;
    outP.set(0, -straight - 0.05 - R * Math.sin(phi), -R + R * Math.cos(phi));
    outN.set(0, -Math.sin(phi), Math.cos(phi));
  };

  function seedNotch(span, maxDepth) {
    bites.reset();
    const u1 = st.headU + 0.03; const u0 = u1 - span;
    for (let i = 0; i <= 28; i++) {
      const t = i / 28;
      const u = lerp(u0, u1, t);
      bites.bite(u, maxDepth * Math.sin(Math.PI * Math.min(1, t * 1.1)) * (0.85 + 0.15 * Math.sin(i * 2.7)), side, 0.32);
    }
  }

  function perchPose() {
    const per = plant.perch;
    const up = per.axis.clone().normalize();
    const hint = new THREE.Vector3(1, 0, -0.3);
    const fwd = hint.addScaledVector(up, -hint.dot(up)).normalize();
    const X = new THREE.Vector3().crossVectors(up, fwd);
    const quat = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(X, up, fwd));
    const pos = per.position.clone().addScaledVector(up, 0.6).addScaledVector(fwd, -0.55);
    return { pos, quat };
  }
  function placeAdultPerch() {
    plant.perch.group.add(adult.root);
    const { pos, quat } = perchPose();
    adult.root.position.copy(pos); adult.root.quaternion.copy(quat);
    adult.root.scale.setScalar(1);
  }
  function perchWorld() {
    const { pos, quat } = perchPose();
    const g = plant.perch.group; g.updateWorldMatrix(true, false);
    const wq = new THREE.Quaternion(); g.getWorldQuaternion(wq);
    return { pos: pos.applyMatrix4(g.matrixWorld), quat: wq.multiply(quat) };
  }
  function placeAdultHanging() {
    chry.swing.add(adult.root);
    adult.root.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(new THREE.Vector3(-1, 0, 0), new THREE.Vector3(0, 0, 1), new THREE.Vector3(0, 1, 0)));
    adult.root.position.set(0, -2.95, 0.3);
  }

  function setVisible(mode) {
    egg.group.visible = mode === 'egg';
    cat.group.visible = mode === 'caterpillar' || mode === 'jhang';
    chry.group.visible = mode === 'jhang' || mode === 'chrysalis' || mode === 'emerge' || mode === 'flight' || mode === 'adult';
    adult.root.visible = mode === 'emerge' || mode === 'flight' || mode === 'adult';
  }

  const tmp = new THREE.Vector3();
  function worldOf(obj, local = new THREE.Vector3()) { obj.updateWorldMatrix(true, false); return local.clone().applyMatrix4(obj.matrixWorld); }
  function shotFrom(target, dir, r, limits) {
    const d = dir.clone().normalize();
    return { target, r, theta: Math.atan2(d.x, d.z), phi: Math.acos(clamp(d.y, -1, 1)), limits };
  }
  function shot(id) {
    if (id === 'egg') {
      const t = worldOf(egg.group, new THREE.Vector3(0, 0.03, 0));
      const h = heroEgg.holder; h.updateWorldMatrix(true, false);
      const wq = new THREE.Quaternion(); h.getWorldQuaternion(wq);
      const n = eN.clone().applyQuaternion(wq);
      const lat = new THREE.Vector3(1, 0, 0).applyQuaternion(wq);
      if (lat.z < 0) lat.negate();
      return shotFrom(t, n.negate().multiplyScalar(0.42).add(lat), 1.5, { minR: 0.6, maxR: 40, minPhi: 0.2, maxPhi: 2.75 });
    }
    if (id === 'caterpillar' || id === 'hatch') {
      const t = worldOf(heroCat.holder, catSurf.surf(st.headU - 0.12, 0.5));
      return shotFrom(t, new THREE.Vector3(0.55, 0.9, 1), 10.5, { minR: 3, maxR: 70, minPhi: 0.15, maxPhi: 2.6 });
    }
    if (id === 'chrysalis' || id === 'jhang' || id === 'emerge') {
      const t = worldOf(anchor, new THREE.Vector3(0, id === 'emerge' ? -2.4 : id === 'jhang' ? -2.4 : -1.2, 0));
      return shotFrom(t, new THREE.Vector3(0.35, 0.1, 1), id === 'emerge' ? 9 : id === 'jhang' ? 10 : 6.5, { minR: 2, maxR: 70, minPhi: 0.15, maxPhi: 2.6 });
    }
    if (id === 'overview') return shotFrom(new THREE.Vector3(3, 31, 0), new THREE.Vector3(0.5, 0.28, 1), 108, { minR: 10, maxR: 160, minPhi: 0.2, maxPhi: 1.62 });
    const t = worldOf(plant.perch.group, plant.perch.position.clone().addScaledVector(plant.perch.axis, 1.2));
    return shotFrom(t, new THREE.Vector3(0.2, 0.32, 1), 13, { minR: 3, maxR: 90, minPhi: 0.15, maxPhi: 2.4 });
  }

  function enter(mode, opts = {}) {
    st.mode = mode;
    st.seq = null; st.flight = null;
    setVisible(mode);
    if (mode === 'egg') {
      st.develop = opts.develop ?? 0.15; egg.setDevelop(st.develop); egg.setHatched(0);
      bites.reset();
    }
    if (mode === 'caterpillar') {
      heroCat.holder.add(cat.group);
      cat.group.position.set(0, 0, 0); cat.group.quaternion.identity();
      st.scale = opts.scale ?? 1; st.headU = opts.headU ?? 0.66; st.nextCrawl = 2.5;
      if (opts.seed !== false) seedNotch(0.16, 0.95); else bites.reset();
    }
    if (mode === 'jhang') {
      anchor.add(cat.group);
      cat.group.position.set(0, 0, 0); cat.group.quaternion.identity();
      st.scale = 1; chry.group.scale.setScalar(1); chry.swing.scale.setScalar(0.001);
    }
    if (mode === 'chrysalis') {
      chry.swing.scale.setScalar(1); st.mature = opts.mature ?? 0; st.empty = 0;
      chry.setMature(st.mature); chry.setEmpty(0);
      if (opts.seed !== false) seedNotch(0.3, 1.3);
    }
    if (mode === 'emerge') {
      chry.swing.scale.setScalar(1);
      placeAdultHanging();
      st.seq = { t: 0 };
      adult.setCrumple(1); adult.setProboscis(0);
    }
    if (mode === 'adult') {
      chry.swing.scale.setScalar(1); chry.setMature(1); chry.setEmpty(1);
      placeAdultPerch(); adult.setCrumple(0); adult.setLegs(1);
      st.perchT = opts.fresh ? 0 : 3;
      if (opts.seed !== false) seedNotch(0.3, 1.3);
    }
    if (opts.camera !== false) rig.flyTo(shot(mode), opts.camDur ?? 1.9);
  }

  function startFlight(onLand) {
    const startW = new THREE.Vector3(); adult.root.getWorldPosition(startW);
    const startQ = new THREE.Quaternion(); adult.root.getWorldQuaternion(startQ);
    scene.attach(adult.root);
    const pw = perchWorld();
    const endW = pw.pos;
    const above = endW.clone().add(new THREE.Vector3(-3, 6, 4));
    const pts = [startW, startW.clone().add(new THREE.Vector3(2, -2, 7)), new THREE.Vector3(22, 40, 18), new THREE.Vector3(14, 58, -14), new THREE.Vector3(-16, 56, 6), above, endW.clone().add(new THREE.Vector3(-0.6, 1.2, 0.8)), endW];
    const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
    st.flight = { curve, t: 0, dur: curve.getLength() / 34, startQ, endQ: pw.quat, onLand };
    st.mode = 'flight';
    setVisible('flight');
    rig.flyTo(shotFrom(new THREE.Vector3(4, 44, 2), new THREE.Vector3(0.4, 0.3, 1), 70, { minR: 6, maxR: 160, minPhi: 0.15, maxPhi: 2.4 }), 1.4);
  }

  const qTmp = new THREE.Quaternion(); const mTmp = new THREE.Matrix4();
  function updateFlight(dt, time) {
    const f = st.flight;
    f.t += dt;
    const k = clamp(f.t / f.dur);
    const kk = 1 - Math.pow(1 - k, 1.6) * (1 - k * 0.2);
    const p = f.curve.getPointAt(clamp(kk));
    const tg = f.curve.getTangentAt(clamp(kk));
    const bob = Math.sin(time * 14) * 0.35 * (1 - smooth((k - 0.85) / 0.15));
    adult.root.position.copy(p).add(tmp.set(0, bob, 0));
    const fwd = tg.clone();
    const right = new THREE.Vector3().crossVectors(UP, fwd).normalize();
    const up = new THREE.Vector3().crossVectors(fwd, right).normalize();
    up.applyAxisAngle(fwd, Math.sin(time * 2.1) * 0.25);
    mTmp.makeBasis(new THREE.Vector3().crossVectors(up, fwd).normalize(), up, fwd);
    qTmp.setFromRotationMatrix(mTmp);
    if (k < 0.08) qTmp.slerp(f.startQ, 1 - k / 0.08);
    const land = smooth((k - 0.82) / 0.18);
    if (land > 0) qTmp.slerp(f.endQ, land);
    adult.root.quaternion.copy(qTmp);
    const flapRate = 11 - land * 6;
    st.wingT += dt * flapRate;
    const flap = 0.62 + Math.sin(st.wingT) * 0.72;
    adult.setWings(lerp(flap, 0.35, land * land));
    adult.setLegs(land);
    adult.setProboscis(0);
    rig.follow(p, 1.8, dt);
    if (k >= 1) {
      placeAdultPerch();
      st.flight = null;
      st.mode = 'adult';
      st.perchT = 0;
      setVisible('adult');
      if (f.onLand) f.onLand();
    }
  }

  function updatePerched(dt, time) {
    st.perchT += dt;
    const settle = smooth(st.perchT / 2.5);
    const bask = smooth((Math.sin(time * 0.42) - 0.15) / 0.7);
    const open = lerp(0.3, 0.03 + 0.92 * bask, settle);
    adult.setWings(open);
    const ext = smooth((st.perchT - 1.2) / 2.2);
    adult.setProboscis(ext, -1.42 + Math.sin(time * 1.3) * 0.08 * ext, lerp(1.45, 0.66, ext));
    adult.setLegs(1);
  }

  function updateEmerge(dt) {
    const s = st.seq; s.t += dt;
    const t = s.t;
    chry.setMature(1);
    chry.setEmpty(smooth((t - 0.8) / 1.6));
    const slide = easeInOut((t - 1.0) / 3.0);
    adult.root.position.set(0, lerp(-1.4, -2.95, slide), lerp(0.05, 0.3, slide));
    adult.root.scale.setScalar(lerp(0.55, 1, smooth((t - 1) / 4)));
    adult.setLegs(0.2, 1);
    const expand = smooth((t - 4.5) / 6);
    adult.setCrumple(1 - expand);
    adult.setWings(0.02 + (t > 11 ? 0.25 * Math.max(0, Math.sin((t - 11) * 2.2)) : 0), 0, 1.05 - expand * 0.25);
    if (st.cycle) onStatus({ day: 29 + clamp(t / 12) * 0.6 });
    if (t > 13.5) { st.seq = null; startFlight(() => { if (st.cycle) st.cycle.next(); }); }
  }

  function updateCaterpillar(dt, time) {
    cat.tickCrawl(dt);
    if (!cat.crawling) {
      st.chew += dt;
      st.nextCrawl -= dt;
      const hu = st.headU + 0.012;
      const hw = leafHalfWidth(hu) * L;
      const x0 = Math.max(0.2, hw - (0.42 + 0.6 * st.scale));
      const reach = clamp(hw - bites.depthAt(hu + 0.01) - x0 - 0.12 * st.scale, 0, 1.1 * st.scale + 0.2);
      const sweep = 0.5 + 0.5 * Math.sin(st.chew * 2.6);
      cat.setHead(reach / Math.max(0.3, st.scale) * (0.55 + 0.45 * sweep), 0.03 * Math.sin(st.chew * 9));
      if (st.chew > 0.32 * (0.6 + st.scale * 0.4)) {
        st.chew = 0;
        const u = hu + (0.02 + Math.random() * 0.012) * (0.6 + st.scale * 0.4);
        bites.bite(u, Math.min(0.5 + 1.8 * st.scale, bites.depthAt(u) + 0.07 + 0.08 * st.scale), side, 0.14 + 0.26 * st.scale);
      }
      if (st.nextCrawl < 0 && st.headU < 0.79) {
        cat.crawl.stride = 0.28 * Math.max(0.3, st.scale);
        cat.startCrawl((stride) => { st.headU += stride * 0.95 / L; });
        st.nextCrawl = 5 + Math.random() * 3;
      }
    } else {
      cat.setHead(0.15, 0);
    }
    cat.update(time, st.scale, catPath);
  }

  const CYCLE = [
    { id: 'egg', dur: 7, d0: 0, d1: 4 },
    { id: 'caterpillar', dur: 18, d0: 4, d1: 18 },
    { id: 'jhang', dur: 5, d0: 18, d1: 19 },
    { id: 'chrysalis', dur: 9, d0: 19, d1: 29 },
    { id: 'emerge', dur: Infinity, d0: 29, d1: 30 },
    { id: 'adult', dur: Infinity, d0: 30, d1: 30 },
  ];
  function cycleEnter(i) {
    const c = st.cycle; c.i = i; c.t = 0;
    const seg = CYCLE[i];
    if (seg.id === 'egg') enter('egg', { develop: 0 });
    else if (seg.id === 'caterpillar') enter('caterpillar', { scale: 0.12, headU: 0.6, seed: false });
    else if (seg.id === 'jhang') enter('jhang');
    else if (seg.id === 'chrysalis') enter('chrysalis', { mature: 0, seed: false, camera: false });
    else if (seg.id === 'emerge') enter('emerge');
    else if (seg.id === 'adult') { st.cycle = null; onStatus({ day: 30, done: true }); }
    if (st.cycle) onStatus({ stage: seg.id === 'jhang' ? 'caterpillar' : seg.id === 'emerge' ? 'chrysalis' : seg.id, day: seg.d0 });
  }
  function updateCycle(dt) {
    const c = st.cycle; c.t += dt;
    const seg = CYCLE[c.i];
    const k = clamp(c.t / seg.dur);
    if (Number.isFinite(seg.dur)) onStatus({ day: lerp(seg.d0, seg.d1, k), instar: seg.id === 'caterpillar' ? 1 + [6.2, 8.4, 10.8, 13.6].filter((d) => lerp(seg.d0, seg.d1, k) > d).length : 0 });
    if (seg.id === 'egg') {
      egg.setDevelop(smooth(k / 0.85));
      egg.setHatched(smooth((k - 0.88) / 0.12));
    } else if (seg.id === 'caterpillar') {
      const day = lerp(4, 18, k);
      const steps = [4, 6.2, 8.4, 10.8, 13.6, 18];
      let inst = 0; while (inst < 4 && day > steps[inst + 1]) inst++;
      const within = (day - steps[inst]) / (steps[inst + 1] - steps[inst]);
      const sizes = [0.12, 0.22, 0.38, 0.6, 0.82, 1.0];
      st.scale = lerp(sizes[inst], sizes[inst + 1], smooth(within * 1.4));
      st.headU = Math.min(st.headU, 0.62 + k * 0.17);
    } else if (seg.id === 'jhang') {
      const pupate = smooth((k - 0.55) / 0.4);
      st.scale = 1 - pupate * 0.999;
      chry.swing.scale.setScalar(Math.max(0.001, smooth((k - 0.6) / 0.4)));
    } else if (seg.id === 'chrysalis') {
      st.mature = smooth((k - 0.55) / 0.45);
      chry.setMature(st.mature);
    }
    if (c.t >= seg.dur) cycleEnter(c.i + 1);
  }

  return {
    get state() { return st; },
    bindRig(r) { rig = r; },
    shot,
    showStage(id) {
      st.cycle = null;
      if (id === 'adult') enter('adult', {});
      else enter(id, {});
    },
    overview() { rig.flyTo(shot('overview'), 2.2); },
    playCycle() {
      st.cycle = { i: 0, t: 0, next: () => { cycleEnter(CYCLE.length - 1); } };
      cycleEnter(0);
    },
    stopCycle() { st.cycle = null; },
    emerge() {
      st.cycle = null;
      if (st.mode !== 'chrysalis') enter('chrysalis', { camera: false });
      st.mature = 1; chry.setMature(1);
      enter('emerge');
    },
    takeFlight() {
      if (st.mode !== 'adult' || st.flight) return;
      st.cycle = null;
      startFlight(() => rig.flyTo(shot('adult'), 1.6));
    },
    update(dt, time) {
      if (st.cycle) updateCycle(dt);
      const mode = st.mode;
      if (mode === 'caterpillar') updateCaterpillar(dt, time);
      else if (mode === 'jhang') {
        cat.setHead(0, 0.04 * Math.sin(time * 1.5));
        cat.update(time, Math.max(0.001, st.scale), jPath);
      } else if (mode === 'emerge' && st.seq) updateEmerge(dt);
      else if (mode === 'flight' && st.flight) updateFlight(dt, time);
      else if (mode === 'adult') updatePerched(dt, time);
      if (mode === 'chrysalis' || mode === 'jhang' || mode === 'emerge' || mode === 'adult' || mode === 'flight') {
        chry.swing.rotation.z = Math.sin(time * 0.9) * 0.05;
        chry.swing.rotation.x = Math.sin(time * 0.7 + 1) * 0.035;
      }
      adult.tick(time);
    },
    hotspots() {
      return [
        { id: 'egg', visible: egg.group.visible, pos: () => worldOf(egg.group, new THREE.Vector3(0, 0.06, 0)), r: 0.3 },
        { id: 'caterpillar', visible: cat.group.visible, pos: () => cat.headPosition(new THREE.Vector3()).applyMatrix4(cat.group.matrixWorld), r: 2.2 },
        { id: 'chrysalis', visible: chry.group.visible, pos: () => worldOf(anchor, new THREE.Vector3(0, -1, 0)), r: 1.3 },
        { id: 'adult', visible: adult.root.visible, pos: () => worldOf(adult.root, new THREE.Vector3(0, 0, 0.3)), r: 2.2 },
        { id: 'flower', visible: true, pos: () => worldOf(plant.perch.group, plant.perch.position), r: 3.5 },
        { id: 'leaf', visible: true, pos: () => worldOf(heroCat.holder, catSurf.surf(0.5, -0.3)), r: 4.5 },
      ];
    },
    dispose() { bites.texture.dispose(); },
  };
}
