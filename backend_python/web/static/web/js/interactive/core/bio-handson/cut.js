// Cutting along a guide. A dashed guide line marches along the surface where the cut should
// go; as the blade travels it the incision opens behind the tip: a dark wet line with paler
// lips. Only a cut that follows the line advances; straying off it is reported to the step.
import { THREE } from '../engine.js';
import { canvasTexture } from './kit.js';

function dashTexture() {
  return canvasTexture('bh-dash', 64, 16, (g) => {
    g.clearRect(0, 0, 64, 16);
    g.fillStyle = 'rgba(255,255,255,1)'; g.fillRect(4, 3, 30, 10);
  }, { wrapS: true });
}

function ribbon(samples, normals, width, withColor) {
  const n = samples.length;
  const pos = new Float32Array(n * 2 * 3); const uv = new Float32Array(n * 2 * 2);
  const col = withColor ? new Float32Array(n * 2 * 3) : null;
  const side = new THREE.Vector3(); const tan = new THREE.Vector3();
  let len = 0;
  for (let i = 0; i < n; i++) {
    const a = samples[Math.max(0, i - 1)]; const b = samples[Math.min(n - 1, i + 1)];
    tan.subVectors(b, a).normalize();
    side.crossVectors(normals[i], tan).normalize().multiplyScalar(width / 2);
    const p = samples[i];
    pos.set([p.x + side.x, p.y + side.y, p.z + side.z, p.x - side.x, p.y - side.y, p.z - side.z], i * 6);
    if (i > 0) len += samples[i].distanceTo(samples[i - 1]);
    uv.set([len, 0, len, 1], i * 4);
  }
  const idx = [];
  for (let i = 0; i < n - 1; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  g.setIndex(idx);
  g.computeVertexNormals();
  return { geometry: g, length: len, col };
}

/**
 * points: Vector3 (parent-local) on the surface, start to end. opts.normal(i, p, out) gives the
 * surface normal (default up). Returns an object with feed(localPoint) and progress.
 */
export function createCut(parent, points, opts = {}) {
  const curve = new THREE.CatmullRomCurve3(points, false, 'centripetal');
  const M = opts.samples || 160;
  const samples = curve.getSpacedPoints(M - 1);
  const normals = samples.map((p, i) => { const nn = new THREE.Vector3(0, 1, 0); if (opts.normal) opts.normal(i / (M - 1), p, nn); return nn; });
  const lifted = samples.map((p, i) => p.clone().addScaledVector(normals[i], opts.lift ?? 0.003));
  const width = opts.width || 0.012;

  const gR = ribbon(lifted, normals, width * 0.9, false);
  const tex = dashTexture().clone(); tex.needsUpdate = true; tex.wrapS = THREE.RepeatWrapping;
  tex.repeat.set(1 / (width * 4), 1);
  const guideMat = new THREE.MeshBasicMaterial({ map: tex, color: opts.guideColor ?? 0x22d3ee, transparent: true, opacity: 0.95, depthWrite: false, toneMapped: false, polygonOffset: true, polygonOffsetFactor: -2 });
  const guide = new THREE.Mesh(gR.geometry, guideMat); guide.renderOrder = 5; guide.userData.noPick = true;
  parent.add(guide);

  const lipLift = lifted.map((p, i) => p.clone().addScaledVector(normals[i], 0.0008));
  const lips = ribbon(lipLift, normals, width * 1.25, false);
  const lipMat = new THREE.MeshStandardMaterial({ color: opts.lipColor ?? 0xf0a3a3, roughness: 0.4, polygonOffset: true, polygonOffsetFactor: -3 });
  const lipMesh = new THREE.Mesh(lips.geometry, lipMat); lipMesh.userData.noPick = true; lipMesh.renderOrder = 4;
  const coreLift = lifted.map((p, i) => p.clone().addScaledVector(normals[i], 0.0016));
  const core = ribbon(coreLift, normals, width * 0.55, false);
  const coreMat = new THREE.MeshStandardMaterial({ color: opts.cutColor ?? 0x5b0f16, roughness: 0.25, polygonOffset: true, polygonOffsetFactor: -4 });
  const coreMesh = new THREE.Mesh(core.geometry, coreMat); coreMesh.userData.noPick = true; coreMesh.renderOrder = 5;
  parent.add(lipMesh, coreMesh);
  lips.geometry.setDrawRange(0, 0); core.geometry.setDrawRange(0, 0);

  let k = 0; // samples cut so far
  const tmp = new THREE.Vector3(); const scr = new THREE.Vector3();
  const api = {
    curve, samples, normals,
    length: gR.length,
    get progress() { return k / (M - 1); },
    get done() { return k >= M - 1; },
    /** The surface point where the next stretch of cut begins. */
    head(out) { return out.copy(samples[Math.min(M - 1, k)]); },
    /**
     * Feeds a blade position (parent-local). Returns 0 = near the path and cutting forward,
     * 1 = on the path but somewhere other than the cut's head, 2 = off the path.
     */
    feed(p, tolerance = width * 2.5, reach = 14) {
      let best = Infinity; let bi = -1;
      const lo = Math.max(0, k - 4); const hi = Math.min(M - 1, k + reach);
      for (let i = lo; i <= hi; i++) { const d = tmp.subVectors(samples[i], p).lengthSq(); if (d < best) { best = d; bi = i; } }
      const d = Math.sqrt(best);
      if (d <= tolerance) {
        if (bi > k) { k = bi; const n = (k) * 6; lips.geometry.setDrawRange(0, n); core.geometry.setDrawRange(0, n); }
        return 0;
      }
      // is the blade on the guide but far from the head (jumping ahead, or starting at the wrong end)?
      for (let i = 0; i < M; i += 3) if (tmp.subVectors(samples[i], p).length() < tolerance) return 1;
      return 2;
    },
    /**
     * Screen-space version of feed: (px, py) is the pointer in stage pixels and project(v, out)
     * maps a world point to stage pixels. Tolerant of a finger that slips off a thin specimen.
     * Writes the nearest guide point (world) to outWorld.
     */
    feedScreen(px, py, project, tolPx = 24, reach = 16, outWorld = null) {
      parent.updateWorldMatrix(true, false);
      let best = Infinity; let bi = -1; let anyNear = false;
      for (let i = 0; i < M; i++) {
        tmp.copy(samples[i]); parent.localToWorld(tmp); project(tmp, scr);
        const d = (scr.x - px) * (scr.x - px) + (scr.y - py) * (scr.y - py);
        if (i >= k - 4 && i <= k + reach && d < best) { best = d; bi = i; }
        if (d < tolPx * tolPx) anyNear = true;
      }
      const d = Math.sqrt(best);
      if (outWorld && bi >= 0) { outWorld.copy(samples[bi]); parent.localToWorld(outWorld); }
      if (d <= tolPx) {
        if (bi > k) { k = bi; const n = k * 6; lips.geometry.setDrawRange(0, n); core.geometry.setDrawRange(0, n); }
        return 0;
      }
      return anyNear ? 1 : 2;
    },
    /** Nearest guide sample to the pointer over the whole path: returns pixel distance, writes the local point. */
    nearestScreen(px, py, project, outLocal) {
      parent.updateWorldMatrix(true, false);
      let best = Infinity; let bi = 0;
      for (let i = 0; i < M; i++) { tmp.copy(samples[i]); parent.localToWorld(tmp); project(tmp, scr); const d = Math.hypot(scr.x - px, scr.y - py); if (d < best) { best = d; bi = i; } }
      if (outLocal) outLocal.copy(samples[bi]);
      return best;
    },
    /** Pixel distance from (px, py) to the guide, for deciding whether a press starts a cut. */
    screenDistance(px, py, project) {
      parent.updateWorldMatrix(true, false);
      let best = Infinity;
      for (let i = 0; i < M; i += 2) { tmp.copy(samples[i]); parent.localToWorld(tmp); project(tmp, scr); best = Math.min(best, Math.hypot(scr.x - px, scr.y - py)); }
      return best;
    },
    finish() { k = M - 1; const n = k * 6; lips.geometry.setDrawRange(0, n); core.geometry.setDrawRange(0, n); guide.visible = false; },
    showGuide(v) { guide.visible = v; },
    update(dt) { tex.offset.x -= dt * 0.8; guideMat.opacity = 0.75 + 0.2 * Math.sin(performance.now() * 0.006); },
    /** Widens the opened incision (0..1), e.g. as flaps are drawn back. */
    gape(v) { lipMesh.scale.setScalar(1); lipMat.color.setHex(opts.lipColor ?? 0xf0a3a3); lipMesh.visible = v < 0.98; coreMesh.visible = v < 0.98; },
    dispose() { [guide, lipMesh, coreMesh].forEach((m) => { parent.remove(m); m.geometry.dispose(); m.material.dispose(); }); tex.dispose(); },
  };
  return api;
}
