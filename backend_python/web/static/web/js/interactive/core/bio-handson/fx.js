// Small effects shared by every practical: a pooled burst of droplets (coelomic fluid, stain,
// water), a ring pulse that marks where to act, and a hover highlight that warms an object's
// emissive glow instead of swapping its material.
import { THREE } from '../engine.js';
import { canvasTexture } from './kit.js';

function dotTexture() {
  return canvasTexture('bh-dot', 64, 64, (g) => {
    const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.45, 'rgba(255,255,255,0.85)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  });
}
function ringTexture() {
  return canvasTexture('bh-ring', 128, 128, (g) => {
    g.strokeStyle = 'rgba(255,255,255,1)'; g.lineWidth = 9; g.beginPath(); g.arc(64, 64, 52, 0, Math.PI * 2); g.stroke();
    g.globalAlpha = 0.35; g.fillStyle = '#fff'; g.beginPath(); g.arc(64, 64, 46, 0, Math.PI * 2); g.fill();
  });
}

export function createFx(scene) {
  const N = 160;
  const geo = new THREE.BufferGeometry();
  const posA = new Float32Array(N * 3); const colA = new Float32Array(N * 3);
  geo.setAttribute('position', new THREE.BufferAttribute(posA, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colA, 3));
  const vel = new Float32Array(N * 3); const life = new Float32Array(N); const floor = new Float32Array(N);
  const mat = new THREE.PointsMaterial({ size: 0.018, map: dotTexture(), vertexColors: true, transparent: true, depthWrite: false, sizeAttenuation: true });
  const points = new THREE.Points(geo, mat);
  points.frustumCulled = false; points.renderOrder = 6;
  scene.add(points);
  for (let i = 0; i < N; i++) posA[i * 3 + 1] = -100;
  let head = 0; let alive = 0;
  const c = new THREE.Color();

  const ringMat = new THREE.MeshBasicMaterial({ map: ringTexture(), transparent: true, depthWrite: false, color: 0x22c55e, toneMapped: false });
  const markers = [];

  const hl = { obj: null, mats: [], k: 0 };
  function matsOf(o) { const out = []; o.traverse((n) => { if (n.isMesh && n.material && n.material.emissive) out.push(n.material); }); return out; }

  return {
    burst(at, color, n = 10, speed = 0.25, floorY = at.y) {
      c.set(color);
      for (let k = 0; k < n; k++) {
        const i = head; head = (head + 1) % N;
        posA[i * 3] = at.x; posA[i * 3 + 1] = at.y; posA[i * 3 + 2] = at.z;
        const a = Math.random() * Math.PI * 2; const s = speed * (0.4 + Math.random() * 0.8);
        vel[i * 3] = Math.cos(a) * s * 0.6; vel[i * 3 + 1] = s * (0.6 + Math.random()); vel[i * 3 + 2] = Math.sin(a) * s * 0.6;
        colA[i * 3] = c.r; colA[i * 3 + 1] = c.g; colA[i * 3 + 2] = c.b;
        life[i] = 0.5 + Math.random() * 0.5; floor[i] = floorY;
      }
      alive = 1.2;
    },
    /** A pulsing target ring lying on a surface. Returns the mesh; remove with unmark. */
    mark(at, radius = 0.05, color = 0x22c55e) {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(radius * 2, radius * 2), ringMat.clone());
      m.material.color.set(color);
      m.rotation.x = -Math.PI / 2; m.position.copy(at); m.position.y += 0.002; m.renderOrder = 7;
      m.userData.noPick = false; m.userData.marker = true; m.userData.phase = Math.random() * 6;
      scene.add(m); markers.push(m);
      return m;
    },
    get marks() { return markers; },
    unmark(m) { const i = markers.indexOf(m); if (i >= 0) markers.splice(i, 1); scene.remove(m); m.geometry.dispose(); m.material.dispose(); },
    clearMarks() { while (markers.length) this.unmark(markers[0]); },
    highlight(obj) {
      if (hl.obj === obj) return;
      hl.mats.forEach((m) => { m.emissive.setRGB(0, 0, 0); });
      hl.obj = obj; hl.mats = obj ? matsOf(obj) : []; hl.k = 0;
    },
    update(dt, t) {
      for (let i = 0; i < markers.length; i++) {
        const m = markers[i]; const p = 0.5 + 0.5 * Math.sin(t * 4 + m.userData.phase);
        m.scale.setScalar(0.85 + p * 0.3); m.material.opacity = 0.55 + 0.45 * p;
      }
      if (hl.obj) {
        hl.k = Math.min(1, hl.k + dt * 6);
        const v = (0.10 + 0.06 * Math.sin(t * 6)) * hl.k;
        for (let i = 0; i < hl.mats.length; i++) hl.mats[i].emissive.setRGB(v * 0.9, v * 0.75, v * 0.3);
      }
      if (alive <= 0) return;
      alive -= dt;
      for (let i = 0; i < N; i++) {
        if (life[i] <= 0) continue;
        life[i] -= dt;
        vel[i * 3 + 1] -= 2.2 * dt;
        posA[i * 3] += vel[i * 3] * dt; posA[i * 3 + 1] += vel[i * 3 + 1] * dt; posA[i * 3 + 2] += vel[i * 3 + 2] * dt;
        if (posA[i * 3 + 1] < floor[i]) { posA[i * 3 + 1] = floor[i]; vel[i * 3] *= 0.3; vel[i * 3 + 2] *= 0.3; vel[i * 3 + 1] = 0; }
        if (life[i] <= 0) posA[i * 3 + 1] = -100;
      }
      geo.attributes.position.needsUpdate = true; geo.attributes.color.needsUpdate = true;
    },
    dispose() { scene.remove(points); geo.dispose(); mat.dispose(); this.clearMarks(); ringMat.dispose(); },
  };
}
